"""
Φ-Chain Integration Module: Bridging the Reversible Core with the Canonical Architecture

This module integrates the reversible Fibonacci core with the existing phi_chain_core and
phi_chain_prototype modules, creating a unified system where:

- The forward chain (phi_chain_prototype) operates on positive Fibonacci indices
- The reversible core (reversible_phi_core) provides bidirectional state transitions
- The integration layer ensures mathematical consistency across all layers
- Economic models, consensus, and cryptography are unified under Φ-invariant principles

The result is a blockchain that operates on universal law, not arbitrary convention.
"""

import json
from typing import Dict, List, Tuple
import numpy as np
from phi_chain_core import FibonacciUtils, GenesisParameters, ValidatorSet, FibonacciQMatrix
from reversible_phi_core import ReversibleFibonacciCore, TetrahedralPruning


class UnifiedPhiChain:
    """
    Unified architecture combining forward chain with reversible core.
    
    This class orchestrates the interaction between:
    1. Forward chain (positive indices, creation)
    2. Reversible core (bidirectional, resolution)
    3. Economic model (Fibonacci-scaled incentives)
    4. Consensus (Fibonacci Byzantine Agreement + Quantum Loop)
    """
    
    def __init__(self):
        """Initialize the unified Φ-Chain system."""
        # Forward chain components
        self.genesis_params = GenesisParameters()
        self.validator_set = ValidatorSet(self.genesis_params)
        self.q_matrix = FibonacciQMatrix()
        
        # Reversible core components
        self.reversible_core = ReversibleFibonacciCore()
        self.pruning = TetrahedralPruning()
        
        # Load the reversible genesis
        try:
            with open("reversible_phi_genesis.json", "r") as f:
                self.reversible_genesis = json.load(f)
        except FileNotFoundError:
            self.reversible_genesis = None
    
    def validate_phi_invariance(self) -> bool:
        """
        Verify that the system maintains Φ-invariance across all layers.
        
        Φ-invariance means:
        - F(n) + F(-n) = 0 for all n > 0
        - Economic rewards + penalties = 0
        - State transitions preserve the Golden Ratio eigenvalue
        
        Returns:
            True if all invariance checks pass
        """
        checks = []
        
        # Check 1: Bidirectional Fibonacci symmetry
        for n in range(1, 21):
            forward = self.reversible_core.fib(n)
            backward = self.reversible_core.fib(-n)
            if forward + backward != 0:
                checks.append(False)
            else:
                checks.append(True)
        
        # Check 2: Q-Matrix eigenvalues
        eigenvalues = self.q_matrix.eigenvalues()
        phi_check = abs(eigenvalues[0] - self.reversible_core.phi) < 1e-10
        checks.append(phi_check)
        
        # Check 3: Economic symmetry
        if self.reversible_genesis:
            slashing_tiers = self.reversible_genesis.get("economic_model", {}).get("slashing_tiers", {})
            for tier_name, tier_data in slashing_tiers.items():
                net = tier_data.get("net_balance", 1)
                if net != 0:
                    checks.append(False)
                else:
                    checks.append(True)
        
        return all(checks)
    
    def compute_validator_effective_stake(self, base_stake: int, borrowed_negative: int) -> int:
        """
        Compute the effective stake using reversible Fibonacci mechanics.
        
        Validators can borrow negative Fibonacci amounts to increase their
        effective stake, creating asymmetric growth potential while maintaining
        perfect symmetry in the economic model.
        
        Args:
            base_stake: The validator's positive Fibonacci stake
            borrowed_negative: The negative Fibonacci amount borrowed (as a negative number)
            
        Returns:
            The net effective stake
        """
        # Verify both are Fibonacci numbers
        if not FibonacciUtils.is_fibonacci(abs(base_stake)):
            raise ValueError(f"{base_stake} is not a Fibonacci number")
        if not FibonacciUtils.is_fibonacci(abs(borrowed_negative)):
            raise ValueError(f"{borrowed_negative} is not a Fibonacci number")
        
        return base_stake + borrowed_negative
    
    def generate_zeckendorf_address(self, validator_id: str) -> List[int]:
        """
        Generate a Zeckendorf-encoded address for a validator.
        
        This creates a unique, non-arbitrary address based on the validator's
        ID hashed through Fibonacci representation.
        
        Args:
            validator_id: The validator's identifier
            
        Returns:
            A list of Fibonacci numbers representing the address
        """
        # Hash the validator ID to a number
        hash_value = int(hashlib.sha256(validator_id.encode()).hexdigest(), 16) % (2**32)
        
        # Encode as Zeckendorf representation
        return self.reversible_core.zeckendorf_representation(hash_value)
    
    def compute_state_transition_reversible(self, state: np.ndarray, steps: int, direction: str = "forward") -> np.ndarray:
        """
        Compute state transitions in either direction.
        
        Args:
            state: The current state vector
            steps: The number of steps to transition
            direction: "forward" or "backward"
            
        Returns:
            The state after transitions
        """
        result = state.copy()
        
        if direction == "forward":
            for _ in range(steps):
                result = self.q_matrix.transition(result)
        elif direction == "backward":
            # Use the inverse matrix for backward transitions
            q_inv = np.linalg.inv(self.q_matrix.Q.astype(np.float64))
            for _ in range(steps):
                result = q_inv @ result
        else:
            raise ValueError(f"Unknown direction: {direction}")
        
        return result
    
    def demonstrate_integration(self):
        """Display key integration insights."""
        print("\n" + "=" * 70)
        print("UNIFIED Φ-CHAIN INTEGRATION DEMONSTRATION")
        print("=" * 70)
        
        print("\n1. PHI-INVARIANCE VERIFICATION:")
        invariant = self.validate_phi_invariance()
        print(f"   All checks passed: {invariant}")
        
        print("\n2. VALIDATOR EFFECTIVE STAKE CALCULATION:")
        base = FibonacciUtils.fibonacci(10)  # 55
        borrowed = FibonacciUtils.fibonacci(-9)  # -34
        effective = self.compute_validator_effective_stake(base, borrowed)
        print(f"   Base stake F(10): {base}")
        print(f"   Borrowed F(-9): {borrowed}")
        print(f"   Effective stake: {effective}")
        
        print("\n3. ZECKENDORF ADDRESS GENERATION:")
        addr = self.generate_zeckendorf_address("validator_1")
        print(f"   Validator 1 address: {addr}")
        
        print("\n4. STATE TRANSITION (FORWARD & BACKWARD):")
        initial_state = np.array([FibonacciUtils.fibonacci(2), FibonacciUtils.fibonacci(1)])
        print(f"   Initial state: {initial_state}")
        
        forward_state = self.compute_state_transition_reversible(initial_state, 3, "forward")
        print(f"   After 3 forward steps: {forward_state}")
        
        backward_state = self.compute_state_transition_reversible(forward_state, 3, "backward")
        print(f"   After 3 backward steps: {backward_state}")
        print(f"   Recovery check (should match initial): {np.allclose(backward_state, initial_state)}")
        
        print("\n5. REVERSIBLE GENESIS METADATA:")
        if self.reversible_genesis:
            meta = self.reversible_genesis.get("metadata", {})
            print(f"   Chain name: {meta.get('chain_name')}")
            print(f"   Creator: {meta.get('creator')}")
            print(f"   Vision: {meta.get('vision')}")
            print(f"   Quantum symmetric: {meta.get('quantum_symmetric')}")
        
        print("\n" + "=" * 70)
        print("✅ UNIFIED Φ-CHAIN INTEGRATION COMPLETE")
        print("=" * 70)


import hashlib

if __name__ == "__main__":
    unified = UnifiedPhiChain()
    unified.demonstrate_integration()
