import random
from typing import List
from sympy import symbols

def reconstruct_secret(evaluations_format : str) -> int:
    """
    Reconstructs the secret from the polynomial evaluations.

    Args:
        evaluations_format (str): Polynomial evaluations formatted:
            x, P(x)
            x_1, P(x_1)
            .
            .
            .
            x_n, P(x_n)

    Return:
        secret(int): The secret reconstructed from the evaluations.

    Raises:
        ValueError: If evaluations_format does not match the given format.
    """
    x = symbols('x')
    evaluations = get_evaluations(evaluations_format)
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

def generate_shares(secret, n, t):
    """
    Generates n shares of the secret using a polynomial of degree k-1.

    Args:
        secret (int): The secret to be shared.
        n (int): The total number of shares to be generated.
        t (int): The minimum number of shares needed to reconstruct the secret.

    Returns:
        evaluations_format (str): Polynomial evaluations formatted:
            x, P(x)
            x_1, P(x_1)
            .
            .
            .
            x_n, P(x_n)

    Raises;
        ValueError: If t > n
    """
    coefficients = _generate_polynomial(secret, t)
    evaluations = [(x, _evaluate_polynomial(coefficients, x)) for x in range(1, n + 1)]
    return get_evaluations_format(evaluations)


def _generate_polynomial(secret, k):
    """
    Generates a polynomial of degree k-1 with the secret as the constant term.

    Args:
        secret (int): The secret to be shared.
        k (int): The minimum number of shares needed to reconstruct the secret.

    Returns:
        list: List of polynomial coefficients.
    """
    coefficients = [secret] + [random.randint(1, 100) for _ in range(k - 1)]
    return coefficients

def _evaluate_polynomial(coefficients, x):
    """
    Evaluates the polynomial at a given point.

    Args:
        coefficients (list): List of polynomial coefficients.
        x (int): The point at which the polynomial is evaluated.

    Returns:
        int: The value of the polynomial evaluated at x.
    """
    return sum(c * (x ** i) for i, c in enumerate(coefficients))

def get_evaluations_format(evaluations : List[tuple[int, int]]) -> str:
    evaluations_format = "x, P(x)"
    for evaluation in evaluations:
        if len(evaluation) != 2:
            raise ValueError("No 2 dimensional point")
        evaluations_format += f"\n{evaluation[0]}, {evaluation[1]}"
    return evaluations_format

def get_evaluations(evaluations_format : str) -> List[tuple[int, int]]:
    if not "x, P(x)" in evaluations_format:
        raise ValueError("Invalid fomart there is no header.")
    raw_evaluations = evaluations_format.replace("x, P(x)\n", "").split("\n")
    evaluations = list()
    for raw_evaluation in raw_evaluations:
        try:
            x, y = map(int, raw_evaluation.split(', '))
            evaluations.append((x, y))
        except ValueError:
            raise ValueError(f"Invalid format: {raw_evaluation} is not in 'x, y' format")
    return evaluations