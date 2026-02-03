import json

from eth_account.signers.local import LocalAccount
from web3 import AsyncWeb3


class BaseContract:
    def __init__(self, web3: AsyncWeb3, address: str, abi: str):
        self.web3 = web3
        self.contract = web3.eth.contract(
            address=web3.to_checksum_address(address),
            abi=json.loads(abi),
        )

    async def call(
        self, function_name: str, *params, block_identifier: str | int | None = "latest"
    ):
        return await getattr(self.contract.functions, function_name)(
            *params or []
        ).call(block_identifier=block_identifier)

    async def tx(
        self, function_name: str, signer: LocalAccount | str, *params, value=0
    ):
        if isinstance(signer, LocalAccount):
            # Normal signing with private key
            sent_tx = await getattr(self.contract.functions, function_name)(
                *params or []
            ).transact(
                {
                    "chainId": await self.web3.eth.chain_id,
                    "from": signer.address,
                    "nonce": await self.web3.eth.get_transaction_count(signer.address),
                    "value": value,
                }
            )

            return await self.web3.eth.wait_for_transaction_receipt(sent_tx)

        else:
            # Impersonated account (just use the address string)
            sent_tx = await getattr(self.contract.functions, function_name)(
                *params or []
            ).transact({"from": self.web3.to_checksum_address(signer)})

            return await self.web3.eth.wait_for_transaction_receipt(sent_tx)
