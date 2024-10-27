import pytest
import re
from template_parser.template_processor import TemplateProcessor

PLACEHOLDER_PATTERN = re.compile(
    r'(?P<quote>"?)<'
    r'(?P<name>[^<>:|]+)'              # Placeholder name
    r'(:(?P<type>[^<>:|]+))?'          # Optional type
    r'(?P<options>(?:\|[^<>|]+)*)'     # Optional options
    r'>\1'
)

def test_extract_placeholders_simple():
    processor = TemplateProcessor()
    template_text = "Hello, <name>!"
    expected = {
        'name': {'type': 'str', 'options': {}}
    }
    result = processor.extract_placeholders(template_text)
    assert result == expected

def test_extract_placeholders_with_type():
    processor = TemplateProcessor()
    template_text = "Your age is <age:int>."
    expected = {
        'age': {'type': 'int', 'options': {}}
    }
    result = processor.extract_placeholders(template_text)
    assert result == expected

def test_extract_placeholders_with_type_and_option():
    processor = TemplateProcessor()
    template_text = "Date: <date_input:date|format=%Y-%m-%d>"
    expected = {
        'date_input': {'type': 'date', 'options': {'format': '%Y-%m-%d'}}
    }
    result = processor.extract_placeholders(template_text)
    assert result == expected

def test_extract_placeholders_with_multiple_options():
    processor = TemplateProcessor()
    template_text = "Amount: <amount:currency|format=long|symbol=false|currency_code=USD>"
    expected = {
        'amount': {
            'type': 'currency',
            'options': {
                'format': 'long',
                'symbol': 'false',
                'currency_code': 'USD'
            }
        }
    }
    result = processor.extract_placeholders(template_text)
    assert result == expected

def test_extract_placeholders_multiple_placeholders():
    processor = TemplateProcessor()
    template_text = "Name: <name>, Age: <age:int>, Date: <date:date|format=%Y-%m-%d>"
    expected = {
        'name': {'type': 'str', 'options': {}},
        'age': {'type': 'int', 'options': {}},
        'date': {'type': 'date', 'options': {'format': '%Y-%m-%d'}}
    }
    result = processor.extract_placeholders(template_text)
    assert result == expected

def test_extract_placeholders_options_without_values():
    processor = TemplateProcessor()
    template_text = "Flag: <flag:bool|optional>"
    expected = {
        'flag': {'type': 'bool', 'options': {'optional': True}}
    }
    result = processor.extract_placeholders(template_text)
    assert result == expected

def test_extract_placeholders_with_quotes():
    processor = TemplateProcessor()
    template_text = '{"message": "<greeting>"}'
    expected = {
        'greeting': {'type': 'str', 'options': {}}
    }
    result = processor.extract_placeholders(template_text)
    assert result == expected

def test_extract_placeholders_special_characters_in_name():
    processor = TemplateProcessor()
    template_text = "Value: <value_1:int>"
    expected = {
        'value_1': {'type': 'int', 'options': {}}
    }
    result = processor.extract_placeholders(template_text)
    assert result == expected

def test_extract_placeholders_missing_closing_bracket():
    processor = TemplateProcessor()
    template_text = "Value: <value:int"
    expected = {}
    result = processor.extract_placeholders(template_text)
    assert result == expected

def test_extract_placeholders_no_placeholders():
    processor = TemplateProcessor()
    template_text = "This template has no placeholders."
    expected = {}
    result = processor.extract_placeholders(template_text)
    assert result == expected
