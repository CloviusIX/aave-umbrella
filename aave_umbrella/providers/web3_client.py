from typing import Any

from web3 import AsyncHTTPProvider, AsyncWeb3
from web3.contract import AsyncContract


async def build_web3_connection() -> AsyncWeb3:
    """
    Connect to the blockchain network
    :return: The asynchronous web3 connection
    """
    w3 = AsyncWeb3(AsyncHTTPProvider("http://127.0.0.1:8545"))

    # Check if the connection is successful
    if not await w3.is_connected():
        raise ConnectionError("Failed to connect to the network")

    return w3


async def eth_call(
    contract: AsyncContract,
    function_name: str,
    params: list[Any] | None = None,
    block_identifier: str | int | None = "pending",
) -> Any:
    """
    Asynchronously calls a given smart contract function using its name and parameters, and returns the result.
    """
    contract_function = getattr(contract.functions, function_name)
    return await contract_function(*params or []).call(
        block_identifier=block_identifier
    )
