import requests

def add_transaction(sender, receiver, amount, encryption_mode='cbc'):
    url = 'http://localhost:5000/add_transaction'
    data = {
        'sender': sender,
        'receiver': receiver,
        'amount': amount,
        'encryption_mode': encryption_mode
    }
    response = requests.post(url, json=data)
    print(response.json())

def mine_block():
    url = 'http://localhost:5000/mine_block'
    response = requests.get(url)
    print(response.json())

def get_chain(decrypted=False):
    if decrypted:
        url = 'http://localhost:5000/get_decrypted_chain'
    else:
        url = 'http://localhost:5000/get_chain'
    response = requests.get(url)
    print(response.json())

if __name__ == '__main__':
    while True:
        print("\nBlockchain Client Menu:")
        print("1. Add Transaction")
        print("2. Mine Block")
        print("3. View Encrypted Blockchain")
        print("4. View Decrypted Blockchain")
        print("5. Exit")
        choice = int(input("Enter choice: "))

        if choice == 1:
            sender = input("Enter sender address: ")
            receiver = input("Enter receiver address: ")
            amount = float(input("Enter amount: "))
            print("Encryption modes: cbc, ctr, none")
            mode = input("Enter encryption mode (default: cbc): ") or "cbc"
            add_transaction(sender, receiver, amount, mode)
        elif choice == 2:
            mine_block()
        elif choice == 3:
            get_chain(False)
        elif choice == 4:
            get_chain(True)
        elif choice == 5:
            break
        else:
            print("Invalid choice, please try again.")
