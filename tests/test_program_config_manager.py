import pytest
from unittest.mock import MagicMock, patch
import os
import json
from template_parser.config_manager import ProgramConfigManager
from template_parser.interfaces import IFileManager

@pytest.fixture
def mock_file_manager():
    return MagicMock(spec=IFileManager)

@pytest.fixture
def program_config_manager(tmp_path, mock_file_manager):
    config_path = tmp_path / "config.json"
    return ProgramConfigManager(config_path=str(config_path), file_manager=mock_file_manager)

def test_load_valid_config(program_config_manager, mock_file_manager):
    valid_config = {
        "required_variables": ["var1", "var2"],
        "output_filename_format": "{var1}_{var2}.json",
        "locale": "en_US"
    }
    mock_file_manager.read_file.return_value = json.dumps(valid_config)
    with patch('os.path.isfile', return_value=True):
        program_config_manager.load_config()
    assert program_config_manager.get_required_variables() == ["var1", "var2"]
    assert program_config_manager.get_output_filename_format() == "{var1}_{var2}.json"
    assert program_config_manager.get_locale() == "en_US"

def test_config_file_not_found(program_config_manager, mock_file_manager, capsys):
    mock_file_manager.read_file.return_value = ''
    with patch('os.path.isfile', return_value=False):
        program_config_manager.load_config()
    captured = capsys.readouterr()
    assert "Configuration file" in captured.out
    assert program_config_manager.get_required_variables() == []
    assert program_config_manager.get_output_filename_format() == "output_{date}_{time}.json"
    assert program_config_manager.get_locale() == "en_GB"

def test_invalid_json_in_config_file(program_config_manager, mock_file_manager, capsys):
    mock_file_manager.read_file.return_value = '{invalid_json: true'
    with patch('os.path.isfile', return_value=True):
        program_config_manager.load_config()
    captured = capsys.readouterr()
    assert "contains invalid JSON" in captured.out
    assert program_config_manager.get_required_variables() == []
    assert program_config_manager.get_output_filename_format() == "output_{date}_{time}.json"
    assert program_config_manager.get_locale() == "en_GB"

def test_exception_during_file_read(program_config_manager, mock_file_manager, capsys):
    mock_file_manager.read_file.side_effect = Exception("Read error")
    with patch('os.path.isfile', return_value=True):
        program_config_manager.load_config()
    captured = capsys.readouterr()
    assert "Error reading" in captured.out
    assert program_config_manager.get_required_variables() == []
    assert program_config_manager.get_output_filename_format() == "output_{date}_{time}.json"
    assert program_config_manager.get_locale() == "en_GB"

def test_missing_keys_in_config(program_config_manager, mock_file_manager):
    incomplete_config = {
        "required_variables": ["var1"]
        # Missing 'output_filename_format' and 'locale'
    }
    mock_file_manager.read_file.return_value = json.dumps(incomplete_config)
    with patch('os.path.isfile', return_value=True):
        program_config_manager.load_config()
    assert program_config_manager.get_required_variables() == ["var1"]
    assert program_config_manager.get_output_filename_format() == "output_{date}_{time}.json"
    assert program_config_manager.get_locale() == "en_GB"

def test_empty_config_file(program_config_manager, mock_file_manager):
    mock_file_manager.read_file.return_value = '{}'
    with patch('os.path.isfile', return_value=True):
        program_config_manager.load_config()
    assert program_config_manager.get_required_variables() == []
    assert program_config_manager.get_output_filename_format() == "output_{date}_{time}.json"
    assert program_config_manager.get_locale() == "en_GB"

def test_non_string_values_in_config(program_config_manager, mock_file_manager):
    config_with_wrong_types = {
        "required_variables": "should_be_list",
        "output_filename_format": 123,
        "locale": True
    }
    mock_file_manager.read_file.return_value = json.dumps(config_with_wrong_types)
    with patch('os.path.isfile', return_value=True):
        program_config_manager.load_config()
    assert program_config_manager.get_required_variables() == "should_be_list"
    assert program_config_manager.get_output_filename_format() == 123
    assert program_config_manager.get_locale() == True

def test_valid_config_with_extra_keys(program_config_manager, mock_file_manager):
    config_with_extra_keys = {
        "required_variables": ["var1", "var2"],
        "output_filename_format": "{var1}_{var2}.json",
        "locale": "en_US",
        "extra_key": "extra_value"
    }
    mock_file_manager.read_file.return_value = json.dumps(config_with_extra_keys)
    with patch('os.path.isfile', return_value=True):
        program_config_manager.load_config()
    assert program_config_manager.get_required_variables() == ["var1", "var2"]
    assert program_config_manager.get_output_filename_format() == "{var1}_{var2}.json"
    assert program_config_manager.get_locale() == "en_US"
