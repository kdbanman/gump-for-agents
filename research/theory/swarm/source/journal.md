# source: journal (append-only)

Line: the self-made randomness. A successor should read `claims.md` first (current list, with tags), then this
file. Each entry is a finished result or a recorded dead end. Tags: **[proved]** (proof here), **[sketched]**,
**[guessed]**. "From memory" marks a literature statement I have not opened.

---

## 2026-11-13, round 1

### S1. Conventions fixed

**Layers.** One notation for both rules. The vessel is a stack of layers 𝓛_0 (the face, or edge row), 𝓛_1, 𝓛_2, …
going inward; everything on the other side of 𝓛_0 is dead for ever.
- 2D rule: 𝓛_k = row k of a strip, cells (x, k), x ∈ Z_L (or Z, or a box). A cell of 𝓛_k has 4 neighbours in
  𝓛_k and one in each of 𝓛_{k±1}, 𝓛_{k±2}.
- gump: 𝓛_k = the {111} layer s = s₀ + 2k for the inward signed diagonal d, cross-section a torus (slab
  geometry, the clean case by board E3) or the whole plane. By T1 a cell of 𝓛_k has 6 neighbours in 𝓛_k, 2 in
  each of 𝓛_{k±1}, 1 in each of 𝓛_{k±2}.

**The deep neighbour.** Every cell p ∈ 𝓛_k has exactly one neighbour in 𝓛_{k+2}; call it D(p). 2D: D(x, k) =
(x, k + 2). Gump: if p has odd axis a and the other axes are b, c, then D(p) = p + 2d_b e_b + 2d_c e_c (the
coplanar neighbour with d·offset = +4). D keeps the orientation class and is a translation on each class, so
**D is a bijection 𝓛_k → 𝓛_{k+2}** (also on a torus cross-section). All other neighbours of p lie in
𝓛_{≤ k+1}. Consequence used everywhere below: the state of 𝓛_k at time t depends on the initial state of
𝓛_{≤ k+2t} only, and on 𝓛_{k+2t} only through the cells D^t(p).

**Top process and drive.** Fix w ≥ 1. Z_t ∈ {0,1}^{𝓛_0 ∪ … ∪ 𝓛_{w−1}} is the state of the top w layers, b_t the
live/dead pattern of 𝓛_w ∪ 𝓛_{w+1} at time t (the *drive*). Under the true rule in the top w layers,
Z_{t+1} = G(Z_t, b_t) for a fixed map G (cells of 𝓛_{w−1} read 𝓛_w and 𝓛_{w+1}; cells of 𝓛_{w−2} read 𝓛_w).
The face dies at T = min{t : 𝓛_0 empty at t}; "𝓛_0 empty" is absorbing for G whatever the drive (a dead face
cell with empty face sees ≤ 3, resp. ≤ 2). So **{T > t} = {𝓛_0 non-empty at time t}: an event about the state at
one time.**

**Dice models.** D_w(ν): the Markov chain Z_{t+1} = G(Z_t, b_t) with b_t fresh at every generation, its cells
i.i.d. Bernoulli(ρ) (law ν), independent of the past. (w = 1 is "the face over fresh random layers".)
D_w[κ], *state-dependent dice*: the same with b_t drawn from κ_t(· | Z_t), a kernel from top states to drive
patterns. D_w(ν) is the case κ_t(· | z) ≡ ν.
Which τ: for a dice chain, τ = 1/(1 − λ) with λ the top eigenvalue of the kernel restricted to living states
(Darroch–Seneta; board, lemma exchange). For a deterministic system, the hazard h_t = P(T = t + 1 | T > t) under
a stated initial law.

**Deterministic relatives.** A bulk rule on cells of 𝓛_{≥ w} with states in a finite alphabet B is
*deep-permutive* if y_{t+1}(p) = π_p( y_t(D p) ; the states at time t of p and of its other neighbours ), where
for every value of the second argument π_p(· ; c) is a bijection of B. Examples with B = {0,1}: the parity rule
"alive next iff the number of live neighbours is odd" (outer-totalistic on gump's own 12 neighbours, or on the
cross; permutive in *every* neighbour); the pure conveyor y_{t+1}(p) = y_t(Dp); any y_t(Dp) ⊕ g(the rest).
**R_w(Q)** is the cellular automaton on the half-infinite stack in which 𝓛_0 … 𝓛_{w−1} (and everything outside)
run the true rule and 𝓛_{≥ w} run a deep-permutive rule Q; top cells read a source cell as alive iff φ(y) = 1 for
a fixed φ : B → {0,1}; source cells in 𝓛_w, 𝓛_{w+1} may read the top layers (two-way coupling).

### S2. Lemma 1 (exact source, with feedback) [proved]

**Lemma 1.** In R_w(Q) let the source cells at time 0 be i.i.d. uniform on B, independent of Z_0 (any law λ_0).
Then for every t ≥ 0 the source configuration at time t is i.i.d. uniform on B and independent of
(Z_0, …, Z_t, b_0, …, b_{t−1}). Hence (Z_t) is exactly the Markov chain D_w(ν), ν = Bernoulli(|φ⁻¹(1)|/|B|),
started from λ_0; in particular T has exactly the dice law and κ_t ≡ ν.

*Proof.* Claim: for p ∈ 𝓛_k, k ≥ w, y_t(p) = Π( y_0(D^t p) ; y_0 on 𝓛_{< k+2t} ) with Π(· ; c) a bijection of B for
every c. For t = 0 this is trivial. If true for t, then in y_{t+1}(p) = π_p( y_t(Dp) ; … ) the first argument is a
bijective function of y_0(D^{t+1} p) given y_0 on 𝓛_{< k+2+2t}, and the other arguments (cells of 𝓛_{≤ k+1} at
time t) depend on y_0 on 𝓛_{≤ k+1+2t} only; a bijection of a bijection is a bijection. Now fix t and K. Given
c_0 = y_0 on 𝓛_{< w+2t}, the map (y_0 on 𝓛_{w+2t}, …, 𝓛_{w+2t+K}) ↦ (y_t on 𝓛_w, …, 𝓛_{w+K}) is triangular
with bijective diagonal blocks (D^t is a bijection 𝓛_{k} → 𝓛_{k+2t}), so it is a bijection; the left side is
uniform and independent of c_0, hence so is the right side. Finally Z_0, …, Z_t and b_0, …, b_{t−1} are functions
of c_0 (b_{t−1} lives on 𝓛_w ∪ 𝓛_{w+1} at time t − 1 and depends on 𝓛_{≤ w+2t−1}). ∎

*Smallest case by hand.* One column, w = 1: face state X, source cells y(1), y(2), …, rule
y′(j) = y(j+1) ⊕ y(j−1) (j ≥ 2), y′(1) = y(2) ⊕ X, X′ = Φ(X, y(1)). Then y_1(1) = y_0(2) ⊕ X_0 and
y_2(1) = y_0(3) ⊕ y_0(1) ⊕ Φ(X_0, y_0(1)): each new symbol read by the face contains a new initial bit by XOR, so
(y_0(1), y_1(1), y_2(1)) is a bijective image of (y_0(1), y_0(2), y_0(3)) for each X_0, although the source is
being written to by the face.

*Remarks.* (1) The feedback from the face into the source is harmless because the fresh symbol enters by a
bijection (a one-time pad). (2) Every drive cell has a private chain of ancestors p, Dp, D²p, …, so **all
independence between neighbouring face cells survives, in every dimension**; what it costs is a reservoir whose
cross-section is the whole face. A source that is permutive only *along* the face cannot do this: a
one-dimensional automaton of radius r under a ring of L edge cells supplies at most L + 2rt initial symbols to
the L·t symbols the edge reads in t generations. (3) Density: B = Z_m, rule y_t(Dp) + g(rest) mod m,
φ(y) = 1[y < k] gives ρ = k/m. With B = {0,1}, ρ = ½.

**The relative, and exactly how it differs from gump.** "Gump on parity": gump's lattice and neighbourhood; rule
B45/S345 in 𝓛_{< w} and outside; rule "n odd" in 𝓛_{≥ w}.

