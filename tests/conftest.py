import pytest_asyncio
from web3 import AsyncWeb3


@pytest_asyncio.fixture(scope="session")
async def web3():
    """Initialize Web3 connection to Anvil"""
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider("http://127.0.0.1:8545"))
    yield w3
    await w3.provider.disconnect()
