import pytest

from aave_umbrella.actions.deposit import deposit
from aave_umbrella.config.addresses import (
    USDC_ADDRESS,
    USDC_STAKE_TOKEN,
)
from aave_umbrella.contracts.batch_helper import IOData
from aave_umbrella.contracts.erc20 import ERC20
from aave_umbrella.forks.funding import fund_user
from aave_umbrella.utils.math import balance_to_decimal


@pytest.mark.asyncio
async def test_deposit(web3, user_account):
    """Test deposit function of BatchHelper contract"""
    stake_token_address = USDC_STAKE_TOKEN
    edge_token_address = USDC_ADDRESS
    stake_stata_token = ERC20(web3, stake_token_address)
    deposit_amount = balance_to_decimal(500, 6)  # 500 USDC

    # Fund the user account
    await fund_user(web3, user_account)

    # Get current Umbrella shares before staking (should be equal to 0)
    current_shares_balance = await stake_stata_token.balance_of(
        wallet_address=user_account.address
    )

    assert current_shares_balance == 0

    deposit_status = await deposit(
        web3=web3,
        user_account=user_account,
        params=IOData(
            stake_token=web3.to_checksum_address(stake_token_address),
            edge_token=web3.to_checksum_address(edge_token_address),
            value=int(deposit_amount),
        ),
    )

    assert deposit_status is True

    # Verify shares in user account
    final_shares_balance = await stake_stata_token.balance_of(
        wallet_address=user_account.address, readable=True
    )

    assert final_shares_balance > current_shares_balance
