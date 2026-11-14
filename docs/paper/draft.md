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
symmetry of the face in ways not yet reduced to a formula (Sections 5.5 and 7).

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
behaviour beyond period 2, chaos and clockwork alike, is driven at overcrowded cells.

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

## 5. How confined chaos ends

### 5.1 The staircase is the hull losing one layer at a time

The 2012 population logs of cubic seeds show a long noisy plateau followed by a staircase of lower plateaus.
**[measured]** (F1; B) For the side-11 cube the hull radius (outermost live layer along every diagonal, in doubled
units about the centre) falls from 31 to 27 within five generations, stays at 27 for 3,285 generations, and then
every face loses its outer layer at generations 3,290, 3,477 and 3,796 (the first generation at which that layer
is empty), before a final collapse ending at 4,218; no interior firewall forms before the final collapse.
**[measured]** (F3; B) The side-13 cube does the same at about 130,200, 145,850, 156,800, 166,650 and 168,200,
ending at 169,049. Each stair is the loss of one {111} layer from every face of the octahedron (all eight at once
because the seed is O_h-symmetric); by Theorem 2 each loss is irreversible. *Preliminary* **[measured]** (F2; C):
the plateau heights of side 11 are 0.79, 0.61, 0.48 of the first, against hull-volume ratios (R/27)³ = 0.79,
0.62, 0.47. A tracked picture of a peel as a kymograph of layer populations is `web/docs/peel-kymograph.png`.

So the lifetime of confined chaos is a sum of waiting times for well-defined irreversible events, and the
question becomes: what is the law of the wait for one face layer to die?

**Vessels and faces.** Two families of vessel are used. (i) *Octahedra*: all cells with |p − c|₁ ≤ R (doubled
units) in open space, c a cube centre (R odd) or a lattice vertex (R even); by Theorem 2 the outside is dead for
ever, so the simulation is exact. Its eight faces are the outermost layers; a face has A = 3k(k + 1)/2 cells with
k = ⌈R/2⌉ (A = 30, 45, 63, 84, 108, 135 for R = 7, …, 17; checked by direct count for every size used,
`docs/paper/check_face_area.py`). (ii) *Slabs*: m consecutive {111} layers (m = 8 unless said), periodic in the
plane with a period lattice of index n, so that each of the two faces is a torus of A = 3n cells with no edges.
Theorem 4 makes the slab a closed system. A *face death* is the first generation at which an outer layer is
empty. Random initial conditions have density 0.3–0.4; replicas are followed from an age T₀ (200 generations
unless said) and only while their hull is still the full vessel.

### 5.2 The face-extinction law

**Estimator.** For an ensemble of replicas of one vessel, the mean wait to the first face death is
(total exposure in replica-generations)/(number of deaths), the maximum-likelihood estimate for an exponential
wait with censoring. We quote the per-face time τ_face = (number of faces) × (mean first wait): × 8 for
octahedra, × 2 for slabs. This treats the faces of a vessel as dying independently, an assumption that the
comparison of octahedra with slabs below shows to be only approximately harmless. Replicas that settle into a
periodic state while a face is still occupied never die and must be censored at every period (Section 12).

**Memoryless.** **[measured]** (F5; A) For slab faces of A ≥ 36 the first-death times have coefficient of
variation 0.96–1.05 and pass a Kolmogorov–Smirnov test against the exponential (p = 0.5–0.96); an independent
engine-only measurement on octahedra gave CV 1.03 and 0.99 at R = 9 and 11. Faces of A ≤ 27 are
transient-dominated and are not exponential. **[measured]** (GP5; B−) In the largest sample, 5,971 deaths of
cube-centred O_h-symmetric soups at R = 43 with replica ages up to 2.6 τ, a censored Weibull fit gives shape
k = 1.020 (95%: 1.000–1.042): no ageing. (An apparent fall of the death rate with age in a shorter run at this
size was noise; the same indication at R = 45, k = 0.84 on 192 deaths, has not been re-run.)

**Exponential in the area.** **[measured]** (F4; B from the curated table, with the slope supported at grade A by
two independent routes) For slab faces with m = 8 on eight near-square period lattices, A = 27 to 90, a weighted
fit gives

$$\ln \tau_{\rm face} = (-0.091 \pm 0.047) + (0.2088 \pm 0.0009)\,A,$$

with residuals up to 0.18 and τ_face from 2.8 × 10² to 1.6 × 10⁸ generations
(`python3 research/peeling/face_law_fit.py`; figure `research/figures/peel_face_law.png`, which predates the
measurements below and plots symmetric faces against a rescaled area that this paper does not use). The first
death time does not depend on the slab's thickness once m ≥ 7: at A = 48 it is 9.9, 10.4, 10.3, 10.3, 10.3 × 10³
generations for m = 7, 8, 9, 10, 12 (`research/peeling/slab_area.csv`). This fit is a first description only:
Section 7 shows that it mixes faces of different widths, that a single slope does not describe periodic faces,
and that its slope is inflated by the mixture.

**Octahedral faces.** **[measured]** Table 2 gives the per-face lifetimes of asymmetric soups in octahedra. The
law has the same form and octahedral faces are tougher than periodic ones: 1.7–1.9 times the slab line at
A = 45, 63, 84 (F6; B + A), and at A = 108 an octahedral face has ln τ_face larger by 0.91 ± 0.06 than a 6 × 6
periodic face measured with the same estimator (GP7; B), or by 0.84 ± 0.04 against the pooled, firewall-resolved
slab value 22.537 ± 0.031 (GP8; B). What makes them tougher (the rim, eight faces sharing edges, the interior, the
shape) has not been separated. The cost per cell is not constant: the local slopes of Table 2 are 0.201, 0.212,
0.215, 0.218 ± 0.001 and 0.221 ± 0.009, still rising at A = 135 (GP1; B−). Its limit, if there is one, is not
known. An earlier extrapolated limit, 0.2077 ± 0.0014, was withdrawn when it was found to miss its own data.

| R | A | face deaths | ln τ_face | source and independent values |
|---:|---:|---:|---:|---|
| 7 | 30 | 117,851 | 6.804 ± 0.003 | symmetry-free bit-sliced CPU ensemble (F9, tabulated value; B); an engine-only run gives −ln h/A = 0.2274 against 0.2268 |
| 9 | 45 | 137,243 | 9.820 ± 0.003 | same (F9; B); engine-only run of 13,765 deaths: 9.824 (F8; A) |
| 11 | 63 | 764,941 | 13.635 ± 0.001 | GPU ensemble (calibration row of GP1); CPU: 13.633 ± 0.008 |
| 13 | 84 | 34,026 | 18.141 ± 0.005 | GPU; two independent CPU runs: 18.154 ± 0.025 and 18.148 ± 0.028; the earlier CPU value 18.077 ± 0.054 (342 deaths) |
| 15 | 108 | 1,059 | 23.376 ± 0.031 | GPU only (GP1; B−) |
| 17 | 135 | 16 | 29.34 ± 0.25 | GPU only (GP1; B−); replica ages reach 1/900 of the mean |

Table 2. Asymmetric soups (density 0.35) in octahedra of L1 radius R; τ_face = 8 × mean wait to the first face
death. **[measured]** Local slopes between successive rows: 0.2011, 0.2119, 0.2146, 0.2181, 0.2209. Nothing at
A ≥ 108 has been reproduced by a second implementation or a second GPU run; the kernel was checked bit for bit
against the CPU steppers by emulation, which cannot check the GPU's execution.

Figure 2 (placeholder; does not exist): *ln τ_face against A for octahedral faces (Table 2), periodic faces by
width family (Table 6), and O_h-symmetric faces (Table 3), with the lines 0.2072·A and 0.2088·A for reference.*

### 5.3 A face dies off the end of its own stationary distribution

**[measured]** (F8; A + B: the study's symmetry-free ensemble, an engine-only rerun, and a third rerun of 3,000
soups) Let n be the number of live cells of one face of a living asymmetric octahedron, sampled every generation
from T₀ on, and p_k the quasi-stationary probability that n = k. At R = 7, 9, 11, 13 (A = 30–84):

- ln p_k is linear in k from k ≈ 10 down to k = 1, with ratio p_k/p_{k+1} ≈ 0.65 (the engine-only run at R = 9
  gives 0.658, 0.499, 0.778, 0.650, 0.630, 0.652, 0.655 for k = 1, 2, …: straight apart from an excess at k = 3);
- the death rate per face per generation h is the next point on the line: h/p₁ = 0.645, 0.613, 0.601, 0.594 at
  the four sizes (engine-only at R = 9: 0.616–0.621), against p₁/p₂ ≈ 0.66;
