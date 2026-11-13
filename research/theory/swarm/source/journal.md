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
