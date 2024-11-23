import pytest
import os
import sys
sys.path.append(os.path.abspath("./src/main"))
from cipher import encrypt, decrypt
from io_manager import read_binary_file, read_text_file

def test_direct_encrypt():
    """
    Test that the encrypt function returns a byte sequence.
    """
    text = "Hello, World!"
    password = "securepassword"
    encrypted_content = encrypt(text, password)
    assert isinstance(encrypted_content, bytes)
    assert encrypted_content != text.encode('utf-8')

def test_direct_decrypt():
    """
    Test that the decrypt function returns a string.
    """
    text = "Hello, World!"
    password = "securepassword"
    encrypted_content = encrypt(text, password)
    decrypted_content = decrypt(encrypted_content, password)
    assert isinstance(decrypted_content, str)
    assert decrypted_content == text

def test_common_text_encrypt():
    text = read_text_file("src/tests/resources/text/common.txt")
    password = "securepassword"
    encrypted_content = encrypt(text, password)
    decrypted_content = decrypt(encrypted_content, password)
    assert isinstance(encrypted_content, bytes)
    assert encrypted_content != text.encode('utf-8')
    assert isinstance(decrypted_content, str)
    assert decrypted_content == text
