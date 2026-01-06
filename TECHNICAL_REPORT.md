# Φ-Chain Technical Report: Mainnet Implementation

## 1. System Overview
The Φ-Chain Mainnet is a high-performance blockchain implemented in Python, with a responsive web-based UI and a robust validator network. The system is designed to be self-evolving, with autonomous research aggregation and update mechanisms.

## 2. Core Engine (`phi_chain.py`)
The core logic is contained in `phi_chain.py`, which integrates:
- **Fibonacci Utility Class**: For all mathematical derivations.
- **Genesis Parameters**: Derived from Fibonacci indices (F_6, F_18, F_20, etc.).
- **PhiState Class**: Implements the Q-Matrix state transition logic.
- **PhiBlock & PhiTransaction**: Optimized for OPEVM and Pipelined BFT.

## 3. Wallet API (`api/wallet_api.py`)
A FastAPI-based backend providing RESTful endpoints for wallet operations, staking, mining, and blockchain queries. It includes WebSocket support for real-time updates.

### Key Endpoints:
- **Wallet**: Balance, transactions, send operations.
- **Staking**: Validator registration, rewards tracking.
- **Mining**: PoC mining interface, block submission.
- **Blockchain**: Chain info, block queries, validation.

## 4. Validator Network (`validator_node.py`)
Validators are the backbone of Φ-Chain security. The `validator_node.py` module provides a complete implementation of a validator node.
- **Key Generation**: Uses `secrets` and `hashlib` for secure key derivation.
- **Node Configuration**: Automated setup via `tools/deploy_mainnet.py`.
- **Consensus**: Implements Fibonacci Byzantine Agreement (FBA) with a finality threshold of F_15 (610).

## 5. Wallet & UI (`wallet_mainnet.html`)
The Φ-Chain Wallet (`wallet_mainnet.html`) provides:
- **Mainnet Connectivity**: Real-time balance and transaction tracking.
- **PoC Mining**: An interactive interface for Proof-of-Coherence mining.
- **Staking**: Fibonacci-weighted staking management.
- **Responsive Design**: Optimized for both desktop and mobile devices.

## 6. Deployment & Monitoring
- **Mainnet Deployment**: Handled by `tools/deploy_mainnet.py`, which initializes the genesis block and validator network.
- **Real-time Dashboard**: `dashboard.html` provides live metrics on block height, validator status, and consensus health.

## 7. Self-Evolving Intelligence
The system includes a `research_aggregator.py` script scheduled to run every 24 hours. This script monitors external repositories (Ethereum, Solana, Bitcoin) for innovations and logs potential improvements for autonomous integration into the Φ-Chain ecosystem.

## 8. Mathematical Verification
All system parameters have been verified to align with the Golden Ratio (Φ) and the Fibonacci sequence. The state transition matrix \( Q \) has been tested to ensure deterministic evolution of the chain's metrics.

## 9. Testing and Validation
A comprehensive testing suite (`tests/test_phi_chain.py`) has been developed to ensure the correctness and reliability of the Φ-Chain implementation. The tests cover all aspects of the core engine, from Fibonacci utilities to consensus mechanisms.

### Test Coverage:
- **Fibonacci Utilities**: Tests for the Fibonacci sequence, Golden Ratio calculation, and Fibonacci number detection.
- **Block and Transaction Tests**: Tests for block creation, hashing, and validation.
- **Consensus Tests**: Tests for the PoC scoring, FBA voting, and validator selection.
- **Blockchain Tests**: Tests for mining, validation, and balance calculation.
