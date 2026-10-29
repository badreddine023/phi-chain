"""Deterministic metrics for the Φ-Chain Sacred Architecture layer.

These helpers are classical mathematics and should not be interpreted as
physical quantum mechanics or as a measure of consciousness.
"""

from __future__ import annotations

from math import isfinite, sqrt
from typing import List

PHI = (1.0 + sqrt(5.0)) / 2.0
INV_PHI = 1.0 / PHI


def fibonacci(index: int) -> int:
    """Return F(index) for a non-negative index using bounded integer math."""
    if index < 0:
        raise ValueError("index must be non-negative")
    previous, current = 0, 1
    for _ in range(index):
        previous, current = current, previous + current
    return previous


def consecutive_ratio(index: int) -> float:
    """Return F(index + 1) / F(index), excluding the undefined F(0) ratio."""
    if index < 1:
        raise ValueError("index must be at least 1")
    return fibonacci(index + 1) / fibonacci(index)


def phi_ratio_error(index: int) -> float:
    """Return the absolute error between a Fibonacci ratio and φ."""
    return abs(consecutive_ratio(index) - PHI)


def inverse_phi_weights(count: int) -> List[float]:
    """Return normalized φ⁻ⁱ weights for a classical candidate list.

    This is a deterministic weighting heuristic for experiments. It is not a
    quantum probability distribution and provides no physical quantum effect.
    """
    if count < 0:
        raise ValueError("count must be non-negative")
    if count == 0:
        return []
    raw = [PHI ** (-index) for index in range(count)]
    total = sum(raw)
    weights = [value / total for value in raw]
    if not all(isfinite(value) for value in weights):
        raise ArithmeticError("non-finite weight generated")
    return weights


def coherence_fraction(affirmations: int, total_validators: int) -> float:
    """Return an observable agreement fraction for reporting and dashboards."""
    if total_validators <= 0:
        raise ValueError("total_validators must be positive")
    if affirmations < 0 or affirmations > total_validators:
        raise ValueError("affirmations must be within the validator count")
    return affirmations / total_validators