| | gump | R_w(parity) |
|---|---|---|
| lattice, neighbourhood, rule in the top w layers | — | the same |
| rule below depth w | B45/S345 | n odd (or any deep-permutive rule) |
| vessel | finite hull or slab | half-infinite stack over a torus (or plane) cross-section |
| dead face stays dead (T2 at the face) | yes | yes (T2's proof uses only the rule at the face and outside) |
| firewall T3, sealed sets T6 | yes | inside the top w layers (the proofs are local to gump cells) |
| peeling of successive faces | yes | the first w faces (after j deaths the system is R_{w−j}) |
| energy, drive only at overcrowded cells (T5) | yes | no: every source cell is sensitive to every neighbour at every step |
| entropy available | ≤ N bits for ever | |𝓛_w ∪ 𝓛_{w+1}|·log₂|B| fresh bits reach the top layers per generation, for ever |
| drive seen by the top w layers | a function of the vessel's past | i.i.d., independent of the past: D_w(ν) exactly |

So every theorem about D_w(ν) is, word for word, a theorem about the deterministic automaton R_w(Q) started
from (anything) ⊗ (uniform). Nothing about R_w is hard that is not hard about D_w.

### S3. Lemma 2 (exact dice need an infinite reservoir) [proved]

**Lemma 2.** Let F be a map of a finite set Ω, ω_0 random with any law, b_t = β(F^t ω_0) any observable. Then
Σ_{t<T} H(b_t | b_0, …, b_{t−1}) = H(b_0, …, b_{T−1}) ≤ H(ω_0) ≤ log₂|Ω|. In particular if b_0, …, b_{T−1} are
i.i.d. with entropy H(ν) each, T ≤ log₂|Ω| / H(ν).
*Proof.* (b_0, …, b_{T−1}) is a function of ω_0; chain rule. ∎

Consequences. (a) In a vessel of N cells the drive of a face of area A (2A cells in a slab) can be exact dice
for at most N/(2A·H₂(ρ)) generations, about half the number of layers; R_w with a binary source of H layers
(missing deep neighbours read as 0) gives exact dice for ⌊H/2⌋ generations, so the bound is attained.
(b) Over a lifetime τ ≈ e^{γA} the drive's conditional entropy
given its own past averages at most N/τ bits per generation: essentially zero. **No property of gump's bulk
that conditions on the past of the drive (conditional entropy, Santha–Vazirani-type bounds, ψ-mixing in time
given the past) can hold in a finite vessel on the time scale of the law.** Whatever replaces dice in gump must
be a statement that does not condition on the past. S4 says which.

### S4. Lemma 3 (the death law depends only on equal-time conditional laws) [proved]

**Lemma 3 (Markovian projection).** Let (ω_t) be any process (for instance a deterministic map with a random
initial state), π a map from its state space to a finite set S, and λ_t the law of π(ω_t). Put
K_{t+1}(s, s′) = P(π(ω_{t+1}) = s′ | π(ω_t) = s). Then λ_{t+1} = λ_t K_{t+1}. So for every set Δ ⊂ S that π(ω_t)
cannot leave, the hitting time T of Δ satisfies P(T > t) = (λ_0 K_1 ⋯ K_t)(S ∖ Δ): the law of T is that of the
absorption time of the time-inhomogeneous Markov chain with kernels K_t started from λ_0.
*Proof.* λ_{t+1}(s′) = Σ_s P(π(ω_t) = s) P(π(ω_{t+1}) = s′ | π(ω_t) = s). And {T > t} = {π(ω_t) ∉ Δ}. ∎

Applied to gump (any vessel, any initial law), π = the top w layers of a face, Δ = {𝓛_0 empty}:
K_{t+1}(z, z′) = Σ_β κ_t(β | z) 1[G(z, β) = z′], where

  **κ_t(β | z) = P( 𝓛_w ∪ 𝓛_{w+1} shows β at time t | 𝓛_0 … 𝓛_{w−1} show z at time t )**

is the *equal-time conditional law of the two layers beneath given the w layers above*. So:

> The death time of a gump face has exactly the law of the absorption time of the dice chain D_w[κ_t], for every
> w. The bulk enters only through κ_t. The process (Z_t) is not Markov and the drive is strongly correlated in
> time; neither matters for the law of T (nor for any event that is absorbing for the top layers: the next
> faces, firewalls inside the top w layers).

The same holds with any extra absorbing flag carried along (for the board's τ: π = (top w layers, 1[state is on a
cycle]), and the hazard is taken among states with flag 0 and living face).

*Smallest case by hand (and a warning).* Face Z ∈ {0, 1}, Z′ = Z·b, drive constant in time, b_t = b_0 ~
Bernoulli(½). Then κ_0(1 | Z = 1) = ½ and κ_t(1 | Z_t = 1) = 1 for t ≥ 1: K_1(1, 0) = ½, K_t(1, 0) = 0 afterwards,
P(T > t) = ½ for all t ≥ 1. Correct, and it shows what reused randomness looks like in κ: *given that the face is
alive, the drive is one that does not kill it.* The average distance of κ_t from ν can be tiny while κ_t is
totally different on the rare states from which the face can die. Any hypothesis on κ has to be a *ratio* bound
on those states, not an average.

Consequences.
(a) **Transfer identity.** For any kernel P on S (the dice kernel of D_w(ν), say), f = 1[alive], V_s = P^s f:
  P(T > R) − (λ_0 P^R)(alive) = Σ_{t=0}^{R−1} E[ ((K_{t+1} − P) V_{R−t−1})(Z_t) ].
(Telescoping: E V_{R−t−1}(Z_{t+1}) − E V_{R−t}(Z_t).) The error of the dice model is the sum over generations
of how differently κ_t(· | Z_t) and ν weigh the dice chain's own survival function.
(b) **Memorylessness.** The hazard is constant from T_0 on iff the conditional law of (Z_t, b_t) given
{T > t, not settled} is constant in t from T_0 on (then K_t ≡ K on living states and P(T > t) is geometric).
"Memoryless" is the stationarity of one equal-time law; no mixing in time is involved.
(c) **In the relatives R_w(Q), κ_t ≡ ν exactly** (Lemma 1). In gump κ_t is not a product and depends on z.
(d) **Exactly testable.** For a vessel small enough to enumerate, λ_t and κ_t are computable exactly for every t.

**Aim B, stated.** Find a class 𝒦 of kernels κ(β | z) such that (i) the lifetime theorem for dice holds for
every chain D_w[κ] with κ_t ∈ 𝒦, with constants uniform over 𝒦, and (ii) "κ_t ∈ 𝒦" is a finite statement about
the equal-time law of w + 2 layers. Then (i) + Lemma 3 is a theorem for gump under the single hypothesis (ii).
By S3 and the warning above, 𝒦 cannot be defined by conditioning on the past, nor by an average distance to ν.

### S5. Lemma 4 (the threshold lemma, localised) [proved]

Setting of T5 (threshold.md), on any set of cells V, **finite or infinite**, outside dead: n_i, x_i, h_i = n_i + x_i;
gump: x_i(t+1) = 1 iff h_i(t) ≥ 4 and n_i(t) ≤ 5; a *mismatch* at (i, t) is x_i(t+1) ≠ x_i(t−1); an *O1 event* is a
mismatch with n_i(t) ≥ 6 (then x_i(t−1) = 1, x_i(t+1) = 0).

**Lemma 4.** Let d : V → [0, ∞) satisfy |d_i − d_j| ≤ 1 for neighbours (graph distance to a cell o, or to a set such
as a face), 1 < λ < (4/3)^{1/2}, a_i = λ^{−d_i}, and suppose S = Σ_i a_i² < ∞. Put θ′ = (4/λ + 3λ)/2,
m = (4/λ − 3λ)/2 > 0, c′ = 12λ + 1 − θ′. Then for all T, along every orbit of gump,

  m · Σ_{mismatches (i,t), 1≤t≤T, not O1} a_i²  ≤  (12λ + 1 + θ′)·S + c′ · Σ_{O1 events (i,t), 1≤t≤T} a_i².

For the uncapped rule U there are no O1 events and the right side is (13λ + θ′)·S.

