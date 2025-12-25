"""
test_phi_chain.py - Unit tests for Phi Chain core components.
"""

import unittest
from typing import Dict, List, Tuple
from phi_chain_core import PhiTransaction, PipelinedBFTMessage
from opevm_executor import OPEVMExecutor

class TestOPEVMExecutor(unittest.TestCase):
    """
    Tests the Optimistic Parallelized EVM (OPEVM) Executor logic.
    """
    
    def setUp(self):
        # Initial State for all tests
        self.initial_state: Dict[str, int] = {
            "0xAlice_balance": 1000,
            "0xBob_balance": 500,
            "0xContract_A_data": 10,
            "0xContract_B_data": 20,
        }
        self.executor = OPEVMExecutor(self.initial_state.copy())

    def _create_tx(self, sender: str, recipient: str, value: int, nonce: int, read_set: List[str], write_set: List[str]) -> PhiTransaction:
        """Helper to create a PhiTransaction."""
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

    def test_non_conflicting_transactions(self):
        """Test case where all transactions can be executed in parallel."""
        tx_alice_bob = self._create_tx("0xAlice", "0xBob", 100, 1, 
                                       ["0xAlice_balance", "0xBob_balance"], 
                                       ["0xAlice_balance", "0xBob_balance"])
        
        tx_contract_b = self._create_tx("0xUser", "0xContractB", 0, 1, 
                                        ["0xContract_B_data"], 
                                        ["0xContract_B_data"])
        
        transactions = [tx_alice_bob, tx_contract_b]
        final_state, re_executed = self.executor.execute_block(transactions)
        
        # Assert no re-execution occurred
        self.assertEqual(re_executed, [])
        
        # Assert final state is correct
        self.assertEqual(final_state["0xAlice_balance"], 900) # 1000 - 100
        self.assertEqual(final_state["0xBob_balance"], 600)   # 500 + 100
        # Contract B data is unchanged in this simple simulation, but the write set was committed
        self.assertEqual(final_state["0xContract_B_data"], 20) 

    def test_conflicting_transactions(self):
        """Test case where a conflict forces sequential re-execution."""
        # Tx 0: Alice -> Bob (Writes to Alice's balance)
        tx0 = self._create_tx("0xAlice", "0xBob", 100, 1, 
                             ["0xAlice_balance", "0xBob_balance"], 
                             ["0xAlice_balance", "0xBob_balance"])
        
        # Tx 1: Alice -> Charlie (Also writes to Alice's balance, must conflict with Tx 0)
        tx1 = self._create_tx("0xAlice", "0xCharlie", 50, 2, 
                             ["0xAlice_balance"], 
                             ["0xAlice_balance"])
        
        transactions = [tx0, tx1]
        final_state, re_executed = self.executor.execute_block(transactions)
        
        # Assert Tx 1 was flagged for re-execution
        self.assertEqual(re_executed, [1])
        
        # Assert final state is correct (Sequential execution: Tx 0 then Tx 1)
        # Tx 0: Alice: 1000 -> 900
        # Tx 1: Alice: 900 -> 850 (The re-execution uses the state after Tx 0)
        self.assertEqual(final_state["0xAlice_balance"], 850)
        self.assertEqual(final_state["0xBob_balance"], 600)
        # Note: The simulation for Tx 1 does not update Charlie's balance, but the logic is sound.

class TestPipelinedBFTMessage(unittest.TestCase):
    """
    Tests the Pipelined BFT supermajority logic.
    """
    
    def test_supermajority_reached(self):
        """Test case where 2/3+ supermajority is reached."""
        total_validators = 10
        # 7 is the minimum for 2/3+ of 10 (2/3 * 10 = 6.66, so 7 is required)
        messages = [
            PipelinedBFTMessage("PREVOTE", "hash", 0, f"Validator_{i}", b"sig")
            for i in range(7)
        ]
        
        # Use the method on a sample message
        self.assertTrue(messages[0].is_supermajority(messages, total_validators))

    def test_supermajority_not_reached(self):
        """Test case where 2/3+ supermajority is not reached."""
        total_validators = 10
        # 6 is not enough
        messages = [
            PipelinedBFTMessage("PREVOTE", "hash", 0, f"Validator_{i}", b"sig")
            for i in range(6)
        ]
        
        # Use the method on a sample message
        self.assertFalse(messages[0].is_supermajority(messages, total_validators))

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
