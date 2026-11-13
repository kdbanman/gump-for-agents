# Algebraic and permutive automata as exact random sources

Request (lead, item 5; source line): the exact statement about time-columns of a bipermutive automaton, its
hypotheses, and what is known in two dimensions. Tags: **[paper]**, **[secondary: X]**, **[mine]** (a remark I
had to add to make a statement precise; flagged so it can be checked).

Notation used by the sources. A one-dimensional cellular automaton on alphabet P (p letters) with neighbourhood
[l, r] (integers l ≤ r) and rule F : P^{r−l+1} → P is the map (Tx)_i = F(x_{i+l}, …, x_{i+r}). F is
**right-permutative** if for every fixed (x_l, …, x_{r−1}) the map x_r ↦ F(…, x_r) is a bijection of P;
**left-permutative** likewise in the first variable; **bipermutative** if both. μ = the uniform Bernoulli
(product) measure on P^Z.

---

## 1. The time-column statement

### 1a. Shereshevsky 1992

M. A. Shereshevsky, "Ergodic properties of certain surjective cellular automata", Monatsh. Math. 114 (1992),
305–316. Read: scan at the Göttingen digitisation centre, linked from EuDML (https://eudml.org/doc/178592;
PDF https://gdz.sub.uni-goettingen.de/download/pdf/PPN362162050_0114/LOG_0027.pdf). Abstract, §1 and §2
(statements) read; proofs not read.

**[paper]**

- Prop. 1.3–1.4 (quoted from Hedlund and Coven–Paul): T is surjective iff it preserves μ; a right- or
  left-permutative rule gives a surjective T.
- **Theorem 2.1 (attributed to Shereshevsky–Afraimovich [SA]).** If l < 0 < r and F is bipermutative, then
  (P^Z, T) is topologically conjugate to the one-sided full shift on p^{|l|+r} symbols.
  Followed by a counterexample: with only one-sided permutativity this fails; for p = 2,
  F(x_{−1}, x_0, x_1) = x_{−1} + x_0x_1 (mod 2) is not expansive, hence not conjugate to a one-sided shift.
- **Theorem 2.2.** If (RP) 0 ≤ l < r and F is right-permutative, or (LP) l < r ≤ 0 and F is left-permutative,
  then the natural extension of (P^Z, μ, T) is a Bernoulli automorphism.
- **Theorem 2.3.** If (RP′) 0 < r and F is right-permutative, or (LP′) l < 0 and F is left-permutative, then
  (P^Z, μ, T) is k-mixing for all k ≥ 1.
- **Theorem 2.4.** If 0 < l ≤ r or l ≤ r < 0 and T is surjective, the natural extension is a K-automorphism.
- **Prop. 2.6.** p = 2, neighbourhood [0, 2], F(x_0, x_1, x_2) = x_0 + x_1(x_2 + 1) (mod 2): surjective
  (left-permutative) and **not ergodic** for μ. Permutativity in the variable at the cell itself does not help.
- **Theorem 2.7.** If F is bipermutative and r > l, the Z²-action of the two shifts on the space-time subshift
  Ω = {ω : ω_{i,j+1} = F(ω_{i+l,j}, …, ω_{i+r,j})} with the measure induced by μ is mixing, and every element
  τ_H^m τ_V^n, (m, n) ≠ (0, 0), is Bernoulli. This generalises Ledrappier's example F(x_0, x_1) = x_0 + x_1.

The reference [SA] as printed: Shereshevsky and Afraimovich, "Bipermutative cellular automata are
topologically conjugate to the one-sided Bernoulli shift", Random and Computational Dynamics 1 (1992), "to
appear". Not obtained.

### 1b. The conjugacy written out

- **[paper: Sablik 2007, §2]** "A bipermutative CA (A^Z, F) of smallest neighborhood U is topologically
  conjugate to ((A^t)^N, σ) where t = max(U ∪ {0}) − min(U ∪ {0}), via the conjugacy
  φ : x ↦ (F^n(x)_{[0,t]})_{n∈N}. So the uniform Bernoulli measure is a maximal entropy measure."
  (M. Sablik, "Measure rigidity for algebraic bipermutative cellular automata", Ergodic Theory Dynam. Systems
  27 (2007); read as the author's copy https://www.math.univ-toulouse.fr/~msablik/article/2007-etds.pdf,
  introduction and §2.) The window is printed [0, t]; for the image to be (A^t)^N it has to be t consecutive
  cells, e.g. [0, t − 1].
- **[paper: Pivato 2003, Lemma 8]** For a right-permutative automaton on the one-sided space A^N with
  neighbourhood {0, 1}, the map Ξ(a) = (a_0, Φ(a)_0, Φ²(a)_0, …) is a topological conjugacy from (A^N, Φ) to
  the shift (A^N, σ). In the conclusion: for a bipermutative Φ with neighbourhood {0, 1}, "the system
  (A^Z, Φ, λ) is measurably isomorphic to the uniform Bernoulli shift (A^N, σ, λ)", citing Shereshevsky 1992.
  (M. Pivato, "Invariant measures for bipermutative cellular automata", arXiv:math/0306211; §1–2 read.)

### 1c. What this says about one cell's states over time

**Statement.** Let T be bipermutative with neighbourhood [l, r], l < 0 < r, and t = r − l. Start from the
uniform product measure μ. Then the sequence of blocks ((T^n x)_0, …, (T^n x)_{t−1}), n = 0, 1, 2, …, is
i.i.d. uniform on P^t. Consequently:

1. the states of **one** cell at times 0, 1, 2, … are i.i.d. uniform on P;
2. the time-columns of any **t adjacent** cells are jointly independent (t = 2 for a radius-one rule);
3. the columns of t + 1 adjacent cells are **not** independent: the t columns determine the whole
   configuration (that is what "conjugacy" means), hence every other column.

Status of each part. That the block columns determine x and are a full shift: [paper], Theorem 2.1/Sablik.
That their law under μ is the uniform product law: [mine], by counting. The first n rows of the t columns
are a function of x on a window of exactly tn cells, and by bipermutativity this function is a bijection
P^{tn} → P^{tn} (each new row reveals r new cells on the right through right-permutativity and |l| on the
left through left-permutativity); a bijection carries the uniform law to the uniform law. Sablik's sentence
"so the uniform Bernoulli measure is a maximal entropy measure" and Pivato's "measurably isomorphic to the
uniform Bernoulli shift" are the same fact in the literature's words. Items 1–3 are then immediate.

**Hypotheses, exactly.** (i) one-dimensional; (ii) bipermutative with l < 0 < r, or one-sided: on P^N,
right-permutative with neighbourhood [0, r], blocks of r cells [Pivato, Lemma 8 for r = 1]; (iii) the
initial law is the **uniform product measure**, exactly. For any other product measure the single-site law
does not even converge: for x_0 + x_1 mod 2 and density p ≠ ½, at times 2^k the cell is x_0 + x_{2^k}
[paper: Ferrari et al., introduction; Lind, Theorem 2(i)]. (iv) It is a statement about the law, not about
one configuration; the deterministic companion is Lind's Theorem 1 below (frequencies along μ-almost every
orbit).

