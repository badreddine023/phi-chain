"""
test_phi_chain.py - Φ-Chain Core Testing Suite

This module contains comprehensive tests for the Φ-Chain core engine.
"""

import unittest
import time
from phi_chain import (
    FibonacciUtils,
    GenesisParameters,
    PhiState,
    PhiTransaction,
    PhiBlock,
    Blockchain,
    ProofOfCoherence,
    FBAConsensus
)

class TestFibonacciUtils(unittest.TestCase):
    """Test Fibonacci and Golden Ratio utilities"""
    
    def test_fibonacci_positive(self):
        """Test Fibonacci sequence for positive indices"""
        self.assertEqual(FibonacciUtils.fibonacci(0), 0)
        self.assertEqual(FibonacciUtils.fibonacci(1), 1)
        self.assertEqual(FibonacciUtils.fibonacci(2), 1)
        self.assertEqual(FibonacciUtils.fibonacci(6), 8)
        self.assertEqual(FibonacciUtils.fibonacci(18), 2584)
        self.assertEqual(FibonacciUtils.fibonacci(20), 6765)
        self.assertEqual(FibonacciUtils.fibonacci(33), 3524578)
    
    def test_fibonacci_negative(self):
        """Test Fibonacci sequence for negative indices"""
        self.assertEqual(FibonacciUtils.fibonacci(-1), 1)
        self.assertEqual(FibonacciUtils.fibonacci(-2), -1)
        self.assertEqual(FibonacciUtils.fibonacci(-3), 2)
    
    def test_golden_ratio(self):
        """Test Golden Ratio calculation"""
        phi = FibonacciUtils.golden_ratio()
        self.assertAlmostEqual(float(phi), 1.618033988749895, places=10)
    
    def test_is_fibonacci(self):
        """Test Fibonacci number detection"""
        self.assertTrue(FibonacciUtils.is_fibonacci(0))
        self.assertTrue(FibonacciUtils.is_fibonacci(1))
        self.assertTrue(FibonacciUtils.is_fibonacci(8))
        self.assertTrue(FibonacciUtils.is_fibonacci(2584))
        self.assertFalse(FibonacciUtils.is_fibonacci(7))
        self.assertFalse(FibonacciUtils.is_fibonacci(-1))

class TestGenesisParameters(unittest.TestCase):
    """Test Genesis Parameters"""
    
    def setUp(self):
        self.params = GenesisParameters()
    
    def test_parameters(self):
        """Test all genesis parameters are correctly set"""
        self.assertEqual(self.params.SLOT_DURATION, 8)  # F_6
        self.assertEqual(self.params.EPOCH_DURATION, 2584)  # F_18
        self.assertEqual(self.params.MIN_VALIDATOR_STAKE, 6765)  # F_20
        self.assertEqual(self.params.MAX_VALIDATOR_COUNT, 1597)  # F_17
        self.assertEqual(self.params.TARGET_COMMITTEE_SIZE, 377)  # F_14
        self.assertEqual(self.params.FINALITY_THRESHOLD, 610)  # F_15
        self.assertEqual(self.params.GENESIS_SUPPLY, 3524578)  # F_33
        self.assertEqual(self.params.BLOCK_REWARD, 89)  # F_11
        self.assertEqual(self.params.TRANSACTION_FEE_BASE, 21)  # F_8
    
    def test_phi_value(self):
        """Test PHI value is correctly calculated"""
        self.assertAlmostEqual(self.params.PHI, 1.618033988749895, places=10)

class TestPhiState(unittest.TestCase):
    """Test Fibonacci Q-Matrix State Transitions"""
    
    def setUp(self):
        self.state = PhiState(1, 1)
    
    def test_initial_state(self):
        """Test initial state vector"""
        f1, f0 = self.state.get_current_metrics()
        self.assertEqual(f1, 1)
        self.assertEqual(f0, 1)
    
    def test_state_evolution(self):
        """Test state evolution through Q-Matrix"""
        # Initial: S_0 = [F_1, F_0] = [1, 1]
        f1, f0 = self.state.get_current_metrics()
        self.assertEqual(f1, 1)
        self.assertEqual(f0, 1)
        
        # Evolve to S_1 = [F_2, F_1] = [2, 1]
        self.state.evolve()
        f2, f1 = self.state.get_current_metrics()
        self.assertEqual(f2, 2)
        self.assertEqual(f1, 1)
        
        # Evolve to S_2 = [F_3, F_2] = [3, 2]
        self.state.evolve()
        f3, f2 = self.state.get_current_metrics()
        self.assertEqual(f3, 3)
        self.assertEqual(f2, 2)
    
    def test_state_hash(self):
        """Test state hash generation"""
        state_hash = self.state.get_state_hash()
        self.assertIsInstance(state_hash, str)
        self.assertEqual(len(state_hash), 64)  # SHA-256 hash

