# The symmetric collapse (PROGRAM M5): what the 1/6, the −0.196·√A and the centring factor are

2026-11-15. The measured law of an O_h-symmetric face, ln τ ≈ 0.698 + (0.209/6)·A − 0.196·√A (cube-centred), with
vertex-centred faces "1.5 times" longer-lived, has three fitted ingredients. This study takes them apart with
symmetric soups of *lower* symmetry, on slab tori and in octahedral vessels, all on one to three CPU cores.
Statements are tagged **[proved]**, **[measured]** (number, error, command) or **[conjectured]**. Forecasts were
committed before the runs that test them (`PREDICTIONS.md`; commits 4f455e7, 814c3d4, 96e2292, 6061d61, 98a66d8,
4020d9e) and are scored below; more than a third failed, and the failures are what changed the picture.

All numbers are ln τ_face (per independent face, generations), ± one standard error from the death count.
Every table is printed by `python3 research/theory/symmetric/report.py` from `data/runs.csv`.

## Verdict

1. **The 1/6.** [proved] A symmetric state is, exactly, gump on the orbit graph: one node per orbit, each node's
   12 neighbour slots the orbits of its representative's neighbours. For a group acting freely (translations) the
   orbit graph is a smaller torus and "1/|G|" is exact with no correction. For the stabiliser C3v of a face the
   orbit graph is a 30-60-90 wedge of A/6 cells that is gump's own graph except within one step of its two mirror
   edges and its corners. [conjectured] The slope is asymptotically c/6 because the face law is local; that is
   as unproved as the area law itself. [measured] It holds at reachable sizes wherever the wedge's rim borders
   *living* faces: faces with a threefold axis only (group T, free rims) lie on **(0.209/3)·A + 0.00 ± 0.04** at
   A = 108–198 (slopes × 3: 0.204, 0.215, 0.210); faces with the full C3v and free rims (group T_d) have slope × 6
   = **0.2035 ± 0.002** at A = 315–459 (0.201 and 0.208 in the two sub-series of sizes, out to A = 570) and sit at
   (0.209/6)·A − 0.3…−0.6 there; a C3v triangle with no hull rim at all (slab torus) reaches 0.207 at 60–72
   quotient cells. Below about 50 quotient cells every mirror-bounded quotient has a lower slope (0.17–0.20),
   rising with size. The wedge is not a torus of A/6 cells: a mirror-bounded quotient of n cells outlives the
   n-cell torus by an offset that shrinks with size (triangle: +0.72 at 32 cells, +0.38 at 72), which is the form
   the shape dependence of periodic faces takes here.
2. **The √A term is not a mirror-line term. It is the rim, and the rim term bends.** [measured] Imposing a
   mirror, a threefold axis, or both on a slab face *lengthens* its life relative to the asymmetric torus of
   equal quotient area (by 0.4–1.9, 0.5–0.7 and 0.4–0.7). The deficit of O_h faces sits on the **rim**: an edge
   of a hull face whose two faces die together. Per edge it is additive (one, two, three edges: −2.18, −4.34,
   −6.47 at A = 63), it does not need a mirror (a twofold rotation that swaps the two faces costs −1.93 where the
   mirror costs −2.18; inversion, which pairs faces that share no edge, costs −0.06 ± 0.02), and its marginal
   cost is **0.4 to 0.55 per period of rim** in three independent families (whole D2h faces 0.55, 0.50,
   0.43 ± 0.09; T minus T_h 0.49; T_d minus O_h, the wedge's own rim term, 0.47–0.54 on average over 5.5 to 9
   periods, depending on the fit). An O_h wedge has (R−1)/4 = 0.408·√A − 0.75 rim periods, so a marginal cost ρ
   is a √A coefficient −0.408·ρ: **−0.19 to −0.22**, measured without reference to the O_h fit, against the
   fitted −0.157 to −0.244 (the fit's value depends on the c assumed, 0.2072 to 0.2179; −0.196 was for c = 0.209
   and A ≤ 693). **But the term is not linear in the rim at these sizes.** Its marginal cost falls: 0.55, 0.46,
   0.38 ± 0.05 per period in one sub-series of sizes (R = 23, 27, 31, 35) and 0.49, 0.49, 0.45 ± 0.08 in the other
   (R = 25, 29, 33, 37); a quadratic term is −0.031 ± 0.007 per period². T_d faces keep a slope × 6 of 0.201–0.208
   out to A = 570, and with that slope the GPU's O_h points at A = 759 and 828 leave the rim a marginal cost of
   only 0.2–0.4 between 9 and 11 periods. So "−0.196·√A" describes a rim deficit that is still growing at A ≈ 500
   but more slowly than its length. Whether it tends to a line term with a smaller coefficient or saturates is
   **not settled**; one T_d ensemble at A = 759 on a GPU would settle it (26.4 if the rim term stays linear, about
   25.7 if T_d keeps its slope).
