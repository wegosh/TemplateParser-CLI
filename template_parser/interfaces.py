from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Any

class IFileManager(ABC):
    @abstractmethod
    def read_file(self, file_path: str) -> str:
        pass

    @abstractmethod
    def write_file(self, file_path: str, content: str) -> None:
        pass

    @abstractmethod
    def list_directory(self, directory_path: str, extension: Optional[str] = None) -> List[str]:
        pass

    @abstractmethod
    def ensure_directory(self, directory_path: str) -> None:
        pass

class IInputCollector(ABC):
    @abstractmethod
    def collect_input(self, prompt: str, validation_func: Optional[Callable[[str], Any]] = None) -> str:
        pass

class IConfigManager(ABC):
    @abstractmethod
    def load_config(self) -> dict:
        pass

    @abstractmethod
    def save_config(self, config_entry: dict) -> None:
        pass

class ITemplateProcessor(ABC):
    @abstractmethod
    def extract_placeholders(self, template_text: str) -> List[str]:
        pass
