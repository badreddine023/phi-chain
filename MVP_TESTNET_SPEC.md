# Φ-Chain MVP Testnet Specification

## 🎯 MVP Goals

### Primary Objectives
1. **Demonstrate Fibonacci Byzantine Agreement (FBA)** in a live network
2. **Validate mathematical consensus** with real validators
3. **Prove reversible transaction capability** 
4. **Establish baseline performance metrics**
5. **Enable developer experimentation**

### Success Criteria
- ✅ 21 validators running FBA consensus (F_8)
- ✅ 8-second block times (F_6) with <1% variance
- ✅ 610 signature finality threshold (F_15)
- ✅ Reversible transaction demonstration
- ✅ 100+ TPS sustained throughput
- ✅ 99.9% uptime over 30 days

## 🏗️ Technical Architecture

### Core Components

#### 1. Φ-Node (Rust Implementation)
```rust
// Core node structure
struct PhiNode {
    consensus: FibonacciByzantineAgreement,
    storage: PhiStorage,
    network: P2PNetwork,
    rpc: JsonRpcServer,
    metrics: PrometheusMetrics,
}

// Fibonacci parameters
const BLOCK_TIME: Duration = Duration::from_millis(8000); // F_6 seconds
const VALIDATOR_COUNT: usize = 21; // F_8
const FINALITY_THRESHOLD: usize = 610; // F_15
const COMMITTEE_SIZE: usize = 377; // F_14
```

#### 2. Consensus Engine
```rust
// FBA consensus implementation
struct FibonacciByzantineAgreement {
    validators: ValidatorSet,
    current_epoch: u64,
    phi_ratio: f64, // 1.618033988749895
    signature_aggregator: BlsAggregator,
}

impl Consensus for FibonacciByzantineAgreement {
    fn propose_block(&self) -> Result<Block, ConsensusError>;
    fn validate_block(&self, block: &Block) -> Result<bool, ConsensusError>;
    fn finalize_block(&self, signatures: &[Signature]) -> Result<(), ConsensusError>;
}
```

#### 3. Reversible Core
```rust
// Temporal symmetry implementation
struct ReversibleCore {
    q_matrix: [[i64; 2]; 2], // [[1,1],[1,0]]
    state_history: Vec<BlockState>,
    fibonacci_cache: HashMap<i32, i64>,
}

impl ReversibleCore {
    fn forward_transition(&mut self, state: BlockState) -> BlockState;
    fn backward_transition(&mut self, state: BlockState) -> BlockState;
    fn verify_temporal_symmetry(&self) -> bool;
}
```

### Network Layer

#### P2P Protocol
- **Transport:** libp2p with custom Φ-routing
- **Discovery:** Kademlia DHT with Fibonacci node IDs
- **Gossip:** Efficient block/transaction propagation
- **Sync:** Fast sync with φ-optimized checkpoints

#### API Endpoints
```typescript
// JSON-RPC API
interface PhiChainAPI {
  // Block operations
  getBlock(hash: string): Promise<Block>;
  getBlockByNumber(number: number): Promise<Block>;
  
  // Transaction operations
  sendTransaction(tx: Transaction): Promise<string>;
  reverseTransaction(txHash: string): Promise<string>;
  
  // Consensus information
  getValidators(): Promise<Validator[]>;
  getFinalityStatus(blockHash: string): Promise<FinalityStatus>;
  
  // Fibonacci utilities
  getFibonacci(n: number): Promise<bigint>;
  getPhiRatio(): Promise<number>;
}
```

### Storage Layer

#### Database Schema
```sql
-- Blocks table
CREATE TABLE blocks (
    hash VARCHAR(66) PRIMARY KEY,
    number BIGINT NOT NULL,
    parent_hash VARCHAR(66),
    timestamp BIGINT,
    validator_address VARCHAR(42),
    fibonacci_index INTEGER,
    phi_coherence DECIMAL(20,18),
    signature_count INTEGER,
    finalized BOOLEAN DEFAULT FALSE
);

-- Transactions table  
CREATE TABLE transactions (
    hash VARCHAR(66) PRIMARY KEY,
    block_hash VARCHAR(66),
    from_address VARCHAR(42),
    to_address VARCHAR(42),
    value DECIMAL(36,18),
    fibonacci_fee INTEGER,
    reversible BOOLEAN DEFAULT TRUE,
    reversed_by VARCHAR(66)
);

-- Validator set
CREATE TABLE validators (
    address VARCHAR(42) PRIMARY KEY,
    stake DECIMAL(36,18),
    fibonacci_weight INTEGER,
    phi_score DECIMAL(10,8),
    active BOOLEAN DEFAULT TRUE
);
```

## 🚀 Deployment Strategy

### Infrastructure Requirements

#### Validator Nodes (21 nodes)
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: phi-validator
spec:
  replicas: 21
  template:
    spec:
      containers:
      - name: phi-node
        image: phichain/node:testnet-v1
        resources:
          requests:
            cpu: 2
            memory: 4Gi
          limits:
            cpu: 4
            memory: 8Gi
        env:
        - name: PHI_NETWORK
          value: "testnet"
        - name: PHI_VALIDATOR_KEY
          valueFrom:
            secretKeyRef:
              name: validator-keys
              key: private-key
