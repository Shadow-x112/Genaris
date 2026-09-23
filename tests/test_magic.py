"""Ledger and pathway checks for the magic field (doctrine Sections 3/5).

Run from the repo root:  uv run python -m unittest discover -s tests
"""
from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genaris.magic import MagicAccountingError, MagicConfig, MagicField  # noqa: E402
from genaris.world import World  # noqa: E402


def make_field(config: MagicConfig | None = None, seed: int = 7) -> MagicField:
    world = World(20, 20, random.Random(seed))
    return MagicField(world, random.Random(seed + 1), config)


class LedgerTests(unittest.TestCase):
    def test_starts_empty(self) -> None:
        f = make_field()
        self.assertEqual(f.total_free(), 0.0)
        self.assertEqual(f.total_bound(), 0.0)
        self.assertEqual(f.generated, 0.0)

    def test_conserved_over_long_run(self) -> None:
        f = make_field()
        for tick in range(1, 20_000):
            f.tick(tick)  # check() runs after every update and raises on imbalance
        self.assertGreater(f.generated, 0.0)
        self.assertAlmostEqual(f.total_free() + f.total_bound(), f.generated, delta=1e-6 * f.generated)

    def test_bound_never_exceeds_capacity(self) -> None:
        f = make_field(MagicConfig(absorption_rate=0.1))  # fast absorption to force saturation
        for tick in range(1, 20_000):
            f.tick(tick)
        for y in range(f.height):
            for x in range(f.width):
                self.assertLessEqual(f.bound[y][x], f.capacity[y][x] * (1 + 1e-9))

    def test_generation_continues_when_abundant(self) -> None:
        f = make_field()
        for tick in range(1, 20_000):
            f.tick(tick)
        before = f.total_free() + f.total_bound()
        f.update(10)
        after = f.total_free() + f.total_bound()
        self.assertAlmostEqual(after - before, f.total_rate * 10, places=6)

    def test_closed_edges_lose_nothing(self) -> None:
        # no generation; put energy in one corner and let it spread
        cfg = MagicConfig(baseline_rate=0.0, hotspot_count=0)
        f = make_field(cfg)
        f.free[0][0] = 1000.0
        f.initial_total = 1000.0
        for _ in range(5_000):
            f.update(10)
        f.check()
        self.assertAlmostEqual(f.total_free() + f.total_bound(), 1000.0, places=6)
        self.assertGreater(f.free[f.height - 1][f.width - 1], 0.0)  # it actually spread

    def test_tampering_is_detected(self) -> None:
        f = make_field()
        for tick in range(1, 1_000):
            f.tick(tick)
        f.free[3][3] += 5.0  # energy from nowhere
        with self.assertRaises(MagicAccountingError):
            f.check()

    def test_negative_store_is_detected(self) -> None:
        f = make_field()
        f.free[0][0] = -1.0
        f.free[0][1] = 1.0  # totals still balance; the negative store alone must fail
        with self.assertRaises(MagicAccountingError):
            f.check()

    def test_unstable_config_rejected(self) -> None:
        with self.assertRaises(ValueError):
            MagicConfig(diffusion_rate=0.05, update_interval_ticks=10)


if __name__ == "__main__":
    unittest.main()
