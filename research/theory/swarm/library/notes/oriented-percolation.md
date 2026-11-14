# Oriented percolation in 1+1 dimensions: critical values, Liggett's survival theorem, finite volume

Written for the probability line's Theorem A and the source line's Theorem A (requests of 2026-11-13 from the
critic and from probability). Every statement is tagged **[paper]** (read in the paper), **[secondary: X]**
(read in X, which quotes or reports it), **[abstract]**, or **[not found]**. Remarks of mine are marked
*librarian*; they are arithmetic or one-line consequences, not sources.

Models. *Two-parent oriented site percolation* (2dOP below): sites of Z × Z₊ open independently with
probability p; (y, n+1) is reached iff it is open and one of its two parents (y, n), (y+1, n) is reached
(equivalently parents y−1, y+1 on the even sublattice; equivalently arrows ↑ and → on Z²). Conditional
independence of the sites of level n+1 given level n is automatic: they are functions of disjoint i.i.d.
variables. *Bond* percolation: the arcs are open instead. The two are different models with different
critical values (numerically ≈ 0.7055 site, ≈ 0.6447 bond).

---

## 1. Upper bounds below 3/4 for the site critical value (request: critic (a))

### Balister, Bollobás, Stacey 1993 and 1994

P. Balister, B. Bollobás, A. Stacey, "Upper bounds for the critical probability of oriented percolation in two
dimensions", Proc. Roy. Soc. London Ser. A 440 (1993), no. 1908, 201–220; and "Improved upper bounds for the
critical probability of oriented percolation in two dimensions", Random Structures Algorithms 5 (1994), no. 4,
573–589. **Neither opened** (Royal Society: Cloudflare wall; Wiley: not open). Abstracts read through the
Crossref metadata record.

- **[abstract, 1993]** "We give a method for obtaining upper bounds on the critical probability in oriented bond
  percolation in two dimensions. This method enables us to prove that the critical probability is at most
  0.6863 … We also prove that our method can be used to give arbitrarily good upper bounds. We also use a slight
  variant of our method to obtain an upper bound of 0.72599 for the critical probability in oriented site
  percolation."
- **[abstract, 1994]** "We refine the method of our previous paper [2] which gave upper bounds for the critical
  probability in two-dimensional oriented percolation. We use our refinement to show that [formula]" — the
  displayed formula is missing from every copy of the abstract I could reach.
- **[secondary: Hartarsky–Szabó, arXiv:2103.15621v1, §5.7.2, pp. 28–29]** "In [1993] and the later refinement,
  [1994], a two-dimensional renormalisation argument was used together with extensive computer calculations to
  conclude that p_c^OP ⩽ 0.7491 (there is a misprint in [1993] as explained in [1994]). Subsequently Liggett
  [1995] proved p_c^OP ⩽ 3/4 without resorting to a computer." Their OP is **site** percolation with neighbourhood
  {(0,1),(1,1)} (GOSP is a site model; §1.1–1.2), i.e. 2dOP above. So the 0.72599 of the 1993 abstract is the
  misprint, and the site bound actually established is 0.7491. The renormalisation criterion is restated in
  general form as their Theorem 24 [paper]: if for some block parameters and some up-set A ∌ ∅ the worst-case
  block-to-block probabilities are ⩾ 8/9 = 1 − (1 − 2/3)², then p > p_c; "2/3 may be replaced by any rigorous
  upper bound on the critical probability of oriented bond percolation in two dimensions (see [Liggett 1995])".
- **[secondary: Holmes–Salisbury, "Forward clusters for degenerate random environments", Combin. Probab. Comput.
  25 (2016); arXiv:1307.2787v1, pp. 3–4]** "The best rigorous bounds that we have found in the literature are
  0.5466 ≤ p_c^{↖↑} ≤ 0.7491, where the latter comes from the fact that p_c^{↖↑} ≤ p_c^{↑→} ≤ 0.7491 (the latter,
  referring to oriented percolation on the square lattice, is in Balister et al [1994])." Here p_c^{↑→} is
  oriented **site** percolation on Z² with arrows up and right: 2dOP.
