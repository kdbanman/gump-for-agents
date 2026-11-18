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
cells share cells beneath (the cube lemma), which this model drops; S outlives gump's wrapped faces by 1.8–2.6 nats
at 27–48 cells (claim 8), so **S is a model of the mechanism, not of gump's constant**.

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

Labels: **[proved]**, **[measured]** (exact = `qsd.c`, 10+ digits; MC = `mc.c`, ± standard error), **[conjectured]**.
Everything below is about the surrogate S at (0.44, 0.42) unless gump is named.

1. **[proved] The tilt identity (THEOREMS.md, Theorem 2).** With ε_i(x) = −ln P(cell i is dead next | x) and
   E = Σ_i ε_i: ln τ = ∫₀¹⟨E⟩_s ds = Σ_i c_i, c_i = ∫₀¹⟨ε_i⟩_s ds, ⟨·⟩_s the mean under μ_s ∝ μ e^{−sE} (μ the
   quasi-stationary law; μ₁ the last living state). So ln τ is *exactly* a sum of local costs: one price per
   orientation on a wrapped face at every size, an exact price map on a rimmed one. Checked to 12 digits on every
   shape (`./qsd g 0.44 0.42 4000 2e-12 0 tilt`, lines `tilt_sum_ci`, `price_map`). Corollaries [proved]:
   ⟨E⟩₁ ≤ ln τ ≤ ⟨E⟩₀ ≤ 2.509·A (Theorem 1, the upper bound B1; 2.079·A at fair coins).
