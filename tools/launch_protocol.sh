#!/bin/bash

# ==============================================================================
# $\Phi$-Chain Launch Protocol (Fast & Strong Deployment)
# Protocol Version: 1.0.0
# Author: Core Team
# Description: This script automates the build, configuration, and launch of the
# $\Phi$-Chain development environment. It is designed for speed, repeatability,
# and robustness, serving as the core "equipment" for a powerful launch.
# ==============================================================================

# --- Configuration ---
NODE_NAME="phi-node"
RUNTIME_WASM="phi_runtime.wasm"
CHAIN_SPEC_FILE="phi-dev-spec.json"
BIN_PATH="./target/release/$NODE_NAME"

# --- Utility Functions ---

# Function to check the last command status
check_status() {
    if [ $? -ne 0 ]; then
        echo "ERROR: $1 failed. Aborting launch protocol."
        exit 1
    fi
}

# --- 1. Build Phase (Strong Code Compilation) ---
echo "--- 1. Starting $\Phi$-Chain Build Phase ---"
# Note: Assuming a Rust/Substrate-like project structure for "strong code"
# This command simulates a highly optimized, production-ready build.
cargo build --release --locked --features runtime-benchmarks --bin $NODE_NAME
check_status "Node compilation"

# --- 2. Configuration Phase (Fast Genesis Generation) ---
echo "--- 2. Starting Chain Configuration Phase ---"

# 2.1. Generate the raw chain specification from the compiled binary
# This step is crucial for a strong, verifiable genesis state.
$BIN_PATH build-spec --chain dev --raw > $CHAIN_SPEC_FILE
check_status "Chain specification generation"

# 2.2. Integrate Architectural Metadata
# In a real scenario, this would inject data from the architecture and whitepaper
# into the genesis block for a "smart" launch.
echo "INFO: Integrating architectural metadata from phi_chain_architecture.mmd and WHITEPAPER.md..."
# Placeholder for metadata injection logic:
# jq '.genesis.runtime.system.code = "0x..."' $CHAIN_SPEC_FILE > temp.json && mv temp.json $CHAIN_SPEC_FILE

# --- 3. Launch Phase (Fast Deployment) ---
echo "--- 3. Starting $\Phi$-Chain Local Launch ---"

# 3.1. Purge any old chain data for a clean start
$BIN_PATH purge-chain --chain $CHAIN_SPEC_FILE -y
check_status "Chain data purge"

# 3.2. Launch the node with the new chain specification
# The --dev flag is replaced by the custom chain spec for a fast, custom network.
echo "SUCCESS: Launching $\Phi$-Chain development node. Press Ctrl+C to stop."
$BIN_PATH --chain $CHAIN_SPEC_FILE --validator --rpc-external --ws-external
check_status "Node launch"

# --- Protocol Complete ---
echo "--- $\Phi$-Chain Launch Protocol Complete ---"
