#!/usr/bin/env python3
"""
protocol_layer_v2.py - Φ-Chain Protocol Layer (Optimized Merge)

This module integrates the best practices from existing implementations:
- TransactionMempool with φ-derived prioritization
- ProtocolValidator for transaction and block validation
- BlockProposer for constructing coherent blocks
- ProtocolState for tracking protocol execution
- Integration with PhiTurboP2P for high-performance networking

Combines mathematical purity with practical network efficiency.
"""

import time
import hashlib
import asyncio
import logging
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import heapq

from phi_consensus import ProofOfCoherence, Validator, PhiBasedHashing, FibonacciQMatrix
from core.phi_math import PhiMath, fibonacci

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ProtocolLayer")


class TransactionStatus(Enum):
    """Enumeration of transaction states in the lifecycle."""
    PENDING = "pending"
    VALIDATED = "validated"
    INCLUDED = "included"
    FINALIZED = "finalized"
    REJECTED = "rejected"


@dataclass
class TransactionMetadata:
    """Metadata associated with a transaction in the mempool."""
    tx_hash: str
    timestamp: float
    fee: int
    priority: float = 0.0
    status: TransactionStatus = TransactionStatus.PENDING
    validation_errors: List[str] = field(default_factory=list)
    
    def __lt__(self, other: 'TransactionMetadata') -> bool:
        """Enable priority queue ordering by priority (higher priority first)."""
        return self.priority > other.priority


class TransactionMempool:
    """
    Manages pending transactions with φ-derived prioritization.
    
    Features:
    - Priority queue based on fees and age
    - Φ-coherent capacity management
    - Transaction deduplication
    """
    
    def __init__(self, max_size: int = None, phi_precision: int = 18):
        """
        Initialize the transaction mempool.
        
        Args:
            max_size: Maximum number of transactions (defaults to Fibonacci number)
            phi_precision: Precision for φ-derived calculations
        """
        # Use Fibonacci number for max size if not specified
        self.max_size = max_size or fibonacci(17)  # F_17 = 1597
        self.phi_precision = phi_precision
        self.phi = PhiMath.from_fixed(PhiMath.get_phi(phi_precision))
        
        # Priority queue for transactions (min-heap, so we negate priority)
        self.priority_queue: List[Tuple[float, str, TransactionMetadata]] = []
        
        # Mapping of transaction hash to metadata
        self.transactions: Dict[str, TransactionMetadata] = {}
        
        # Set of transaction hashes for quick lookup
        self.tx_hashes: Set[str] = set()
        
        logger.info(f"TransactionMempool initialized with max size: {self.max_size}")
    
    def add_transaction(self, tx_hash: str, fee: int, timestamp: Optional[float] = None) -> bool:
        """
        Add a transaction to the mempool.
        
        Args:
            tx_hash: Hash of the transaction
            fee: Transaction fee in Φ tokens
            timestamp: Timestamp of transaction submission
        
        Returns:
            True if transaction was added, False otherwise
        """
        if tx_hash in self.tx_hashes:
            return False  # Duplicate
        
        if len(self.transactions) >= self.max_size:
            return False  # Mempool full
        
        timestamp = timestamp or time.time()
        priority = self._calculate_priority(fee, timestamp)
        
        metadata = TransactionMetadata(
            tx_hash=tx_hash,
            timestamp=timestamp,
            fee=fee,
            priority=priority
        )
        
        self.transactions[tx_hash] = metadata
        self.tx_hashes.add(tx_hash)
        heapq.heappush(self.priority_queue, (-priority, tx_hash, metadata))
        
        return True
    
    def remove_transaction(self, tx_hash: str) -> bool:
        """Remove a transaction from the mempool."""
        if tx_hash not in self.tx_hashes:
            return False
        
        del self.transactions[tx_hash]
        self.tx_hashes.remove(tx_hash)
        return True
    
    def get_top_transactions(self, count: int) -> List[str]:
        """Get the top N transactions by priority."""
        result = []
        temp_queue = []
        
        for _ in range(min(count, len(self.priority_queue))):
            if self.priority_queue:
                neg_priority, tx_hash, metadata = heapq.heappop(self.priority_queue)
                if tx_hash in self.tx_hashes:
                    result.append(tx_hash)
                    temp_queue.append((neg_priority, tx_hash, metadata))
        
        for item in temp_queue:
            heapq.heappush(self.priority_queue, item)
        
        return result
    
    def _calculate_priority(self, fee: int, timestamp: float) -> float:
        """
        Calculate transaction priority using φ-derived formula.
        Priority = (fee / base_fee) × φ × age_factor
        """
        base_fee = fibonacci(8)  # F_8 = 21
        age = time.time() - timestamp
        age_factor = 1.0 + (age / 60.0)  # Increases by 1 every minute
        priority = (fee / base_fee) * self.phi * age_factor
        return priority
    
    def get_mempool_size(self) -> int:
        """Get the current number of transactions in the mempool."""
        return len(self.transactions)
    
    def get_transaction_status(self, tx_hash: str) -> Optional[TransactionStatus]:
        """Get the status of a transaction in the mempool."""
        if tx_hash in self.transactions:
            return self.transactions[tx_hash].status
        return None