- the end-game does not depend on size: 62–63% of deaths are from a single surviving cell and 23–25% from two; a
  face reduced to one cell dies rather than recovers with probability 0.67–0.72.

So, at these sizes, τ_face ≈ 1/(0.6·p₁): the whole factor e^{−0.2A} is the quasi-stationary probability of being
down to one cell, and no separate mechanism of death is needed. The endpoints are −ln h/A = 0.2268, 0.2182,
0.2164, 0.2152 at A = 30, 45, 63, 84 (F9; B for these four values; the limit fitted to them is withdrawn). A tail
extrapolated from densities n/A ≥ 0.1, which is all one can sample on large faces, misses ln h by 0.5–0.8; the
endpoint has to be measured. Figure: `research/figures/fluct_tail.png`.

*Preliminary* **[measured]** (C): the commonest three-cell remnant is a triangle of the kagome layer, the three
faces round one cube corner (38% of three-cell faces; F10); a dying face is statistically ordinary until about 16
generations before its death and empties in 10–12 (F12); forward-flux sampling along n is unbiased but gains
nothing, because two copies of a state differing in one cell have 55–95% correlated fates over the few
generations of the plunge (F12). The last point matters for method: the rare event here is a rare
*configuration* reached quickly, not a slow rare path, and what made large faces measurable was brute force on
bit-sliced and symmetry-reduced steppers.

### 5.4 The competing channel: transverse firewalls

A slab or an elongated vessel can also die by a three-layer firewall (Theorem 3) across one of the other three
diagonals, after which a face dies within a small fraction of the wait. Lifetimes that count any outer-layer
death therefore mix two channels, and the face law must be read from the face channel alone. **[measured]**
(GP8; B) With every life ended at its first event and the two channels counted separately, the firewall rate at a
cut of 216 cells is the same in a square and a non-square slab: ln τ_fw = 26.79 ± 0.28 per direction (6 × 6 × 8,
13 firewalls) and 26.87 ± 0.19 (6 × 7 × 8, 29 firewalls). The method was validated on a slab where both channels
are common: 3 × 6 × 8 gives ln τ_face = 11.084 ± 0.001 and ln τ_fw = 12.327 ± 0.002 on the GPU and
11.076 ± 0.007 and 12.310 ± 0.018 in an independent CPU run with a different stepper. *Preliminary*
**[measured]** (F11; C): over thin slabs the firewall costs about 0.12 per cell of the three-layer band that
must die, roughly half the cost per cell of a face, and the first event switches from firewall to face death
when the thickness is about the width. In an octahedron the faces are the smallest {111} sections and no interior
firewall was seen before the final collapse of the cubes examined (F1). A practical consequence: eight-layer
slabs cannot measure the face channel beyond A ≈ 110 unless firewalls are detected.

### 5.5 Symmetric initial conditions die exponentially sooner

An O_h-symmetric soup (one coin per orbit of cells) stays symmetric. Its eight faces are images of one another
and die in the same generation, so the residence time at a given hull radius is measured directly. Table 3 gives
it for cube-centred (R odd) and vertex-centred (R even) hulls.

| A | cube-centred: R, deaths, ln τ | vertex-centred: R, deaths, ln τ | ln(τ_v/τ_c) |
|---:|---|---|---:|
| 360 | | 30; 66,555; 9.988 ± 0.004 | |
| 408 | 31; 1,087; 10.993 ± 0.030 | 32; 14,641; 11.411 ± 0.008 | 0.42 ± 0.03 |
| 459 | 33; 5,141; 12.473 ± 0.014 | 34; 4,181; 12.898 ± 0.015 | 0.42 ± 0.02 |
| 513 | 35; 933; 14.151 ± 0.033 | 36; 2,177; 14.620 ± 0.021 (GPU: 99,763; 14.625 ± 0.003) | 0.47 ± 0.04 |
| 570 | 37; 167; 15.881 ± 0.077 | 38; 279; 16.278 ± 0.060 (GPU: 112,545; 16.345 ± 0.003) | 0.40 ± 0.10 |
| 630 | 39; 96; 17.799 ± 0.102 | 40; 46; 18.220 ± 0.147 (GPU: 45,785; 18.273 ± 0.005) | 0.42 ± 0.18 (0.47 ± 0.10 with the GPU value) |
| 693 | 41; 58; 19.68 ± 0.13 | 42; 45; 20.38 ± 0.15 | 0.70 ± 0.20 |
| 759 | 43; GPU 1,057; 21.903 ± 0.031 (with a longer run: 21.889 ± 0.012) | 44; GPU 637; 22.409 ± 0.040 | 0.51 ± 0.05 |
| 828 | 45; GPU 192; 24.175 ± 0.072 | | |

Table 3. O_h-symmetric soups; τ = mean residence at hull radius R, states older than 1,000 generations.
**[measured]** CPU rows: orbit-reduced stepper, `research/fluct/data/sym_residence.csv`, fresh soups only (S2,
S3; B, with agreement between two independent implementations at A = 408–630, grade A). GPU rows: GP2, GP3
(B−, B). The ratio column uses the CPU values; `python3 research/fluct/sym_fit.py` prints 0.27 ± 0.13 at A = 630
and 0.87 ± 0.18 at A = 693 because it pools copies of the side-16 cube's own states into the vertex values there.

**[measured]** What the table shows.

- *Scale.* A symmetric face family of 759 cells lives about as long (ln τ ≈ 21.9) as an asymmetric octahedral
  face of roughly 100 cells (Table 2). The 2012 side-13 cube lasted 1.7 × 10⁵ generations in a hull whose faces
  have 459 cells; symmetric soups at that size have mean residence 2.6 × 10⁵.
- *No fixed "effective area".* Over A = 408–693 the cube-centred values are fitted (χ² = 4.0 on 4) by
  ln τ = 0.698 + (0.209/6)·A − 0.196·√A, i.e. the periodic-face slope shared among the six images of a face cell
  under the face's stabiliser, less a boundary term (S2; B + A). This is a description of that range, not an
  established law: free fits to the same points prefer slopes between 0.024 and 0.044 depending on the curvature
  term, and the two GPU points beyond the range lie 0.16 and 0.27 above the fitted curve. The local slope between
  A = 759 and 828 is 0.0329 ± 0.0011, to be compared with 0.209/6 = 0.0348 (GP2; B−). The asymptotic symmetric
  slope is open.
- *Centre matters.* Vertex-centred hulls are tougher than cube-centred ones of equal face area by a factor about
  1.5 (ln ratio 0.40–0.47 at A = 408–630), 1.66 ± 0.08 at A = 759 on the GPU, and 2.0 ± 0.4 at A = 693 from fresh
  soups (S3; B). It is not explained. (*Preliminary*, not in the ledger: one line of the theory effort, checked
  by one critic, shows that the two kinds of face have equal numbers of orbits, which would make the factor a
  boundary effect.)
- *Still memoryless.* Vertex-centred O_h soups wait exponentially at R = 36, 38, 40 (GP3; B) and cube-centred
  ones at R = 43 (GP5, above). Runs from deterministic cube-like O_h seeds (cubes with surface orbits removed,
  hollow cubes) wait like soups: at hull radius 31–38, 1,248 plateaus have mean T/τ = 0.99 and CV 1.02 against
  3,261 soup plateaus (two-sample KS p = 0.98), with no correlation between consecutive plateaus (L1; B); at
  vertex-centred R = 40, 3,857 lineages wait exponentially on the plateaus at 40, 38, 36 (mean T/τ 0.99, 1.01,
  0.98), with a weak correlation between the first two (Spearman ρ = +0.049) traced to lineages that peel early
  (GP6; B−).

*Interpretation, and what is only preliminary.* In a symmetric state the cells of an orbit share one state, so a
face has about A/6 independent cells and its fluctuation to emptiness is correspondingly cheaper; in addition
cells on mirror planes are depleted (P7, Section 4). *Preliminary* **[measured → conjecture]** (S4; C): across
symmetry groups and on tori without faces, a symmetric system lives about as long as an asymmetric one of c
times its fundamental domain's volume, c ≈ 1.5–3.5. *Preliminary* **[measured]** (SW3; C, one run by one
examiner): octahedral faces cut by a single mirror plane cost 0.1026 ± 0.0003 per cell at A = 84–135, 0.47 of
the asymmetric value, and the first face to die is a mirror-fixed one in more than 99.9% of replicas.

### 5.6 The cubes, and the forecasts that were made in advance

