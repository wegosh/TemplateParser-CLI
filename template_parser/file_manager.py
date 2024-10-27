import os
from typing import List
from .interfaces import IFileManager

class FileManager(IFileManager):
    def read_file(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise IOError(f"Error reading file {file_path}: {e}") from e

    def write_file(self, file_path: str, content: str) -> None:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise IOError(f"Error writing to file {file_path}: {e}") from e

    def list_directory(self, directory_path: str, extension: str) -> List[str]:
        try:
            return [f for f in os.listdir(directory_path) if f.endswith(extension)]
        except FileNotFoundError:
            raise FileNotFoundError(f"The directory '{directory_path}' does not exist.")
        except Exception as e:
            raise IOError(f"Error accessing directory '{directory_path}': {e}") from e

    def ensure_directory(self, directory_path: str) -> None:
        try:
            os.makedirs(directory_path, exist_ok=True)
        except Exception as e:
            raise PermissionError(f"Error creating directory '{directory_path}': {e}") from e
