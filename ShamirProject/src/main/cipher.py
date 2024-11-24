import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def generate_key(password: str) -> bytes:
    """
    Generates a key from the provided password using SHA-256.

    Args:
        password (str): The password used to generate the key.

    Returns:
        bytes: The generated key as a byte sequence.
    """
    # Generate a SHA-256 hash from the password
    return hashlib.sha256(password.encode()).digest()

def pad(data: bytes) -> bytes:
    """Pads the data to make it a multiple of the block size."""
    padding_length = 16 - len(data) % 16
    padding = bytes([padding_length] * padding_length)
    return data + padding

def unpad(data: bytes) -> bytes:
    """Removes padding from the data."""
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
    key = generate_key(password)
    iv = os.urandom(16)  # Generate a random initialization vector

    # Create a Cipher object using AES in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the text to be a multiple of the block size (16 bytes for AES)
    padded_text = pad(text.encode('utf-8'))
    
    # Encrypt the padded text
    encrypted_content = iv + encryptor.update(padded_text) + encryptor.finalize()
    
    return encrypted_content

def decrypt(encrypted_content: bytes, password: str) -> str:
    """
    Decrypts the encrypted content using the provided password.

    Args:
        encrypted_content (bytes): The encrypted content to be decrypted.
        password (str): The password used to encrypt the text.

    Returns:
        str: The decrypted content as plaintext.
    """
    key = generate_key(password)

    # Extract the IV from the beginning of the encrypted content
    iv = encrypted_content[:16]
    encrypted_text = encrypted_content[16:]

    # Create a Cipher object using AES in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the encrypted text
    padded_text = decryptor.update(encrypted_text) + decryptor.finalize()

    # Unpad the text
    return unpad(padded_text).decode('utf-8')

def get_key(input_string: str) -> int:
    """
    Generates a SHA-256 key from the input string and converts it to an integer.

    Args:
        input_string (str): The input string to generate a key from.

    Returns:
        int: The SHA-256 hash of the input string converted to an integer.
    """
    sha256_hash = hashlib.sha256(input_string.encode()).digest()
    return int.from_bytes(sha256_hash, 'big')  # Convertir a entero
