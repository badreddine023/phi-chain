import math
import numpy as np

# --- 1. Fibonacci Utility Function ---

def fibonacci(n):
    """Calculates the nth Fibonacci number F_n."""
    if n <= 0:
        return 0
    if n == 1 or n == 2:
        return 1
    
    # Using the closed-form Binet's formula for efficiency and precision,
    # though iterative calculation is also common.
    phi = (1 + math.sqrt(5)) / 2
    return int(round((phi**n - (1-phi)**n) / math.sqrt(5)))

# --- 2. Parameter Derivation ---

def derive_parameters():
    """Derives and prints the core Φ-Chain parameters from Fibonacci indices."""
    
    # The Golden Ratio constant (Phi)
    PHI = (1 + math.sqrt(5)) / 2
    
    # Parameters from Section IV, derived from F_n
    parameters = {
        "Golden Ratio Constant (Φ)": f"{PHI:.59f}",
        "Slot Duration (F_6)": fibonacci(6),
        "Epoch Duration (F_18)": fibonacci(18),
        "Min Validator Stake (F_20)": fibonacci(20),
        "Max Validator Count (F_17)": fibonacci(17),
        "Target Committee Size (F_14)": fibonacci(14),
        "Finality Threshold (F_15)": fibonacci(15),
        "Slots per Epoch (F_18 / F_6)": fibonacci(18) // fibonacci(6),
    }
    
    print("--- Φ-Chain Genesis Parameters (Derived from F_n) ---")
    for name, value in parameters.items():
        print(f"{name:<30}: {value}")
    
    # Minimum Balance Tiers (F_1 to F_15)
    balance_tiers = [fibonacci(i) for i in range(1, 16)]
    print("\nMinimum Balance Tiers (F_1 to F_15):")
    print(f"  {balance_tiers}")
    
    # Fee Tiers (F_1 to F_12)
    fee_tiers = [fibonacci(i) for i in range(1, 13)]
    print("\nFee Tiers (F_1 to F_12):")
    print(f"  {fee_tiers}")
    
    return parameters

# --- 3. State Transition Simulation (The Matrix) ---

def simulate_state_transition(steps=5):
    """
    Simulates the chain's state transition using the Fibonacci Q-matrix.
    The Q-matrix is the core of the chain's logic, where eigenvalues are Φ and 1-Φ.
    
    State Vector S_n = [F_{n+1}, F_n]^T
    New State S_{n+1} = Q * S_n
    """
    
    # The Fibonacci Q-Matrix
    Q_matrix = np.array([[1, 1], [1, 0]])
    
    # Initial State Vector S_0. We use F_1 and F_0 for the simplest start.
    # The state vector can represent any two sequential, growing metrics of the chain.
    # Let's use [Total Stake, Active Validators] for a more conceptual example.
    initial_stake = fibonacci(20) # F_20
    initial_validators = fibonacci(17) # F_17
    
    # We will use a simpler state vector [F_n, F_{n-1}] to demonstrate the matrix property.
    # Let S_0 = [F_2, F_1] = [1, 1]
    current_state = np.array([fibonacci(2), fibonacci(1)])
    
    print("\n--- State Transition Simulation (The Fibonacci Matrix) ---")
    print("The core state transition is governed by the Q-Matrix: [[1, 1], [1, 0]]")
    print(f"Initial State Vector S_0 (e.g., [F_2, F_1]): {current_state}")
    
    for i in range(1, steps + 1):
        # S_i = Q * S_{i-1}
        next_state = Q_matrix @ current_state
        
        # The resulting vector should be [F_{i+2}, F_{i+1}]
        print(f"State S_{i} (after {i} step{'s' if i > 1 else ''}): {next_state}")
        
        # Check against actual Fibonacci numbers for verification
        expected_state = np.array([fibonacci(i + 2), fibonacci(i + 1)])
        if not np.array_equal(next_state, expected_state):
            print(f"ERROR: Expected {expected_state}, got {next_state}")
            
        current_state = next_state

# --- Main Execution ---

if __name__ == "__main__":
    derive_parameters()
    simulate_state_transition(steps=8) # Demonstrate up to F_10
