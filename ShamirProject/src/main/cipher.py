import hashlib
from shamir_scheme import generate_shares, reconstruct_secret
from typing import Tuple, List

def encrypt(text: str, password: str, n: int, t: int) -> Tuple[bytes, List[Tuple[int, int]]]:
    """
    Encrypts the plaintext using the provided password.

    Args:
        text (str): The plaintext to be encrypted.
        password (str): The password used to encrypt the text.
        n (int): The total number of shares to be generated.
        t (int): The minimum number of shares needed to reconstruct the secret.
        
    Return:
        Tuple[bytes, List[Tuple[int, int]]]: The encrypted content as a byte sequence and the evaluations.
    """
    if n <= 0 or t <= 0 or t > n:
        raise ValueError("Invalid number of evaluations")

    key = get_key(password)
    secret = sum(key) % 256  # Using the sum of the key for simplicity
    evaluations = generate_shares(secret, n, t)  # Generate shares

    # Simple XOR encryption
    encrypted_content = bytearray()
    for i in range(len(text)):
        encrypted_content.append(ord(text[i]) ^ key[i % len(key)])

    return bytes(encrypted_content), evaluations

def decrypt(encrypted_content: bytes, evaluations: List[Tuple[int, int]], password: str) -> str:
    """
    Decrypts the encrypted content using the provided evaluations.

    Args:
        encrypted_content (bytes): The encrypted content to be decrypted.
        evaluations (List[Tuple[int, int]]): The evaluations to use for reconstruction.
        password (str): The password used to encrypt the text.

    Return:
        str: The decrypted content as plaintext.
    """
    secret = reconstruct_secret(evaluations)  # Reconstruct secret using evaluations
    key = get_key(password)

    # Simple XOR decryption (same as encryption)
    decrypted_content = bytearray()
    for i in range(len(encrypted_content)):
        decrypted_content.append(encrypted_content[i] ^ key[i % len(key)])

    return decrypted_content.decode('utf-8')  # Decode the decrypted content back to string

def get_key(input_string: str) -> bytes:
    """
    Generates a SHA-256 key from the input string.

    Args:
        input_string (str): The input string to generate a key from.

    Returns:
        bytes: The SHA-256 hash of the input string as a byte sequence.
    """
    sha256_hash = hashlib.sha256(input_string.encode()).digest()
    return sha256_hash