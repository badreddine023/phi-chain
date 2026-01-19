"""
core/blockchain.py: The main Blockchain class for Φ-Chain

This module implements the core blockchain logic, managing the chain of blocks,
validating transactions, and maintaining the ledger state.
"""

from typing import List, Dict, Any, Optional
from .block import Block, GenesisBlock
import sys
sys.path.insert(0, '..')
from phi_chain_core import FibonacciUtils


class Blockchain:
    """
    The Φ-Chain Blockchain - a distributed ledger based on the Golden Ratio.
    
    This class manages:
    - The chain of blocks
    - Block validation
    - Transaction processing
    - State management
    """
    
    def __init__(self):
        """Initialize the blockchain with the Genesis Block."""
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict[str, Any]] = []
        self.validators: Dict[str, int] = {}
        
        # Create and add the Genesis Block
        genesis_block = GenesisBlock()
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain."""
        return self.chain[-1]
    
    def add_block(self, new_block: Block) -> bool:
        """
        Add a new block to the blockchain.
        
        Args:
            new_block: The block to add
            
        Returns:
            True if the block was added successfully, False otherwise
        """
        # Validate the new block
        if not self.is_valid_block(new_block):
            return False
        
        self.chain.append(new_block)
        return True
    
    def is_valid_block(self, block: Block) -> bool:
        """
        Validate a block according to Φ-Chain rules.
        
        Args:
            block: The block to validate
            
        Returns:
            True if the block is valid, False otherwise
        """
        # Check that the block's previous hash matches the latest block
        if block.previous_hash != self.get_latest_block().hash:
            return False
        
        # Check that the block's hash is correct
        if block.hash != block.calculate_hash():
            return False
        
        # Check that the block index is sequential
        if block.index != len(self.chain):
            return False
        
        return True
    
    def add_transaction(self, transaction: Dict[str, Any]) -> bool:
        """
        Add a pending transaction to the mempool.
        
        Args:
            transaction: The transaction to add
            
        Returns:
            True if the transaction was added successfully
        """
        # Validate the transaction
        if self.is_valid_transaction(transaction):
            self.pending_transactions.append(transaction)
            return True
        return False
    
    def is_valid_transaction(self, transaction: Dict[str, Any]) -> bool:
        """
        Validate a transaction.
        
        Args:
            transaction: The transaction to validate
            
        Returns:
            True if the transaction is valid
        """
        # Check required fields
        required_fields = ["from", "to", "amount", "timestamp"]
        if not all(field in transaction for field in required_fields):
            return False
        
        # Check that amount is positive
        if transaction["amount"] <= 0:
            return False
        
        return True
    
    def mine_pending_transactions(self, miner_id: str, difficulty: int = 2) -> Optional[Block]:
        """
        Mine pending transactions into a new block.
        
        Args:
            miner_id: The ID of the miner/validator
            difficulty: The proof-of-work difficulty
            
        Returns:
            The newly mined block, or None if mining failed
        """
        if not self.pending_transactions:
            return None
        
        # Create a new block with pending transactions
        latest_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=FibonacciUtils.fibonacci(6),  # F_6 slot duration
            data={"transactions": self.pending_transactions},
            previous_hash=latest_block.hash,
            validator_id=miner_id
        )
        
        # Mine the block
        new_block.mine_block(difficulty)
        
        # Add the block to the chain
        if self.add_block(new_block):
            self.pending_transactions = []
            return new_block
        
        return None
    
    def get_balance(self, address: str) -> float:
        """
        Calculate the balance for an address.
        
        Args:
            address: The address to check
            
        Returns:
            The balance of the address
        """
        balance = 0.0
        
        for block in self.chain:
            if "transactions" in block.data:
                for transaction in block.data["transactions"]:
                    if transaction.get("from") == address:
                        balance -= transaction.get("amount", 0)
                    if transaction.get("to") == address:
                        balance += transaction.get("amount", 0)
        
        return balance
    
    def is_chain_valid(self) -> bool:
        """
        Validate the entire blockchain.
        
        Returns:
            True if the chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check current block's hash
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check link to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_chain_length(self) -> int:
        """Get the length of the blockchain."""
        return len(self.chain)
    
    def get_chain_summary(self) -> Dict[str, Any]:
        """Get a summary of the blockchain."""
        return {
            "length": len(self.chain),
            "is_valid": self.is_chain_valid(),
            "pending_transactions": len(self.pending_transactions),
            "latest_block_hash": self.get_latest_block().hash,
            "latest_block_index": self.get_latest_block().index
        }


if __name__ == "__main__":
    # Demonstrate blockchain creation
    blockchain = Blockchain()
    print(f"Blockchain created with {blockchain.get_chain_length()} block(s)")
    print(f"Genesis Block: {blockchain.chain[0]}")
    print(f"Chain summary: {blockchain.get_chain_summary()}")
