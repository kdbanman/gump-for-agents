# toy2d — is there a 2D gump? (PROGRAM node G1, with G3 in view)

*Toy-2D agent, 2026-11-13. Tags: **[proved]** argument given here (and brute-force checked where said);
**[measured]** with n, error and the command; **[conjecture]**. Commands run from `research/toy2d/`; bulk output
goes to `research/scratch/toy2d/`; curated numbers are in `data/`. Forecasts were committed in `PREDICTIONS.md`
before the symmetric runs.*

## Verdict

**Yes — and the cleanest example is not on the Moore lattice.** On the *cross* neighbourhood
`(±1,0), (±2,0), (0,±1), (0,±2)` ("cross2", the range-2 von Neumann cross, 8 neighbours) the rule **B34/S234** —
"alive next iff n + x ≥ 3, except that a cell with n ≥ 5 dies" — is gump's construction one dimension down:
a symmetric threshold rule plus an overcrowding cap, with births that cannot cross a lattice line. It shows every
item of the 3D story that I could test: confinement to a box that only shrinks; steady chaos inside;
death of a whole edge row after a memoryless wait with **ln τ_edge = 0.73 + 0.416·L** (L = 12–36: τ from 286 to 5.8×10⁶
generations); a population distribution of the living edge whose log-tail is straight down to n = 1 with the
death rate as its next point; a mirror-symmetric edge that dies exponentially sooner; the threshold lemma; and no
finite sealed set. It is also *minimal* in its family exactly as gump is in its: of the capped thresholds
B3…/S2… on cross2 only the cap at 5 lives (B3/S2, B3/S23, B345/S2345 … all settle), as gump is a
minimal member of its own rule neighbourhood.

On the **Moore** lattice the phenomenon exists but is not "gump": confinement forces birth ≥ 4 of 8, a *majority*
threshold, and no capped-threshold Moore rule sustains confined chaos (all five die or settle; B456/S3456 is chaotic
on a torus but its edges erode). 93 of the 711 longest-lived Moore rules do die edge by edge (class EDGE below);
they all need survival at low counts (S2, usually S1 too) or holes in S at 5/7 — exceptions to any threshold rule
that the cap alone does not supply. The best-measured one, **B45/S23467**, has a clean law at L ≥ 24
(ln τ = 4.32 + 0.259·L) but a curved tail near n = 1. Why the Moore lattice is the wrong 2D analogue is a
one-line count (§2): a lattice line holds only 2 of the 8 Moore neighbours, so confinement needs birth ≥ ½ of the
neighbourhood; gump's {111} plane holds 6 of 12 and the cross holds 4 of 8, which is what lets the threshold sit at
about a third.

## 1. Method

- **Stepper** `t2d.c`: 256 replicas in the bits of 4 machine words per cell, any cell graph (dead-forever
  neighbours = index N), any outer-totalistic rule (bit-sliced neighbour count, then the B/S terms).
  Modes `life` (soups to settling), `qsd` (quasi-stationary sampling with restarts, as `research/fluct/qsd.py`),
  `trace`. Settling = period ≤ 2 (every generation) or equality with a snapshot taken every 64 / 4096 generations
  (periods ≤ 4096). `validate.py` → **ALL OK**: population and every watched line count, every generation for 300
  generations, plus the final state, against a numpy stepper, for 8 rule/lattice/vessel/symmetry cases.
- **Vessels** (`geom.py`): L×L boxes and W×L strips periodic in x (rows outside dead forever — exact by
  confinement, §2). *Events* end a replica's residence: an edge row empty (a peel), an interior run of
  firewall-width dead rows, and — added after it bit me, see §4.4 — a transverse run of dead columns that cuts the
  periodic strip open. Symmetric soups: the soup is drawn once per orbit of the symmetry and the dynamics keeps it.
