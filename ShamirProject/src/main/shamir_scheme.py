from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from polynomial import evaluate_polynomial, generate_polynomial
from sympy import symbols
import hashlib
from typing import List, Tuple, Dict

def _generate_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()

def _reconstruct_secret(evaluations: List[Tuple[int, int]]) -> int:
    """
    Reconstructs the secret from the polynomial evaluations.

    Args:
        evaluations (list[tuple[int, int]]): A list of tuples where each tuple contains a pair (x, y) representing an evaluation of the polynomial.

    Returns:
        int: The secret reconstructed from the evaluations.
    """
    x = symbols('x')
    secret = 0
    n = len(evaluations)

    for j in range(n):
        x_j, y_j = evaluations[j]
        L_j = 1
        for m in range(n):
            if m != j:
                x_m, _ = evaluations[m]
                L_j *= (x - x_m) / (x_j - x_m)
        secret += y_j * L_j
    return int(secret.subs(x, 0))

def encrypt(text: str, password: str, n: int, t: int) -> Tuple[bytes, Dict[int, int]]:
    """
    Encrypts the plaintext using the provided password.

    Args:
        text (str): The plaintext to be encrypted.
        password (str): The password used to encrypt the text.
        n (int): The total number of shares to generate.
        t (int): The minimum number of shares needed to reconstruct the secret.

    Returns:
        Tuple:
            - encrypted_content (bytes): The encrypted content as a byte sequence.
            - evaluations (dict[int, int]): The evaluations of the polynomial.
    """
    secret = int.from_bytes(text.encode(), 'big')

    coefficients = generate_polynomial(secret, t)
    evaluations = {x: evaluate_polynomial(coefficients, x) for x in range(1, n + 1)}

    key = _generate_key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_content = iv + cipher.encrypt(pad(str(evaluations).encode(), AES.block_size))

    return encrypted_content, evaluations

def decrypt(encrypted_content: bytes, evaluations: Dict[int, int], password: str) -> str:
    """
    Decrypts the encrypted content using the provided password.

    Args:
        encrypted_content (bytes): The encrypted content to be decrypted.
        evaluations (dict[int, int]): Points of the polynomial (x, P(x)).
        password (str): The password used to decrypt the content.

    Returns:
        str: The decrypted content as plaintext.
    """
    key = _generate_key(password)
    iv = encrypted_content[:16]  
    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted_content = unpad(cipher.decrypt(encrypted_content[16:]), AES.block_size)
    
    secret = _reconstruct_secret(list(evaluations.items()))
    
    return secret.to_bytes((secret.bit_length() + 7) // 8, 'big').decode()