from eth_account.signers.local import LocalAccount

from aave_umbrella.actions.deposit import deposit
from aave_umbrella.config.addresses import USDC_ADDRESS, USDC_UMBRELLA_STAKE_TOKEN
from aave_umbrella.contracts.batch_helper import IOData
from aave_umbrella.contracts.erc20 import ERC20
from aave_umbrella.forks.funding import fund_user
from aave_umbrella.providers.web3_client import AsyncW3
from aave_umbrella.utils.math import amount_to_small_units


async def fund_and_deposit(web3: AsyncW3, user_account: LocalAccount) -> int:
    stake_token_address = USDC_UMBRELLA_STAKE_TOKEN
    edge_token_address = USDC_ADDRESS
    deposit_amount = amount_to_small_units(500, 6)  # 500 USDC
    stake_token_contract = ERC20(web3, stake_token_address)

    # Fund the user account
    await fund_user(web3, user_account)

    # Deposit assets into the stake token
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
    balance = await stake_token_contract.balance_of(wallet_address=user_account.address)

    return balance


async def back_to_the_future(web3: AsyncW3, target_timestamp: int) -> None:
    """
    Advances EVM time to after the cooldown period.
    :param target_timestamp:
    :param web3:
    :return:
    """
    # Simulate waiting for the cooldown period to pass
    delta = await compute_delta_to_redeemable(web3=web3, target_timestamp=target_timestamp)

    await web3.provider.make_request("evm_increaseTime", [delta])  # around 20 days
    await web3.provider.make_request("evm_mine", [])

    # Check that we are in the future
    block = await web3.eth.get_block("latest")
    assert block["timestamp"] >= target_timestamp


async def compute_delta_to_redeemable(
    web3: AsyncW3,
    target_timestamp: int,
    buffer: int = 1,
) -> int:
    """
    Computes how many seconds to advance EVM time so that
    block.timestamp >= endOfCooldown (inside withdrawal window).
    :param web3: Web3 connection
    :param target_timestamp: Timestamp when target ends
    :param buffer: Additional buffer time in seconds
    :return: Number of seconds to advance EVM time
    """

    block = await web3.eth.get_block("latest")
    current_ts = block["timestamp"]
    target_ts = target_timestamp + buffer

    delta = target_ts - current_ts

    return max(delta, 0)