**The side-16 cube.** **[measured]** (C2; B: schedule and summary re-derived from the committed event log; the
run itself, several days on one core, was not repeated) The cube of side 16 sat at hull radius 42 (vertex-centred,
A = 693) until generation 2,362,434,048, then at 40 until 2,886,100,480, and ended as a 96-cell still life at
2,919,617,676:

| hull radius R (face cells A) | 42 (693) | 40 (630) | 38 (570) | 36 (513) | 34 (459) | 32 (408) | 30 and below |
|---|---|---|---|---|---|---|---|
| generations spent | 2.362 × 10⁹ | 5.237 × 10⁸ | 3.08 × 10⁷ | 2.71 × 10⁶ | 7,040 | 27,712 | 1,792 in all |

Table 4. Residence schedule of the side-16 cube (`research/data/cube16_events.jsonl`; events sampled every 64
generations).

**Forecasts.** Several quantities in this section were forecast in files committed before the outcome was known.
Table 5 lists every one we found, with its score.

| # | forecast (where committed) | outcome | score |
|---|---|---|---|
| 1 | Side-16 lifetime: mean 2.4 × 10⁸, 90% interval 3.9 × 10⁷–6.3 × 10⁸, from a proportional "effective area" fit to symmetric soups (`research/peeling/cube_lifetime.csv`) | 2,919,617,676 | **failed**, low by a factor 12 (C3; B) |
| 2 | Side-16 first face death: median 2.2 × 10⁹, 90% 1.50–5.2 × 10⁹, from perturbed copies of the running cube's state with restarts; committed about two hours before the event (`research/fluct/PREDICTIONS.md`, commit 2e72d57) | 2,362,434,048 | held, at about the 58th percentile (C4; B for the commit time and the arithmetic; the wall-clock time of the event itself is grade C) |
| 3 | Second face death, from fits to symmetric soups only: median 2.60 × 10⁹, 90% 2.531–2.89 × 10⁹ | 2,886,100,480 | held, at the 95th percentile (C5; B) |
| 4 | Second face death, from 64 copies of the cube's state (τ = 8.2 × 10⁷): 90% 2.529–2.78 × 10⁹ | 2,886,100,480 | **missed** (C5; B) |
| 5 | Cube-centred O_h soups at A = 828 (the first plateau of a side-17 cube): ln τ = 24.0 ± 0.4 | 24.175 ± 0.072 | held (C9, GP2; B, B−) |
| 6 | O_h soups at A = 759: cube-centred 21.8 ± 0.2, vertex-centred 22.3 ± 0.4 (`research/gpu/PREDICTIONS.md`) | 21.903 ± 0.031, 22.409 ± 0.040 | held (GP2; B−) |
| 7 | Slab 6 × 7 × 8 with firewalls resolved: ln τ_face = 26.30 ± 0.15, ln τ_fw = 27.0 ± 0.4, firewall-first share 10–30% | 26.405 ± 0.104, 26.87 ± 0.19, 24% | held, all three (GP8; B) |
| 8 | Slab 6 × 6 × 8: share 0.5–4%; ln τ_face = 22.49 ± 0.07 | 2.1%; 22.568 ± 0.041 | share held; face value missed by 0.01 (GP8; B) |
| 9 | At equal area the lifetime of a periodic face does not depend on its width ("area only"; 4 × 9 against 6 × 6: 0.00 ± 0.10) | −0.196 ± 0.059 | **missed** (GP9; A + B) |
| 10 | The lifetime of a periodic face is a function of area and shortest loop alone, with stated sizes (`research/shape/PREDICTIONS.md`) | ordering held; "alone" refuted at A = 60; sizes missed | **partly failed** (SH1, SH2; A) |
| 11 | Six candidate laws in area and shortest loop, parameters fixed before the census (`research/shape2/PREDICTIONS.md`, commit 80906fe) | none fits at A = 48, 60 or 72 | **all refuted** (SH5; A) |
| 12 | Six layers of the rule over coin flips: ln τ = 7.40, 9.94 for slab faces of A = 36, 48 (Section 6) | 7.397 ± 0.009, 9.945 ± 0.014 | held (SW2; B) |
| 13 | Depth of rule needed over noise for octahedral faces: three layers | three layers miss by 0.3–1.0 in ln τ; four to five are needed | **missed** (recorded in `research/theory/exponent.md`) |

Table 5. Forecasts committed before their outcomes. Forecasts about other rules and about results graded C are
omitted; several of those also failed (Section 9).

**What the failure of forecast 1 showed.** The forecast multiplied a fit made on cube-centred symmetric soups
with faces of at most 513 cells by a fixed factor for the vertex-centred hull. Both steps were wrong in the same
direction: the cost per cell of a symmetric face rises with its size (Table 3), and the data on vertex-centred
hulls then reached only A = 408. **[measured]** Against fresh vertex-centred soups in the same hull
(τ = 7.1 × 10⁸, 45 deaths) the cube's first plateau is 3.3 means (probability 0.036 for one exponential wait);
radius 42 is an ordinary size (C8; pooled value re-derived, B).

**An open question, not a finding.** **[measured]** The cube stayed 5.24 × 10⁸ generations at R = 40, which is
7.4 times the mean of an ensemble that pools fresh soups with copies of the cube (probability 6 × 10⁻⁴ for one
exponential wait; C5; B), or 6.1 times the fresh-soup mean 8.63 × 10⁷ (probability 0.002). A count over the
sixteen largest plateaus of cubes 13–16 finds three longer than four means (C6; B for the arithmetic), but that
statistic was chosen after the side-16 plateaus suggested it; without side 16 it gives P ≈ 0.18, and it is not
evidence. Cube-like seeds and soups are memoryless at every size tested up to R = 40 (L1, GP6). So either the
side-16 cube was lucky at about the 1% level, or its own lineage carries something that ensembles of similar
states do not; the cube's own lineage at R ≥ 42 has not been, and at present cannot be, replicated.

**Extrapolations** **[conjecture]**. A side-17 cube's first plateau has mean about 3.2 × 10¹⁰ generations if the
soup value at A = 828 applies to it (C9); the cube has not been run. The 2012 run from a side-19 cube, which was
never finished because its hull wrapped the 2012 torus (R8; A), would last 10¹³–10¹⁴ generations properly
confined, on fits far outside any data (C10). An asymmetric soup filling the side-13 hull (A = 459) would hold
each face for about 10⁴¹ generations on the fit of Section 5.2 extrapolated fivefold in area (F13); this cannot
be tested, and Sections 5.2 and 7 show that fit is not the right law for octahedral faces.

## 6. The exponent is made in a boundary layer over noise

The face law's exponent could depend on the deterministic chaos beneath the face in some detailed way. It does
not, at the precision reached. Take a face, keep the rule on its top w layers, and replace every cell beneath
them, at every generation, by an independent coin flip. Measure the face's lifetime in this model as in
Section 5.2, censoring repeating states.

**[measured]** (X1; A: an adversarial reviewer's own steppers, bit-identical to the reference implementation, and
own seeds)

- *Periodic slab faces.* With w = 5 the model's ln τ_face equals the deterministic slab's within 0.015 at A = 27,
  48 and 60, and is +0.02 ± 0.04 at A = 75 (where the deterministic slab is 15.660 ± 0.027). With w = 4 it is
  0.06–0.07 too high.
- *Octahedral faces.* Models with four or five layers agree with the deterministic octahedron within 0.05 at
  A = 45, 63, 84 (deterministic values 9.823, 13.644, 18.148 ± 0.028), but deeper models (w = 6, 8) settle
  0.03–0.04 *below* the deterministic value, 4–5 standard errors at A = 45: there is a small systematic offset,
  and the agreement at w = 4 is partly a crossing. That four to five layers suffice for octahedra was noticed
  after the runs (forecast 13 of Table 5 had said three).

**[measured]** (SW2; B: run by an examiner who had not made the prediction) With six layers over fair coins, slab
faces of A = 36 and 48 give 7.397 ± 0.009 and 9.945 ± 0.014 against the deterministic 7.398 and 9.936.

