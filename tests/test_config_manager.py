import pytest
from unittest.mock import MagicMock, patch
import json
from template_parser.config_manager import ConfigManager
from template_parser.file_manager import FileManager
from template_parser.user_interface import UserInterface

@pytest.fixture
def mock_file_manager():
    return MagicMock(spec=FileManager)

@pytest.fixture
def mock_user_interface():
    return MagicMock(spec=UserInterface)

@pytest.fixture
def config_manager(mock_file_manager, mock_user_interface):
    return ConfigManager("config.json", file_manager=mock_file_manager, user_interface=mock_user_interface)

class TestConfigManager:
    def test_load_config_invalid_json(self, mock_file_manager, mock_user_interface, config_manager):
        invalid_mock_data = '''
        {
            "name": "productID", "type": "str",
            {"name": "schemaVersion", "type": "int"}
        '''
        mock_file_manager.read_file.return_value = invalid_mock_data

        with patch('os.path.isfile', return_value=True):
            config_manager.load_config()

        mock_user_interface.display_warning.assert_called_with("config.json contains invalid JSON. Overwriting it.")
        assert config_manager.config_data == []

    def test_save_config_write_error(self, mock_file_manager, mock_user_interface, config_manager):
        mock_file_manager.write_file.side_effect = Exception("Write error")
        new_entry = {"name": "userID", "type": "str"}

        config_manager.save_config(new_entry)

        mock_user_interface.display_error.assert_called_with("Error writing to config.json: Write error")

    def test_load_config_success(self, mock_file_manager, config_manager):
        mock_data = '''
        [
            {"name": "productID", "type": "str"},
            {"name": "schemaVersion", "type": "int"}
        ]
        '''
        mock_file_manager.read_file.return_value = mock_data

        with patch('os.path.isfile', return_value=True):
            config_manager.load_config()

        assert config_manager.config_data == json.loads(mock_data)

    def test_load_config_file_not_found(self, mock_file_manager, config_manager):
        with patch('os.path.isfile', return_value=False):
            config_manager.load_config()

        assert config_manager.config_data == []

    def test_save_config_success(self, mock_file_manager, config_manager):
        new_entry = {"name": "userID", "type": "str"}

        config_manager.save_config(new_entry)

        assert config_manager.config_data == [new_entry]
        mock_file_manager.write_file.assert_called_with("config.json", json.dumps([new_entry], indent=2))
