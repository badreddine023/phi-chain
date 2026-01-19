# Φ-Chain Mainnet Deployment Guide

**Version:** 1.0  
**Date:** January 19, 2026  
**Status:** Production Ready  
**Optimization Level:** 25-40% Performance Improvement

---

## Executive Summary

This comprehensive guide provides step-by-step procedures for deploying the optimized Φ-Chain to mainnet. The deployment incorporates performance optimizations, monitoring infrastructure, and rollback capabilities to ensure a smooth and reliable production launch.

**Key Deployment Features:**
- Zero-downtime deployment strategy
- Automated health checks and monitoring
- Performance baseline validation
- Comprehensive rollback procedures
- Real-time metrics collection

---

## Pre-Deployment Requirements

### Infrastructure Requirements

**Minimum Specifications:**
- **CPU:** 8+ cores (Intel/AMD x86-64)
- **RAM:** 32 GB minimum (64 GB recommended)
- **Storage:** 500 GB SSD (NVMe preferred)
- **Network:** 1 Gbps minimum bandwidth
- **Redundancy:** Multi-region deployment capability

**Recommended Infrastructure:**
- **CPU:** 16+ cores with high clock speed
- **RAM:** 64+ GB for optimal cache performance
- **Storage:** 1+ TB NVMe SSD
- **Network:** 10 Gbps or higher
- **Backup:** Automated daily snapshots

### Software Requirements

```bash
# Python environment
Python 3.9+
pip3 (latest)

# System packages
git
curl
wget
systemd (for service management)

# Development tools
gcc/clang (for compilation)
make
```

### Pre-Deployment Validation

**1. Code Verification**
```bash
# Verify commit hash
git log --oneline -1
# Expected: 9995ff29 ⚡ Performance Optimization: 25-40% System Improvement

# Verify file integrity
sha256sum core/blockchain.py crypto/hash.py
```

**2. Test Suite Execution**
```bash
# Run comprehensive tests
python -m pytest tests/test_optimizations.py -v

# Expected result: All 25+ tests passing
```

**3. Performance Baseline**
```bash
# Establish baseline metrics
python scripts/benchmark_baseline.py

# Document results for comparison
```

---

## Deployment Phases

### Phase 1: Pre-Deployment (Days 1-2)

#### 1.1 Environment Preparation

**Step 1: Provision Infrastructure**
```bash
# Create production environment
mkdir -p /opt/phi-chain/{mainnet,data,logs,backups}
chmod 755 /opt/phi-chain

# Create system user
useradd -r -s /bin/bash phi-chain
chown -R phi-chain:phi-chain /opt/phi-chain
```

**Step 2: Deploy Code**
```bash
# Clone optimized repository
cd /opt/phi-chain/mainnet
git clone https://github.com/badreddine023/phi-chain.git .
git checkout main

# Verify deployment
git log --oneline -1
```

**Step 3: Install Dependencies**
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Verify installation
python3 -c "import phi_chain_core; print('✅ Dependencies OK')"
```

#### 1.2 Configuration Setup

**Step 1: Create Configuration File**
```bash
# Create mainnet config
cat > /opt/phi-chain/mainnet/config.mainnet.yaml << 'EOF'
# Φ-Chain Mainnet Configuration
network:
  name: "phi-chain-mainnet"
  version: "1.0.0"
  environment: "production"

blockchain:
  genesis_timestamp: 1705689600
  difficulty: 4
  block_time: 8  # seconds (Fibonacci F_6)

performance:
  balance_cache_enabled: true
  incremental_validation_enabled: true
  fibonacci_cache_enabled: true
  hash_cache_size: 1024

monitoring:
  metrics_enabled: true
  logging_level: "INFO"
  performance_tracking: true

security:
  require_ssl: true
  certificate_path: "/opt/phi-chain/mainnet/certs/mainnet.crt"
  key_path: "/opt/phi-chain/mainnet/certs/mainnet.key"
EOF
```

**Step 2: Initialize Database**
```bash
# Create database directory
mkdir -p /opt/phi-chain/data/mainnet
chown phi-chain:phi-chain /opt/phi-chain/data/mainnet

