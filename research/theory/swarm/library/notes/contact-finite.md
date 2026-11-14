# The finite contact process: extinction time exponential in the size

Sources in this file, in the order read. Every statement is tagged **[paper]** (I read it in the paper),
**[secondary: X]** (read in X, which reports it), or **[abstract]**.

Common notation (Durrett's): the *basic contact process* with parameter λ is the continuous-time Markov process
on subsets of a graph in which each occupied site becomes vacant at rate 1 and each vacant site becomes occupied
at rate λ × (number of occupied neighbours). The empty set is absorbing. λ_c is the critical value on the
infinite lattice (infimum of the λ for which the process from one occupied site survives for ever with positive
probability).

---

## 1. Durrett and Liu 1988 (part I)

R. Durrett and X.-F. Liu, "The contact process on a finite set", Ann. Probab. 16 (1988), no. 3, 1158–1173.
Read: author's reprint (scan), https://sites.math.duke.edu/~rtd/reprints/paper39.pdf. Pages 1158–1166 and
1169–1173 read in full; 1167–1168 (biased voter estimates) not read.

### Setting [paper]

ζ_t^N = basic contact process on {1, …, N} (nearest neighbours, **one dimension**), started from all sites
occupied. σ_N = inf{t : ζ_t^N = ∅}. ξ_t^0 = the process on Z from {0}; ξ̂_t^A = the process on the half-line
{1, 2, …} from A, with extinction time τ̂^A; τ^A = extinction time of the process on Z from A.

### Theorems [paper]

- **Theorem 1 (subcritical).** Let λ < λ_c and γ₁(λ) = −lim_{n→∞} (1/n) log P(ξ_n^0 ≠ ∅). Then
  σ_N / log N → 1/γ₁(λ) in probability as N → ∞.
- **Theorem 2 (supercritical).** Let λ > λ_c and let −α₂(λ), −β₂(λ) be the lim sup and lim inf of
  (1/n) log P(τ̂^{{1,…,n}} < ∞). For every ε > 0, as N → ∞,
  P( (log σ_N)/N > β₂(λ) + ε ) → 0 and P( (log σ_N)/N < α₂(λ)/2 − ε ) → 0.
  Section 3 shows 0 < α₂ ≤ β₂ < ∞. So log σ_N is of order N, with constants that may differ by a factor of 2.
- **Theorem 3, 4 (biased voter model** on {1, …, N}: an occupied site is vacated at rate = number of vacant
  neighbours, a vacant one occupied at rate λ × number of occupied neighbours). For λ < 1, σ_N/N converges in
  probability to a constant. For λ > 1, (1/N) log σ_N → log λ in probability. Here the limit exists because the
  process is an interval whose two ends are independent random walks.
- **Epilogue [paper]:** announces that Durrett and Schonmann have shown α₂ = β₂ and removed the factor 2
  (this is part II, below).

### Method, and where each property is used [paper]

*Upper bound on σ_N* (p. 1165). (i) P(nθ ≤ τ̂^{{1,…,n}} < ∞) ≤ C e^{−δnθ} (a supercritical process that dies,
dies quickly; from the contour method of Durrett 1984), so for θ large the event {τ̂^{{1,…,n}} ≤ nθ} already
has probability ≥ exp(−(1+ε)β₂ n). (ii) "Comparing σ_N with a process which is reset to {1, …, N} at times
Nθ, 2Nθ, …" gives P(σ_N > t) ≤ P(τ̂^{{1,…,N}} > Nθ)^{⌊t/Nθ⌋}. Step (ii) is **monotonicity**: adding
particles (the reset) and enlarging the space (half-line instead of interval) can only delay extinction. The
authors say so: "the only property of the contact process used above is that it is a monotone or 'attractive'
process" (p. 1165).

*Lower bound on σ_N* (pp. 1165–1166). Let l̂_t = leftmost particle of the half-line process started full.
(i) **Self-duality**: P(l̂_t > n) = P(τ̂^{{1,…,n}} ≤ t). (ii) The expected time before t that l̂ spends beyond
N/2 is ≤ t·P(τ̂^{{1,…,N/2}} < ∞) ≈ t·e^{−α₂N/2}; so up to time exp((1−2ε)α₂N/2) the left edge of the
half-line process from the left, and by symmetry the right edge of the one from the right, do not reach the
middle. (iii) On that event ζ_t^N = [l_t, r_t] ∩ ξ̂_t (their (4)): the finite system is the half-line system
between its own edges. This is the **nearest-neighbour, one-dimensional path-crossing** identity. The N/2 is
the origin of the factor 2.

*Existence of exponents.* P(τ^{{1,…,m+n}} < ∞) ≥ P(τ^{{1,…,m}} < ∞) P(τ^{{1,…,n}} < ∞) by **Harris'
(FKG) inequality** for decreasing events of the graphical representation, then subadditivity (p. 1164).

*Subcritical case.* The authors remark (p. 1163) that the existence of γ₁ and the bound
P(ξ_t^0 ≠ ∅) ≤ e^{−γ₁t} "follow from monotonicity and the Markov property", and that the rest is valid for any
finite-range interaction.

---

## 2. Durrett and Schonmann 1988 (part II)

R. Durrett and R. H. Schonmann, "The contact process on a finite set. II", Ann. Probab. 16 (1988), no. 4,
1570–1583. Read: author's reprint (scan), https://sites.math.duke.edu/~rtd/reprints/paper42.pdf. Pages
1570–1577 and 1580–1583 read; 1578–1579 (Lemmas 2–4) not read.

### Theorems [paper]

Same setting: {1, …, N}, nearest neighbours, d = 1, started full.

- **Theorem 2.** Let λ > λ_c. There is a constant γ₂(λ) > 0 such that, as N → ∞,
  (a) (1/N) log P(τ^{{1,…,N}} < ∞) → −γ₂(λ) (process on Z);
  (b) (1/N) log P(τ̂^{{1,…,N}} < ∞) → −γ₂(λ) (process on the half-line);
  (c) (1/N) log P(τ^{eq ∩ {1,…,N}} < ∞) → −γ₂(λ) (process on Z started from the upper invariant measure
      restricted to {1, …, N});
  (d) (log σ_N)/N → γ₂(λ) in probability.
- **Theorem 3.** Let β_N = inf{t : P(σ_N > t) ≤ e^{−1}}. As N → ∞, (a) P(σ_N/β_N > x) → e^{−x};
  (b) E σ_N / β_N → 1. The paper proves (a) only. It attributes the result to Cassandro, Galves, Olivieri and
  Vares (1984) "for large λ" and to Schonmann (1985) "for all λ > λ_c", and (b) to Galves and Vares, "given in
  Schonmann (1985)".
- The same proofs give Grimmett's (1981) theorem for sponge crossings in two-dimensional bond percolation:
  the height reached from the bottom of [1, N] × [0, ∞) satisfies (log σ_N)/N → γ(p) for p > 1/2, and the new
  statement that σ_N/Eσ_N is asymptotically exponential.

### Method, and where each property is used [paper]

- **Planar graph duality** (Section 2): in the graphical representation of the nearest-neighbour process on Z,
  either there is an open path across a space-time region or a "dual path" (a contour) cutting it, not both.
  Proposition 3: P(τ^{eq ∩ {1,…,n}} < ∞) = P(there is a dual path from (n + ½, 0) to (½, 0)). Extinction of the
  finite system is thereby a crossing event for dual paths. This needs the space-time picture to be planar:
  **d = 1 and nearest neighbours**.
- Dual-path events are decreasing; **Harris' inequality** gives supermultiplicativity, so the limits exist
  (Lemma 1); an observation of J. and L. Chayes says the rates for paths confined to strips converge to the
  rate in the plane (Lemma 2).
- (d), lower bound on σ_N (Lemma 6): a union bound over where a dual path can cross [½, N + ½] × [0, t];
  the upper bound is quoted from part I (monotonicity).
- Theorem 3(a) (Section 4): shows |P(σ_N > β_N(s+t)) − P(σ_N > β_N s) P(σ_N > β_N t)| → 0. One inequality is the
  Markov property plus monotonicity. The other glues a path that survives to time β_N s to one that starts at
  that time, using crossings of three thin parallelograms (the renormalised construction of Durrett 1984;
  positive edge speed α(λ)) and **Harris' inequality for increasing events**. The only input from Theorem 2
  is β_N/N → ∞.

---

## 3. Mountford 1993 (d dimensions: the exponential limit law)

T. S. Mountford, "A metastable result for the finite multidimensional contact process", Canad. Math. Bull.
36 (1993), no. 2, 216–226. DOI 10.4153/CMB-1993-031-3. Read: publisher's open PDF (Cambridge Core), text layer
is rough OCR; pages 216–223 and 225–226 read, the proof of Lemma 2.2 (pp. 223–225) skimmed.

### Theorem [paper]

Let ζ_t be the d-dimensional nearest-neighbour contact process restricted to the cube [1, n]^d with infection
rate λ > λ_d (the critical value of the unrestricted process on Z^d), started from all sites occupied, and
τ^n the hitting time of the empty configuration. Then τ^n / E[τ^n] converges in distribution to a mean-one
exponential variable as n → ∞. (The proof is written for d = 2; the author states that it extends.)

**What this paper does not contain:** the rate of growth of E[τ^n]. The only lower bound proved is
Proposition 2.1 [paper]: for some d′ > 0 and n large, P(τ^n < e^{d′n}) < e^{−d′n}, i.e. exponential in the
*side* n, which is all the limit law needs. Exponential in the volume n^d is the 1999 paper.

### Method [paper]

- **Lemma 1.1** ("follows simply from attractiveness"): P¹(τ^n > s) P¹(τ^n > t) ≥ P¹(τ^n > s + t), P¹ = started
  full.
- **Proposition 1.2 (a criterion for the exponential law).** Suppose there are a(n), b(n) → ∞ with
  (1) b(n)/a(n) → ∞; (2) uniformly over initial configurations ζ₀, with probability → 1 the process from ζ₀
  either is dead at time a(n) or coincides at time a(n) with the process started full (both built on the same
  Harris system); (3) P¹(τ^n < b(n)) → 0. Then τ^n/E[τ^n] → exponential(1) under P¹.
  In words: if "regeneration" (forgetting the initial state, given survival) takes a time negligible compared
  with the lifetime, the lifetime is asymptotically memoryless. The proof uses Lemma 1.1 (attractiveness) for
  one inequality and the coupling (2) plus independence of disjoint time slabs for the other.
- (3) with b(n) = e^{d′n}: comparison of the process in a slab with supercritical 1-dependent oriented
  percolation (Bezuidenhout–Grimmett 1990 renormalisation), then contour estimates (Durrett 1984).
- (2) with a(n) of order n⁴: **self-duality** turns "ζ_a ≠ ζ¹_a" into "some dual path from (x, a) reaches time 0
  but misses ζ₀"; the process and the dual each become "established" in every slab (again oriented
  percolation), and established forward and dual processes meet.

