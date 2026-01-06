"""
Phi-Performance-Analyzer: أداة تحليل الأداء لمشروع Phi-Chain
تقوم هذه الأداة بقياس عدد المعاملات في الثانية (TPS) وزمن الاستجابة (Latency).
"""

import time
import statistics

class PhiPerformanceAnalyzer:
    def __init__(self):
        self.latencies = []
        self.total_transactions = 0

    def simulate_load(self, tx_count=100):
        print(f"📊 بدء تحليل الأداء لـ {tx_count} معاملة...")
        start_time = time.time()
        
        for i in range(tx_count):
            tx_start = time.time()
            # محاكاة معالجة المعاملة
            time.sleep(0.01) # 10ms processing time
            tx_end = time.time()
            
            self.latencies.append((tx_end - tx_start) * 1000)
            self.total_transactions += 1
            
        end_time = time.time()
        total_duration = end_time - start_time
        
        self.report(total_duration)

    def report(self, duration):
        tps = self.total_transactions / duration
        avg_latency = statistics.mean(self.latencies)
        p95_latency = statistics.quantiles(self.latencies, n=20)[18] # 95th percentile

        print("\n" + "="*40)
        print("📈 تقرير أداء Phi-Chain")
        print("="*40)
        print(f"إجمالي المعاملات: {self.total_transactions}")
        print(f"الوقت المستغرق: {duration:.2f} ثانية")
        print(f"المعاملات في الثانية (TPS): {tps:.2f}")
        print(f"متوسط زمن الاستجابة: {avg_latency:.2f} ms")
        print(f"زمن الاستجابة (P95): {p95_latency:.2f} ms")
        print("="*40)

if __name__ == "__main__":
    analyzer = PhiPerformanceAnalyzer()
    analyzer.simulate_load(200)
