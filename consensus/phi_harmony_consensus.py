import logging
from typing import List, Dict, Any
from core.phi_integer_math import PhiIntegerMath, PHI_NUMERATOR, PHI_DENOMINATOR
from core.phi_block_system import GoldenBlock

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PhiHarmonyConsensus")

class PhiHarmonyConsensus:
    """
    Proof-of-Phi-Harmony Consensus.
    No mining or energy burn; consensus is reached through mathematical harmony.
    """
    
    def validate_block(self, block: GoldenBlock) -> bool:
        """
        Validate a block based on Phi Harmony.
        """
        # 1. Verify Golden Nonce Harmony
        # The nonce must be in a 'Golden Position' relative to the block height
        target_harmony = (block.height * PHI_NUMERATOR) // PHI_DENOMINATOR
        actual_harmony = (block.golden_nonce * PHI_NUMERATOR) // PHI_DENOMINATOR
        
        if actual_harmony % 1000 != target_harmony % 1000:
            logger.warning(f"Block {block.height} failed harmony check.")
            return False
            
        # 2. Verify Transactions
        for tx in block.transactions:
            if not self.validate_phi_transaction(tx):
                return False
                
        logger.info(f"Block {block.height} validated via Proof-of-Harmony.")
        return True

    def validate_phi_transaction(self, tx: Dict[str, Any]) -> bool:
        """
        Validate a transaction: Amount must be a Fibonacci number.
        """
        amount = tx.get("amount", 0)
        if not PhiIntegerMath.is_fibonacci_number(amount):
            logger.warning(f"Invalid transaction amount: {amount} is not a Fibonacci number.")
            return False
        return True

    def calculate_phi_reward(self, height: int) -> int:
        """
        Calculate block reward using Fibonacci sequence.
        Rewards follow the sequence: 1, 1, 2, 3, 5, 8, 13... PHI
        """
        return PhiIntegerMath.golden_fibonacci(height % 20 + 1) # Cycle through first 20 Fib numbers

if __name__ == "__main__":
    consensus = PhiHarmonyConsensus()
    # Test valid Fibonacci amount
    print(f"Is 144 valid? {consensus.validate_phi_transaction({'amount': 144})}")
    # Test invalid amount
    print(f"Is 100 valid? {consensus.validate_phi_transaction({'amount': 100})}")
    # Test reward
    print(f"Reward for block 10: {consensus.calculate_phi_reward(10)}")
