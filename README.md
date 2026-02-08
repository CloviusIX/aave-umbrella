# Aave Umbrella — Forked Mainnet Integration

This project demonstrates programmatic interaction with **Aave Umbrella** contracts using a **local fork of Ethereum mainnet**.
All protocol calls are executed against real deployed contracts, using forked state for accuracy and realism.

📘 **Technical Analysis & Documentation**

A detailed technical analysis of **Aave Umbrella**, including protocol architecture, contract flows, risk analysis, and forked mainnet interactions, is available here:

👉 [https://loris-leonard.gitbook.io/aave-umbrella-technical-analysis/](https://loris-leonard.gitbook.io/aave-umbrella-technical-analysis/)

This repository complements the documentation with executable code and real on-chain interactions.

---

## Prerequisites

Make sure the following are installed on your machine:

* **Python 3.14** (required Python version)
* **Make** (to run the project Makefile)
* **Docker Desktop** (includes Docker and Docker Compose)

---

## Project Setup

Clone the repository and install dependencies by running:

```bash
make
```

### IDE Configuration

After installation, configure your IDE to use the virtual environment created in the project root.

The Python interpreter is located at:

```
.venv/bin/python3.14
```

### Local Ethereum Fork

This project uses **Anvil** to run a local fork of **Ethereum mainnet** in Docker.

Start the environment with:

```bash
make docker-setup
```

This command will:

* create a `.env` file from `.env.example` with default environment variable values
* pull the required Docker images
* start the Anvil container in the background

The local RPC endpoint will be available at:

```
http://127.0.0.1:8545
```

The fork runs at a **fixed block height** to guarantee deterministic results across runs.

> ℹ️ You can change the Ethereum RPC URL in the .env file if you prefer using your own (Alchemy, Infura, local node, etc.). If you modify these values, restart the Docker environment for the changes to take effect.


### Restarting the environment

If the fork needs to be reset or the .env variables have been updated, restart the environment with:

```bash
make docker-restart
```
This will recreate the containers and start a fresh fork.

---

## Running the Notebook

Once Anvil is running, start Jupyter and open the following notebook:

```
05_forked_mainnet_integration.ipynb
```

This notebook demonstrates:

* Depositing into Aave Umbrella stake tokens
* Reward accrual
* Claiming rewards
* Redeeming positions
* Reading on-chain state directly from forked mainnet contracts

Time manipulation is performed via `evm_increaseTime` and `evm_mine` on the local fork to simulate reward accrual and cooldown periods.

All interactions use real contract ABIs and addresses against forked state.

### Funding Test Account

For demonstration purposes, the project impersonates a **USDC whale account** holding **over 20 million USDC** on mainnet.

Using the forked environment, this whale account is used to fund the user account with sufficient USDC balances, enabling realistic deposit, staking, reward, and withdrawal flows.

This approach mirrors real on-chain conditions while keeping all interactions local and deterministic.

---

## Code Structure & Design

The notebook focuses on visualization and interactive exploration of the protocol,
while **all core logic is implemented in the project codebase and covered by tests.**

### Actions

All protocol operations are implemented in:

```
aave_umbrella/actions
```

This includes:

* **Deposit**
* **Harvest / claim rewards**
* **Withdraw / redeem**

Each action maps directly to on-chain contract calls and is reused across tests and notebooks to ensure consistency and correctness.

---

### Contract Abstractions

The project defines a set of **BaseContract** abstractions to model on-chain contracts as first-class Python objects.

These base classes:

* Wrap contract addresses and ABIs
* Expose contract functions as typed, reusable methods
* Simplify interaction with multiple Umbrella-related contracts
* Make on-chain reads and writes explicit and easy to trace

This approach allows contract entities to be reproduced programmatically and interacted with in a clear, composable way, while staying close to actual on-chain behavior.

---

### Reusability

The Jupyter notebook **reuses the same action and contract layers as the test suite**, with additional logging and formatted output for clarity.

This design avoids duplicated logic and ensures that notebook demonstrations accurately reflect production-grade interactions.

---
Enjoy exploring the project 🚀