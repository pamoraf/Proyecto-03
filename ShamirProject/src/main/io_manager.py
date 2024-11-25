def read_bytes_file(file_path : str):
    """
    Reads byte content of a file.
    
    Args:
        file_path (str): The path of the file.
    
    Returns:
        bytes: The bytes content of the file.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file is not readable.
    """
    with open(file_path, 'rb') as file:
        return file.read()


def write_bytes_file(file_path : str, data : bytes):
    """
    Writes bytes data to a file.
    
    Args:
        file_path (str): The path of the file.
        data (bytes): The byte data to write.
    
    Raises:
        FileNotFoundError: If the directory does not exist.
        PermissionError: If the directory is not writable.
    """
    with open(file_path, 'wb') as file:
        file.write(data)

def read_text_file(file_path : str):
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

def write_text_file(file_path : str, data : bytes):
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
