import re
from exceptions import ValidationError

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_name(name: str) -> str:
    name = name.strip()

    if not name:
        raise ValidationError("Name can't be empty")

    if not all(char.isalpha() or char.isspace() for char in name):
        raise ValidationError("Name must contain letters only")

    return name


def validate_email(email: str) -> str:

    email = email.strip().lower()

    if not EMAIL_PATTERN.match(email):
        raise ValidationError("Invalid email format")
    return email


def validate_contact(contact: str):
    contact = contact.strip()

    if not contact.isdigit():
        raise ValidationError("Contact must contain digits only")

    if len(contact) != 11:
        raise ValidationError("Contact must contain 11 digits")
    return contact


def validate_currency(currency: str) -> str:
    currency_list = ["EGP", "USD", "AED", "EUR", "SAR"]
    currency = currency.strip().upper()

    if not currency:
        raise ValidationError("currency can't be empty")

    if not currency in currency_list:
        raise ValidationError("Not supported currency")

    return currency


def validate_account_status(status: str) -> str:
    status_list = ["active", "closed", "frozen"]

    status = status.strip().lower()

    if not status:
        raise ValidationError("status can't be empty")

    if not status in status_list:
        raise ValidationError("Not supported status")

    return status
