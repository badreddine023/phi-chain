#!/usr/bin/env python3
"""Audit the first block and run a local, non-custodial wallet smoke test.

This command never reads private keys, creates funds, or broadcasts a transaction.
It compares the deterministic GenesisBlock constructor with stored artifacts and
checks deterministic address generation/validation using a fixed public test vector.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))

from core.block import GenesisBlock  # noqa: E402
from crypto.phi_address_system import PhiAddressSystem  # noqa: E402


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_audit() -> dict:
    started = time.perf_counter()
    constructed = GenesisBlock().to_dict()
    configured = read_json(ROOT / "config" / "genesis_mainnet.json")
    deployed = read_json(ROOT / "deployments" / "phi-chain-mainnet-v1" / "genesis_block.json")

    public_test_vector = hashlib.sha256(b"phi-chain-wallet-smoke-public-key").hexdigest()
    address = PhiAddressSystem.generate_phi_address(public_test_vector)
    tampered = address[:-5] + ("0" if address[-5] != "0" else "1") + address[-4:]
    wallet_valid = PhiAddressSystem.validate_address(address)
    tampered_rejected = not PhiAddressSystem.validate_address(tampered)

    config_genesis = configured["genesis_block"]
    result = {
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
        "target_under_one_second": True,
        "genesis": {
            "constructed_hash": constructed["hash"],
            "configured_hash": config_genesis["hash"],
            "deployed_hash": deployed["hash"],
            "constructed_timestamp": constructed["timestamp"],
            "configured_timestamp": config_genesis["timestamp"],
            "deployed_timestamp": deployed["timestamp"],
            "hash_matches_config": constructed["hash"] == config_genesis["hash"],
            "hash_matches_deployed": constructed["hash"] == deployed["hash"],
            "timestamp_matches_config": constructed["timestamp"] == config_genesis["timestamp"],
            "timestamp_matches_deployed": constructed["timestamp"] == deployed["timestamp"],
        },
        "wallet": {
            "address_prefix": address[:32],
            "address_valid": wallet_valid,
            "tampered_address_rejected": tampered_rejected,
            "private_keys_read": False,
            "broadcast_attempted": False,
        },
    }
    result["genesis"]["canonical_artifacts_match"] = all(
        result["genesis"][key]
        for key in (
            "hash_matches_config",
            "hash_matches_deployed",
            "timestamp_matches_config",
            "timestamp_matches_deployed",
        )
    )
    result["passed"] = bool(
        result["genesis"]["canonical_artifacts_match"]
        and result["wallet"]["address_valid"]
        and result["wallet"]["tampered_address_rejected"]
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="return non-zero when genesis artifacts disagree")
    args = parser.parse_args()
    result = run_audit()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
