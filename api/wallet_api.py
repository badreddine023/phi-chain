"""
api/wallet_api.py - Φ-Chain Wallet Backend API

This module provides REST API endpoints for wallet operations, staking, mining, and blockchain queries.
"""

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import asyncio
from typing import Dict, List, Optional
import sys
sys.path.insert(0, '..')

from phi_chain import (
    Blockchain,
    GenesisParameters,
    PhiTransaction,
    ProofOfCoherence,
    FibonacciUtils
)

# Initialize FastAPI app
app = FastAPI(title="Φ-Chain Wallet API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global blockchain instance
blockchain = Blockchain()
poc = ProofOfCoherence(blockchain)
params = GenesisParameters()

# Connected clients for WebSocket
connected_clients: List[WebSocket] = []

# --- Wallet Endpoints ---

@app.get("/api/wallet/balance/{address}")
async def get_balance(address: str):
    """Get wallet balance for an address."""
    try:
        balance = blockchain.get_balance(address)
        return {
            "address": address,
            "balance": balance,
            "symbol": "Φ"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/wallet/send")
async def send_transaction(transaction_data: Dict):
    """Send a transaction."""
    try:
        # Validate required fields
        required_fields = ["from", "to", "amount"]
        if not all(field in transaction_data for field in required_fields):
            raise ValueError("Missing required fields")
        
        # Create transaction
        tx = PhiTransaction(
            sender=transaction_data["from"],
            recipient=transaction_data["to"],
            value=int(transaction_data["amount"]),
            nonce=transaction_data.get("nonce", 0)
        )
        
        # Validate transaction
        if not tx.validate(blockchain):
            raise ValueError("Invalid transaction")
        
        # Add to blockchain
        blockchain.add_transaction(tx)
        
        return {
            "status": "success",
            "tx_hash": tx.calculate_hash(),
            "message": "Transaction added to mempool"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/wallet/transactions/{address}")
async def get_transactions(address: str):
    """Get transaction history for an address."""
    try:
        transactions = []
        for block in blockchain.chain:
            for tx in block.transactions:
                if tx.sender == address or tx.recipient == address:
                    transactions.append({
                        "hash": tx.calculate_hash(),
                        "from": tx.sender,
                        "to": tx.recipient,
                        "amount": tx.value,
                        "timestamp": tx.timestamp,
                        "type": "sent" if tx.sender == address else "received"
                    })
        
        return {
            "address": address,
            "transactions": transactions,
            "total": len(transactions)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Staking Endpoints ---

@app.post("/api/staking/stake")
async def stake_tokens(staking_data: Dict):
    """Stake tokens to become a validator."""
    try:
        validator_id = staking_data.get("validator_id")
        stake_amount = int(staking_data.get("amount", 0))
        
        # Check if stake is Fibonacci number
        if not FibonacciUtils.is_fibonacci(stake_amount):
            raise ValueError(f"Stake amount {stake_amount} is not a Fibonacci number")
        
        # Check minimum stake
        if stake_amount < params.MIN_VALIDATOR_STAKE:
            raise ValueError(f"Minimum stake is {params.MIN_VALIDATOR_STAKE} Φ")
        
        # Add validator
        if blockchain.add_validator(validator_id, stake_amount):
            return {
                "status": "success",
                "validator_id": validator_id,
                "stake": stake_amount,
                "message": "Validator registered successfully"
            }
        else:
            raise ValueError("Failed to register validator")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/staking/validators")
async def get_validators():
    """Get list of all validators."""
    try:
        validators = []
        for validator_id, validator_data in blockchain.validators.items():
            validators.append({
                "id": validator_id,
                "stake": validator_data["stake"],
                "participation": validator_data["participation"],
                "blocks_proposed": validator_data["blocks_proposed"],
                "rewards": validator_data["rewards"],
                "coherence_score": poc.calculate_coherence_score(validator_id)
            })
        
        return {
            "validators": validators,
            "total": len(validators),
            "max_validators": params.MAX_VALIDATOR_COUNT
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/staking/rewards/{validator_id}")
async def get_rewards(validator_id: str):
    """Get staking rewards for a validator."""
    try:
        if validator_id not in blockchain.validators:
            raise ValueError("Validator not found")
        
        validator = blockchain.validators[validator_id]
        return {
            "validator_id": validator_id,
            "total_rewards": validator["rewards"],
            "stake": validator["stake"],
            "apr": 14.4  # F_12 = 144 / 10 = 14.4%
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Mining Endpoints ---

@app.post("/api/mining/start")
async def start_mining(mining_data: Dict):
    """Start PoC mining."""
    try:
        miner_id = mining_data.get("miner_id")
        
        return {
            "status": "success",
            "miner_id": miner_id,
            "message": "Mining started",
            "hashrate": "1.618 GH/s",
            "coherence_score": 0.999
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/mining/submit_block")
async def submit_block(block_data: Dict):
    """Submit a mined block."""
    try:
        # In production, validate PoW and block structure
        miner_id = block_data.get("miner_id")
        
        # Mine pending transactions
        block = blockchain.mine_pending_transactions(miner_id)
        
        if block:
            return {
                "status": "success",
                "block_hash": block.hash,
                "block_index": block.index,
                "reward": params.BLOCK_REWARD
            }
        else:
            raise ValueError("No pending transactions to mine")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/mining/stats")
async def get_mining_stats():
    """Get mining statistics."""
    try:
        return {
            "difficulty": 2,
            "pending_transactions": len(blockchain.pending_transactions),
            "block_reward": params.BLOCK_REWARD,
            "average_block_time": params.SLOT_DURATION,
            "network_hashrate": "1.618 TH/s"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Blockchain Endpoints ---

@app.get("/api/blockchain/info")
async def get_blockchain_info():
    """Get blockchain information."""
    try:
        summary = blockchain.get_chain_summary()
        return {
            "chain_length": summary["length"],
            "is_valid": summary["is_valid"],
            "latest_block": {
                "hash": summary["latest_block_hash"],
                "index": summary["latest_block_index"],
                "timestamp": summary["latest_block_timestamp"]
            },
            "f_vector": summary["f_vector"],
            "total_supply": summary["total_supply"],
            "symbol": "Φ"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/blockchain/blocks/{block_index}")
async def get_block(block_index: int):
    """Get block details by index."""
    try:
        if block_index < 0 or block_index >= len(blockchain.chain):
            raise ValueError("Block not found")
        
        block = blockchain.chain[block_index]
        return {
            "index": block.index,
            "hash": block.hash,
            "previous_hash": block.previous_hash,
            "timestamp": block.timestamp,
            "proposer": block.proposer,
            "f_vector": block.f_vector,
            "transactions": [tx.to_dict() for tx in block.transactions],
            "nonce": block.nonce
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/blockchain/blocks")
async def get_blocks(limit: int = 10):
    """Get latest blocks."""
    try:
        blocks = []
        start_index = max(0, len(blockchain.chain) - limit)
        
        for block in blockchain.chain[start_index:]:
            blocks.append({
                "index": block.index,
                "hash": block.hash,
                "timestamp": block.timestamp,
                "proposer": block.proposer,
                "transactions": len(block.transactions)
            })
        
        return {
            "blocks": blocks,
            "total": len(blockchain.chain)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/blockchain/validate")
async def validate_blockchain():
    """Validate the entire blockchain."""
    try:
        is_valid = blockchain.is_chain_valid()
        return {
            "is_valid": is_valid,
            "chain_length": len(blockchain.chain),
            "message": "Blockchain is valid" if is_valid else "Blockchain is invalid"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Parameters Endpoints ---

@app.get("/api/parameters")
async def get_parameters():
    """Get all genesis parameters."""
    try:
        return {
            "parameters": params.to_dict(),
            "phi": params.PHI,
            "description": "All Φ-Chain parameters derived from Fibonacci sequence"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- WebSocket for Real-time Updates ---

@app.websocket("/ws/blockchain")
async def websocket_blockchain(websocket: WebSocket):
    """WebSocket endpoint for real-time blockchain updates."""
    await websocket.accept()
    connected_clients.append(websocket)
    
    try:
        while True:
            # Send blockchain updates every 5 seconds
            await asyncio.sleep(5)
            
            summary = blockchain.get_chain_summary()
            update = {
                "type": "blockchain_update",
                "chain_length": summary["length"],
                "pending_transactions": summary["pending_transactions"],
                "latest_block_hash": summary["latest_block_hash"]
            }
            
            await websocket.send_json(update)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)

# --- Health Check ---

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "blockchain_length": len(blockchain.chain),
        "validators": len(blockchain.validators),
        "pending_transactions": len(blockchain.pending_transactions)
    }

# --- Root Endpoint ---

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Φ-Chain Wallet API",
        "version": "1.0.0",
        "endpoints": {
            "wallet": "/api/wallet",
            "staking": "/api/staking",
            "mining": "/api/mining",
            "blockchain": "/api/blockchain",
            "parameters": "/api/parameters"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("Φ-CHAIN WALLET API SERVER")
    print("=" * 60)
    print("Starting server on http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
