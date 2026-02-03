import pytest
from eth_account.signers.local import LocalAccount

from aave_umbrella.actions.deposit import deposit
from aave_umbrella.config.addresses import (
    USDC_ADDRESS,
    USDC_UMBRELLA_STAKE_TOKEN,
)
from aave_umbrella.contracts.batch_helper import IOData
from aave_umbrella.contracts.erc20 import ERC20
from aave_umbrella.forks.funding import fund_user
from aave_umbrella.providers.web3_client import AsyncW3
from aave_umbrella.utils.math import (
    amount_to_small_units,
)


@pytest.mark.asyncio
async def test_deposit(web3: AsyncW3, user_account: LocalAccount) -> None:
    """Test deposit function of BatchHelper contract"""
    stake_token_address = USDC_UMBRELLA_STAKE_TOKEN
    edge_token_address = USDC_ADDRESS
    stake_token_contract = ERC20(web3, stake_token_address)
    deposit_amount = amount_to_small_units(500, 6)  # 500 USDC

    # Fund the user account
    await fund_user(web3, user_account)

    # Get current Umbrella shares before staking (should be equal to 0)
    current_shares_balance = await stake_token_contract.balance_of(wallet_address=user_account.address)

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
    final_shares_balance = await stake_token_contract.balance_of(wallet_address=user_account.address)

    assert final_shares_balance > current_shares_balance
