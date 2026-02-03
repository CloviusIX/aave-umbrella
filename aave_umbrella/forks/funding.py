from decimal import Decimal

from eth_account.signers.local import LocalAccount
from web3 import AsyncWeb3

from aave_umbrella.config.addresses import USDC_ADDRESS
from aave_umbrella.contracts.erc20 import ERC20
from aave_umbrella.forks.impersonate import impersonate_account
from aave_umbrella.utils.math import balance_to_decimal

USDC_WHALE = "0x3757c6490019b6c9b0b38c3b89fdf83155c2661f"

# Default token configurations: {token_address: (whale_address, amount)}
DEFAULT_TOKENS = {
    USDC_ADDRESS: (USDC_WHALE, 1000),
    # Add more tokens here as needed
}


async def fund_user(
    web3: AsyncWeb3,
    user_account: LocalAccount,
    tokens: dict[str, tuple[str, int]] | None = None,
) -> bool:
    """
    Fund an address with tokens from whale accounts
    :param web3: Web3 connection
    :param user_account: Account to fund
    :param tokens: Dict of {token_address: (whale_address, amount)}. If None, uses DEFAULT_TOKENS
    :return: True if all funding succeeded
    """
    if tokens is None:
        tokens = DEFAULT_TOKENS

    user_address = user_account.address
    all_success = True

    for token_address, (whale_address, amount) in tokens.items():
        token_contract = ERC20(web3, token_address)
        decimals = await token_contract.decimals()
        token_amount = balance_to_decimal(amount, decimals)

        async with impersonate_account(web3, whale_address):
            success = await _fund(
                web3,
                token_address=token_address,
                from_address=whale_address,
                to_address=user_address,
                amount=token_amount,
            )
            all_success = all_success and success

    return all_success


async def _fund(
    web3: AsyncWeb3,
    token_address: str,
    from_address: str,
    to_address: str,
    amount: Decimal,
) -> bool:
    token = ERC20(web3, token_address)
    tx_receipt = await token.transfer(signer=from_address, to=to_address, amount=amount)

    return tx_receipt["status"] == 1
