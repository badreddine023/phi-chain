import hashlib
import json
from math_primitives import fibonacci_sequence, PHI, PHI_INV
import decimal
from decimal import Decimal

# Use the same precision as math_primitives
decimal.getcontext().prec = 50

# --- MANUS Prototype: Phi-Merkle Tree and EDO ---

class EntangledDataObject:
    """
    Represents an Entangled Data Object (EDO) that unifies digital and physical state.
    The coherence hash enforces the Quantum-Classical Bridge.
    """
    def __init__(self, digital_state, physical_state):
        self.digital_state = digital_state
        self.physical_state = physical_state
        self.coherence_hash = self._calculate_coherence_hash()

    def _calculate_coherence_hash(self):
        """
        Calculates a hash that is only valid if the ratio of digital to physical
        entropy approaches PHI or PHI_INV.
        
        For this prototype, we simplify 'entropy' to the length of the JSON string.
        """
        digital_str = json.dumps(self.digital_state, sort_keys=True)
        physical_str = json.dumps(self.physical_state, sort_keys=True)
        
        # Simplified 'entropy' as length
        digital_entropy = Decimal(len(digital_str))
        physical_entropy = Decimal(len(physical_str))
        
        if physical_entropy == 0:
            # Avoid division by zero, treat as non-coherent
            ratio = Decimal(0)
        else:
            ratio = digital_entropy / physical_entropy
        
        # Check for phi-coherence (within a small tolerance for the prototype)
        tolerance = Decimal("0.01")
        is_phi_coherent = (abs(ratio - PHI) < tolerance) or (abs(ratio - PHI_INV) < tolerance)
        
        # Combine states and coherence flag for the final hash
        combined_data = digital_str + physical_str + str(is_phi_coherent)
        return hashlib.sha256(combined_data.encode('utf-8')).hexdigest()

    def is_coherent(self):
        """Checks if the EDO is phi-coherent based on its internal hash calculation."""
        # Recalculate the hash and compare to the stored one
        return self.coherence_hash == self._calculate_coherence_hash()

    def get_leaf_data(self):
        """Returns the data used as a leaf in the Phi-Merkle Tree."""
        return self.coherence_hash

class PhiMerkleTree:
    """
    A Merkle Tree with a dynamic branching factor chosen from the Fibonacci sequence.
    """
    def __init__(self, leaves):
        self.leaves = [l.get_leaf_data() for l in leaves]
        self.root = self._build_tree(self.leaves)

    def _hash(self, data):
        """Simple SHA256 hash function."""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _get_fibonacci_branching_factor(self, num_nodes):
        """
        Selects the largest Fibonacci number <= num_nodes as the branching factor.
        This is a simplification of the dynamic scaling.
        """
        fibs = fibonacci_sequence(10) # F_0 to F_9
        fibs = [f for f in fibs if f >= 2] # Branching factor must be >= 2
        
        best_factor = 2
        for f in sorted(fibs, reverse=True):
            if num_nodes >= f:
                best_factor = f
                break
        return best_factor

    def _build_tree(self, nodes):
        if len(nodes) == 1:
            return nodes[0]

        branching_factor = self._get_fibonacci_branching_factor(len(nodes))
        
        next_level = []
        i = 0
        while i < len(nodes):
            # Group nodes by the branching factor
            group = nodes[i:i + branching_factor]
            
            # Pad the last group with the last element if necessary (simplified padding)
            while len(group) < branching_factor and len(group) > 0:
                group.append(group[-1])
            
            if group:
                # Concatenate and hash the group
                combined_hash = self._hash("".join(group))
                next_level.append(combined_hash)
            
            i += branching_factor
            
        return self._build_tree(next_level)

# --- Prototype Execution ---
if __name__ == "__main__":
    print("--- MANUS Prototype: EDO and Phi-Merkle Tree ---")
    
    # 1. Create EDOs
    # EDO 1: Coherent (Ratio close to PHI)
    digital_1 = {"url": "https://phi.chain", "content": "A" * 162} # Length 162
    physical_1 = {"coord": "1.618", "sensor": "B" * 100} # Length 100
    # Ratio is 162/100 = 1.62, which is close to PHI (1.618...)
    edo1 = EntangledDataObject(digital_1, physical_1)
    
    # EDO 2: Non-Coherent (Arbitrary ratio)
    digital_2 = {"url": "https://flat.torus", "content": "C" * 50} # Length 50
    physical_2 = {"coord": "9.6.3", "sensor": "D" * 100} # Length 100
    # Ratio is 50/100 = 0.5, which is not close to PHI or PHI_INV
    edo2 = EntangledDataObject(digital_2, physical_2)
    
    # EDO 3: Coherent (Ratio close to PHI_INV)
    digital_3 = {"url": "https://quantum.bridge", "content": "E" * 62} # Length 62
    physical_3 = {"coord": "2.618", "sensor": "F" * 100} # Length 100
    # Ratio is 62/100 = 0.62, which is close to PHI_INV (0.618...)
    edo3 = EntangledDataObject(digital_3, physical_3)
    
    edos = [edo1, edo2, edo3]
    
    print(f"EDO 1 Coherent: {edo1.is_coherent()} (Ratio: {Decimal(len(json.dumps(digital_1, sort_keys=True))) / Decimal(len(json.dumps(physical_1, sort_keys=True))):.3f})")
    print(f"EDO 2 Coherent: {edo2.is_coherent()} (Ratio: {Decimal(len(json.dumps(digital_2, sort_keys=True))) / Decimal(len(json.dumps(physical_2, sort_keys=True))):.3f})")
    print(f"EDO 3 Coherent: {edo3.is_coherent()} (Ratio: {Decimal(len(json.dumps(digital_3, sort_keys=True))) / Decimal(len(json.dumps(physical_3, sort_keys=True))):.3f})")
    
    # 2. Build Phi-Merkle Tree
    # 3 leaves. Largest Fibonacci number <= 3 is 3 (F4). Branching factor will be 3.
    tree = PhiMerkleTree(edos)
    
    print("-" * 35)
    print(f"Phi-Merkle Tree Leaves: {[e.get_leaf_data()[:8] + '...' for e in edos]}")
    print(f"Phi-Merkle Tree Root: {tree.root}")
    print(f"Expected Branching Factor for 3 leaves: 3 (F4)")
