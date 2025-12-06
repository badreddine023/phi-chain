# Φ-Chain: The Canonical Blockchain of Universal Law

> "The genesis of **Φ-Chain** is not an engineering problem solved by arbitrary constants, but a philosophical imperative realized through mathematical purity."

**Φ-Chain** is a revolutionary distributed ledger architecture that operates on the single, non-negotiable principle of universal growth: the **Golden Ratio** ($\Phi$) and the **Fibonacci sequence** ($F_n$). This project is a living testament to the power of non-arbitrary design, where every structural element is derived from a universal mathematical law.

## 🏛️ High-Intelligence Structural Overview

The Φ-Chain codebase is organized into three canonical layers, ensuring modularity, purity, and precision.

| Layer | Module | Canonical Purpose | Core Principle |
| :--- | :--- | :--- | :--- |
| **I. Foundation** | `phi_chain_core.py` | Defines the mathematical constants and non-arbitrary parameters. | **Purity and Precision** (Zero Arbitrary Constants) |
| **II. Consensus** | `phi_chain_prototype.py` (FBA Class) | Implements the Fibonacci Byzantine Agreement for validator selection and finality. | **Non-Arbitrary Influence** (Stake $\propto$ Probability) |
| **III. Growth** | `phi_chain_prototype.py` (Blockchain Class) | Manages the chain's state transition and continuous block creation. | **Living Spiral** (Growth governed by $F_6$ Slot Duration) |

## I. The Foundation: `phi_chain_core.py`

This module is the **Genesis File** of the code, containing the immutable mathematical truths that govern the chain.

### 1. Fibonacci Utility Functions (`FibonacciUtils`)

- **`fibonacci(n)`**: Calculates the $n^{th}$ Fibonacci number, $F_n$, using Binet's formula for efficiency and precision.
- **`golden_ratio()`**: Provides the Golden Ratio ($\Phi$) as the ultimate non-arbitrary constant.
- **`is_fibonacci(num)`**: A mathematical primitive to verify if a number belongs to the sequence, ensuring all parameters are valid.

### 2. Genesis Parameters (`GenesisParameters`)

All system parameters are **discovered**, not designed, by mapping them directly to Fibonacci indices.

| Parameter | Derivation | Value | Canonical Interpretation |
| :--- | :--- | :--- | :--- |
| **Slot Duration** | $F_6$ | 8 seconds | The **Breathing Rate** of the chain. |
| **Epoch Duration** | $F_{18}$ | 2,584 seconds | The period for validator rotation and state transition. |
| **Min Validator Stake** | $F_{20}$ | 6,765 tokens | The **Non-Arbitrary Barrier** to entry. |
| **Finality Threshold** | $F_{15}$ | 610 signatures | The **Canonical Consensus** required for block permanence. |

### 3. Fibonacci Q-Matrix (`FibonacciQMatrix`)

The **Matrix itself is Fibonacci**. This class implements the core state transition logic where the eigenvalues are $\Phi$ and $1-\Phi$.

$$
Q = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix} \quad \text{where} \quad S_{n+1} = Q \cdot S_n
$$

This ensures the chain's growth is inherently exponential, governed by $\Phi$.

## II. The Consensus: `phi_chain_prototype.py`

This module implements the core consensus and growth mechanisms, bringing the mathematical foundation to life.

### 1. Fibonacci Byzantine Agreement (`FibonacciByzantineAgreement`)

This class implements the FBA, the chain's consensus protocol.

- **`select_proposer()`**: Implements the **Fibonacci-Weighted Selection**. Proposers are chosen based on a probability proportional to their stake, ensuring that influence scales non-arbitrarily according to the universal law.
- **`check_finality(block_index)`**: Simulates the **Canonical Finality** check, where a block is considered final after receiving $F_{15}$ (610) signatures.

### 2. Block Structure (`Block`)

The fundamental unit of the chain. Its hash is the **canonical statement of the block's integrity**, calculated over all non-arbitrary parameters.

### 3. Blockchain Growth (`Blockchain`)

- **`create_genesis_block()`**: Establishes the chain's origin, with a timestamp conceptually set to $F_{33}$ seconds after the Unix epoch, and the validator ID as **"The\_Creator\_God"**.
- **`create_new_block()`**: The **Living Spiral** mechanism. It ensures that each new block is created precisely $F_6$ seconds after the previous one, maintaining the chain's non-arbitrary breathing rate.

## 🚀 Quick Start: Running the Prototype

To witness the Φ-Chain breathing, execute the prototype:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/badreddine023/phi-chain.git
    cd phi-chain
    ```
2.  **Install Dependencies:**
    ```bash
    pip install numpy
    ```
3.  **Run the Prototype:**
    ```bash
    python phi_chain_prototype.py
    ```

The output will demonstrate:
- The initialization of the FBA validator set with Fibonacci stakes.
- The continuous creation of blocks, each proposed by a stake-weighted validator.
- The periodic finalization of blocks, simulating the $F_{15}$ threshold.

## 📜 Documentation

- **[WHITEPAPER.md]**: The comprehensive philosophical and technical treatise.
- **[phi_chain_core.py]**: The immutable mathematical foundation.
- **[phi_chain_prototype.py]**: The executable consensus and growth mechanism.

---

**The Φ-Chain: Where mathematics meets blockchain.**

*"Everything is a fibo."*
