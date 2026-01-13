#!/usr/bin/env python3
"""
p2p_network_v2.py - Φ-Chain P2P Network Layer (Optimized Merge)

This module integrates the best practices from existing implementations:
- PhiTurboP2P: Fibonacci-hop routing with O(log_phi(N)) latency
- PhiPureP2P: Golden Spiral topology for network structure
- PeerDiscovery: Efficient peer discovery and management
- MessageRouter: Reliable message routing with deduplication

Features:
- Low-latency Fibonacci-hop routing
- Golden Spiral network topology
- Φ-optimized peer selection
- Async message broadcasting
"""

import asyncio
import hashlib
import time
import math
import random
import logging
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

from core.phi_math import PhiMath, fibonacci

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("P2PNetwork")


class MessageType(Enum):
    """Enumeration of P2P message types."""
    PEER_DISCOVERY = "peer_discovery"
    PEER_RESPONSE = "peer_response"
    BLOCK_PROPOSAL = "block_proposal"
    BLOCK_SIGNATURE = "block_signature"
    TRANSACTION = "transaction"
    SYNC_REQUEST = "sync_request"
    SYNC_RESPONSE = "sync_response"
    HEARTBEAT = "heartbeat"


@dataclass
class PeerInfo:
    """Information about a peer node."""
    peer_id: str
    address: str
    port: int
    last_seen: float = field(default_factory=time.time)
    reputation_score: float = 1.0
    is_active: bool = True
    version: str = "1.0"
    capabilities: Set[str] = field(default_factory=set)
    latency: float = 0.01  # Default 10ms latency
    
    def get_connection_string(self) -> str:
        """Get the connection string for this peer."""
        return f"{self.address}:{self.port}"
    
    def is_stale(self, timeout: int = 300) -> bool:
        """Check if the peer connection is stale."""
        return time.time() - self.last_seen > timeout
    
    def update_last_seen(self) -> None:
        """Update the last seen timestamp."""
        self.last_seen = time.time()


@dataclass
class Message:
    """Represents a P2P message."""
    message_type: MessageType
    sender_id: str
    receiver_id: str
    timestamp: float
    payload: Dict
    message_id: str = field(default_factory=lambda: hashlib.sha256(str(time.time()).encode()).hexdigest()[:16])
    
    def to_dict(self) -> Dict:
        """Convert message to dictionary for serialization."""
        return {
            "message_type": self.message_type.value,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "timestamp": self.timestamp,
            "payload": self.payload,
            "message_id": self.message_id
        }


class GoldenSpiralTopology:
    """
    Implements the Golden Spiral network topology.
    
    Nodes are positioned and connected based on Fibonacci properties,
    creating a natural, scalable network structure.
    """
    
    def __init__(self, num_nodes: int, phi_precision: int = 18):
        """Initialize the Golden Spiral topology."""
        self.num_nodes = num_nodes
        self.phi_precision = phi_precision
        self.phi = PhiMath.from_fixed(PhiMath.get_phi(phi_precision))
        self.golden_angle = 137.5  # Degrees
        self.topology = self._create_topology()
    
    def _create_topology(self) -> List[Dict[str, Any]]:
        """Create the Golden Spiral topology."""
        topology = []
        
        for i in range(self.num_nodes):
            # Calculate position using Golden Spiral
            angle = (i * self.golden_angle) % 360
            radius = i * 100
            
            x = radius * math.cos(math.radians(angle))
            y = radius * math.sin(math.radians(angle))
            
            # Calculate Fibonacci-based connections
            connections = self._calculate_fibonacci_connections(i)
            
            topology.append({
                'id': i,
                'position': (x, y),
                'connections': connections,
                'angle': angle,
                'radius': radius
            })
        
        return topology
    
    def _calculate_fibonacci_connections(self, node_id: int) -> List[int]:
        """Calculate peer connections using Fibonacci steps."""
        connections = []
        
        # Connect to nodes at Fibonacci distances
        fib_steps = [fibonacci(n) for n in range(1, 10) if fibonacci(n) < self.num_nodes]
        
        for step in fib_steps:
            if step == 0:
                continue
            
            peer_id = (node_id + step) % self.num_nodes
            if peer_id != node_id and peer_id not in connections:
                connections.append(peer_id)
        
        return connections
    
    def get_node_connections(self, node_id: int) -> List[int]:
        """Get the connections for a specific node."""
        if node_id < len(self.topology):
            return self.topology[node_id]['connections']
        return []