**[measured]** (X2; A: independent numpy code against the study's driver) The same holds in the two-dimensional
analogue of Section 9: eight rows of the rule over coin flips give ln τ_edge = 5.654, 7.425, 9.136 against the
deterministic strips' 5.644, 7.407, 9.142 at edge lengths L = 12, 16, 20, and are 0.067 ± 0.027 high at L = 24;
the density of the coins hardly matters.

*Preliminary* (X3; C): the noise-driven models can settle. The six faces of one cube lying on the face are a
fixed point whatever the coins do once w ≥ 4–5, and a replica in such a state never dies; uncensored, one model
reads 6.94 where the censored value is 6.54.

*What this does and does not establish.* At sizes A ≤ 84 and precisions of 0.01–0.05 in ln τ, the deterministic
bulk enters the face law only as a source of noise produced within five or six layers. The question "why about
0.21 per cell" is thereby reduced to one about a probabilistic cellular automaton of finite depth, for which
lifetimes can be sampled without the bulk and computed exactly at small sizes. It is not shown that the
reduction survives at larger A, where the cost per cell is still drifting (Table 2), and the offset for
octahedral faces is unexplained. No theorem is claimed. Figures of the study (not re-examined for this draft):
`research/figures/exponent_gump.png`, `research/figures/exponent_hierarchy.png`.

## 7. The lifetime of a periodic face depends on its shape

Slab faces are tori. If the face law were a law of area, tori of equal area would have equal lifetimes. They do
not.

### 7.1 Width

**[measured]** (GP9; A for the pair at A = 72, which an independent CPU run with a different stepper reproduces
as −0.344 ± 0.020; B for the rest, recomputed twice from the per-life data; no second GPU run) Fourteen slabs
s × M × 8 with rectangular period lattices, every life ended at its first event, the firewall channel counted
separately:

| short side s | ln τ_face at face area A (share of lives ended by a firewall) | slope within the family |
|---:|---|---|
| 3 | 11.082 (54; 13%), 14.621 ± 0.003 (72; 87%), 18.046 ± 0.011 (90; 99.6%) | 0.1966, then 0.1902: curved |
| 4 | 12.486 (60), 14.971 ± 0.002 (72), 17.465 ± 0.005 (84), 19.943 ± 0.018 (96), 22.373 ± 0.042 (108; 99.2%) | 0.2072 ± 0.0001 |
| 5 | 15.661 ± 0.003 (75), 18.786 ± 0.011 (90), 21.890 ± 0.040 (105), 25.046 ± 0.073 (120; 92%) | 0.2082 ± 0.0006 |
| 6 | 22.568 ± 0.041 (108; 2%), 26.405 ± 0.104 (126; 24%) | 0.213 ± 0.006 |

Table 6. Periodic slab faces by width (`research/data/gpu_facelaw/`;
`python3 research/audit/gpu_pr16_lead_check.py research/data/gpu_facelaw`).

- At equal area the narrower face dies sooner: 3 × 8 against 4 × 6 (A = 72), −0.349 ± 0.004; 3 × 10 against 5 × 6
  (A = 90), −0.740 ± 0.016; 4 × 9 against 6 × 6 (A = 108), −0.196 ± 0.059. The same slab in both orientations
  agrees to −0.002 ± 0.003. The face hazard is flat in the age of the life from about 200 generations on in
  every slab, including those where firewalls end 99% of lives.
- For s = 4, 5, 6 the data do not require a width-dependent cost per cell: one slope 0.2072 ± 0.0001 with
  intercepts 0.053, 0.121, 0.203 fits (χ² = 8.4 on 8), and so does ln τ = a + 0.2117·A − 0.054·M with M the long
  side (χ² = 5.6 on 9). The two cannot be told apart with these data. Either way the correction to an area law is
  linear in a side length. Whether the cost per cell of a wide periodic face is 0.2072 or 0.2117 is **not
  decided**.
- An area-only fit over the slabs with s ≥ 4 gives 0.2085 per cell with χ² = 512 on 10: wider slabs were also the
  larger ones, so mixing widths inflates the slope. The 0.2088 of Section 5.2 is a slope of that kind. (An
  independent series at A = 27–75 with widths 3 to 5 gives 0.2121 ± 0.0004 for the same reason;
  `research/audit/REVIEW-class.md` §3.1.)
- Width 3 is cheaper per cell and curved; its last point is also the one where 99.6% of lives end in a firewall,
  so curvature and proximity to the firewall channel are not separated there.

### 7.2 The shortest way round

For rectangular tori "width" and "shortest closed loop" are the same thing. Twisting the period lattice separates
them: the lattice generated by (a, k) and (0, b) in the in-plane cube coordinates has A = 3ab cells for every k,
and its closed loops have squared lengths x² + xy + y² in units of the in-plane lattice vector (the two in-plane
axes are at 60°).

**[measured]** (SH1; A for five tori rerun with an independent bit-sliced stepper and fixed seeds, B for the other
presentations) At A = 72 the lifetime rises with the shortest loop, and different shapes with the same shortest
loop agree (χ² = 1.1 on 4 over distinct shapes):

| shortest loop² (length) | tori at A = 72 | ln τ_face | independent rerun |
|---|---|---|---|
| 9 (3.00) | 3 × 8; (8,2),(0,3) | 14.613 ± 0.010 | 14.614 ± 0.014 |
| 12 (3.46) | (4,4),(0,6); (2,5),(0,12) | 14.877 ± 0.010 | 14.866 ± 0.016 |
| 13 (3.61) | (4,3),(0,6), three presentations | 14.921 ± 0.008 | |
| 16 (4.00) | 4 × 6 (two presentations); (6,1),(0,4); (6,3),(0,4) | 14.973 ± 0.007 | 14.966 ± 0.008 |
| 19 (4.36) | (2,3),(0,12) | 15.011 ± 0.014 | 15.020 ± 0.017 |
| 21 (4.58) | (4,1),(0,6) | 15.066 ± 0.014 | 15.035 ± 0.009 |

Table 7. Twisted periodic faces of 72 cells (`research/shape/README.md`;
`python3 research/audit/shape_lead_check.py`). The two runs at loop² 21 differ by 1.9 standard errors; pooled,
15.043 ± 0.007.

Two other candidate variables are refuted by the same data: distance counted in lattice steps (the tori with
loop² 12 and 13 have step-distance 4, like 4 × 6, and lie 0.096 ± 0.012 and 0.052 ± 0.011 below it), and
proneness to transverse firewalls (it predicted those tori above 4 × 6). Tori with no observed firewall channel
lie on the same curve as tori with 5% and 87% firewall endings.

**[measured]** (SH2; A: four runs, two codes) The shortest loop is not the only variable. At A = 60 two tori with
the same shortest loop (squared 16) and second-shortest loops squared 19 and 21 differ by 0.0142 ± 0.0019 in
ln τ_face (χ² = 4.7 on 3 over the four runs; the first published value was 0.019 ± 0.004). At A = 48 two tori
with shortest loop² 12 and second loop² 16 and 19 differ by 0.0151 ± 0.0017. In both pairs the face with the
shorter second loop dies sooner. Two pairs do not identify the variable, and it has not been found.

### 7.3 Every torus of a given area

**[measured]** (SH3; A for A = 48 → 60, where an independent stepper gives 0.1144, 0.1415, 0.1922, 0.2076,
0.2127; B for 60 → 72, one code) Measuring every class of period lattice at A = 48 and 60 and five more at
A = 72 gives a cost per cell that depends on the shortest loop and saturates:

| shortest loop² | 3 | 4 | 7 | 12 | 13 | 16 |
|---|---|---|---|---|---|---|
| d ln τ_face/dA, A = 48 → 60 | 0.1148 ± 0.0003 | 0.1414 ± 0.0003 | 0.1918 ± 0.0003 | 0.2073 ± 0.0002 | 0.2090 ± 0.0003 | 0.2125 ± 0.0003 |
| d ln τ_face/dA, A = 60 → 72 | 0.1107 ± 0.0004 | 0.1346 ± 0.0010 | 0.1872 ± 0.0010 | 0.2049 ± 0.0009 | 0.2061 ± 0.0007 | 0.2076 ± 0.0006 |

Table 8. Cost per cell of a periodic face by shortest loop (`research/shape2/README.md`;
`python3 research/audit/shape2_lead_check.py`). The slopes compare different lattices with equal shortest loop,
not one torus grown. The loop² 4 lifetimes carry a tie-resolution bias of about −0.018 in ln τ (the slope is not
affected), and the loop² 4 tori are multigraphs (a cell counts one neighbour twice), so only loop² 3 is strictly
"the same automaton on a narrow cylinder".

A face only √3 cells around still lives a time exponential in its area, at about half the wide-face cost per
cell; on these thin tori the hazard is flat in age and face death is permanent, so they are the same kind of
object.

**[measured]** (SH4; A, two codes, but only four lattices at A = 48) Above loop² 12 the shortest loop no longer
orders the classes at A = 48: the four classes with loop² 12, 12, 13, 16 span 0.016, and the 4 × 4 torus
(loop² 16) lies 0.0135 ± 0.0021 *below* a loop² 12 class. At A = 60 the step from loop² 12 to 16 is +0.056 to
+0.063, and at A = 72 it is about +0.10 (Table 7). The shape term grows with the area.

**[measured; a refutation]** (SH5; A: χ² recomputed with separate code on separate runs) Six candidate laws
expressing ln τ_face through the area and the shortest loop (or a sum over loops), with parameters fixed before
the census, all fail at each of A = 48, 60 and 72. The one that appeared to pass at A = 60 on the census's own
run (χ² = 5.4 on 5) fails on independent values (22.7 on 5) and on all runs pooled (45.4 on 5).

**Reading** **[conjecture]**. ln τ_face = c·A + (a term set by how the face closes on itself); the second term is
not small, not constant in A, and not a function of one length. Two consequences are firm regardless. First, no
family of periodic faces measured so far isolates the constant c of an unwrapped flat face to better than about
±0.004: the families give 0.205 to 0.2125 at these sizes, and octahedral faces give 0.215–0.221 (Table 2), with
nothing yet connecting the two. Second, the thin tori are quasi-one-dimensional systems with their own costs per
cell (0.11, 0.14, 0.19), which may be within reach of a transfer-matrix calculation.

Figure 3 (placeholder; does not exist): *ln τ_face at A = 72 against shortest loop length (Table 7), with the
A = 60 and A = 48 classes offset, and the two equal-shortest-loop pairs marked.* Figure 4 (placeholder): *cost
per cell against shortest loop² (Table 8).*

## 8. What is left: debris and clockwork

When the last chaos has gone a seed leaves still lifes and oscillators (or nothing: the side-15 cube ends
extinct).

**Still lifes.** **[proved, by exhaustive search]** (Z1; A + B) The smallest still lifes have 6 cells, and there
are exactly four up to symmetry; they include the six faces of a single cube (each sees exactly 4 others) and the
six-cell hexagon of one kagome layer. **[proved, exhaustive]** (Z2; B for these sizes) The numbers of strict
still lifes with n = 6, …, 13 cells are 4, 2, 7, 9, 27, 45, 228, 851. *Preliminary* (C): 3,388, 12,255, 47,578
for n = 14, 15, 16.

**Period 2.** **[proved, exhaustive]** (Z3; B for unions up to 11) The smallest period-2 oscillator has a union
of 9 cells; there are 3, 6 and 4 classes with unions of 9, 10 and 11 cells. *Preliminary* (C): all of these are
"hinge flips", in which live faces swing 90° about a shared edge; no period-3 oscillator has union ≤ 12 and the
smallest has union exactly 13 (Z4).

**Why anything has period above 2.** By Theorem 5 every oscillator of period ≥ 3 has cells that are overcrowded
after having been alive two generations earlier, and over a period the drive at those cells balances the
dissipation exactly; this was verified on all 329 catalogued objects of period ≥ 3.

**Long periods are short loops closed by a symmetry.** *Preliminary* **[measured]** (Z5; C): soups in small
octahedra leave oscillators of periods 1–16, 20, 22, 48 and 66. The longest has a simple anatomy.

**Twist lemma [proved]** (ledger T7; A). Let a closed box (a diagonal hull) have symmetry group G; G commutes
with the box's map F. Let a cycle of period P first return to a symmetric image of itself after L generations,
F^L(x) = g·x with g ∈ G. Then P = m·L, where m is the order of g acting on the cycle; for subgroups of O_h,
m ∈ {1, 2, 3, 4, 6}; and every cell fixed by g has period dividing L.
*Proof.* Let Γ be the subgroup of G preserving the cycle. Sending g ∈ Γ to the phase shift k(g) with
g·x₀ = F^{k(g)}(x₀) is a homomorphism Γ → Z_P whose kernel is the stabiliser of x₀, so its image is cyclic, of
order m say, generated by the shift L = P/m. A cell fixed by g has the same state at times t and t + L. ∎
In the terminology of Life catalogues, L is the oscillator's "mod" [LW-Mod]; there period/mod ∈ {1, 2, 4} on the
square grid and {1, 2, 3, 6} on hexagonal and triangular grids, and the lemma is that statement for boxes of
this lattice.

**[proved, by direct computation; two independent steppers]** (Z6; A) The period-66 oscillator P66.27a is a plate
three kagome layers thick whose diagonal hull has 45 cells, every one of them live in some phase; its phase at
t + 33 is the mirror image of its phase at t. Forty cells have period 66, the three cells on the mirror plane
have period 33, two are always live; no cell has period 2, 3, 6, 11 or 22. It is a 33-step loop closed by a
reflection, not a product of gears.

**[measured]** (Z7; A) Every twist order the lemma allows occurs: C48.24a has period 48 = 6 × 8 (every 8
generations the plate reappears turned 60° about a body diagonal and inverted: a screw), C36.33a 36 = 4 × 9,
C12.43a 12 = 6 × 2, C40.24a 40 = 2 × 20, P15.22a 15 = 3 × 5, P48.34a 48 = 2 × 24. **[measured]** (Z8; A + B) In a
census of 9,700 oscillators of period ≥ 3 found in 402 small closed boxes, 249 are *compound*: no cell has the
full period, and they are two or three sub-clocks of coprime periods on a shared frame with nothing passing
between them (for example C44.26a, periods 4 and 11); Life terminology calls such periods trivial [LW-NT].
**[measured]** (Z9; B + A) Among the remaining objects, twisted loops are a steady 3–8% at every loop length
(295 of 9,278 with L ≥ 3; 30 of 670 with L ≥ 7; 9 of 120 with L ≥ 12; 5 of 66 with L ≥ 16), so the twist
multiplies ordinary loops rather than selecting long ones; the longest untwisted loop found is C35.29a (L = 35).
*Preliminary* (Z10; C): P66.27a is reached from 4.1 × 10⁻⁴ of the random states of its own box, and single-cell
perturbations destroy it more often than not. No object found carries or gates a signal.

Figure 5 (placeholder; does not exist): *P66.27a at phases 0 and 33, layer by layer.* A text rendering is
produced by `engine/target/release/gump show --cells research/clockwork/views/P66.27a.cells --orbit`.

## 9. The rule's neighbourhood: other rules, a 2D analogue, other lattices

**Rule space on the same lattice.** **[measured]** (Q1; B, re-derived from the committed table
`research/phase/rules.csv`; the survey itself was not re-run) Among the 960 rules with birth set B ⊆ {4,…,7}
non-empty and survival set S ⊆ {2,…,7}, 421 are chaotic on a 24³ torus, but only 146 have a median lifetime of
at least 10³ generations in an octahedral vessel of radius 10 (16 soups each), 142 of them with 4 ∈ B. Gump's
median there is 3,420, and B45/S345 is one of 50 minimal elements of the long-lived set: removing any one count
collapses it (B4/S345: 104; B5/S345: 21; B45/S45: 20; B45/S35: 22; B45/S34: 36 generations). **[measured]** (Q2;
B) Adding survival at 2 or at 7 extends the median at least 29-fold (those medians sit at the survey's cap of
10⁵). **[measured]** (Q3; B) For B45/S3457 the medians are 79, 3.5 × 10⁴ and above 10⁶ at radius 6, 8 and 10,
against 28, 254 and 3,420 for gump. **[measured]** (K4; B, an adversarial review's own code) The capped threshold
with the cap one higher, B456/S3456, has a slab face law within 0.2 in ln τ of gump's at five sizes (area-only
slopes 0.2156 ± 0.0005 and 0.2121 ± 0.0004 on the same mixed-width faces). *Preliminary* (Q4; C): rules with
birth at 3 are not confined and invade vacuum across {111} planes, as the hypothesis of Theorem 2 leads one to
expect.

**A two-dimensional analogue.** **[measured]** (G1; A for the central law: an independent stepper at L = 12–24
gives slope 0.42) On the square lattice with the range-2 cross neighbourhood (±1,0), (±2,0), (0,±1), (0,±2), the
rule B34/S234 ("alive next iff n + x ≥ 3, except that n ≥ 5 dies") is gump's construction one dimension down. It
has steady chaos at density 0.472, and in strips 16 deep and periodic along the edge a whole edge row dies after
a memoryless wait with

$$\ln \tau_{\rm edge} = 0.73 + 0.416\,L, \qquad L = 12\text{–}36,$$

τ_edge from 286 to 5.8 × 10⁶ generations. *Preliminary* (G2; C: proved in the study and brute-force checked there,
re-derived by a second reader by hand in part only): it is confined to its bounding box, three dead rows are a
firewall, the threshold lemma holds with exceptions exactly at overcrowded cells, and no finite set is sealed.
*Preliminary* **[measured]** (G3, G4, SW4; C): a mirror perpendicular to the edge multiplies the slope by 0.42
and full square symmetry by 0.50, but a forecast that symmetries fixing no edge cost nothing failed for four-fold
rotation; no capped-threshold rule on the Moore neighbourhood sustains confined chaos; an edge with a two-cell
dead notch has slope 0.346 against 0.412 for the intact edge. That the 2D slope 0.416 is twice the periodic-face
slope of the 3D rule to three figures has no known reason, and given Section 7 neither number is an asymptotic
constant.

**Other lattices.** **[proved]** (ledger K1 of the class study; A) Confinement is a property of half-spaces
(Section 3). **[measured]** (K4; B) On the face-centred cubic lattice with 12 neighbours, B45/S345 has a
memoryless slab face law with slope 0.181 ± 0.001 per face cell. The variant of the present rule with
edge-sharing coplanar neighbours is likewise confined (to a box), chaotic, and dies a wall at a time, and is not
treated here. A study of which capped-threshold rules on which lattices behave this way was reviewed
adversarially; its theorems stand (K4; B), and its measured regularity is that, given confinement, no finite
sealed set, no immortal wall and a chaotic bulk, the outer layer dies as a whole after a memoryless wait roughly
exponential in its area (42 of 50 lattice–cap pairs by a scoring rule fixed in advance). *Preliminary* (C): on a
honeycomb-based lattice the wall law is concave rather than linear, and on a bond lattice boxes outlive the
forecast from the slab law by a factor of about 10⁶ because adjacent walls hold each other up along their edges.
Nothing known predicts which rules are chaotic or how strong the law is.

Figure: `research/figures/phase_rulemap.png` (the 960-rule survey), `research/figures/toy2d_law.png` (the 2D
edge law).

## 10. What is proved, what is conditional, what is open

### 10.1 Proved without conditions

Theorems 1–6 and Proposition 7 of Section 3; the half-space criterion for confinement; the twist lemma; the
exhaustive enumerations of Section 8 within their stated sizes; the anatomy of P66.27a. None of these says
anything about lifetimes beyond the trivial bound that a seed with a hull of N cells is periodic within 2^N
generations, which is exponential in the hull's *volume*.

### 10.2 Proved under a condition

**(a) A conditional area law for gump** **[proved, conditional]** (SW5; A: read by a critic and then by an
independent second reader who recomputed every step with separate code, including an exact check on all 2²²
states of a small vessel). For a family of faces of area A, pool over the living ensemble the one-step
transitions of the face population Z: exposure N(z), deaths D(z), transitions F(z, z′), table T̄ = F/N with
T̄(z, 0) = D(z)/N(z), and M_k(s) = Σ_{k′ ≥ 0} T̄(k, k′) e^{−s(k′ − k)}. *Hazard identity:* the number of deaths
equals the direct deaths from above a low set, plus the entry flux into the low set weighted by the committor of
the pooled table, plus a boundary term at the start of the observation window minus one at its end; no Markov
property of Z is assumed (and Z is not Markov). *Conditional law:* suppose there are θ₀, κ > 0 and k₀, ε, c
independent of A such that, with K = ⌈κA⌉, (R) M_k(θ₀) ≤ 1 for every visited row k₀ ≤ k < K; (Φ) the entry term
is at most e^{εA}; and (W) the window term is controlled (the window starts above the low set, or the pooled law
is quasi-stationary with censoring at most c times the hazard and a stated bound on the low-set weight). Then the
death rate satisfies

$$\bar h_A \le 2e^{\theta_0 k_0}\, e^{-(\theta_0\kappa - \varepsilon)A}, \qquad\text{so}\qquad
\liminf_{A\to\infty} \tfrac1A \ln \tau_A \ge \theta_0\kappa - \varepsilon .$$

(`research/theory/swarm/audit/AUDIT-path.md`, §§0–2; the statement first written, from "R and R⁺", was not
sufficient and is replaced by this one.) **[measured]** Hypothesis (R) holds with θ₀ = 0.40, κ = 0.35, k₀ = 5 on
the four measured octahedral tables, A = 30–84 (block minima of the local roots 0.403–0.426; at A = 30 the margin
is 0.003). It is a statement
about the rule known only from those samples; it is not derived, and testing it at a new size costs as much as
measuring τ there. With these values the theorem accounts for 0.13–0.14 of the roughly 0.21 per cell. A companion
structure lemma **[proved]** (same audit, Proposition S′): every permanent loss of cells to the largest dead
sealed set is the extinction, at one instant, of a set that is minimal among the sealed sets of what was not yet
sealed.

**(b) An exactly solvable deterministic relative of the 2D rule** **[proved, conditional]** (SW1; A: audited line
by line by a reader who was neither author nor critic, with its own enumerations; an independent simulation
reproduces the exact values). Let 𝒜(L) be the automaton on cells (x, j), x on a ring of L columns, j = 0, 1, 2,
…, in which row 0 follows B34/S234 on the range-2 cross with nothing above it and every other row copies the row
two below; the initial state is any row 0 above independent fair bits, each written into two consecutive rows.
The map is deterministic; the only randomness is the initial tape. Then row 0 is exactly a Markov chain, the edge
dies after an exactly geometric wait from its quasi-stationary law, with mean τ_L ≤ 3·8^L, and τ_L is at least
the lifetime of five-parent oriented site percolation of density ½ on the ring. *If* (F1) the critical density of
two-parent oriented site percolation is below ¾ [BBS94, p_c ≤ 0.7491, computer-assisted, known here only
second-hand; a second route through L95 at exactly ¾] *and* (F2) supercritical oriented site percolation on a
cylinder of circumference n survives for a time e^{cn} [HS22, Cor. 4.8, whose printed proof is a sketch], *then*
e^{cL} ≤ τ_L ≤ 3·8^L for all large L. **[exact]** ln τ_L = 6.5319, 9.4733, 12.2492, 13.5946 at L = 8, 12, 16, 18.
This is the simplest system with the 2D rule's own edge in which "memoryless and exponential in the length" is a
theorem. It is not self-generated randomness: the edge consumes fresh bits for ever and the bulk does not process
them. The audit also shows that the comparison method stops short of the rule's own bulk statistics and of a gump
face.

### 10.3 Open

1. **Why area.** No proof that the wait is exponential in the face's area exists for gump, for the 2D analogue in
   a vessel run by the rule, or for the finite-depth noise-driven models of Section 6. A dedicated theory effort
   by several independent lines ended without one.
2. **The constant.** It is not derived from the rule. It is also not yet *measured* as an asymptotic constant:
   octahedral slopes are still rising at A = 135; periodic faces carry a wrap-around term (Section 7); no flat
   face without periodic identification or rim has been measured. One conjectured value exists, a quasi-potential
   of a measured one-step table with a stated continuation, 0.2191 per cell at A = 84 **[conjecture]**.
3. **The second shape variable** of a periodic face, and why octahedral faces are tougher than periodic ones.
4. **Symmetric faces:** the asymptotic slope (is it the asymmetric slope divided by 6?), the factor ≈ 1.5 between
   vertex- and cube-centred hulls, and the excess length of the side-16 cube's plateaus.
5. **Infinite volume.** Whether the chaotic state is stable or only metastable on the infinite lattice; whether
   one- and two-layer slabs cannot sustain chaos (reduced in `research/theory/thickness.md` §4 to a percolation
   statement, unproved).
6. **Hypothesis (R)** of Section 10.2(a) from the rule.
7. **Fauna:** periods beyond 66; whether any oscillator can pass a signal.
8. **Rule space:** what makes a capped threshold chaotic at a given cap; how strong the wall law is.

## 11. What is new here and what is not

This section relies entirely on the project's prior-art survey (`research/PRIOR-ART.md`, two search passes on
2026-11-13, and the theory effort's library, `research/theory/swarm/library/shelf.md`). That survey was made by
web search with a lossy fetcher; several key sources could not be opened (notably the review [TL08]); and
"not found" below means not found by that survey, nothing stronger.

| result | nearest known work recorded | judgment |
|---|---|---|
| The automaton itself (faces of the cubic honeycomb, this neighbourhood) | No automaton on this vertex set found in two searches. Near misses: 12-neighbour sub-neighbourhoods of the Moore neighbourhood (the fcc lattice) on LifeWiki's cubic-honeycomb page [LW-CH]; Life on kagome and other Archimedean lattices, in 2D [G]; the same lattice studied as an antiferromagnet, not a cellular automaton [arXiv:1510.05924] | Appears new as a cellular automaton "on this lattice" (not "with 12 neighbours"). Not a result in itself |
| Confinement to the diagonal hull, no spaceships (Thm 2); firewalls (Thm 3); kagome sub-automata (Thm 4) | Eppstein [E09]: no births on 1–3 neighbours implies confinement to the bounding box for Life-like rules; a bounding-diamond argument of the same shape for some B3 rules. LifeWiki [LW-OT]: rules with lowest birth ≥ 4 never grow beyond their bounding box | **New instances of a known principle.** The method is not new. The {111} half-space on this lattice, the octahedral hull that only shrinks, and the three-layer firewall were not found stated. (The survey's second pass could not re-read [E09]'s body) |
| Threshold lemma with the exact identity ΔE = D − Q (Thm 5) | Period-two theorem and energy for symmetric threshold networks [GO80, GO81, GFP85], read only through [KMMK11, GMRS23] | **Standard theorem, applied.** The observation that a capped rule is a symmetric threshold network except at overcrowded cells, with an exact drive term there, was not found; it is elementary. [citation needed: whether energy identities with a drive term for capped or bi-threshold rules are in Goles–Martínez or later work] |
| No finite sealed set in ≥ 3 layers; finite sealed sets in 1 and 2 (Thm 6) | Nothing recorded | Appears new; elementary; a new instance of a "no local absorbing set" statement |
| Memoryless collapse with mean lifetime exponential in size (Section 5.2) | Supertransients [CK88, WS03, HKTP10, TL08] and stable chaos [PT09]: numerical only. [HKTP10] reports τ(L) = exp(AL + B), Poisson statistics, and collapse only with non-periodic boundaries through boundary layers of fixed thickness. For stochastic monotone systems the analogue is a theorem: the finite contact process [DL88, DS88, M93, M99, MMVY12]; exact exponential law from a quasi-stationary distribution [MV12] | **A new instance of a known phenomenon.** Possibly new within it: (i) confinement and firewall are theorems, so collapse proceeds by irreversible layer events that can be timed one by one; (ii) the exponent is set by the area of one face of a three-dimensional vessel, not the volume; (iii) a deterministic cellular automaton with an absorbing state (none in the sources read) |
| Death as the end of the quasi-stationary tail, measured to one cell (Section 5.3) | QSD theory [MV12, DS65]; large deviations in cellular automata exist [BGPV19] but not for a density tail used as an extinction-rate predictor | The structure is **standard**; the measurement down to k = 1, with the death rate as the next point, **was not found** |
| The exponent is made in five or six layers over independent noise (Section 6) | Dice models of deterministic networks with lifetime e^{cn} (monotone) [CD11, MV10]; probabilistic cellular automata [LMS90, MST19]; boundary layers of fixed thickness in [HKTP10] | **Appears new** as a quantitative statement (agreement to 0.015 in ln τ). The idea that boundaries of fixed thickness control the collapse is in [HKTP10]; whether replacing the bulk by noise has been tested for supertransients is not known to us (the review [TL08] is unread) |
| Symmetric initial conditions die exponentially sooner (Section 5.5) | Nothing found on lifetimes. Life lexicon: symmetric soups produce different objects [LL-soup]; symmetric soup censuses exist | **Not found; appears new as a quantified result.** Conceptually close to standard symmetry reduction, so "new" should be worded "not found" |
| Lifetime of a periodic face depends on its shape at fixed area (Section 7) | Open systems with holes of equal measure and different escape rates, ordered by recurrence time [BY08]; escape rate = measure of the hole times one minus a return factor [KL08]; [HKTP10] on the role of boundary conditions | **Not found; probably new as a measurement**, and at present a negative result (no law fits). The analogy with [BY08] is ours and is untested |
| Period = twist × loop; statistics of twisted oscillators (Section 8) | Period and "mod" in Life catalogues, including thirds and sixths on hexagonal and triangular grids [LW-Mod]; trivial versus non-trivial oscillators [LW-NT] | The lemma is a **re-expression of period/mod**. The three-dimensional screw twists and the statistics were not found |
| Conditional area law; hazard identity (Section 10.2a) | Not surveyed. [citation needed: committor and flux identities in transition-path theory and in QSD theory; the project's library has none] | Unknown. The identity is of a standard kind; its use without a Markov property, and the reduction of the area law to a one-step hypothesis on a pooled table, may or may not be known |
| Exponential law for the automaton 𝒜(L) (Section 10.2b) | Comparison with oriented percolation [L95, BBS94, HS22]; the one recorded non-monotone survival theorem is [BN94] (not obtained); no finite-size exponential-lifetime theorem without monotonicity was found | A **constructed example** using standard tools. Honest but artificial: a random tape read once |
| Minimality of the rule among its neighbours; the class (Section 9) | Survey of 6,144 outer-totalistic rules with metastable states and nucleation [RK14] | Survey-level; a new instance |

**Ranking.** The four results we judge most likely to interest a reader who knows cellular automata and
metastability, with what each still lacks before it could carry a paper.

1. **The face-extinction law in an automaton with proved confinement, and its tail measured to one cell**
   (Sections 3, 5.2, 5.3). *Why:* it is a supertransient whose collapse is decomposed by theorems into
   irreversible events, measured over more than twenty units of ln τ, with a mechanism-free account of the death
   rate; it is simple enough to be a model system for proofs. *Missing:* the law is measured, not proved; the
   constant is neither derived nor even isolated (rising octahedral slope, wrap-around terms); nothing at A ≥ 108
   has a second implementation; the top point has 16 deaths; the review [TL08] and the primary supertransient
   papers must be read by a person before any claim of novelty for "area, not volume".
2. **The exponent is made in a boundary layer over noise** (Section 6). *Why:* it turns a question about
   deterministic chaos into one about a finite-depth probabilistic automaton, where the tools that prove
   exponential lifetimes for stochastic systems might apply; it was confirmed by independent code and by a
   forecast. *Missing:* sizes beyond A = 84; an account of the 0.03–0.04 offset for octahedral faces; any
   theorem for the noise-driven model; a check that this is not already known for supertransients.
3. **Symmetry shortens lifetimes exponentially** (Section 5.5). *Why:* it is simple to state, large (a symmetric
   face of 759 cells lives like an asymmetric one of about 100), explains a visible feature of the 2012 runs, and
   was not found in the literature searched. *Missing:* the asymptotic slope is not determined (free fits
   0.024–0.044 per cell); the factor 1.5 between centres is unexplained; the general "volume over group order"
   statement is grade C; in the 2D analogue a forecast for rotations failed and is not understood.
4. **The structure theorems as a package** (Section 3): confinement and firewalls, the exact energy identity, and
   the sealed-set dichotomy at thickness three. *Why:* complete proofs, short, and they are what makes the rest
   measurable; this is the only part that could be written up as it stands. *Missing:* a reading of [E09] and of
   the Goles primaries to place Theorems 2 and 5 correctly; the proofs have been re-derived by independent
   automated readers and brute-force checked, and have not been read by a mathematician.

The shape dependence of Section 7 is probably new and is the most thoroughly cross-checked measurement in the
paper, but as it stands it is a refutation (no law in area and shortest loop) without a replacement; it would
move up the list if the second variable were found or if the thin-torus costs per cell were computed exactly.

## 12. Methods and reproducibility

**Implementations.** A reference implementation in numpy that reproduces the 2012 code's semantics, including its
array-index torus; a bit-sliced engine; bit-sliced replica steppers on arbitrary cell graphs; an orbit-reduced
stepper for O_h-symmetric states; two GPU kernels. Acceptance rule: a stepper's numbers are used only after it
agrees bit for bit with the engine or the reference over thousands of generations on several vessels
(`research/check.sh`, 20 exact checks). The GPU kernels were checked by emulating them on a CPU against two CPU
steppers, with deliberately broken kernels as negative controls; that the GPU executes the kernel as the
emulation does cannot be checked without a second GPU run, and none was made.

**Estimators.** Mean wait = exposure/deaths over replicas older than T₀ whose vessel is intact; statistical error
of ln τ = 1/√deaths; τ_face multiplies by the number of faces. Memorylessness was tested by the coefficient of
variation, a Kolmogorov–Smirnov test, the hazard in age bins, and in one case a censored Weibull fit.

**Three traps, each met more than once.** (i) *Settled debris.* A replica that settles into a still life or
oscillator with cells in the outer layer never dies; counted as living it inflates τ without limit (one tool read
6.2 × 10⁴ where single runs gave 630). Every estimator must censor every period, not only periods 1 and 2;
periods beyond the detectors' windows (128 generations on the GPU, divisors of 840 on the CPU) would not be
seen, and none has been. (ii) *Competing channels.* Lifetimes that count any outer-layer death mix face deaths
with transverse firewalls (Section 5.4). (iii) *Ties.* When events are checked every 16 generations, a face death
and a firewall in one window must be attributed by convention, which biases the firewall-dominated tori of
Section 7.3 by about 0.02.

**Verification.** Each claim is recorded in a ledger with the command that reproduces it and a grade; an
independent audit re-derived the theorems and the exact numbers and re-ran the cheaper statistics; later results
were each given to an adversarial reviewer with code of its own before being recorded. Forecasts were committed
before runs (Table 5). Not repeated by anyone: the side-16 run; the 960-rule survey; any GPU run.

**Availability.** Code, curated tables and per-life data for the GPU experiments are in the repository; bulk
output is not tracked, and some analysis scripts need it (listed in `docs/paper/GAPS.md`).

## References

Only works recorded in `research/PRIOR-ART.md` or `research/theory/swarm/library/shelf.md` are cited, with how
far each was read there. No citation has been checked against a library by a person.

- [BBS94] P. Balister, B. Bollobás, A. Stacey, "Improved upper bounds for the critical probability of oriented
  percolation in two dimensions", Random Structures Algorithms 5 (1994) 573–589. *Not obtained; statement
  second-hand.*
- [BGPV19] Buca, Garrahan, Prosen, Vanicat, "Exact large deviation statistics and trajectory phase transition of
  a deterministic boundary driven cellular automaton", arXiv:1901.00845. *Abstract page opened.*
- [BN94] M. Bramson, C. Neuhauser, "Survival of one-dimensional cellular automata under random perturbations",
  Ann. Probab. 22 (1994) 244–263. *Not obtained.*
- [BY08] L. A. Bunimovich, A. Yurchenko, "Where to place a hole to achieve a maximal escape rate",
  arXiv:0811.4438. *Abstract and statements.*
- [CD11] S. Chatterjee, R. Durrett, "Persistence of activity in threshold contact processes, an 'annealed
  approximation' of random Boolean networks", Random Structures Algorithms 39 (2011) 228–246; arXiv:0911.5339.
  *§1.*
- [CK88] J. P. Crutchfield, K. Kaneko, "Are attractors relevant to turbulence?", Phys. Rev. Lett. 60 (1988)
  2715–2718. *Abstract only.*
- [DL88] R. Durrett, X.-F. Liu, "The contact process on a finite set", Ann. Probab. 16 (1988) 1158–1173.
  *Statements and proofs of Thms 1, 2, 4.*
- [DS65] J. N. Darroch, E. Seneta, "On quasi-stationary distributions in absorbing discrete-time finite Markov
  chains", J. Appl. Probab. 2 (1965) 88–100. *Not obtained.*
- [DS88] R. Durrett, R. H. Schonmann, "The contact process on a finite set. II", Ann. Probab. 16 (1988)
  1570–1583. *Statements and most proofs.*
- [E09] Eppstein, "Growth and Decay in Life-Like Cellular Automata", arXiv:0911.2890. *Read in the first
  survey pass; body not re-verified in the second.*
- [G] Guttesen, "Game of Life on Archimedean Lattices: Glider Guns and Phase Dynamics", arXiv:2608.27622.
  *Abstract only.*
- [GFP85] E. Goles-Chacc, F. Fogelman-Soulié, D. Pellegrin, "Decreasing energy functions as a tool for studying
  threshold networks", Discrete Appl. Math. 12 (1985) 261–277. *Not obtained.*
- [GMRS23] E. Goles, P. Montealegre, M. Ríos-Wilson, S. Sené, "Dynamical stability of threshold networks over
  undirected signed graphs", arXiv:2309.01854. *§4.1.*
- [GO80, GO81] E. Goles, J. Olivos, "Periodic behaviour of generalized threshold functions", Discrete Math. 30
  (1980) 187–189; "Comportement périodique des fonctions à seuil binaires et applications", Discrete Appl. Math.
  3 (1981) 93–105. *Not obtained.*
- [HKTP10] S. M. Houghton, E. Knobloch, S. M. Tobias, M. R. E. Proctor, "Transient spatiotemporal chaos in the
  complex Ginzburg–Landau equation on long domains", Phys. Lett. A 374 (2010) 2030–2034. *Abstract,
  introduction, lifetime results, conclusion.*
- [HS22] I. Hartarsky, R. Szabó, "Generalised oriented site percolation", Markov Process. Related Fields 28
  (2022); arXiv:2103.15621. *Statements; the proof of Cor. 4.8 is a sketch.*
- [KL08] G. Keller, C. Liverani, "Rare events, escape rates and quasistationarity: some exact formulae",
  arXiv:0810.2229. *§1–3.1, §5.2.*
- [KMMK11] C. J. Kuhlman, H. S. Mortveit, D. Murrugarra, V. S. A. Kumar, "Bifurcations in Boolean networks",
  arXiv:1108.2974. *Introduction, §3.1, appendix.*
- [L95] T. M. Liggett, "Survival of discrete time growth models, with applications to oriented percolation",
  Ann. Appl. Probab. 5 (1995) 613–636. *Abstract; key statement second-hand.*
- [LL-soup] Life Lexicon, "soup", https://playgameoflife.com/lexicon/soup. *Opened.*
- [LMS90] J. L. Lebowitz, C. Maes, E. R. Speer, "Statistical mechanics of probabilistic cellular automata",
  J. Statist. Phys. 59 (1990) 117–170. *Abstract only.*
- [LW-CH], [LW-Mod], [LW-NT], [LW-OT] LifeWiki pages "Cubic honeycomb", "Mod", "Non-trivial",
  "Outer-totalistic", read through the mirror conwaylife.njohnston.ca. *Opened.*
- [M93] T. S. Mountford, "A metastable result for the finite multidimensional contact process", Canad. Math.
  Bull. 36 (1993) 216–226. *Whole.*
- [M99] T. S. Mountford, "Existence of a constant for finite system extinction", J. Statist. Phys. 96 (1999)
  1331–1341. *Abstract only.*
- [MMVY12] T. Mountford, J.-C. Mourrat, D. Valesin, Q. Yao, "Exponential extinction time of the contact process
  on finite graphs", arXiv:1203.2972. *Statements.*
- [MST19] I. Marcovici, M. Sablik, S. Taati, "Ergodicity of some classes of cellular automata subject to noise",
  Electron. J. Probab. 24 (2019) paper 41; arXiv:1712.05500. *§1–2 and statements.*
- [MV10] T. Mountford, D. Valesin, "Supercriticality of annealed approximations of Boolean networks",
  arXiv:1007.0862. *Abstract, §1.*
- [MV12] S. Méléard, D. Villemonais, "Quasi-stationary distributions and population processes", Probab. Surv. 9
  (2012) 340–410; arXiv:1112.4732. *§2.1, §3.*
- [PT09] A. Politi, A. Torcini, "Stable chaos", arXiv:0902.2545. *§1 and the starts of §3, §4.*
- [RK14] Reia, Kinouchi, "Conway's game of life is a near-critical metastable state in the multiverse of
  cellular automata", arXiv:1407.1006. *Abstract only.*
- [TL08] T. Tél, Y.-C. Lai, "Chaotic transients in spatially extended systems", Phys. Rep. 460 (2008) 245–275.
  *Not obtained.*
- [WS03] R. Wackerbauer, K. Showalter, "Collapse of spatiotemporal chaos", Phys. Rev. Lett. 91 (2003) 174103.
  *Not obtained; known through [HKTP10].*
- [arXiv:1510.05924] "Monte Carlo Simulations of ABC Stacked Kagome Lattice Thin Films". *Abstract only.*
  [citation needed: authors]

## Appendix: ledger rows not used

Superseded and therefore absent: F7 (an early engine-only slope), S1 (the proportional "effective area" law for
symmetric faces), the fitted limit of F9 and GP4 (the extrapolated constant 0.2077). Graded C and mentioned only
as preliminary: P4–P6, F2, F10–F12, S4, Z4, Z5, Z10, the thickness measurements, Q4, G2–G4, X3, SW3, SW4, and
the other-lattice results. Graded C and not mentioned: R6 (the web stepper's tests), C7, Z11, L2, L3, the
remaining other-lattice rows. Rows about the edge-neighbour variant (not this automaton) are outside the paper.
