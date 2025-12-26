import time
import hashlib
from typing import List, Dict, Any
from core.phi_integer_math import PhiIntegerMath, PHI_NUMERATOR, PHI_DENOMINATOR

class GoldenBlock:
    """
    Golden Phi Block - No Decimals.
    Uses Phi-Proof-of-Harmony for consensus.
    """
    
    def __init__(self, height: int, previous_hash: str, transactions: List[Dict[str, Any]] = None):
        self.height = height
        self.previous_hash = previous_hash
        self.timestamp = int(time.time())
        self.transactions = transactions or []
        self.golden_nonce = self.find_golden_nonce()
        self.phi_hash = self.calculate_phi_hash()
    
    def find_golden_nonce(self) -> int:
        """
        Find a nonce that produces a Phi-harmonious value.
        The target is based on the height and the Golden Ratio.
        """
        target = (self.height * PHI_NUMERATOR) // PHI_DENOMINATOR
        nonce = 0
        
        # Search for a nonce where (nonce * Phi) % 1000 matches the target's harmony
        while True:
            test_value = (nonce * PHI_NUMERATOR) // PHI_DENOMINATOR
            if test_value % 1000 == target % 1000:
                return nonce
            nonce += 1
            if nonce > 1000000: # Safety break for simulation
                return nonce
    
    def calculate_phi_hash(self) -> str:
        """
        Calculate hash using only Phi properties.
        """
        # Combine block data into a large integer
        tx_data = "".join([str(tx) for tx in self.transactions])
        data = f"{self.height}{self.previous_hash}{self.golden_nonce}{tx_data}"
        data_int = int.from_bytes(data.encode(), 'big')
        
        # Apply multiple Phi transformations (7 times - a Fibonacci number)
        transformed = data_int
        for _ in range(7):
            transformed = PhiIntegerMath.phi_multiply(transformed, PHI_NUMERATOR)
        
        # Return as a PHI-prefixed hex string
        return f"PHI{transformed:064X}"[-64:]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "height": self.height,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "golden_nonce": self.golden_nonce,
            "phi_hash": self.phi_hash,
            "transactions": self.transactions
        }

class PhiBlockchain:
    """
    A blockchain built on Pure Phi principles.
    """
    def __init__(self):
        self.chain: List[GoldenBlock] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = GoldenBlock(0, "0" * 64)
        self.chain.append(genesis)

    def add_block(self, transactions: List[Dict[str, Any]]):
        previous_block = self.chain[-1]
        new_block = GoldenBlock(len(self.chain), previous_block.phi_hash, transactions)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.previous_hash != previous.phi_hash:
                return False
            
            # Re-verify the golden nonce harmony
            target = (current.height * PHI_NUMERATOR) // PHI_DENOMINATOR
            test_value = (current.golden_nonce * PHI_NUMERATOR) // PHI_DENOMINATOR
            if test_value % 1000 != target % 1000:
                return False
                
        return True

if __name__ == "__main__":
    blockchain = PhiBlockchain()
    print(f"Genesis Block Hash: {blockchain.chain[0].phi_hash}")
    
    blockchain.add_block([{"from": "A", "to": "B", "amount": 5}])
    print(f"Block 1 Hash: {blockchain.chain[1].phi_hash}")
    print(f"Is Chain Valid? {blockchain.is_chain_valid()}")
