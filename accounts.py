from exceptions import CustomerNotFoundError, AccountNotFoundError
from validators import validate_currency


def next_account_id(accounts: dict):
    max_id = 0

    for key in accounts.keys():

        number = int(key[1:])
        if number > max_id:
            max_id = number
    new_id = max_id

    return f"A{new_id + 1:03d}"


def create_account(
    accounts: dict, customers: dict, customer_id: str, currency: str
) -> str:

    if not customer_id in customers:
        raise CustomerNotFoundError(f"Customer {customer_id} does not exist")

    currency = validate_currency(currency)

    account_id = next_account_id(accounts)

    accounts[account_id] = {
        "customer_id": customer_id,
        "currency": currency,
        "balance": 0,
        "status": "active",
    }

    customers[customer_id]["account_ids"].append(account_id)
    return account_id


def get_customer_accounts(accounts: dict, customers: dict, customer_id: str) -> dict:

    if customer_id not in customers:
        raise CustomerNotFoundError(f"Customer not found: {customer_id}")

    account_ids = customers[customer_id]["account_ids"]

    customer_accounts = {}

    for account_id in account_ids:
        customer_accounts[account_id] = accounts[account_id]

    return customer_accounts


def get_account(accounts: dict, account_id: str) -> dict:
    if not account_id in accounts:
        raise AccountNotFoundError(f"No accounts for {account_id}")
    return accounts[account_id]


def close_account(accounts: dict, account_id: str) -> str:
    if account_id not in accounts:
        raise AccountNotFoundError(f"Account not found: {account_id}")

    if accounts[account_id]["status"] == "closed":
        return "Account already closed"

    if accounts[account_id]["balance"] != 0:
        return "Rejected: Account has a balance"

    accounts[account_id]["status"] = "closed"
    return "Account closed successfully"


def freeze_account(accounts: dict, account_id: str) -> str:
    if account_id not in accounts:
        raise AccountNotFoundError(f"Account not found: {account_id}")

    if accounts[account_id]["status"] == "frozen":
        return "Account already frozen"

    if accounts[account_id]["status"] == "closed":
        return "Cannot freeze a closed account"

    accounts[account_id]["status"] = "frozen"
    return "Account frozen successfully"


def unfreeze_account(accounts: dict, account_id: str) -> str:
    if account_id not in accounts:
        raise AccountNotFoundError(f"Account not found: {account_id}")

    if accounts[account_id]["status"] == "active":
        return "Account is already active"

    if accounts[account_id]["status"] == "closed":
        return "Cannot unfreeze a closed account"

    accounts[account_id]["status"] = "active"
    return "Account unfrozen successfully"
