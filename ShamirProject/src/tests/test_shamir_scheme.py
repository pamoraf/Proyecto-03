import pytest
import os
import sys
sys.path.append(os.path.abspath("./src/main"))
from shamir_scheme import encrypt, decrypt

EVALUATIONS = [
    (1, 1),
    (10, 1),
    (5, 4),
    (300, 100),
    (32, 6),
    (1000, 30),
    (4, 2),
    (1000, 1000),
    (321, 114)
]

@pytest.fixture(scope="module")
def password_samples():
    passwords = [
        "1234567890",
        "JHxj3£3+`0|1",
        "5MjQ,rc50@\\=",
        "uTHpayUPlYpI",
        "FOLUdyLEaLDMArphInAtechruE",
        "oF031'jlVr<H-:tL]$PN}£%1^f",
        "2zt}S,=Cv9+-R1[I'euD]£`O$|"
    ]
    return passwords

def get_subarrays(array, n):
    if n > len(array):
        return []
    subarrays = []
    for i in range(len(array) - n):
        subarrays.append(array[i: i + n])
    return subarrays

@pytest.mark.parametrize("total_evaluations, minimum_evaluations", [
    (0, 1),
    (1, 0),
    (1, -1),
    (-1, 1),
    (5, 6),
    (0, 0),
    (-1, -1),
    (-6, -3),
    (0, -1)
])
def test_encrypt_invalid_evaluations(text_samples, password_samples, total_evaluations, minimum_evaluations):
    with pytest.raises(ValueError):
        encrypt(text_samples[0], password_samples[0], total_evaluations, minimum_evaluations)

def test_encrypt_empty_text(password_samples):
    password = password_samples[0]
    encrypted_text, evaluations = encrypt("", password, 10, 5)
    assert len(evaluations) == 10
    assert len(evaluations) == len(set(evaluations))

@pytest.mark.parametrize("total_evaluations, minimum_evaluations", EVALUATIONS)
def test_encrypt(text_samples, password_samples, total_evaluations, minimum_evaluations):
    for text in text_samples:
        for password in password_samples:
            encrypted_text, evaluations = encrypt(text, password, total_evaluations, minimum_evaluations)
            assert encrypted_text != bytes([0])
            assert len(evaluations) == total_evaluations
            assert len(evaluations) == len(set(evaluations))

@pytest.mark.parametrize("total_evaluations, minimum_evaluations", EVALUATIONS)
def test_decrypt(text_samples, password_samples, total_evaluations, minimum_evaluations):
    for text in text_samples:
        for password in password_samples:
            encrypted_text, evaluations = encrypt(text, password, total_evaluations, minimum_evaluations)
            decrypted_text = decrypt(encrypted_text, evaluations)
            assert decrypted_text == text
            decrypted_text = decrypt(encrypted_text, evaluations[:minimum_evaluations - 1])
            assert decrypted_text == text

@pytest.mark.parametrize("total_evaluations, minimum_evaluations", [
    (3, 1),
    (2, 2),
    (10, 3),
    (15, 4),
    (50, 6),
    (100, 86),
    (12, 4),
    (6, 3),
    (1, 1)
])
def test_decrypt_evaluations(text_samples, password_samples, total_evaluations, minimum_evaluations):
    for text in text_samples:
        for password in password_samples:
            encrypted_text, evaluations = encrypt(text, password, total_evaluations, minimum_evaluations)
            decrypted_text = decrypt(encrypted_text, evaluations)
            assert decrypted_text == text
            for minimal_evaluation in get_subarrays(evaluations, minimum_evaluations):
                decrypted_text = decrypt(encrypted_text, minimal_evaluation)
                assert decrypted_text == text



