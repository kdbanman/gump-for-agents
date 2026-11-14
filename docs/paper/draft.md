# Confined chaos on the faces of the cubic honeycomb: a cellular automaton whose turbulence dies one face at a time

(authors to be decided by the owner)

*Draft 1, 2026-11-14. Internal draft; it stays in the repository. How the work was produced and how that is
disclosed is the owner's decision and is not addressed here.*

**How to read the tags.** Every sentence that states a result carries one of **[proved]**, **[measured]**,
**[conjecture]**; a forecast is a conjecture until scored. After the tag comes the row of the project's claims
ledger (`research/CLAIMS.md`) and its verification grade: **A** = re-derived independently by different code or a
different reader; **B** = re-run or recomputed from the committed data and matched; **B−** = as B, but the runs
were made on a GPU that no second implementation has repeated. Only A and B claims appear as results. A claim
graded **C** (has a command, not re-run) appears only where marked *preliminary*. "ln τ ± x" always means the
statistical error 1/√(number of deaths) unless said otherwise; it does not include systematic errors, which are
discussed where known. Section 12 defines the estimators.

## Abstract

We study "gump", a three-dimensional outer-totalistic cellular automaton written as a Processing sketch in 2012,
whose cells are the *faces* of the cubic honeycomb. A face has twelve neighbours (the eight perpendicular faces
sharing an edge with it and the four coplanar faces touching it at a corner); it is born on 4 or 5 live neighbours
and survives on 3, 4 or 5. **Proved:** no birth can cross a {111} plane, so every finite pattern is confined for
ever to an octahedral hull that can only shrink, and is eventually periodic; three consecutive dead {111} layers
separate their two sides for ever; each {111} layer is a closed automaton on a kagome lattice; in a finite vessel
the rule is a symmetric threshold network except at overcrowded cells, with an exact energy identity
ΔE = D − Q; and in a slab three or more layers thick no finite set of cells can die unconditionally.
**Measured:** inside a hull, random initial conditions settle into a chaotic state (density 0.41552 ± 0.00002 on
tori) that is metastable and ends layer by layer: an outer {111} face goes extinct as a whole after a memoryless
wait whose mean grows exponentially with the number A of cells in the face, by a factor of about e^{0.21} per
cell, over ln τ from 5.6 to 29.3. The death of a face is the end of its own quasi-stationary fluctuations: the
log-probability of finding k live cells is linear in k down to k = 1 and the death rate is the next point on the
line. The law is not a function of area alone: octahedral faces are tougher than periodic faces of equal area,
the lifetime of a periodic face depends on how its torus closes on itself, and every candidate law in area and
shortest loop that was fixed before the runs was refuted. Symmetric initial conditions die exponentially sooner;
this accounts for the 2012 series of cubic seeds, extended here to a cube of side 16 that ran 2,919,617,676
generations, although the one forecast of that lifetime made before the run was low by a factor 12. Five or six
layers of the rule above fresh coin flips reproduce a slab face's lifetime to 0.015 in ln τ, so the exponent is
set in a boundary layer driven by noise. **Not proved:** the area law, and its constant. We give what is known
rigorously (a conditional area law resting on a measured hypothesis; an exponential law for a deterministic
relative of a two-dimensional analogue, conditional on two published percolation statements), relate the
phenomenon to supertransient chaos, and say candidly which parts appear to be new.

## 1. Introduction

Long-lived chaotic transients whose mean lifetime grows exponentially with system size, and which end abruptly
with exponentially distributed lifetimes, are known numerically in coupled map lattices, reaction–diffusion
systems and the complex Ginzburg–Landau equation under the name *supertransients* [CK88, WS03, HKTP10, TL08],
and in cellular-automaton-like coupled maps as *stable chaos* [PT09]. In everything recorded in this project's
literature notes the statements are fits to simulations; nothing is proved (`research/PRIOR-ART.md`, last
section). This paper describes a cellular automaton in which the *geometry* of such a collapse is a matter of
theorems, so that the statistics can be measured one irreversible event at a time.

