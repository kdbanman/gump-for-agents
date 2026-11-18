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
- `dying.py` → `out/dying.txt`: how gump's own faces die (last 24 generations of every dying face, dumped by `gs` under `GS_DUMP`).
- `PREDICTIONS.md`: forecasts frozen before the tallies were analysed (commit 5d9d07c), scored in `REVIEW.md`.

## Results in one screen (details, errors and commands in `REVIEW.md`)

- [measured] My ln τ: hull 30, 45, 63, 84 cells 6.780 ± 0.002, 9.818 ± 0.002, 13.659 ± 0.010, 18.157 ± 0.091; torus 63 cells
  13.171 ± 0.018 (`sh run.sh`, then the header line of each `.tal`).
- [computed] Hull minimum action with each size's own map, B = whole layer beneath: 6.275, 10.182, 14.640 (± 0.01, 0.01,
  0.05; independent of the extrapolation rule) and 18.8–19.8 at 84 cells (rule-dependent). S/A = 0.209, 0.226, 0.232,
  0.224–0.236. Increments per cell 0.2605, 0.2477, 0.197–0.248; gump's 0.2010, 0.2119, 0.2147.
  `python3 hullsum.py 7,9,11 visited:200 visited:50 nearest:200 poly2:200`; `python3 hullsum.py 9,11,13 <rules>`.
- [computed] Second-difference price on (30,45,63): 0.184 ± 0.019 with linear term +1.15 ± 0.29 (gump on the same sizes:
  0.266, −0.98). `python3 staterr.py 200 0 h7 h9 h11`.
- [computed] With B = the part of the layer beneath under the face, the hull's cheapest route is a jump and a crash at every
  size; at 84 cells it ties with the fade even for the whole layer. `python3 dp.py <tal> 1 visited 200`;
  `DP_PCAP=46 python3 dp.py 'h13.tal+h13b.tal' 0 carry 50 h11.tal` against the same without `DP_PCAP`.
- [computed] Torus 63 cells: S = 10.116 (0.1606 per cell), route (33,25) → (45,43) → (16,6). `python3 dp.py t63.tal 0 visited 50`.
- [measured] The jump's tail at 63 cells: +0.802 ± 0.027 nats on (46,42). `python3 box.py t63.tal`.
- [measured] Gump's dying faces: torus 63 cells, (33.3, 25.2) → (48.6, 39.7) → (12.1, 9.9) about the last over-full generation,
  which 65.4 ± 1.2% of deaths have in their last 20 generations; hull faces of 30, 45, 63 cells fade (median 9–10 generations
  from the living mode to empty) with the layer beneath at 19–20 of 63, not the chain's 12–13. `python3 dying.py …` (see `REVIEW.md` (f)).
- Tallies are under `research/scratch/blast/ref-map/` (ignored by git); `sh run.sh` regenerates them (same seeds, same numbers).
- Not checked: listed at the end of `REVIEW.md`.
