"""Spatial food memory and perception (doctrine Sections 17-19).

Run from the repo root:  python -m unittest discover -s tests
"""
from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genaris.agent import Agent, Sex  # noqa: E402
from genaris.genome import Genome  # noqa: E402
from genaris.memory import FoodMemory  # noqa: E402
from genaris.world import Cell, Terrain, World  # noqa: E402

DAY = 24 * 60


def barren_world(size: int = 20) -> World:
    """A world with no food anywhere, so tests place food exactly."""
    world = World(size, size, random.Random(0))
    for y in range(size):
        for x in range(size):
            world.grid[y][x] = Cell(terrain=Terrain.GRASS, food=0.0, regrow_rate=0.0)
    return world


def hungry_agent(x: int, y: int) -> Agent:
    genome = Genome(metabolism=1.0, speed=1.0, max_energy=1.0)
    return Agent(genome=genome, sex=Sex.FEMALE, x=x, y=y, energy=30.0)


class FoodMemoryTests(unittest.TestCase):
    def test_confidence_halves_each_half_life(self) -> None:
        m = FoodMemory(half_life_ticks=DAY)
        m.observe(1, 1, 5.0, now=0, strength=1.0)
        b = m.beliefs[(1, 1)]
        self.assertAlmostEqual(m.confidence(b, 0), 1.0)
        self.assertAlmostEqual(m.confidence(b, DAY), 0.5)
        self.assertAlmostEqual(m.confidence(b, 3 * DAY), 0.125)

    def test_faded_beliefs_are_forgotten(self) -> None:
        m = FoodMemory(half_life_ticks=DAY)
        m.observe(1, 1, 5.0, now=0, strength=1.0)
        m.forget(now=10 * DAY)  # 1/1024 < FORGET_BELOW
        self.assertEqual(len(m), 0)

    def test_capacity_drops_weakest(self) -> None:
        m = FoodMemory(capacity=3, half_life_ticks=DAY)
        m.observe(0, 0, 5.0, now=0, strength=1.0)  # oldest, weakest
        m.observe(1, 0, 5.0, now=100, strength=1.0)
        m.observe(2, 0, 5.0, now=200, strength=1.0)
        m.observe(3, 0, 5.0, now=0, strength=2.0)  # old but eaten there: strong
        m.forget(now=300)
        self.assertEqual(len(m), 3)
        self.assertNotIn((0, 0), m.beliefs)
        self.assertIn((3, 0), m.beliefs)

    def test_fresh_sighting_overwrites(self) -> None:
        m = FoodMemory()
        m.observe(4, 4, 9.0, now=0, strength=2.0)
        m.observe(4, 4, 0.0, now=50, strength=1.0)
        b = m.beliefs[(4, 4)]
        self.assertEqual((b.amount, b.observed_tick, b.strength), (0.0, 50, 1.0))

    def test_empty_spots_are_kept_but_never_targeted(self) -> None:
        m = FoodMemory()
        m.observe(5, 5, 0.0, now=0, strength=1.0)
        m.forget(now=0)
        self.assertIn((5, 5), m.beliefs)  # being empty is still knowledge
        self.assertIsNone(m.best_target(0, 0, now=0, min_amount=0.5))

    def test_target_prefers_more_food_and_closer(self) -> None:
        m = FoodMemory()
        m.observe(10, 0, 8.0, now=0, strength=1.0)  # far
        m.observe(2, 0, 8.0, now=0, strength=1.0)  # near, same amount
        m.observe(3, 0, 1.0, now=0, strength=1.0)  # near, little food
        b = m.best_target(0, 0, now=0, min_amount=0.5)
        self.assertEqual((b.x, b.y), (2, 0))


class PerceptionTests(unittest.TestCase):
    def test_no_noise_is_exact(self) -> None:
        a = hungry_agent(0, 0)
        a.PERCEPTION_NOISE = 0.0
        self.assertEqual(a._perceive(7.25, random.Random(1)), 7.25)

    def test_noise_varies_and_stays_non_negative(self) -> None:
        a = hungry_agent(0, 0)
        rng = random.Random(1)
        values = [a._perceive(5.0, rng) for _ in range(2000)]
        self.assertTrue(all(v >= 0.0 for v in values))
        self.assertGreater(len(set(values)), 1000)
        self.assertAlmostEqual(sum(values) / len(values), 5.0, delta=0.1)


class BeliefCanBeWrongTests(unittest.TestCase):
    def test_stale_belief_sends_agent_to_eaten_food(self) -> None:
        world = barren_world()
        world.cell(3, 3).food = 8.0
        agent = hungry_agent(0, 0)
        agent.PERCEPTION_NOISE = 0.0
        rng = random.Random(1)

        agent._look_for_food(world, rng)  # sees the food at (3, 3) and remembers it
        self.assertIn((3, 3), agent.memory.beliefs)

        # walk out of sight, then someone else eats it while the agent is away
        agent.x, agent.y = 15, 15
        world.cell(3, 3).food = 0.0

        # the agent still believes it's there and heads back
        self.assertEqual(agent._recall_food(), (3, 3))
        self.assertAlmostEqual(agent.memory.beliefs[(3, 3)].amount, 8.0)

        # on coming back into view the trip counts as a miss, and the belief is corrected
        agent.x, agent.y = 6, 6
        agent._look_for_food(world, rng)
        self.assertEqual((agent.trips, agent.trip_hits), (1, 0))
        self.assertEqual(agent.memory.beliefs[(3, 3)].amount, 0.0)

    def test_trip_to_real_food_counts_as_hit(self) -> None:
        world = barren_world()
        world.cell(3, 3).food = 8.0
        agent = hungry_agent(0, 0)
        agent.PERCEPTION_NOISE = 0.0
        rng = random.Random(1)
        agent._look_for_food(world, rng)
        agent.x, agent.y = 15, 15
        agent._recall_food()
        agent.x, agent.y = 6, 6
        agent._look_for_food(world, rng)
        self.assertEqual((agent.trips, agent.trip_hits), (1, 1))

    def test_newborn_has_no_memories(self) -> None:
        a, b = hungry_agent(0, 0), hungry_agent(0, 1)
        b.sex = Sex.MALE
        a.memory.observe(1, 1, 5.0, now=0, strength=1.0)
        child = Agent.reproduce(a, b, random.Random(1))
        self.assertEqual(len(child.memory), 0)


if __name__ == "__main__":
    unittest.main()
