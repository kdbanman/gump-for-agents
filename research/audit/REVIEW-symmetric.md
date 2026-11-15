# Review of research/theory/symmetric/: the symmetric collapse (rim term, 1/6, centring)

Adversarial review, 2026-11-15. Object: `research/theory/symmetric/` at dc213dc (README, PREDICTIONS blocks at
4f455e7, 814c3d4, 96e2292, 6061d61, 98a66d8, 4020d9e; `data/runs.csv`). Code in `research/audit/symmetric/`; bulk
output in `research/scratch/audit_symmetric/` (git-ignored). Nothing is imported from `research/theory/symmetric/`;
`sy.c`, `geom.py`, `run.py` were read, never compiled, imported or linked.

**The independent stepper** is `st.c` with its own geometry `geo.py` (cells and the 12 offsets written from
AUTOMATON.md section 2; vessels and slab tori built by own code; groups as matrices about the centre; orbits by
union-find; every generator checked to be an automorphism of the neighbour table). It runs the **full, unreduced
system** on a symmetric soup (one Bernoulli(0.4) draw per orbit), so it also tests the orbit-graph reduction
instead of relying on it. Bit-sliced, 256 replicas, a ripple counter for the 12-neighbour sum (sy.c: carry-save),
xoshiro256** soups, **events every generation** (sy.c: every 4), **Brent settled test** (snapshot at ages 1, 2, 4, …;
equality checked every generation; a settled life is recorded at the snapshot age, "S-low" at half of it), a
record per life with the mask of faces that died, so deaths can be split by face orbit. Same estimator form as the
line (ln τ_face = ln(nf·E/D), T0 = 512, ± 1/√D), own code (`ana.py`).

Validation (`validate.py`, output `validate_out.txt`): lane 0's whole state against `reference/oracle.py` on the
legacy array torus at every generation, 1,500 generations for v11c (R = 11, cube-centred) with c1, csz, c2v, d2h, ci,
c2e and v12v with c1, csz; 300 generations for the slab tori s8x2 cs and s4x2 c1, lifted to an H = 96 array torus
(the slab repeated with out-of-plane period (24,0,0), four dead layers between copies). In the vessels no cell
outside the octahedron ever came alive in the oracle (T2 checked along the way). Negative control (birth on 4 only
in the oracle) fails at generation 1. A later option (finer snapshot ladder) left the default mode's output
byte-identical (`cmp` of a 20,000-generation D2h run).

    python3 research/audit/symmetric/validate.py v11c c2e 1500 1      # one system (~1 s); all: validate_out.txt
    bash research/audit/symmetric/plan.sh 1; bash research/audit/symmetric/plan.sh 2    # A = 63 ladder, slab (two cores, ~5 min)
    bash research/audit/symmetric/plan.sh 3; bash research/audit/symmetric/plan.sh 4; bash research/audit/symmetric/plan.sh 5
    python3 research/audit/symmetric/ana.py        # every run: ln tau, T0 variants, S-low, deaths per face orbit
    python3 research/audit/symmetric/ladder.py     # the A = 63 ladder, the c2e split, the slab pair  (-> ladder_out.txt)
    python3 research/audit/symmetric/geomcheck.py  # section-1 geometry (-> geomcheck_out.txt)
    python3 research/audit/symmetric/fits.py       # refits from data/runs.csv (-> fits_out.txt)

Plan: seeds 9101–9108 fixed in 7b68ff0 before any run; part 3 (centring pairs, 9111–9115) in affc8b6, part 4
(9116) in 8c9d8c0, part 5 (9117–9118) in 2d0f4ed, each before its runs. Two slips, both fixed without changing a
seed or a length: plan.sh's lane-2 branch was a bare `else`, so starting part 3 restarted lane 2 and truncated the
ci file (killed; ci rerun with its planned seed, 3fdd41b); the ladder option divided by zero in the default mode
and part 5 died before producing output (8d7a7d7, rerun).

## Summary

