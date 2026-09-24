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

    def retention(self, now: int, half_life_ticks: int) -> float:
        """How strongly the belief is still held -- governs forgetting only.
        Not a probability and not confidence (see ValidityModel)."""
        return self.strength * 0.5 ** ((now - self.observed_tick) / half_life_ticks)


class ValidityModel:
    """The agent's learned sense of how long a food memory stays true.

    Each time a remembered food spot comes back into view after a gap, the
    agent records the belief's age and whether food was still there.
    Confidence in a belief of age t is the agent's own smoothed hit rate
    for that age range: (hits + 1) / (tries + 2), a probability in (0, 1).
    With no experience it is 0.5 -- "I don't know yet". Learned in one
    lifetime, not inherited (Section 14); lifetime-learned expectation
    (Section 35). It tracks the ecology rather than a hand-set decay rate,
    so it stays calibrated if regrowth or crowding change.
    """

    # lower edges of age bins, in ticks (roughly log-spaced)
    AGE_BINS = (0, 5, 10, 25, 50, 100, 200, 400, 800)
    # a belief refreshed on the previous tick (continuous view while
    # feeding) is trivially still right; only a return after a gap is a test
    MIN_TEST_AGE = 2

    def __init__(self) -> None:
        self.hits = [0] * len(self.AGE_BINS)
        self.tries = [0] * len(self.AGE_BINS)

    def _bin(self, age: int) -> int:
        i = 0
        while i + 1 < len(self.AGE_BINS) and age >= self.AGE_BINS[i + 1]:
            i += 1
        return i

    def record(self, age: int, still_there: bool) -> None:
        if age < self.MIN_TEST_AGE:
            return
        i = self._bin(age)
        self.tries[i] += 1
        self.hits[i] += still_there

    def probability(self, age: int) -> float:
        i = self._bin(age)
        return (self.hits[i] + 1) / (self.tries[i] + 2)


class FoodMemory:
    SEEN_STRENGTH = 1.0
    ATE_STRENGTH = 2.0
    FORGET_BELOW = 0.02  # beliefs this faint are gone (decay forgetting)

    def __init__(self, capacity: int = 8, half_life_ticks: int = 24 * 60):
        self.capacity = capacity
        self.half_life_ticks = half_life_ticks
        self.beliefs: dict[tuple[int, int], FoodBelief] = {}
        self.validity = ValidityModel()

    def __len__(self) -> int:
        return len(self.beliefs)

    def retention(self, belief: FoodBelief, now: int) -> float:
        return belief.retention(now, self.half_life_ticks)

    def confidence(self, belief: FoodBelief, now: int) -> float:
        """Probability, as the agent has learned it, that a food belief
        this old is still true. Kept separate from retention: a strongly
        held memory (e.g. somewhere it ate) is not thereby more likely to
        be current."""
        return self.validity.probability(now - belief.observed_tick)

    def check_against_sight(self, x: int, y: int, radius: int, seen_cells: set[tuple[int, int]], now: int,
                            min_amount: float) -> None:
        """Before fresh sightings overwrite them: every remembered food spot
        now in view is a test of the memory -- learn from whether food is
        still seen there. Call before observe() for this look."""
        for b in self.beliefs_within(x, y, radius):
            if b.amount > min_amount:
                self.validity.record(now - b.observed_tick, (b.x, b.y) in seen_cells)

    def observe(self, x: int, y: int, perceived: float, now: int, strength: float) -> None:
        """Record a direct observation. A fresh sighting replaces any older
        belief about the same cell (see module docstring)."""
        self.beliefs[(x, y)] = FoodBelief(x, y, perceived, now, strength)

    def forget(self, now: int) -> None:
        """Drop beliefs that decayed away, then the weakest ones if over
        capacity (interference / limited storage). Ties break by cell
        coordinates so the result doesn't depend on dict order."""
        for key in [k for k, b in self.beliefs.items() if self.retention(b, now) < self.FORGET_BELOW]:
            del self.beliefs[key]
        while len(self.beliefs) > self.capacity:
            weakest = min(self.beliefs.values(), key=lambda b: (self.retention(b, now), b.x, b.y))
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
