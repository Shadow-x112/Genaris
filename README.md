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

This runs Slice 0: ~15 agents on a 30x30 grid, each with a tiny heritable
genome, for 60 simulated days. It prints a daily summary and every death
event. Right now nobody should die (food is abundant) -- that's fine; the
point of Slice 0 is "does a tiny population survive on its own", not
"watch things die interestingly" yet.

## Project layout

- `src/genaris/genome.py` -- heritable traits + inheritance/mutation
- `src/genaris/world.py` -- the grid, terrain, food regrowth
- `src/genaris/agent.py` -- a single tracked inhabitant's needs/behavior/death
- `src/genaris/simulation.py` -- the tick loop and event log
- `src/genaris/main.py` -- entry point / demo runner
- `docs/` -- the full world-law doctrine and concept brief (reference
  material for later slices, not a checklist to implement all at once)

## Status

**Slice 0: agents that survive.** No magic, no reproduction, no language,
no visualization yet. See `CLAUDE.md` for the phased roadmap.
