# Φ-Chain Genesis-to-Wallet Rebuild

The genesis review, wallet smoke workflow, React website rebuild, and checkpoint are complete. The wallet path is locally non-custodial and executes in under one second; the first-block artifacts remain inconsistent and must be canonicalized before any real launch.

## Evidence

- `tools/genesis_wallet_smoke.py` compares the constructed, configured, and deployed first block.
- Wallet address generation, validation, and tamper rejection passed without reading private keys or broadcasting transactions.
- Measured local smoke runtime: `0.422 ms`.
- React typecheck and production build pass.
- Website checkpoint saved as `73c818c7`.

## Required before launch

- [ ] Choose one canonical genesis timestamp, schema, and hash derivation.
- [ ] Regenerate and verify all genesis artifacts from that source of truth.
- [ ] Add a strict CI gate that fails when genesis artifacts disagree.
- [ ] Replace placeholder/conceptual wallet and validator data before any live deployment.
