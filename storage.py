import json
from exceptions import DataPersistenceError

PATH = "/media/atiyah/Garage/FAANG ROAD 101/Phase 1 /CS50P/Projects/toys/banking_system/data/bank_data.json"


def save_data(customers, accounts, transactions):
    data = {"customers": customers, "accounts": accounts, "transactions": transactions}

    with open(PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_data():
    try:
        with open(PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        return (data["customers"], data["accounts"], data["transactions"])

    except FileNotFoundError:
        return {}, {}, {}

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise DataPersistenceError(f"Could not load banking data: {e}") from e
