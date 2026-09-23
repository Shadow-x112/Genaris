"""
How an agent values a food spot. One scoring rule for every source of
knowledge about food -- live sight now, remembered spots once memory
exists -- so the two can't drift into separate heuristics.
"""
from __future__ import annotations


def food_score(amount: float, distance: int, confidence: float = 1.0) -> float:
    """Value of heading for a spot: more food, more certainty, and closer
    all help. Live sight is confidence 1.0.

    There is no minimum-amount cutoff: a hungry agent with nothing better
    in range still goes for crumbs. Distance 0 (the agent's own cell)
    counts as 1, so food underfoot is compared fairly with a richer spot
    nearby rather than always winning.
    """
    return amount * confidence / (1 + distance)
