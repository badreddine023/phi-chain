"""
tests/test_optimizations.py: Test suite for Φ-Chain code optimizations

Tests validate that optimized implementations:
1. Maintain functional correctness
2. Improve performance
3. Handle edge cases properly
4. Preserve Mathematical Purity
"""

import sys
import time
import unittest
from typing import List, Dict, Any

sys.path.insert(0, '..')

# Import optimized modules
from crypto.hash_optimized import PhiHashOptimized, FibonacciCache, MerkleTreeOptimized
from core.blockchain_optimized import BlockchainOptimized


class TestFibonacciCache(unittest.TestCase):
    """Test suite for FibonacciCache optimization."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Clear cache before each test
        FibonacciCache.fibonacci.cache_clear()
    
    def test_fibonacci_correctness(self):
        """Test that cached Fibonacci values are correct."""
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        for i, expected_value in enumerate(expected):
            self.assertEqual(FibonacciCache.fibonacci(i), expected_value)
    
    def test_fibonacci_caching(self):
        """Test that Fibonacci caching improves performance."""
        # First call - cache miss
        start = time.time()
        result1 = FibonacciCache.fibonacci(20)
        time1 = time.time() - start
        
        # Second call - cache hit
        start = time.time()
        result2 = FibonacciCache.fibonacci(20)
        time2 = time.time() - start
        
        # Results should be identical
        self.assertEqual(result1, result2)
        
        # Cached call should be faster
        self.assertLess(time2, time1)
    
    def test_fibonacci_precompute(self):
        """Test that precompute populates cache correctly."""
        FibonacciCache.precompute(10)
        cache_info = FibonacciCache.get_cache_info()
        
        # Should have at least 11 cached values (0-10)
        self.assertGreaterEqual(cache_info['currsize'], 11)
    
    def test_fibonacci_large_values(self):
        """Test Fibonacci computation for larger indices."""
        # Test F_50
        result = FibonacciCache.fibonacci(50)
        self.assertEqual(result, 12586269025)


class TestPhiHashOptimized(unittest.TestCase):
    """Test suite for PhiHashOptimized."""
    
    def setUp(self):
        """Set up test fixtures."""
        PhiHashOptimized.clear_cache()
    
    def test_sha256_string_input(self):
        """Test SHA-256 with string input."""
        data = "Hello, Φ-Chain!"
        result = PhiHashOptimized.sha256(data)
        
        # Should return 64-character hex string
        self.assertEqual(len(result), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in result))
    
    def test_sha256_bytes_input(self):
        """Test SHA-256 with bytes input."""
        data = b"Hello, Φ-Chain!"
        result = PhiHashOptimized.sha256(data)
        
        # Should return 64-character hex string
        self.assertEqual(len(result), 64)
    
    def test_sha256_caching(self):
        """Test that SHA-256 results are cached."""
        data = "test_data"
        
        # First call
        result1 = PhiHashOptimized.sha256(data)
        cache_info1 = PhiHashOptimized.get_cache_stats()
        
        # Second call (should hit cache)
        result2 = PhiHashOptimized.sha256(data)
        cache_info2 = PhiHashOptimized.get_cache_stats()
        
        # Results should be identical
        self.assertEqual(result1, result2)
        
        # Cache hits should increase
        self.assertGreater(cache_info2['hits'], cache_info1['hits'])
    
    def test_fibonacci_hash(self):
        """Test Fibonacci-based hashing."""
        data = "test_data"
        result = PhiHashOptimized.fibonacci_hash(data, fib_index=10)
        
        # Should return 64-character hex string
        self.assertEqual(len(result), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in result))
    
    def test_hmac_sha256(self):
        """Test HMAC-SHA256 computation."""
        data = "test_data"
        key = "secret_key"
        result = PhiHashOptimized.hmac_sha256(data, key)
        
        # Should return 64-character hex string
        self.assertEqual(len(result), 64)
    
    def test_hmac_verification(self):
        """Test HMAC signature verification."""
        data = "test_data"
        key = "secret_key"
        
        # Generate signature
        signature = PhiHashOptimized.hmac_sha256(data, key)
        
        # Verify correct signature
        self.assertTrue(PhiHashOptimized.verify_hmac(data, key, signature))
        
        # Verify incorrect signature fails
        bad_signature = "0" * 64
        self.assertFalse(PhiHashOptimized.verify_hmac(data, key, bad_signature))


class TestMerkleTreeOptimized(unittest.TestCase):
    """Test suite for MerkleTreeOptimized."""
    
    def test_merkle_tree_creation(self):
        """Test Merkle tree creation."""
        data = ["tx1", "tx2", "tx3", "tx4"]
        tree = MerkleTreeOptimized(data)
        
        # Should have a root
        self.assertIsNotNone(tree.get_root())
        
        # Root should be 64-character hex string
        root = tree.get_root()
        self.assertEqual(len(root), 64)
    
    def test_merkle_proof_generation(self):
        """Test Merkle proof generation."""
        data = ["tx1", "tx2", "tx3", "tx4"]
        tree = MerkleTreeOptimized(data)
        
        # Get proof for first item
        proof = tree.get_proof(0)
        
        # Proof should not be empty
        self.assertGreater(len(proof), 0)
        
        # All proof elements should be valid hashes
        for hash_elem in proof:
            self.assertEqual(len(hash_elem), 64)
    
    def test_merkle_proof_verification(self):
        """Test Merkle proof verification."""
        data = ["tx1", "tx2", "tx3", "tx4"]
        tree = MerkleTreeOptimized(data)
        
        # Get proof for first item
        proof = tree.get_proof(0)
        root = tree.get_root()
        
        # Verify correct proof
        self.assertTrue(MerkleTreeOptimized.verify_proof("tx1", 0, proof, root))
        
        # Verify incorrect data fails
        self.assertFalse(MerkleTreeOptimized.verify_proof("tx_wrong", 0, proof, root))
    
    def test_merkle_tree_odd_items(self):
        """Test Merkle tree with odd number of items."""
        data = ["tx1", "tx2", "tx3"]
        tree = MerkleTreeOptimized(data)
        
        # Should still have a valid root
        self.assertIsNotNone(tree.get_root())
        
        # Should be able to verify proofs
        proof = tree.get_proof(0)
        root = tree.get_root()
        self.assertTrue(MerkleTreeOptimized.verify_proof("tx1", 0, proof, root))


class TestBlockchainOptimized(unittest.TestCase):
    """Test suite for BlockchainOptimized."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.blockchain = BlockchainOptimized()
    
    def test_blockchain_initialization(self):
        """Test blockchain initialization."""
        # Should have genesis block
        self.assertEqual(self.blockchain.get_chain_length(), 1)
        
        # Chain should be valid
        self.assertTrue(self.blockchain.is_chain_valid())
    
    def test_transaction_validation(self):
        """Test optimized transaction validation."""
        # Valid transaction
        valid_tx = {
            "from": "alice",
            "to": "bob",
            "amount": 10.0,
            "timestamp": 1234567890
        }
        self.assertTrue(self.blockchain.is_valid_transaction(valid_tx))
        
        # Invalid transaction - missing field
        invalid_tx = {
            "from": "alice",
            "to": "bob",
            "amount": 10.0
        }
        self.assertFalse(self.blockchain.is_valid_transaction(invalid_tx))
        
        # Invalid transaction - negative amount
        invalid_tx2 = {
            "from": "alice",
            "to": "bob",
            "amount": -10.0,
            "timestamp": 1234567890
        }
        self.assertFalse(self.blockchain.is_valid_transaction(invalid_tx2))
    
    def test_balance_caching(self):
        """Test balance caching optimization."""
        # Add transactions
        tx1 = {
            "from": "alice",
            "to": "bob",
            "amount": 10.0,
            "timestamp": 1234567890
        }
        self.blockchain.add_transaction(tx1)
        
        # Get balance (first call - not cached)
        balance1 = self.blockchain.get_balance("alice")
        self.assertEqual(balance1, -10.0)
        
        # Get balance again (should be cached)
        balance2 = self.blockchain.get_balance("alice")
        self.assertEqual(balance2, -10.0)
        
        # Cache should be valid
        self.assertTrue(self.blockchain._cache_valid)
    
    def test_chain_validation_incremental(self):
        """Test incremental chain validation optimization."""
        # Initial validation
        self.assertTrue(self.blockchain.is_chain_valid())
        
        # Add transaction
        tx = {
            "from": "alice",
            "to": "bob",
            "amount": 10.0,
            "timestamp": 1234567890
        }
        self.blockchain.add_transaction(tx)
        
        # Chain should still be valid
        self.assertTrue(self.blockchain.is_chain_valid())
    
    def test_cache_statistics(self):
        """Test cache statistics reporting."""
        stats = self.blockchain.get_cache_stats()
        
        # Should have cache statistics
        self.assertIn('cached_addresses', stats)
        self.assertIn('cache_valid', stats)
        self.assertIn('last_validated_index', stats)
        self.assertIn('total_blocks', stats)
        self.assertIn('validated_blocks', stats)
    
    def test_clear_cache(self):
        """Test cache clearing."""
        # Add transaction and get balance
        tx = {
            "from": "alice",
            "to": "bob",
            "amount": 10.0,
            "timestamp": 1234567890
        }
        self.blockchain.add_transaction(tx)
        self.blockchain.get_balance("alice")
        
        # Cache should have entries
        self.assertGreater(len(self.blockchain._balance_cache), 0)
        
        # Clear cache
        self.blockchain.clear_balance_cache()
        
        # Cache should be empty
        self.assertEqual(len(self.blockchain._balance_cache), 0)
        self.assertFalse(self.blockchain._cache_valid)


