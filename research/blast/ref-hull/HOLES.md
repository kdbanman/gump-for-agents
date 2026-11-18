# HOLES.md: referee's verdict on agent `holes` (ref-hull, 2026-11-18, 12:28–12:50 UTC)

Own code only: `sl.c` (slab torus) and `rh.c` (hull), the steppers validated against the oracle earlier tonight
(`validate.py`, `validate_slab.py`; the stepping kernel is unchanged, the new modes only read the state; ring of
past states lengthened from 8 to 16, re-checked: `python3 validate_slab.py 12 0 12 1 300 0 1` and
`python3 validate.py 11 1 300` pass). I read `research/blast/holes/README.md` and its `data/` tables, not its code.
Rows: `out/holes/`; tables: `out/HOLES-ANALYSIS.txt` (`python3 holes.py out/holes/h_torus.txt out/holes/h_hull21.txt`).
Everything is **[measured]** unless marked.

| claim | verdict |
|---|---|
| 1. torus: f = −ln P(rhombus empty), mixed differences 0.2646 and 0.2595 per cell | numbers **CONFIRMED**; "the bulk cost of a hole is 0.26" **confirmed with a correction** (it is the cost of widening a hole 2–4 units wide) |
| 2. hull interior = torus; rim −0.98, corner −3.21 | **CONFIRMED** |
| 3. 18-cell hull face, ln τ = 4.855 ± 0.015, plateau | number and plateau **CONFIRMED**; "same family" **doubtful** (two corrections) |
| 4. closed tori 3 × 6 and 2 × 8 against `points.txt` | **both right**: different definitions (firewalls along the short diagonals) |
| 5. else | one consequence of 4 for its item 2; busts and fits not checked |

## 1. The torus 12 × 12 × 8

