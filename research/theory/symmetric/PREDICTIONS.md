# Forecasts for the symmetric collapse (PROGRAM M5)

Each block is committed before the runs that test it. Amendments are dated and appended; original text stays.
Protocol for every number below: `run.py` (512 replicas, renewal lives from 0.4 soups drawn once per orbit, events
every 4 generations, doubling-snapshot settled test, T0 = 512 generations, ln τ_face = ln(nf·E/D), ties counted as
face deaths). "Partner" = the asymmetric torus whose cell graph away from the mirrors is the quotient's.

Notation. u1 = (2,−2,0), w = (2,2,−4) (doubled coordinates; |w| = √3·|u1|). A mirror x↔y cuts a {111} layer in a
line along w and fixes one cell per |w| of it ("mirror cell"). `rect_P_Q` is the slab torus with periods P·u1, Q·w
(face area 6PQ); with the mirror imposed (`_cs`) its quotient is a strip of 3PQ cells between two mirror lines of
Q mirror cells each (2Q in all). `hex_N_0` has periods N·u1, N·u2 (face area 3N²).

## Block 1 — committed 2026-11-15, before any symmetric run (only `rect_4_2_c1`, asymmetric, had been run: 9.928 ± 0.010)

What was known when this was written: the stepper is bit-exact against the engine on 26 systems
(`validate.py`); the O_h fit 0.698 + (0.209/6)·A − 0.196·√A; vertex/cube ln-ratios 0.418 ± 0.031, 0.425 ± 0.021,
0.468 ± 0.039, 0.397 ± 0.098 at A = 408–570 and 0.51 ± 0.05 at 759; the phase study's median lifetimes of D2h,
T_d and O_h vessels (NOTEBOOK 2026-11-12, mirror depletion and lockstep).

The model being tested (derivation in README): a symmetric face is, exactly, gump on the orbit graph; if the face
law is local, then

    ln τ = const + c·(cells of the quotient) + Σ_lines σ_line·(length) + Σ_points κ_point

For an O_h face the quotient is a 30-60-90 wedge of A/6 cells whose boundary is one median on diagonal mirrors
(√(A/6) mirror cells) and half an edge of the face, the rim, which lies on a coordinate mirror (√(A/6) rim periods
of length |u1|). So the √A coefficient should be (σ_d + σ_r)/√6, with σ_d the cost of a diagonal mirror per mirror
cell and σ_r the cost of a rim on a coordinate mirror per period; the two centrings share σ_d and differ in σ_r
(cube-centred: the rim row is a chain of cells bisected by the mirror plane; vertex-centred: a row of cells lying
in it) and in the corner.

**P1 (the 1/|G|, mirror).** For the mirror-symmetric soups `rect_P_2_cs`, P = 8, 10, 12, the steps
ln τ(P+2) − ln τ(P) equal the steps of the partners `rect_(P/2)_2_c1` within ± 0.10 each. Equivalently
Δ(P,Q) = ln τ(rect_P_Q_cs) − ln τ(rect_(P/2)_Q_c1) does not depend on P for P ≥ 8. The slope per cell of the
quotient from P = 8 to 12 at Q = 2 is 0.205–0.215 (24 cells: step 4.92–5.16), i.e. half that per cell of the face.
Fails if the slope per quotient cell is outside 0.195–0.225.

**P2 (the cost of a diagonal mirror).** Δ(P,Q) = 2Q·σ_d (+ a constant independent of Q). My forecast, from
splitting the fitted −0.196·√A = (σ_d + σ_r^c)/√6 with the rim estimated from the phase study's medians
(σ_r − σ_free ≈ −0.34): **σ_d = −0.14 ± 0.08 per mirror cell**, so Δ(8,2) = −0.56 ± 0.32, Δ(8,3) = −0.84 ± 0.48.
The notebook's verbal picture (all of the √A term is the mirror lines of the face) forecasts instead
σ_d = −0.196·√6 = −0.48 ± 0.03: Δ(8,2) = −1.92 ± 0.12, Δ(8,3) = −2.88 ± 0.18. The two are separated by 4σ.

