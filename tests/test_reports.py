from reports import (
    generate_account_statement,
    generate_customer_report,
    generate_daily_transaction_report,
    generate_bank_summary,
)


def test_account_statement():
    accounts = {
        "A001": {
            "customer_id": "C001",
            "balance": 1000,
            "currency": "EGP",
            "status": "active",
        }
    }

    transactions = {}

    report = generate_account_statement(accounts, transactions, "A001")

    assert isinstance(report, str)
    assert "A001" in report


def test_customer_report():
    customers = {
        "C001": {
            "name": "Ahmed Ali",
            "email": "ahmed@gmail.com",
            "contact": "01012345678",
            "account_ids": ["A001"],
        }
    }

    accounts = {
        "A001": {
            "customer_id": "C001",
            "balance": 1000,
            "currency": "EGP",
            "status": "active",
        }
    }

    report = generate_customer_report(customers, accounts, "C001")

    assert isinstance(report, str)
    assert "Ahmed Ali" in report


def test_daily_report():
    transactions = {}

    report = generate_daily_transaction_report(transactions, "2026-11-02")

    assert isinstance(report, str)


def test_bank_summary():
    customers = {}
    accounts = {}
    transactions = {}

    report = generate_bank_summary(customers, accounts, transactions)

    assert isinstance(report, str)
