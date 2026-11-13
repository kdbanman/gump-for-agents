# Systems with an absorbing state that are not monotone

Request (lead, item 2): "any exponential-lifetime theorem that survives without monotonicity".

**Short answer from what I could read.** I found no theorem giving a lifetime e^{c·size} for a finite
non-monotone system. What exists and is readable: (a) survival on the *infinite* lattice for two non-monotone
families, by comparison with oriented percolation, where the comparison theorem itself does not need
monotonicity (§1–3); (b) the "threshold contact process" papers the lead listed, which are about a
**monotone, additive** process and so do not belong under this heading (§4). Tags: **[paper]**,
**[secondary: X]**, **[abstract]**.

---

## 1. The comparison theorem (block construction) does not assume monotonicity

R. Durrett, "Ten lectures on particle systems", in *Lectures on Probability Theory (Saint-Flour 1993)*, Lecture
Notes in Math. 1608, Springer 1995, pp. 97–201. Read: author's reprint,
https://sites.math.duke.edu/~rtd/reprints/paper85.pdf (OCR text). Section 4 (statements), a remark in §2, and
the paragraph on Bramson–Neuhauser read; the appendix proofs not read.

### Statements [paper]

Oriented percolation lives on L = {(x, n) ∈ Z² : x + n even, n ≥ 0}; sites are open (ω = 1) or closed; the
ω(x, n) are *M-dependent with density at least 1 − γ* if for any sites (x_i, n_i), 1 ≤ i ≤ I, at mutual sup-norm
distance > M, P(ω(x_i, n_i) = 0 for all i) ≤ γ^I (their (4.1); the paper notes this is weaker than classical
M-dependence and is all that is used).

- **Theorem 4.1.** If γ ≤ 6^{−4(2M+1)²} then P(|C₀| < ∞) ≤ 55 γ^{1/(2M+1)²} ≤ 1/20 (C₀ = cluster of the origin).

- **Comparison assumptions.** Given: a translation-invariant finite-range process ξ_t on Z^d with finitely many
  states, built from a graphical representation; an integer L; and a set H of configurations *determined by
  the values of ξ on [−L, L]^d*, such that: for every ξ ∈ H there is an event G_ξ, measurable with respect to the
  graphical representation in [−k₀L, k₀L]^d × [0, j₀T], with P(G_ξ) > 1 − γ, on which, if ξ₀ = ξ, then ξ_T lies in
  both translates σ_{2Le₁}H and σ_{−2Le₁}H.
- **Theorem 4.3.** Under the comparison assumptions, with X_n = {m : (m, n) ∈ L, ξ_{nT} ∈ σ_{2mLe₁}H}, one can
  define variables ω(x, n) such that X_n dominates an M-dependent oriented percolation (M = max(j₀, k₀)) with
  initial set X₀ and density ≥ 1 − γ.
- **Theorem 4.2.** If the initial set is Bernoulli with density p > 0 and γ ≤ 6^{−4(2M+1)²}, then
  lim inf P(0 ∈ W_{2n}) ≥ 1 − 55 γ^{1/(2M+1)²} > 19/20.

Nothing in the hypotheses mentions attractiveness. What replaces it is that H depends only on the block, so
G_ξ must do its job **for every configuration outside the block**, and must be measurable in a bounded
space-time box. In the attractive examples (H = "at least K ones in the block") this uniformity is free:
the worst outside is the empty one. For a non-monotone rule it is the whole difficulty.

Remark in §2 [paper]: "A process with increasing birth rates and decreasing death rates is said to be
attractive. … this assumption is not very attractive for biological systems since there the death rate usually
increases due to crowding".

### Does it apply here?

- A dice model (true rule on the face, random layers beneath) is finite-range, finite-state, with a graphical
  representation (the dice). So the theorem is available in form.
- The hypothesis to verify is a set H of block configurations of the face/edge from which, **whatever the rest
  of the face and whatever the dice outside a bounded box**, good configurations appear in the neighbouring
  blocks with probability > 1 − 6^{−4(2M+1)²}. The board's graveyard (6) reports exactly this failing for the 2D
  edge driven by an *unknown* (adversarial) outside. With an outside that is itself dice the adversary is only
  the rest of the same row. Not checked by anyone.
- The comparison is along one direction e₁. It yields survival of a one-dimensional chain of blocks. A lifetime
  for a *finite* chain of m blocks then needs a finite-volume fact about oriented percolation; the one I have
  read is [secondary: Mountford 1993, Fact 2.1, attributed to the contour methods of Durrett 1984]: for
  1-dependent oriented percolation on [1, m] with bond probability > p₀, P(extinct before e^{dm}) < e^{−dm}.
  That is exponential in the *length* of the chain; for a two-dimensional face it would give an exponent
  proportional to a side, not the area.

---

## 2. Bramson and Neuhauser 1994 (the non-monotone cellular automaton with deaths)

