def encrypt(text: str, password: str, n : int, t: int) -> tuple[bytes, dict[int, int]]:
    """
    Encrypts the plaintext using the provided password.

    Args:
        text(str): The plaintext to be encrypted.
        password(str): The password used to encrypt the text.
        n(int): The number of rounds to perform.
        t(int): The number of threads to use.

    Return:
        tuple:
            -encrypted_content(bytes): The encrypted content as a byte sequence.
            -dict[int, int] : The totality of points evaluated (n).
    """
    pass  


def _get_password() -> str:
    """
    Prompts the user to enter a password.

    Args:
        None.

    Return:
        password(str): The password entered by the user.
    """
    pass  


def decrypt(encrypted_content: bytes, evaluations: dict[int, int]) -> str:
    """
    Decrypts the encrypted content using the provided password.

    Args:
        encrypted_content(bytes): The encrypted content to be decrypted.
        evaluations(dict[int, int]): Points of the polynomial (x, P(x)).

    Return:
        plaintext(str): The decrypted content as plaintext.
    """
    pass


def _reconstruct_secret(evaluations: list[tuple[int, int]]) -> int:
    """
    Reconstructs the secret from the polynomial evaluations.

    Args:
        evaluations(list[tuple[int, int]]): A list of tuples where each tuple contains a pair (x, y) representing an evaluation of the polynomial.

    Return:
        secret(int): The secret reconstructed from the evaluations.
    """
    pass  


def read_evaluations(evaluations_file_path: str) -> dict[int, int]:
    """
    Reads the polynomial evaluations from a file.

    Args:
        evaluations_file_path(str): The path to the file containing the evaluations.

    Return:
        dict[int, int]: Points of the polynomial (x, P(x)).
    """
    pass  