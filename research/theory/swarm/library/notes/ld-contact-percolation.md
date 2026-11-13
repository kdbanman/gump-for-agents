# Large deviations of the density: volume order above, surface order below

R. Durrett and R. H. Schonmann, "Large deviations for the contact process and two dimensional percolation",
Probab. Theory Related Fields 77 (1988), 583–603. Read: author's reprint,
https://sites.math.duke.edu/~rtd/reprints/paper43.pdf (OCR text). Sections 1–4 (statements) read; proofs
(Sections 5–6) not read. Nobody asked for this one; it is shelved because it is a proved instance of
"area on one side, perimeter on the other".

## Statements [paper]

Notation: X_n = density of 1's in {1, …, n}^d; a measure is *FKG* if increasing functions are positively
correlated; a *translation-invariant attractive spin system* (TIASS) has flip rates c(i, η) that are
non-decreasing in η when η(i) = 0 and non-increasing when η(i) = 1.

- **Earlier result quoted (Lebowitz–Schonmann, [LS], Theorem 1)** [secondary: this paper, §2]: for a
  translation-invariant FKG measure μ on {0,1}^{Z^d} other than the two point masses, the limits
  lim n^{−d} log μ{X_n ≥ x} = −φ₊(x) and lim n^{−d} log μ{X_n ≤ x} = −φ₋(x) exist and are convex and bounded.
  For an invariant FKG measure of a TIASS, φ > 0 outside [ρ₋, ρ₊] (the densities of the lower and upper
  invariant measures). Nothing is said inside [ρ₋, ρ₊].
- **Theorem 1.** For the upper invariant measure ν of the one-dimensional basic contact process, λ > λ_c:
  there is a convex φ : [0,1] → [0, ∞), zero only at the density ρ(λ), with
  lim n^{−1} log ν{X_n ∈ [a, b]} = −inf_{[a,b]} φ. In particular low density (and the empty interval) costs
  exponentially in the number of sites.
- **Theorem 2.** Supercritical site percolation on Z², σ(i) = 1 iff i is in the infinite cluster, Y_n = density
  of σ in an n × n square, θ(p) its mean: deviations *above* θ(p) decay like exp(−φ·n²) (area).
- **Theorem 3.** Deviations *below*: for 0 ≤ a < b < θ(p), C₁e^{−γ₁n} ≤ μ{Y_n ∈ [a,b]} ≤ C₂e^{−γ₂n}
  (perimeter). The lower bound at a = 0 is "trivial": make the 4(n+1) sites round the square vacant.
- Conjecture 1 and the surrounding discussion: a low density is produced by one "bubble" whose cost is
  proportional to its perimeter.

## Method [paper, introduction]

Renormalisation to 1-dependent oriented site percolation with density near 1, then contour estimates. All
fields are monotone functions of independent variables (Harris–FKG applies throughout).

## Does it apply here?

- The mechanism for surface order in Theorem 3 is *sealing*: a closed ring cuts the square off from the
  infinite cluster, at a cost per boundary site, and after that the inside is "dead" for free. The repository's
  sealed-set results (`thickness.md` T6; board, lemma exchange) say the corresponding cheap seal does not
  exist inside a gump face: the smallest sealed set is a whole face. That is the same dichotomy, stated for a
  deterministic rule; this paper is a place where the dichotomy is a theorem.
- Theorem 1 is the nearest statement to "P(edge row empty) = e^{−γ₂L}" for a random relative: it is for the
  stationary measure of a monotone, self-dual, nearest-neighbour process. Hypotheses failing here: as in
  `contact-finite.md` (monotone, FKG).
- The Lebowitz–Schonmann existence theorem needs only FKG and translation invariance, not a dynamics. Whether
  the natural (quasi-stationary) measure of a gump face is FKG is not known and, given the overcrowding cap,
  not expected.

## Corrections to this repository

None; the paper was not cited. `PRIOR-ART.md` §3 could cite it for "exponent = number of sites" in the
stationary measure of the contact process (d = 1).
