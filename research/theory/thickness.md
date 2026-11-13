# S6 — critical thickness: what is true, what is proved

*2026-11-13, theory agent (S5/S6). Tags: **[proved]**, **[measured]** (n, command), **[conjecture]**.
Scripts: `sealed.py`, `kagtorus.py`, `exhaust.c` (build: `cc -O2 -o research/scratch/theory/exhaust
research/theory/exhaust.c`), `overcrowd.py`; data: `kagome_osc.json`, `exhaust_results.txt`.*

## Summary

1. **The hoped-for theorem is false.** The one-layer (kagome) automaton does **not** always reach period ≤ 2: it has
   oscillators of periods 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 (and composites 18, 22) — oracle-verified, one layer
   thick, with tiny rotors (3–15 cells) held in large still stators. So no energy argument can prove "freezing";
   the budget (c) of S5 balances exactly on these cycles.
2. **What *is* true and proved is a sharp geometric dichotomy at thickness 3** (§2). Call a set of cells *sealed* if
   each of its cells has ≤ 3 neighbours outside it (in the vessel). A dead sealed set stays dead whatever happens
   elsewhere; dead sealed sets only accumulate. Then:
   - in **1 and 2 layers**, there are **finite** sealed sets (6 cells: a kagome hexagon ring; 36 cells in two layers),
     so permanent death can **nucleate locally, anywhere**;
   - in **≥ 3 layers** (and in 3D), **no finite set is sealed**: every component of the permanently dead region must
     wrap the torus or touch the vessel's outside. Permanent death can only come from a global object — a face
     (peeling) or a spanning firewall. This is exactly the mechanism measured in the notebook.
   - In one layer, moreover, **every half-plane is sealed**: a one-layer pattern never leaves the convex hull of its
     live cells (a 2D confinement much stronger than the octahedral T2).
3. **Measured**: in one layer the permanently dead region (the *skeleton*) covers 25% of the lattice at t = 0 (ρ = 0.4),
   64% at t = 1, 92% at t = 5; the unsealed region breaks into finite pockets (largest ~ 10² cells, growing only
   slowly with system size) by t ≈ 2–3. Two layers: the same by t ≈ 50–100. Three layers: the skeleton stays
   exactly empty through 1,000 generations. After fragmentation each pocket is a finite closed system, which is why
   lifetimes grow only like log(area).
4. **Not proved**: that local sealing actually halts activity for typical (random) configurations of the infinite
   layer — reduced below (§4) to a precisely stated percolation statement.

## 1. What the one- and two-layer automata do [measured, exhaustive where stated]

**Oscillators in one layer.** From the kagome soup census (`research/scratch/atlas/kagome_soup.jsonl`, written by
`research/atlas/kagome_soup.py 24 300 SEED --census`; 1,728-cell tori), the R-connected objects of period ≥ 3 were
re-stepped on the infinite lattice with `research/atlas/lattice.py` and the representatives in `kagome_osc.json`
re-verified with the numpy oracle (`lattice.oracle_verify`): periods 3 (33 cells), 4 (27), 5 (68), 6 (52),
7 (110), 8 (60), 9 (68), 10 (65), 11 (70), 12 (74), all **thickness 1** along one diagonal. Per-cell periods show
they are genuine: e.g. the P11 (70 cells) has 62 still cells and 8 cells of period 11; the P7 (110) 103 still and 8
of period 7; every P12 found is a period-3 rotor and a period-4 rotor side by side (compound), and the soup's
P18/P22 are 2 + 9 and 2 + 11 compounds. Every one has O1 events (S5), all at cells with exactly 6 live neighbours.
Census counts of non-wrapping one-layer objects by period (22 census records, all densities): P1 70,432,
P2 1,967, P3 196, P4 391, P5 5, P6 103, P7 4, P8 11, P9 6, P10 9, P11 3, P12 28, P18 2, P22 1.

**Exhaustive phase portraits of small closed vessels** (`exhaust.c`; all 2^n states; tori from `kagtorus.py`:
in-plane sublattice (p, q, r) of index pr, 3prm cells; full results in `exhaust_results.txt`):

