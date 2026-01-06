#!/usr/bin/env python3
"""
Φ-Chain Consensus Module: Fibonacci-Based Proof-of-Coherence (PoC)

This module implements the core consensus mechanism for Φ-Chain, where validator
weights are determined by Fibonacci numbers and the finality threshold is the
reciprocal of the Golden Ratio (61.8%).

Mathematical Foundation:
- Validator weight: w(v) = F(v_index + 1) / F(v_index) → φ
- Finality threshold: 1/φ ≈ 0.618 (61.8% of total weight)
- Block finality: Achieved when cumulative weight ≥ finality threshold
"""

import hashlib
import math
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Golden Ratio constant
PHI = (1 + math.sqrt(5)) / 2
PHI_RECIPROCAL = 1 / PHI  # ≈ 0.618

# Fibonacci sequence (pre-computed for efficiency)
FIBONACCI = [0, 1]
for i in range(2, 100):
    FIBONACCI.append(FIBONACCI[-1] + FIBONACCI[-2])


@dataclass
class Validator:
    """Represents a validator in the Φ-Chain network."""
    index: int
    stake: int
    participation_rate: float
    
    def get_fibonacci_weight(self) -> float:
        """
        Calculate validator weight based on Fibonacci sequence.
        
        Weight = F(index + 1) / F(index) → φ as index increases
        """
        if self.index >= len(FIBONACCI) - 1:
            return PHI  # Converges to φ for large indices
        
        fib_next = FIBONACCI[self.index + 1]
        fib_curr = FIBONACCI[self.index]
        
        if fib_curr == 0:
            return 1.0
        
        return fib_next / fib_curr
    
    def get_coherence_score(self) -> float:
        """
        Calculate Coherence Score for validator selection.
        
        Coherence = (Stake / Participation Rate) × φ
        """
        if self.participation_rate == 0:
            return 0.0
        
        return (self.stake / self.participation_rate) * PHI


class ProofOfCoherence:
    """Implements Proof-of-Coherence consensus mechanism."""
    
    def __init__(self, validators: List[Validator]):
        """
        Initialize PoC consensus with a list of validators.
        
        Args:
            validators: List of Validator objects
        """
        self.validators = validators
        self.finality_threshold = PHI_RECIPROCAL  # 61.8%
    
    def calculate_total_weight(self) -> float:
        """Calculate total weight of all validators."""
        return sum(v.get_fibonacci_weight() * v.stake for v in self.validators)
    
    def calculate_validator_weights(self) -> Dict[int, float]:
        """
        Calculate normalized weights for all validators.
        
        Returns:
            Dictionary mapping validator index to normalized weight
        """
        total_weight = self.calculate_total_weight()
        
        if total_weight == 0:
            return {}
        
        weights = {}
        for validator in self.validators:
            fib_weight = validator.get_fibonacci_weight()
            normalized_weight = (fib_weight * validator.stake) / total_weight
            weights[validator.index] = normalized_weight
        
        return weights
    
    def check_finality(self, signatures: Dict[int, bool]) -> bool:
        """
        Check if a block has achieved finality.
        
        A block is final when cumulative weight of signatures ≥ finality threshold.
        
        Args:
            signatures: Dictionary mapping validator index to signature presence
        
        Returns:
            True if block is final, False otherwise
        """
        weights = self.calculate_validator_weights()
        cumulative_weight = sum(
            weights.get(v_index, 0) 
            for v_index, has_signature in signatures.items() 
            if has_signature
        )
        
        return cumulative_weight >= self.finality_threshold
    
    def select_proposer(self) -> int:
        """
        Select block proposer using Fibonacci-weighted randomness.
        
        Validators with higher Coherence Scores are selected more frequently.
        
        Returns:
            Index of selected proposer
        """
        if not self.validators:
            raise ValueError("No validators available")
        
        # Calculate coherence scores
        coherence_scores = [v.get_coherence_score() for v in self.validators]
        total_coherence = sum(coherence_scores)
        
        if total_coherence == 0:
            # Fallback to random selection if all coherence scores are 0
            return self.validators[0].index
        
        # Weighted random selection
        import random
        probabilities = [score / total_coherence for score in coherence_scores]
        selected_index = random.choices(
            range(len(self.validators)), 
            weights=probabilities, 
            k=1
        )[0]
        
        return self.validators[selected_index].index


