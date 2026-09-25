"""Food-choice scoring: amount weighed against distance, no cutoff.

Run from the repo root:  python -m unittest discover -s tests
"""
from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genaris.agent import Agent, Sex  # noqa: E402
from genaris.foraging import food_score  # noqa: E402
from genaris.genome import Genome  # noqa: E402
from genaris.world import Cell, Terrain, World  # noqa: E402


def barren_world(size: int = 20) -> World:
    """No food anywhere and no regrowth, so tests place food exactly."""
    world = World(size, size, random.Random(0))
    for y in range(size):
        for x in range(size):
            world.grid[y][x] = Cell(terrain=Terrain.GRASS, food=0.0, regrow_rate=0.0)
    return world


def hungry_agent(x: int, y: int) -> Agent:
    genome = Genome(metabolism=1.0, speed=1.0, max_energy=1.0)
    agent = Agent(genome=genome, sex=Sex.FEMALE, x=x, y=y, energy=30.0)
    agent.PERCEPTION_NOISE = 0.0  # these tests check the choice rule, not perception
    return agent


class FoodScoreTests(unittest.TestCase):
    def test_more_food_and_closer_both_help(self) -> None:
        self.assertGreater(food_score(9.0, 2), food_score(0.6, 1))
        self.assertGreater(food_score(5.0, 1), food_score(5.0, 3))
        self.assertGreater(food_score(5.0, 1, confidence=1.0), food_score(5.0, 1, confidence=0.5))


class ForagingChoiceTests(unittest.TestCase):
    def test_walks_past_crumb_to_rich_cell(self) -> None:
        world = barren_world()
        world.cell(6, 5).food = 0.6  # one step away, a crumb
        world.cell(7, 5).food = 9.0  # two steps away, a meal
        agent = hungry_agent(5, 5)
        agent.tick(world, random.Random(1))
        self.assertEqual((agent.x, agent.y), (6, 5))  # stepped toward (7, 5)...
        self.assertAlmostEqual(world.cell(6, 5).food, 0.6)  # ...without eating the crumb
        agent.tick(world, random.Random(1))
        self.assertEqual((agent.x, agent.y), (7, 5))

    def test_still_eats_crumbs_when_nothing_better(self) -> None:
        world = barren_world()
        world.cell(5, 5).food = 0.6
        agent = hungry_agent(5, 5)
        before = agent.energy
        agent.tick(world, random.Random(1))
        self.assertEqual((agent.x, agent.y), (5, 5))
        self.assertEqual(world.cell(5, 5).food, 0.0)
        self.assertGreater(agent.energy, before - 1.0)  # gained 2.4 from the crumb, paid ~0.6 upkeep

    def test_leaves_crumb_underfoot_for_rich_neighbor(self) -> None:
        world = barren_world()
        world.cell(5, 5).food = 0.6  # underfoot: score 0.6
        world.cell(6, 5).food = 9.0  # adjacent: score 4.5
        agent = hungry_agent(5, 5)
        agent.tick(world, random.Random(1))
        self.assertEqual((agent.x, agent.y), (6, 5))
        self.assertAlmostEqual(world.cell(5, 5).food, 0.6)

    def test_eats_rich_cell_underfoot(self) -> None:
        world = barren_world()
        world.cell(5, 5).food = 9.0  # underfoot: score 9
        world.cell(6, 5).food = 10.0  # adjacent: score 5
        agent = hungry_agent(5, 5)
        agent.tick(world, random.Random(1))
        self.assertEqual((agent.x, agent.y), (5, 5))
        self.assertAlmostEqual(world.cell(5, 5).food, 6.0)


class MealTests(unittest.TestCase):
    """Hunger hysteresis: a meal runs from 'hungry' to 'satiated'."""

    def test_keeps_eating_past_unhungry_until_satiated(self) -> None:
        world = barren_world()
        world.cell(5, 5).food = 10.0
        agent = hungry_agent(5, 5)
        agent.energy = 60.0  # deficit 0.40 > 0.35: meal starts
        rng = random.Random(1)
        agent.tick(world, rng)  # bite 3 -> ~71: no longer hungry, but still in the meal
        self.assertTrue(agent.feeding)
        agent.tick(world, rng)  # bite 3 -> ~83
        agent.tick(world, rng)  # bite 3 -> ~94, still below 95
        self.assertTrue(agent.feeding)
        agent.tick(world, rng)  # last 1.0 food -> ~98
        self.assertAlmostEqual(world.cell(5, 5).food, 0.0)  # one visit emptied the cell
        agent.tick(world, rng)
        self.assertFalse(agent.feeding)  # satiated: meal over

    def test_meal_ends_at_satiation(self) -> None:
        world = barren_world()
        world.cell(5, 5).food = 10.0
        agent = hungry_agent(5, 5)
        agent.feeding = True
        agent.energy = 96.0  # already at/above 95% of max 100
        agent.tick(world, random.Random(1))
        self.assertFalse(agent.feeding)
        self.assertAlmostEqual(world.cell(5, 5).food, 10.0)  # didn't eat

    def test_no_meal_until_search_threshold(self) -> None:
        world = barren_world()
        world.cell(5, 5).food = 10.0
        agent = hungry_agent(5, 5)
        agent.energy = 70.0  # deficit 0.30 < 0.35: not hungry, not in a meal
        agent.tick(world, random.Random(1))
        self.assertFalse(agent.feeding)
        self.assertAlmostEqual(world.cell(5, 5).food, 10.0)


if __name__ == "__main__":
    unittest.main()
