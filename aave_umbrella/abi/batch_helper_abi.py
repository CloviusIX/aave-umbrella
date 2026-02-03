BATCH_HELPER_ABI = """[
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "contract IStakeToken",
                        "name": "stakeToken",
                        "type": "address"
                    },
                    {"internalType": "address", "name": "edgeToken", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"}
                ],
                "internalType": "struct IUmbrellaBatchHelper.IOData",
                "name": "io",
                "type": "tuple"
            }
        ],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "contract IStakeToken",
                        "name": "stakeToken",
                        "type": "address"
                    },
                    {"internalType": "address", "name": "edgeToken", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"}
                ],
                "internalType": "struct IUmbrellaBatchHelper.IOData",
                "name": "io",
                "type": "tuple"
            }
        ],
        "name": "redeem",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]"""