The automaton lives on the faces of the cubic honeycomb. Its key structural fact is one inequality: a dead cell
just outside a {111} plane has at most three live neighbours behind the plane, and birth needs four. From it
follow confinement to an octahedral hull, the absence of spaceships, permanent "firewalls" of three dead layers,
and a decomposition of the lattice into a stack of closed kagome automata (Section 3). Inside a hull the rule
sustains chaos for a time that is astronomically long in the hull's size, and the chaos can only end by events
that the theorems single out: the extinction of an outer {111} layer (after which, by confinement, that layer is
dead for ever and the hull is one layer smaller), or a three-layer firewall. We measure the waiting-time law of
those events (Section 5), find where its exponent is made (Section 6), and find that it depends on the shape and
symmetry of the face in ways not yet reduced to a formula (Sections 5.4 and 7).

The results fall into three kinds, and we keep them apart throughout.

- *Proved*: the structure theorems of Section 3, the twist lemma for oscillators (Section 8), the half-space
  criterion for confinement (Section 9), and two conditional theorems about lifetimes (Section 10).
- *Measured*: the chaotic phase (Section 4), the face-extinction law and its dependence on geometry and symmetry
  (Sections 5–7), the debris (Section 8), the neighbourhood in rule space (Section 9).
- *Conjectured or open*: that the wait is exponential in the area for a reason derivable from the rule; the value
  of the constant; several extrapolations. Section 10 lists them.

Several measurements were preceded by forecasts committed to the repository before the runs; we report every such
forecast we found, including those that failed (Section 5.6).

## 2. The automaton and its lattice

### 2.1 Cells

The cells are the faces of the cubic honeycomb. In *doubled coordinates* a cell is a point p = (x, y, z) ∈ Z³
with exactly one odd coordinate: cubes have side 2 and centres with all coordinates even, and the odd coordinate
of a cell is its normal axis. (Two odd coordinates would be an edge midpoint, three a vertex.) There are three
cells per cube; a torus of N³ cubes has 3N³ cells. Equivalently the cells are the bonds of the dual cubic
lattice, i.e. the vertex set of the rectified cubic honeycomb; crystallographically this is the anion sublattice
of the ReO₃ / cubic perovskite structure (`research/PRIOR-ART.md` §2; the identification with the perovskite
anion lattice is standard crystallography that the project's survey did not source: [citation needed: a
crystallography reference for the ReO₃ anion sublattice and its {111} kagome layers]).

### 2.2 Neighbourhood and rule

A face with normal axis a (other axes b, c) has twelve neighbours, at doubled offsets

- ±2e_b ± 2e_c: the four coplanar faces that touch it only at a corner;
- ±e_a ± e_b and ±e_a ± e_c: the eight perpendicular faces that share an edge with it (every face of its two
  adjoining cubes other than itself and the two faces opposite it).

The four coplanar faces that share an edge with it, and the two parallel faces across the adjoining cubes, are
not neighbours. In terms of the rectified cubic honeycomb the eight perpendicular neighbours are the edge graph
and the four coplanar ones are a second shell at distance 2√2.

The rule is outer-totalistic and synchronous, **B45/S345**: with n the number of live neighbours, a dead cell
becomes live iff n ∈ {4, 5}; a live cell stays live iff n ∈ {3, 4, 5}. Writing x ∈ {0, 1} for the cell's own
state, this is "alive next iff n + x ≥ 4 and n ≤ 5": a threshold with a cap. The neighbourhood is invariant under
translations by cube steps and under the 48-element octahedral group O_h, so the dynamics is; a symmetry of the
initial condition is preserved for ever.

The rule studied here is the rule as coded and run in 2012; its author intended the four coplanar neighbours to
be the edge-sharing ones, and that variant is a different automaton (confined to a box, not an octahedron) which
this paper does not treat.

