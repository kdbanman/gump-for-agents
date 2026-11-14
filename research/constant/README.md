# Is there one cost per cell? What the lifetimes in hand can and cannot say about c_inf

Analyst on the constant, 2026-11-14. Confined chaos in gump ends when a boundary face of A cells goes extinct, after
a mean wait τ_face with ln τ_face ≈ 0.21·A. The question: is there a single cost per cell c_inf of an unbounded
face, what is it, and with what error. No new simulation was run; every number below is recomputed from tracked
data by the scripts of this directory (`load.py --check` prints each value beside the one quoted in the READMEs
and the ledger). Tags: **[measured]** a statistic of tracked data; **[fitted: …]** with what was free;
**[conjectured]**.

## Verdict

**The data in hand do not define c_inf. Two families give two values, each well fitted on its own, and they
disagree by 5 to 12%.**

1. **Periodic slab faces** (no rim; A = 48 to 126, shortest loop ≥ √12 cube steps) **[fitted]**: every form that
   describes them puts the cost per cell between **0.205 and 0.212**: 0.2072 ± 0.0001 (one offset per width),
   0.2117 ± 0.0002 (a term in the long side), 0.2121 ± 0.0028 (terms in both sides free), 0.2108 ± 0.0003
   (capillary-wave shape term), 0.2063 ± 0.0008 (massive loop sum). Midpoint and half-range:
   **0.2085 ± 0.0035 (spread between models) ± 0.001 (statistical)**.
2. **Hull (octahedral) faces** (a rim of 6k − 3 cells on a triangle of side k; A = 45 to 135) **[fitted]**: with
   one correction term the cost per cell is **0.2226 ± 0.0010** (correction p·ln A) or **0.2317 ± 0.0019**
   (correction r·k, proportional to the rim), both with χ² ≤ 1.8 on 2 and both forecasting the held-out A = 108
   and 135 within 1.3σ. Midpoint: **0.227 ± 0.005 (models) ± 0.002 (stat)**.
3. **The tension, precisely** [fitted]: hull faces at A = 45, 63, 84, 108 (local slopes 0.2119 ± 0.0002,
   0.2146 ± 0.0003, 0.2181 ± 0.0013, rising) against periodic faces of widths 4 and 5 at A = 60 to 120 (slopes
   0.2072 ± 0.0001 and 0.2082 ± 0.0006, flat). c_hull − c_periodic is **+0.0109 ± 0.0010 at the least** (log
   correction against long-side term) **and +0.0245 ± 0.0019 at the most** (rim against offsets). Forcing one c
   with one correction term per family costs Δχ² = 110 to 238 for one degree of freedom, and leaves the hull
   points at A = 84 and 108 above the fit by 0.04 to 0.06 (7 to 11σ) and 0.17 to 0.24 (5 to 8σ).
4. **What would make one c_inf consistent with everything** [fitted; conjectured as physics]: a hull correction
   with two terms, a + r·k + q/k, with the rim *raising* the lifetime (r = +0.29 to +0.40 per unit of side, about
   +0.05 to +0.07 per rim cell) and q ≈ +9 to +10. Then c is whatever the periodic family says (0.2072 to 0.2117),
   the joint χ² is 22.6 on 10 or 24.4 on 11 (p ≈ 0.01, marginal; the hull part alone is 14 to 19 for six points
   and three parameters of its own), and the hull's local slope has stopped rising: it stays at 0.217 to 0.218
   out to A = 234. The alternative is that periodic faces up to 6 cubes wide are still 5 to 10% cheap. The data do
   not choose: both readings forecast ln τ(A = 135) = 29.22 to 29.25 (measured 29.34 ± 0.25, 16 deaths) and differ
   by 0.12 at A = 165, where one death costs about 10⁶ GPU-seconds.
