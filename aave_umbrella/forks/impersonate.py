from contextlib import asynccontextmanager
from typing import AsyncIterator

from aave_umbrella.providers.web3_client import AsyncW3


@asynccontextmanager
async def impersonate_account(web3: AsyncW3, address: str) -> AsyncIterator[None]:
    """
    Context manager for impersonating accounts
    :param web3: Web3 connection
    :param address: Account to impersonate
    """
    await web3.provider.make_request("anvil_impersonateAccount", [address])
    await anvil_set_balance(web3, address, 1)  # fund 1 ETH
    try:
        yield
    finally:
        await web3.provider.make_request("anvil_stopImpersonatingAccount", [address])


async def anvil_set_balance(web3: AsyncW3, address: str, eth_amount: int) -> None:
    """
    Force-set ETH balance of `address` on an Anvil fork.
    eth_amount is in ETH.
    :param web3: Web3 connection
    :param address: Account to send the ETH
    :param eth_amount: ETH balance to impersonate
    """
    checksum_address = web3.to_checksum_address(address)
    wei = int(eth_amount * 10**18)

    response = await web3.provider.make_request("anvil_setBalance", [checksum_address, hex(wei)])

    if "error" in response:
        raise RuntimeError(f"anvil set balance error: {response['error']}")
