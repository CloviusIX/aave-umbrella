from contextlib import asynccontextmanager

from web3 import AsyncWeb3


@asynccontextmanager
async def impersonate_account(web3: AsyncWeb3, address: str):
    """
    Context manager for impersonating accounts
    :param web3: Web3 connection
    :param address: Account to impersonate
    """
    await web3.provider.make_request("anvil_impersonateAccount", [address])
    try:
        yield address
    finally:
        await web3.provider.make_request("anvil_stopImpersonatingAccount", [address])
