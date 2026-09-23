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

## Actual status: Slices 1 (reproduction) and 2 (magic accounting) implemented and run

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

Observed (200-day runs, 8 seeds, ~50s each): population grows from 15 to
a food-limited plateau (roughly 50-155 depending on seed; never extinct,
never unbounded), reaches generation 12-13, starvation is the main death
cause. Across all 8 seeds mean metabolism falls (~1.0 -> 0.81-0.91) and
mean speed and max_energy rise -- consistent selection, not scripted.

**Magic (Slice 2), `magic.py`:** free energy per grid cell, generated at
fixed regional rates (baseline + 3 seeded hotspots), spreading between
neighbors (closed world edges), absorbed into terrain matter up to a
per-terrain capacity and leaking back. Terrain-only storage -- agents do
not hold or sense magic, and it has no effect on anything yet. The field
starts at zero. A ledger enforces `free + bound == initial + generated`
after every update and raises `MagicAccountingError` rather than clamping.
No sinks exist, so the total grows linearly forever -- doctrine-correct
for this slice, not a bug. Strain (Section 6) is deferred: there is no
magical activity to cause it. Magic uses its own seeded stream
(`"magic:{seed}"`), so agent outcomes per seed are unchanged by it.

Tuning (current `MagicConfig` placeholders): slow diffusion (0.0002) and
large terrain stores (grass 500 / empty 150) so regions stay distinct and
stores fill over months. Observed at day 200 (2 seeds): stores ~66% full,
richest/poorest free-energy ratio ~27-31x. The first tuning (diffusion
0.005, stores 50/15) saturated stores by day 25 and flattened the map to
~1.2x. Note: with no sinks, both effects are only delayed, never
prevented -- free energy rises forever, so stores eventually fill and the
*ratio* between regions drifts toward 1 (the absolute gap stabilizes).

Code layout:
- `src/genaris/genome.py` -- heritable traits, inheritance + mutation
- `src/genaris/world.py` -- grid, terrain, food regrowth
- `src/genaris/magic.py` -- magic field, terrain storage, ledger
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
- **Slice 3:** memory & beliefs (doctrine Sections 18/19) -- agents start
  remembering things and can be wrong.
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
