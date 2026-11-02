from storage import load_data, save_data
from customers import register_customer
from accounts import create_account
from transactions import deposit, withdraw, transfer
from exceptions import BankingError, DataPersistenceError


def main():

    try:
        customers, accounts, transactions = load_data()
    except DataPersistenceError as e:
        print("Could not load data:", e)
        return

    while True:

        print("\n===== BANKING SYSTEM =====")
        print("1. Register customer")
        print("2. Create account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Transfer")
        print("6. Save and exit")

        choice = input("Choose an option: ")

        try:

            if choice == "1":
                name = input("Name: ")
                email = input("Email: ")
                contact = input("Contact: ")

                customer_id = register_customer(customers, name, email, contact)
                print("Customer registered:", customer_id)

            elif choice == "2":
                customer_id = input("Customer ID: ")
                currency = input("Currency: ")

                account_id = create_account(accounts, customers, customer_id, currency)
                print("Account created:", account_id)

            elif choice == "3":
                account_id = input("Account ID: ")
                amount = int(input("Amount: "))

                transaction_id = deposit(accounts, transactions, account_id, amount)
                print("Deposit successful:", transaction_id)

            elif choice == "4":
                account_id = input("Account ID: ")
                amount = int(input("Amount: "))

                transaction_id = withdraw(accounts, transactions, account_id, amount)
                print("Withdrawal successful:", transaction_id)

            elif choice == "5":
                sender_id = input("Sender account ID: ")
                receiver_id = input("Receiver account ID: ")
                amount = int(input("Amount: "))

                transfer_id = transfer(
                    accounts, transactions, sender_id, receiver_id, amount
                )
                print("Transfer successful:", transfer_id)

            elif choice == "6":
                save_data(customers, accounts, transactions)
                print("Data saved successfully. Goodbye!")
                break

            else:
                print("Invalid menu choice. Choose 1-6.")

        except ValueError:
            print("Invalid input. Please enter a whole number.")

        except BankingError as e:
            print("Banking error:", e)

        except DataPersistenceError as e:
            print("Storage error:", e)


if __name__ == "__main__":
    main()
