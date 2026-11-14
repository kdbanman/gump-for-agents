# Audit of the counting line (`research/theory/swarm/counting/claims.md`)

_Second reader, 2026-11-14. Audited: `counting/claims.md` and `counting/journal.md` at commit `7c018f9`.
Verdicts were formed from the statements and the journal's proofs before anything of the critic's was opened
(`critic/to-counting.md`, `critic/board.md`); the section "Where I differ from the critic" was written afterwards.
All code is the audit's own (`c*_*.py` in this directory), written from `docs/AUTOMATON.md` and, for the 2D rule
and face12e, from the one-line definitions in `PROBLEM.md`; the only imports from the repository are
`reference/oracle.py` (through the audit's `p0_lib.py`) and no data files._

**State of this file: PART 1 (verdicts from reading, before any recomputation and before the critic was opened).
Parts added later are marked.**

## Part 1. Verdicts from reading the proofs line by line

Verdicts: *correct*; *correct after filling a gap*; *true but narrower than worded*; *wrong*; *not a proof*.

| # | claim (journal entry) | verdict from reading | note |
|---|---|---|---|
| 1 | union bound; gap bound for bijections (2) | correct | (a) and (b) followed line by line; Kac sum, gap sum R(R−1)/2 and Cauchy–Schwarz are right. On a finite set a μ-preserving map is a bijection of the support of μ, so "no bijectivity needed" in (a) is true but empty there |
| 2 | second-order lift (3) | correct | inverse checked; confinement uses T2 once for f(v) and once for u; Φ(H₂) ⊆ H₂ needs f(H) ⊆ H, which is T2 for the face layer |
| 3 | λ(T ≤ k) = \|f^{−k}H\|/\|X\| (1, 3) | correct | identity; needs only f(H) ⊆ H |
| 4 | Theorem 3 (4) | correct | every step followed: light cone ⊆ {\|x′−x\| + r ≤ 2k}; trace = L-periodic words (all L ≥ 1, the ring read as the quotient of the line, neighbours with multiplicity when L ≤ 4); Gelfand; c_k > 0 from the still triple and Perron–Frobenius; monotone in k; c_1 ≤ 0.562 by hand bound (i); table w(s, k) and the worked case 2507 re-derived by hand |
| 5 | c_1, c_2 (9) | computed: to recompute | c_3 is measured: out of scope |
| 6 | gump slab face, fixed k; same for face12e (4, 14) | correct | lower bound H ⊆ f^{−k}H; guard: light-cone induction on max-norm distance 2k + 2 − 2j; the face12e guard argument (an outside face holds one cube edge, so sees ≤ 2 of the cube) is right |
| 7 | box edge (5a, 9) | correct | the padded word has L + 4k windows, of which the 4k centred outside the box are allowed automatically (columns confine); equality c⁰ = c for k = 1, 2 rests on a computed class structure: to recompute |
| 8 | symmetry at a fixed age (5b, c, e) | correct | (b) injection symmetric killable states → allowed open words of ⌊L/2⌋ + 1 columns; (c) the only identifications inside the band are left corner square ↔ right corner square when L ≥ 4k + 3; (e) product measure on one cell per orbit |
| 9 | "mirror = exactly half" | sketched: out of scope | |
| 10 | gump: top cubes (6, 8) | correct (with entry 8's "six") | 6-cycle, private cell, 40 of 64, kill sets K(s, k) all re-derived by hand; the product formula needs a slab ≥ 3 layers deep and the six cells beneath a cube distinct |
| 11 | beneath empty: dies iff …; a full face always dies (6, 8) | first part correct; "a full face always dies" true but narrower than worded | holds when every face cell has six in-face neighbours (rim-free slab face; the journal says "k = 6 everywhere"). On a hull face rim cells have k < 6: the full R = 3 face over empty layers keeps its six cells with k = 4 |
| 12 | gaps persist (10) | correct | |
| 13 | c_k(p) ≤ −ln(1 − p) (10) | correct | from claim 12 with k → 0 |
| 14 | dice hierarchy (10) | correct | rows read at generation t ≥ 1 are ≤ 2k − 2 ≤ w − 1; dice enter only at generation 0 |
| 15 | Lemma 7 (11) | correct | the four fractions re-derived by hand |
| 16 | lone cell, lone triangle over dice (12) | correct | needs a face without doubled neighbours |
| 17 | Cauchy–Schwarz inequality (7, 8) | correct (the inequality) | "hypothesis false" is the lab's measurement; the atom argument is right arithmetic |
| 18 | no finite still pattern robust to the outside (7) | correct | the lowest cell of the right-most column has ≥ 4 free neighbours and ≤ 4 fixed ones: live can be starved (m ≤ 1) or crowded (m ≥ 1); dead can be given n ∈ {3, 4} for every m ≤ 4 |
| 19 | Lemma 8 and corollary (13) | correct after filling a gap | π is "a law on the living states" but the product laws of the corollary charge the dead state; put φ = 0 there (then θ⁻(π) ≤ −ln(1 − p) automatically). "c_k(π) of entries 4 and 10" must be read as the fixed-age exponent of the dice chain itself |
| 20 | Lemma 2′ (16) | lemma correct; second sentence true but narrower than worded | "an invariant measure charging the living states" must mean positive on every living state (or: μ-almost every living state never dies). Gump itself has an invariant measure carried by living states (a still life with a live face cell) |
| 21 | face12e Proposition F (14, 17) | correct | offsets read; Θ^j(full) = {d ≥ j} followed; "gone in n steps" (n − 1 for even n) |
| 22 | face12e Proposition G, Π₁ (14) | correct | table of allowed m re-derived from the rule for every (s, a); Π₁ counts a, k for every cell re-derived; 32^n(8^n + 2·6^n + 5^n) re-derived |
| 23 | face12e lone cell (14) | correct | ladder: 7 edges; the coefficient list re-derived (15 = 8 + 7; 20 = 2 + 8 + 10; 15 = 5 + 8 + 2; 6 = 2 + 4); 3793/8192 |
| 24 | O_h faces (15) | correct | counts re-derived by hand for general N where a formula is given (area, mirrors, rim cells, shared cells); bonds and hexagons to be listed |
| C2 | c_∞(½) > 0 | guessed: out of scope | |
