# research/constant: forecasts committed before the results

Analyst on the constant, 2026-11-14. Two forecasts. Both are conjectures until scored. Repository state when this
file was first committed: HEAD 020a882; `ls research/data/gpu_facelaw | grep -ci patch` gives 0 and nothing of the
empty-patch experiment exists in the tree.

## A. Empty patches on a face too large to die (GPU session, slab 12 × 12 × 8)

The experiment (NOTEBOOK 2026-11-14, "a forecast before the run"): on the two faces (A = 432 each) of a periodic
slab 12 × 12 × 8, the frequency P with which a patch is entirely dead; rhombi a × b of 3ab cells (1 × 1 to 6 × 6)
and strips 1 × b. Hypothesis under test: ln P = const − c·cells − σ·perimeter, with c the cost per cell of an
unwrapped, rimless face. The lead forecast c = 0.21 ± 0.015 and gave no forecast for σ.

No simulation of patches was made for this forecast. It rests on the lifetimes already in the repository
(`python3 research/constant/load.py`), on the fits of this directory as they stood at this commit
(`out/shape_tests_summary.txt`, `out/pairs.txt`; hull fits in the write-up), on the single-cell limit, and on the
2D toy's empty windows (`research/theory/exponent.md`, section 4).

Units. A patch a × b has perimeter 2(a + b) in cube steps of the face plane, 8(a + b) − 4 cut in-layer bonds and
(for a, b ≥ 2) 5(a + b) − 8 boundary cells (`python3 research/constant/patch_geom.py`). I state σ per cube step
of perimeter; per cut in-layer bond it is σ/4, per boundary cell about σ/2.5.

**Forecast.**

1. **c = 0.212 ± 0.015** (68%), for the three-parameter fit over rhombi from 2 × 2 up. 95%: 0.185 to 0.24.
   I put about 15% on c > 0.222.
2. **σ > 0** (the perimeter makes an empty patch rarer; the cost per cell of small patches is above c and falls
   towards it). **Size: σ = 0.34 per cube step of perimeter (68% range 0.15 to 0.6)**, that is about 0.086 per cut
   in-layer bond, 0.14 per boundary cell. Equivalent statement: the perimeter term is as large as emptying a margin
   of about 1.6 further cells (range 0.7 to 2.8) per cube step of boundary at the bulk price.
3. const = 0 ± 0.7 when the perimeter is counted in cut bonds (the form then passes through ln P = 0 for the empty
   set).
4. What these give, as −ln P (central value, and the range from σ alone):
   single cell 0.73 (input: face density 0.52); 1 × 1: 1.7 (1.1 to 2.4); 2 × 2: 5.0 (3.6 to 6.7);
   3 × 3: 9.5 (7.4 to 12.3); 4 × 4: 15.3 (12.4 to 19.2); 5 × 5: 22.4 (18.8 to 27.3); 6 × 6: 30.8 (26.3 to 36.7).
   (Computed as c·cells + (σ/4)·cut bonds with c = 0.212.)
   Strips 1 × b: −ln P rises by 3c + 2σ = 1.32 per cube step (0.94 to 1.84), 0.44 per cell (0.31 to 0.61): a strip
   never shows the bulk price.
5. Apparent cost per cell (−ln P)/cells falls monotonically with the size of the rhombus: about 0.56, 0.41, 0.35,
   0.32, 0.30, 0.285 for a = 1 … 6. If it rises anywhere between 2 × 2 and 5 × 5, my reasoning for σ is wrong.

**Reasons.**

- *c.* The families in hand do not agree on a cost per cell (write-up, verdict). Periodic faces, the only family
  with no boundary, give 0.205 to 0.212 depending on the wrap-around model (slopes within one width 0.2072 and
  0.2082 ± 0.0006; equilateral tori 4 × 4, 5 × 5, 6 × 6: local slopes 0.2122 then 0.2093 ± 0.0012). Hull faces give
  0.2226 (logarithmic correction) to 0.2317 (rim correction proportional to the side) when their A ≥ 45 points are
  fitted with one correction term, and local slopes of 0.218 to 0.221 at A = 84 to 135. A patch is flat and has
  every neighbour, like a periodic face, so I centre on the periodic family; but its boundary is a live face, as a
  hull face's is, and a fit of five sizes with boundary cells making up 48% to 100% of the patch has the hull
  family's weakness: one more slowly varying term (λ ln cells with |λ| near 1) would move the fitted c by 0.02 to
  0.03. Hence a centre just above the periodic values and an error as wide as the lead's.