*Proof.* K(t) = Σ_{i,j} a_i a_j W_ij x_i(t) x_j(t−1) − θ′ Σ_i a_i² (x_i(t) + x_i(t−1)), W = A + I, ordered pairs; the
sums converge absolutely. Since a_i a_j W_ij is symmetric, exactly as in threshold.md §2,
K(t+1) − K(t) = Σ_i (x_i(t+1) − x_i(t−1)) a_i² (g_i(t) − θ′), g_i(t) = Σ_{j ∈ N(i) ∪ {i}} (a_j/a_i) x_j(t).
Each ratio a_j/a_i lies in [1/λ, λ], so h_i/λ ≤ g_i ≤ λ h_i. A term vanishes unless (i, t) is a mismatch. Mismatch
with x_i(t+1) = 1: h_i(t) ≥ 4, term ≥ a_i²(4/λ − θ′) = m a_i². Mismatch with x_i(t+1) = 0 and n_i(t) ≤ 5: h_i(t) ≤ 3,
term = a_i²(θ′ − g_i) ≥ a_i²(θ′ − 3λ) = m a_i². O1 event: g_i ≤ 12λ + 1, term ≥ −c′ a_i². Sum over t and use
−2θ′S ≤ K ≤ c′S (for U: K ≤ (13λ − θ′)S). ∎

*Smallest case by hand.* V = {o}, x(−1) = x(0) = 1: K(0) = 1 − 2θ′; x(1) = 0, K(1) = −θ′; K(1) − K(0) = θ′ − 1,
and the formula gives (0 − 1)(g − θ′) with g = 1: the same, ≥ m.

The 2D rule: the same with thresholds 3 and 2: λ < (3/2)^{1/2}, θ′ = (3/λ + 2λ)/2, m = (3/λ − 2λ)/2, c′ = 8λ + 1 − θ′.

**Corollary 4a (answers the question left open in threshold.md §3, §6).** Under the uncapped rule, on the
infinite lattice or any subset, from *every* initial configuration, each cell has at most
C_U = (13λ + θ′)S/m mismatches, a constant independent of the configuration (S is finite because balls grow
polynomially). So every cell is eventually of period ≤ 2. (The advancing front of threshold.md is consistent:
each cell changes once, which is two mismatches.) The technique, a pair energy with weights decaying slowly enough that the weighted
threshold still separates the two cases, is from the literature on majority dynamics on infinite graphs
(Ginosar–Holzman; Tamuz–Tessler; from memory, not opened; requested from the library). The proof above is
self-contained.

**Corollary 4b (what T5 says about where the randomness is made).**
(i) *A threshold bulk is not a source, however large.* Under U a set Λ of cells has at most C_U|Λ| mismatches
in all of time, even over an infinite half-space of random initial bits. A cell's time series is fixed by its
first two values and its mismatch times, so the whole future of Λ carries at most O(C_U |Λ| log t) bits up to
time t: entropy rate zero. Compare the parity bulk: 1 fresh bit per cell per generation for ever (Lemma 1).
The cap is what stands between the two.
(ii) *In gump, what a cell does beyond period 2 is paid for by overcrowding near it.* For a face Λ = 𝓛_0 of a
slab take d = graph distance to the face (a cell of 𝓛_k has d = ⌈k/2⌉), so S = A(1 + 2/(λ² − 1)):

  #{mismatches in the face, not O1, up to T} ≤ [ (12λ+1+θ′)·S + c′ Σ_k λ^{−2⌈k/2⌉} · #{O1 events in 𝓛_k up to T} ] / m.

Overcrowding events count with a weight that decays geometrically with depth, at best by a factor just under
3/4 per two layers (gump; 2/3 in 2D). A region with no O1 events is a period-2 region up to a leak that is
exponentially small in its width.
(iii) *Entropy rate.* If cell i mismatches at rate r_i ≤ ½ per generation, its time series has entropy rate
≤ H₂(r_i) (the entropy of a binary sequence with a given expected number of ones). So the entropy rate of the
face is at most A·H₂ of the right side of (ii) per cell and generation.
(iv) *Death itself is not made at the cap.* The last cells of a face die at mismatches with x(t+1) = 0; when
these are not overcrowded they are threshold events (h ≤ 3: starvation) and each *dissipates* at least m a_i².
The cap keeps the bulk moving; the face dies of the threshold. (Consistent with threshold.md §5: the O1 rate
in the outer live layer halves in the 50 generations before it empties.)

The constants are honest but poor (λ = 1.1: m = 0.168, c′ = 10.7, c′/m ≈ 64, S ≈ 10.5·A): with the measured O1
rates (0.07–0.12) the inequality in (ii) is numerically empty. Its content is qualitative: zero drive nearby ⇒
bounded activity; drive far away is discounted geometrically.

### S6. A dead end recorded: the conveyor of finitely many frames

Tempting finite relative: a ring of P frozen random frames ξ_0, …, ξ_{P−1} (i.i.d. ν) rotating under the face,
b_t = ξ_{t mod P}, one-way coupling. Within one turn it is exact dice. After that it is not, and not slightly:
Z_{(k+1)P} = Ψ_ξ(Z_{kP}) for one fixed random map Ψ_ξ, so the face is iterating a fixed map; once
Ψ_ξ(Z) = Z at a living Z the face is immortal. In the language of S4: on the event that the face is in the
state it was in one turn earlier, the drive is the frame that did not kill it then, so the conditional law of
the drive puts no mass on killing patterns there. If the dice chain forgets its state within one turn
(coalescence), death essentially occurs only during the first turns: P(T < ∞) is of order P·h. **A one-way
source of period P reproduces the law only if P ≳ τ**, i.e. the source must have at least log₂ τ ≈ γA/ln 2
cells; a short periodic source gives an immortal fraction instead of a lifetime. [Proved: the first three
sentences. Sketch: "of order P·h", which assumes coalescence within one turn.] This is the mechanism of the board's "a positive fraction never dies" in its
simplest form, and it is why exactness for a finite time (Lemma 1 with a finite reservoir) does not extend.

---

## Round 1 report

**Definitions fixed (S1).** Layers 𝓛_k, deep neighbour D (a bijection 𝓛_k → 𝓛_{k+2}); top process Z_t (w layers),
drive b_t (the two layers beneath); dice models D_w(ν) and state-dependent dice D_w[κ]; deep-permutive bulk
rules; the relatives R_w(Q), e.g. "gump on parity".

**Claims.**
1. [proved] Lemma 1: in R_w(Q) from (any law) ⊗ (uniform), the top w layers are exactly the dice chain D_w(ν),
   with two-way coupling allowed. Table of differences from gump in S2.
2. [proved] Lemma 2: exact dice for T generations need T·H(ν) bits; in a finite vessel no dice-like property
   conditioned on the past can hold over a lifetime.
3. [proved] Lemma 3: the death law of a gump face equals the absorption law of D_w[κ_t], κ_t = the equal-time
   conditional law of the two layers beneath given the w layers above. Transfer identity; memorylessness =
   stationarity of that one law.
4. [proved] Lemma 4 (local T5) with Corollary 4a (the uncapped rule on infinite configurations: boundedly many
   mismatches per cell, so cellwise period ≤ 2) and 4b (a threshold bulk has entropy rate zero at any face;
   in gump activity at the face is bounded by overcrowding discounted geometrically with depth).
5. [sketched] S6: a periodic one-way source needs period ≳ τ.

**What I aim to prove next.** (a) Theorem A in final form once the target dice model is known: R_w(Q) for that
model, with the statement of which τ. (b) Aim B of S4: a class 𝒦 of state-dependent dice, defined by ratio
bounds on the conditional law of the drive given a precarious top state, for which lifetime bounds hold
uniformly, so that the theorem for gump has the one hypothesis "κ_t ∈ 𝒦". First the upper bound (easy
direction: if every drive cell has conditional probability ≥ δ of each value given the top state and the other
drive cells, then τ ≤ C·δ^{−cA}, using the face game), then what the lower bound needs.

**Weakest step.** Lemma 3 is exact but moves the whole difficulty into κ_t: it could turn out that every class 𝒦
for which the dice theorem is provable excludes gump's κ_t (S4's warning: reuse of randomness shows up exactly
on the rare precarious states). Lemma 4's constants are too weak to give numbers. S6's "order P·h" is not proved.
My present belief: a theorem for gump itself along this line is out of reach (no permutive variable, no
invariant product measure, finite entropy); the realistic outputs are the relative (done modulo the target
model) and a theorem under the hypothesis κ_t ∈ 𝒦.

**For the critic.** Please point me to the dice model the probability line has fixed (which layers are fresh,
with what law, which τ).

