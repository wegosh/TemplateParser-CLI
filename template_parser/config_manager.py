import os
import json
from typing import Any, Dict, List
from .interfaces import IConfigManager, IFileManager
from .user_interface import UserInterface

class ConfigManager(IConfigManager):
    def __init__(self, config_path, file_manager: IFileManager, user_interface: UserInterface):
        self.config_path = config_path
        self.file_manager = file_manager
        self.user_interface = user_interface
        self.config_data = []

    def load_config(self) -> None:
        if os.path.isfile(self.config_path):
            try:
                content: str = self.file_manager.read_file(self.config_path)
                existing_data: Any = json.loads(content)
                if isinstance(existing_data, list):
                    self.config_data = existing_data
                else:
                    self.user_interface.display_warning(f"{self.config_path} is not a list. Overwriting it.")
            except json.JSONDecodeError:
                self.user_interface.display_warning(f"{self.config_path} contains invalid JSON. Overwriting it.")
            except Exception as e:
                self.user_interface.display_error(f"Error reading {self.config_path}: {e}")

    def save_config(self, config_entry: Dict[str, Any]) -> None:
        self.config_data.append(config_entry)
        try:
            self.file_manager.ensure_directory(os.path.dirname(self.config_path))
            self.file_manager.write_file(self.config_path, json.dumps(self.config_data, indent=2))
            self.user_interface.display_message(f"User inputs appended to {self.config_path}")
        except Exception as e:
            self.user_interface.display_error(f"Error writing to {self.config_path}: {e}")

class ProgramConfigManager:
    def __init__(self, config_path, file_manager: IFileManager):
        self.config_path = config_path
        self.file_manager = file_manager
        self.config = {}
        self.load_config()

    def load_config(self) -> None:
        if os.path.isfile(self.config_path):
            try:
                content: str = self.file_manager.read_file(self.config_path)
                self.config = json.loads(content)
            except json.JSONDecodeError:
                print(f"Warning: {self.config_path} contains invalid JSON. Using default configuration.")
            except Exception as e:
                print(f"Error reading {self.config_path}: {e}. Using default configuration.")
        else:
            print(f"Configuration file {self.config_path} not found. Using default configuration.")

    def get_required_variables(self) -> List[str]:
        return self.config.get("required_variables", [])

    def get_output_filename_format(self) -> str:
        return self.config.get("output_filename_format", "output_{date}_{time}.json")
    
    def get_locale(self) -> str:
        return self.config.get('locale', 'en_GB')