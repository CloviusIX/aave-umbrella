from decimal import Decimal


def balance_to_decimal(balance: int, decimals: int) -> Decimal:
    """Convert balance from integer to decimal representation."""
    return balance * (10**decimals)


def decimal_to_balance(balance: Decimal, decimals: int) -> int:
    """Convert amount from decimal to integer balance representation."""
    return int(balance / (10**decimals))