class TestPhiTransaction(unittest.TestCase):
    """Test Transaction Structure"""
    
    def setUp(self):
        self.tx = PhiTransaction(
            sender="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            recipient="0x0000000000000000000000000000000000000000",
            value=89,
            nonce=1
        )
    
    def test_transaction_creation(self):
        """Test transaction initialization"""
        self.assertEqual(self.tx.sender, "0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
        self.assertEqual(self.tx.recipient, "0x0000000000000000000000000000000000000000")
        self.assertEqual(self.tx.value, 89)
        self.assertEqual(self.tx.nonce, 1)
    
    def test_transaction_hash(self):
        """Test transaction hash calculation"""
        tx_hash = self.tx.calculate_hash()
        self.assertIsInstance(tx_hash, str)
        self.assertEqual(len(tx_hash), 64)
    
    def test_transaction_to_dict(self):
        """Test transaction serialization"""
        tx_dict = self.tx.to_dict()
        self.assertIn("sender", tx_dict)
        self.assertIn("recipient", tx_dict)
        self.assertIn("value", tx_dict)
        self.assertEqual(tx_dict["value"], 89)

class TestPhiBlock(unittest.TestCase):
    """Test Block Structure"""
    
    def setUp(self):
        self.block = PhiBlock(
            index=0,
            previous_hash="0" * 64,
            timestamp=time.time(),
            transactions=[
                PhiTransaction(
                    sender="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
                    recipient="0x0000000000000000000000000000000000000000",
                    value=89,
                    nonce=0
                )
            ],
            state_root="state_hash",
            proposer="0x0000000000000000000000000000000000000000",
            f_vector=(1, 1)
        )
    
    def test_block_creation(self):
        """Test block initialization"""
        self.assertEqual(self.block.index, 0)
        self.assertEqual(self.block.previous_hash, "0" * 64)
        self.assertEqual(len(self.block.transactions), 1)
        self.assertEqual(self.block.proposer, "0x0000000000000000000000000000000000000000")
    
    def test_block_hash(self):
        """Test block hash calculation"""
        block_hash = self.block.calculate_hash()
        self.assertIsInstance(block_hash, str)
        self.assertEqual(len(block_hash), 64)
    
    def test_block_mining(self):
        """Test Proof-of-Work mining"""
        # Test mining with difficulty 2
        self.block.mine(difficulty=2)
        self.assertEqual(self.block.hash[:2], "00")

class TestBlockchain(unittest.TestCase):
    """Test Blockchain Operations"""
    
    def setUp(self):
        self.blockchain = Blockchain()
    
    def test_genesis_block(self):
        """Test genesis block creation"""
        self.assertEqual(self.blockchain.get_chain_length(), 1)
        genesis = self.blockchain.get_latest_block()
        self.assertEqual(genesis.index, 0)
        self.assertEqual(genesis.previous_hash, "0" * 64)
    
    def test_add_transaction(self):
        """Test transaction addition"""
        tx = PhiTransaction(
            sender="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            recipient="0x0000000000000000000000000000000000000000",
            value=89,
            nonce=1
        )
        self.assertTrue(self.blockchain.add_transaction(tx))
        self.assertEqual(len(self.blockchain.pending_transactions), 1)
    
    def test_mine_block(self):
        """Test block mining"""
        # Add transaction
        tx = PhiTransaction(
            sender="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            recipient="0x0000000000000000000000000000000000000000",
            value=89,
            nonce=1
        )
        self.blockchain.add_transaction(tx)
        
        # Mine block
        block = self.blockchain.mine_pending_transactions("validator_001")
        self.assertIsNotNone(block)
        self.assertEqual(block.index, 1)
        self.assertEqual(len(self.blockchain.pending_transactions), 0)
    
    def test_balance_calculation(self):
        """Test balance calculation"""
        # Initial balance from genesis
        balance = self.blockchain.get_balance("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
        self.assertEqual(balance, 3524578)
        
        # Add transaction
        tx = PhiTransaction(
            sender="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            recipient="0x0000000000000000000000000000000000000000",
            value=89,
            nonce=1
        )
        self.blockchain.add_transaction(tx)
        
        # Mine block
        self.blockchain.mine_pending_transactions("validator_001")
        
        # Check updated balance
        balance = self.blockchain.get_balance("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
        self.assertEqual(balance, 3524578 - 89)
    
    def test_chain_validation(self):
        """Test chain validation"""
        self.assertTrue(self.blockchain.is_chain_valid())
        
        # Add transaction and mine block
        tx = PhiTransaction(
            sender="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            recipient="0x0000000000000000000000000000000000000000",
            value=89,
            nonce=1
        )
        self.blockchain.add_transaction(tx)
        self.blockchain.mine_pending_transactions("validator_001")
        
        self.assertTrue(self.blockchain.is_chain_valid())

class TestProofOfCoherence(unittest.TestCase):
    """Test Proof-of-Coherence Consensus"""
    
    def setUp(self):
        self.blockchain = Blockchain()
        self.poc = ProofOfCoherence(self.blockchain)
    
    def test_validator_addition(self):
        """Test validator addition"""
        # Add validator with Fibonacci stake
        self.assertTrue(self.blockchain.add_validator("validator_001", 6765))
        self.assertEqual(self.blockchain.get_validator_count(), 1)
        
        # Try to add validator with non-Fibonacci stake
        self.assertFalse(self.blockchain.add_validator("validator_002", 1000))
        self.assertEqual(self.blockchain.get_validator_count(), 1)
    
    def test_coherence_score(self):
        """Test coherence score calculation"""
        # Add validators
        self.blockchain.add_validator("validator_001", 6765)
        self.blockchain.add_validator("validator_002", 10946)
        
        # Calculate scores
        score1 = self.poc.calculate_coherence_score("validator_001")
        score2 = self.poc.calculate_coherence_score("validator_002")
        
        # Validator with higher stake should have higher score
        self.assertGreater(score2, score1)
    
    def test_proposer_selection(self):
        """Test proposer selection"""
        # Add validators with different stakes
        self.blockchain.add_validator("validator_001", 6765)
        self.blockchain.add_validator("validator_002", 10946)
        self.blockchain.add_validator("validator_003", 17711)
        
        # Select proposer
        proposer = self.poc.select_proposer()
        self.assertIn(proposer, ["validator_001", "validator_002", "validator_003"])

class TestFBAConsensus(unittest.TestCase):
    """Test Fibonacci Byzantine Agreement"""
    
    def setUp(self):
        self.blockchain = Blockchain()
        self.fba = FBAConsensus(self.blockchain)
    
    def test_supermajority_check(self):
        """Test supermajority threshold calculation"""
        # Add validators
        for i in range(10):
            self.blockchain.add_validator(f"validator_{i:03d}", 6765)
        
        # Test supermajority for 10 validators
        self.assertFalse(self.fba.check_supermajority(6))  # 6/10 < 7/10
        self.assertTrue(self.fba.check_supermajority(7))   # 7/10 >= 7/10
        
        # Test supermajority for 100 validators
        for i in range(10, 100):
            self.blockchain.add_validator(f"validator_{i:03d}", 6765)
        
        self.assertFalse(self.fba.check_supermajority(66))  # 66/100 < 67/100
        self.assertTrue(self.fba.check_supermajority(67))    # 67/100 >= 67/100
    
    def test_vote_processing(self):
        """Test vote processing"""
        # Add validator
        self.blockchain.add_validator("validator_001", 6765)
        
        # Process vote
        self.assertTrue(self.fba.process_vote("validator_001", "block_hash", "prepare"))
        
        # Check participation increased
        validator = self.blockchain.validators["validator_001"]
        self.assertEqual(validator["participation"], 1)

if __name__ == "__main__":
    print("=" * 60)
    print("Φ-CHAIN TESTING SUITE")
    print("=" * 60)
    
    # Run all tests
    unittest.main(verbosity=2)