M. Bramson and C. Neuhauser, "Survival of one-dimensional cellular automata under random perturbations",
Ann. Probab. 22 (1994), no. 1, 244–263, DOI 10.1214/aop/1176988858. **Not obtained**: the paper is open access
on Project Euclid, but Project Euclid refuses automated clients (a bot wall), and I found no author copy.
Citation data from a search listing of the Project Euclid record.

What I can report is secondary:

- **[secondary: Durrett, Ten lectures, p. 146]** They "studied perturbations of one dimensional cellular
  automata. Their results are exciting because they apply to a number of examples that are not attractive."
  Special case: for the addition-mod-2 automaton η_{n+1}(x) = η_n(x − 1) + η_n(x + 1) (mod 2) with spontaneous
  deaths added at a small rate ε, "there is a stationary distribution close to product measure with density 1/2".
- **[secondary: Marcovici–Sablik–Taati 2019, §5.1]** For the XOR automaton with neighbourhood {−1, 0, 1} and
  zero-range noise 0 → 1 with probability p, 1 → 0 with probability q: in the degenerate case (p or q in {0, 1};
  e.g. p = 0, deaths only, so that all-0 is absorbing) "Bramson and Neuhauser have proved that the system is not
  ergodic, at least in the one-dimensional case".

So, as far as I can verify: an **infinite-volume survival theorem** (a non-trivial stationary law besides the
empty one) for small noise, for a non-monotone, in fact linear, rule. I cannot confirm the exact class of
automata, the form of the perturbation, or whether anything is said about finite systems. *This is the single
most relevant paper I could not open.* A person with a browser can download it from the DOI above.

### Does it apply here?

The theorem is for one-dimensional, nearest-neighbour, mod-2-type rules under small noise. Gump's face and
the 2D rule's edge are not linear and their "noise" (the layers beneath) is not small. What would transfer is
the method, if it is the block construction of §1 (Durrett presents it under that heading; unverified).

---

## 3. Bramson, Ding and Durrett 1991 (annihilating branching process)

M. Bramson, W.-D. Ding and R. Durrett, "Annihilating branching processes", Stochastic Process. Appl. 37 (1991),
1–17. Read: author's reprint, https://sites.math.duke.edu/~rtd/reprints/paper59.pdf (OCR text). Sections 1–2
read; Sections 3–5 (tagged particle, block event, Theorem 1.3) not read.

### The process [paper]

η_t ⊂ Z^d. (i) Particles die at rate δ ≥ 0. (ii) An occupied x gives birth onto each neighbour y at rate 1.
(iii) A birth onto an occupied site annihilates both. With "coalesce" in place of "annihilate" this is the
contact process. It is **not monotone** (adding a particle can remove one) and the empty set is absorbing.

### Theorems [paper]

- **Theorem 1.1.** If δ is small, the process started from one particle survives for ever with positive
  probability.
