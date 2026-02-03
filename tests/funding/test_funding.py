import pytest
from eth_account import Account

from aave_umbrella.contracts.erc20 import ERC20
from aave_umbrella.forks.funding import USDC_ADDRESS, fund_user
from aave_umbrella.utils.math import balance_to_decimal


@pytest.mark.asyncio
async def test_fund_user(web3):
    """Test funding a user from whale account"""
    # Arrange
    user_account = Account.create()
    usdc_contract = ERC20(web3, USDC_ADDRESS)
    current_expected_amount = 0
    expected_amount_int = 1000
    expected_amount = balance_to_decimal(expected_amount_int, 6)

    current_balance = await usdc_contract.balance_of(user_account.address)
    assert current_balance == current_expected_amount

    token_to_wallets = {
        USDC_ADDRESS: (
            "0x3757c6490019b6c9b0b38c3b89fdf83155c2661f",
            expected_amount_int,
        ),
    }

    success = await fund_user(web3, user_account, token_to_wallets)

    assert success is True
    final_balance = await usdc_contract.balance_of(user_account.address)
    assert final_balance == expected_amount
