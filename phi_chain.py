"""
phi_chain.py - Unified Φ-Chain Core Engine

This module integrates all core blockchain components:
- Fibonacci Q-Matrix state transitions
- Proof-of-Coherence (PoC) mining
- Fibonacci Byzantine Agreement (FBA) consensus
- Genesis block generation
- Full blockchain operations
"""

import time
import json
import hashlib
from typing import List, Dict, Optional, Tuple, Any
from core.phi_math import PhiMath, fibonacci
import numpy as np

# --- 1. Fibonacci & Golden Ratio Utilities ---

class FibonacciUtils:
    """Fibonacci sequence and Golden Ratio calculations"""
    
    @staticmethod
    def fibonacci(n: int) -> int:
        """Calculates the nth Fibonacci number F_n with support for negative indices."""
        if n == 0:
            return 0
        if abs(n) <= 2:
            return 1 if n > 0 else (-1 if abs(n) % 2 == 0 else 1)
        
        a, b = 1, 1
        target = abs(n)
        for _ in range(3, target + 1):
            a, b = b, a + b
        
        result = b
        if n < 0:
            result *= (-1) ** (target + 1)
        return result
    
    @staticmethod
    def golden_ratio(precision: int = 18) -> int:
        """Calculates the Golden Ratio (Φ) with high precision using fixed-point arithmetic."""
        return PhiMath.get_phi(precision)
    
    @staticmethod
    def is_fibonacci(n: int) -> bool:
        """Checks if a number is a Fibonacci number."""
        if n < 0: return False
        def is_perfect_square(x):
            s = int(np.sqrt(x))
            return s*s == x
        return is_perfect_square(5*n*n + 4) or is_perfect_square(5*n*n - 4)
    
    @staticmethod
    def fibonacci_sequence(start: int, end: int) -> List[int]:
        """Generate Fibonacci sequence from F_start to F_end."""
        sequence = []
        for i in range(start, end + 1):
            sequence.append(FibonacciUtils.fibonacci(i))
        return sequence

# --- 2. Genesis Parameters (Derived from Fibonacci) ---