- **Duality (1.1).** P(|η_t^A ∩ B| is odd) = P(|A ∩ η_t^B| is odd) for finite B (a *cancellative* duality, in
  Griffeath's 1979 sense: count paths in the graphical representation mod 2).
- For δ = 0 the product measure ν_{1/2} with density ½ is stationary (their (1.5)).
- **Theorem 1.2.** For δ > 0 and any translation-invariant initial law giving no mass to ∅, η_t converges weakly
  to η_∞^{1/2}, the limit started from ν_{1/2}. **Theorem 1.3.** For δ = 0, if the initial state is a.s. non-empty,
  η_t ⇒ ν_{1/2}.
- **Lemma 2.3 (parity of independent bits).** If X₁, …, X_n are independent with P(X_i = 1) = θ_i ∈ [β, 1 − β],
  then |P(X₁ + … + X_n is odd) − ½| ≤ ½(1 − 2β)^n.

### Method, and how non-monotonicity is handled [paper, introduction]

Survival: "the ABP dominates oriented percolation with parameter 1 − ε" by the block construction. The
statement proved is their (**): given η_{nT} = A with A ∩ I_m ≠ ∅, there is a good event in the space-time box
with conditional probability ≥ 1 − ε **for all such A**, on which the two neighbouring blocks are non-empty at
time (n + 1)T. The uniformity over A is obtained by following one *tagged particle* (Section 3, not read),
i.e. by an argument that does not care what the other particles do. The hard work is done at δ = 0 and
extended to small δ by continuity ("the proof immediately generalizes to cover perturbation by any mechanism
that is translation invariant and has bounded rates"). Convergence: duality turns the law of η_t into parities
of |η_t ∩ η̃_t| for an independent copy; Lemma 2.3 makes the parity fair once the intersection is large.

### Does it apply here?

- Continuous time, one particle at a time, cancellative duality: none holds for gump. The rule
  "alive iff n + x ≥ 4, n ≤ 5" is not a mod-2 rule.
- The structural lesson that is independent of the model: **a block event that follows one robust local
  object and holds uniformly over the rest of the configuration** is how the comparison assumptions get
  verified without monotonicity. Whether a gump face has such an object is an open question for the solvers.
- For the source line: (1.5) and Lemma 2.3 are exact statements of "a cancellative system manufactures fair
  bits"; the stationary law is exactly product measure when δ = 0.

---

## 4. Threshold contact process on random graphs: these papers are about a monotone process

S. Chatterjee and R. Durrett, "Persistence of activity in threshold contact processes, an 'annealed
approximation' of random Boolean networks", arXiv:0911.5339v1; Random Structures Algorithms 39 (2011), 228–246
(journal data from Durrett's publication list). Read: arXiv PDF, §1 (model, Theorems 1–3).

T. Mountford and D. Valesin, "Supercriticality of annealed approximations of Boolean networks",
arXiv:1007.0862v2 (2012). Read: arXiv PDF, abstract and §1 (Theorem 1.1). Journal reference not verified.

### The model [papers]

Random directed graph G_n on n vertices, each vertex x with r distinct inputs y₁(x), …, y_r(x) chosen uniformly.
Discrete time. Given the state at time t, independently for each x: if at least one input of x is 1, then
x is 1 at time t + 1 with probability q, otherwise 0; if no input is 1, x is 0. All-0 is absorbing.

This rule is **monotone** (more ones now, more ones later, under the natural coupling) and **additive**: both
papers work through its dual, a coalescing branching process (each occupied x, with probability q, occupies all
of y₁(x), …, y_r(x)), with duality {ξ_t^A ∩ B ≠ ∅} = {ξ̂_t^B ∩ A ≠ ∅}. It is "threshold" only in the sense of
threshold one.

### Theorems [papers]

ρ = survival probability of the branching process with r children w.p. q and none w.p. 1 − q.

- **Chatterjee–Durrett, Theorem 1.** If q(r − 1) > 1 and δ > 0, there is C(δ) > 0 with
  inf_{t ≤ exp(C(δ)n)} P(|ξ_t¹|/n ≥ ρ − 2δ) → 1. **Theorem 3.** If only qr > 1: the same up to time
  exp(C(δ) n^{B(δ)}), B(δ) = (1/8 − 2δ) log(qr − δ)/log r. **Theorem 2** is an isoperimetric inequality for the
  graph (small sets U have |U*| ≥ (r − 1 − η)|U|).
- **Mountford–Valesin, Theorem 1.1.** If qr > 1 there is c > 0 such that for every ε > 0 and t_n → ∞, t_n ≤ e^{cn}:
  inf_{t_n ≤ t ≤ e^{cn}} P(ρ − ε < |ξ_t|/n < ρ + ε) → 1.

### Why they are still worth a line here

The papers start from Kauffman's random Boolean network, a **deterministic** automaton on a random graph, and
replace its self-made randomness by fresh dice at every step (Derrida–Pomeau's "annealed approximation";
Chatterjee–Durrett keep the graph fixed and re-draw only the rule tables). All theorems are for the dice
model. Mountford–Valesin [paper, §1]: "This simplification destroys important correlations in the system".
Neither paper proves anything about the deterministic network. This is the same move as the probability line's
"replace the chaos by dice", made in a setting where the dice model happens to be monotone.

---

## Corrections to this repository's citations

- `requests.md` item 2 lists Chatterjee–Durrett and Mountford–Valesin under "non-monotone systems with an
  absorbing state". Their process is monotone and additive (§4). They are exponential-lifetime theorems for a
  monotone dice model of a deterministic network.
- `requests.md` item 2, "Chatterjee–Durrett ('Persistence of activity in threshold contact processes …',
  lifetime exponential in system size on random graphs)": exponential in n only when q(r − 1) > 1; for
  1/r < q ≤ 1/(r − 1) they get exp(c n^{B}) with B < 1/8. The full exponential under qr > 1 is Mountford–Valesin.
- `requests.md` item 2, Bramson–Neuhauser 1994: title and year right (Ann. Probab. 22, 244–263). From the two
  secondary accounts it is a survival theorem on the infinite line, not a finite-size lifetime theorem.
- `critic/board.md`, graveyard 6 ("Block construction … Reported to fail at the first step: the rule is not
  monotone …"). Monotonicity is not a hypothesis of the block construction (§1), and it has been carried out
  for non-monotone systems (§2, §3). What the construction needs is a block event uniform over the outside.
  The graveyard's second reason (an unknown outside contaminates the block) is the real obstruction and is
  exactly the hypothesis of Theorem 4.3 that fails; the first reason, as worded, is not an obstruction.

## Not followed up (leads only; nothing below was opened)

A search listing shows finite-size extinction/metastability results for systems of interacting neurons that
may not be monotone: arXiv:1910.00055 (André, Planche), arXiv:2004.13353 (Löcherbach, Monmarché),
arXiv:1812.09409 (Brochini, Abadi). R. Durrett's book draft "Interacting particle systems: ideas, techniques,
applications" (https://sites.math.duke.edu/~rtd/PASTA/PASTAcon.html, version of 2 Sept 2026) has a final
chapter "Nonlinear contact processes" (Toom, Gray–Griffeath, Bramson–Gray 1991, quadratic contact process);
I searched its text for Bramson–Neuhauser and for finite-volume lifetimes of non-attractive systems and found
neither.
