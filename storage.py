import json
import os
import tempfile
from pathlib import Path

from exceptions import DataPersistenceError

PATH = Path(__file__).resolve().parent / "data" / "bank_data.json"


def save_data(customers, accounts, transactions):
    data = {"customers": customers, "accounts": accounts, "transactions": transactions}

    path = Path(PATH)
    tmp_name = None

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write to a temp file in the same directory, then atomically replace
        # the real file so a crash mid-write can't corrupt existing data.
        fd, tmp_name = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        os.replace(tmp_name, path)

    except BaseException as e:
        if tmp_name and os.path.exists(tmp_name):
            os.remove(tmp_name)
        if isinstance(e, OSError):
            raise DataPersistenceError(f"Could not save banking data: {e}") from e
        raise


def load_data():
    try:
        with open(PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        return (data["customers"], data["accounts"], data["transactions"])

    except FileNotFoundError:
        return {}, {}, {}

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise DataPersistenceError(f"Could not load banking data: {e}") from e
