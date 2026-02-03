from contextlib import asynccontextmanager
from typing import AsyncIterator

from web3 import AsyncHTTPProvider, AsyncWeb3


@asynccontextmanager
async def impersonate_account(web3: AsyncWeb3[AsyncHTTPProvider], address: str) -> AsyncIterator[None]:
    """
    Context manager for impersonating accounts
    :param web3: Web3 connection
    :param address: Account to impersonate
    """
    await web3.provider.make_request("anvil_impersonateAccount", [address])
    try:
        yield
    finally:
        await web3.provider.make_request("anvil_stopImpersonatingAccount", [address])
