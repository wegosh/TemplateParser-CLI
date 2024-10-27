import pytest
from template_parser.validators import InputValidators

def test_validate_non_empty_valid():
    result, error = InputValidators.validate_non_empty("Test input")
    assert result is True
    assert error is None

def test_validate_non_empty_invalid():
    result, error = InputValidators.validate_non_empty("")
    assert result is False
    assert error == "Input cannot be empty. Please provide a value."

def test_validate_int_valid():
    result, error = InputValidators.validate_int("42")
    assert result is True
    assert error is None

def test_validate_int_invalid_string():
    result, error = InputValidators.validate_int("abc")
    assert result is False
    assert error == "Invalid input. Please enter an integer."

def test_validate_int_invalid_float():
    result, error = InputValidators.validate_int("3.14")
    assert result is False
    assert error == "Invalid input. Please enter an integer."

def test_validate_float_valid():
    result, error = InputValidators.validate_float("3.14")
    assert result is True
    assert error is None

def test_validate_float_valid_integer():
    result, error = InputValidators.validate_float("42")
    assert result is True
    assert error is None

def test_validate_float_invalid_string():
    result, error = InputValidators.validate_float("abc")
    assert result is False
    assert error == "Invalid input. Please enter a floating-point number."

def test_validate_url_valid():
    result, error = InputValidators.validate_url("https://www.example.com")
    assert result is True
    assert error is None

def test_validate_url_missing_scheme():
    result, error = InputValidators.validate_url("www.example.com")
    assert result is False
    assert error == "Invalid URL. Please enter a valid URL."

def test_validate_url_invalid_format():
    result, error = InputValidators.validate_url("not a url")
    assert result is False
    assert error == "Invalid URL. Please enter a valid URL."

def test_validate_date_valid_dd_mm_yyyy():
    result, error = InputValidators.validate_date("25-12-2023")
    assert result is True
    assert error == ""

def test_validate_date_valid_dd_mm_yyyy_hh_mm():
    result, error = InputValidators.validate_date("25-12-2023 15:30")
    assert result is True
    assert error == ""

def test_validate_date_invalid_format():
    result, error = InputValidators.validate_date("12/25/2023")
    assert result is False
    assert error == "Invalid date format. Expected formats: DD-MM-YYYY or DD-MM-YYYY HH:MM"

def test_validate_date_invalid_string():
    result, error = InputValidators.validate_date("not a date")
    assert result is False
    assert error == "Invalid date format. Expected formats: DD-MM-YYYY or DD-MM-YYYY HH:MM"

def test_validate_currency_valid_integer():
    result, error = InputValidators.validate_currency("100")
    assert result is True
    assert error == ""

def test_validate_currency_valid_float():
    result, error = InputValidators.validate_currency("1234.56")
    assert result is True
    assert error == ""

def test_validate_currency_invalid_string():
    result, error = InputValidators.validate_currency("one hundred")
    assert result is False
    assert error == "Invalid currency format. Please enter a numeric value."
