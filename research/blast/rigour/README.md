# blast/rigour: what can be proved, and a surrogate solved exactly

Standing account of agent `rigour` (night of 2026-11-18). Results, the command behind each number, what was not
checked. Proofs are in `THEOREMS.md`; forecasts in `PREDICTIONS.md`; tables regenerate with `python3 report.py`
(its output at the last commit is `data/report.txt`).

## The surrogate

**S(G): one face layer on gump's rule over private coins.** Cells of one `{111}` layer with their 6 in-layer
neighbours; each generation every cell draws its own three coins (two of density ρ1 for the layer beneath, one of
density ρ2 for the layer below that), b = their sum, n = (live in-layer neighbours) + b, and B45/S345 is applied to
all cells at once. Main densities (0.44, 0.42) (the living means of gump's second and third layers,
`research/theory/exponent.md` §"How a gump face dies"); a second set at (½, ½). A Markov chain on 2^A states with
the empty face absorbing. It is the swarm's "face over independent counts" at depth 1; in gump neighbouring face
cells share cells beneath (the cube lemma), which this model drops, and depth 1 is known to be about a nat
short-lived (board E13), so **S is a model of the mechanism, not of gump's constant**.

- Graphs from the 12 offsets of `docs/AUTOMATON.md` (`geom.py`); **checked against `reference/oracle.py`**: with no
  coins S is the one-layer automaton, and the oracle's torus of side 2n seeded in one layer runs it on the wrapped
  face (n,0),(0,n). `python3 check_graph.py`: 0 mismatches over 2,000 random states and 20,000 trajectory
  generations at 27 and at 48 cells; one swapped neighbour gives 562 and 249 mismatches. [measured]
- Exact solver `qsd.c` (power iteration on the killed chain; the product v ↦ vP done cell by cell on an array of
  2^(A + frontier) entries). **Checked against an independent dense code** (`dense.py`, kernel built by enumerating
  coins, eigenvalues by numpy): h = 1 − λ agrees to 13 digits on five cases of 9 and 12 cells, e.g. hull R = 3 at
  (0.44, 0.42): 8.3432634405108e-02 against 8.3432634405110e-02. `python3 dense.py graph ρ1 ρ2` vs `./qsd graph ρ1 ρ2`.
- **Correction to the brief.** For a *synchronous* product kernel one product costs 2^(A + frontier), not A·2^A:
  the old bits of a cell are needed until all its neighbours are updated. With 6 GB that is 18 cells for wrapped
  faces (27 bits) and 24 for thin ones; a 27-cell torus needs 39 bits. Loop² ≥ 9, where gump's measurements
  live, is out of exact reach in one layer (and a two-layer surrogate doubles the bits: out of reach at 9 cells
  of face). Larger faces of the same chain are sampled by `mc.c`, which reproduces an exact value
  (15-cell torus (1,1),(0,5): 4.3888 ± 0.0022 against 4.3872; density 0.52446 against 0.52439).

## Claims

RESULTS_PLACEHOLDER

## Reproduce

    gcc -O3 -march=native -o qsd qsd.c -lm; gcc -O3 -march=native -o mc mc.c -lm
    python3 check_graph.py                         # graph against the oracle, negative control
    python3 geom.py torus 2 0 2 > t.g; ./qsd t.g 0.44 0.42; python3 dense.py t.g 0.44 0.42
    ./qsd t.g 0.44 0.42 4000 2e-12 0 tilt          # adds the tilt identity, price map, tilt path (Theorem 2)
    python3 table.py run 25 0.44 0.42              # exact rows -> data/exact.csv (minutes; 26-27 bits: 1 GB, longer)
    python3 mcrun.py 0.44 0.42 1.5e9               # Monte Carlo rows -> data/mc.csv
    python3 report.py                              # every table of this README

## Not checked

- No second reader has gone through the proofs of `THEOREMS.md` (Lemma 0, Theorems 1–3). Theorem 3 is conditional
  on (SSM), which is not proved for any model and, by the argument given there, is expected to FAIL at one tilt
  if the quasi-stationary tail is straight over a range of populations that grows with the face.
- `qsd.c` beyond 12 cells is checked only by `mc.c` (one case) and by mass conservation and the identity
  h = Σ μ(x) d(x) computed two ways in every run (`h` and `check_h`).
- Lemma 0 is proved for wrapped faces only; for hull faces and strips uniqueness of the dominant eigenvalue is
  numerical.
- The coins' densities were taken from one table of the earlier study, not re-measured; shared coins (the cube
  lemma) and correlated coins (the brief's second model) were not run.
- Nothing here is a measurement of gump. Every comparison with gump is of signs and orders, not of values.