5. **If one number must be quoted** [conjectured]: **c_inf = 0.2085 ± 0.004**, the periodic family's, *with a
   one-sided systematic of +0.02* that stands until the hull family is understood. I prefer the periodic value
   because that family has no boundary and its correction is small (rim cells are 38 to 70% of every hull face
   measured, and no three-parameter form fits the hull's A = 30 point). "About 0.21" survives as a rounding of the
   periodic family; "0.2077 + 0.55/A" (retired) was a hull-face fit whose constant no hull fit of this page
   reproduces.
6. Out-of-sample forecasts of the largest one or two sizes (the table below) **do not discriminate** between the
   defensible models: the held-out sizes are the least precise points (± 0.04 to ± 0.25), and the models differ
   there by less than 0.1. They do reject the area-only line in both families.
7. O_h-symmetric faces (A = 360 to 828) put no constraint on c_inf: six times their cost per cell is 0.218 ± 0.007
   or 0.249 ± 0.015 (cube-centred, log or rim correction), 0.2065 or 0.2294 (vertex-centred, neither form fits),
   and equating it with c_inf is itself a conjecture ("lockstep").

## Data

`python3 research/constant/load.py --check` (→ `out/points.txt`). ln τ_face = ln(faces × exposure / deaths),
error 1/√deaths; faces = 2 (slab), 8 (asymmetric hull), 1 (O_h hull: the eight die together).

| family | points | source files | notes |
|---|---|---|---|
| periodic, rectangular s × M × 8 | 15 slabs (14 shapes), A = 54 to 126 | `research/data/gpu_facelaw/fwslab*.json` | firewall channel resolved; ln(2E/F) |
| periodic, twisted | 8 + 9 + 14 classes at A = 48, 60, 72 (shortest loop² ≥ 3) | `research/shape/data/A60.csv, A72.csv`; `research/shape2/data/A48.csv, A60.csv, A72x.csv` | recomputed from exposure and deaths |
| hull, asymmetric | A = 30, 45, 63, 84, 108, 135 | `research/fluct/data/qsd_summary.json` (R = 7 to 13), `gpu_facelaw/R*_A10G.json` (R = 11 to 17, T0 = 200) | pooled by size |
| hull, O_h-symmetric | 8 + 8 sizes, A = 360 to 828 | `research/fluct/data/sym_residence.csv` (fresh soups only), `gpu_facelaw/sym[cv]R*.json` (T0 = 1000) | copies of the side-16 cube excluded |

Periodic runs of one torus are pooled by isometry class of the period lattice (reduced Gram matrix, `lat.py`;
`python3 research/constant/lat.py selftest` checks it against research/shape2's class tables), summing exposure
and deaths; 42 classes with shortest loop² ≥ 3 in all. "Wide" = shortest loop² ≥ 12 (26 classes).

Where sources disagree, or my value differs from a quoted one:

- Hull A = 84: CPU 18.077 ± 0.054 (342 deaths) against GPU 18.141 ± 0.005; pooled 18.1407 is used. Local slopes
  on the pooled values: 0.2010, 0.2119, 0.2146, 0.2181 ± 0.0013, 0.2209 ± 0.0093 (quoted 0.201 … 0.221: agree).
- 6 × 6 × 8: I use the firewall-resolved run alone, 22.568 ± 0.041 (592 deaths). CLAIMS GP8's "pooled 22.537"
  adds the earlier run, whose statistic is the first event of either kind.
- 3 × 6 × 8: its two GPU runs give 11.0845 ± 0.0007 and 11.0813 ± 0.0005 (χ² 12.6 on 1; the launch caps differ).
  Width 3 enters no fit of c here.
- Width families: one slope with an offset per width gives 0.2072 ± 0.0001 with offsets 0.055, 0.123, 0.206,
  χ² 8.3 on 7 (ledger GP9: 0.053, 0.121, 0.203, 8.4 on 8; I pool the GPU's 4 × 5 and 4 × 6 with the CPU runs of the
  same tori and count 6 × 4 with 4 × 6). a + cA − βM: 0.2117, β = 0.054, χ² 5.3 on 8 (ledger: 5.6 on 9).
- Cost per cell by shortest loop between areas (`shape_models.py slopes`): 48 → 60: 0.1148, 0.1414, 0.1918, 0.2074,
  0.2090, 0.2127 at loop² 3, 4, 7, 12, 13, 16; 60 → 72: 0.1107, 0.1353, 0.1872, 0.2047, 0.2062, 0.2072 (ledger
  SH3: 0.2125 and 0.208 at loop² 16; mine include the GPU's 4 × 5 and 4 × 6).
- Not used: `research/peeling/slab_area.csv` (first peels not screened for firewalls), the mirror-cut hulls of the
  swarm's exam (three values, no tracked data file), research/shape3 (in flight; see PREDICTIONS.md).

## Models, as stated before fitting

ln τ_face = c_inf·A + (correction of the family) + constant. A fit **fails** if its χ² has p < 0.01 at the
statistical errors.

Hull faces (triangle of side k, A = 3k(k + 1)/2; 6k − 3 of its cells lie on the hull's edges and belong to two
faces, three of them to four):

| | form | parameters | meaning of the correction |
|---|---|---|---|
| H0 | a + cA | 2 | none |
| H1 | a + cA + r·k | 3 | rim cells cost c + r/6 each instead of c (r < 0: fewer neighbours, cheaper; r > 0: held up by the neighbouring faces) |
| HL | a + cA + p·ln A | 3 | a power of A in the prefactor of the rate (entropy of where the collapse starts, or a fluctuating edge) |
| H2 | a + cA + r·k + q/k | 4 | rim plus the next order (corners interacting with the rim) |

Periodic faces (no rim; period lattice with sides s ≤ M for rectangular slabs, shape modulus τ in general):

| | form | parameters | meaning |
|---|---|---|---|
| PA | a + cA | 2 | none |
| PO | a(s) + cA | 4 (three widths) | transfer-matrix picture: a strip of width s has its own prefactor, one cost per cell |
| PM | a + cA − βM | 3 | the cost per cell of a strip of width s is c − β/(3s) |
| PS | a + cA + αs | 3 | an offset growing with the short side |
| PSM | a + cA + αs + βM | 4 | both; how well c is known when the side term's form is not assumed |
| Pcw | a + cA + κF(τ) | 3 | **massless (capillary wave)**: F = −½ ln Im τ − 2 ln\|η(τ)\|, the log of the free-boson partition function of the face torus (Caselle, Gliozzi, Vinti 1993: κ = −1 for an Ising interface) |
| mexp, mk0 | a + A[c − g·Σ_v f(\|v\|/ξ)] | 4 | **massive**: each nonzero period vector v lowers the cost per cell; f = e^{−r} or K₀(r); ξ ≤ 3 cube steps |
| mexp2 | the same + h·Σ_v f | 5 | the intercept moves with the same sum |

Lengths are in cube steps of the face plane (the unit in which a slab's side is counted; one step = √2 cube sides).
Joint models: one c, the hull's correction and the periodic family's, fitted to both families together.

## Results

`python3 research/constant/fit.py` (→ `out/main_table.txt`: every fit with the residual of every point; 35 s).
Summary of sections 1 to 3 [fitted: all parameters of each form]; "−1", "−2": the form fitted without the largest
one or two sizes (of each width, for the rectangular family) and scored on them, Σz² / points and the largest
residual, z = residual/√(error² + forecast error²):

| family | model | par. | χ²/dof | verdict | c | −1 | −2 |
|---|---|---:|---:|---|---:|---|---|
| hull, six sizes | H0 | 2 | 1491.7/4 | fails | 0.2090 | 5.3/1, 0.66 | 14.2/2, 0.67 |
| | H1 rim | 3 | 106.9/3 | fails | 0.2480 | 0.2/1, 0.12 | 0.5/2, 0.14 |
| | HL log | 3 | 69.1/3 | fails | 0.2293 | 0.0/1, 0.05 | 0.3/2, 0.06 |
| | H2 rim + 1/k | 4 | 6.9/2 | fits (p 0.03) | 0.1917 ± 0.0057 | 0.8/1, 0.24 | 7.5/2, 0.31 |
| hull, A ≥ 45 | H0 | 2 | 100.3/3 | fails | 0.2128 | 2.1/1, 0.38 | 9.7/2, 0.39 |
| | **H1 rim** | 3 | 1.3/2 | fits | **0.2317 ± 0.0019** | 0.1/1, 0.10 | 1.3/2, 0.11 |
| | **HL log** | 3 | 1.8/2 | fits | **0.2226 ± 0.0010** | 0.2/1, 0.12 | 1.9/2, 0.14 |
| | H2 | 4 | 0.0/1 | fits | 0.263 ± 0.028 | 0.0/1, 0.02 | – |
| periodic, s = 4 alone | PA | 2 | 4.3/3 | fits | 0.2072 ± 0.0001 | 1.8/1, 0.06 | 1.8/2, 0.06 |
| periodic, s = 5 alone | PA | 2 | 0.3/2 | fits | 0.2082 ± 0.0006 | 0.1/1, 0.02 | 0.2/2, 0.02 |
| periodic, s = 4, 5, 6 (11 classes) | PA | 2 | 515.5/9 | fails | 0.2085 | 6.2/3, 0.16 | 6.5/6, 0.16 |
| | **PO offsets** | 4 | 8.3/7 | fits | **0.2072 ± 0.0001** | 3.5/3, 0.11 | – |
| | **PM long side** | 3 | 5.3/8 | fits | **0.2117 ± 0.0002** | 2.2/3, 0.06 | 2.7/6, 0.06 |
| | PS short side | 3 | 8.4/8 | fits | 0.2072 ± 0.0001 | 3.6/3, 0.11 | 3.7/6, 0.11 |
| | PSM both | 4 | 5.3/7 | fits | 0.2121 ± 0.0028 | 2.3/3, 0.06 | 2.4/6, 0.06 |
| | Pcw | 3 | 38.0/8 | fails | 0.2105 | 0.3/3, 0.02 | 4.4/6, 0.05 |
| | mexp | 4 | 7.8/7 | fits (degenerate) | 0.2080 ± 0.0003 | 3.3/3, 0.13 | 3.9/6, 0.13 |
| periodic, wide (26 classes) | PA | 2 | 1902.7/24 | fails | 0.2104 | 15.1/5, 0.19 | – |
| | Pcw | 3 | 320.1/23 | fails | 0.2114 | 8.4/5, 0.09 | – |
| | mexp | 4 | 205.5/22 | fails | 0.2050 | 7.7/5, 0.19 | – |
| | mk0 | 4 | 209.0/22 | fails | 0.2048 | 7.7/5, 0.19 | – |

(For the wide set the held-out points are the five classes with A ≥ 105. The s = 6 width has two points, slope
0.2131 ± 0.0062. On the rectangular family alone mexp runs to ξ = 0.14 with g at its bound: it has become the
offset model. H0 and PA are the only forms the forecasts reject.)

Further [measured / fitted]:

- **No three-parameter form fits all six hull sizes**: the A = 30 face (21 of its 30 cells on the rim) lies 0.09 to
  0.10 above the forms that fit A ≥ 45 (30 standard errors). With four parameters the hull's c is free between 0.19 and 0.26.
- **Wide periodic faces at the level where shape is understood.** No global form fits the 26 wide classes at their
  statistical errors (± 0.001 to 0.003 at A ≤ 75). Two equal-area, equal-loop pairs differ by 0.015 for a reason
  nobody has found (CLAIMS SH2); with 0.015 added in quadrature to every error, Pcw fits (χ² 18.6 on 23, c =
  0.2108 ± 0.0003, κ = −1.19 ± 0.11) and so does the massive form (15.4 on 22, c = 0.2063 ± 0.0008, ξ = 0.79 ± 0.16
  cube steps = 1.1 cube sides); the area-only line does not (134.9 on 24).
- **Equilateral tori**, the one family of constant shape (4 × 4, 5 × 5, 6 × 6: only the size changes): local slopes
  0.2122 ± 0.0001 (A = 48 → 75) and 0.2093 ± 0.0012 (75 → 108), a change of −0.0029 ± 0.0013 (2.3σ). A massive
  correction predicts a fall towards c, the capillary-wave form none, the hull reading a rise.
- **Symmetric faces** (c₆ per cell of the symmetric face): cube-centred, H1: 6c₆ = 0.249 ± 0.015, χ² 2.9 on 5; HL:
  0.218 ± 0.007, 2.8 on 5; both forecast the held-out A = 759 and 828 within 0.04. Vertex-centred: neither fits
  (χ² 158 and 162 on 5). The ledger's S2 fixes the slope at 0.209/6; left free, it is not determined.
- **The 2D relative has the same disease, larger** (`extras.py toy`, from research/toy2d's tables): rings have local
  slopes 0.44 to 0.38 (falling), edges of boxes 0.33 to 0.36, at L = 12 to 36. There the cornered family is
  *below* the wrapped one; in gump the rimmed family is above.

Joint fits (section 4 of the table) [fitted: c, the hull's correction, the periodic family's]:

| hull correction × periodic correction | c_hull − c_per, separately | joint c | joint χ²/dof | hull part | penalty for one c |
|---|---|---:|---:|---:|---:|
| rim × offsets | +0.0245 ± 0.0019 | 0.2073 | 175.3/10 | 166.4 on 5 | 165.7 |
| log × offsets | +0.0154 ± 0.0010 | 0.2074 | 248.2/10 | 236.6 on 5 | 238.1 |
| rim × long side | +0.0200 ± 0.0019 | 0.2118 | 116.7/11 | 110.5 on 5 | 110.1 |
| log × long side | +0.0109 ± 0.0010 | 0.2120 | 124.7/11 | 115.9 on 5 | 117.6 |
| rim × capillary wave | +0.0212 ± 0.0019 | 0.2106 | 163.2/11 | 124.6 on 5 | 124.0 |
| log × capillary wave | +0.0121 ± 0.0010 | 0.2107 | 186.0/11 | 145.3 on 5 | 146.2 |
| rim + 1/k (six sizes) × offsets | −0.0155 ± 0.0057 | 0.2072 | 22.6/10 (p 0.012) | 14.3 on 6 | 7.3 |
| rim + 1/k (six sizes) × long side | −0.0200 ± 0.0057 | 0.2117 | 24.4/11 (p 0.011) | 19.1 on 6 | 12.2 |
| rim + 1/k (six sizes) × capillary wave | −0.0188 ± 0.0057 | 0.2105 | 55.7/11 | 17.7 on 6 | 10.8 |

The periodic points have errors ten times smaller than the hull's large sizes, so a joint fit takes its c from the
periodic family and the hull pays. In the last three rows the hull's rim coefficient is r = +0.40, +0.29, +0.32 per
unit of side and q = +9.7, +8.7, +9.0.

## The two wrap-around models asked for by the lead

`python3 research/constant/shape_models.py tests` (→ `out/shape_tests.txt`), `slopes` (→ `out/slopes.txt`),
`pairs` (→ `out/pairs.txt`). All [fitted: a, c and the model's own parameters].

| model | par. | census A = 48, 60 (17 classes): χ²/dof | → A = 72 (14 classes): rms residual | wide (26): χ²/dof | wide → thin: rms | thin → wide: rms | all 42: χ²/dof |
|---|---:|---:|---:|---:|---:|---:|---:|
| area only | 2 | 1,128,759/15 | 1.23 | 1902.7/24 | 1.49 | 1.57 | 1,983,098/40 |
| (a) capillary wave | 3 | 48,004/14 | 0.27 | 320.1/23 | 0.29 | 0.58 | 89,799/39 |
| (b) massive, e^{−r} | 4 | 20,925/13 (ξ at its bound) | 0.14 | 205.5/22 | 0.58 | 0.11 (ξ at bound) | 25,598/38 |
| (b) massive, K₀ | 4 | 33,260/13 (ξ at bound) | 0.15 | 209.0/22 | 0.52 | 0.32 | 47,172/38 |
| (b) + intercept term | 5 | 9,304/12 | 0.18 | 180.7/21 | 0.52 | 0.48 | 19,039/37 |

- **Neither model, nor any variant tried, fits at any scope, and none carries from thin faces to wide ones or
  back.** Thin tori (shortest loop² 3, 4, 7) differ from wide ones in the intercept as well as in the cost per cell
  (the line through a loop class at A = 48 and 60 has intercept +3.13, +2.70, +0.61, against −0.03 to −0.28 for
  the wide classes; `out/slopes.txt`), which a
  correction to the cost per cell alone cannot give; with the thin tori in, the massive fits run to the bound on ξ,
  where the lattice sum is degenerate with a + cA. The five-parameter variant brings the rms residual over all 42
  classes (ln τ from 8.6 to 26.4) to 0.08 with ξ = 0.51 cube steps = 0.72 cube sides, the bulk correlation length
  (0.68), but its χ² is 19,039 on 37.
- **The lead's reading of the census holds as a description**: the deficit of the cost per cell falls about
  exponentially with the shortest loop, not as its inverse square. Fitted to the six loop classes, c − D·e^{−s/ξ}
  gives ξ = 0.71 ± 0.01 and 0.74 ± 0.02 cube steps (1.0 cube side) with residuals ≤ 0.006; c − D/s² has residuals
  up to 0.0085 and twice the χ² (770 against 353 between A = 48 and 60, 175 against 95 between 60 and 72); a free
  power is 2.3 to 2.4. All three fail formally, and the asymptote of the exponential form is 0.2171 ± 0.0003 from
  one pair of areas and 0.2122 ± 0.0005 from the other: **this route does not give c_inf to better than 0.005.**
- **Among wide faces the capillary-wave term does most of the work with one parameter**: κ = −1.37 ± 0.03 (wide,
  statistical errors), −1.19 ± 0.11 (with the 0.015 floor), −1.01 ± 0.01 on the census classes with loop² ≥ 7
  (χ² 860 on 8: it fails there too; Ising interface: −1). It forecasts the held-out A ≥ 105 classes best (largest residual 0.09 against 0.19).
  The massive form fits the same faces slightly better in-sample with ξ = 0.95 ± 0.07 cube steps (1.3 cube sides,
  twice the bulk correlation length) and a lower c (0.205), and under-forecasts every A ≥ 105 class (+0.03 to
  +0.19). The two forms differ by 0.005 in c; the wide data do not choose.
- **The second variable has the models' sign and about four times their size.** For the
  equal-area, equal-loop pairs both models give d ≥ 0 always and nearly the same number (+0.004 for P1 and P2,
  +0.0006 for P3), against the measured +0.0151 ± 0.0017, +0.0142 ± 0.0019, +0.0063 ± 0.0035: 6σ and 5σ low.
  Forecasts for every pair of research/shape3's plan, and what of that experiment I had already seen, are in
  `PREDICTIONS.md` (B).

## Forecasts committed before results

`PREDICTIONS.md` (commit 5dd18b9): (A) empty patches on the 12 × 12 × 8 slab: c = 0.212 ± 0.015, σ > 0, σ = 0.34 per
cube step of perimeter (0.15 to 0.6); (B) the wrap-around models on research/shape3's pairs.

## Three measurements that would shrink the uncertainty most

Costs from `research/gpu/README.md` (A10G: about 2.4 × 10¹² node-updates/s; a slab of n columns has 24n nodes).

1. **Equilateral face tori** (`extras.py equilateral`): n = 19, 21, 27, 28, 31, 37 columns (A = 57, 63, 81, 84, 93,
   111; lattices (1,7,19), (1,4,21), (3,3,9), (2,4,14), (1,5,31), (1,10,37)), firewall channel resolved, with
   10⁵ face deaths each for A ≤ 84, 3 × 10⁴ at A = 93, 2,000 at A = 111, and 6 × 6 × 8 topped up to 2,000. About
   3 GPU-hours, scaled from the 6 × 6 × 8 run's 2,367 face deaths per hour (`extras.py costs`). *Decides* the slope of the one constant-shape family to ± 0.001 at nine sizes: falling towards
   0.206 (massive), flat at 0.209 to 0.212 (capillary wave: then c_inf is that slope, with no shape model), or
   rising towards the hull's 0.22. Now: 0.2122 then 0.2093 ± 0.0012.
2. **Hull faces of equal area and different rim** (truncated octahedral hulls, unequal face offsets, A ≈ 63 to 84,
   10⁴ deaths per vessel, minutes of GPU each). *Decides* the sign of the rim term directly instead of through the
   size dependence: the one-term reading needs −0.06 per rim cell (c_inf ≈ 0.223 to 0.232), the reading compatible
   with the periodic constant +0.05 to +0.07; six rim cells more or less move ln τ by ∓ or ± 0.36. Needs a vessel
   builder for general diagonal hulls and a check of it against the engine.
3. **The slope of width 6**: 6 × 6 × 8 to 2,000 face deaths (0.6 GPU-hour more) and 6 × 7 × 8 to 800 (about 15
   GPU-hours at the recorded 46 face deaths per hour, most of a month's budget; 400 deaths give ± 0.003), with one
   6 × 6 × 12 run of 600 deaths beside them (thickness 8 has never been tested at A ≥ 108). *Decides* whether the
   cost per cell within a width is still rising: 0.2072, 0.2082 ± 0.0006, then 0.2131 ± 0.0062 now. 0.208 at
   ± 0.002 closes the periodic family at ≤ 0.212 and leaves the hull's rim as the unknown; ≥ 0.215 means periodic
   faces this narrow are not yet asymptotic.

More hull deaths at A = 135, or A = 165, would not decide: every reading forecasts 29.22 to 29.25 and 35.7 to 35.8.

## Methods that failed, and why

- **Out-of-sample forecasting as an arbiter.** Every defensible form passes; the held-out sizes are too imprecise.
- **One global shape law for periodic faces** (capillary wave, loop sums with two kernels, shortest loop only, an
  added intercept term): all fail at the statistical errors, as research/shape2's laws did; a + cA is forced on
  lattices of different shape at different areas, and the unexplained 0.015 is ten error bars.
- **Reading c_inf off the loop dependence** (asymptote of the cost per cell against the shortest loop): unstable
  at 0.005 between pairs of areas, because slopes between areas compare different lattices.
- **The massive form on the rectangular family alone**: degenerate (ξ → 0.14, g at its bound); three widths cannot
  fix a decay length.
- **Symmetric faces as a lever** (large A, cheap): the slope depends on the correction's form by 15% and its link
  to c_inf is a conjecture.
- **A four-parameter hull fit**: c anywhere from 0.19 to 0.26.

## Not checked

- No new run; nothing here tests the GPU kernel or the steppers. The hull values at A ≥ 108 and the slab values
  at A ≥ 96 come from one GPU implementation (ledger grade B−).
- Thickness: every periodic value is for 8 layers. That 8 layers suffice at A ≥ 108 is not tested anywhere.
- Soup transients and caps: ages below T0 are excluded for hulls (200) but not for slabs; the sources bound the
  effect at ≤ 0.005 in ln τ, which is larger than the statistical error of the best points. I did not re-derive
  those bounds. The 0.015 floor is a round number taken from the pair differences, not a fitted variance.
- Loop² 4 tori are multigraphs and carry a tie-resolution bias of about −0.018 (research/shape2); they are in the
  thin set as measured.
- Classes pooled across codes (GPU, rep.c) assume equal hazards; the pooled χ² are printed by `load.py` (worst:
  3 × 6 × 8, 12.6 on 1).
- The 2D relative was not fitted, only its local slopes printed. The mirror-cut hulls and research/shape3 were not
  used. The lifetimes of research/peeling's CPU slabs (A = 12 to 84) were not compared point by point.
- Forecast errors use the parameter covariance inflated by χ²/dof and treat points as independent.
- Whether "cost per cell" is the right asymptotic notion at all (an extensive large-deviation rate) is assumed, not
  tested; the empty-patch experiment is the first test of it for gump.

## Reproduce

    python3 research/constant/lat.py selftest            # lattice code against research/shape2's class tables
    python3 research/constant/load.py --check            # every point, and quoted values against data
    python3 research/constant/fit.py                     # the main table (35 s) -> out/main_table.txt
    python3 research/constant/shape_models.py tests      # wrap-around models (4 min) -> out/shape_tests.txt
    python3 research/constant/shape_models.py slopes     # cost per cell against the shortest loop
    python3 research/constant/shape_models.py pairs      # pair forecasts -> out/pairs.txt
    python3 research/constant/extras.py toy; python3 research/constant/extras.py equilateral
    python3 research/constant/extras.py costs            # recorded GPU death rates of the widest slabs
    python3 research/constant/patch_geom.py              # perimeter measures of a rhombic patch