# Initialize blockchain
python3 -c "
from core.blockchain_optimized import BlockchainOptimized
bc = BlockchainOptimized()
print(f'✅ Genesis block created: {bc.get_latest_block().hash}')
"
```

#### 1.3 Monitoring Setup

**Step 1: Install Monitoring Stack**
```bash
# Install Prometheus
apt-get install -y prometheus

# Install Grafana
apt-get install -y grafana-server

# Start services
systemctl start prometheus
systemctl start grafana-server
systemctl enable prometheus grafana-server
```

**Step 2: Configure Metrics Collection**
```bash
# Create Prometheus config
cat > /etc/prometheus/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'phi-chain'
    static_configs:
      - targets: ['localhost:9090']
    metrics_path: '/metrics'
EOF

# Restart Prometheus
systemctl restart prometheus
```

### Phase 2: Staging Deployment (Days 3-4)

#### 2.1 Staging Environment

**Step 1: Deploy to Staging**
```bash
# Create staging environment
mkdir -p /opt/phi-chain/staging
cd /opt/phi-chain/staging
git clone https://github.com/badreddine023/phi-chain.git .
git checkout main

# Run full test suite
python -m pytest tests/ -v --tb=short
```

**Step 2: Performance Testing**
```bash
# Run performance benchmarks
python scripts/benchmark_staging.py

# Compare with baseline
python scripts/compare_benchmarks.py baseline staging

# Expected: 25-40% improvement confirmed
```

**Step 3: Load Testing**
```bash
# Simulate production load
python scripts/load_test.py \
  --transactions-per-second 100 \
  --duration 3600 \
  --concurrent-connections 50

# Monitor resource usage
# Expected: CPU <80%, Memory <60%, Disk I/O <70%
```

#### 2.2 Security Validation

**Step 1: Security Audit**
```bash
# Run security checks
python -m bandit -r core/ crypto/ network/

# Expected: No critical vulnerabilities
```

**Step 2: Dependency Audit**
```bash
# Check for vulnerable dependencies
pip3 install safety
safety check

# Expected: No high-risk vulnerabilities
```

### Phase 3: Mainnet Deployment (Days 5-6)

#### 3.1 Pre-Launch Checklist

**Verification Steps:**
- [ ] Code commit verified (9995ff29)
- [ ] All tests passing (25+ tests)
- [ ] Performance baseline established
- [ ] Staging deployment successful
- [ ] Load testing completed successfully
- [ ] Security audit passed
- [ ] Monitoring infrastructure ready
- [ ] Backup procedures tested
- [ ] Rollback procedures documented
- [ ] Team trained on procedures
- [ ] Communication channels established
- [ ] Incident response plan ready

#### 3.2 Deployment Execution

**Step 1: Final Verification**
```bash
# Verify code integrity
git verify-commit HEAD

# Verify all systems operational
python scripts/pre_deployment_check.py

# Expected output:
# ✅ Code integrity: VERIFIED
# ✅ Tests: ALL PASSING
# ✅ Monitoring: OPERATIONAL
# ✅ Backups: CONFIGURED
```

**Step 2: Deploy to Mainnet**
```bash
# Create deployment snapshot
tar -czf /opt/phi-chain/backups/mainnet_$(date +%Y%m%d_%H%M%S).tar.gz \
  /opt/phi-chain/mainnet

# Deploy code
cd /opt/phi-chain/mainnet
git pull origin main

# Verify deployment
git log --oneline -1
```

**Step 3: Start Services**
```bash
# Create systemd service
cat > /etc/systemd/system/phi-chain-mainnet.service << 'EOF'
[Unit]
Description=Φ-Chain Mainnet Node
After=network.target

[Service]
Type=simple
User=phi-chain
WorkingDirectory=/opt/phi-chain/mainnet
ExecStart=/usr/bin/python3 -m phi_chain_core.mainnet
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl daemon-reload
systemctl enable phi-chain-mainnet
systemctl start phi-chain-mainnet

# Verify service
systemctl status phi-chain-mainnet
```

**Step 4: Health Checks**
```bash
# Monitor initial startup
tail -f /opt/phi-chain/logs/mainnet.log

# Verify blockchain synchronization
curl http://localhost:8000/api/status

