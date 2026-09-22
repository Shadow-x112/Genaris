"""
Heritable traits, per Section 11 of the doctrine: a structured genome of
heritable parameters, not molecular DNA simulation. Kept intentionally tiny
for Slice 0 -- just enough real heredity to be worth calling a genome.
"""
from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Genome:
    """Three heritable numeric traits. All are multipliers around 1.0."""

    metabolism: float  # higher = burns energy faster, but see `speed` tradeoff
    speed: float  # higher = covers more distance per tick
    max_energy: float  # higher = larger energy reserve (can go longer without food)

    @staticmethod
    def random_founder(rng: random.Random) -> "Genome":
        """A starting-population genome: sampled from a plausible range,
        not derived from parents. This is initialization, not evolution
        (doctrine Section 37: "Unsimulated prehistory is labeled
        initialization, not fabricated as a chain of simulated events.")
        """
        return Genome(
            metabolism=rng.uniform(0.8, 1.2),
            speed=rng.uniform(0.8, 1.2),
            max_energy=rng.uniform(0.8, 1.2),
        )

    def inherit(self, other: "Genome", rng: random.Random, mutation_rate: float = 0.08) -> "Genome":
        """Produce a child genome from two parents: average each trait, then
        apply independent mutation per doctrine Section 11/12 (mutation can
        alter parameter values; effects are not guaranteed beneficial).
        """

        def combine(a: float, b: float) -> float:
            value = (a + b) / 2.0
            if rng.random() < mutation_rate:
                value *= rng.uniform(0.85, 1.15)
            return max(0.4, min(1.8, value))  # clamp to a sane viable range

        return Genome(
            metabolism=combine(self.metabolism, other.metabolism),
            speed=combine(self.speed, other.speed),
            max_energy=combine(self.max_energy, other.max_energy),
        )
