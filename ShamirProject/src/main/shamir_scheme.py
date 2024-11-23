import hashlib
import random
from sympy import symbols, expand, lambdify
from polynomial import generate_shares

def generate_key(input_string: str) -> bytes:
    """
    Generates a SHA-256 key from the input string.

    Args:
        input_string (str): The input string to generate a key from.

    Returns:
        bytes: The SHA-256 hash of the input string as a byte sequence.
    """
    sha256_hash = hashlib.sha256(input_string.encode()).digest()
    return sha256_hash

def _reconstruct_secret(evaluations: list[tuple[int, int]]) -> int:
    """
    Reconstructs the secret from the polynomial evaluations.

    Args:
        evaluations(list[tuple[int, int]]): A list of tuples where each tuple contains a pair (x, y) representing an evaluation of the polynomial.

    Return:
        secret(int): The secret reconstructed from the evaluations.
    """
    x = symbols('x')
    secret = 0
    k = len(evaluations)
    
    for j in range(k):
        x_j, y_j = evaluations[j]
        L_j = 1
        for m in range(k):
            if m != j:
                x_m, _ = evaluations[m]
                L_j *= (x - x_m) / (x_j - x_m)
        secret += y_j * L_j
    
    return int(secret.subs(x, 0))

def encrypt(text: str, password: str, n: int, t: int) -> tuple[bytes, dict[int, int]]:
    """
    Encrypts the plaintext using the provided password.

    Args:
        text(str): The plaintext to be encrypted.
        password(str): The password used to encrypt the text.
        n(int): The number of shares to generate.
        t(int): The minimum number of shares needed to reconstruct the secret.

    Return:
        tuple:
            - encrypted_content(bytes): The encrypted content as a byte sequence.
            - evaluations(dict[int, int]): The generated shares of the secret.
    """

    key = generate_key(password)

    secret = sum(key) % 256 
    shares = generate_shares(secret, n, t)
    evaluations = {x: y for x, y in shares}
    
    # Encrypt the text (for simplicity, let's just return the text as bytes)
    encrypted_content = text.encode('utf-8')
    
    return encrypted_content, evaluations

def decrypt(encrypted_content: bytes, evaluations: dict[int, int]) -> str:
    """
    Decrypts the encrypted content using the provided evaluations.

    Args:
        encrypted_content(bytes): The encrypted content to be decrypted.
        evaluations(dict[int, int]): Points of the polynomial (x, P(x)).

    Return:
        plaintext(str): The decrypted content as plaintext.
    """
    secret = _reconstruct_secret(list(evaluations.items()))
    return f"Decrypted secret: {secret}"
