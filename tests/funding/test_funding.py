import pytest
from eth_account.signers.local import LocalAccount

from aave_umbrella.config.addresses import USDC_ADDRESS
from aave_umbrella.contracts.erc20 import ERC20
from aave_umbrella.forks.funding import fund_user
from aave_umbrella.providers.web3_client import AsyncW3
from aave_umbrella.utils.math import amount_to_small_units
from tests.helpers.helper import USDC_WHALE_TEST


@pytest.mark.asyncio
async def test_fund_user(web3: AsyncW3, user_account: LocalAccount) -> None:
    """Test funding a user from whale account"""
    # Arrange
    usdc_contract = ERC20(web3, USDC_ADDRESS)
    current_expected_amount = 0
    expected_amount_int = 1000
    expected_amount = amount_to_small_units(expected_amount_int, 6)

    current_balance = await usdc_contract.balance_of(user_account.address)
    assert current_balance == current_expected_amount

    token_to_wallets = {
        USDC_ADDRESS: (
            USDC_WHALE_TEST,
            expected_amount_int,
        ),
    }

    success = await fund_user(web3, user_account, token_to_wallets)

    assert success is True
    final_balance = await usdc_contract.balance_of(user_account.address)
    assert final_balance == expected_amount