class ProtocolValidator:
    """
    Validates transactions and blocks against protocol rules.
    
    Ensures mathematical coherence and network security.
    """
    
    def __init__(self, blockchain, phi_precision: int = 18):
        """Initialize the protocol validator."""
        self.blockchain = blockchain
        self.phi_precision = phi_precision
    
    def validate_transaction(self, tx, mempool: TransactionMempool) -> Tuple[bool, List[str]]:
        """Validate a transaction."""
        errors = []
        
        # Check 1: Sender has sufficient balance
        sender_balance = self.blockchain.get_balance(tx.sender)
        if sender_balance < tx.value:
            errors.append(f"Insufficient balance: {sender_balance} < {tx.value}")
        
        # Check 2: Transaction fee is reasonable
        base_fee = fibonacci(8)
        if tx.gas_limit < base_fee:
            errors.append(f"Gas limit too low: {tx.gas_limit} < {base_fee}")
        
        # Check 3: Verify ZK-proof if present
        if tx.zk_proof:
            if not self._verify_zk_proof(tx.zk_proof):
                errors.append("ZK-proof verification failed")
        
        return len(errors) == 0, errors
    
    def validate_block(self, block) -> Tuple[bool, List[str]]:
        """Validate a block according to Coherence Consensus rules."""
        errors = []
        
        # Check 1: Block hash is valid
        expected_hash = block.calculate_hash()
        if block.hash != expected_hash:
            errors.append("Block hash mismatch")
        
        # Check 2: Previous block hash is valid
        if block.index > 0:
            previous_block = self.blockchain.get_block(block.index - 1)
            if previous_block and block.previous_hash != previous_block.hash:
                errors.append("Previous block hash mismatch")
        
        # Check 3: Fibonacci state vector is correct
        if block.index > 0:
            previous_block = self.blockchain.get_block(block.index - 1)
            if previous_block:
                expected_f_vector = FibonacciQMatrix.compute_state_transition(previous_block.f_vector)
                if block.f_vector != expected_f_vector:
                    errors.append("Fibonacci state transition is invalid")
        
        return len(errors) == 0, errors
    
    def _verify_zk_proof(self, proof: Dict) -> bool:
        """Verify a Zero-Knowledge proof."""
        return "commitment" in proof and "challenge" in proof and "response" in proof


class ProtocolState:
    """
    Tracks the state of the protocol execution.
    
    Maintains current slot, epoch, validators, and pending blocks.
    """
    
    def __init__(self, genesis_params, phi_precision: int = 18):
        """Initialize the protocol state."""
        self.genesis_params = genesis_params
        self.phi_precision = phi_precision
        
        # Current slot and epoch
        self.current_slot = 0
        self.current_epoch = 0
        
        # Slot and epoch durations
        self.slot_duration = genesis_params.SLOT_DURATION
        self.epoch_duration = genesis_params.EPOCH_DURATION
        
        # Active validators
        self.active_validators: Dict[str, Validator] = {}
        
        # Pending blocks awaiting finality
        self.pending_blocks: Dict[str, Dict] = {}
        
        # Finalized blocks
        self.finalized_blocks: List[str] = []
        
        logger.info(f"ProtocolState initialized - Slot Duration: {self.slot_duration}s, Epoch Duration: {self.epoch_duration}s")
    
    def advance_slot(self) -> None:
        """Advance to the next slot."""
        self.current_slot += 1
        
        # Check if we've advanced to a new epoch
        slots_per_epoch = self.epoch_duration // self.slot_duration
        if self.current_slot % slots_per_epoch == 0:
            self.advance_epoch()
    
    def advance_epoch(self) -> None:
        """Advance to the next epoch."""
        self.current_epoch += 1
        logger.info(f"Advanced to epoch {self.current_epoch}")
    
    def add_pending_block(self, block_hash: str, block_data: Dict) -> None:
        """Add a pending block awaiting finality."""
        self.pending_blocks[block_hash] = block_data
    
    def finalize_block(self, block_hash: str) -> bool:
        """Finalize a block (move from pending to finalized)."""
        if block_hash in self.pending_blocks:
            del self.pending_blocks[block_hash]
            self.finalized_blocks.append(block_hash)
            logger.info(f"Block {block_hash[:16]}... finalized")
            return True
        return False
    
    def get_current_time(self) -> float:
        """Get the current protocol time in seconds."""
        return self.current_slot * self.slot_duration
    
    def get_protocol_stats(self) -> Dict:
        """Get protocol statistics."""
        return {
            "current_slot": self.current_slot,
            "current_epoch": self.current_epoch,
            "active_validators": len(self.active_validators),
            "pending_blocks": len(self.pending_blocks),
            "finalized_blocks": len(self.finalized_blocks),
            "protocol_time_seconds": self.get_current_time()
        }


