# blast/rigour: what can be proved, and a surrogate solved exactly

Standing account (agent `rigour`, night of 2026-11-18). In progress; see the commit log for the time of each part.

## Files

- `geom.py`: face-layer graphs (wrapped tori, hull faces, strips, patches) from the offsets of `docs/AUTOMATON.md`.
- `check_graph.py`: the graph against `reference/oracle.py` (one-step images, trajectories, negative control).
- `qsd.c`: exact quasi-stationary law and extinction rate of the one-layer dice surrogate (transfer product).
- `dense.py`: independent dense check of `qsd.c` (A <= 12).

(results follow)