Figure 1 (placeholder; does not exist): *one face with its twelve neighbours, the eight perpendicular ones and
the four coplanar corner-touching ones, and the same neighbourhood resolved into {111} layers (1, 2, 6, 2, 1).*
A tracked image that shows one {111} layer as a kagome lattice is `web/docs/kagome-face-layer.png`.

### 2.3 Fidelity to the 2012 runs

**[measured]** A short reference implementation (`reference/oracle.py`) reproduces the population logs of the
2012 runs from closed cubic seeds of side 8 to 12 at every generation (R1, R2; B), and a bit-sliced engine
reproduces the reference state for state and all six surviving logs, sides 8 to 13, at every generation, in open
space and on the 2012 code's torus (R3; B). **[measured]** The 2012 lifetimes for sides 8–13 are free of
wrap-around artefacts (R4; B). A "side-n closed cube" is an n × n × n block of cubes with all faces live:
**[proved]** it has 3n²(n + 1) cells and its diagonal hull has L1 radius 3n − 2 in doubled units about its centre
(T6 of the ledger; A). Every other stepper used in this paper (numpy, bit-sliced C on arbitrary cell graphs,
symmetry-reduced, GPU) was required to agree with the engine or the reference bit for bit before its numbers
were used (R7; B; Section 12).

| side n | generations to the final state | final state | source |
|---:|---:|---|---|
| 8 | 23 | static, 384 cells | 2012 log; reference matches (R1) |
| 9 | 71 | static, 54 cells | 2012 log; R1 |
| 10 | 65 | static, 264 cells | 2012 log; R1 |
| 11 | 4,218 | static, 36 cells | 2012 log; R1 |
| 12 | 24,286 | static, 288 cells | 2012 log; R2 |
| 13 | 169,049 | static, 108 cells | 2012 log; engine (R3) |
| 14 | 4,460,298 | period 2, 528 cells | this work (C1; B) |
| 15 | 37,367,092 | extinct | this work (C1; B) |
| 16 | 2,919,617,676 | static, 96 cells | this work (C2; B: data re-derived, the run not repeated) |

Table 1. Closed cubic seeds. **[measured]** For sides 14 and 16 the figure is the generation at which the
engine detected the final cycle, one or two generations after it was entered (`docs/AUTOMATON.md` §4).

## 3. Structure theorems

Let d ∈ {±1}³ be a body diagonal and s = d·p. Since exactly one coordinate of a cell is odd, s is odd for every
cell: each diagonal slices the lattice into *layers* s = …, −3, −1, 1, 3, … There are four diagonal axes.

**Theorem 1 (layer histogram) [proved]** (T1; A). For every cell and every d, its twelve neighbours are
distributed over layers as Δs = −4: 1, −2: 2, 0: 6, +2: 2, +4: 1.
*Proof.* Enumeration of the twelve offsets. For a face with normal x and d = (1,1,1): the coplanar offsets
(0, ±2, ±2) give Δs = 4, 0, 0, −4; the offsets (±1, ±1, 0) and (±1, 0, ±1) give Δs = 2, 0, 0, −2 twice. The other
orientations and diagonals follow by symmetry. ∎

**Theorem 2 (octahedral confinement) [proved]** (T2; A). If every cell with s > C is dead, that remains true for
ever.
*Proof.* A dead cell in layer C + 2 has at most 1 + 2 = 3 neighbours in layers ≤ C; one in layer C + 4 has at
most 1. Birth needs 4. ∎

*Consequences* **[proved]**. Define the *diagonal hull* of a finite pattern as the intersection of the eight
tightest half-spaces d·p ≤ C_d containing it (an octahedron, possibly truncated). A finite pattern stays inside
its diagonal hull for ever, and the hull never grows. Hence there are no spaceships and no unbounded growth;
every finite pattern is eventually periodic, within 2^N generations for a hull of N cells; and the finite
environment needed to simulate a finite seed exactly and for ever is computable from the seed. Axis-aligned
half-spaces do *not* confine: a dead cell just outside one can have four live neighbours inside (ledger T5; A),
which is why cubic seeds grow into octahedra. Information travels at most one cube per generation in the
max-norm, through the coplanar neighbours.

