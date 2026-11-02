from storage import load_data, save_data
from customers import register_customer, search_customer
from accounts import (
    create_account,
    close_account,
    freeze_account,
    unfreeze_account,
)
from transactions import deposit, withdraw, transfer
from reports import (
    generate_account_statement,
    generate_customer_report,
    generate_daily_transaction_report,
    generate_bank_summary,
)
from exceptions import BankingError, DataPersistenceError

MENU = """
===== BANKING SYSTEM =====
1. Register customer
2. Create account
3. Deposit
4. Withdraw
5. Transfer
6. Manage account status (freeze / unfreeze / close)
7. Find customer by email
8. Reports
9. Save and exit"""

REPORTS_MENU = """
--- Reports ---
1. Account statement
2. Customer report
3. Daily transaction report
4. Bank summary
5. Back"""

STATUS_MENU = """
--- Account status ---
1. Freeze
2. Unfreeze
3. Close
4. Back"""


def reports_menu(customers, accounts, transactions):
    print(REPORTS_MENU)
    choice = input("Choose a report: ").strip()

    if choice == "1":
        account_id = input("Account ID: ").strip()
        print(generate_account_statement(accounts, transactions, account_id))
    elif choice == "2":
        customer_id = input("Customer ID: ").strip()
        print(generate_customer_report(customers, accounts, customer_id))
    elif choice == "3":
        date = input("Date (YYYY-MM-DD): ").strip()
        print(generate_daily_transaction_report(transactions, date))
    elif choice == "4":
        print(generate_bank_summary(customers, accounts, transactions))
    elif choice != "5":
        print("Invalid choice.")


def status_menu(accounts):
    print(STATUS_MENU)
    choice = input("Choose an action: ").strip()

    if choice not in ("1", "2", "3"):
        if choice != "4":
            print("Invalid choice.")
        return

    account_id = input("Account ID: ").strip()
    actions = {"1": freeze_account, "2": unfreeze_account, "3": close_account}
    print(actions[choice](accounts, account_id))


def main():

    try:
        customers, accounts, transactions = load_data()
    except DataPersistenceError as e:
        print("Could not load data:", e)
        return

    while True:

        print(MENU)

        choice = input("Choose an option: ").strip()

        try:

            if choice == "1":
                name = input("Name: ")
                email = input("Email: ")
                contact = input("Contact: ")

                customer_id = register_customer(customers, name, email, contact)
                print("Customer registered:", customer_id)

            elif choice == "2":
                customer_id = input("Customer ID: ").strip()
                currency = input("Currency (EGP, USD, AED, EUR, SAR): ")

                account_id = create_account(accounts, customers, customer_id, currency)
                print("Account created:", account_id)

            elif choice == "3":
                account_id = input("Account ID: ").strip()
                amount = int(input("Amount: "))

                transaction_id = deposit(accounts, transactions, account_id, amount)
                print("Deposit successful:", transaction_id)

            elif choice == "4":
                account_id = input("Account ID: ").strip()
                amount = int(input("Amount: "))

                transaction_id = withdraw(accounts, transactions, account_id, amount)
                print("Withdrawal successful:", transaction_id)

            elif choice == "5":
                sender_id = input("Sender account ID: ").strip()
                receiver_id = input("Receiver account ID: ").strip()
                amount = int(input("Amount: "))

                transfer_id = transfer(
                    accounts, transactions, sender_id, receiver_id, amount
                )
                print("Transfer successful:", transfer_id)

            elif choice == "6":
                status_menu(accounts)

            elif choice == "7":
                email = input("Email: ").strip().lower()
                info = search_customer(customers, email)
                print(f"Name: {info['name']}")
                print(f"Email: {info['email']}")
                print(f"Contact: {info['contact']}")
                print(f"Accounts: {', '.join(info['account_ids']) or 'none'}")

            elif choice == "8":
                reports_menu(customers, accounts, transactions)

            elif choice == "9":
                save_data(customers, accounts, transactions)
                print("Data saved successfully. Goodbye!")
                break

            else:
                print("Invalid menu choice. Choose 1-9.")

        except ValueError as e:
            # int() parse failures and the daily report's date check land here.
            print("Invalid input:", e)

        except BankingError as e:
            print("Banking error:", e)


if __name__ == "__main__":
    main()
