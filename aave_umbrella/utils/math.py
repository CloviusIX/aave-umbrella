from decimal import Decimal


def amount_to_small_units(amount: Decimal | int, decimals: int) -> int:
    """
    Convert token units to base units (uint256).
    Example: 0.5 USDC → 500_000
    """
    return int(amount * (Decimal(10) ** decimals))
