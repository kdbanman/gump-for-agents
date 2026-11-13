# Is a face's death just the far tail of its stationary fluctuations?

Fluctuation agent, 2026-11-13. Question from the lead: confined chaos dies by losing outer `{111}` face layers;
the wait is memoryless with ln τ ≈ −0.09 + 0.209·A. Conjecture: death needs no special mechanism — it is the far
tail of the living face's ordinary stationary fluctuations. Tested here directly, by measuring the
quasi-stationary distribution (QSD) of the face population n *all the way to n = 0* together with the death rate,
at sizes where both are reachable, and by brute-forcing symmetric faces up to A = 828 with a new symmetry-reduced,
bit-sliced stepper.

Tags: **[proved]**, **[measured]** (n, error, command), **[conjecture]**. Commands run from the repo root.

## Corrections to the lead's claims (up front)

1. **The face-law constant is not an extrapolation any more: it is the measured zero point of the living face's
   stationary distribution** [measured]. At A = 30–84 the QSD is measured down to n = 1 and the death rate h (per face
   per generation) sits exactly where the distribution continued to n = 0 puts it. The lead's "I(0) ≈ 0.20 by
   extrapolation, the curve is flattening" is close but slightly low and the shape claim is off: near n = 0 the tail
   is *straight* in n (ln p_k linear, constant ratio p_k/p_{k+1} ≈ 0.6–0.66), not flattening. Endpoint
   I_A(0) = −ln h/A = 0.2268, 0.2182, 0.2164, 0.2152 at A = 30, 45, 63, 84 → **I(0) = 0.2077 ± 0.0014 + 0.55/A**.
2. **R = 9 first-peel mean: 2300 ± 6** (137,243 peels), not 2.60×10³ ± 0.17×10³ [measured; 1.8σ apart — the lead's
   value is high or uses an earlier start, T0 = 60 vs my 200; the hazard is flat in age from 200 to 7×10⁵ at R = 11].
   R = 11: 1.04×10⁵ ± 0.008×10⁵ (16,240 peels; agrees with 9.4×10⁴ ± 0.9×10⁴). R = 13: 8.86×10⁶ ± 0.48×10⁶ (342 peels).
3. **Side 16's first plateau was under-predicted because of the vertex factor, not the cube-centred law**
   [measured]. Cube-centred O_h faces follow the lead's revised fit closely up to A = 693 (measured ln τ = 19.64 ± 0.22
   at A = 693 vs the fit's 19.47). But the vertex/cube factor at equal area, ≈1.5–1.6 at A = 360, 513, 630
   (1.53, 1.60 ± 0.06, 1.53 ± 0.3), is **3.3 (ln 1.19 ± 0.28) at A = 693**: side-16 copies and vertex soups give
   τ = 1.1×10⁹, not 4–7×10⁸. Whether the factor really grows or A = 630's clone value is low is not settled (2.6σ).
   The side-16 face is an ordinary member of its class: copies of the cube (24 deaths) and O_h soups at the same hull
   (5 deaths) agree.
4. **Splitting along n does not work in this system** (negative result; the lead's option 3): forward-flux sampling
   is unbiased within ~0.1 nats where checkable (A = 45, 63) but gains almost nothing, because one flipped cell leaves
   clone outcomes 55–95% correlated — a dip to death takes ~10 generations, faster than a perturbation spreads.
   What does reach the big faces is symmetry reduction + bit-slicing: brute force at A = 693 is a 10-minute job.

> **Lead's notes after checking (2026-11-13).** The small-face results below were re-derived with the engine alone
> (`research/experiments/face_endgame_check.py`) and stand. The side-16 second plateau ended at 2,886,100,480:
> inside the fit-only forecast, outside the clone-run one; the cube ended at 2,919,617,676. The symmetric table in
> `data/sym_residence.csv` now also holds the lead's runs (vertex-centred R = 32, 34, 38, 40; copies of the
> 2.875×10⁹ state): the vertex/cube factor is a flat ≈1.5 from A = 360 to 630, and 2.0 ± 0.4 at A = 693 once
> fresh soups are measured properly (45 deaths; the 3.3 of correction 3 below leaned on copies of the cube).
> `qsd.py`'s symmetric ensembles are not reliable below R = 30 (settled debris is counted as a living face:
> R = 24 v reads 6.2×10⁴ where the engine gives 630). Details: `research/NOTEBOOK.md`, 2026-11-13.

