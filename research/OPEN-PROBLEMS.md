# Open problems

One place for what is not settled. Evidence and commands are in `NOTEBOOK.md`; this file only says what is open,
how sure we are, and what would settle it. Remove an item when it is settled (and say where). Tags as in the notebook.

## What can be proved

1. **[proved] Every finite seed is eventually periodic, within 2^N generations**, N = cells in its diagonal hull
   (T2 confines it; a deterministic map on a finite set must cycle). This is the only rigorous lifetime bound we
   have, and it is exponential in the hull's *volume* (side-13 cube: N = 27,474).
2. **[proved] A face layer that empties stays empty** (T2), so the hull only shrinks; "death of a face" is well defined.
3. **[conjecture] The wait for a face to die is exponential in its *area*:** −ln(death rate)/A ≈ 0.21, with no
   known limit (the fitted limit 0.2077 is retired, CLAIMS GP4; see the postscript below). Measured
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
   **2026-11-14:** the deterministic bulk is not needed. Five or six layers of the rule over fresh coin flips give
   the face the same lifetime (to 0.015 in ln τ at A = 27–60; `research/theory/exponent.md`, reviewed). The problem
   is therefore one about a finite-depth probabilistic automaton, where the second route above applies as stated.
   The measured constant is itself not settled beyond A ≈ 90 (0.2088 on slabs; 0.215 ± 0.006 from A = 108 to 126;
   0.216–0.221 on octahedral faces).
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
   cube-centred runs the death rate seemed to fall with age (p = 0.04, 0.01). At R = 43 (A = 759) that was noise: a
   longer run to 2.6 τ shows no ageing (Weibull k = 1.020, 5,971 deaths; CLAIMS GP5). At R = 45 (A = 828, k = 0.84)
   it has not been re-run, and it bears on side 17 (τ ≈ 3.2×10¹⁰ if the rate is constant). Side 17 itself is not run.
