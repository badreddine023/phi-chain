"""
crypto/hash.py: Cryptographic hashing utilities for Φ-Chain

This module provides secure hashing functions based on SHA-256 and
Fibonacci-derived parameters.
"""

import hashlib
import hmac
from typing import Union
import sys
sys.path.insert(0, '..')
from phi_chain_core import FibonacciUtils


class PhiHash:
    """
    Φ-Chain cryptographic hashing utilities.
    
    Provides SHA-256 hashing with Fibonacci-based salt and
    HMAC authentication.
    """
    
    @staticmethod
    def sha256(data: Union[str, bytes]) -> str:
        """
        Compute SHA-256 hash of data.
        
        Args:
            data: The data to hash (string or bytes)
            
        Returns:
            Hexadecimal hash string
        """
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def fibonacci_hash(data: Union[str, bytes], fib_index: int = 10) -> str:
        """
        Compute hash with Fibonacci-derived salt.
        
        Args:
            data: The data to hash
            fib_index: The Fibonacci index for salt generation
            
        Returns:
            Hexadecimal hash string
        """
        if isinstance(data, str):
            data = data.encode()
        
        # Generate Fibonacci-based salt
        salt = str(FibonacciUtils.fibonacci(fib_index)).encode()
        
        # Combine data with salt
        combined = data + salt
        return hashlib.sha256(combined).hexdigest()
    
    @staticmethod
    def hmac_sha256(data: Union[str, bytes], key: Union[str, bytes]) -> str:
        """
        Compute HMAC-SHA256 for message authentication.
        
        Args:
            data: The data to authenticate
            key: The secret key
            
        Returns:
            Hexadecimal HMAC string
        """
        if isinstance(data, str):
            data = data.encode()
        if isinstance(key, str):
            key = key.encode()
        
        return hmac.new(key, data, hashlib.sha256).hexdigest()
    
    @staticmethod
    def verify_hmac(data: Union[str, bytes], key: Union[str, bytes], signature: str) -> bool:
        """
        Verify an HMAC signature.
        
        Args:
            data: The original data
            key: The secret key
            signature: The signature to verify
            
        Returns:
            True if the signature is valid
        """
        computed = PhiHash.hmac_sha256(data, key)
        return hmac.compare_digest(computed, signature)


class MerkleTree:
    """
    Merkle Tree implementation for efficient data verification.
    
    Used for transaction verification and efficient state proofs.
    """
    
    def __init__(self, data_list: list):
        """
        Initialize a Merkle Tree.
        
        Args:
            data_list: List of data items to include in the tree
        """
        self.data_list = data_list
        self.tree = []
        self.root = None
        self.build_tree()
    
    def build_tree(self):
        """Build the Merkle tree from the data list."""
        if not self.data_list:
            return
        
        # Hash all leaf nodes
        current_level = [PhiHash.sha256(str(item)) for item in self.data_list]
        self.tree.append(current_level)
        
        # Build tree bottom-up
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                if i + 1 < len(current_level):
                    combined = current_level[i] + current_level[i + 1]
                else:
                    combined = current_level[i] + current_level[i]
                
                next_level.append(PhiHash.sha256(combined))
            
            self.tree.append(next_level)
            current_level = next_level
        
        # The root is the last item
        self.root = current_level[0] if current_level else None
    
    def get_root(self) -> str:
        """Get the Merkle root hash."""
        return self.root
    
    def get_proof(self, index: int) -> list:
        """
        Get the Merkle proof for an item at a given index.
        
        Args:
            index: The index of the item
            
        Returns:
            List of hashes forming the proof path
        """
        if index >= len(self.data_list):
            return []
        
        proof = []
        current_index = index
        
        for level in self.tree[:-1]:
            if current_index % 2 == 0:
                if current_index + 1 < len(level):
                    proof.append(level[current_index + 1])
            else:
                proof.append(level[current_index - 1])
            
            current_index //= 2
        
        return proof
    
    @staticmethod
    def verify_proof(data: str, index: int, proof: list, root: str) -> bool:
        """
        Verify a Merkle proof.
        
        Args:
            data: The data item
            index: The original index
            proof: The Merkle proof
            root: The expected root hash
            
        Returns:
            True if the proof is valid
        """
        current_hash = PhiHash.sha256(data)
        current_index = index
        
        for proof_hash in proof:
            if current_index % 2 == 0:
                combined = current_hash + proof_hash
            else:
                combined = proof_hash + current_hash
            
            current_hash = PhiHash.sha256(combined)
            current_index //= 2
        
        return current_hash == root


if __name__ == "__main__":
    # Demonstrate hashing
    data = "Hello, Φ-Chain!"
    print(f"SHA-256: {PhiHash.sha256(data)}")
    print(f"Fibonacci Hash: {PhiHash.fibonacci_hash(data)}")
    
    # Demonstrate HMAC
    key = "secret_key"
    signature = PhiHash.hmac_sha256(data, key)
    print(f"HMAC-SHA256: {signature}")
    print(f"Verification: {PhiHash.verify_hmac(data, key, signature)}")
    
    # Demonstrate Merkle Tree
    transactions = ["tx1", "tx2", "tx3", "tx4"]
    merkle = MerkleTree(transactions)
    print(f"\nMerkle Root: {merkle.get_root()}")