The lead's wording in `PROBLEM.md` ("for a bipermutive one-dimensional automaton started from the uniform
product measure, the states of one cell over time are i.i.d. uniform") is **correct** under (i)–(iii) with
l < 0 < r, and the stronger block statement holds.

---

## 2. Lind 1984 (the mod-2 automaton, by Fourier analysis)

D. A. Lind, "Applications of ergodic theory and sofic systems to cellular automata", Physica D 10 (1984),
36–44. Read: author's copy (scan), https://sites.math.washington.edu/~lind/Papers/ApplicationsToCA.pdf,
§1–4 (pp. 36–40); §5 on (nonlinear) rules and sofic systems not read.

**[paper]** τ is the rule (τx)_i = x_{i−1} + x_{i+1} (mod 2) on X = {0,1}^Z; μ_p = product measure of density
p; μ_H = μ_{1/2} = Haar measure.

- τ is a four-to-one group homomorphism preserving μ_H, ergodic for μ_H; σ and τ generate a jointly ergodic
  action of Z × N.
- **Theorem 1.** For μ_H-almost every x, the frequency of any finite space-time pattern P in the τ-evolution of
  x exists and equals ∫ f_P dμ_H (its probability under Haar). Examples: the block 1 0^k 1 in a row has
  frequency ¼·2^{−k}; triangles of zeros of base k have density (3/16)·2^{−k}.
- **Theorem 2.** (i) If p ≠ ½, τ^n μ_p does not converge. (ii) For 0 < p < 1, (1/N) Σ_{n≤N} τ^n μ_p → μ_H.
  Key formula (4.3): the Fourier coefficient of μ_p at a character supported on r sites is (1 − 2p)^r; for a
  one-site character the support of τ^n g has 2 sites when n is a power of 2, while the set of n for which the
  support has at most M sites has density zero, for every M.
