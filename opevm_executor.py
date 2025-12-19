"""
opevm_executor.py - Optimistic Parallelized EVM (OPEVM) Executor
This module simulates the OPEVM's core logic: parallel execution and the
three-stage conflict detection system.
"""

from typing import List, Dict, Set, Tuple
from phi_chain_core import PhiTransaction

class OPEVMExecutor:
    """
    Simulates the Optimistic Parallelized EVM (OPEVM) execution environment.
    """
    def __init__(self, state: Dict[str, int]):
        # The global state, mapping storage slots (keys) to values
        self.state = state
        # A simple counter for simulation purposes
        self.execution_count = 0

    def _simulate_execution(self, tx: PhiTransaction, local_state: Dict[str, int]) -> Tuple[Dict[str, int], Set[str], Set[str]]:
        """
        Simulates the execution of a single transaction.
        In a real EVM, this would involve running bytecode.
        Here, we simulate state changes based on the estimated sets.
        Returns: (new_state_changes, actual_reads, actual_writes)
        """
        self.execution_count += 1
        
        # In a real scenario, the actual read/write sets are determined during execution.
        # For this simulation, we'll use the estimated sets as the actual sets.
        actual_reads = set(tx.estimated_read_set)
        actual_writes = set(tx.estimated_write_set)
        
        # Simulate a state change: e.g., transfer value
        state_changes = {}
        
        # Simple simulation logic: if the transaction is from Alice, simulate a transfer
        if tx.sender == "0xAlice":
            sender_key = "0xAlice_balance"
            recipient_key = f"0x{tx.recipient.split('x')[-1]}_balance" # Simple way to get a key like 0xBob_balance
            
            # Only update sender's balance if it's in the write set
            if sender_key in actual_writes:
                state_changes[sender_key] = local_state.get(sender_key, 0) - tx.value
            
            # Only update recipient's balance if it's in the write set
            if recipient_key in actual_writes:
                state_changes[recipient_key] = local_state.get(recipient_key, 0) + tx.value
                
        return state_changes, actual_reads, actual_writes

    def execute_block(self, transactions: List[PhiTransaction]) -> Tuple[Dict[str, int], List[int]]:
        """
        Executes a list of transactions using the OPEVM's three-stage process.
        Returns the final state and a list of re-executed transaction indices.
        """
        print(f"\n--- OPEVM Execution of {len(transactions)} Transactions ---")
        
        # --- Stage 1: Pre-Execution Static Analysis (Scheduling) ---
        # In a real system, this would group transactions for parallel threads.
        # For simulation, we just collect the estimated sets.
        print("Stage 1: Pre-Execution Static Analysis (Simulated Parallel Scheduling)")
        
        # --- Stage 2: Optimistic Parallel Execution & Dynamic Monitoring ---
        
        # We use a list to store the results of the optimistic execution
        optimistic_results = []
        
        # Keep track of state slots written to by *already committed* transactions
        committed_writes: Set[str] = set()
        
        # Keep track of transactions that need re-execution
        conflicting_tx_indices: List[int] = []
        
        # Simulate parallel execution by iterating and checking for conflicts
        for i, tx in enumerate(transactions):
            # Simulate a local copy of the state for the parallel thread
            local_state = self.state.copy()
            
            # Simulate execution
            state_changes, actual_reads, actual_writes = self._simulate_execution(tx, local_state)
            
            # --- Conflict Check (Dynamic Monitoring) ---
            # Conflict occurs if the transaction reads a slot that was written by a committed tx,
            # OR if the transaction writes to a slot that was written by a committed tx.
            read_conflict = not actual_reads.isdisjoint(committed_writes)
            write_conflict = not actual_writes.isdisjoint(committed_writes)
            
            if read_conflict or write_conflict:
                print(f"  [Conflict Detected] Tx {i} conflicts with committed writes. Flagged for re-execution.")
                conflicting_tx_indices.append(i)
                # Do NOT commit the writes of this transaction yet
                optimistic_results.append(None)
            else:
                # No conflict, optimistically commit the writes
                committed_writes.update(actual_writes)
                optimistic_results.append((state_changes, actual_reads, actual_writes))
                print(f"  [Optimistic Commit] Tx {i} executed successfully. Writes: {actual_writes}")

        # --- Stage 3: Post-Execution Global Verification (Re-execution) ---
        
        final_state = self.state.copy()
        re_executed_indices = []
        
        # Apply non-conflicting results first
        for i, result in enumerate(optimistic_results):
            if result is not None:
                state_changes, _, _ = result
                final_state.update(state_changes)
        
        # Re-execute conflicting transactions sequentially in canonical order
        if conflicting_tx_indices:
            print(f"\nStage 3: Post-Execution Global Verification (Re-executing {len(conflicting_tx_indices)} transactions)")
            for i in conflicting_tx_indices:
                tx = transactions[i]
                # Re-execute against the current final state (which includes all prior successful txs)
                state_changes, _, _ = self._simulate_execution(tx, final_state)
                final_state.update(state_changes)
                re_executed_indices.append(i)
                print(f"  [Re-executed] Tx {i} applied sequentially.")

        # Update the executor's state
        self.state = final_state
        print(f"\nExecution Complete. Total executions (including re-executions): {self.execution_count}")
        return self.state, re_executed_indices

# --- Conceptual Usage Example ---

if __name__ == "__main__":
    # Initial State
    initial_state = {
        "0xAlice_balance": 1000,
        "0xBob_balance": 500,
        "0xContract_A_data": 10,
        "0xContract_B_data": 20,
    }
    
    executor = OPEVMExecutor(initial_state)
    
    # Define transactions
    # Tx 0: Alice -> Bob (Non-conflicting with Tx 1)
    tx0 = PhiTransaction("0xAlice", "0xBob", 100, b"", 1, 21000, b"sig0",
                         estimated_read_set=["0xAlice_balance", "0xBob_balance"],
                         estimated_write_set=["0xAlice_balance", "0xBob_balance"])
    
    # Tx 1: Contract A update (Non-conflicting with Tx 0)
    tx1 = PhiTransaction("0xUser", "0xContractA", 0, b"call_update", 1, 50000, b"sig1",
                         estimated_read_set=["0xContract_A_data"],
                         estimated_write_set=["0xContract_A_data"])

    # Tx 2: Alice -> Charlie (Conflicting with Tx 0 on Alice's balance)
    tx2 = PhiTransaction("0xAlice", "0xCharlie", 50, b"", 2, 21000, b"sig2",
                         estimated_read_set=["0xAlice_balance"],
                         estimated_write_set=["0xAlice_balance"])
    
    transactions = [tx0, tx1, tx2]
    
    final_state, re_executed = executor.execute_block(transactions)
    
    print("\n--- Final State ---")
    print(final_state)
    print(f"Re-executed Transactions (Indices): {re_executed}")
    
    # Expected Result:
    # Tx 0: Alice: 1000 -> 900, Bob: 500 -> 600
    # Tx 1: Contract A: 10 -> (simulated change)
    # Tx 2: Conflicts with Tx 0 on Alice's balance. Re-executed sequentially.
    #       Alice's balance after Tx 0 is 900. Tx 2 changes it to 900 - 50 = 850.
    # Final Alice Balance: 850
    # Final Bob Balance: 600
    
    # The simulation should show that Tx 2 is flagged for re-execution.
