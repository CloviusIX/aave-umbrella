REWARDS_CONTROLLER_ABI = """[
    {
        "inputs": [
            {"internalType": "address", "name": "asset", "type": "address"},
            {"internalType": "address", "name": "user", "type": "address"}
        ],
        "name": "calculateCurrentUserRewards",
        "outputs": [
            {"internalType": "address[]", "name": "", "type": "address[]"},
            {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "asset", "type": "address"},
            {"internalType": "address", "name": "reward", "type": "address"}
        ],
        "name": "calculateCurrentEmission",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "asset", "type": "address"},
            {"internalType": "address", "name": "receiver", "type": "address"}
        ],
        "name": "claimAllRewards",
        "outputs": [
            {"internalType": "address[]", "name": "", "type": "address[]"},
            {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]"""
