from typing import NamedTuple, cast

from eth_account.signers.local import LocalAccount
from web3.types import TxReceipt

from aave_umbrella.abi.stake_token_impl import STAKE_TOKEN_IMPL_ABI
from aave_umbrella.contracts.base import BaseContract
from aave_umbrella.providers.web3_client import AsyncW3


class CooldownSnapshot(NamedTuple):
    amount: int
    end_of_cooldown: int
    withdrawal_window: int


class StakeToken(BaseContract):
    def __init__(self, web3: AsyncW3, address: str):
        super().__init__(web3, address, STAKE_TOKEN_IMPL_ABI)

    async def approve(self, signer: LocalAccount, spender: str, value: int) -> TxReceipt:
        return await self.tx("approve", signer, self.web3.to_checksum_address(spender), value)

    async def cooldown(self, signer: LocalAccount) -> TxReceipt:
        return await self.tx("cooldown", signer)

    async def get_staker_cooldown(self, user_address: str) -> CooldownSnapshot:
        res = cast(
            tuple[int, int, int],
            await self.call("getStakerCooldown", user_address),
        )
        return CooldownSnapshot(*res)