| vessel (p,q,r; m) | cells | periods that occur | max transient |
|---|---|---|---|
| 1 layer, (3,1,1) | 9 | 1, 2 | 3 |
| 1 layer, (5,1,1) | 15 | 1, 2 | 12 |
| 1 layer, (3,2,2) | 18 | 1, 2, 6 | 14 |
| 1 layer, (7,1,1) / (7,2,1) | 21 | 1, 2 / 1, 2, 6 | 15 / 28 |
| 1 layer, (8,1,1) | 24 | 1, 2, 3, 6, 8 | 20 |
| 1 layer, (4,1,2) | 24 | 1, 2, 4, 6, 8 | 31 |
| 1 layer, (3,0,3) = 3×3 | 27 | 1, 2, 3, 4, 6 | 17 |
| 1 layer, (3,1,3) | 27 | 1, 2, 3, 4 | 39 |
| 1 layer, (10,1,1) | 30 | 1, 2, 3, 4, **20** | 25 |
| 1 layer, (5,1,2) | 30 | 1, 2, 3, 4, 6, 8 | 56 |
| 2 layers, (3,1,1) | 18 | 1, 2, 4, 6 | 13 |
| 2 layers, (5,1,1) | 30 | 1, 2, 3, 4, 5, 6, 8, **70** | 88 |
| uncapped rule, every vessel above with ≤ 24 cells | | 1, 2 only | ≤ 11 |

(The 2 × 2 tori, 12 and 24 cells, have doubled edges; they are listed in the results file as weighted networks.)
Small tori are dominated by orbits that wrap around them (the P20 and P70 are on 1-cube-wide tori), so these
tables say what small closed systems do, not what the infinite layer does.

**Soups** (`overcrowd.py timecourse 16 m 40 1001 7`, N = 16, ρ = 0.4): in one layer O1 events (the only energy
source) fall from 1.3% of cells at t = 1 to zero by t ≈ 20 and activity M to 0; two layers keep O1 ≈ 0.07–0.1 for
~20 generations and lose it by t ≈ 100; three layers hold O1 ≈ 0.115 indefinitely (table in threshold.md).
Earlier measurements (notebook): mean lifetimes 4.6 → 11.9 (m = 1) and 44 → 101 (m = 2) for N = 4 → 32, i.e.
∝ log(area).

## 2. Sealed sets [proved]

Let V be a vessel (here: m consecutive `{111}` layers on the infinite lattice or on a torus; cells outside are dead
forever by T4). For W ⊆ V let out(c, W) = number of neighbours of c in V \ W.

**Lemma 1 (sealing).** If out(c, W) ≤ 3 for every c ∈ W ("W is sealed") and W is dead at time t, W is dead at all
later times. Conversely, if some c ∈ W has out(c, W) ≥ 4, there is a configuration with W dead whose successor has
c alive. *Proof.* A dead cell of W sees at most out(c, W) ≤ 3 live cells, and birth needs 4. Conversely make exactly
four of c's outside neighbours live and everything else dead: c has n = 4 and is born. ∎

**Lemma 2 (skeleton).** Unions of sealed sets are sealed (out(c, W₁ ∪ W₂) ≤ out(c, W₁)). Hence the dead set at time t
has a largest sealed subset K(t), and K(t) ⊆ K(t+1). Neighbour-components of a sealed set are sealed (a cell's
neighbours inside W lie in its own component). *Proof.* Immediate; K(t) is dead at t+1 by Lemma 1, and sealed. ∎

