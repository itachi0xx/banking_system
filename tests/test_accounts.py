import pytest

from accounts import (
    create_account,
    get_account,
    freeze_account,
    unfreeze_account,
    close_account,
)
from exceptions import CustomerNotFoundError, AccountNotFoundError, AccountInactiveError


@pytest.fixture
def bank_data():
    customers = {
        "C001": {
            "name": "Ahmed Ali",
            "email": "ahmed@gmail.com",
            "contact": "01012345678",
            "account_ids": [],
        }
    }
    accounts = {}
    return customers, accounts


def test_create_account(bank_data):
    customers, accounts = bank_data

    account_id = create_account(accounts, customers, "C001", "EGP")

    assert account_id == "A001"
    assert accounts["A001"]["balance"] == 0
    assert accounts["A001"]["status"] == "active"
    assert "A001" in customers["C001"]["account_ids"]


def test_customer_not_found(bank_data):
    customers, accounts = bank_data

    with pytest.raises(CustomerNotFoundError):
        create_account(accounts, customers, "C999", "EGP")


def test_get_account(bank_data):
    customers, accounts = bank_data
    create_account(accounts, customers, "C001", "EGP")

    account = get_account(accounts, "A001")

    assert account["currency"] == "EGP"


def test_account_not_found(bank_data):
    customers, accounts = bank_data

    with pytest.raises(AccountNotFoundError):
        get_account(accounts, "A999")


def test_freeze_account(bank_data):
    customers, accounts = bank_data
    create_account(accounts, customers, "C001", "EGP")

    freeze_account(accounts, "A001")

    assert accounts["A001"]["status"] == "frozen"


def test_unfreeze_account(bank_data):
    customers, accounts = bank_data
    create_account(accounts, customers, "C001", "EGP")

    freeze_account(accounts, "A001")
    unfreeze_account(accounts, "A001")

    assert accounts["A001"]["status"] == "active"


def test_close_account(bank_data):
    customers, accounts = bank_data
    create_account(accounts, customers, "C001", "EGP")

    close_account(accounts, "A001")

    assert accounts["A001"]["status"] == "closed"
