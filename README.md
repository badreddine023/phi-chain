# Φ-Chain: The Golden Ratio Blockchain

Welcome to the official repository of **Φ-Chain**, the first autonomous blockchain ecosystem governed by the Golden Ratio (Φ) and the Fibonacci sequence.

## 🚀 Quick Start

### 1. Mainnet Deployment
To initialize the Φ-Chain Mainnet and generate the genesis block:
```bash
python3 tools/deploy_mainnet.py
```

### 2. Start a Validator Node
After deployment, you can start a validator node using the generated configuration:
```bash
python3 consensus/node_runner.py config/validators/node_0.json
```

### 3. Launch the Wallet
Open `wallet.html` in your browser to manage your assets, stake tokens, and start PoC mining.

### 4. Monitor the Network
Open `consensus-monitor.html` to view real-time network metrics and validator performance.

## 🛠 Architecture

- **Core**: `phi_chain_core.py` - Fibonacci logic, Q-Matrix state transitions, and block structures.
- **Consensus**: `consensus/` - Validator logic, node runner, and FBA implementation.
- **Tools**: `tools/` - Deployment, key generation, and research aggregation.
- **UI**: `index.html`, `wallet.html`, `consensus-monitor.html`.

## 📖 Documentation

- [WHITEPAPER.md](WHITEPAPER.md): Theoretical foundation and economic model.
- [TECHNICAL_REPORT.md](TECHNICAL_REPORT.md): Detailed implementation and setup guide.

## 🤖 Self-Evolution
Φ-Chain is designed to evolve autonomously. The `research_aggregator.py` script monitors external innovations every 24 hours to ensure Φ-Chain remains at the forefront of blockchain technology.

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
