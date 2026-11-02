import pytest

from transactions import deposit, withdraw, transfer
from exceptions import (
    AccountNotFoundError,
    AccountInactiveError,
    InvalidAmountError,
    InsufficientAmountError,
    SameAccountError,
    InvalidTransactionError,
)


@pytest.fixture
def bank_data():
    accounts = {
        "A001": {
            "customer_id": "C001",
            "balance": 1000,
            "currency": "EGP",
            "status": "active",
        },
        "A002": {
            "customer_id": "C002",
            "balance": 500,
            "currency": "EGP",
            "status": "active",
        },
    }
    transactions = {}
    return accounts, transactions


def test_deposit(bank_data):
    accounts, transactions = bank_data

    deposit(accounts, transactions, "A001", 200)

    assert accounts["A001"]["balance"] == 1200
    assert len(transactions) == 1


def test_deposit_negative_amount(bank_data):
    accounts, transactions = bank_data

    with pytest.raises(InvalidAmountError):
        deposit(accounts, transactions, "A001", -100)


def test_deposit_unknown_account(bank_data):
    accounts, transactions = bank_data

    with pytest.raises(AccountNotFoundError):
        deposit(accounts, transactions, "A999", 100)


def test_withdraw(bank_data):
    accounts, transactions = bank_data

    withdraw(accounts, transactions, "A001", 200)

    assert accounts["A001"]["balance"] == 800


def test_insufficient_funds(bank_data):
    accounts, transactions = bank_data

    with pytest.raises(InsufficientAmountError):
        withdraw(accounts, transactions, "A001", 2000)

    assert accounts["A001"]["balance"] == 1000


def test_withdraw_from_frozen_account(bank_data):
    accounts, transactions = bank_data
    accounts["A001"]["status"] = "frozen"

    with pytest.raises(AccountInactiveError):
        withdraw(accounts, transactions, "A001", 100)


def test_transfer(bank_data):
    accounts, transactions = bank_data

    transfer(accounts, transactions, "A001", "A002", 300)

    assert accounts["A001"]["balance"] == 700
    assert accounts["A002"]["balance"] == 800
    assert len(transactions) == 2


def test_transfer_to_same_account(bank_data):
    accounts, transactions = bank_data

    with pytest.raises(SameAccountError):
        transfer(accounts, transactions, "A001", "A001", 100)


def test_transfer_different_currencies(bank_data):
    accounts, transactions = bank_data
    accounts["A002"]["currency"] = "USD"

    with pytest.raises(InvalidTransactionError):
        transfer(accounts, transactions, "A001", "A002", 100)
