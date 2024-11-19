import os

def _validate_file(file_path):
    """
    Ensures that a file exists at the given file path.
    
    Args:
        file_path (str): The path to the file.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file is not readable.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"El archivo {file_path} no se puede leer.")

def _validate_directory(file_path):
    """
    Ensures that the directory for the given file path exists.
    
    Args:
        file_path (str): The path to the file.
    
    Raises:
        FileNotFoundError: If the directory does not exist.
        PermissionError: If the directory is not writable.
    """
    directory = os.path.dirname(file_path)
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"El directorio {directory} no existe.")
    if not os.access(directory, os.W_OK):
        raise PermissionError(f"En el directorio {directory} no se puede escribir.")

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
    _validate_file(file_path)
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
    _validate_directory(file_path)
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
    _validate_file(file_path)
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
    _validate_directory(file_path)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)