import os

def read_binary_file(file_path):
    """
    Reads a binary file and returns its content.
    
    Args:
        file_path (str): The path to the binary file.
    
    Returns:
        bytes: The content of the binary file.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file is not readable.
    """
    with open(file_path, 'rb') as file:
        return file.read()


def write_binary_file(file_path, data):
    """
    Writes binary data to a file.
    
    Args:
        file_path (str): The path to the binary file.
        data (bytes): The binary data to write.
    
    Raises:
        FileNotFoundError: If the directory does not exist.
        PermissionError: If the directory is not writable.
    """
    with open(file_path, 'wb') as file:
        file.write(data)

def read_text_file(file_path):
    """
    Reads a text file and returns its content.
    
    Args:
        file_path (str): The path to the text file.
    
    Returns:
        str: The content of the text file.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file is not readable.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_text_file(file_path, data):
    """
    Writes text data to a file.
    
    Args:
        file_path (str): The path to the text file.
        data (str): The text data to write.
    
    Raises:
        FileNotFoundError: If the directory does not exist.
        PermissionError: If the directory is not writable.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)

def format_evaluations(evaluations: dict[int, int]) -> str:
    """
    """
    pass

def get_evaluations(format : str) -> dict[int, int]:
    """
    """
    pass
