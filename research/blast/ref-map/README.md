# ref-map: referee of "the rimmed price is the Gaussian fade action of the measured two-layer map"

Standing account. The verdicts and numbers are in `REVIEW.md`. Nothing here used `ref-anatomy`'s code; only its `THEORY.md`.

- `build_vessel.py`: vessel graphs (hull of radius R; slab of 8 layers with in-plane lattice (1,K),(0,D)), from `docs/AUTOMATON.md`.
- `gs.c`: B45/S345 on a vessel graph, 64 replicas bit-sliced; tallies n and the moments of (P′, B′) per cell (P, B) for
  every face, for two definitions of B (d=0 the whole layer beneath, d=1 on a hull only its part under the face).
- `validate.py` → `validate.out`: `gs` is identical to `reference/oracle.py`'s `step` state for state for 1,100
  generations on hull 9, 11, 13 and the 63-cell torus (two replicas each); one swapped neighbour fails within 14 generations.
- `run.sh`: the tallies (one core, about 12 minutes unloaded) → `research/scratch/blast/ref-map/{h9,h11,h13,t63}.tal`.
- `dp.py`: the Gaussian chain: minimum action by value iteration, route, exact ln τ by power iteration; extrapolation rules.
- `hullsum.py` → `out/hullsum.txt`: the three hull sizes under every rule; prices from differences.
- `box.py`: the jump's one-step law from the launch box on the torus.
- `PREDICTIONS.md`: forecasts frozen before the tallies were analysed (commit 5d9d07c), scored in `REVIEW.md`.
