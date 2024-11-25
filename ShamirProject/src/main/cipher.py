import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
    
def pad(data: bytes) -> bytes:
    """
    Pads the given data to make its length a multiple of the block size (16 bytes).

    Args:
        data (bytes): The input data to be padded.

    Returns:
        bytes: The padded data, with padding bytes appended to make the total length a multiple of 16.
    """
    padding_length = 16 - len(data) % 16
    padding = bytes([padding_length] * padding_length)
    return data + padding

def unpad(data: bytes) -> bytes:
    """
    Removes padding from the given data.

    This function assumes that the padding is in the PKCS#7 format, where the value of each added byte is the number of bytes that are added. For example, if the padding length is 4, the last four bytes of the data will all have the value 4.

    Args:
        data (bytes): The padded data from which padding needs to be removed.

    Returns:
        bytes: The data with the padding removed.
    """
    padding_length = data[-1]
    return data[:-padding_length]

def encrypt(text: str, password: str) -> bytes:
    """
    Encrypts the plaintext using the provided password.

    Args:
        text (str): The plaintext to be encrypted.
        password (str): The password used to encrypt the text.
        
    Returns:
        bytes: The encrypted content as a byte sequence.
    """
    key = get_key(password)
    iv = os.urandom(16)  
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_text = pad(text.encode('utf-8'))
    encrypted_content = iv + encryptor.update(padded_text) + encryptor.finalize()
    return encrypted_content

def decrypt(encrypted_content: bytes, key: bytes) -> str:
    """
    Decrypts the encrypted content using the provided password.

    Args:
        encrypted_content (bytes): The encrypted content to be decrypted.
        password (str): The password used to encrypt the text.

    Returns:
        str: The decrypted content as plaintext.
    """
    iv = encrypted_content[:16]
    encrypted_text = encrypted_content[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(encrypted_text) + decryptor.finalize()
    return unpad(padded_text).decode('utf-8')

def get_key(input_string: str) -> bytes:
    """
    Generates a SHA-256 key from the input string and converts it to an integer.

    Args:
        input_string (str): The input string to generate a key from.

    Returns:
        bytes: The SHA-256 hash of the input string converted to an integer.
    """
    return hashlib.sha256(input_string.encode()).digest()