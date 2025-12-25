import sys
import os
import unittest
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from phi_chain_core import FibonacciUtils, GenesisParameters, PhiState, PhiBlock, PhiTransaction

class TestPhiChainE2E(unittest.TestCase):
    def test_fibonacci_utils(self):
        self.assertEqual(FibonacciUtils.fibonacci(6), 8)
        self.assertEqual(FibonacciUtils.fibonacci(10), 55)
        self.assertTrue(FibonacciUtils.is_fibonacci(6765)) # F_20
        self.assertFalse(FibonacciUtils.is_fibonacci(10))

    def test_genesis_parameters(self):
        params = GenesisParameters()
        self.assertEqual(params.SLOT_DURATION, 8)
        self.assertEqual(params.MIN_VALIDATOR_STAKE, 6765)

    def test_state_evolution(self):
        state = PhiState(1, 1)
        state.evolve()
        self.assertEqual(state.get_current_metrics(), (2, 1))
        state.evolve()
        self.assertEqual(state.get_current_metrics(), (3, 2))

    def test_block_hashing(self):
        tx = PhiTransaction("sender", "recipient", 100)
        block = PhiBlock(1, "prev", time.time(), [tx], "root", "proposer", (1, 1))
        h1 = block.calculate_hash()
        h2 = block.calculate_hash()
        self.assertEqual(h1, h2)

if __name__ == "__main__":
    unittest.main()
