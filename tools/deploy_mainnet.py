#!/usr/bin/env python3
"""
tools/deploy_mainnet.py - Φ-Chain Mainnet Deployment Script

This script initializes and deploys the Φ-Chain Mainnet with:
- Genesis block creation
- Validator network setup
- Configuration generation
- Initial state initialization
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_chain import (
    Blockchain,
    GenesisParameters,
    FibonacciUtils,
    generate_genesis_block,
    save_blockchain_to_file
)
from validator_node import ValidatorNetwork, ValidatorNode

class MainnetDeployer:
    """Manages Φ-Chain Mainnet deployment"""
    
    def __init__(self, network_name: str = "phi-chain-mainnet"):
        """Initialize mainnet deployer"""
        self.network_name = network_name
        self.deployment_dir = Path("deployments") / network_name
        self.blockchain = Blockchain()
        self.validator_network = ValidatorNetwork(self.blockchain)
        self.params = GenesisParameters()
        self.deployment_time = datetime.now().isoformat()
        
        # Create deployment directory
        self.deployment_dir.mkdir(parents=True, exist_ok=True)
    
    def print_header(self):
        """Print deployment header"""
        print("\n" + "=" * 70)
        print("Φ-CHAIN MAINNET DEPLOYMENT")
        print("=" * 70)
        print(f"Network: {self.network_name}")
        print(f"Deployment Time: {self.deployment_time}")
        print("=" * 70 + "\n")
    
    def print_section(self, title: str):
        """Print section header"""
        print(f"\n{'─' * 70}")
        print(f"  {title}")
        print(f"{'─' * 70}\n")
    
    def deploy_genesis(self):
        """Deploy genesis block"""
        self.print_section("1. GENESIS BLOCK INITIALIZATION")
        
        genesis_block = self.blockchain.get_latest_block()
        
        print(f"✅ Genesis Block Created:")
        print(f"   Index: {genesis_block.index}")
        print(f"   Hash: {genesis_block.hash}")
        print(f"   Timestamp: {genesis_block.timestamp}")
        print(f"   Proposer: {genesis_block.proposer}")
        print(f"   F-Vector: {genesis_block.f_vector}")
        print(f"   Transactions: {len(genesis_block.transactions)}")
        
        # Save genesis block
        genesis_file = self.deployment_dir / "genesis_block.json"
        with open(genesis_file, 'w') as f:
            json.dump({
                "index": genesis_block.index,
                "hash": genesis_block.hash,
                "timestamp": genesis_block.timestamp,
                "proposer": genesis_block.proposer,
                "f_vector": genesis_block.f_vector,
                "transactions": [tx.to_dict() for tx in genesis_block.transactions]
            }, f, indent=2)
        
        print(f"\n   Saved to: {genesis_file}")
    
    def deploy_parameters(self):
        """Deploy genesis parameters"""
        self.print_section("2. GENESIS PARAMETERS")
        
        params_dict = self.params.to_dict()
        
        print("Φ-Chain Parameters (All Fibonacci-Derived):")
        print(f"   PHI (Golden Ratio): {self.params.PHI}")
        print(f"   Slot Duration: {self.params.SLOT_DURATION} seconds (F_6)")
        print(f"   Epoch Duration: {self.params.EPOCH_DURATION} seconds (F_18)")
        print(f"   Min Validator Stake: {self.params.MIN_VALIDATOR_STAKE} Φ (F_20)")
        print(f"   Max Validators: {self.params.MAX_VALIDATOR_COUNT} (F_17)")
        print(f"   Target Committee Size: {self.params.TARGET_COMMITTEE_SIZE} (F_14)")
        print(f"   Finality Threshold: {self.params.FINALITY_THRESHOLD} (F_15)")
        print(f"   Genesis Supply: {self.params.GENESIS_SUPPLY} Φ (F_33)")
        print(f"   Block Reward: {self.params.BLOCK_REWARD} Φ (F_11)")
        print(f"   Transaction Fee Base: {self.params.TRANSACTION_FEE_BASE} (F_8)")
        
        # Save parameters
        params_file = self.deployment_dir / "genesis_parameters.json"
        with open(params_file, 'w') as f:
            json.dump(params_dict, f, indent=2)
        
        print(f"\n   Saved to: {params_file}")
    
    def deploy_validators(self, validator_count: int = 10):
        """Deploy validator network"""
        self.print_section(f"3. VALIDATOR NETWORK DEPLOYMENT ({validator_count} validators)")
        
        # Fibonacci stakes for validators
        fibonacci_stakes = [
            FibonacciUtils.fibonacci(20),  # 6765
            FibonacciUtils.fibonacci(21),  # 10946
            FibonacciUtils.fibonacci(22),  # 17711
            FibonacciUtils.fibonacci(23),  # 28657
            FibonacciUtils.fibonacci(24),  # 46368
            FibonacciUtils.fibonacci(25),  # 75025
            FibonacciUtils.fibonacci(26),  # 121393
            FibonacciUtils.fibonacci(27),  # 196418
            FibonacciUtils.fibonacci(28),  # 317811
            FibonacciUtils.fibonacci(29),  # 514229
        ]
        
        validators_config = []
        total_stake = 0
        
        for i in range(min(validator_count, len(fibonacci_stakes))):
            validator_id = f"validator_{i:03d}"
            stake = fibonacci_stakes[i]
            
            # Add validator to network
            validator = self.validator_network.add_validator(validator_id, stake)
            
            if validator:
                print(f"   ✅ {validator_id}: {stake:>7} Φ (F_{20+i})")
                total_stake += stake
                
                validators_config.append({
                    "validator_id": validator_id,
                    "stake": stake,
                    "public_key": validator.key_manager.public_key,
                    "index": i
                })
        
        print(f"\n   Total Validators: {len(validators_config)}")
        print(f"   Total Stake: {total_stake:,} Φ")
        print(f"   Average Stake: {total_stake // len(validators_config):,} Φ")
        
        # Save validator configurations
        validators_dir = self.deployment_dir / "validators"
        validators_dir.mkdir(exist_ok=True)
        
        for config in validators_config:
            validator_file = validators_dir / f"{config['validator_id']}.json"
            with open(validator_file, 'w') as f:
                json.dump(config, f, indent=2)
        
        # Save validators list
        validators_list_file = self.deployment_dir / "validators_list.json"
        with open(validators_list_file, 'w') as f:
            json.dump(validators_config, f, indent=2)
        
        print(f"\n   Saved to: {validators_dir}/")
        print(f"   List saved to: {validators_list_file}")
    
    def activate_validators(self):
        """Activate all validators"""
        self.print_section("4. VALIDATOR ACTIVATION")
        
        count = self.validator_network.activate_all()
        
        print(f"✅ Activated {count} validators")
        
        # Get network status
        status = self.validator_network.get_network_status()
        print(f"\nNetwork Status:")
        print(f"   Total Validators: {status['total_validators']}")
        print(f"   Active Validators: {status['active_validators']}")
        print(f"   Synced Validators: {status['synced_validators']}")
        print(f"   Total Stake: {status['total_stake']:,} Φ")
        print(f"   Blockchain Height: {status['blockchain_height']}")
    
    def initialize_state(self):
        """Initialize blockchain state"""
        self.print_section("5. BLOCKCHAIN STATE INITIALIZATION")
        
        # Get blockchain summary
        summary = self.blockchain.get_chain_summary()
        
        print(f"Blockchain State:")
        print(f"   Chain Length: {summary['length']}")
        print(f"   Is Valid: {summary['is_valid']}")
        print(f"   Latest Block Hash: {summary['latest_block_hash']}")
        print(f"   Latest Block Index: {summary['latest_block_index']}")
        print(f"   F-Vector: {summary['f_vector']}")
        print(f"   Total Supply: {summary['total_supply']:,} Φ")
        print(f"   Pending Transactions: {summary['pending_transactions']}")
        
        # Save blockchain state
        blockchain_file = self.deployment_dir / "blockchain_state.json"
        save_blockchain_to_file(self.blockchain, str(blockchain_file))
        
        print(f"\n   Saved to: {blockchain_file}")
    
    def generate_deployment_manifest(self):
        """Generate deployment manifest"""
        self.print_section("6. DEPLOYMENT MANIFEST")
        
        manifest = {
            "network_name": self.network_name,
            "deployment_time": self.deployment_time,
            "genesis_block": {
                "hash": self.blockchain.get_latest_block().hash,
                "index": self.blockchain.get_latest_block().index
            },
            "parameters": self.params.to_dict(),
            "validators": {
                "total": len(self.validator_network.validators),
                "active": sum(1 for v in self.validator_network.validators.values() if v.is_active),
                "total_stake": sum(v.stake for v in self.validator_network.validators.values())
            },
            "blockchain": {
                "chain_length": self.blockchain.get_chain_length(),
                "is_valid": self.blockchain.is_chain_valid(),
                "total_supply": self.params.GENESIS_SUPPLY
            },
            "deployment_directory": str(self.deployment_dir)
        }
        
        # Save manifest
        manifest_file = self.deployment_dir / "deployment_manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"✅ Deployment Manifest Generated:")
        print(f"   Network: {manifest['network_name']}")
        print(f"   Genesis Block: {manifest['genesis_block']['hash'][:16]}...")
        print(f"   Validators: {manifest['validators']['total']}")
        print(f"   Total Stake: {manifest['validators']['total_stake']:,} Φ")
        print(f"   Chain Valid: {manifest['blockchain']['is_valid']}")
        
        print(f"\n   Saved to: {manifest_file}")
    
    def generate_startup_script(self):
        """Generate startup script for mainnet"""
        self.print_section("7. STARTUP SCRIPT GENERATION")
        
        startup_script = f"""#!/bin/bash
