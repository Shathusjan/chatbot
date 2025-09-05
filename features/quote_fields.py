QUOTE_FIELDS = [
    ("delivery_in_melbourne", "Will the delivery be within Melbourne?", ["Yes", "No"]),
    ("name", "What is your name?"),
    ("email", "What is your email address?"),
    ("mobile", "What is your mobile number?"),
    ("cake_or_cupcake", "Are you interested in a cake or cupcakes?", ["Cake", "Cupcakes"]),
    ("servings", "How many servings do you need?"),
    ("coffee_or_standard", "Would you like coffee or standard cake/cupcake?", ["Coffee", "Standard"]),
    ("flavour", "What flavour would you like?", ["Vanilla", "Chocolate", "Red velvet", "Lemon", "Carrot"]),
    ("filling", "What filling would you prefer?", ["Cream", "Jam", "Chocolate ganache", "Fruit"]),
    ("event_date", "What is the date of your event?"),
    ("extras", "Do you want any extras (e.g. decorations, toppers)?"),
    ("message", "Any additional message or notes?"),
]

import re
from datetime import datetime

def validate_email(email):
    if not email:
        return False
    # Basic email regex pattern
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_mobile(mobile):
    if not mobile:
        return False
    # Allow digits, spaces, dashes, parentheses, plus sign
    pattern = r'^[\d\s\-\+\(\)]+$'
    return re.match(pattern, mobile) is not None

def validate_non_empty(value):
    return bool(value and str(value).strip())

def validate_servings(value):
    if not value:
        return False
    return value.isdigit() and int(value) > 0

def validate_date(value):
    if not value:
        return False
    try:
        event_date = datetime.strptime(value, "%Y-%m-%d")
        return event_date >= datetime.now()
    except ValueError:
        return False

VALIDATORS = {
    "delivery_in_melbourne": validate_non_empty,
    "name": validate_non_empty,
    "email": validate_email,
    "mobile": validate_mobile,
    "cake_or_cupcake": validate_non_empty,
    "servings": validate_servings,
    "coffee_or_standard": validate_non_empty,
    "flavour": validate_non_empty,
    "filling": validate_non_empty,
    "event_date": validate_date,
    "extras": lambda x: True,  # extras can be optional
    "message": lambda x: True,  # message can be optional
}