- **[secondary: Gomes–Pereira, "Upper bounds for critical probabilities in Bernoulli percolation models",
  J. Appl. Probab. (2025), arXiv:2106.10388v2, §4.4 and remark (9)]** use "Liggett's upper bound p⃗_c^s(2) ≤ 3/4"
  for oriented site percolation in d = 2, and p⃗_c^b(2) ≤ 2/3 for bond.

**Status of 0.7491.** Two independent secondary sources call it rigorous and attribute it to BBS 1994; one says
it rests on "extensive computer calculations" (computer-assisted proof). I did not see the 1994 paper, so I
have not seen the theorem as printed, nor how the computation was certified. It is for **site** percolation,
two parents, square lattice. The third decimal: 0.7491 < 0.75 by 0.0009.

**Numerical value [paper: Wang, Liu, Deng, arXiv:1201.3006v1, Table IX]:** square-lattice directed site
percolation p_c = 0.705 485 25(9) (bond 0.644 700 19(5)). Monte Carlo, not a bound.

---

## 2. Liggett 1995 (request: probability (a))

T. M. Liggett, "Survival of discrete time growth models, with applications to oriented percolation", Ann. Appl.
Probab. 5 (1995), no. 3, 613–636. DOI 10.1214/aoap/1177004698. Open access on Project Euclid, but **not
obtained**: the site refuses automated clients; a cloud browser reached the article page and the PDF (24 pages)
but could not read the PDF's text. (One automated "extraction" of the PDF returned theorem statements that are
not in the paper — invented by the extraction tool. Nothing from that attempt is used here.)

- **[abstract, Project Euclid page]** "We prove survival for a class of discrete time Markov processes whose
  states are finite sets of integers. As applications, we obtain upper bounds for the critical values of various
  two-dimensional oriented percolation models. The technique of proof is based generally on that used by Holley
  and Liggett to prove survival of the one-dimensional basic contact process. However, the fact that our
  processes evolve in discrete time requires that we make substantial changes in the way this technique is
  used. When applied to oriented percolation on the two-dimensional square lattice, our result gives the
  following bounds: p_c ≤ 2/3 for bond percolation and p_c ≤ 3/4 for site percolation."
- **[secondary: Ráth–Valesin, "On the threshold of spread-out contact process percolation", arXiv:1912.09825v3,
  Appendix 7.2, pp. 59–61]**
  - Their process: η_{n+1}(z) = Z(z, n+1) · max(η_n(z), η_n(z + e₁)), Z i.i.d. Bernoulli(p) (Definition 3.5).
    "the transition rules of our process (η_n) with parameter p are the same as the ones of the process (A_n)
    of [Li95], with parameters q = p in the notation of that paper (see the beginning of the Introduction
    there)."
  - "The assumption for the aforementioned Proposition 2.1 of [Li95] is that p > 1/2 and q ≥ 4p(1 − p), which
    when p = q means simply that p ≥ 3/4." So **equality is allowed** in Proposition 2.1 as they quote it, and
    they apply it at p = 3/4.
  - What Proposition 2.1 gives (the special case they state as their Proposition 7.3): with
    a = (1 − p + √(1−p))/p, b = (1 − p − √(1−p))/p, c_k = (2k)!/(4^k (k!)² (2k − 1)), F(1) = 1 and
    F(k) = −(2/(a − b)²) Σ_{j=0}^{k} c_j c_{k−j} a^{2j} b^{2(k−j)} for k > 1: "If p ≥ 3/4 then F is positive and
    non-increasing, moreover Σ_k F(k) < ∞." F is the tail of the gap law of a renewal measure Ψ on {0,1}^Z.
  - "Equation (1.4) in [Li95] gives … for any finite subset A of Z: Ψ(η⁰ ∩ A = ∅) ≥ P(η⁰ ∩ η₁^A = ∅)" (η⁰ ~ Ψ
    independent of the percolation): one step of the process makes the set "less likely to miss" a Ψ-sample.
    This is the Holley–Liggett comparison; survival is deduced from it in the paper, but I have not seen that
    step or its theorem number.

