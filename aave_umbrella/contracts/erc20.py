from eth_account.signers.local import LocalAccount
from web3 import AsyncWeb3

from aave_umbrella.abi.erc20_abi import ERC20_ABI
from aave_umbrella.contracts.base import BaseContract


class ERC20(BaseContract):
    def __init__(self, web3: AsyncWeb3, address: str):
        super().__init__(web3, address, ERC20_ABI)

    async def balance_of(self, wallet_address: str) -> int:
        return await self.call(
            "balanceOf", self.web3.to_checksum_address(wallet_address)
        )

    async def decimals(self) -> int:
        return await self.call("decimals")

    async def transfer(self, signer: LocalAccount | str, to: str, amount: int):
        return await self.tx(
            "transfer", signer, self.web3.to_checksum_address(to), amount
        )

    async def approve(self, signer: LocalAccount | str, spender: str, amount: int):
        return await self.tx(
            "approve", signer, self.web3.to_checksum_address(spender), amount
        )