`./sl hole 12 0 12 SEED 250000`, SEED = 1 … 8 (soup 1/2, first 500 generations dropped; class P = the three outward
cells of a cube, cube centres (2I, 6 − 2I − 2J, 2J), rhombus I0 ≤ I < I0 + a, J0 ≤ J < J0 + b, the same orientation
as `holes`'s (⌊x/2⌋, ⌊z/2⌋); all 144 translates, both faces; a × b and b × a pooled). 5.1 × 10⁸ replica-generations
(8% of `holes`'s). Errors: delete-one jackknife over the 64 groups of 32 lanes, beside the scatter of the 8 seeds.

| shape | mine | `holes` | mine − `holes` |
|---|---|---|---|
| 2 × 2 | 6.1598 ± 0.0001 | 6.1598 ± 0.0001 | 0.0000 |
| 2 × 3 | 8.6753 ± 0.0003 | 8.6753 ± 0.0001 | 0.0000 |
| 3 × 3 | 11.9819 ± 0.0016 | 11.9849 ± 0.0007 | −0.0030 (1.7 errors) |
| 2 × 4 | 11.1414 ± 0.0008 | 11.1417 ± 0.0002 | −0.0003 |
| 3 × 4 | 15.2238 ± 0.0052 | 15.2298 ± 0.0022 | −0.0060 (1.1) |
| 4 × 4 | 19.15 ± 0.05 (710 hits) | 19.2377 ± 0.0151 | −0.09 (1.8) |
| M(2.5, 2.5)/3 | 0.2637 ± 0.0005 | 0.2646 ± 0.0002 | −0.0009 (1.7) |
| M(2.5, 3.5)/3 | 0.2586 ± 0.0014 | 0.2595 ± 0.0005 | −0.0009 (0.6) |
| M(1.5, 2.5)/3, M(1.5, 3.5)/3 | 0.2813 ± 0.0001, 0.2689 ± 0.0003 | 0.2814, 0.2691 | |
| M(3.5, 3.5)/3 | 0.228 ± 0.015 | 0.2543 ± 0.0045 | −0.026 (1.7) |

- **0.26 stands** at (2.5, 2.5) and (2.5, 3.5). (1 × 1 and 1 × 2: 1.9718, 3.6260, identical; a × b minus b × a,
  which symmetry makes zero: 0.0001 ± 0.0003 for 2 × 3, −0.010 ± 0.008 for 3 × 4.)
- **Errors honest.** My jackknife and my seed scatter agree (3 × 3: 0.0016 and 0.0019; 3 × 4: 0.0052 and 0.0056;
  M(2.5, 3.5): 0.0014 and 0.0013). Scaled to `holes`'s exposure (× 0.285) they predict 0.0005 for 3 × 3, 0.0015
  for 3 × 4, 0.0004 for M(2.5, 3.5): its 0.0007, 0.0022, 0.0005 are that or larger. Lanes are independent
  replicas, so a jackknife over lane groups is legitimate; with eight groups the error itself is good to a quarter.
- **The logic, with a correction.** The mixed difference removes any g(a) + h(b) exactly. But f is not "bulk +
  perimeter + corners" at these sizes: the pure second differences f(a+1, b) − 2f(a, b) + f(a−1, b), zero for that
  form, are −0.018, −0.071 ± 0.001, −0.103 ± 0.005 at a = 2 for b = 2, 3, 4 and −0.050, −0.065 ± 0.004 at a = 3
  for b = 2, 3: they grow with the other side, i.e. the cost per unit length of a strip depends on its width (the
  two long edges are not independent). So M(a+½, b+½) is "what one more row adds to a strip's cost per unit of
  length", λ(a+1) − λ(a), and it equals the bulk price only for strips wider than both edge zones. Reached: widths
  1.5 to 3.5. Its flatness along b at a = 2.5 is expected in either regime and does not test convergence in the
  width; across the width the values are 0.264 → 0.259 → 0.254 ± 0.005 (mine 0.228 ± 0.015) at b = 2.5 … 3.5. **What
  is established: widening a hole 2 to 4 units wide costs 0.26 per cell. That wide holes cost 0.26 and not 0.2087
  is not established** (`holes` says so in its item 6; its item 1 and its opening answer do not).

## 2. Interior, rim and corner of a hull face (R = 21, 198-cell faces)

`./rh hole 21 SEED 250000`, SEED = 1 … 4 (2.6 × 10⁸ replica-generations; every patch pooled over the 48 images of
the hull; margin ≥ 2 = every unit cell two or more rows from every rim; no face ever empty).

| patch | mine, hull | reference | difference |
|---|---|---|---|
| interior 2 × 2 | 6.1601 ± 0.0003 | my torus 6.1598 ± 0.0001 | **+0.0004 ± 0.0003** (`holes`: +0.0001) |
| interior 2 × 3 | 8.6763 ± 0.0010 | my torus 8.6753 ± 0.0003 | **+0.0009 ± 0.0010** (`holes`: +0.0007) |
| interior 3 × 3 | 11.977 ± 0.006 | my torus 11.9819 ± 0.0016 | −0.005 ± 0.007 |
| 3 × 3, first row on a rim (other rims ≥ 3 rows away) | 10.997 ± 0.003 | my torus 3 × 3 | **−0.985** (`holes`: −0.98) |
| corner 3 × 3 | 8.7752 ± 0.0016 | my torus 3 × 3 | **−3.207** (`holes`: −3.21; its R = 21 value 8.775) |
| corner 2 × 2, 2 × 3 | 4.0559 ± 0.0002, 6.0616 ± 0.0004 | `holes` 4.0556, 6.0608 | +0.0003, +0.0008 |

Confirmed to the digit. (A single unit cell at margin ≥ 2 is likelier empty than on the torus by 0.0016 at R = 21.)

## 3. The 18-cell hull face (R = 5)

`./rh life 5 SEED 400000 160 DENS CENSOR` (256 lanes refilled at each first death; hazard of the first empty face
by age of the soup; CENSOR = 1 drops a lane when its state repeats with period ≤ 12, as `holes` does). ln(8E/D):

| generations | soup 0.35, censored | soup 0.50, censored | soup 0.50, not censored |
|---|---|---|---|
| 21–40 | 4.8657 ± 0.0010 | 4.8997 ± 0.0008 | 4.9021 |
| 41–60 | 4.8502 ± 0.0018 | 4.8575 ± 0.0016 | 4.8845 |
| 61–80 | 4.8573 ± 0.0035 | 4.8556 ± 0.0030 | 4.961 |
| 81–100 | 4.8665 ± 0.0067 | 4.8552 ± 0.0057 | 5.22 |
| 101–120 | 4.908 ± 0.013 | 4.891 ± 0.011 | 5.84 |
| 141–160 | 5.42 ± 0.05 | 5.23 ± 0.04 | 8.00 |
| 41–100 pooled | **4.8526 ± 0.0016** | **4.8570 ± 0.0013** | |

- **There is a plateau and it is 4.855**, the same from soups of 0.35 and 0.50 once the soup is forgotten (the two
  differ by 0.034, 0.007, 0.002 in successive windows). `holes`'s ± 0.015 is generous.
- It exists only with the censoring: 0.25% of soups freeze into periodic states with all eight faces occupied, and
  uncensored they take over the risk set within 60 generations. Even censored, states of period above 12 remain
  (458 of 4.6 × 10⁶ soups reach generation 160) and lift the last windows.
- **Same family? Two corrections.** (a) The plateau lasts 3.7 lifetimes of a hull that lives 16 generations, while
  the memory of the soup decays by a factor 5 per 20 generations: the "living state" relaxes about as slowly as it
  dies (R = 7: 112 generations against the same relaxation; R = 9: 2,300). (b) **Faces do not die one at a time:**
  after generation 40, 14.5% of first deaths empty two or more faces in the same generation, 1.176 faces per first
  death (R = 7: 2.5% and 1.025; R = 9: 0.2% and 1.002; `./rh life 7 23 600000 1200 0.35 1`, `./rh life 9 24 300000
  3000 0.35 1`, which also give plateaus 6.805 ± 0.002 and 9.83 ± 0.01). The anchors' 8E/D counts a first death as
  one face; counted per emptied face the 18-cell value is 4.855 − ln 1.176 = **4.693** (R = 7: 6.779; R = 9
  unchanged). The rows formula says 4.589: its miss is 0.27 by first deaths and 0.10 by faces [not refitted with
  the shifted 30-cell anchor]. So "the rows formula is refuted" and the price 0.223 of formula S rest on a point
  whose meaning moves by 0.16 with the convention. The face density in the plateau, 0.420, does continue the
  series 0.453, 0.480, 0.496 of R = 7, 9, 11.

## 4. Closed tori 3 × 6 and 2 × 8: who is right

Both. `./sl life H 0 D SEED GENS 300 200000 0.5` follows 256 slabs from soup and books, after generation 300, the
first of: a face empty; a **firewall** = three consecutive dead layers along any of the four body diagonals (T3;
along the slab's own normal, or along the three others, whose layers close up around the torus: 2D, 2H and
2·gcd(H, D) of them). ln(2E/F) with F = faces emptied with no firewall before, E = exposure up to the first event:

| torus | my ln(2E/F), no firewall before | `points.txt` | my firewall share | its fw% | `holes` (first empty face, any cause) | ln(2E/F) + ln(1 − share) |
|---|---|---|---|---|---|---|
| 2 × 8 | 9.472 ± 0.007 (seed 1: 9.489 ± 0.012) | 9.4888 ± 0.0030 | 64.7% (35,952 of the 35,959 firewalls along a short diagonal) | 65.4 | 8.4504 | 8.43 |
| 3 × 6 | 11.078 ± 0.007 | 11.0824 | 12.8% | | 10.9428 | 10.94 |
| 4 × 4, 4 × 5 | 9.923 ± 0.006, 12.475 ± 0.014 | (9.9251) | 0.5%, 0.5% | | 9.9282, 12.4708 | |

- `points.txt` is the face channel alone; `holes` counts every first empty face, including the faces of slabs that
  a firewall had already cut (on 3 × 6, 86% of those do not lose a face within 300 generations: they decay slowly).
  With firewalls ignored my code gives `holes`'s number: `./sl life` before the diagonal firewalls were added read
  8.464 ± 0.007 for 2 × 8.
- Firewall shares of the other shapes it uses: 2 × 6 17.5%, 3 × 3 3.3%, 3 × 5 2.5%, 3 × 4 1.5%.
- **Consequence for `holes`'s item 2.** The comparison "hole against the death of a closed face of its own shape"
  should use the face channel. At (3.5, 3.5) and (3.5, 4.5) this changes nothing (shares ≤ 3.3%, +0.003 per cell):
  "dearer by 0.044 ± 0.005" stands. The rows built on two-unit tori and on 3 × 6 do not: D(3 × 6) becomes 10.87, not
  11.00, against 10.98 ± 0.08 for 4 × 5, and D(2 × 8) 11.6, not 12.65.

## Not checked

- Item 6 of `holes` (busts, launch fullness), the fits of its section 5, the triangles and strips of its item 5,
  class Q, anything at R = 29, patches beyond 4 × 4.
- Lifetimes of the 3 × 3, 3 × 4, 3 × 5 tori: my `sl life` has no censoring of periodic states and reads high there
  (6.51 for 3 × 3 against `holes`'s 5.487, whose own windows are flat); only its firewall shares are used.
- Which convention `points.txt` uses for a firewall and a face emptying in the same generation (I book it as
  firewall; 0.1–0.5% of events).
- The rows formula refitted with per-face counts.
