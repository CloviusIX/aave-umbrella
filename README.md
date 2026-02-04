# Aave Umbrella — Forked Mainnet Integration

📘 **Technical Analysis & Documentation**

A detailed technical analysis of **Aave Umbrella**, including protocol architecture, contract flows, risk analysis, and forked mainnet interactions, is available here:

👉 [https://loris-leonard.gitbook.io/aave-umbrella-technical-analysis/](https://loris-leonard.gitbook.io/aave-umbrella-technical-analysis/)

This repository complements the documentation with executable code and real on-chain interactions.

---

## Overview

This project demonstrates programmatic interaction with **Aave Umbrella** contracts using a **local fork of Ethereum mainnet**.
All protocol calls are executed against real deployed contracts, using forked state for accuracy and realism.

---

## Prerequisites

Make sure the following are installed on your machine:

* **Python 3.14**
* **Make** (required to run the project Makefile)
* **Anvil** (Foundry local node)
  Installation guide: [https://getfoundry.sh/anvil/overview/](https://getfoundry.sh/anvil/overview/)

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

### Forking Ethereum Mainnet

Before running the notebook, start a local fork of Ethereum mainnet using **Anvil**:

```bash
anvil --fork-url https://ethereum.reth.rs/rpc --fork-block-number 24383419
```

This forks Ethereum mainnet at a fixed block height to ensure deterministic behavior across runs.

> ℹ️ The RPC URL is provided as a convenience. It can be replaced with any Ethereum mainnet RPC endpoint (e.g. Infura, Alchemy, local node) according to your preference.

**Leave this process running in a separate terminal.**

### Environment Configuration

The project expects a local Ethereum RPC endpoint provided by Anvil.

Create a .env file at the root of the repository and add the following variable:

```
FORK_URL=http://127.0.0.1:8545
```

This value should point to the RPC endpoint of your running Anvil fork.

> ℹ️ If you start Anvil on a different host or port, update FORK_URL accordingly.
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