2. **[proved, conditional] One bulk price (Theorem 3, the brief's B4).** If the local means ⟨ε_i⟩_s depend on the far
   geometry only up to K e^{−r/ξ}, uniformly in s ∈ [0,1] (hypothesis SSM, not proved), then
   |ln τ − c_∞A| ≤ K Σ_i e^{−r_i/ξ}: the same c_∞ for wrapped and rimmed faces, loops enter as a discount per
   cell (additive over loop vectors at first order), a rim as a term linear in its length, and a discount growing
   like length² at fixed girth cannot persist. SSM fails exactly when the tilted family has two coexisting kinds
   of face at one tilt. Finding 4 says it does.
3. **[measured, exact] 25 small faces solved** (`data/exact.csv`, `data/report.txt`; `python3 table.py run 25 0.44 0.42`).
   At equal area the order is not gump's and not monotone in anything simple:

   | cells | wrapped faces (ln τ) | free strips, periodic along | free rim all round |
   |---|---|---|---|
   | 9 | (1,0),(0,3): 3.3935247191; (1,1),(0,3): 2.6946266059 | 1×3: 2.7988780569 | triangle R=3: 2.4837157463; patch 1×3: 1.8804189341 |
   | 12 | (1,0),(0,4): 4.1330124063; (2,0),(0,2): 3.9818365883; (1,1),(0,4): 3.7118338988 | 2×2: 4.4893195856; 1×4: 2.6373948650 | patch 2×2: 3.3854987010 |
   | 15 | (1,0),(0,5): 4.6335254447; (1,1),(0,5): 4.3871947401 | 1×5: 2.4517229018 | patch 1×5: 2.0388020889 |
   | 18 | (1,0),(0,6): 4.9945459981; MC (1,1),(0,6): 5.104 ± 0.007; (2,0),(0,3): 5.338 ± 0.007 | 2×3: 6.1754024793; 3×2: 5.8253390091; 1×6: 2.3062451767 | triangle R=5: 4.2316548327; patch 2×3: 4.4727866504 |

   - Free strips one unit cell wide are **subcritical**: ln τ falls with length (2.80, 2.64, 2.45, 2.31) and so does
     the density (0.60 → 0.30). Any block argument for a lower bound needs blocks ≥ 2 unit cells wide.
   - A straight free rim **lengthens** life (strips 2×2, 2×3, 3×2 outlive every wrapped face of equal area: the rim
     face is fuller, density 0.56–0.62 against 0.39–0.52, because a rim row cannot be overcrowded); **corners shorten it** (patches and
     triangles are below the wrapped faces).
   - Exact price map of the 18-cell triangle (`tilt`): corners 0.0234, rim cells next to a corner 0.2164, mid-rim
     0.3007, interior 0.3530 (sum 4.2316548327 = ln τ). Occupancies: corners 0.098, mid-rim 0.614, interior 0.547:
     a fuller rim row and nearly empty corners, as in gump (+0.061; 0.175), from the cap alone.
   - Deaths come from 1, 2, 3 live cells in the proportions 57–79%, 5–24%, 0–5% over the shapes at least two
     unit cells wide (gump: 62, 24, 9); the
     quasi-stationary tail is not log-concave near zero (p₂/p₁ = 1.0–1.6 rising to 1.5 at n = 4–5 on the 18-cell
     triangle), i.e. straight or convex in ln p_n, the signature of two kinds of face.
4. **[measured, exact] Two routes to death, with gump's shape dependence** (`./qsd g 0.44 0.42 4000 2e-12 0 - bust`;
   `data/routes.txt`). Share of the quasi-stationary death flux whose last 6 generations contain a fall of at least
   half the face in one generation (in brackets: the same event for a face merely alive at the end of the window):

   | cells | wrapped | tube girth 1 | strip, two free rims | free rim all round |
   |---|---|---|---|---|
   | 9 | (1,1),(0,3): 0.9369 (0.2675) | | | triangle: 0.0170 (0.0063) |
   | 12 | (2,0),(0,2): 0.5675 (0.1931); (1,1),(0,4): 0.7909 (0.2716) | 0.4466 (0.1671) | 2×2: 0.2875 (0.0910) | patch 2×2: 0.0196 (0.0080) |
   | 15 | (1,1),(0,5): 0.8177 (0.1718) | | | |
   | 18 | MC (1,1),(0,6): 0.811; (2,0),(0,3): 0.712 | | MC 2×3: 0.197 | triangle: 0.0030 (0.0009) |
   | 21–36, MC ± 0.003–0.008 | 0.740 (21), 0.679 (27), 0.639 (30), 0.558 (36) | | 3×3: 0.252; 2×5: 0.014 | triangle 30: 0.0021; rim at face density: 0.023 |

   (`mc.c` reproduces the exact shares: 0.5693 against 0.5675 on the 12-cell torus; `data/mc_routes.csv`.)
   Agent `anatomy` measured in gump 0.57–0.60 on wrapped faces of 48–75 cells and 0.016–0.022 on hull faces.
   **So boom-and-bust on wrapped faces and starvation on rimmed ones is a property of the cap and the layer's
   lattice: it is there with private coins beneath and no chaos at all.** A face whose rim cannot be overcrowded
   has no bust branch.
5. **[measured] Two branches of one killed chain, and what they do to a tube.** h = h_bust + h_starve; with p the
   bust share, d ln τ/dA = p c_b + (1−p) c_s and d² ln τ/dA² = −p(1−p)(c_b − c_s)² (+ terms from c′; THEOREMS.md,
   Lemma R [proved]). On the surrogate's tube (1,1),(0,D) (loop² 3, 3 cells per unit) the bust share falls
   0.818 (D=5, exact), 0.81, 0.758, 0.713, 0.636, 0.577, 0.494, 0.417, 0.339 (D = 14): ln odds falls by 0.29 per
   unit of length. The step of ln τ per unit falls with it: 0.847 (7→8), 0.800, 0.745, 0.746, 0.710, 0.694
   (12→13), each ± 0.008–0.010 (MC, 2·10⁴–4·10⁴ deaths), and step − p·0.29 is 0.63, 0.60, 0.57, 0.59, 0.58, 0.58: constant from D = 8 on.
   **A tube price that falls with length is, in the surrogate, the crossover from the bust branch (0.29 per cell)
   to the starve branch (0.19 per cell)**, a discount that looks like length² over D = 7–14 and must saturate
   (Theorem 3 (d) agrees). Wide wrapped faces show the same drift more slowly (bust share 0.74 → 0.56 from 21 to 36
   cells, c_b − c_s ≈ 0.054 per cell). In gump the wide tori's share *rises* slowly (0.572, 0.590, 0.601 at 48, 63,
   75 cells: c_s − c_b ≈ 0.004 per cell), so there the two branches are nearly degenerate; **"two prices = two
   branches" as the whole account of 0.231 against 0.209 is refuted by that number** (it would need the share's
   log-odds to rise by 0.022 per cell). What survives is the test R9 of PREDICTIONS.md for gump's long tubes.
