# shape3: candidate second variables and their forecasts (fixed before any production run)

2026-11-14. Committed together with the run plan (`run3.py`) before the first production job. Nothing measured in
this experiment has been looked at: the only runs so far are the validation traces (`data/validate.log`, 4,000
generations from one soup per torus, and 60,000-generation event files compared between two steppers, never
reduced to a rate).

## The structural fact that shapes the test

Write the reduced Gram matrix of the period lattice as (Q1, 2B, Q2), Q1 = shortest loop², Q2 = second loop²,
0 ≤ B ≤ Q1/2. Its determinant D = Q1·Q2 − B² is fixed by the area (D = 0.75·n², n = A/3).
So **at equal area and equal shortest loop the lattice up to isometry is fixed by one number**: Q2, or equally B,
or the angle θ (cos θ = B/√(Q1Q2)), or the third loop Q3 = Q1 + Q2 − 2B (which *falls* as Q2 rises), or the shape
modulus τ = (B + i√D)/Q1, which moves along the horizontal line Im τ = h = √D/Q1 with x = Re τ = B/Q1 ∈ [0, ½].
Every candidate that depends on the lattice only through its metric (loop lengths, theta series, angle, loop
counts, any function of the torus as a flat surface) is therefore a function of x alone within a group, and all
the natural ones are monotone in x. **They cannot disagree in sign on any equal-area, equal-loop pair; they can
only disagree in size.** Two classes with the same Gram matrix (same metric, different orientation against the
cell lattice) would separate metric from non-metric candidates, but none exists with Q1 ≥ 9 at A ≤ 72
(`enum3.py`: Q1 = 12 and 16 are achiral, so the reflection through the shortest loop is a lattice symmetry).

So the experiment separates candidates by **size**, where their forecasts differ by factors 3 to 50.

Groups (all of them with Q1 ≥ 12 and A ≤ 84 are at A = 48, 60, 72, 84; `python3 research/shape3/enum3.py 14 28`;
A = 84 is out of budget). Below saturation, Q1 = 9 groups exist at A = 36, 45, 54, 63, 72 and are cheap; they are
included as a second, clearly separate set (the first variable is equal within each group anyway).

| label | A | from → to | Gram from → to | h | x from → to |
|---|---:|---|---|---:|---|
| P1 (known) | 48 | (2,2,8) → (1,6,16) | (12,0,16) → (12,12,19) | 1.155 | 0 → ½ |
| P2 (known) | 60 | (1,5,20) → (1,4,20) | (16,4,19) → (16,12,21) | 1.083 | ⅛ → ⅜ |
| P3 (known) | 60 | (1,8,20) → (2,2,10) | (12,0,25) → (12,12,28) | 1.443 | 0 → ½ |
| T01 | 72 | (1,6,24) → (2,4,12) | (16,0,27) → (16,8,28) | 1.299 | 0 → ¼ |
| T12 | 72 | (2,4,12) → (1,5,24) | (16,8,28) → (16,16,31) | 1.299 | ¼ → ½ |
| N72 | 72 | (2,2,12) → (1,10,24) | (12,0,36) → (12,12,39) | 1.732 | 0 → ½ |
| Q36 | 36 | (1,4,12) → (1,3,12) | (9,0,12) → (9,6,13) | 1.155 | 0 → ⅓ |
| Q45 | 45 | (1,5,15) → (1,4,15) | (9,3,19) → (9,9,21) | 1.443 | ⅙ → ½ |
| Q54 | 54 | (3,0,6) → (1,5,18) | (9,0,27) → (9,6,28) | 1.732 | 0 → ⅓ |
| Q63 | 63 | (1,6,21) → (1,7,21) | (9,3,37) → (9,9,39) | 2.021 | ⅙ → ½ |

d(X → Y) = ln τ_face(Y) − ln τ_face(X); Y always has the longer second loop. T02 = T01 + T12 is not independent.

## Candidates

