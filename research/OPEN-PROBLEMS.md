# Open problems

One place for what is not settled. Evidence and commands are in `NOTEBOOK.md`; this file only says what is open,
how sure we are, and what would settle it. Remove an item when it is settled (and say where). Tags as in the notebook.

## What can be proved

1. **[proved] Every finite seed is eventually periodic, within 2^N generations**, N = cells in its diagonal hull
   (T2 confines it; a deterministic map on a finite set must cycle). This is the only rigorous lifetime bound we
   have, and it is exponential in the hull's *volume* (side-13 cube: N = 27,474).
2. **[proved] A face layer that empties stays empty** (T2), so the hull only shrinks; "death of a face" is well defined.
3. **[conjecture] The wait for a face to die is exponential in its *area*:** −ln(death rate)/A → 0.208. Measured
   (A = 30–84 directly). Not proved, and probably not provable with present methods for the deterministic rule: it
   needs control of the stationary measure of a chaotic deterministic automaton. Routes that look feasible:
   - a *conditional* theorem: if the quasi-stationary state has exponentially decaying correlations, the chance of a
     near-empty face obeys a large-deviation principle in A, and the measured end-game (death rate ≈ 0.6 × P(one
     cell left)) turns that into the law;
   - a *noisy* gump (each live cell also dies independently with probability ε): then P(face dies this generation)
     ≥ ε^A whatever the state, so the mean wait is ≤ ε^(−A) — an exponential-in-area upper bound in two lines.
     A matching lower bound would be a contour argument of the kind used for the contact process;
   - deriving 0.208 from a model: near empty the face is one small cluster and P(k cells) falls by a constant
     factor 0.65 per cell, which is what a birth–death walk of a single cluster would give.
4. **[conjecture, heuristic] "Chaos always ends" is false as a theorem but true with overwhelming probability.**
   If the chaotic map is treated as a random map with killing rate h = 1/τ, about τ of the 2^N hull states lie on
   cycles that never lose a face, and a random seed reaches one before peeling with probability ~τ²/2^N.
   The long-period oscillators in small boxes (period 66 in a 45-cell hull) are the small-N end of the same thing.
   Not checked numerically. A seed that is *extinct* (population 0) is not the generic end either: still lifes remain.

## Measured, cause unknown

5. **Whole cubes are over-dispersed against memoryless ensembles** (3 of 16 large plateaus beyond 4 means; side 16
   stayed 7.4 means at R = 40; P ≈ 0.01). Luck or real? In progress: `research/lineage/`.
6. **Even (vertex-centred) cubes are ≈1.5× tougher** than odd ones at equal face area. No explanation.
7. **Symmetric faces:** is the asymptotic slope exactly 0.209/6? Fits differ by 0.6 nats at A = 828. Side 17's first
   plateau is forecast in writing (`research/fluct/PREDICTIONS.md`: ≈2×10¹⁰) and not run.
8. **Asymmetric faces beyond A = 84:** one peel at A = 108; the collapse of the rate function to A = 135 is indirect.
9. **Interior firewalls** cost ≈0.12 per cell of the band; no account of that number.
10. **The favoured nine-cell state of a dying symmetric face** (10× over-represented) has been counted, not looked at.

## Fauna

11. **Periods beyond 66.** A loop of thirty-odd steps in a 4- or 6-fold box would give 120–200. Nothing forbids it.
12. **Can any oscillator pass a signal to another?** All compound objects found are non-communicating.
13. The 94 clockwork objects (`research/clockwork/objects/`) are not merged into the atlas catalogue.

## Neighbouring rules

14. B45/S3457 (lifetimes ×100 per radius step) and B45/S3456 (glassy freezing): does the face law, with another
    constant, hold there?

## Prior art (`PRIOR-ART.md`)

15. Whether Eppstein's bounding-diamond argument (arXiv 0911.2890) is the same method as T2: one agent says yes,
    the reviewer could not read the paper. Someone should read it.
16. No automaton on this lattice and no lifetime-versus-symmetry result was found in two searches. Absence of evidence.

## Tools

17. `research/fluct/qsd.py` over-counts exposure for symmetric soups below R = 30. Use the engine there, or fix
    its settle test.
18. No single-state symmetry-reduced engine (needed for side 17 in reasonable time); no GPU stepper.
