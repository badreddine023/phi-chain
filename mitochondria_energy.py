"""
Mitochondria: The Energy Battery System of Φ-Chain

This module implements a biological metaphor for energy management in the blockchain.
Mitochondria represents the "powerhouse" of the Φ-Chain, managing:

- Fibonacci-tiered energy levels
- Energy production and consumption
- Battery charging and discharging mechanics
- Metabolic efficiency optimization
- ATP-like energy currency (Φ-Energy)
"""

import numpy as np
from typing import Dict, List, Tuple
from phi_chain_core import FibonacciUtils, GenesisParameters


class MitochondrialCell:
    """
    A single mitochondrial cell, representing a unit of energy production.
    
    Each cell maintains energy state based on Fibonacci cycles, creating
    natural rhythms of energy production and consumption.
    """
    
    def __init__(self, cell_id: int, tier: int):
        """
        Initialize a mitochondrial cell.
        
        Args:
            cell_id: Unique identifier for the cell
            tier: The energy tier (1-6, based on Fibonacci)
        """
        self.cell_id = cell_id
        self.tier = tier
        
        # Energy capacity based on Fibonacci
        self.max_energy = FibonacciUtils.fibonacci(tier + 10)  # F_11 to F_16
        self.current_energy = self.max_energy * 0.5  # Start at 50%
        
        # Metabolic rate (energy production per cycle)
        self.production_rate = FibonacciUtils.fibonacci(tier + 5) / 100.0
        
        # Efficiency factor based on golden ratio
        self.efficiency = 1.0 / FibonacciUtils.golden_ratio()
    
    def produce_energy(self) -> float:
        """
        Produce energy in this cycle.
        
        Returns:
            Amount of energy produced
        """
        produced = self.production_rate * self.efficiency
        self.current_energy = min(self.current_energy + produced, self.max_energy)
        return produced
    
    def consume_energy(self, amount: float) -> bool:
        """
        Consume energy from this cell.
        
        Args:
            amount: Amount of energy to consume
            
        Returns:
            True if energy was available, False otherwise
        """
        if self.current_energy >= amount:
            self.current_energy -= amount
            return True
        return False
    
    def get_charge_level(self) -> float:
        """Get the current charge level as a percentage (0-1)."""
        return self.current_energy / self.max_energy


class MitochondrialOrgan:
    """
    A collection of mitochondrial cells forming an energy-producing organ.
    
    Multiple cells work in concert to provide robust energy production
    with redundancy and efficiency.
    """
    
    def __init__(self, organ_id: int, cell_count: int = 144):
        """
        Initialize a mitochondrial organ.
        
        Args:
            organ_id: Unique identifier for the organ
            cell_count: Number of cells (default F_12 = 144)
        """
        self.organ_id = organ_id
        self.cells = []
        
        # Create cells with varying tiers for diversity
        for i in range(cell_count):
            tier = (i % 6) + 1  # Tiers 1-6
            self.cells.append(MitochondrialCell(i, tier))
        
        # Organ-level parameters
        self.total_cycles = 0
        self.energy_history = []
    
    def cycle(self) -> float:
        """
        Execute one energy production cycle.
        
        Returns:
            Total energy produced in this cycle
        """
        total_produced = 0.0
        for cell in self.cells:
            total_produced += cell.produce_energy()
        
        self.total_cycles += 1
        self.energy_history.append(total_produced)
        
        # Keep history bounded
        if len(self.energy_history) > FibonacciUtils.fibonacci(13):
            self.energy_history.pop(0)
        
        return total_produced
    
    def get_total_energy(self) -> float:
        """Get total energy stored across all cells."""
        return sum(cell.current_energy for cell in self.cells)
    
    def get_total_capacity(self) -> float:
        """Get total energy capacity across all cells."""
        return sum(cell.max_energy for cell in self.cells)
    
    def get_charge_level(self) -> float:
        """Get overall charge level as a percentage (0-1)."""
        total = self.get_total_energy()
        capacity = self.get_total_capacity()
        return total / capacity if capacity > 0 else 0.0
    
    def distribute_energy(self, amount: float) -> float:
        """
        Distribute energy to consumers.
        
        Args:
            amount: Amount of energy requested
            
        Returns:
            Amount of energy actually provided
        """
        remaining = amount
        for cell in self.cells:
            if remaining <= 0:
                break
            
            available = min(cell.current_energy, remaining)
            if cell.consume_energy(available):
                remaining -= available
        
        return amount - remaining