class TestPerformanceBenchmarks(unittest.TestCase):
    """Performance benchmark tests."""
    
    def test_fibonacci_performance(self):
        """Benchmark Fibonacci caching performance."""
        # Clear cache
        FibonacciCache.fibonacci.cache_clear()
        
        # First call (cache miss)
        start = time.time()
        for i in range(50):
            FibonacciCache.fibonacci(i)
        time_first = time.time() - start
        
        # Second iteration (cache hits)
        start = time.time()
        for i in range(50):
            FibonacciCache.fibonacci(i)
        time_second = time.time() - start
        
        # Second iteration should be significantly faster
        speedup = time_first / time_second if time_second > 0 else float('inf')
        print(f"\nFibonacci Caching Speedup: {speedup:.1f}x")
        self.assertGreater(speedup, 1.5)
    
    def test_hash_caching_performance(self):
        """Benchmark hash result caching performance."""
        PhiHashOptimized.clear_cache()
        
        data = "test_data_for_hashing"
        
        # First call (cache miss)
        start = time.time()
        for _ in range(1000):
            PhiHashOptimized.sha256(data)
        time_first = time.time() - start
        
        # Second iteration (cache hits)
        start = time.time()
        for _ in range(1000):
            PhiHashOptimized.sha256(data)
        time_second = time.time() - start
        
        # Second iteration should be significantly faster
        speedup = time_first / time_second if time_second > 0 else float('inf')
        print(f"Hash Caching Speedup: {speedup:.1f}x")
        self.assertGreater(speedup, 10.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
