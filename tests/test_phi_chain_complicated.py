"""
test_phi_chain_complicated.py - Advanced stress tests for Phi Chain.
This script tests complex transaction dependencies, high-concurrency conflicts,
and Fibonacci-based consensus edge cases.
"""

import unittest
import time
import random
from typing import Dict, List, Set
from phi_chain_core import PhiTransaction, PipelinedBFTMessage, PhiState, FibonacciUtils
from opevm_executor import OPEVMExecutor

class TestComplicatedOPEVM(unittest.TestCase):
    def setUp(self):
        # Initialize a large state
        self.initial_state = {f"0xAccount_{i}": 10000 for i in range(100)}
        self.executor = OPEVMExecutor(self.initial_state.copy())

    def _create_tx(self, sender: str, recipient: str, value: int, nonce: int, read_set: List[str], write_set: List[str]) -> PhiTransaction:
        return PhiTransaction(
            sender=sender,
            recipient=recipient,
            value=value,
            data=b"",
            nonce=nonce,
            gas_limit=21000,
            signature=b"sig",
            estimated_read_set=read_set,
            estimated_write_set=write_set
        )

    def test_circular_dependency_chain(self):
        """
        Tests a chain of transactions where each depends on the previous one.
        Tx0: A -> B
        Tx1: B -> C
        Tx2: C -> D
        ...
        In the current OPEVM simulation:
        - Tx0: Executes and commits (Writes to A, B)
        - Tx1: Conflicts with Tx0 (Reads B), flagged for re-execution.
        - Tx2: Executes against initial state. Since Tx1 was NOT committed, Tx2 does NOT conflict with Tx1 yet.
        - Tx3: Conflicts with Tx2 (Reads D), flagged for re-execution.
        ...
        This results in [1, 3, 5, 7, 9] being re-executed.
        """
        txs = []
        for i in range(10):
            sender = f"0xAccount_{i}"
            recipient = f"0xAccount_{i+1}"
            txs.append(self._create_tx(
                sender, recipient, 10, i,
                [f"{sender}_balance", f"{recipient}_balance"],
                [f"{sender}_balance", f"{recipient}_balance"]
            ))
        
        final_state, re_executed = self.executor.execute_block(txs)
        
        # In this simulation, every other transaction conflicts because the previous one was not committed.
        self.assertEqual(re_executed, [1, 3, 5, 7, 9])
        self.assertEqual(final_state["0xAccount_0_balance"], 9990)
        self.assertEqual(final_state["0xAccount_10_balance"], 10010)

    def test_high_concurrency_hotspot(self):
        """
        Tests many transactions hitting the same 'hot' account.
        All Tx: Account_X -> HotAccount
        """
        hot_account = "0xHotAccount"
        self.executor.state[f"{hot_account}_balance"] = 0
        txs = []
        for i in range(20):
            sender = f"0xAccount_{i}"
            txs.append(self._create_tx(
                sender, hot_account, 1, i,
                [f"{sender}_balance", f"{hot_account}_balance"],
                [f"{sender}_balance", f"{hot_account}_balance"]
            ))
            
        final_state, re_executed = self.executor.execute_block(txs)
        
        # Only the first transaction should succeed optimistically.
        # All others conflict on the hot_account balance.
        self.assertEqual(len(re_executed), 19)
        self.assertEqual(final_state[f"{hot_account}_balance"], 20)

    def test_complex_read_only_concurrency(self):
        """
        Tests that read-only transactions do not conflict with each other,
        but do conflict with writers.
        """
        # Tx0: Writer to A
        tx0 = self._create_tx("0xWriter", "0xAccount_A", 100, 1, ["0xAccount_A_balance"], ["0xAccount_A_balance"])
        # Tx1-5: Readers of A
        readers = [self._create_tx(f"0xReader_{i}", "0xSomewhere", 0, 1, ["0xAccount_A_balance"], []) for i in range(5)]
        
        txs = [tx0] + readers
        final_state, re_executed = self.executor.execute_block(txs)
        
        # Readers 1-5 should all conflict with Tx0's write.
        self.assertEqual(re_executed, [1, 2, 3, 4, 5])

class TestComplicatedConsensus(unittest.TestCase):
    def test_fibonacci_state_evolution_stress(self):
        """Stress test the Q-Matrix evolution over many steps."""
        state = PhiState(1, 1) # F2, F1
        for i in range(20):
            state.evolve()
        
        f_n_plus_1, f_n = state.get_current_metrics()
        # After 20 evolutions from F2, F1:
        # Step 1: F3, F2
        # ...
        # Step 20: F22, F21
        self.assertEqual(f_n, FibonacciUtils.fibonacci(21))
        self.assertEqual(f_n_plus_1, FibonacciUtils.fibonacci(22))

    def test_bft_supermajority_edge_cases(self):
        """Test BFT thresholds for various network sizes."""
        test_cases = [
            (1, 1),   # 1 validator: 2/3 of 1 is 0.66, threshold 1
            (3, 3),   # 3 validators: 2/3 of 3 is 2, threshold 3
            (4, 3),   # 4 validators: 2/3 of 4 is 2.66, threshold 3
            (10, 7),  # 10 validators: 2/3 of 10 is 6.66, threshold 7
            (100, 67) # 100 validators: 2/3 of 100 is 66.66, threshold 67
        ]
        
        for total, required in test_cases:
            msg = PipelinedBFTMessage("PREVOTE", "hash", 0, "val", b"sig")
            # Create 'required' messages
            msgs = [PipelinedBFTMessage("PREVOTE", "hash", 0, f"val_{i}", b"sig") for i in range(required)]
            self.assertTrue(msg.is_supermajority(msgs, total), f"Failed for {total} validators")
            
            # Create 'required - 1' messages
            msgs_fail = [PipelinedBFTMessage("PREVOTE", "hash", 0, f"val_{i}", b"sig") for i in range(required - 1)]
            self.assertFalse(msg.is_supermajority(msgs_fail, total), f"Should fail for {total} validators with {required-1} votes")

if __name__ == "__main__":
    unittest.main()
