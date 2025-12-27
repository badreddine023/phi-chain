import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_chain import Blockchain, PhiTransaction, PhiBlock
import time

def test_longest_chain():
    print("Testing Longest Chain Rule...")
    
    # 1. Initialize two nodes (blockchains)
    node_a = Blockchain()
    node_b = Blockchain()
    
    print(f"Initial length: Node A = {node_a.get_chain_length()}, Node B = {node_b.get_chain_length()}")
    
    # 2. Node A mines a block
    tx1 = PhiTransaction("0xAlice", "0xBob", 10)
    node_a.add_transaction(tx1)
    node_a.mine_pending_transactions("validator_a")
    
    print(f"After Node A mines: Node A = {node_a.get_chain_length()}, Node B = {node_b.get_chain_length()}")
    
    # 3. Node B mines two blocks (creating a longer chain)
    tx2 = PhiTransaction("0xCharlie", "0xDave", 20)
    node_b.add_transaction(tx2)
    node_b.mine_pending_transactions("validator_b")
    
    tx3 = PhiTransaction("0xEve", "0xFrank", 30)
    node_b.add_transaction(tx3)
    node_b.mine_pending_transactions("validator_b")
    
    print(f"After Node B mines 2 blocks: Node A = {node_a.get_chain_length()}, Node B = {node_b.get_chain_length()}")
    
    # 4. Node A resolves conflicts with Node B's chain
    print("Node A resolving conflicts with Node B's chain...")
    node_a.resolve_conflicts([node_b.chain])
    
    print(f"Final length: Node A = {node_a.get_chain_length()}, Node B = {node_b.get_chain_length()}")
    
    if node_a.get_chain_length() == 3:
        print("✅ Success: Node A adopted the longer chain from Node B.")
    else:
        print("❌ Failure: Node A did not adopt the longer chain.")

if __name__ == "__main__":
    test_longest_chain()
