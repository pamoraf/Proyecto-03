import random
from typing import List, Tuple
from sympy import symbols

def reconstruct_secret(evaluations_format: str) -> int:
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
    secret_expr = 0 * x  
    k = len(evaluations)
    for j in range(k):
        x_j, y_j = evaluations[j]
        L_j = 1
        for m in range(k):
            if m != j:
                x_m, _ = evaluations[m]
                L_j *= (x - x_m) / (x_j - x_m)
        secret_expr += y_j * L_j
    result = secret_expr.subs(x, 0)
    return int(result)

def generate_shares(secret : int, n : int, t: int):
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

    Raises:
        ValueError: If t > n or if n <= 0 or t <= 0.
    """
    if t > n or n <= 0 or t <= 0:
        raise ValueError("Invalid values for n and t. Ensure that n > 0, t > 0, and t <= n.")
    spacing = 100000000000000000000
    coefficients = _generate_polynomial(secret, t)
    evaluations = [(x, _evaluate_polynomial(coefficients, x * spacing)) for x in range(1, n + 1)]
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

def get_evaluations_format(evaluations: List[Tuple[int, int]]) -> str:
    """
    Converts a list of (x, P(x)) tuples into a formatted string.

    Args:
        evaluations (List[Tuple[int, int]]): A list of tuples where each tuple contains two integers representing a point (x, P(x)).

    Returns:
        str: A formatted string where each line contains the x and P(x) values separated by a comma.

    Raises:
        ValueError: If any tuple in the evaluations list does not contain exactly two elements.
    """
    evaluations_format = "x, P(x)"
    for evaluation in evaluations:
        if len(evaluation) != 2:
            raise ValueError("No 2 dimensional point")
        evaluations_format += f"\n{evaluation[0]}, {evaluation[1]}"
    return evaluations_format

def get_evaluations(evaluations_format: str) -> List[Tuple[int, int]]:
    """
    Parses a string containing evaluations in the format "x, P(x)" and returns a list of tuples.

    Args:
        evaluations_format (str): A string containing evaluations in the format "x, P(x)".
                                    The first line should be "x, P(x)" as a header, followed by
                                    evaluations in the format "x, y" on each subsequent line.

    Returns:
        List[Tuple[int, int]]: A list of tuples where each tuple contains two integers (x, y).

    Raises:
        ValueError: If the input string does not contain the header "x, P(x)".
        ValueError: If any line in the input string is not in the format "x, y".
    """
    if not "x, P(x)" in evaluations_format:
        raise ValueError("Invalid format: there is no header.")
    raw_evaluations = evaluations_format.replace("x, P(x)\n", "").split("\n")
    evaluations = list()
    for raw_evaluation in raw_evaluations:
        try:
            x, y = map(int, raw_evaluation.split(', '))
            evaluations.append((x, y))
        except ValueError:
            raise ValueError(f"Invalid format: {raw_evaluation} is not in 'x, y' format")
    return evaluations