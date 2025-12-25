"""
validator_node.py - Φ-Chain Validator Node Implementation

This module implements a complete validator node with:
- Key generation and management
- Block proposal and validation
- Consensus participation
- Reward tracking
- Monitoring and metrics
"""

import json
import time
import hashlib
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import sys
sys.path.insert(0, '.')

from phi_chain import (
    Blockchain,
    GenesisParameters,
    PhiTransaction,
    ProofOfCoherence,
    FBAConsensus,
    FibonacciUtils
)

# --- Validator Key Management ---

class ValidatorKeyManager:
    """Manages validator keys and cryptographic operations"""
    
    def __init__(self, validator_id: str):
        self.validator_id = validator_id
        self.public_key = self._generate_key()
        self.private_key = self._generate_key()
    
    def _generate_key(self) -> str:
        """Generate a cryptographic key"""
        data = f"{self.validator_id}{uuid.uuid4()}{time.time()}".encode()
        return hashlib.sha256(data).hexdigest()
    
    def sign_message(self, message: str) -> str:
        """Sign a message with the validator's private key"""
        data = f"{message}{self.private_key}".encode()
        return hashlib.sha256(data).hexdigest()
    
    def verify_signature(self, message: str, signature: str) -> bool:
        """Verify a message signature"""
        expected_signature = self.sign_message(message)
        return signature == expected_signature
    
    def to_dict(self) -> Dict[str, str]:
        """Export key information"""
        return {
            "validator_id": self.validator_id,
            "public_key": self.public_key,
            "private_key": self.private_key
        }

# --- Validator Node ---

