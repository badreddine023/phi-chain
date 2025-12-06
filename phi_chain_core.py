"""
Φ-Chain Core Module

This module contains the core components of the Φ-Chain blockchain architecture,
including Fibonacci utilities, parameter derivation, and the Fibonacci Q-Matrix
state transition logic.
"""

import math
import numpy as np
from typing import List, Tuple, Dict

# --- 1. Fibonacci Utility Functions ---

class FibonacciUtils:
    """Utility class for Fibonacci sequence calculations."""
    
    # Cache for Fibonacci numbers to avoid recalculation
    _fib_cache = {}
    
    @classmethod
    def fibonacci(cls, n: int) -> int:
        """
        Calculate the nth Fibonacci number F_n.
        
        Args:
            n: The index of the Fibonacci number to calculate.
        
        Returns:
            The nth Fibonacci number.
        """
        if n in cls._fib_cache:
            return cls._fib_cache[n]
        
        if n <= 0:
            return 0
        if n == 1 or n == 2:
            return 1
        
        # Use Binet's formula for efficiency
        phi = (1 + math.sqrt(5)) / 2
        result = int(round((phi**n - (1-phi)**n) / math.sqrt(5)))
        cls._fib_cache[n] = result
        return result
    
    @classmethod
    def golden_ratio(cls, precision: int = 59) -> float:
        """
        Calculate the Golden Ratio (Phi) to a specified precision.
        
        Args:
            precision: Number of decimal places.
        
        Returns:
            The Golden Ratio as a float.
        """
        return (1 + math.sqrt(5)) / 2
    
    @classmethod
    def is_fibonacci(cls, num: int) -> bool:
        """
        Check if a number is a Fibonacci number.
        
        Args:
            num: The number to check.
        
        Returns:
            True if the number is a Fibonacci number, False otherwise.
        """
        # A number is Fibonacci if one or both of (5*n^2 + 4) or (5*n^2 - 4) is a perfect square
        def is_perfect_square(x):
            sqrt = int(math.sqrt(x))
            return sqrt * sqrt == x
        
        return is_perfect_square(5 * num * num + 4) or is_perfect_square(5 * num * num - 4)


# --- 2. Genesis Parameters ---

class GenesisParameters:
    """Encapsulates all genesis parameters of the Φ-Chain."""
    
    def __init__(self):
        """Initialize all genesis parameters from Fibonacci indices."""
        self.phi = FibonacciUtils.golden_ratio()
        
        # Timing Parameters
        self.slot_duration = FibonacciUtils.fibonacci(6)  # 8 seconds
        self.epoch_duration = FibonacciUtils.fibonacci(18)  # 2584 seconds
        self.slots_per_epoch = self.epoch_duration // self.slot_duration  # 323
        
        # Consensus Parameters
        self.max_validators = FibonacciUtils.fibonacci(17)  # 1597
        self.committee_size = FibonacciUtils.fibonacci(14)  # 377
        self.finality_threshold = FibonacciUtils.fibonacci(15)  # 610
        self.proof_recursion_limit = FibonacciUtils.fibonacci(11)  # 89
        self.state_expiry_epochs = FibonacciUtils.fibonacci(13)  # 233
        
        # Economic Parameters
        self.min_validator_stake = FibonacciUtils.fibonacci(20)  # 6765 tokens
        
        # Balance and Fee Tiers
        self.balance_tiers = [FibonacciUtils.fibonacci(i) for i in range(1, 16)]
        self.fee_tiers = [FibonacciUtils.fibonacci(i) for i in range(1, 13)]
        
        # Shard Schedule
        self.shard_schedule = {
            0: FibonacciUtils.fibonacci(3),  # 2 shards
            FibonacciUtils.fibonacci(18): FibonacciUtils.fibonacci(4),  # 3 shards
            FibonacciUtils.fibonacci(20): FibonacciUtils.fibonacci(5),  # 5 shards
            FibonacciUtils.fibonacci(21): FibonacciUtils.fibonacci(6),  # 8 shards
            FibonacciUtils.fibonacci(22): FibonacciUtils.fibonacci(7),  # 13 shards
            FibonacciUtils.fibonacci(23): FibonacciUtils.fibonacci(8),  # 21 shards
        }
    
    def to_dict(self) -> Dict:
        """Convert parameters to a dictionary."""
        return {
            "phi": self.phi,
            "slot_duration": self.slot_duration,
            "epoch_duration": self.epoch_duration,
            "slots_per_epoch": self.slots_per_epoch,
            "max_validators": self.max_validators,
            "committee_size": self.committee_size,
            "finality_threshold": self.finality_threshold,
            "proof_recursion_limit": self.proof_recursion_limit,
            "state_expiry_epochs": self.state_expiry_epochs,
            "min_validator_stake": self.min_validator_stake,
            "balance_tiers": self.balance_tiers,
            "fee_tiers": self.fee_tiers,
            "shard_schedule": self.shard_schedule,
        }
    
    def print_parameters(self):
        """Print all genesis parameters in a formatted manner."""
        print("=" * 60)
        print("Φ-CHAIN GENESIS PARAMETERS")
        print("=" * 60)
        print(f"\nGolden Ratio (Φ): {self.phi:.59f}")
        print(f"\nTiming Parameters:")
        print(f"  Slot Duration:     {self.slot_duration} seconds (F_6)")
        print(f"  Epoch Duration:    {self.epoch_duration} seconds (F_18)")
        print(f"  Slots per Epoch:   {self.slots_per_epoch} (F_18 / F_6)")
        print(f"\nConsensus Parameters:")
        print(f"  Max Validators:    {self.max_validators} (F_17)")
        print(f"  Committee Size:    {self.committee_size} (F_14)")
        print(f"  Finality Threshold: {self.finality_threshold} signatures (F_15)")
        print(f"  Proof Recursion Limit: {self.proof_recursion_limit} (F_11)")
        print(f"  State Expiry:      {self.state_expiry_epochs} epochs (F_13)")
        print(f"\nEconomic Parameters:")
        print(f"  Min Validator Stake: {self.min_validator_stake} tokens (F_20)")
        print(f"  Balance Tiers:     {self.balance_tiers}")
        print(f"  Fee Tiers:         {self.fee_tiers}")
        print("\n" + "=" * 60)


