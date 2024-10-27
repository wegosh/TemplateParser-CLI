import pytest
import os
from unittest.mock import patch, MagicMock
from template_parser.file_manager import FileManager

@pytest.fixture
def file_manager():
    return FileManager()

def test_read_file_existing(file_manager, tmp_path):
    file_path = tmp_path / "test_file.txt"
    content = "Hello, World!"
    file_path.write_text(content, encoding='utf-8')
    result = file_manager.read_file(str(file_path))
    assert result == content

def test_read_file_non_existing(file_manager):
    file_path = "/non/existing/path/test_file.txt"
    with pytest.raises(IOError) as exc_info:
        file_manager.read_file(file_path)
    assert f"Error reading file {file_path}" in str(exc_info.value)

def test_read_file_no_permission(file_manager, tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Content", encoding='utf-8')

    with patch("builtins.open", side_effect=PermissionError("Permission denied")):
        with pytest.raises(IOError) as exc_info:
            file_manager.read_file(str(file_path))
        assert f"Error reading file {file_path}" in str(exc_info.value)


def test_write_file(file_manager, tmp_path):
    file_path = tmp_path / "test_file.txt"
    content = "Sample content"
    file_manager.write_file(str(file_path), content)
    assert file_path.read_text(encoding='utf-8') == content

def test_write_file_no_permission(file_manager, tmp_path):
    file_path = tmp_path / "test_file.txt"
    content = "Sample content"

    with patch("builtins.open", side_effect=PermissionError("Permission denied")):
        with pytest.raises(IOError) as exc_info:
            file_manager.write_file(str(file_path), content)
        assert f"Error writing to file {file_path}" in str(exc_info.value)


def test_write_file_non_existing_directory(file_manager, tmp_path):
    dir_path = tmp_path / "non_existing_dir"
    file_path = dir_path / "test_file.txt"
    content = "Sample content"
    with pytest.raises(IOError) as exc_info:
        file_manager.write_file(str(file_path), content)
    assert f"Error writing to file {file_path}" in str(exc_info.value)

def test_list_directory_with_matching_files(file_manager, tmp_path):
    (tmp_path / "file1.txt").write_text("Content")
    (tmp_path / "file2.txt").write_text("Content")
    (tmp_path / "file3.json").write_text("{}")
    result = file_manager.list_directory(str(tmp_path), ".txt")
    assert sorted(result) == sorted(["file1.txt", "file2.txt"])

def test_list_directory_no_matching_files(file_manager, tmp_path):
    (tmp_path / "file1.json").write_text("{}")
    result = file_manager.list_directory(str(tmp_path), ".txt")
    assert result == []

def test_list_directory_non_existing(file_manager):
    dir_path = "/non/existing/directory"
    with pytest.raises(FileNotFoundError) as exc_info:
        file_manager.list_directory(dir_path, ".txt")
    assert f"The directory '{dir_path}' does not exist." in str(exc_info.value)

def test_list_directory_no_permission(file_manager, tmp_path):
    dir_path = tmp_path / "no_permission_dir"
    dir_path.mkdir()

    with patch("os.listdir", side_effect=PermissionError("Permission denied")):
        with pytest.raises(IOError) as exc_info:
            file_manager.list_directory(str(dir_path), ".txt")
        assert f"Error accessing directory '{dir_path}'" in str(exc_info.value)

def test_ensure_directory_create_new(file_manager, tmp_path):
    dir_path = tmp_path / "new_directory"
    assert not dir_path.exists()
    file_manager.ensure_directory(str(dir_path))
    assert dir_path.exists()
    assert dir_path.is_dir()

def test_ensure_directory_already_exists(file_manager, tmp_path):
    dir_path = tmp_path / "existing_directory"
    dir_path.mkdir()
    file_manager.ensure_directory(str(dir_path))
    assert dir_path.exists()
    assert dir_path.is_dir()

def test_ensure_directory_no_permission(file_manager, tmp_path):
    dir_path = tmp_path / "new_directory"

    with patch("os.makedirs", side_effect=PermissionError("Permission denied")):
        with pytest.raises(PermissionError) as exc_info:
            file_manager.ensure_directory(str(dir_path))
        assert "Permission denied" in str(exc_info.value)