- **Theorem 3.** If dμ = f dμ_H with f continuous, then τ^n μ → μ_H.
- "Extensions to higher dimensions should be clear" (§2; no statement given).

## 3. Ferrari, Maass, Martínez and Ney 2000

P. A. Ferrari, A. Maass, S. Martínez and P. Ney, "Cesàro mean distribution of group automata starting from
measures with summable decay", arXiv:math/9912135; Ergodic Theory Dynam. Systems (2000). Read: arXiv PDF,
abstract, §1 and the start of §2.

**[paper] Theorem 1.3.** G a finite abelian group with |G| = p^r, p prime; φ on G^N given by
(φx)_n = μx_n + νx_{n+1} with integers μ, ν prime to p. Let P be a translation-invariant measure on G^Z with
*complete connections* (P_w{x_0 = g} > 0 for every g and every past w) and *summable decay*
(Σ_m γ_m < ∞, where γ_m bounds |P_w{x_0 = g}/P_v{x_0 = g} − 1| over pasts v, w agreeing on [−m, −1]).
Then for every past w the Cesàro mean of P_w ∘ φ^{−m} exists and equals the uniform product measure.
Method: a regeneration representation of P (i.i.d. uniform symbols at random renewal times) and the
distribution of Pascal's triangle mod p. Note that γ_m is a **ratio** bound.

## 4. Pivato and Yassawi 2002 (any dimension)