**Theorem 3 (firewall) [proved]** (T3; A). If three consecutive layers C + 2, C + 4, C + 6 of some diagonal are
dead, they stay dead for ever, and the two sides never influence each other again. Two dead layers are not
enough.
*Proof.* A cell of layer C + 2 has at most 1 + 2 = 3 live neighbours (in layers C − 2 and C), a cell of layer
C + 6 likewise from the other side, and a cell of layer C + 4 at most 1 + 1 = 2. With only two dead layers a cell
of one of them can have 1 + 2 on one side and 1 on the other, which is 4. ∎ The statement holds for infinite and
toroidal configurations too.

**Theorem 4 (closed sub-automata; the kagome stack) [proved]** (T4; A). A pattern contained in m consecutive
layers stays in them. The cells of one {111} layer form a kagome lattice: the four in-layer perpendicular
neighbours of a cell are its kagome nearest neighbours and the two in-layer coplanar neighbours sit across the
two hexagons it borders. Each layer is therefore a closed two-dimensional automaton running B45/S345 on six
neighbours, and the full automaton is an ABC stack of kagome layers in which a cell is coupled to 6 cells of its
own layer, 2 + 2 of the adjacent layers and 1 + 1 of the layers after those.

Theorems 2 and 3 hold for every outer-totalistic rule on this neighbourhood whose smallest birth count is at
least 4. More generally **[proved]** (ledger K1 of the class study; A): for any lattice, any neighbourhood and
least birth count b, the outside of a half-space H = {u·p ≤ C}, once dead, stays dead if and only if no cell
outside H has b or more neighbours inside H; with one cell type the condition depends on the direction u alone
(`research/audit/REVIEW-class.md` §1.2). Theorem 2 is the case u = d, b = 4.

**Theorem 5 (threshold lemma) [proved]** (T8; A, the algebra re-derived by an independent reader; numerical
checks B). Let V be a finite vessel (a torus, or a region whose outside is dead for ever), A the adjacency matrix
of the neighbour graph on V, W = A + I, and x(t) ∈ {0,1}^V the state. Write n_i(t) = (A x(t))_i and
h_i = n_i + x_i. The *uncapped* rule U, "alive next iff h ≥ 4", is a threshold network with symmetric weights.
Gump agrees with U at every cell with n ≤ 5 and differs from it at every *overcrowded* cell, n ≥ 6 (gump: dead;
U: alive). Define, summing over ordered pairs,

$$E(t) = -\,x(t)^{\mathsf T} W\, x(t-1) + 3.5\,\bigl(|x(t)| + |x(t-1)|\bigr).$$

Then for gump, exactly,

$$E(t+1) - E(t) = D(t) - Q(t),$$

where Q(t) = Σ |h_i(t) − 3.5| ≥ 0 over non-overcrowded cells with x_i(t+1) ≠ x_i(t−1), and
D(t) = Σ (h_i(t) − 3.5) ≥ 0 over overcrowded cells with x_i(t−1) = 1 ("O1 events").
*Proof.* By symmetry of W, x(t)ᵀW x(t−1) = Σ_i x_i(t−1) h_i(t), so
E(t+1) − E(t) = −Σ_i (x_i(t+1) − x_i(t−1))(h_i(t) − 3.5). A term vanishes unless x_i(t+1) ≠ x_i(t−1). At a
non-overcrowded cell the rule is U: if x_i(t+1) = 1 then h_i(t) ≥ 4, if x_i(t+1) = 0 then h_i(t) ≤ 3, and in both
cases the term is −|h_i(t) − 3.5| ≤ −½. At an overcrowded cell x_i(t+1) = 0 and the term is
x_i(t−1)(h_i(t) − 3.5), which is zero or lies in [2.5, 9.5]. ∎