9. **Asymmetric faces: where does the cost per cell level off?** Local slopes 0.201, 0.212, 0.215, 0.218, 0.221 up
   to A = 135 (16 peels at the top; with ln τ_face(84) = 18.141 ± 0.005 from the GPU throughout,
   `research/gpu/README.md`). Slabs without a rim: 0.2088 over mixed widths, 0.2072 within a width family (CLAIMS
   GP9). Slab faces at A > 90 have since been run (CLAIMS GP7, GP8: 0.215 ± 0.006 from A = 108 to 126, and part of
   that is width, GP9), so the question is now whether the cost per cell of a wide face rises at all, and whether
   the octahedral excess is the rim. Still needed: octahedral faces at A ≥ 165 and wide slabs at fixed width.
   **Wrapped faces, 2026-11-15 (CLAIMS GL3, WL1–WL3):** with no closed loop shorter than √21 the price is
   0.2086 ± 0.0001 from 63 to 126 cells with no drift. Each shorter loop direction shortens the life (0.125,
   0.096, 0.054, 0.013 in ln τ at 63 cells for loop² 12, 13, 16, 19; nothing at 21). A face with one short loop
   is a tube with its own straight line: 0.2044, 0.2060, 0.2072 per cell at loop² 12, 13, 16 (the 84-cell face,
   forecast first, refuted the exponential form at 5σ). Open: (a) **whether those lines bend at all** — a
   power-law share is 0.017 from the straight line at 96 cells and 0.035 at 108; forecasts frozen in
   `research/wrap/PREDICTIONS.md` and queued for the card; and why a tube's price depends on its girth in just
   this way (2.0%, 1.3%, 0.7% below the open price); (b) why the effect ends between loops of √19 and √21; (c) how the discounts of several loops
   combine (neither sums of log-discounts nor sums of rates is established); (d) faces below 48 cells and loop²
   9, where no form fits (the 36-cell face with three loops of 12 dies sooner than the loop² 9 faces of its
   area).
   **Since (the same day, CLAIMS WL4–WL6, `research/wraplocal/`):** (b) had a false premise. In the living state
   the density of the face layer is lower by one term for every loop round the face, falling smoothly with the
   loop's length (f(21) is two thirds of f(19) and 45σ from zero), and the tube discounts at 12, 13, 16 are 1.85
   times that deficit; the "end at 21" was the lifetimes' resolution. Now open: (e) **does the relation hold past
   16?** If it does, faces with "no short loop" differ by their long loops and the price with no loop at all is
   about 0.2075, not 0.2086 (W13: the 84-cell face with loops of 21 and 28, forecast 17.534 against 17.547,
   queued for the card); (f) why 1.85, and why the price follows occupation and not turnover (as an elasticity
   the price moves 4.6 times the density); (g) what carries the deficit round a loop: it is not an equal-time
   correlation at the loop vector (below 10⁻⁴); (h) tubes of girth three are cut by transverse firewalls and
   their price falls with length: is every tube, at great enough length, cut the same way, so that no tube line
   is straight for ever? (None in 29,412 deaths of the 84-cell loop-12 tube.)
   **Since (2026-11-16, CLAIMS CN5):** the hull face of 108 cells is 23.3392 ± 0.0099, which refutes one price
   with a linear rim term: rimmed faces pay about 0.231 per cell, wrapped ones 0.209. Open: (i) **why two
   prices**: depth (the card runs thicker slabs), occupation (is a living hull face denser in its interior by the
   0.012 that WL5's relation would ask; forecasts H1–H5 in `research/wrap/PREDICTIONS.md`), or a correction to
   small rimmed faces that is not linear in the rim; (j) the 135-cell hull face would decide the last (29.230
   against 29.163) and is out of the card's reach.
   **Since (the same day, CLAIMS CN3, `research/hulllocal/`):** occupation and depth are ruled out as the reason:
   a living hull face's interior is at the wrapped face's density within 0.001 and slab thickness changes nothing.
   What is left of (i): how a face dies. A hull face has nearly empty corners and a rim of one fuller row and one
   thinner; a wrapped face has neither. **(k)** Watch hull faces and wrapped faces die (as `research/dying` did
   for hull faces): where does the last living patch sit, does a wrapped face's death start anywhere while a hull
   face's must start away from, or at, its corners, and does the dip rate per cell differ between the two?
   **Since (10:20 UTC the same day, CLAIMS WL7, WL8, CN4; the card's rows):** the card measured thicker slabs and
   the price did not move (0.20863 ± 0.00022 at 16 layers), so depth is excluded on lifetimes too. And the wrapped
   side is not one number either: tubes with one loop² of 12 pay 0.2016 ± 0.0005 per cell from 84 to 108 cells
   against 0.2044 from 54 to 84. **(l)** What is the form of a long tube's lifetime: a bend that goes on (towards a
   lifetime set by the girth and not the area, as for the loop² 9 tubes that firewalls cut), or a second straight
   line? Do tubes of loop² 13 and 16 bend too (their lines rest on CPU values, to 75 and 108 cells)? Is the long
   tube's death local, a dead band across the girth that then spreads, where a wide face dies whole? **(m)** The
   loop of 21 costs 0.0047 ± 0.0023: a 2σ answer. A third face with a loop of 21 and none shorter, or the same two
   to ± 0.0015, would settle whether the tail of the density law carries a price.
   **Since (2026-11-17, CLAIMS WL9):** the equilateral 108-cell face at 22.5405 ± 0.0074 is again between the two
   readings and nearer the relation; with the loop-21 face, "long ways round cost nothing" has χ² 5.7 on 2. Not
   settled. The card is running more seeds on the long tubes and long faces of loop² 13 and 16 (for (l)).
   **Since (2026-11-18, CLAIMS WL10):** (l) in part. The bend is not special to loop² 12: a loop² 13 tube at 96
   cells is 4.0 combined errors below its line, loop² 16 leans (2.2), and the 12-tubes hold at 0.20198 ± 0.00031 on
   eight seeds. Still open: the form (the 120-cell tube is due on the 18th); whether 16 bends; and what the
   firewalls on girth-4 faces (ten per face death at 96 cells) do to those lifetimes.
10. **Interior firewalls** cost ≈0.12 per cell of the band; no account of that number.
11. **The favoured nine-cell state of a dying symmetric face** (10× over-represented) has been counted, not looked at.

## Fauna

12. **Periods beyond 66.** A loop of thirty-odd steps in a 4- or 6-fold box would give 120–200. Nothing forbids it.
    **Answered, 2026-11-15 (proof checked by a second agent): periods are unbounded.** A wire between two caps with one extra
    cell is a free-standing oscillator of period 4N + 2 for N units of wire, so every period 6, 10, 14, … occurs
    (`research/signals/README.md` §11; CLAIMS SG5; checked on the oracle at 24 lengths from 1 to 257 by three codes). Still open:
    any period 0 mod 4 above the ones in the fauna, and any odd period above those.
13. **Can any oscillator pass a signal to another?** All compound objects found by sampling are non-communicating.
    **Answered in part, 2026-11-15: yes, signals exist.** Free-standing wires along (1,0,−1) carry pulses at half the
    speed limit; one flipped cell emits a pulse; a standing defect 36 cubes away receives it (and creeps one cube per
    signal); two pulses pass or stop each other by parity (`research/signals/README.md`; notebook entry "gump carries
    signals"; CLAIMS SG1–SG4, confirmed by the review in `research/audit/REVIEW-signals.md`: the receiver is a
    counter that takes d − 1 pulses over d cubes, after which the wire burns). Still open: a bounded or
    closed track (a pulse that turns or comes back), a receiver that stays put, a gate with an output, whether any
    soup-born wire carries a pulse, and whether a pulse can cross living chaos.
    **Second push, 2026-11-15** (CLAIMS SG5–SG10; notebook "a clock of every length"; review in
    `research/audit/REVIEW-signals-2.md` when done): a bounded track exists (the clock; what shuttles is a rake);
    a collision gate with outputs along the input lines; a counter moved by pulses from either side (sixteen positions); wires B and
    C arise from one random unit repeated (not from soups three to six units long, 60,000 tried); chaos destroys any wire it touches, and
    the isolating gap is three empty layers (T3; the review corrected "two"). Reviewed: `research/audit/REVIEW-signals-2.md`. Still open:
    a corner or a crossing (nothing found, nothing searched outside one wire direction), a reusable reflector for a
    pulse (none inside the searched bounds), a receiver that toggles, a gate with its own output line, and with
    them whether gump can compute.
    **Third push, 2026-11-15** (CLAIMS SG12–SG15; notebook "the third signals push" and "the third signals push
    reviewed"; `research/audit/REVIEW-signals-3.md`): no emitter, no corner, no clock of period 4N was found. The
    clock's left cap swallows every word of pulses and keeps no trace (proved, reviewed). The counter wall 8|C counts
    isolated pulses and **reflects a double pulse** (two in, one count, one pulse back; oracle, three codes), on a ring
    only: wire 8 burns from a cut end. An emitter of left-going pulses on the end of wire C is a cap that writes a
    periodic, non-constant word, and none of word period 2 to 4 exists near the end of the 3 × 3 tube. Clock periods
    are 4N + 2 because every lone-rake-turning cap in that tube has the same turn constant (measured, and measured
    to carry over into clocks); the eight caps of the other class one tube size up destroy themselves in the turn.
    Sharpened questions: **(a)** an emitter outside what was excluded: word period ≥ 5, wide pulses, emitters of
    moving objects, emitters beside a wire, other wires; **(b)** a cap of the other turn class that survives a turn
    (a clock of period 4N); **(c)** a proof that the in-clock turn constant equals the lone one, and the invariant
    that fixes it; **(d)** a corner: one scan of 205 placements of a second wire beside a lit clock found nothing,
    and no other search exists; **(e)** a cap for wire 8 (a free-standing second counter); **(f)** whether the
    double-pulse reflection can be made into a shuttle or a reusable reflector.
    **Fourth push, reviewed 2026-11-15** (notebook "the fourth signals push reviewed"; CLAIMS SG16–SG22;
    `research/audit/REVIEW-signals-4.md`): question (a) is answered for moving objects. A 15-cell standing gun of
    period 4 writes a rake onto bare wire every period; gun, wire and receiver make a free-standing oscillator at
    every length (proved); the catalogue oscillator C8.24a beside the stream turns every second rake into a hole
    and is not changed (the divider, period 8); every word of holes heals. Still absent: anything that reads the
    word; a second stage (a second divider on the halved stream never divides again); a clock of period 4N; a
    corner (never searched). New questions: **(g)** a reader: a standing object left in a different lasting state
    by a hole than by a rake (a wall that moves per hole, an absorber with two states); **(h)** a switch: the
    divider works at one of the oscillator's eight phases and one cell on the wire at the right moment destroys
    it, so is there an input that shifts its phase or place without destroying it; **(i)** a divide-by-four, or
    any word other than rake, hole (oscillators of period 24 and 32 beside the stream, enumerated and not
    sampled); **(j)** a corner as an exact constraint problem, with the stream as a standing probe; **(k)** why
    the turn class is forced (no invariant is known; the negative is bounded by turn time T ≤ 36).
    **Fifth push, reviewed 2026-11-15** (notebook "the fifth signals push" and "… reviewed"; CLAIMS SG23–SG27):
    (g) was asked directly and the answer within bounds is no: among 741 ends of the stream in the 3 × 3 tube,
    599 heal every word of holes and 142 are destroyed by every word; over every one-unit change of an arriving
    rake no end is left alive and changed; beside the stream (samples) a gap heals or destroys. Two things are
    new. A second one-cell signal (K0) rides the stream, and 503 of the ends tell it from a hole by dying of one
    and not the other. And the receiving cap with a catalogue oscillator beside it answers a hole with an
    **echo**: a three-cell signal sent back up the stream through the oncoming rakes, the end restored; it kills
    the gun when it arrives. New questions: **(l)** what an echo and a hole do when they meet, at every phase
    (the gate question); **(m)** a gun that survives an echo, by absorbing it or by returning a hole, and then a
    signal that goes round between two ends; **(n)** what about the cap and its neighbour makes the echo, and a
    simpler reflector (no bare end of the 741 echoes anything); **(o)** the "wall" outcomes, in which a gap at
    the end converts the stream into a different uniform wire behind a moving front: what wire, and is the front
    a signal; **(p)** a listener is still not known: the bounds are the 3 × 3 tube, periods 4 and 8, one-unit
    events, and samples beside the stream.
    **Sixth push, reviewed 2026-11-15** (notebook "the sixth signals push" and "… reviewed"; CLAIMS SG28–SG32):
    (l) is answered: the stream carries at least nine rigid signals (three up, six down); opposite-moving ones
    never pass: U and K0 cancel exactly, E or U against a hole turns the stream into wire B for ever, E against
    K0 punches every rake. (m): no gun survives an echo within bounds, whatever it may send back; eleven guns
    absorb U. (n): the reflector couples through one cell and works once; no bare end in the tube answers. New
    questions: **(q)** the full meeting table of the nine signals (N1 to N4 are untested), and whether the list
    of signals is complete; **(r)** a count that lasts: an echo against a word of holes writes one unit of wire
    B′ per hole, but only inside a stream that is being converted; is there an end for the spreading edges of
    wire B (something that stops the conversion and stands), which would make that count a record; **(s)** a
    safe up-channel: U is absorbed by eleven guns and cancels K0 exactly, so an end that answers with U instead
    of E would give a wire that survives being answered (none inside the tube for a hole at C ≤ 35; beside the
    tube untried); **(t)** period 8 and the 5 × 5 tube at both ends, where every negative here stops.
14. The 94 clockwork objects (`research/clockwork/objects/`) are not merged into the atlas catalogue.

## Neighbouring rules

15. B45/S3457 (lifetimes ×100 per radius step) and B45/S3456 (glassy freezing): does the face law, with another
    constant, hold there?

15b. The edge-neighbour rule (what the owner intended in 2012; gump is the rule as coded, with corner-touching coplanar
    neighbours): quick tests show box confinement, bulk chaos at density about 0.40, steeply size-dependent lifetimes
    and a staircase. Nothing fitted or audited. Does the area law hold on a box face, and with what cost per site?
    Off main on purpose: branch `claude/edge-neighbour-tangent`, `research/tangents/edge-neighbours/README.md`.
    **Answered 2026-11-14** (`research/audit/REVIEW-class.md` §2, under the name face12e): yes, with 0.41 per wall face,
    which is 0.205 per cell of the layer that dies (gump: 0.212, the area-only slope of slab faces of mixed widths
    over A = 27–75, `research/theory/class.md`; within one width family it is 0.207, CLAIMS GP9). Open now: why those two numbers nearly agree;
    symmetric seeds; boxes beyond 6³.

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
