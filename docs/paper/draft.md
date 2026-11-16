# Confined chaos on the faces of the cubic honeycomb: a cellular automaton whose turbulence dies one face at a time

(authors to be decided by the owner)

*Draft 2, 2026-11-15, revised the same day for the symmetric collapse; again for how a face dies, the
empty-patch rerun and the corrected 4 × 4 anchor; and again for the last two rounds on how a face dies, the wrapped
faces measured on a second GPU, signals and the state space a seed explores (draft 1: 2026-11-14). Internal draft; it stays in the repository. How the work was produced and how that is
disclosed is the owner's decision and is not addressed here.*

**How to read the tags.** Every sentence that states a result carries one of **[proved]**, **[measured]**,
**[conjecture]**; a forecast is a conjecture until scored. After the tag comes the row of the project's claims
ledger (`research/CLAIMS.md`) and its verification grade: **A** = re-derived independently by different code or a
different reader; **B** = re-run or recomputed by someone other than the producer and matched (where it matters the
text says what was repeated: the runs on the producer's own seeds, which checks code and transcription but not the
statistics; the analysis from the producer's records; or the runs on fresh seeds); **B−** = as B, but the runs were
made on a GPU that no second implementation has repeated. Only A and B claims appear as results. A claim graded
**C** (has a command, not re-run) appears only where marked *preliminary*. "ln τ ± x" always means the statistical
error 1/√(number of deaths) unless said otherwise; it does not include systematic errors, which are discussed where
known. Section 12 defines the estimators.

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
shortest loop that was fixed before the runs was refuted, as were five candidate second variables; the
differences at equal shortest loop are gone by A = 72. Wrapped faces of one shape, measured on a second GPU, cost
0.2084 per cell from 63 cells up, after a kink near 61 cells that no smooth correction fits, while the local slopes
of octahedral faces (0.2119, 0.2146, 0.2181) move away from that value; whether the two families share one
asymptotic price is open. The thinnest periodic face costs about 0.099 per cell in the limit (0.093 to
0.107 by the correction form), half a wide face's. Symmetric initial conditions die exponentially sooner,
mainly because symmetry forces faces that share an edge to die together: at A = 63 each such edge costs about
2.15 in ln τ, additively, while pairing faces that share no edge costs at most about 0.1; a cost along mirror
lines, which we first proposed, is not the mechanism of most of the deficit. This
accounts for the 2012 series of cubic seeds, extended here to a cube of side 16 that ran 2,919,617,676
generations, although the one forecast of that lifetime made before the run was low by a factor 12. Looked at in
the generations before it dies, a tied face dies as an untied one does: a tie changes the stationary face (a
thinner rim) and how likely each further step down a dip of its population is, not how often dips start or how
the end runs. Five or six
layers of the rule above fresh coin flips reproduce a slab face's lifetime to 0.015 in ln τ, so the exponent is
set in a boundary layer driven by noise. Settled replicas missed by the detectors are bounded in every CPU run but
not in the largest GPU runs (Section 12). Although no finite pattern can move through empty space, gump carries
signals along free-standing wires: pulses that move one cube every two generations and leave the wire as it was, a
transmission to a counter, and an inhibition element (measured, with the reference implementation as judge); and,
**proved**, a clock of period exactly 4N + 2 for every N, so that free-standing oscillators have unbounded periods,
and a tape on which every sequence of two kinds of wire unit moves rigidly. **Not proved:** the area law, and its constant. We give what is known
rigorously (a conditional area law resting on a measured hypothesis; an exponential law for a deterministic
relative of a two-dimensional analogue, conditional on two published percolation statements), relate the
phenomenon to supertransient chaos, and say which parts our literature search did not find and which parts have
not been searched for at all. Several pieces are instances of known results, and we say so where they appear: the
tail statement is the standard flux identity of quasi-stationary distributions, already used for deterministic
spatially extended transients; that death enters through a boundary is published for spiral-defect chaos; that
the shorter side of a torus controls a lifetime is a theorem for equilibrium tunnelling; and the dead sets that
stay dead unconditionally are a 9-core, the complement of a bootstrap-percolation closure, with the firewall a
blocking set in the sense of cellular-automaton dynamics (Section 11).

## 1. Introduction

Long-lived chaotic transients whose mean lifetime grows exponentially with system size, and which end abruptly
with exponentially distributed lifetimes, are known numerically in coupled map lattices, reaction–diffusion
systems and the complex Ginzburg–Landau equation under the name *supertransients* [CK88, WS03, HKTP10, TL08],
and in cellular-automaton-like coupled maps as *stable chaos* [PT09]. In every source on supertransients and stable chaos recorded in this project's
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
symmetry of the face in ways not yet reduced to a formula (Sections 5.5 and 7), and ask whether all faces share
one asymptotic cost per cell (Section 7.5): wrapped faces of one shape cost 0.2084 per cell above a kink near 61
cells, octahedral faces more and with rising slopes, and one price or two is open. When the chaos has gone, ordered
matter remains, and some of it carries signals: pulses run along free-standing wires, and from them a clock of every
period 4N + 2 and a rigidly moving tape are built and proved (Section 8.1). Section 11 places each result
against the nearest work our searches found; several are instances of known results (the quasi-stationary flux
identity for the death rate, boundary-controlled death, the shorter side of a torus setting an equilibrium
tunnelling time, blocking sets and k-cores for the sets that die for ever), and what may be ours is stated there
narrowly.

The results fall into three kinds, and we keep them apart throughout.

- *Proved*: the structure theorems of Section 3, the twist lemma for oscillators (Section 8), the clock and the
  tape (Section 8.1), the half-space criterion for confinement (Section 9), and two conditional theorems about
  lifetimes (Section 10).
- *Measured*: the chaotic phase (Section 4), the face-extinction law and its dependence on geometry and symmetry
  (Sections 5–7), how much of its state space a seed explores (Section 6.1), the debris and the signals (Section 8),
  the neighbourhood in rule space (Section 9).
- *Conjectured or open*: that the wait is exponential in the area for a reason derivable from the rule; the value
  of the constant; several extrapolations. Section 10 lists them.

Several measurements were preceded by forecasts committed to the repository before the runs; we report every such
forecast about gump found in the files named under Table 5, including those that failed (Section 5.7).

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
space and on the 2012 code's torus for even H (R3; B). **[measured]** The 2012 lifetimes for sides 8–13 are free of
wrap-around artefacts (R4; B). A "side-n closed cube" is an n × n × n block of cubes with all faces live:
**[proved]** it has 3n²(n + 1) cells and its diagonal hull has L1 radius 3n − 2 in doubled units about its centre
(T6 of the ledger; A). Every other stepper used in this paper (numpy, bit-sliced C on arbitrary cell graphs,
symmetry-reduced, GPU) was required to agree with the engine or the reference bit for bit before its numbers
were used: the numpy, bit-sliced and orbit-reduced steppers by direct comparison (R7; B), the GPU kernels only by
emulating them on a CPU against the engine and the CPU steppers (GP1; B−; GP7; B), which cannot check the GPU's
own execution (Section 12).

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
*Remark.* Read along one diagonal with whole layers as letters, a firewall is a *blocking word* in the sense of
Kůrka and Blanchard–Tisseur [BT00], of the simplest kind (its image is "dead" at every time); it is also the
non-monotone, three-dimensional counterpart of the bootstrap-percolation fact that an empty strip of a width set by
the rule, orthogonal to a pair of stable directions, stays empty [BSU15].

**Theorem 4 (closed sub-automata; the kagome stack) [proved]** (T4; A). A pattern contained in m consecutive
layers stays in them. The cells of one {111} layer form a kagome lattice: the four in-layer perpendicular
neighbours of a cell are its kagome nearest neighbours and the two in-layer coplanar neighbours sit across the
two hexagons it borders. Each layer is therefore a closed two-dimensional automaton running B45/S345 on six
neighbours, and the full automaton is an ABC stack of kagome layers in which a cell is coupled to 6 cells of its
own layer, 2 + 2 of the adjacent layers and 1 + 1 of the layers after those.

Theorems 2 and 3 hold for every outer-totalistic rule on this neighbourhood whose smallest birth count is at
least 4. More generally **[proved]** (ledger K9, the class study; A): for any lattice, any neighbourhood and
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
The minimality of the 36-cell two-layer set is computer-checked within a finite patch only (T9; B: the search was
re-run by a second agent for one and for two layers), and beyond that patch it is not claimed.)