**P3 (the 1/|G|, rotation only).** Threefold-symmetric soups on hexagonal tori have a quotient with no boundary and
three cone points. Forecast: ln τ(hex_N_0_c3) and the chiral tori hex_A_B_c3 lie on the asymmetric line through
this protocol's partners at equal quotient area, ref(n) = ln τ(rect_4_2_c1) + c·(n − 48), c = 0.2085, within
± 0.30 (the three cone points together cost less than 0.3 in either direction): 7.42 (n = 36), 8.05 (39), 8.89
(43), 9.93 (48), 10.13 (49), 10.76 (52), 11.80 (57), 12.64 (61), 13.26 (64), each ± 0.30. Slope between n = 49
and n = 64: 3.13 ± 0.10 (0.202–0.215 per quotient cell).

**P4 (the centring is the rim).** If the vertex/cube factor of O_h faces is a rim effect, the data in hand give
ln(τ_v/τ_c) = k·√A with k = 0.0198 ± 0.0008, i.e. σ_r^v − σ_r^c = 0.0485 per rim period. A D2h-symmetric soup
(three coordinate mirrors only) has whole faces of A cells with all three edges on mirrors: six times the rim of
an O_h wedge, no diagonal mirror, no centre. Forecast:

    ln τ_face(oct_R+1_v_d2h) − ln τ_face(oct_R_c_d2h) = 0.119·√A + κ,  |κ| ≤ 0.15
    A = 45 (R = 9, 10): 0.80;  A = 63 (11, 12): 0.94;  A = 84 (13, 14): 1.09;  A = 108 (15, 16): 1.24   (each ± 0.15)

and the difference grows: (A = 108) − (A = 45) = 0.44 ± 0.10. The alternative "an object of fixed size" (the
centre of the face or its corner) gives a difference that does not grow with A (zero if it is the centre, since a
D2h face has none). Fails for me if the difference at A = 84 is below 0.6 or does not grow.

**P5 (it is the mirror, not the shape of the hull).** Asymmetric soups in the same two hulls:
|ln τ_face(oct_10_v_c1) − ln τ_face(oct_9_c_c1)| and the same at R = 11, 12 are below one third of the D2h
differences of P4. (No number for the sign.)

**P6 (the rim on a mirror is cheap; already seen crudely).** ln τ_face(c1) − ln τ_face(d2h) at equal hull:
5.4 ± 0.7 at A = 45 and 6.9 ± 0.7 at A = 63 (mean of the two centrings). This restates the phase study's medians
(133 against 3.8×10³ at R = 10; 567 against 1.1×10⁵ at R = 12) as face lifetimes; it is a consistency forecast,
not an independent one.

## Block 2 — committed 2026-11-15 01:3x UTC, after block 1's short runs, before `oct_15_c_d2h`, `oct_16_v_d2h` and every run of `batch2.sh`

What block 1 had shown when this was written (numbers in README): the diagonal mirror does not shorten a slab
face's life (mirror-symmetric soups outlive their partners of equal quotient area, P2 fails in sign); threefold
centres do not either; asymmetric vertex-centred faces outlive cube-centred ones of equal area by 0.74 (A = 45)
and 0.68 (A = 63), so P5 fails; D2h faces are 6 to 8 nats below asymmetric faces of the same hull (A = 63, 84),
with a cost per cell of only 0.134–0.140 between those two sizes. So the deficit of symmetric vessels sits where
a face meets a coordinate mirror, and the forecasts below test that reading. D2h values of block 1 carry an
uncertainty from settled lives (one third of the exposure); the stepper now records settled lives at the matching
snapshot on a finer ladder, and the D2h runs are repeated with it.

**Q1 (the rim deficit turns from area-like to line-like).** ln τ_face(D2h, A = 108) − ln τ_face(D2h, A = 84) =
3.9 ± 0.35 in each centring (0.163 ± 0.015 per cell, against 0.134–0.140 from 63 to 84).

