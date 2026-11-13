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
4. **[open question] "Chaos always ends" is false as a theorem but plausibly true with overwhelming probability.**
   **Stated model [heuristic, untested]:** a uniformly random map on M = 2^N states in which every step is
   independently fatal (a face dies) with probability h = 1/τ, τ ≪ √M. A random map has on average 1/k cycles of
   length k; a k-cycle is immortal with probability (1 − h)^k; so the expected number of states on immortal cycles
   is Σ_k (1 − h)^k ≈ τ. A random orbit closes on itself at step t with probability ≈ t/M and is still alive then
   with probability (1 − h)^t, so it reaches an immortal cycle with probability ≈ Σ_t (t/M)(1 − h)^t ≈ τ²/M.
   (Without killing, √(πM/2) states are cyclic; the killing is what cuts that to τ.) Whether gump's chaos behaves
   like such a map is the open part — testable in small vessels (PROGRAM E2).
   The long-period oscillators in small boxes (period 66 in a 45-cell hull) are the small-N end of the same thing.
   Not checked numerically. A seed that is *extinct* (population 0) is not the generic end either: still lifes remain.

5. **Characterising end states.** All that is proved is that an end state exists and is periodic. Open:
   (a) classifying periodic patterns beyond small sizes (still lifes are exhaustive only to 16 cells; no search for
   space-filling or hull-filling periodic textures has been made); (b) deriving, rather than measuring, the mix of
   debris a typical seed leaves, and why some cubes go extinct (side 15) and others leave still lifes (side 16);
   (c) proving that a typical seed ends in *small* debris (see 4).

   Now also **[proved]** (`research/theory/`): the threshold lemma (all behaviour beyond period 2 is driven at
   overcrowded cells; ΔE = D − Q) and the sealed-set theorem (no finite set can die unconditionally in ≥ 3 layers).
   **Open from them:** (a) a critical drive rate below which activity must stop; (b) the percolation statement that
   would prove thin slabs cannot sustain chaos; (c) the primary Goles–Olivos sources have not been read.

## Measured, cause unknown

6. **Do whole cubes outlive their ensembles?** Side 16 stayed 7.4 ensemble means at R = 40 (P = 6×10⁻⁴ for that
   one plateau) and 2.8, 2.6, 1.2 at its other large ones. A count over cubes 13–16 gives P ≈ 0.01, but it is post
   hoc (without side 16, P ≈ 0.18 — audit 2026-11-13). Tested 2026-11-13 (`research/lineage/`): 1,248 plateaus of
   cube-like seeds at R = 31–38 wait exactly like soups (mean 0.99 τ, CV 1.02) with no memory between plateaus. So
   it is luck, or something that appears only at side 16's sizes (vertex-centred R ≥ 40), which single engine runs
   cannot reach. GPU ensembles (2026-11-13) find soup lineages memoryless at R = 36–40 too, and with the soup-only
   lifetime at R = 40 (8.6×10⁷) side 16's long plateau is 6.1 means and the sixteen-plateau P is 0.016. Left open:
   cube-like seeds at those sizes, and a weak slow variable (copies of a state inherit ±15–25%
   of its hazard; seen once, ρ ≈ +0.2) whose nature and lifetime are unknown.
7. **Even (vertex-centred) cubes are ≈1.5× tougher** than odd ones at equal face area. No explanation.
8. **Symmetric faces:** is the asymptotic slope exactly 0.209/6 = 0.0348? Measured 2026-11-13 on GPUs: local slope
   0.0329 ± 0.0011 between A = 759 and 828; the A = 828 forecast held (24.175 against 24.0 ± 0.4). In the two
   cube-centred runs the death rate falls with age (p = 0.04, 0.01): unexplained, and it bears on side 17
   (τ ≈ 3.2×10¹⁰ if the rate is constant). Side 17 itself is not run.
9. **Asymmetric faces: where does the cost per cell level off?** Local slopes 0.201, 0.212, 0.212, 0.218, 0.221 up
   to A = 135 (16 peels at the top). Slabs without a rim: 0.2088. Is the rise the rim, or does the bulk constant
   itself sit above 0.22? Needs slab faces at A > 90 and octahedral faces at A ≥ 165.
10. **Interior firewalls** cost ≈0.12 per cell of the band; no account of that number.
11. **The favoured nine-cell state of a dying symmetric face** (10× over-represented) has been counted, not looked at.

## Fauna

12. **Periods beyond 66.** A loop of thirty-odd steps in a 4- or 6-fold box would give 120–200. Nothing forbids it.
13. **Can any oscillator pass a signal to another?** All compound objects found are non-communicating.
14. The 94 clockwork objects (`research/clockwork/objects/`) are not merged into the atlas catalogue.

## Neighbouring rules

15. B45/S3457 (lifetimes ×100 per radius step) and B45/S3456 (glassy freezing): does the face law, with another
    constant, hold there?

## Prior art (`PRIOR-ART.md`)

16. Whether Eppstein's bounding-diamond argument (arXiv 0911.2890) is the same method as T2: one agent says yes,
    the reviewer could not read the paper. Someone should read it.
17. No automaton on this lattice and no lifetime-versus-symmetry result was found in two searches. Absence of evidence.
    The area law itself does have prior art, found 2026-11-13: *supertransients* (chaos lasting exp(c·size), then
    abrupt memoryless collapse), numerical only, nothing proved (`PRIOR-ART.md`, last section;
    `research/theory/swarm/library/`). The key reviews (Tél–Lai 2008) and Bramson–Neuhauser 1994 could not be
    opened by an agent; someone with a browser should read them before a paper claims anything.

## Tools

18. `research/fluct/qsd.py` over-counts exposure for symmetric soups below R = 30. Use the engine there, or fix
    its settle test.
19. No single-state symmetry-reduced engine (needed for side 17 in reasonable time). GPU ensembles exist
    (`research/gpu/`, needs Modal).
