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
