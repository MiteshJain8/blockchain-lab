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
    response = requests.post(url, json=data)
    print(response.json())


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


if __name__ == "__main__":
    while True:
        print("\nBlockchain Client Menu:")
        print("1. Select role")
        print("2. View Blockchain")
        print("3. Check Blockchain Validity")
        print("4. Exit")
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
            break
        else:
            print("Invalid choice, please try again.")
