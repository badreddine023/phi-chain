import os
import json
import hashlib
import secrets
from typing import List, Dict

def generate_validator_key():
    """Generates a secure private key and derives a validator ID."""
    priv_key = secrets.token_hex(32)
    validator_id = "phi_val_" + hashlib.sha256(priv_key.encode()).hexdigest()[:16]
    return priv_key, validator_id

def setup_validators(count: int = 5):
    """Sets up multiple validator nodes with keys and configs."""
    validators = []
    os.makedirs("/home/ubuntu/phi-chain/config/validators", exist_ok=True)
    
    for i in range(count):
        priv_key, val_id = generate_validator_key()
        config = {
            "validator_id": val_id,
            "private_key": priv_key,
            "port": 5000 + i,
            "peers": [5000 + j for j in range(count) if i != j]
        }
        
        config_path = f"/home/ubuntu/phi-chain/config/validators/node_{i}.json"
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
        
        validators.append({"id": val_id, "config": config_path})
        print(f"Validator {i} setup complete: {val_id}")
    
    return validators

if __name__ == "__main__":
    print("--- Φ-Chain Validator Setup ---")
    setup_validators(7) # F_4 + F_3 = 7 (Conceptual Fibonacci count)