## 4. Mountford 1999 (d dimensions: exponential in the volume)

T. S. Mountford, "Existence of a constant for finite system extinction", J. Statist. Phys. 96 (1999), no. 5–6,
1331–1341. DOI 10.1023/A:1004652719999. **Abstract only** (publisher's page; the PDF is behind a paywall).

**[abstract]** There is a constant γ ∈ (0, ∞) such that, if τ_n is the extinction time of a supercritical
contact process on [1, n]^d started from full occupancy, then log(E[τ_n]) / n^d → γ as n → ∞.

**[secondary: Mountford–Mourrat–Valesin–Yao 2012, introduction]** summarises the cube case as: for λ > λ_c,
"lim log E[τ]/n^d exists and τ/E[τ] converges in distribution to the unit exponential distribution
[DS88, Mo93, Mo99]". **[secondary: Schapira–Valesin 2015, reference list]** also lists, for boxes of Z^d, Chen,
J. W., "The contact process on a finite system in higher dimensions", Chinese J. Contemp. Math. 15 (1994),
13–20 (not obtained; I do not know what it proves).

I could not read the proof. The best accessible account of *a* proof that the lifetime is exponential in the
number of sites is §5–6 below (general graphs), which does not give the existence of the limit.

## 5. Mountford, Mourrat, Valesin and Yao 2012 (bounded-degree graphs)

T. Mountford, J.-C. Mourrat, D. Valesin and Q. Yao, "Exponential extinction time of the contact process on
finite graphs", arXiv:1203.2972v1 (2012). Read: arXiv PDF, abstract, introduction and theorem statements;
proofs not read. (Journal reference not verified by me.)

### Theorems [paper]

Λ(n, d) = trees with n vertices and degree ≤ d; G(n, d) = graphs with a spanning tree in Λ(n, d); τ_G = extinction
time of the contact process on G started full; λ_c(Z) = critical value on the line.

- **Theorem 1.1.** For d ≥ 2 and λ > λ_c(Z) there is c > 0 with inf_{T ∈ Λ(n,d)} (log E[τ_T])/n ≥ c for n large.
- **Theorem 1.2.** For G_n ∈ G(n, d), τ_{G_n}/E[τ_{G_n}] converges in distribution to the unit exponential.
- **Theorem 1.3.** inf_{T ∈ Λ(n,d)} P(τ_T ≥ e^{cn}) → 1.
- "By attractiveness" Λ(n, d) can be replaced by all graphs having a subgraph in Λ(n, d); "for instance … any
  sequence of increasingly large connected subsets of Z^d". So for every connected region of Z^d with n sites
  and λ > λ_c(Z) (not λ_c(Z^d)) the lifetime is at least e^{cn}: exponential in the **number of sites**,
  whatever the shape.
- Theorem 1.4: the same on power-law random graphs for every λ > 0 (improves Chatterjee–Durrett 2009).

### Method [paper, introduction only]

Split the tree into two subtrees each with a fixed fraction of the vertices; bound the process below by
independent processes on the two pieces which, once extinct, are re-ignited after a delay (the other piece
re-infects it); conclude E[τ_T] ≥ (polynomial factor)^{-1} × E[τ_{T₁}] E[τ_{T₂}]; induct. The exponential law is
obtained "using a general metastability argument from [Mo93]". Attractiveness is invoked at each comparison.

## 6. Schapira and Valesin 2015 (general graphs; a short proof)

B. Schapira and D. Valesin, "Extinction time for the contact process on general graphs", arXiv:1509.04133v1
(2015). Read: arXiv PDF, introduction, §2.1–2.3 statements, §3.2. (Journal reference not verified by me.)

### Theorems [paper]

- **Theorem 1.1** (quoted from earlier work): (ii) for d ∈ N and λ > λ_c(Z) there is c > 0 such that
  E[τ_G] ≥ exp(c|G|) for every connected graph G of degree ≤ d with at least two vertices.
- **Theorem 1.2.** For λ > λ_c(Z) and ε > 0 there is c_ε > 0 such that for every connected graph G with at least
  two vertices, E[τ_G] ≥ exp(c_ε |G| / (log |G|)^{1+ε}), and for every non-empty A the process from A is alive
  at time exp(c_ε|G|/(log|G|)^{1+ε}) with probability > c_ε.
- **Theorem 1.3.** For λ > λ_c(Z) and any graphs G_n with |G_n| → ∞, τ_{G_n}/E[τ_{G_n}] → Exp(1) in distribution.

### The tools, which are the reusable part [paper]

- **Lemma 2.3(i):** P(τ_G ≤ t) ≤ t / E[τ_G]. Proof: "by attractiveness", τ_G is stochastically dominated by
  t × a geometric variable with parameter P(τ_G ≤ t).
- **Lemma 2.3(ii):** E[τ_G] ≤ e^{n + 2λm} (n vertices, m edges): in each unit of time, with probability
  e^{−n−2λm} every vertex recovers and nothing is transmitted. (The trivial upper bound; no monotonicity beyond
  the restart.)
- **Proposition 2.7 (coupling).** For every tree G with n ≥ 2 vertices, every t ≥ 0 and non-empty A,
  P(ξ_t^A ≠ ∅, ξ_t^A ≠ ξ_t^1) ≤ exp(−c t / (n (log n)³)). A process that is still alive after time ≫ n(log n)³
  equals the process started full.
- **Proposition 2.9 (supermultiplicativity).** For a tree G containing N disjoint connected subtrees G₁…G_N,
  E[τ_G] ≥ c (2|G|³)^{−(N+1)} ∏ E[τ_{G_i}]. With boundedly many pieces this gives e^{c|G|} by induction.
- §3.2: the exponential law follows from Proposition 2.7, a polynomial lower bound on E[τ] and Lemma 2.3, via
  Lemma A.1 of Mountford et al. (the criterion of Mountford 1993, Proposition 1.2 above).

Where monotonicity enters: Lemma 2.3(i); the reduction to spanning trees (Remark 2.1: the process on a
subgraph is dominated by the process on the graph); the coupling 2.7 (the process from A lies inside the
process from full, and infection paths are concatenated).

---

## Does it apply here? (parts I and II)

| hypothesis | gump face / 2D edge |
|---|---|
| absorbing empty state | holds (T2 and its 2D analogue: an empty face or edge stays empty) |
| randomness: a Markov process driven by independent Poisson clocks | fails: the rule is deterministic; holds only for a dice model |
| monotone ("attractive") | fails: a cell with n ≥ 6 (gump) or n ≥ 5 (2D) dies |
| self-duality / additivity (the state is a union of the offspring of single particles) | fails; additivity implies monotonicity |
| Harris–FKG inequality for the graphical representation | available only for monotone events of independent variables; the events "survives" are not monotone in the dice of a non-monotone rule |
| d = 1, nearest neighbours (planar space-time, edges l_t, r_t) | fails: the gump face is two-dimensional; the 2D rule's edge is one-dimensional but has range 2 and is fed from the rows beneath |

What transfers. The *upper* bound on the lifetime (restart argument) needs only: from every state, probability
≥ p of extinction within time s; without monotonicity the "worst state" is no longer the full one, so p must be
bounded over all states (this is what the trivial bounds B′, C in `research/theory/exponent/theorems.md` do).
The *lower* bound e^{cN}, which is the missing half in this repository, rests in both papers on duality and
planar contours; nothing in the argument survives the loss of monotonicity. The memoryless law (Theorem 3(a))
uses a positive-speed "regeneration from any surviving state" step (gluing of paths), again through
monotone paths.

Note on "area versus perimeter": in parts I and II the system is one-dimensional, so the exponent N is the
length. In d dimensions the exponent is the volume n^d (Mountford 1999, abstract), and for any connected set of
n sites it is at least cn when λ > λ_c(Z) (§5, §6).

### The d-dimensional and general-graph results (§3–6)

Same table: every proof read here uses the Harris graphical construction and attractiveness, and §3 uses
self-duality. Three statements are worth separating, because they are *conditional* and their hypotheses can
be asked of any system with an absorbing state:

1. **Memorylessness from fast regeneration** (Mountford 1993, Prop. 1.2). Hypotheses: submultiplicativity of
   the survival function from the reference initial law; a time a(n) ≪ lifetime after which, from *any* initial
   state, the system is dead or indistinguishable from one started in the reference state. For the contact
   process "indistinguishable" is exact equality under the monotone coupling. For a deterministic rule there is
   no coupling; the analogue would have to be a statement about laws (conditioned on survival, the law at time
   a(n) is close to one fixed law, uniformly in the start), which is a quasi-stationary-mixing statement and is
   the board's "ratio-type" requirement in another form. Not known to hold here.
2. **Exponential lower bound from supermultiplicativity** (Schapira–Valesin Prop. 2.9): if a system splits into
   two halves each of which, while alive, re-ignites the other faster than the other's lifetime, then
   E τ(whole) ≥ poly^{-1} · E τ(half)². Hypothesis that fails here: "alive" is not enough; the contact process
   re-ignites from a single particle with probability bounded below, by monotonicity. A gump face with a few
   live cells is not known to recover with probability bounded below.
3. **P(τ ≤ t) ≤ t/Eτ** (Lemma 2.3(i)): needs the reference state to be the worst case for extinction
   (monotonicity). For a quasi-stationary start the corresponding statement is an identity (exact geometric
   law; see the QSD notes), with no monotonicity needed.

## Corrections to this repository's citations

- `requests.md` item 1: "Durrett–Liu 1988; Durrett–Schonmann 1988 ('The contact process on a finite set' I, II)"
  is right (both Ann. Probab. 16, 1988). There is also a part III: Durrett, Schonmann and Tanaka, "The contact
  process on a finite set. III: the critical case", Ann. Probab. 17 (1989), 1303–1321 (citation from Durrett's
  own publication list; paper not read).