**Lab requests** (exact; all tiny).
- L1 (check of Lemma 1). Vessel: 2D box, 3 columns × 7 rows, no wrap, outside dead. Rule: row 0 runs B34/S234 on
  the cross (reading rows 1, 2); rows 1–6 run "alive next iff the number of live cross neighbours is odd" (row 0
  counts as a neighbour of rows 1, 2). Random: all 21 cells uniform. Claim: the map from the initial state to
  the record (row 0 at t = 0; rows 1–2 at t = 0, 1, 2) is a bijection of {0,1}^21, and rows 1–2 at t = 3 are a
  function of that record. No convention needed for states that never die.
- L2 (check of Lemma 4's case analysis). Vessel: gump hull R = 2v (12 cells), o any cell, d = graph distance in
  the vessel, λ = 1.1. For every pair (u, v) of states, with x(t−1) = u, x(t) = v, x(t+1) = gump(v): verify
  K(t+1) − K(t) ≥ m·Σ_{non-O1 mismatches} a_i² − c′·Σ_{O1} a_i². Same for the 2D rule on the 3 × 4 box with
  λ = 1.15 and the 2D constants of S5.
- L3 (first look at κ_t; low priority). Vessel: 2D strip 4 × 6, true rule everywhere, uniform initial state,
  t = 0, …, 30. Among states at time t that are not on a cycle and have row 0 non-empty, for w = 1: (a) the
  hazard h_t; (b) for each population n of row 0, the probability that row 0 is empty at t + 1, under the true
  κ_t and under the product law with the measured density of rows 1–2; (c) whether (a), (b) are constant in t
  over some range. States that never lose the edge stay in the population until they reach their cycle.

### Addendum to round 1 (same day): the board's round 0b and the library note appeared while I was writing

Read after the report above was written: `critic/board.md` as of commit 3a76d44 and
`library/notes/algebraic-ca.md`. What changes:

- **The pointer I asked for is on the board**: the dice models are D2(L, ρ; w) (2D rule, w rows over two rows of
  dice) and D3(face, ρ; w) (gump). These are my D_w(ν). From here on I use the board's names. Lemma 1 then reads:
  *R_w(Q) for the 2D rule is D2(L, ρ; w) exactly, and for gump on a periodic face D3(face, ρ; w) exactly*
  (ρ = ½ for a binary source). With the board's exact value (lab L0b.4), the deterministic automaton "2D rule
  in row 0 over parity rows", ring of 16, has ln τ = 8.6764 exactly.
- **Overlap.** The board's "permutive sources" lemma (the field {x_p(t)} of an automaton permutive in an extreme
  variable e is i.i.d. on any set of cells no two of which differ by a multiple of e) is Lemma 1 without the top
  layers. What Lemma 1 adds: the source may be *written to* by the layers it drives (the bulk of a two-rule
  automaton, not a separate tape), and it stays uniform and independent of everything the top has seen. The
  board's graveyard 15 is Lemma 2's first sentence; what Lemma 2 adds is the consequence for conditioning on
  the past. Lemmas 3 and 4 are not on the board.
- **Literature.** The library confirms the one-dimensional time-column statement (Shereshevsky 1992, Sablik
  2007, Pivato 2003) and reports no published statement of exact independence for a source of dimension ≥ 2
  ("a gap on the shelf, not a known negative"). Lemma 1 and the board's lemma fill it for rules permutive in a
  deep variable; both are proved here, not cited. Marcovici–Sablik–Taati 2019, Theorem 3.16 (a permutive rule
  with positive permutation noise forgets its initial law exponentially fast, uniformly) is the natural tool for
  a source that is *not* started from the uniform measure; not used yet.
- The request to the critic in the report ("point me to the dice model") is thereby answered; L1–L3 stand.

---

## 2026-11-13, round 2

Read for this round: `critic/to-source.md` (reply to round 1), the board as of commit cc0b7a3,
`library/notes/source-requests.md`, `algebraic-ca.md`, `nonmonotone.md`; the committed data files
`research/theory/exponent/data/hierarchy.json`, `gump_model.json` and the outcomes F8, F9 in
`research/theory/exponent/PREDICTIONS.md` (sampled values of the dice models; unchecked by the critic).

### S7. Corrections to round 1 (all four of the critic's points accepted)

1. **S4(b), C4.** Only one direction holds: *if* the conditional law of (Z_t, b_t) given {T > t, not settled} is
   constant in t, the hazard is constant. The converse is false (two living states with the same death
   probability and a law alternating between them).
2. **S3, Lemma 2(b).** The entropy count excludes properties that condition on the *whole* past of the drive (more
   of the past than the vessel holds). It says nothing about a window of m generations: a maximal-length shift
   register is nearly uniform given any m < N earlier bits for 2^N − 1 steps. The sentence in bold in S3 should
   read "…that conditions on the whole past of the drive…". For gump a window condition fails for a different,
   local reason: S9 below.
3. **Cor. 4b(iv).** "The last cells die at mismatches" is wrong at the step of dying (born at t − 1 and dead at
   t + 1 is no mismatch). The correct and sharper statement is the critic's (board, "starvation"): in a face with at
   most three live cells no live face cell is overcrowded (k ≤ 2, b ≤ 3, n ≤ 5), so in a death from n ≤ 3 every cell
   dies with n ≤ 2. The figure "halves in the 50 generations before" is board E4, an average over layers of all
   sizes, and should not be quoted as a property of faces of a given size.
4. **Cor. 4b(ii).** The weight of an O1 event at graph distance d is λ^{−2d} with λ^{−2} *above* 3/4 (gump; above
   2/3 in 2D): the discount per step is at best just short of a factor 4/3, and only as m → 0.

The library (source-requests §2) confirms that the published period-two theorems on infinite graphs
(Moran; Ginosar–Holzman; Tamuz–Tessler, Theorem 1.5, read by the librarian) are for majority with odd degree; no
infinite-graph statement for general thresholds with a self-weight was found. Attribution for Lemma 4: energy of
Goles–Olivos, geometric weights of Ginosar–Holzman and Tamuz–Tessler, extended here to the threshold 4 of 13 and
to the capped rule. Their constant, ((d+1)/(d−1))·d·M_d, is of the same kind as C_U.

### S8. Lemma 1 for an arbitrary top; an exact quasi-stationary law [proved]

**Lemma 1′.** The proof of Lemma 1 uses nothing about the top w layers except that they are finitely many layers
whose cells read no deeper than 𝓛_{w+1}. So it holds with *any* local rule and any finite alphabets in the top
w layers: over a deep-permutive bulk started uniform, the top is the Markov chain Z_{t+1} = G̃(Z_t, U_t) with U_t
fresh uniform symbols on 𝓛_w ∪ 𝓛_{w+1}. Hence every probabilistic cellular automaton on finitely many layers
whose local randomness is a function of finitely many fresh uniform symbols (all probabilities rational) is the
top of a deterministic automaton. In particular: D2 and D3 with any rational ρ (source alphabet Z_m, a top cell
reads y as alive iff y < k); any rational law π on the number b ∈ {0, 1, 2} of live cells beneath an edge cell
(two decoder rows, both functions of one fresh symbol of the row below them); drive laws that depend on the top
state one generation earlier (decoder cells that read the top). What makes the write-back harmless, in the
terms of the librarian's note (source-requests §1): the top reads 𝓛_w ∪ 𝓛_{w+1}, while the symbol that masks what
it writes into a source cell p comes from D(p), two layers deeper, and is independent of everything the top has
read (Lemma 1). In their counterexample x ↦ x + w(x) the boundary word is a function of the very symbol that
should mask it; a finite window always ends in such cells, which is the ⌊H/2⌋ of S3.

**Proposition 1″ (an exact conditionally invariant measure).** Let μ be a quasi-stationary law of the finite
chain D_w(ν) (eigenvalue λ; Darroch–Seneta, read through `library/notes/qsd.md`). In R_w(Q) started from
μ ⊗ uniform, the law of the whole configuration at time t conditioned on {T > t} is again μ ⊗ uniform, and
P(T > t) = λ^t exactly.
*Proof.* By Lemma 1 the source at time 1 is uniform and independent of (Z_0, Z_1); conditioning on {Z_1 alive}, an
event of Z_1, leaves the source uniform and independent of Z_1, and Z_1 given alive has law μ. Induct. ∎
So the deterministic automaton R_w(Q) has an exact quasi-stationary law and an exactly geometric wait. A finite
deterministic system has neither (board, trapdoors (v); `notes/escape-rates.md` B1). That contrast is the whole
difference between the relative and gump, in one line: the relative owns a conditionally invariant measure
because fresh symbols keep arriving.