M. Pivato and R. Yassawi, "Limit measures for affine cellular automata", Ergodic Theory Dynam. Systems 22
(2002), 1269–1287; arXiv:math/0108082v2. Read: arXiv PDF, §1, the definitions in §3–4, Theorems 12 and 15,
conclusion. (Part II, arXiv:math/0108083, and "Asymptotic randomization of sofic shifts by linear cellular
automata", arXiv:math/0306136, downloaded but not read.)

**[paper]** M a countable monoid (Z^D, N^E, free groups …), A a finite abelian group, F a linear cellular
automaton on A^M (a shift-commuting continuous endomorphism). The *rank* of a character χ is the number of
coordinates it involves. μ is **harmonically mixing** if for every ε there is R with |μ̂(χ)| < ε whenever
rank χ > R (no stationarity required). F is **diffusive** if rank(χ ∘ F^n) → ∞ for every non-trivial χ, and
*diffusive in density* if this holds along a set of n of density 1.

- **Theorem 12.** If μ is harmonically mixing and F is diffusive, F^j μ → Haar weak*; if F is diffusive in
  density, F^j μ → Haar along a set of density 1, hence in Cesàro mean.
- **Theorem 15.** For p prime, A = Z/p and **every D ≥ 1**, every non-trivial linear automaton on A^{Z^D} (one
  whose polynomial has at least two non-zero coefficients) is diffusive in density.
- Non-trivial Bernoulli measures on A^{Z^D} and fully supported N-step Markov measures on A^Z are harmonically
  mixing. Linear automata over Z/p on Z^D are never diffusive outright (F^{p^n} is F rescaled).
- Reports earlier work [secondary]: Lind 1984 as above; Ferrari et al. as above.

## 5. Noise on top of a permutive rule

I. Marcovici, M. Sablik and S. Taati, "Ergodicity of some classes of cellular automata subject to noise",
Electron. J. Probab. 24 (2019), paper 41; arXiv:1712.05500v3. Read: arXiv PDF, §1, summary of results, the
statements of Theorems 3.16 and 5.1 and the first half of the proof of 3.16. See also `pca.md`.

**[paper]**

- **Theorem 3.16.** Every probabilistic automaton obtained by adding positive *permutation noise* (after the
  rule, each symbol is independently replaced by its image under a random permutation; includes additive
  noise) to a one-dimensional permutive automaton is uniformly ergodic, with the uniform Bernoulli measure as
  its unique invariant measure; the law on any finite window converges exponentially fast, uniformly in the
  initial measure. Idea: with the cells to the right of a window frozen to any word, a left-permutive rule
  acts on the window as a bijection, so the window is a finite Markov chain that the noise drives to uniform
  whatever the boundary does. "A special case of a result of Vasilyev". "Analogous results can be obtained in
  higher dimensions", where "the definition of a permutive CA is more cumbersome".
- **Theorem 5.1.** The XOR automaton (sum mod 2 over a neighbourhood in Z^d) with positive zero-range noise
  (0 → 1 w.p. p, 1 → 0 w.p. q, 0 < p, q < 1) is uniformly ergodic and its invariant measure is spatially mixing.
  In the degenerate case (p or q in {0, 1}) the system is not ergodic in one dimension [secondary: they cite
  Bramson–Neuhauser].

## 6. Measure rigidity (why the uniform measure is the only "random" invariant one)

**[secondary: Pivato 2003, Prop. 3; Sablik 2007, Theorem 1.1]** Host, Maass and Martínez (2003): for A = Z/p,
p prime, and Φ(a)_z = c_0 a_z + c_1 a_{z+1} with c_0, c_1 ≠ 0, a measure that is Φ-invariant, σ-ergodic and of
positive entropy for Φ is the uniform Bernoulli measure. Pivato 2003 and Sablik 2007 extend this to larger
classes of bipermutative algebraic automata. The original paper was not read.

---

## What is known in two dimensions (as far as I could read)

- **Asymptotic randomisation holds in every dimension** for linear rules over Z/p: Pivato–Yassawi Theorems 12
  and 15 [paper]. This is convergence in density of the law at a fixed time, not independence over time.
- **Space-time of a one-dimensional rule** is a two-dimensional field: mixing as a Z²-action, each element
  Bernoulli (Shereshevsky, Theorem 2.7) [paper].
- **Exact independence of time-columns for an automaton on Z²:** I found no statement in anything I read.
  Lind says extensions "should be clear"; Marcovici–Sablik–Taati say the higher-dimensional notion of
  permutivity is "cumbersome" and do not state it. The standard reference for which sets of sites carry
  independent coordinates in such algebraic systems is K. Schmidt's *Dynamical systems of algebraic origin*
  (Birkhäuser 1995) and the papers of Kitchens–Schmidt; not obtained (book; not open). This is a gap on the
  shelf, not a known negative.

## Does it apply here?

- Gump and the 2D rule are **not permutive** in any variable: they are counting rules, and changing one
  neighbour changes the output only when the count sits at a threshold. They are not surjective either
  (PROBLEM.md: "far from invertible"), so by Hedlund's criterion (Shereshevsky Prop. 1.3) they do not preserve
  the uniform measure. None of §1–4 applies to gump's own bulk.
- For the source line's aim (a), a deterministic source feeding a gump-like face: §1c supplies exact dice from
  a one-dimensional bipermutative automaton, with the limits (i)–(iv). Two limits bite. First, the layers
  beneath a gump face are two-dimensional, and for a two-dimensional source I can cite only convergence
  results, not exact independence. Second, in one dimension only t = r − l adjacent cells have independent
  columns; t + 1 adjacent columns are functionally dependent. A design that feeds neighbouring face cells from
  neighbouring source cells has to respect that count.
- For aim (b), properties to ask of gump's bulk: the hypotheses under which these theorems transfer
  randomness are of **ratio** or **Fourier-rank** type (summable decay γ_m in §3; harmonic mixing in §4), not
  covariance decay. This agrees with the board's graveyard (3).
- Lemma 2.3 of Bramson–Ding–Durrett (`nonmonotone.md` §3) and Lind's (4.3) are the same computation: an XOR
  of r independent bits of bias (1 − 2p) has bias (1 − 2p)^r.

## Corrections to this repository's citations

- `requests.md` item 5, "bipermutive automata and the independence of a cell's states over time
  (Shereshevsky 1992; Kleveland 1997)": the topological conjugacy with the one-sided full shift is credited by
  Shereshevsky himself to Shereshevsky–Afraimovich (Random Comput. Dynam. 1, 1992). Shereshevsky 1992 proves
  the Bernoulli, K and mixing properties. Kleveland 1997 (Proc. Amer. Math. Soc. 125, "Mixing properties of
  one-dimensional cellular automata") was **not obtained**: ams.org refuses automated clients. I cannot say
  what it adds.
- `requests.md` item 5 "Pivato–Yassawi 2002, 2004": part I is Ergodic Theory Dynam. Systems 22 (2002),
  1269–1287 [paper]; part II's journal data not verified (its arXiv listing says "to appear" there).
- `requests.md` item 5, "Pivato's survey 'Ergodic theory of cellular automata'": it is a chapter of Springer's
  *Encyclopedia of Complexity and Systems Science* (2009), DOI 10.1007/978-0-387-30440-3_178; not on arXiv,
  not open. **Not obtained.** The primary papers above cover the statements wanted.
- `PROBLEM.md`, source line, "the states of one cell over time are i.i.d. uniform": correct; see §1c for the
  hypotheses (l < 0 < r, or the one-sided version) and for how many adjacent cells are jointly independent.
