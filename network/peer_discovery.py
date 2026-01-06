import asyncio
import json
import logging
import random
from typing import List, Set

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PeerDiscovery")

class PeerDiscovery:
    """
    Handles peer discovery for the Phi-Chain network.
    Uses a list of seed nodes and potentially a DHT-like mechanism.
    """
    def __init__(self, seed_nodes: List[str]):
        self.seed_nodes = seed_nodes
        self.discovered_peers: Set[str] = set(seed_nodes)

    async def discover(self):
        """
        Periodically attempt to discover new peers.
        In a real implementation, this would query seed nodes or use Kademlia DHT.
        """
        while True:
            logger.info(f"Current discovered peers: {self.discovered_peers}")
            # Simulate discovery logic
            # 1. Query known peers for their peer lists
            # 2. Update self.discovered_peers
            await asyncio.sleep(60)  # Discover every minute

    def get_peers(self) -> List[str]:
        """Return a list of discovered peers."""
        return list(self.discovered_peers)

    def add_peer(self, peer_url: str):
        """Add a newly discovered peer."""
        self.discovered_peers.add(peer_url)

    def remove_peer(self, peer_url: str):
        """Remove a peer that is no longer active."""
        if peer_url in self.discovered_peers:
            self.discovered_peers.remove(peer_url)

if __name__ == "__main__":
    async def main():
        discovery = PeerDiscovery(["ws://seed1.phi-chain.io:8765", "ws://seed2.phi-chain.io:8765"])
        await discovery.discover()

    asyncio.run(main())
