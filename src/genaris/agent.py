"""
A single tracked inhabitant. Each agent gets hungry, looks for food, eats,
remembers where it found food (and can be wrong about it), ages, seeks a
mate when fed and fertile, and can die. No memory of individuals, no
magic, no language -- those are later slices (doctrine Sections 15-20).
"""
from __future__ import annotations

import itertools
import random
from dataclasses import dataclass, field
from enum import Enum

from genaris.foraging import food_score
from genaris.genome import Genome
from genaris.memory import FoodMemory
from genaris.world import World

_id_counter = itertools.count(1)


class DeathCause(Enum):
    STARVATION = "starvation"
    OLD_AGE = "old age"


class Sex(Enum):
    FEMALE = "F"
    MALE = "M"


TICKS_PER_DAY = 24 * 60


@dataclass(frozen=True)
class LifeHistory:
    """Life-stage timing and reproduction costs.

    Kept separate from per-tick behavior constants so the timescale can be
    swapped without retuning foraging/metabolism.
    """

    label: str
    maturity_ticks: int  # age at which reproduction becomes possible
    fertility_end_ticks: int  # age after which reproduction stops
    max_lifespan_ticks: int  # death of old age
    repro_cooldown_ticks: int  # minimum gap between an agent's reproductions
    # absolute energy required to reproduce -- fixed, not relative to max_energy,
    # so a small reserve does not make the bar easier to clear
    repro_energy_min: float = 60.0
    repro_cost: float = 25.0  # energy each parent transfers to the child


# Deliberately compressed so generations turn over within a runnable
# session. NOT a claim about the world's real biology -- a dev profile,
# to be replaced once adaptive time resolution (doctrine Section 23) exists.
DEV_COMPRESSED = LifeHistory(
    label="dev-compressed",
    maturity_ticks=15 * TICKS_PER_DAY,
    fertility_end_ticks=50 * TICKS_PER_DAY,
    max_lifespan_ticks=70 * TICKS_PER_DAY,
    repro_cooldown_ticks=3 * TICKS_PER_DAY,
)


