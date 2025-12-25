# Φ-Chain Project

## Overview
The Φ-Chain is a blockchain architecture where every parameter is derived from the Fibonacci sequence and the Golden Ratio (Φ), eliminating arbitrary constants and grounding the system in universal mathematical law.

**Creator:** BadreddineBaha  
**Project Type:** Static Website + Python Blockchain Simulation

## Project Structure

### Frontend (Static Website)
- **index.html** - Main website showcasing the Φ-Chain vision and roadmap
- **styles.css** - Styling with a Golden Ratio color scheme
- **script.js** - Interactive animations and smooth scrolling

### Backend (Python Simulations)
- **phi_chain_core.py** - Core blockchain logic with Fibonacci utilities, genesis parameters, and Q-Matrix state transitions
- **phi_chain_prototype.py** - Full blockchain prototype with consensus mechanism
- **phi_chain_simulator.py** - Advanced blockchain simulator
- **main.py** - Entry point for running simulations

### Documentation
- **README.md** - Project overview and quick start
- **WHITEPAPER.md** - Comprehensive technical and philosophical treatise
- **phi_chain_report.md** - Simulation results and parameter analysis

## How to Run

### Static Website (Default)
The website runs automatically on port 5000 using a simple HTTP server:
```bash
python -m http.server 5000 --bind 0.0.0.0
```
Access the website through the webview panel.

### Python Simulations
Run the blockchain simulations locally:
```bash
python phi_chain_core.py          # Core utilities demo
python phi_chain_prototype.py     # Full blockchain simulation
python phi_chain_simulator.py     # Advanced simulator
python main.py                    # Main entry point
```

## Deployment
The project is configured for static deployment:
- **Type:** Static website
- **Public Directory:** `.` (root directory)
- **Frontend:** Automatically served at the published URL

## Key Features
- **Zero Arbitrary Constants** - All parameters derived from Fibonacci indices
- **Golden Ratio Governance** - Chain growth follows Φ = 1.618...
- **Q-Matrix State Transitions** - Eigenvalues are Φ and 1-Φ
- **Fibonacci Byzantine Agreement** - Consensus with F₁₅ (610) finality threshold

## Technologies
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Python 3.11, NumPy
- **Architecture:** Static website with optional Python simulations

## Project Philosophy
The Φ-Chain is not an engineering problem solved by arbitrary constants. It is a philosophical imperative realized through mathematical purity. Every aspect of the blockchain—from consensus timing (F₆ = 8 seconds) to validator counts (F₁₇ = 1,597)—is governed by the universal law of the Fibonacci sequence.

## User Preferences
- Clean, professional code structure
- Mathematical precision and accuracy
- Comprehensive documentation
- Modular, maintainable architecture

## Recent Changes
- **2025-12-06**: Project imported to Replit
  - Configured static HTTP server on port 5000
  - Set up deployment for static website hosting
  - Verified all Python scripts and frontend display correctly
  - Added comprehensive project documentation
