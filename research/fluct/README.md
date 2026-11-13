# Is a face's death just the far tail of its stationary fluctuations?

Fluctuation agent, 2026-11-13. Question from the lead: confined chaos dies by losing outer `{111}` face layers;
the wait is memoryless with ln τ ≈ −0.09 + 0.209·A. Conjecture: death needs no special mechanism — it is the far
tail of the living face's ordinary stationary fluctuations. Tested here directly, by measuring the
quasi-stationary distribution (QSD) of the face population n *all the way to n = 0* together with the death rate,
at sizes where both are reachable, and by brute-forcing symmetric faces up to A = 828 with a new symmetry-reduced,
bit-sliced stepper.

Tags: **[proved]**, **[measured]** (n, error, command), **[conjecture]**. Commands run from the repo root.

## Corrections to the lead's claims (up front)

RESULTS_CORRECTIONS

## Verdict

RESULTS_VERDICT

## Tools (all validated against the engine)

- `fl.c` / `fl.py` — 64·W replicas of gump in the bits of machine words on an arbitrary finite cell graph
  (kernel from `research/peeling/rep.c`), with per-generation weighted layer counts (bit-sliced counters), per-replica
  freezing, soup reseeding, and detection of settled replicas (period 1–2 every generation, any period dividing 840).
  Vessels are exact diagonal hulls (T2). **O_h orbit reduction**: an O_h-symmetric state is stepped on one node per
  orbit (a node's neighbours are the orbits of its representative's 12 neighbours); the side-16 cube is 946 nodes
  instead of ≈45,000 cells, and 64 diversified copies run at ≈3–7×10⁶ replica-generations/s on one core
  (≈30–60× the engine on the same state, per core).
- `validate.py` — **[measured]** bit-exact agreement with `gump run` for 2000–3000 generations, every generation
  (outer-layer count against gump's kymograph) and the final cell set: asymmetric soups R = 11, 19; O_h soups
  R = 27 (cube-centred) and 24 (vertex-centred); the side-16 checkpoint; plus distinct states in distinct lanes
  (W = 2), all 16 group counts against a direct count, and `run_until` freezing. `python3 research/fluct/validate.py`
  → `ALL OK`.
- `qsd.py` — quasi-stationary sampling with restarts (a replica whose face dies is recorded and reseeded; settled
  replicas are reseeded and not counted; states younger than T0 = 200 (asym) / 1000 (sym) generations are not
  measured). Records the face histogram, joint (face, layer below), deaths and exposure (also by age), one-step
  transitions, committor tallies, the last 64 generations before every death. `snap` mode: copies of a snapshot,
  each diversified by one orbit flip, dead replicas replaced by perturbed copies of living ones (Fleming–Viot).
  Resumable (state and tallies saved every 2 min; re-running tops up to the wall-time target).
- `ffs.py` — forward-flux sampling along m = min over faces of n, with clones diversified by one flipped cell
  at depth ≥ D. `clone_corr.py` — do perturbed clones become independent?
- Analyses: `analyze_qsd.py` (rate-function collapse, death flux, committor), `analyze_tail.py` (tail → hazard),
  `coord.py` (is n the coordinate?), `predeath.py` (the last generations), `predict.py` (residence + predictive
  interval for one living state). Run lists: `run_qsd.sh`, `run_sym.sh`, `run_after.sh`.

RESULTS_BODY