# --- 3. Fibonacci Q-Matrix State Transition ---

class FibonacciQMatrix:
    """Implements the Fibonacci Q-Matrix for state transitions."""
    
    def __init__(self):
        """Initialize the Fibonacci Q-Matrix."""
        self.Q = np.array([[1, 1], [1, 0]], dtype=np.int64)
    
    def transition(self, state: np.ndarray) -> np.ndarray:
        """
        Perform a single state transition using the Q-Matrix.
        
        Args:
            state: The current state vector [F_{n+1}, F_n].
        
        Returns:
            The next state vector [F_{n+2}, F_{n+1}].
        """
        return self.Q @ state
    
    def transition_n_steps(self, state: np.ndarray, n: int) -> np.ndarray:
        """
        Perform n state transitions.
        
        Args:
            state: The initial state vector.
            n: The number of transitions.
        
        Returns:
            The state after n transitions.
        """
        result = state.copy()
        for _ in range(n):
            result = self.transition(result)
        return result
    
    def eigenvalues(self) -> Tuple[float, float]:
        """
        Calculate the eigenvalues of the Q-Matrix.
        
        Returns:
            A tuple of the two eigenvalues.
        """
        eigenvalues = np.linalg.eigvals(self.Q)
        return tuple(sorted(eigenvalues, reverse=True))
    
    def simulate(self, initial_state: np.ndarray, steps: int):
        """
        Simulate state transitions for a given number of steps.
        
        Args:
            initial_state: The initial state vector.
            steps: The number of transitions to perform.
        """
        print("=" * 60)
        print("FIBONACCI Q-MATRIX STATE TRANSITIONS")
        print("=" * 60)
        print(f"\nQ-Matrix:\n{self.Q}")
        print(f"\nEigenvalues: {self.eigenvalues()}")
        print(f"\nInitial State: {initial_state}")
        
        current_state = initial_state.copy()
        for i in range(1, steps + 1):
            current_state = self.transition(current_state)
            print(f"State S_{i}: {current_state}")
        
        print("\n" + "=" * 60)


# --- 4. Validator and Stake Management ---

class ValidatorSet:
    """Manages validators and their stakes."""
    
    def __init__(self, genesis_params: GenesisParameters):
        """
        Initialize the validator set.
        
        Args:
            genesis_params: The genesis parameters.
        """
        self.genesis_params = genesis_params
        self.validators = {}  # {validator_id: stake}
    
    def add_validator(self, validator_id: str, stake: int) -> bool:
        """
        Add a validator to the set.
        
        Args:
            validator_id: Unique identifier for the validator.
            stake: The amount of tokens staked.
        
        Returns:
            True if the validator was added, False if the stake is below the minimum.
        """
        if stake < self.genesis_params.min_validator_stake:
            return False
        
        if len(self.validators) >= self.genesis_params.max_validators:
            return False
        
        self.validators[validator_id] = stake
        return True
    
    def get_total_stake(self) -> int:
        """Get the total stake across all validators."""
        return sum(self.validators.values())
    
    def get_validator_weight(self, validator_id: str) -> float:
        """
        Get the weight of a validator (stake / total stake).
        
        Args:
            validator_id: The validator's ID.
        
        Returns:
            The validator's weight as a fraction.
        """
        total_stake = self.get_total_stake()
        if total_stake == 0:
            return 0.0
        return self.validators.get(validator_id, 0) / total_stake


# --- 5. Core Demonstrator ---

def demonstrate_core_logic():
    """Demonstrates the core mathematical and parameter logic of the Φ-Chain."""
    # Initialize genesis parameters
    genesis = GenesisParameters()
    genesis.print_parameters()
    
    # Initialize and simulate the Q-Matrix
    q_matrix = FibonacciQMatrix()
    initial_state = np.array([FibonacciUtils.fibonacci(2), FibonacciUtils.fibonacci(1)])
    q_matrix.simulate(initial_state, steps=8)
    
    # Initialize validator set
    validators = ValidatorSet(genesis)
    print("\n" + "=" * 60)
    print("VALIDATOR SET EXAMPLE")
    print("=" * 60)
    
    # Add some validators with Fibonacci stakes
    for i in range(1, 6):
        stake = FibonacciUtils.fibonacci(20 + i)
        validator_id = f"validator_{i}"
        if validators.add_validator(validator_id, stake):
            print(f"Added {validator_id} with stake {stake} tokens")
    
    print(f"\nTotal Validators: {len(validators.validators)}")
    print(f"Total Stake: {validators.get_total_stake()} tokens")
    print("=" * 60)

if __name__ == "__main__":
    demonstrate_core_logic()