```

#### Monitoring Stack
- **Metrics:** Prometheus + Grafana
- **Logs:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Alerting:** PagerDuty integration
- **Uptime:** Custom Φ-Chain health checks

### Geographic Distribution
```
Region          | Validators | Purpose
----------------|------------|------------------
North America   | 8          | Primary development
Europe          | 8          | Regulatory compliance  
Asia Pacific    | 5          | Global accessibility
```

## 🧪 Testing Framework

### Automated Testing
```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_fibonacci_consensus() {
        let mut network = TestNetwork::new(21);
        network.start_consensus();
        
        // Verify F_6 block timing
        let blocks = network.mine_blocks(10);
        for window in blocks.windows(2) {
            let time_diff = window[1].timestamp - window[0].timestamp;
            assert_eq!(time_diff, 8000); // 8 seconds
        }
    }
    
    #[test]
    fn test_reversible_transactions() {
        let mut chain = TestChain::new();
        
        // Forward transaction
        let tx = Transaction::new(alice, bob, 100);
        let tx_hash = chain.execute_transaction(tx);
        
        // Reverse transaction
        let reverse_hash = chain.reverse_transaction(tx_hash);
        assert!(reverse_hash.is_ok());
        
        // Verify state restoration
        assert_eq!(chain.get_balance(alice), initial_balance);
    }
}
```

### Performance Benchmarks
```bash
# Load testing script
#!/bin/bash

# TPS testing
echo "Testing transaction throughput..."
for i in {1..1000}; do
    curl -X POST localhost:8545 \
        -H "Content-Type: application/json" \
        -d '{"method":"phi_sendTransaction","params":[...]}'
done

# Latency testing
echo "Testing block finality latency..."
start_time=$(date +%s%N)
# Submit transaction and wait for finality
end_time=$(date +%s%N)
latency=$((($end_time - $start_time) / 1000000)) # Convert to ms
echo "Finality latency: ${latency}ms"
```

## 🔧 Developer Tools

### Φ-Chain CLI
```bash
# Installation
npm install -g @phichain/cli

# Basic usage
phi-cli init my-dapp
phi-cli deploy contract.phi
phi-cli query balance 0x123...
phi-cli reverse-tx 0xabc...

# Validator operations
phi-cli validator start
phi-cli validator stake 1000
phi-cli validator status
```

### SDK Examples
```javascript
// JavaScript SDK
import { PhiChain } from '@phichain/sdk';

const phi = new PhiChain('https://testnet.phichain.org');

// Send reversible transaction
const tx = await phi.sendTransaction({
    to: '0x742d35Cc6634C0532925a3b8D',
    value: phi.utils.toWei('1.618', 'phi'),
    reversible: true
});

// Check Fibonacci properties
const blockNumber = await phi.getBlockNumber();
const fibIndex = phi.utils.getFibonacciIndex(blockNumber);
console.log(`Block ${blockNumber} is F_${fibIndex}`);
```

## 📊 Success Metrics

### Technical Metrics
- **Block Time Variance:** <1% deviation from 8 seconds
- **Finality Time:** <30 seconds average
- **TPS:** 100+ sustained, 500+ peak
- **Uptime:** 99.9% over 30 days
- **Sync Time:** <10 minutes for new nodes

### Adoption Metrics
- **Active Validators:** 21/21 online
- **Developer Signups:** 100+ in first month
- **Transactions:** 10,000+ total
- **dApps:** 5+ deployed applications
- **Community:** 1,000+ Discord/Telegram members

### Mathematical Validation
- **Consensus Accuracy:** 100% FBA compliance
- **Phi Ratio Precision:** 15+ decimal places
- **Reversibility Success:** 99.9% successful reversals
- **Fibonacci Verification:** All parameters validated

## 🗓️ Launch Timeline

### Phase 1: Infrastructure (Weeks 1-4)
- Deploy validator nodes
- Configure monitoring
- Set up CI/CD pipelines
- Security hardening

### Phase 2: Network Launch (Weeks 5-6)
- Genesis block creation
- Validator onboarding
- Initial consensus testing
- Performance optimization

### Phase 3: Developer Tools (Weeks 7-8)
- CLI tool release
- SDK documentation
- Tutorial creation
- Developer outreach

### Phase 4: Community Testing (Weeks 9-12)
- Public testnet announcement
- Bug bounty program
- Community feedback integration
- Performance tuning

## 🛡️ Security Considerations

### Validator Security
- Hardware security modules (HSMs)
- Multi-signature key management
- Regular security audits
- Incident response procedures

### Network Security
- DDoS protection
- Rate limiting
- Encrypted communications
- Intrusion detection

### Smart Contract Security
- Formal verification tools
- Automated testing
- Code review processes
- Bug bounty programs

---

**Estimated Development Time:** 3-4 months
**Estimated Cost:** $300K - $500K
**Team Size:** 5-7 developers
**Launch Target:** Q2 2025