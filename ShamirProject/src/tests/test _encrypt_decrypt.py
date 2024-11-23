import pytest
from your_module import encrypt, decrypt  # Reemplaza 'your_module' con el nombre de tu módulo

# Fixture para Contraseñas
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

# Fixture para Textos
@pytest.fixture(scope="module")
def text_samples():
    return [
        "Hello, World!",
        "This is a test.",
        "Shamir's Secret Sharing is interesting.",
        "Python is great for cryptography.",
        "Let's test edge cases."
    ]

# Test para Cifrado con Texto Vacío
def test_encrypt_empty_text(password_samples):
    password = password_samples[0]
    encrypted_text, evaluations = encrypt("", password, 10, 5)
    assert len(evaluations) == 10
    assert len(evaluations) == len(set(evaluations))

# Test para Evaluaciones Inválidas
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

# Test para Cifrado
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
def test_encrypt(text_samples, password_samples, total_evaluations, minimum_evaluations):
    for text in text_samples:
        for password in password_samples:
            encrypted_text, evaluations = encrypt(text, password, total_evaluations, minimum_evaluations)
            assert encrypted_text is not None
            assert len(evaluations) == total_evaluations
            assert len(evaluations) == len(set(evaluations))

# Test para Descifrado
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
def test_decrypt(text_samples, password_samples, total_evaluations, minimum_evaluations):
    for text in text_samples:
        for password in password_samples:
            encrypted_text, evaluations = encrypt(text, password, total_evaluations, minimum_evaluations)
            decrypted_text = decrypt(encrypted_text, evaluations)
            assert decrypted_text == text
            decrypted_text = decrypt(encrypted_text, evaluations[:minimum_evaluations])
            assert decrypted_text == text

# Test para Evaluaciones en Descifrado
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
            for minimal_evaluation in get_subarrays(evaluations,