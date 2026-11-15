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