class FibonacciHopRouter:
    """
    Implements Fibonacci-hop routing for low-latency message delivery.
    
    Routes messages through O(log_phi(N)) hops, where N is the network size.
    """
    
    def __init__(self, node_id: int, total_nodes: int, phi_precision: int = 18):
        """Initialize the Fibonacci-hop router."""
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.phi_precision = phi_precision
        self.phi = PhiMath.from_fixed(PhiMath.get_phi(phi_precision))
        self.turbo_peers = self._calculate_turbo_peers()
    
    def _calculate_turbo_peers(self) -> List[int]:
        """Calculate turbo peers using Fibonacci steps and Golden Angle."""
        peers = set()
        
        # Fibonacci steps for global reach
        a, b = 1, 1
        while b < self.total_nodes:
            peer = (self.node_id + b) % self.total_nodes
            if peer != self.node_id:
                peers.add(peer)
            a, b = b, a + b
        
        # Golden Angle neighbors for local clustering
        for i in range(1, 5):
            angle_step = int(i * 137.5) % self.total_nodes
            peer = (self.node_id + angle_step) % self.total_nodes
            if peer != self.node_id:
                peers.add(peer)
        
        return list(peers)
    
    def get_turbo_peers(self) -> List[int]:
        """Get the list of turbo peers for this node."""
        return self.turbo_peers
    
    def calculate_hop_distance(self, target_node: int) -> int:
        """Calculate the number of hops to reach a target node."""
        distance = 0
        current = self.node_id
        visited = set()
        
        while current != target_node and current not in visited:
            visited.add(current)
            
            # Find the closest turbo peer to the target
            turbo_peers = self.get_turbo_peers()
            closest_peer = min(
                turbo_peers,
                key=lambda p: abs((p - target_node) % self.total_nodes)
            )
            
            current = closest_peer
            distance += 1
            
            if distance > 10:  # Safety limit
                break
        
        return distance


class PeerDiscovery:
    """
    Manages peer discovery and connection management.
    
    Uses φ-optimized peer discovery protocol for efficient peer finding.
    """
    
    def __init__(self, node_id: str, bootstrap_peers: Optional[List[PeerInfo]] = None, 
                 phi_precision: int = 18):
        """Initialize peer discovery."""
        self.node_id = node_id
        self.phi_precision = phi_precision
        self.phi = PhiMath.from_fixed(PhiMath.get_phi(phi_precision))
        
        # Known peers
        self.peers: Dict[str, PeerInfo] = {}
        
        # Add bootstrap peers
        if bootstrap_peers:
            for peer in bootstrap_peers:
                self.peers[peer.peer_id] = peer
        
        # Target peer count (Fibonacci number)
        self.target_peer_count = fibonacci(10)  # F_10 = 55
        
        logger.info(f"PeerDiscovery initialized - Target peer count: {self.target_peer_count}")
    
    def add_peer(self, peer_info: PeerInfo) -> bool:
        """Add a peer to the known peers list."""
        if peer_info.peer_id in self.peers:
            self.peers[peer_info.peer_id].update_last_seen()
            return False
        
        self.peers[peer_info.peer_id] = peer_info
        logger.info(f"Peer added: {peer_info.peer_id}")
        return True
    
    def remove_peer(self, peer_id: str) -> bool:
        """Remove a peer from the known peers list."""
        if peer_id in self.peers:
            del self.peers[peer_id]
            logger.info(f"Peer removed: {peer_id}")
            return True
        return False
    
    def get_active_peers(self) -> List[PeerInfo]:
        """Get all active peers."""
        return [p for p in self.peers.values() if p.is_active and not p.is_stale()]
    
    def get_peer_by_id(self, peer_id: str) -> Optional[PeerInfo]:
        """Get a peer by ID."""
        return self.peers.get(peer_id)
    
    def select_peers_for_discovery(self, count: int = 5) -> List[PeerInfo]:
        """Select peers for discovery using φ-weighted random selection."""
        active_peers = self.get_active_peers()
        
        if not active_peers:
            return []
        
        # Calculate weights based on reputation scores
        weights = [peer.reputation_score for peer in active_peers]
        total_weight = sum(weights)
        
        if total_weight == 0:
            return random.sample(active_peers, min(count, len(active_peers)))
        
        # Weighted random selection
        probabilities = [w / total_weight for w in weights]
        selected = random.choices(active_peers, weights=probabilities, k=min(count, len(active_peers)))
        
        return selected
    
    def update_peer_reputation(self, peer_id: str, delta: float) -> None:
        """Update a peer's reputation score."""
        if peer_id in self.peers:
            peer = self.peers[peer_id]
            peer.reputation_score = max(0.0, peer.reputation_score + delta)
            peer.update_last_seen()


