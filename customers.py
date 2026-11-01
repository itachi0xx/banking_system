from validators import validate_name, validate_email, validate_contact
from exceptions import DuplicateCustomerError, CustomerNotFoundError


def next_customer_id(customers: dict) -> str:

    max_id = 0

    for key in customers.keys():
        number = int(key[1:])
        if number > max_id:
            max_id = number
    new_id = max_id

    return f"C{new_id + 1:03d}"


def register_customer(customers: dict, name: str, email: str, contact: str) -> str:

    name = validate_name(name)
    email = validate_email(email)
    contact = validate_contact(contact)

    for customer in customers.values():
        if customer["email"] == email:
            raise DuplicateCustomerError("Email is already found")

    customer_id = next_customer_id(customers)

    customers[customer_id] = {
        "name": name,
        "email": email,
        "contact": contact,
        "accounts_ids": [],
    }

    return customer_id


def get_customer(customers: dict, customer_id: str) -> dict:

    try:
        return customers[customer_id]
    except KeyError:
        raise CustomerNotFoundError(f"Customer not found: {customer_id}")
