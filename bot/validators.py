from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def phonevalidate(value):
    if len(value) != 13 or not value.startswith("+998"):
        return False
    return True


def emailvalidate(email):
    try:
        validate_email(email)
        return True
    except ValidationError as e:
        return False
