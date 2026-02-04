import os
from typing import TypeAlias

from dotenv import load_dotenv
from web3 import AsyncHTTPProvider, AsyncWeb3

load_dotenv()

AsyncW3: TypeAlias = AsyncWeb3[AsyncHTTPProvider]
FORK_URL = os.getenv("FORK_URL") or "http://127.0.0.1:8545"  # Anvil default endpoint


async def build_web3_connection(is_notebook: bool = False) -> AsyncW3:
    """
    Connect to the blockchain network
    :param is_notebook: Ignore the connection if notebook
    :return: The asynchronous web3 connection
    """
    w3 = AsyncWeb3(AsyncHTTPProvider(FORK_URL))

    # Check if the connection is successful
    if not is_notebook and not await w3.is_connected():
        raise ConnectionError("Failed to connect to the network")

    return w3