(K is the local version of PROGRAM.md's "skeleton"; T2's outside of a hull and T3's firewalls are sealed sets.)

**Theorem 3 (no finite sealed sets in ≥ 3 layers or in 3D).** In the m-layer slab with m ≥ 3, and in the full
lattice, every nonempty sealed set is infinite; on a torus slab every component of a nonempty sealed set contains a
non-contractible loop; in a finite diagonal-hull vessel (octahedron) every component of a sealed set has a cell
adjacent to the vessel's outside.

*Proof.* Each cell's 12 offsets are centrally symmetric, and negation reverses the layer step Δs. Per T1 they are:
6 in-layer (3 ± pairs), 2 at Δs = +2 (call them a, b) whose negatives are the 2 at Δs = −2, and 1 at Δs = +4 (e)
whose negative is at −4. Direct check for the face with normal x and d = (1,1,1): a = (1,1,0), b = (1,0,1),
e = (0,2,2), so **e + 2(a + b) = 4d**, i.e. the in-plane projections satisfy ē = −2(ā + b̄); the same holds for the
other orientations and diagonals by symmetry (verified numerically for all three orientations).
Let W be finite and nonempty, and v an in-plane vector with v·ō ≠ 0 for every offset o (all projections ō are
nonzero, so such v exist). Let c ∈ W maximise v·p (any maximiser). Every neighbour c + o with v·ō > 0 is outside W.
Among those *inside the slab*: exactly 3 in-layer. If c is in an interior layer, both ±a and ±b are in the slab and
one of each pair has v·ō > 0: total ≥ 5. If c is in the bottom layer, the in-slab candidates are a, b (layer +1)
and e (layer +2, in the slab because m ≥ 3); if v·ā < 0 and v·b̄ < 0 then v·ē = −2(v·ā + v·b̄) > 0. So at least one
is outside W: total ≥ 4. The top layer is the same with −a, −b, −e. So out(c, W) ≥ 4: W is not sealed.
In 3D take v generic in R³: 6 of the 12 neighbours of the maximiser are outside W.
Torus: lift a sealed set to the universal cover (the infinite slab); it stays sealed; a contractible component
lifts to finite components, each sealed by Lemma 2 — impossible. Hull vessel V (an intersection of half-spaces
d·p ≤ C_d): its complement X is sealed in Z³ (T2: a cell outside sees ≤ 3 inside), so for W ⊆ V sealed in V,
W ∪ X is sealed in Z³; a component of W not adjacent to X would be a finite sealed component of W ∪ X. ∎

**Theorem 4 (one layer: everything local is sealable; convex confinement).**
(i) The 6 cells of a kagome hexagon ring form a sealed set; no sealed set has fewer cells.
(ii) Every half-plane of a layer is sealed. Hence a one-layer pattern never leaves the convex hull of its live cells
(positions in doubled coordinates), and that hull is non-increasing in time.
*Proof.* (i) Each ring cell has its two ring neighbours (kagome bonds along the hexagon) and the opposite ring cell
(its across-the-hexagon neighbour) inside: out = 3. Minimality: SAT search over all sets through a fixed cell in a
hexagonal patch of radius 8 (`python3 research/theory/sealed.py minsat 1 8 6`; every cell is equivalent under the
layer's symmetries, and a connected set of ≤ 5 cells lies within that patch) — none with ≤ 5 cells.
(ii) For any in-plane v, at most one of each ± pair of in-layer offsets has v·o < 0, so a cell of {v·p > C} has ≤ 3
neighbours in its complement. The complement of the convex hull is a union of such open half-planes; apply Lemmas
1–2. ∎ (In two layers this fails: a bottom-layer cell can have 5 neighbours behind a line.)

**Proposition 5 (two layers).** The two-layer slab has finite sealed sets; the smallest has **36 cells** (18 per
layer: one closed 18-cell kagome loop in each layer, offset). *Status:* existence [proved] by the explicit set
(`sealed.py minsat 2 7 36` prints it; `is_sealed` checks it). Minimality [computer-checked within a patch]: SAT finds
none with ≤ 35 cells among sets through a fixed cell inside the hexagonal patch of radius 7 (all cells equivalent:
translations, the 3-fold axis, and the inversion swapping the layers); a 35-cell set reaching beyond that patch is
not excluded. Exhaustive DFS (`sealed.py minimal 2 …`) excludes ≤ 9 cells everywhere.

Patch check (`python3 research/theory/sealed.py patches`): the largest sealed subset of hexagonal / parallelogram
patches of radius 3, 6, 10 is (almost) the whole patch for m = 1, ~85% of it for m = 2, and **empty** for m = 3, 4, 5.

**Torus slabs, m = 3** (`python3 research/theory/sealed.py torusmin N 3 500`; SAT, exact): TORUSMIN

## 3. The skeleton in soups [measured]

`python3 research/theory/sealed.py skeleton 16 m 20 1001 5` (N = 16 torus, ρ = 0.4, 20 soups; |K(t)|/|V|):

| t | 0 | 1 | 2 | 5 | 10 | 20 | 50 | 100 | 1000 |
|---|---|---|---|---|---|---|---|---|---|
| m = 1 | 0.252 | 0.639 | 0.776 | 0.921 | 0.963 | 0.967 | 0.967 | 0.967 | 0.967 |
| m = 2 | 0 | 0 | 0.017 | 0.059 | 0.175 | 0.357 | 0.739 | 0.851 | 0.856 |
| m = 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

(Monotonicity of K asserted along every run.) Pockets — components of the unsealed region U(t) = V \ K(t), each a
closed system from then on (`sealed.py pockets N m 10 1 [rho] [times]`), largest pocket mean / max over 10 soups:

| m = 1 | t = 0 | 1 | 2 | 3 | 5 | 10 | 20 |
|---|---|---|---|---|---|---|---|
| N = 16 (768 cells) | 545 / 634 | 167 / 262 | 84 / 124 | 56 / 108 | 42 / 87 | 28 / 65 | 22 / 53 |
| N = 32 (3,072) | 2270 / 2524 | 541 / 1214 | 132 / 205 | 84 / 135 | 49 / 81 | 30 / 43 | 27 / 41 |
| N = 64 (12,288) | 8955 / 9359 | 1453 / 2423 | 228 / 368 | 142 / 256 | 76 / 97 | 51 / 77 | 45 / 74 |

| m = 2 | t = 0 | 10 | 20 | 50 | 100 | 200 |
|---|---|---|---|---|---|---|
| N = 16 (1,536) | 1536 | 1234 | 894 | 132 | 44 | 44 |
| N = 32 (6,144) | 6144 | 5259 | 3736 | 310 | 64 | 59 |

In one layer U(t) percolates at t = 0 (a giant pocket of ~73% of the cells), is near-critical at t = 1, and from
t ≈ 2 is broken into pockets whose largest size grows only slowly with the system (84 → 132 → 228 at t = 2 for 16× the
area). Two layers fragment by t ≈ 50. At the end, every dead cell of a one-layer final state is in K (5/5 soups,
N = 16; 0.1% exceptions) — debris in one layer is "live cells + sealed vacuum".

## 4. What a full proof of "thin slabs cannot sustain chaos" still needs

*Reduction [proved].* If at some time t₀ every component of U(t₀) is finite (and, on a torus, contractible), the
dynamics from t₀ on is a product of finite closed systems, so every cell is eventually periodic, with transient ≤
t₀ + max over its pocket P of the transient of the P-automaton (≤ 2^|P|), and no activity crosses between pockets.
*Missing:* a proof that for a Bernoulli(ρ) initial condition on the infinite layer, U(t₀) has no infinite component
almost surely for some fixed t₀ (data: t₀ = 2–3 for one layer at ρ = 0.4; t₀ ≈ 50 for two). One rigorous route:
replace K by the *local* skeleton (the union of hexagon rings dead at some time ≤ t₀ — local, so U is a finite-range
dependent field) and verify non-percolation by a finite-size criterion for k-dependent percolation (Liggett–Schonmann–
Stacey domination plus a computer-checked block estimate). I have not done this; it would be computer-assisted and
would hold only for the ρ checked, and only for the hexagon-ring skeleton in one layer (two layers need the 36-cell
sets, a much weaker local skeleton).

*Why no proof can be purely energetic:* the oscillators of §1 balance drive and dissipation exactly, and some are
stable inside sealed vacuum. "Thin slabs cannot sustain chaos" must therefore be a statement about typical
configurations, and the theorem behind the *threshold at 3* is geometric (Theorem 3 vs Theorem 4/Prop. 5), not
energetic.

**[conjecture]** For every ρ ∈ (0, 1), in the one-layer and two-layer automata on the infinite lattice started from
Bernoulli(ρ), U(t) has only finite components for all t ≥ t₀(ρ) a.s.; consequently every cell is eventually periodic
and P(cell still active at t) decays exponentially in t. In ≥ 3 layers, by Theorem 3, K(t) = ∅ for all t on the
infinite slab, whatever the initial condition — *permanent death never nucleates; only a face can die*.

## 5. Consequences for the programme

- **D2 (debris by geometry)** gets a definition with teeth: a state is debris if its unsealed region U consists of
  pockets too thin to contain a finite sealed-free region — in practice, pockets of a 1- or 2-layer vessel. In
  ≥ 3 layers an interior pocket can only be cut off by a spanning sealed set (the measured transverse firewall).
- The critical thickness 3 is **exactly** where finite sealed sets stop existing (Theorem 3 needs the Δs = +4
  neighbour, i.e. a third layer, and the identity ē = −2(ā + b̄)). This is a sharp, proved structural threshold that
  coincides with the measured one.