- `PROBLEM.md` ("extinction time exponential in volume; Durrett–Liu, Durrett–Schonmann, Mountford") and
  `PRIOR-ART.md` §3: Durrett–Liu and Durrett–Schonmann treat only the one-dimensional nearest-neighbour
  process on {1, …, N}. Durrett–Liu alone do not get the exponent (bounds within a factor 2); the limit
  (log σ_N)/N → γ₂ is Durrett–Schonmann. The exponential limit law is Cassandro–Galves–Olivieri–Vares (large λ)
  and Schonmann (all λ > λ_c), reproved in part II. "Exponential in volume" in d ≥ 2 is Mountford **1999**
  (log E τ_n / n^d → γ), not Mountford 1993, which proves the exponential *limit law* and only a lower bound
  exponential in the side length.
- `requests.md` item 1 has both Mountford titles and years right. The 1999 title in full: "Existence of a
  constant for finite system extinction".
- `PRIOR-ART.md` §3 cites "Mountford–Mourrat–Valesin–Yao on trees". The paper is about finite graphs with a
  bounded-degree spanning tree, which includes every connected finite subset of Z^d; it is not only about
  trees. The sentence quoted there from the abstract is accurate.
- `PRIOR-ART.md` §3: "Lifetime ~ exp(c·volume) … is the same form as our exp(0.209·A), where A is a face area
  rather than a volume." For the contact process the exponent is the number of sites *of the whole system*;
  nothing read here gives an exponent proportional to the size of a boundary layer of a larger system.
