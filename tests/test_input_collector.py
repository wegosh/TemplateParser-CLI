import pytest
from unittest.mock import patch
from template_parser.input_collector import InputCollector

@pytest.fixture
def input_collector():
    return InputCollector()

def test_collect_input_without_validation(input_collector):
    prompt = "Enter something: "
    user_input = "Test Input"
    with patch("builtins.input", return_value=user_input):
        result = input_collector.collect_input(prompt)
        assert result == user_input.strip()

def test_collect_input_with_validation_valid_input(input_collector):
    prompt = "Enter a number: "
    user_input = "42"
    validation_func = lambda x: (x.isdigit(), "Please enter a valid number.")
    with patch("builtins.input", return_value=user_input):
        result = input_collector.collect_input(prompt, validation_func)
        assert result == user_input.strip()

def test_collect_input_with_validation_invalid_input(input_collector, capsys):
    prompt = "Enter a number: "
    inputs = ["abc", "42"]
    validation_func = lambda x: (x.isdigit(), "Please enter a valid number.")
    input_iter = iter(inputs)

    def mock_input(_):
        return next(input_iter)

    with patch("builtins.input", side_effect=mock_input):
        result = input_collector.collect_input(prompt, validation_func)
        assert result == "42"
        captured = capsys.readouterr()
        assert "Please enter a valid number." in captured.out

def test_collect_input_multiple_invalid_inputs(input_collector, capsys):
    prompt = "Enter a number between 1 and 10: "
    inputs = ["0", "11", "5"]
    validation_func = lambda x: (x.isdigit() and 1 <= int(x) <= 10, "Number must be between 1 and 10.")
    input_iter = iter(inputs)

    def mock_input(_):
        return next(input_iter)

    with patch("builtins.input", side_effect=mock_input):
        result = input_collector.collect_input(prompt, validation_func)
        assert result == "5"
        captured = capsys.readouterr()
        assert captured.out.count("Number must be between 1 and 10.") == 2

def test_collect_input_strip_whitespace(input_collector):
    prompt = "Enter something: "
    user_input = "   Test Input   "
    with patch("builtins.input", return_value=user_input):
        result = input_collector.collect_input(prompt)
        assert result == "Test Input"

def test_collect_input_empty_input_no_validation(input_collector):
    prompt = "Enter something: "
    user_input = ""
    with patch("builtins.input", return_value=user_input):
        result = input_collector.collect_input(prompt)
        assert result == ""

def test_collect_input_empty_input_with_validation(input_collector, capsys):
    prompt = "Enter a non-empty string: "
    inputs = ["", "Valid Input"]
    validation_func = lambda x: (bool(x.strip()), "Input cannot be empty.")
    input_iter = iter(inputs)

    def mock_input(_):
        return next(input_iter)

    with patch("builtins.input", side_effect=mock_input):
        result = input_collector.collect_input(prompt, validation_func)
        assert result == "Valid Input"
        captured = capsys.readouterr()
        assert "Input cannot be empty." in captured.out
