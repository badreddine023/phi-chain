from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Tuple
import json
import asyncio
import time
import hashlib
import numpy as np
import sys
import os

# Configuration de l'API
app = FastAPI(title="Φ-Chain API", description="API de gestion de la blockchain Fibonacci")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Noyau Minimaliste pour l'API ---
def fibonacci(n: int) -> int:
    if n == 0: return 0
    if abs(n) <= 2: return 1
    a, b = 1, 1
    for _ in range(3, abs(n) + 1):
        a, b = b, a + b
    return b

def is_fibonacci_number(n: int) -> bool:
    if n < 0: return False
    # Check if 5n^2 + 4 or 5n^2 - 4 is a perfect square
    def is_perfect_square(x):
        if x < 0: return False
        root = int(x**0.5)
        return root*root == x
    return is_perfect_square(5*n*n + 4) or is_perfect_square(5*n*n - 4)

class Block:
    def __init__(self, index: int, previous_hash: str, transactions: List[Dict], validator: str, f_vector: Tuple[int, int]):
        self.index = index
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.validator = validator
        self.f_vector = f_vector
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.timestamp}{self.previous_hash}{json.dumps(self.transactions)}{self.validator}{self.f_vector}{self.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()

    def mine(self, difficulty=2):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "validator": self.validator,
            "f_vector": self.f_vector,
            "hash": self.hash,
            "nonce": self.nonce
        }

class PhiChain:
    def __init__(self):
        self.state_vector = np.array([1, 1]) # [F_2, F_1]
        self.q_matrix = np.array([[1, 1], [1, 0]])
        self.chain = [Block(0, "0"*64, [], "Genesis", (1, 1))]
        self.pending_transactions = []
        self.balances = {"PHI[A4F2-89BC-11D4-E902][C8A1][F032]": 1597}
        self.validators = {
            "Genesis_Node": {"stake": 6765, "coherence": 1.618, "blocks": 1},
            "Node_Alpha": {"stake": 4181, "coherence": 1.597, "blocks": 0},
            "Node_Beta": {"stake": 2584, "coherence": 1.440, "blocks": 0}
        }

    def get_balance(self, address):
        return self.balances.get(address, 0)

    def evolve_state(self):
        self.state_vector = self.q_matrix @ self.state_vector
        return tuple(map(int, self.state_vector))

    def add_transaction(self, sender, recipient, amount):
        if self.get_balance(sender) < amount:
            return False
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": time.time()
        })
        return True

    def mine_block(self, validator="Genesis_Node"):
        f_vector = self.evolve_state()
        new_block = Block(len(self.chain), self.chain[-1].hash, self.pending_transactions, validator, f_vector)
        new_block.mine(2)
        
        # Update balances
        for tx in self.pending_transactions:
            s, r, a = tx["sender"], tx["recipient"], tx["amount"]
            self.balances[s] = self.balances.get(s, 0) - a
            self.balances[r] = self.balances.get(r, 0) + a
            
        self.chain.append(new_block)
        if validator in self.validators:
            self.validators[validator]["blocks"] += 1
            # Dynamic coherence update simulation
            self.validators[validator]["coherence"] = min(2.0, self.validators[validator]["coherence"] + 0.01)
            
        self.pending_transactions = []
        return new_block

    def get_metrics(self):
        return {
            "total_blocks": len(self.chain),
            "total_transactions": sum(len(b.transactions) for b in self.chain),
            "current_f_vector": tuple(map(int, self.state_vector)),
            "phi_convergence": 1.618033988749895,
            "active_validators": len(self.validators),
            "total_stake": sum(v["stake"] for v in self.validators.values()),
            "pending_tx_count": len(self.pending_transactions)
        }

# --- API Logic ---
phi_chain = PhiChain()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try: await connection.send_json(message)
            except: pass

manager = ConnectionManager()

class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: int

@app.get("/")
async def root():
    return {"status": "Harmonious", "phi": 1.618, "message": "Welcome to the Φ-Chain API"}

@app.get("/metrics")
async def get_metrics():
    return phi_chain.get_metrics()

@app.get("/validators")
async def get_validators():
    return phi_chain.validators

@app.get("/balance/{address}")
async def get_balance(address: str):
    return {"address": address, "balance": phi_chain.get_balance(address), "unit": "Φ"}

@app.post("/transactions/new")
async def new_transaction(tx: Transaction):
    if not is_fibonacci_number(tx.amount):
        raise HTTPException(status_code=400, detail="Amount must be a Fibonacci number.")
    
    if phi_chain.add_transaction(tx.sender, tx.recipient, tx.amount):
        await manager.broadcast({"type": "NEW_TRANSACTION", "data": tx.dict()})
        return {"message": "Transaction added", "transaction": tx.dict()}
    raise HTTPException(status_code=400, detail="Insufficient balance.")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True: await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def auto_mine():
    while True:
        await asyncio.sleep(8) # F_6 = 8 seconds
        validator = np.random.choice(list(phi_chain.validators.keys()))
        block = phi_chain.mine_block(validator)
        await manager.broadcast({
            "type": "NEW_BLOCK", 
            "data": block.to_dict(),
            "metrics": phi_chain.get_metrics()
        })

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(auto_mine())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
