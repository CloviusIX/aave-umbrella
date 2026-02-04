from typing import AsyncIterator

import pytest_asyncio
from eth_account.signers.local import LocalAccount

from aave_umbrella.forks.account import get_user_account
from aave_umbrella.providers.web3_client import AsyncW3, build_web3_connection


@pytest_asyncio.fixture(scope="session")
async def web3() -> AsyncIterator[AsyncW3]:
    """Initialize Web3 connection to Anvil"""
    w3 = await build_web3_connection()
    yield w3
    await w3.provider.disconnect()


@pytest_asyncio.fixture(scope="session")
async def user_account(web3: AsyncW3) -> LocalAccount:
    """Create a new Ethereum account for testing"""
    return await get_user_account(web3)