class PhiBasedHashing:
    """Implements φ-based block hashing."""
    
    @staticmethod
    def compute_block_hash(block_data: str, nonce: int) -> str:
        """
        Compute block hash using φ-based encoding.
        
        Hash = SHA256(block_data ⊕ ⌊φ·nonce⌋)
        
        Args:
            block_data: Serialized block data
            nonce: Proof-of-work nonce
        
        Returns:
            Hexadecimal hash string
        """
        # Calculate φ-encoded nonce
        phi_encoded = int(PHI * nonce)
        
        # XOR block data with φ-encoded nonce
        block_bytes = block_data.encode('utf-8')
        nonce_bytes = phi_encoded.to_bytes(32, byteorder='big')
        
        xored_data = bytes(a ^ b for a, b in zip(block_bytes, nonce_bytes))
        
        # Compute SHA256 hash
        hash_object = hashlib.sha256(xored_data)
        return hash_object.hexdigest()
    
    @staticmethod
    def find_valid_nonce(block_data: str, difficulty: int) -> int:
        """
        Find a nonce that produces a hash meeting difficulty requirement.
        
        Difficulty is measured in leading zeros in the hash.
        
        Args:
            block_data: Serialized block data
            difficulty: Number of leading zeros required
        
        Returns:
            Valid nonce
        """
        nonce = 0
        target = '0' * difficulty
        
        while True:
            block_hash = PhiBasedHashing.compute_block_hash(block_data, nonce)
            
            if block_hash.startswith(target):
                return nonce
            
            nonce += 1
            
            # Safety check to prevent infinite loops
            if nonce > 10_000_000:
                raise RuntimeError(f"Could not find valid nonce after {nonce} attempts")


class FibonacciQMatrix:
    """Implements Fibonacci Q-Matrix state transitions."""
    
    @staticmethod
    def compute_state_transition(state: Tuple[int, int]) -> Tuple[int, int]:
        """
        Compute next state using Fibonacci Q-Matrix.
        
        Q = [[1, 1], [1, 0]]
        S_{n+1} = Q · S_n
        
        Args:
            state: Current state vector [F_{n+1}, F_n]
        
        Returns:
            Next state vector [F_{n+2}, F_{n+1}]
        """
        f_n_plus_1, f_n = state
        
        # Q-Matrix multiplication
        # [F_{n+2}] = [1 1] [F_{n+1}]   = [F_{n+1} + F_n]     = [F_{n+2}]
        # [F_{n+1}]   [1 0] [F_n    ]     [F_{n+1}        ]     [F_{n+1}]
        
        f_n_plus_2 = f_n_plus_1 + f_n
        
        return (f_n_plus_2, f_n_plus_1)
    
    @staticmethod
    def evolve_state(initial_state: Tuple[int, int], steps: int) -> Tuple[int, int]:
        """
        Evolve state over multiple steps.
        
        Args:
            initial_state: Initial state vector
            steps: Number of state transitions
        
        Returns:
            Final state after evolution
        """
        state = initial_state
        
        for _ in range(steps):
            state = FibonacciQMatrix.compute_state_transition(state)
        
        return state


# Example usage and testing
if __name__ == "__main__":
    # Create validators
    validators = [
        Validator(index=0, stake=6765, participation_rate=0.95),
        Validator(index=1, stake=10946, participation_rate=0.98),
        Validator(index=2, stake=17711, participation_rate=0.92),
    ]
    
    # Initialize PoC consensus
    poc = ProofOfCoherence(validators)
    
    print("=== Φ-Chain Consensus Test ===\n")
    
    # Test validator weights
    print("Validator Fibonacci Weights:")
    for v in validators:
        weight = v.get_fibonacci_weight()
        print(f"  Validator {v.index}: {weight:.6f}")
    
    print(f"\nTotal Weight: {poc.calculate_total_weight():.2f}")
    print(f"Finality Threshold: {poc.finality_threshold:.4f} (61.8%)\n")
    
    # Test block finality
    signatures = {0: True, 1: True, 2: False}
    is_final = poc.check_finality(signatures)
    print(f"Block Finality (signatures {signatures}): {is_final}\n")
    
    # Test block hashing
    block_data = "genesis_block_data"
    nonce = 12345
    block_hash = PhiBasedHashing.compute_block_hash(block_data, nonce)
    print(f"Block Hash: {block_hash}\n")
    
    # Test Fibonacci Q-Matrix
    initial_state = (1, 1)  # F_2, F_1
    final_state = FibonacciQMatrix.evolve_state(initial_state, 5)
    print(f"Fibonacci Q-Matrix Evolution: {initial_state} → {final_state}")
    print(f"Expected: (13, 8) [F_7, F_6]")