*Consequences* **[proved]**. (i) For U, D ≡ 0 and −6N ≤ E ≤ 7N (N = |V|), so U reaches period ≤ 2 within 26N + 1
steps; this is the period-two theorem for symmetric threshold networks, attributed to Goles and Olivos [GO80,
GO81; read only through KMMK11, GMRS23], with the two-time energy attributed to [GFP85] (not obtained; the bound
26N + 1 is derived here and has not been compared with that paper). (ii) A gump orbit with no O1 event from some
time on has period ≤ 2. (iii) Over any periodic orbit total drive equals total dissipation, and every oscillator
of period ≥ 3 has O1 events, at least R₃/10 per period if R₃ of its cells have period ≥ 3. (iv) The lemma is
false for infinite configurations: under U a half-space of live cells advances for ever. **[measured]** The
identity was checked at every step of 5,683 steps on tori, slabs and an octahedral vessel, and
Σ_period D = Σ_period Q on all 1,307 catalogued objects, of which all 329 of period ≥ 3 have an O1 event and none
of the 978 of period ≤ 2 does (`research/theory/threshold.md` §4; covered by `research/check.sh`). So all
behaviour beyond period 2, chaos and clockwork alike, is driven at overcrowded cells; in the 2D analogue of
Section 9 the same holds.

**Theorem 6 (sealed sets; why three layers) [proved]** (T9; A for the theorem, read and re-derived by an
independent reader). Call a set W of cells of a vessel *sealed* if each of its cells has at most 3 neighbours in
the vessel outside W. (a) A dead sealed set stays dead whatever happens elsewhere; unions of sealed sets are
sealed; so the largest dead sealed set K(t) is non-decreasing in t. The outside of a hull (Theorem 2) and a
firewall (Theorem 3) are instances. (b) In a slab of m ≥ 3 consecutive {111} layers, and in the full lattice,
every non-empty sealed set is infinite; on a torus slab every component of a sealed set contains a
non-contractible loop; in a diagonal-hull vessel every component of a sealed set is adjacent to the vessel's
outside. (c) In one layer the six cells of a kagome hexagon ring are sealed, and so is every half-plane, so a
one-layer pattern never leaves the convex hull of its live cells. In two layers there is a sealed set of 36
cells.
*Proof of (b).* Per Theorem 1 the twelve offsets of a cell are centrally symmetric: six in-layer (three ± pairs),
two at Δs = +2 (call them a, b) with negatives at −2, and one at +4 (call it e) with negative at −4. For the face
with normal x and d = (1,1,1), a = (1,1,0), b = (1,0,1), e = (0,2,2), so e + 2(a + b) = 4d: the in-plane
projections satisfy ē = −2(ā + b̄); the other cases follow by symmetry. Let W be finite and non-empty, v an
in-plane vector with v·ō ≠ 0 for every offset o, and c ∈ W a maximiser of v·p. Every neighbour c + o with
v·ō > 0 is outside W. Three of these are in-layer. If c is in an interior layer, one of each pair ±a, ±b
qualifies: at least 5 in all. If c is in the bottom layer, the candidates are a, b and e (in the slab because
m ≥ 3): if v·ā < 0 and v·b̄ < 0 then v·ē = −2(v·ā + v·b̄) > 0, so at least one qualifies: at least 4. The top
layer is symmetric. So c has at least 4 neighbours outside W and W is not sealed. In the full lattice take v
generic in R³: six neighbours of the maximiser are outside. The torus and hull statements follow by lifting to
the cover and by adjoining the (sealed) outside of the hull. ∎ (Full proofs: `research/theory/thickness.md` §2.
The minimality of the 36-cell two-layer set is computer-checked within a finite patch only, grade C, and is not
claimed.)

Theorem 6 says that in three or more layers unconditional death cannot start locally: it must come in from a face
or span the vessel. This is the mechanism the measurements of Section 5 find. It also explains, as far as a
theorem about sealed sets can, the role of thickness 3: *preliminary* **[measured]** (ledger K1 of the thickness
study; C) soups in slabs one or two layers thick settle in times growing like the logarithm of the area (means
4.6–11.9 and 44–101 generations), while in three layers ln τ grows linearly with the slab's width. That thin
slabs "freeze" is a statement about typical states only: *preliminary* **[measured]** (C) the one-layer automaton
has oscillators of periods 3 to 12.

