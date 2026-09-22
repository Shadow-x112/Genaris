"""
Entry point: build a tiny world and founding population, run it for a
while, print a periodic summary and every birth/death event. This is meant
to be run and watched, not just read.
"""
from __future__ import annotations

import random

from genaris.agent import TICKS_PER_DAY, Agent, Sex
from genaris.genome import Genome
from genaris.simulation import Simulation
from genaris.world import World

WORLD_SIZE = 30
NUM_AGENTS = 15
DAYS = 200  # several generations under the dev-compressed life history
SUMMARY_EVERY_DAYS = 5
SEED = 20260922


def build_simulation(seed: int = SEED) -> Simulation:
    rng = random.Random(seed)
    world = World(WORLD_SIZE, WORLD_SIZE, rng)

    agents = []
    for _ in range(NUM_AGENTS):
        x = rng.randrange(WORLD_SIZE)
        y = rng.randrange(WORLD_SIZE)
        genome = Genome.random_founder(rng)
        sex = rng.choice([Sex.FEMALE, Sex.MALE])
        # founders start as young adults of staggered ages, so they don't all
        # hit old age on the same tick (initialization, per Section 37)
        life = Agent.LIFE
        age = rng.randrange(life.maturity_ticks, life.maturity_ticks + 15 * TICKS_PER_DAY)
        agents.append(Agent(genome=genome, sex=sex, x=x, y=y, age_ticks=age))

    return Simulation(world, agents, rng)


def main() -> None:
    sim = build_simulation()
    print(
        f"Starting Genaris Slice 1: {NUM_AGENTS} founders on a {WORLD_SIZE}x{WORLD_SIZE} world "
        f"(life history: {Agent.LIFE.label})."
    )
    print(sim.summary())

    last_event_count = 0
    for day in range(SUMMARY_EVERY_DAYS, DAYS + 1, SUMMARY_EVERY_DAYS):
        sim.run(SUMMARY_EVERY_DAYS * TICKS_PER_DAY)

        # print any birth/death events since the last summary
        for event in sim.events[last_event_count:]:
            print(f"  [day {event.tick / TICKS_PER_DAY:.1f}] {event.text}")
        last_event_count = len(sim.events)

        print(sim.summary())

        if not sim.living_agents():
            print("Population extinct. Stopping early.")
            break

    print("\nDone.")
    print(f"Total events logged: {len(sim.events)}")


if __name__ == "__main__":
    main()
