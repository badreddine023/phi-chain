"""
Phi-Network-Monitor: أداة مراقبة الشبكة لمشروع Phi-Chain
تقوم هذه الأداة بمراقبة حالة العقد (Nodes)، سرعة إنتاج الكتل، وحالة الإجماع.
"""

import time
import json
import random
from datetime import datetime

class PhiNetworkMonitor:
    def __init__(self, nodes_count=7):
        self.nodes_count = nodes_count
        self.start_time = datetime.now()
        self.blocks_produced = 0

    def get_network_status(self):
        """محاكاة الحصول على حالة الشبكة"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "uptime": str(datetime.now() - self.start_time),
            "active_nodes": random.randint(nodes_count-1, nodes_count),
            "total_nodes": self.nodes_count,
            "avg_block_time": f"{random.uniform(1.5, 1.7):.2f}s",
            "consensus_health": "Optimal (Φ-Coherent)"
        }
        return status

    def run_monitor(self, duration_seconds=10):
        print(f"🚀 بدء مراقبة شبكة Phi-Chain (المدة: {duration_seconds} ثوانٍ)...")
        print("-" * 50)
        
        elapsed = 0
        while elapsed < duration_seconds:
            status = self.get_network_status()
            print(f"[{status['timestamp']}] عقد نشطة: {status['active_nodes']}/{status['total_nodes']} | "
                  f"زمن الكتلة: {status['avg_block_time']} | الحالة: {status['consensus_health']}")
            time.sleep(2)
            elapsed += 2
            
        print("-" * 50)
        print("✅ انتهت جلسة المراقبة.")

if __name__ == "__main__":
    nodes_count = 7 # القيمة الافتراضية لـ F_4 في فيبوناتشي
    monitor = PhiNetworkMonitor(nodes_count)
    monitor.run_monitor()