- Cassandro–Galves–Olivieri–Vares 1984 and Schonmann 1985: **abstract only** (Springer pages; paywalled).
  CGOV [abstract]: "a new approach to metastability for stochastic dynamics … study the statistics of each
  path, performing time averages along the evolution"; convergence of the rescaled process of time averages to
  a measure-valued Markov jump process is shown for the Curie–Weiss dynamics and for the Harris contact process.
  Schonmann [abstract]: "the Harris contact process shows metastable behavior for any supercritical value of
  the parameter". What they prove for σ_N is as reported by Durrett–Schonmann (§2) and Mountford (§3):
  [secondary] one dimension only; CGOV for λ large, Schonmann for all λ > λ_c; Schonmann also shows that no
  such result holds in the subcritical case (Mountford 1993, p. 216).
- The title of Cassandro–Galves–Olivieri–Vares, as given in both reference lists: "Metastable behavior of
  stochastic dynamics: a pathwise approach", J. Statist. Phys. 35 (1984), 603–634 (part II's list prints
  603–628). `requests.md` gives only a description, which matches.

---

## 7. The Williams–Bjerknes (biased voter) model: the count of occupied sites is a biased walk (request: path, 1)

Source read: O. Louidor, R. J. Tessler, A. Vandenberg-Rodes, "The Williams Bjerknes model on regular trees",
arXiv:1211.5694v2, pp. 1–2 (introduction). Bramson–Griffeath, "On the Williams–Bjerknes tumour growth model"
I (Ann. Probab. 9 (1981) 173–185) and II (Math. Proc. Cambridge Philos. Soc. 88 (1980) 339–357): **not
obtained** (Project Euclid; Cambridge).

