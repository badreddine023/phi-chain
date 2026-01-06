import logging
import hashlib
import json
from typing import List, Dict, Any, Set

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LiveConsensusEngine")

class LiveConsensusEngine:
    """
    Implements a Federated Byzantine Agreement (FBA) inspired consensus engine.
    """
    def __init__(self, node_id: str, quorum_slices: List[Set[str]]):
        self.node_id = node_id
        self.quorum_slices = quorum_slices
        self.current_round = 0
        self.votes: Dict[int, Dict[str, Any]] = {}

    def propose(self, value: Any):
        """Propose a value for the current consensus round."""
        self.current_round += 1
        logger.info(f"Node {self.node_id} proposing value for round {self.current_round}")
        # In a real FBA, this would involve multiple phases: Nominate, Prepare, Commit
        return self.cast_vote(self.current_round, value)

    def cast_vote(self, round_id: int, value: Any):
        """Cast a vote for a specific round."""
        vote = {
            "node_id": self.node_id,
            "round_id": round_id,
            "value": value,
            "signature": self.sign_vote(value)
        }
        return vote

    def sign_vote(self, value: Any) -> str:
        """Sign the vote (placeholder for actual cryptographic signing)."""
        return hashlib.sha256(str(value).encode()).hexdigest()

    def process_vote(self, vote: Dict[str, Any]):
        """Process a vote received from another node."""
        round_id = vote["round_id"]
        if round_id not in self.votes:
            self.votes[round_id] = {}
        
        self.votes[round_id][vote["node_id"]] = vote["value"]
        
        if self.check_quorum(round_id):
            logger.info(f"Quorum reached for round {round_id}")
            return True
        return False

    def check_quorum(self, round_id: int) -> bool:
        """Check if a quorum has been reached for a given round."""
        if round_id not in self.votes:
            return False
        
        received_nodes = set(self.votes[round_id].keys())
        
        # Check if any quorum slice is satisfied
        for slice in self.quorum_slices:
            if slice.issubset(received_nodes):
                # Check if they all voted for the same value
                values = [self.votes[round_id][node] for node in slice]
                if len(set(map(str, values))) == 1:
                    return True
        return False

if __name__ == "__main__":
    # Simple test
    slices = [{"node1", "node2"}, {"node1", "node3"}]
    engine = LiveConsensusEngine("node1", slices)
    
    vote1 = engine.propose("block_hash_abc")
    engine.process_vote(vote1)
    
    vote2 = {"node_id": "node2", "round_id": 1, "value": "block_hash_abc"}
    if engine.process_vote(vote2):
        print("Consensus reached!")