@dataclass
class ValidatorMetrics:
    """Metrics for a validator node"""
    blocks_proposed: int = 0
    blocks_validated: int = 0
    votes_cast: int = 0
    consensus_participation: int = 0
    total_rewards: float = 0.0
    uptime_seconds: int = 0
    last_block_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class ValidatorNode:
    """Φ-Chain Validator Node"""
    
    def __init__(self, validator_id: str, stake: int, blockchain: Optional[Blockchain] = None):
        """
        Initialize a validator node.
        
        Args:
            validator_id: Unique validator identifier
            stake: Amount of Φ tokens staked (must be Fibonacci number)
            blockchain: Reference to the blockchain (optional)
        """
        self.validator_id = validator_id
        self.stake = stake
        self.blockchain = blockchain or Blockchain()
        self.params = GenesisParameters()
        
        # Key management
        self.key_manager = ValidatorKeyManager(validator_id)
        
        # Consensus
        self.poc = ProofOfCoherence(self.blockchain)
        self.fba = FBAConsensus(self.blockchain)
        
        # Metrics
        self.metrics = ValidatorMetrics()
        self.start_time = time.time()
        
        # State
        self.is_active = False
        self.is_synced = False
        self.pending_blocks: List[Dict[str, Any]] = []
        
        # Register validator
        self._register()
    
    def _register(self) -> bool:
        """Register this validator with the blockchain"""
        if not FibonacciUtils.is_fibonacci(self.stake):
            raise ValueError(f"Stake {self.stake} is not a Fibonacci number")
        
        if self.stake < self.params.MIN_VALIDATOR_STAKE:
            raise ValueError(f"Stake below minimum {self.params.MIN_VALIDATOR_STAKE}")
        
        return self.blockchain.add_validator(self.validator_id, self.stake)
    
    def activate(self) -> bool:
        """Activate the validator node"""
        self.is_active = True
        self.is_synced = True
        return True
    
    def deactivate(self) -> bool:
        """Deactivate the validator node"""
        self.is_active = False
        return True
    
    def propose_block(self) -> Optional[Dict[str, Any]]:
        """
        Propose a new block if selected as proposer.
        
        Returns:
            The proposed block data, or None if not selected
        """
        if not self.is_active or not self.is_synced:
            return None
        
        # Check if this validator is the proposer
        proposer = self.poc.select_proposer()
        if proposer != self.validator_id:
            return None
        
        # Mine pending transactions
        block = self.blockchain.mine_pending_transactions(self.validator_id)
        
        if block:
            # Update metrics
            self.metrics.blocks_proposed += 1
            self.metrics.last_block_time = time.time()
            
            # Sign block
            block_hash = block.hash
            signature = self.key_manager.sign_message(block_hash)
            
            return {
                "block_hash": block_hash,
                "block_index": block.index,
                "signature": signature,
                "proposer": self.validator_id,
                "timestamp": time.time()
            }
        
        return None
    
    def validate_block(self, block_data: Dict[str, Any]) -> bool:
        """
        Validate a proposed block.
        
        Args:
            block_data: The block to validate
            
        Returns:
            True if the block is valid
        """
        if not self.is_active or not self.is_synced:
            return False
        
        # Verify block structure
        required_fields = ["block_hash", "block_index", "signature", "proposer"]
        if not all(field in block_data for field in required_fields):
            return False
        
        # Update metrics
        self.metrics.blocks_validated += 1
        
        return True
    
    def cast_vote(self, block_hash: str, vote_type: str = "prepare") -> bool:
        """
        Cast a vote on a block during consensus.
        
        Args:
            block_hash: The block being voted on
            vote_type: "prepare" or "commit"
            
        Returns:
            True if vote was cast successfully
        """
        if not self.is_active or not self.is_synced:
            return False
        
        # Sign the vote
        vote_message = f"{block_hash}:{vote_type}"
        signature = self.key_manager.sign_message(vote_message)
        
        # Process vote through FBA
        self.fba.process_vote(self.validator_id, block_hash, vote_type)
        
        # Update metrics
        self.metrics.votes_cast += 1
        self.metrics.consensus_participation += 1
        
        return True
    
    def get_coherence_score(self) -> float:
        """Get this validator's coherence score"""
        return self.poc.calculate_coherence_score(self.validator_id)
    
    def get_status(self) -> Dict[str, Any]:
        """Get validator node status"""
        uptime = int(time.time() - self.start_time)
        
        return {
            "validator_id": self.validator_id,
            "is_active": self.is_active,
            "is_synced": self.is_synced,
            "stake": self.stake,
            "coherence_score": self.get_coherence_score(),
            "public_key": self.key_manager.public_key,
            "metrics": self.metrics.to_dict(),
            "uptime_seconds": uptime,
            "blockchain_height": self.blockchain.get_chain_length()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Export validator node configuration"""
        return {
            "validator_id": self.validator_id,
            "stake": self.stake,
            "public_key": self.key_manager.public_key,
            "is_active": self.is_active,
            "is_synced": self.is_synced,
            "metrics": self.metrics.to_dict()
        }

# --- Validator Network ---

class ValidatorNetwork:
    """Network of validator nodes"""
    
    def __init__(self, blockchain: Optional[Blockchain] = None):
        """Initialize validator network"""
        self.blockchain = blockchain or Blockchain()
        self.validators: Dict[str, ValidatorNode] = {}
        self.params = GenesisParameters()
    
    def add_validator(self, validator_id: str, stake: int) -> Optional[ValidatorNode]:
        """
        Add a validator to the network.
        
        Args:
            validator_id: Unique validator identifier
            stake: Amount of Φ tokens staked
            
        Returns:
            The created ValidatorNode, or None if failed
        """
        try:
            validator = ValidatorNode(validator_id, stake, self.blockchain)
            self.validators[validator_id] = validator
            return validator
        except ValueError as e:
            print(f"Failed to add validator {validator_id}: {e}")
            return None
    
    def activate_all(self) -> int:
        """Activate all validators"""
        count = 0
        for validator in self.validators.values():
            if validator.activate():
                count += 1
        return count
    
    def deactivate_all(self) -> int:
        """Deactivate all validators"""
        count = 0
        for validator in self.validators.values():
            if validator.deactivate():
                count += 1
        return count
    
    def get_validator(self, validator_id: str) -> Optional[ValidatorNode]:
        """Get a validator by ID"""
        return self.validators.get(validator_id)
    
    def get_all_validators(self) -> List[ValidatorNode]:
        """Get all validators"""
        return list(self.validators.values())
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get network status"""
        active_validators = sum(1 for v in self.validators.values() if v.is_active)
        synced_validators = sum(1 for v in self.validators.values() if v.is_synced)
        total_stake = sum(v.stake for v in self.validators.values())
        
        return {
            "total_validators": len(self.validators),
            "active_validators": active_validators,
            "synced_validators": synced_validators,
            "total_stake": total_stake,
            "blockchain_height": self.blockchain.get_chain_length(),
            "pending_transactions": len(self.blockchain.pending_transactions)
        }
    
    def simulate_consensus_round(self) -> Dict[str, Any]:
        """Simulate a consensus round"""
        results = {
            "blocks_proposed": 0,
            "blocks_validated": 0,
            "votes_cast": 0,
            "consensus_reached": False
        }
        
        # Propose blocks
        for validator in self.validators.values():
            if validator.is_active:
                block = validator.propose_block()
                if block:
                    results["blocks_proposed"] += 1
        
        # Validate blocks
        for validator in self.validators.values():
            if validator.is_active:
                # Simulate block validation
                results["blocks_validated"] += 1
        
        # Cast votes
        for validator in self.validators.values():
            if validator.is_active:
                if validator.cast_vote("block_hash"):
                    results["votes_cast"] += 1
        
        # Check consensus
        if results["votes_cast"] >= self.params.FINALITY_THRESHOLD:
            results["consensus_reached"] = True
        
        return results
    
    def export_configuration(self, filename: str):
        """Export validator network configuration to JSON"""
        config = {
            "network": self.get_network_status(),
            "validators": [v.to_dict() for v in self.validators.values()],
            "parameters": self.params.to_dict(),
            "timestamp": time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
    
    def import_configuration(self, filename: str):
        """Import validator network configuration from JSON"""
        with open(filename, 'r') as f:
            config = json.load(f)
        
        # Load validators from config
        for validator_config in config.get("validators", []):
            validator_id = validator_config["validator_id"]
            stake = validator_config["stake"]
            self.add_validator(validator_id, stake)

# --- Validator Node Runner ---

class ValidatorNodeRunner:
    """Runs and manages a validator node"""
    
    def __init__(self, config_file: str):
        """
        Initialize validator node runner.
        
        Args:
            config_file: Path to validator configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()
        self.node = self._initialize_node()
        self.running = False
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Configuration file not found: {self.config_file}")
    
    def _initialize_node(self) -> ValidatorNode:
        """Initialize validator node from configuration"""
        validator_id = self.config.get("validator_id")
        stake = self.config.get("stake")
        
        if not validator_id or not stake:
            raise ValueError("Invalid configuration: missing validator_id or stake")
        
        return ValidatorNode(validator_id, stake)
    
    def start(self):
        """Start the validator node"""
        print(f"Starting validator node: {self.node.validator_id}")
        self.node.activate()
        self.running = True
        print(f"✅ Validator node started and activated")
    
    def stop(self):
        """Stop the validator node"""
        print(f"Stopping validator node: {self.node.validator_id}")
        self.node.deactivate()
        self.running = False
        print(f"✅ Validator node stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get validator node status"""
        return self.node.get_status()
    
    def run_loop(self, duration: int = 60):
        """
        Run the validator node for a specified duration.
        
        Args:
            duration: Duration in seconds to run
        """
        self.start()
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                # Propose blocks
                block = self.node.propose_block()
                if block:
                    print(f"📦 Block proposed: {block['block_hash'][:16]}...")
                
                # Cast votes
                self.node.cast_vote("block_hash")
                
                # Sleep
                time.sleep(self.node.params.SLOT_DURATION)
        except KeyboardInterrupt:
            print("\n⏹️ Interrupted by user")
        finally:
            self.stop()

if __name__ == "__main__":
    print("=" * 60)
    print("Φ-CHAIN VALIDATOR NODE")
    print("=" * 60)
    
    # Create a test validator
    print("\nCreating test validator...")
    validator = ValidatorNode("validator_001", 6765)
    
    print(f"\n✅ Validator created:")
    print(f"  ID: {validator.validator_id}")
    print(f"  Stake: {validator.stake} Φ")
    print(f"  Public Key: {validator.key_manager.public_key[:16]}...")
    
    # Activate validator
    print(f"\nActivating validator...")
    validator.activate()
    
    # Get status
    status = validator.get_status()
    print(f"\nValidator Status:")
    print(f"  Active: {status['is_active']}")
    print(f"  Synced: {status['is_synced']}")
    print(f"  Coherence Score: {status['coherence_score']:.6f}")
    print(f"  Blockchain Height: {status['blockchain_height']}")
    
    print("\n" + "=" * 60)