**What this does and does not settle.**
- *Equality.* As quoted by Ráth–Valesin, the hypothesis of Liggett's Proposition 2.1 is q ≥ 4p(1 − p) with
  equality allowed, together with p > 1/2. Whether Liggett's *survival theorem* also holds at equality I could
  not see. Note the abstract's "p_c ≤ 3/4" is true whether or not there is survival at 3/4.
- *Conditional independence.* I could not see Liggett's definition. Ráth–Valesin identify his process with q = p
  with the site model above, whose sites are conditionally independent given the previous level, and they use
  his (1.4), a statement about the joint law of η₁^A, for it. Since the definition is a transition law
  for a whole set A_n → A_{n+1}, I would expect independence of sites given A_n to be part of the definition
  rather than a separate hypothesis, but that is an inference, not a reading.
- *Librarian's check of the parametrisation* (consistent with the abstract, not read in the paper): with p the
  probability for a site with exactly one occupied parent and q with two, site percolation has q = p and
  p ≥ 4p(1 − p) ⇔ p ≥ 3/4; bond percolation with arc probability r has p = r, q = 1 − (1 − r)² and
  2r − r² ≥ 4r(1 − r) ⇔ r ≥ 2/3. Both match the abstract's 3/4 and 2/3.
- *Survival exactly at 3/4* does follow from §1 if BBS's 0.7491 is accepted: θ is non-decreasing in p, so
  p_c ≤ 0.7491 < 3/4 gives θ(3/4) > 0. It does **not** follow from "p_c ≤ 3/4" alone, because θ(p_c) = 0
  for oriented percolation (Bezuidenhout–Grimmett 1990 for the contact process; Bezuidenhout–Gray 1994 for
  attractive finite-range systems; stated for GOSP in Hartarsky–Szabó, Remark 4.6 [paper]). So a proof
  anchored at exactly 3/4 rests either on the computer-assisted 0.7491 (secondary) or on a reading of
  Liggett's survival theorem at equality (not available here).

---

## 3. Finite volume: survival for time e^{cK} at every p > p_c (request: critic (b), probability (b))

### Hartarsky and Szabó 2022 (general oriented site percolation)

I. Hartarsky, R. Szabó, "Generalised oriented site percolation", Markov Process. Related Fields 28 (2022), no. 2;
arXiv:2103.15621 (v3 read: §1, §3, §4.1–4.2; v1 read: §2.1, §5.5, §5.7.2, Appendix A.4).

