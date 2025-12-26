import asyncio
import json
import logging
import websockets
from typing import Set, Dict, Any, Optional
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("P2PLiveHandler")

class P2PLiveHandler:
    """
    Handles real-time P2P connections for the Phi-Chain network using WebSockets.
    """
    def __init__(self, host: str, port: int, blockchain: Any):
        self.host = host
        self.port = port
        self.blockchain = blockchain
        self.peers: Set[str] = set()
        self.connections: Dict[str, websockets.WebSocketClientProtocol] = {}
        self.server: Optional[websockets.WebSocketServer] = None

    async def start(self):
        """Start the P2P server."""
        self.server = await websockets.serve(self.handle_connection, self.host, self.port)
        logger.info(f"P2P Server started on ws://{self.host}:{self.port}")

    async def handle_connection(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle incoming peer connections."""
        peer_address = websocket.remote_address
        logger.info(f"New peer connected: {peer_address}")
        try:
            async for message in websocket:
                await self.process_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Peer disconnected: {peer_address}")
        finally:
            # Cleanup if needed
            pass

    async def connect_to_peer(self, peer_url: str):
        """Connect to a remote peer."""
        if peer_url in self.peers:
            return
        
        try:
            async with websockets.connect(peer_url) as websocket:
                self.peers.add(peer_url)
                self.connections[peer_url] = websocket
                logger.info(f"Connected to peer: {peer_url}")
                
                # Send a handshake or initial sync request
                await self.send_message(websocket, "handshake", {"address": f"ws://{self.host}:{self.port}"})
                
                async for message in websocket:
                    await self.process_message(websocket, message)
        except Exception as e:
            logger.error(f"Failed to connect to peer {peer_url}: {e}")
            if peer_url in self.peers:
                self.peers.remove(peer_url)

    async def process_message(self, websocket: Any, message: str):
        """Process incoming messages from peers."""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            payload = data.get("payload")

            if msg_type == "handshake":
                peer_ws_url = payload.get("address")
                if peer_ws_url:
                    self.peers.add(peer_ws_url)
                    logger.info(f"Received handshake from {peer_ws_url}")

            elif msg_type == "new_block":
                logger.info("Received new block from peer")
                # Logic to validate and add block to blockchain
                
            elif msg_type == "new_transaction":
                logger.info("Received new transaction from peer")
                # Logic to add transaction to mempool

            elif msg_type == "sync_request":
                logger.info("Received sync request")
                # Logic to send missing blocks

        except json.JSONDecodeError:
            logger.error("Received invalid JSON message")

    async def broadcast(self, msg_type: str, payload: Any):
        """Broadcast a message to all connected peers."""
        message = json.dumps({"type": msg_type, "payload": payload})
        if self.connections:
            await asyncio.gather(*[ws.send(message) for ws in self.connections.values()])

    async def send_message(self, websocket: Any, msg_type: str, payload: Any):
        """Send a message to a specific peer."""
        message = json.dumps({"type": msg_type, "payload": payload})
        await websocket.send(message)

if __name__ == "__main__":
    # Placeholder for testing
    import sys
    from core.blockchain import Blockchain
    
    async def main():
        blockchain = Blockchain()
        handler = P2PLiveHandler("localhost", 8765, blockchain)
        await handler.start()
        await asyncio.Future()  # run forever

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        asyncio.run(main())