class GenesisParameters:
    """All Φ-Chain parameters derived from Fibonacci sequence"""
    
    def __init__(self):
        self.PHI_FIXED = FibonacciUtils.golden_ratio()
        self.PHI = PhiMath.from_fixed(self.PHI_FIXED)
        self.SLOT_DURATION = FibonacciUtils.fibonacci(6)      # F_6 = 8
        self.EPOCH_DURATION = FibonacciUtils.fibonacci(18)    # F_18 = 2584
        self.MIN_VALIDATOR_STAKE = FibonacciUtils.fibonacci(20) # F_20 = 6765
        self.MAX_VALIDATOR_COUNT = FibonacciUtils.fibonacci(17) # F_17 = 1597
        self.TARGET_COMMITTEE_SIZE = FibonacciUtils.fibonacci(14) # F_14 = 377
        self.FINALITY_THRESHOLD = FibonacciUtils.fibonacci(15) # F_15 = 610
        self.GENESIS_SUPPLY = FibonacciUtils.fibonacci(33)    # F_33 = 3524578
        self.BLOCK_REWARD = FibonacciUtils.fibonacci(11)      # F_11 = 89
        self.TRANSACTION_FEE_BASE = FibonacciUtils.fibonacci(8) # F_8 = 21
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert parameters to dictionary for JSON serialization."""
        return {
            "phi": self.PHI,
            "slot_duration": self.SLOT_DURATION,
            "epoch_duration": self.EPOCH_DURATION,
            "min_validator_stake": self.MIN_VALIDATOR_STAKE,
            "max_validator_count": self.MAX_VALIDATOR_COUNT,
            "finality_threshold": self.FINALITY_THRESHOLD,
            "genesis_supply": self.GENESIS_SUPPLY,
            "block_reward": self.BLOCK_REWARD,
            "transaction_fee_base": self.TRANSACTION_FEE_BASE
        }

# --- 3. State Transition (Fibonacci Q-Matrix) ---

class PhiState:
    """
    Represents the chain state, evolved via the Fibonacci Q-Matrix.
    State Vector S_n = [F_{n+1}, F_n]^T
    """
    
    def __init__(self, f_n_plus_1: int = 1, f_n: int = 1):
        self.vector = np.array([f_n_plus_1, f_n], dtype=np.int64)
        self.Q_matrix = np.array([[1, 1], [1, 0]], dtype=np.int64)
        self.step = 0
    
    def evolve(self) -> np.ndarray:
        """S_{n+1} = Q * S_n"""
        self.vector = self.Q_matrix @ self.vector
        self.step += 1
        return self.vector
    
    def get_current_metrics(self) -> Tuple[int, int]:
        """Get current Fibonacci state values."""
        return int(self.vector[0]), int(self.vector[1])
    
    def get_state_hash(self) -> str:
        """Generate hash of current state for block inclusion."""
        state_str = f"{self.vector[0]}:{self.vector[1]}:{self.step}"
        return hashlib.sha256(state_str.encode()).hexdigest()

# --- 4. Transaction Structure ---

class PhiTransaction:
    """Φ-Chain transaction with Fibonacci-based validation"""
    
    def __init__(self,
                 sender: str,
                 recipient: str,
                 value: int,
                 data: bytes = b"",
                 nonce: int = 0,
                 gas_limit: int = 21000,
                 signature: bytes = b"",
                 read_set: Optional[List[str]] = None,
                 write_set: Optional[List[str]] = None):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.data = data
        self.nonce = nonce
        self.gas_limit = gas_limit
        self.signature = signature
        self.read_set = read_set or []
        self.write_set = write_set or []
        self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary."""
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "value": self.value,
            "data": self.data.hex() if isinstance(self.data, bytes) else self.data,
            "nonce": self.nonce,
            "gas_limit": self.gas_limit,
            "signature": self.signature.hex() if isinstance(self.signature, bytes) else self.signature,
            "read_set": self.read_set,
            "write_set": self.write_set,
            "timestamp": self.timestamp
        }
    
    def calculate_hash(self) -> str:
        """Calculate transaction hash."""
        import json
        tx_data = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(tx_data.encode()).hexdigest()
    
    def validate(self, blockchain: 'Blockchain') -> bool:
        """Validate transaction against blockchain state."""
        # Check if sender has sufficient balance
        sender_balance = blockchain.get_balance(self.sender)
        if sender_balance < self.value:
            return False
        
        # Check if nonce is correct
        # (In production, track nonce per address)
        return True

# --- 5. Block Structure ---

