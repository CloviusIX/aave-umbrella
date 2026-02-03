STAKE_TOKEN_IMPL_ABI = """[
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "cooldown",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "getStakerCooldown",
        "outputs": [
            {
                "components": [
                    {"internalType": "uint192", "name": "amount", "type": "uint192"},
                    {
                        "internalType": "uint32",
                        "name": "endOfCooldown",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "withdrawalWindow",
                        "type": "uint32"
                    }
                ],
                "internalType": "struct IERC4626StakeToken.CooldownSnapshot",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]"""
