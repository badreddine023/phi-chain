#!/usr/bin/env python3
"""
Φ-Chain Mainnet Deployment Script

This script automates the complete deployment lifecycle for Φ-Chain:
1. Genesis block creation with Fibonacci parameters
2. Validator network initialization
3. Configuration generation
4. Network launch

Usage:
    python3 deploy_phi_chain.py [--network mainnet|testnet] [--validators N]
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
import math

# Golden Ratio and Fibonacci constants
PHI = (1 + math.sqrt(5)) / 2
FIBONACCI = [0, 1]
for i in range(2, 50):
    FIBONACCI.append(FIBONACCI[-1] + FIBONACCI[-2])

# Mainnet parameters (all Fibonacci-derived)
MAINNET_PARAMS = {
    "network_name": "phi-chain-mainnet-v1",
    "slot_duration": 8,  # F_6 seconds
    "epoch_duration": 2584,  # F_18 seconds
    "min_stake": 6765,  # F_20 Φ
    "max_validators": 1597,  # F_17
    "finality_threshold": 610,  # F_15 signatures
    "genesis_supply": 3524578,  # F_33 Φ
    "block_reward_base": 1,  # Φ per block
    "inflation_rate": 1 / PHI,  # 61.8% annually
}

# Testnet parameters (smaller Fibonacci numbers)
TESTNET_PARAMS = {
    "network_name": "phi-chain-testnet-v1",
    "slot_duration": 8,  # F_6 seconds
    "epoch_duration": 377,  # F_14 seconds
    "min_stake": 233,  # F_13 Φ
    "max_validators": 144,  # F_12
    "finality_threshold": 89,  # F_11 signatures
    "genesis_supply": 46368,  # F_24 Φ
    "block_reward_base": 1,  # Φ per block
    "inflation_rate": 1 / PHI,  # 61.8% annually
}


class GenesisBlockGenerator:
    """Generates the genesis block for Φ-Chain."""
    
    def __init__(self, network_params: dict):
        """
        Initialize genesis block generator.
        
        Args:
            network_params: Network parameters dictionary
        """
        self.params = network_params
    
    def generate_genesis_block(self) -> dict:
        """
        Generate genesis block with Fibonacci parameters.
        
        Returns:
            Genesis block dictionary
        """
        genesis_block = {
            "index": 0,
            "timestamp": datetime.utcnow().isoformat(),
            "network": self.params["network_name"],
            "previous_hash": "0" * 64,  # No previous block
            "nonce": 0,
            "hash": "",  # To be computed
            "transactions": [],
            "state": {
                "total_supply": self.params["genesis_supply"],
                "total_staked": 0,
                "active_validators": 0,
                "block_height": 0,
            },
            "parameters": {
                "slot_duration": self.params["slot_duration"],
                "epoch_duration": self.params["epoch_duration"],
                "min_stake": self.params["min_stake"],
                "max_validators": self.params["max_validators"],
                "finality_threshold": self.params["finality_threshold"],
                "block_reward": self.params["block_reward_base"],
                "inflation_rate": self.params["inflation_rate"],
            },
            "metadata": {
                "version": "1.0",
                "phi_constant": PHI,
                "fibonacci_indices": {
                    "slot_duration": 6,
                    "epoch_duration": 18 if "mainnet" in self.params["network_name"] else 14,
                    "min_stake": 20 if "mainnet" in self.params["network_name"] else 13,
                    "max_validators": 17 if "mainnet" in self.params["network_name"] else 12,
                    "finality_threshold": 15 if "mainnet" in self.params["network_name"] else 11,
                    "genesis_supply": 33 if "mainnet" in self.params["network_name"] else 24,
                },
            },
        }
        
        return genesis_block
    
    def compute_genesis_hash(self, genesis_block: dict) -> str:
        """
        Compute hash of genesis block.
        
        Args:
            genesis_block: Genesis block dictionary
        
        Returns:
            Hexadecimal hash string
        """
        import hashlib
        
        # Serialize block (excluding hash field)
        block_copy = {k: v for k, v in genesis_block.items() if k != "hash"}
        block_json = json.dumps(block_copy, sort_keys=True)
        
        # Compute SHA256 hash
        hash_object = hashlib.sha256(block_json.encode('utf-8'))
        return hash_object.hexdigest()


class ValidatorNetworkInitializer:
    """Initializes the validator network."""
    
    def __init__(self, network_params: dict, num_validators: int):
        """
        Initialize validator network.
        
        Args:
            network_params: Network parameters dictionary
            num_validators: Number of validators to initialize
        """
        self.params = network_params
        self.num_validators = min(num_validators, network_params["max_validators"])
    
    def generate_validators(self) -> list:
        """
        Generate validator configurations.
        
        Returns:
            List of validator configurations
        """
        validators = []
        
        for i in range(self.num_validators):
            # Fibonacci-indexed stake distribution
            fib_index = i % len(FIBONACCI)
            stake = FIBONACCI[fib_index] * 100  # Scale by 100 for reasonable values
            
            validator = {
                "index": i,
                "address": f"0x{i:064x}",  # Placeholder address
                "stake": min(stake, self.params["genesis_supply"] // self.num_validators),
                "participation_rate": 0.95,  # Initial 95% participation
                "coherence_score": 0.0,  # To be computed
                "status": "active",
            }
            
            validators.append(validator)
        
        return validators


class ConfigurationGenerator:
    """Generates configuration files for Φ-Chain deployment."""
    
    def __init__(self, network_params: dict, genesis_block: dict, validators: list):
        """
        Initialize configuration generator.
        
        Args:
            network_params: Network parameters dictionary
            genesis_block: Genesis block dictionary
            validators: List of validator configurations
        """
        self.params = network_params
        self.genesis_block = genesis_block
        self.validators = validators
    
    def generate_config(self) -> dict:
        """
        Generate complete configuration.
        
        Returns:
            Configuration dictionary
        """
        config = {
            "network": {
                "name": self.params["network_name"],
                "version": "1.0",
                "genesis_block": self.genesis_block,
            },
            "consensus": {
                "mechanism": "Proof-of-Coherence",
                "finality_threshold": self.params["finality_threshold"],
                "slot_duration": self.params["slot_duration"],
                "epoch_duration": self.params["epoch_duration"],
            },
            "staking": {
                "min_stake": self.params["min_stake"],
                "max_validators": self.params["max_validators"],
                "reward_rate": self.params["inflation_rate"],
            },
            "validators": self.validators,
            "deployment": {
                "timestamp": datetime.utcnow().isoformat(),
                "deployed_by": "phi-chain-deployment-script",
            },
        }
        
        return config


class PhiChainDeployer:
    """Orchestrates the complete Φ-Chain deployment."""
    
    def __init__(self, network_type: str = "mainnet", num_validators: int = 100):
        """
        Initialize deployer.
        
        Args:
            network_type: "mainnet" or "testnet"
            num_validators: Number of validators to initialize
        """
        self.network_type = network_type
        self.num_validators = num_validators
        
        # Select network parameters
        if network_type == "mainnet":
            self.params = MAINNET_PARAMS
        else:
            self.params = TESTNET_PARAMS
    
    def deploy(self, output_dir: str = "./deployments") -> dict:
        """
        Execute complete deployment.
        
        Args:
            output_dir: Directory to save deployment files
        
        Returns:
            Deployment summary dictionary
        """
        print(f"\n=== Φ-Chain {self.network_type.upper()} Deployment ===\n")
        
        # Create output directory
        output_path = Path(output_dir) / self.params["network_name"]
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Step 1: Generate genesis block
        print("Step 1: Generating genesis block...")
        genesis_gen = GenesisBlockGenerator(self.params)
        genesis_block = genesis_gen.generate_genesis_block()
        genesis_block["hash"] = genesis_gen.compute_genesis_hash(genesis_block)
        
        genesis_file = output_path / "genesis_block.json"
        with open(genesis_file, 'w') as f:
            json.dump(genesis_block, f, indent=2)
        print(f"  ✓ Genesis block created: {genesis_file}")
        
        # Step 2: Initialize validator network
        print("\nStep 2: Initializing validator network...")
        validator_init = ValidatorNetworkInitializer(self.params, self.num_validators)
        validators = validator_init.generate_validators()
        
        validators_file = output_path / "validators.json"
        with open(validators_file, 'w') as f:
            json.dump(validators, f, indent=2)
        print(f"  ✓ {len(validators)} validators initialized: {validators_file}")
        
        # Step 3: Generate configuration
        print("\nStep 3: Generating configuration...")
        config_gen = ConfigurationGenerator(self.params, genesis_block, validators)
        config = config_gen.generate_config()
        
        config_file = output_path / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"  ✓ Configuration generated: {config_file}")
        
        # Step 4: Generate deployment summary
        print("\nStep 4: Generating deployment summary...")
        summary = {
            "network": self.params["network_name"],
            "network_type": self.network_type,
            "timestamp": datetime.utcnow().isoformat(),
            "genesis_block_hash": genesis_block["hash"],
            "num_validators": len(validators),
            "total_supply": self.params["genesis_supply"],
            "parameters": self.params,
            "files": {
                "genesis_block": str(genesis_file),
                "validators": str(validators_file),
                "config": str(config_file),
            },
        }
        
        summary_file = output_path / "deployment_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"  ✓ Deployment summary: {summary_file}")
        
        # Print summary
        print("\n=== Deployment Summary ===")
        print(f"Network: {self.params['network_name']}")
        print(f"Genesis Block Hash: {genesis_block['hash'][:16]}...")
        print(f"Validators: {len(validators)}")
        print(f"Total Supply: {self.params['genesis_supply']} Φ")
        print(f"Finality Threshold: {self.params['finality_threshold']} signatures")
        print(f"Output Directory: {output_path}\n")
        
        return summary


def main():
    """Main entry point for deployment script."""
    parser = argparse.ArgumentParser(
        description="Φ-Chain Mainnet Deployment Script"
    )
    parser.add_argument(
        "--network",
        choices=["mainnet", "testnet"],
        default="mainnet",
        help="Network type (default: mainnet)"
    )
    parser.add_argument(
        "--validators",
        type=int,
        default=100,
        help="Number of validators to initialize (default: 100)"
    )
    parser.add_argument(
        "--output",
        default="./deployments",
        help="Output directory for deployment files (default: ./deployments)"
    )
    
    args = parser.parse_args()
    
    # Execute deployment
    deployer = PhiChainDeployer(
        network_type=args.network,
        num_validators=args.validators
    )
    
    summary = deployer.deploy(output_dir=args.output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