class PhiBlock:
    """Φ-Chain block with Fibonacci state and PoC mining"""
    
    def __init__(self,
                 index: int,
                 previous_hash: str,
                 timestamp: float,
                 transactions: List[PhiTransaction],
                 state_root: str,
                 proposer: str,
                 f_vector: Tuple[int, int],
                 bls_signature: Optional[bytes] = None,
                 nonce: int = 0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.state_root = state_root
        self.proposer = proposer
        self.f_vector = f_vector  # Fibonacci state at this block
        self.bls_signature = bls_signature
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate block hash including Fibonacci state."""
        import json
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "proposer": self.proposer,
            "f_vector": list(self.f_vector),
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine(self, difficulty: int = 2) -> bool:
        """Proof-of-Work mining with Fibonacci difficulty."""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return True

# --- 6. Blockchain Implementation ---

class Blockchain:
    """Φ-Chain distributed ledger with PoC mining and FBA consensus"""
    
    def __init__(self, genesis_params: Optional[GenesisParameters] = None):
        """Initialize the blockchain with Genesis Block."""
        self.chain: List[PhiBlock] = []
        self.pending_transactions: List[PhiTransaction] = []
        self.validators: Dict[str, Dict[str, Any]] = {}
        self.state = PhiState()
        self.params = genesis_params or GenesisParameters()
        
        # Create and add the Genesis Block
        self.create_genesis_block()
    
    def create_genesis_block(self) -> PhiBlock:
        """Create the Genesis Block with initial state."""
        # Genesis transactions: initial supply distribution
        genesis_txs = [
            PhiTransaction(
                sender="0x0000000000000000000000000000000000000000",
                recipient="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
                value=self.params.GENESIS_SUPPLY,
                nonce=0
            )
        ]
        
        genesis_block = PhiBlock(
            index=0,
            previous_hash="0" * 64,
            timestamp=time.time(),
            transactions=genesis_txs,
            state_root=self.state.get_state_hash(),
            proposer="0x0000000000000000000000000000000000000000",
            f_vector=self.state.get_current_metrics(),
            nonce=0
        )
        
        # Mine the genesis block
        genesis_block.mine(difficulty=2)
        
        self.chain.append(genesis_block)
        return genesis_block
    
    def get_latest_block(self) -> PhiBlock:
        """Get the most recent block in the chain."""
        return self.chain[-1]
    
    def add_block(self, new_block: PhiBlock) -> bool:
        """
        Add a new block to the blockchain.
        
        Args:
            new_block: The block to add
            
        Returns:
            True if the block was added successfully, False otherwise
        """
        # Validate the new block
        if not self.is_valid_block(new_block):
            return False
        
        self.chain.append(new_block)
        
        # Evolve state after block addition
        self.state.evolve()
        
        return True
    
    def is_valid_block(self, block: PhiBlock) -> bool:
        """
        Validate a block according to Φ-Chain rules.
        
        Args:
            block: The block to validate
            
        Returns:
            True if the block is valid, False otherwise
        """
        # Check that the block's previous hash matches the latest block
        if block.previous_hash != self.get_latest_block().hash:
            return False
        
        # Check that the block's hash is correct
        if block.hash != block.calculate_hash():
            return False
        
        # Check that the block index is sequential
        if block.index != len(self.chain):
            return False
        
        # Check that transactions are valid
        for tx in block.transactions:
            if not tx.validate(self):
                return False
        
        return True
    
    def add_transaction(self, transaction: PhiTransaction) -> bool:
        """
        Add a pending transaction to the mempool.
        
        Args:
            transaction: The transaction to add
            
        Returns:
            True if the transaction was added successfully
        """
        # Validate the transaction
        if transaction.validate(self):
            self.pending_transactions.append(transaction)
            return True
        return False
    
    def mine_pending_transactions(self, proposer_id: str, difficulty: int = 2) -> Optional[PhiBlock]:
        """
        Mine pending transactions into a new block (Proof-of-Coherence).
        
        Args:
            proposer_id: The ID of the proposer/validator
            difficulty: The proof-of-work difficulty
            
        Returns:
            The newly mined block, or None if mining failed
        """
        if not self.pending_transactions:
            return None
        
        # Create a new block with pending transactions
        latest_block = self.get_latest_block()
        new_block = PhiBlock(
            index=len(self.chain),
            previous_hash=latest_block.hash,
            timestamp=time.time(),
            transactions=self.pending_transactions.copy(),
            state_root=self.state.get_state_hash(),
            proposer=proposer_id,
            f_vector=self.state.get_current_metrics(),
            nonce=0
        )
        
        # Mine the block
        new_block.mine(difficulty)
        
        # Add the block to the chain
        if self.add_block(new_block):
            self.pending_transactions = []
            return new_block
        
        return None
    
    def get_balance(self, address: str) -> float:
        """
        Calculate the balance for an address.
        
        Args:
            address: The address to check
            
        Returns:
            The balance of the address
        """
        balance = 0.0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.value
                if transaction.recipient == address:
                    balance += transaction.value
        
        return balance
    
    def is_chain_valid(self) -> bool:
        """
        Validate the entire blockchain.
        
        Returns:
            True if the chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check current block's hash
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check link to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_chain_length(self) -> int:
        """Get the length of the blockchain."""
        return len(self.chain)
    
    def get_chain_summary(self) -> Dict[str, Any]:
        """Get a summary of the blockchain."""
        latest_block = self.get_latest_block()
        return {
            "length": len(self.chain),
            "is_valid": self.is_chain_valid(),
            "pending_transactions": len(self.pending_transactions),
            "latest_block_hash": latest_block.hash,
            "latest_block_index": latest_block.index,
            "latest_block_timestamp": latest_block.timestamp,
            "f_vector": latest_block.f_vector,
            "total_supply": self.params.GENESIS_SUPPLY
        }
    
    def add_validator(self, validator_id: str, stake: int) -> bool:
        """
        Add a validator to the network.
        
        Args:
            validator_id: The validator's address
            stake: The amount staked (must be a Fibonacci number)
            
        Returns:
            True if validator was added successfully
        """
        if not FibonacciUtils.is_fibonacci(stake):
            return False
        
        if stake < self.params.MIN_VALIDATOR_STAKE:
            return False
        
        self.validators[validator_id] = {
            "stake": stake,
            "participation": 0,
            "blocks_proposed": 0,
            "rewards": 0
        }
        return True
    
    def get_validator_count(self) -> int:
        """Get the number of active validators."""
        return len(self.validators)

# --- 7. Consensus: Proof-of-Coherence (PoC) ---

class ProofOfCoherence:
    """Proof-of-Coherence consensus mechanism"""
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.validators = blockchain.validators
    
    def calculate_coherence_score(self, validator_id: str) -> float:
        """
        Calculate coherence score for a validator.
        Score = (stake / total_stake) * (participation / total_participation)
        """
        if validator_id not in self.validators:
            return 0.0
        
        validator = self.validators[validator_id]
        total_stake = sum(v["stake"] for v in self.validators.values())
        total_participation = sum(v["participation"] for v in self.validators.values())
        
        if total_stake == 0:
            return 0.0
        
        # If no participation yet, use stake only
        if total_participation == 0:
            return validator["stake"] / total_stake
        
        stake_weight = validator["stake"] / total_stake
        participation_weight = validator["participation"] / total_participation
        
        return stake_weight * participation_weight
    
    def select_proposer(self) -> str:
        """Select the next block proposer based on coherence scores."""
        if not self.validators:
            return ""
        
        scores = {
            vid: self.calculate_coherence_score(vid)
            for vid in self.validators.keys()
        }
        
        # Select validator with highest score
        proposer = max(scores, key=scores.get)
        return proposer
    
    def check_finality(self, block_hash: str, signatures: List[bytes]) -> bool:
        """
        Check if a block has reached finality.
        Finality requires signatures from at least F_15 = 610 validators.
        """
        return len(signatures) >= self.blockchain.params.FINALITY_THRESHOLD

# --- 8. Fibonacci Byzantine Agreement (FBA) ---

class FBAConsensus:
    """Fibonacci Byzantine Agreement consensus protocol"""
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.validators = blockchain.validators
    
    def check_supermajority(self, votes: int) -> bool:
        """
        Check if votes reach supermajority threshold.
        Threshold = (2 * total_validators) // 3 + 1
        """
        total_validators = len(self.validators)
        threshold = (2 * total_validators) // 3 + 1
        return votes >= threshold
    
    def process_vote(self, validator_id: str, block_hash: str, vote_type: str) -> bool:
        """
        Process a vote from a validator.
        
        Args:
            validator_id: The validator's ID
            block_hash: The block being voted on
            vote_type: "prepare" or "commit"
            
        Returns:
            True if vote is valid and processed
        """
        if validator_id not in self.validators:
            return False
        
        # In production, verify BLS signature and track votes
        self.validators[validator_id]["participation"] += 1
        return True

# --- 9. Genesis Block Generation ---

def generate_genesis_block() -> PhiBlock:
    """Generate the Φ-Chain Genesis Block."""
    params = GenesisParameters()
    state = PhiState()
    
    # Genesis transactions
    genesis_txs = [
        PhiTransaction(
            sender="0x0000000000000000000000000000000000000000",
            recipient="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            value=params.GENESIS_SUPPLY,
            nonce=0
        )
    ]
    
    genesis_block = PhiBlock(
        index=0,
        previous_hash="0" * 64,
        timestamp=time.time(),
        transactions=genesis_txs,
        state_root=state.get_state_hash(),
        proposer="0x0000000000000000000000000000000000000000",
        f_vector=state.get_current_metrics(),
        nonce=0
    )
    
    # Mine the genesis block
    genesis_block.mine(difficulty=2)
    
    return genesis_block

# --- 10. Utility Functions ---

def save_blockchain_to_file(blockchain: Blockchain, filename: str):
    """Save blockchain state to JSON file."""
    data = {
        "chain": [
            {
                "index": int(block.index),
                "hash": block.hash,
                "previous_hash": block.previous_hash,
                "timestamp": float(block.timestamp),
                "proposer": block.proposer,
                "f_vector": [int(x) for x in block.f_vector],
                "transactions": [tx.to_dict() for tx in block.transactions]
            }
            for block in blockchain.chain
        ],
        "validators": {
            vid: {
                "stake": int(v["stake"]),
                "participation": int(v["participation"]),
                "blocks_proposed": int(v["blocks_proposed"]),
                "rewards": float(v["rewards"])
            }
            for vid, v in blockchain.validators.items()
        },
        "state": {
            "vector": [int(x) for x in blockchain.state.vector],
            "step": int(blockchain.state.step)
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    # Quick verification and demonstration
    print("=" * 60)
    print("Φ-CHAIN CORE ENGINE - INITIALIZATION")
    print("=" * 60)
    
    # Initialize blockchain
    blockchain = Blockchain()
    print(f"\n✅ Blockchain initialized with {blockchain.get_chain_length()} block(s)")
    
    # Display genesis block
    genesis = blockchain.get_latest_block()
    print(f"\nGenesis Block:")
    print(f"  Index: {genesis.index}")
    print(f"  Hash: {genesis.hash}")
    print(f"  Proposer: {genesis.proposer}")
    print(f"  F-Vector: {genesis.f_vector}")
    
    # Display parameters
    params = GenesisParameters()
    print(f"\nGenesis Parameters:")
    print(f"  PHI: {params.PHI}")
    print(f"  Slot Duration: {params.SLOT_DURATION} seconds (F_6)")
    print(f"  Epoch Duration: {params.EPOCH_DURATION} seconds (F_18)")
    print(f"  Min Validator Stake: {params.MIN_VALIDATOR_STAKE} Φ (F_20)")
    print(f"  Genesis Supply: {params.GENESIS_SUPPLY} Φ (F_33)")
    
    # Test PoC mining
    print(f"\nTesting PoC Mining...")
    tx = PhiTransaction(
        sender="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        recipient="0x0000000000000000000000000000000000000000",
        value=89,
        nonce=1
    )
    blockchain.add_transaction(tx)
    
    block = blockchain.mine_pending_transactions("validator_001")
    if block:
        print(f"✅ Block mined successfully!")
        print(f"  New Block Index: {block.index}")
        print(f"  New Block Hash: {block.hash}")
    else:
        print(f"❌ Mining failed")
    
    # Display chain summary
    summary = blockchain.get_chain_summary()
    print(f"\nChain Summary:")
    print(f"  Length: {summary['length']}")
    print(f"  Valid: {summary['is_valid']}")
    print(f"  Latest Block: #{summary['latest_block_index']}")
    print(f"  Total Supply: {summary['total_supply']} Φ")
    
    print("\n" + "=" * 60)
    print("Φ-CHAIN CORE ENGINE - READY")
    print("=" * 60)
