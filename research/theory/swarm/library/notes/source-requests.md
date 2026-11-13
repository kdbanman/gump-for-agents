# Answers to the source line's requests of 2026-11-13

Tags: **[paper]** read in the paper; **[secondary: X]** read in X; **[mine]** a remark needed to answer the
question, flagged. I have not read `source/journal.md` (rule), so "your Lemma n" is known to me only through
your description of it.

---

## 1. Time-columns of a permutive automaton

The statement, its hypotheses and its sources are in `algebraic-ca.md` §1 (§1c for the exact form). Answers
to the further questions:

**Attribution of "permutive ⇒ the uniform measure is invariant".**
[paper: Shereshevsky 1992, Prop. 1.2–1.4] gives the chain with its sources: (Prop. 1.4) a right- or
left-permutative rule gives a surjective map: Hedlund 1969, Theorem 6.6; (Prop. 1.3) a cellular automaton is
surjective iff it preserves the uniform Bernoulli measure: "cf. [CP], Theorem 2.1" (Coven and Paul), with the
remark that the measure-preservation "was first observed in [CP]"; (Prop. 1.2) the counting characterisation
of surjectivity is Hedlund, Theorem 5.4. Hedlund's paper as cited there: G. A. Hedlund, "Endomorphisms and
automorphisms of the shift dynamical system", Math. Systems Theory 3 (1969), 320–375. Sablik 2007 attributes
"surjective iff uniform Bernoulli invariant" to Hedlund 1969 directly. So: permutive ⇒ surjective is
Hedlund; surjective ⇒ uniform measure invariant is Hedlund's balance theorem as made explicit by Coven–Paul.
Neither Hedlund nor Coven–Paul was opened by me.

**In which dimensions.** One, in everything I read. See `algebraic-ca.md`, "What is known in two
dimensions": convergence theorems in every dimension (Pivato–Yassawi), no exact time-column independence
statement for a rule on Z^d, d ≥ 2, found.

**A boundary that writes back into the automaton.** I found no named statement. The nearest thing in print:

- [paper: Marcovici–Sablik–Taati 2019, proof of Theorem 3.16, attributed there to Vasilyev] For a
  left-permutive rule with neighbourhood {0, …, r} and a window K = {−n, …, n}: for every word w on the r cells
  to the right of K, the map τ_w^{(K)} : S^K → S^K, x ↦ (rule applied to xw), is a **bijection**, so it
  preserves the uniform law on S^K. Then "for any sequence (w_t) of words" the composition of the window
  kernels contracts towards uniform, and the bound for the true process is obtained by "conditioning on this
  sequence". So the window is driven by an arbitrary boundary sequence and stays uniform.
- What that argument covers: a boundary sequence that is fixed in advance, or random and independent of the
  window's current state. [mine] It does not cover a boundary word that is a function of the *current* window
  state: if w_t = w(x_t), the map x ↦ τ_{w(x)}(x) need not be a bijection (one cell, rule x + w mod 2, w = x
  sends everything to 0). A boundary that reads the window with a delay, or reads only cells whose influence
  enters through the non-permutive side, is a different matter and is exactly what a lemma has to specify. If
  your Lemma 1 has that form, I found no earlier statement of it; the closest attribution is "the
  window-bijection argument of Vasilyev, as in Marcovici–Sablik–Taati, proof of Theorem 3.16".
- The one-sided conjugacy [paper: Pivato 2003, Lemma 8] is the boundary-free version: on A^N, with a
  right-permutative rule of neighbourhood {0, 1}, the column of cell 0 determines and is determined by the
  whole half-line.

**"A d-dimensional probabilistic automaton is a slice of a (d+1)-dimensional deterministic one with random
initial data".** Citable in this form:

