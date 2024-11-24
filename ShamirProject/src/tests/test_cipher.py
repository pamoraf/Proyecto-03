import pytest
import os
import sys
sys.path.append(os.path.abspath("./src/main"))
from cipher import encrypt, decrypt, get_key

PASSWORDS = [
    "P63t7$9lSCZ)",
    "IveRThAvEneU",
    "$|4QORry^S3k?<GZ8=z|<oTO`2\\NDMMG",
    "eR3-3jj5A%]8,>:<,`Y$Yx?I|pm}j9Tx",
    "****************",
    "hola hola",
    "HOla hola",
    "HOLA HOLA",
    "P63T7$9lSCz)",
    "IVeRThAvEneU"
    "$|4QORry^S3k?<GZ8=z|<oTO`2\\NDmmG",
    "ER3-3jj5A%]8,>:<,`Y$Yx?I|pm}j9Tx",
    "*****************"
]

@pytest.mark.parametrize("password", PASSWORDS)
def test_direct_encrypt(password, text_samples):
    """
    Test that the encrypt function returns a byte sequence.

    Args:
        password (str): The password used for encryption.
        text_samples (list): A list of text samples to be encrypted.
    """
    for text in text_samples:
        encrypted_content = encrypt(text, password)
        assert isinstance(encrypted_content, bytes)
        assert encrypted_content != text.encode('utf-8')

@pytest.mark.parametrize("password", PASSWORDS)
def test_direct_decrypt(password, text_samples):
    """
    Test that the decrypt function returns a string.

    Args:
        password (str): The password used for decryption.
        text_samples (list): A list of text samples to be decrypted.
    """
    for text in text_samples:
        encrypted_content = encrypt(text, password)
        decrypted_content = decrypt(encrypted_content, get_key(password))
        assert isinstance(decrypted_content, str)
        assert decrypted_content == text

@pytest.mark.parametrize("password", PASSWORDS)
def test_get_key(password):
    """
    Test the `get_key` function with various passwords.

    This test ensures that the `get_key` function returns an integer key for each password
    and that the keys generated for different passwords are unique.

    Parameters:
        password (str): The password to generate the key for.
    """
    key = get_key(password)
    assert isinstance(key, int)
    for alternative_password in PASSWORDS:
        if password != alternative_password:
            alternative_key = get_key(alternative_password)
            assert key != alternative_key
