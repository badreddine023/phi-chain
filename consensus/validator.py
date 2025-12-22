"""
consensus/validator.py: Validator management for Φ-Chain

This module implements validator selection, stake management, and
the Fibonacci Byzantine Agreement (FBA) consensus mechanism.
"""

from typing import Dict, List, Optional
import random
import sys
sys.path.insert(0, '..')
from phi_chain_core import FibonacciUtils, GenesisParameters


class Validator:
    """
    A validator in the Φ-Chain network.
    
    Each validator maintains:
    - Stake (must be a Fibonacci number)
    - Performance metrics
    - Slashing history
    """
    
    def __init__(self, validator_id: str, stake: int):
        """
        Initialize a validator.
        
        Args:
            validator_id: Unique identifier
            stake: The validator's stake (must be Fibonacci)
        """
        self.validator_id = validator_id
        self.stake = stake
        self.active = True
        self.blocks_proposed = 0
        self.blocks_finalized = 0
        self.slashing_count = 0
        self.reputation = 1.0
    
    def propose_block(self) -> bool:
        """Record that this validator proposed a block."""
        if not self.active:
            return False
        self.blocks_proposed += 1
        return True
    
    def finalize_block(self) -> bool:
        """Record that this validator finalized a block."""
        if not self.active:
            return False
        self.blocks_finalized += 1
        return True
    
    def slash(self, amount: int) -> bool:
        """
        Slash the validator's stake for misbehavior.
        
        Args:
            amount: Amount to slash
            
        Returns:
            True if slash was successful
        """
        if self.stake < amount:
            return False
        
        self.stake -= amount
        self.slashing_count += 1
        
        # Deactivate if stake drops below minimum
        if self.stake < FibonacciUtils.fibonacci(20):
            self.active = False
        
        return True
    
    def get_performance_score(self) -> float:
        """Calculate the validator's performance score."""
        if self.blocks_proposed == 0:
            return 0.5
        
        finalization_rate = self.blocks_finalized / self.blocks_proposed
        slashing_penalty = 1.0 - (self.slashing_count * 0.1)
        
        return (finalization_rate + slashing_penalty) / 2.0


class ValidatorSet:
    """
    The set of validators in the Φ-Chain network.
    
    Manages validator registration, selection, and consensus.
    """
    
    def __init__(self, genesis_params: GenesisParameters = None):
        """
        Initialize the validator set.
        
        Args:
            genesis_params: The Φ-Chain genesis parameters
        """
        self.genesis_params = genesis_params or GenesisParameters()
        self.validators: Dict[str, Validator] = {}
        self.current_epoch = 0
        self.total_stake = 0
    
    def register_validator(self, validator_id: str, stake: int) -> bool:
        """
        Register a new validator.
        
        Args:
            validator_id: The validator's ID
            stake: The validator's stake (must be Fibonacci)
            
        Returns:
            True if registration was successful
        """
        # Check that stake is a Fibonacci number
        if not FibonacciUtils.is_fibonacci(stake):
            return False
        
        # Check minimum stake
        if stake < self.genesis_params.MIN_VALIDATOR_STAKE:
            return False
        
        # Check that validator doesn't already exist
        if validator_id in self.validators:
            return False
        
        # Register the validator
        self.validators[validator_id] = Validator(validator_id, stake)
        self.total_stake += stake
        
        return True
    
    def select_proposer(self) -> Optional[str]:
        """
        Select the next block proposer using Fibonacci-weighted selection.
        
        Returns:
            The ID of the selected proposer, or None if no validators available
        """
        if not self.validators:
            return None
        
        # Get active validators
        active_validators = [v for v in self.validators.values() if v.active]
        if not active_validators:
            return None
        
        # Compute selection probabilities based on stake
        total_stake = sum(v.stake for v in active_validators)
        
        # Weighted random selection
        r = random.uniform(0, total_stake)
        cumulative = 0
        
        for validator in active_validators:
            cumulative += validator.stake
            if r <= cumulative:
                return validator.validator_id
        
        return active_validators[-1].validator_id
    
    def get_finality_threshold(self) -> int:
        """
        Get the number of signatures required for finality.
        
        Returns:
            The finality threshold (F_15 = 610)
        """
        return self.genesis_params.FINALITY_THRESHOLD
    
    def check_finality(self, signatures: int) -> bool:
        """
        Check if a block has reached finality.
        
        Args:
            signatures: Number of signatures received
            
        Returns:
            True if the block is finalized
        """
        return signatures >= self.get_finality_threshold()
    
    def get_validator_info(self, validator_id: str) -> Optional[Dict]:
        """
        Get information about a validator.
        
        Args:
            validator_id: The validator's ID
            
        Returns:
            Dictionary with validator info, or None if not found
        """
        if validator_id not in self.validators:
            return None
        
        v = self.validators[validator_id]
        return {
            "validator_id": v.validator_id,
            "stake": v.stake,
            "active": v.active,
            "blocks_proposed": v.blocks_proposed,
            "blocks_finalized": v.blocks_finalized,
            "slashing_count": v.slashing_count,
            "performance_score": v.get_performance_score()
        }
    
    def get_network_stats(self) -> Dict:
        """Get statistics about the validator network."""
        active_validators = [v for v in self.validators.values() if v.active]
        
        return {
            "total_validators": len(self.validators),
            "active_validators": len(active_validators),
            "total_stake": self.total_stake,
            "average_stake": self.total_stake / len(self.validators) if self.validators else 0,
            "current_epoch": self.current_epoch,
            "finality_threshold": self.get_finality_threshold()
        }


if __name__ == "__main__":
    # Demonstrate validator management
    genesis_params = GenesisParameters()
    validator_set = ValidatorSet(genesis_params)
    
    # Register validators with Fibonacci stakes
    stakes = [FibonacciUtils.fibonacci(i) for i in range(20, 26)]
    for i, stake in enumerate(stakes):
        validator_set.register_validator(f"validator_{i}", stake)
    
    print("Validator Network Stats:")
    print(validator_set.get_network_stats())
    
    print("\nProposer Selection:")
    for _ in range(5):
        proposer = validator_set.select_proposer()
        print(f"Selected proposer: {proposer}")