class MitochondriaEnergySystem:
    """
    The complete Mitochondria energy system for Φ-Chain.
    
    This system manages energy production, storage, and distribution
    across the entire blockchain network.
    """
    
    def __init__(self, genesis_params: GenesisParameters = None):
        """
        Initialize the Mitochondria energy system.
        
        Args:
            genesis_params: The Φ-Chain genesis parameters
        """
        self.genesis_params = genesis_params or GenesisParameters()
        
        # Create mitochondrial organs
        self.organs = []
        for organ_id in range(1, 6):  # 5 organs (F_5 = 5)
            self.organs.append(MitochondrialOrgan(organ_id))
        
        # Energy tiers based on Fibonacci
        self.energy_tiers = {
            "tier_1": FibonacciUtils.fibonacci(8),   # F_8 = 21
            "tier_2": FibonacciUtils.fibonacci(10),  # F_10 = 55
            "tier_3": FibonacciUtils.fibonacci(12),  # F_12 = 144
            "tier_4": FibonacciUtils.fibonacci(14),  # F_14 = 377
            "tier_5": FibonacciUtils.fibonacci(16),  # F_16 = 987
            "tier_6": FibonacciUtils.fibonacci(18),  # F_18 = 2584
        }
        
        # Global energy tracking
        self.total_produced = 0.0
        self.total_consumed = 0.0
        self.cycle_count = 0
    
    def metabolic_cycle(self) -> Dict:
        """
        Execute one metabolic cycle across all organs.
        
        Returns:
            Dictionary with cycle statistics
        """
        cycle_data = {
            "cycle": self.cycle_count,
            "organs_produced": [],
            "total_produced": 0.0,
            "system_charge": self.get_system_charge()
        }
        
        for organ in self.organs:
            produced = organ.cycle()
            cycle_data["organs_produced"].append(produced)
            cycle_data["total_produced"] += produced
            self.total_produced += produced
        
        self.cycle_count += 1
        return cycle_data
    
    def get_system_charge(self) -> float:
        """Get overall system charge level (0-1)."""
        total_energy = sum(organ.get_total_energy() for organ in self.organs)
        total_capacity = sum(organ.get_total_capacity() for organ in self.organs)
        return total_energy / total_capacity if total_capacity > 0 else 0.0
    
    def allocate_energy_to_validator(self, validator_id: str, tier: str) -> float:
        """
        Allocate energy to a validator based on their tier.
        
        Args:
            validator_id: The validator's identifier
            tier: The energy tier ("tier_1" to "tier_6")
            
        Returns:
            Amount of energy allocated
        """
        if tier not in self.energy_tiers:
            return 0.0
        
        requested_energy = self.energy_tiers[tier]
        
        # Try to allocate from organs in round-robin fashion
        allocated = 0.0
        for organ in self.organs:
            if allocated >= requested_energy:
                break
            
            remaining = requested_energy - allocated
            provided = organ.distribute_energy(remaining)
            allocated += provided
        
        self.total_consumed += allocated
        return allocated
    
    def get_energy_efficiency(self) -> float:
        """
        Calculate the overall energy efficiency of the system.
        
        Returns:
            Efficiency ratio (produced / consumed)
        """
        if self.total_consumed == 0:
            return 1.0
        return self.total_produced / self.total_consumed
    
    def demonstrate_energy_system(self):
        """Display the Mitochondria energy system's capabilities."""
        print("\n" + "=" * 70)
        print("MITOCHONDRIA: ENERGY BATTERY SYSTEM OF Φ-CHAIN")
        print("=" * 70)
        
        print("\n1. SYSTEM ARCHITECTURE:")
        print(f"   Organs: {len(self.organs)}")
        total_cells = sum(len(organ.cells) for organ in self.organs)
        print(f"   Total cells: {total_cells}")
        
        print(f"\n2. ENERGY TIERS (Fibonacci-based):")
        for tier_name, energy in self.energy_tiers.items():
            print(f"   {tier_name}: {energy} Φ-Energy")
        
        print(f"\n3. METABOLIC CYCLES:")
        for cycle in range(8):  # F_6 = 8 cycles
            cycle_data = self.metabolic_cycle()
            print(f"   Cycle {cycle}: {cycle_data['total_produced']:.2f} Φ-Energy produced, " +
                  f"System charge: {cycle_data['system_charge']:.2%}")
        
        print(f"\n4. ENERGY ALLOCATION:")
        validators = ["validator_1", "validator_2", "validator_3"]
        tiers = ["tier_1", "tier_2", "tier_3"]
        for validator, tier in zip(validators, tiers):
            allocated = self.allocate_energy_to_validator(validator, tier)
            print(f"   {validator} ({tier}): {allocated:.2f} Φ-Energy allocated")
        
        print(f"\n5. SYSTEM STATISTICS:")
        print(f"   Total produced: {self.total_produced:.2f} Φ-Energy")
        print(f"   Total consumed: {self.total_consumed:.2f} Φ-Energy")
        print(f"   Efficiency: {self.get_energy_efficiency():.4f}")
        print(f"   Current charge: {self.get_system_charge():.2%}")
        
        print("\n" + "=" * 70)
        print("✅ MITOCHONDRIA ENERGY SYSTEM OPERATIONAL")
        print("=" * 70)


if __name__ == "__main__":
    mitochondria = MitochondriaEnergySystem()
    mitochondria.demonstrate_energy_system()
