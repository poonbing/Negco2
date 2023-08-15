from wtforms.validators import ValidationError
import re


def validate_phone(_, field):
    pattern = re.compile(r"^\d{8}$")
    if not pattern.match(field.data):
        raise ValidationError("Phone number must be exactly eight digits.")


def validate_image(_, field):
    if not field.data:
        image_mime = field.data.mimetype
        accepted_types = ["image/png", "image/jpeg"]
        if image_mime not in accepted_types:
            raise ValidationError("File type can only be PNG or JPEG")


def validate_password(_, field):
    password = field.data

    length_error = len(password) < 8
    digit_error = not re.search(r"\d", password)
    uppercase_error = not re.search(r"[A-Z]", password)
    lowercase_error = not re.search(r"[a-z]", password)
    symbol_error = not re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password)

    if (
        length_error
        or digit_error
        or uppercase_error
        or lowercase_error
        or symbol_error
    ):
        raise ValidationError(
            "Password must be at least 8 characters long and contain at least one digit, one uppercase letter, one lowercase letter, and one symbol."
        )


def validate_username(_, field):
    username = field.data
    if not re.match(r"^[a-zA-Z0-9]+$", username):
        raise ValidationError("Username can only contain alphanumeric characters")


def validate_name(_, field):
    name = field.data
    if not re.match(r"^[a-zA-Z]+$", name):
        raise ValidationError("Name can only contain alphabets")


def alphanumeric_validator(_, field):
    if not re.match(r"^[a-zA-Z0-9\s]+$", field.data):
        raise ValidationError(
            "Field must only contain alphanumeric characters and spaces"
        )


def rate_validator(_, field):
    if not re.match(r"^[1-5]$", field.data):
        raise ValidationError("Rate must be between 1 and 5")


def datetime_validator(_, field):
    if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", field.data):
        raise ValidationError("Time must be in the format YYYY-MM-DDTHH:MM:SS")


def tracker_item_validator(_, field):
    valid_items = [
        " Shower ",
        " Air Conditioning ",
        " Lighting ",
        " Laundry ",
        " Cooking ",
    ]
    if field.data not in valid_items:
        raise ValidationError("Item must be one of: " + ", ".join(valid_items))
