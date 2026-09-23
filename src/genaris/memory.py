"""
Spatial memory of food, per doctrine Sections 18/19 -- the smallest
useful slice: an agent remembers where it saw or ate food, how much it
perceived there, when, and how sure it is. Beliefs can be wrong two ways:
perception was noisy when formed, or the world changed since (others ate
it, or it regrew) -- the agent assumes things stay as last seen.

Deliberately NOT here yet (Sections 18/19): episodic memory, memories of
individuals, skills, reports from others, inference about regrowth, and
contradictory memories of the same place. A fresh sighting simply
overwrites the old belief about that cell. That is a simplification for
this slice, not the intended long-term architecture: once beliefs can also
come from reports (Slice 4), observation and report can disagree and must
be able to coexist.
"""
from __future__ import annotations

from dataclasses import dataclass

from genaris.foraging import food_score


@dataclass
class FoodBelief:
    x: int
    y: int
    amount: float  # perceived amount when last observed -- not necessarily the truth, then or now
    observed_tick: int
    strength: float  # encoding strength at observation (eating encodes more strongly than seeing)
    source: str = "observed"  # only direct observation exists until Slice 4

    def confidence(self, now: int, half_life_ticks: int) -> float:
        """Confidence decays with disuse. It is the agent's certainty, and is
        tracked separately from whether the belief is accurate (Section 18)."""
        return self.strength * 0.5 ** ((now - self.observed_tick) / half_life_ticks)


class FoodMemory:
    SEEN_STRENGTH = 1.0
    ATE_STRENGTH = 2.0
    FORGET_BELOW = 0.02  # beliefs this faint are gone (decay forgetting)

    def __init__(self, capacity: int = 8, half_life_ticks: int = 24 * 60):
        self.capacity = capacity
        self.half_life_ticks = half_life_ticks
        self.beliefs: dict[tuple[int, int], FoodBelief] = {}

    def __len__(self) -> int:
        return len(self.beliefs)

    def confidence(self, belief: FoodBelief, now: int) -> float:
        return belief.confidence(now, self.half_life_ticks)

    def observe(self, x: int, y: int, perceived: float, now: int, strength: float) -> None:
        """Record a direct observation. A fresh sighting replaces any older
        belief about the same cell (see module docstring)."""
        self.beliefs[(x, y)] = FoodBelief(x, y, perceived, now, strength)

    def forget(self, now: int) -> None:
        """Drop beliefs that decayed away, then the weakest ones if over
        capacity (interference / limited storage). Ties break by cell
        coordinates so the result doesn't depend on dict order."""
        for key in [k for k, b in self.beliefs.items() if self.confidence(b, now) < self.FORGET_BELOW]:
            del self.beliefs[key]
        while len(self.beliefs) > self.capacity:
            weakest = min(self.beliefs.values(), key=lambda b: (self.confidence(b, now), b.x, b.y))
            del self.beliefs[(weakest.x, weakest.y)]

    def beliefs_within(self, x: int, y: int, radius: int) -> list[FoodBelief]:
        return [b for b in self.beliefs.values() if max(abs(b.x - x), abs(b.y - y)) <= radius]

    def best_target(self, x: int, y: int, now: int, min_amount: float) -> FoodBelief | None:
        """The remembered spot worth walking to, scored by the same
        `food_score` as live sight, with the belief's current confidence.
        Beliefs remembered as empty are never targets."""
        best, best_score = None, 0.0
        for b in self.beliefs.values():
            if b.amount <= min_amount or (b.x, b.y) == (x, y):
                continue
            dist = max(abs(b.x - x), abs(b.y - y))
            score = food_score(b.amount, dist, self.confidence(b, now))
            if score > best_score or (score == best_score and best is not None and (b.x, b.y) < (best.x, best.y)):
                best, best_score = b, score
        return best
