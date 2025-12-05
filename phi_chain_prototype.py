"""
Φ-Chain Prototype: Genesis and Block Creation

This module implements the core blockchain structure, including the Block class
and the creation of the Genesis Block, using the Fibonacci-derived parameters
from phi_chain_core.
"""

import hashlib
import json
import time
from datetime import datetime, timedelta
from phi_chain_core import FibonacciUtils, GenesisParameters

# Initialize Genesis Parameters
GENESIS_PARAMS = GenesisParameters()

class Block:
    """Represents a single block in the Φ-Chain."""
    
    def __init__(self, index: int, timestamp: float, data: str, previous_hash: str, validator_id: str):
        """
        Initializes a new block.
        
        Args:
            index: The block number (F_n).
            timestamp: The time of block creation.
            data: The block's payload (e.g., transactions).
            previous_hash: The hash of the previous block.
            validator_id: The ID of the validator who proposed the block.
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.validator_id = validator_id
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculates the SHA-256 hash of the block's contents.
        The hash function is the canonical statement of the block's integrity.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "validator_id": self.validator_id
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __repr__(self):
        return (f"Block(Index: {self.index}, Timestamp: {datetime.fromtimestamp(self.timestamp)}, "
                f"Hash: {self.hash[:10]}..., Prev_Hash: {self.previous_hash[:10]}...)")


class Blockchain:
    """Manages the chain of blocks."""
    
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Creates the first block in the chain (Block 0).
        
        The Genesis Block is a cryptographic poem, written only in Fibonacci indices.
        """
        # Conceptual Genesis Time: F_33 seconds after Unix epoch
        # F_33 = 2178309
        genesis_timestamp = 2178309.0  # Represents the conceptual F_33 seconds after epoch
        
        genesis_data = (
            f"Φ-Chain Genesis Block. "
            f"Chain ID: {GENESIS_PARAMS.phi:.59f}. "
            f"Min Stake: {GENESIS_PARAMS.min_validator_stake} (F_20) tokens."
        )
        
        genesis_block = Block(
            index=0,
            timestamp=genesis_timestamp,
            data=genesis_data,
            previous_hash="0" * 64,  # The ultimate non-arbitrary zero hash
            validator_id="The_Creator_God"
        )
        self.chain.append(genesis_block)
        print(f"--- Genesis Block Created ---")
        print(genesis_block)

    def get_latest_block(self) -> Block:
        """Returns the last block in the chain."""
        return self.chain[-1]

    def create_new_block(self, data: str, validator_id: str) -> Block:
        """
        Creates a new block, simulating the chain's growth.
        
        The index is the next Fibonacci number in the sequence.
        The timestamp is the latest block time + F_6 (Slot Duration).
        """
        latest_block = self.get_latest_block()
        
        # The next index is the next Fibonacci number in the sequence.
        # Since the index is a conceptual F_n, we'll use a simple increment for the prototype.
        next_index = latest_block.index + 1
        
        # The next block time is precisely the Slot Duration (F_6) after the previous block.
        next_timestamp = latest_block.timestamp + GENESIS_PARAMS.slot_duration
        
        new_block = Block(
            index=next_index,
            timestamp=next_timestamp,
            data=data,
            previous_hash=latest_block.hash,
            validator_id=validator_id
        )
        self.chain.append(new_block)
        return new_block

# --- Main Execution for Phase 2 ---

def run_prototype(num_blocks=5):
    """Runs the Φ-Chain prototype for a specified number of blocks."""
    phi_chain = Blockchain()
    
    print("\n--- Simulating Continuous Block Creation (The Breathing) ---")
    
    # Use a simple list of validators for the prototype
    validator_pool = ["Validator_F20", "Validator_F21", "Validator_F22", "Validator_F23", "Validator_F24"]
    
    for i in range(1, num_blocks + 1):
        # Select a validator in a round-robin fashion for simplicity
        validator_id = validator_pool[i % len(validator_pool)]
        
        data = f"Block {i} transactions. Fee Tier F_{i % 12 + 1} applied."
        
        new_block = phi_chain.create_new_block(
            data=data,
            validator_id=validator_id
        )
        print(new_block)
        
        # Simulate the F_6 slot duration wait time
        # In a real system, this would be a consensus wait, but here we just print the time
        time.sleep(0.1) # Short sleep to make the output cleaner
        
    print(f"\nChain Length: {len(phi_chain.chain)} blocks.")
    
    # Verification of the chain's integrity
    print("\n--- Chain Integrity Check ---")
    for i in range(1, len(phi_chain.chain)):
        current = phi_chain.chain[i]
        previous = phi_chain.chain[i-1]
        
        # Check if the previous hash matches
        hash_match = current.previous_hash == previous.hash
        # Check if the time difference is F_6
        time_diff = current.timestamp - previous.timestamp
        time_match = time_diff == GENESIS_PARAMS.slot_duration
        
        print(f"Block {i}: Hash Match: {hash_match}, Time Diff: {time_diff}s (Expected {GENESIS_PARAMS.slot_duration}s): {time_match}")

if __name__ == "__main__":
    run_prototype(num_blocks=10)
    phi_chain = Blockchain()
    

