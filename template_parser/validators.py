import urllib.parse
from typing import Callable, Optional, Tuple, Any
from datetime import datetime

class InputValidators:
    validators: dict[str, Callable[[str], Tuple[bool, Optional[str]]]] = {}

    @classmethod
    def register_validator(cls, name: str, func: Callable[[str], Tuple[bool, Optional[str]]]) -> None:
        cls.validators[name] = func

    @classmethod
    def get_validator(cls, name: str) -> Callable[[str], Tuple[bool, Optional[str]]]:
        return cls.validators.get(name, cls.validate_non_empty)

    @staticmethod
    def validate_non_empty(value: str) -> Tuple[bool, Optional[str]]:
        if value:
            return True, None
        else:
            return False, "Input cannot be empty. Please provide a value."

    @staticmethod
    def validate_int(value: str) -> Tuple[bool, Optional[str]]:
        try:
            int(value)
            return True, None
        except ValueError:
            return False, "Invalid input. Please enter an integer."

    @staticmethod
    def validate_float(value: str) -> Tuple[bool, Optional[str]]:
        try:
            float(value)
            return True, None
        except ValueError:
            return False, "Invalid input. Please enter a floating-point number."

    @staticmethod
    def validate_url(value: str) -> Tuple[bool, Optional[str]]:
        try:
            result = urllib.parse.urlparse(value)
            if all([result.scheme, result.netloc]):
                return True, None
            else:
                return False, "Invalid URL. Please enter a valid URL."
        except:
            return False, "Invalid URL. Please enter a valid URL."

    @staticmethod
    def validate_date(value):
        formats = ['%d-%m-%Y %H:%M', '%d-%m-%Y']  # List of accepted formats
        for fmt in formats:
            try:
                datetime.strptime(value.strip(), fmt)
                return True, ""
            except ValueError:
                continue
        return False, "Invalid date format. Expected formats: DD-MM-YYYY or DD-MM-YYYY HH:MM"
    
    @staticmethod
    def validate_currency(value):
        try:
            float(value)
            return True, ""
        except ValueError:
            return False, "Invalid currency format. Please enter a numeric value."