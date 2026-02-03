from dataclasses import astuple, dataclass

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import AsyncWeb3

from aave_umbrella.abi.batch_helper_abi import BATCH_HELPER_ABI
from aave_umbrella.config.addresses import BATCH_HELPER_ADDRESS
from aave_umbrella.contracts.base import BaseContract


@dataclass
class IOData:
    stake_token: ChecksumAddress  # Umbrella vault address
    edge_token: ChecksumAddress  # token | aToken | StateToken address to deposit
    value: int  # small units


class BatchHelper(BaseContract):
    def __init__(self, web3):
        super().__init__(web3, BATCH_HELPER_ADDRESS, BATCH_HELPER_ABI)

    async def deposit(self, signer: LocalAccount, params: IOData):
        params_tuple = astuple(params)
        return await self.tx("deposit", signer, params_tuple)
