from customers import register_customer
from exceptions import DuplicateCustomerError


def test_register_customer():

    customers = {}

    customer_id = register_customer(
        customers, "Ahmed Ali", "ahmed@gmail.com", "01012345678"
    )

    assert customer_id == "C001"
    assert customers["C001"]["name"] == "Ahmed Ali"


def test_duplicate_customer():

    customers = {}

    register_customer(customers, "Ahmed Ali", "ahmed@gmail.com", "01012345678")

    try:
        register_customer(customers, "Ahmed Mohamed", "ahmed@gmail.com", "01099999999")
    except DuplicateCustomerError:
        pass
    else:
        assert False, "Expected DuplicateCustomerError"


def test_registered_customer_can_open_account():
    from accounts import create_account

    customers, accounts = {}, {}

    customer_id = register_customer(
        customers, "Ahmed Ali", "ahmed@gmail.com", "01012345678"
    )
    account_id = create_account(accounts, customers, customer_id, "EGP")

    assert account_id in customers[customer_id]["account_ids"]
