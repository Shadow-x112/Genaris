# Project Genaris — notes for Claude Code

## What this project is

A living fantasy-world simulation built around emergence, not scripted
storytelling: define rules, agents, and pressures, then let history
happen. Long-term goal (stated by the person building this): "a real
living world with sentient beings," humanoid, visually detailed
eventually.

## Read this first

`docs/GENARIS_Consolidated_World_Laws_and_Simulation_Doctrine_V0.md` is
the canonical world-law reference -- 40 sections covering magic, souls,
genetics, cognition, culture, history, etc. `docs/Project_Genaris_Concept_Brief.md`
is the earlier, more readable concept brief.

**Do not try to implement these documents wholesale, and do not reopen
their open questions.** They are reference law for a fully mature version
of this world, years away. Treat them the way a novel's "world bible"
relates to its first chapter: consistent with it, but nowhere near
covering everything in it yet. The single biggest risk to this project is
re-litigating metaphysics instead of writing code -- that is exactly what
happened in an earlier attempt (with a different AI) that produced 600+
lines of doctrine and zero working code.

## Actual status: Slices 1-3 (reproduction, magic accounting, memory) implemented and run

```
cd src && python -m genaris.main
# or: uv run python -m genaris.main

# tests (from repo root; stdlib unittest, no dependencies)
python -m unittest discover -s tests
```

15 founders, tiny heritable genome (metabolism/speed/max_energy), two
sexes, a 30x30 grid with grass/food regrowth, hunger-driven foraging,
mate-seeking, sexual reproduction via `Genome.inherit`, aging, death by
starvation or old age. No dependencies beyond the standard library.

**Timescale:** life stages use the `DEV_COMPRESSED` profile in `agent.py`
(adult at 15 days, fertile until 50, lifespan 70, 3-day birth cooldown).
This is a deliberate dev compression so generations turn over in a
runnable session -- not the world's real biology. Tick is still 1 minute.

Reproduction rules: opposite-sex, both fertile, both >= 60 energy (a fixed
bar -- a bar relative to max_energy selected for *smaller* reserves), off
cooldown, adjacent. Each parent pays 25 energy; the child starts with
that 50 (energy conserved). No gestation, no parental care, no mate
choice yet -- intentionally.

**Foraging:** a hungry agent picks the visible food cell (including its
own) with the best `food_score(amount, distance)` in `foraging.py` --
amount / (1 + distance), no minimum cutoff, so crumbs are still eaten when
nothing better is in range. Hunger has hysteresis: a meal starts at a 35%
energy deficit (`SEARCH_HUNGER_RATIO`) and continues one bite per tick
until 95% of max (`SATIATION_ENERGY_RATIO`), ~9 food per meal every ~48
ticks. Before that, a "meal" was one bite (agents stopped the moment they
were no longer hungry), so no visit could ever empty a cell. Until this fix (found via the Slice 3
ablation) agents walked to the *nearest* cell with any food and spent
ticks on tiny bites, which capped every Slice 0-2 population number at
roughly a third of what the food supply supports.

**Food regrowth:** `regrow_rate = 0.01` per tick, so an emptied cell is
visible again (> 0.5 food) after 50 ticks -- set just above the measured
~48-tick gap between meals. Flat regrowth makes this rate both the
recovery delay *and* the total food supply; they can't be tuned apart.
At the original 0.15, cells refilled in 3.3 ticks and never looked empty.
Now ~44% of grass cells sit below 1.0 food and ~3% of hungry looks find
nothing in sight (was 0%).

Observed (200-day runs, 8 seeds, regrow 0.01): population plateaus at
~18-39 (roughly 25 on average) -- small, so extinction risk over longer
runs is real, though none of 8 seeds went extinct in 200 days.
Generation 10-12; starvation is still the main death cause. Mean
metabolism falls strongly in all 8 seeds (~1.0 -> 0.75-0.82, the
strongest selection so far). Speed rises in 6 seeds and is flat or down
in 2; max_energy is mixed (up in 5, down in 3). History: 50-155 with
the original nearest-crumb forager, ~290-450 after the foraging fix with
one-bite meals and fast regrowth.