- *Sign of σ.* (i) One cell is dead with probability 1 − ρ ≈ 0.48: 0.73 nats for one cell, 3.5 times the bulk
  price; the cost per cell has to come down with size. (ii) A dead face cell whose six in-layer neighbours are dead
  cannot be born (it has at most 3 live neighbours, all below; birth needs 4): the interior of an empty patch is
  held for a generation at no cost, and only cells with a live in-layer neighbour (the boundary cells) have to be
  kept dead against births. (iii) The 2D relative: the cost of lengthening an empty window falls from 0.61 for
  the first cell to 0.43 at 10 cells and about 0.385 at 30 to 40.
- *Size of σ.* Bond-additive interpolation anchored on the single cell: −ln P = c·cells + σ_b·(cut in-layer
  bonds), exact for the empty set and for one cell (6 cut bonds): σ_b = (0.73 − 0.212)/6 = 0.086. Lower end:
  the surroundings of a large hole are depleted, which cheapens its boundary (half the anchored value). Upper end:
  in the 2D toy the excess over the bulk price keeps growing with the window (0.23 nats at one cell, 1.0 to 1.5 at
  10 to 30 cells), four to six times the single-cell anchor; if gump does a fraction of that, σ is near 0.6.
- A consequence I am committing to: because σ·perimeter is 3 to 8 nats out of 5 to 31, the experiment measures σ
  better than c. With sizes to 5 × 5 only, I expect the statistical error on c to be near ± 0.01 and the systematic
  one (choice of perimeter measure, inclusion of 1 × 1, a logarithmic term) to be larger.

**What each outcome would decide** (write-up, section "the tension"):
c ≤ 0.214 with σ > 0: the periodic family's constant stands, and the hull faces' local slope (0.218 to 0.221) has
to come down beyond A = 135. c ≥ 0.222: the hull family's reading stands and periodic faces up to 6 cubes wide are
still about 5% cheap. σ ≤ 0: the static picture (positive association of dead cells) is wrong for gump and this
forecast's reasoning with it.

## B. Equal area, equal shortest loop: what the two wrap-around models forecast (research/shape3)

Asked by the lead while the pairs were being measured. Models, as stated in the write-up:

- **(a) massless, capillary wave:** ln τ = a + c·A + κ·F(τ), F = −½ ln Im τ − 2 ln|η(τ)| the logarithm of the
  free-boson partition function of the face torus with shape modulus τ (`lat.F_boson`). Three parameters.
- **(b) massive:** ln τ = a + A·[c − g·Σ_v f(|v|/ξ)], the sum over every nonzero period vector of the face, f(r) =
  e^{−r} (b-exp) or K₀(r) (b-K0). Four parameters. ξ bounded by 3 cube steps.

d(X → Y) = ln τ_face(Y) − ln τ_face(X), Y the lattice with the longer second loop, as in
`research/shape3/PREDICTIONS.md`. Forecasts: `python3 research/constant/shape_models.py pairs` (→ `out/pairs.txt`).
Primary fit **W**: every wide periodic face (shortest loop² ≥ 12; 26 classes, A = 48 to 126; the GPU's rectangular
slabs, research/shape, research/shape2; nothing from research/shape3). The other columns show how little the
forecast depends on the fitting set: **C** = the census classes at A = 48 and 60 with loop² ≥ 7 (the lead's
prescription, thin tori left out), **C3** = the same with the thin tori (loop² 3 and 4) in, **P7** = every periodic
face with loop² ≥ 7.