**Setting [paper, §1.1].** d ⩾ 2; a neighbourhood X ⊂ Z^d \ {0}, finite, |X| ⩾ 2, with ⟨x, u⟩ > 0 for all
x ∈ X for some u (orientation; normalised to u = e_d); the group generated by X is Z^d ("can be achieved by an
invertible linear transformation of Z^d and, possibly, a restriction to a sublattice"). Sites open i.i.d.
Bernoulli(p); a → b if there are open a₁, …, a_m = b with a₁ − a ∈ X, a_i − a_{i−1} ∈ X (a itself need not be
open). R = max{t : (x, t) ∈ X}. p_c = inf{p : θ(p) > 0}. For d = 2 this covers one-dimensional oriented site
percolation with **any finite set of parents**: X = {(0,1),(1,1)} (two parents) and X = {(−2,1), …, (2,1)}
(five parents) both qualify, R = 1.

**Theorem 4.1 [paper, p. 9; credited to Bezuidenhout–Gray 1994].** If θ(p) > 0 then for every ε > 0 there are
n, h, w, v such that from any box B_n placed in the block B(w, h, v), with probability > 1 − ε the box infects,
*inside the bounded region B(4w, 8h, v)*, translates of B_n in both target blocks B(w,h,v) + 7h(v,1) ± 2w e_{d−1}.

**Theorem 4.2 (BG renormalisation) [paper, p. 10].** Fix q < 1. If (10) holds with ε small enough (depending on
q), the GOSP can be coupled with two-parent oriented percolation ζ of parameter q so that j ∈ ζ_k implies an
infected box in the block indexed (j, k). (Proof: 1-dependent oriented percolation with density ⩾ 1 − ε, then
Liggett–Schonmann–Stacey 1997.) The events used live in bounded space-time regions, which is what makes a
finite-volume version possible.

**Theorem 4.3 (exponential death bounds) [paper, p. 12].** For every p > p_c there is ε(p) > 0 with, for all
A ⊂ S and t ⩾ R: P_p(t ⩽ τ^A < ∞) ⩽ e^{−εt} and P_p(τ^A < ∞) ⩽ e^{−ε|A|} (process on the infinite lattice).

**Corollary 4.8 [paper, v3 p. 14; Theorem 17 in v1, §5.5].** GOSP on the quotient graph with vertex set
T_n^{d−1} × Z (torus of side n in the space directions; for d = 2, a **cylinder of circumference n**). Extinction
time τ^T = sup{t ⩾ 0 : T_n^{d−1} × {0, −1, −2, …} → T_n^{d−1} × {t}} (i.e. started **full**).
- For all p < p_c: τ^T / log n → (d − 1)/c(p) in probability.
- **For all p > p_c there exist c, C ∈ (0, ∞) such that τ^T / E_p[τ^T] → E (standard exponential) in law, and
  e^{c n^{d−1}} < E_p[τ^T] < e^{C n^{d−1}} for n large enough.**

Proof status [paper]: stated "for completeness"; "the proofs rely on Theorems 4.2, 4.3 and 4.7", with a sketch
in v1 Appendix A.4: the exponential law as in Mountford 1993 Proposition 1.2 (regeneration + submultiplicativity
of P(τ^S ⩾ t)); "lim_n P_p(τ^S < e^{εn}) = 0 for some ε > 0 follows from Theorem 3 [the BG coupling] and the
same assertion for 2dOP on finite volume with parameter close to 1 started from one site"; the lower bound on
E τ^T "as in [Liggett 1999, Theorem I.3.9]", embedding a path of ε n^{d−1} boxes in the torus so that the
GOSP dominates a finite-range-dependent 2dOP with parameter close to 1, then Liggett–Schonmann–Stacey. So the
statement is printed for all p > p_c, but its proof is a sketch built on the near-1 finite-volume fact.

**What this gives for the request (librarian's one-line consequence).** For d = 2 and any p > p_c: by the
exponential limit, P(τ^T > E τ^T / 2) → e^{−1/2}, and E τ^T > e^{cn}, so P(τ^T > e^{cn}/2) ⩾ 1/2 for n large.
That is "on a cylinder of width K, started full, alive at time e^{c′K} with probability bounded below", for
two-parent **and** five-parent site percolation, at every density above the respective p_c.

**What it does not give.** (i) An *interval* with dead (closed) boundary rather than a cylinder: the authors
remark (v3 p. 14) that for GOSP "considering a box is either inappropriate or requires tilting the lattice
first", and they state nothing for an interval. For a symmetric neighbourhood (two-parent written as
{(−1,1),(1,1)}, or the symmetric five-parent one) the drift v can be taken 0 and the interval is the natural
analogue, but I found no printed statement. The near-1 interval fact is Mountford 1993 Fact 2.1 (see
`nonmonotone.md` §1, "Does it apply here?"), which is what the BG coupling feeds. (ii) An explicit c.

### Other candidates named in the request

- **R. Durrett, "Oriented percolation in two dimensions", Ann. Probab. 12 (1984), 999–1040** [paper, author's
  reprint https://sites.math.duke.edu/~rtd/reprints/paper23.pdf, scan; pp. 999–1001 read]. Bond percolation
  (§2: arcs (0,1), (1,0) open with probability p). Contents: §7 exponential estimates for p < p_c; §9 "A
  construction for studying p > p_c"; §10 "P(τ^A < ∞) ⩽ C exp(−γ|A|)"; §11 large deviations for the edge.
  The table of contents lists no finite-interval or finite-cylinder section; I did not read §§9–10.
- **C. Bezuidenhout, G. Grimmett, "The critical contact process dies out", Ann. Probab. 18 (1990) 1462–1482** and
  **C. Bezuidenhout, L. Gray, "Critical attractive spin systems", Ann. Probab. 22 (1994) 1160–1194**: **not
  obtained** (Project Euclid). Their block construction is stated in Hartarsky–Szabó Theorems 4.1–4.2 above
  [secondary]. Bezuidenhout–Gray is the reference for finite-range attractive systems, which covers the
  five-parent model.
- **Durrett–Schonmann 1988 (finite set II)** and **Durrett–Liu 1988**: on the shelf (`contact-finite.md` §§1–2);
  continuous-time contact process on an interval, nearest neighbour, d = 1, all λ > λ_c. Part II remarks that
  its proofs give Grimmett's sponge-crossing theorem for (unoriented) bond percolation; no statement for
  oriented percolation was seen.
- **T. M. Liggett, Stochastic Interacting Systems (Springer 1999), Theorem I.3.9**: cited by Hartarsky–Szabó for
  the lower bound; **not obtained** (book).
- **J. W. Chen, "The contact process on a finite set in higher dimensions", Chinese J. Contemp. Math. 15 (1994)
  13–20**: cited by Hartarsky–Szabó for e^{c n^d} in d dimensions; **not obtained**.

---

## 4. Five parents (request: probability (b))

- **Critical value of five-parent oriented *site* percolation: not found** (neither a rigorous bound nor a
  numerical estimate).
- **[paper: Soares, Andrade, Herrmann, "Precise calculation of the threshold of various directed percolation
  models on a square lattice", arXiv:cond-mat/0503408v1 (2005), Table I]** Monte Carlo thresholds for directed
  **bond** percolation where a site connects to k sites in the row below. "Model II" (standard square lattice,
  k odd; k = 5 means parents y−2, …, y+2): k = 3: 0.4395 ± 0.0003; **k = 5: 0.2249 ± 0.0003**; k = 7: 0.1470.
  "Model I" (tilted lattice, k even): k = 2: 0.6447, k = 4: 0.3272, k = 6: 0.2121. The authors conjecture
  p_c = η/(k − 1) for model II (η = 0.9 ± 0.1). This is bond, not site; it is an unrefereed short preprint as
  far as the arXiv record shows.
- *Librarian's remarks, not from a source:* adding parents can only add paths, so the five-parent site
  threshold is at most the three-parent one, which is at most the two-parent one (≈ 0.7055 numerically,
  ⩽ 0.7491 by §1).
- **Finite-volume survival for finite-range monotone oriented percolation in one dimension: yes, on a
  cylinder** — Hartarsky–Szabó Corollary 4.8 above covers every finite neighbourhood X in d = 2 (one space
  dimension), at every p > p_c(X). The underlying block construction is Bezuidenhout–Gray 1994 (finite-range
  attractive systems), as the request expected.

---

## Does it apply here?

- Probability's / source's Theorem A anchored at density exactly 3/4 for two-parent site percolation: supported
  only through BBS's p_c ⩽ 0.7491, which I have **second-hand** (two papers call it rigorous; computer-assisted;
  the 1993 paper's site number was a misprint). Liggett's p_c ⩽ 3/4 alone does not give survival at 3/4.
  Liggett's Proposition 2.1 hypothesis q ⩾ 4p(1−p) includes equality (second-hand), but whether the survival
  conclusion is stated at equality is unread.
- Conditional independence: automatic for site percolation; for a comparison process that is only
  *dominated-by* or *dominating* site percolation, the hypothesis must be checked separately (not settled for
  Liggett's general theorem).
- Finite volume at any p > p_c: available on a **cylinder** (periodic space), started full, for any finite
  neighbourhood (Hartarsky–Szabó Cor. 4.8, proof sketched). Not available as printed for an interval with
  dead ends; there one has Mountford's Fact 2.1 (density near 1, 1-dependent) only.

## Corrections to this repository

- "BBS 1994 gives 0.7491 for site percolation": consistent with two secondary sources. The 1993 abstract's
  0.72599 for site percolation is a misprint (Hartarsky–Szabó); do not cite it.
- "Liggett 1995 gives 3/4": the abstract says p_c ⩽ 3/4 (site) and p_c ⩽ 2/3 (bond); it is a bound on p_c, not
  a statement of survival at 3/4.
