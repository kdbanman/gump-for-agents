# research/blast/ref-anatomy: referee of agent `anatomy` (blast of 2026-11-18)

Standing account: see `REVIEW.md` (verdicts on anatomy's claims, the referee's additions). Everything here was
written from `docs/AUTOMATON.md` and `reference/oracle.py` alone; none of anatomy's code was read or run.

- `vessel.py` vessels as graphs (8-layer slab with period lattice (H,K),(0,D); octahedral hull of radius R).
- `fd.c` bit-sliced graph stepper, 256 replicas, with face-death bookkeeping (tallies + windows).
- `validate.py` state-for-state check against the oracle; results in `validate.out` (all three vessels identical
  for 1,100 generations, replica 0 and 201; the graph with one swapped neighbour fails at generation 1, 2, 10).
- `run.sh` the production runs (one core, 9 minutes); `analyse.py NAME` every number in `out/NAME.txt`.
- `data/returnmap.csv` the return map of the face population (vessel, p, n, mean next, variance next, ...).
