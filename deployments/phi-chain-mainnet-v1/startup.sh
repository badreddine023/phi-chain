#!/bin/bash
# Φ-Chain Mainnet Startup Script
# Generated: 2025-12-22T18:29:14.277096

echo "Starting Φ-Chain Mainnet..."
echo "Network: phi-chain-mainnet-v1"

# Start API server
echo "Starting API server..."
python3 api/wallet_api.py &
API_PID=$!

# Wait for API to start
sleep 2

# Start validators
echo "Starting validators..."
for validator_file in deployments/phi-chain-mainnet-v1/validators/*.json; do
    validator_id=$(basename "$validator_file" .json)
    echo "  Starting $validator_id..."
    python3 consensus/node_runner.py "$validator_file" &
done

echo "Φ-Chain Mainnet is running!"
echo "API Server PID: $API_PID"
echo "Press Ctrl+C to stop"

wait
