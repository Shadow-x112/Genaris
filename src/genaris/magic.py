"""
Magical-energy accounting, per doctrine Sections 3 and 5 -- just the
bookkeeping. The field generates energy at fixed regional rates, free
energy spreads between neighboring cells, and terrain matter absorbs and
leaks it. Nothing spends it and nothing perceives it yet: no techniques,
no resonance, no strain (Section 6 strain comes from magical activity,
and there is none).

Every change has a named pathway, and a ledger checks that
    free + bound == initial + generated
after every update. There is no cap, no automatic deletion, and no
clamping: with a source and no sinks, the world total grows without
bound, which is the doctrine-correct result for this slice.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

from genaris.world import Terrain, World


class MagicAccountingError(RuntimeError):
    """Raised when the ledger does not balance or a store becomes invalid.
    The run stops rather than silently repairing state."""


@dataclass(frozen=True)
class MagicConfig:
    """Placeholder values, not calibrated (doctrine: explicit versioned
    configuration before a system runs; values require calibration)."""

    update_interval_ticks: int = 10  # doctrine environmental max interval: 10 minutes
    baseline_rate: float = 0.0005  # energy generated per cell per minute everywhere
    hotspot_count: int = 3
    hotspot_peak_rate: float = 0.01  # extra generation per minute at a hotspot's center
    hotspot_sigma: float = 4.0  # hotspot falloff width, in cells
    diffusion_rate: float = 0.005  # fraction of a concentration difference moved per minute per neighbor
    absorption_rate: float = 0.001  # fraction of free energy absorbed per minute into an empty store
    leakage_rate: float = 0.0001  # fraction of bound energy leaked back to the field per minute
    capacity: dict[Terrain, float] = field(
        default_factory=lambda: {Terrain.GRASS: 50.0, Terrain.EMPTY: 15.0}
    )
    tolerance: float = 1e-9  # relative ledger tolerance for floating-point rounding

    def __post_init__(self) -> None:
        dt = self.update_interval_ticks
        # explicit diffusion with up to 4 neighbors is only stable (and
        # never drives a cell negative) if each cell gives away < 100%
        if 4 * self.diffusion_rate * dt >= 1.0:
            raise ValueError("diffusion_rate * update_interval_ticks too large for a stable update")
        if self.absorption_rate * dt > 1.0 or self.leakage_rate * dt > 1.0:
            raise ValueError("absorption/leakage rate * update_interval_ticks must be <= 1")


class MagicField:
    """Free and bound magical energy on the world's grid."""

    def __init__(self, world: World, rng: random.Random, config: MagicConfig | None = None):
        self.config = config or MagicConfig()
        self.width = world.width
        self.height = world.height
        w, h = self.width, self.height

        # regional generation rates, fixed at world generation (Section 3)
        cfg = self.config
        hotspots = [(rng.uniform(0, w - 1), rng.uniform(0, h - 1)) for _ in range(cfg.hotspot_count)]
        self.rate = [[cfg.baseline_rate for _x in range(w)] for _y in range(h)]
        for y in range(h):
            for x in range(w):
                for hx, hy in hotspots:
                    d2 = (x - hx) ** 2 + (y - hy) ** 2
                    self.rate[y][x] += cfg.hotspot_peak_rate * math.exp(-d2 / (2 * cfg.hotspot_sigma**2))
        self.total_rate = sum(sum(row) for row in self.rate)

        self.capacity = [[cfg.capacity[world.cell(x, y).terrain] for x in range(w)] for y in range(h)]
        self.free = [[0.0] * w for _ in range(h)]
        self.bound = [[0.0] * w for _ in range(h)]

        # ledger: the world starts with no magical energy anywhere
        self.initial_total = 0.0
        self.generated = 0.0

    # -- per-tick entry point --

    def tick(self, tick_count: int) -> None:
        if tick_count % self.config.update_interval_ticks == 0:
            self.update(self.config.update_interval_ticks)
            self.check()

    def update(self, dt: int) -> None:
        self._generate(dt)
        self._diffuse(dt)
        self._exchange_with_matter(dt)

    # -- pathways --

    def _generate(self, dt: int) -> None:
        for y in range(self.height):
            row, rrow = self.free[y], self.rate[y]
            for x in range(self.width):
                row[x] += rrow[x] * dt
        self.generated += self.total_rate * dt

    def _diffuse(self, dt: int) -> None:
        """Conservative flux across each shared edge, from a snapshot of
        the field. World edges are closed: nothing flows out of the map."""
        k = self.config.diffusion_rate * dt
        old = [row[:] for row in self.free]
        for y in range(self.height):
            for x in range(self.width):
                here = old[y][x]
                if x + 1 < self.width:
                    flux = k * (here - old[y][x + 1])
                    self.free[y][x] -= flux
                    self.free[y][x + 1] += flux
                if y + 1 < self.height:
                    flux = k * (here - old[y + 1][x])
                    self.free[y][x] -= flux
                    self.free[y + 1][x] += flux

    def _exchange_with_matter(self, dt: int) -> None:
        """Absorption into terrain (slowing as the store fills) and leakage
        back to the same cell's free field. A full store absorbs nothing;
        the excess simply stays free (Section 5 overload, no failure yet)."""
        cfg = self.config
        for y in range(self.height):
            frow, brow, crow = self.free[y], self.bound[y], self.capacity[y]
            for x in range(self.width):
                cap = crow[x]
                bound = brow[x]
                absorbed = 0.0
                if cap > 0.0 and bound < cap:
                    absorbed = cfg.absorption_rate * dt * frow[x] * (1.0 - bound / cap)
                    absorbed = min(absorbed, cap - bound)
                leaked = cfg.leakage_rate * dt * bound
                frow[x] += leaked - absorbed
                brow[x] = bound + absorbed - leaked

    # -- ledger --

    def total_free(self) -> float:
        return sum(sum(row) for row in self.free)

    def total_bound(self) -> float:
        return sum(sum(row) for row in self.bound)

    def imbalance(self) -> float:
        return (self.total_free() + self.total_bound()) - (self.initial_total + self.generated)

    def check(self) -> None:
        expected = self.initial_total + self.generated
        error = self.imbalance()
        if not math.isfinite(error) or abs(error) > self.config.tolerance * max(1.0, expected):
            raise MagicAccountingError(f"ledger imbalance {error!r} (expected total {expected!r})")
        # rounding can leave -1e-15 style residue; anything larger is a real bug
        floor = -self.config.tolerance * max(1.0, expected)
        for name, grid in (("free", self.free), ("bound", self.bound)):
            for y, row in enumerate(grid):
                for x, v in enumerate(row):
                    if not math.isfinite(v) or v < floor:
                        raise MagicAccountingError(f"invalid {name} energy {v!r} at ({x}, {y})")
                    if name == "bound" and v > self.capacity[y][x] * (1 + self.config.tolerance):
                        raise MagicAccountingError(f"bound energy {v!r} exceeds capacity at ({x}, {y})")

    def summary(self) -> str:
        free = self.total_free()
        bound = self.total_bound()
        cap = sum(sum(row) for row in self.capacity)
        cells = [v for row in self.free for v in row]
        return (
            f"magic: free {free:.1f} + bound {bound:.1f} ({100 * bound / cap:.0f}% of capacity) "
            f"= generated {self.generated:.1f}, imbalance {self.imbalance():.2e} | "
            f"free per cell min {min(cells):.2f} max {max(cells):.2f}"
        )