3. **The centring is both an object and a line.** [measured] Without any symmetry a vertex-centred hull face
   already outlives a cube-centred one of equal area by 0.75, 0.74, 0.68, 0.65 ± 0.06 at A = 30, 45, 63, 84: a
   constant factor of about 2, a property of the hull's shape (the cube-centred face has three apex cells and a
   rim row of twice as many cells). A threefold face (T) shows a third of it, 0.25, 0.25, 0.22. With rims that die
   together the difference grows with the rim: D2h 0.51, 0.65, 0.83 at A = 63, 84, 108; O_h 0.33 ± 0.05 at A = 234
   to 0.52 ± 0.04 at 759, where a constant is now excluded (χ² 60.8 on 10) and d0 + k·√A fits with
   d0 = 0.10 ± 0.04, k = 0.0155 ± 0.0022 (χ² 12.5 on 9). So "1.5" is e^(0.10 + 0.0155·√A): a fixed part (one
   sixth of the asymmetric face's 0.7 would be 0.12) and a line part carried by the rim row, which differs
   between the centrings. The centre of the face is not the object: its three kinds change lifetimes by under 0.02
   per centre on slabs and leave no period-3 pattern in the O_h residuals.

What is derived, measured and conjectured for each question is itemised under "Status of the three questions".

## Tools and validation

- `geom.py` builds a full system (a slab torus of 8 {111} layers with any in-plane period lattice, or an
  octahedral vessel, cube- or vertex-centred), a group from affine generators, and the orbit graph. Every generator
  is checked to be an automorphism of the neighbour table before use (so a torus that does not admit the symmetry
  is refused), and every cell's neighbour-orbit multiset is checked against its representative's.
- `sy.c` steps 512 bit-sliced replicas on any orbit graph (the carry-save kernel of `research/fluct/fl.c`), with
  renewal lives from fresh 0.4 soups (one draw per orbit) and events every 4 generations.
- **[measured] Bit-exact against the Rust engine** on 41 systems (every family and group used here, both
  centrings, and the largest vessel run for each of c1, D2h, T_d, O_h): the population at each of 1,500
  generations and the final cell set, from a random orbit state expanded to the full symmetric cell set and run
  by `gump run` (slab tori replicated on a cubic torus).
  `python3 research/theory/symmetric/validate.py` → `ALL OK` (about 5 minutes).
- **Protocol** (`run.py`, fixed before the runs): a life ends at a face death F (a face layer empty: dead for
  ever by T2), a transverse firewall W (slabs only), both at one check X, settled S, or open at the end of the job.
  Exposure and deaths are counted from age T0 = 512; ln τ_face = ln(nf·E/D) with nf the number of face orbits; X
  counts as a face death. `report` columns give T0 = 128 and 2048 as well: they agree within errors except where
  noted.
- **Settled lives** (the trap of lives that settle into long cycles): the state is compared at every check with a
  snapshot of the same life taken on a ladder of ages (each rung one eighth beyond the last), which catches any
  period; equality proves periodicity. A settled life is recorded at the age of the snapshot it matched (an upper
  bound on when it settled) and the table's `S-low` column counts it only to the rung before (a practical lower
  bound). The two differ by less than 0.01 everywhere except D2h (0.02–0.07 at R ≤ 14), O (0.02–0.04) and O_h or
  T_d at R ≤ 24 (0.02–0.07), where up to 45% of the exposure belongs to lives that end settled. No age cap.
  The first 20 runs of block 1 used an earlier version (doubling snapshots, settled lives recorded at detection);
  `run.py` reads both; the D2h runs made with it are not used.
