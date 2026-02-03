from dataclasses import astuple

from eth_account.signers.local import LocalAccount

from aave_umbrella.config.addresses import BATCH_HELPER_ADDRESS
from aave_umbrella.contracts.batch_helper import BatchHelper, IOData
from aave_umbrella.contracts.stake_token import StakeToken
from aave_umbrella.providers.web3_client import AsyncW3


async def cooldown(web3: AsyncW3, user_account: LocalAccount, stake_token: str) -> bool:
    stake_token_contract = StakeToken(web3, stake_token)
    tx_receipt = await stake_token_contract.cooldown(signer=user_account)
    return tx_receipt["status"] == 1


async def redeem(
    web3: AsyncW3,
    user_account: LocalAccount,
    redeem_params: IOData,
    spender: str = BATCH_HELPER_ADDRESS,
) -> bool:
    """
    Redeem assets from Aave StakeToken
    :param web3: Web3 connection
    :param user_account: User account performing the redeem
    :param redeem_params: IOData object containing stake_token, edge_token, and value
    :param spender: Spender address for approval (default is BatchHelper)
    :return: True if redeem succeeded
    """
    stake_token, edge_token, amount = astuple(redeem_params)

    stake_token_contract = StakeToken(web3, stake_token)
    batch_helper_contract = BatchHelper(web3)

    # Approve the batch helper to redeem the stake token
    await stake_token_contract.approve(signer=user_account, spender=spender, value=amount)

    tx_receipt = await batch_helper_contract.redeem(signer=user_account, params=redeem_params)

    return tx_receipt["status"] == 1