# Expected response:
# {
#   "status": "running",
#   "blocks": 1,
#   "peers": 0,
#   "performance": "optimized"
# }
```

### Phase 4: Post-Deployment (Days 7+)

#### 4.1 Monitoring & Validation

**Step 1: Performance Monitoring**
```bash
# Access Grafana dashboard
# URL: http://localhost:3000
# Default credentials: admin/admin

# Key metrics to monitor:
# - Block validation time
# - Balance cache hit rate
# - Transaction throughput
# - Memory usage
# - CPU utilization
```

**Step 2: Performance Verification**
```bash
# Collect production metrics
python scripts/collect_metrics.py --duration 24h

# Verify optimization benefits
python scripts/verify_optimizations.py

# Expected:
# - Balance cache hit rate: >80%
# - Validation time: <15ms per block
# - Transaction throughput: >1000 TPS
```

**Step 3: Continuous Monitoring**
```bash
# Set up automated alerts
# Alert on:
# - CPU usage >85%
# - Memory usage >75%
# - Disk usage >80%
# - Block validation time >50ms
# - Transaction failures >1%
```

---

## Deployment Scripts

### Script 1: Pre-Deployment Check

```python
#!/usr/bin/env python3
"""
pre_deployment_check.py: Comprehensive pre-deployment validation
"""

import subprocess
import sys
from pathlib import Path

def check_code_integrity():
    """Verify code integrity and commit hash."""
    result = subprocess.run(
        ['git', 'log', '--oneline', '-1'],
        capture_output=True,
        text=True
    )
    commit = result.stdout.strip()
    expected = '9995ff29'
    
    if expected in commit:
        print(f"✅ Code integrity: VERIFIED ({commit})")
        return True
    else:
        print(f"❌ Code integrity: FAILED (expected {expected}, got {commit})")
        return False

