"""
phi_chain_core.py - Core Data Structures for Phi Chain
This module defines the fundamental data structures for the Phi Chain,
including the Block, Transaction, and P-BFT Consensus Message.
"""

import time
from typing import List, Dict, Optional

# --- 1. Transaction Structure (Optimized for OPEVM) ---

class PhiTransaction:
    """
    Represents a transaction in the Phi Chain, including fields necessary
    for the Optimistic Parallelized EVM (OPEVM) conflict detection.
    """
    def __init__(self,
                 sender: str,
                 recipient: str,
                 value: int,
                 data: bytes,
                 nonce: int,
                 gas_limit: int,
                 signature: bytes,
                 estimated_read_set: Optional[List[str]] = None,
                 estimated_write_set: Optional[List[str]] = None):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.data = data
        self.nonce = nonce
        self.gas_limit = gas_limit
        self.signature = signature
        
        # OPEVM-specific fields for Pre-Execution Static Analysis
        # List of state storage slots (keys) the transaction is expected to touch
        self.estimated_read_set = estimated_read_set if estimated_read_set is not None else []
        self.estimated_write_set = estimated_write_set if estimated_write_set is not None else []

    def to_dict(self) -> Dict:
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "value": self.value,
            "data": self.data.hex(),
            "nonce": self.nonce,
            "gas_limit": self.gas_limit,
            "signature": self.signature.hex(),
            "read_set": self.estimated_read_set,
            "write_set": self.estimated_write_set,
        }

# --- 2. Block Structure ---

class PhiBlock:
    """
    Represents a block in the Phi Chain, incorporating the P-BFT finality
    and the OPEVM execution results.
    """
    def __init__(self,
                 index: int,
                 previous_hash: str,
                 timestamp: float,
                 transactions: List[PhiTransaction],
                 state_root: str,
                 receipts_root: str,
                 proposer: str,
                 bls_aggregated_signature: Optional[bytes] = None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.state_root = state_root
        self.receipts_root = receipts_root
        self.proposer = proposer
        
        # P-BFT-specific field for finality proof
        # This signature proves that 2/3+ of validators have committed to this block
        self.bls_aggregated_signature = bls_aggregated_signature

    def calculate_hash(self) -> str:
        """
        Conceptual method to calculate the block's hash (e.g., using SHA-256).
        """
        # In a real implementation, this would serialize the block and hash it.
        return f"hash_{self.index}_{self.timestamp}"

# --- 3. P-BFT Consensus Message Structure ---

class PipelinedBFTMessage:
    """
    Represents a message used in the Pipelined BFT consensus process.
    """
    def __init__(self,
                 msg_type: str, # e.g., "PROPOSE", "PREVOTE", "PRECOMMIT"
                 block_hash: str,
                 block_index: int,
                 validator_id: str,
                 signature: bytes):
        self.msg_type = msg_type
        self.block_hash = block_hash
        self.block_index = block_index
        self.validator_id = validator_id
        self.signature = signature
        
    def is_supermajority(self, messages: List['PipelinedBFTMessage'], total_validators: int) -> bool:
        """
        Conceptual check for 2/3+ supermajority.
        """
        required = (2 * total_validators) // 3 + 1
        unique_validators = {msg.validator_id for msg in messages if msg.msg_type == self.msg_type}
        return len(unique_validators) >= required

# --- Conceptual Usage Example ---

if __name__ == "__main__":
    # 1. Create a sample transaction
    tx1 = PhiTransaction(
        sender="0xAlice",
        recipient="0xBob",
        value=100,
        data=b"",
        nonce=1,
        gas_limit=21000,
        signature=b"sig1",
        estimated_read_set=["0xAlice_balance", "0xBob_balance"],
        estimated_write_set=["0xAlice_balance", "0xBob_balance"]
    )
    
    # 2. Create a conceptual block
    genesis_block = PhiBlock(
        index=0,
        previous_hash="0x0000000000000000000000000000000000000000000000000000000000000000",
        timestamp=time.time(),
        transactions=[tx1],
        state_root="0xInitialStateRoot",
        receipts_root="0xInitialReceiptsRoot",
        proposer="0xProposerNode"
    )
    
    print(f"Genesis Block Hash: {genesis_block.calculate_hash()}")
    print(f"Transaction 1 Read Set: {tx1.estimated_read_set}")
    
    # 3. Conceptual P-BFT message flow
    total_validators = 10
    prevote_msgs = [
        PipelinedBFTMessage("PREVOTE", genesis_block.calculate_hash(), 0, f"Validator_{i}", b"sig")
        for i in range(7) # 7 out of 10 is a supermajority
    ]
    
    # Check for supermajority
    is_finalized = prevote_msgs[0].is_supermajority(prevote_msgs, total_validators)
    print(f"Prevote Supermajority Reached: {is_finalized}")
    
    # The block is finalized by setting the aggregated signature
    if is_finalized:
        genesis_block.bls_aggregated_signature = b"BLS_Aggregated_Signature_Proof"
        print("Block 0 is finalized.")
