import pytest_asyncio
from web3 import AsyncWeb3

from aave_umbrella.forks.account import get_user_account


@pytest_asyncio.fixture(scope="session")
async def web3():
    """Initialize Web3 connection to Anvil"""
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider("http://127.0.0.1:8545"))
    yield w3
    await w3.provider.disconnect()


@pytest_asyncio.fixture(scope="session")
async def user_account(web3):
    """Create a new Ethereum account for testing"""
    return await get_user_account(web3)