**Proposition 7 (the vertex star) [proved]** (T10; A). The 12 faces incident to one lattice vertex form a closed
vessel: each sees 5 of the others, and no cell outside sees more than 2 of them. Of its 4,096 states, all settle
within 3 generations, 2,750 die, 107 are non-empty still lifes and 195 lie on two-cycles (10 still lifes and 14
period-2 oscillators up to symmetry).

## 4. The chaotic phase

All statements in this section are about random initial conditions ("soups": each cell live independently with a
stated probability) and are **[measured]**.

**Bulk.** On tori of 16³, 32³ and 64³ cubes the density of live cells settles at
ρ* = 0.41552 ± 0.00002, the same at all three sizes (P1; A + B: an independent 32³ run gave 0.4152 and an
independent 64³ rerun 0.415516 ± 0.000003). The susceptibility of the global density,
χ = N·Var(ρ)/ρ(1 − ρ), is 3.16 ± 0.05 and size-independent, and the global density rings: its autocorrelation at
lags 1–4 is −0.44, −0.10, +0.34, −0.23 (P2; B: rerun 3.158 ± 0.037 and −0.44, −0.10, +0.33, −0.24).

**Mean field** **[proved, a calculation]** (P3; A). The single-site mean-field map
f(p) = (1 − p)·P[Bin(12, p) ∈ {4, 5}] + p·P[Bin(12, p) ∈ {3, 4, 5}] has fixed points 0, 0.178 (unstable) and 0.444
with slope −1.55, hence also unstable: its attractor is a 4-cycle 0.319 → 0.486 → 0.369 → 0.511 with mean 0.421.
The lattice state is stationary at 0.4155 with a damped oscillation instead; the mean field alone does not
describe it.

**Symmetric states are depleted on mirror planes** (P7; A, two independent measurements agree). In
O_h-symmetric states cells on mirror planes have density ≈ 0.31–0.35 against 0.41–0.42 off them; a symmetric
octahedron runs at ≈ 0.39 overall, while asymmetric confined chaos runs at ≈ 0.43 with its outer face layers
*enhanced*, ≈ 0.51. So the density ≈ 0.39–0.40 visible in the 2012 population logs is a property of symmetric
seeds, not of the phase.

**The bulk without faces is long-lived.** Whole-torus soups (no faces) have mean lifetime 1.18 × 10³ generations
at N = 4 cubes a side and 8.7 × 10⁵ at N = 5, and none of 512 ended within 10⁶ generations at N = 6, 7 or 8 (P8;
A + B: reruns gave 1194 ± 53 at N = 4, and 8.6 ± 0.8 × 10⁵ and 1.3 ± 0.2 × 10⁶ in two batches at N = 5). We do not
claim the chaotic state is stable in infinite volume; that is not known.

*Preliminary* (grade C; each has a command and has not been re-run): correlations are isotropic with correlation
length ξ = 0.68 ± 0.01 cube (P4); damage from one flipped cell spread in 40 of 40 trials as a sphere at
0.83–0.87 cube per generation (P5); chaos invades vacuum through planar fronts at 0.177 ({100}) and 0.165 ({110})
cube per generation (P6). That the front speed across {111} is exactly zero is Theorem 2. A referee would ask for
a Lyapunov exponent or an equivalent; none has been measured, and "chaotic" in this paper means: aperiodic over
the times observed, with damage spreading (P5, preliminary) and short correlations (P4, preliminary).

Figures: `research/figures/phase_bulk.png` (bulk density and its fluctuations),
`research/figures/phase_spread.png` (damage and fronts; supports only the preliminary statements),
`research/figures/phase_symmetry.png` (density by symmetry class).

