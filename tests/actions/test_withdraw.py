import pytest
from eth_account.signers.local import LocalAccount

from aave_umbrella.config.addresses import (
    BATCH_HELPER_ADDRESS,
    USDC_ADDRESS,
    USDC_UMBRELLA_STAKE_TOKEN,
)
from aave_umbrella.contracts.batch_helper import BatchHelper, IOData
from aave_umbrella.contracts.erc20 import ERC20
from aave_umbrella.contracts.stake_token import StakeToken
from aave_umbrella.providers.web3_client import AsyncW3
from aave_umbrella.utils.math import amount_to_small_units
from tests.helpers.helper import back_to_the_future, fund_and_deposit


@pytest.mark.asyncio
async def test_redeem(web3: AsyncW3, user_account: LocalAccount) -> None:
    """Test redeem function"""
    stake_token_address = USDC_UMBRELLA_STAKE_TOKEN
    edge_token_address = USDC_ADDRESS
    stake_token_contract = StakeToken(web3, stake_token_address)
    batch_helper_contract = BatchHelper(web3)

    shares_balance = await fund_and_deposit(web3, user_account)

    # Verify cooldown info before initiating cooldown
    before_cooldown = await stake_token_contract.get_staker_cooldown(user_address=user_account.address)

    assert before_cooldown == (0, 0, 0)

    # Initiate cooldown
    await stake_token_contract.cooldown(user_account)

    (
        cooldown_expected_shares,
        end_of_cooldown,
        _,
    ) = await stake_token_contract.get_staker_cooldown(user_address=user_account.address)

    assert shares_balance == cooldown_expected_shares

    # Move time forward to after the cooldown period
    await back_to_the_future(web3, end_of_cooldown)

    # Approve the batch helper to redeem stake tokens
    await stake_token_contract.approve(
        signer=user_account,
        spender=BATCH_HELPER_ADDRESS,
        value=cooldown_expected_shares,
    )

    # Redeem stake tokens
    tx_receipt = await batch_helper_contract.redeem(
        signer=user_account,
        params=IOData(
            stake_token=web3.to_checksum_address(stake_token_address),
            edge_token=web3.to_checksum_address(edge_token_address),
            value=cooldown_expected_shares,
        ),
    )
    assert tx_receipt["status"] == 1

    stake_stata_contract = ERC20(web3, stake_token_address)
    stake_stata_balance = await stake_stata_contract.balance_of(wallet_address=user_account.address)

    edge_token_contract = ERC20(web3, edge_token_address)
    edge_token_balance = await edge_token_contract.balance_of(wallet_address=user_account.address)

    assert stake_stata_balance == 0
    edge_token_decimal = await edge_token_contract.decimals()
    assert edge_token_balance >= amount_to_small_units(1000, edge_token_decimal)  # 500 initial + 500 redeemed
