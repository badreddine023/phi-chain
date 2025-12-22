"""
phi_chain_core.py - Core Data Structures and Fibonacci Logic for Phi Chain
This module defines the fundamental data structures and mathematical logic
for the Phi Chain, including Fibonacci-derived parameters and Q-Matrix state transitions.
"""

import time
import math
import numpy as np
from typing import List, Dict, Optional, Tuple
from decimal import Decimal, getcontext

# --- 1. Fibonacci & Golden Ratio Utilities ---

class FibonacciUtils:
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
    def golden_ratio(precision: int = 60) -> Decimal:
        """Calculates the Golden Ratio (Φ) with high precision."""
        getcontext().prec = precision + 10
        sqrt5 = Decimal(5).sqrt()
        phi = (Decimal(1) + sqrt5) / Decimal(2)
        getcontext().prec = precision
        return +phi

    @staticmethod
    def is_fibonacci(n: int) -> bool:
        """Checks if a number is a Fibonacci number."""
        if n < 0: return False
        def is_perfect_square(x):
            s = int(math.isqrt(x))
            return s*s == x
        return is_perfect_square(5*n*n + 4) or is_perfect_square(5*n*n - 4)

# --- 2. Genesis Parameters (Derived from Fibonacci) ---

class GenesisParameters:
    def __init__(self):
        self.PHI = float(FibonacciUtils.golden_ratio())
        self.SLOT_DURATION = FibonacciUtils.fibonacci(6)      # F_6 = 8
        self.EPOCH_DURATION = FibonacciUtils.fibonacci(18)    # F_18 = 2584
        self.MIN_VALIDATOR_STAKE = FibonacciUtils.fibonacci(20) # F_20 = 6765
        self.MAX_VALIDATOR_COUNT = FibonacciUtils.fibonacci(17) # F_17 = 1597
        self.TARGET_COMMITTEE_SIZE = FibonacciUtils.fibonacci(14) # F_14 = 377
        self.FINALITY_THRESHOLD = FibonacciUtils.fibonacci(15) # F_15 = 610
        
    def to_dict(self) -> Dict:
        return {
            "phi": self.PHI,
            "slot_duration": self.SLOT_DURATION,
            "epoch_duration": self.EPOCH_DURATION,
            "min_validator_stake": self.MIN_VALIDATOR_STAKE,
            "max_validator_count": self.MAX_VALIDATOR_COUNT,
            "finality_threshold": self.FINALITY_THRESHOLD
        }

# --- 3. State Transition (Fibonacci Q-Matrix) ---

class PhiState:
    """
    Represents the chain state, evolved via the Fibonacci Q-Matrix.
    State Vector S_n = [F_{n+1}, F_n]^T
    """
    def __init__(self, f_n_plus_1: int = 1, f_n: int = 1):
        self.vector = np.array([f_n_plus_1, f_n])
        self.Q_matrix = np.array([[1, 1], [1, 0]])

    def evolve(self):
        """S_{n+1} = Q * S_n"""
        self.vector = self.Q_matrix @ self.vector
        return self.vector

    def get_current_metrics(self) -> Tuple[int, int]:
        return int(self.vector[0]), int(self.vector[1])

# --- 4. Transaction Structure ---

class PhiTransaction:
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

    def to_dict(self) -> Dict:
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
        }

# --- 5. Block Structure ---

class PhiBlock:
    def __init__(self,
                 index: int,
                 previous_hash: str,
                 timestamp: float,
                 transactions: List[PhiTransaction],
                 state_root: str,
                 proposer: str,
                 f_vector: Tuple[int, int],
                 bls_signature: Optional[bytes] = None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.state_root = state_root
        self.proposer = proposer
        self.f_vector = f_vector # Fibonacci state at this block
        self.bls_signature = bls_signature

    def calculate_hash(self) -> str:
        import hashlib
        import json
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "proposer": self.proposer,
            "f_vector": list(self.f_vector)
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

# --- 6. Consensus Message ---

class PipelinedBFTMessage:
    def __init__(self, msg_type: str, block_hash: str, validator_id: str, signature: bytes):
        self.msg_type = msg_type
        self.block_hash = block_hash
        self.validator_id = validator_id
        self.signature = signature

    @staticmethod
    def check_supermajority(votes: int, total_validators: int) -> bool:
        threshold = (2 * total_validators) // 3 + 1
        return votes >= threshold

if __name__ == "__main__":
    # Quick verification
    utils = FibonacciUtils()
    params = GenesisParameters()
    state = PhiState(utils.fibonacci(2), utils.fibonacci(1))
    
    print(f"Genesis PHI: {params.PHI}")
    print(f"Initial State: {state.get_current_metrics()}")
    state.evolve()
    print(f"Evolved State: {state.get_current_metrics()}")
    
    tx = PhiTransaction("0xAlice", "0xBob", 100)
    block = PhiBlock(0, "0"*64, time.time(), [tx], "root", "proposer", state.get_current_metrics())
    print(f"Genesis Block Hash: {block.calculate_hash()}")
