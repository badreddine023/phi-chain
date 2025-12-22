import os
import json
import time
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from phi_chain_core import GenesisParameters, PhiBlock, PhiTransaction, FibonacciUtils

def initialize_mainnet():
    print("🚀 Initializing Φ-Chain Mainnet Deployment...")
    
    # 1. Generate Genesis Parameters
    params = GenesisParameters()
    print(f"Genesis Parameters: {params.to_dict()}")
    
    # 2. Create Genesis Block
    genesis_tx = PhiTransaction(
        sender="0x0000000000000000000000000000000000000000",
        recipient="0x742d35Cc6634C0532925a3b844Bc454e4438f44e", # Initial allocation
        value=FibonacciUtils.fibonacci(33), # F_33 = 3,524,578 Φ
        data=b"Genesis Block - The Golden Ratio Era Begins"
    )
    
    genesis_block = PhiBlock(
        index=0,
        previous_hash="0" * 64,
        timestamp=time.time(),
        transactions=[genesis_tx],
        state_root="phi_genesis_root",
        proposer="phi_genesis_proposer",
        f_vector=(1, 1)
    )
    
    genesis_data = {
        "parameters": params.to_dict(),
        "genesis_block": {
            "hash": genesis_block.calculate_hash(),
            "timestamp": genesis_block.timestamp,
            "initial_supply": genesis_tx.value
        }
    }
    
    with open("/home/ubuntu/phi-chain/config/genesis_mainnet.json", "w") as f:
        json.dump(genesis_data, f, indent=4)
    
    print(f"✅ Genesis Block created: {genesis_data['genesis_block']['hash']}")
    
    # 3. Setup Validator Network (Conceptual)
    print("📡 Setting up Validator Network...")
    os.system("python3 /home/ubuntu/phi-chain/tools/setup_validators.py")
    
    print("✨ Mainnet Deployment Ready!")
    print("To start the network, run: python3 consensus/node_runner.py config/validators/node_0.json")

if __name__ == "__main__":
    initialize_mainnet()
