import time
import sys
import os

# Add the directory to path so we can import phi_chain
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from phi_chain import Blockchain, PhiTransaction, FibonacciUtils

def test_fibonacci_cache():
    print("\n--- Testing Fibonacci Cache ---")
    start_time = time.time()
    # First call (calculates and caches)
    f30 = FibonacciUtils.fibonacci(30)
    mid_time = time.time()
    # Second call (should be instant from cache)
    f30_cached = FibonacciUtils.fibonacci(30)
    end_time = time.time()
    
    print(f"F_30 = {f30}")
    print(f"First call time: {mid_time - start_time:.6f}s")
    print(f"Cached call time: {end_time - mid_time:.6f}s")
    assert f30 == f30_cached

def test_balance_cache():
    print("\n--- Testing Balance Cache ---")
    bc = Blockchain()
    address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    
    # Initial balance (calculates and caches)
    start_time = time.time()
    bal1 = bc.get_balance(address)
    mid_time = time.time()
    # Second call (should be instant from cache)
    bal2 = bc.get_balance(address)
    end_time = time.time()
    
    print(f"Balance: {bal1}")
    print(f"First call time: {mid_time - start_time:.6f}s")
    print(f"Cached call time: {end_time - mid_time:.6f}s")
    assert bal1 == bal2

def test_chain_validation_cache():
    print("\n--- Testing Chain Validation Cache ---")
    bc = Blockchain()
    # Add some blocks
    for i in range(5):
        tx = PhiTransaction("0xAlice", "0xBob", 10, i)
        bc.add_transaction(tx)
        bc.mine_pending_transactions("0xMiner")
    
    # First validation (full)
    start_time = time.time()
    bc.is_chain_valid()
    mid_time = time.time()
    # Second validation (incremental - should be faster)
    bc.is_chain_valid()
    end_time = time.time()
    
    print(f"Chain length: {len(bc.chain)}")
    print(f"First validation time: {mid_time - start_time:.6f}s")
    print(f"Second validation time: {end_time - mid_time:.6f}s")

if __name__ == "__main__":
    test_fibonacci_cache()
    test_balance_cache()
    test_chain_validation_cache()
    print("\nAll performance tests passed!")