| claim | verdict |
|---|---|
| 1a. Mirror/threefold on rim-free slab faces lengthen life | **stands with correction.** rect_8_2_cs − partner: **+0.926 ± 0.014** independently (theirs +0.872 ± 0.013). The quoted range "+0.4 to +1.9" takes its top from `rect_6_4_cs`, which has 69% firewalls and is "not used"; without it +0.4 to +1.65. Every family's offset shrinks with size, so the sign is established only at 36–72 quotient cells. |
| 1b. A = 63 ladder | **numbers stand; the c2e reading does not.** Own values agree with every rung within 2σ (largest: c2v +0.021 ± 0.012); D2h agrees once the settled-life bracket is narrowed (finer snapshot ladder). **c2e is mislabelled**: it pairs edge-sharing faces in only two of its four face orbits; the other two pair *opposite* faces. Split by face orbit, the rotated edge costs **−2.536 ± 0.015** cube-centred (mirror −2.194 ± 0.014) and **−1.960 ± 0.022** vertex-centred (mirror −2.120 ± 0.018); the opposite-paired orbits cost −0.10 ± 0.04 and +0.02 ± 0.05. "89% of the mirror" becomes 116% and 93%. |
| 1. "Rim, not mirror" | **stands only in a weaker form.** A mirror is not needed (rotation costs more); pairing faces that share no edge costs ≤ 0.1. But the coordinate mirror *is* the rim in every O_h face, so the vessel ladder cannot separate the two; the slab test is at 36–72 cells with shrinking offsets; and on hull faces T_d (diagonal mirrors, free rims) falls below T's slope by a term growing like √A (−0.06·√A at c = 0.209). A diagonal-mirror share of up to a third of the −0.196 is not excluded. |
| 2. The reduction [proved] | **stands, one false lemma.** Orbit-graph statement, free actions, the in-layer symmetry group, the coordinate-mirror statement, hull areas, rim counts and "rim removal gives the vertex-centred face of radius R−3" all check by computation. But "a node at distance > r from every cell with a non-trivial stabiliser has the lattice's radius-r neighbourhood" is false: c2e at R = 11 c has no fixed cell and 24 cells adjacent to their own image (quotient self-loops); ci at R = 12 v likewise (12). |
| 3. Size of the rim term and the √A coefficient | **numbers reproduce; "gives the fitted coefficient without using the fit" does not stand.** The comparison band (−0.157 to −0.244) is the fit's dependence on an assumed c, which spans nearly the whole plausible range of a rim measurement. The rim coefficient is compared to fits whose c (0.2072–0.2179) differs from T_d's own measured slope (0.2035); with c pinned at T_d's slope the O_h fit gives −0.127, and a synthetic O_h built from T_d's slope and a linear rim at 0.47/period returns −0.237 under the c = 0.209 fit, against −0.171 found. The agreement is a coincidence of ranges, not a test. |
| 4. "The rim term bends"; forecasts S3/S5 | **"bends" may not be stated as a finding.** The quadratic term (−0.062 ± 0.013 in marginal cost per period) rests on the two smallest sizes: without R = 23, 25 it is −0.018 ± 0.040. The second sub-series is flat (0.49, 0.49, 0.45 ± 0.08). The GPU leg needs an assumption about T_d. The forecasts 26.4 ± 0.3 and 25.65 ± 0.25 are 1.9σ apart in their own errors; the "linear" forecast is 26.2 with the all-size fit instead of the R ≤ 33 line. |
| 5. Slope × stabiliser order | **stands with correction.** T: 0.2091 ± 0.0016 (χ²-scaled; theirs 0.210 ± 0.003). T_d 315–459: 0.2035 ± 0.0024. The "0.201 and 0.208 in the two sub-series out to A = 570" are last local increments; weighted line fits of the sub-series give 0.1978 and 0.2024. T_d's slope is below T's by 0.006–0.011: "exactly c/6" is not supported for T_d at these sizes; "c/6 within 5%" is. |
| 6. Centring | **stands with correction.** Equal areas hold exactly (A_c(R) = A_v(R+1)); the A = 30, 45, 63 pairs are both this study's CPU runs, only A = 84's cube-centred value is the GPU's. Independent: **+0.754 ± 0.013, +0.725 ± 0.009, +0.655 ± 0.017** at A = 30, 45, 63 (line 0.747, 0.738, 0.676). But the free-rim difference is not constant (χ² 21 on 2; it falls by −0.037 ± 0.009 per unit √A): "an object of fixed size" does not stand. O_h fits not refitted. |
| 7. Forecast discipline, estimator | **stands with small corrections.** Every forecast commit precedes the JSON of the runs that test it (block 2b's case is disclosed). The tally 23/1/14 counts Q7 (3 sizes) as one statement but R1 as three; P4 is scored "failed" although its committed failure line was not crossed. "Two seeds for the D2h faces at R ≤ 14" is not what runs.csv holds (one job each). The estimator reproduces within ≤ 0.04 everywhere it was rerun, except where settled lives carry exposure (D2h). |

## 1. Claim 1: where the deficit sits

### 1b. The A = 63 ladder, independently (R = 11, cube-centred; full system, symmetric soups, events every generation)

`python3 research/audit/symmetric/ladder.py` (output `ladder_out.txt`):

| group | face orbits | this review | line (runs.csv) | step, this review | step, line |
|---|---:|---|---|---|---|
| c1 | 8 | **13.638 ± 0.010** (9,730 deaths) | 13.634 ± 0.018 | | |
| csz | 4 | **11.444 ± 0.010** | 11.456 ± 0.011 | **−2.194 ± 0.014** from c1 | −2.178 ± 0.021 |
| c2v | 2 | **9.312 ± 0.009** (S-low 9.303) | 9.291 ± 0.008 | **−2.133 ± 0.013** from csz | −2.165 ± 0.013 |
| D2h | 1 | **7.171 ± 0.009**, previous rung 7.146 (LADDER=16, seed 9116); Brent: 7.293, S-low 7.023 | 7.168 ± 0.003, S-low 7.122 | **−2.141 ± 0.013** from c2v | −2.124 |
| ci | 4 | **13.574 ± 0.014** (rerun after the truncation: identical) | 13.578 ± 0.014 | **−0.065 ± 0.017** from c1 | −0.056 ± 0.023 |
| c2e, all four orbits pooled | 4 | **11.712 ± 0.010** | 11.704 ± 0.005 | **−1.927 ± 0.014** from c1 | −1.930 ± 0.019 |
| c2e, the two orbits whose faces share an edge | 2 | **11.102 ± 0.010** (9,105 deaths) | not measured | **−2.536 ± 0.015** from c1 | |
| c2e, the two orbits pairing opposite faces | 2 | **13.537 ± 0.035** (798 deaths) | not measured | **−0.10 ± 0.04** from c1 | |

What each group does (`python3 research/audit/symmetric/geo.py info v11c G`; `geomcheck.py`):

- csz (z → −z): four face orbits, each a pair of faces sharing the z = 0 edge (12 shared cells); 144 fixed cells, 44
  on faces (the four z = 0 rim rows). c2v: two orbits of four faces, each face with its x = 0 and y = 0 edges on
  mirrors. D2h: one orbit, three edges. Labels as in the README.
- ci (inversion about the cube centre): acts freely (no fixed cell); four orbits, each a pair of opposite faces (no
  shared cell). As labelled.
- **c2e ((x,y,z) → (y,x,−z)) is mislabelled.** It acts freely on cells. Its face orbits are {(+++),(++−)} and
  {(−−+),(−−−)} (edge-sharing, 12 shared cells) but also {(+−+),(−+−)} and {(+−−),(−++)}: **opposite faces**, like
  inversion. ln(nf·E/D) with nf = 4 averages two orbits that pay for a lockstep edge and two that do not. The
  deaths split 4,561 / 385 / 413 / 4,544 (A = 63): the pooled −1.93 is the mixture, not "89% of the mirror". The
  same applies to the A = 84 value (15.834) and to forecast S2's "c2e above csz", which held only for the mixture.
  If the opposite-paired orbits again cost about 0.1 at A = 84, the edge-paired c2e faces there are near 15.2,
  i.e. below csz (15.506) [inferred, not run].
- So the README's puzzle "for a single edge the rotation is the milder one (c2e above csz by 0.25 and 0.33)" is an
  artefact of the pooling: cube-centred, the rotated edge is the *stronger* one (as the group O is against T_h);
  vertex-centred it is slightly milder (next item).
- Vertex-centred (R = 12, A = 63; plan part 5 and seed 9115): c1 **14.293 ± 0.014** (line 14.310 ± 0.026), csz
  **12.173 ± 0.011** (line 12.182), step −2.120 ± 0.018; c2e edge-paired orbits **12.333 ± 0.017**, i.e.
  **−1.960 ± 0.022**, opposite-paired 14.316 ± 0.047 (+0.02 ± 0.05); pooled 12.897 ± 0.016. Here the rotated edge
  is the *milder* one (93% of the mirror's cost), where cube-centred it is the stronger (116%). Which of the two
  costs more depends on the centring; that the rotation costs about as much as the mirror does not.

Edges add: −2.194, −2.133, −2.141 (± 0.013–0.014) for the first, second and third edge, equal within 3%. D2h is the
one rung where the estimator matters: 35% of its exposure belongs to lives that end settled, and with Brent
snapshots the bracket is 7.02–7.29 and drifts with T0 (upper 7.25 → 7.48, lower 7.06 → 6.94 for T0 = 128 → 2048);
with snapshots every 1/16 of the age the bracket is 7.146–7.171, containing the line's 7.122–7.168.

### 1a. Slab faces

`ladder.py`, last line: s8x2 cs (= `rect_8_2_cs`, 48 quotient cells) **10.846 ± 0.010** (line 10.807 ± 0.011),
partner s4x2 c1 (= `rect_4_2_c1`) **9.921 ± 0.010** (line 9.935 ± 0.006; shape2 9.924–9.926); difference
**+0.926 ± 0.014** (line +0.872 ± 0.013). Firewalls: 3 and 11 of about 10,000 lives. The mirror case differs from the
line by +0.039 ± 0.015 (2.6σ; one comparison among about twelve here; not pursued). The sign stands.

### The reading "rim, not mirror"

What the numbers force:

- Pairing two faces across their shared edge costs 2.1–2.2 (mirror containing the edge) or 2.0–2.5 (twofold
  rotation through its midpoint; 2.54 cube-centred, 1.96 vertex-centred) in ln τ_face at A = 63, additively per
  edge for the mirror. A mirror is not needed.
- Pairing faces that share no edge costs at most about 0.1 (ci −0.065 ± 0.017; c2e's opposite orbits −0.10 ± 0.04
  cube-centred, +0.02 ± 0.05 vertex-centred).
- A diagonal mirror through a rim-free slab face does not shorten life at 36–72 quotient cells.

What they do not force:

- In an O_h face the rim *is* on a coordinate mirror. "Rim, not mirror" is a statement about mechanism (lockstep of
  edge-sharing faces would cost the same without the mirror), not one that separates two places.
- The slab comparison is at small quotient sizes and every family's advantage shrinks with size: Q = 2 strips
  +1.14, +0.87, +0.64, +0.41 at 36–72 cells (about −0.02 per cell; a line through them crosses zero near 90 cells),
  C3v triangles +0.72 → +0.38, threefold +0.65 → +0.46. The reference (equal-area torus) carries its own shape
  dependence. The Q = 3 strips at equal P are *higher* than Q = 2 (+1.65 against +1.14 at P = 6), so at fixed area
  more mirror length lengthens life; but in the triangle family the offset falls as the mirror length grows with N
  (+0.72 → +0.38 for 8 → 12 mirror cells on the boundary), which a constant plus −0.09 per mirror cell fits as well
  as anything else. The slab data do not pin a per-mirror-cell coefficient at all.
- On hull faces the only faces with diagonal mirrors and free rims are T_d. Against T's own slope (0.2091 ± 0.0016,
  T having no mirror), T_d − (c/6)·A = 0.79 − (0.147 ± 0.015)·√(A/6) over A = 234–570 (with the R mod 4
  alternation; χ² 44/5), i.e. **−0.06·√A**; with c = T_d's own 0.2035, −0.027·√A. So a growing deficit sits on the
  faces with diagonal mirrors and no lockstep rim, of up to a third of the fitted −0.196·√A
  (`fits.py`, section 5). The README treats it as "the T_d part still bending".

Accepted wording: see correction 1.

## 2. Claim 2: the reduction [proved]

Read line by line. The orbit-graph statement is correct as stated (G-invariance plus a G-preserved slot table gives
equal counts on an orbit; I also never used it: all runs here are on the full system and agree with the line's
quotient runs). Free actions: correct. In-layer symmetries: M must fix (1,1,1), so M is a permutation; t·(1,1,1) = 0;
the reflections are the three transpositions, each fixing the normal-z cells with x = y, one per w = (2,2,−4)
(checked). "Only mirror lines are the three diagonal ones" should say "and their translates" (p3m1 also has glide
lines). Coordinate mirror: never preserves a layer, exchanges two faces, fixes their common rim row (csz fixes 44
face cells = four 12-cell rows sharing apex cells; checked).

`geomcheck.py` (output `geomcheck_out.txt`), for R = 7–37 cube-centred and 8–24 vertex-centred: A = 3(R+1)(R+3)/8 and
3R(R+2)/8; rim = 3(R−1) chain cells + 3 apex cells (cube) and 3R/2 cells, no apex (vertex); the cube-centred face
minus its rim is *literally* the vertex-centred face of radius R−3 (same cell set, no translation needed).

**False lemma.** "A node at graph distance more than r from every cell with a non-trivial stabiliser has the same
radius-r neighbourhood as in the unreduced lattice." c2e at R = 11 c fixes no cell, yet 24 cells are neighbours of
their own image (e.g. (−6,−5,0) ↔ (−5,−6,0), offset (1,−1,0)): their quotient node has a self-loop. ci at R = 12 v:
no fixed cell, 12 such cells near the centre. The correct condition is distance from cells that are within one step
(r steps) of an image under a non-trivial element. Nothing in the measurements depends on the lemma.

## 3. Claim 3: size of the rim term, and the √A coefficient

`fits.py` sections 1 and 3 (from `data/runs.csv` and the O_h points of `oh_data.py` section 2), all reproduced:
rim T_d − O_h = 1.783 … 3.619 (n = 5.5–9); sub-series increments 0.548, 0.464, 0.379 and 0.492, 0.492, 0.453; line
with alternation 0.5035 ± 0.0061 (χ² 27.4/5; ± 0.014 scaled); unweighted 0.472; quadratic: marginal 0.478 ± 0.008 at
n = 7, falling 0.062 ± 0.013 per period; −0.408 × these: −0.205, −0.193, −0.220. The pinned-c O_h coefficients
−0.157, −0.171, −0.193, −0.244 for c = 0.2072, 0.209, 0.2117, 0.2179 reproduce (dB/dc = −8.1).

Why the agreement is not a test:

1. The comparison band is the fit's response to an assumed c. Any rim estimate between −0.16 and −0.24 would have
   "agreed"; the rim fits themselves span −0.19 to −0.22, inside it by construction of the ranges.
2. The comparison is not like for like. O_h = T_d − rim, so the pinned-c O_h coefficient contains whatever T_d does
   beyond c/6. T_d's measured slope is 0.2035, not 0.209: with c pinned at 0.2035 the O_h fit gives −0.127; a
   synthetic O_h = (0.2035/6)·A − 0.47·n fitted with c = 0.209 returns −0.237, with ρ = 0.40 −0.208, against −0.171
   from the data. A consistent reading needs either a smaller rim cost beyond A ≈ 500 or a T_d that steepens — which
   is the open question of claim 4, not a confirmation.

## 4. Claim 4: "the rim term bends"; S3 and S5

- Without the two smallest sizes (R = 23, 25; O_h lives of ln τ 6.2 and 7.1, where the line reports T0 shifts and
  settled-life brackets of 0.02–0.07), the quadratic + alternation fit gives −0.018 ± 0.040 per period (χ² 3.8/2):
  no curvature. With settled lives counted low, −0.044 ± 0.013. The falling sub-series (0.548 → 0.379) starts at
  R = 23; the other sub-series is flat within its errors. The GPU leg (0.2–0.4 per period beyond 9) is conditional on
  T_d not steepening, and the T_d data are compatible with a √A deficit of their own (section 1).
- The two forecasts: 26.4 ± 0.3 (rim linear; reproduced as 26.43 from the R ≤ 33 line, but 26.20 from the all-size
  line with alternation) and 25.65 ± 0.25 (T_d keeps its slope; 25.53–25.82 for slope × 6 = 0.201–0.208). They are
  0.75 apart with a combined forecast error of 0.39 (1.9σ); a GPU result between about 25.9 and 26.2 decides nothing.
  They are also not exhaustive (a T_d that steepens and a rim that bends can give either number).

## 5. Claim 5: slope × stabiliser order

`fits.py` section 2. T (A = 108–198): 0.2091 ± 0.0004 weighted, χ² 30.8/2, ± 0.0016 scaled; local 0.204, 0.215, 0.210;
residuals from (0.209/3)·A −0.001, −0.044, +0.014, +0.025 (the README's "+0.00 ± 0.04" is right). T_d 315–459:
0.2035 ± 0.0008 (± 0.0024 scaled) — matches. T_d 315–570: 0.2034 ± 0.0017. Sub-series lines: R = 23, 27, 31, 35:
0.1978 ± 0.0012; R = 25, …, 37: 0.2024 ± 0.0018 (scaled). The README's "0.201 and 0.208" are the last local
increments, each from two points. "Exactly c/6": for T the data give c/3 with c = 0.209 ± 0.002; T_d is 3–5% below
that at every fit choice. The wedge-versus-torus offsets (+0.72 at 32 cells, +0.38 at 72) are arithmetic on the
table (checked), not rerun.

## 6. Claim 6: the centring

Equal area: A_c(R) = 3(R+1)(R+3)/8 = A_v(R+1) exactly (geomcheck; 30, 45, 63, 84 for R = 7, 9, 11, 13). The A = 30, 45,
63 asymmetric references are this study's own runs (oct_7…12, same protocol), not GPU values; only A = 84's
cube-centred 18.141 is from the GPU (soup 0.35, other start-up cut), for which the line's own cross-checks show
protocol differences ≤ 0.04, an order below 0.646. Independent reruns (plan part 3):

| A | cube-centred c1 | vertex-centred c1 | v − c, this review | line |
|---:|---|---|---|---|
| 30 | 6.815 ± 0.012 (R = 7) | 7.568 ± 0.005 (R = 8) | **+0.754 ± 0.013** | +0.747 ± 0.016 |
| 45 | 9.825 ± 0.005 (R = 9) | 10.550 ± 0.007 (R = 10) | **+0.725 ± 0.009** | +0.738 ± 0.013 |
| 63 | 13.638 ± 0.010 (R = 11) | 14.293 ± 0.014 (R = 12) | **+0.655 ± 0.017** | +0.676 ± 0.032 |

(`ladder.py`, last block.) Each agrees with the line's value. But the difference is **not constant**: a constant
fit to these three has χ² 21.2 on 2 (the line's four values: 6.2 on 3); a + b·√A gives b = −0.037 ± 0.009. The
"object of fixed size" reading of the asymmetric part does not stand at these sizes: it shrinks, from 0.75 at A = 30
to 0.65 at 63–84. (At A = 30 the cube-centred lives last about 110 generations, so only about 1% of lives reach
T0 = 512; the value is still stable to 0.01 between T0 = 128 and 512.) The claim that a *growing* part appears only
with lockstep rims is unaffected in sign, but the free-rim baseline it is read against is itself falling.

The O_h χ² values (constant 60.8/10, d0 + k√A 12.5/9) were not refitted here.

## 7. Claim 7: forecast discipline and estimator

- Commit order (`git log` against the modification times of the line's JSON files, which are written at job end):
  every forecast block precedes the first JSON of the runs it scores. Block 2b (Q7, 01:44:12) was committed while
  oct_31/32/33_c_td ran; they finished at 01:46:04, 01:48:31, 01:52:25 (disclosed in the block). Block 4 (01:48:35)
  was written after the T_h results (01:45) and uses them as input for S2's O forecast; legitimate, as O finished at
  01:51:48+. `rect_3_2_c1` finished 2 s after block 1's commit (an asymmetric partner, started with batch 1).
- Tally: the 38 statements count Q7 (three sizes) as one and R1 (three sizes) as three; counting each size gives 25
  held, 1 on its limit, 14 failed of 40. P4's "levels failed" is stricter than its committed failure line (not
  crossed). Neither changes the picture.
- One job, one seed: runs.csv has jobs = 2 only for oct_37_c_td and rect_4_2_c1; the D2h faces at R ≤ 14 are one job
  each (the seed-1 files were set aside), contrary to the README's "two for … the D2h faces at R ≤ 14".
- Estimator: with events every generation (not every 4) and Brent snapshots, the independent values agree with the
  line's within 0.04 on every rerun system; the start-up cut moves nothing by more than 0.01 except D2h (above).
  Settled lives matter only where they carry exposure (D2h 35%, c2v 1.7% here).

## Corrections to the README (numbered replacement sentences)

1. Verdict 2, first sentences → "The deficit is not a cost of mirror lines as such. Pairing two faces that share an
   edge costs about 2.1–2.2 by a mirror containing the edge and 2.0–2.5 by a twofold rotation through its midpoint
   (depending on the centring) in ln τ_face at A = 63, additively per edge; pairing faces that share no edge costs at
   most about 0.1; and diagonal
   mirror lines through a rim-free slab face lengthen its life at 36–72 quotient cells, by an amount that shrinks
   with size. In an O_h face the lockstep rim lies on a coordinate mirror, so the two cannot be separated there; on
   hull faces with diagonal mirrors and free rims (T_d) a deficit growing like √A (−0.03 to −0.06·√A, depending on
   the bulk constant) remains, so a share of the −0.196·√A on the diagonal mirrors is not excluded."
2. Verdict 2 and section 3, c2e → "The twofold rotation c2e pairs edge-sharing faces in two of its four face
   orbits and opposite faces in the other two. Split by face orbit, the rotated edge costs −2.54 ± 0.02 at A = 63
   cube-centred (the mirror −2.19) and −1.96 ± 0.02 vertex-centred (the mirror −2.12); the opposite pairs cost
   −0.10 ± 0.04 and +0.02 ± 0.05; the pooled −1.93 is the mixture." Delete
   "the rotation gives 89% and 88% of the mirror's effect" and the "Not understood: for a single edge the rotation is
   the milder one"; S2's second line held for the mixture only.
3. Verdict 2, "the rim term bends" and its numbers → "Its marginal cost is 0.45–0.55 per period over 5.5–9 periods.
   A fall within that range rests on the two smallest sizes (without them the curvature is −0.02 ± 0.04 per period);
   with the GPU's O_h points it would have to fall to 0.2–0.4 beyond 9 periods unless T_d steepens. Whether the rim
   term bends is open."
4. Verdict 2, "measured without reference to the O_h fit, against the fitted −0.157 to −0.244" → "The comparison is
   not a test: the fitted band is the fit's dependence on an assumed c, and the fits assume c = 0.207–0.218 while
   T_d's own slope is 0.2035, at which the O_h fit gives −0.127."
5. Verdict 2 and section 2, "+0.4 to +1.9" → "+0.4 to +1.65" (rect_6_4_cs, 69% firewalls, is not used).
6. Verdict 1 and section 3, "0.201 and 0.208 in the two sub-series" → "local increments 0.201 and 0.208 at the
   largest sizes (weighted lines through each sub-series: 0.198 and 0.202)".
7. Section 1, the distance lemma → "A node at graph distance more than r from every cell that is within r steps of
   its own image under a non-trivial element has the lattice's radius-r neighbourhood. (Distance from fixed cells is
   not enough: c2e fixes no cell but has quotient self-loops along its axis.)"
8. Section 1, "the only mirror lines are the three diagonal ones" → "… the three diagonal ones and their translates".
9. Not checked, "Each number is one job with one seed (two for rect_4_2_c1, the D2h faces at R ≤ 14 and T_d at
   R = 37)" → "(two for rect_4_2_c1 and T_d at R = 37)".
10. Verdict 3, "a constant factor of about 2, a property of the hull's shape" → "a factor of about 2 that falls
    slowly with size (0.75, 0.73, 0.66 at A = 30, 45, 63 independently; a constant is excluded, χ² 21 on 2), a
    property of the hull's shape"; and section 5, "Free rims: no growth. The asymmetric difference is an object of
    fixed size" → "Free rims: no growth; the asymmetric difference even shrinks over A = 30–84".
11. Forecast tally → "38 statements as tabulated (Q7 counted once, R1 three times); counting each size, 25 held, one
    fell on its limit and 14 failed."

## Not checked

- Nothing beyond A = 63 was rerun independently for the vessels (no T, T_d, O_h, T_h, O run here; the rim-term
  numbers in sections 3–5 are refits of the line's data). The c2e split at A = 84 is inferred, not run.
- Only one slab pair (48 quotient cells); the threefold, C3v-triangle and Q = 3 slab runs were not rerun.
- The orbit-graph stepper `sy.c` was not run or validated by me (the lead's validate.py rerun is the check). My runs
  are on the full system and agree with its quotient values.
- The O_h centring fits (χ² 60.8/10, d0 + k√A), the earlier GPU/CPU O_h data themselves, and `oh_data.py`'s mirror
  and centre-kind counts.
- Stepper validated for 1,500 generations (vessels) and 300 (slabs) per system, not for the 10⁶ of production lives.
- No look at the faces (occupancy, last cells); the mechanism of the lockstep cost is untouched here too.
