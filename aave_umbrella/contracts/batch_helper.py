from dataclasses import astuple, dataclass

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3.types import TxReceipt

from aave_umbrella.abi.batch_helper_abi import BATCH_HELPER_ABI
from aave_umbrella.config.addresses import BATCH_HELPER_ADDRESS
from aave_umbrella.contracts.base import BaseContract
from aave_umbrella.providers.web3_client import AsyncW3


@dataclass
class IOData:
    stake_token: ChecksumAddress  # Umbrella vault address
    edge_token: ChecksumAddress  # token | aToken | stataToken address to deposit
    value: int  # small units


class BatchHelper(BaseContract):
    def __init__(self, web3: AsyncW3):
        super().__init__(web3, BATCH_HELPER_ADDRESS, BATCH_HELPER_ABI)

    async def deposit(self, signer: LocalAccount, params: IOData) -> TxReceipt:
        params_tuple = astuple(params)
        return await self.tx("deposit", signer, params_tuple)

    async def redeem(self, signer: LocalAccount, params: IOData) -> TxReceipt:
        params_tuple = astuple(params)
        return await self.tx("redeem", signer, params_tuple)