**Memory & perception (Slice 3), `memory.py`:** each agent holds up to 8
food beliefs (cell, perceived amount, when, encoding strength, source =
"observed"). Confidence halves per simulated day; eating encodes twice as
strongly as seeing; weakest beliefs are dropped when full. Beliefs form
only while the agent attends to food (hungry and looking, or eating --
Section 18 attention), from the same 4-cell `SIGHT_RADIUS` as live sight:
memory adds recall, not range. When nothing is in sight, the agent walks
to its best remembered spot, scored by the same `food_score` with the
belief's confidence. Spots seen empty are remembered as empty. Perception
has 15% multiplicative noise (`PERCEPTION_NOISE`), uncoupled from
distance; eating uses the true amount. Newborns start with no memories.
Deliberately cut: contradictory memories of one place (a fresh sighting
overwrites -- a simplification, not the architecture; Slice 4 reports
will need observation and report to coexist), episodic memory, memories
of individuals, skills, inference about regrowth. `Agent.MEMORY_ENABLED`
and `PERCEPTION_NOISE = 0` together reproduce pre-Slice-3 behavior
exactly (verified byte-for-byte on the default seed).

Observed (8 seeds x 200 days, on fixed foraging): memory has **no
measurable effect** -- mean population 384 (noise only) vs 380 (noise +
memory), within seed spread; only 0-12 recall trips per run. Cause is
ecological, not memory: grass regrows from empty to "food present" in
3.3 minutes, so every grass cell shows food essentially always (measured
100% of cells; 0 of 35,261 hungry looks found nothing in sight) and
recall never triggers. Memory is built and verified but dormant until
food is patchy in space or time. On the few trips taken, agents departed
at confidence ~1.00 but found food only ~0-50% of the time -- the
confidence/accuracy gap Section 18 predicts. Perception noise also
consistently strengthens selection on metabolism (final mean ~0.86 vs
~0.91 without noise, lower in all 8 seeds).

Code layout:
- `src/genaris/genome.py` -- heritable traits, inheritance + mutation
- `src/genaris/world.py` -- grid, terrain, food regrowth
- `src/genaris/foraging.py` -- `food_score`, the one rule for valuing a food spot
- `tests/test_foraging.py` -- food-choice tests
- `src/genaris/magic.py` -- magic field, terrain storage, ledger
- `src/genaris/memory.py` -- food beliefs, confidence decay, forgetting
- `tests/test_memory.py` -- memory/perception/wrong-belief tests
- `tests/test_magic.py` -- ledger/pathway tests
- `src/genaris/agent.py` -- one inhabitant's needs/behavior/reproduction/death,
  plus the `LifeHistory` profile
- `src/genaris/simulation.py` -- tick loop + event log
- `src/genaris/main.py` -- entry point / demo runner

## The phased roadmap (do not skip ahead)

Each slice should run stably (no crashes, no nonsense state) before the
next one starts:

- **Slice 0 (done):** agents survive -- hunger, foraging, aging, death.
- **Slice 1 (implemented):** reproduction + real genetic inheritance.
- **Slice 2 (implemented):** a minimal magic-energy field -- just the accounting (regional
  generation, storage, leakage per doctrine Sections 3/5/6). No techniques,
  no resonance yet.
- **Slice 3 (implemented; memory dormant in current ecology):** memory &
  beliefs (doctrine Sections 18/19) -- agents remember and can be wrong.
- **Slice 4:** simple signaling -> early language (Section 20).
- Later, in rough order: settlements/culture, the historical archive
  (Section 26), a real visualization, magic techniques/resonance (Sections
  4/8/9), the observer/godlike interface (Section 39).

Ask before starting a slice out of order. A genuinely new design question
that contradicts the doctrine is worth raising; wanting to "just quickly
add" something from a later slice while an earlier one isn't solid is not.

## Graphics / engine -- deliberately not started

The person wants eventually-detailed 3D humanoid visuals (Unreal Engine +
MetaHuman is the planned target, discussed and agreed, not yet built).
This must stay decoupled: the simulation is a standalone Python program
producing state (agent positions/ages/etc.), rendering is a separate
concern that reads that state. Do not introduce Unreal, any game engine,
or any graphics library as a dependency of `genaris/` itself.

Sequencing agreed with the person:
1. Headless Python (Slices 0-2ish) -- no graphics at all. **This is where
   the project currently is.**
2. A crude debug visualization (e.g. pygame or a simple grid print) once
   agents do something worth watching -- fast iteration, not final art.
3. Unreal + MetaHuman -- only once behavior is stable enough to know what
   needs animating/rendering. Species: humanoid, no specific design locked
   in yet, so a flexible base is fine.

Do not jump to step 2 or 3 just because it's asked for in the moment --
check with the person if a request seems to be skipping ahead, per the
"working unattended" judgment call, but default to headless-first.

## Dev environment

Windows machine. Python managed via `uv`. VS Code with Python/Pylance/
Ruff/Jupyter. Git for Windows + GitHub Desktop available. No game engine
installed or needed yet.
