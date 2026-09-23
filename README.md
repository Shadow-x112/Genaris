# Project Genaris

A living fantasy-world simulation, built around emergence rather than
scripted storytelling: define the rules, let history happen.

This repo is intentionally starting **far** smaller than the full design
doctrine (see `docs/`). See `CLAUDE.md` for the full context on why, and
what's deliberately not built yet.

## Run it

No dependencies yet -- pure standard-library Python.

```
uv run python -m genaris.main
```

or, without uv:

```
cd src
python -m genaris.main
```

This runs 15 founding agents on a 30x30 grid for 200 simulated days
(about a minute and a half). Every 5 days it prints a population summary
(sexes, births, generations, average heritable traits) and a magic-field
ledger line, plus every birth and death since the last summary.

Life stages use a deliberately compressed dev timescale (adult at 15 days,
lifespan 70 days) so generations turn over within one run. That is a
development setting, not the world's real biology.

## Tests

```
python -m unittest discover -s tests
```

## Project layout

- `src/genaris/genome.py` -- heritable traits + inheritance/mutation
- `src/genaris/world.py` -- the grid, terrain, food regrowth
- `src/genaris/magic.py` -- magical-energy field, terrain storage, ledger
- `src/genaris/agent.py` -- a single inhabitant's needs/behavior/reproduction/death
- `src/genaris/simulation.py` -- the tick loop and event log
- `src/genaris/main.py` -- entry point / demo runner
- `tests/` -- magic ledger tests
- `docs/` -- the full world-law doctrine and concept brief (reference
  material for later slices, not a checklist to implement all at once)

## Status

- **Slice 0:** agents survive -- hunger, foraging, aging, death.
- **Slice 1:** two sexes, reproduction, genetic inheritance with mutation.
  Population settles at a food-limited level; traits shift under selection.
- **Slice 2:** magical-energy accounting -- regional generation, spreading,
  storage in terrain, and a ledger that must always balance. Nothing uses
  magic yet.

Next is Slice 3 (memory and beliefs). No visualization yet. See `CLAUDE.md`
for the phased roadmap.
