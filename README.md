# Banking System

A small command-line banking application written in pure Python (standard library only). It manages customers, accounts, and transactions, validates all input, persists state to a JSON file, and can generate plain-text statements and reports.

The project is deliberately dependency-free and split into small, single-purpose modules, with a unit-test suite built on `pytest`.

## Features

- **Customers**: register with name, email, and an 11-digit contact number; duplicate emails are rejected; look up by ID or email.
- **Accounts**: open accounts in `EGP`, `USD`, `AED`, `EUR`, or `SAR`; freeze, unfreeze, and close accounts (closing requires a zero balance).
- **Transactions**: deposit, withdraw, and transfer between accounts. Transfers are recorded as a linked `transfer_out` / `transfer_in` pair sharing one `TRxxx` ID, and are only allowed between active accounts of the same currency.
- **Reports**: account statement, customer report, daily transaction report, and an overall bank summary.
- **Persistence**: all data is loaded on startup and saved on exit to `data/bank_data.json`. Saves are atomic (temp file + rename), so a crash mid-write can't corrupt existing data, and a corrupted file raises a clear error instead of being silently overwritten.
- **Validation and errors**: a hierarchy of custom exceptions (all derived from `BankingError`) so the CLI can report problems cleanly.

## Requirements

- Python 3.8+
- `pytest` (only needed to run the tests)

## Getting Started

```bash
git clone https://github.com/itachi0xx/banking_system.git
cd banking_system

# optional: virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

python main.py
```

### Using the CLI

```
===== BANKING SYSTEM =====
1. Register customer
2. Create account
3. Deposit
4. Withdraw
5. Transfer
6. Manage account status (freeze / unfreeze / close)
7. Find customer by email
8. Reports
9. Save and exit
```

Changes live in memory until you choose **9. Save and exit**. Quitting any other way (Ctrl+C, closing the terminal) discards the session's changes.

Amounts are whole numbers (integers); decimals are not supported.

The data file location is resolved relative to the project (`data/bank_data.json`), so the app runs from any checkout. The `data/` folder is created automatically on first save.

## Project Structure

```
banking_system/
├── main.py            # Interactive CLI menu loop (including report and status sub-menus)
├── customers.py       # Register / get / search customers, ID generation (C001, C002, ...)
├── accounts.py        # Create accounts, freeze / unfreeze / close, ID generation (A001, ...)
├── transactions.py    # Deposit, withdraw, transfer, filters (T001..., TR001...)
├── reports.py         # Statement, customer, daily, and bank-summary reports
├── validators.py      # Name, email, contact, currency, and status validation
├── storage.py         # JSON load / atomic save
├── exceptions.py      # Custom exception hierarchy
├── data/
│   └── bank_data.json # Sample data (3 customers, 3 accounts, transactions)
└── tests/             # pytest suite (28 tests)
```

## Data Model

State is three dictionaries keyed by ID, stored together in one JSON file:

```jsonc
{
  "customers": {
    "C001": { "name": "Alex Morgan", "email": "alex.morgan@example.com",
              "contact": "01000000001", "account_ids": ["A001"] }
  },
  "accounts": {
    "A001": { "customer_id": "C001", "currency": "EGP",
              "balance": 300, "status": "active" }   // active | frozen | closed
  },
  "transactions": {
    "T001": { "type": "deposit",                      // deposit | withdraw | transfer_out | transfer_in
              "account_id": "A001", "amount": 1000, "status": "success",
              "timestamp": "2026-11-01T23:50:35+00:00",  // UTC, ISO 8601
              "transfer_id": null }                   // "TRxxx" for both legs of a transfer
  }
}
```

## Business Rules

| Rule | Behavior |
|---|---|
| Name | Letters and spaces only, non-empty |
| Email | Basic `user@domain.tld` format, lowercased, must be unique |
| Contact | Exactly 11 digits |
| Currency | One of `EGP`, `USD`, `AED`, `EUR`, `SAR` |
| Amount | Positive integer |
| Deposit / withdraw | Account must be `active`; withdrawals cannot exceed the balance |
| Transfer | Different accounts, both `active`, same currency, sufficient funds |
| Close account | Only when the balance is zero |

## Running the Tests

```bash
pip install pytest
python -m pytest -v
```

The suite covers customers, accounts, transactions, reports, and storage (including missing files, corrupted files, and failed saves). Storage tests use `tmp_path` and `monkeypatch`, so they never touch your real data file.

## Programmatic Use

The modules are plain functions operating on dictionaries, so they can be used without the CLI:

```python
from customers import register_customer
from accounts import create_account
from transactions import deposit, transfer
from reports import generate_account_statement

customers, accounts, transactions = {}, {}, {}

cid = register_customer(customers, "Ahmed Ali", "ahmed@example.com", "01012345678")
a1 = create_account(accounts, customers, cid, "EGP")
a2 = create_account(accounts, customers, cid, "EGP")

deposit(accounts, transactions, a1, 1000)
transfer(accounts, transactions, a1, a2, 250)

print(generate_account_statement(accounts, transactions, a1))
```

## Roadmap Ideas

- Customer lookup by ID from the menu
- Basic authentication / per-customer login
- Decimal-safe money handling (`decimal.Decimal` or integer minor units)
- Transaction history for failed attempts (the `status` field already allows it)
- Currency conversion for cross-currency transfers

## License

No license has been specified yet. Add a `LICENSE` file (for example MIT) to clarify usage terms.