| pair | A | Gram X → Y | (a) W | (b-exp) W | (b-K0) W | range over C, C3, P7, all three models |
|---|---:|---|---:|---:|---:|---|
| P1 | 48 | (12,0,16) → (12,12,19) | +0.0039 | +0.0037 | +0.0037 | +0.0023 to +0.0036 |
| P2 | 60 | (16,4,19) → (16,12,21) | +0.0043 | +0.0042 | +0.0041 | +0.0032 to +0.0048 |
| P3 | 60 | (12,0,25) → (12,12,28) | +0.0006 | +0.0006 | +0.0006 | +0.0005 to +0.0007 |
| T01 | 72 | (16,0,27) → (16,8,28) | +0.0008 | +0.0007 | +0.0007 | +0.0006 to +0.0010 |
| T12 | 72 | (16,8,28) → (16,16,31) | +0.0008 | +0.0007 | +0.0007 | +0.0006 to +0.0010 |
| N72 | 72 | (12,0,36) → (12,12,39) | +0.0001 | +0.0001 | +0.0001 | +0.0001 |
| Q36 | 36 | (9,0,12) → (9,6,13) | +0.0029 | +0.0025 | +0.0026 | +0.0012 to +0.0027 |
| Q45 | 45 | (9,3,19) → (9,9,21) | +0.0005 | +0.0004 | +0.0005 | +0.0003 to +0.0004 |
| Q54 | 54 | (9,0,27) → (9,6,28) | +0.0001 | +0.0001 | +0.0001 | +0.0001 |
| Q63 | 63 | (9,3,37) → (9,9,39) | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

The fits' own errors on these differences are ≤ 0.0007 (with the parameter covariance inflated by χ²/dof).

