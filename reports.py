from transactions import get_account_transactions
from accounts import get_account, get_customer_accounts
from exceptions import CustomerNotFoundError
from datetime import datetime


def generate_account_statement(
    accounts: dict, transactions: dict, account_id: str
) -> str:

    account = get_account(accounts, account_id)
    account_transactions = get_account_transactions(transactions, account_id)

    total_deposits = 0
    total_withdrawals = 0
    total_transferred_out = 0
    total_transferred_in = 0

    for transaction in account_transactions.values():
        transaction_type = transaction["type"]
        amount = transaction["amount"]

        if transaction_type == "deposit":
            total_deposits += amount

        elif transaction_type == "withdraw":
            total_withdrawals += amount

        elif transaction_type == "transfer_out":
            total_transferred_out += amount

        elif transaction_type == "transfer_in":
            total_transferred_in += amount

    lines = [
        "========== ACCOUNT STATEMENT ==========",
        "",
        f"Account ID: {account_id}",
        f"Currency: {account['currency']}",
        f"Current Balance: {account['balance']}",
        f"Account Status: {account['status']}",
        "",
        "Transaction ID | Type | Amount | Status",
        "-" * 50,
    ]

    for transaction_id, transaction in account_transactions.items():
        lines.append(
            f"{transaction_id} | "
            f"{transaction['type']} | "
            f"{transaction['amount']} | "
            f"{transaction['status']}"
        )

    lines.extend(
        [
            "",
            "========== TRANSACTION SUMMARY ==========",
            f"Total transactions: {len(account_transactions)}",
            f"Total deposits: {total_deposits}",
            f"Total withdrawals: {total_withdrawals}",
            f"Total transferred out: {total_transferred_out}",
            f"Total transferred in: {total_transferred_in}",
            "=" * 50,
        ]
    )

    return "\n".join(lines)


def generate_customer_report(customers: dict, accounts: dict, customer_id: str) -> str:

    if customer_id not in customers:
        raise CustomerNotFoundError(f"Customer not found: {customer_id}")

    customer = customers[customer_id]

    customer_accounts = get_customer_accounts(accounts, customers, customer_id)

    currency_totals = {}

    for account in customer_accounts.values():
        currency = account["currency"]
        balance = account["balance"]

        if currency not in currency_totals:
            currency_totals[currency] = 0

        currency_totals[currency] += balance

    lines = [
        "========== CUSTOMER REPORT ==========",
        "",
        f"Customer ID: {customer_id}",
        f"Name: {customer['name']}",
        f"Email: {customer['email']}",
        f"Contact: {customer['contact']}",
        "",
        f"Number of accounts: {len(customer_accounts)}",
        "",
        "Account ID | Currency | Balance | Status",
        "-" * 50,
    ]

    for account_id, account in customer_accounts.items():
        lines.append(
            f"{account_id} | "
            f"{account['currency']} | "
            f"{account['balance']} | "
            f"{account['status']}"
        )

    lines.extend(["", "========== BALANCE SUMMARY =========="])

    for currency, total in currency_totals.items():
        lines.append(f"{currency} Total: {total}")

    lines.append("=" * 50)

    return "\n".join(lines)


def generate_daily_transaction_report(transactions: dict, target_date: str) -> str:

    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format")

    daily_transactions = {}

    for transaction_id, transaction in transactions.items():
        transaction_date = transaction["timestamp"].split("T")[0]

        if transaction_date == target_date:
            daily_transactions[transaction_id] = transaction

    total_deposits = 0
    total_withdrawals = 0
    total_transferred_out = 0
    total_transferred_in = 0

    for transaction in daily_transactions.values():
        transaction_type = transaction["type"]
        amount = transaction["amount"]

        if transaction_type == "deposit":
            total_deposits += amount

        elif transaction_type == "withdraw":
            total_withdrawals += amount

        elif transaction_type == "transfer_out":
            total_transferred_out += amount

        elif transaction_type == "transfer_in":
            total_transferred_in += amount

    lines = [
        "========== DAILY TRANSACTION REPORT ==========",
        "",
        f"Report Date: {target_date}",
        f"Total Transactions: {len(daily_transactions)}",
        "",
        "Transaction ID | Account ID | Type | Amount | Status",
        "-" * 65,
    ]

    for transaction_id, transaction in daily_transactions.items():
        lines.append(
            f"{transaction_id} | "
            f"{transaction['account_id']} | "
            f"{transaction['type']} | "
            f"{transaction['amount']} | "
            f"{transaction['status']}"
        )

    lines.extend(
        [
            "",
            "========== DAILY SUMMARY ==========",
            f"Total deposits: {total_deposits}",
            f"Total withdrawals: {total_withdrawals}",
            f"Total transferred out: {total_transferred_out}",
            f"Total transferred in: {total_transferred_in}",
            "=" * 50,
        ]
    )

    return "\n".join(lines)


def generate_bank_summary(customers: dict, accounts: dict, transactions: dict) -> str:

    active_accounts = 0
    frozen_accounts = 0
    closed_accounts = 0

    for account in accounts.values():
        if account["status"] == "active":
            active_accounts += 1

        elif account["status"] == "frozen":
            frozen_accounts += 1

        elif account["status"] == "closed":
            closed_accounts += 1

    currency_totals = {}

    for account in accounts.values():
        currency = account["currency"]
        balance = account["balance"]

        if currency not in currency_totals:
            currency_totals[currency] = 0

        currency_totals[currency] += balance

    total_deposits = 0
    total_withdrawals = 0

    for transaction in transactions.values():

        if transaction["status"] != "success":
            continue

        if transaction["type"] == "deposit":
            total_deposits += transaction["amount"]

        elif transaction["type"] == "withdraw":
            total_withdrawals += transaction["amount"]

    lines = [
        "========== OVERALL BANK SUMMARY ==========",
        "",
        f"Total customers: {len(customers)}",
        f"Total accounts: {len(accounts)}",
        "",
        "ACCOUNT STATUS SUMMARY",
        "-" * 40,
        f"Active accounts: {active_accounts}",
        f"Frozen accounts: {frozen_accounts}",
        f"Closed accounts: {closed_accounts}",
        "",
        "TRANSACTION SUMMARY",
        "-" * 40,
        f"Total deposits: {total_deposits}",
        f"Total withdrawals: {total_withdrawals}",
        "",
        "BALANCE SUMMARY",
        "-" * 40,
    ]

    for currency, total in currency_totals.items():
        lines.append(f"{currency} Total balance: {total}")

    lines.append("=" * 50)

    return "\n".join(lines)
