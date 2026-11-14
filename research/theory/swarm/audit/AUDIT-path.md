# Audit of the path line (`research/theory/swarm/path/claims.md`)

_Second reader, 2026-11-14. Audited: `path/claims.md` and `path/journal.md` at commit `1b9993a`. Verdicts were
formed from the statements and the journal's proofs before anything of the critic's was opened
(`critic/to-path.md`, `critic/board.md` at `3405de3`); the section "Where I differ from the critic" was written
afterwards. All code is the audit's own, written from `docs/AUTOMATON.md`; the only imports from the repository
are `reference/oracle.py` (neighbour offsets; ground truth for the stepper) and, in `p7`, the lab's data file._

## Summary

Verdicts: *correct*; *correct after filling a gap*; *true but narrower than worded*; *wrong*; *not a proof*.
"Read" = statement and proof checked line by line. "Recomputed" = tested with the scripts below. A recomputation
is evidence for a statement and was never used in place of reading its proof.

| claim (journal entry) | verdict | how checked |
|---|---|---|
| **P̄** (8) | **correct.** The slogan "hazard = entry flux × committor" leaves out two terms of the identity (direct deaths from above; the window's boundary term), §1 | both: exact rational identity on an exhaustive gump vessel (2²² soups), on hidden Markov chains, and on a sample of 6.4 × 10⁶ face-generations of the hull R = 7 (`p1`, `p5`) |
| **C** (18) | **correct**; the monotone rows of q are used (control: 63 of 3,000 fail without them) | both (`p2`) |
| **T′** (17.2) | **correct** | both (`p2`: 18,000 cases) |
| **T** (17.3) | **correct** | both (`p2`: 19,127 cases) |
| **X** (17.4 a, b, c) | **correct** | both (`p2`) |
| **Q**, final form (23.2) | (Q1), (Q2) **correct**. The closing line "R and R⁺ give ln τ ≥ θ₀(K − k₀) − ln C⁺ − window" is **true but narrower than worded**: (i) the window term is not controlled by R and R⁺ and can carry the whole hazard (example, §2.2); (ii) R⁺ as a supremum over every visited row cannot hold with a bounded C⁺ on a rim-free gump face, because a full face is empty one generation later (§2.3). Corrected wording in §2.4. The measured numbers of the claim are reproduced (§2.5) | both (`p3`, `p5`, `p6`, `p7`) |
| **V⁻** (24.2) | **correct** | both (`p2`: 36,381 cases; control fails 67,598 of 143,043) |
| **Lemma E1**, **V⁻(E)** (24.3) | **correct**, including the "nothing subtracted" form for the m-fold family of a table with positive roots. The last sentence of the claim (a gump face's bottom rows cost O(1)) is **not a proof**: a conditional remark with two unstated hypotheses, §3 | both (`p2`); thresholds m₀ = 41, 197, 489 reproduced (`p7`) |
| **H** (24.4) | **correct** as an inequality; the same two caveats as Q (window term; R⁺ and B⁺ as suprema), §2 | both (`p3`) |
| **V′** (24.5) | **correct** as stated in the journal. The line in `claims.md` omits the hypothesis that W is admissible with e = 0, without which it is false (control: 1,868 of 4,855 fail), §3 | both (`p2`) |
| **R** (10) | **correct** | both (`p3`: exact rationals, every starting set on 8 graphs) |
| **P** (3) | **correct** (needs a < 1 − s̄, which the hypothesis a + ε ≤ 1 − s̄ gives when ε > 0). One number of its illustration is wrong: "exact 1.8 × 10⁻¹⁵" is 1.62 × 10⁻¹⁵, §4 | both (`p3`) |
| **L1** (2, 7; with 1.1, 1.2 and the cube lemma) | **correct** | both (`p4`: every state of the R = 3 face and the cells beneath, 2²⁴) |
| **L1′** (9) | **correct** | both (`p4`) |
| **S** (9) | **true but narrower than worded.** "Lost for ever" has to mean "has joined the skeleton K(t)": cells can be dead for ever without lying in any dead sealed set (96 such cells in the end state of the side-8 cube). And S(iii) is about the first loss; "every permanent loss is the extinction of an inclusion-minimal sealed set" is true with "minimal among the sealed sets of V \ K(t − 1)", proved in §5 | both (`p4`) |
| **L3** (4) | **correct** | both (`p4`) |
| **L4, 4a** (4, 12) | **correct** | both (`p4`: hulls R = 7, 9) |
| **F** (20) | **correct**; "at least two cubes deep" is used (at depth one Σ ∪ Λ is sealed but not minimal) | both (`p4`) |
| **R5** (4, 7, 13) | **correct** as a statement of which facts are shared; the lifetimes are the survey's and were read, not re-measured | read; the five rows of `research/phase/rules.csv` |

Nothing tagged proved is wrong. Three statements are narrower than their wording (Q's closing line and with it H's;
S), one line of `claims.md` drops a hypothesis (V′), one sentence is a remark (the end of V⁻(E)), one illustrative
number is off (P).

### Scripts

All in this directory; each runs on one core. Outputs quoted below are from these commands. `p4` also reads
`research/phase/rules.csv`.

| command | time | what |
|---|---|---|
| `python3 p0_lib.py` | 1 s | the audit's stepper against `reference/oracle.py`: hulls R = 3, 5, 7, 20 random states × 6 generations each, 0 differing cells |
| `python3 p1_pbar_exact.py` | 35 s | P̄: exhaustive gump vessel; hidden Markov chains; the worked walk |
| `python3 p2_tables.py` | 75 s | T′, T, X, C, V⁻, V′, E1, V⁻(E) on random tables, with controls |
| `python3 p3_hazard.py` | 15 s | Q, H, P on non-Markov processes; R exactly; the window term |
| `python3 p4_structure.py` | 60 s | L1, L1′, S, L3, L4, F, R5 by enumeration |
| `python3 p5_hull30.py 60000 1` | 55 s | a sample of the living state of the hull R = 7: P̄ exactly on the sample; R, Φ, C⁺ over all rows |
| `python3 p6_top_rows.py` | 8 s | what a full face does in one step (R⁺ at the top rows) |
| `python3 p7_tallies.py` | 1 s | the measured numbers of Q and V⁻(E) from the lab's tallies |

## 0. The conditional area law: what the condition is, what it is about, and whether the last step is airtight

**Objects.** For each face size A: a vessel, an initial law, the rule; S_t = "this face is alive and the replica is
still observed at t" (any nested rule of censoring); Z_t = the face's population; a window t₀ ≤ t ≤ t₁. Pooled
exposure N(z), deaths D(z), transitions F(z, z′) (journal entry 8); T̄ = F/N with T̄(z, 0) = D(z)/N(z);
M_k(s) = Σ_{k′ ≥ 0} T̄(k, k′)e^{−s(k′ − k)}; p_z = N(z)/Expo; h̄ = Deaths/Expo, τ = 1/h̄.

**What is proved (Q1), with nothing left out.** Let θ₀ > 0, 0 ≤ k₀ < K. If

    (R)   M_k(θ₀) ≤ 1 for every visited row k₀ ≤ k < K, k ≥ 1,

then

    h̄  ≤  e^{−θ₀(K − k₀)}·Φ  +  B/Expo,
    Φ = Σ_{z ≥ K} p_z Σ_{0 ≤ z′ < K} T̄(z, z′) e^{θ₀(K − z′)},
    B = E[ψ(Z_{t₀}); Z_{t₀} < K, S_{t₀}] − E[ψ(Z_{t₁+1}); Z_{t₁+1} < K, S_{t₁+1}],   ψ(k) = e^{−θ₀(k − k₀)⁺}.

**The area law that follows, airtight** (the audit's wording; proofs in §2). For a family of faces A → ∞ with
K = ⌈κA⌉, suppose there are θ₀, κ > 0 and k₀, ε, c independent of A with

1. (R) on every table of the family;
2. (Φ) Φ_A ≤ e^{εA}. A sufficient form: R⁺ with constant C⁺ on a set 𝒵 of rows z ≥ K, and the living weight of
   the other rows z ≥ K at most e^{−θ₀K}; then Φ ≤ C⁺ + 1 (§2.4);
3. (W) one of: (a) the window starts above the low set, Z_{t₀} ≥ K on S_{t₀}; (b) the pooled law is
   quasi-stationary over the window, censoring is at most c times the hazard (s̄ ≤ c·h̄, c ≥ 0), and
   w = Σ_{z<K} p_z ψ(z) ≤ 1/(2(1 + c)).

Then h̄_A ≤ 2e^{θ₀k₀}·e^{−(θ₀κ − ε)A}, that is, liminf (1/A)·ln τ_A ≥ θ₀κ − ε. (In a quasi-stationary window without
censoring, and with R⁺ on all visited rows, h̄ ≤ C⁺e^{−θ₀(K − k₀)} with no window term and no condition on w.)

**What the condition is about.** T̄_A is the one-step table of the face population *pooled over the living
ensemble*: a functional of the rule, the vessel, the initial law, the censoring rule and the window. It is not a
transition law of the rule: the population is not a Markov chain (in the exhaustive vessel of `p1` the table's
committor at the entry point z′ = 4 is 0.939 and the true probability of dying before leaving the low set is
0.337). So (R) is a statement about the rule, through an average over whatever else the living state carries at
each population; nobody has derived it. It is known from samples: the lab's tallies at A = 30, 45, 63, 84 (rows
≤ A/2; block minima 0.4034, 0.4261, 0.4117, 0.4172, reproduced by `p7`) and the audit's own sample at A = 30 with
every row tallied (0.4139 on 6.4 × 10⁶ face-generations, `p5`).

Two remarks on sampled tables.
- Theorem P̄, and so (Q1), applied to a sample's own counts is exact for that sample: no sampling error enters
  (`p5` checks the identity in rational arithmetic on the sample). "R holds on the tallied table" therefore bounds
  that sample's deaths over exposure, provided every row was tallied.
- As evidence for (R) at sizes not measured it is thin, and it cannot be made cheap: the rows that matter
  (k₀ ≤ k ≲ 10) are visited about as rarely as faces die, so testing (R) at a new size costs what measuring τ
  there costs. The theorem turns "exponential in the area" into a one-step statement; it does not make it easier
  to observe. (Path says the hypothesis is not derived and cannot follow from the graph and θ, R5; I agree.)

**Is the step from the condition to "exponential in the area" airtight?** From (R), (Φ), (W): yes; every step
(P̄, T′, Q1) was read and recomputed. From "R and R⁺" as worded in `claims.md`: no, for the two reasons of §2.2
and §2.3. Neither reason changes what Q gives at the measured sizes: on the audit's sample at A = 30 the
inequality (Q1) holds with Φ over all rows and the boundary term as measured (§2.2), and the block's 0.13–0.14
per cell is θ₀κ.

**The second conditional result** (V⁻(E), H): the condition is on a *family* of tables and a rate family Λ:
(E) ln M^{(m)}_n(s) ≤ mΛ_{n/m}(s) + e_m for all real s on the block, with a margin (R_ε). It gives a bound on the
table's committor, liminf −(1/m)·ln ψ*_m ≥ V − V̄, airtight as proved. To reach the hazard it needs the same two
things as Q (the entry term Φ[ψ]; the window term). For gump (E) concerns tables of faces of thousands of cells,
which do not exist; I did not test it (the critic did, between tallied sizes).

## 1. P̄ (journal entry 8)

**Statement as proved** (any process; events S_t ⊇ S_{t+1} ⊔ D_{t+1}; Z countably valued on S_t; 𝓛 finite; ψ ≥ 0 on 𝓛
with D(z) + Σ_{z′∈𝓛} F(z, z′)ψ(z′) ≤ N(z)ψ(z) on 𝓛):

    Deaths ≤ D(𝓛ᶜ) + Σ_{z∉𝓛, z′∈𝓛} F(z, z′)ψ(z′) + E[ψ(Z_{t₀}); Z_{t₀}∈𝓛, S_{t₀}] − E[ψ(Z_{t₁+1}); Z_{t₁+1}∈𝓛, S_{t₁+1}],

with equality iff the hypothesis holds with equality on 𝓛. The proof (identity (I), sum over 𝓛, cancel the finite
double sum) is complete and correct. The same lines prove it for the integer counts of a finite sample.

**One detail to fill.** "ψ* = (I − T̄_𝓛)⁻¹ d̄" assumes I − T̄_𝓛 is invertible. Define instead ψ* = Σ_{i ≥ 0} T̄_𝓛^i d̄,
which always converges (its partial sums are probabilities), is the smallest non-negative solution, and satisfies
the hypothesis with equality; the inverse exists iff no set of visited low states is closed under the table. At a
row with N(z) = 0 the hypothesis reads 0 ≤ 0 and ψ*(z) is immaterial (its entries are cancelled by the end term).

**What "the hazard is the entry flux times the committor" leaves out.** The identity for ψ* is

    Deaths = (direct deaths from 𝓛ᶜ) + Σ_{entries} ψ*(entry point) + (start term) − (end term).

On the audit's sample of the hull R = 7 (A = 30, low set 1…10; `p5`): 7363 = 2 + 6789.29 + 571.71 − 0. So 7.8% of the
deaths are not entries: they are replicas whose first measured state (age T0 = 200) is already in the low set.
In a quasi-stationary window the boundary term is w·(Deaths + Censored), w = Σ p_z ψ(z) (journal, after the proof;
correct), so it is of relative size (1 + s̄/h̄)·w: with the lab's convention a replica leaves when any of its
eight faces dies, s̄ ≈ 7h̄, which is why the term is eight times larger than w. It vanishes exponentially with A
if the living weight of the low set does; at A = 30 it is 8%.

**Tests.**

`python3 p1_pbar_exact.py` (exhaustive: the truncated hull C_d = (1,3,3,5,5,3,3,1), 22 cells, a face of 11; every
one of the 2²² initial states; S = {Z > 0} and S = {Z > 0, not periodic}; two ensembles, three windows, seven low
sets including non-intervals; all arithmetic in fractions, both sides compared with `==`):

    A. gump, exhaustive: truncated hull C_d=(1,3,3,5,5,3,3,1), all 2^22 initial states
      22 cells, face of 11 cells, 434 periodic states
      S={Z>0}; all states; window [0,14]; L=[1, 2, 3, 4]: Deaths=2.39291e+06 Expo=3.30422e+07 direct=29697 entry*psi=2.52766e+06 start=1.10643e+06 end=1.27088e+06  identity exact: True; supersolution slack exact: True
      not Markov: entry point z', true P(die before leaving L | entered at z'), psi*(z') of the pooled table
         z'=2: true 0.87806   psi* 0.99948   (423144 entries)
         z'=3: true 0.57429   psi* 0.99598   (835723 entries)
         z'=4: true 0.33708   psi* 0.93921   (1202179 entries)
      S={Z>0, not periodic}; all states; window [0,14]; L=[1, 2, 3, 4]: Deaths=2.39291e+06 Expo=1.21749e+07 direct=29697 entry*psi=1.62952e+06 start=733693 end=0  identity exact: True; supersolution slack exact: True
      all exhaustive cases exact: True
    B. hidden Markov chain with censoring, exact rationals ... all hidden-Markov cases exact: True
    C. ... p1=0.2087 p2=0.7913 lambda=0.9478 h=0.0522  entry flux=0.1978  flux*psi=0.0495  w=psi(1)p1=0.0522  flux*psi/(1-w)=0.0522

("Supersolution slack exact": for ψ = ψ* + (I − T̄_𝓛)⁻¹η, η ≥ 0, the right side exceeds Deaths by exactly Σ N(z)η(z).)
The smallest case of the claim is right; its "0.0495/(1 − 0.0522)" divides by 1 − w, and w = ψ(1)p₁ happens to
equal h in this example.

`python3 p5_hull30.py 60000 1` (the living state of the hull R = 7; soups of density 0.35, replicas measured from
age 200 while all eight faces live; statistic = population of a face, pooled over the eight):

    hull R=7: faces of A=30 cells; 60000 soups, 7191 replicas reached age 200 with eight living faces; 0 settled; exposure 6395360 face-generations, 7363 deaths
    hazard = 1.1513e-03, -ln h = 6.767 +- 0.012   (board: ln tau = 6.804 at A = 30); 7191 replicas lost a face (172 deaths are second faces emptying in the same generation; counting one death per replica: -ln h = 6.790)
    1. P-bar, low set 1..10: Deaths = 7363;  direct deaths from above = 2, sum over entries of psi* = 6789.2931, start = 571.7069, end = 0.0000;  identity exact: True
    1. P-bar, low set 1..15: Deaths = 7363;  direct deaths from above = 0, sum over entries of psi* = 6528.8529, start = 834.1471, end = 0.0000;  identity exact: True

## 2. Q (23.2) and H (24.4)

### 2.1 What is correct

T′ (ψ = e^{−θ₀(k−k₀)⁺} is a supersolution under R), then P̄, then the two bounds ψ(z′) ≤ e^{−θ₀(K−k₀)}e^{θ₀(K−z′)} for
1 ≤ z′ < K and 1 ≤ e^{θ₀k₀} for a direct death: (Q1) is exact bookkeeping. (Q2), Φ ≤ sup over visited z ≥ K of
M_z(θ₀)e^{−θ₀(z−K)}, follows by adding the non-negative terms z′ ≥ K. Corollary H is the same computation with the
certificate of V⁻ (Hölder over the at most K landing points). All three were read line by line, and tested on
processes whose population is not Markov (`python3 p3_hazard.py`):

    Q  : 1488 (process, window, K, k0, theta0) cases: violations of (Q1) 0, of (Q2) 0
         size of the start term against the main term e^(-theta0(K-k0)) Expo Phi in these cases: median 0.26, 90th percentile 1.5, max 62
    H  : 319 cases with good rows: violations of Deaths <= Expo Phi[psi] + boundary 0; of the bound on Phi[psi] under R+ and B+ 0

(In H the slack e of B⁺ need not be the e of the admissibility of W; the proof goes through with a separate e⁺,
and the test uses the least e⁺.) The smallest case of the claim: Φ = ¾p₃ = 0.538, C⁺ = 1.50, (Φ/27)/(1 − w) = 0.0208,
exact h = 0.0143 (`p7`).

### 2.2 The window term is not controlled by R and R⁺

The journal writes "− (window term)" and says what the term is; it does not say when it is small, and the
board's closing line drops it. It needs a hypothesis.

*Example (`p3`, last block).* Living states 1, 2; state 0 dead. Row 1: to 0 with probability 10⁻⁴, stay ½, to 2
with 0.4999. Row 2: to 1 with 0.005, stay 0.095, censored 0.9. K = 2, k₀ = 0. Then θ₁ = 8.517 = θ₀ (R holds), C⁺ =
M₂(θ₀) = 25.09 (R⁺ holds), and in the quasi-stationary state

    quasi-stationary law (0.4513, 0.5487), h = 4.513e-05, censoring rate 0.494
    C+ e^(-theta0 (K-k0)) = 1.004e-06;  h / that = 44.9
    the theorem itself: h(1-w) = 4.512e-05 <= e^(-2 theta0) Phi + w sbar = 4.513e-05  (w sbar = 4.458e-05)

The hazard is 45 times C⁺e^{−θ₀(K−k₀)}; the theorem holds because the window term w·s̄ carries it. Heavy censoring
above the low set leaves the surviving mass sitting in the low set.

*Filling (Proposition W).* In the setting of (Q1), with ψ ≤ 1 the block certificate and B the boundary term:

- (a) B ≤ P(Z_{t₀} < K, S_{t₀}); and B ≤ 0 if Z_{t₀} ≥ K on S_{t₀}. *Proof.* ψ ≤ 1 and the end term is ≥ 0. ∎
- (b) If the law of Z_t given S_t is the same law π for t₀ ≤ t ≤ t₁ + 1, then with w = Σ_{z<K} π(z)ψ(z) and
  s̄ = Censored/Expo:  h̄(1 − w) ≤ e^{−θ₀(K−k₀)}Φ + w·s̄. Hence if s̄ ≤ c·h̄ and (1 + c)w < 1,
  h̄ ≤ e^{−θ₀(K−k₀)}Φ / (1 − (1 + c)w).
  *Proof.* B = w·(P(S_{t₀}) − P(S_{t₁+1})) = w·(Deaths + Censored) (the journal's remark after P̄). Insert in (Q1),
  divide by Expo, and move w·h̄ and c·w·h̄ to the left. ∎
- (c) In (b) with no censoring: h̄ ≤ C⁺e^{−θ₀(K−k₀)}, C⁺ the supremum of (Q2); no window term.
  *Proof.* p_z = π(z), so Φ ≤ C⁺·π(Z ≥ K) by the proof of (Q2), and 1 − w ≥ 1 − π(Z < K) = π(Z ≥ K). ∎

Tested (`p3`):

    W1 : quasi-stationary, no censoring: 5052 cases, violations of h <= C+ e^(-theta0(K-k0)): 0 (largest h / bound 0.180)
    W2 : quasi-stationary with censoring: 6414 cases, violations of h(1-w) <= e^(-theta0(K-k0)) Phi + w sbar: 0

*Size on gump, A = 30* (`p5`, θ₀ = 0.4139, K = 11, k₀ = 5): pooled mass below K 0.199; w = 0.0713; s̄ = 6.81·h̄; so the
window term w·s̄ = 5.6 × 10⁻⁴ is half the hazard (1.15 × 10⁻³), and the start term of the actual window is 6.4 × 10⁻⁴.
The main term is 1.4 × 10⁻², so nothing is at risk at this size; (b) applies with c = 6.81, (1 + c)w = 0.56. For
the area law one needs (1 + c)w bounded away from 1 as A grows: true if the living weight of the low set tends to
zero, which the tallies show and R does not imply.

### 2.3 R⁺ (and B⁺) as suprema over every visited row

R⁺ asks C_z := M_z(θ₀)e^{−θ₀(z−K)} = E_z[e^{−θ₀(Z′−K)}] ≤ C⁺ at *every* row z ≥ K with p_z > 0.

*Fact (from the rule; journal 1.1, the "doomed" cell).* A face cell with its six in-face neighbours alive has
n ≥ 6 and is dead next, whatever lies beneath. So on a rim-free face (a {111} slab periodic in the plane) a full
face is empty one generation later with probability one, T̄(A, 0) = 1, and from A − j live cells the next
population is at most 7j (survivors need a dead in-face neighbour: at most 6j; births: at most j). Hence
C_A = e^{θ₀K} exactly and C_{A−j} ≥ e^{θ₀(K−7j)}: **if the full row is visited at all, C⁺ ≥ e^{θ₀K} and the closing line of
Q reads ln τ ≥ −θ₀k₀ − window.** B⁺ fails the same way (T̄(A, 0) = 1 forces e ≥ W(n₁)). On a hull face the rim
softens this: at A = 30 most cells are rim.

`python3 p6_top_rows.py`:

    (i) periodic slab, 3 layers of 27 cells; top face; 20000 random states beneath for each j
        from A - 0 = 27 live cells: next population max 0 (bound 7j = 0), mean 0.00
        from A - 1 = 26 live cells: next population max 6 (bound 7j = 7), mean 1.28
        from A - 2 = 25 live cells: next population max 12 (bound 7j = 14), mean 2.67
    (ii) hull R=7, face of 30 cells, rest of the hull at random (densities 0.2, 0.4, 0.6); theta0 = 0.41, K = 11
        from 30 live cells: next population mean 13.20, min 2, max 21; P(next < K) = 0.288; C_z = E e^(-theta0 (Z'-K)) = 1.41   (e^(theta0 K) = 90.9)
    (iii) exhaustive vessel (22 cells, face of 11): number of the 2^22 soups whose face is full at time t
        t = 0..8: [2048, 4930, 1461, 1615, 1994, 1242, 755, 414, 155]

((iii): full rows are visited at every time of an exact pooled law, not only in the initial soup. Whether a full
rim-free face is reachable after t = 0 I did not determine; in the initial soup it has probability ρ^A.)

On the audit's sample at A = 30, with every row tallied (`p5`):

    rows K..A/2: Phi = 0.1384, C+ = 1.0494 (at row 11), direct deaths 2, share of the exposure 0.481   (path, K..A/2: Phi 0.136, C+ 1.043, 1 direct death)
    all rows K..A: Phi = 0.1676, C+ = 2.2991 (at row 29), direct deaths 2, share of the exposure 0.801

So over all rows C⁺ is 2.30, not 1.05, on one visit to row 29; Φ, which weights each row by its exposure, moves
from 0.138 to 0.168. The quantity the proof needs is Φ.

### 2.4 Corrected wording of Q's closing line

> Let R hold, and let 𝒵 be a set of rows z ≥ K on which M_z(θ₀) ≤ C⁺e^{θ₀(z−K)}. Then
> h̄ ≤ C⁺e^{−θ₀(K−k₀)} + p(Z ≥ K, Z ∉ 𝒵) + B/Expo, with B as in §0 and bounded as in Proposition W.
> (Equivalently Φ ≤ C⁺ + e^{θ₀K}·p(Z ≥ K, Z ∉ 𝒵).)

*Proof.* P̄ with the block certificate ψ ≤ 1. A row of 𝒵 contributes at most p_z·C⁺e^{−θ₀(K−k₀)}, as in (Q1) and
(Q2). A row outside 𝒵 contributes at most p_z·(T̄(z, 0) + Σ_{z′<K} T̄(z, z′)ψ(z′)) ≤ p_z. ∎ For H: the same with the
certificate of V⁻, R⁺ and B⁺ asked on 𝒵 only.

For an area law with exponent θ₀κ the living weight of the excluded rows must then be at most e^{−θ₀κA}: a
hypothesis on the *upper* tail of the living law, of the same exponential order as the bound itself; and on a
rim-free face the rows next to A cannot be in 𝒵 with a bounded C⁺. Nobody has tallied a rim-free face's table.

### 2.5 The measured numbers of the claim

`python3 p7_tallies.py` (the lab's tallies, the audit's code):

    A=30: K=11; roots of rows 1..5: 0.000 0.276 0.390 0.478 0.483; least root on [5,11) = 0.4034 (row 10); chi = 0.0563; Phi = 0.1362; C+ = 1.043 (row 11); theta0(K-5) - ln Phi = 4.41; -ln h = 6.81; exposure above A/2: 0.32
    A=45: K=16; ... least root on [5,16) = 0.4261 (row 15); chi = 0.0336; Phi = 0.1034; C+ = 1.054 (row 16); theta0(K-5) - ln Phi = 6.96; -ln h = 9.82; exposure above A/2: 0.44
    A=63: K=23; ... least root on [5,23) = 0.4117 (row 22); chi = 0.0230; Phi = 0.0850; C+ = 1.068 (row 23); theta0(K-5) - ln Phi = 9.88; -ln h = 13.63; exposure above A/2: 0.49
    A=84: K=30; ... least root on [5,30) = 0.4172 (row 29); chi = 0.0103; Phi = 0.0458; C+ = 1.068 (row 30); theta0(K-5) - ln Phi = 13.51; -ln h = 18.08; exposure above A/2: 0.51

All as in `claims.md` and 23.3. R(0.35, 0.40, 5) holds at A = 30 by 0.003 on the lab's table; on the audit's
independent sample the block minimum is 0.4139 (6.4 × 10⁶ face-generations against the lab's 1.06 × 10⁸; the
audit's hazard, counted one death per replica, is −ln h = 6.790 ± 0.012 against 6.805). "0.13–0.14 per cell" is
θ₀κ; "0.16–0.17" is the slope of θ₀(K−5) − ln Φ between sizes (0.170, 0.162, 0.173), with Φ over the rows K…A/2 only.

## 3. V⁻, V⁻(E), V′

**V⁻ (24.2).** Correct as stated and proved: g vanishes on rows ≤ k₀; at a row with g > 0 the chain
g(n) − g(n′) ≤ G(n) − G(n′) ≤ (1−δ)(W(n) − W(n′)) + δθ₀(n − n′) ≤ (1−δ)(−ln T̄ + e) + δθ₀(n − n′) uses n > k₀ and (B); the
sum over the N_n landing points ≤ n₁ is Hölder's inequality; the committor is the smallest non-negative
supersolution; ψ* ≥ e^{−W°} is one path. Two definitions a reader of `claims.md` needs from the journal:
N_n = #{n′ ≤ n₁ : T̄(n, n′) > 0} and W̄₀ = max_{0≤j≤k₀} W(j). W must be real-valued (W° is, iff every low state can reach
0 inside the low set).

**Lemma E1, Corollary V⁻(E) (24.3).** Correct: Chernoff for a point and (E) make W(n) = mV(n/m) admissible with
slack e_m on the rows n > ⌊mx₀⌋ (these are exactly the rows with n/m > x₀, and their landing points n′/m ≤ x₁ are
where V's Bellman inequality is available); (E) at s = θ₀ with (R_ε) and N_n ≤ mx₁ + 1 give (G) under (S); W̄₀ ≤ mV̄.
The "nothing subtracted" paragraph is correct (rows n < m are T₁^{∗n}; V(y) ≤ y·w₁ for y ≤ 1; needs m ≥ n₀(δ)).

`python3 p2_tables.py`:

    V- : 36381 cases with every block row good (W = W°, W_J, with slack, scaled), violations 0; in 19372 the certificate at the top row exceeds theta0 (n1-k0)
         control (some row not good, delta < 1): the formula fails in 67598 of 143043
         psi* >= exp(-W°): 7016 rows, violations 0;  W_J <= W° and W_J admissible: violations 0
    V' : 3898 cases satisfying the hypothesis with W = W° (admissible, e = 0), violations 0;  control (W = 3 W°, not admissible, the two numerical conditions still met): 1868 of 4855 fail
    E1 : largest |ln M^(m)_n(s) - m Lambda_(n/m)(s)| over all rows, m = 2, 3, 5, four real s: 1.78e-15
    V-(E): 1496 (base table, m, block, theta0, delta) cases satisfying (S): rows not good 0, violations of the bound 0
           'nothing subtracted' form (k0 = n0(delta)-1): 215 cases, violations 0

(The family test uses W_J of the m-fold chain, which equals m times the quasi-potential with paths restricted to
the lattice (1/m)ℤ; that function is admissible and at least mV, so the test is of Theorem V⁻ on the family and of
the chain "(S) ⟹ every row good", not of the infimum over real paths that defines V.)
The thresholds of the claim on the A = 84 table are reproduced (`p7`): block 5…29, best θ₀ = 0.300, ε₀ = 0.1760,
m₀ = 41, 197, 489 at δ = 0.5, 0.2, 0.1.

**The last sentence of the claim** ("for a gump face the rim lemma (N_n ≤ 7n + 1) makes the bottom cost O(1) when
sparse rows have a margin proportional to their population"). N_n ≤ 7n + 1 is proved (L1(a)). The rest is a remark:
it needs, and does not state, (i) a function W admissible on the sparse rows as well, where (E) is not assumed
(the rows n ≤ mx₀ lie outside the block), and (ii) W(j) bounded in A for j below the first good row. With
W = W° of each table both hold if direct deaths from j ≤ n₀ cells have probability bounded below, but then the
conclusion is about W°, not about mV. Verdict: not a proof; nothing else rests on it.

**V′ (24.5).** The journal's proposition is correct (targets that gain c₁ contract by e^{−(1−δ)c₁}; the others are
bounded through (B) by T̄^δ ≤ e^{−δa}, at most n₁ + 1 of them). The row in `claims.md` omits "W admissible with
e = 0", which the second kind of target uses; without it the statement is false (control above). The example's
numbers ("fails at m = 5, 10, holds from m = 20") were not recomputed.

## 4. C, T′, T, X, R, P

Read line by line; no gap. Notes for a successor:

- **T′.** Needs θ₀ ≥ 0 and M_k(θ₀) ≤ 1 on the rows k₀ ≤ k < K, k ≥ 1 (row k₀ included when k₀ ≥ 1). Unvisited rows
  have M ≡ 0 and are harmless.
- **T.** Needs k₀ ≥ 1, every state of the block leaving it with probability one (stated), and finite roots (a row
  with no downward step has no admissible s_k). The supergradient step, S(k′) − S(k) ≤ s_k(k′ − k) with s_k the
  increment *into* k, is right for non-increasing increments.
- **X.** (a) needs r_k ≤ r̄ < 1 on the block (then r_k = e^{−θ_k}); (b) the lower bound is q^k − q^K, so "up to a
  constant factor" means a factor 1 − q for k ≤ K − 1; (c) 1.695 < 1.863 < 2.234 reproduced.
- **C.** The committor of q is non-increasing because rows 0, …, K − 1 of q are ordered (row 0 = δ₀ is the least
  law); the censored mass of the table is placed at +∞ where ψ_q = 0.
- **R.** Graph finite and connected, λ > 1 as stated; exact on 8 graphs × 3 values of λ, every starting set.
- **P.** The recursion w_{t+1} ≤ (a·w_t + ε)/(1 − s̄) needs y ≤ 1 − s_{t+1}, which is a + ε ≤ 1 − s̄; the geometric sum
  needs a < 1 − s̄. In the illustration "K = 30, p = 3/4: bound 4.0 × 10⁻¹³; exact 1.8 × 10⁻¹⁵", the exact hazard is
  **1.619 × 10⁻¹⁵** (left-eigenvector recursion in 60-digit decimals; 1.776 × 10⁻¹⁵ is eight units in the last place
  of 1 − λ in double precision, which is where 1.8 comes from). The bound 4.0 × 10⁻¹³ at r = 0.344 is right. No
  statement depends on the number.

`python3 p2_tables.py`, `python3 p3_hazard.py`:

    T' : 18000 (table, block, theta0) cases, violations 0;  control (theta0 doubled): 2170 of 8892 fail
    T  : 19127 (table, block, row) cases, violations 0
    X(a): 500 skip-free tables: gambler's-ruin formula and r_k = d_k/u_k reproduced; psi*(k)/pi_k within [(1-rbar), 1/(1-rbar)]: min ratio/(1-rbar) = 1.0106, max ratio*(1-rbar) = 0.9401
    X(b): 1266 branching rows: q^k - q^K <= psi* <= q^k and theta_k = -ln q, violations 0
    X(c): theta1=1.386 theta2=0.847 block bound 1.695 < -ln psi*(2) = 1.863 < root sum 2.234
    C  : 3000 (monotone q, dominating table) pairs, violations of psi*_T <= psi_q: 0;  control (q not monotone): 63 of 3000 fail
    P  : 238 hidden chains with (*) verified at every time of a 60-step window (eps taken as the least constant that makes (*) true): violations of the hazard bound 0
    R  : P(empty before full) == (lam^-n - lam^-N)/(1 - lam^-N) exactly, every starting set, 8 graphs x 3 values of lam: True

## 5. The structure lemmas

**L1, with 1.1, 1.2 and the cube lemma.** Proof of Lemma 1: a dead cell of the face with no live in-face neighbour
has n ≤ m = 3 < 4. Correct, and (a), (b), (c) follow as stated. The geometry it uses was derived again from the
offsets and enumerated (`p4`, hulls R = 3 … 11, d = (1,1,1)): the face is the disjoint union of the triples
{2c + e_x, 2c + e_y, 2c + e_z} over cubes c; beneath the cell 2c + e_a lie u_b = 2c − e_b, u_c = 2c − e_c (layer R − 2) and
v_a = 2c + e_a − 2e_b − 2e_c (layer R − 4); each u is beneath two cells of the same triple, which are in-face
neighbours; each v is beneath one cell; the only face cells without a v in the hull are the three corners.

    G  : hull R=7: face of 30 cells (9 with all six in-face neighbours); beneath each cell u_b, u_c, v_a as in the cube lemma; cells without a private cell: [(0, 0, 7), (0, 7, 0), (7, 0, 0)]; cells of layer R-2 beneath two / one / no face cell: 30 / 0 / 0
    L1 : hull R=3, face of 9 cells and the 15 cells beneath: all 2^24 = 16777216 states: cells alive at t+1 outside N_F[live set]: 0; one-step death <=> the constraints of (c): True
         hull R=7, one live interior face cell (1, 2, 4): 18 distinct cells beneath its seven closed-neighbourhood cells, all 2^18 states: max n(t+1) = 7; 'dies iff each of the seven triples has a dead cell' fails in 0 states

(The seven triples of the smallest case are not disjoint: 18 cells, not 21, because cells of one cube share u's.
The statement "each of the seven triples contains a dead cell" is right as worded.)

**L1′, L3.** One-line proofs, correct. L3's second half uses that closed sets are closed under intersection (so
the smallest closed set containing the live set exists). Enumerated on two vessels with K(t) computed by brute
force as the union of all dead sealed sets:

    truncated hull C=(1,1,1,3,3,3,5,3): 19 cells, 58601 non-empty sealed sets, 612 inclusion-minimal (sizes 2..12); sealed <=> complement closed: True
         1000 random states x 30 generations: K(brute force) != V minus closure(live): 0; L1' violations: 0; K shrank: 0
    one kagome layer: 15 cells, 15062 non-empty sealed sets, 14 inclusion-minimal (sizes 1..6); sealed <=> complement closed: True
         1000 random states x 30 generations: K(brute force) != V minus closure(live): 0; L1' violations: 0; K shrank: 0

The hexagon ring of L3's smallest case: each ring cell has two perpendicular ring neighbours and the coplanar
cell opposite inside, three outside (checked on the offsets).

**S.** (i) and (ii) are `thickness.md`'s lemmas and are right. (iii) as proved: *the first time K(t) is non-empty is
the extinction time of an inclusion-minimal non-empty sealed set of V* (V finite, so a minimal one exists inside
any non-empty sealed set). Two points of wording.

1. *"Lost for ever" is not "in K".* A cell can be dead at every later time without lying in any dead sealed set.
   The closed cube of side 8, run with `reference/oracle.py` in a padded box, is static from generation 23 with 384
   cells; the bootstrap closure of the live set has 480 cells; the 96 extra cells are dead for ever (each has six
   or more live neighbours) and belong to no dead sealed set. In the 19-cell vessel 186 of 1,000 random states end
   on orbits with such cells. So Proposition S describes the growth of the certified dead region K(t), not every
   cell that never lives again. For a face the two agree: a face is sealed (T2), so its death is its entry into K.
2. *"Every permanent loss"* (the journal's title and the board's summary) needs minimality relative to what is
   already lost. **Proposition S′.** If K(t) ≠ K(t − 1), put V′ = V \ K(t − 1). Then K(t) \ K(t − 1) is a non-empty sealed
   set of the vessel V′; every set M inside it that is inclusion-minimal among the non-empty sealed sets of V′ is
   dead at t and has a live cell at t − 1. *Proof.* A cell of K(t) \ K(t − 1) has at most 3 neighbours in
   V \ K(t) = V′ \ (K(t) \ K(t − 1)): sealed in V′. M ⊆ K(t) is dead at t. If M were dead at t − 1, M ∪ K(t − 1) would be a
   dead sealed set of V at t − 1 (a cell of M has at most 3 neighbours in V′ \ M = V \ (M ∪ K(t − 1))), larger than
   K(t − 1). ∎ M need not be minimal, or even sealed, in V: after a hull face has died the next layer is sealed
   in V′ (3 neighbours beneath) and not in V (5).

        2062 growths of K examined (22 with more than 12 new cells skipped): cases in which no minimal sealed set of V minus K(t-1) went extinct at that step: 0; of the 244 first losses, not the extinction of a minimal sealed set of V: 0
        S  : closed cube of side 8 (oracle, padded box): static from generation 23 with 384 cells; closure of the live set has 480 cells: 96 cells are dead for ever and lie in no dead sealed set (96 of them overcrowded, 0 with <= 3 live neighbours)

**L4, 4a.** Lemma 4: the three d-upward neighbours of a top cell are outside W, so no fourth neighbour in V may
be. Correct. 4a's description of d-deep cells (t ≤ R − 4; d′·p ≤ R − 4 for d with the normal coordinate flipped;
≤ R − 2 for each of the other two flips) was re-derived from the three upward offsets and enumerated:

    L4 : hull R=7: 'd-deep' <=> the three inequalities of 4a: 0 disagreements over all cells and diagonals; 4314 (sealed set, diagonal, deep top cell) instances, violations of Lemma 4: 0; Corollary 4a: 334017 cells claimed to be in W, 0 are not
    L4 : hull R=9: ... 6864 ... instances, violations of Lemma 4: 0; Corollary 4a: 960210 cells claimed to be in W, 0 are not

(Sealed sets made as complements of bootstrap closures of random sets in random half-spaces.)

**F.** Counts (i), (ii) from the offsets; sealedness; minimality: a sealed W′ ⊆ Σ ∪ Λ containing a Λ cell contains
its 8 neighbours in Σ ∪ Λ, Λ is connected through in-layer neighbours, and every Σ cell is next to a Λ cell; a W′ ⊆ Σ
has 4 neighbours in Λ outside. Correct. Enumerated, minimality by the criterion "for every cell c of W the
closure of (V \ W) ∪ {c} is V":

    F  : face12e slab 3x3 wall, 2 cubes deep: |Sigma|=9, |Lambda|=18; Sigma cell (in Sigma, in Lambda, outside vessel, elsewhere) = [(4, 4, 4, 0)]; Lambda cell (Lambda, Sigma, next sheet, next layer, outside) = [(6, 2, 2, 1, 1)]; Sigma+Lambda sealed: True, minimal: True; Sigma alone sealed: False; Lambda alone sealed: False
    (the same for 3x4 x 2, 4x5 x 3, 5x3 x 4)
    F  : face12e slab 3x3 wall, 1 cubes deep: ... Lambda cell ... = [(6, 2, 2, 0, 2)]; Sigma+Lambda sealed: True, minimal: False

**R5.** The sealed-set statements use the graph and the smallest birth count; their converse (a set that is not
sealed can be re-entered) uses that 4 is a birth count. All five rules have both. The survey's rows:

    R5 : B4/S345: torus class chaos; median lifetimes in the three hulls 8, 50, 104
    R5 : B45/S34: torus class chaos; median lifetimes in the three hulls 10.5, 20, 36
    R5 : B45/S345: torus class chaos; median lifetimes in the three hulls 28, 254, 3420
    R5 : B45/S35: torus class chaos; median lifetimes in the three hulls 7, 14.5, 22
    R5 : B45/S45: torus class chaos; median lifetimes in the three hulls 6, 12.5, 20

## Where I differ from the critic

The critic confirmed every claim audited here; so do I, as far as correctness of what is proved goes. Differences:

1. **The window term of P̄, Q, H.** The critic's replies do not discuss it; the board's closing line states
   "hazard = entry flux × committor" and "Theorem Q: ln τ ≥ θ₀(κA − k₀) − ln Φ if R". Both are missing the boundary
   term. It is not implied small by R and R⁺ (the example of §2.2: the hazard is 45 times the stated bound), and
   on gump at A = 30 it is 8% of the deaths in the identity for ψ* and half the hazard in Q's inequality. With
   Proposition W (censoring at most a multiple of the hazard; the low set a small part of the living law) the
   conclusion stands. The critic's test of H on "chains run to stationarity" used restarted chains, where the
   term is absent.
2. **Entries from the rows above A/2.** The critic reconstructs them from the inflow identity, which folds the
   start term into "entries" (they say so: "up to two terms of relative order deaths/exposure"). Relative to the
   deaths that term is not small at A = 30: 7.8%. Direct tally (`p5`): Φ over all rows 0.168 against 0.138 on
   K…A/2 (rows above A/2 add 21%); the critic's reconstruction gave 0.159 (17%, "good to a factor of two").
   Consistent.
3. **R⁺ and B⁺ as suprema.** Same finding as the critic's closing reply (§3 there). I add: on a rim-free face it
   is exact that T̄(A, 0) = 1 and that A − j cells leave at most 7j; at A = 30 the supremum over all tallied rows is
   2.30 (row 29) against 1.05 on K…A/2; and the weighted form puts a hypothesis on the upper tail of the living
   law that is of the same exponential order as the bound.
4. **S.** The critic confirms S and the board says "every permanent loss is the extinction, at one instant, of
   an inclusion-minimal sealed set". As worded that is false twice over (cells dead for ever outside K; later
   losses are minimal only relative to V \ K(t − 1)); the statement proved, and its extension to every growth of K,
   are in §5. (The board's definitions do say sealedness is sufficient, not necessary.)
5. **Theorem P's illustration.** The critic confirmed "the worked numbers"; the K = 30 "exact 1.8 × 10⁻¹⁵" is a
   rounding artefact (1.62 × 10⁻¹⁵).
6. **V⁻(E), last sentence; V′ in `claims.md`.** The critic confirms "the paragraph on the bottom rows"; I confirm
   its m-fold part and class the gump sentence as a remark (§3). The missing hypothesis in the `claims.md` row
   of V′ is not mentioned by the critic.

Where the critic went further than this audit and I have nothing to add: the weakenings of V⁻'s hypotheses
(their §2.1), the test of (E) between tallied sizes (§2.3), B⁺ on the tallies, the integer programme for F.

## Not checked

- Anything not tagged proved: V (upper half; the numbers 0.2191, 0.2054, 0.2305, 0.144), V∞, A, G1, W, F12, Dr, the
  exam entries; the data readings of journal entries 5, 11, 15, 16; `bellman.py`, `check_limit.py`,
  `mf_deadend.py`, `vminus_check.py` (none was run or imported).
- Hypothesis (E) on any pair of real tables; the tables of 24.8 (m-fold chains to 2,688 cells); the example of
  24.5; B⁺ on the tallies (−2.4 … −0.6); the collapse and extensivity numbers of 17.5, 22.2, 24.7.
- The infimum over real-valued paths that defines V: the family tests use the lattice version (§3).
- The lab's statements attached to path's claims: "the face is the smallest sealed set of a hull, R ≤ 10"; "Σ ∪ Λ
  is the smallest sealed set iff 3·max(N, M) ≤ 5D + 2".
- The 2D rule's versions of L1 and of N_n ≤ 5n + 1 (same proof with m = 2, θ = 3; not enumerated). L1(b) and the
  growth bounds n_{t+s} ≤ (4s + 1)n_t, O(s²)n_t (immediate from (a); not enumerated).
- The corollary of C on the tallies (its hypotheses are the lab's L9.2). Corollary P1's burn-in length.
- Whether a full rim-free face is reachable after the initial soup; any table of a rim-free face.
- R5's lifetimes and "chaotic on a torus" (read from `research/phase/rules.csv`).
- The audit's sample (`p5`) censors on period 1 or 2 only (none occurred) and is one seed; its hazard was
  compared with the board's at A = 30 only. The stepper was checked against the oracle on hulls R = 3, 5, 7.
- Sizes other than A = 30 were not sampled; nothing was run above 264 cells.
