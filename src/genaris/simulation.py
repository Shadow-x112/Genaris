"""
The tick loop and event log. One global timeline, one tick = one simulated
minute (doctrine Section 24 specifies microsecond addressability and a
global timeline in general; this uses a coarse fixed tick since nothing
here needs finer resolution yet -- adaptive resolution is Section 23,
explicitly deferred until something requires it).
"""
from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass

from genaris.agent import Agent, Sex
from genaris.world import World


@dataclass
class Event:
    tick: int
    text: str


class Simulation:
    def __init__(self, world: World, agents: list[Agent], rng: random.Random):
        self.world = world
        self.agents = agents
        self.rng = rng
        self.tick_count = 0
        self.events: list[Event] = []
        self.births = 0

    def log(self, text: str) -> None:
        self.events.append(Event(self.tick_count, text))

    def _occupancy(self) -> dict[tuple[int, int], list[Agent]]:
        occ: dict[tuple[int, int], list[Agent]] = defaultdict(list)
        for a in self.agents:
            if a.alive:
                occ[(a.x, a.y)].append(a)
        return occ

    def step(self) -> None:
        self.tick_count += 1
        self.world.tick()
        occupancy = self._occupancy()
        for agent in self.agents:
            if not agent.alive:
                continue
            agent.tick(self.world, self.rng, occupancy)
            if not agent.alive:
                cause = agent.death_cause.value if agent.death_cause else "unknown"
                self.log(
                    f"Agent {agent.id} died of {cause} "
                    f"at age {agent.age_days:.1f} days (tick {self.tick_count})"
                )
        self._pair_and_birth()
        # drop the dead so the per-tick loops don't grow with history
        self.agents = [a for a in self.agents if a.alive]

    def _pair_and_birth(self) -> None:
        """Resolve reproduction after everyone has moved, so no agent pairs
        twice in a tick and children are not added mid-iteration."""
        candidates = [a for a in self.agents if a.can_reproduce()]
        if len(candidates) < 2:
            return
        self.rng.shuffle(candidates)
        occupancy = self._occupancy()
        children: list[Agent] = []
        for a in candidates:
            if not a.can_reproduce():  # already paired this tick
                continue
            partner = None
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    for b in occupancy.get((a.x + dx, a.y + dy), ()):
                        if b is not a and b.sex is not a.sex and b.can_reproduce():
                            partner = b
                            break
                    if partner:
                        break
                if partner:
                    break
            if partner is None:
                continue
            child = Agent.reproduce(a, partner, self.rng)
            children.append(child)
            self.births += 1
            self.log(
                f"Agent {child.id} ({child.sex.value}, gen {child.generation}) "
                f"born to {a.id} and {partner.id}"
            )
        self.agents.extend(children)

    def run(self, ticks: int) -> None:
        for _ in range(ticks):
            self.step()

    def living_agents(self) -> list[Agent]:
        return [a for a in self.agents if a.alive]

    def summary(self) -> str:
        living = self.living_agents()
        if not living:
            return f"tick {self.tick_count}: all agents dead."
        n = len(living)
        avg_energy = sum(a.energy for a in living) / n
        avg_age = sum(a.age_days for a in living) / n
        females = sum(1 for a in living if a.sex is Sex.FEMALE)
        max_gen = max(a.generation for a in living)
        met = sum(a.genome.metabolism for a in living) / n
        spd = sum(a.genome.speed for a in living) / n
        mxe = sum(a.genome.max_energy for a in living) / n
        return (
            f"tick {self.tick_count}: {n} alive ({females}F/{n - females}M), "
            f"births {self.births}, max gen {max_gen}, "
            f"avg energy {avg_energy:.1f}, avg age {avg_age:.1f}d | "
            f"traits met {met:.3f} spd {spd:.3f} maxE {mxe:.3f}"
        )