### S9. Lemma 5 (frozen drive cells: why a one-generation window is already too much to condition on) [proved]

**Lemma 5.** Gump, any vessel. Let p ∈ 𝓛_w have state x and k live neighbours in 𝓛_{≤ w+1} at time t. Its state at
t + 1 is a function of (x, k), whatever 𝓛_{w+2} holds, **unless k + x = 3 or k = 5**. A cell of 𝓛_{w+1} (three
neighbours in 𝓛_{w+2} ∪ 𝓛_{w+3}) is determined by (x, k) iff (x, k) = (0, 0) or k ≥ 6. For the 2D rule: unless
k + x = 2 or k = 4; and (two unknown neighbours) iff (x, k) = (0, 0), (1, 2) or k ≥ 5.
*Proof.* p has one neighbour deeper than 𝓛_{w+1}, so n ∈ {k, k + 1}; "alive next iff n + x ≥ 4 and n ≤ 5" gives
different answers at n = k and n = k + 1 iff k + x = 3 (the threshold) or k = 5 (the cap). For three unknown
neighbours n ranges over [k, k + 3], which lies outside [4 − x, 5] iff k + 3 < 4 − x or k ≥ 6, and never inside.
(2D, two unknown: [k, k + 2] lies inside [3 − x, 4] exactly for (x, k) = (1, 2), the safe cell of Lemma A.) ∎

Consequences. (i) Given the top w + 2 layers at time t, a drive cell of 𝓛_w at time t + 1 has a conditional law
that is a point mass in every context except the two named; no bound δ ≤ P(drive cell alive | previous
generation) ≤ 1 − δ holds over all contexts. Fresh dice at every generation (D2, D3) differ from gump's drive
by an unbounded likelihood ratio over two consecutive generations, at every depth w. So the dice models are
not small perturbations of gump in any ratio sense that involves two times; whatever makes them work at depth
4–8 is screening by the layers above (S12), not closeness of the drive. (ii) The two sensitive contexts are
T5's two mechanisms: the threshold (present in the uncapped rule, where by Cor. 4a it carries boundedly many
changes per cell) and the cap. A bulk cell passes on what lies beneath it only when its count is at the
threshold or at the cap; the parity bulk of R_w passes it on always.

### S10. What equal-time finite energy of the drive gives: Theorems U and H [proved]

w = 1. A *unit* is an edge cell (2D) or the three face cells of one cube (gump, periodic face or interior;
board, cube lemma). ω_c is the drive read by unit c: the two cells beneath (2D), or the six cells
(u_x, u_y, u_z, v_x, v_y, v_z) with b_a = u_b + u_c + v_a (gump). Units read disjoint sets of drive cells which
together make up 𝓛_1 ∪ 𝓛_2 (each cell of 𝓛_1 is a face of exactly one cube of the layer; D is a bijection
𝓛_0 → 𝓛_2). For a face state z let D_c(z) be the set of values of ω_c for which every face cell of unit c is dead
at the next generation. Unit c is *inert* in z if D_c(z) is everything (2D: a dead cell with k = 0), *locked* if
D_c(z) = ∅ (2D: a live cell with k = 2; gump: board E10). F(z) = number of non-inert units; z is *killable* if no
unit is locked. The face is empty at t + 1 iff ω_c(t) ∈ D_c(Z_t) for every unit.

Hypotheses on the equal-time kernel κ_t of S4, for all face states z of positive probability at time t:
- **UFE(θ):** for every non-inert unit c, κ_t(ω_c ∈ D_c(z) | z, the drives of all other units) ≤ θ < 1.
- **LFE(δ):** for every unit c and every value ω, κ_t(ω_c = ω | z, the drives of all other units) ≥ δ > 0.
(Uniform finite energy of the drive given the face, in units; Newman–Schulman's notion, through
`library/notes/source-requests.md` §4. For dice: δ = min(ρ, 1−ρ)² in 2D and ⁶ in gump, θ = 1 − δ.)

**Theorem H.** UFE(θ) at time t gives h_t ≤ E[θ^{F(Z_t)} | T > t]. LFE(δ) at time t gives
h_t ≥ E[δ^{F(Z_t)} ; Z_t killable | T > t].
*Proof.* By Lemma 3, h_t = Σ_z λ_t(z | alive) κ_t(∩_c {ω_c ∈ D_c(z)} | z). Order the units; the chain rule writes
the last factor as a product over units of κ_t(ω_c ∈ D_c | z, earlier units in their D's), and each factor is an
average of conditional probabilities given all other units' drives: ≤ θ for a non-inert unit, ≥ δ for a
non-inert, non-locked one, = 1 for an inert one. ∎

**Theorem U.** Let g be a number of generations in which the free-drive face game empties every state (2D,
L ≥ 5: g = 3, `exponent/theorems.md` Theorem B; gump: g = 2 on the hull faces R = 3, 5, board L0b.3; not known in
general), and U the number of units (L, or A/3). If LFE(δ) holds at times t, …, t + g − 1 then
P(T ≤ t + g | T > t) ≥ δ^{gU}; on a window of gj generations P(T > t + gj | T > t) ≤ (1 − δ^{gU})^j.
*Proof.* The game's strategy prescribes at each of its g steps a non-empty set of drives for each unit; by the
chain rule its κ-probability is ≥ δ^U at whatever state the chain is in; apply this along the Markov chain of
Lemma 3. ∎

*Smallest cases.* A lone cell (2D, or gump interior): the non-inert units are its own and those of its four
other in-face neighbours' cells, F = 5 in both rules, none locked. So **δ⁵·P(n_t = 1 | T > t) ≤ h_t**: under
LFE the ratio h/p₁ is bounded below independently of the size of the face. In D2(L, ρ) the factor is exact,
(1 − ρ²)⁵ = 0.2836 at ρ = 0.472, and the board's exact h/p₁ = 0.394 with 72% of deaths from one cell is
0.72 × 0.394 = 0.2837.

What these are worth. Theorem U is an **upper bound e^{CA} on the lifetime of the deterministic rule, in a vessel
of any depth, under one equal-time hypothesis** (the only unconditional bound is 2^N, the volume). Theorem H
says the hazard is an exponential moment of the number of active units of the face, with base between δ and θ:
"death is the tail of the living face's own distribution" becomes an inequality, and the area law's lower bound
is reduced to: UFE, plus "the living face is rarely sparse". Neither theorem bounds that tail. Both hypotheses
quantify over *all* face states at the times concerned, including states of tiny probability, and UFE/LFE in
the strict form fail if some face state and some drive elsewhere force a unit's drive (a pattern on three
layers with no predecessor would do it). They are exactly testable in an enumerable vessel; I do not know that
they hold in gump.

### S11. The end-game rows under dice, in closed form, against the measured ones [formula proved; comparison uses measured numbers]

By Lemma 3 with π = the face population, the death law depends on the rows K_t(n, ·) = law of the next
population given n. For n = 1 and product dice the row is explicit.

**Gump, lone interior face cell** (axis x of cube c). The only cells that can be alive next are the lone cell and
its six in-face neighbours, each iff its b = 3. Two of the six are the other two cells of cube c; the other four
lie in four different cubes. With A_x = {u_y = u_z = v_x = 1} etc.:
P(some cell of cube c alive next) = 3ρ³ − 3ρ⁵ + ρ⁶, and each of the four others is alive with probability ρ³,
independently. So

  P(death | lone cell) = (1 − 3ρ³ + 3ρ⁵ − ρ⁶)(1 − ρ³)⁴,   E[n′ | lone cell] = 7ρ³.

| ρ | P(n′ = 0) | P(1) | P(2) | P(3) | E n′ |
|---|---|---|---|---|---|
| 0.4155 (bulk density; D3 at w = 1) | 0.6065 | 0.3035 | 0.0737 | 0.0141 | 0.50 |
| ½ (gump on parity, w = 1) | 0.4122 = 108045/262144 | 0.3729 | 0.1565 | 0.0465 | 0.875 |
| 0.52 | 0.367 | 0.378 | 0.179 | 0.059 | 0.98 |

**2D, lone edge cell:** P(death) = (1 − ρ²)⁵, E n′ = 5ρ²: 0.2836 and 1.11 at ρ = 0.472; 0.2373 and 1.25 at ρ = ½.