**In words.** Both models put the longer-lived face where the second loop is longer (every d ≥ 0), as observed for
P1, P2 and P3. Both make the effect small: at most 0.004, and below 0.001 for every pair with h = Im τ ≥ 1.29
(T01, T12, N72, Q54, Q63). The three forecasts agree with one another to 0.0005 on every pair: within a group of
equal area and equal shortest loop the lattice moves along Im τ = const, and both a modular function and a lattice
sum reduce to the same leading term there (research/shape3's "structural fact"). So this experiment cannot tell
(a) from (b); it tests their common size.

**What is already known against them (not blind).** With amplitudes fixed by the gross dependence of the lifetime
on the shortest loop, both models are too small by a factor 3.5 to 4 on the published pairs: P1 measured
+0.0151 ± 0.0017, P2 +0.0142 ± 0.0019, P3 +0.0063 ± 0.0035 (CLAIMS SH2, REVIEW-shape2 claim 4) against +0.004,
+0.004, +0.0006. That is 6σ and 5σ on P1 and P2. So the "second variable" has the models' sign and not their
size: neither (a) nor (b), as fitted to lifetimes, is the second variable.

**Disclosure: what I had seen before writing this.** Not blind for four pairs. Before the lead's request reached
me I had opened `research/shape3/data/report.txt` (its first 60 lines, as of commit 831947a) and the first rows of
`research/shape3/data/runs.csv`, and read: P1 +0.0144 ± 0.0019, **Q36 −0.0223 ± 0.0007**, Q45 +0.0076 ± 0.0013,
Q54 −0.0020 ± 0.0019. (`research/shape3/PREDICTIONS.md` itself discloses the first-plan Q36 ≈ −0.023 to −0.027
and Q45 ≈ +0.007.) So I know that both models miss Q36 in sign (they cannot produce a negative d at all) and Q45
in size, and that Q54 agrees with them. I have also seen the published single runs at A = 72
(`research/shape/data/A72.csv`: T01 −0.013 ± 0.014, T12 −0.006 ± 0.014, N72 +0.003 ± 0.020), which are in fitting
set W. I have not opened anything else under `research/shape3/data/`, nor the results part of its README (a
placeholder when I read it), nor its later commits.

**Blind, then:** the cap-free, higher-precision values of T01, T12, N72, Q63, and the re-measurements of P2 and P3.
Forecast of both models for T01, T12, N72 and Q63: **zero within ± 0.001** (signs positive, sizes ≤ 0.001).
Scoring: z = (measured − forecast)/σ_measured for each pair (the forecast errors are negligible); a model is
refuted on the new pairs if Σz² over T01, T12, N72, Q63 has p < 0.01 (χ² on 4), the experiment's own criterion.
My expectation, outside the models: a measured |d| above 0.008 on T01 or T12 would be a second refutation of both;
values within ± 0.008 (2σ of the planned ± 0.004) leave the models standing on the wide pairs while P1, P2, Q36
and Q45 already refute them as a theory of the second variable.

## C. Equilateral face tori (constant shape): forecasts under three readings, before the request is sent

Added 2026-11-14 at the lead's request, before the GPU session is asked for measurement 1 of the write-up.
Repository state: HEAD 46a03df; of this family only 4 × 4, 5 × 5 and 6 × 6 are measured anywhere in the tracked data
(`python3 research/constant/extras.py equilateral`). Numbers: `python3 research/constant/eq_forecast.py`
(→ `out/eq_forecast.txt`).

**The tori.** Slab of **8 {111} layers**, soup 0.4, first event of a life (face death, or a transverse firewall
where one can form), ln τ_face = ln(2 × exposure / face deaths), as in `research/gpu/fwslab.py` and
`research/shape/tslab.py`. In-plane period lattice generated by (a, k) and (0, b) in the cube coordinates (i, j)
of research/shape (k = t − i − j), index n = ab, A = 3n. Every lattice below has reduced Gram matrix (n, n, n):
three shortest loops of length √n at 60°, the shape of 4 × 4, 5 × 5, 6 × 6. A mirror image (for example (1, 11, 19))
is the same torus.

| n | (a, k), (0, b) | A | shortest loop | cheapest firewall cut | planned deaths (error) |
|---:|---|---:|---:|---|---|
| 16 | (4, 0), (0, 4) | 48 | 4.00 | 144 | measured: 9.9324 ± 0.0020 |
| 19 | (1, 7), (0, 19) | 57 | 4.36 | none (every diagonal has 2 layers) | 10⁵ (± 0.0032) |
| 21 | (1, 4), (0, 21) | 63 | 4.58 | none | 10⁵ (± 0.0032) |
| 25 | (5, 0), (0, 5) | 75 | 5.00 | 180 | measured: 15.6614 ± 0.0026 |
| 27 | (3, 3), (0, 9) | 81 | 5.20 | 324 | 10⁵ (± 0.0032) |
| 28 | (2, 4), (0, 14) | 84 | 5.29 | 504 | 10⁵ (± 0.0032) |
| 31 | (1, 5), (0, 31) | 93 | 5.57 | none | 3 × 10⁴ (± 0.0058) |
| 36 | (6, 0), (0, 6) | 108 | 6.00 | 216 | measured 22.5684 ± 0.0411 (592); to 2,000 (± 0.022) |
| 37 | (1, 10), (0, 37) | 111 | 6.08 | none | 2,000 (± 0.022) |

(Cuts from the layer periods 4a, 4·gcd(k, b), 4·gcd(a + k, b) of `research/shape/README.md`; I checked the formula
on 4 × 6, (4,4),(0,6) and (1,1),(0,16) against the tables there, not with `tslab.py check`. The GPU session should
run that check and the engine comparison on each torus as research/shape did.)

**The readings.** All three are anchored on the three measured tori.

- **Flat** (the capillary-wave form: its shape term is constant in this family): ln τ = a + c·A. Weighted line
  through the anchors: c = 0.21214 ± 0.00012, a = −0.250; χ² 5.2 on 1 (p 0.022): the 6 × 6 run is already 0.093
  (2.3σ) below it. Forecast errors are inflated by √5.2.
- **Massive**: ln τ = a + A·[c − g·Σ_v e^{−|v|/ξ}], ξ = 0.95 cube steps (the wide-face fit), exact through the
  three anchors: c = 0.2069 ± 0.0023, g = 0.067 ± 0.029 (the errors are the 6 × 6 run's). With ξ = 0.70 or 1.20
  the forecasts move by ≤ 0.002 and c becomes 0.2080 or 0.2055. Errors: anchors, and half the ξ range.
- **Rising** (the hull family's constant is the true one and faces this narrow are still cheap): ln τ = a +
  c_h·A + ρ·√A with c_h = 0.2226 or 0.2317, (a, ρ) by weighted least squares on the anchors (ρ = −0.163, −0.306).
  **Already strained before any new run**: the 6 × 6 value lies 0.155 (3.8σ) and 0.208 (5.1σ) below these curves.

**Forecast ln τ_face.**

| n | A | flat | massive | rising to 0.2226 | rising to 0.2317 |
|---:|---:|---|---|---:|---:|
| 19 | 57 | 11.842 ± 0.004 | 11.855 ± 0.006 | 11.835 | 11.828 |
| 21 | 63 | 13.115 ± 0.004 | 13.128 ± 0.006 | 13.107 | 13.100 |
| 27 | 81 | 16.933 ± 0.007 | 16.923 ± 0.006 | 16.940 | 16.946 |
| 28 | 84 | 17.570 ± 0.008 | 17.552 ± 0.009 | 17.581 | 17.591 |
| 31 | 93 | 19.479 ± 0.010 | 19.437 ± 0.019 | 19.506 | 19.530 |
| 36 | 108 | 22.661 ± 0.014 | 22.568 ± 0.041 (the anchor) | 22.723 | 22.777 |
| 37 | 111 | 23.298 ± 0.015 | 23.194 ± 0.046 | 23.367 | 23.428 |

(The rising curves carry errors of about ± 0.004 from the two precise anchors; their own uncertainty is the choice
of c_h, shown by the two columns.)

**Forecast local slopes** (planned error from the planned deaths):

| A → A | flat | massive | rising (0.2226, 0.2317) | planned error |
|---|---:|---:|---|---:|
| 48 → 57 | 0.2121 | 0.2136 | 0.2113, 0.2106 | 0.0004 |
| 57 → 63 | 0.2121 | 0.2123 | 0.2121, 0.2120 | 0.0007 |
| 63 → 75 | 0.2121 | 0.2111 | 0.2128, 0.2133 | 0.0003 |
| 75 → 81 | 0.2121 | 0.2102 | 0.2134, 0.2144 | 0.0007 |
| 81 → 84 | 0.2121 | 0.2098 | 0.2136, 0.2149 | 0.0015 |
| 84 → 93 | 0.2121 | 0.2094 | 0.2139, 0.2155 | 0.0007 |
| 93 → 108 | 0.2121 | 0.2088 | 0.2145, 0.2165 | 0.0015 |
| 108 → 111 | 0.2121 | 0.2084 | 0.2148, 0.2171 | 0.0105 |
| **48 → 63** | 0.2121 | 0.2131 | 0.2116, 0.2112 | 0.0002 |
| **84 → 111** | 0.2121 | 0.2090 | 0.2143, 0.2162 | 0.0008 |

**What refutes each reading at the planned precision.** Write Δ = slope(84 → 111) − slope(48 → 63), planned error
± 0.0008: flat forecasts 0, massive −0.0041, rising +0.0027 or +0.0050.

- **Flat is refuted** if |Δ| > 0.0025 (3σ), or if a straight line through the nine tori has χ² with p < 0.01
  (7 dof). Single values that do it alone: ln τ(93) below 19.445 or above 19.513; A = 57 and 63 both more than
  0.010 off the chord between 4 × 4 and 5 × 5 on the same side.
- **Massive is refuted** if Δ > −0.0016 (the slope does not fall by at least 0.0016), or if A = 57 and 63 do not
  lie above the 4 × 4 – 5 × 5 chord (forecast +0.013 ± 0.006 each; refuted if both are below +0.001), or if the
  three-parameter fit of the form to the nine tori (ξ = 0.95) gives g ≤ 0 within 2σ or has p < 0.01. If it
  survives, that fit gives its c to about ± 0.0006 (now ± 0.0023).
- **Rising is refuted** if Δ < +0.0003 (3σ below its smaller forecast), or by either of ln τ(93) < 19.488 and the
  topped-up 6 × 6 below 22.656. It needs the present 6 × 6 run to be a 3.8σ low draw (or 8 layers to be too few at
  A = 108, which the 6 × 6 × 12 control of measurement 3 would show).
- The three are separated by 0.013 and 0.007 at A = 57 and 63 (massive above flat above rising), cross between 63
  and 81, and at A = 93 stand at 19.437, 19.479, 19.506 to 19.530 against a planned ± 0.006: A = 93 and the pair
  57, 63 carry the test; A = 111 adds little beyond the 6 × 6 top-up.
- An outcome none of them allows: a slope that falls and then rises, or A = 57 and 63 on opposite sides of the
  chord by more than 0.01. That would mean the equilateral tori do not form one family (some lattice-scale
  variable beyond the shape), as the equal-loop pairs already suggest at the 0.015 level; at that level
  (± 0.015 on any single torus) none of the three forecasts should be trusted individually, which is why the
  criteria above use the slopes and the common pattern.

**My own expectation** (conjecture): massive in sign, that is a falling slope, Δ between −0.005 and −0.001, with
c between 0.205 and 0.210. I put 60% on massive surviving, 30% on flat, under 10% on rising.
