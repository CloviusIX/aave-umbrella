import json

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3.contract import AsyncContract

from aave_umbrella.abi.erc20_abi import ERC20_ABI
from aave_umbrella.config.addresses import USDC_ADDRESS
from aave_umbrella.contracts.erc20 import ERC20
from aave_umbrella.forks.impersonate import impersonate_account
from aave_umbrella.providers.web3_client import AsyncW3
from aave_umbrella.utils.math import amount_to_small_units

USDC_WHALE = "0x2d4fbc5ee56f063d33e9c6390265eeac97afcda8"

# Default token configurations: {token_address: (whale_address, amount)}
DEFAULT_TOKENS = {
    USDC_ADDRESS: (USDC_WHALE, 1000),
    # Add more tokens here as needed
}


async def fund_user(
    web3: AsyncW3,
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
    abi = json.loads(ERC20_ABI)
    all_success = True

    for token_address, (whale_address, amount) in tokens.items():
        token_contract = ERC20(web3, token_address)
        decimals = await token_contract.decimals()
        token_amount = amount_to_small_units(amount, decimals)
        contract = web3.eth.contract(
            address=web3.to_checksum_address(token_address),
            abi=abi,
        )

        async with impersonate_account(web3, whale_address):
            success = await _fund(
                web3,
                contract=contract,
                from_address=web3.to_checksum_address(whale_address),
                to_address=user_address,
                amount=token_amount,
            )
            all_success = all_success and success

    return all_success


async def _fund(
    web3: AsyncW3,
    *,
    contract: AsyncContract,
    from_address: ChecksumAddress,
    to_address: ChecksumAddress,
    amount: int,
) -> bool:
    """
    Transfer tokens from impersonate account
    :param web3: Web3 connection
    :param contract: Token contract
    :param from_address: Impersonated address
    :param to_address: Funding address
    :param amount: Amount to fund (e.g. 100 USDC)
    :return: True if all funding succeeded
    """
    sent_tx = await contract.functions.transfer(
        to_address,
        amount,
    ).transact({"from": from_address})

    tx_receipt = await web3.eth.wait_for_transaction_receipt(sent_tx)

    return tx_receipt["status"] == 1
