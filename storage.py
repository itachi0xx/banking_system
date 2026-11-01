import json
import os

path = "/media/atiyah/Garage/FAANG ROAD 101/Phase 1 /CS50P/Projects/toys/banking_system/data/bank_data.json"


def save_data(customers: dict):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(customers, file, indent=4, ensure_ascii=False)


def load_data():
    try:
        with open(path, "r", encoding="utf-8") as file:
            json.load(file)

    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        return f"Ivalid Json file {e}"