- **Agreement with earlier work [measured]**: asymmetric tori of 72 cells 14.611 ± 0.019, 14.864 ± 0.022,
  14.967 ± 0.023 (CLAIMS SH1: 14.613, 14.877, 14.973); `rect_4_2_c1` 9.935 ± 0.006 (shape2's (2,2,8): 9.924–9.926);
  asymmetric hull faces 6.816, 9.816, 13.634 at A = 30, 45, 63 (fluct: 6.805, 9.820, 13.632); O_h faces at R = 31,
  32, 33, 34 within 0.03 of `research/fluct` (differences −0.009 ± 0.032, −0.004 ± 0.016, −0.003 ± 0.018,
  +0.029 ± 0.021), −0.037 ± 0.011 at R = 30, and −0.034 ± 0.035, −0.011 ± 0.081 at R = 35, 37 (report section I).

## 1. The reduction, and what a face can have for symmetry [proved]

- **Orbit graph.** Let G be a group of permutations of the cells of a finite system that preserves the 12-slot
  neighbour table. If a state is G-invariant, every cell of an orbit has the same live-neighbour count, namely
  the sum of the orbit states over its 12 slots; so the next state is G-invariant and is given by B45/S345 on the
  graph whose nodes are orbits. ∎ (Checked bit-exactly, above.) A node at graph distance more than r from every
  cell with a non-trivial stabiliser has the same radius-r neighbourhood as in the unreduced lattice.
- **Free actions.** If G is a group of translations of a slab torus with period lattice Λ, the orbit graph is the
  slab torus with period lattice Λ + G: its lifetime law is that torus's, exactly. The "1/|G|" then has no
  correction, and all the shape dependence of periodic faces (CLAIMS SH1–SH9) applies to the quotient.
- **Symmetries of a {111} slab.** The lattice's symmetry group is {p → Mp + t : M ∈ O_h, t ∈ (2Z)³}. The elements
  that keep every layer x+y+z = s in place have M one of the six coordinate permutations and t·(1,1,1) = 0: the
  plane group p3m1 on the in-plane lattice Λ0 = ⟨u1, u2⟩, u1 = (2,−2,0), u2 = (0,2,−2). So inside a face the only
  mirror lines are the three *diagonal* ones (x ↔ y and its conjugates, along w = (2,2,−4) and its images); each
  fixes one cell per |w| (the cells with normal z and x = y); every threefold centre lies on mirror lines. A
  *coordinate* mirror never preserves a {111} layer: in a hull it exchanges two faces and fixes the row of cells
  they share.
- **Which tori admit which symmetry** (verified by `geom.py`'s automorphism check on every torus used). Threefold
  rotation: Λ = ⟨v, Rv⟩ for any v ∈ Λ0 (index a² + ab + b²; `hex_A_B`). The mirror: Λ rectangular ⟨P·u1, Q·w⟩
  (`rect_P_Q`, face area 6PQ, two mirror lines of Q cells each; the quotient is a strip of 3PQ cells between
  them) or centred ⟨P·u1, (P·u1 + Q·w)/2⟩ (`cent_P_Q`, one mirror line; the quotient is a Möbius band). Both:
  `hex_N_0` (the quotient is an equilateral triangle of N²/2 cells with three mirror sides of N/3 cells each) and
  `hex_N_N`. On `hex_N_0` the three rotation centres are of the three different kinds (hexagon centre, the two
  triangle centres, as seen from the top face) unless 3 | N, when they are of one kind chosen by the axis.
- **Hull faces** (`python3 research/theory/symmetric/oh_data.py`, section 1). Cube-centred, radius R odd:
  A = 3(R+1)(R+3)/8; the rim is a chain of 3(R−1) cells bisected by the coordinate planes, two per period |u1|,
  plus 3 apex cells on the fourfold axes. Vertex-centred, R even: A = 3R(R+2)/8; the rim is a row of 3R/2 cells
  lying *in* the coordinate planes, one per period; no apex cell. Removing the rim of a cube-centred face of
  radius R leaves the vertex-centred face of radius R−3 and conversely. The rim rows are shared: two adjacent
  face layers of the hull intersect exactly in their common rim row, and four meet in an apex cell. The diagonal
  mirror planes are the same planes in both centrings. The kind of the face's centre cycles with R mod 6 in both
  centrings, and at equal area the two centrings never have the same kind.
- **Geometric factors of the wedge.** Rim periods in a wedge: (R−1)/4 cube-centred, R/4 vertex-centred, i.e.
  0.408·√A − 0.75 and 0.408·√A − 0.25. Mirror cells on one median: 0.83–0.94 × √(A/6) cube-centred, 0.97–1.03
  vertex-centred for the faces measured (exact counts in `oh_data.py`); the count steps every second R, so the
  point where a mirror line meets the rim comes in two kinds alternating with R mod 4.

## 2. Slab faces with an imposed symmetry: no deficit from mirror lines or centres [measured]

`bash research/theory/symmetric/batch1.sh`, `batch3.sh 1`; report sections A–C.

| quotient | cells | ln τ_face | asymmetric torus of equal quotient area | difference |
|---|---:|---|---|---|
| mirror strip `rect_6_2_cs` | 36 | 8.561 ± 0.004 | 7.420 ± 0.006 | +1.142 ± 0.007 |
| `rect_8_2_cs` | 48 | 10.807 ± 0.011 | 9.935 ± 0.006 | +0.872 ± 0.013 |
| `rect_10_2_cs` | 60 | 13.066 ± 0.022 | 12.426 ± 0.016 | +0.640 ± 0.027 |
| `rect_12_2_cs` | 72 | 15.277 ± 0.037 | 14.864 ± 0.022 | +0.413 ± 0.043 |
| `rect_6_3_cs` | 54 | 12.713 ± 0.018 | 11.062 ± 0.013 | +1.650 ± 0.022 |
| `rect_8_3_cs` | 72 | 16.489 ± 0.069 | 14.967 ± 0.023 | +1.521 ± 0.072 |
| `rect_6_4_cs` (69% firewalls) | 72 | 16.532 ± 0.070 | 14.611 ± 0.019 | +1.921 ± 0.073 |
| threefold, `hex_A_B_c3`, nine tori | 36–64 | 10.480 + 0.2011·(n − 48), scatter 0.03 | 9.935 + 0.2086·(n − 48) | +0.65 (n = 36) to +0.46 (n = 64) |
| C3v triangle `hex_8_0_c3v` … `hex_12_0_c3v` | 32, 40.5, 50, 60.5, 72 | 7.314, 8.956, 10.822, 12.935, 15.319 (± 0.004–0.027) | 6.60, 8.37, 10.35, 12.54, 14.94 | +0.72, +0.59, +0.47, +0.39, +0.38 |

- The mirror-symmetric, threefold and C3v soups all outlive their asymmetric partners. Whatever a mirror line or a
  rotation centre does to a face with no rim, it is not a loss.
- Slopes per quotient cell: mirror strips 0.187, 0.188, 0.184 (Q = 2, P = 6 → 12; the partners give 0.210, 0.208,
  0.203) and 0.222, 0.210 (Q = 3); threefold 0.2011 ± 0.0003 over nine tori (0.2029 ± 0.0012 from n = 49 to 64);
  C3v triangle 0.193, 0.196, 0.201, 0.207 for successive N. So the cost per cell of a quotient is c within
  about 10% at 36–72 cells, depends on the family as periodic faces' cost does on their shape, and for the
  triangle climbs to the asymmetric value by 70 cells. The Q = 2 strips stay at 0.186 up to a width of six
  lattice constants with no sign of converging; I have no account of that (their partners' slope also falls
  with length, 0.210 → 0.203).
- The three kinds of threefold centre: `hex_6_0_c3` with three centres of one kind gives 8.079, 8.105, 8.057
  (± 0.005) for the three kinds, a spread of 0.016 per centre.

## 3. Vessels: the deficit is on edges whose two faces die together [measured]

`batch1.sh` to `batch5.sh`; report sections D–G. Asymmetric values not run here are the GPU's (CLAIMS GP1).

**One edge at a time (A = 63, R = 11 cube-centred; in brackets R = 12 vertex-centred).** Groups generated by one,
two, three coordinate mirrors put one, two, three edges of every face on a mirror:

| group | edges in lockstep | ln τ_face | step |
|---|---:|---|---|
| none (c1) | 0 | 13.634 ± 0.018 [14.310 ± 0.026] | |
| one mirror (csz) | 1 | 11.456 ± 0.011 [12.182 ± 0.016] | −2.178 ± 0.021 [−2.128] |
| two (c2v) | 2 | 9.291 ± 0.008 [9.997 ± 0.011] | −2.165 ± 0.013 [−2.185] |
| three (D2h) | 3 | 7.168 ± 0.003, 7.122 with settled lives counted low [7.673, 7.603] | −2.124 [−2.324] |
| inversion (ci) | 0 (opposite faces paired) | 13.578 ± 0.014 | −0.056 ± 0.023 from c1 |
| twofold rotation about an edge-midpoint axis (c2e) | 1, no mirror | 11.704 ± 0.005 | −1.930 ± 0.019 from c1 |

At A = 84 (R = 13 c): 18.141 (GPU), 15.506 ± 0.026, 12.857 ± 0.019, 10.022 ± 0.007: steps −2.635, −2.649,
−2.835; c2e 15.834 ± 0.030 (−2.307). So: edges add (to 2% at A = 63, 7% at A = 84); the group's order is
irrelevant (inversion costs nothing); a mirror is not needed (the rotation gives 89% and 88% of the mirror's
effect). What matters is that the two faces sharing the edge die together.

**By size (D2h against asymmetric, cube-centred).** Per edge and per period of rim ((R−1)/2 periods an edge):

| A | R | c1 | D2h | per edge | per period | D2h, vertex-centred (R+1) |
|---:|---:|---|---|---:|---:|---|
| 63 | 11 | 13.634 ± 0.018 | 7.168 ± 0.003 | 2.155 | 0.431 | 7.673 ± 0.004 |
| 84 | 13 | 18.141 ± 0.005 | 10.022 ± 0.007 | 2.706 | 0.451 | 10.667 ± 0.009 |
| 108 | 15 | 23.376 ± 0.031 | 13.774 ± 0.022 | 3.201 | 0.457 | 14.604 ± 0.033 |
| 135 | 17 | 29.34 ± 0.25 | 18.449 ± 0.071 | 3.630 | 0.454 | |

(A = 45: 9.816 against 5.226, but D2h lives there last about 200 generations and depend on T0.) The marginal cost
is 0.55, 0.50 and 0.43 ± 0.09 per period. D2h faces' own cost per cell is 0.136 (63 → 84), 0.156 (84 → 108) and
0.173 (108 → 135): the faces are
so small that most of each lies within reach of a rim, which is why the phase study read D2h vessels as "an
asymmetric vessel of 0.41–0.46 of the volume". Against the rim-free slab line −0.091 + 0.2088·A a D2h face is
lower by 0.39–0.41 per period of rim, an asymmetric hull face higher by about 0.04: [conjectured] the hull's rim
zone is intrinsically weak, and a face that dies alone pays, along each edge, for the living face it shares that
edge with; faces that die together do not pay it.

**Faces with a threefold axis** (cube-centred; vertex-centred values in the report):

| A | R | T (C3, free rims) | (0.209/3)·A | T_h (C3, rims in lockstep) | T_d (C3v, free rims) | (0.209/6)·A | O_h (C3v, lockstep) | T_d − O_h |
|---:|---:|---|---:|---|---|---:|---|---|
| 108 | 15 | 7.523 ± 0.004 | 7.524 | | | | | |
| 135 | 17 | 9.361 ± 0.008 | 9.405 | | | | | |
| 165 | 19 | 11.509 ± 0.010 | 11.495 | 8.464 ± 0.005 | 6.051 ± 0.006 | 5.748 | | |
| 198 | 21 | 13.819 ± 0.022 | 13.794 | 10.289 ± 0.012 | 6.996 ± 0.004 | 6.897 | | |
| 234 | 23 | | | 12.612 ± 0.038 | 8.018 ± 0.005 | 8.151 | 6.235 ± 0.004 | 1.783 |
| 273 | 25 | | | | 9.312 ± 0.003 | 9.510 | 7.131 ± 0.004 | 2.181 |
| 315 | 27 | | | | 10.664 ± 0.007 | 10.973 | 8.334 ± 0.007 | 2.330 |
| 360 | 29 | | | | 12.206 ± 0.014 | 12.540 | 9.533 ± 0.008 | 2.673 |
| 408 | 31 | | | | 13.778 ± 0.015 | 14.212 | 10.984 ± 0.011 | 2.794 |
| 459 | 33 | | | | 15.635 ± 0.032 | 15.989 | 12.470 ± 0.011 | 3.165 |
| 513 | 35 | | | | 17.291 ± 0.040 | 17.870 | 14.118 ± 0.012 | 3.173 |
| 570 | 37 | | | | 19.489 ± 0.074 | 19.855 | 15.870 ± 0.023 | 3.619 |

- T: on (0.209/3)·A to 0.04 over four sizes. The lockstep of three sectors is all there is.
- T_d: local slopes × 6 are 0.172, 0.170, 0.199, 0.193, 0.206, 0.197, 0.218, 0.184, 0.231: they alternate with R
  mod 4 (the two kinds of point where a mirror meets the rim; R ≡ 1 mod 4 is the high branch). A line through
  A = 315–459 has slope × 6 = 0.2035 ± 0.0008 (± 0.002 with the scatter). Within a sub-series the slopes × 6 are
  0.196, 0.201, 0.201 ± 0.002 (R = 23, 27, 31, 35) and 0.200, 0.208, 0.208 ± 0.004 (R = 25, 29, 33, 37): the two
  branches move apart (T_d − (0.209/6)·A = −0.13, −0.31, −0.43, −0.58 and −0.20, −0.33, −0.35, −0.37), so the
  "alternation" is not simply a fixed offset; I have no account of that.
- The rim term of the wedge, T_d − O_h, rises from 1.78 at 5.5 rim periods to 3.62 ± 0.08 at 9: about 0.5 per
  period, with the same alternation (± 0.07) and a slowly falling increment (section 4). Vertex-centred
  (R = 24–32): 1.848, 2.054, 2.362, 2.509, 2.777, i.e. −0.98 + 0.470·n. In a threefold sector with a whole edge,
  T − T_h = 3.045, 3.530 at 9 and 10 periods (marginal 0.49), and at A = 234 (using T's line) 3.69 against
  2 × 1.783 = 3.57 for the two half-edges of two wedges: the term goes with the length of rim in the quotient.
- The group O (rotations only; adjacent faces are images under twofold rotations, no mirror anywhere) has the
  shortest-lived threefold faces: 7.086 ± 0.003 and 8.694 ± 0.006 at A = 165, 198 (T_h: 8.464, 10.289; T: 11.509,
  13.819). Mirrors are not needed for a deficit of this kind, and here they are the milder case. Not understood:
  for a single edge the rotation is the milder one (c2e above csz by 0.25 and 0.33).

## 4. The O_h law taken apart

`python3 research/theory/symmetric/report.py`, sections G and J; `python3 research/theory/symmetric/oh_data.py`.

    ln τ_Oh(A) = ln τ_Td(A) − rim(A)        n = (R−1)/4 = 0.408·√A − 0.75 rim periods in the wedge (cube-centred)

- **[measured] The rim term**, T_d − O_h of section 3, eight sizes, n = 5.5 to 9:

  | fit | result |
  |---|---|
  | line, R ≤ 33 (made before the two largest sizes were run) | −1.13 + (0.539 ± 0.059)·n |
  | line with an alternation in R mod 4, all eight sizes, weighted | −0.91 + (0.504 ± 0.006)·n ± 0.067; χ² 27.4 on 5 |
  | the same, unweighted | −0.71 + 0.472·n ± 0.077; rms 0.04 |
  | with a quadratic term, weighted | marginal cost 0.478 ± 0.008 at n = 7, falling by 0.062 ± 0.014 per period; χ² 5.2 on 4 |
  | increments per period, R = 23, 27, 31, 35 | 0.548 ± 0.011, 0.464 ± 0.021, 0.379 ± 0.045 |
  | increments per period, R = 25, 29, 33, 37 | 0.492 ± 0.017, 0.492 ± 0.037, 0.453 ± 0.084 |

  As a coefficient of √A (−0.408 × the marginal cost): −0.19 to −0.22 from the lines; step by step, −0.22, −0.20,
  −0.19, −0.20, −0.15 ± 0.02, −0.18 ± 0.03 for the six increments in order of size (A = 234–315 up to 459–570);
  −0.16 ± 0.02 for the last period measured (the two last increments pooled: 0.40 ± 0.04). The coefficient fitted
  to the earlier O_h data (A = 408–828, slope pinned at c/6) is −0.157, −0.171, −0.193, −0.244 for c = 0.2072,
  0.209, 0.2117, 0.2179; the −0.196 first quoted was for c = 0.209 and A ≤ 693. The rim term measured here is as
  large as the whole fitted term, and it gives the fitted coefficient without using the fit.
- **[measured] The T_d part.** Line through A = 315–459: −0.02 + (0.03392 ± 0.00014)·A; with the slope pinned at
  c/6 the intercept is −0.33 (c = 0.209), −0.48 (0.2117), −0.83 (0.2179). Out to A = 570 the slopes × 6 within the
  two sub-series are 0.201 ± 0.002 and 0.208 ± 0.004 (section 3): no steepening.
- **[measured] Rebuilt law minus measured O_h.** Parts fitted at A ≤ 459 only (the T_d line with pinned c on
  A = 315–459 and the rim line on R ≤ 33); O_h measured here to A = 570, earlier CPU and GPU values beyond:

  | A | measured | c = 0.209 | 0.2117 | 0.2155 | 0.2179 |
  |---:|---|---:|---:|---:|---:|
  | 513 | 14.118 ± 0.012 | −0.03 | +0.04 | +0.15 | +0.22 |
  | 570 | 15.870 ± 0.023 | −0.07 | +0.03 | +0.18 | +0.27 |
  | 630 | 17.799 ± 0.102 | −0.18 | −0.05 | +0.14 | +0.25 |
  | 693 | 19.676 ± 0.131 | −0.13 | +0.03 | +0.25 | +0.39 |
  | 759 | 21.889 ± 0.012 | −0.32 | −0.13 | +0.14 | +0.31 |
  | 828 | 24.175 ± 0.072 | −0.47 | −0.25 | +0.06 | +0.26 |

  For c between 0.2117 and 0.2155 the rebuilt law is within 0.25 of every point out of 14 to 24. **It does so by
  compensation.** At A = 513 and 570, where both parts were measured after the fits, the T_d line is too high (by
  0.25 and 0.04 for c = 0.209; 0.33 and 0.14 for 0.2117) and the rim line is too high by nearly as much (0.28 and
  0.11). The agreement is therefore no evidence that either part continues as fitted.
- **[measured, with one assumption] What the GPU's O_h points leave for the rim.** If T_d faces keep a slope
  c_T/6 beyond their last measured sizes, the rim term at A = 759 (n = 10.5) and 828 (n = 11) must be 3.69 and
  4.01 for c_T = 0.2022 (a marginal cost of 0.26 and 0.20 per period beyond the last measured size), 3.97 and 4.30
  for 0.209 (0.40, 0.34), 4.24 and 4.58 for 0.2155 (0.53, 0.48). T_d's measured slope is 0.201–0.208. So unless
  T_d steepens beyond A = 570, the rim's marginal cost between 9 and 11 periods is 0.2–0.4: it continues the fall
  seen inside the measured range.
- **What is not known: the form at large A.** A rim term that settles to ρ∞ per period gives a true √A term with
  coefficient −0.408·ρ∞ (and ρ∞ is then at most about 0.4, coefficient at most −0.16 in size). A rim term that
  saturates gives no √A term: O_h's law is then T_d's minus a constant of 4 or more, and its slope tends to T_d's.
  The data here do not choose. The intercepts (of the T_d line and of the rim term) are fitted, not derived: they
  are the fixed-size objects of the wedge (the centre, the apex, the two ends of the half-edge).
- The earlier fit's free version (a + sA + b√A: s × 6 = 0.249 ± 0.015, b = −0.50 ± 0.12 on A = 408–828) shows
  that the O_h data alone do not pin the form either. With the slope pinned at 0.209/6 the same data give
  b = −0.171 ± 0.003 (χ² 9.8 on 6), not −0.196: the GPU points pull it, which is the same flattening. Below A = 400
  the curvature is stronger (O_h − (0.209/6)·A falls by 0.26 per unit of √A from A = 234 to 459), because the T_d
  part is still bending there.

## 5. The centring [measured]

Report section H. v − c at equal area:

| group | rims | A: v − c |
|---|---|---|
| none | free | 30: +0.747 ± 0.016; 45: +0.738 ± 0.013; 63: +0.676 ± 0.032; 84: +0.646 ± 0.060 |
| T | free | 108: +0.248 ± 0.006; 135: +0.250 ± 0.012; 165: +0.224 ± 0.015 |
| T_d | free | 165–408: +0.249, +0.185, +0.398, +0.240, +0.382, +0.254, +0.405 (± 0.005–0.024): alternating, no trend |
| D2h | lockstep | 63: +0.505; 84: +0.645 ± 0.011; 108: +0.830 ± 0.039 (settled-life bracket ± 0.03) |
| T_h | lockstep | 165: +0.128; 198: +0.290; 234: +0.147 ± 0.056 |
| O_h | lockstep | 234: +0.333; 273: +0.367; 315: +0.351; 360: +0.418; 408: +0.422; 459: +0.457 (± 0.006–0.018, settled-life bracket up to 0.05 at 234); earlier data 513: +0.473 ± 0.033; 759: +0.520 ± 0.041 |

- Free rims: no growth. The asymmetric difference is an object of fixed size, and with a threefold axis it is
  divided by three (T: 0.24 against 0.72/3). The cube-centred face of equal area has 3 apex cells and
  3(R−1) rim-chain cells where the vertex-centred has 3R/2 rim cells: at equal A it has fewer interior cells.
- Lockstep rims: growth. D2h rises by 0.33 over six more rim periods (0.054 per period); the O_h fit
  d0 + k·√A has k = 0.0155 ± 0.0022, i.e. 0.038 per rim period of the wedge; the difference of the two rim terms
  of section 4 is 0.069 per period. The three estimates of the line part agree only in sign and order of
  magnitude.
- O_h over eleven areas (this study below A = 400 with the settled-life bracket in the error, earlier data from
  408): constant 0.3745, χ² 60.8/10; k·√A with k = 0.0213 ± 0.0003, χ² 19.4/10; d0 + k·√A, d0 = 0.104 ± 0.039,
  k = 0.0155 ± 0.0022, χ² 12.5/9.
- T_d's alternation (v − c high where the cube-centred R ≡ 3 mod 4, low where R ≡ 1) follows the number of
  mirror cells on a median, which steps every second R: the end of a mirror line at the rim is an object of fixed
  size with two kinds. In ln τ it is worth about ± 0.03 cube-centred (R ≡ 1 mod 4 high) and ± 0.06 vertex-centred
  (R ≡ 0 mod 4 high), in antiphase at equal area. O_h's v − c does not show it.

## Status of the three questions

1. **The 1/6.** *Derived:* the exact reduction to the wedge; exactness of 1/|G| for free actions; which tori
   admit which symmetry. *Measured:* slope × |stabiliser| = 0.210 ± 0.003 (T, A = 108–198), 0.2035 ± 0.002 (T_d,
   A = 315–459; 0.201 and 0.208 in its two sub-series of sizes out to A = 570), 0.207 ± 0.003 (rim-free C3v
   triangle, 60–72 quotient cells), 0.2011 ± 0.0003 (threefold slab quotients), against asymmetric references
   0.203–0.218 in the same protocol. *Conjectured:* that the limit is
   exactly c/6 (it needs the face law to be a local large-deviation rate, which nobody has proved), and that O_h's
   own slope × 6 (0.191 from A = 570 to 759, 0.199 from 759 to 828) rises to T_d's as the rim term's growth slows.
2. **The √A term.** *Derived:* the geometric factors (rim periods and mirror cells of the wedge, both ≈ 0.41·√A).
   *Measured:* mirror lines and centres do not shorten a rim-free face's life (the mirror-line reading is
   refuted, wrong sign); the deficit is the rim's, additive over edges, present without any mirror, 0.4–0.55 per
   period at the margin in three families; as a √A coefficient −0.19 to −0.22 over A = 234–570, against the
   fit's −0.16 to −0.24; the marginal cost falls within the measured range (0.55 to 0.40 ± 0.04) and the GPU's
   points leave 0.2–0.4 beyond it. *Conjectured:* the mechanism (a face dying alone pays for living neighbours
   along its edges; faces dying together do not). *Open:* whether the term is asymptotically a √A term at all
   (S3 and S5 of PREDICTIONS.md are the test).
3. **The centring.** *Derived:* what differs between the centrings (the rim row and the apex; not the mirror
   lines, not systematically the centre). *Measured:* a fixed part present with no symmetry (0.68–0.75 for a
   whole face, a third of it for T) and a part that grows only when rims die together; for O_h a constant factor
   is excluded and e^(0.10 + 0.0155·√A) fits. *Conjectured:* that the fixed part of the O_h wedge is the
   asymmetric face's share (0.12) and the line part a difference in the rim rows' cost per period (0.04–0.07).

## Forecasts, scored

| forecast | said | found | |
|---|---|---|---|
| P1 slope of mirror strips per quotient cell, P = 8 → 12 at Q = 2 | 0.205–0.215; fail outside 0.195–0.225 | 0.1863 ± 0.0016 | **failed** |
| P2 a diagonal mirror costs σ_d = −0.14 ± 0.08 per mirror cell (the notebook's picture: −0.48) | Δ(8,2) = −0.56 ± 0.32 (−1.92) | +0.872 ± 0.013 | **failed, wrong sign** (both) |
| P3 threefold slab quotients on the asymmetric line ± 0.30 | nine values | all +0.46 to +0.65 | **failed** |
| P3 slope n = 49 → 64 | 3.13 ± 0.10 | 3.044 ± 0.017 | held |
| P4 D2h v − c = 0.119·√A ± 0.15 | 0.94, 1.09, 1.24 at A = 63, 84, 108; growth from A = 45 to 108: 0.44 ± 0.10 | 0.505, 0.645, 0.830; growth 0.40 | levels **failed** (low by 0.4); growth held; the stated failure line (below 0.6 at A = 84) was not crossed |
| P5 asymmetric v − c below a third of D2h's | below 0.14 (A = 45), 0.17 (63) | 0.738, 0.676 | **failed** |
| P6 c1 − D2h, mean of the centrings | 5.4 ± 0.7 (A = 45), 6.9 ± 0.7 (63) | 4.74 (c 4.59, v 4.90; D2h lives too short there to be reliable); 6.55 (6.47, 6.64) | held (at A = 45 by 0.04) |
| Q1 D2h from A = 84 to 108 | 3.9 ± 0.35 | 3.752 ± 0.023 (c), 3.937 ± 0.034 (v) | held |
| Q2 edges add, A = 63 | csz 11.48, c2v 9.32 (± 0.4) from the same hull's c1 and D2h | 11.456, 9.291 (v: within 0.11) | held |
| Q3 inversion costs nothing; one coordinate mirror | 13.63 ± 0.3; 11.5 ± 0.4 | 13.578 ± 0.014; 11.456 ± 0.011 | held; held |
| Q3 rotation about an edge costs little | 13.3 ± 0.4 | 11.704 ± 0.005 | **failed**: lockstep, not the mirror plane |
| Q4 T_d − O_h = 0.34·√(A/6) ± 0.35 | 2.12, 2.29, 2.46, 2.80, 2.97 | 1.783, 2.181, 2.330, 2.794, 3.165 | held |
| Q4 its growth from A = 234 to 459 | 0.85 ± 0.25 | 1.38 ± 0.03 | **failed** (the marginal cost is about 0.5, not 0.34) |
| Q5 T_d slope A = 234 → 408 | 0.031 ± 0.002 per face cell; 0.0348 would mean no deficit | 0.0331 ± 0.0001 | at the upper limit (0.0330), between the two readings |
| Q6 v − c: T_d 0.05 ± 0.15; T 0.15 ± 0.15; O_h 0.40 ± 0.08 (A = 234–315) | | T_d 0.398, 0.240, 0.382; T 0.250, 0.224; O_h 0.333, 0.367, 0.351 | T_d **failed**; T, O_h held |
| Q7 T_d from O_h plus 0.5 per rim period | 13.81 ± 0.15, 14.27 ± 0.15, 15.55 ± 0.20 | 13.778 ± 0.015, 14.183 ± 0.019, 15.635 ± 0.032 | held (3 of 3) |
| R1 rim-free C3v triangle | 7.8, 11.55, 16.1 (± 0.7) | 7.314, 10.822, 15.319 | held, **failed** by 0.03, **failed** by 0.08: above the asymmetric line, by less than forecast |
| R1 triangle above the T_d wedge of equal quotient area at N = 10 | 1.4 ± 0.7 | 0.65 | **failed** by 0.05 |
| R1 slope N = 8 → 12 | 0.19–0.22 | 0.2001 | held |
| R2 edges add, A = 84 | csz 15.43 ± 0.12, c2v 12.73 ± 0.12 | 15.506 ± 0.026, 12.857 ± 0.019 | held; **failed** by 0.007 |
| R3 D2h at A = 135 | 18.24 ± 0.4 | 18.449 ± 0.071 | held |
| R4 asymmetric v − c | 0.72 ± 0.12 (A = 30); 0.66 ± 0.10 (A = 84) | 0.747 ± 0.016; 0.646 ± 0.060 | held; held |
| S1 T_d at A = 513 (O_h plus a linear rim term) | 17.52 ± 0.15 | 17.291 ± 0.040 | **failed** (low by 0.23) |
| S2 group O above T_h by 0.35 | 8.81 ± 0.2, 10.66 ± 0.2 | 7.086, 8.694 | **failed**: O is below T_h by 1.4–1.6 |
| S2 c2e above csz at A = 84 | +0.30 ± 0.15 | +0.328 ± 0.040 | held |
| S4a O_h in this protocol, A = 513, 570 | 14.13 ± 0.05; 15.86 ± 0.10 | 14.118 ± 0.012; 15.870 ± 0.023 | held; held |
| S4b T_d at A = 570 | 19.42 ± 0.12 | 19.489 ± 0.074 | held |
| S4c rim term at 9 periods | 3.56 ± 0.12; "linear" if ≥ 3.62, "flattening" if ≤ 3.50 | 3.619 ± 0.077 | number held; the decision rule returns "undecided" (by 0.001) |
| S4d rim term at 8.5 periods with this study's O_h | 3.16 ± 0.07 | 3.173 ± 0.041 | held |
| S3 O_h v − c at A = 828: 0.55 ± 0.04; T_d at A = 759: 26.4 ± 0.3 (linear rim) | | not run (needs a GPU) | open |
| S5 (amends S3 after block 5) T_d at A = 759 | 25.65 ± 0.25 (T_d keeps its slope) | not run (needs a GPU) | open |

Of 38 scored statements 23 held, one fell on its limit (Q5) and 14 failed, five of them by less than 0.1 beyond
the stated tolerance (R1 three times, R2, S1).

## Not checked

- Nothing beyond A = 570 was run here, and the two largest T_d values rest on 634 and 183 deaths. The rim term is
  measured over 5.5–9 rim periods of the wedge (5–8 of a whole edge for D2h). Its fall in marginal cost rests on
  the eight-size fit (where the smallest sizes, with lives of a few thousand generations that depend on T0,
  carry most of the weight), on one sub-series of increments, and on the GPU's O_h points combined with the
  assumption that T_d's slope does not change beyond A = 570. None of the three is decisive alone.
- Whether the rim term saturates. S3/S5 (a T_d ensemble at A = 759) would test it; it needs a GPU.
- The asymptotic slope: every slope quoted is at 30–80 quotient cells. "Exactly c/6" is not established, and c
  itself is only known to 0.207–0.219.
- The mechanism of the rim deficit (the "living neighbour" reading) is an interpretation of the ladder, the
  rotation and the inversion runs. Nobody has looked at the faces: no occupancy maps, no last-cells analysis of a
  D2h or O_h death, no measurement of how the neighbour face behaves while an asymmetric face dies.
- Why the group O is so much weaker than T_h while a single rotated edge (c2e) is milder than a single mirrored
  one; why the Q = 2 mirror strips keep a slope of 0.186; why T_d's intercept is −0.3 to −0.6 and why its two
  sub-series of sizes (R mod 4) move apart.
- The fixed-size objects (centre, apex, ends of mirror lines) are not measured one by one; only the alternation
  with R mod 4 and the three centre kinds on a slab were seen. OPEN-PROBLEMS 11 (the nine-cell state) was not
  touched.
- One protocol throughout (soup 0.4, T0 = 512, events every 4 generations); the comparison values from the GPU and
  `research/fluct` use soup 0.35 and T0 = 200 or 1000. Where both exist they agree within 0.04 (section I of the
  report), but the A = 84, 108, 135 asymmetric references were not rerun here.
- Each number is one job with one seed (two for `rect_4_2_c1`, the D2h faces at R ≤ 14 and T_d at R = 37); no
  independent stepper reran any of them. The stepper is validated for 1,500 generations per system, not for the 10⁶–10⁷ of
  production lives.
- Short-lived systems (ln τ below about 7: D2h at R ≤ 12, O_h and T_d at R ≤ 24, O) move by up to 0.3 with T0 and
  carry the settled-life bracket; they enter the conclusions only through the A = 63 ladder (where the three
  steps agree) and the lowest two points of the T_d − O_h line.
- Firewalls: slab runs end a life at a transverse firewall and count face deaths only; `rect_4_4_cs`,
  `rect_6_4_cs`, `rect_3_4_c1`, `rect_3_3_c1` and `rect_4_3_cs` have firewall shares of 9–87% and are quoted but
  not used in any conclusion. Vessels have no firewall test (as in the earlier vessel studies).
- The centred (Möbius) mirror tori and the √3-type C3v torus were validated but not used beyond `hex_6_6_c3v`
  (12.027 ± 0.013 at 54 quotient cells).

## Reproduce

```sh
python3 research/theory/symmetric/validate.py              # orbit stepper against the engine: ALL OK (~5 min)
bash research/theory/symmetric/batch1.sh                   # block 1 (~20 min, one core)
for L in 1 2 3; do bash research/theory/symmetric/batch2.sh $L & done; wait      # block 2 (~12 min, three cores)
for L in 1 2 3; do bash research/theory/symmetric/batch3.sh $L & done; wait      # block 3 (~20 min)
bash research/theory/symmetric/batch4.sh                   # block 4 (~17 min)
for L in 1 2 3; do bash research/theory/symmetric/batch5.sh $L & done; wait      # block 5 (~36 min)
python3 research/theory/symmetric/run.py csv               # scratch -> data/runs.csv, and the full table
python3 research/theory/symmetric/report.py                # every table and fit above
python3 research/theory/symmetric/oh_data.py               # face geometry; the earlier O_h data and its fits
python3 research/theory/symmetric/run.py run oct_11_c_csz 400000 1    # one run: SPEC, generations per replica, seed
```

Seeds are fixed in the batch files, so a rerun reproduces the lives exactly. Two differences from what is
tabulated: `batch1.sh` as rerun today uses the ladder snapshots throughout (the first 20 of its runs were made
with doubling snapshots, which changes only how settled lives are recorded), and its D2h runs at R ≤ 14 would be
pooled with the seed-2 runs of `batch2.sh` (here the seed-1 files were set aside in
`research/scratch/symmetric/block1_doubling/`). Bulk output: `research/scratch/symmetric/` (one uint32 per life).
A candidate line for `research/check.sh`: `python3 research/theory/symmetric/validate.py 300` must print `ALL OK`.
