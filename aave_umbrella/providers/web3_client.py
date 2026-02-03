from typing import TypeAlias

from web3 import AsyncHTTPProvider, AsyncWeb3

AsyncW3: TypeAlias = AsyncWeb3[AsyncHTTPProvider]


async def build_web3_connection() -> AsyncW3:
    """
    Connect to the blockchain network
    :return: The asynchronous web3 connection
    """
    w3 = AsyncWeb3(AsyncHTTPProvider("http://127.0.0.1:8545"))

    # Check if the connection is successful
    if not await w3.is_connected():
        raise ConnectionError("Failed to connect to the network")

    return w3
