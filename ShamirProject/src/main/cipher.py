#Aqui va lo del cifrado AES
import hashlib

def encrypt(text: str, password : str) -> bytes:
    """
    Encrypts the plaintext using the provided password.

    Args:
        text(str): The plaintext to be encrypted.
        password(str): The password used to encrypt the text.
        
    Return:
        encrypted_content(bytes): The encrypted content as a byte sequence.
    """

    key = generate_key(password)

    secret = sum(key) % 256 
    shares = generate_shares(secret, n, t)
    evaluations = {x: y for x, y in shares}
    
    # Encrypt the text (for simplicity, let's just return the text as bytes) XD copigod
    encrypted_content = text.encode('utf-8')
    
    return encrypted_content

def decrypt(encrypted_content: bytes, key : int) -> str:
    """
    Decrypts the encrypted content using the provided evaluations.

    Args:
        encrypted_content(bytes): The encrypted content to be decrypted.
        key (int): The key to use 

    Return:
        plaintext(str): The decrypted content as plaintext.
    """
    secret = _reconstruct_secret(list(evaluations.items()))
    return f"Decrypted secret: {secret}"

def _generate_key(input_string: str) -> bytes:
    """
    Generates a SHA-256 key from the input string.

    Args:
        input_string (str): The input string to generate a key from.

    Returns:
        bytes: The SHA-256 hash of the input string as a byte sequence.
    """
    sha256_hash = hashlib.sha256(input_string.encode()).digest()
    return sha256_hash