## Verdict

**Supported, and in a sharper form than conjectured** [measured]. A face's death is the stationary tail
reaching n = 0: at every size where both can be measured (asymmetric A = 30–84, symmetric A = 360–693) the death rate
equals the quasi-stationary probability of n = 1 times a size-independent ≈0.6 per generation, and the end-game —
committor ½ at 1.5–1.7 cells, 62% of deaths from a single surviving cell, ~10-generation plunge — is identical at all
sizes; all the size dependence is in P_qs(n = 1) ≈ exp(−A·I(0)). The rate function collapses (A = 30–135) with
corrections ≤ 0.25/A. Two caveats: n is the right *coordinate* only in a weak sense — it explains ≈18–20% of a near-empty
face's fate, the layer below adds 1–5%, nothing simple does better; the fate is decided by the next few generations of
chaos. And a tail *extrapolated* from x ≥ 0.1 to 0 is unreliable by 0.5–4 nats; the endpoint must be measured.
Predictions: side 16's first plateau **hit** (predicted median 2.2×10⁹, 90% 1.50–5.2×10⁹; died at 2.362×10⁹);
second plateau (R = 40) and side 17 predicted in `PREDICTIONS.md` before they resolved.

## Tools (all validated against the engine)

- `fl.c` / `fl.py` — 64·W replicas of gump in the bits of machine words on an arbitrary finite cell graph
  (kernel from `research/peeling/rep.c`), with per-generation weighted layer counts (bit-sliced counters), per-replica
  freezing, soup reseeding, and detection of settled replicas (period 1–2 every generation, any period dividing 840).
  Vessels are exact diagonal hulls (T2). **O_h orbit reduction**: an O_h-symmetric state is stepped on one node per
  orbit (a node's neighbours are the orbits of its representative's 12 neighbours); the side-16 cube is 946 nodes
  instead of ≈45,000 cells, and 64 diversified copies run at ≈3–7×10⁶ replica-generations/s on one core
  (≈30–60× the engine's throughput per core for ensembles; no gain for a single state).
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

## 1. Asymmetric faces: the stationary distribution down to n = 0

`research/fluct/run_qsd.sh a` (= `qsd.py R SECONDS 4` for R = 7, 9, 11, 13; 300–4800 s each, 256 replicas,
density 0.35, T0 = 200) and `run_qsd.sh b` (R = 15, 17, 19, `lite`). Tables: `python3 research/fluct/analyze_qsd.py`
(→ `data/qsd_summary.json`). Face-generations measured: 1.1×10⁸ (R=7) … 2.4×10¹⁰ (R=13), 1.3–2.0×10¹⁰ (R=15–19).

**[measured] Rate function collapse.** I_A(x) = −ln P(n ≤ xA)/A (ln P interpolated linearly at n = xA):

| A | mean/A | var/A | x=0.40 | 0.30 | 0.25 | 0.20 | 0.15 | 0.10 | 0.05 | **0** (= −ln h/A) | peels |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 30 | 0.454 | 0.488 | .0337 | .0658 | .0851 | .1060 | .1289 | .1534 | .1967 | **.2268** | 117,851 |
| 45 | 0.480 | 0.460 | .0321 | .0654 | .0852 | .1062 | .1284 | .1522 | .1825 | **.2182** | 137,243 |
| 63 | 0.496 | 0.436 | .0309 | .0653 | .0861 | .1082 | .1311 | .1548 | .1803 | **.2164** | 16,240 |
| 84 | 0.505 | 0.423 | .0296 | .0645 | .0860 | .1090 | .1329 | .1571 | .1822 | **.2152** | 342 |
| 108 | 0.511 | 0.415 | .0283 | .0637 | .0855 | .1091 | .1337 | .1587 | – | (1 peel) | 1 |
| 135 | 0.515 | 0.409 | .0272 | .0628 | .0849 | .1090 | .1354 | – | – | – | 0 |
| 165 | 0.517 | 0.405 | .0263 | .0633 | .0849 | .1086 | – | – | – | – | 0 |

Fits I_A(x) = I∞(x) + b(x)/A over all sizes: b = +0.24 (x=0.4), +0.10 (0.3), −0.01 (0.25), −0.14 (0.2), −0.25 (0.15),
−0.22 (0.1): finite-size corrections are a few % at A = 30 and < 1% at A ≥ 100; no drift of the curve with size.
Endpoint **I(0) = 0.2077 ± 0.0014 + 0.55/A** (4 sizes) — i.e. ln τ_face = 0.208·A + 0.55 for octahedral faces, the
face law's 0.209 with the octahedral ×1.5 in the intercept.

**[measured] The death rate is the QSD continued to n = 0.** ln p_k (p_k = P_qs(n = k) per face-generation) is a
straight line from k ≈ 10 down to k = 1, and h sits on it at k = 0 (`figures/fluct_tail.png`, middle panel):
h/p₁ = 0.645, 0.613, 0.601, 0.594 at A = 30, 45, 63, 84, against p₁/p₂ = 0.65, 0.66, … . A straight line through
the lowest decade of ln p_k predicts ln h to within 0.06–0.08 nats at all four sizes (`analyze_tail.py`, column a).
Using only x ≥ 0.1 (what one has at large A) and a quadratic extrapolation misses by 0.5–0.8 nats; the Gaussian by
2–7 nats. One excess: p₃ is ≈1.5–2× the straight line at every size (a favoured three-cell configuration).

**[measured] The end-game is size-independent** (one-step transitions and committors, `analyze_qsd.py`):

| A | n* (p_B = ½) | p_B(1) | p_B(2) | p_B(3) | deaths from n = 1 / 2 / 3 | h / P_qs(n=1) |
|---|---|---|---|---|---|---|
| 30 | 1.69 | 0.72 | 0.40 | 0.22 | 62% / 23% / 9% | 0.645 |
| 45 | 1.53 | 0.67 | 0.35 | 0.17 | 63% / 23% / 9% | 0.613 |
| 63 | 1.53 | 0.67 | 0.35 | 0.16 | 63% / 23% / 9% | 0.601 |
| 84 | 1.59 | 0.68 | 0.37 | 0.17 | 63% / 25% / 8% | 0.594 |

(p_B(k) = probability that a visit to n = k is followed by n = 0 before n ≥ A/2.) So τ_face = 1 / (ν · P_qs(n ≤ n*))
with n* ≈ 1.5, attempt rate ν ≈ 0.6 per generation, holds *by construction of the measurement* at these sizes; the
content is that ν and n* do not depend on A while P_qs(n = 1) carries all of exp(−0.208·A).

**[measured] The last generations** (`predeath.py R`, every death's last 64 generations): the face is ordinary
until ≈16 generations before death (mean n within 0.2 sd of the living mean at −16), then plunges to 0 in 10–12
generations; at −6, 13–31% of dying faces are still within one sd of the mean. The layer below sags only to 0.62–0.75
of its mean and *recovers* at the moment of death (0.71 at A = 45, 0.89 at A = 84): the face dies on top of a living layer.

**[measured] Is n the coordinate?** (`coord.py R 4`): for visits with 1 ≤ n ≤ 4, n alone removes 16–18% of the
outcome entropy (die vs recover); the layer below adds 1.6–4.9% (saturated table), the best linear mix n + α·n₂ adds
nothing (α → 0 at A ≥ 63). At fixed n the committor does depend on n₂ (A = 45, n = 3: 0.25 / 0.14 / 0.10 across n₂
terciles), but the bulk of the fate is not in any simple coarse variable — it is decided by the following ~5
generations of chaos. n is as good a coordinate as the simple alternatives, and a poor one in absolute terms.

## 2. Forward-flux sampling: validated, but useless here (negative result)

`ffs.py asym R --D D --M M --N0 N0 --reps K` (m = min over the 8 faces; interfaces every ½ sd from mean−sd to 0;
clones diversified by one flipped cell at layer depth ≥ D). Results (`research/scratch/fluct/ffs_v*.jsonl`):

| case | reps | ln(1 / mean rate) | direct |
|---|---|---|---|
| R=9, D = −1 (no perturbation) / 1 / 3, M = 4000 | 16 each | 7.79 ± 0.04 / 7.72 ± 0.03 / 7.82 ± 0.04 | 7.741 ± 0.003 |
| R=11, D = 1 / 3 / 3 with T0 = 5000 / 3 with λ_A = 30, M = 20000 | 8 each | 11.64 ± 0.15 / 11.76 ± 0.08 / 11.30 ± 0.15 / 11.64 ± 0.09 | 11.55 ± 0.01 |

Unbiased within ~0.1–0.2 nats, but the spread between repetitions is 3–4× the naive FFS error and grows with depth
(sd of ln P_i 0.006 at the first interface, 0.2 at the last ones). Cause, measured with `clone_corr.py 11 16|8`: two
clones of one configuration, independently perturbed, have outcome correlation 0.86–0.95 (to the next interface) and
0.54–0.73 (four interfaces down), whatever the depth of the flip (D = 0…5); trials last 2.6–4 generations. The
descent is too fast for a one-cell perturbation to diversify it, so the ancestry collapses (20,000 crossings → ~80
ancestors at the last stage) and splitting buys almost nothing over brute force. Stronger perturbations would bias.
**[conjecture]** This is generic for this automaton: the rare event is a rare *configuration* reached in ~10
generations, not a slow rare *path*, so path-splitting along n cannot help; static importance sampling would need a
model of the face's stationary measure, which we do not have.

## 3. Symmetric faces by brute force (O_h orbit stepper)

`run_sym.sh`, `run_after*.sh` (= `qsd.py sym R c|v SECONDS 1 [lite]`, `qsd.py snap FILE v …`); table:
`python3 research/fluct/sym_fit.py` → `data/sym_residence.csv`. Mean residence = exposure/deaths, states after
T0 = 1000 generations, 64 replicas.

| A | centre | source | deaths | mean residence τ | ln τ ± | n/A | var/A |
|---|---|---|---|---|---|---|---|
| 360 | v | O_h soups R=30 | 66,555 | 2.18×10⁴ | 9.99 ± 0.004 | 0.407 | 4.61 |
| 408 | c | R=31 | 1,087 | 5.95×10⁴ | 10.99 ± 0.03 | 0.412 | 3.08 |
| 459 | c | R=33 | 5,141 | 2.61×10⁵ | 12.47 ± 0.01 | 0.421 | 2.93 |
| 513 | c | R=35 | 933 | 1.40×10⁶ | 14.15 ± 0.03 | 0.429 | 2.86 |
| 513 | v | R=36 (side-14 plateau) | 2,177 | 2.24×10⁶ | 14.62 ± 0.02 | 0.441 | 2.97 |
| 570 | c | R=37 | 167 | 7.9×10⁶ | 15.88 ± 0.08 | 0.435 | 2.80 |
| 630 | c | R=39 | 96 | 5.4×10⁷ | 17.80 ± 0.10 | 0.441 | 2.76 |
| 630 | v | copies of `cube16_gen2525000000` (R=40) | 31 | 8.2×10⁷ | 18.22 ± 0.18 | 0.451 | 2.87 |
| 693 | c | R=41 | 20 | 3.4×10⁸ | 19.64 ± 0.22 | 0.446 | 2.73 |
| 693 | v | copies of `cube16_gen1025000000` | 24 | 1.08×10⁹ | 20.80 ± 0.20 | 0.454 | 2.83 |
| 693 | v | O_h soups R=42 | 5 | 1.25×10⁹ | 20.94 ± 0.45 | 0.454 | 2.83 |
| 759 | c | R=43 | 1 | 6×10⁹ (90%: 2×10⁹ … 1.2×10¹¹) | 22.5 ± 1.0 | 0.450 | 2.70 |

**[measured] Agreement with the lead's gump batches**: A = 408: 5.9×10⁴ (lead 5.8×10⁴); 459: 2.6×10⁵ (2.3, 3.4×10⁵);
513: 1.40×10⁶ (1.66×10⁶ [1.34, 2.20]); 570: 7.9×10⁶ (8.9×10⁶ [7.2, 11.8]); 630: 5.4×10⁷ (5.4×10⁷ [3.5, 11.9]).

**[measured] Tail ↔ hazard for symmetric faces.** The same end-game in units of orbits: deaths from n = 3, 6, 9, 12
(19%, 44%, 13%, 15–19% at A = 408 and 570), committor ½ at n ≈ 12 (two six-cell orbits), p₉ ≈ 10× its neighbours (a
favoured nine-cell configuration, the symmetric twin of the asymmetric n = 3 excess). The straight-line endpoint rule
predicts ln h within 0.1–0.7 nats (the orbit lattice of n makes it rougher). The symmetric face's plunge takes ≈16
generations, like the asymmetric one.

**Fits of ln τ(A), cube-centred** (weights = deaths; 5 points 408–630 plus 693 and 759 where measured): a + bA: b = 0.0304, χ² 6.2/4 → ln τ(828) = 23.72;
a + bA + c√A: χ² 2.4/3 → 24.27 ± 0.30; a + bA + cA²: χ² 2.8/3 → 24.36 ± 0.37; the lead's a + (0.209/6)A + c√A
(c = −0.197): χ² 4.1/4 → 23.90 ± 0.10. All agree with the single death at 759 (fits 21.6–22.0 vs 22.5 ± 1.0). The
lead's form, refitted on these data, matches the cube-centred points as well as anything [measured]; whether the
slope is really 0.209/6 is not decided by them (free slopes 0.024–0.044 depending on the curvature term).

## 4. Predictions (timestamped in `PREDICTIONS.md`)

- **Side 16, first plateau (R = 42, A = 693, vertex):** committed 01:28Z with 8 deaths: τ = 1.04×10⁹, death at median
  2.2×10⁹, 90% 1.50–5.2×10⁹. **Outcome (from the lead): died at last_alive = 2,362,434,048 — inside, at predictive
  quantile ≈ 0.57.** Final ensemble estimate: τ = 1.11×10⁹ (90% CI 0.84–1.55×10⁹; 29 deaths, copies + soups).
- **Side 16, second plateau (R = 40, A = 630, vertex):** committed 04:08Z from fits only (τ ≈ 1.1×10⁸; death median
  2.60×10⁹, 90% 2.531–2.89×10⁹ given alive at 2.525×10⁹), then a 10-minute clone run from the 2.525×10⁹ checkpoint:
  τ = 8.2×10⁷ (31 deaths), death median 2.58×10⁹, 90% 2.529–2.78×10⁹. Outcome not known to me at writing.
- **Side 17, first plateau (R = 45, A = 828, cube-centred):** ln τ = 24.0 ± 0.4, τ ≈ 2.6×10¹⁰ (68%: 1.8–4.0×10¹⁰);
  first peel at median 2×10¹⁰, 90% 1.4×10⁹–1.0×10¹¹ — days of single-core engine time, so a direct test is possible
  but long. (The orbit stepper's gain is throughput over 64 replicas; for one state it is no faster than the engine.)

## What I could not settle

- The asymptotic symmetric slope: the cube-centred points 408–693 are fitted equally well by a + bA + c√A,
  a + bA + cA² and the lead's a + (0.209/6)A + c√A; they differ by ~0.5–0.7 nats at A = 828.
- Whether 0.209 per site holds beyond A = 84 for asymmetric faces: no direct deaths beyond A = 108 (1 peel), FFS
  cannot reach it, and the rate-function collapse to A = 135 is only indirect support.
- The geometry of the favoured 3-cell (asymmetric) / 9-cell (symmetric) near-death configurations — counted, not looked at.
- Why FFS at R = 11 with T0 = 5000 came out 0.25 nats low (2σ); probably the variance, not age (hazard is flat in age).

## Reproduce

```sh
python3 research/fluct/validate.py                       # stepper vs engine: ALL OK
research/fluct/run_qsd.sh a; research/fluct/run_qsd.sh b # asymmetric QSD runs (resumable)
research/fluct/run_sym.sh                                # symmetric series + side-16 copies
python3 research/fluct/qsd.py sym 41 c 3000 1 lite; python3 research/fluct/qsd.py sym 43 c 4200 1 lite
python3 research/fluct/qsd.py snap research/data/cube16_gen2525000000.gump v 600 1 lite
python3 research/fluct/analyze_qsd.py; python3 research/fluct/analyze_tail.py; python3 research/fluct/coord.py 13 4
python3 research/fluct/predeath.py 13; python3 research/fluct/sym_fit.py; python3 research/fluct/figures.py
python3 research/fluct/predict.py snap_cube16_gen1025000000 sym42v
for D in -1 1 3; do python3 research/fluct/ffs.py asym 9 --M 4000 --N0 3000 --reps 16 --D $D --tag v9_D$D; done
python3 research/fluct/clone_corr.py 11 16 3000
```
Bulk output: `research/scratch/fluct/` (npz tallies, ffs jsonl, logs). Curated: `data/qsd_summary.json`,
`data/sym_residence.csv`, figure `research/figures/fluct_tail.png`.