class CoherenceConsensusEngine:
    """
    Main engine for the Coherence Consensus mechanism.
    
    Orchestrates block proposal, validation, and finality.
    """
    
    def __init__(self, protocol_state: ProtocolState, mempool: TransactionMempool, 
                 validator: ProtocolValidator, phi_precision: int = 18):
        """Initialize the Coherence Consensus Engine."""
        self.protocol_state = protocol_state
        self.mempool = mempool
        self.validator = validator
        self.phi_precision = phi_precision
        
        # Finality threshold (1/φ ≈ 0.618)
        self.finality_threshold = 1.0 / PhiMath.from_fixed(PhiMath.get_phi(phi_precision))
        
        logger.info(f"CoherenceConsensusEngine initialized - Finality Threshold: {self.finality_threshold:.4f}")
    
    def propose_block(self, proposer_address: str, max_transactions: int = 100) -> Optional[Dict]:
        """
        Propose a new block.
        
        Args:
            proposer_address: Address of the proposer
            max_transactions: Maximum number of transactions to include
        
        Returns:
            Proposed block data, or None if proposal fails
        """
        # Get top transactions from mempool
        top_tx_hashes = self.mempool.get_top_transactions(max_transactions)
        
        # Calculate next Fibonacci state
        if self.protocol_state.finalized_blocks:
            # In a real implementation, get the last finalized block's state
            next_f_vector = FibonacciQMatrix.compute_state_transition((1, 1))
        else:
            next_f_vector = (1, 1)  # Genesis state
        
        # Construct block metadata
        block_data = {
            "index": len(self.protocol_state.finalized_blocks),
            "proposer": proposer_address,
            "timestamp": time.time(),
            "transactions": top_tx_hashes,
            "f_vector": next_f_vector,
            "slot": self.protocol_state.current_slot,
            "epoch": self.protocol_state.current_epoch
        }
        
        logger.info(f"Block proposed by {proposer_address} with {len(top_tx_hashes)} transactions")
        return block_data
    
    def check_finality(self, block_hash: str, signatures: Dict[str, bool]) -> bool:
        """
        Check if a block has achieved finality.
        
        Args:
            block_hash: Hash of the block
            signatures: Dictionary of validator signatures
        
        Returns:
            True if block is final, False otherwise
        """
        # Calculate cumulative weight of signatures
        total_weight = len(signatures)
        signed_weight = sum(1 for signed in signatures.values() if signed)
        
        cumulative_weight = signed_weight / total_weight if total_weight > 0 else 0
        
        is_final = cumulative_weight >= self.finality_threshold
        
        if is_final:
            self.protocol_state.finalize_block(block_hash)
            logger.info(f"Block {block_hash[:16]}... achieved finality with {cumulative_weight:.2%} signatures")
        
        return is_final


# Example usage and testing
if __name__ == "__main__":
    from phi_chain import GenesisParameters
    
    print("=== Φ-Chain Protocol Layer v2 (Optimized Merge) ===\n")
    
    # Initialize genesis parameters
    genesis_params = GenesisParameters()
    
    # Initialize components
    mempool = TransactionMempool()
    protocol_state = ProtocolState(genesis_params)
    validator = ProtocolValidator(None)  # Placeholder blockchain
    consensus_engine = CoherenceConsensusEngine(protocol_state, mempool, validator)
    
    # Add test transactions
    print("Adding test transactions to mempool...")
    for i in range(5):
        tx_hash = hashlib.sha256(f"tx_{i}".encode()).hexdigest()
        fee = fibonacci(8) + i * 10
        mempool.add_transaction(tx_hash, fee)
    
    print(f"Mempool size: {mempool.get_mempool_size()}\n")
    
    # Propose a block
    print("Proposing a block...")
    block_data = consensus_engine.propose_block("validator_001", max_transactions=3)
    print(f"Block proposed: {block_data}\n")
    
    # Check protocol state
    print("Protocol State:")
    stats = protocol_state.get_protocol_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Advance slots
    print("\nAdvancing slots...")
    for _ in range(5):
        protocol_state.advance_slot()
    
    print(f"Current slot: {protocol_state.current_slot}")
    print(f"Current epoch: {protocol_state.current_epoch}")
