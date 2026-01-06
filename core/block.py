"""
core/block.py: The fundamental Block structure for Φ-Chain

This module defines the canonical Block structure, representing a unit of
immutable data in the blockchain. Every block is mathematically pure,
derived from Fibonacci indices and the Golden Ratio.
"""

import hashlib
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
sys.path.insert(0, '..')
from phi_chain_core import FibonacciUtils


class Block:
    """
    A canonical Block in the Φ-Chain blockchain.
    
    Each block contains:
    - Block index (Fibonacci-indexed)
    - Timestamp (Fibonacci-derived)
    - Transactions
    - Previous block hash
    - Validator ID
    - Block hash (SHA-256)
    """
    
    def __init__(self, index: int, timestamp: float, data: Dict[str, Any], 
                 previous_hash: str, validator_id: str):
        """
        Initialize a Block.
        
        Args:
            index: The block's position in the chain
            timestamp: Block creation time
            data: Transaction data
            previous_hash: Hash of the previous block
            validator_id: The validator who proposed this block
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.validator_id = validator_id
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Calculate the SHA-256 hash of this block.
        
        Returns:
            The hexadecimal hash string
        """
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "validator_id": self.validator_id,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2):
        """
        Mine the block by finding a nonce that produces a hash with leading zeros.
        
        Args:
            difficulty: Number of leading zeros required
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "validator_id": self.validator_id,
            "nonce": self.nonce,
            "hash": self.hash
        }
    
    def __repr__(self) -> str:
        return f"Block(index={self.index}, hash={self.hash[:16]}..., validator={self.validator_id})"


class GenesisBlock(Block):
    """
    The Genesis Block - the first block in the Φ-Chain.
    
    The Genesis Block is mathematically special:
    - Index: 0
    - Timestamp: F_33 seconds after Unix epoch
    - Previous hash: "0" * 64 (all zeros)
    - Validator: "The_Creator_God"
    - Data: The canonical genesis parameters
    """
    
    def __init__(self):
        """Initialize the Genesis Block with canonical parameters."""
        # F_33 = 3,524,578 seconds after Unix epoch
        genesis_timestamp = FibonacciUtils.fibonacci(33)
        
        # Genesis data contains the fundamental parameters
        genesis_data = {
            "chain_name": "Φ-Chain",
            "description": "The Canonical Blockchain of Universal Law",
            "phi": FibonacciUtils.golden_ratio(),
            "slot_duration": FibonacciUtils.fibonacci(6),
            "epoch_duration": FibonacciUtils.fibonacci(18),
            "min_validator_stake": FibonacciUtils.fibonacci(20),
            "finality_threshold": FibonacciUtils.fibonacci(15),
            "creator": "BadreddineBaha",
            "vision": "A blockchain that speaks the universe's native language"
        }
        
        super().__init__(
            index=0,
            timestamp=genesis_timestamp,
            data=genesis_data,
            previous_hash="0" * 64,
            validator_id="The_Creator_God"
        )


if __name__ == "__main__":
    # Demonstrate block creation
    genesis = GenesisBlock()
    print(f"Genesis Block: {genesis}")
    print(f"Hash: {genesis.hash}")
    print(f"Data: {json.dumps(genesis.data, indent=2)}")