**Q2 (rims add).** With one coordinate mirror (`csz`: every face has one edge on it) and two (`c2v`: two edges),
at R = 11 c and R = 12 v (A = 63): ln τ_face(csz) = c1 − Δ/3 and ln τ_face(c2v) = c1 − 2Δ/3, Δ = c1 − d2h of the
same hull, each within ± 0.4. With the block-1 values: csz 11.5, c2v 9.4 (cube-centred).

**Q3 (a mirror plane, not lockstep as such).** Two other groups of order two at R = 11 c: inversion (`ci`,
opposite faces in lockstep, no fixed plane) and the twofold rotation about an edge-midpoint axis (`c2e`, the two
faces that share that edge in lockstep, their rim not fixed). Forecast: ci = c1 within ± 0.3 (13.63 ± 0.3);
c2e = 13.3 ± 0.4; csz = 11.5 ± 0.4. "Lockstep of adjacent faces" would instead put c2e at csz; "lockstep of the
volume" would put all three at csz.

**Q4 (T_d against O_h: the rim term of a wedge).** T_d has the same face stabiliser C3v as O_h but no coordinate
mirror: its faces have free rims. With ρ = 0.34 ± 0.05 per rim period (from D2h − c1 at A = 63, 84 over
6·√(A/6) periods), cube-centred:

    ln τ_face(td) − ln τ_face(oh) = ρ·√(A/6) = 2.12 (A = 234), 2.29 (273), 2.46 (315), 2.80 (408), 2.97 (459), each ± 0.35

and it grows: (A = 459) − (A = 234) = 0.85 ± 0.25.

**Q5 (the C3v wedge is below c/6 even with free rims).** Slope of ln τ_face(td) from A = 234 to 408:
0.031 ± 0.002 per face cell (0.186 ± 0.012 per quotient cell, the value the mirror strips of block 1 gave), not
0.0348. If it is 0.0348 ± 0.001 the whole deficit of O_h is its rim.

**Q6 (the centring, by group).** v − c at equal area. From the asymmetric values, split additively into rim
periods and corners (two points, so weakly determined: −0.021 per period, +0.36 per corner), a quotient with free
rims gets: T_d (√(A/6) periods, half a corner) 0.05 ± 0.15 at A = 234–315; T (2√(A/6) periods, one corner)
0.15 ± 0.15 at A = 135–198. O_h at A = 234–315: 0.40 ± 0.08 (continuing the known values). If T_d shows the
O_h value, the centring effect belongs to the C3v wedge and not to the rim on a mirror.

## Block 2b — committed 2026-11-15 01:44 UTC, while `oct_31_c_td`, `oct_32_v_td`, `oct_33_c_td` were running (no output of theirs seen)

(The header of block 2 says "01:3x UTC"; its commit, 814c3d4, is stamped 01:26 UTC.)

Seen so far in block 2: one edge on a coordinate mirror lowers ln τ_face by 2.18 at A = 63, two by 4.34, three by
6.47 (cube-centred): rims add. Per rim and per period of rim ((R−1)/2 periods an edge, cube-centred) the three-rim
deficits at A = 63, 84, 108 are 2.16, 2.71, 3.20: the marginal cost is 0.5 per period. T_d minus O_h, a wedge with
half an edge, is 1.78, 2.18, 2.33 (cube-centred, A = 234, 273, 315) and 1.85, 2.06, 2.36 (vertex-centred).

**Q7.** The rim term of the wedge keeps the marginal cost that whole D2h faces show, 0.5 per period:
T_d − O_h = 2.33 + 0.5·((R−1)/4 − 6.5) cube-centred, 2.36 + 0.5·(R/4 − 7) vertex-centred. With this study's O_h
values 10.984 (R = 31), 11.406 (R = 32) and the earlier 12.473 (R = 33):

    ln τ_face(oct_31_c_td) = 13.81 ± 0.15      ln τ_face(oct_32_v_td) = 14.27 ± 0.15      ln τ_face(oct_33_c_td) = 15.55 ± 0.20

