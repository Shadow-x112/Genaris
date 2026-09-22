"""
A single tracked inhabitant. Slice 0 gives each agent just enough behavior
to have a life worth logging: it gets hungry, looks for food, eats, ages,
and can die. No beliefs, no memory of individuals, no magic, no language --
those are later slices (doctrine Sections 15-20).
"""
from __future__ import annotations

import itertools
import random
from dataclasses import dataclass, field
from enum import Enum

from genaris.genome import Genome
from genaris.world import World

_id_counter = itertools.count(1)


class DeathCause(Enum):
    STARVATION = "starvation"
    OLD_AGE = "old age"


@dataclass
class Agent:
    genome: Genome
    x: int
    y: int
    energy: float = 70.0
    age_ticks: int = 0
    alive: bool = True
    death_cause: DeathCause | None = None
    id: int = field(default_factory=lambda: next(_id_counter))

    # -- tunable constants (Slice 0 defaults; not claimed to be calibrated) --
    BASE_METABOLISM = 0.6  # energy spent per tick at rest, before genome scaling
    MOVE_COST = 0.4  # extra energy spent per tick when moving, before genome scaling
    EAT_RADIUS = 4  # how far an agent can "see" food
    MAX_LIFESPAN_TICKS = 70 * 365 * 24 * 60  # ~70 simulated years at 1 tick/minute
    STARVE_THRESHOLD = 0.0

    @property
    def max_energy(self) -> float:
        return 100.0 * self.genome.max_energy

    def tick(self, world: World, rng: random.Random) -> None:
        if not self.alive:
            return

        self.age_ticks += 1

        # --- decide and act ---
        cell = world.cell(self.x, self.y)
        hunger_ratio = 1.0 - (self.energy / self.max_energy)
        is_hungry = hunger_ratio > 0.35

        moved = False
        if is_hungry:
            if cell.terrain.name == "GRASS" and cell.food > 0.5:
                # eat: convert local food into energy
                bite = min(cell.food, 3.0)
                cell.food -= bite
                self.energy = min(self.max_energy, self.energy + bite * 4.0)
            else:
                # seek nearest known food
                candidates = world.nearby_food_cells(self.x, self.y, self.EAT_RADIUS)
                if candidates:
                    tx, ty, _food = candidates[0]
                    self._step_toward(tx, ty, world)
                    moved = True
                else:
                    self._wander(world, rng)
                    moved = True
        else:
            # not hungry: wander occasionally, rest otherwise
            if rng.random() < 0.5:
                self._wander(world, rng)
                moved = True

        # --- pay upkeep ---
        cost = self.BASE_METABOLISM * self.genome.metabolism
        if moved:
            cost += self.MOVE_COST * self.genome.metabolism / max(0.4, self.genome.speed)
        self.energy -= cost

        # --- check death conditions ---
        if self.energy <= self.STARVE_THRESHOLD:
            self.alive = False
            self.death_cause = DeathCause.STARVATION
        elif self.age_ticks >= self.MAX_LIFESPAN_TICKS:
            self.alive = False
            self.death_cause = DeathCause.OLD_AGE

    def _step_toward(self, tx: int, ty: int, world: World) -> None:
        dx = (tx > self.x) - (tx < self.x)
        dy = (ty > self.y) - (ty < self.y)
        nx, ny = self.x + dx, self.y + dy
        if world.in_bounds(nx, ny):
            self.x, self.y = nx, ny

    def _wander(self, world: World, rng: random.Random) -> None:
        dx, dy = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)])
        nx, ny = self.x + dx, self.y + dy
        if world.in_bounds(nx, ny):
            self.x, self.y = nx, ny

    @property
    def age_days(self) -> float:
        return self.age_ticks / (24 * 60)
