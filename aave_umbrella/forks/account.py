from eth_account import Account
from web3 import AsyncWeb3

# Anvil's default accounts are deterministic and publicly known
ANVIL_PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"


async def get_user_account(web3: AsyncWeb3):
    """
    Get user account from Anvil accounts
    :param web3: Web3 connection
    :return: LocalAccount signer
    """
    accounts = await web3.eth.accounts

    if not accounts:
        raise ValueError("No accounts available")

    signer = Account.from_key(ANVIL_PRIVATE_KEY)

    # Verify the address matches
    assert signer.address == accounts[0], "Address mismatch"

    return signer
