# research/blast/ref-anatomy: referee of agent `anatomy` (blast of 2026-11-18)

**The standing account is `REVIEW.md`**: verdicts on anatomy's claims (headline not broken; several numbers
corrected), the attack points (a)–(e), and the referee's additions (return maps, autocorrelations, "q depends on
the way down", the hull face's slow population, one live cell by place). Everything was written from
`docs/AUTOMATON.md` and `reference/oracle.py` alone; of anatomy's files only its README was read.

Reproduce: `sh run.sh` (one core, about 10 minutes of wall time; bulk output under
`research/scratch/blast/ref-anatomy/`), then `sh analyse_all.sh` (one minute).

- `vessel.py`: vessels as graphs (8-layer slab with period lattice (H,K),(0,D); octahedral hull of radius R).
- `fd.c`: bit-sliced graph stepper, 256 replicas; modes `trace` (for validation), `run` (lifetimes, joint
  histograms of P(t), P(t+1), P(t+2), excursion tallies, window records of deaths / living faces / over-full
  generations / non-fatal falls), `island` (one live cell left on a face).
- `validate.py`: state-for-state check against the oracle. `validate.out`, `validate_t48.out`, `validate_h45.out`:
  identical for 1,100 generations on every vessel used (several replicas); one swapped neighbour fails.
- `check_windows.py` → `out/check_windows.txt`: 72,000 recorded transitions re-derived in Python from the rule, 0 wrong.
- `analyse.py NAME` → `out/NAME.txt` (every number of the review, each line tagged); `island.py` → `out/island.txt`;
  `twolayer.py` → `out/twolayer.txt` (what the layer beneath adds to the return map).
- `data/returnmap.csv`: vessel, p, n, mean_next, var_next, mean_next2, var_next2 (two generations on),
  p_next_le_quarter (share with P(t+1) ≤ 15·A/63), p_dead_next. `data/autocorr.csv`: vessel, lag, rho, source.
  Vessels: t63 = torus (1,4),(0,21); tube60 = (1,8),(0,20); h63 = hull radius 11; t48 = torus (4,0),(0,4);
  h45 = hull radius 9.
- `PREDICTIONS.md`: forecasts for the hull run (written before its output was read) and their scores.

Not checked: see `REVIEW.md` §5.
