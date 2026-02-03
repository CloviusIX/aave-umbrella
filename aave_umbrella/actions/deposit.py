from dataclasses import astuple

from eth_account.signers.local import LocalAccount

from aave_umbrella.config.addresses import BATCH_HELPER_ADDRESS, GHO_UMBRELLA_STAKE_TOKEN
from aave_umbrella.contracts.batch_helper import BatchHelper, IOData
from aave_umbrella.contracts.erc20 import ERC20
from aave_umbrella.providers.web3_client import AsyncW3


async def deposit(
    web3: AsyncW3,
    user_account: LocalAccount,
    params: IOData,
    spender: str = BATCH_HELPER_ADDRESS,
) -> bool:
    """
    Deposit assets into Aave StakeToken
    :param web3: Web3 connection
    :param user_account: User account performing the deposit
    :param params: IOData object containing stake_token, edge_token, and value
    :param spender: The address allowed to spend the edge token (usually the BatchHelper contract)
    :return: True if deposit succeeded
    """

    stake_token, edge_token, amount = astuple(params)

    if stake_token == GHO_UMBRELLA_STAKE_TOKEN:
        raise NotImplementedError("GHO deposits are not supported yet.")
        # Call depositWithPermit() on GHO stake token

    token_contract = ERC20(web3, edge_token)
    batch_helper_contract = BatchHelper(web3)

    # Approve the batch helper to deposit the asset
    await token_contract.approve(signer=user_account, spender=spender, amount=amount)

    # Deposit assets into the stake token
    tx_receipt = await batch_helper_contract.deposit(signer=user_account, params=params)
    return tx_receipt["status"] == 1