# Φ-Chain Mainnet Startup Script
# Generated: {self.deployment_time}

echo "Starting Φ-Chain Mainnet..."
echo "Network: {self.network_name}"

# Start API server
echo "Starting API server..."
python3 api/wallet_api.py &
API_PID=$!

# Wait for API to start
sleep 2

# Start validators
echo "Starting validators..."
for validator_file in {self.deployment_dir}/validators/*.json; do
    validator_id=$(basename "$validator_file" .json)
    echo "  Starting $validator_id..."
    python3 consensus/node_runner.py "$validator_file" &
done

echo "Φ-Chain Mainnet is running!"
echo "API Server PID: $API_PID"
echo "Press Ctrl+C to stop"

wait
"""
        
        startup_file = self.deployment_dir / "startup.sh"
        with open(startup_file, 'w') as f:
            f.write(startup_script)
        
        # Make executable
        os.chmod(startup_file, 0o755)
        
        print(f"✅ Startup Script Generated:")
        print(f"   Saved to: {startup_file}")
        print(f"   Usage: bash {startup_file}")
    
    def deploy(self, validator_count: int = 10):
        """Execute full mainnet deployment"""
        self.print_header()
        
        try:
            self.deploy_genesis()
            self.deploy_parameters()
            self.deploy_validators(validator_count)
            self.activate_validators()
            self.initialize_state()
            self.generate_deployment_manifest()
            self.generate_startup_script()
            
            self.print_section("DEPLOYMENT COMPLETE")
            print(f"✅ Φ-Chain Mainnet successfully deployed!")
            print(f"\nDeployment Directory: {self.deployment_dir}")
            print(f"Configuration Files:")
            print(f"   - genesis_block.json")
            print(f"   - genesis_parameters.json")
            print(f"   - validators_list.json")
            print(f"   - blockchain_state.json")
            print(f"   - deployment_manifest.json")
            print(f"   - startup.sh")
            print(f"\nNext Steps:")
            print(f"   1. Review deployment_manifest.json")
            print(f"   2. Run: bash {self.deployment_dir}/startup.sh")
            print(f"   3. Access wallet at: http://localhost:8000")
            print("\n" + "=" * 70 + "\n")
            
            return True
        except Exception as e:
            print(f"\n❌ Deployment failed: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main deployment function"""
    # Create deployer
    deployer = MainnetDeployer("phi-chain-mainnet-v1")
    
    # Execute deployment
    success = deployer.deploy(validator_count=10)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