- **Model [secondary: Louidor–Tessler–Vandenberg-Rodes, eq. (1)]**: on a graph, an infected vertex becomes healthy
  at rate equal to its number of healthy neighbours; a healthy vertex becomes infected at rate λ times its
  number of infected neighbours.
- **Statement [secondary: same, eqs. (2)–(4)]**: "As was noticed by Williams and Bjerknes, observed at the times
  of transition … the process (|ξ_{τ_k}|) is just a nearest-neighbor random walk on Z₊ with an absorbing state at
  0 and drift (λ − 1)/(λ + 1). Therefore global survival … has probability P = 1 − λ^{−|ξ₀|}", "regardless of the
  underlying graph, as long as it is infinite, connected and has a bounded degree". So the attribution is to
  Williams and Bjerknes (1972) themselves; it holds in every dimension and on every bounded-degree graph,
  because each disagreeing edge contributes rate 1 down and rate λ up.
- Bramson and Griffeath's contribution, per the same source: a shape theorem with linear growth on Z^d, all d,
  all λ > 1.
- **Finite volume with vacant boundary in d ≥ 2: not found.** Durrett–Liu Theorems 3–4 (§1 above) are d = 1.
  On a finite graph the same walk argument gives P(fixation) = (1 − λ^{−1})/(1 − λ^{−N}) for one initial cell
  ([secondary: search-engine summary of a Moran-process source; not opened]); a *vacant* (permanently healthy)
  boundary breaks the walk property, since boundary edges add rate down only.
