import pytest

from aave_umbrella.actions.harvest import (
    calculate_current_user_rewards,
    claim_all_rewards,
)
from aave_umbrella.config.addresses import USDC_STAKE_TOKEN
from aave_umbrella.contracts.erc20 import ERC20
from tests.helpers.helper import back_to_the_future, fund_and_deposit


@pytest.mark.asyncio
async def test_harvest(web3, user_account):
    """Test harvest function"""
    stake_token_address = USDC_STAKE_TOKEN
    stake_token_address_checksum = web3.to_checksum_address(stake_token_address)
    user_address_checksum = user_account.address

    await fund_and_deposit(web3, user_account)

    # Calculate current rewards before time travel
    current_rewards = await calculate_current_user_rewards(
        web3=web3,
        stake_token=stake_token_address_checksum,
        user_address=user_address_checksum,
    )

    has_no_reward = all(amount == 0 for amount in current_rewards[1])

    assert has_no_reward is True

    # Move time forward to accrue rewards
    await back_to_the_future(
        web3,
        target_timestamp=1833204488,  # 2 years from now
    )  # Move time forward to accrue rewards

    # Calculate current rewards after time travel
    new_rewards = await calculate_current_user_rewards(
        web3=web3,
        stake_token=stake_token_address_checksum,
        user_address=user_address_checksum,
    )

    has_rewards = all(amount > 0 for amount in new_rewards[1])
    assert len(new_rewards) and has_rewards is True

    # Claim all rewards
    is_success = await claim_all_rewards(
        web3,
        user_account,
        stake_token=stake_token_address_checksum,
        receiver=user_address_checksum,
    )

    assert is_success is True

    # Verify that the user received the rewards
    reward_tokens, reward_amounts = new_rewards
    for address, amount in zip(reward_tokens, reward_amounts):
        reward_contract = ERC20(web3, address)
        balance = await reward_contract.balance_of(user_address_checksum)
        assert balance == amount

    # Calculate current rewards after claiming
    rewards_after_claim = await calculate_current_user_rewards(
        web3=web3,
        stake_token=stake_token_address_checksum,
        user_address=user_address_checksum,
    )

    has_no_reward_after_claim = all(amount == 0 for amount in rewards_after_claim[1])
    assert has_no_reward_after_claim is True