- **QSD** (`law.py`, `analyze.py`): 256 replicas, soup p = 0.4, states younger than T0 = 300 not measured; a
  replica that dies or settles is reseeded. h = edge deaths / (2·exposure) per edge per generation, τ_edge = 1/h,
  error of ln τ = 1/√deaths. Ages at death → CV; hazard in log₂ age bins; histogram of the edge-row population
  pooled over both edges → p_k.
- **Search** (`search.py`, `screen.py`, `classify.py`): stage 1, every rule B ⊆ {b_min..8} (non-empty) × S ⊆ {0..8}
  in a 10×10 box, 256 soups at p = 0.3 and 0.5, cap 4000 (Moore 15,872 rules, cross2 32,256). Stage 2, rules with
  median ≥ 300 in periodic strips W = 10, L = 12 and 20, 20,000 generations × 256 replicas, classified.

## 2. Structure [proved; brute-force checked by `python3 structure2d.py` → ALL OK]

For a lattice direction d write s = d·offset ("layer offset"). A dead cell one layer outside a half-plane sees at most
c live cells; births ≥ c + 1 cannot cross (T2 analogue). Firewall = fewest consecutive dead layers that stay dead
whatever lies on both sides (T3 analogue).

| lattice | K | layer histogram (axis lines) | c | b_min | threshold fraction (b_min − ½)/K | confining lines | firewall |
|---|---|---|---|---|---|---|---|
| gump (3D, {111}) | 12 | 1, 2, **6**, 2, 1 | 3 | 4 | 0.29 | 4 diagonal planes (octahedron) | 3 layers |
| **cross2** | 8 | 1, 1, **4**, 1, 1 | 2 | 3 | 0.31 | rows and columns (box) | 3 rows |
| Moore | 8 | 3, **2**, 3 | 3 | 4 | 0.44 | rows, columns and diagonals (octagon) | 2 rows / 3 diagonals |
| hex | 6 | 2, **2**, 2 | 2 | 3 | 0.42 | the 3 line families (hexagon) | 2 rows |
| von Neumann | 4 | 1, **2**, 1 | 1 | 2 | 0.38 | rows and columns (diagonals leak) | 2 rows |

