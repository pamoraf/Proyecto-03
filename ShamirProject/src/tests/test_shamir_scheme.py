import pytest
import os
import sys
import math
sys.path.append(os.path.abspath("./src/main"))
from shamir_scheme import (
    reconstruct_secret, 
    generate_shares,
    get_evaluations,
    get_evaluations_format
)

POLYNOMIAL_POINST_WITH_KEYS = [
    (1, 1, 35),
    (10, 1, 35),
    (5, 4, 35),
    (30, 10, 35),
    (32, 6, 35),
    (40, 30, 35),
    (4, 2, 35),
    (10, 1, 35),
    (3, 2, 35)
]

def get_subarrays(evaluations_format, n):
    """
    Generate subarrays of length n from the given evaluations_format.

    Args:
        evaluations_format (str): The formatted evaluations string.
        n (int): The length of subarrays to generate.

    Returns:
        str: A formatted string of subarrays of length n.
    """
    evaluations = get_evaluations(evaluations_format)
    sub_evaluations = evaluations[:n]
    return get_evaluations_format(sub_evaluations)

@pytest.mark.parametrize("total_evaluations, minimum_evaluations, key", [
    (0, 1, 35),
    (1, 0, 35),
    (1, -1, 35),
    (-1, 1, 35),
    (5, 6, 35),
    (0, 0, 35),
    (-1, -1, 35),
    (-6, -3, 35),
    (0, -1, 35)
])
def test_generate_shares_invalid_evaluations(total_evaluations, minimum_evaluations, key):
    """
    Test that generate_shares raises ValueError for invalid evaluation parameters.

    Args:
        total_evaluations (int): Total number of evaluations.
        minimum_evaluations (int): Minimum number of evaluations required to reconstruct the secret.
        key (int): The secret key.
    """
    with pytest.raises(ValueError):
        generate_shares(key, total_evaluations, minimum_evaluations)

@pytest.mark.parametrize("total_evaluations, minimum_evaluations, key", POLYNOMIAL_POINST_WITH_KEYS)
def test_generate_shares(total_evaluations, minimum_evaluations, key):
    """
    Test that generate_shares produces the correct number of unique evaluations.

    Args:
        total_evaluations (int): Total number of evaluations.
        minimum_evaluations (int): Minimum number of evaluations required to reconstruct the secret.
        key (int): The secret key.
    """
    evaluations_format = generate_shares(key, total_evaluations, minimum_evaluations)
    evaluations = get_evaluations(evaluations_format)
    assert len(evaluations) == total_evaluations
    assert len(evaluations) == len(set(evaluations))

@pytest.mark.parametrize("total_evaluations, minimum_evaluations, key", [
    (5, 4, 1),
    (10, 7, 43),
    (90, 10, 76824),
    (8, 4, 24),
    (15, 11, 12345),
    (27, 23, 67890),
    (25, 10, 132),
    (30, 22, 22),
    (33, 30, 35133),
    (46, 3, 0)
])
def test_shares_dispersion(total_evaluations, minimum_evaluations, key):
    """
    Test the dispersion of shares and check for patterns.

    This test ensures that the spacing between the x-coordinates of the shares is not uniform
    and checks for patterns in the x-coordinates and y-coordinates of the shares.

    Args:
        total_evaluations (int): The total number of shares to generate.
        minimum_evaluations (int): The minimum number of shares required to reconstruct the key.
        key (int): The secret key to be shared.
    """
    evaluations_format = generate_shares(key, total_evaluations, minimum_evaluations)
    evaluations = get_evaluations(evaluations_format)
    region = sorted([point[0] for point in evaluations])
    spacing = abs(region[0] - region[1])
    for i in range(1, len(region) - 1):
        actual_space = abs(region[i] - region[i + 1])
        assert not math.isclose(spacing, actual_space, abs_tol=10000)
    image = sorted([point[1] for point in evaluations])
    spacing = abs(image[0] - image[1])
    for i in range(1, len(image) - 1):
        actual_space = abs(image[i] - image[i + 1])
        assert not math.isclose(spacing, actual_space, abs_tol=10000)
    for i in range(2, len(region)):
        assert not (region[i] - region[i-1] == region[i-1] - region[i-2])
    for i in range(2, len(image)):
        assert not (image[i] - image[i-1] == image[i-1] - image[i-2])

