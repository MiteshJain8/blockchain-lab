import requests

def add_transaction(sender, receiver, amount):
    url = 'http://localhost:5000/add_transaction'
    data = {
        'sender': sender,
        'receiver': receiver,
        'amount': amount
    }
    response = requests.post(url, json=data)
    print(response.json())

def mine_block():
    url = 'http://localhost:5000/mine_block'
    response = requests.get(url)
    print(response.json())

def get_chain():
    url = 'http://localhost:5000/get_chain'
    response = requests.get(url)
    print(response.json())

if __name__ == '__main__':
    while True:
        print("\nBlockchain Client Menu:")
        print("1. Add Transaction")
        print("2. Mine Block")
        print("3. View Blockchain")
        print("4. Exit")
        choice = int(input("Enter choice: "))

        if choice == 1:
            sender = input("Enter sender address: ")
            receiver = input("Enter receiver address: ")
            amount = float(input("Enter amount: "))
            add_transaction(sender, receiver, amount)
        elif choice == 2:
            mine_block()
        elif choice == 3:
            get_chain()
        elif choice == 4:
            break
        else:
            print("Invalid choice, please try again.")
