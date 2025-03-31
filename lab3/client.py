import requests
import json


def add_transaction(sender, receiver, amount):
    url = "http://localhost:5000/add_transaction"
    password = input(f"Enter {sender} password: ")
    data = {
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "password": password,
    }
    response = requests.post(url, json=data)
    print(response.json())


def mine_block(sender):
    url = "http://localhost:5000/mine_block"
    password = input(f"Enter {sender} password: ")
    data = {"sender": sender, "password": password}
    
    # First get the current pending transactions to show what's going to be mined
    pending_tx = requests.get("http://localhost:5000/get_pending_transactions").json()
    if 'pending_transactions' in pending_tx and len(pending_tx['pending_transactions']) > 0:
        print(f"\nMining block with {len(pending_tx['pending_transactions'])} pending transactions:")
        for i, tx in enumerate(pending_tx['pending_transactions'], 1):
            print(f"  Transaction {i}: {tx['sender']} -> {tx['receiver']}: {tx['amount']}")
    else:
        print("\nMining new block (only mining reward transaction will be included)")
    
    print("\nMining in progress... This may take a moment.")
    response = requests.post(url, json=data)
    result = response.json()
    
    print(f"\nSuccess! Block #{result['index']} has been mined.")
    print(f"Total transactions in block: {result.get('transactions_count', len(result['transactions']))}")
    print(f"Mining reward: 1 coin for {sender}")
    
    if 'transactions' in result and len(result['transactions']) > 1:
        print("\nTransactions included in this block:")
        for i, tx in enumerate(result['transactions'], 1):
            if tx['sender'] == '0':
                print(f"  Transaction {i}: Mining reward to {tx['receiver']}: {tx['amount']}")
            else:
                print(f"  Transaction {i}: {tx['sender']} -> {tx['receiver']}: {tx['amount']}")
    
    print(f"Proof of work: {result['proof']}")
    print(f"Previous hash: {result['previous_hash']}")


def get_chain():
    url = "http://localhost:5000/get_chain"
    response = requests.get(url)
    print(response.json())


def is_chain_valid():
    url = "http://localhost:5000/is_valid"
    response = requests.get(url)
    print(response.text)


def check_balance(role):
    url = "http://localhost:5000/get_balance"
    password = input(f"Enter {role} password: ")
    data = {"role": role, "password": password}
    response = requests.post(url, json=data)
    print(response.json())


def get_pending_transactions():
    url = "http://localhost:5000/get_pending_transactions"
    response = requests.get(url)
    data = response.json()
    
    if 'pending_transactions' in data and len(data['pending_transactions']) > 0:
        print("\nPending Transactions:")
        print(f"Total count: {data['transaction_count']}")
        
        for i, tx in enumerate(data['pending_transactions'], 1):
            print(f"\nTransaction {i}:")
            print(f"  From: {tx['sender']}")
            print(f"  To: {tx['receiver']}")
            print(f"  Amount: {tx['amount']}")
            
            if 'waiting_time' in tx:
                print(f"  Waiting for: {tx['waiting_time']} seconds")
            
            if 'transaction_id' in tx:
                print(f"  ID: {tx['transaction_id'][:8]}...")
    else:
        print("\nNo pending transactions found.")


if __name__ == "__main__":
    while True:
        print("\nBlockchain Client Menu:")
        print("1. Select role")
        print("2. View Blockchain")
        print("3. Check Blockchain Validity")
        print("4. View Pending Transactions")
        print("5. Exit")
        choice = int(input("Enter choice: "))

        if choice == 1:
            while True:
                print("\nBlockchain Role Menu:")
                print("1. Doctor")
                print("2. Diagnosis lab")
                print("3. Pharmacy")
                print("4. Back to Client Menu")
                role = input("Enter role: ")
                if role == "1":
                    print("\nDoctor's Menu:")
                    print("1. Add transaction")
                    print("2. Mine Block")
                    print("3. Check Balance")
                    print("4. Back to Client Menu")
                    to_do = input("Enter option: ")
                    if to_do == "1":
                        receiver = input("Enter receiver address: ")
                        amount = float(input("Enter amount: "))
                        add_transaction("Doctor", receiver, amount)
                    elif to_do == "2":
                        mine_block("Doctor")
                    elif to_do == "3":
                        check_balance("Doctor")
                    elif to_do == "4":
                        break
                elif role == "2":
                    print("\nDiagnosis lab's Menu:")
                    print("1. Add transaction")
                    print("2. Mine Block")
                    print("3. Check Balance")
                    print("4. Back to Client Menu")
                    to_do = input("Enter option: ")
                    if to_do == "1":
                        receiver = input("Enter receiver address: ")
                        amount = float(input("Enter amount: "))
                        add_transaction("Diagnosis lab", receiver, amount)
                    elif to_do == "2":
                        mine_block("Diagnosis lab")
                    elif to_do == "3":
                        check_balance("Diagnosis lab")
                    elif to_do == "4":
                        break
                elif role == "3":
                    print("\nPharmacy's Menu:")
                    print("1. Add transaction")
                    print("2. Mine Block")
                    print("3. Check Balance")
                    print("4. Back to Client Menu")
                    to_do = input("Enter option: ")
                    if to_do == "1":
                        receiver = input("Enter receiver address: ")
                        amount = float(input("Enter amount: "))
                        add_transaction("Pharmacy", receiver, amount)
                    elif to_do == "2":
                        mine_block("Pharmacy")
                    elif to_do == "3":
                        check_balance("Pharmacy")
                    elif to_do == "4":
                        break
                elif role == "4":
                    break
                else:
                    print("Invalid choice, please try again.")
        elif choice == 2:
            get_chain()
        elif choice == 3:
            is_chain_valid()
        elif choice == 4:
            get_pending_transactions()
        elif choice == 5:
            break
        else:
            print("Invalid choice, please try again.")