@dataclass
class Agent:
    genome: Genome
    sex: Sex
    x: int
    y: int
    energy: float = 70.0
    age_ticks: int = 0
    alive: bool = True
    death_cause: DeathCause | None = None
    generation: int = 0  # 0 = founder (initialization, not simulated birth)
    parent_ids: tuple[int, int] | None = None
    repro_cooldown: int = 0  # ticks until this agent may reproduce again
    # spatial food memory; newborns start empty, nothing is inherited (Section 14)
    memory: FoodMemory = field(default_factory=FoodMemory)
    trip_target: tuple[int, int] | None = None  # remembered spot currently being walked to
    trip_confidence: float = 0.0  # confidence in that belief when the trip started
    # instrumentation only -- the agent itself never sees these
    trips: int = 0  # trips to a remembered spot that got close enough to see it
    trip_hits: int = 0  # ...where food was actually there
    trip_confidence_sum: float = 0.0
    id: int = field(default_factory=lambda: next(_id_counter))

    # -- tunable constants (Slice 0 defaults; not claimed to be calibrated) --
    BASE_METABOLISM = 0.6  # energy spent per tick at rest, before genome scaling
    MOVE_COST = 0.4  # extra energy spent per tick when moving, before genome scaling
    # How far an agent can see food. Memories form from exactly these
    # observations: memory adds recall, not a wider perception range.
    SIGHT_RADIUS = 4
    MATE_RADIUS = 4  # how far an agent can "see" a potential mate
    STARVE_THRESHOLD = 0.0
    LIFE = DEV_COMPRESSED
    MEMORY_ENABLED = True  # off = Slice 2 foraging (for ablation runs)
    PERCEPTION_NOISE = 0.15  # std-dev of multiplicative error on perceived food amounts; 0 = exact
    FOOD_PRESENT = 0.5  # food amount an agent treats as "there's food here"

    @property
    def max_energy(self) -> float:
        return 100.0 * self.genome.max_energy

    def can_reproduce(self) -> bool:
        life = self.LIFE
        return (
            self.alive
            and life.maturity_ticks <= self.age_ticks < life.fertility_end_ticks
            and self.repro_cooldown == 0
            and self.energy >= life.repro_energy_min
        )

    def tick(
        self,
        world: World,
        rng: random.Random,
        occupancy: dict[tuple[int, int], list["Agent"]] | None = None,
    ) -> None:
        """`occupancy` maps cell -> agents there, as of the start of this
        tick. It is what the agent can perceive of others; it goes slightly
        stale as agents move during the tick, which is acceptable."""
        if not self.alive:
            return

        self.age_ticks += 1
        if self.repro_cooldown > 0:
            self.repro_cooldown -= 1

        # --- decide and act ---
        cell = world.cell(self.x, self.y)
        hunger_ratio = 1.0 - (self.energy / self.max_energy)
        is_hungry = hunger_ratio > 0.35

        moved = False
        if is_hungry:
            seen = self._look_for_food(world, rng)
            if seen:
                # food in sight (this cell included): weigh perceived amount
                # against distance. Any trip to a remembered spot that hasn't
                # come into view yet is abandoned.
                self.trip_target = None
                # seen is nearest-first, so max() breaks ties toward nearer
                tx, ty, _amount = max(
                    seen,
                    key=lambda c: food_score(c[2], max(abs(c[0] - self.x), abs(c[1] - self.y))),
                )
                if (tx, ty) == (self.x, self.y):
                    # eat: convert local food into energy. Eating is contact,
                    # not sighting, so the bite uses the true amount.
                    bite = min(cell.food, 3.0)
                    cell.food -= bite
                    self.energy = min(self.max_energy, self.energy + bite * 4.0)
                    if self.MEMORY_ENABLED:
                        # what matters is encoded more strongly (Section 18)
                        self.memory.observe(
                            self.x, self.y, self._perceive(cell.food, rng), self.age_ticks, FoodMemory.ATE_STRENGTH
                        )
                        self.memory.forget(self.age_ticks)
                else:
                    self._step_toward(tx, ty, world)
                    moved = True
            elif (target := self._recall_food()) is not None:
                # nothing in sight: head for the best remembered spot
                self._step_toward(target[0], target[1], world)
                moved = True
            else:
                self._wander(world, rng)
                moved = True
        else:
            mate = self._nearest_mate(occupancy) if occupancy and self.can_reproduce() else None
            if mate is not None:
                # fed and fertile: approach the nearest eligible partner;
                # once adjacent, stay put (pairing happens in Simulation)
                if max(abs(mate.x - self.x), abs(mate.y - self.y)) > 1:
                    self._step_toward(mate.x, mate.y, world)
                    moved = True
            elif rng.random() < 0.5:
                # otherwise wander occasionally, rest otherwise
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
        elif self.age_ticks >= self.LIFE.max_lifespan_ticks:
            self.alive = False
            self.death_cause = DeathCause.OLD_AGE

    def _perceive(self, true_amount: float, rng: random.Random) -> float:
        """Direct observation is not exact (Section 17). Noise is small and
        uncoupled from distance or anything else, deliberately."""
        if self.PERCEPTION_NOISE <= 0.0:
            return true_amount
        return max(0.0, true_amount * (1.0 + rng.gauss(0.0, self.PERCEPTION_NOISE)))

    def _look_for_food(self, world: World, rng: random.Random) -> list[tuple[int, int, float]]:
        """Scan for food within sight, returning perceived (x, y, amount),
        nearest first. Only a hungry agent attends to food (attention
        influences encoding, Section 18), so this is also when memories form."""
        seen = []
        for x, y, true_amount in world.nearby_food_cells(self.x, self.y, self.SIGHT_RADIUS):
            perceived = self._perceive(true_amount, rng)
            if perceived > self.FOOD_PRESENT:
                seen.append((x, y, perceived))
        if not self.MEMORY_ENABLED:
            return seen

        now = self.age_ticks
        # a remembered spot has come into view: score the trip against the truth
        if self.trip_target is not None:
            tx, ty = self.trip_target
            if max(abs(tx - self.x), abs(ty - self.y)) <= self.SIGHT_RADIUS:
                self.trips += 1
                self.trip_confidence_sum += self.trip_confidence
                if world.cell(tx, ty).food > self.FOOD_PRESENT:
                    self.trip_hits += 1
                self.trip_target = None

        seen_cells = {(x, y) for x, y, _ in seen}
        for x, y, amount in seen:
            self.memory.observe(x, y, amount, now, FoodMemory.SEEN_STRENGTH)
        # remembered spots now in view with no food seen: remembered as empty
        for b in self.memory.beliefs_within(self.x, self.y, self.SIGHT_RADIUS):
            if (b.x, b.y) not in seen_cells:
                self.memory.observe(b.x, b.y, 0.0, now, FoodMemory.SEEN_STRENGTH)
        self.memory.forget(now)
        return seen

    def _recall_food(self) -> tuple[int, int] | None:
        if not self.MEMORY_ENABLED:
            return None
        belief = self.memory.best_target(self.x, self.y, self.age_ticks, self.FOOD_PRESENT)
        if belief is None:
            self.trip_target = None
            return None
        if self.trip_target != (belief.x, belief.y):
            self.trip_target = (belief.x, belief.y)
            self.trip_confidence = self.memory.confidence(belief, self.age_ticks)
        return self.trip_target

    def _nearest_mate(self, occupancy: dict[tuple[int, int], list["Agent"]]) -> "Agent | None":
        best, best_dist = None, None
        r = self.MATE_RADIUS
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                for other in occupancy.get((self.x + dx, self.y + dy), ()):
                    if other is self or other.sex is self.sex or not other.can_reproduce():
                        continue
                    dist = max(abs(dx), abs(dy))
                    if best_dist is None or dist < best_dist:
                        best, best_dist = other, dist
        return best

    @staticmethod
    def reproduce(a: "Agent", b: "Agent", rng: random.Random) -> "Agent":
        """Create a child from two eligible parents. Each parent pays
        `repro_cost` energy and the child starts with exactly that sum
        (capped at its own max; any excess is lost) -- no energy is created."""
        life = a.LIFE
        genome = a.genome.inherit(b.genome, rng)
        child = Agent(
            genome=genome,
            sex=rng.choice([Sex.FEMALE, Sex.MALE]),
            x=a.x,
            y=a.y,
            energy=0.0,
            generation=max(a.generation, b.generation) + 1,
            parent_ids=(a.id, b.id),
        )
        for parent in (a, b):
            parent.energy -= life.repro_cost
            parent.repro_cooldown = life.repro_cooldown_ticks
        child.energy = min(child.max_energy, 2 * life.repro_cost)
        return child

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
        return self.age_ticks / TICKS_PER_DAY
