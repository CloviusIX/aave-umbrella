import asyncio

from aave_umbrella.forks.account import get_user_account
from aave_umbrella.forks.funding import fund_user
from aave_umbrella.providers.web3_client import build_web3_connection


async def main() -> None:
    web3 = await build_web3_connection()
    user_account = await get_user_account(web3)
    await fund_user(web3, user_account)


if __name__ == "__main__":
    asyncio.run(main())