## Block 3 — committed 2026-11-15 01:46 UTC, before every run of `batch3.sh`

**R1 (a wedge with no rim).** `hex_N_0_c3v`: threefold axis and mirrors imposed on a slab torus; the quotient is an
equilateral triangle of N²/2 cells bounded by three diagonal mirror lines (N mirror cells), with no hull rim.
Block 1 found that mirrors and threefold centres raise a slab face's life above the asymmetric torus of equal
quotient area (by 0.4 to 1.9 and by 0.5 to 0.7). Forecast: ln τ_face = ref(N²/2) + 1.2 ± 0.7 with
ref(n) = 9.935 + 0.2086·(n − 48): **7.8 (N = 8), 11.55 (N = 10), 16.1 (N = 12), each ± 0.7**, and the triangle
outlives the T_d wedge of equal quotient area (8.02 + 0.196·(n − 39), from this study's cube-centred T_d values):
at N = 10 by 1.4 ± 0.7. Slope from N = 8 to 12: 0.19–0.22 per quotient cell.

**R2 (rims add, second size).** A = 84, cube-centred, with c1 = 18.141 (GPU) and d2h = 10.022 (block 2):
ln τ_face(oct_13_c_csz) = 15.43 ± 0.12, ln τ_face(oct_13_c_c2v) = 12.73 ± 0.12.

**R3 (the marginal rim cost stays 0.5 per period).** ln τ_face(oct_17_c_d2h) (A = 135) = 29.34 − 3·3.70 =
18.24 ± 0.4 (the asymmetric value 29.34 ± 0.25 is the GPU's).

**R4 (without symmetry the centring is an object of fixed size).** Asymmetric soups, v − c at equal area:
0.72 ± 0.12 at A = 30 (R = 8, 7) and 0.66 ± 0.10 at A = 84 (R = 14 against the GPU's 18.141 at R = 13), i.e.
ln τ_face(oct_14_v_c1) = 18.80 ± 0.10. A line term of the size seen in D2h and O_h faces (0.119·√A for a whole
face) would give 1.09 at A = 84.

## Block 4 — committed 2026-11-15 01:49 UTC, before `batch4.sh` (and before the results of `oct_32_v_td`, `oct_33_c_td` and block 3 were seen, except `hex_8_0_c3v` = 7.314 and `hex_9_0_c3v` = 8.956)

(Block 3's header says 01:46 UTC; its commit, 6061d61, is stamped 01:44 UTC.)

Seen since block 3 was written: T faces (threefold axis, free rims) lie on (0.209/3)·A within 0.04 at A = 108–198;
T − T_h = 3.05, 3.53 at 9 and 10 rim periods; T_d − O_h rises by 0.49–0.54 per rim period of the wedge
(`report.py`, section G); `oct_31_c_td` = 13.778 (Q7 said 13.81 ± 0.15); `oct_11_c_c2e` = 11.704, close to
`csz` (11.456) and far from c1 (13.634): Q3 failed, the deficit belongs to two faces that share an edge dying
together, with or without a mirror through the edge.

**S1 (the rim term, one size further).** ln τ_face(oct_35_c_td) = 14.151 (the earlier O_h value at A = 513) +
rim term 3.37 = **17.52 ± 0.15** (rim term: 2.794 at R = 31 plus 0.5 per period for one more period, or the fit
−1.11 + 0.536·8.5 = 3.45; the mean of the two).

**S2 (rotation against mirror, in a threefold sector).** The group O (24 rotations) has threefold faces whose
neighbours across every edge are their images under a twofold rotation; T_h has the same faces with mirrors
through the edges. At A = 63 the rotation costs 1.93 for one edge and the mirror 2.18. Forecast:
ln τ_face(oct_19_c_o) = 8.81 ± 0.2 and ln τ_face(oct_21_c_o) = 10.66 ± 0.2 (T_h + 0.35), both far below T (11.51,
13.82). And ln τ_face(oct_13_c_c2e) = ln τ_face(oct_13_c_csz) + 0.30 ± 0.15.

**S3 (for a GPU; not testable here).** O_h, vertex minus cube at A = 828 (R = 46 v against 45 c): 0.55 ± 0.04,
from d0 + k√A with d0 = 0.104 ± 0.039, k = 0.0155 ± 0.0022 (`report.py`, section H); a constant factor 1.5 gives
0.41, a pure line term 0.61. With the GPU's 24.175 ± 0.072 at R = 45: ln τ(46 v) = 24.72 ± 0.09.
T_d at A = 759 (R = 43 c): the GPU's O_h value 21.889 plus the rim term −1.11 + 0.536·10.5 = 4.52: 26.4 ± 0.3.

## Block 5 — committed 2026-11-15 02:18 UTC, before every run of `batch5.sh`

(Block 4's header says 01:49 UTC; its commit, 98a66d8, is stamped 01:48 UTC.)

Seen since block 4 was written, all of blocks 3 and 4. S1 failed: `oct_35_c_td` = 17.291 ± 0.040 against
17.52 ± 0.15, so T_d − O_h at 8.5 rim periods is 3.140 ± 0.052 (with the earlier O_h value 14.151 ± 0.033) where
the line fitted at R ≤ 33 gives 3.46. T_d alternates with R mod 4 (R ≡ 1 high, R ≡ 3 low, by about ± 0.03–0.05).
Within the sub-series R = 23, 27, 31, 35 the T_d slopes × 6 are 0.196, 0.201, 0.201 and the rim term's increments
per period 0.55, 0.46, 0.35; within R = 25, 29, 33 the slopes are 0.200, 0.208 and the increments 0.49, 0.49.
The GPU's O_h points at A = 759, 828 need either a T_d slope × 6 that rises to 0.2155 with the rim's marginal
cost staying 0.5, or a T_d slope that stays 0.20–0.21 with the marginal cost falling to 0.3–0.4
(`report.py`, section J). This block tests the next size of the second sub-series, R = 37 (A = 570, 9 rim
periods), and reruns O_h at A = 513 and 570 in this study's protocol so that the rim term does not rest on values
measured with another soup density and T0.

**S4a (O_h in this protocol).** ln τ_face(oct_35_c_oh) = 14.13 ± 0.05 and ln τ_face(oct_37_c_oh) = 15.86 ± 0.10
(the earlier values 14.151 ± 0.033 and 15.881 ± 0.077, lowered by the 0.02 by which this protocol sat below them
at R = 30–33).

**S4b (T_d at A = 570).** ln τ_face(oct_37_c_td) = **19.42 ± 0.12**. The two readings bracket it: "the rim's
marginal cost stays 0.49 in this sub-series" gives 15.86 + 3.165 + 0.49 = 19.52 (and needs the T_d slope × 6
from R = 33 to rise to 0.210); "T_d keeps the slope 0.201" gives 15.635 + (0.201/6)·111 = 19.35 (and makes the
rim's last increment 0.33). My forecast is between them because I expect both to move: the T_d slope still
climbing slowly towards c/6 as the rim-free triangle's did, the rim's marginal cost settling a little below 0.5.

**S4c (the rim term at 9 periods, the number this block is for).** T_d − O_h at R = 37, both from these runs:
**3.56 ± 0.12**. Decision rule fixed now: at or above 3.62 the marginal cost has stayed at or above 0.46 per period
and S1's shortfall is the alternation plus noise; at or below 3.50 (0.34 per period or less) the rim term is
flattening and is not a √A term with the coefficient −0.21; between, undecided. The expected error of the
measurement is ± 0.07 (about 200 T_d deaths, 2,000 O_h deaths).

**S4d (S1 revisited with this study's O_h).** T_d − O_h at R = 35 = 17.291 − ln τ_face(oct_35_c_oh): 3.16 ± 0.07.

## Scores — appended 2026-11-15 after the last run; everything above is as committed

Header times against commit stamps: block 1 is commit 4f455e7; block 2 (header "01:3x UTC") is 814c3d4, stamped
01:26 UTC; block 2b is 96e2292; block 3 (header 01:46) is 6061d61, stamped 01:44; block 4 (header 01:49) is
98a66d8, stamped 01:48; block 5 (header 02:18) is 4020d9e, stamped 02:16. In every case the commit precedes the
first run of the block, except block 2b, which was committed while its three runs were in progress and before any
output of theirs had been read (`git log --format='%h %cI %s' -- research/theory/symmetric`; run times are the `.json`
files' in `research/scratch/symmetric/`). The protocol line at the top says "doubling-snapshot settled test": from
block 2 on the test is the ladder of snapshots described in README.md.

All values are ln τ_face ± one standard error; they are printed by `python3 research/theory/symmetric/report.py`.

| forecast | said | found | score |
|---|---|---|---|
| P1 slope of mirror strips per quotient cell, P = 8 → 12, Q = 2; their steps equal the partners' within 0.10 | 0.205–0.215; fail outside 0.195–0.225 | 0.1863 ± 0.0016; steps lower than the partners' by 0.23, 0.23 | failed |
| P2 Δ(8,2), mirror strip minus partner | −0.56 ± 0.32 (the notebook's picture: −1.92) | +0.872 ± 0.013 | failed, wrong sign |
| P3 threefold slab quotients on the asymmetric line ± 0.30 | nine values | +0.46 to +0.65 above it | failed |
| P3 step n = 49 → 64 | 3.13 ± 0.10 | 3.044 ± 0.017 | held |
| P4 D2h v − c = 0.119·√A ± 0.15 | 0.80, 0.94, 1.09, 1.24 (A = 45, 63, 84, 108); growth from A = 45 to 108: 0.44 ± 0.10 | 0.429, 0.505, 0.645, 0.830; growth 0.40 | levels failed (low by 0.4); growth held; the stated failure line (below 0.6 at A = 84) was not crossed |
| P5 asymmetric v − c below a third of D2h's | below 0.14 (A = 45), 0.17 (63) | 0.738 ± 0.013, 0.676 ± 0.032 | failed |
| P6 c1 − D2h, mean of the centrings | 5.4 ± 0.7 (A = 45), 6.9 ± 0.7 (63) | 4.74, 6.55 | held (A = 45 by 0.04, on D2h lives too short to be reliable) |
| Q1 D2h from A = 84 to 108 | 3.9 ± 0.35 | 3.752 ± 0.023 (c), 3.937 ± 0.034 (v) | held |
| Q2 edges add, A = 63 | csz 11.48, c2v 9.32 (± 0.4) | 11.456, 9.291 | held |
| Q3 inversion; one coordinate mirror | 13.63 ± 0.3; 11.5 ± 0.4 | 13.578 ± 0.014; 11.456 ± 0.011 | held; held |
| Q3 twofold rotation swapping two adjacent faces | 13.3 ± 0.4 | 11.704 ± 0.005 | failed |
| Q4 T_d − O_h = 0.34·√(A/6) ± 0.35 | 2.12, 2.29, 2.46, 2.80, 2.97 | 1.783, 2.181, 2.330, 2.794, 3.165 | held |
| Q4 its growth from A = 234 to 459 | 0.85 ± 0.25 | 1.38 ± 0.03 | failed |
| Q5 T_d slope per face cell, A = 234 → 408 | 0.031 ± 0.002; 0.0348 ± 0.001 would mean no deficit | 0.0331 ± 0.0001 | at the upper limit (0.0330), between the two readings |
| Q6 v − c | T_d 0.05 ± 0.15; T 0.15 ± 0.15; O_h 0.40 ± 0.08 | T_d 0.398, 0.240, 0.382; T 0.250, 0.224; O_h 0.333, 0.367, 0.351 | T_d failed; T, O_h held |
| Q7 T_d from O_h plus 0.5 per rim period | 13.81 ± 0.15, 14.27 ± 0.15, 15.55 ± 0.20 | 13.778 ± 0.015, 14.183 ± 0.019, 15.635 ± 0.032 | held |
| R1 rim-free C3v triangle, N = 8, 10, 12 | 7.8, 11.55, 16.1 (± 0.7) | 7.314, 10.822, 15.319 | held; failed by 0.03; failed by 0.08 |
| R1 triangle above the T_d wedge of equal quotient area, N = 10 | 1.4 ± 0.7 | 0.65 | failed by 0.05 |
| R1 slope N = 8 → 12 | 0.19–0.22 | 0.2001 | held |
| R2 edges add, A = 84 | csz 15.43 ± 0.12, c2v 12.73 ± 0.12 | 15.506 ± 0.026, 12.857 ± 0.019 | held; failed by 0.007 |
| R3 D2h at A = 135 | 18.24 ± 0.4 | 18.449 ± 0.071 | held |
| R4 asymmetric v − c | 0.72 ± 0.12 (A = 30); 0.66 ± 0.10 (A = 84) | 0.747 ± 0.016; 0.646 ± 0.060 | held; held |
| S1 T_d at A = 513 (O_h plus a linear rim term) | 17.52 ± 0.15 | 17.291 ± 0.040 | failed, low by 0.23 |
| S2 group O above T_h by 0.35 | 8.81 ± 0.2, 10.66 ± 0.2 | 7.086 ± 0.003, 8.694 ± 0.006 | failed: O is 1.4–1.6 below T_h |
| S2 c2e above csz at A = 84 | +0.30 ± 0.15 | +0.328 ± 0.040 | held |
| S4a O_h in this protocol, A = 513, 570 | 14.13 ± 0.05; 15.86 ± 0.10 | 14.118 ± 0.012; 15.870 ± 0.023 | held; held |
| S4b T_d at A = 570 | 19.42 ± 0.12 | 19.489 ± 0.074 (183 deaths, two seeds) | held |
| S4c rim term at 9 periods | 3.56 ± 0.12 | 3.619 ± 0.077 | held; the decision rule (linear at 3.62 or above, flattening at 3.50 or below) returns "undecided", 0.001 short of "linear" |
| S4d rim term at 8.5 periods with this study's O_h | 3.16 ± 0.07 | 3.173 ± 0.041 | held |
| S3 (GPU) | O_h v − c at A = 828: 0.55 ± 0.04; T_d at A = 759: 26.4 ± 0.3 | not run | open |

Of 38 scored statements 23 held, one fell on its limit (Q5) and 14 failed, five of them by less than 0.1 beyond the
stated tolerance (R1 three times, R2, S1).

## Amendment S5 — 2026-11-15, after block 5; for a GPU, not testable here. S3 stays as written.

S3's number for T_d at A = 759 (26.4 ± 0.3) assumed a rim term linear in the rim, −1.11 + 0.536 per period. Since
then: the rim term's increments per period are 0.548, 0.464, 0.379 ± 0.045 (R = 23, 27, 31, 35) and 0.492, 0.492,
0.453 ± 0.084 (R = 25, 29, 33, 37), and T_d faces keep a slope × 6 of 0.201 ± 0.002 and 0.208 ± 0.004 in those two
sub-series out to A = 513 and 570. If T_d keeps that slope from 17.291 at A = 513 (R = 43 is in the same
sub-series as R = 35):

**S5.** ln τ_face(oct_43_c_td) = **25.65 ± 0.25**, i.e. a rim term of 3.76 ± 0.25 at 10.5 periods with the GPU's
O_h value 21.889, a marginal cost of 0.3 ± 0.12 per period beyond R = 35. At or above 26.1 the rim term has stayed
linear (S3's reading) and T_d has steepened to 0.215 or more; at or below 25.9 the rim term is flattening.
