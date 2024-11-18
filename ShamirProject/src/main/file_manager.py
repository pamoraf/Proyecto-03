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
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"The file {file_path} is not readable.")

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
        raise FileNotFoundError(f"The directory {directory} does not exist.")
    if not os.access(directory, os.W_OK):
        raise PermissionError(f"The directory {directory} is not writable.")

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
        IOError: If an error occurs while reading the file.
    """
    _validate_file(file_path)
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        raise
    except PermissionError:
        raise
    except Exception as e:
        raise IOError(f"An error occurred while reading the file {file_path}: {e}")

def write_binary_file(file_path, data):
    """
    Writes binary data to a file.
    
    Args:
        file_path (str): The path to the binary file.
        data (bytes): The binary data to write.
    
    Raises:
        FileNotFoundError: If the directory does not exist.
        PermissionError: If the directory is not writable.
        IOError: If an error occurs while writing to the file.
    """
    _validate_directory(file_path)
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
    except FileNotFoundError:
        raise
    except PermissionError:
        raise
    except Exception as e:
        raise IOError(f"An error occurred while writing to the file {file_path}: {e}")

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
        IOError: If an error occurs while reading the file.
    """
    _validate_file(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise
    except PermissionError:
        raise
    except Exception as e:
        raise IOError(f"An error occurred while reading the file {file_path}: {e}")

def write_text_file(file_path, data):
    """
    Writes text data to a file.
    
    Args:
        file_path (str): The path to the text file.
        data (str): The text data to write.
    
    Raises:
        FileNotFoundError: If the directory does not exist.
        PermissionError: If the directory is not writable.
        IOError: If an error occurs while writing to the file.
    """
    _validate_directory(file_path)
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(data)
    except FileNotFoundError:
        raise
    except PermissionError:
        raise
    except Exception as e:
        raise IOError(f"An error occurred while writing to the file {file_path}: {e}")