*Remark (a restatement in classical terms, checked from the definitions; `docs/AUTOMATON.md`, after T6).* Every
cell has 12 neighbours, so "at most 3 neighbours outside" is "at least 9 inside": the largest dead sealed set K(t)
is the **9-core** of the graph induced on the dead cells. Equivalently it is the set never reached when the live
cells are closed under bootstrap percolation with threshold 4 (a cell joins once 4 of its neighbours have); that
k-core and bootstrap percolation are complementary in this way is published [Mil16]. "K(t) only grows" is then
the comparison of gump with that monotone rule (the uncapped rule U of Theorem 5), and follows from the definition;
it is a remark, not a result. The object is classical; what is specific to this lattice is (b) and (c), the
statement about three layers and the finite sealed sets of one and two layers. (A further reading, that (b) says
threshold-4 bootstrap percolation on this lattice is not *subcritical* in the sense of Gravner–Griffeath, known to
us through [BSU15], is a reviewer's and is not checked here.)

Theorem 6 says that in three or more layers unconditional death cannot start locally: it must come in from a face
or span the vessel. This is the mechanism the measurements of Section 5 find. It also explains, as far as a
theorem about sealed sets can, the role of thickness 3: **[measured]** (ledger K1 of the thickness study; B:
repeated by a second agent on fresh seeds, every mean within 2 combined standard errors) soups in slabs one or two
layers thick settle in times growing like the logarithm of the area (means 4.6–11.9 and 44–101 generations), while
in three layers ln τ grows linearly with the slab's width. That thin slabs "freeze" is a statement about typical
states only: **[measured]** (ledger K3 of the thickness study; B: every object re-verified with the reference
implementation by a second agent) the one-layer automaton has oscillators of periods 3 to 12.

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

**Correlations, damage and fronts.** **[measured]** (P4; B: two sets of 12 snapshots at N = 64, the second made
by a second agent with 8 of its 12 new, fitted by the lead with separate code) Correlations are isotropic at small
k. The structure factor has the Ornstein–Zernike form for k ≤ 2.5 per cube, with correlation length
ξ = 0.65 ± 0.03 cube (0.64 ± 0.013 and 0.66 ± 0.014 on the two sets) and S(0) ≈ 3.1 ≈ χ. An earlier value,
0.68 ± 0.01, came from a fit window in which the form no longer fits, with error bars too small by √24.
**[measured]** (P5; B: re-run by a second agent on the producer's own seeds and snapshots, which checks the code
and the transcription, not the statistics) Damage from one flipped cell spread in 40 of 40 trials as a sphere at
0.83–0.87 cube per generation. **[measured]** (P6; B: re-run by a second agent) Chaos invades vacuum through planar
fronts, at 0.177 cube per generation across {100}; the {110} front slows, from 0.165 cube per generation in fit
windows ending by generation 80 to 0.154 over generations 60–110. That the front speed across {111} is exactly zero
is Theorem 2. A referee would ask for a Lyapunov exponent or an equivalent; none has been measured, and "chaotic"
in this paper means: aperiodic over the times observed, with damage spreading (P5) and short correlations (P4).

Figures: `research/figures/phase_bulk.png` (bulk density and its fluctuations),
`research/figures/phase_spread.png` (damage and fronts; not re-examined for this draft),
`research/figures/phase_symmetry.png` (density by symmetry class).

## 5. How confined chaos ends

### 5.1 The staircase is the hull losing one layer at a time

The 2012 population logs of cubic seeds show a long noisy plateau followed by a staircase of lower plateaus.
**[measured]** (F1; B) For the side-11 cube the hull radius (outermost live layer along every diagonal, in doubled
units about the centre) falls from 31 to 27 within five generations, stays at 27 for 3,285 generations, and then
every face loses its outer layer at generations 3,290, 3,477 and 3,796 (the first generation at which that layer is
empty), before a final collapse ending at 4,218; no interior firewall forms before the final collapse.
**[measured]** (F3; B) The side-13 cube does the same at about 130,200, 145,850, 156,800, 166,650 and 168,200,
ending at 169,049. Each stair is the loss of one {111} layer from every face of the octahedron (all eight at once
because the seed is O_h-symmetric); by Theorem 2 each loss is irreversible. **[measured]** (F2; B: re-run by a
second agent; the heights only to within ±0.03, because they depend on an averaging window that was not recorded)
the plateau heights of side 11 are 0.79, 0.61, 0.48 of the first (0.770, 0.604, 0.454 averaged over whole
plateaus), against hull-volume ratios (R/27)³ = 0.79, 0.62, 0.47. A tracked picture of a peel as a kymograph of
layer populations is `web/docs/peel-kymograph.png`.

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

**Memoryless.** **[measured]** (F5; A) For the slab faces of the face-law fit below (m = 8, near-square) with
A ≥ 36 that carry a test in the table (four batches, 3 × 4, 3 × 5, 4 × 4, 4 × 5, A = 36–60; the fit's batches at
A ≥ 72 had 55–475 of their 512 runs censored at the run's cap and have no CV or KS value), the first-death times have coefficient of variation 0.964–1.045 and pass a
Kolmogorov–Smirnov test against the exponential (p = 0.519–0.96) (`research/peeling/slab_area.csv`, columns cv,
ks_p). Over every batch of that table with A ≥ 36 and a test (14 batches, all thicknesses and shapes) p runs from
0.042 to 0.974, one batch (4 × 5 × 10) below 0.05, and the CV from 0.962 to 1.06. An independent
engine-only measurement on octahedra gave CV 1.03 and 0.99 at R = 9 and 11. Faces of A ≤ 27 are
transient-dominated and are not exponential. **[measured]** (GP5; B−) In the largest sample, 5,971 deaths of
cube-centred O_h-symmetric soups at R = 43 with replica ages up to 2.6 τ, a censored Weibull fit gives shape
k = 1.020 (95%: 1.000–1.042): no ageing. (An apparent fall of the death rate with age in a shorter run at this
size was noise; the same indication at R = 45, k = 0.84 on 192 deaths, has not been re-run.)

**Exponential in the area.** **[measured]** (F4; B, refitted from the curated table. The ledger also grades the
slope A on the strength of two independent measurements on octahedral faces; Table 2 and Section 7 show that
those are not the same quantity, so we rely on the B only.) For slab faces with m = 8 on eight near-square period lattices, A = 27 to 90, a weighted
fit gives

$$\ln \tau_{\rm face} = (-0.091 \pm 0.047) + (0.2088 \pm 0.0009)\,A,$$

with residuals up to 0.18 and τ_face from 2.8 × 10² to 1.6 × 10⁸ generations
(`python3 research/peeling/face_law_fit.py`; figure `research/figures/peel_face_law.png`, which predates the
measurements below and plots symmetric faces against a rescaled area that this paper does not use). The first
death time does not depend on the slab's thickness once m ≥ 7: at A = 48 it is 9.9, 10.4, 10.3, 10.3, 10.3 × 10³
generations for m = 7, 8, 9, 10, 12 (`research/peeling/slab_area.csv`). This fit is a first description only:
Section 7 shows that it mixes faces of different widths, that a single slope does not describe periodic faces,
and that its slope is inflated by the mixture.

**Octahedral faces.** **[measured]** Table 2 gives the per-face lifetimes of asymmetric soups in octahedra. The law
has the same form and octahedral faces are tougher than periodic ones: 1.7–1.9 times the slab line at A = 45, 63,
84 (F6; B + A), and at A = 108 an octahedral face has ln τ_face larger by 0.91 ± 0.06 than a 6 × 6 periodic face
measured with the same estimator (GP7; B), or by 0.84 ± 0.04 against the pooled, firewall-resolved slab value
22.537 ± 0.031 (GP8; B; every value compared is †, Section 12). What makes them tougher (the rim, eight faces
sharing edges, the interior, the shape) has not been separated. The cost per cell is not constant: the local slopes
of Table 2 are 0.201, 0.212, 0.215, 0.218 ± 0.001 and 0.221 ± 0.009, still rising at A = 135 (GP1; B−). Its limit,
if there is one, is not known (Section 7.5). An earlier extrapolated limit, 0.2077 ± 0.0014, was withdrawn when it
was found to miss its own data.

| R | A | face deaths | ln τ_face | source and independent values |
|---:|---:|---:|---:|---|
| 7 | 30 | 117,851 | 6.805 ± 0.003 | symmetry-free bit-sliced CPU ensemble (F9, tabulated value; B); an engine-only run gives −ln h/A = 0.2274 against 0.2268 |
| 9 | 45 | 137,243 | 9.820 ± 0.003 | same (F9; B); engine-only run of 13,765 deaths: 9.825 ± 0.009 (F8; A) |
| 11 | 63 | 764,941 | 13.635 ± 0.001 | GPU ensemble (calibration row of GP1); CPU: 13.632 ± 0.008 |
| 13 | 84 | 34,026 | 18.141 ± 0.005 | GPU; two independent CPU runs: 18.154 ± 0.025 and 18.148 ± 0.028; the earlier CPU value 18.077 ± 0.054 (342 deaths) |
| 15 | 108 | 1,059 | 23.376 ± 0.031 † | GPU only (GP1; B−) |
| 17 | 135 | 16 | 29.34 ± 0.25 † | GPU only (GP1; B−); replica ages reach 1/900 of the mean |

Table 2. Asymmetric soups (density 0.35) in octahedra of L1 radius R; τ_face = 8 × mean wait to the first face
death. The CPU values at R = 7, 9, 11 are ln(8 × first_peel_mean) in `research/fluct/data/qsd_summary.json`
(6.8054, 9.8202, 13.6317); `research/fluct/README.md` and the notebook print 6.804, 9.819, 13.633, which differ
from the file in the last digit. The engine-only value at R = 9 is ln(8 × exposure/deaths) from `python3
research/experiments/face_endgame_check.py 9 16000` (re-run 2026-11-14: 13,765 first peels, exposure 31,826,744
soup-generations, mean 2312.1 ± 19.7, the notebook's 2312 ± 20); the 9.824 printed in an earlier draft is not what
the script gives. **[measured]** Local slopes between successive rows: 0.2010, 0.2119, 0.2146, 0.2181, 0.2209.
Nothing at A ≥ 108 has been reproduced by a second implementation or a second GPU run; the kernel was checked bit
for bit against the CPU steppers by emulation, which cannot check the GPU's execution. † These runs admit no bound
on settled replicas the GPU missed; at A = 63 and 84 the bounds are 1.3 × 10⁻⁴ and 6.7 × 10⁻³ (ZL2; B; Section 12).

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
down to one cell, and no separate mechanism of death is needed. The relation itself is not new: rate = Σ (exit
rate × quasi-stationary probability of the state exited from) is the standard flux identity of quasi-stationary
distributions [AM17, eq. 6], and it has been used for deterministic spatially extended transients with a measured
distribution: spiral-defect counts [SK15, VR19] and pipe-flow puffs [NA21]. What these measurements add is the
count followed down to a single cell with the exit rate measured rather than fitted, in a deterministic automaton.
The endpoints are −ln h/A = 0.2268, 0.2182,
0.2164, 0.2152 at A = 30, 45, 63, 84 (F9; B for these four values; the limit fitted to them is withdrawn). A tail
extrapolated from densities n/A ≥ 0.1, which is all one can sample on large faces, misses ln h by 0.5–0.8; the
endpoint has to be measured. Figure: `research/figures/fluct_tail.png`.

**[measured]** (F10; B: re-run by a second agent on the producer's own seeds) The commonest three-cell remnant is a
triangle of the kagome layer, the three faces round one cube corner (38% of three-cell faces). *Preliminary*
**[measured]** (F12; C): a dying face is statistically ordinary until about 16 generations before its death and
empties in 10–12; forward-flux sampling along n is unbiased but gains nothing, because two copies of a state
differing in one cell have 55–95% correlated fates over the few generations of the plunge (F12). The last point
matters for method: the rare event here is a rare *configuration* reached quickly, not a slow rare path, and what
made large faces measurable was brute force on bit-sliced and symmetry-reduced steppers.

### 5.4 The competing channel: transverse firewalls

A slab or an elongated vessel can also die by a three-layer firewall (Theorem 3) across one of the other three
diagonals, after which a face dies within a small fraction of the wait. Lifetimes that count any outer-layer death
therefore mix two channels, and the face law must be read from the face channel alone. **[measured]** (GP8; B) With
every life ended at its first event and the two channels counted separately, the firewall rate at a cut of 216
cells is the same in a square and a non-square slab: ln τ_fw = 26.79 ± 0.28 per direction (6 × 6 × 8, 13 firewalls)
and 26.87 ± 0.19 (6 × 7 × 8, 29 firewalls). The method was validated on a slab where both channels are common: 3 ×
6 × 8 gives ln τ_face = 11.084 ± 0.001 and ln τ_fw = 12.327 ± 0.002 on the GPU and 11.076 ± 0.007 and 12.310 ±
0.018 in an independent CPU run with a different stepper. **[measured]** (F11; B (table): rebuilt by a second agent
from the producer's raw slab records, which are not in git, without re-running the slabs) Over thin slabs the
firewall costs about 0.12 per cell of the three-layer band that must die, roughly half the cost per cell of a face,
and the first event switches from firewall to face death when the thickness is about the width. The fit behind the
0.12, ln τ_fw = −1.4 + 0.54·N·m + 0.22·N (N the side of the slab's face, m its thickness), is weighted by the
numbers of firewall-first lives; unweighted it is −2.00 + 0.533·N·m + 0.356·N. In an octahedron the faces are the
smallest {111} sections and no interior firewall was seen before the final collapse of the cubes examined (F1). A
practical consequence: eight-layer slabs cannot measure the face channel beyond A ≈ 110 unless firewalls are
detected.

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
| 759 | 43; GPU 1,057; 21.903 ± 0.031 † (with a longer run: 21.889 ± 0.012) | 44; GPU 637; 22.409 ± 0.040 † | 0.51 ± 0.05 |
| 828 | 45; GPU 192; 24.175 ± 0.072 † | | |

Table 3. O_h-symmetric soups; τ = mean residence at hull radius R, states older than 1,000 generations.
**[measured]** CPU rows: orbit-reduced stepper, `research/fluct/data/sym_residence.csv`, fresh soups only (S2, S3;
B, with agreement between two independent implementations at A = 408–630, grade A). GPU rows: GP2, GP3 (B−, B). †:
no bound on settled replicas the GPU missed (ZL2, Section 12); the longer R = 43 run is bounded by 1.2 × 10⁻²
against its error 0.013 (*preliminary*, C). The ratio column uses the CPU values; `python3
research/fluct/sym_fit.py` prints 0.27 ± 0.13 at A = 630 and 0.87 ± 0.18 at A = 693 because it pools copies of the
side-16 cube's own states into the vertex values there.

**[measured]** What the table shows.

- *Scale.* A symmetric face family of 759 cells lives about as long (ln τ ≈ 21.9) as an asymmetric octahedral
  face of roughly 100 cells (Table 2). The 2012 side-13 cube lasted 1.7 × 10⁵ generations in a hull whose faces
  have 459 cells; symmetric soups at that size have mean residence 2.6 × 10⁵.
- *No fixed "effective area".* Over A = 408–693 the cube-centred values are fitted (χ² = 4.0 on 4) by
  ln τ = 0.698 + (0.209/6)·A − 0.196·√A, i.e. the periodic-face slope shared among the six images of a face cell
  under the face's stabiliser, less a boundary term (S2; B + A). This is a description of that range, not an
  established law: free fits to the same points prefer slopes between 0.024 and 0.044 depending on the curvature
  term, and the two GPU points beyond the range lie 0.166 and 0.275 above the fitted curve (the curve printed by
  `python3 research/fluct/sym_fit.py`, 0.698134 and −0.195996, gives 21.737 at A = 759 and 23.900 at 828; against
  the pooled 21.889 the first offset is 0.152). The local slope between
  A = 759 and 828 is 0.0329 ± 0.0011, to be compared with 0.209/6 = 0.0348 (GP2; B−). The asymptotic symmetric
  slope is open. Two qualifications (S2's note of 2026-11-15, S8; B): the √A coefficient depends on the
  asymmetric slope assumed in the fit (it moves by −8.1 per unit of that slope; with the slope pinned at 0.2035,
  the value measured on faces with diagonal mirrors below, the fit gives −0.127), and whether −0.196·√A is an
  asymptotic form at all is open (below).
- *Centre matters, but not by a constant factor.* Vertex-centred hulls are tougher than cube-centred ones of equal
  face area by a factor about 1.5 (ln ratio 0.40–0.47 at A = 408–630), 1.66 ± 0.08 at A = 759 on the GPU, and
  2.0 ± 0.4 at A = 693 from fresh soups (S3; B). The factor is not one object. **[measured]** (S9; A, two codes)
  With no symmetry at all, vertex-centred faces already outlive cube-centred ones of equal area, by +0.754 ± 0.013,
  +0.725 ± 0.009 and +0.655 ± 0.017 in ln τ at A = 30, 45, 63, a difference that falls with size. *Preliminary*
  (S9; C, not rerun or refitted): with three edges in lockstep (D2h) a part grows (0.505, 0.645, 0.830 at A = 63,
  84, 108), and for O_h a constant factor is excluded by the theory line's fit (χ² 60.8 on 10). So "about 1.5" is a
  snapshot of a slowly changing difference.
- *Still memoryless.* Vertex-centred O_h soups wait exponentially at R = 36, 38, 40 (GP3; B) and cube-centred
  ones at R = 43 (GP5, above). Runs from deterministic cube-like O_h seeds (cubes with surface orbits removed,
  hollow cubes) wait like soups: at hull radius 31–38, 1,248 plateaus have mean T/τ = 0.99 and CV 1.02 against
  3,261 soup plateaus (two-sample KS p = 0.98), with no correlation between consecutive plateaus (L1; B); at
  vertex-centred R = 40, 3,857 lineages wait exponentially on the plateaus at 40, 38, 36 (mean T/τ 0.99, 1.01,
  0.98), with a weak correlation between the first two (Spearman ρ = +0.049) traced to lineages that peel early
  (GP6; B−).

**Why symmetric faces die sooner: shared edges, not mirror lines.** A theory line set out to derive the three
fitted ingredients above (the 1/6, the √A term and the factor between centrings) from the asymmetric law and
geometry, with its forecasts committed before its runs (`research/theory/symmetric/`); an adversarial review ran
the unreduced system with a stepper of its own (`research/audit/REVIEW-symmetric.md`). No derivation came out.
What did:

**[proved]** (S5; A) A G-symmetric state evolves exactly as gump on the orbit graph, and for free actions the factor
one over the order of G is exact. Inside a {111} face the only mirrors are the three diagonal ones and their
translates; a coordinate mirror never preserves a face: it exchanges two hull faces and fixes the rim row they
share. (One auxiliary lemma of the line is false as stated; no measurement uses it.)

| symmetry imposed (octahedral vessel, A = 63, R = 11, cube-centred) | ln τ_face, theory line (orbit stepper) | ln τ_face, review (full system) |
|---|---:|---:|
| none | 13.634 ± 0.018 | 13.638 ± 0.010 |
| one coordinate mirror: one edge of every face in lockstep | 11.456 ± 0.011 | 11.444 ± 0.010 |
| two: two edges | 9.291 ± 0.008 | 9.312 ± 0.009 |
| three (D2h): three edges | 7.168 ± 0.003 | 7.171 ± 0.009 (bracket 7.02–7.29) |
| inversion: pairs faces that share no edge | 13.578 ± 0.014 | 13.574 ± 0.014 |

Table 3a. The edge ladder. **[measured]** (S6; A: the review's own stepper on the unreduced system; the line's
orbit stepper is bit-exact against the engine on 41 systems). The bracket on the review's three-mirror value comes
from lives that settled (35% of its exposure). Each edge shared with a face that is forced to die at the same moment
costs about 2.15 in ln τ, additively; inversion costs −0.056 ± 0.023, at most about 0.1. A twofold rotation about an
edge costs 2.54 ± 0.02 (cube-centred; 1.96 ± 0.02 vertex-centred) on the edge-sharing faces it pairs and about 0.1
on the opposite ones (the split by face orbit is the reviewer's, at A = 63 only): no mirror is needed.

**[measured]** (S7; B: one pair rerun by the reviewer, the other slab families not rerun) A mirror, a threefold axis
or both, imposed on a rim-free periodic slab face, *lengthen* its life against the asymmetric torus of equal area,
by +0.4 to +1.65 in ln τ at 36–72 quotient cells and by an amount that shrinks with size (the rerun pair: +0.926 ±
0.014 against the line's +0.872 ± 0.013; the sign stands). The line had forecast a loss. In a fully symmetric face the
lockstep rim lies on a coordinate mirror, so "rim" and "mirror" cannot be separated there; and faces with diagonal
mirrors and free rims (T_d) fall below the mirror-free ones (T) by an amount growing like √A, so a diagonal-mirror
share of up to about a third of the −0.196 is not excluded. **[conjecture]** (S7) The mechanism: edge-sharing faces
that die together cannot hold each other up. Section 5.6 looks at the dying faces: they do not show this in its
dynamical form (a live neighbour feeding a free rim), only a static one (a tied rim is thinner at all times).

**[measured]** (S8; B: the reviewer's refits of the line's data; no T, T_d or O_h run repeated by a second code; one
job and one seed per size) The slope times the order of the face's stabiliser is 0.2091 ± 0.0016 for T faces
(threefold axis, free rims, A = 108–198) and 0.2035 ± 0.0024 for T_d faces (A = 315–459), 3–5% lower. "c/6 within
5%" is supported; "exactly c/6" is not shown, and c itself is not known (wrapped faces of one shape give 0.2084, hull faces' slopes are higher and
rising; Section 7.5). The rim's
marginal cost is 0.45–0.55 per rim period over 5.5–9 periods, which corresponds to a √A coefficient of −0.19 to
−0.22, close to the fitted −0.196; the review shows that this agreement is a coincidence of ranges, not a test.
Whether the rim term bends, and so whether −0.196·√A is an asymptotic form at all, is open: the fall in marginal
cost rests on the two smallest sizes. A T_d ensemble at A = 759 would speak to it (forecasts 26.2–26.4 if linear,
25.65 ± 0.25 if T_d keeps its slope; only 1.9σ apart); it needs a GPU and has not been run.

*What this corrects.* From 2026-11-12 the project described Table 3 as six lockstep domains less a penalty along
the mirror lines, and earlier versions of this draft offered, as interpretation, that cells on mirror planes
are depleted (P7, Section 4). The depletion stands as a measurement, but the picture is corrected, not reversed:
the cost is mainly that edge-sharing faces die together, and "the chaos runs thin along mirror lines" is not the
mechanism of most of it. The line's forecasts fared accordingly: of 40 statements, counted per size, 25 held, 1 sat
on its limit and 14 failed (Table 5, row 19).

*What remains preliminary.* In a symmetric state the cells of an orbit share one state (exactly, S5), so a face has
about A/6 independent cells and its fluctuation to emptiness is correspondingly cheaper. *Preliminary*
**[measured → conjecture]** (S4; C): across symmetry groups and on tori without faces, a symmetric system lives
about as long as an asymmetric one of c times its fundamental domain's volume, c ≈ 1.5–3.5. **[measured]** (SW3;
B: run by one examiner and re-run by a second agent on the examiner's seed sequence, not by different code):
octahedral faces cut by a single mirror plane cost 0.1026 ± 0.0003 per cell at A = 84–135, 0.47 of the asymmetric
value, and the first face to die is a mirror-fixed one in more than 99.9% of replicas.

### 5.6 How a face dies

The edge ladder of Table 3a was explained before anyone had looked at a face. A study then did
(`research/dying/`): in the vessel of Table 3a (R = 11 cube-centred, faces of 63 cells) with no, one, two or three
edges of each face tied to a face in lockstep (c1, csz, c2v, D2h), it kept the 512 generations before each of 11,930
first face deaths and a stationary control, and in a second round followed the excursions of the face population
in long stationary runs. Forecasts were committed before each round's runs (`research/dying/PREDICTIONS.md`). An
adversarial review reran both rounds on fresh seeds with a stepper of its own, matched to the reference
implementation at every generation on twelve systems (`research/audit/REVIEW-dying.md`). Every result of these two
rounds is graded A on that basis; where the review did not confirm a reading, we say so. Two later rounds, also
reviewed, follow at the end of this section with their own grades.

**The run-up.** **[measured]** (DY1; A: same plunge medians and mean curves in both codes) The *mean* dying face
stays at its stationary density until about 20 generations before death and then fades over the whole face, with no
erosion from an edge: relative to its own stationary value, a band along a tied edge empties no earlier than one
along a free edge. The final plunge (from half the stationary population to empty) has median 6, 6, 7, 7
generations in the four groups, although their lifetimes differ by e^6.5. Single deaths are not uniform fades (the
review's statement): at half population 32–39% of them are more lopsided than 95% of stationary faces thinned at
random to the same count, against 9–11% in a control 64 generations earlier. The depleted side is not the tied edge
and does not persist beyond what thinning implies. (The *preliminary* description of the plunge in Section 5.3, F12,
concerns asymmetric octahedra and uses other definitions; the two were not compared.)

**What a tie changes.** **[measured]** (DY2; A: study and review agree to three digits on the rim rows) An edge
tied to a face in lockstep is thinner at all times. Stationary occupancy of the rim row is 0.512 along a free edge
and 0.349, 0.323, 0.298 along a tied one (csz, c2v, D2h); the stationary face population is 31.25, 28.90, 26.28,
23.50. Cube-centred, the loss sits in the rim row itself, and the loss per tied rim cell is the same in a larger
vessel (R = 13: 0.149–0.186 against 0.148–0.185). ln τ is not a function of the mean population: a cell lost at a
tied edge costs 0.64–1.00 in ln τ, one gained by growing the untied face buys 0.40, one gained by re-centring 0.23.
In D2h, 36.5% of old living states are in lives that have settled; the stationary control leaves them out and the
ln τ rung of Table 3a counts their exposure, so the two D2h figures are not taken over the same lives.

**The neighbour.** **[measured]** (DY3; A) When an untied face dies, its neighbour's own second row along the shared
edge falls to 0.56–0.61 of its stationary occupancy and the rest of the neighbour stays at 0.95. The larger drop
first reported (the neighbour's band at 0.21) is the shared rim row, whose cells are the dying face's own: adjacent
faces share that row.

**A death is a dip that keeps going.** For a face with stationary mean population P̄, let ν(p) be the rate per face
per generation of excursions that start above the mean and reach p·P̄, and q(p) the fraction of them that end in
the face's death before the population is back above the mean; then 1/τ_face = ν(p)·q(p) at every level, by
bookkeeping (every death ends an excursion). **[measured]** (DY4; A: the reviewer's stepper on fresh seeds gives
the same p* to three digits) −ln(νq) = 13.632, 11.454, 9.274 (c1, csz, c2v; review 13.614, 11.473, 9.275) against
13.634, 11.456, 9.291 from the lifetimes of Table 3a; the agreement checks the counting, not a mechanism. The point
of no return (q = 1/2) is at 0.079, 0.114, 0.152, 0.245 of the mean, about 2.5 live cells of 31 in the untied face,
and an untied face that has lost half its cells recovers 99.92% of the time (q(0.5) = 0.0008). In D2h the
figure depends on what is done with lives that settle: 7.32 with them, 6.86 without, 7.168 in the study; every D2h
quantity that involves exposure carries that ambiguity.

**[measured]** (DY5; A for the rates and slopes) Ties do not make dips start more often: dips to 0.7 of the mean come
at ln ν = −4.16, −3.80, −3.77, −3.74 per face per generation (review −4.16, −3.80, −3.78, −3.88), and at 0.9 of the
mean the untied face dips the most often. The groups part below about 0.6 of the mean, where each tied edge raises
ln q by 1.5–2.7. ln ν is Gaussian with the stationary variance down to about 0.6 of the mean and fatter below. Over
the last 3–12 cells the price per further cell lost is nearly constant (local slope 0.51–0.48 per cell in c1,
falling to 0.34 by 17–20 cells) and is higher the more free edges a face has; that it is a constant price is a **[conjecture]**. The
review did not confirm a straight tail, a change of regime at half the mean, or a fixed step per free edge (the
lead's "5.5 + 3.4 per free edge" ranges from 3.0 to 4.5 with the fit window).

**[measured]** (DY6; A: both codes) On a dying untied face births fail before survival: births per empty cell are
0.90–0.91 of stationary at lag 16 while survival is 0.98–0.99, and 0.45 and 0.88 at lag 8. This is mostly what the
face's own lower population predicts, since stationary births depend strongly on the face's population and survival
does not (review: births 0.61 at lag 8 where the population predicts 0.77). Depleted faces are lopsided whether or
not they go on to die: in c1 the survivors' centroid is 1.6 times further out than in a face thinned at random, in
dying faces and in faces that are low by chance alike. At equal count, dying untied faces are *less* lopsided than
chance-low ones (2.47 against 3.09) and dying D2h faces *more* (2.94 against 2.70).

**[measured]** (DY7; A) ln τ = 3.43 + 0.582·P̄²/(2σ_P²) fits the eight lifetimes of the four groups at 63 and 84
cells within 0.31, but a + b·A + c·P̄, with no width in it, fits as well (0.27), and leaving one point out gives
0.50: a description, not a law.

*Readings withdrawn after the review.* That the stationary population falls in steps as equal as those of ln τ
(they are −2.35, −2.62, −2.77 against −2.18, −2.17, −2.12); that a cell lost at a tied edge costs 0.86 in ln τ,
"twice the 0.436 per live cell" of the untied face (0.436 is an average, not a marginal; the marginals are those of
DY2); that the neighbour face is dragged down as a whole (it is one row); that chance-low faces are as lopsided as
dying ones in every group (in D2h they are not); and the picture of a constant price per cell with a live clump and
a hole coexisting on a depleted face, which the clumping does not support. **[conjecture]** What survives of the
"hold each other up" account (S7) is static: a tied face has a thinner rim at all times, sits closer to empty and
needs a smaller fluctuation to die; nothing here shows that this causes the −2.15 per edge.

*Forecasts.* The lead's forecasts for the first round failed from L2 to L7 (the rim is not the late survivor; the
tied edge is not where emptying begins; the neighbour does not stay within 10%; the plunge is not faster with more
ties); L1, a deduction, is consistent with everything seen. Of the seven for the second round one held (A2). The
review confirms that every definition was fixed before the data and reproduces every score (Table 5, rows 20 and
21). Not checked: deaths at other sizes or centrings (the review's other vessels are stationary sampling only);
c2e and O_h; one seed per group in the study's excursion runs; births by neighbour count; whether the position of
the surviving clump predicts recovery; differences of 1.8σ between the two codes in the csz and D2h populations.

**Round 3: the dips across sizes.** A third round (`research/dying/README.md`, "Round 3"; forecasts T1–T4 committed
first) measured the rate ν(p) of dips to a fraction p of the usual population on free (c1) hull faces of 45, 63, 84
and 108 cells and on one rim-free face (the equilateral torus of 63 cells, Section 7.5), and looked at faces caught
deep in a dip. The review reran it with its own stepper on fresh seeds and added 135 cells (`research/audit/REVIEW-dying.md`,
"Round 3").

**[measured]** (DY8; A: study and review agree to 3–4 digits) The dip curve per cell is one curve only down to about
half the population: −ln ν(0.5)/A = 0.120, 0.103, 0.093, 0.089, 0.086 at A = 45, 63, 84, 108, 135, while its
shallow part, [ln ν(0.9) − ln ν(0.5)]/A, is 0.065–0.067 at every size. Below p ≈ 0.55 the curves of different sizes
differ by a fixed number of nats K(p), not by a number per cell; K grows smoothly to 2.1 at p = 0, half of it below
p = 0.15. ln ν(0.9) itself falls by about 0.002 per cell.

**[measured]** (DY9; A for the line, B for the estimate of c, which is the review's alone) For free hull faces of
45–108 cells, ln τ_face + ln ν(0.9) = 0.2125·A − 2.07 within 0.01 nats. The slope depends on which dip rate is taken
as the attempt (0.218 for every crossing of the mean, 0.204 for ν(0.8)), and the dips at p ≥ 0.2 alone, extrapolated
in size and then to p = 0, give c = 0.215 ± 0.005, which does not separate 0.207 from 0.219 and adds nothing to the
lifetimes' own local slopes (Section 7.5). Withdrawn after the review: a levelling off of the end points near
0.19–0.20 (they follow c − K/A and still rise at 135 cells); a constant K ≈ 2.4 (it runs 2.37 → 2.78); a formula for
c from the density and the Fano factor.

**[measured]** (DY10; A: study, review and the lead) Over 0.1–0.45 of the usual population the tail of the dip curve
costs 0.50–0.52 per live cell at A ≥ 63 (0.44–0.47 at 45), rising slowly with size; locally it runs from 0.53 deep
down to 0.40 near half.

**[measured]** (DY11; B: the study's numbers reproduce; the alignment-free figures and the rule-aware baseline are
the review's alone) A free face of 63 cells caught at 0.3 of its usual population (8.3 live cells on average) is at
about half its stationary density near a survivor (0.46–0.54), the excess reaching about 3.5 doubled units, and at
0.15–0.20 of stationary elsewhere: thinner far away, not emptied. Thinner faces have a looser patch. A thin csz face
is depleted at its tied edge beyond the stationary deficit (its centroid nearest the tied edge in 22.4% of faces,
against 29.8% for stationary faces thinned to the same count). That a face "refills from its patch" is forced by the
rule (0.994 against a rule-aware baseline of 0.991) and says nothing.

**Round 4: is a depleted face two phases?** Before round 4 the lead read the rule's cooperativity as implying that a
deeply depleted face is a void beside a remnant held at a fixed density, the remnant shrinking as the population
falls (a lever rule), and that the dip curve is a parabola joined to its tangent (`research/dying/PREDICTIONS.md`,
"Round 4", F1–F6, committed before any run). Round 4 caught free hull faces of 63, 84 and 108 cells at six depths,
0.9 to 0.15 of their usual population, beside a control of stationary faces thinned at random to the same count. The
review reran it with its own stepper and geometry on seeds the study did not use (`research/audit/REVIEW-dying.md`,
"Round 4").

**[measured]** (DY13; B: two steppers and two analyses agree at 63 and 84 cells; 108 cells at p = 0.15 and the null
below are one code each) The *company* C, the occupancy within two steps of a live cell over its stationary value,
falls steadily with depth: at 108 cells 0.833, 0.738, 0.646, 0.542, 0.439, 0.288 from p = 0.9 to 0.15, and
C(0.15)/C(0.45) = 0.38, 0.49, 0.53 at 63, 84, 108 cells. A caught face is far from a random thinning: it has 1.15 to
2.4 times the control's company and 2.3 to 3.2 times its void at p = 0.3.

*What does not follow.* The study read the falling company as "a depleted face thins as one thing; there is no
remnant". The review built the alternative and put it through the same code: a compact patch held at any fixed
density from 0.45 to 0.8, with nothing outside it, reads C(0.15)/C(0.45) = 0.45–0.48, 0.58–0.61, 0.65–0.69 at 63, 84,
108 cells, because at four to eight live cells such a patch is about the size of the two-step neighbourhood over
which the company is counted. So a finite face with a remnant at fixed density reads the same way, the registered
tests could not have told the two readings apart, and **"no remnant at fixed density" is withdrawn**. What does
separate a caught face from such a patch is a ratio 0.07–0.14 below the null's and a more peaked profile against
distance from a survivor (0.45, 0.16, 0.04, 0.03 against 0.33, 0.22, 0.08, 0.005 at four live cells of 63): a
tighter knot with a thin scatter beyond it, not an even patch with an edge.

**[measured]** (DY14; B: redone by the reviewer from the study's table and, at 63 cells, from its own run) What
ends the two-phase reading is its number, not its picture: the parabola-plus-tangent construction overshoots the
true end point of the dip curve, [ln τ + ln ν(0.9)]/A, by 1.07, 1.21, 1.34 nats at 63, 84, 108 cells, and the
straight tail alone by 0.53, 0.51, 0.46 nats.

**[measured]** (DY15; B: matched, the reviewer's code; unmatched, both codes) At equal live count, faces that go on
to die are looser at the catch than faces that recover: C = 0.145 against 0.166 at p = 0.15 (difference 0.021 ±
0.001) and 0.303 against 0.320 at p = 0.3 (0.017 ± 0.003), at 63 cells. Unmatched, most of the gap (0.151 against
0.204) is the count.

*What a caught face is and is not.* It is not a random thinning of a stationary face (more company, a larger void)
and not an even patch at a fixed density (its profile is more peaked); near a survivor it is at about half the
stationary density, and far away thinner, not empty, at 0.3 of the usual population (DY11). No plateau is seen; the
company cannot test a lever rule on faces of 108 cells or fewer; whether a remnant in some looser sense exists is
open and is not reachable at sizes where faces can be caught this deep. There is no model for the shape of the dip
curve below half the population.

*Forecasts and what was not checked.* Round 3: T1a (the raw curve collapses), T1b and T2 failed, T3 and T4 held (T4
nearly forced by the rule; T1b failed as registered, a count-weighted fit that integer thresholds break, and the
unweighted fit would have held). Round 4: F1–F5 failed as registered, and the review shows that F1, F2 and F6 could
not test the reading they were written for. Over the four rounds three of the lead's twenty-three forecasts held
(Table 5, rows 22 and 23). Not checked: one fresh seed per hull size in both reviews (two for the torus); the
lifetimes at 108 and 135 cells are the GPU's; the patch in csz and D2h and its change with depth; at 108 cells the
review ran 1.5 million generations, with no catch at p = 0.15 and no deaths; the null is one patch shape (a ball);
at 84 cells there were 82 deaths, so the dying-against-recovering comparison is tested properly only at 63 cells.

### 5.7 The cubes, and the forecasts that were made in advance

**The side-16 cube.** **[measured]** (C2; B: schedule and summary re-derived from the committed event log; the
run itself, several days on one core, was not repeated) The cube of side 16 sat at hull radius 42 (vertex-centred,
A = 693) until generation 2,362,434,048, then at 40 until 2,886,100,480, and ended as a 96-cell still life at
2,919,617,676. The two face-death generations, here and in Table 5, are *last-alive* generations: the run checked
its layers every 64 generations, and these are the last checks at which the outer layer was seen live. Section 5.1
defines a face death as the first generation with the layer empty; by that definition the two deaths lie in
2,362,434,049–2,362,434,112 and 2,886,100,481–2,886,100,544 (the next checks, at which the layers were empty;
`research/data/cube16_events.jsonl`, fields gen and last_alive). The difference, under 64 generations, changes
none of the comparisons below.

| hull radius R (face cells A) | 42 (693) | 40 (630) | 38 (570) | 36 (513) | 34 (459) | 32 (408) | 30 and below |
|---|---|---|---|---|---|---|---|
| generations spent | 2.362 × 10⁹ | 5.237 × 10⁸ | 3.08 × 10⁷ | 2.71 × 10⁶ | 7,040 | 27,712 | 1,932 in all (1,792 to the last layer death) |

Table 4. Residence schedule of the side-16 cube (`research/data/cube16_events.jsonl`; events sampled every 64
generations).

**Forecasts.** Several quantities in this section were forecast in files committed before the outcome was known.
Table 5 lists every forecast about gump found in the sources named in its caption, with its score, failures
included.

| # | forecast (where committed) | outcome | score |
|---|---|---|---|
| 1 | Side-16 lifetime: mean 2.4 × 10⁸, 90% interval 3.9 × 10⁷–6.3 × 10⁸, from a proportional "effective area" fit to symmetric soups (`research/peeling/cube_lifetime.csv`) | 2,919,617,676 | **failed**, low by a factor 12 (C3; B) |
| 2 | Side-16 first face death: median 2.2 × 10⁹, 90% 1.50–5.2 × 10⁹, from perturbed copies of the running cube's state with restarts; committed about two hours before the event (`research/fluct/PREDICTIONS.md`, commit 2e72d57) | 2,362,434,048 | held, at about the 57th percentile (quantile 0.566; C4; B for the commit time and the arithmetic; the wall-clock time of the event itself is grade C) |
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
| 14 | The remnant of a dying face is the same in every vessel: on a rim-free slab face (5 × 4 × 8, A = 60) the mean face population 1, 2, 3, 4 generations before death is the hull's 1.6, 3.4, 6.4, 9.7; refuted if lags 3 or 4 are more than 20% off (swarm path E3, `research/theory/swarm/PREDICTIONS.md`, protocol committed before the run in `research/theory/swarm/exam/OUTCOMES.md`) | 1.66, 4.29, 10.70, 18.40 (3,188 face deaths) | **failed** at lags 3 and 4 (+67%, +90%); lag 1 and the one-cell share (59.4% against 62 ± 5%) held (SW7; B: re-run by a second agent on the shared seed sequence, lags 1.689, 4.348, 10.958, 18.440; the refutation reproduced) |
| 15 | Five candidate second variables at equal area and shortest loop, fitted on three pairs (`research/shape3/PREDICTIONS.md`, commit 46baf66) | none fits (χ² ≥ 111 on 7) | **all refuted** (SH9; A) |
| 16 | Empty patches on a 12 × 12 × 8 face: ln P = const − c·cells − σ·perimeter with c = 0.21 ± 0.015 (`research/NOTEBOOK.md`, entry "a forecast before the run") | c = 0.264; the form fails (χ² 3,369 on 3) | **missed** as stated (GP10; A + B−) |
| 17 | The thin-face study's 14 forecasts, each committed before its run (`research/theory/thin/PREDICTIONS.md`) | rescored by the review | 8 hit, 2 half, 2 mostly missed, 2 missed (TH7; B) |
| 18 | The constant analysis's forecasts (`research/constant/PREDICTIONS.md`): −ln P = 5.0, 9.5, 15.3 for empty 2×2, 3×3, 4×4 patches; about zero for the equal-loop pairs at A = 63 and 72 | 6.25, 12.13, 19.42; Σz² 3.7 on 4, wrong in sign at A = 36 | patches **missed** (low by 1.3, 2.6, 4.1); pairs not refuted there; the equilateral tori of its part C are row 24 (CN2; B: scores recomputed by a second agent) |
| 19 | The symmetric-collapse line's forecasts (`research/theory/symmetric/PREDICTIONS.md`), among them that a mirror or threefold axis on a rim-free periodic face would shorten its life | 40 statements counted per size: 25 held, 1 on its limit, 14 failed; the symmetry lengthens such a face's life (+0.4 to +1.65) | **14 failed**, the mirror forecast among them (S7; B for the slab values). The tally has no ledger row (NOTEBOOK 2026-11-15, "the symmetric collapse") |
| 20 | How a face dies, first round (`research/dying/PREDICTIONS.md`, commit 75e5212): L1 death an event of the whole face; L2–L7, among them that the rim outlives the interior (band/interior ratio ≥ 1.5 at lag 4), that emptying begins at the tied edge, that the neighbour stays within 10%, that the plunge shortens with more ties | L1 consistent; ratio 1.06–1.22; emptying not at the tied edge; neighbour 0.893; plunge medians 6, 6, 7, 7 | **L2–L7 failed** (L4 undecided with another choice of band); scores reproduced by the review (DY1–DY3; A). The tally has no ledger row (NOTEBOOK 2026-11-15, "how a face dies") |
| 21 | How a face dies, second round (same file, commit 6d40e72): seven forecasts, among them a point of no return at 0.25–0.5 of the mean, the ladder in ν rather than q at half population, 2.8–3.1 cells lost per tied edge at 84 cells, no function of the stationary mean and width fitting all eight lifetimes | p* = 0.08; the ladder mostly in q; 2.68, 2.95, 3.38; one fit within 0.31 | **one of seven held** (A2, ln ν Gaussian to 0.6 of the mean); scores reproduced by the review (DY4–DY7; A). The tally has no ledger row (NOTEBOOK 2026-11-15, "a death is a dip that keeps going") |
| 22 | How a face dies, third round (same file, "Round 3", T1–T4): among them that the dip curve per cell collapses across sizes (T1a), a straight tail (T1b), a patch at 0.8 of stationary round a survivor (T2) | no collapse; T1b failed as registered (count-weighted); no such patch | **T1a, T1b, T2 failed**; T3, T4 held, T4 nearly forced by the rule (DY8, DY10, DY11; A, A, B). The tally has no ledger row (NOTEBOOK 2026-11-15, "what the dips say about the price of a cell") |
| 23 | How a face dies, fourth round (same file, "Round 4", F1–F6): a depleted face is a void beside a remnant at fixed density (a lever rule), the dip curve a parabola joined to its tangent | company falls steadily with depth; the construction overshoots the end point by 1.07–1.34 nats | **F1–F5 failed** as registered; F1, F2, F6 could not test the reading (the review's null); the reading ends on its number (DY13, DY14; B). Over the four rounds 3 of the lead's 23 held. No ledger row for the tally (NOTEBOOK 2026-11-15, "round 4 reviewed") |
| 24 | Equilateral face tori under three readings, flat, massive and rising (`research/constant/PREDICTIONS.md` part C; e.g. A = 93: 19.479 ± 0.010, 19.437 ± 0.019, 19.506–19.530) | A = 93: 19.4141 ± 0.0053; A = 57 and 63 above every reading (flat by 0.034 and 0.047, massive by 0.021 and 0.034) | **no reading survives**: flat and rising refuted at A = 93 by their own lines, massive missed at 57 and 63 (GL3; A at 57, 63, 75, C at 93). Scores in the file's dated blocks |
| 25 | The lead's N1–N4 for the same tori (same file, second note of 2026-11-15): N1 A = 93 above flat by at least 0.03; N2 A = 57 likewise; N3 A = 81, 84 between massive and flat; N4 the excess per cell falls with size | 0.070 below flat; 0.034–0.039 above; not yet run | **N1, N4 failed**; N2 held, on a reason that A = 93 ended; N3 open (GL3). No ledger row for the tally |
| 26 | The lead's signals forecasts S1–S10 (`research/signals/PREDICTIONS.md`): among them S1 that the wires on file carry nothing, S3 a transmission (one chance in five), S8 a receiver that toggles, S9 that carriers arise from soup | fronts run the whole wire; a transmission to a counter; no toggle; carriers from one random unit repeated | S1, S8 **failed**; S2, S7, S10 held; S3 held with a caveat; S6 half; S9 held only in a weak sense (re-scored after the review); S4, S5 untested (SG1–SG10). No ledger row for the tally (NOTEBOOK 2026-11-15, the signals entries) |
| 27 | The lead's state-space forecasts E1–E7 (`research/statespace/PREDICTIONS.md`, before any enumeration) | see Section 6.1 | three and a half of seven held: E1, E4 failed, E6 failed as a general rule, E2 half (SS1). No ledger row for the tally (NOTEBOOK 2026-11-15, "how much of its state space a seed explores") |

Table 5. Forecasts committed before their outcomes. Sources searched: `research/peeling/cube_lifetime.csv`,
`research/fluct/PREDICTIONS.md`, `research/gpu/PREDICTIONS.md`, `research/shape/PREDICTIONS.md`,
`research/shape2/PREDICTIONS.md`, `research/shape3/PREDICTIONS.md` (its five candidates only),
`research/theory/thin/PREDICTIONS.md` and `research/constant/PREDICTIONS.md` as scored in TH7 and CN2, the notebook
entry named in row 16, `research/theory/exponent.md`, and the swarm's `research/theory/swarm/PREDICTIONS.md` as
scored in `research/theory/swarm/exam/OUTCOMES.md`, and `research/theory/symmetric/PREDICTIONS.md` as scored in the
notebook entry "the symmetric collapse", and rounds 1 and 2 of `research/dying/PREDICTIONS.md` as scored in the
notebook entries "how a face dies" and "a death is a dip that keeps going", rounds 3 and 4 of the same file as scored
in the entries "what the dips say about the price of a cell" and "round 4 reviewed", part C of
`research/constant/PREDICTIONS.md` with the lead's N1–N4 as scored in that file's dated blocks, the lead's S1–S10 in
`research/signals/PREDICTIONS.md` and E1–E7 in `research/statespace/PREDICTIONS.md` as scored in the notebook;
within these, the ledger rows C3–C5, C9, GP2, GP8, GP9, GP10,
SH1, SH2, SH5, SH9, SW2, TH7, CN2, S7, DY1–DY15, GL3, SG1–SG10, SS1. Not searched for this table: the other tracked
forecast files and blocks (the signals investigators' own I1–I9 and J1–J10, scored in their file; the second card's
forecasts in its own `PREDICTIONS.md` on its branch, and the reviewer's table of predictions by correction form,
both for runs not yet reported;
`research/theory/exponent/PREDICTIONS.md` entry by entry, `research/theory/class/PREDICTIONS.md`,
`research/theory/class/followup/PREDICTIONS.md`, `research/toy2d/PREDICTIONS.md`,
`research/audit/class/PREDICTION-*.md`), so the table may be incomplete. Omitted: forecasts about other rules.
Among the swarm exam's entries these are the ones on the 2D rule and its dice models: counting C-E2 failed (slope
0.3676 ± 0.0006 against 0.447 ± 0.012), probability P-E1 is undecided at its refutation line (0.512 ± 0.012 against
a line at 0.51), path E2 was not refuted but its central value missed at L = 36 (7.99 ± 0.38 against 9.8 ± 1.0);
path E1 and source S-E1 held. The exam's one other gump entry, counting C-E1, held (0.1026 ± 0.0003 against 0.105 ±
0.009; SW3, grade B, Section 5.5). Several forecasts about other rules also failed (Section 9).

**What the failure of forecast 1 showed.** The forecast multiplied a fit made on cube-centred symmetric soups
with faces of at most 513 cells by a fixed factor for the vertex-centred hull. Both steps were wrong in the same
direction: the cost per cell of a symmetric face rises with its size (Table 3), and the data on vertex-centred
hulls then reached only A = 408. **[measured]** Against fresh vertex-centred soups in the same hull
(τ = 7.1 × 10⁸, 45 deaths) the cube's first plateau is 3.3 means (probability 0.036 for one exponential wait);
radius 42 is an ordinary size (C8; pooled value re-derived, B).

**An open question, not a finding.** **[measured]** The cube stayed 5.24 × 10⁸ generations at R = 40, which is 7.4
times the mean of an ensemble that pools fresh soups with copies of the cube (probability 6 × 10⁻⁴ for one
exponential wait; C5; B), or 6.1 times the fresh-soup mean 8.63 × 10⁷ (probability 0.002). A count over the sixteen
largest plateaus of cubes 13–16 finds three longer than four means (C6; B for the arithmetic), but that statistic
was chosen after the side-16 plateaus suggested it; without side 16 it gives P ≈ 0.18, and it is not evidence.
Cube-like seeds and soups are memoryless at every size tested up to R = 40 (L1, GP6). So either the side-16 cube
was lucky (*post hoc*: at about the 1% level by a statistic chosen after its plateaus were seen, L3; B (table), the
script re-run on the same data), or its own lineage carries something that ensembles of similar states do not; the
cube's own lineage at R ≥ 42 has not been, and at present cannot be, replicated.

**Extrapolations** **[conjecture]**. A side-17 cube's first plateau has mean about 3.2 × 10¹⁰ generations if the
soup value at A = 828 applies to it (GP2's 24.175; C9's forecast, made before that run, gave 2.6 × 10¹⁰); the cube has not been run. The 2012 run from a side-19 cube, which was
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
- *The thinnest periodic face* (TH4; A for w = 5 and 4 at A = 48). The same depth: +0.006 ± 0.003 at w = 5,
  +0.049 ± 0.003 at w = 4, and 0.4–2.3 at w ≤ 3, not rerun (Section 7.4).

**[measured]** (SW2; B: run by an examiner who had not made the prediction) With six layers over fair coins, slab
faces of A = 36 and 48 give 7.397 ± 0.009 and 9.945 ± 0.014 against the deterministic 7.398 and 9.936.

**[measured]** (X2; A: independent numpy code against the study's driver) The same holds in the two-dimensional
analogue of Section 9: eight rows of the rule over coin flips give ln τ_edge = 5.654, 7.425, 9.136 against the
deterministic strips' 5.644, 7.407, 9.142 at edge lengths L = 12, 16, 20, and are 0.067 ± 0.027 high at L = 24;
the density of the coins hardly matters.

**[proved by exhibiting the fixed point; measured]** (X3; B: the reviewer's script re-run by a second agent) The
noise-driven models can settle. The six faces of one cube lying on the face are a fixed point whatever the coins
do (w ≥ 4 for a cube at a hull vertex, w ≥ 5 for one anywhere on the face), and a replica in such a state never
dies; censored, one model reads 6.542 ± 0.001. *Preliminary* (X3; C): uncensored, the same model reads 6.94.

*What this does and does not establish.* At sizes A ≤ 84 and precisions of 0.01–0.05 in ln τ, the deterministic
bulk enters the face law only as a source of noise produced within five or six layers. The question "why about
0.21 per cell" is thereby reduced to one about a probabilistic cellular automaton of finite depth, for which
lifetimes can be sampled without the bulk and computed exactly at small sizes. It is not shown that the
reduction survives at larger A, where the cost per cell is still drifting (Table 2), and the offset for
octahedral faces is unexplained. No theorem is claimed. Figures of the study (not re-examined for this draft):
`research/figures/exponent_gump.png`, `research/figures/exponent_hierarchy.png`.

*Relation to known work.* The method is an instance of a known one, run in mirror image: Carretero-González et
al. [CG99] drive a small window of a chaotic coupled map lattice with white noise at its edges and recover the
large lattice's one- and two-point statistics, exponentially fast in the window size (full text read); dos Santos
et al. [dS08] call such inputs a thermal bath (abstract only, as paraphrased by a fetch tool). They keep a window
and randomise its outside; we keep the boundary layer and randomise the inside, and neither compares lifetimes.
That death enters through the boundary is also not ours: for spiral-defect chaos the death rate is proportional to
the length of the non-conducting boundary [VR19, R22], and [HKTP10] fit boundary layers of fixed thickness with
interior defect production as under periodic conditions (full text read), but model the lifetime in the whole
length. Not found in our searches: a work that replaces a chaotic interior by noise and compares transient
lifetimes or escape rates, or that attributes a supertransient's exponent to a thin layer over noise. The review
[TL08] was not obtained.

### 6.1 How much of its state space a seed explores

Within a hull there are finitely many states; the owner asked how many of them a long-lived seed visits
(`docs/OWNER-JOURNAL.md`). Study: `research/statespace/` (forecasts committed before any enumeration); review:
`research/audit/REVIEW-statespace.md`, with its own vessel builder (two deliberately broken neighbour tables caught),
its own enumerator, its own hull search and its own entropy sampler.

**[proved]** An orbit of a deterministic map cannot repeat a state before it reaches its cycle, so the states a seed
visits number its settling time plus its final period. The question is the lifetime question in other units.

**[proved by enumeration]** (SS1; A for seventeen vessels, enumerated independently: by the reviewer's enumerator on
eight, by the lead with the reference on one, by an older enumerator, `research/theory/exhaust.c`, on eight; A for
the symmetry statement on eight; B for the rest, one enumerator matched to the reference) All 2^N states were listed
for 301 vessels of up to 30 cells: 262 diagonal hulls of 2–29 cells at most 6 layers wide, six of 30 cells, slab tori
of 1–3 layers, and 3D tori. Over the 34 vessels of 27–30 cells the mean seed visits 4.5–14.4 states and the most
patient 15–94. In vessels of 15 cells or more 57–98% of all states have no predecessor (53% at the least over all
listed vessels); the states on cycles are mostly still or of period 2; and no most-patient seed of a vessel of 19 or
more cells has a symmetry. At these sizes nothing is chaotic yet: the faces have 9–30 cells, under the 36 or so where
lifetimes turn exponential (Section 5.2). The review corrected three readings: the ranges (first given from the
largest vessel of each family); "linear, not exponential" (a line and an exponential with rate 0.02–0.09 per cell fit
the mean visited count equally well, so the sizes listed cannot tell linear from slowly exponential growth); and the
census, which is complete only for hulls at most 6 layers wide (at least 325 more hulls of 1–29 cells are wider).

**[proved, from single runs]** (SS2; B for sides 8–15, re-run by the reviewer; side 16 *preliminary*, C, not re-run)
The closed cubes of Table 1: side 16 visited 2,919,617,676 states (2^31.44) of the 2^51,888 of its hull; sides 8–16
all come to 0.0005–0.0008 bits per hull cell. Side 14 enters its period-2 cycle at generation 4,460,296 (Table 1's
4,460,298 is the generation of detection).

**[measured]** (SS3; B: two samplers and two context orders agree to 0.001; every bound is one-sided) Read in bits,
the face law says that an asymmetric seed visits about 2^(0.30·A) states for a face of A cells (0.296–0.305 bits per
face cell from the face laws on file). A living face is close to coin flips: its top layer seen alone carries 0.986
bits per cell, the whole 8-layer face slab at most 0.9585 (an upper bound, still falling slowly with the size of the
context). An upper bound on the entropy is a lower bound on the *deficit* against coin flips of the same density,
since a finite context can hide redundancy but not invent it. One layer alone is at least 0.006–0.013 bits per cell
short of coins (the top layer 0.013, flat from 10 context cells; the layer under it 0.008; a bulk layer 0.006 against
coins at 0.4155); the slab jointly at least 0.027, most of it between layers. So any one layer of the chaos is within
about 1% of coin flips of its own density, and most of what distinguishes the chaos from noise lies between layers.
A seed therefore sees a vanishing share even of one layer's configurations (at most 2^(−0.69·A)); against the states
of a chaotic region several layers deep, or of the hull, its share is far smaller. Withdrawn after the review: the
comparison with a uniform random map, the wrong yardstick when most states have no predecessor (a random map with
gump's own in-degrees would visit 18–1,650 states where gump visits 7–10, so gump settles 3 to 160 times sooner than
that, by a birthday estimate, not thousands of times).

*Bearing on Section 6.* The deficit is the size of what the coin-flip models of Section 6 leave out below their
layers of rule: a few hundredths of a bit per cell. It does not say why five or six layers of the rule must be kept
above the coins; Section 6 measures that depth, and nothing here derives it. *Not checked:* hulls wider than 6
layers; any vessel above 30 cells exactly; where the small vessels' regime joins the exponential one; small faces
conditioned on survival (a large slab stands in for them); any lower bound on the entropy. The lead's forecasts
E1–E7, made before any enumeration, scored three and a half of seven (Table 5, row 27).

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
| 4 | 12.486 (60), 14.970 ± 0.002 (72), 17.465 ± 0.005 (84) †, 19.943 ± 0.018 (96), 22.373 ± 0.042 (108; 99.2%) | 0.2072 ± 0.0001 |
| 5 | 15.661 ± 0.003 (75), 18.786 ± 0.011 (90) †, 21.890 ± 0.040 (105) †, 25.046 ± 0.073 (120; 92%) † | 0.2082 ± 0.0006 |
| 6 | 22.568 ± 0.041 (108; 2%) †, 26.405 ± 0.104 (126; 24%) † | 0.213 ± 0.006 |

Table 6. Periodic slab faces by width (`research/data/gpu_facelaw/`; `python3 research/audit/gpu_pr16_lead_check.py
research/data/gpu_facelaw`). †: no bound on settled replicas the GPU missed (ZL2, Section 12); the run at A = 96 is
bounded by 1.0 × 10⁻² against its error 0.018 (*preliminary*, C). The A = 84 run's log has no age bins, so it has
no bound either (ZL2).

- At equal area the narrower face dies sooner: 3 × 8 against 4 × 6 (A = 72), −0.349 ± 0.004; 3 × 10 against 5 × 6
  (A = 90), −0.740 ± 0.016; 4 × 9 against 6 × 6 (A = 108), −0.196 ± 0.059. The same slab in both orientations
  agrees to −0.002 ± 0.003. The face hazard is flat in the age of the life from about 200 generations on in
  every slab, including those where firewalls end 99% of lives.
- For s = 4, 5, 6 the data do not require a width-dependent cost per cell: one slope 0.2072 ± 0.0001 with
  intercepts 0.053, 0.121, 0.203 fits (χ² = 8.4 on 8), and so does ln τ = a + 0.2117·A − 0.054·M with M the long
  side (χ² = 5.6 on 9). The two cannot be told apart with these data. Either way the correction to an area law is
  linear in a side length. Whether the cost per cell of a wide periodic face is 0.2072 or 0.2117 is **not
  decided** by these slabs; tori of constant shape give 0.2084 from 63 cells up (Section 7.5).
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

**[measured]** (SH2; A: two codes) On small faces the shortest loop is not the only variable: at A = 60 two tori
with shortest loop² 16 and second loop² 19 and 21 differ by 0.0142 ± 0.0019 in ln τ_face, and at A = 48 two with
loop² 12 and second loop² 16 and 19 by 0.0151 ± 0.0017, the shorter second loop dying sooner.

**The difference does not persist and has no fixed sign.** Let d be ln τ_face of the member with the longer second
loop minus the other's. **[measured]** (SH6; B) At A = 72 the three equal-loop differences, −0.0062 ± 0.0041 and
+0.0005 ± 0.0041 (loop² 16) and +0.0018 ± 0.0061 (loop² 12), are zero within error (χ² = 2.9 on 3). **[measured]**
(SH7; A at A = 36 and 45, an independent stepper giving −0.0220 ± 0.0009 and +0.0085 ± 0.0014; B at 54 and 63) At
shortest loop² 9, d is −0.0223 ± 0.0007 at A = 36, +0.0076 ± 0.0013 at 45, −0.0020 ± 0.0019 at 54 and +0.0017 ±
0.0020 at 63: at A = 36 the face with the *longer* second loop dies sooner.

**[proved]** (SH8; A) The reduced Gram matrix (Q1, 2B, Q2) of a face torus of index n = A/3 has
Q1·Q2 − B² = 0.75 n², so at equal area and equal shortest loop² Q1 one number fixes the lattice: second loop, third
loop, angle and Re τ (τ the torus's modular parameter) carry the same information, and candidates can differ only
in the form of their dependence, not in its sign within a group. **[measured; a refutation]** (SH9; A) Five
candidates fitted on the three earlier pairs, with forecasts committed before the runs (linear in the second loop;
linear in the angle; cos 2π Re τ; a sum over closed loops of e^(−1.41 × length); a modular form
e^(−2πh) cos 2π Re τ), are all refuted under the committed rule (χ² ≥ 111 on 7), and none can give a negative d.

**Reading** **[conjecture; not tested]**. There is no second geometric variable in the sense looked for:
differences of at most 0.02, irregular in sign on small faces and gone at A = 72, while the dependence on the
shortest loop itself grows with area (Section 7.3), look like a commensurability effect, the chaotic state's
short-range structure fitting round a small torus, which would not enter the asymptotic constant. The test is that
equal-loop differences stay below 0.005 at every A ≥ 72 (A = 84 has two pairs with loop² ≥ 12).

### 7.3 Every torus of a given area

**[measured]** (SH3; A for A = 48 → 60, where an independent stepper gives 0.1144, 0.1415, 0.1922, 0.2076,
0.2127; B for 60 → 72, one code) Measuring every class of period lattice at A = 48 and 60 and five more at
A = 72 gives a cost per cell that depends on the shortest loop and saturates:

| shortest loop² | 3 | 4 | 7 | 12 | 13 | 16 |
|---|---|---|---|---|---|---|
| d ln τ_face/dA, A = 48 → 60 | 0.1148 ± 0.0003 | 0.1414 ± 0.0003 | 0.1918 ± 0.0003 | 0.2073 ± 0.0002 | 0.2090 ± 0.0003 | 0.2131 ± 0.0002 ‡ |
| d ln τ_face/dA, A = 60 → 72 | 0.1107 ± 0.0004 | 0.1353 ± 0.0008 | 0.1872 ± 0.0010 | 0.2049 ± 0.0009 | 0.2061 ± 0.0007 | 0.2076 ± 0.0006 |

Table 8. Cost per cell of a periodic face by shortest loop (`research/shape2/README.md`; `python3
research/audit/shape2_lead_check.py`; values as in `research/shape2/data/explore_report.txt`, first block, which
also gives the A = 72 values for loop² ≥ 12 that the lead check does not print. The loop² 4 entry at 60 → 72 is
that file's 0.1353 ± 0.0008, which the lead check reproduces as 0.1353; the README's table has 0.1346 ± 0.0010).
‡ The file's 0.2125 ± 0.0003 uses the census's 4 × 4 torus, 9.9324 ± 0.0020, which was a high draw (GL1; A: three
codes give 9.9251 ± 0.0004, 9.9246 ± 0.0006 and, with the census's own pipeline on fresh seeds, 9.9240 ± 0.0014;
pooled 9.9249 ± 0.0003); with that value the slope is (12.4818 − 9.9249)/12 = 0.2131 (SH3's note of 2026-11-15).
The slopes compare different lattices with equal shortest loop, not one torus grown. The loop² 3 entries are local
slopes of a law that is still bending (Section 7.4). The census stamps layer deaths every 16 generations, and
where face deaths tie with firewalls inside one window it reads ln τ high: measured on the same lives (GL3; B), by
0.0174 at A = 48 and 0.0184 ± 0.0011 at A = 60 for the loop² 4 classes, by 0.00167 ± 0.00006 at 4 × 4 and at most
0.0008 for long-lived classes at A = 60; the slopes of the table move by at most 0.0003. The loop² 4 tori are
multigraphs (a cell counts one neighbour
twice), so only loop² 3 is strictly "the same automaton on a narrow cylinder".

Even the thinnest tori live a time exponential in their area, with a hazard flat in age and permanent face death
(SH3): they are the same kind of object as wide faces (Section 7.4).

**[measured]** (SH4; A, two codes, but only four lattices at A = 48) Above loop² 12 the shortest loop no longer
orders the classes at A = 48: the four classes with loop² 12, 12, 13, 16 span 0.016, and the 4 × 4 torus
(loop² 16) lies *below* the loop² 12 class with second loop² 19, by 0.0135 ± 0.0021 in the review's runs
(`research/audit/REVIEW-shape2.md`, claim 3) and by 0.0135 ± 0.0020 in the census once its 4 × 4 value is replaced
by the best value 9.9249 of GL1 (`research/shape2/data/A48.csv` gives 9.9384 for the loop² 12 class; against the
reviewer's own 9.9246 alone the gap would be 0.0138). The census's
own 4 × 4 value, 9.9324, gave 0.0061 ± 0.0028 and a tension with the review (χ² = 4.4 on 1); that value was a high
draw (Table 8, ‡), and the tension is gone. At A = 60 the step from loop² 12 to 16 is +0.056 to
+0.063, and at A = 72 it is about +0.10 (Table 7). The shape term grows with the area.

**[measured; a refutation]** (SH5; A: χ² recomputed with separate code on separate runs) Six candidate laws
expressing ln τ_face through the area and the shortest loop (or a sum over loops), with parameters fixed before
the census, all fail at each of A = 48, 60 and 72. The one that appeared to pass at A = 60 on the census's own
run (χ² = 5.4 on 5) fails on independent values (22.7 on 5) and on all runs pooled (45.4 on 5).

**Reading** **[conjecture]**. ln τ_face = c·A + (a term set by how the face closes on itself); the second term is
not small, not constant in A, and not a function of one length. What the families together say about c is in
Section 7.5; the thinnest torus, a quasi-one-dimensional system with its own cost per cell, is Section 7.4.

*Relation to known work.* That the shape of a torus at fixed area changes an exponential time is known in
equilibrium. For zero-field Ising and Potts Metropolis dynamics on a K × L grid at low temperature, Nardi and
Zocca prove that the tunnelling time is asymptotically exponential with exponent 2·min{K, L} + 2 under periodic
boundaries [NZ17, Thm 1.1; §§1–2 read]: on a rectangular torus the shorter side, which is the shortest loop, sets
the exponent at leading order, so the use of the shortest loop as the length that controls a lifetime is not ours.
Caselle, Gliozzi and Vinti measure the tunnelling splitting through a 3D Ising interface on a periodic L1 × L2
cross-section as e^{−σL1L2} times a universal function of L1/L2, tested at equal area [CGV93, read in full]. Both
are reversible, equilibrium interfaces on untwisted rectangles. For a twist, the nearest work found is about
quantum memories: the logical failure rate of surface codes under biased noise is controlled by gcd(j, k) of the
lattice dimensions [T19, abstract only; open boundaries, not a torus]. In three dimensions, lifetimes of
excitable-media transients grow only above a critical thickness [LCP17, abstract only], a statement of the same
shape as Section 3's role of thickness three, but not a fixed-area shape test. Not found in our searches: any
dependence of a chaotic-transient, turbulent, nucleation or extinction lifetime on the aspect ratio or twist of a
periodic domain at fixed size, or a second shape variable beyond the shortest loop.

Figure 3 (placeholder; does not exist): *ln τ_face at A = 72 against shortest loop length (Table 7), with the
A = 60 and A = 48 classes offset, and the two equal-shortest-loop pairs marked.* Figure 4 (placeholder): *cost
per cell against shortest loop² (Table 8).*

### 7.4 The thinnest face

The torus with periods (1,1) and (0,b) has shortest loop² 3, one cube step: its face is a ring of b sites of three
cells, A = 3b. **[measured]** (TH1; A: an independent stepper at b = 16, 24, 26, 28, 30, 32, within 1.3σ) Its
lifetimes (b = 16 … 36) bend: the local cost per cell is 0.1144 and 0.1104 over A = 48–72 (Table 8's loop² 3
column), 0.1081 ± 0.0003 over 72–84, 0.1067 ± 0.0004 over 84–96 and about 0.103 at 108. **[measured]** (TH2; A for
21, 29, 37 sites, C for 45 and 61) The same face with two free ends (a wall of dead face sites cut into the ring)
costs a straight 0.0993 ± 0.0003 per cell from A = 75 to 135.

**[measured: the fits]** (TH3; B) The long-face limit is about 0.099 per cell, between 0.093 and 0.107 depending on
the unknown form of the finite-size correction: a spread of fitted forms, not a confidence interval. An error bar
of ± 0.004 first given for it did not survive review; it was the spread of the forms first chosen, and others fit
as well and land outside it. **[conjecture]** If rings, segments, empty windows and the wall front share one limit,
it lies in 0.097–0.102. The thinnest face costs about half of what a wide one does per cell.

**Why it is not derived.** Noise beneath is enough only from five layers (TH4, Section 6). **[exact]** (TH5; A for
the values) One layer of the rule over coins is solvable (ln τ = 3.967199 on a ring of 5 sites). *Preliminary*
(TH5; C): its cost per site is 22% above gump's and two better closures are 11% and 5.6% above, so no exactly
solvable closure found gives the number. **[measured]** (TH6; A) The face dies as an island shrinking from both
ends: looking back from the death its population is 1.7, 4.1, 7.3, 10.1, 12.6, 14.8 at successive steps, over a
time proportional to its length. What sets the ratio of the thin face's cost to the wide face's is open.

### 7.5 Is there one asymptotic cost per cell?

**[measured, model-free]** (CN1; A) The local slopes of octahedral faces at A = 63–108 (0.2146, 0.2181 ± 0.0013;
Table 2) lie above those of periodic faces within a width family (0.2072, 0.2082; Table 6), and are rising.
**[fitted]** (CN1; A: 64 points, models stated before fitting and scored on held-out sizes; a review with its own
fits; the data of 2026-11-14) That does not separate the limits. Periodic faces give an asymptotic c = 0.207–0.216 depending on the form,
octahedral faces 0.218–0.232 with one correction term and 0.2156 with a saturating slope; a single constant passes
jointly with ordinary parameters (c = 0.2179 with a 1/A octahedral correction, joint p 0.28); of 84 pairings of an
octahedral with a periodic form, 36 pass with one constant at p ≥ 0.01, with c = 0.2072 to 0.2190. **Those data allow
one asymptotic constant anywhere from about 0.207 to 0.219; they do not fix it, and they do not show that there are
two.** Every passing reading with c ≤ 0.214 needs a two-term correction on octahedral faces; every one with c ≥
0.2155 needs periodic faces to approach c as slowly as 1/s in the width s. *Conjecture* (not tested): the thin
tori, whose deficit falls roughly exponentially in the shortest loop, argue for the lower half. **[refuted]** (CN1)
Neither a capillary-wave law for the wrap-around term nor a sum over period vectors fits (χ² 20,925 on 13 and
48,004 on 14 at A = 48 and 60). These fits include the census's 4 × 4 torus value, a high draw (Section 12), and
were not redone (CN1's note of 2026-11-15). With the tori below, the notebook reads the range 0.207–0.219 as the
distance between the two families, not as an uncertainty in one number.

**Wrapped faces of constant shape, on a second card.** Equilateral face tori have period lattices whose three
shortest loops are equal and at 60°, the shape of 4 × 4, 5 × 5 and 6 × 6 (8 layers, soup 0.4, every life ended at
its first event). Five were measured with one driver on the second GPU (Section 12), and every one but the largest
again by a CPU code:

| n | period lattice | A | shortest loop | face deaths | ln τ_face, second card | second code |
|---:|---|---:|---:|---:|---|---|
| 16 | (4,0),(0,4) | 48 | 4.00 | 7,478,823 | 9.9251 ± 0.0004 | 9.9246 ± 0.0006 (reviewer's stepper); 9.9240 ± 0.0014 (census pipeline, fresh seeds) (GL1; A) |
| 19 | (1,7),(0,19) | 57 | 4.36 | 3,283,133 | 11.8756 ± 0.0006 (two seeds, 2.6σ apart) | 11.8744 ± 0.0015 (reviewer, 445,165 deaths) (GL3; A) |
| 21 | (1,4),(0,21) | 63 | 4.58 | 1,811,510 | 13.1622 ± 0.0007 | 13.176 ± 0.011 (review of the dying-face study, DY12) (GL3; A) |
| 25 | (5,0),(0,5) | 75 | 5.00 | 183,954 | 15.6630 ± 0.0023 | 15.667 ± 0.010 (reviewer); 15.6614 ± 0.0026 on the first GPU (Table 6) (GL3; A) |
| 31 | (1,5),(0,31) | 93 | 5.57 | 35,521 | 19.4141 ± 0.0053 (four seeds, χ² 0.70 on 3) | none: *preliminary* (GL3; C; the line and the kink below rest on it) |

Table 8a. Equilateral face tori (`research/gpu-local/README.md` and `research/data/gpu_local_eqtorus/` on branch
`claude/gpu-local-1080`, pull request 23, not merged; every value recomputed by the lead from the rows as
ln(2 × exposure/deaths) ± 1/√deaths; review `research/audit/REVIEW-gpu-local-tori.md`, with a stepper built from
`docs/AUTOMATON.md` alone and equal to the reference every generation on both tori it ran). Shortest loops in cube
steps. The 93-cell run had the guard of Section 12 on, and none of its 45,761 lives settled. Tori 19, 21 and 31 have
oblique shortest loops and no possible firewall; 16 and 25 have loops along the lattice rows.

**[measured]** (GL3; B for the line and the kink: the reviewer's refit, on one degree of freedom) The tori of 63, 75
and 93 cells lie on one line, ln τ_face = 0.033 + 0.2084·A (slope 0.20840 ± 0.00014, χ² 0.0002 on 1); those of 48
and 57 cells lie below it, by 0.111 and 0.036. The local slopes are 0.2167, 0.2144, 0.2084, 0.2084. No smooth
correction fits the five values: a term decaying in the shortest loop, in 1/A, in 1/A and 1/A², a massive-like sum
and a stretched exponential give χ² of 15 to 117 on 1 (59–70 with the 57-cell error inflated). The deficit goes
0.111, 0.036, then below 0.01 between shortest loops of 4.00, 4.36 and 4.58 cube steps: an abrupt change near 61
cells, **a kink, not a fading correction**. At 2σ the data still allow a residual of 0.01 at 63 cells or a slope
change of 0.0009 above it. So at constant shape the bend lies wholly below 63 cells, and it is the small tori that
are short-lived, not the large ones that are cheap; the 6 × 6 slab of Table 6 (22.568 ± 0.041) is 0.7σ above the
line. *Conjecture* (the lead's): the loop at which the bend ends is about the width of what is left of a dying face
plus its reach (Section 5.6), so that a wrapped face stops being short-lived once its last patch cannot feel itself
round the loop. Four more tori (81, 84, 108, 111 cells) have forecasts committed before their rows (the card's: the
line, 16.913, 17.539, 22.540, 23.165; the reviewer's: the 81-cell torus separates the line from every smooth form by
0.014 against a planned ± 0.003); they are not reported here.

**Against the hull family.** **[measured]** Free hull faces of the same areas live longer than the line by 0.41,
0.47, 0.60, 0.84 at 45, 63, 84, 108 cells, and their local slopes, 0.2119, 0.2146, 0.2181 (Table 2), move away from
0.2084, not toward it. The dips of Section 5.6 give c = 0.215 ± 0.005 for hull faces (DY9; B), which separates
neither reading. **Whether there is one price per cell or two is open.** One asymptotic constant for both families now needs
the hull slope to turn round beyond 108 cells and fall by about 0.01; the other reading is that a face held by living
neighbours along its rim and a face wrapped onto itself have different prices per cell. Nothing on hull faces at
A ≥ 108 has a second implementation (Table 2), and the octahedral face at A = 108 with 10⁴ deaths, which the
constant analysis held would eliminate 35 of its 36 single-constant readings (its review disputed the power), has
not been run.

**The forecasts, scored** (Table 5, rows 24 and 25). Before these runs, part C of `research/constant/PREDICTIONS.md`
forecast the family under three readings, each anchored on the three tori then measured (4 × 4, 5 × 5, 6 × 6):
*flat*, a shape term constant in the family (c = 0.21214); *massive*, a shape term falling with size
(c = 0.2069 ± 0.0023); *rising*, the hull family's constant (c_h = 0.2226 or 0.2317) approached with a √A term. At
93 cells flat (19.479 ± 0.010, refuted below 19.445) and rising (19.506–19.530, refuted below 19.488) are refuted by
their own lines, and massive (19.437 ± 0.019) is 0.023 high, within 1.2σ; at 57 and 63 cells every reading is low,
flat by 0.034 and 0.047 and massive by 0.021 and 0.034. **No reading of part C survives.** All three were anchored on
the 4 × 4 torus, which lies inside the bend (and whose value on file was a high draw: with the corrected anchor the
forecasts move by −0.005 to +0.010 in ln τ, `research/audit/REVIEW-gpu-local-pr23.md`, section 2). Of the lead's
forecasts added once the 63-cell torus was measured, N1 and N4 failed, N2 held on a reason that the 93-cell torus
ended, and N3 is open.

**Empty patches** (GP10; A for the table up to 4 × 5, by an independent CPU stepper and counter). On a
periodic slab 12 × 12 × 8 (A = 432 per face) in which no face died in 3.04 × 10¹⁰ replica-generations, rhombic
patches have **[measured]** ln P(empty) from −6.254 (2 × 2) to −19.423 ± 0.007 (4 × 4) and −23.318 ± 0.047
(4 × 5) on the GPU. Eighteen CPU runs (2.76 × 10¹⁰ replica-generations, 0.9 of the GPU's exposure) give −23.412 ±
0.049 at 4 × 5 from 541 hits, 1.4σ from the GPU; combined, −23.364 ± 0.034. (A first CPU value, −23.75 ± 0.16 on 43
hits, was a low fluctuation.) **[failed forecast]** A forecast committed before the run, c = 0.21 ± 0.015 from the fit
ln P = const − c·cells − σ·perimeter, missed as stated: the fit gives c = 0.264 and does not describe the data
(χ² 3,369 on 3), a failure of the presumed form. **[fitted, post hoc]** Second differences along similar shapes,
which remove every term linear in the side, give a perimeter-free cost per cell of 0.273, 0.252 and 0.237 at 12, 18 and 27
cells and 0.226 ± 0.006 at 36 (GPU 0.2185 ± 0.0079 and CPU 0.2349 ± 0.0082 combined). The last value is about 1σ
above the range of the lifetime laws (0.205–0.221), not inside it as an earlier version of this draft said; the
sequence is still falling, and the asymptote is not established (0.16–0.24). Hits come in clusters, so the true
error is 1.13–1.28 times the Poisson one; the batch-means errors quoted here include that.

## 8. What is left: debris and clockwork

When the last chaos has gone a seed leaves still lifes and oscillators (or nothing: the side-15 cube ends
extinct).

**Still lifes.** **[proved, by exhaustive search]** (Z1; A + B) The smallest still lifes have 6 cells, and there
are exactly four up to symmetry; they include the six faces of a single cube (each sees exactly 4 others) and the
six-cell hexagon of one kagome layer. **[proved, exhaustive]** (Z2; B for these sizes, the search re-run by a second
agent) The numbers of strict still lifes with n = 6, …, 15 cells are 4, 2, 7, 9, 27, 45, 228, 851, 3,388, 12,255.
*Preliminary* (Z2; C): 47,578 for n = 16.

**Period 2.** **[proved, exhaustive]** (Z3; B for unions up to 13, the search re-run by a
second agent) The smallest period-2 oscillator has a union of 9 cells; there are 3, 6, 4, 11 and 10 classes with
unions of 9 to 13 cells. **[proved, exhaustive]** (Z4; B for this statement) No period-4 oscillator has union
≤ 10. *Preliminary* (Z3, Z4; C): all period-2 oscillators with union ≤ 11 are "hinge flips", in which live faces
swing 90° about a shared edge; no period-3 oscillator has union ≤ 12 and the smallest has union exactly 13.

**Why anything has period above 2.** By Theorem 5 every oscillator of period ≥ 3 has cells that are overcrowded
one generation after being alive, and over a period the drive at those cells balances the
dissipation exactly; this was verified on all 329 catalogued objects of period ≥ 3.

**Long periods are short loops closed by a symmetry.** **[measured]** (Z5; B: all 14 batches re-run by a second
agent on the producer's own seeds, identical) Soups in small octahedra leave oscillators of periods 1–16, 20, 22,
48 and 66. The longest has a simple anatomy.

**Twist lemma [proved]** (ledger T7; A). Let B be a closed box (a diagonal hull: a finite non-empty set of
cells) and F its map on the states x ∈ {0,1}^B. Let G be the group of *lattice symmetries* of B: the maps
g(p) = Rp + t with R ∈ O_h (a signed permutation matrix) and t ∈ (2Z)³ that carry B onto itself, acting on states
by (g·x)(c) = x(g⁻¹c). Each such map preserves the set of cells and the neighbourhood (Section 2.2), so G commutes
with F. Let C be a cycle of F of period P through x₀, and let L ≥ 1 be the first time at which it reaches a
symmetric image of x₀, F^L(x₀) = g·x₀ with g ∈ G. Then P = m·L, where m is the order of g acting on the cycle
(that is, of F^L on C); m ∈ {1, 2, 3, 4, 6}; and every cell fixed by g has period dividing L.
*Proof.* (1) Let Γ = {g ∈ G : g·C = C}. For g ∈ Γ, g·x₀ ∈ C, so g·x₀ = F^{k(g)}(x₀) for a unique k(g) ∈ Z_P;
because G commutes with F, k(gh) = k(g) + k(h), so k is a homomorphism Γ → Z_P whose kernel is the stabiliser of
x₀. Its image is a subgroup of the cyclic group Z_P, hence cyclic; let m be its order. The subgroup of Z_P of
order m consists of the multiples of P/m. (2) If F^j(x₀) = g·x₀ with g ∈ G, then g·C is the cycle through
F^j(x₀) ∈ C, so g ∈ Γ and j mod P lies in the image of k; conversely every element of the image is such a j. So
the times at which the orbit of x₀ meets G·x₀ are exactly the multiples of P/m; the first is L = P/m, so P = m·L,
and g acts on C as F^L, a rotation of C of order m. (3) *The order of the twist.* Sending g ∈ G to its linear
part R is a homomorphism G → O_h, and it is injective: if g, g′ ∈ G have the same linear part, then g′⁻¹g is a
translation p ↦ p + t that carries the finite set B onto itself; summing p over B gives |B|·t = 0, so t = 0.
So every element of G has the order of a signed permutation matrix R. If σ ∈ S₃ is the permutation underlying R
and c ∈ {1, 2, 3} its order, then R^c is diagonal with entries ±1, so R^{2c} = I and the order of R divides 2, 4
or 6; the orders of the elements of O_h are therefore among 1, 2, 3, 4, 6. Now take g ∈ Γ with k(g) = L, a
generator of the image of k: k(g) has order m in Z_P, and since k is a homomorphism, m divides the order of g.
Hence m ∈ {1, 2, 3, 4, 6}. (4) If g(c) = c, then (F^{t+L}x₀)(c) = (F^t(g·x₀))(c) = (g·F^t x₀)(c) =
(F^t x₀)(g⁻¹c) = (F^t x₀)(c). ∎
The hypothesis that step (3) uses is that G consists of lattice symmetries, affine maps whose linear part lies in
O_h; a permutation of B that preserves the neighbour graph but is not of this form is not covered. (The
repository's first version, `research/clockwork/README.md`, stated "for a subgroup of O_h" without step (3); the
step was written out on 2026-11-14 there and here.)
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
**[proved, by stepping]** (Z12; A for the periods and cell periods, re-derived by a stepper written from the rule
alone; C for their absence from the box-census lists) Five oscillators new to the catalogue were found among the
settled states of lifetime runs (Section 12): C9.24a, C9.28a (period 9), C11.29a (11), C13.24a (13) and C52.33a,
a compound of period 52 = 4 × 13 with no cell of period 52 (24 still cells, 4 of period 4, 14 of period 13).
**[measured]** (Z9; B + A) Among the remaining objects, twisted loops are a steady 3–8% at every loop length
(295 of 9,278 with L ≥ 3; 30 of 670 with L ≥ 7; 9 of 120 with L ≥ 12; 5 of 66 with L ≥ 16), so the twist
multiplies ordinary loops rather than selecting long ones; the longest untwisted loop found is C35.29a (L = 35).
**[measured]** (Z10; B: re-run by a second agent on the producer's seed) P66.27a is reached from 4.1 × 10⁻⁴ of
the random states of its own box, and single-cell perturbations destroy it more often than not (30% of 6,600
heal). No object found in these censuses carries or gates a signal; Section 8.1 constructs objects that do.

Figure 5 (placeholder; does not exist): *P66.27a at phases 0 and 33, layer by layer.* A text rendering is
produced by `engine/target/release/gump show --cells research/clockwork/views/P66.27a.cells --orbit`.

### 8.1 Signals

No finite pattern moves through empty space (Theorem 2), so a signal needs a medium: something periodic along a
line that a defect can run along. A sustained search for one (`research/signals/README.md`; objects in
`research/signals/objects/`) found media by constraint search, none of them among the objects soup had given. Every
object below is stated with what verifies it. *Oracle-verified* means that a verifier stepping only
`reference/oracle.py` reproduced the claimed state cell for cell; every such verifier was re-run by the lead, and
two adversarial reviews (`research/audit/REVIEW-signals.md`, `research/audit/REVIEW-signals-2.md`) rebuilt the
objects with steppers of their own, each matched to the reference. Vocabulary: a *wire* is a pattern periodic along
one lattice vector v and bounded across it; a *unit* is one repeat; a *pulse* is a defect that moves along the wire
and leaves it as it was; a *front* leaves a different wire behind (it uses the medium up). All wires here run along
(1,0,−1).

**Pulses.** **[measured]** (SG1; A: three codes on the reference) Wire B is a free-standing period-2 wire of 5 cells
per cube. Flip two of its cells at an even generation and the flip moves one cube every two generations, half the
speed limit, for as long as it is followed; the state is the bare wire with the moved defect and nothing else. The
mirror pulse runs the other way; pulse A is 5 cells on another period-2 wire (6 cells per cube); pulse S is 32 cells
on a still wire. Every pulse found has period 2 and shift 1. The pulses translate exactly on rings of 9–64 cubes, on
box tori and on the reference's cubic torus, and on a 600-cube finite wire in the infinite lattice, with no torus at
all. On the period-19 wire W00 a single flip starts a front instead. (`python3 research/signals/verify_pulse.py
research/signals/objects/pulse-B.json`, likewise `pulse-A`, `pulse-S`, `pulse-B-left`; the lead's separate check
`python3 research/audit/signals_lead_check.py research/signals/objects/pulse-B.json`.)

*Two remarks* **[proved; no ledger row]** (README §4; the first review found the first argument incomplete as
written, and it was repaired). A wire cannot grow at its end: with D the body diagonals d with d·v < 0, Theorem 2
holds the wire in every half-space d·p ≤ C_d, and −v is a non-negative combination of the elements of D, so the
support never passes a plane perpendicular to v; fronts burn wire, and nothing lays track. And a pulse on a wire of
period ≤ 2 without a drive of its own carries its drive (Theorem 5 applied on a ring, with the shift symmetry): pulse
B has one overcrowded cell per generation, dead at the time, the bare wires none.

**A transmission, with a capacity.** **[measured]** (SG2; A: rebuilt by the first review with its own code on rings
of 48 and 96) Flipping one cell of wire B at a sender A emits a pulse; a receiver d cubes away, a wall between wire B
and a second period-2 wire B′, swallows it and moves one cube toward the sender, the line between left exactly as it
was and an untouched control unchanged. It works d − 1 times (35 shots over 36 cubes; the study had run six); the
next shot, with the receiver beside the sender, sets the line on fire. The receiver is a unary counter with a
capacity, not a line that can be used indefinitely. Of the 84 one-cell flips of wire B, 74 heal, 2 leave a standing
defect, 2 emit a pulse (one each way) and 6 start a front. (`python3 research/signals/verify_transmission.py
research/signals/objects/transmission-B.json`.)

**Interaction.** **[measured]** (SG3; A: the first review's code, every separation 2–44) Two pulses of wire B meeting
head-on pass through each other without delay at odd separation and stop each other at even separation, leaving a
3-cell standing mark; on rings of 64 and 65 parity is the whole rule for head-on pairs. Pulses going the same way run
as rigid trains at any spacing.

**Bounds of the first search.** **[measured, constraint search, no certificate]** (SG4; A for the 2 × 2 and 2 × 3
rows, where a transfer-graph search sharing no code agrees on every row both answered; B for the 3 × 3 rows and the
fronts) In closed tubes along (1,0,−1) with a background repeat of one cube, no pulse of any width exists in the
2 × 2 tube for the twelve (period, shift) pairs tried, nor in the 2 × 3 tube for nine pairs and (6,5), where only
(2,1) pulses exist; the 3 × 3 rows rest on one SAT encoding. A single flipped cell starts a front in 14 of the 18
distinct wires on file and a pulse in none.

**Theorem 8 (a clock of every length) [proved, computer-assisted]** (SG5; A: the proof read and its enumeration
redone by a second agent with its own code; three codes on the reference at 24 lengths from 1 to 257). Wire C (five
cells per unit) of N units between two caps is a free-standing object K_N of 32 + 5N cells, stationary with period 2.
For every N ≥ 1 there is a finite pattern in empty space, K_N with a rake running between the caps (a rake is one
added cell, below), whose period is exactly 4N + 2. (At every length stepped on the reference no cell is ever alive
outside the diagonal hull of K_N.) Hence gump has free-standing oscillators of every period 6, 10, 14, …, every
period ≡ 2 (mod 4) from 6 up: periods are unbounded, which answers open problem 12 of `research/OPEN-PROBLEMS.md` (periods beyond 66, Section 8).
*How it runs* (README §11, measured). The rake runs to one cap laying a train of left-moving pulses behind it; the
cap turns it into the mirror rake, which runs back laying a train of right-moving pulses; the other cap turns it
again; each cap swallows the train aimed at it and is as it was after each pulse. Travel takes 2N generations each
way and the two turns 2.
*Argument in outline.* Write a unit as the cells with x in {2u, 2u + 1}. A cell's neighbours lie in its own unit or
the adjacent ones, so the step of a stretch of units depends only on that stretch and one unit either side (the
light cone; the second review re-derived it). Lengths below 8 are stepped on the reference. For N = 8 + j the cycle
is assembled from the computed cycle X(s) of the base clock of length 8 (period p = 34) by cutting the wire at unit
m = 4 and inserting j units: at unit m + i the new state shows the base's unit m at a base time c_i(t) that runs as
t − 2i, repeats a four-generation loop j − i times when the rakes have passed at one time t_a and i times at a
second time t_b, and runs on, so that the period is p + 4j = 4N + 2. Five finite checks on the base make this an
orbit: two (B1, B2) that the strip [m − 1, m] two generations earlier (B1) or later (B2), moved one unit on, equals
the strip [m, m + 1], over stated ranges of s; two (B3, B4) that the base states at t_a + 1 and t_a − 3 agree on the
units at or below m + 1, and at t_b + 1 and t_b − 3 on the units at or above m − 1, which is what the loops need;
and one (B5) that the strip [m − 1, m + 1] repeats only once per period, which gives the least period. With B1 and
B2 neighbouring charts agree where they overlap (the cases are listed in order of t in the README), with B3 and B4
every chart's time advances by one except at loop-backs whose states agree on what that chart supplies, and so by
the light cone the assembled sequence is an orbit. Full proof: `research/signals/README.md` §11 and `python3
research/signals/prove_clock.py 8 4` (1 s; it also passes with bases 12 and 20, enumerates all chart pairs for
j ≤ 40 and steps the assembled orbit for j ≤ 6); checked in `research/audit/REVIEW-signals-2.md` §1, whose own
script (`research/audit/signals2/prove_check.py`) redoes the enumeration for up to 150 inserted units on a base
computed by the reference. *Not proved* (measured): that adding the one cell leads into this cycle for every N. On the
reference at 14 lengths up to N = 257 and with the reviewer's stepper for every N up to 400 it does, after a
transient of exactly max(N − 2, 0) generations. Other caps give shuttle clocks too, all of period 4N + 2; no period
divisible by 4 was found in the family, and no reason is known.

**A rake and a collision gate.** **[measured, oracle]** (SG6; A: the gate by the lead's own code at twelve
separations, the rake by the second review's code at separations 3–22) One cell added to wire C is a *rake*: it
moves a unit every 2 generations and emits a pulse every 2 generations, and a pulse met head-on is swallowed or
stops it, by parity. Two pulses of wire C meeting head-on: exactly one survives, undelayed and unchanged, and the
wire is as it was; the left-mover survives at even separation, the right-mover at odd. With inputs L and R (a pulse
sent from either end) and outputs read further along the same two lines, the element computes (L, R ∧ ¬L) at even
separation and (L ∧ ¬R, R) at odd: one line inhibits the other, reusably and without delay. It is an inhibition
element whose outputs leave along its input lines (the second review's wording; the study called it a gate): there is
no third line and no crossing. On wire B, by contrast, both pulses pass or both stop.

**A counter.** **[measured, oracle]** (SG7; A: rebuilt by the second review with its own code, which found its range)
The wall between wire B and wire B′ moves one unit towards whichever side a pulse arrives from; written by a
one-cell flip on one side, erased by one on the other. It has sixteen positions and breaks when the wall reaches the
write or the erase site; it takes a pulse arriving 1 to 31 generations after the last, but two writes 2 generations
apart fail. The study's "register" is this bounded counter; it is not a toggle, and no receiver that toggles on
pulses from one side was found (below).

**Theorem 9 (the tape) [proved, computer-assisted]** (SG7; A: the proof checked and 36 more words run on the reference
by the second review). Every sequence of units of wire B and wire C, on a ring or infinite, moves rigidly towards −v
at one unit per 2 generations. *Argument.* Two generations reach two units either way, so what a unit becomes after
two generations is decided by a window of five units, itself and two on each side. A ring of 40 units whose word
contains all 32 windows of five letters over {B, C} moves rigidly on the reference, so every window maps as the
statement requires, and hence so does every word. Full argument: `research/signals/README.md` §10 ("The tape");
`python3 research/audit/signals_lead_check.py research/signals/objects/tape-BC.json 20`; review
`research/audit/REVIEW-signals-2.md` §5. Read this way, a left-moving pulse of wire C is one unit of B in it and a wall
between B and C is a front. Of all 120 pairs of the 16 unit types of the family, only {B, C} moves.

**Where carriers come from.** **[measured]** (SG8; B: reproduced on other seeds with the second review's stepper,
12,789 / 368 / 10 / 305) Of 100,000 soups in the 3 × 3 tube, 12,780 settle into uniform wires of period ≤ 2 (366
distinct), ten of which carry a 2-cell pulse; the carriers came from 279 soups. But almost all were on rings of one
unit, where the "soup" is one random unit of 14 cells repeated, a few on rings of two, and none in 60,000 soups on
rings of 3, 4 or 6 units. So a random unit repeated along the tube settles into a pulse-carrying wire about once in a
few hundred; the study's "born from soup" was nearly all one-unit rings (the second review's correction), and nothing
shows that soup with no imposed repeat makes a carrier.

**A wire against chaos.** **[measured]** (SG9; B: the second review's stepper, other seeds, block sizes and densities)
Living chaos destroys a wire it touches: on 800 of 800 sides in the study and about 1,500 more in the review, with
one exception. The fire runs at pulse speed for wire B, and for wire C at density 0.4; at lower densities many sides
of wire C burn at half that speed (the review's correction: fire speed depends on density). On a few sides in a
hundred of wire C a clean pulse leaves the chaos ahead of the fire, the first pulses here to come out of anything
random, with the fire behind it. **[proved]** The gap that isolates order from chaos for ever is three empty diagonal
layers, Theorem 3. Two are not enough in general: a wire running past chaos two empty layers off is hit at
generation 2 in 20 of 20 soups (measured, SG9). Two suffice only for the capped end of wire C in the geometry the
study ran, where a count of the cells that could couple the two sides shows that none can be born; the study's "two
empty layers isolate a wire" is corrected to this (the second review). Nothing sent into chaos could be read on the
far side, because nothing survives the contact.

**Absent inside stated bounds.** **[measured, exhaustive inside the bounds]** (SG10; B: brute force gives the same
caps cell for cell at the two smallest planes, a second solver reproduces the UNSATs, odd delays added) Among caps of
period 2 inside the 3 × 3 tube there is no restoring reflector for a pulse of wire B or C, no cap of wire B that
reflects or toggles (a complete census to plane 33), and every cap of wire C that reflects a pulse is changed by the
reflection. Not excluded: caps of period above 2, caps outside the tube, a reflector whose cap is still settling when
the pulse returns. The tube is too tight a search space in any case: pulses of wire C that reach outside it were seen
leaving chaos and are in the study (README §10; no ledger row).

**Open.** A corner between two wire directions; a closed polygon; a crossing; a reusable reflector; a gate with its
own output line; a stationary source of pulses; a receiver that toggles on pulses from one side; a clock whose period
is set by its length and divisible by 4; whether the clock's one-cell ignition leads into its cycle for every N; whether soup without an
imposed repeat makes a carrier. The prior art for these objects has not been searched (Section 11). Further work on
signals is in progress and is not reported here.

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

**A two-dimensional analogue.** **[measured]** (G1; A for the slope of the law only, as the ledger scopes it: an independent stepper at L = 12–24
gives slope 0.42) On the square lattice with the range-2 cross neighbourhood (±1,0), (±2,0), (0,±1), (0,±2), the
rule B34/S234 ("alive next iff n + x ≥ 3, except that n ≥ 5 dies") is gump's construction one dimension down. It
has steady chaos at density 0.472, and in strips 16 deep and periodic along the edge a whole edge row dies after
a memoryless wait with

$$\ln \tau_{\rm edge} = 0.73 + 0.416\,L, \qquad L = 12\text{–}36,$$

τ_edge from 286 to 5.8 × 10⁶ generations. **[proved]** (G2; B for the brute-force checks, re-run by a second agent;
the proofs, in the study, were re-derived by a second reader by hand in part only) It is confined to its bounding
box, three dead rows are a firewall, the threshold lemma holds with exceptions exactly at overcrowded cells, and no
finite set is sealed. *Preliminary* **[measured]** (G3, G4; C): a mirror perpendicular to the edge multiplies the
slope by 0.42 and full square symmetry by 0.50, but a forecast that symmetries fixing no edge cost nothing failed
for four-fold rotation; no capped-threshold rule on the Moore neighbourhood sustains confined chaos. **[measured]**
(SW4; B: re-run by a second agent on the same seed sequence) An edge with a two-cell dead notch has slope 0.346
against 0.412 for the intact edge. The 2D slope is 0.416; twice the 3D periodic-face values 0.2072 to 0.2131
(Section 7; the top value was 0.2125 before the 4 × 4 anchor was corrected, Table 8) is 0.414 to 0.426. Whether this is more than a coincidence is not established, and given Section 7
neither number is an asymptotic constant.

**Other lattices.** **[proved]** (ledger K9, the class study; A) Confinement is a property of half-spaces (Section
3). **[measured]** (K4; B) On the face-centred cubic lattice with 12 neighbours, B45/S345 has a memoryless slab
face law with slope 0.181 ± 0.001 per face cell. The variant of the present rule with edge-sharing coplanar
neighbours is likewise confined (to a box), chaotic, and dies a wall at a time, and is not treated here. A study of
which capped-threshold rules on which lattices behave this way was reviewed adversarially; its theorems stand (K4;
B), and its measured regularity is that, given confinement, no finite sealed set, no immortal wall and a chaotic
bulk, the outer layer dies as a whole after a memoryless wait roughly exponential in its area (42 of 50 lattice–cap
pairs by a scoring rule fixed in advance). *Preliminary* (K7, K8; C): on a honeycomb-based lattice the wall law is
concave rather than linear, and on a bond lattice boxes outlive the forecast from the slab law by a factor of about
10⁶ because adjacent walls hold each other up along their edges. Nothing known predicts which rules are chaotic or
how strong the law is.

Figure: `research/figures/phase_rulemap.png` (the 960-rule survey), `research/figures/toy2d_law.png` (the 2D
edge law).

## 10. What is proved, what is conditional, what is open

### 10.1 Proved without conditions

Theorems 1–6 and Proposition 7 of Section 3; the half-space criterion for confinement; the twist lemma; the
exhaustive enumerations of Section 8 at the sizes that have been re-run (Z1, the smallest still lifes; Z2, the
still-life counts for n ≤ 15; Z3, the period-2 classes with unions up to 13; Z4, no period-4 oscillator with
union ≤ 10); the anatomy of P66.27a; the reduction of a symmetric state to gump on its orbit graph and the
list of mirrors inside a face (S5, Section 5.5); Theorem 8, a free-standing clock of period exactly 4N + 2 for
every N ≥ 1, so that periods are unbounded (SG5; computer-assisted, the proof checked and its enumeration redone by
a second agent), and Theorem 9, the tape on which every sequence of units of wires B and C moves rigidly (SG7; the
same), Section 8.1; the two remarks on wires there (no growth at a wire's end, a pulse carries its drive), which
have no ledger row; and the exact state counts of Section 6.1 for the seventeen vessels enumerated independently
(SS1). None of these says anything about lifetimes beyond the trivial bound that a seed with a hull of N cells is
periodic within 2^N generations, which is exponential in the hull's *volume*. Not proved, though measured to
N = 400: that one added cell leads the clock into its cycle.

*Preliminary* (exhaustive computer enumerations graded C: each has a command and has not been re-run): the
still-life count for n = 16 (Z2); the statement that every period-2 oscillator with union ≤ 11 is a hinge flip
(Z3); no period-3 oscillator with union ≤ 12, and the smallest period-3 union exactly 13 (Z4).

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
is quasi-stationary over the window, censoring is at most c times the hazard, and the low-set weight
w = Σ_{z<K} p_z ψ(z) ≤ 1/(2(1 + c)) with ψ(k) = e^{−θ₀(k − k₀)⁺}). Then the
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
dies after an exactly geometric wait from its quasi-stationary law, with mean τ_L ≤ 3·8^L (L ≥ 5), and, with row 0 started full, τ_L is at least
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

1. **Why area.** No proof that the wait is exponential in the face's area exists for gump, for the 2D analogue in a
   vessel run by the rule, or for the finite-depth noise-driven models of Section 6. A dedicated theory effort by
   several independent lines ended without one.
2. **The constant, or two.** It is not derived from the rule. It is also not yet *measured* as an asymptotic
   constant: wrapped faces of one shape cost 0.2084 per cell from 63 cells up, after a kink near 61 cells that no
   smooth correction fits, and the local slopes of octahedral faces rise away from that value (Section 7.5), so
   whether the two families have one price per cell or two is open; why the kink, and whether the line holds beyond
   93 cells (the 93-cell value has one code), are open too. No flat face without periodic identification or rim has
   been measured. One conjectured value exists, a quasi-potential of a measured one-step table with a
   stated continuation, 0.2191 per cell at A = 84 **[conjecture]**. So are the thin face's limit and its ratio to
   the wide face's (Section 7.4).
3. **Shape.** Whether the equal-loop differences of periodic faces are a commensurability effect that vanishes on
   large faces (Section 7.2; the test is A = 84), and why octahedral faces are tougher than periodic ones.
4. **Symmetric faces:** whether the slope is exactly the asymmetric one divided by 6 (within 5% is supported);
   how much of the √A term a diagonal mirror carries (up to about a third is not excluded); whether the rim term
   bends, and so whether −0.196·√A is asymptotic (a T_d ensemble at A = 759, on a GPU, would speak to it); why
   faces tied across an edge die sooner (the dying faces, looked at in Section 5.6, show a tied rim thinner at all
   times and no dynamical holding-up; whether the thinner rim causes the cost is not shown); the difference between vertex- and cube-centred hulls, which is not a constant factor; and the
   excess length of the side-16 cube's plateaus (Section 5.7).
5. **Infinite volume.** Whether the chaotic state is stable or only metastable on the infinite lattice; whether
   one- and two-layer slabs cannot sustain chaos (reduced in `research/theory/thickness.md` §4 to a percolation
   statement, unproved).
6. **Hypothesis (R)** of Section 10.2(a) from the rule.
7. **Fauna and signals.** Periods beyond 66 (open problem 12 of `research/OPEN-PROBLEMS.md`) are answered by
   Theorem 8, and signals exist (Section 8.1). Open: a clock whose period is set by its length and divisible by 4
   (every one found is 2 mod 4; small oscillators with such periods exist, Section 8), and odd periods beyond those
   of the fauna (`research/OPEN-PROBLEMS.md`, problem 12); a
   corner between wire directions, a closed polygon, a crossing; a reusable reflector; a gate with its own output
   line; a stationary source of pulses; a receiver that toggles; whether the clock's one-cell ignition works for
   every N; whether soup with no imposed repeat makes a carrier wire.
8. **Rule space:** what makes a capped threshold chaotic at a given cap; how strong the wall law is.
9. **The dying face below half its population.** Whether a depleted face holds a remnant in some looser sense than
   a patch at fixed density (not reachable on faces of 108 cells or fewer), and what shape the dip curve has below
   half the population: there is no model for it (Section 5.6).
10. **State space beyond 30 cells.** Whether the visited counts grow linearly or slowly exponentially at small
   sizes, where they join the face law, and whether hulls wider than 6 layers hold longer transients (Section 6.1).

## 11. What is new here and what is not

This section relies entirely on the project's prior-art survey (`research/PRIOR-ART.md`: two search passes on
2026-11-13; a third pass on 2026-11-14 aimed at the boundary layer over noise, the shape of a periodic face and
sealed sets; and an adversarial review of that third pass, which tried to refute each "not found" and overrides
the pass where they differ) and the theory effort's library (`research/theory/swarm/library/shelf.md`, §§10–11
for the 2026-11-14 works). The survey was made by web search with a lossy fetcher and no citation index (one
citation list was obtained, for [CG99]); several key sources could not be opened (notably the review [TL08]); and
"not found" below means not found by that survey, nothing stronger. How far each work was read is in the
References.

| result | nearest known work recorded | judgment |
|---|---|---|
| The automaton itself (faces of the cubic honeycomb, this neighbourhood) | No automaton on this vertex set found in two searches. Near misses: 12-neighbour sub-neighbourhoods of the Moore neighbourhood (the fcc lattice) on LifeWiki's cubic-honeycomb page [LW-CH]; Life on kagome and other Archimedean lattices, in 2D [G]; the same lattice studied as an antiferromagnet, not a cellular automaton [arXiv:1510.05924] | **Not found in our search** as a cellular automaton "on this lattice" (not "with 12 neighbours"). Not a result in itself |
| Confinement to the diagonal hull, no spaceships (Thm 2); firewalls (Thm 3); kagome sub-automata (Thm 4) | Eppstein [E09]: no births on 1–3 neighbours implies confinement to the bounding box for Life-like rules; a bounding-diamond argument of the same shape for some B3 rules. LifeWiki [LW-OT]: rules with lowest birth ≥ 4 never grow beyond their bounding box. For the firewall: blocking words [BT00, after Kůrka], a word whose occurrence "completely disconnects coordinates to its right and left"; in d ≥ 2, blocking patterns [AC25, definitions; the thesis they cite not obtained]; an empty strip orthogonal to stable directions stays empty under monotone bootstrap rules [BSU15] | **New instances of known principles.** The method is not new, and the firewall is a blocking word of the simplest kind (constant image "dead"), read along one direction with layers as letters. The {111} half-space on this lattice, the octahedral hull that only shrinks, and the three-layer threshold were not found stated. Possibly ours, narrowly: a blocking set for a non-monotone rule whose blocking letter is the quiescent state, in 3D on this lattice. (The survey's second pass could not re-read [E09]'s body) |
| Threshold lemma with the exact identity ΔE = D − Q (Thm 5) | Period-two theorem and energy for symmetric threshold networks [GO80, GO81, GFP85], read only through [KMMK11, GMRS23] | **Standard theorem, applied.** The observation that a capped rule is a symmetric threshold network except at overcrowded cells, with an exact drive term there, was not found; it is elementary. [citation needed: whether energy identities with a drive term for capped or bi-threshold rules are in Goles–Martínez or later work] |
| Sealed sets; no finite sealed set in ≥ 3 layers; finite sealed sets in 1 and 2 (Thm 6) | The largest dead sealed set is the 9-core of the dead cells, equivalently the complement of the live set's closure under threshold-4 bootstrap percolation (Remark after Thm 6); k-core and bootstrap percolation are complementary [Mil16, k-core and bootstrap sections read]; blocking words [BT00]; in freezing automata the frozen set grows by definition of the class [GMMO19, STT21, abstracts only]; Gravner–Griffeath's subcritical class, "closed cofinite proper subsets", quoted in [BSU15] (Gravner–Griffeath's own papers not read) | **The object is classical.** "The largest sealed set only grows" follows from the definition (comparison with the monotone rule U) and is a remark, not a result; no sentence stating it for a non-monotone rule was found, which we do not count as novelty. Possibly ours, narrowly: the lattice-specific facts, namely no finite sealed set from three layers on, the hexagon ring in one layer and the 36-cell set in two. Elementary. Not searched: Boolean-network frozen cores and trap spaces |
| Memoryless collapse with mean lifetime exponential in size (Section 5.2) | Supertransients [CK88, WS03, HKTP10, TL08] and stable chaos [PT09]: numerical only. [HKTP10] reports τ(L) = exp(AL + B), Poisson statistics, and collapse only with non-periodic boundaries through boundary layers of fixed thickness. For stochastic monotone systems the analogue is a theorem: the finite contact process [DL88, DS88, M93, M99, MMVY12]; exact exponential law from a quasi-stationary distribution [MV12]. Death through the boundary: for spiral-defect chaos the death rate is proportional to the length of the non-conducting boundary and τ is exponential in the area [VR19, abstract and relevant sections; R22, full text] | **A new instance of a known phenomenon**, and boundary-controlled death is an instance of a known result [VR19, HKTP10]. Not found in our search, within it: (i) confinement and firewall are theorems, so collapse proceeds by irreversible layer events that can be timed one by one; (ii) the exponent is set by the area of one face of a three-dimensional vessel whose walls are theorems, not the volume; (iii) a deterministic cellular automaton with an absorbing state (none in the sources read) |
| Death as the end of the quasi-stationary tail, measured to one cell (Section 5.3) | The flux identity 1/τ = Σ_r W_r π_r [AM17, §2 read, eq. 6]; QSD theory [MV12, DS65]; the same relation in deterministic spatially extended transients, each with a measured distribution: spiral-defect counts T(N) = 1/(Z p(2)) [SK15, §§I, III, IV read], 1/τ = W₋₁(1)P_qs(1) + W₋₂(2)P_qs(2) checked against simulation [VR19], pipe-flow puffs τ_d = δt/P(h_th) [NA21, §§1–3 read], extreme-value view [GGG10, abstract only]; the SIS form 1/(μ₁q₁) [N11, not obtained]; large deviations in cellular automata [BGPV19] | **An instance of a known result** (the quasi-stationary flux identity), with precedents in deterministic systems. Possibly ours, narrowly: the count followed down to a single cell (ln p_k linear to k = 1) with the exit rate measured rather than fitted, in a deterministic automaton. That narrower form was not found in our searches |
| The exponent is made in five or six layers over independent noise (Section 6) | Window of a chaotic coupled map lattice driven by white-noise boundary inputs reproduces the bulk's statistics [CG99, read in full; its 12 citing works, read as titles, have none on lifetimes]; "thermal bath" inputs [dS08, abstract as paraphrased]; deterministic CML "behave like stochastic models" [MvHB02, abstract]; boundary layers of fixed thickness, lifetime still fitted in the whole length [HKTP10, now read in full]; boundary-controlled death [VR19, R22]; dice models of deterministic networks with lifetime e^{cn} (monotone) [CD11, MV10]; probabilistic cellular automata [LMS90, MST19] | **The method is an instance of a known one** ([CG99], in mirror image: they randomise the outside of a window, we the inside of a boundary layer), and that death enters through the boundary is known [VR19]. **Not found in our searches:** a reduction of a transient lifetime to a thin layer over noise, or any comparison of lifetimes or escape rates with the chaotic interior replaced by noise. The review [TL08] and a 2007 paper on noise and the collapse of spatiotemporal chaos (seen as a search result only) were not read |
| Symmetric initial conditions die exponentially sooner (Section 5.5) | Nothing found on lifetimes. Life lexicon: symmetric soups produce different objects [LL-soup]; symmetric soup censuses (apgsearch, Catagolue) were seen in search results only, not opened, and are not citable | **Not found in our search** as a quantified result. Conceptually close to standard symmetry reduction, which is what S5 proves here (a symmetric state is gump on its orbit graph); the edge ladder (each edge tied to a neighbour that dies at the same moment costs about the same) was not searched for |
| Lifetime of a periodic face depends on its shape at fixed area (Section 7) | Proved for equilibrium tunnelling: zero-field Ising/Potts on a K × L torus, exponent 2·min{K, L} + 2 with an exponential limit law [NZ17, §§1–2 read]; tunnelling splitting through a 3D Ising interface on a periodic L1 × L2 cross-section depends on L1/L2 at equal area [CGV93, read in full]; droplet shape transitions on tori [NH03, abstract]; surface-code failure controlled by gcd of the lattice dimensions [T19, abstract only]; critical thickness for 3D transients [LCP17, abstract only]; plane-Couette lifetimes against box size with shape not separated [Man09, a miss]; holes of equal measure with different escape rates [BY08], escape-rate formulae [KL08] | **The shortest loop of a torus controlling an exponential time is an instance of a known result** (equilibrium tunnelling, [NZ17] at leading order, [CGV93] in the prefactor). **Not found in our searches:** a dependence of a chaotic-transient, turbulent, nucleation or extinction lifetime on aspect ratio or twist at fixed size; a second shape variable (none was found in our data either: Section 7.2). Possibly ours, narrowly: the twisted-torus census for a chaotic transient, with the refutation of every law in area and shortest loop and of five candidate second variables. The analogy with [BY08] is ours and is untested |
| Period = twist × loop; statistics of twisted oscillators (Section 8) | Period and "mod" in Life catalogues, including thirds and sixths on hexagonal and triangular grids [LW-Mod]; trivial versus non-trivial oscillators [LW-NT] | The lemma is a **re-expression of period/mod**. The three-dimensional screw twists and the statistics were not found in our search |
| Conditional area law; hazard identity (Section 10.2a) | The quasi-stationary flux identity in its Markov form [AM17, eq. 6]. Not surveyed otherwise. [citation needed: committor and flux identities in transition-path theory; the project's library has none] | Unknown. The identity is of a standard kind; its use without a Markov property, and the reduction of the area law to a one-step hypothesis on a pooled table, may or may not be known |
| Exponential law for the automaton 𝒜(L) (Section 10.2b) | Comparison with oriented percolation [L95, BBS94, HS22]; the one recorded non-monotone cellular-automaton survival theorem is [BN94] (not obtained); no finite-size exponential-lifetime theorem without monotonicity was found | A **constructed example** using standard tools. Honest but artificial: a random tape read once |
| Minimality of the rule among its neighbours; the class (Section 9) | Survey of 6,144 outer-totalistic rules with metastable states and nucleation [RK14] | Survey-level; a new instance |
| Signals on free-standing wires: pulses, transmission to a counter, the inhibition element, the clock of period 4N + 2, the tape (Section 8.1) | **Not searched.** No pass of the survey addressed signals, wires, collision logic, or constructions of oscillators of every period, in this or any other automaton | **Unknown.** Nothing here is claimed as new; the objects may be instances of known constructions, and a search is owed before any judgment |
| How much of its state space a seed explores (Section 6.1) | **Not searched** (transient lengths and in-degree statistics of finite automata and random maps were not surveyed) | **Unknown.** The exact counts are small-vessel enumerations; the 0.30 bits per face cell is the face law restated |

**Ranking.** The four results we judge most likely to interest a reader who knows cellular automata and
metastability, with what each still lacks before it could carry a paper. Revised 2026-11-14 after the third
search pass and its review; the order is unchanged, the claims attached to each are narrower, and each item says
why it stays. Revised again 2026-11-15: unchanged, because the new results change what items 1 and 2 lack, not their
standing, and the shape dependence did not meet either condition for joining (below).

1. **The face-extinction law in an automaton with proved confinement** (Sections 3, 5.2, 5.3). *Why:* it is a
   supertransient whose collapse is decomposed by theorems into irreversible events, measured over more than
   twenty units of ln τ; it is simple enough to be a model system for proofs. *Why it stays first:* the new prior
   art takes from it the tail relation (an instance of the quasi-stationary flux identity, with precedents in
   [SK15, VR19, NA21]) and boundary-controlled death [VR19], but nothing found has a face-area law in a vessel
   whose walls are theorems. *Missing:* the law is measured, not proved; the constant is not derived and not
   isolated: wrapped faces of one shape give 0.2084 above a kink, hull faces' slopes rise away from it, and one
   price or two is open (Section 7.5); nothing at A ≥ 108 has a second implementation or a
   bound on missed settled replicas (Section 12; a guard now exists, with a stated limit, and no run at those sizes
   has used it); the top point has 16 deaths; the review [TL08] and the primary
   supertransient papers must be read by a person before any claim of novelty for "area, not volume".
2. **The exponent is made in a boundary layer over noise** (Section 6). *Why:* it turns a question about
   deterministic chaos into one about a finite-depth probabilistic automaton, where the tools that prove
   exponential lifetimes for stochastic systems might apply; it was confirmed by independent code and by a
   forecast. *Why it stays second:* the method has a mirror-image precedent [CG99] and death through the boundary
   is known [VR19], but the reduction of a lifetime to a thin layer over noise was not found in two searches, one
   of them adversarial; the thinnest face needs the same five layers (Section 7.4).
   *Missing:* sizes beyond A = 84; an account of the 0.03–0.04 offset for octahedral faces;
   any theorem for the noise-driven model; [TL08] unread.
3. **Symmetry shortens lifetimes exponentially** (Section 5.5). *Why:* it is simple to state, large (a symmetric
   face of 759 cells lives like an asymmetric one of about 100), explains a visible feature of the 2012 runs, and
   was not found in the literature searched. *Why it stays third:* the 2026-11-14 searches did not address it, and
   the result of 2026-11-15 corrects its explanation rather than its size: the cost is mainly that faces sharing an
   edge die together (about 2.15 in ln τ per edge, additively, two codes), not a cost along mirror lines; that is
   cleaner to state but rests on one vessel at A = 63 for the ladder. *Missing:* the asymptotic slope is not
   determined (free fits 0.024–0.044 per cell; "c/6 within 5%" only); whether the √A term is asymptotic; the
   mechanism (the dying faces have now been looked at, in one vessel at A = 63, Section 5.6: a tie thins the rim at
   all times and makes each step down a dip likelier, and nothing shows that this is the cause); the general "volume over group order" statement is grade C; in the 2D
   analogue a forecast for rotations failed and is not understood.
4. **The structure theorems as a package** (Section 3): confinement and firewalls, the exact energy identity, and
   the sealed-set dichotomy at thickness three. *Why:* complete proofs, short, and they are what makes the rest
   measurable; this is the only part that could be written up as it stands. *Why it stays fourth, and narrower:*
   its interest was always as a foundation, and the review shows the firewall is a blocking word and the sealed
   sets a 9-core, so what remains ours is lattice-specific (the {111} half-space, the three-layer threshold, the
   one- and two-layer sealed sets). *Missing:* a reading of [E09] and of the Goles primaries to place Theorems 2
   and 5 correctly; the proofs have been re-derived by independent automated readers and brute-force checked,
   and have not been read by a mathematician.

The shape dependence of Section 7 stays outside the list: it is the most thoroughly cross-checked measurement in
the paper, but as it stands it is a refutation (no law in area and shortest loop) without a replacement, and the
searches now show that the shortest loop as the controlling length is a theorem in equilibrium [NZ17], so what
could be ours is narrower (fixed-area shape and twist for a chaotic transient). It would have moved up the list
if the second variable had been found or the thin-torus cost computed exactly; neither happened (Sections 7.2,
7.4). The kink in the wrapped-face line (Section 7.5) does not change this: it is one measurement on one family,
with its largest point on one code.

The signals of Section 8.1 and the state-space counts of Section 6.1 are not ranked, because their prior art has
not been searched at all (`docs/paper/GAPS.md`, gap 50). The clock and the tape are complete proofs, and would be
candidates for the list only after such a search.

## 12. Methods and reproducibility

**Implementations.** A reference implementation in numpy that reproduces the 2012 code's semantics, including its
array-index torus; a bit-sliced engine; bit-sliced replica steppers on arbitrary cell graphs; an orbit-reduced
stepper for O_h-symmetric states; two GPU kernels. Acceptance rule: a stepper's numbers are used only after it
agrees bit for bit with the engine or the reference over thousands of generations on several vessels
(`research/check.sh`, 20 exact checks). The GPU kernels were checked by emulating them on a CPU against two CPU
steppers, with deliberately broken kernels as negative controls; that the GPU executes the kernel as the
emulation does cannot be checked without a second GPU run. A second card (the owner's GTX 1080, a different GPU
model, run by a separate session; its code, on branch `claude/gpu-local-1080`, pull request 23, is not yet merged)
has since passed the same acceptance checks on its producer's report, with the port checked line by line by a
reviewer but not its execution. It measured the five equilateral tori of Table 8a; four of them agree with a CPU code
(GL1, GL3; A), and one, the 5 × 5 slab, repeats a value of the first GPU (Table 6: 15.661 ± 0.003; the card
15.6630 ± 0.0023; a CPU stepper 15.667 ± 0.010). No other GPU result quoted in this paper has been repeated on it.
*Verifiers judged by the reference.* Every object of Section 8.1 is checked by a script that steps only
`reference/oracle.py` and compares whole states cell for cell (`research/signals/verify_*.py`); the lead re-ran
every one and wrote separate checks from the reference alone (`research/audit/signals_lead_check.py`,
`signals_clock_lead_check.py`, `signals_gate_lead_check.py`). The state-space enumerator was matched to the
reference on every vessel, and the lead enumerated one 16-cell hull with the reference itself
(`python3 research/audit/statespace_lead_check.py hull_-1_1_-5_-1_-5_3_-3_5`, 40 s).

**Estimators.** Mean wait = exposure/deaths over replicas older than T₀ whose vessel is intact; statistical error
of ln τ = 1/√deaths; τ_face multiplies by the number of faces. Memorylessness was tested by the coefficient of
variation, a Kolmogorov–Smirnov test, the hazard in age bins, and in one case a censored Weibull fit.

**Three traps, each met more than once.** (i) *Settled debris.* A replica that settles into a still life or
oscillator with cells in the outer layer never dies; counted as living it inflates τ without limit (one tool read
6.2 × 10⁴ where single runs gave 630). Every estimator must censor every period, not only periods 1 and 2; what the
detectors miss is the threat to validity described next. (ii) *Competing channels.* Lifetimes that count any
outer-layer death mix face deaths with transverse firewalls (Section 5.4). (iii) *Ties.* When events are checked
every 16 generations, a face death and a firewall in one window must be attributed by convention, which biases the
firewall-dominated tori of Section 7.3 by about 0.02.

**Threat to validity: lives that settle and are not recognised.** **[measured]** (ZL1; A for the state and the
rate, B for the bounds) The CPU steppers recognised a settled replica by comparing it with its state 840
generations earlier, which misses every period not dividing 840; such a replica never dies and adds exposure until
the run ends or an age cap cuts it. These cycles exist (a 42-cell state of period 16, confirmed by the engine;
periods 9–52 seen) at a rate of 3.5 × 10⁻⁶ of lives at A = 36 and about 4 × 10⁻⁶ at A = 48; without an age cap they
put +0.017 into ln τ in one A = 36 run. In the earlier capped CPU runs (Sections 7.2–7.3) the shift is at most
0.0004 at A = 48, 0.0007 at A = 60 and 10⁻⁵ at A = 72, below every quoted error; the later steppers (Sections 7.2,
7.4) catch every period seen. **[bound]** (ZL2; B at A = 63 and 84, recomputed with separate code; C elsewhere) The
GPU runs have no age cap and catch periods up to 128, or only 1–2 in the octahedral runs of Table 2 and the patch
runs. Where a run is long compared with a mean life, the deficit of old deaths bounds the share of exposure such
replicas could carry (95% upper bounds, not measured biases): ≤ 1.3 × 10⁻⁴ at A = 63, ≤ 6.7 × 10⁻³ at A = 84
against a statistical error of 0.005, and elsewhere (C) at most 1.2 × 10⁻², comparable to the errors. **Runs
shorter than about one mean life admit no bound** (marked † where quoted): Table 2 at A = 108 and 135, three GPU
rows of Table 3, the slabs 6 × 6 × 8 and 6 × 7 × 8, five wider slabs of Table 6 and the 4 × 7 × 8 slab (no age bins in its log). Moving the A = 108 value by
its error would need 2–3% of lives to be of this kind, against < 10⁻⁴ wherever the rate can be measured; that the
rate does not rise with size is assumed **[conjecture]**. No number changes. *Preliminary* **[measured]** (Z13; C,
one agent): of the 37 settled states of period 9–52 logged from small twisted-torus slabs, none needs the walls, 14
are finite free-space objects (five of them new, Section 8), 21 are wires (periodic along one short vector of the
torus: infinite oscillating lines) and 2 are sheets that close only on their own torus. So most exist only because
a small torus lets a line close on itself, which fits a rate falling steeply with area.

**A guard, and its limit.** **[measured]** (GL2; B: the logic exercised on a CPU stand-in by a reviewer, against
its own prediction and two deliberately broken guards; the GPU-side tests are the producer's) A guard for GPU
lifetime runs now exists: one snapshot per replica at doubling ages, compared at every launch boundary; a replica
equal to its snapshot is in a cycle of some period and its life ends as censored. It is off by default and inert
when off, cannot miss a cycle for ever, and recognises no life that is not in one. Its limit: the time between
settling and recognition is up to about the settling age plus period × launch length, which for an odd period
above 128 exceeds a mean life at A ≤ 93. Guarded results must therefore cut the censored lives' exposure at the
snapshot age, or report both figures. Of the results in this paper only the 93-cell torus of Table 8a was run with
the guard on (none of its lives settled); the † runs above are still unbounded.

**Errors of the census pipeline.** **[measured]** (GL1; A) The per-job scatter of the twisted-torus census
(Section 7.3) is mildly larger than Poisson (χ² 100 on 75 and 169 on 151 for two sets of jobs on the 4 × 4 torus),
so the census's quoted errors are 5–15% small. Its 4 × 4 value on file, 9.9324 ± 0.0020, reproduces bit for bit from
its own jobs and lies 3.4σ (with that scatter allowed for) above the value pooled from the second card, a reviewer's own stepper and the census's
pipeline rerun on fresh seeds, 9.9249 ± 0.0003, and the reason Table 8 and Section 7.3 now use the corrected value.
**[measured]** (GL3; B: the card's session and the reviewer, on the same lives) Of its excess of 0.0075, 0.0017 is a
bias of the pipeline and 0.0058 (2.9σ) the draw (GL1's note of 2026-11-15): the census stamps layer deaths every 16
generations, which reads ln τ high by 0.00167 ± 0.00006 at 4 × 4, by at most 0.0008 for long-lived classes at A = 60,
and by 0.0174–0.0184 for the classes with shortest loop² 4, whose face deaths tie with firewalls inside one window
(Table 8). Differences between long-lived classes at one area move by less than 0.001. Where a single torus value
carries an argument it should be measured twice.

**Verification.** Each claim is recorded in a ledger with the command that reproduces it and a grade (164 claims
when this was written: 78 graded A, 75 B, 10 C, 1 D, each by the best grade any part of it has; `python3
research/audit/claims_tally.py`); an independent audit re-derived the theorems and the exact numbers and re-ran the
cheaper statistics; later results were each given to an adversarial reviewer with code of its own before being
recorded. The reviews behind the results added in this revision are `research/audit/REVIEW-dying.md` (rounds 3 and
4), `research/audit/REVIEW-gpu-local-tori.md`, `research/audit/REVIEW-signals.md`,
`research/audit/REVIEW-signals-2.md` and `research/audit/REVIEW-statespace.md`; each corrected something, and the
corrections are stated where the results are. Forecasts were committed
before runs (Table 5). Not repeated by anyone: the side-16 run; the 960-rule survey; the GPU runs quoted here except the 5 × 5 slab
(the second card's other tori are new runs, four of them checked against CPU codes); the 93-cell torus.

**Availability.** Code, curated tables and per-life data for the GPU experiments are in the repository; bulk
output is not tracked, and some analysis scripts need it (listed in `docs/paper/GAPS.md`).

## References

Only works recorded in `research/PRIOR-ART.md` or `research/theory/swarm/library/shelf.md` are cited, with how
far each was read there. No citation has been checked against a library by a person.

- [AC25] N. Ait Sadi, R. Chemlal, "Irrational eigenvalues of D-dimensional cellular automata", arXiv:2509.00933.
  *Definitions and attributions (HTML v1).*
- [AM17] M. Assaf, B. Meerson, "WKB theory of large deviations in stochastic populations", J. Phys. A 50 (2017)
  263001; arXiv:1612.01470. *§2.*
- [BBS94] P. Balister, B. Bollobás, A. Stacey, "Improved upper bounds for the critical probability of oriented
  percolation in two dimensions", Random Structures Algorithms 5 (1994) 573–589. *Not obtained; statement
  second-hand.*
- [BGPV19] Buca, Garrahan, Prosen, Vanicat, "Exact large deviation statistics and trajectory phase transition of
  a deterministic boundary driven cellular automaton", arXiv:1901.00845. *Abstract page opened.*
- [BN94] M. Bramson, C. Neuhauser, "Survival of one-dimensional cellular automata under random perturbations",
  Ann. Probab. 22 (1994) 244–263. *Not obtained.*
- [BSU15] B. Bollobás, P. Smith, A. Uzzell, "Monotone cellular automata in a random environment", Combin. Probab.
  Comput. 24 (2015); arXiv:1204.3980. *§1 (Defs 1.2–1.3 and discussion).*
- [BT00] F. Blanchard, P. Tisseur, "Some properties of cellular automata with equicontinuity points", Ann. Inst.
  H. Poincaré Probab. Statist. 36 (2000) 569–582; arXiv:math/0312137. *§1, §2.2.*
- [BY08] L. A. Bunimovich, A. Yurchenko, "Where to place a hole to achieve a maximal escape rate",
  arXiv:0811.4438. *Abstract and statements.*
- [CD11] S. Chatterjee, R. Durrett, "Persistence of activity in threshold contact processes, an 'annealed
  approximation' of random Boolean networks", Random Structures Algorithms 39 (2011) 228–246; arXiv:0911.5339.
  *§1.*
- [CG99] R. Carretero-González, S. Ørstavik, J. Huke, D. S. Broomhead, J. Stark, "Thermodynamic limit from small
  lattices of coupled maps", Phys. Rev. Lett. 83 (1999) 3633–3636; arXiv:chao-dyn/9904009. *Whole (4 pages); its
  citing works read as titles only.*
- [CGV93] M. Caselle, F. Gliozzi, S. Vinti, "Finite-size effects in the interface of 3D Ising model", Phys. Lett.
  B 302 (1993) 74–79; arXiv:hep-lat/9212013. *Whole.*
- [CK88] J. P. Crutchfield, K. Kaneko, "Are attractors relevant to turbulence?", Phys. Rev. Lett. 60 (1988)
  2715–2718. *Abstract only.*
- [DL88] R. Durrett, X.-F. Liu, "The contact process on a finite set", Ann. Probab. 16 (1988) 1158–1173.
  *Statements and proofs of Thms 1, 2, 4.*
- [dS08] A. M. dos Santos, R. L. Viana, S. R. Lopes, S. E. de S. Pinto, A. M. Batista, "Collective behavior in
  coupled chaotic map lattices with random perturbations", Physica A 387 (2008) 1655–1668. *Abstract, as
  paraphrased by the fetch tool; full text not obtained.*
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
- [GGG10] N. Goldenfeld, N. Guttenberg, G. Gioia, "Extreme fluctuations and the finite lifetime of the turbulent
  state", Phys. Rev. E 81 (2010) 035304(R); arXiv:0906.3572. *Abstract only.*
- [GMMO19] E. Goles, D. Maldonado, P. Montealegre, N. Ollinger, "On the complexity of the stability problem of
  binary freezing totalistic cellular automata", arXiv:1912.02953. *Abstract only.*
- [GMRS23] E. Goles, P. Montealegre, M. Ríos-Wilson, S. Sené, "Dynamical stability of threshold networks over
  undirected signed graphs", arXiv:2309.01854. *§4.1.*
- [GO80, GO81] E. Goles, J. Olivos, "Periodic behaviour of generalized threshold functions", Discrete Math. 30
  (1980) 187–189; "Comportement périodique des fonctions à seuil binaires et applications", Discrete Appl. Math.
  3 (1981) 93–105. *Not obtained.*
- [HKTP10] S. M. Houghton, E. Knobloch, S. M. Tobias, M. R. E. Proctor, "Transient spatiotemporal chaos in the
  complex Ginzburg–Landau equation on long domains", Phys. Lett. A 374 (2010) 2030–2034. *Abstract,
  introduction, lifetime results, conclusion; on 2026-11-14 the whole (White Rose copy), including the
  boundary-layer fit and the reference list.*
- [HS22] I. Hartarsky, R. Szabó, "Generalised oriented site percolation", Markov Process. Related Fields 28
  (2022); arXiv:2103.15621. *Statements; the proof of Cor. 4.8 is a sketch.*
- [KL08] G. Keller, C. Liverani, "Rare events, escape rates and quasistationarity: some exact formulae",
  arXiv:0810.2229. *§1–3.1, §5.2.*
- [KMMK11] C. J. Kuhlman, H. S. Mortveit, D. Murrugarra, V. S. A. Kumar, "Bifurcations in Boolean networks",
  arXiv:1108.2974. *Introduction, §3.1, appendix.*
- [L95] T. M. Liggett, "Survival of discrete time growth models, with applications to oriented percolation",
  Ann. Appl. Probab. 5 (1995) 613–636. *Abstract; key statement second-hand.*
- [LCP17] T. Lilienkamp, J. Christoph, U. Parlitz, "Features of chaotic transients in excitable media governed by
  spiral and scroll waves", Phys. Rev. Lett. 119 (2017) 054101. *Abstract only.*
- [LL-soup] Life Lexicon, "soup", https://playgameoflife.com/lexicon/soup. *Opened.*
- [LMS90] J. L. Lebowitz, C. Maes, E. R. Speer, "Statistical mechanics of probabilistic cellular automata",
  J. Statist. Phys. 59 (1990) 117–170. *Abstract only.*
- [LW-CH], [LW-Mod], [LW-NT], [LW-OT] LifeWiki pages "Cubic honeycomb", "Mod", "Non-trivial",
  "Outer-totalistic", read through the mirror conwaylife.njohnston.ca. *Opened.*
- [M93] T. S. Mountford, "A metastable result for the finite multidimensional contact process", Canad. Math.
  Bull. 36 (1993) 216–226. *Whole.*
- [M99] T. S. Mountford, "Existence of a constant for finite system extinction", J. Statist. Phys. 96 (1999)
  1331–1341. *Abstract only.*
- [Man09] P. Manneville, "Spatiotemporal perspective on the decay of turbulence in wall-bounded flows", Phys. Rev.
  E 79 (2009) 025301(R); arXiv:1102.5703. *Via the fetch tool (ar5iv).*
- [Mil16] J. C. Miller, "Equivalence of several generalized percolation models on networks", Phys. Rev. E 94
  (2016) 032313; arXiv:1505.01396. *k-core and bootstrap sections.*
- [MMVY12] T. Mountford, J.-C. Mourrat, D. Valesin, Q. Yao, "Exponential extinction time of the contact process
  on finite graphs", arXiv:1203.2972. *Statements.*
- [MST19] I. Marcovici, M. Sablik, S. Taati, "Ergodicity of some classes of cellular automata subject to noise",
  Electron. J. Probab. 24 (2019) paper 41; arXiv:1712.05500. *§1–2 and statements.*
- [MV10] T. Mountford, D. Valesin, "Supercriticality of annealed approximations of Boolean networks",
  arXiv:1007.0862. *Abstract, §1.*
- [MV12] S. Méléard, D. Villemonais, "Quasi-stationary distributions and population processes", Probab. Surv. 9
  (2012) 340–410; arXiv:1112.4732. *§2.1, §3.*
- [MvHB02] R. Mikkelsen, M. van Hecke, T. Bohr, "Universal and non-universal properties of transitions to
  spatio-temporal chaos in coupled map lattices", arXiv:cond-mat/0207208. *Abstract only.*
- [N11] I. Nåsell, *Extinction and Quasi-Stationarity in the Stochastic Logistic SIS Model* (Springer, 2011).
  *Not obtained; statement from a search result.*
- [NA21] T. Nemoto, A. Alexakis, "Do extreme events trigger turbulence decay? A numerical study of turbulence
  decay time in pipe flows", J. Fluid Mech. 912 (2021) A38; arXiv:2005.03530. *§§1–3.*
- [NH03] T. Neuhaus, J. S. Hager, "2D crystal shapes, droplet condensation and exponential slowing down in
  simulations of first-order phase transitions", J. Stat. Phys. 113 (2003) 47–83; arXiv:cond-mat/0201324.
  *Abstract only.*
- [NZ17] F. R. Nardi, A. Zocca, "Tunneling behavior of Ising and Potts models in the low-temperature regime",
  arXiv:1708.09677. *§§1–2. Place of publication not checked.*
- [PT09] A. Politi, A. Torcini, "Stable chaos", arXiv:0902.2545. *§1 and the starts of §3, §4.*
- [R22] W.-J. Rappel et al., "Stochastic termination of spiral wave dynamics in cardiac tissue", Front. Netw.
  Physiol. 2 (2022) 809532. *Full text, via the fetch tool.*
- [RK14] Reia, Kinouchi, "Conway's game of life is a near-critical metastable state in the multiverse of
  cellular automata", arXiv:1407.1006. *Abstract only.*
- [SK15] K. Sugimura, H. Kori, "Exponential system-size dependence of the lifetime of transient spiral chaos in
  excitable and oscillatory media", Phys. Rev. E 92 (2015) 062915; arXiv:1512.08333. *§§I, III, IV.*
- [STT21] V. Salo, G. Theyssier, I. Törmä, "Cellular automata and bootstrap percolation", arXiv:2110.00656.
  *Abstract only.*
- [T19] D. K. Tuckett, A. S. Darmawan, C. T. Chubb, S. Bravyi, S. D. Bartlett, S. T. Flammia, "Tailoring surface
  codes for highly biased noise", Phys. Rev. X 9 (2019) 041031; arXiv:1812.08186. *Abstract only.*
- [TL08] T. Tél, Y.-C. Lai, "Chaotic transients in spatially extended systems", Phys. Rep. 460 (2008) 245–275.
  *Not obtained (an author copy exists and returned HTTP 503 three times on 2026-11-14).*
- [VR19] D. Vidmar, W.-J. Rappel, "Extinction dynamics of spiral defect chaos" (arXiv title "Extinction dynamics
  of cardiac fibrillation"), Phys. Rev. E 99 (2019) 012407; arXiv:1808.01991. *Abstract and the relevant
  sections, via the fetch tool.*
- [WS03] R. Wackerbauer, K. Showalter, "Collapse of spatiotemporal chaos", Phys. Rev. Lett. 91 (2003) 174103.
  *Not obtained; known through [HKTP10].*
- [arXiv:1510.05924] "Monte Carlo Simulations of ABC Stacked Kagome Lattice Thin Films". *Abstract only.*
  [citation needed: authors]

## Appendix: ledger rows not used

Superseded and therefore absent: F7 (an early engine-only slope), S1 (the proportional "effective area" law for
symmetric faces), the fitted limit of F9 and GP4 (the extrapolated constant 0.2077). Graded C and mentioned only as
preliminary or with their grade named: F12, S4, Q4, G3, G4, Z13, the other-lattice results (K7, K8), and the parts
graded C of Z2 (n = 16), Z3 (the hinge flips), Z4 (period 3), Z12 (absence from the census lists), S9, TH2, TH4,
TH5, X3 (the uncensored value), ZL2, C4 (the wall-clock time), GL3 (the 93-cell torus) and SS2 (side 16). Graded B and not used: R6 (the web stepper's
tests), C7, Z11, K2. Graded C and not mentioned: L2, K5 (the remaining other-lattice row), and the parts graded C
of C2 (the composition of the final state), C8 (the runs; only the pooled value, graded B, is used) and Z10 (the
phase shifts). Every row added on 2026-11-15 for the dying face (DY8–DY15), the second card (GL3), signals (SG1–SG10) and the
state space (SS1–SS3) is used. Rows about the edge-neighbour variant (not this automaton) are outside the paper.