def check_tests():
    """Run test suite."""
    result = subprocess.run(
        ['python', '-m', 'pytest', 'tests/test_optimizations.py', '-v'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Tests: ALL PASSING")
        return True
    else:
        print("❌ Tests: FAILED")
        print(result.stdout)
        return False

def check_dependencies():
    """Verify all dependencies installed."""
    try:
        import phi_chain_core
        from core.blockchain_optimized import BlockchainOptimized
        from crypto.hash_optimized import PhiHashOptimized
        print("✅ Dependencies: INSTALLED")
        return True
    except ImportError as e:
        print(f"❌ Dependencies: MISSING ({e})")
        return False

def main():
    """Run all pre-deployment checks."""
    print("🔍 Running Pre-Deployment Checks...\n")
    
    checks = [
        ("Code Integrity", check_code_integrity),
        ("Test Suite", check_tests),
        ("Dependencies", check_dependencies),
    ]
    
    results = []
    for name, check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ {name}: ERROR ({e})")
            results.append(False)
    
    print("\n" + "="*50)
    if all(results):
        print("✅ ALL CHECKS PASSED - READY FOR DEPLOYMENT")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - DO NOT DEPLOY")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

### Script 2: Performance Monitoring

```python
#!/usr/bin/env python3
"""
monitor_performance.py: Real-time performance monitoring
"""

import time
import psutil
from core.blockchain_optimized import BlockchainOptimized
from crypto.hash_optimized import PhiHashOptimized, FibonacciCache

class PerformanceMonitor:
    """Monitor system and application performance."""
    
    def __init__(self):
        self.blockchain = BlockchainOptimized()
        self.start_time = time.time()
    
    def get_system_metrics(self):
        """Collect system metrics."""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "uptime": time.time() - self.start_time
        }
    
    def get_blockchain_metrics(self):
        """Collect blockchain metrics."""
        stats = self.blockchain.get_cache_stats()
        cache_info = FibonacciCache.get_cache_info()
        
        return {
            "chain_length": self.blockchain.get_chain_length(),
            "balance_cache_size": len(self.blockchain._balance_cache),
            "hash_cache_hits": stats['hits'],
            "hash_cache_misses": stats['misses'],
            "fibonacci_cache_hits": cache_info['hits'],
            "fibonacci_cache_misses": cache_info['misses']
        }
    
    def print_metrics(self):
        """Print formatted metrics."""
        system = self.get_system_metrics()
        blockchain = self.get_blockchain_metrics()
        
        print("\n" + "="*60)
        print("SYSTEM METRICS")
        print("="*60)
        print(f"CPU Usage:      {system['cpu_percent']:.1f}%")
        print(f"Memory Usage:   {system['memory_percent']:.1f}%")
        print(f"Disk Usage:     {system['disk_percent']:.1f}%")
        print(f"Uptime:         {system['uptime']:.0f}s")
        
        print("\n" + "="*60)
        print("BLOCKCHAIN METRICS")
        print("="*60)
        print(f"Chain Length:   {blockchain['chain_length']}")
        print(f"Balance Cache:  {blockchain['balance_cache_size']} addresses")
        print(f"Hash Cache:     {blockchain['hash_cache_hits']} hits, {blockchain['hash_cache_misses']} misses")
        print(f"Fibonacci Cache: {blockchain['fibonacci_cache_hits']} hits, {blockchain['fibonacci_cache_misses']} misses")

def main():
    """Run continuous monitoring."""
    monitor = PerformanceMonitor()
    
    try:
        while True:
            monitor.print_metrics()
            time.sleep(60)  # Update every 60 seconds
    except KeyboardInterrupt:
        print("\n✅ Monitoring stopped")

if __name__ == '__main__':
    main()
```

---

## Rollback Procedures

### Emergency Rollback

**If Critical Issues Occur:**

```bash
# 1. Stop current service
systemctl stop phi-chain-mainnet

# 2. Restore from backup
tar -xzf /opt/phi-chain/backups/mainnet_YYYYMMDD_HHMMSS.tar.gz \
  -C /opt/phi-chain

# 3. Revert to previous commit
cd /opt/phi-chain/mainnet
git reset --hard HEAD~1

# 4. Restart service
systemctl start phi-chain-mainnet

# 5. Verify rollback
systemctl status phi-chain-mainnet
curl http://localhost:8000/api/status
```

### Gradual Rollback

**For Non-Critical Issues:**

```bash
# 1. Deploy previous version to staging
cd /opt/phi-chain/staging
git checkout HEAD~1

# 2. Run tests
python -m pytest tests/ -v

# 3. If successful, promote to mainnet
cd /opt/phi-chain/mainnet
git checkout HEAD~1
systemctl restart phi-chain-mainnet
```

---

## Performance Targets

### Expected Performance Metrics

| Metric | Target | Threshold |
| :--- | :--- | :--- |
| Block Validation Time | <15ms | <50ms |
| Transaction Throughput | >1000 TPS | >500 TPS |
| Balance Cache Hit Rate | >80% | >50% |
| CPU Usage | <50% | <80% |
| Memory Usage | <40% | <75% |
| Disk I/O | <30% | <70% |

### Alert Thresholds

**Critical Alerts (Immediate Action Required):**
- Block validation time >100ms
- Transaction failures >5%
- CPU usage >90%
- Memory usage >85%
- Disk usage >90%

**Warning Alerts (Monitor Closely):**
- Block validation time >50ms
- Transaction failures >1%
- CPU usage >80%
- Memory usage >75%
- Disk usage >80%

---

## Maintenance Schedule

### Daily Tasks
- Monitor system metrics
- Check error logs
- Verify blockchain synchronization
- Backup critical data

### Weekly Tasks
- Performance analysis
- Security updates
- Dependency updates
- Capacity planning review

### Monthly Tasks
- Full system audit
- Disaster recovery test
- Performance optimization review
- Documentation updates

---

## Support & Escalation

### Support Channels
- **Critical Issues:** Immediate escalation to DevOps
- **Performance Issues:** Engineering team review
- **Security Issues:** Security team notification
- **General Questions:** Documentation review

### Escalation Procedure
1. Document issue with timestamp and details
2. Contact on-call engineer
3. Escalate to team lead if unresolved in 30 minutes
4. Escalate to management if unresolved in 2 hours

---

## Conclusion

This comprehensive deployment guide ensures a smooth, reliable, and well-monitored launch of the optimized Φ-Chain to mainnet. Following these procedures will maximize the benefits of the performance optimizations while maintaining system stability and reliability.

**Status:** ✅ Ready for Production Deployment

---

**Document Version:** 1.0  
**Last Updated:** January 19, 2026  
**Next Review:** February 19, 2026
