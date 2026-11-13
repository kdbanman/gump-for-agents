# Open systems, escape rates, and hitting times of rare events in deterministic systems

Request (lead, item 4; counting line). Tags: **[paper]**, **[secondary: X]**.

Two families of results sit here. (A) *Hitting-time laws*: for a stationary process or a measure-preserving
map with enough mixing, the first time a rare set D_n is entered is asymptotically exponential with mean
≈ 1/(λ·μ(D_n)). These are theorems about **deterministic** maps with an **invariant** measure. (B) *Escape
rates*: a map with a hole, a reference measure that leaks, and the leading eigenvalue of a transfer operator.

---

## A. Hitting times of rare events

### A1. Galves and Schmitt 1990: the closest theorem in form to "memoryless wait, exponent ∝ size"

A. Galves and B. Schmitt, "Occurence times of rare events for mixing dynamical systems", Ann. Inst. H. Poincaré
Phys. Théor. 52 (1990), no. 3, 267–281. Read: NUMDAM, https://www.numdam.org/item/AIHPA_1990__52_3_267_0/
(introduction, §2 statement and the first step of the proof; §3 example not read).

**[paper] Setting.** (Ω, A, S, μ): S measurable, μ an S-invariant probability. Assume
(i) a finite generating partition P (⋁_{i≥0} S^{−i}P = A);
(ii) *exponentially strong mixing in ratio form*: there are K > 0, 0 < γ < 1 such that for all atoms
C_n of ⋁_{i<n} S^{−i}P and C_m of ⋁_{i<m} S^{−i}P and all k ≥ n,
|μ(C_n ∩ S^{−k}C_m) − μ(C_n)μ(C_m)| ≤ K γ^{k−n} μ(C_n) μ(C_m).
Let D_n be events with: 1. D_n is measurable with respect to the first n coordinates (⋁_{i<n} S^{−i}P);
2. (1/n) log μ(D_n) → −θ with θ > 0.
T_n = first k with S^kω ∈ D_n; β_n = max{k : μ(T_n ≥ k) ≥ e^{−1}}.

**[paper] Theorem.** 1. T_n/β_n converges in law to the exponential law of parameter 1. 2. (1/n) log β_n → θ.
3. E T_n / β_n → 1.

**[paper] Method.** Show g_n(t + s) − g_n(t)g_n(s) → 0 for g_n(t) = μ(T_n ≥ β_n t) (their (0)); the proof
introduces a sequence of gap lengths d_n and uses (ii) to factorise events separated by a gap. (The text layer
of the scan loses the displayed formulas; I read the statement pages as images but not the remaining
estimates.) The introduction motivates it by large deviations of time averages of an expanding map (the time
to see an empirical frequency q ≠ ρ over a window of N steps is exponential with scale exp(N × free energy))
and says the law being exponential "means that the time needed to perform the large fluctuation is
unpredictable"; it links this to the pathwise approach to metastability (Cassandro–Galves–Olivieri–Vares).

