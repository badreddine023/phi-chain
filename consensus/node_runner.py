import time
import json
import sys
import os

# Add parent directory to path to import core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from phi_chain_core import PhiState, FibonacciUtils

class ValidatorNode:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.state = PhiState()
        self.is_running = False
        self.blocks_processed = 0

    def start(self):
        print(f"Node {self.config['validator_id']} starting on port {self.config['port']}...")
        self.is_running = True
        try:
            while self.is_running:
                # Simulate block processing and state evolution
                self.state.evolve()
                self.blocks_processed += 1
                metrics = self.state.get_current_metrics()
                print(f"[{self.config['validator_id']}] Processed block {self.blocks_processed}. State: {metrics}")
                time.sleep(FibonacciUtils.fibonacci(6)) # F_6 = 8 seconds slot time
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print(f"Node {self.config['validator_id']} stopping...")
        self.is_running = False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 node_runner.py <config_path>")
        sys.exit(1)
    node = ValidatorNode(sys.argv[1])
    node.start()