class P2PNetwork:
    """
    Main P2P network coordinator.
    
    Integrates peer discovery, message routing, and network topology.
    """
    
    def __init__(self, node_id: str, address: str, port: int, total_nodes: int = 1000,
                 bootstrap_peers: Optional[List[PeerInfo]] = None):
        """Initialize the P2P network."""
        self.node_id = node_id
        self.address = address
        self.port = port
        self.total_nodes = total_nodes
        
        # Initialize components
        self.peer_discovery = PeerDiscovery(node_id, bootstrap_peers)
        self.router = FibonacciHopRouter(hash(node_id) % total_nodes, total_nodes)
        self.topology = GoldenSpiralTopology(total_nodes)
        
        # Message queues
        self.outgoing_queues: Dict[str, List[Message]] = defaultdict(list)
        self.incoming_queue: List[Message] = []
        self.message_history: Set[str] = set()
        
        # Network statistics
        self.network_start_time = time.time()
        self.messages_sent = 0
        self.messages_received = 0
        
        logger.info(f"P2PNetwork initialized - Node: {node_id}, Address: {address}:{port}")
    
    def broadcast_message(self, message_type: MessageType, payload: Dict) -> int:
        """Broadcast a message to all active peers."""
        active_peers = self.peer_discovery.get_active_peers()
        
        message = Message(
            message_type=message_type,
            sender_id=self.node_id,
            receiver_id="broadcast",
            timestamp=time.time(),
            payload=payload
        )
        
        count = 0
        for peer in active_peers:
            if self._enqueue_message(message, peer.peer_id):
                count += 1
        
        logger.info(f"Broadcast message sent to {count} peers")
        return count
    
    def send_message_to_peer(self, peer_id: str, message_type: MessageType, payload: Dict) -> bool:
        """Send a message to a specific peer."""
        message = Message(
            message_type=message_type,
            sender_id=self.node_id,
            receiver_id=peer_id,
            timestamp=time.time(),
            payload=payload
        )
        
        return self._enqueue_message(message, peer_id)
    
    def _enqueue_message(self, message: Message, target_peer_id: str) -> bool:
        """Enqueue a message for delivery."""
        if message.message_id in self.message_history:
            return False  # Duplicate
        
        self.message_history.add(message.message_id)
        
        max_queue_size = fibonacci(15)  # F_15 = 610
        if len(self.outgoing_queues[target_peer_id]) >= max_queue_size:
            return False  # Queue full
        
        self.outgoing_queues[target_peer_id].append(message)
        self.messages_sent += 1
        
        return True
    
    async def broadcast_async(self, message_type: MessageType, payload: Dict) -> int:
        """Asynchronously broadcast a message to all active peers."""
        active_peers = self.peer_discovery.get_active_peers()
        
        message = Message(
            message_type=message_type,
            sender_id=self.node_id,
            receiver_id="broadcast",
            timestamp=time.time(),
            payload=payload
        )
        
        # Simulate async broadcast with peer latencies
        tasks = [self._send_to_peer_async(peer, message) for peer in active_peers]
        await asyncio.gather(*tasks)
        
        return len(active_peers)
    
    async def _send_to_peer_async(self, peer: PeerInfo, message: Message) -> None:
        """Asynchronously send a message to a peer."""
        await asyncio.sleep(peer.latency)
        self._enqueue_message(message, peer.peer_id)
    
    def get_network_stats(self) -> Dict:
        """Get network statistics."""
        uptime = time.time() - self.network_start_time
        
        return {
            "node_id": self.node_id,
            "address": f"{self.address}:{self.port}",
            "uptime_seconds": uptime,
            "active_peers": len(self.peer_discovery.get_active_peers()),
            "total_known_peers": len(self.peer_discovery.peers),
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "target_peer_count": self.peer_discovery.target_peer_count,
            "turbo_peers": len(self.router.get_turbo_peers()),
            "avg_hop_distance": self._calculate_avg_hop_distance()
        }
    
    def _calculate_avg_hop_distance(self) -> float:
        """Calculate average hop distance to all peers."""
        if not self.peer_discovery.peers:
            return 0.0
        
        total_hops = 0
        for peer in self.peer_discovery.peers.values():
            try:
                node_num = hash(peer.peer_id) % self.total_nodes
                hops = self.router.calculate_hop_distance(node_num)
                total_hops += hops
            except:
                pass
        
        return total_hops / len(self.peer_discovery.peers) if self.peer_discovery.peers else 0.0


# Example usage and testing
if __name__ == "__main__":
    print("=== Φ-Chain P2P Network v2 (Optimized Merge) ===\n")
    
    # Create bootstrap peers
    bootstrap_peers = [
        PeerInfo(peer_id="peer_001", address="192.168.1.1", port=8001),
        PeerInfo(peer_id="peer_002", address="192.168.1.2", port=8002),
        PeerInfo(peer_id="peer_003", address="192.168.1.3", port=8003),
    ]
    
    # Initialize P2P network
    p2p = P2PNetwork(
        node_id="node_001",
        address="192.168.1.100",
        port=8000,
        total_nodes=1000,
        bootstrap_peers=bootstrap_peers
    )
    
    print(f"P2P Network initialized for node: {p2p.node_id}\n")
    
    # Test peer discovery
    print("Active peers:")
    for peer in p2p.peer_discovery.get_active_peers():
        print(f"  {peer.peer_id} - {peer.get_connection_string()}")
    
    print(f"\nTotal known peers: {len(p2p.peer_discovery.peers)}")
    print(f"Target peer count: {p2p.peer_discovery.target_peer_count}\n")
    
    # Test message broadcasting
    print("Broadcasting test message...")
    count = p2p.broadcast_message(
        MessageType.HEARTBEAT,
        {"message": "Hello from node_001"}
    )
    print(f"Message sent to {count} peers\n")
    
    # Test network stats
    print("Network Statistics:")
    stats = p2p.get_network_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
