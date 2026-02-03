from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import AsyncWeb3

from aave_umbrella.contracts.rewards_controller import RewardsController


async def claim_all_rewards(
    web3: AsyncWeb3,
    user_account: LocalAccount,
    stake_token: ChecksumAddress,
    receiver: ChecksumAddress,
) -> bool:
    """
    Claim all rewards for a user for stake token
    :param web3: Web3 connection
    :param user_account: User account performing the redeem
    :param stake_token: Stake token address
    :param receiver: Address to receive the rewards
    :return: True if claim succeeded
    """
    rewards_contract = RewardsController(web3=web3)
    tx_receipt = await rewards_contract.claim_all_rewards(
        signer=user_account, stake_token=stake_token, receiver=receiver
    )
    return tx_receipt["status"] == 1


async def calculate_current_user_rewards(
    web3: AsyncWeb3, stake_token: ChecksumAddress, user_address: ChecksumAddress
):
    """
    Calculate the current rewards for a user for stake token
    :param web3: Web3 connection
    :param stake_token: Stake token address
    :param user_address: User address performing the redeem
    :return: Current rewards amount
    """
    rewards_contract = RewardsController(web3=web3)
    current_rewards = await rewards_contract.calculate_current_user_rewards(
        stake_token, user_address
    )
    return current_rewards


async def calculate_current_emission(
    web3: AsyncWeb3, stake_token: ChecksumAddress, reward_address: ChecksumAddress
) -> int:
    """
    Calculate the current emission for a stake token and reward token
    :param web3: Web3 connection
    :param stake_token: Stake token address
    :param reward_address: Reward token address
    :return: Current emission amount
    """
    rewards_contract = RewardsController(web3=web3)
    current_emission = await rewards_contract.calculate_current_emission(
        stake_token, reward_address
    )
    return current_emission
