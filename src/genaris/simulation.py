"""
The tick loop and event log. One global timeline, one tick = one simulated
minute (doctrine Section 24 specifies microsecond addressability and a
global timeline in general; Slice 0 uses a coarse fixed tick since nothing
here needs finer resolution yet -- adaptive resolution is Section 23,
explicitly deferred until something requires it).
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

from genaris.agent import Agent, DeathCause
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

    def log(self, text: str) -> None:
        self.events.append(Event(self.tick_count, text))

    def step(self) -> None:
        self.tick_count += 1
        self.world.tick()
        for agent in self.agents:
            if not agent.alive:
                continue
            was_alive = agent.alive
            agent.tick(self.world, self.rng)
            if was_alive and not agent.alive:
                cause = agent.death_cause.value if agent.death_cause else "unknown"
                self.log(
                    f"Agent {agent.id} died of {cause} "
                    f"at age {agent.age_days:.1f} days (tick {self.tick_count})"
                )

    def run(self, ticks: int) -> None:
        for _ in range(ticks):
            self.step()

    def living_agents(self) -> list[Agent]:
        return [a for a in self.agents if a.alive]

    def summary(self) -> str:
        living = self.living_agents()
        if not living:
            return f"tick {self.tick_count}: all agents dead."
        avg_energy = sum(a.energy for a in living) / len(living)
        avg_age = sum(a.age_days for a in living) / len(living)
        return (
            f"tick {self.tick_count}: {len(living)}/{len(self.agents)} alive, "
            f"avg energy {avg_energy:.1f}, avg age {avg_age:.1f}d"
        )
