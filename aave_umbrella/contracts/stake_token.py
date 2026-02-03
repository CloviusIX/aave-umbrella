from eth_account.signers.local import LocalAccount
from web3 import AsyncWeb3

from aave_umbrella.abi.stake_token_impl import STAKE_TOKEN_IMPL_ABI
from aave_umbrella.contracts.base import BaseContract


class StakeToken(BaseContract):
    def __init__(self, web3: AsyncWeb3, address: str):
        super().__init__(web3, address, STAKE_TOKEN_IMPL_ABI)

    async def approve(self, signer: LocalAccount | str, spender: str, value: int):
        return await self.tx(
            "approve", signer, self.web3.to_checksum_address(spender), value
        )

    async def cooldown(self, signer: LocalAccount):
        return await self.tx("cooldown", signer)

    async def get_staker_cooldown(self, user_address: str):
        return await self.call("getStakerCooldown", user_address)
