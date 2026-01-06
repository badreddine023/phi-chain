import time
import logging
import psutil
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PhiMonitoring")

class PhiMonitoringSystem:
    """
    Monitors the health and performance of a Phi-Chain node.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id

    def get_system_metrics(self) -> Dict[str, Any]:
        """Collect system-level metrics."""
        metrics = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "timestamp": time.time()
        }
        return metrics

    def get_node_metrics(self, blockchain: Any) -> Dict[str, Any]:
        """Collect blockchain-specific metrics."""
        metrics = {
            "chain_length": blockchain.get_chain_length(),
            "pending_transactions": len(blockchain.pending_transactions),
            "is_valid": blockchain.is_chain_valid()
        }
        return metrics

    def run_forever(self, blockchain: Any):
        """Periodically log metrics."""
        while True:
            sys_metrics = self.get_system_metrics()
            node_metrics = self.get_node_metrics(blockchain)
            
            logger.info(f"Node {self.node_id} Metrics: SYS={sys_metrics}, NODE={node_metrics}")
            
            # In a real system, push these to Prometheus or Grafana
            time.sleep(30)

if __name__ == "__main__":
    from core.blockchain import Blockchain
    blockchain = Blockchain()
    monitor = PhiMonitoringSystem("node_001")
    # monitor.run_forever(blockchain) # Uncomment to run
    print(monitor.get_system_metrics())
