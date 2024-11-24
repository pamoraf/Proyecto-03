import pytest
import os
import sys
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

def get_subarrays(array, n):
    if n > len(array):
        return []
    subarrays = []
    for i in range(len(array) - n + 1):
        subarrays.append(array[i: i + n])
    return subarrays

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
    with pytest.raises(ValueError):
        generate_shares(total_evaluations, minimum_evaluations, key)

@pytest.mark.parametrize("total_evaluations, minimum_evaluations, key", POLYNOMIAL_POINST_WITH_KEYS)
def test_generate_shares(total_evaluations, minimum_evaluations, key):
    evaluations_format = generate_shares(total_evaluations, minimum_evaluations, key)
    evaluations = get_evaluations(evaluations_format)
    assert len(evaluations) == total_evaluations
    assert len(evaluations) == len(set(evaluations))

@pytest.mark.parametrize("total_evaluations, minimum_evaluations, key", POLYNOMIAL_POINST_WITH_KEYS)
def test_reconstruct_secret(total_evaluations, minimum_evaluations, key):
    evaluations_format = generate_shares(total_evaluations, minimum_evaluations, key)
    secret = reconstruct_secret(evaluations_format)
    assert secret == key
    for i in range(minimum_evaluations + 1 , total_evaluations + 1):
        secret = reconstruct_secret(get_subarrays(i))
        assert secret == key

@pytest.mark.parametrize("evaluations_format, evaluations", [
    ("x, P(x)\n1, 2\n4, 5\n-3, -3\n0, 0", [(1, 2), (4, 5), (-3, -3), (0, 0)]),
    ("x, P(x)\n1, 2\n3, 4\n5, 6\n7, 8\n9, 10", [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]),
    ("x, P(x)\n11, 21\n43, 55\n-36, -33\n1000, 0", [(11, 21), (43, 55), (-36, -33), (1000, 0)]),
])
def test_get_evaluation_format(evaluations_format, evaluations):
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
    assert get_evaluations(evaluations_format) == evaluations
