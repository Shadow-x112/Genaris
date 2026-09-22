"""
Slice 0 entry point: build a tiny world and population, run it for a
while, print a summary periodically and every death event. This is meant
to be run and watched, not just read.
"""
from __future__ import annotations

import random

from genaris.agent import Agent
from genaris.genome import Genome
from genaris.simulation import Simulation
from genaris.world import World

WORLD_SIZE = 30
NUM_AGENTS = 15
TICKS = 60 * 24 * 60  # ~60 simulated days
SUMMARY_EVERY = 24 * 60  # once per simulated day
SEED = 20260922


def build_simulation(seed: int = SEED) -> Simulation:
    rng = random.Random(seed)
    world = World(WORLD_SIZE, WORLD_SIZE, rng)

    agents = []
    for _ in range(NUM_AGENTS):
        x = rng.randrange(WORLD_SIZE)
        y = rng.randrange(WORLD_SIZE)
        genome = Genome.random_founder(rng)
        agents.append(Agent(genome=genome, x=x, y=y))

    return Simulation(world, agents, rng)


def main() -> None:
    sim = build_simulation()
    print(f"Starting Genaris Slice 0: {NUM_AGENTS} agents on a {WORLD_SIZE}x{WORLD_SIZE} world.")
    print(sim.summary())

    last_event_count = 0
    for day in range(1, TICKS // SUMMARY_EVERY + 1):
        sim.run(SUMMARY_EVERY)

        # print any death events that happened this day
        for event in sim.events[last_event_count:]:
            print(f"  [day {day}] {event.text}")
        last_event_count = len(sim.events)

        print(sim.summary())

        if not sim.living_agents():
            print("Population extinct. Stopping early.")
            break

    print("\nDone.")
    print(f"Total events logged: {len(sim.events)}")


if __name__ == "__main__":
    main()
