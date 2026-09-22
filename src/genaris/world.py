"""
The physical world: a small grid of terrain cells. Deliberately crude --
constant climate, two terrain types, simple food regrowth. This stands in
for Sections 33/34 (ecology, weather) at the lowest possible fidelity, on
purpose: refine only once something actually depends on the extra detail.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum


class Terrain(Enum):
    EMPTY = "empty"
    GRASS = "grass"


@dataclass
class Cell:
    terrain: Terrain
    food: float  # 0..max_food. Only meaningful for GRASS cells.
    max_food: float = 10.0
    regrow_rate: float = 0.15  # food regrown per tick while below max


class World:
    def __init__(self, width: int, height: int, rng: random.Random, grass_fraction: float = 0.55):
        self.width = width
        self.height = height
        self.rng = rng
        self.grid: list[list[Cell]] = []
        for _y in range(height):
            row = []
            for _x in range(width):
                if rng.random() < grass_fraction:
                    row.append(Cell(terrain=Terrain.GRASS, food=rng.uniform(2.0, 10.0)))
                else:
                    row.append(Cell(terrain=Terrain.EMPTY, food=0.0))
            self.grid.append(row)

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    def tick(self) -> None:
        """Regrow food on grass cells. No weather, no seasons yet -- a flat
        constant rate everywhere, deliberately (doctrine Section 34 exists
        for later, richer versions of this)."""
        for row in self.grid:
            for c in row:
                if c.terrain is Terrain.GRASS and c.food < c.max_food:
                    c.food = min(c.max_food, c.food + c.regrow_rate)

    def nearby_food_cells(self, x: int, y: int, radius: int) -> list[tuple[int, int, float]]:
        """Cells within `radius` (Chebyshev distance) that currently have
        food, sorted nearest-first. This models an agent's local awareness,
        not omniscient knowledge of the whole map."""
        found = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if not self.in_bounds(nx, ny):
                    continue
                c = self.cell(nx, ny)
                if c.terrain is Terrain.GRASS and c.food > 0.5:
                    found.append((nx, ny, c.food))
        found.sort(key=lambda item: abs(item[0] - x) + abs(item[1] - y))
        return found