@pytest.mark.parametrize("total_evaluations, minimum_evaluations, key", POLYNOMIAL_POINST_WITH_KEYS)
def test_reconstruct_secret(total_evaluations, minimum_evaluations, key):
    """
    Test that reconstruct_secret correctly reconstructs the secret from evaluations.

    Args:
        total_evaluations (int): Total number of evaluations.
        minimum_evaluations (int): Minimum number of evaluations required to reconstruct the secret.
        key (int): The secret key.
    """
    evaluations_format = generate_shares(key, total_evaluations, minimum_evaluations)
    secret = reconstruct_secret(evaluations_format)
    assert secret == key
    for i in range(minimum_evaluations + 1, total_evaluations + 1):
        subarray_format = get_subarrays(evaluations_format, i)
        secret = reconstruct_secret(subarray_format)
        assert secret == key

@pytest.mark.parametrize("evaluations_format, evaluations", [
    ("x, P(x)\n1, 2\n4, 5\n-3, -3\n0, 0", [(1, 2), (4, 5), (-3, -3), (0, 0)]),
    ("x, P(x)\n1, 2\n3, 4\n5, 6\n7, 8\n9, 10", [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]),
    ("x, P(x)\n11, 21\n43, 55\n-36, -33\n1000, 0", [(11, 21), (43, 55), (-36, -33), (1000, 0)]),
])
def test_get_evaluation_format(evaluations_format, evaluations):
    """
    Test that get_evaluations_format converts evaluations to the correct format.

    Args:
        evaluations_format (str): The expected formatted string.
        evaluations (list): The list of (x, P(x)) tuples.
    """
    assert get_evaluations_format(evaluations) == evaluations_format

@pytest.mark.parametrize("evaluations_format", [
    "x,  P(x)\n1, 2\n4, 5\n-3, -3\n0, 0",
    "x,\n1, 2\n3, 4\n5, 6\n7, 8\n9, 10",
    "\n11, 21\n43, 55\n-36, -33\n 1000, 000", 
    "x, P(x)\na2, 02\n03, 04\n05, 06\n07, 08",
    "x, P(x)\n0/10, 020\n040, 050\n060, 070\n080, 080"
    "x, P(x)\n1.01, 20.0\n40.0, 50.6\n60.6, 70.0\n80.8, 80.0"
])
def test_get_evaluation_format_invalid(evaluations_format):
    """
    Test that get_evaluations_format raises ValueError for invalid formats.

    Args:
        evaluations_format (str): The invalid formatted string.
    """
    with pytest.raises(ValueError):
        get_evaluations_format(evaluations_format)

@pytest.mark.parametrize("evaluations_format, evaluations", [
    ("x, P(x)\n1, 2\n4, 5\n-3, -3\n0, 0", [(1, 2), (4, 5), (-3, -3), (0, 0)]),
    ("x, P(x)\n1, 2\n3, 4\n5, 6\n7, 8\n9, 10", [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]),
    ("x, P(x)\n11, 21\n43, 55\n-36, -33\n1000, 0", [(11, 21), (43, 55), (-36, -33), (1000, 0)]),
    ("x, P(x)\n1, 2\n3, 4\n5, 6\n7, 8", [(1, 2), (3, 4), (5, 6), (7, 8)]),
    ("x, P(x)\n10, 20\n40, 50\n60, 70\n80, 80", [(10, 20), (40, 50), (60, 70), (80, 80)]),
])
def test_get_evaluations(evaluations_format, evaluations):
    """
    Test that get_evaluations correctly parses the formatted string into evaluations.

    Args:
        evaluations_format (str): The formatted string.
        evaluations (list): The expected list of (x, P(x)) tuples.
    """
    assert get_evaluations(evaluations_format) == evaluations