Parameters fitted (weighted least squares) on the three known pair differences only: P1 +0.0151 ± 0.0017,
P2 +0.0142 ± 0.0019, P3 +0.0063 ± 0.0035 (pooled values of research/audit/REVIEW-shape2.md, claim 4). Those three
are in-sample for every candidate; every new difference is a test. `python3 research/shape3/predict3.py --write`
(→ `data/predictions.json`, `data/predictions.txt`).

Metric candidates (functions of x within a group):

- **K1 (second loop, linear):** d = s·ΔQ2. s = 0.00506. In-sample χ² 11.1 on 2 (p 0.004): already strained by
  P2 against P1/P3 (P2 has ΔQ2 = 2 but the same effect as P1 with ΔQ2 = 3).
- **K1a (angle, linear):** d = s_θ·(θ_X − θ_Y), degrees. s_θ = 0.00069. In-sample χ² 12.8 on 2 (p 0.002).
- **K3b (cos 2πx, no size dependence):** d = κ'·(cos 2πx_X − cos 2πx_Y). κ' = 0.0075. In-sample 9.8 on 2 (p 0.008).
- **K2 (massive loop sum):** ln τ = c(A) − B·(A/72)·Σ_{primitive v mod ±} e^{−K|v|}, |v| = √Q (shape2's L3-area
  form). Fitted B = e^4.53, **K = 1.41** (decay length 0.71 in √Q units). In-sample χ² 1.4 on 1.
- **K3 (scale-free / modular):** d = κ·[e^{−2πh_X} cos 2πx_X − e^{−2πh_Y} cos 2πx_Y], the leading Re τ
  dependence of any function of the shape modulus alone (the first q-term of a modular function; the q² term is
  ≤ e^{−4πh} ≈ 10⁻⁶). κ = 9.92. In-sample χ² 2.3 on 2. K2 and K3 are physically different (K2 depends on lengths
  in cell units, K3 only on the conformal shape) but forecast nearly the same here; this experiment does not try to
  separate them.

Non-metric candidates, refuted in-sample before any run (listed so that nobody re-proposes them):

- **Cheapest firewall cut** (smaller cut dies sooner, zero when equal): P2 has equal cuts (144, 144) and differs at
  7σ. Refuted.
- **Short straight rows** (Σ over the three row directions of a decreasing function of the row closure): in P2 the
  longer-lived (1,4,20) has rows {4, 5, 20} against {4, 10, 20}, so any such sum puts it shorter-lived. Refuted.
- **Total number of transverse layers**: P2 (16 layers vs 20) has the wrong sign. Refuted.
- **Number of shortest loops**: 1 in every class of every group; forecasts 0. Refuted by P1, P2.
- **Third loop, shorter dies sooner**: wrong sign in P1 and P2. (With the other sign it is a metric candidate,
  identical in sign to K1.)

## Forecasts (d, with the forecast's own error from the in-sample fit)

| | T01 | T12 | N72 | Q36 | Q45 | Q54 | Q63 |
|---|---|---|---|---|---|---|---|
| K1 l2 | +0.0051 | **+0.0152** | **+0.0152** | +0.0051 | +0.0101 | +0.0051 | **+0.0101** |
| K1a angle | +0.0075 | +0.0070 | +0.0111 | +0.0111 | +0.0086 | +0.0075 | +0.0063 |
| K3b cos 2πx | +0.0075 | +0.0075 | +0.0150 | +0.0113 | +0.0113 | +0.0113 | +0.0113 |
| K2 loop sum | +0.0021 ± 0.0006 | +0.0021 ± 0.0006 | +0.0003 | +0.0121 ± 0.0036 | +0.0019 | +0.0003 | 0.0000 |
| K3 modular | +0.0028 | +0.0028 | +0.0004 | +0.0105 ± 0.0009 | +0.0017 | +0.0003 | 0.0000 |

(Forecast errors of K1, K1a, K3b are ≤ 0.0013; full list in `data/predictions.txt`.) Every candidate forecasts
d ≥ 0 everywhere. The discriminating differences are T12, N72, Q54 and Q63, where the size-free candidates (K1,
K1a, K3b) forecast 0.005–0.015 and the decaying ones (K2, K3) forecast ≤ 0.003; Q36 tests K2/K3's size where they
forecast an effect as large as the others. T12/T01 tests the shape of the x-dependence: 3 for K1, ≈ 1 for the rest.

