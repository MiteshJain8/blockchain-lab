import hashlib
import time
import json
from flask import Flask, request, jsonify

app = Flask(__name__)


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.transaction_ids = set()  # To track transaction IDs and prevent duplicates
        self.create_block(previous_hash="1", proof=100)
        self.balances = {"Doctor": 100, "Diagnosis lab": 100, "Pharmacy": 100}

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "transactions": self.pending_transactions,
            "proof": proof,
            "previous_hash": previous_hash,
        }
        # Save transaction IDs before clearing pending transactions
        for transaction in self.pending_transactions:
            if "transaction_id" in transaction:
                self.transaction_ids.add(transaction["transaction_id"])
        
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()
            ).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_transaction(self, sender, receiver, amount):
        # Create a unique transaction ID using a hash of the transaction details and timestamp
        transaction_time = time.time()
        transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": transaction_time,
            "transaction_id": hashlib.sha256(f"{sender}{receiver}{amount}{transaction_time}".encode()).hexdigest()
        }
        
        # Check if this is a duplicate transaction
        if transaction["transaction_id"] in self.transaction_ids:
            return -1  # Indicate duplicate transaction
        
        self.transaction_ids.add(transaction["transaction_id"])
        self.pending_transactions.append(transaction)
        return self.get_previous_block()["index"] + 1

    def get_pending_transactions(self):
        return self.pending_transactions

    def clear_pending_transactions(self):
        self.pending_transactions = []

    def update_balances(self, sender, receiver, amount):
        if sender != "0":  # Not a mining reward
            self.balances[sender] -= amount
        self.balances[receiver] += amount
        return True


blockchain = Blockchain()
passwords = {"Doctor": "doc", "Diagnosis lab": "lab", "Pharmacy": "med"}


@app.route("/mine_block", methods=["POST"])
def mine_block():
    data = request.get_json()
    if not "password" in data or not "sender" in data:
        return "Missing data", 400
    if data["password"] != passwords[data["sender"]]:
        return "Password invalid", 404
    
    # Check if there are pending transactions to mine
    pending_tx_count = len(blockchain.pending_transactions)
    
    # Add mining reward transaction
    blockchain.add_transaction(sender="0", receiver=data["sender"], amount=1)
    blockchain.update_balances(sender="0", receiver=data["sender"], amount=1)
    
    # Mine the block
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    
    # Create the new block with all pending transactions
    block = blockchain.create_block(proof, previous_hash)
    
    response = {
        "message": "New block mined!",
        "index": block["index"],
        "transactions": block["transactions"],
        "transactions_count": len(block["transactions"]),
        "pending_transactions_mined": pending_tx_count,
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }
    return jsonify(response), 200


@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    data = request.get_json()
    required_fields = ["sender", "receiver", "amount", "password"]
    if not all(field in data for field in required_fields):
        return "Missing data", 400
    if data["password"] != passwords[data["sender"]]:
        return "Password invalid", 404

    if blockchain.balances[data["sender"]] < data["amount"]:
        return jsonify({"message": "Insufficient balance"}), 400

    blockchain.update_balances(data["sender"], data["receiver"], data["amount"])

    index = blockchain.add_transaction(data["sender"], data["receiver"], data["amount"])
    if index == -1:
        return jsonify({"message": "Duplicate transaction"}), 400

    response = {"message": f"Transaction will be added to Block {index}"}
    return jsonify(response), 201


@app.route("/get_balance", methods=["POST"])
def get_balance():
    data = request.get_json()
    if not "role" in data or not "password" in data:
        return "Missing data", 400
    if data["password"] != passwords[data["role"]]:
        return "Password invalid", 404

    balance = blockchain.balances[data["role"]]
    response = {"role": data["role"], "balance": balance}
    return jsonify(response), 200


@app.route("/get_chain", methods=["GET"])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        block_data = {
            "index": block["index"],
            "timestamp": block["timestamp"],
            "proof": block["proof"],
            "previous_hash": block["previous_hash"],
            "transactions": block["transactions"]
        }
        chain_data.append(block_data)
    
    response = {
        "chain": chain_data,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route("/is_valid", methods=["GET"])
def is_valid():
    chain = blockchain.chain
    previous_block = chain[0]
    block_index = 1
    while block_index < len(chain):
        block = chain[block_index]
        if block["previous_hash"] != blockchain.hash(previous_block):
            return "Chain is invalid", 400
        previous_proof = previous_block["proof"]
        proof = block["proof"]
        hash_operation = hashlib.sha256(
            str(proof**2 - previous_proof**2).encode()
        ).hexdigest()
        if hash_operation[:4] != "0000":
            return "Chain is invalid", 400
        previous_block = block
        block_index += 1
    return "Chain is valid", 200


@app.route('/get_pending_transactions', methods=['GET'])
def get_pending_transactions():
    transactions = blockchain.get_pending_transactions()
    
    # Add additional information about each transaction
    for transaction in transactions:
        # Add waiting time information
        if "timestamp" in transaction:
            transaction["waiting_time"] = round(time.time() - transaction["timestamp"], 2)
        
        # You could add more details like estimated block to be included
        # This is just an example with waiting time
    
    response = {
        'message': 'Pending transactions',
        'pending_transactions': transactions,
        'transaction_count': len(transactions),
        'mining_in_progress': False  # You could add a flag if mining is in progress
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
