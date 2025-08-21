
# """
# memory_weight.py

# Utility functions and a small class to manage dynamic importance scores (weights)
# for conversation memories / souvenirs.

# Key ideas implemented:
# - Softmax probability calculation for a set of weights.
# - Temporal decay of weights:   w *= exp(-λ * Δt)
# - Reinforcement on usage:      w += α * (1 - p_i)
# - Pairwise comparison update via Elo ranking.

# Author: Noesis (generated for Nemo)
# """

from __future__ import annotations
from dataclasses import dataclass, field
from math import exp
from datetime import datetime
from typing import Iterable, Dict


@dataclass
class MemoryItem:
    # """Represents a memory with a dynamic weight `w`."""
    text: str
    w: float = 0.0
    created: datetime = field(default_factory=datetime.utcnow)
    last_used: datetime = field(default_factory=datetime.utcnow)

    # Defaults (can be tuned)
    lambda_decay: float = 0.01   # forgetting rate per day
    alpha_gain: float = 0.1      # reinforcement gain
    elo_k: int = 32              # Elo K-factor

    def age_days(self, now: datetime | None = None) -> float:
        now = now or datetime.utcnow()
        return (now - self.created).total_seconds() / 86400.0

    def since_last_use_days(self, now: datetime | None = None) -> float:
        now = now or datetime.utcnow()
        return (now - self.last_used).total_seconds() / 86400.0

    def decay(self, now: datetime | None = None) -> None:
        """Exponential decay of weight with time."""
        dt = self.since_last_use_days(now)
        self.w *= exp(-self.lambda_decay * dt)

    def reinforce(self, p_i: float, now: datetime | None = None) -> None:
        """Reinforce weight when memory is used."""
        self.w += self.alpha_gain * (1 - p_i)
        self.last_used = now or datetime.utcnow()


def softmax_probabilities(items: Iterable[MemoryItem]) -> Dict[MemoryItem, float]:
    items = list(items)
    exp_ws = [exp(it.w) for it in items]
    total = sum(exp_ws)
    if total == 0:
        return {it: 1 / len(items) for it in items}
    return {it: ew / total for it, ew in zip(items, exp_ws)}


def elo_update(item_a: MemoryItem, item_b: MemoryItem, score_a: float) -> None:
    """Update weights of two items using Elo scheme."""
    wa, wb = item_a.w, item_b.w
    expected_a = 1 / (1 + 10 ** ((wb - wa) / 400))
    expected_b = 1 - expected_a
    k = (item_a.elo_k + item_b.elo_k) / 2
    item_a.w = wa + k * (score_a - expected_a)
    item_b.w = wb + k * ((1 - score_a) - expected_b)