Measured (board L1.1, hull faces A = 30…84): P(death | n = 1) = 0.41, 0.38, 0.38, 0.37 and E[n′ | n = 1] = 1.00
(A = 63). So from its last cell a gump face dies with probability 0.38, not the 0.61 of dice at the bulk
density, and has one descendant on average, not half of one. **One number, an effective density ≈ 0.52 of the
cells beneath a last cell and its neighbours, reproduces both** (death 0.38 ⇔ ρ = 0.514; mean 1 ⇔ ρ = 0.523).
Caveats: hull faces are mostly rim (E3) and the formula is for an interior cell; a rim cell has fewer
neighbours to be born, so the interior value implied by the data is lower than 0.38 and ρ_eff a little higher;
and "product at density 0.52" is a one-parameter description, not a derived law. The same reading of the 2D
data (toy2d README: deaths from one cell 53% and h/p₁ = 0.45 at L = 16, 46% and 0.28 at L = 32) gives
P(death | n = 1) = 0.24 and 0.13, i.e. ρ_eff = 0.50 and 0.58 against a bulk 0.472.

Reading, in the terms of S4: κ_t(· | z) for a precarious z is *richer* than dice of the bulk density, in both
rules: a face cell that is still alive is alive because of what lies beneath it, and what lies beneath
persists. (The 4 × 6 strip of L3 shows the opposite sign; the critic's judgement that no enumerable vessel
speaks for the regime of the law stands.) Structure behind it, from the cube lemma and the notebook's fauna: a
kagome triangle in the face (38% of three-cell faces, notebook 2026-11-13) has k = 2 for each cell, so each
survives iff its b ≥ 1. If the triangle is the three faces of an inner cube and the cube's other three faces
(its u's, in 𝓛_1) are alive, every b ≥ 2: this is the closed-cube still life S6a seen from above. If it is the
other orientation and its three private cells (the v's, a triangle in 𝓛_2) are alive, every b ≥ 1: the still
life S6b. Either way the last ember is the top of a still life whose other half is the drive.

Two consequences. (i) For gump, dice at density ½ have an end-game much closer to the true one than dice at
the bulk density (0.41 against 0.38 measured; 0.61). "Gump on parity" is, at the last cell, a better model than
D3 at 0.4155. (ii) The class 𝒦 of Aim B cannot be "close to product at the bulk density": the true kernel is
tilted by a factor 1.6 in the death probability already at n = 1. It has to allow a density beneath the face
that depends on the face.

### S12. Where the dice are needed: screening [guessed, with the evidence]

Evidence already in the repository (sampled; unchecked): the 2D driven model D2(L, ρ; 8) has
ln τ = 7.432 / 7.417 at L = 16 and 9.151 / 9.182 at L = 20 for ρ = 0.30 / 0.60 against 7.432, 9.165 at ρ = 0.472
(exponent study F9), and 7.426, 9.055 for the true rule in 16 rows; D3 on periodic faces at depth 6 and 8 is
within 0.03 nats of the true slab at A = 27…60 (F8). At depth 1 the dependence on ρ is not small
(D2(16, ρ; 1): 8.6350 at 0.472, 8.6764 at 0.5, exact).

**Conjecture S (screening).** For each rule there is a depth w₀ such that, for w ≥ w₀, the exponent of the driven
system D_w[κ] is the same for every drive kernel κ in a class that contains product dice of any density in an
interval around the bulk density and the true bulk. Then, by Lemma 1, **gump has the same exponent as the
deterministic automaton R_w(parity)**, whose top is an honest finite Markov chain; and the answer to (b) is that
the bulk has to satisfy nothing dice-like: the randomness a face uses is made in the w₀ layers beneath it, by
the true rule, and the bulk below only has to keep 𝓛_{w₀} in the chaotic phase. Lemma 4 (activity at the face
is paid for by overcrowding discounted geometrically with depth) and Lemma 5 (a cell forwards what is beneath
it only at the threshold or the cap) are the two proved statements pointing this way; neither proves it.
What would prove it is a contraction statement for the map (law of the drive at depth w) ↦ (law of the top
w − 2 layers and their drive), which is a uniqueness statement for the quasi-stationary law in the depth
direction. Not attempted yet. An exact small test is requested below (L6).

---

## Round 2 report

**Claims.**
1. [proved] Lemma 1′: any local rule on the top layers over a deep-permutive bulk is a chain driven by fresh
   uniform symbols; so every rational probabilistic automaton on finitely many layers is the top of a
   deterministic one. Prop. 1″: R_w(Q) has an exact conditionally invariant measure μ ⊗ uniform and an exactly
   geometric wait.
2. [proved] Lemma 5: a drive cell's next state is fixed by the previous generation of the layers above and
   around it except at the threshold (k + x = 3) or the cap (k = 5).
3. [proved] Theorem H: under equal-time finite energy of the drive given the face (units = cells or cube
   triples), E[δ^F; killable] ≤ h ≤ E[θ^F], F = number of active units of the face; h ≥ δ⁵ p₁. Theorem U: under
   LFE(δ), lifetime ≤ g·δ^{−gU}, a bound in the area for any depth of vessel (g = 3 in 2D; g known only for two
   hull faces in gump).
4. [formula proved] From a lone interior cell, dice of density ρ give P(death) = (1 − 3ρ³ + 3ρ⁵ − ρ⁶)(1 − ρ³)⁴,
   E n′ = 7ρ³ (2D: (1 − ρ²)⁵, 5ρ²). [measured numbers read against it] gump's last cell behaves as if the cells
   beneath had density ≈ 0.52, not 0.4155.
5. [guessed] Conjecture S (screening): beyond a depth w₀ the exponent does not depend on the drive, so gump and
   R_w(parity) share it.
Corrections S7 accepted in full; `claims.md` updated.

**Weakest step.** Theorems H and U quantify over every face state; I have no evidence that UFE/LFE hold in
gump, and a local pattern without predecessor would break the strict form. S11 fits one parameter to two
numbers from hull faces that are mostly rim. Conjecture S rests on sampled values I cannot check and on no
mathematics beyond Lemmas 4 and 5.

**A remark for the critic to route (not my toolkit).** For the population alone, a comparison needs no
certificate: if q is a stochastically monotone kernel on {0, …, A} with 0 absorbing and every true row dominates
it, K_t(n, ·) ⪰ q(n, ·), then by induction on Lemma 3's marginals λ_t ⪰ λ_0 q^t, so P(T > t) ≥ P_q(T > t); and with
⪯ the reverse. If path does not have this, it is theirs.

**Lab requests** (exact or arithmetic on existing tallies).
- L4. From `fluct_tables.npz`: the rows Tr[1, ·], Tr[2, ·], Tr[3, ·] (law of n′) at A = 45, 63, 84, to set against the
  ρ = 0.52 row of S11 (0.367, 0.378, 0.179, 0.059, 0.015); and from J: E[n₂ | n]/A for n = 1, …, 6 and at the mode
  of n, each A. (Is the layer beneath a nearly empty face denser or sparser than beneath a typical one?)
- L5. Check of S11's formula by enumeration of the drive around a lone cell of a periodic face (the six cells of
  its cube and the three beneath each of its four other in-face neighbours): P(face empty next) = 0.6065 at
  ρ = 0.4155 and 108045/262144 at ρ = ½; and that F = 5.
- L6. Sensitivity to the drive, exact: ln τ of D2(L, ρ; w) at ρ = 0.30, 0.472, 0.60 for w = 1, L = 8, 12, 16 and for
  w = 2, L = 5, 6, 7 (2^14 states). Question: is the spread in ρ smaller at w = 2 than at w = 1 at equal L?
- L7. The free-drive face game on periodic gump faces of 12 and 18 cells (slabs 2 × 2 and 2 × 3): the largest
  number of generations any configuration needs (g of Theorem U).
- L8 (if cheap). UFE/LFE in the 4 × 6 strip at t = 3, …, 10: over all edge states of positive probability and all
  cells, the largest and smallest values of κ_t(b_x ∈ S | edge, the other cells' b) for S ranging over the death
  sets D_x(z); in particular whether any is exactly 0 or 1 for a non-inert, non-locked cell.

**Next.** (i) Conjecture S: try to prove a weak form for the relatives themselves (monotonicity or continuity of
τ(D_w(ρ)) in ρ is not available; what might be is a bound on how much the top w − 2 layers' equal-time law can
depend on the drive law, through Lemma 5's sensitive contexts). (ii) Use L4 to decide whether a state-dependent
density ρ(n) is a workable 𝒦. (iii) Exam entries S-E1, S-E2 are filed in `swarm/PREDICTIONS.md`.

---

## 2026-11-13, round 3

Read for this round: the critic's addendum (the probability line's model E₁(π) and its Theorem A, as stated on
the board, "Definitions" and lemma exchange "One row over dice") and the reply to round 2 with lab L4–L8.
I have not read the probability line's directory; everything I use of it is the board's statement.

### S13. Corrections to round 2 (all three accepted)

1. **S11 / C14.** "The drive beneath a precarious face is richer than the bulk" is wrong as worded. Lab L4: the
   whole layer beneath a face of one to twelve cells has density 0.33–0.39 (A = 45…84) against 0.44 beneath a
   typical face: it is *poorer*. What the n = 1 row shows is that the eighteen cells read by the last cell and
   its six neighbours behave like dice at density ≈ 0.52. Correct statement: **locally richer, in a layer that
   is poorer.** The fit is better than I had a right to expect: the dice row at 0.52,
   (0.367, 0.378, 0.179, 0.059, 0.015), against the measured rows (0.384, 0.355, 0.175, 0.070, 0.014),
   (0.377, 0.353, 0.181, 0.069, 0.016), (0.372, 0.333, 0.212, 0.066, 0.017) at A = 45, 63, 84: one parameter, five
   numbers, all within 0.03 (two of the five were used to choose the parameter). It fits the picture of S11:
   what survives of a face is the top of a small supported structure, and the support is under the survivors,
   not under the face.
2. **Conjecture S** has no exact support: at the one depth the lab can reach (w = 2, L = 5…8, lab L6) the spread
   of ln τ over ρ ∈ {0.30, 0.472, 0.60} is larger than at w = 1, and grows with L. Its support is the sampled
   values at depth 6–8 only, and the approach in depth is not monotone for gump (board E13). Tag stays "guessed";
   S-E2 is its test.
3. **Theorems H and U** are implications whose hypotheses are known to fail in the one vessel where they could
   be examined (lab L8: in the 4 × 6 strip, from t = 3 the conditional probability of a death set is exactly 0 or 1
   in 39–90% of the contexts) and are known to hold in none. Theorem U is in addition conditional on g (g = 2 on
   four gump faces, lab L7 and L0b.3; unknown in general). They stand as "what finite energy of the drive would
   give", not as descriptions of gump.

### S14. Theorem A: a deterministic automaton for which the length law is a theorem [proved here: (i); cited: (ii)]

**The automaton 𝒜(L).** Cells (x, j), x ∈ Z_L, j = 0, 1, 2, …; states 0/1.
- Row 0 follows the 2D rule B34/S234 on the cross: its neighbours are (x ± 1, 0), (x ± 2, 0), (x, 1), (x, 2).
- Every cell of a row j ≥ 1 copies the cell two rows beneath it: y_{t+1}(x, j) = y_t(x, j + 2).
- Start: row 0 with any law; beneath it, independent fair bits ξ_{x,i} (i ≥ 1), each written into the two cells
  (x, 2i − 1) and (x, 2i).

Then y_t(x, 1) = y_t(x, 2) = ξ_{x, t+1} for all t ≥ 0: the two cells beneath an edge cell are always equal, and the
bit they carry at generation t has not been read before. So row 0 is exactly the probability line's chain E₁(π)
at its anchor π = (½, 0, ½), from generation 0. (The bulk rule is the simplest deep-permutive rule of S1 and the
statement is Lemma 1 for a start that is uniform on the paired configurations; here it can be seen directly.)

*Variant from the uniform product measure* (Lemma 1′, checked by the critic): rows 1 and 2 both copy the cell of
row 3 in their column, y_{t+1}(x, 1) = y_{t+1}(x, 2) = y_t(x, 3); rows j ≥ 3 follow any deep-permutive rule, for
instance parity on the cross, and may read rows 1 and 2; start uniform on rows ≥ 3, anything above. Then row 0
is E₁(½, 0, ½) from generation 1. With a source alphabet Z_m and two decoder maps φ₁, φ₂ : Z_m → {0, 1} in rows
1, 2, the same construction gives E₁(π) for every rational π.

**Theorem A.** For even L let λ_L be the Perron eigenvalue of E₁(½, 0, ½) on non-empty rows, μ_L its
quasi-stationary law and τ_L = 1/(1 − λ_L).
(i) [source; S8, Prop. 1″] In 𝒜(L) started with row 0 distributed as μ_L, the edge dies at a time T with
P(T > t) = λ_L^t exactly, and conditioned on {T > t} the configuration has again the starting law. From any
other law of row 0 with a live cell, P(T > t) = c·λ_L^t (1 + o(1)) (the chain on non-empty rows is irreducible
and aperiodic; board, "Definitions").
(ii) [the probability line's Theorem A and its three-generation bound, as stated on the board; its lower bound
is modulo two percolation facts not yet on the shelf, F1: the critical density of two-parent oriented site
percolation is ≤ 0.7491, and F2: finite-volume survival] there is c > 0 with **e^{cL} ≤ τ_L ≤ 3·8^L**.
(iii) [lab L4.1, exact] ln τ_L = 6.5319, 9.4733, 12.2492, 13.5946 at L = 8, 12, 16, 18 (≈ 0.67 per cell).

So 𝒜(L) is a fully deterministic cellular automaton, with the 2D rule's own edge, in which an edge row of L
cells dies after an exactly memoryless wait whose mean is exponential in L, with proof (modulo F1, F2).

**How 𝒜(L) differs from the 2D rule in a strip, exactly.**

| | 2D rule, strip W × L | 𝒜(L) |
|---|---|---|
| rule and neighbourhood of the edge row | B34/S234, cross | the same |
| rule beneath | B34/S234 | copy the cell two rows down (variant: two decoder rows, then any deep-permutive rule) |
| what an edge cell reads beneath it | two cells, different, correlated in time and with the edge | two equal cells carrying one fresh fair bit: the cell follows B34/S234 on its four in-row neighbours when the bit is 0, B12/S012 when it is 1 |
| vessel | W rows, finite | half-infinite; with H rows beneath the statement holds for ⌊H/2⌋ generations |
| feedback from the edge into the bulk | yes | not needed (allowed in the variant) |
| empty edge absorbing (T2); three-generation game | yes | yes |
| wait | memoryless as measured, after T0, settled replicas removed | exactly geometric from μ_L ⊗ start |
| exponent per cell | 0.36–0.42 (measured) | ≈ 0.67 (exact to L = 18); proved positive and ≤ ln 8 |
| energy and overcrowding in the bulk (T5) | drive only at overcrowded cells | none: the bulk is a conveyor |

The relative is far from the rule in its exponent and in everything beneath the edge. It is close in one
respect only: the edge itself is the rule's edge, and the mechanism the probability line uses (every cell
within distance 2 of a live cell can be made alive by b = 0 or by b = 2) is a property of that edge.
For gump no such relative has the law as a theorem: the dice theorem is for the 2D edge. One structural
obstacle to copying it, for whoever tries: **a gump face can overcrowd itself and a 2D edge cannot.** A face cell
with all six in-face neighbours alive is dead next whatever lies beneath (n ≥ 6); an edge cell has at most
four in-row neighbours, below the cap of five, and can always be kept alive by b = 0. Also a dead face cell
with three live in-face neighbours is born only for b ∈ {1, 2}, so a two-valued drive (b = 0 or 3 for a whole
cube) does not reach every cell near a live one; three values are needed.

### S15. Theorem L: how a dice theorem of the comparison kind transfers to a deterministic system [proved]

The probability line's lower bound goes through one inequality: the row dominates five-parent oriented site
percolation of density p. That inequality needs much less than dice.

For an edge state z ⊂ Z_L let E(z) be the cells within distance 2 of a live cell, and for x ∈ E(z) let A_x(z) ⊂
{0, 1, 2} be the values of b_x for which x is alive next: non-empty for every x ∈ E(z) (it always contains 0 or 2).
- **INS(p) at time t** (insertion tolerance of the drive): for every edge state z of positive probability and
  every x ∈ E(z), κ_t(b_x ∈ A_x(z) | z, (b_y)_{y ≠ x}) ≥ p. (κ_t is the equal-time kernel of S4, w = 1.)
- Percolation: ω(x, s) i.i.d. Bernoulli(p); W_{s+1} = {x : ω(x, s + 1) = 1 and W_s meets {x, x ± 1, x ± 2}}.

**Theorem L.** Take the 2D rule in any vessel, of any depth, with any initial law (deterministic bulk
included), or any other process whose edge row follows the rule. If INS(p) holds at the times t₀ ≤ t < t₁, then
for every t ≤ t₁ the law of the edge at time t dominates the law of W_{t − t₀} started from W₀ = (the edge at t₀):
there is a coupling with W_{t−t₀} ⊆ Z_t. Hence P(T > t) ≥ P(W_{t−t₀} ≠ ∅), and every lower bound on the survival of
five-parent oriented site percolation of density p on the ring (the probability line's Theorem A when
1 − (1 − p)² exceeds the two-parent critical density, i.e. p > 0.4991 given F1) is a lower bound for the edge on
that window.
*Proof.* Induction on t, on marginal laws only. Suppose (Z_t, W) are coupled with W ⊆ Z_t. Given Z_t = z, the next
edge is {x : b_x ∈ A_x(z)} with b drawn from κ_t(· | z) (Lemma 3). By INS(p), each indicator Y_x = 1[b_x ∈ A_x(z)],
x ∈ E(z), has conditional probability ≥ p given the others, hence given Y_1, …, Y_{i−1} in any order; drawing them
in turn with uniforms U_x, Y_x = 1[U_x < P(Y_x = 1 | earlier)], and putting ω_x = 1[U_x < p], gives ω i.i.d.
Bernoulli(p) with ω_x ≤ Y_x on E(z); draw ω independently off E(z). Then W′ = {x : ω_x = 1, W meets {x, x±1, x±2}}
⊆ {x ∈ E(z) : ω_x = 1} ⊆ Z_{t+1}, because W ⊆ z. The law of ω does not depend on (z, W), so W′ has the percolation
law from W, and Z_{t+1} has the law λ_t K_{t+1} = λ_{t+1}. ∎

Remarks. (a) The hypothesis is one-sided, at equal time, about one cell given the row and the drive of the
other cells; no independence between cells, no mixing in time, no stationarity. This is the weakest property I
can state under which the one existing dice theorem transfers, and it is exactly computable in an enumerable
vessel. (b) In 𝒜(L) it holds with p = ½ for all t. With a paired conveyor started from biased bits (density q)
it holds with p = min(q, 1 − q). (c) **It fails for the 2D rule's own statistics, and already for independent
dice at the bulk density**: a lone cell or a dead cell with one live neighbour is alive next only for b = 2,
probability ρ² = 0.22 at ρ = 0.472 (0.25–0.34 at the effective densities of S11), far below 0.4991. So what
stands between the theorem and the 2D rule is not the quality of the rule's self-made randomness; it is the
reach of the dice theorem, which needs each such cell to be kept alive with probability ½. (d) *Lemma 3 at lag
k.* λ_{t+k} = λ_t K_t^{(k)} with K_t^{(k)}(z, ·) the law of the top k generations later given the present top state
only. A dice theorem proved with block events k generations long transfers, by the same induction along
t₀, t₀ + k, t₀ + 2k, …, under the corresponding domination hypothesis on K_t^{(k)}. Nothing about the past and
nothing about the intermediate states of the bulk enters beyond that kernel.

### S16. Where the line stands [assessment]

In the order of PROBLEM.md's list of what would count.

- *A theorem for gump or the 2D rule themselves:* none, and not by this route. The source toolkit proves
  randomness from permutivity and an invariant product measure; gump has neither (it forwards information only
  at the threshold or the cap, Lemma 5; it is far from surjective), and in a finite vessel there is not enough
  entropy for any statement that conditions on the whole past (Lemma 2) nor any exact quasi-stationary law
  (board, trapdoors (v)). What a proof would have to control is the equal-time kernel κ_t (Lemma 3), a property
  of the quasi-stationary state itself.
- *A close relative for which the law is a theorem, relation stated exactly:* 𝒜(L), S14, with the probability
  line (modulo F1, F2). Its limits are in the table of S14. Every dice model with rational local randomness
  has such a relative (Lemma 1′), so each further dice theorem becomes a theorem about a deterministic automaton
  at no cost; "gump on parity" R_w is the one for D3 at ρ = ½.
- *A theorem under one stated, testable hypothesis:* Theorem L (lower bound, hypothesis INS(p), p > 0.4991; the
  hypothesis is false for the 2D rule's statistics, which is informative); Theorems H and U (hazard between two
  exponential moments of the face's active units; lifetime at most exponential in the area for any depth;
  hypotheses fail strictly in the one enumerable test).
- *A formula for γ:* none.
- *Side facts:* h/p₁ bounded below independently of A under finite energy, with the exact dice value
  (1 − ρ²)⁵ (2D) and (1 − 3ρ³ + 3ρ⁵ − ρ⁶)(1 − ρ³)⁴ (gump); gump's whole n = 1 row is that of dice at local density
  0.52; the last ember as the top of a still life (S11). T5: Lemma 4 and Corollaries 4a, 4b (a threshold bulk is
  not a source; activity at a face is bounded by overcrowding discounted with depth); Corollary 4a closes the
  question left open in threshold.md §6.
- *Open, mine, not reachable with these tools as far as I can see:* Conjecture S (screening); a class 𝒦 that
  contains gump's κ_t and carries a lower bound (S11 and Theorem L(c) say what it must allow: a drive whose
  local density depends on the face, and cells kept alive with probability well below ½); C8 beyond its sketch.

