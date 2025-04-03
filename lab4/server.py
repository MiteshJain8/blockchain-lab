import hashlib
import time
import json
import os
import base64
from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)

# Encryption keys and utils
CBC_KEY = os.urandom(16)  # 128-bit key for AES
CTR_KEY = os.urandom(16)
CBC_IV = os.urandom(16)   # Initialization Vector for CBC mode

def encrypt_cbc(data):
    json_data = json.dumps(data).encode('utf-8')
    cipher = AES.new(CBC_KEY, AES.MODE_CBC, CBC_IV)
    ct_bytes = cipher.encrypt(pad(json_data, AES.block_size))
    return {
        'ciphertext': base64.b64encode(ct_bytes).decode('utf-8'),
        'iv': base64.b64encode(cipher.iv).decode('utf-8')
    }

def decrypt_cbc(encrypted_data):
    iv = base64.b64decode(encrypted_data['iv'])
    ct = base64.b64decode(encrypted_data['ciphertext'])
    cipher = AES.new(CBC_KEY, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return json.loads(pt.decode('utf-8'))

def encrypt_ctr(data):
    json_data = json.dumps(data).encode('utf-8')
    cipher = AES.new(CTR_KEY, AES.MODE_CTR)
    ct_bytes = cipher.encrypt(json_data)
    return {
        'ciphertext': base64.b64encode(ct_bytes).decode('utf-8'),
        'nonce': base64.b64encode(cipher.nonce).decode('utf-8')
    }

def decrypt_ctr(encrypted_data):
    nonce = base64.b64decode(encrypted_data['nonce'])
    ct = base64.b64decode(encrypted_data['ciphertext'])
    cipher = AES.new(CTR_KEY, AES.MODE_CTR, nonce=nonce)
    pt = cipher.decrypt(ct)
    return json.loads(pt.decode('utf-8'))

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_block(previous_hash='1', proof=100)

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_transaction(self, sender, receiver, amount, encryption_mode='cbc'):
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }
        
        # Encrypt transaction data based on specified mode
        if encryption_mode == 'cbc':
            encrypted_transaction = encrypt_cbc(transaction)
            encrypted_transaction['mode'] = 'cbc'
        elif encryption_mode == 'ctr':
            encrypted_transaction = encrypt_ctr(transaction)
            encrypted_transaction['mode'] = 'ctr'
        else:
            # No encryption (for backward compatibility)
            self.pending_transactions.append(transaction)
            return self.get_previous_block()['index'] + 1
        
        self.pending_transactions.append(encrypted_transaction)
        return self.get_previous_block()['index'] + 1
    
    def get_decrypted_transactions(self, block):
        decrypted_transactions = []
        for tx in block['transactions']:
            if isinstance(tx, dict) and 'mode' in tx:
                if tx['mode'] == 'cbc':
                    decrypted_transactions.append(decrypt_cbc(tx))
                elif tx['mode'] == 'ctr':
                    decrypted_transactions.append(decrypt_ctr(tx))
            else:
                # Plain transaction
                decrypted_transactions.append(tx)
        return decrypted_transactions

blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender="0", receiver="miner_address", amount=1)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'New block mined!',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    required_fields = ['sender', 'receiver', 'amount']
    if not all(field in data for field in required_fields):
        return 'Missing data', 400
    
    # Use encryption mode if specified, default to CBC
    encryption_mode = data.get('encryption_mode', 'cbc')
    if encryption_mode not in ['cbc', 'ctr', 'none']:
        return 'Invalid encryption mode', 400
    
    if encryption_mode == 'none':
        index = blockchain.add_transaction(data['sender'], data['receiver'], data['amount'])
    else:
        index = blockchain.add_transaction(data['sender'], data['receiver'], data['amount'], encryption_mode)
    
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/get_decrypted_chain', methods=['GET'])
def get_decrypted_chain():
    decrypted_chain = []
    for block in blockchain.chain:
        decrypted_block = block.copy()
        decrypted_block['transactions'] = blockchain.get_decrypted_transactions(block)
        decrypted_chain.append(decrypted_block)
    
    response = {
        'chain': decrypted_chain,
        'length': len(decrypted_chain)
    }
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    chain = blockchain.chain
    previous_block = chain[0]
    block_index = 1
    while block_index < len(chain):
        block = chain[block_index]
        if block['previous_hash'] != blockchain.hash(previous_block):
            return 'Chain is invalid', 400
        previous_proof = previous_block['proof']
        proof = block['proof']
        hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
        if hash_operation[:4] != '0000':
            return 'Chain is invalid', 400
        previous_block = block
        block_index += 1
    return 'Chain is valid', 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
