def divide(a: float, b: float) -> float:
    """Divide the first number by the second number.

    Args:
        a: Dividend.
        b: Divisor.

    Returns:
        The result of dividing a by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")

    return a / b