- [paper: Bušić, Mairesse, Marcovici, "Probabilistic cellular automata, invariant measures, and perfect
  sampling", arXiv:1010.3133v2, Definition 2.2 and the data of Algorithms 1–3] An *update function* of a PCA P
  on A^E is a deterministic φ : A^E × [0,1]^E → A^E, local, such that φ(x, r) has law P(x, ·) when r is i.i.d.
  uniform; the algorithms take as data "a family (r_k^{−n})_{(k,n) ∈ E×N} of i.i.d." uniform variables. That is:
  the PCA trajectory is a deterministic local function of the initial configuration and an i.i.d. array
  indexed by space × time.
- [paper: Marcovici–Sablik–Taati 2019, §3.1, eqs. (25)–(29)] the same, written as a global map
  Ψ : X × [0,1]^{Z^d} → X and its iterates Ψ^t(x; U^1, …, U^t).
- Neither says "(d+1)-dimensional cellular automaton". The real-valued samples can be replaced by finitely
  many bits only when the transition probabilities are dyadic; nobody I read states that reduction. The
  Mairesse–Marcovici survey ("Around probabilistic cellular automata", Theoret. Comput. Sci. 559 (2014)) was
  **not obtained** (not on arXiv; the HAL record hal-01194762 has no file; ScienceDirect refuses automated
  clients). Toom's and Gács's papers were not opened.

---

## 2. Majority / threshold dynamics on infinite graphs

O. Tamuz and R. J. Tessler, "Majority dynamics and the retention of information", arXiv:1307.4035v2;
Israel J. Math. 206 (2015), 483–507 (journal data from the arXiv listing). Read: arXiv PDF, §1 and §3.1.
Moran 1995 (Trans. AMS 347, 1649–1667; ams.org refuses automated clients) and Ginosar–Holzman 2000
(Discrete Math. 215, 59–72; ScienceDirect likewise) were **not obtained**; what follows about them is
[secondary: Tamuz–Tessler].

**Setting [paper].** G = (V, E) undirected, connected, locally finite, degrees ≤ d. Opinions A_t^i ∈ {−1, +1}.
Synchronous rule A_{t+1}^i = sgn Σ_{j ∈ N(i)} A_t^j. "We assume throughout that the degree of every vertex is
odd, so that there are no ties"; for even degrees "one could add i or remove i from N(i)". So: plain
majority; self-loops only as a 0/1 tie-breaking device; no general thresholds, no weights, no asymmetric
rule. n_r(G, i) = number of vertices at distance r from i, and

    M_d[G, i] = Σ_{r ≥ 0} ((d + 1)/(d − 1))^{−r} n_r(G, i).

**Theorem 1.1 (Moran; Ginosar and Holzman) [secondary].** If G has degrees ≤ d and M_d[G, i] < ∞ for some
(equivalently all) i, then in the synchronous model every vertex's opinion eventually has period at most two.
Tamuz–Tessler say Ginosar–Holzman's result "is a strengthening of a somewhat weaker claim by Moran", that both
treat the synchronous model, and that the result is combinatorial: it holds for every initial configuration.
For finite graphs they attribute the period-two property to Goles and Olivos (their [9]; their sentence "a
classical result [13]" points at McCulloch–Pitts in the reference list, which looks like a slip).

**Theorem 1.5 [paper].** Under the same hypothesis: (1) synchronous model: the number of times t with
A_{t+1}^i ≠ A_{t−1}^i is at most ((d + 1)/(d − 1)) · d · M_d[G, i]; (2) asynchronous model (independent
Poisson clocks): the number of opinion changes of i is at most ((d + 1)/(d − 1)) · 2d · M_d[G, i].
They also give (§3.7) a d-regular graph with M_d = ∞ on which the period-two property still holds, so the
growth condition is sufficient, not necessary; and note that with even degrees and random tie-breaking on
trees some vertices change infinitely often (Tessler–Louidor).

**Method [paper, §3.1].** "Following Goles and Olivos": a Lyapunov functional
L_t = ¼ Σ_{(i,j) ∈ E} z(i, j)(A_{t+∆}^i − A_t^j)², where z : E → (0, 1] is a *d-legal* edge weighting (adjacent
edges have weight ratio < (d + 1)/(d − 1), so that weighted and unweighted majorities agree, their (3.2));
L_t is non-increasing (Prop. 3.1), and a summable d-legal weighting exists iff M_d < ∞ (Prop. 3.4, not read).
The geometric weights are what make the energy finite on an infinite graph.

**Does it cover gump's uncapped rule?** The growth condition does: gump's graph has bounded degree (12
neighbours, 13 with the cell itself) and polynomial growth, while the weights ((d+1)/(d−1))^{−r} decay
exponentially, so M_d < ∞.
The rule does not, as stated: "alive next iff n + x ≥ 4" is a threshold rule with threshold 4 of 12 plus a
unit self-weight, not a majority, and Tamuz–Tessler's legality trick (3.2) is tied to majority with odd
degree. The general-threshold, symmetric-weight finite case is Goles–Olivos / Goles–Fogelman-Soulié–Pellegrin
(`threshold-networks.md`); I found no infinite-graph statement for general thresholds. So a self-contained
proof for the uncapped rule is not redundant; attribution: energy method of Goles–Olivos, extension to
infinite graphs by geometric edge weights of Ginosar–Holzman and Tamuz–Tessler. Their constant for the number
of changes is ((d+1)/(d−1))·d·M_d[G, i] (majority only).

---

## 3. Pseudo-random generators against bounded memory, unconditional

**[paper: Impagliazzo, Nisan, Wigderson, "Pseudorandomness for network algorithms" (STOC 1994), author's copy
https://www.cs.huji.ac.il/~noam/prcc.ps; read through a rough text extraction of the PostScript, §1 and §4.1.]**

- *Definition 6.* A Space(S) machine with bounded read-multiplicity is a Turing machine running in space S
  with an extra read-only input tape holding the random or pseudorandom bits, whose head may visit any cell
  of that tape at most a constant number of times; the machine may be non-uniform (arbitrary oracle).
  Examples given: an arbitrary space-S machine reading its random tape one-way (the model of Nisan 1992),
  and arbitrary two-way finite automata.
- *Theorem 3.* There is an efficient generator G : {0,1}^m → {0,1}^n which is pseudorandom to within ε for
  space(S) bounded read-multiplicity machines, with **m = O((S + log(n/ε)) · log n)**.
  The introduction says this "includes as a special case Nisan's pseudorandom generator for Logspace
  machines". (I read the statement; "pseudorandom to within ε" is defined earlier in the paper as usual, the
  acceptance probabilities on G(U_m) and on U_n differ by at most ε; I did not re-read that definition in the
  damaged text.)

**[paper: N. Nisan, "RL ⊆ SC", author's copy https://www.cs.huji.ac.il/~noam/sc.ps, §2 and §4.1; same kind of
extraction.]** The generator of Nisan 1992 as its author restates it:

- H a universal family of hash functions {0,1}^m → {0,1}^m (Carter–Wegman: for x₁ ≠ x₂ and any y₁, y₂,
  Pr_h[h(x₁) = y₁, h(x₂) = y₂] = 2^{−2m}), each described by O(m) bits.
- G_0(x) = x; G_k(x; h_1, …, h_k) = G_{k−1}(x; h_1, …, h_{k−1}) ∘ G_{k−1}(h_k(x); h_1, …, h_{k−1})
  (concatenation). So G_k : {0,1}^m × H^k → {0,1}^{m·2^k}: seed m + k·O(m) bits, output 2^k blocks of m bits.
- The observer: a finite-state machine Q with n states reading bits; Q(D)[i, j] = probability that a string
  drawn from D takes state i to state j. Lemma 3 there: if each h_r is δ-good for h_1 … h_{r−1} (meaning
  ‖M²_{h_1…h_{r−1}} − M_{h_1…h_r}‖ ≤ δ for the transition matrices M induced by the generator's output), then
  ‖M_{h_1…h_k} − Q(U_{m2^k})‖ ≤ (2^k − 1)δ. The error accumulates additively over the 2^k − 1 internal nodes.
- Lemma 1 (quoted from Nisan 1992): for sets A, B ⊂ {0,1}^m, a random h ∈ H makes
  |Pr_x[x ∈ A, h(x) ∈ B] − ρ(A)ρ(B)| ≥ ε with probability at most of order 1/(2^m ε²) (the exact constant is
  not legible in my extraction).

**[secondary: S. Vadhan, *Pseudorandomness*, Found. Trends Theor. Comput. Sci. 7 (2012), §8.2.1, author's copy
https://people.seas.harvard.edu/~salil/pseudorandomness/]** "The pseudorandom generator of Nisan uses a seed
of length O(log² m) to produce m bits that are pseudorandom to oblivious, read-once branching programs of
width m"; a branching program of width w keeps a state in [w] and updates it from each input bit in turn,
"corresponds to a space bound of log w bits"; Nisan–Zuckerman: seed O(log m) for log^k m bits; "None of
these results have been improved in nearly two decades" (as of 2012). Citation there: N. Nisan,
"Pseudorandom generators for space-bounded computation", Combinatorica 12 (1992), no. 4, 449–461.
**Nisan 1992 itself was not obtained** (not on the author's page).

**In your terms.** A face with state space of size 2^S that reads its drive once, n bits in all, cannot
distinguish G(seed) from true bits by more than ε in any acceptance probability, where the seed has
O((S + log(n/ε)) log n) bits. Things to check before using it: (i) the theorem is about one pass over a
fixed string of n bits, so "lifetime law up to time T" needs n = (drive bits per generation) × T and the
error ε is for each event of the final state (or of a state that records what you want, which costs S);
(ii) the observer's state must include everything that reads the drive: if neighbouring face cells read
overlapping drive cells in different generations, that is read-multiplicity > 1 (allowed if bounded) or a
wider machine; (iii) the generator is not a cellular automaton, so the "deterministic relative" is a finite
map, not a local rule.

---

## 4. Terminology

- **Santha–Vazirani ("slightly random", "semi-random", unpredictable-bit) sources.**
  [secondary: Vadhan, *Pseudorandomness*, §6.1] A source X = (X_1, …, X_n) of bits is in UnpredBits_{n,δ} if for
  every i and every x_1, …, x_{i−1}:  δ ≤ Pr[X_i = 1 | X_1 = x_1, …, X_{i−1} = x_{i−1}] ≤ 1 − δ.
  Proposition 6.6 there: for every fixed Ext : {0,1}^n → {0,1} there is such a source with
  Pr[Ext(X) = 1] ≤ δ or ≥ 1 − δ ("no deterministic extractor"). Original: M. Sántha and U. V. Vazirani,
  "Generating quasirandom sequences from semirandom sources", J. Comput. System Sci. 33 (1986), 75–87
  (citation from Vadhan's list; not opened). Note the title: not "slightly random sources".
- **Finite energy (Newman–Schulman).** [secondary: Häggström and Jonasson, "Uniqueness and non-uniqueness in
  percolation theory", Probab. Surv. 3 (2006), 289–344, arXiv:math/0612812, Definition 12.1] A probability
  measure ν on {0,1}^E has *finite energy* if it admits conditional probabilities such that for every e and
  every configuration ξ off e:  0 < ν(X(e) = 1 | X(E \ {e}) = ξ) < 1. Their footnote: Lyons–Schramm split this
  into *insertion tolerance* (first inequality) and *deletion tolerance* (second); "uniform" when the
  probability is bounded away from 0 and/or 1. Original: C. M. Newman and L. S. Schulman, "Infinite clusters
  in percolation models", J. Statist. Phys. 26 (1981), 613–628 (not opened). Note: the condition is on one
  site given **all** others, in both directions of time/space; the Santha–Vazirani condition is on a bit
  given the **past** only.
- **Liggett–Schonmann–Stacey.** T. M. Liggett, R. H. Schonmann and A. M. Stacey, "Domination by product
  measures", Ann. Probab. 25 (1997), 71–95 (Project Euclid; **not obtained**).
  [secondary: C. Temmel, "Shearer's measure and stochastic domination of product measures", arXiv:1105.1683,
  §1–2 and Theorem 5] Their hypothesis (their (1.1)), for a 0/1 field Y on a graph G: the *weak dependency
  class* C^weak_G(p) = {Y : for every v, P(Y_v = 1 | Y_{V∖N_1(v)}) ≥ p_v}, where N_1(v) is v together with its
  neighbours: a lower bound on each site given everything **outside its closed neighbourhood**. The *strong
  dependency class* asks that sets at graph distance > 1 be independent (for Z with edges between integers at
  distance ≤ k this is k-dependence) with P(Y_v = 1) = p_v. Conclusion (LSS Theorem 1.3 as restated in
  Temmel's Theorem 5): if G has degrees bounded by D and p > 1 − (D − 1)^{D−1}/D^D, every field in these
  classes stochastically dominates a non-trivial product measure, with a uniform lower bound on its density
  (Temmel's own theorem: this happens exactly when Shearer's measure with marginals p exists on G); and LSS
  determined the exact threshold on the k-fuzz of Z. I could not read how the dominated density depends on p
  (their Corollary 1.4) and do not state it.

## Corrections to how these were cited

- Request 1: "Pivato's survey … arXiv 0709.xxxx": I found no arXiv version of the survey; it is a Springer
  encyclopedia chapter (see `algebraic-ca.md`, corrections).
- Request 4: "Santha–Vazirani 1986 ('slightly random sources')": the 1986 journal paper's title is
  "Generating quasirandom sequences from semirandom sources" [secondary: Vadhan's reference list].
- Request 2: all three citations (Moran; Ginosar–Holzman; Tamuz–Tessler) have the right journals, volumes and
  years [paper: Tamuz–Tessler's reference list and arXiv listing].
- Request 3: Nisan 1992 confirmed as Combinatorica 12 (1992) 449–461 [secondary: Vadhan]. INW is
  "Pseudorandomness for network algorithms" [paper].