## Scoring rule (fixed now)

- For each candidate and each of the seven independent new differences, z = (measured − forecast)/√(σ_m² + σ_f²);
  a forecast is a hit if |z| < 2.
- A candidate is **refuted** if Σz² over the seven has p < 0.01 (χ² on 7 dof, forecast parameters, no refit), the
  criterion research/shape2 used. Otherwise it **survives**, out of sample.
- Sign: a difference is "positive" or "negative" if it is beyond 2σ_m from 0, else "zero within 2σ".
- Post hoc (labelled as such): refits on all pairs; the in-sample pairs P1–P3 re-measured cap-free.

## Measurement (run plan `run3.py`, seeds 30001–30042)

ts3 = the review's ts.c (research/audit/shape/ts.c) with a carry-save AVX-512 step kernel and nothing else changed;
validated on all 19 tori against the engine (population × copies equal at each of 4,000 generations, vector path)
and against the unmodified ts.c (identical event files, 512 replicas, 60,000 generations): `validate3.sh`,
`data/validate.log`. Renewal lives, **no cap** (10¹⁵); a life is censored only by the end of its job (≈ 2% of
exposure at A = 72). Events checked every 8 generations; ties (face death and firewall at the same check, type X)
are counted separately and reported both ways. ln τ_face = ln(2E/F) ± 1/√F. Planned precision of d: Q pairs, P1, P2
±0.0015–0.002; P3 ±0.0025; T01, T12 ±0.0037 (short of ±0.003: the budget is two cores for about three hours);
N72 ±0.005. A = 72 jobs run in rounds over the five tori, so a truncated run loses rounds, not tori.

## Amendment, before the production runs of plan v2 (2026-11-14, about 25 minutes after the commit above)

Plan v1 (seeds 30001–30042) was started and **stopped after its first four jobs** (Q36 and Q45, one job per torus).
Reason: without a cap, lives that settle into a state whose period does not divide 840 (or into a translating
pattern) are never caught by ts.c's settled test (equality with the snapshot 840 generations earlier) and keep
adding exposure until the end of the job. In the first Q36 job, 14 of 512 replicas held such a "zombie" life at the
end (ages up to 7 × 10⁶, against a mean life of 800), carrying 1.7% of the exposure: a bias of +0.017 in ln τ that
differs between tori. With the review's cap (5 × 10⁵) the same lives were censored as "C". No forecast and no
candidate was changed; the forecasts above stand as committed.

What was seen before the amendment (it is disclosed because it was seen): the v1 counts of Q36 give d = −0.027
(zombie-biased; −0.023 for lives younger than 65,536), and the v1 summary lines of Q45 give d ≈ +0.007 (equal
exposures, F 1,153,847 against 1,145,644). These v1 numbers are not used in any result.

Changes (plan v2, `run3.py`, seeds 31001–31037):

1. ts3's settled test compares the state with the snapshots taken 840·m generations earlier, m = 1 … 128, within
   the same life, and censors at age − 840·m for the smallest such m. Exact equality of the whole state is proof of
   periodicity, so this cannot censor a chaotic life. On the Q36 job it removed every zombie (0 open lives older than
   20,000 at the end, 106 more lives settled). The step kernel is unchanged; validation is rerun (`validate3.sh`;
   the identity check against ts.c now uses ts3 built with the one-lag test, `-DNSNAP=2`).
2. Budget trimmed to fit: A = 72 runs 5 rounds (triple) and 2 rounds (N72) instead of 6 and 3; P3 300 s per torus.
   Planned precision of d: T01, T12 ≈ ±0.004; N72 ≈ ±0.006; the rest as above.
3. Every life still old at the end of its job is reported (the "open" column). If a torus still shows open lives far
   older than its mean life, the README says so and gives the value with those lives cut at 20 mean lives.

Extension (added before any v2 job had been looked at): after the plan, rounds 6–10 over all five A = 72 tori
(seeds 31038–31062), run as long as the session lasts. Wall time is the only stopping rule; the analysis uses
completed rounds and also reports d from the planned rounds alone.