**Does it apply here?** This is the board's "mixing ⇒ exponential" lemma as a published theorem for
deterministic maps, with the exponent identified (θ = decay rate of μ(D_n)). Hypotheses against gump:
- an **invariant probability measure**: a gump vessel has an absorbing set; the natural object is a
  quasi-stationary (conditionally invariant) measure, which is not invariant. The theorem would apply to the
  face process only inside an invariant model (e.g. the stationary bulk of an infinite system, with "face
  empty" replaced by "a window of n cells empty").
- (ii) is ψ-mixing in *time* for a one-dimensional symbolic coding. The rare events D_n are cylinders in
  time (n consecutive time steps). "A row of L cells empty at one time" is a cylinder in *space*; the theorem
  as stated does not cover a spatially extended system. See A3 for space.
- (ii) is not known for gump. It is a ratio bound, as the board says is needed.

### A2. Abadi and Saussol 2010: α-mixing is enough for the exponential *law*

M. Abadi and B. Saussol, "Hitting and returning into rare events for all alpha-mixing processes",
arXiv:1003.4856v2 (2010). Read: arXiv PDF, §1–3 (statements). Journal reference not verified.

**[paper] Theorem 1.** Let (Σ = A^N, shift, μ) be α-mixing (α(g) = sup |μ(A ∩ B) − μ(A)μ(B)| over events
separated by a gap g, → 0; no rate assumed). For any sets A_n depending on the first n coordinates with
μ(τ_{A_n} ≤ n) → 0 there are constants λ(A_n) > 0 with
sup_t |μ(λ(A_n) μ(A_n) τ_{A_n} > t) − e^{−t}| → 0; lim sup λ(A_n) ≤ 1; the return time is asymptotically a
mixture of a point mass at 0 and an exponential. Example 2: every sequence of cylinders [a_0 … a_{n−1}],
uniformly in a, periodic or not.

**[paper] remarks.** The parameter is λ(A)μ(A), "where λ(A) is a positive number related to the short
recurrence properties of the set A" (the Galves–Schmitt approach). For ψ-mixing systems K ≤ λ(A) ≤ K′ for
constants K, K′ > 0 [secondary: they cite Abadi 2006]; under α-mixing alone λ(A) can be arbitrarily small.
α-mixing is "the weakest among many types of mixing conditions".

**Does it apply here?** It separates two things the board's graveyard (3) warns about. The exponential
*shape* of the waiting-time law needs only α-mixing. The *scale* is 1/(λ(A)μ(A)); mixing of covariance type
says nothing about how small μ(A) is, which is where the area law lives. Same caveats as A1: invariant
measure, cylinders in time.

### A3. Abadi, Chazottes, Redig and Verbitskiy 2003: patterns in space, d ≥ 2

M. Abadi, J.-R. Chazottes, F. Redig and E. Verbitskiy, "Exponential distribution for the occurrence of rare
patterns in Gibbsian random fields", arXiv:math/0310355 ("to appear in Commun. Math. Phys."). Read: arXiv PDF,
abstract and §2 through Remark 2.8.

**[paper] Setting.** A translation-invariant random field P on A^{Z^d}, d ≥ 2. C_n = [0, n]^d. For an
n-pattern A_n, t_{A_n} = the smallest k such that A_n occurs at some translate x with 0 ≤ x_i ≤ k.
Mixing function ϕ(m) = sup (1/|A_1|) |P(E_{A_1} | E_{A_2}) − P(E_{A_1})| over events depending on finite sets
A_1, A_2 at distance ≥ m (note the division by |A_1|: "non-uniform"). The field is *non-uniformly
exponentially ϕ-mixing* if ϕ(m) ≤ C_1 e^{−C_2 m} (2.5); examples: Gibbs fields in the Dobrushin uniqueness
regime, e.g. the high-temperature Ising model.

**[paper] Theorem 2.6.** For a translation-invariant Gibbs field satisfying (2.5) there are constants
C, c, ρ > 0 and 0 < Λ_1 ≤ Λ_2 such that for every n and every n-pattern A_n there is λ_{A_n} ∈ [Λ_1, Λ_2] with
|P( t_{A_n} > (t / (λ_{A_n} P(C(A_n))))^{1/d} ) − e^{−t}| ≤ C P(C(A_n))^ρ e^{−ct} for all t > 0.
And: "P(C(A_n)) … is bounded above by exp(−c′n^d), with c′ > 0, by the Gibbs property."

**[paper] Remark 2.8.** Earlier results for random fields assumed ψ-mixing, and "most Gibbs random fields
(including the Ising model at high temperature) cannot satisfy such a property".

**Does it apply here?**
- This is the spatial statement: in a Gibbs field every pattern on n^d sites, the empty one included, has
  probability ≤ e^{−c′ n^d}. The exponent is the **number of sites** because of the Gibbs property (uniformly
  positive conditional probabilities of local changes), not because of mixing.
- A warning for anyone asking gump's face for ψ-mixing in two dimensions: by Remark 2.8 that is too strong
  even for the high-temperature Ising model. The usable condition is (2.5).
- The field here is a static random field; the "time" is a search volume. No dynamics. Whether the
  stationary space-time field of a deterministic automaton is Gibbs in this sense is not addressed.

---

## B. Maps with holes

### B1. Demers and Young 2006 (survey; includes what Pianigiani–Yorke did)

M. Demers and L.-S. Young, "Escape rates and conditionally invariant measures", Nonlinearity 19 (2006),
377–397. Read: author's copy, https://www.cims.nyu.edu/~lsy/papers/holes.pdf, §1–3 and part of §5.

**[paper]** T̂ : M̂ → M̂, hole H, M = M̂ \ H, M^n = points not escaped by time n. Escape rate of an initial
measure μ: −lim (1/n) log μ(M^n) when it exists; it depends on μ, and two measures with density ratio bounded
above and below have the same rate. μ on M is *conditionally invariant* if T_*μ(A)/T_*μ(M) = μ(A) for all A;
then μ(M^n) = λ^n with λ = μ(M^1): the escape time is exactly geometric.

- **Theorem 3.1.** Under a mild condition (the set of points that escape at step 1 and have pre-images of all
  orders inside M has positive Lebesgue measure), for *every* λ ∈ [0, 1) there are uncountably many absolutely
  continuous conditionally invariant measures with escape rate −log λ. So conditional invariance alone
  selects nothing; a "natural" one must be singled out as the limit of the renormalised push-forwards of
  Lebesgue measure.
- **[secondary: this paper on Pianigiani–Yorke]** G. Pianigiani and J. A. Yorke, "Expanding maps on sets which
  are almost invariant: decay and chaos", Trans. Amer. Math. Soc. 252 (1979), 351–366, introduced
  conditionally invariant measures, with the billiard table with a hole as the motivating question, and
  treated expanding maps of R^n admitting a finite Markov partition after the hole is cut, by showing that the
  normalised transfer operator maps a cone of densities into itself and that iterates converge. (Original
  **not obtained**: ams.org refuses automated clients.)

- **[paper] Existence criterion (§2.1).** A non-trivial conditionally invariant measure (0 < λ < 1) exists if
  and only if there is a backward-infinite orbit inside M that falls into the hole at some finite future time:
  points x_i ∈ M, i ≤ n, with T x_i = x_{i+1} and T̂ x_n ∈ H.

**Does it apply here?**
- **A finite deterministic system has no non-trivial conditionally invariant measure.** [mine, one line from
  the criterion above] In a finite set a backward-infinite orbit repeats a point, hence lies on a cycle, hence
  never reaches the hole. So for the deterministic rule in a finite vessel there is no exact quasi-stationary
  law and no exactly geometric waiting time; "memoryless" can only be an approximate statement on time scales
  short compared with the recurrence time of the finite map. Exact statements need either dice
  (`qsd.md`) or an infinite system. This is the precise form of the board's remark that Darroch–Seneta
  "applies to a dice model, not to the deterministic rule".
- Where conditionally invariant measures do exist (infinite phase space), Theorem 3.1 says there are too many;
  the meaningful one is the limit of renormalised push-forwards of the reference (Lebesgue/uniform) measure.
  The board's definition of τ (hazard among old, unsettled, soup-started replicas) is a finite-time version of
  that limit.

### B2. Keller and Liverani 2009

G. Keller and C. Liverani, "Rare events, escape rates and quasistationarity: some exact formulae",
arXiv:0810.2229v2; J. Stat. Phys. 135 (2009) (journal data as given by the lead; not verified by me).
Read: arXiv PDF, §1–3.1, §5.2.

**[paper] Theorem 2.1 (abstract perturbation).** P_ε a family of bounded operators on a normed space with
leading eigenvalues λ_ε, eigenvectors φ_ε, eigenfunctionals ν_ε, and a uniform spectral gap ((A1)–(A6) in the
paper). Put Δ_ε = ν_0((P_0 − P_ε)φ_0). If the limits
q_k = lim_{ε→0} ν_0((P_0 − P_ε) P_ε^k (P_0 − P_ε) φ_0)/Δ_ε exist, then
lim (λ_0 − λ_ε)/Δ_ε = 1 − Σ_{k≥0} λ_0^{−(k+1)} q_k.

**[paper] For a piecewise expanding mixing interval map** with invariant density φ_0 and holes I_ε shrinking
to a point z (T and φ_0 continuous at z): Δ_ε = μ_0(I_ε), q_k = lim μ_0(I_ε ∩ U_{k,ε})/μ_0(I_ε) with U_{k,ε} the
points that return to the hole for the first time after k + 1 steps, and
- z not periodic: (1 − λ_ε)/μ_0(I_ε) → 1;
- z periodic of period p: (1 − λ_ε)/μ_0(I_ε) → 1 − 1/|(T^p)′(z)|.
For the doubling map: 1 − 2^{−p}. §5.2: for the full 2-shift with p forbidden blocks of length m converging
to points z_i, (log 2 − h)/2^{−m} → Σ_i (1 − 2^{−ℓ(i)}), ℓ(i) the first time the orbit of z_i hits {z_1, …, z_p}.

**Does it apply here?** The formula says: escape rate = (measure of the hole) × (1 − probability of an
immediate return to the hole), to first order **in the size of the hole**, for a system with a spectral gap
that is uniform as the hole shrinks. For the counting line this is the correction factor λ(A) of A2 computed
exactly. Hypotheses that fail or are unknown here: an invariant reference measure with a transfer operator
having a spectral gap on a suitable Banach space (unknown for gump's bulk); and the regime is "hole → 0 at
fixed system", whereas the area law is "system grows, hole = {face empty} shrinks with it".
The repository's measured h ≈ 0.6·P(n = 1) is a statement of the same shape (a hazard equal to the measure
of a pre-hole set times a factor < 1), but nothing here proves it.

### B3. Bunimovich and Yurchenko 2008

L. A. Bunimovich and A. Yurchenko, "Where to place a hole to achieve a maximal escape rate",
arXiv:0811.4438v1; Israel J. Math. 182 (2011) (journal data as given by the lead; not verified).
Read: arXiv PDF, abstract, §2 definitions, statements in §4.

**[paper]** Doubling map with Lebesgue measure λ; Markov holes I_{i,N} = dyadic intervals of length 2^{−N}
(cylinders of length N in the full 2-shift); τ(A) = Poincaré recurrence time of the set A (the least n with
λ(T^n A ∩ A) > 0); Ω_n(A) = points entering A within n steps; ρ(A) = escape rate.

- **Main Theorem.** If τ(I_{j,N}) > τ(I_{i,N}) then ρ(I_{j,N}) > ρ(I_{i,N}), and moreover for **all** n ≥ τ(I_{i,N}),
  1 − λ(Ω_n(I_{j,N})) < 1 − λ(Ω_n(I_{i,N})). (Equal-measure holes; a finite-time statement.)
- **Local escape.** For intervals A_n shrinking to x: ρ(A_n)/λ(A_n) → 1 − 2^{−m} if x is periodic of period m;
  → 1 if x is not periodic (and not dyadic).
- **Monotonicity.** max_i ρ(I_{i,N+1}) = min_j ρ(I_{j,N}).
- Lemma 4.3.1: ρ of the cylinder of a word w is −ln(θ_w/2), θ_w the growth rate of the number of binary words
  avoiding w (a root of a polynomial given by the word's self-overlaps). Theorem 4.8.1: there are sets of
  measure > 1 − ε with escape rate < r, for any ε, r.

**Does it apply here?** Exactly the counting line's setting in the solvable case: a full shift (i.i.d. fair
bits), the hole a single word. It shows that at equal measure the escape rate depends on the hole's
self-overlap (the all-zeros word, period 1, has the **smallest** escape rate among words of its length:
factor 1 − ½). In these theorems the self-overlap of the hole changes the
escape rate by a bounded factor (between ½ and 1 here), not its order of magnitude, which is the measure of
the hole.

### B4. Ferguson and Pollicott 2010

A. Ferguson and M. Pollicott, "Escape rates for Gibbs measures", arXiv:1009.0086v2; Ergodic Theory Dynam.
Systems 32 (2012) (journal data as given by the lead; not verified). Read: arXiv PDF, §1, the assumptions of
§3.1, Theorems 5.1, 5.3, Corollary 5.4.

**[paper] Theorem 5.1.** Σ a topologically mixing subshift of finite type, φ Hölder, μ its equilibrium state,
P(φ) the pressure. Let U_n be nested unions of cylinders of length n shrinking to a point z, with
μ(U_n) ≤ cρ^n and two technical conditions ((4), (5) of §3.1). Then
r_μ(U_n)/μ(U_n) → 1 if z is not periodic, and → 1 − exp(φ^p(z) − pP(φ)) if z has prime period p
(φ^p = Birkhoff sum over the orbit). **Theorem 5.3 / Corollary 5.4:** the same limit for the drop in pressure,
and for the measure of maximal entropy (h_top(σ) − h_top(σ|Σ_n))/μ(U_n) → 1 or 1 − e^{−p·h_top}.
Theorem 1.1 is the same for conformal repellers and balls B(z, ε). They note that Lind (1989) had bounded
the entropy drop for a single forbidden word between c^{−1}μ and cμ, and that the method owes something to
Hirata's proof of the exponential law for return times.

**Does it apply here?** This is the transfer-matrix statement in full generality for **one-dimensional**
finite-type systems with a Gibbs reference measure: removing a cylinder of small measure lowers the
entropy/pressure by (measure) × (1 − overlap factor). Applicable to any dice model of the 2D rule's edge that
is a finite-state Markov chain in time (the edge row over i.i.d. rows: a topological Markov chain on row
states) with hole "row empty"; there the "small parameter" is μ(hole), which is e^{−γL}, and the theorem
gives hazard/μ(hole) → a constant only along a family of nested cylinders in *time*, not along L → ∞. It
does not give γ.

---

## Kac's lemma

Not read in a primary source. It appears on this shelf only through A2/B3, which use Poincaré recurrence and
the relation between hitting and return times ([secondary: Abadi–Saussol cite Haydn–Lacroix–Vaienti for
that relation]). The lead's "counting" starting point (a bijection of a finite set with trapdoor H has mean
hitting time ≥ |X|/(2|H|) − ½ from a uniform start) is the lead's own; I did not look for it in the literature.

