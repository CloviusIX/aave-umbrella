from eth_account.signers.local import LocalAccount
from web3 import AsyncWeb3

from aave_umbrella.abi.rewards_controller import REWARDS_CONTROLLER_ABI
from aave_umbrella.config.addresses import REWARDS_CONTROLLER_ADDRESS
from aave_umbrella.contracts.base import BaseContract


class RewardsController(BaseContract):
    def __init__(self, web3: AsyncWeb3):
        super().__init__(web3, REWARDS_CONTROLLER_ADDRESS, REWARDS_CONTROLLER_ABI)

    async def calculate_current_user_rewards(self, stake_token: str, user_address: str):
        return await self.call("calculateCurrentUserRewards", stake_token, user_address)

    async def calculate_current_emission(self, stake_token: str, reward_address: str):
        return await self.call("calculateCurrentEmission", stake_token, reward_address)

    async def claim_all_rewards(
        self, signer: LocalAccount, stake_token: str, receiver: str
    ):
        return await self.tx("claimAllRewards", signer, stake_token, receiver)
