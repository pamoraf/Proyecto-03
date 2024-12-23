import pytest
import os
import sys
sys.path.append(os.path.abspath("./src/main"))
from io_manager import (
    read_bytes_file,
    write_bytes_file,
    read_text_file,
    write_text_file
)

def test_read_bytes_file_not_found():
    """
    Test that read_bytes_file raises FileNotFoundError
    when the file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        read_bytes_file("src/tests/resources/non_existent_file.bin")

def test_read_bytes_file_permission_error():
    """
    Test that read_bytes_file raises PermissionError
    when the file exists but is not readable.
    """
    with pytest.raises(PermissionError):
        read_bytes_file("src/tests/resources/file_without_permission.bin")

def test_write_bytes_file_directory_not_found():
    """
    Test that write_bytes_file raises FileNotFoundError
    when the directory does not exist.
    """
    with pytest.raises(FileNotFoundError):
        write_bytes_file("src/tests/resources/non_existent_directory/file.bin", b"data")

def test_write_bytes_file_permission_error():
    """
    Test that write_bytes_file raises PermissionError
    when the directory exists but is not writable.
    """
    with pytest.raises(PermissionError):
        write_bytes_file("src/tests/resources/directory_without_permission/file.bin", b"data")

def test_read_text_file_not_found():
    """
    Test that read_text_file raises FileNotFoundError
    when the file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        read_text_file("src/tests/resources/non_existent_file.txt")

def test_read_text_file_permission_error():
    """
    Test that read_text_file raises PermissionError
    when the file exists but is not readable.
    """
    with pytest.raises(PermissionError):
        read_text_file("src/tests/resources/file_without_permission.txt")

def test_write_text_file_directory_not_found():
    """
    Test that write_text_file raises FileNotFoundError
    when the directory does not exist.
    """
    with pytest.raises(FileNotFoundError):
        write_text_file("src/tests/resources/non_existent_directory/file.txt", "data")

def test_write_text_file_permission_error():
    """
    Test that write_text_file raises PermissionError
    when the directory exists but is not writable.
    """
    with pytest.raises(PermissionError):
        write_text_file("src/tests/resources/directory_without_permission/file.txt", "data")