## Corrections to this repository's citations

- `requests.md` item 4, "Galves–Schmitt 1997": the paper I could open is Galves and Schmitt **1990**
  (Ann. IHP Phys. Théor. 52, 267–281, "Occurence [sic] times of rare events for mixing dynamical systems").
  I did not find or verify a 1997 paper by the same authors; if the lead means "Inequalities for hitting
  times in mixing dynamical systems", I could not confirm its data.
- `requests.md` item 4, "Abadi on hitting times in mixing systems": the readable ones are Abadi–Saussol
  (arXiv:1003.4856) and Abadi–Chazottes–Redig–Verbitskiy (arXiv:math/0310355). Abadi's Ann. Probab. 2004
  paper is on Project Euclid, which I cannot reach.
- `requests.md` item 4, "Demers–Young 2006": confirmed, Nonlinearity 19 (2006) 377–397. "Pianigiani–Yorke
  1979": confirmed from Demers–Young's reference list (Trans. AMS 252, 351–366); not read.
- `critic/board.md`, graveyard 3 and lemma "Mixing ⇒ exponential": consistent with the literature. The
  published form is Galves–Schmitt's condition (ii) (A1). Two refinements from what I read: the exponential
  *law* needs much less (A2), and in two dimensions the ratio condition must be the non-uniform one (A3).
- `PRIOR-ART.md` §3 verdict ("its justification (why an effective memoryless description holds) has no
  citation I found"): Galves–Schmitt 1990 is such a citation for deterministic maps with ψ-mixing, with the
  same reading of memorylessness as unpredictability from sensitive dependence. It does not cover spatially
  extended systems or systems with an absorbing state.
