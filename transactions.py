from exceptions import (
    AccountNotFoundError,
    AccountInactiveError,
    InvalidAmountError,
    InsufficientAmountError,
    SameAccountError,
    InvalidTransactionError,
)

from datetime import datetime, timezone


def next_transaction_id(transactions: dict) -> str:
    max_id = 0

    for key in transactions.keys():
        number = int(key[1:])
        if number > max_id:
            max_id = number

    return f"T{max_id + 1:03d}"


def next_transfer_id(transactions: dict) -> str:
    max_id = 0

    for transaction in transactions.values():
        transfer_id = transaction.get("transfer_id")

        if transfer_id is not None:
            number = int(transfer_id[2:])

            if number > max_id:
                max_id = number

    return f"TR{max_id + 1:03d}"


def deposit(accounts: dict, transactions: dict, account_id: str, amount: int) -> str:
    if not account_id in accounts:
        raise AccountNotFoundError(f"Account not found: {account_id}")

    if accounts[account_id]["status"] != "active":
        raise AccountInactiveError("Account must be active")

    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise InvalidAmountError("Amount must be a positive integer")

    accounts[account_id]["balance"] += amount

    transaction_id = next_transaction_id(transactions)

    transactions[transaction_id] = {
        "type": "deposit",
        "account_id": account_id,
        "amount": amount,
        "status": "success",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "transfer_id": None,
    }

    return transaction_id


def withdraw(accounts: dict, transactions: dict, account_id: str, amount: int) -> str:
    if not account_id in accounts:
        raise AccountNotFoundError(f"Account not found: {account_id}")

    if accounts[account_id]["status"] != "active":
        raise AccountInactiveError("Account must be active")

    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise InvalidAmountError("Amount must be a positive integer")

    if accounts[account_id]["balance"] < amount:
        raise InsufficientAmountError("Your balance is insufficient")

    accounts[account_id]["balance"] -= amount

    transaction_id = next_transaction_id(transactions)

    transactions[transaction_id] = {
        "type": "withdraw",
        "account_id": account_id,
        "amount": amount,
        "status": "success",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "transfer_id": None,
    }

    return transaction_id


def transfer(
    accounts: dict, transactions: dict, sender_id: str, receiver_id: str, amount: int
) -> str:
    if not sender_id in accounts:
        raise AccountNotFoundError(f"Account not found: {sender_id}")

    if not receiver_id in accounts:
        raise AccountNotFoundError(f"Account not found: {receiver_id}")

    if sender_id == receiver_id:
        raise SameAccountError("Sender account must be differant from receiver")

    if accounts[sender_id]["status"] != "active":
        raise AccountInactiveError("Account must be active")

    if accounts[receiver_id]["status"] != "active":
        raise AccountInactiveError("Account must be active")

    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise InvalidAmountError("Amount must be a positive integer")

    if accounts[sender_id]["balance"] < amount:
        raise InsufficientAmountError("Your balance is insufficient")

    if accounts[sender_id]["currency"] != accounts[receiver_id]["currency"]:
        raise InvalidTransactionError("Cannot transfer between different currencies")

    transfer_id = next_transfer_id(transactions)

    sender_transaction_id = next_transaction_id(transactions)

    accounts[receiver_id]["balance"] += amount
    accounts[sender_id]["balance"] -= amount

    transactions[sender_transaction_id] = {
        "type": "transfer_out",
        "account_id": sender_id,
        "amount": amount,
        "status": "success",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "transfer_id": transfer_id,
    }

    receiver_transaction_id = next_transaction_id(transactions)

    transactions[receiver_transaction_id] = {
        "type": "transfer_in",
        "account_id": receiver_id,
        "amount": amount,
        "status": "success",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "transfer_id": transfer_id,
    }

    return transfer_id


def get_account_transactions(transactions: dict, account_id: str) -> dict:
    account_transactions = {}

    for transaction_id, transaction in transactions.items():
        if transaction["account_id"] == account_id:
            account_transactions[transaction_id] = transaction

    return account_transactions


def filter_transactions_by_type(transactions: dict, transaction_type: str) -> dict:
    types_of_trasactions = {}

    for transaction_id, transaction in transactions.items():
        if transaction["type"] == transaction_type:
            types_of_trasactions[transaction_id] = transaction
    return types_of_trasactions


def filter_transactions_by_date(transactions: dict, target_date: str) -> dict:

    filtered_transactions = {}

    for transaction_id, transaction in transactions.items():
        transaction_date = transaction["timestamp"].split("T")[0]

        if transaction_date == target_date:
            filtered_transactions[transaction_id] = transaction

    return filtered_transactions
