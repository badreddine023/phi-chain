import decimal

# Set the precision for high-fidelity mathematical purity
# We will use 50 digits of precision to exceed the 15 decimal places specified in the architecture
decimal.getcontext().prec = 50

# --- Core Constants ---

def calculate_phi():
    """Calculates the Golden Ratio (phi) to the set precision."""
    # phi = (1 + sqrt(5)) / 2
    D = decimal.Decimal
    five = D(5)
    one = D(1)
    two = D(2)
    sqrt_five = five.sqrt()
    phi = (one + sqrt_five) / two
    return phi

def calculate_phi_inverse(phi):
    """Calculates the Inverse Golden Ratio (phi_inverse) to the set precision."""
    # phi_inverse = 1 / phi = phi - 1
    one = decimal.Decimal(1)
    phi_inverse = one / phi
    return phi_inverse

PHI = calculate_phi()
PHI_INV = calculate_phi_inverse(PHI)

# --- Sequence Generators ---

def fibonacci_sequence(n):
    """Generates the first n Fibonacci numbers (F_0 to F_{n-1})."""
    if n <= 0:
        return []
    
    sequence = [0, 1]
    if n == 1:
        return [0]
    if n == 2:
        return sequence
    
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence

def lucas_sequence(n):
    """Generates the first n Lucas numbers (L_0 to L_{n-1})."""
    if n <= 0:
        return []
    
    sequence = [2, 1]
    if n == 1:
        return [2]
    if n == 2:
        return sequence
    
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence

# --- Φ-Chain Genesis Parameters (Derived) ---

def get_genesis_parameters():
    """
    Derives the Φ-Chain Genesis Parameters based on the architectural specifications.
    """
    # F_n values
    F7 = fibonacci_sequence(8)[7]  # 13
    F8 = fibonacci_sequence(9)[8]  # 21
    
    # L_n values (for fees, not directly used in genesis params)
    
    # Block Time: phi seconds
    block_time = PHI
    
    # Initial Validators: F7
    initial_validators = F7
    
    # Consensus Threshold: phi_inverse
    consensus_threshold = PHI_INV
    
    # Token Supply: phi * 10^15
    token_supply = PHI * decimal.Decimal(10**15)
    
    # Shard Count: F8
    shard_count = F8
    
    return {
        "block_time": f"{block_time} seconds",
        "initial_validators": initial_validators,
        "consensus_threshold": consensus_threshold,
        "token_supply": token_supply,
        "shard_count": shard_count,
        "phi": PHI,
        "phi_inverse": PHI_INV
    }

if __name__ == "__main__":
    print("--- Φ-Chain Mathematical Primitives ---")
    
    params = get_genesis_parameters()
    
    print(f"PHI (Golden Ratio): {params['phi']}")
    print(f"PHI_INV (Inverse Golden Ratio): {params['phi_inverse']}")
    print("-" * 35)
    print(f"Block Time: {params['block_time']}")
    print(f"Initial Validators (F7): {params['initial_validators']}")
    print(f"Consensus Threshold (phi^-1): {params['consensus_threshold']}")
    print(f"Shard Count (F8): {params['shard_count']}")
    print(f"Token Supply (phi * 10^15): {params['token_supply']}")
    print("-" * 35)
    print(f"First 10 Fibonacci Numbers: {fibonacci_sequence(10)}")
    print(f"First 10 Lucas Numbers: {lucas_sequence(10)}")
