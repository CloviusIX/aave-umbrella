from eth_account.signers.local import LocalAccount
from web3.types import TxReceipt

from aave_umbrella.abi.erc20_abi import ERC20_ABI
from aave_umbrella.contracts.base import BaseContract
from aave_umbrella.providers.web3_client import AsyncW3


class ERC20(BaseContract):
    def __init__(self, web3: AsyncW3, address: str):
        super().__init__(web3, address, ERC20_ABI)

    async def balance_of(self, wallet_address: str) -> int:
        balance = await self.call("balanceOf", self.web3.to_checksum_address(wallet_address))
        return int(balance)

    async def decimals(self) -> int:
        decimals = await self.call("decimals")
        return int(decimals)

    async def transfer(self, signer: LocalAccount | str, to: str, amount: int) -> TxReceipt:
        return await self.tx("transfer", signer, self.web3.to_checksum_address(to), amount)

    async def approve(self, signer: LocalAccount, spender: str, amount: int) -> TxReceipt:
        return await self.tx("approve", signer, self.web3.to_checksum_address(spender), amount)
