import random
from sympy import symbols, Eq, solve

def generate_polynomial(secret, k):
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

def evaluate_polynomial(coefficients, x):
    """
    Evaluates the polynomial at a given point.

    Args:
        coefficients (list): List of polynomial coefficients.
        x (int): The point at which the polynomial is evaluated.

    Returns:
        int: The value of the polynomial evaluated at x.
    """
    return sum(c * (x ** i) for i, c in enumerate(coefficients))

def generate_shares(secret, n, k):
    """
    Generates n shares of the secret using a polynomial of degree k-1.

    Args:
        secret (int): The secret to be shared.
        n (int): The total number of shares to be generated.
        k (int): The minimum number of shares needed to reconstruct the secret.

    Returns:
        list: List of tuples (x, y) representing the shares of the secret.
    """
    coefficients = generate_polynomial(secret, k)
    shares = [(x, evaluate_polynomial(coefficients, x)) for x in range(1, n + 1)]
    return shares

def interpolate(shares, k):
    """
    Reconstructs the secret using Lagrange interpolation.

    Args:
        shares (list): List of tuples (x, y) representing the shares of the secret.
        k (int): The minimum number of shares needed to reconstruct the secret.

    Returns:
        int: The reconstructed secret.

    Raises:
        ValueError: If k is less than the minimum number of shares needed.
    """
    if len(shares) < k:
        raise ValueError("The number of shares provided is less than the minimum number of shares needed to reconstruct the secret.")

    x = symbols('x')
    secret = 0
    for j in range(k):
        x_j, y_j = shares[j]
        L_j = 1
        for m in range(k):
            if m != j:
                x_m, _ = shares[m]
                L_j *= (x - x_m) / (x_j - x_m)
        secret += y_j * L_j
    return secret.subs(x, 0)
