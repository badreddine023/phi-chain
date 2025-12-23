# Φ-Chain (Phi-Chain): The Golden Ratio Blockchain

![Φ-Chain Logo](phi_chain_logo.jpg)

Φ-Chain is a revolutionary decentralized blockchain ecosystem governed by the mathematical principles of the **Golden Ratio (Φ)** and the **Fibonacci sequence**. By integrating these universal constants into its core consensus, state transitions, and economic models, Φ-Chain achieves a unique balance of scalability, security, and mathematical purity.

## 🌟 Vision & Purpose

Traditional blockchains often rely on arbitrary constants for block times, rewards, and validator thresholds. Φ-Chain replaces these with values derived from the Fibonacci sequence, ensuring that every parameter of the network is interconnected through the Golden Ratio. The system is not merely engineered; it is discovered from first principles.

---

## 🚀 Core Features

### 1. Fibonacci Q-Matrix State Transitions
The state of Φ-Chain evolves according to the Fibonacci Q-Matrix:
```
Q = [[1, 1], 
     [1, 0]]
```
The state vector $S_n = [F_{n+1}, F_n]^T$ transitions to $S_{n+1} = Q \cdot S_n$, ensuring that the growth of the network metrics follows the natural progression of the Fibonacci sequence.

### 2. Proof-of-Coherence (PoC) Mining
A novel consensus mechanism where validator influence is weighted by their **Coherence Score**. This score is derived from their stake and historical participation, both of which must align with Fibonacci numbers.

### 3. Fibonacci Byzantine Agreement (FBA)
A robust consensus engine that requires a supermajority of signatures (at least $F_{15} = 610$ validators) to reach finality, providing high security and mathematical consistency.

### 4. Optimistic Parallelized EVM (OPEVM)
High-throughput transaction execution using static analysis to detect state conflicts before execution, maintaining full compatibility with the Ethereum ecosystem.

### 5. Responsive Wallet & Dashboard
- **Wallet UI**: Manage balances, stake tokens, and monitor PoC mining in real-time.
- **Consensus Monitor**: Interactive charts showing Fibonacci convergence and network health.

---

## 🛠 Getting Started

### Prerequisites
- **Python**: 3.10 or higher
- **Node.js**: 18.x or higher
- **Browser**: Modern browser (Chrome, Firefox, Brave)

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/badreddine023/phi-chain.git
   cd phi-chain
   ```

2. **Install dependencies**:
   ```bash
   pip install -r core/requirements.txt
   # or if using uv
   uv sync
   ```

3. **Initialize the Mainnet**:
   ```bash
   python3 tools/deploy_mainnet.py
   ```

---

## 📖 Usage

### Running the Wallet
Open `wallet.html` in your browser to access the mainnet wallet interface.
- **Connect**: Use the built-in web3 connector to link your external wallet.
- **Mine**: Start PoC mining directly from the dashboard.
- **Stake**: Stake Φ tokens (must be a Fibonacci number) to earn rewards.

### Monitoring the Network
Open `consensus-monitor.html` to view:
- Real-time block height and TPS.
- Active validator count ($F_{17} = 1597$ max).
- Fibonacci state vector evolution.

### Validator Node Setup
To run a validator node:
```bash
python3 validator_node.py --id your_validator_id --stake 6765
```
*Note: Minimum stake is $F_{20} = 6765$ Φ.*

---

## 📂 File & Folder Structure

| File / Folder | Description |
| :--- | :--- |
| `phi_chain_core.py` | Core data structures and Fibonacci logic. |
| `phi_chain.py` | Unified blockchain engine (PoC, FBA, State). |
| `validator_node.py` | Validator node implementation and key management. |
| `wallet.html` | Mainnet wallet user interface. |
| `consensus-monitor.html` | Real-time network analytics dashboard. |
| `tools/deploy_mainnet.py` | Automated mainnet deployment script. |
| `api/wallet_api.py` | FastAPI backend for wallet and blockchain queries. |
| `docs/` | Detailed technical reports and whitepapers. |

---

## 📈 Mainnet Parameters

| Parameter | Value | Fibonacci Index |
| :--- | :--- | :--- |
| **Slot Duration** | 8s | $F_6$ |
| **Epoch Duration** | 2,584s | $F_{18}$ |
| **Min Stake** | 6,765 Φ | $F_{20}$ |
| **Max Validators** | 1,597 | $F_{17}$ |
| **Finality Threshold** | 610 | $F_{15}$ |
| **Genesis Supply** | 3,524,578 Φ | $F_{33}$ |

---

## 🤝 Development & Contribution

We welcome contributions that maintain the mathematical integrity of Φ-Chain.
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Ensure all new parameters follow Fibonacci indices.
4. Submit a Pull Request.

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

**Φ-Chain: The Universe is Written in the Language of Mathematics.**