I judge that this line has given what it can. The two exam entries stand as filed.

---

## Round 3 report (interim, paused)

_Written when the lead paused the group (usage budget). Everything above in round 3 (S13–S16) is finished
work that I stand behind; nothing was cut off in the middle of an argument._

**Claims added.**
1. [proved, with the probability line's Theorem A cited from the board, modulo F1, F2] Theorem A: the
   deterministic automaton 𝒜(L) (the 2D rule's edge over a conveyor of paired fair bits) has an exactly
   geometric wait with e^{cL} ≤ τ_L ≤ 3·8^L; exact values to L = 18 from the lab. Table of differences from the
   2D rule in S14.
2. [proved] Theorem L: under equal-time insertion tolerance INS(p) of the drive, the edge of any process that
   follows the 2D rule in row 0 dominates five-parent oriented site percolation of density p, in marginal law
   at each time; so the dice theorem transfers on any window where INS(p > 0.4991) holds. INS at that level is
   false for dice at the bulk density and for the measured rule.
3. [remark] A gump face can overcrowd itself (six live in-face neighbours kill a cell whatever lies beneath);
   a 2D edge cannot. A two-valued coherent drive does not suffice for gump.
Corrections S13 accepted; `claims.md` is final; exam entries S-E1 and S-E2 are in `swarm/PREDICTIONS.md`.

**Weakest step.** Theorem A(ii) is not mine and rests on F1 with almost no margin (1 − (1 − ½)² = 0.75 against
0.7491). Theorem L's hypothesis is one I can only show to hold in relatives. Everything about gump's own bulk
in this journal is either a no-go statement (Lemmas 2, 5), an exact reduction (Lemma 3), a qualitative bound
(Lemma 4), a reading of tallies (S11, S13.1) or a guess (Conjecture S).

**Lab requests.** None. If someone continues: the dice rows from an edge-sharing pair and from the two
orientations of a kagome triangle at ρ = 0.4155, ½, 0.52 (enumeration of the drive, as in L5), to set against the
measured n = 2 and n = 3 rows (death 0.09–0.10 and 0.018–0.019); and INS for the 4 × 6 strip as L8 was done for
the death sets.

**Done.** S13 (corrections), S14 (Theorem A and the table of differences), S15 (Theorem L), S16 (assessment);
`claims.md` brought up to date; exam entries filed in round 2.
**Half-done.** Nothing. Not yet checked by the critic: S14 (the direct argument for 𝒜(L) is three lines; the
variant is Lemma 1′, already checked), S15 (the marginal-coupling induction), and the remark on gump's
self-overcrowding.
**What I would do next, if resumed.** (1) Read the critic's reply to this round and correct. (2) If the
probability line has by then a multi-generation criterion (its T1), state the lag-k form of Theorem L against
it (S15, remark (d)). (3) Otherwise close: in my judgement the line has given what it can (S16), and the next
message from me would be `source: finished`.