6. **[measured] Rimmed against wrapped, and what holds the rim.** Triangles over the same coins as the interior are
   *shorter*-lived than wide wrapped faces: 4.2317 (exact) against 5.10–5.34 at 18 cells; 6.889 ± 0.005 against
   7.985 ± 0.005 at 30; 10.55 ± 0.03 against ≈ 11.8 at 45. Give the rim's coins that are cells of the neighbouring
   faces' own layers the density of a face (0.5177; `geom.py hull2`, `data/mc_hull2.csv`) and the order turns into
   gump's: 5.549 ± 0.007 at 18 and 8.796 ± 0.008 at 30 cells (+0.81 over the wrapped face; gump: +0.53 at 30), with
   slope 0.271 per cell against the wrapped 0.24–0.25. At 0.58 (gump's fuller rim row): 6.539, 10.093.
   **In the one-layer surrogate "rimmed > wrapped" is the second face holding the rim** (rim cells have two of
   their three cells beneath in another face's layer), not the absence of loops. [conjectured for gump]
7. **[measured] Tubes and loops in S do not have gump's sign at loop² 3–4.** Against the wide line
   ln τ = 0.41 + 0.2524·A (wide classes, 27–48 cells, MC): tubes of loop² 4 are *longer*-lived by 0.39–0.69
   (18–42 cells), of loop² 3 by 0.10–0.31; the girth-one tube is shorter-lived by 0.4 (21 cells) to 3.2 (36) and
   its density falls with length (0.455 → 0.335): its quasi-stationary law is a patch, not a full tube.
   **Additivity over loop vectors and the ρ = ρ∞ − Σf law could not be tested**: exact reach ends at 18 cells
   (loops² ≤ 7), and at 27–48 cells the Monte Carlo errors (0.005–0.09) are of the size of the effects at loop² ≥ 9.
8. **S is not gump's constant.** Wide wrapped faces: 7.298 ± 0.006 (27), 9.445 ± 0.016 (36), 12.51 ± 0.09 (48)
   against gump's 5.50, 7.39, 9.93: slope 0.24–0.25 against 0.209. Private coins make the face too tough; depth
   and shared cells matter for the number, not for the routes.

## Where the brief's questions stand

| question | answer |
|---|---|
| ln τ additive over loop vectors? | first order of an image expansion under SSM (Theorem 3); not testable exactly (reach) |
| ρ = ρ∞ − Σf, discount = κ·f? | not tested |
| rimmed > wrapped > tube in the surrogate? | no: strips > wrapped > triangles over interior coins; triangles > wrapped once a second face holds the rim; short tubes > wide |
| tube discount ∝ length²? | reproduced over D = 7–14 on one tube family and explained as a two-branch crossover that saturates |
| exact tail, prefactor, path to death | tail not log-concave near 0; most deaths from one live cell; two routes (bust, starve) with exact shares; prefactors not fitted |
| B1 upper bound | proved (Theorems 1, 2): ln τ ≤ ⟨E⟩₀ ≤ 2.509 A |
| B2 lower bound | not proved; block must be ≥ 2 unit cells wide; the block game is stated, not run |
| B3 inequalities | none proved; three natural ones refuted exactly |
| B4 structure | proved under SSM; SSM is expected to fail where the two branches cross |
| two-layer surrogate | exact product needs 2A + frontier bits: beyond 6–9 face cells; only by sampling (`research/theory/exponent/xp.py`) |


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