The bold entry is the number of neighbours *in* the confining layer. A threshold rule can only be chaotic well below
majority (Goles–Olivos: the uncapped threshold rule reaches period ≤ 2; a majority threshold coarsens), and the
fraction above is forced up toward ½ unless the layer holds many neighbours. gump's plane holds half its
neighbourhood; on Moore a line holds a quarter. The cross is the 2D neighbourhood with gump's proportions: half
in-layer, reach two layers, firewall three layers, and an edge cell sees 6 of 8 (gump's face cell: 9 of 12).

- **T1–T4 analogues** [proved]: the table; each cross2 row is a closed 1D sub-automaton (a pattern in one row
  stays in it: the next row sees ≤ 1 of it), and a single row freezes (median 2 generations, `geom.life` on a
  1×64 strip).
- **T5 analogue** [proved; identity checked]. Any outer-totalistic rule is a symmetric threshold rule "n + x ≥ t"
  plus a set of *exceptions* (x, n). With E(t) = −x(t)ᵀ(A + I)x(t−1) + (t − ½)(|x(t)| + |x(t−1)|), the derivation of
  `research/theory/threshold.md` §2 goes through unchanged (it uses only the symmetry of A): **ΔE = D − Q exactly**,
  drive D only at exception cells (rule says 0 where the threshold says 1 and the cell was live two steps before, or
  rule says 1 where the threshold says 0 and it was dead), Q ≥ 0 elsewhere. So no exception events ⇒ period ≤ 2.
  For cross2 B34/S234 the exceptions are exactly the overcrowded cells n ≥ 5 (the cap) — the precise analogue of
  gump. `python3 energy2d.py B34/S234 cross2 24 3 3000` → 0 violations in 3000 generations, drive events
  **0.114 per cell-generation** (box), and on a 128² torus `python3 bulk2d.py B34/S234 cross2 3` → 0.119 (gump bulk:
  0.115). For Moore B45/S23467 the exceptions are (live, 2) (survival below threshold), (live, 5), (live, 8) and
  (dead, ≥ 6): T5 holds but "drive only at overcrowded cells" does not — undercrowded survival also drives.
- **T6 analogue** [proved]. Sealed = every cell has ≤ b_min − 1 neighbours outside the set. *No finite set is sealed
  in Z²* for Moore (b_min 4), cross2 (3) or hex (3): the cell furthest along a generic direction v has all
  K/2 neighbours with v·o > 0 outside, and K/2 ≥ b_min. (Brute force: no sealed subset of a 4×4 window.) The
  bound is sharp: Moore with b_min 5 seals a discrete octagon (corner cells see exactly 4 outside), so Moore rules
  with B ⊆ {5..8} have permanent finite holes. *In a periodic strip* every finite sealed set contains a whole column
  (take v = (1, ±ε): the furthest cells must have their two in-column neighbours outside the vessel, and any gap
  in that column exposes a cell to ≥ b_min outside), i.e. it is a transverse firewall — the 2D form of "every sealed
  set touches the outside of the hull". Note the difference from 3D: in a slab of any thickness, a band of
  firewall width across the strip *is* finite, whereas gump has no finite sealed set in ≥ 3 layers.

## 3. The search — candidate table

Stage-2 classes (`python3 classify.py ../scratch/toy2d/screen_moore_*.jsonl`; tables `data/moore_classes.csv`,
`data/cross2_classes.csv`, capped-threshold families `data/family_*.csv`):

| lattice | rules | median ≥ 300 at L = 10 | screened | settle | frozen edges ("walled cities") | erode | quiet | **EDGE** |
|---|---|---|---|---|---|---|---|---|
| Moore, B ⊆ {4..8} | 15,872 | 711 | 711 | 434 | 161 | 8 | 15 | **93** |
| cross2, B ⊆ {3..8}, \|B\|+\|S\| ≤ 7 | 32,256 | 5,149 | 439 | 17 | 25 | 0 | 30 | **367** |

EDGE = both edges active (non-period-2 activity ≥ 0.02), edge deaths outnumber firewalls, and τ_edge grows ≥ e-fold
from L = 12 to 20. The screen used W = 10 and no transverse-firewall events, so it is a filter, not a law.

| rule | lattice | τ_edge(12) | τ_edge(20) | slope ln τ / L (12→20) | bulk activity | edge activity | edge density | note |
|---|---|---|---|---|---|---|---|---|
| **B34/S234** | cross2 | 278 | 2.3×10³ | 0.26 (W = 10; 0.42 at W = 16, §4) | 0.35 | 0.31 | 0.51 | capped threshold (θ = 2.5, cap n ≥ 5) — the 2D gump |
| B34/S235 | cross2 | 1.1×10³ | 2.1×10⁴ | 0.37 | 0.46 | 0.46 | 0.56 | |
| B36/S234 | cross2 | 1.1×10³ | 2.1×10⁴ | 0.36 | 0.38 | 0.31 | 0.56 | |
| B3/S0124 | cross2 | 771 | 6.5×10³ | 0.27 | 0.38 | 0.36 | 0.40 | |
| B3/S23, B345/S2345 … B345678/S2345678 | cross2 | — | — | — | | | | the other capped thresholds: all settle |
| **B45/S23467** | Moore | 1.06×10³ | 6.5×10³ | 0.23 | 0.37 | 0.20 | 0.65 | smallest Moore EDGE rule; measured in §5 |
| B45/S234678 | Moore | 4.2×10³ | 4.4×10⁴ | 0.29 | 0.35 | 0.18 | 0.75 | |
| B4567/S34568 | Moore | 3.9×10³ | 7.6×10⁴ | 0.37 | 0.32 | 0.12 | 0.89 | threshold with exceptions only at n ≥ 7 |
| B45678/S34568 | Moore | 1.5×10⁴ | 2.5×10⁶ (4 deaths) | 0.64 | 0.28 | 0.06 | 0.96 | one exception: (live, 7) dies |
| B4/S34, B45/S345, B4567/S34567, B45678/S345678 | Moore | — | — | — | | | | capped thresholds: settle |
| B456/S3456 | Moore | 508 | 163 | < 0 | 0.31 | 0.20 | 0.48 | capped threshold, chaotic on a torus; edges *erode* |
| B46/S2345 | Moore | — | — | — | 0.31 | 0.00 | 0.99 | frozen walls, dies by firewalls ("walled cities" type) |

Observations [measured, same screen]: every Moore EDGE rule has S ⊇ {2, 3, 4} (stage 1: all 331 rules with median ≥ 1000
at L = 10 do); on cross2, EDGE is the *typical* behaviour of a long-lived small rule (367/439). Caveat: stage 1 at
L = 10 can miss rules whose lifetimes only grow at larger L — B34/S234 itself has median ≈ 200 at L = 10 and was
added by hand; I did not re-screen the 15,000 short-lived rules at a larger size.

## 4. The 2D gump: cross2 B34/S234

### 4.1 Edge law [measured]
`python3 law.py B34/S234 cross2 16 12,16,20,24,28,32,36 --deaths 400 --maxsec 900 --tag main` (strips 16 × L);
`python3 analyze.py ../scratch/toy2d/law_cross2_B34S234_W16_none_main.json` (→ `data/law_cross2_B34S234.json`):

| L | edge deaths | τ_edge | ln τ ± | CV | late/early hazard | p₁ | h/p₁ | p₁/p₂ | ln h | straight-tail prediction |
|---|---|---|---|---|---|---|---|---|---|---|
| 12 | 2,693 | 286 | 5.657 ± 0.019 | 1.00 | 0.99 | 6.7×10⁻³ | 0.52 | 0.51 | −5.66 | −5.81 |
| 16 | 4,067 | 1,679 | 7.426 ± 0.016 | 1.02 | 0.99 | 1.3×10⁻³ | 0.45 | 0.44 | −7.43 | −7.57 |
| 20 | 1,086 | 8,564 | 9.055 ± 0.030 | 0.97 | 0.99 | 2.6×10⁻⁴ | 0.45 | 0.39 | −9.06 | −9.29 |
| 24 | 1,046 | 4.75×10⁴ | 10.768 ± 0.031 | 0.99 | 0.94 | 5.8×10⁻⁵ | 0.36 | 0.39 | −10.77 | −10.82 |
| 28 | 898 | 2.35×10⁵ | 12.368 ± 0.033 | 0.97 | 1.02 | 1.3×10⁻⁵ | 0.33 | 0.37 | −12.37 | −12.35 |
| 32 | 676 | 1.27×10⁶ | 14.051 ± 0.038 | 0.94 | 1.02 | 2.8×10⁻⁶ | 0.28 | 0.35 | −14.05 | −13.93 |
| 36 | 495 | 5.84×10⁶ | 15.580 ± 0.045 | 0.96 | 1.00 | — | 0.27 | 0.34 | −15.58 | −15.36 |

- **Length law:** ln τ_edge = (0.729 ± 0.028) + (0.4160 ± 0.0014)·L over L = 12–36 (χ² 28.9/5; L = 20–36 alone:
  0.410 ± 0.003, χ² 6.4/3). With a + IL + b ln L: I = 0.374 ± 0.009, b = 0.87 ± 0.18, χ² 5.8/4 — a mild log
  correction, the same size as gump's intercept terms. **I ≈ 0.41 per edge cell** (gump: 0.208 per face cell).
- **Memoryless:** CV of the residences 0.94–1.02 at every L, late/early hazard 0.94–1.02 (figure, panel c).
- **The death rate is the next point of the straight tail.** ln p_k is straight from k ≈ 5 down to k = 1 and the
  line through the lowest decade, continued to k = 0, predicts ln h to within **0.02–0.23 nats** at all seven sizes
  (gump: 0.06–0.08). h/p₁ tracks p₁/p₂ (0.52/0.51 … 0.27/0.34). Unlike gump, the attempt rate h/p₁ is not
  size-independent: it falls from 0.52 to 0.27 as L grows 12 → 36, together with the tail ratio.
- **End-game:** deaths from n = 1 / 2 / 3: 53 / 27 / 7 % at L = 16, 46 / 33 / 12 % at L = 32 (gump: 62 / 23 / 9 %).
- **Width:** at L = 16, τ_edge = 324, 680, 1,439, 1,664 ± 26, 1,649 ± 26 for W = 6, 8, 12, 16, 24
  (`law.py ... --tag wdep`): converged at W ≥ 16; thin strips also settle (W = 6: 110,513 settles).

### 4.2 Box pictures
`research/figures/toy2d_box.png` (`python3 figures.py`): a 24×24 box, peels at t = 6,855 (left), then the next
column one generation later, 9,531, 14,944 (bottom) …, the last peels in a burst as the edges shorten; final
state at 51,733 (three small debris objects). In 256 boxes (`geom.life`, p 0.5): median total lifetime 2.6×10³,
1.4×10⁴, 6.4×10⁴ at L = 16, 20, 24 (ln ratio 0.40–0.37 per unit L, same as the edge law).

### 4.3 Bulk phase [measured]
128² torus, 2000 generations after 1000 (`bulk2d.py`): density 0.472, mismatch (x(t+1) ≠ x(t−1)) 0.45, drive
events 0.119, overcrowded (n ≥ 5) 35% of cells. Gaps heal: a 32-cell dead stretch cut into a living edge row
(depth 1, 2 or 3 rows) shrinks to the equilibrium longest gap (≈ 8) within 30 generations (`gap.py B34/S234 cross2
32 128 16 64 400 4000 D`); a dead stretch's interior can never be reborn (its cells see ≤ 2), so it closes from
its two ends, which advance into it.

### 4.4 The transverse channel (a correction to my own first run)
Without transverse events, τ_edge at W = 16 *saturated* above L ≈ 28 (ln τ 10.9, 11.2, 11.4, 11.5, 11.7 at
L = 28…48) and a kymograph showed why (`kymo.py B34/S234 cross2 16 64`): the strip had first been cut by three
dead columns (3W = 48 cells; vertical lines confine too), turned into a short box, and lost its short sides. With
those cuts counted as events, they outnumber edge deaths from L ≈ 24–28 at W = 16 (22,252 vs 676 at L = 32). This is
gump's face-versus-firewall competition (firewalls win where the cross-section is smaller than the face): in an
L×L box the cut costs 3L cells against L for an edge, so edges win.

## 5. Symmetry (forecasts in `PREDICTIONS.md`)

All on cross2 B34/S234 (`./run_sym.sh`, plus `law.py ... --vessel box --sym c4 32,36`, `--sym none 32`,
`--sym d4 32`; curated in `data/law_cross2_B34S234_{mx,my,t2,box_*}.json`). τ_first = mean wait for the *first*
edge death of the vessel (lockstep edges count once). Errors on ln τ are 0.015–0.05.

| forecast | measured | verdict |
|---|---|---|
| **F2** translation by L/2 at L = 32 = asymmetric strip at L = 16 (exact) | τ_edge 1,631 ± 25 vs 1,679 ± 26 (Δ ln τ = 0.029 ± 0.023) | **hit** (machinery check) |
| **F1** mirror x → −x (perpendicular to the edges): slope I/2, ratio 0.5 ± 0.1 | strips W = 16, L = 16–56: ln τ = 1.83 + **0.1733 ± 0.0009**·L (χ² 1.5/4) vs 0.410–0.416 asymmetric: ratio **0.42**. Moore B45/S23467: 0.1191 ± 0.0010 (L = 24–56) vs 0.259: ratio **0.46** | **hit, at the low edge**: symmetric edges cost 8–17% *less* per independent cell |
| **F3** mirror y → −y (swaps the two edges): τ_first × 2, slope unchanged | τ_first(my)/τ_first(asym) = 2.22, 2.41, 2.50 at L = 16, 20, 24 | **hit within 25%** (drifting up) |
| **F4** square box with D4: exponent × ½ (not ⅛) | box, ln τ_first = 4.92, 5.60, 6.28, 6.99 at L = 20–32: slope **0.171** vs **0.343** asymmetric: ratio **0.50** | **hit** |
| **F5a** diagonal mirror alone: slope unchanged, τ_first × 2 | ln τ_first 5.44, 6.76, 8.06, 9.41, 10.97 vs 5.39, 6.71, 8.10, 9.40, 10.82 (L = 12–28): slope 0.364 vs 0.340, **ratio of waits ≈ 1.0–1.16, not 2** | **half miss**: exponent unchanged, but each independent edge dies twice as fast as a free one |
| **F5b** C4 alone: slope unchanged, τ_first × 4 | ln τ_first 5.92 … 11.50 at L = 16–36: slope **0.274** vs 0.343, and τ_first(c4)/τ_first(asym) = 0.45, 0.30, 0.18, 0.16 at L = 16, 20, 28, 32 | **miss**: C4 lowers the exponent by ≈ 20% and the wait is *shorter* |

Reading: "symmetry is fatal in proportion to the stabiliser of the dying face" (1/|stabiliser| of the exponent) is
right for the symmetries that fix an edge (mirror ⊥ edge, D4: × ½; gump's O_h: ≈ ⅙). It is wrong as a complete
account: symmetries that fix no edge still shorten life in a box. Small-L symmetric boxes also settle easily
(d4: at L = 12 every soup settles, at L = 16 the few survivors give an outlier τ, so d4 is fitted from L = 20;
c4: 62 M settles at L = 12), the analogue of gump's symmetric-soup debris problem. **[conjecture]** the corner
couples each edge to its symmetric partners (under the diagonal mirror the corner sits on the mirror line; under
C4 the edge's two ends are images of each other through the corners, so the four edges form one ring of period L),
and correlated corners are where edges start to die. Not tested.

## 6. Moore B45/S23467 [measured]
`python3 law.py B45/S23467 moore 16 8,12,...,44 --tag main` (→ `data/law_moore_B45S23467.json`): ln τ_edge =
5.29, 6.98, 8.27, 9.37, 10.56, 11.62, 12.55, 13.64, 14.70, 15.77 at L = 8…44 (± 0.014–0.047): concave below L = 24,
linear above: **ln τ = (4.32 ± 0.07) + (0.259 ± 0.002)·L, L = 24–44, χ² 6.0/4**. Memoryless (CV 0.83–1.02, hazard
ratio 0.91–1.19). The tail is *not* straight near zero: p₁/p₂ = 0.20 at every L but p₂/p₃ ≈ 0.45, p₃/p₄ ≈ 0.6,
and h sits *above* the line (h/p₁ = 0.31–0.36, nearly size-independent like gump's 0.6; straight-line prediction
too low by 0.4–1.1 nats). End-game: 58% of deaths from n = 1, 33% from n = 2. Gap healing as for cross2 but
slower (32-cell stretch closes in ≈ 100 generations).

## 7. gump vs the 2D gump, point by point

| | gump (3D) | cross2 B34/S234 (2D) |
|---|---|---|
| (i) confinement | birth ≥ 4 > 3 across a {111} plane; octahedral hull | birth ≥ 3 > 2 across a row/column; the box is the hull [proved] |
| (ii) steady chaos | density 0.4155, drive 0.115 | density 0.472, drive 0.119 [measured] |
| (iii) death by a whole face/edge, memoryless, exp. in size | ln τ ≈ 0.208·A | **ln τ ≈ 0.73 + 0.416·L**, CV ≈ 1 [measured, L = 12–36] |
| (iv) straight tail to n = 1, h its next point | within 0.06–0.08 nats; h/p₁ ≈ 0.6 constant | within 0.02–0.23 nats; h/p₁ 0.52 → 0.27, falling with L [measured] |
| (v) symmetric seeds die sooner | O_h: slope ≈ 0.209/6 (face stabiliser C3v, order 6) | mirror ⊥ edge and D4: slope × 0.42–0.50 (edge stabiliser order 2) [measured]; C4 and the diagonal mirror, which fix no edge, still shorten life (× 0.8 slope for C4) — not predicted |
| (vi) capped threshold, drive at overcrowded cells (T5) | yes | yes, exceptions = {n ≥ 5} exactly [proved] |
| (vii) no finite sealed set (T6) | none in ≥ 3 layers or 3D | none in Z²; in a strip every sealed set spans it [proved] |
| competing channel | 3-layer interior firewalls, win only in thin slabs | 3-column transverse cuts, win in strips with L ≳ 1.5 W |
| holes | a hole in a face heals from its rim (a curve) | a gap in an edge closes from its two ends |
| minimality | removing any count from B45/S345 collapses lifetimes | the other caps on cross2 (B3/S2, B3/S23, B345/S2345, …) all settle |

## 8. Surprises
1. The Moore lattice — the obvious 2D setting — is the wrong one for the capped-threshold mechanism, for a
   counting reason (§2); the right one is the cross, with gump's exact proportions (half the neighbourhood
   in-layer, reach two layers, three-layer firewalls).
2. On the cross, edge-by-edge death is the *generic* fate of a long-lived small rule (367 of 439).
3. A naive strip measurement looked like a broken law (saturating τ): the strip was being cut across, not peeled.
4. The mirror-symmetric edge costs less per independent cell than an asymmetric one (§5) — the same direction as
   gump's "A/7.7 then rising", but here with no sign of rising up to L = 56.
5. My forecast that symmetries fixing no edge cost nothing in the exponent failed for C4 (slope × 0.8, waits
   shorter than asymmetric ones) and half-failed for the diagonal mirror. The stabiliser rule is not the whole story.

## 9. Not checked / open
- Whether I stays ≈ 0.41 beyond L = 36 for cross2 (deaths cost 900 s per point at L = 36; L = 40 needs ~1 h).
- The rate-function collapse (gump's I(x) curve) — only the endpoint was measured.
- The 15,000 Moore and 27,000 cross2 rules screened out at L = 10, and cross2 rules with |B| + |S| > 7.
- Why C4 and the diagonal mirror shorten life (corner conjecture, §5); whether the C4 slope recovers at large L.
- Triangular lattice; hex measured only structurally; the other cross2 EDGE rules' laws.
- A proof of anything metastable: the 2D case is now available for M2/M3 of the programme (a 1D edge driven by a
  2D bulk, whose gaps close from two ends, is the natural object for a contour or gambler's-ruin argument).

## Reproduce
```sh
cd research/toy2d
python3 validate.py; python3 structure2d.py                       # stepper and structure: ALL OK
python3 search.py stage1 moore ../scratch/toy2d/s1_moore.jsonl    # (sharded: add "0 2" / "1 2")
python3 screen.py ../scratch/toy2d/s1_moore.jsonl ../scratch/toy2d/screen_moore.jsonl
LAT=cross2 MAXSIZE=7 python3 screen.py ../scratch/toy2d/s1_cross2.jsonl ../scratch/toy2d/screen_cross2.jsonl
python3 classify.py ../scratch/toy2d/screen_moore*.jsonl
python3 law.py B34/S234 cross2 16 12,16,20,24,28,32,36 --deaths 400 --maxsec 900 --tag main
python3 law.py B45/S23467 moore 16 8,12,16,20,24,28,32,36,40,44 --deaths 400 --maxsec 900 --tag main
./run_sym.sh; python3 law.py B45/S23467 moore 16 16,24,32,40,48,56 --sym mx --deaths 400 --maxsec 300 --tag sym
python3 energy2d.py B34/S234 cross2 24 3 3000; python3 bulk2d.py B34/S234 cross2 3
python3 gap.py B34/S234 cross2 32 128 16 64 400 4000 1; python3 kymo.py B34/S234 cross2 16 64
python3 curate.py; python3 figures.py
```
