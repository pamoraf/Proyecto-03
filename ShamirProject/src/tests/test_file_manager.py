import pytest
import os
import sys
sys.path.append(os.path.abspath("./src/main"))
from file_manager import (
    _validate_file,
    _validate_directory,
    read_binary_file,
    write_binary_file,
    read_text_file,
    write_text_file
)

def test_validate_file_not_found():
    """
    Test that _validate_file raises FileNotFoundError
    when the file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        _validate_file("resources/non_existent_file.txt")

def test_validate_file_permission_error():
    """
    Test that _validate_file raises PermissionError
    when the file exists but is not readable.
    """
    with pytest.raises(PermissionError):
        _validate_file("resources/file_without_permission.txt")

def test_validate_directory_not_found():
    """
    Test that _validate_directory raises FileNotFoundError
    when the directory does not exist.
    """
    with pytest.raises(FileNotFoundError):
        _validate_directory("resources/non_existent_directory/file.txt")

def test_validate_directory_permission_error():
    """
    Test that _validate_directory raises PermissionError
    when the directory exists but is not writable.
    """
    with pytest.raises(PermissionError):
        _validate_directory("resources/directory_without_permission/file.txt")

def test_read_binary_file_not_found():
    """
    Test that read_binary_file raises FileNotFoundError
    when the file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        read_binary_file("resources/non_existent_file.bin")

def test_read_binary_file_permission_error():
    """
    Test that read_binary_file raises PermissionError
    when the file exists but is not readable.
    """
    with pytest.raises(PermissionError):
        read_binary_file("resources/file_without_permission.bin")

def test_write_binary_file_directory_not_found():
    """
    Test that write_binary_file raises FileNotFoundError
    when the directory does not exist.
    """
    with pytest.raises(FileNotFoundError):
        write_binary_file("resources/non_existent_directory/file.bin", b"data")

def test_write_binary_file_permission_error():
    """
    Test that write_binary_file raises PermissionError
    when the directory exists but is not writable.
    """
    with pytest.raises(PermissionError):
        write_binary_file("resources/directory_without_permission/file.bin", b"data")

def test_read_text_file_not_found():
    """
    Test that read_text_file raises FileNotFoundError
    when the file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        read_text_file("resources/non_existent_file.txt")

def test_read_text_file_permission_error():
    """
    Test that read_text_file raises PermissionError
    when the file exists but is not readable.
    """
    with pytest.raises(PermissionError):
        read_text_file("resources/file_without_permission.txt")

def test_write_text_file_directory_not_found():
    """
    Test that write_text_file raises FileNotFoundError
    when the directory does not exist.
    """
    with pytest.raises(FileNotFoundError):
        write_text_file("resources/non_existent_directory/file.txt", "data")

def test_write_text_file_permission_error():
    """
    Test that write_text_file raises PermissionError
    when the directory exists but is not writable.
    """
    with pytest.raises(PermissionError):
        write_text_file("resources/directory_without_permission/file.txt", "data")