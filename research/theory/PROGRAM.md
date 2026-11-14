# Theory programme: chaos, debris, and the passage between them

*Started 2026-11-13 by the lead, at the owner's invitation. This is a web of goals, not a plan: nodes, what each
would buy, and ways in. Work on whatever node you can move; add nodes; record dead ends here too. Results go in
this directory (one note per result) and, once checked, in `research/NOTEBOOK.md`. Tags as in the notebook.*

## The question

Every finite seed of gump is trapped in a finite hull and so ends periodic. Empirically it does so in two acts: a
long, statistically steady **chaos**, then a sudden collapse to small **debris**. Life and many other rules show the
same thing and nobody can say precisely what the two words mean, let alone prove one leads to the other. Gump has
unusual rigid structure (T1–T4 in `docs/AUTOMATON.md`), which may make it the place where this can be done.

Aim: definitions of *chaos* and *debris* under which (i) they are provably distinct, (ii) "chaos ends" is a theorem
or a sharply stated conjecture with a rate, (iii) what remains is characterised. Partial results are worth having.

## What gump gives us that Life does not

- **An exact irreversible coarse variable.** Call the set of empty `{111}` layers that can never be refilled (outside
  the hull, or inside a 3-layer firewall) the *skeleton*. By T2 and T3 it only grows. A run is therefore a finite
  chain of skeletons, with ordinary dynamics inside a fixed vessel between changes. Lifetime = sum of residences.
- **An exact local reason for confinement** (3 < 4), so boundaries are sharp and events (a face dying) are well defined.
- **Finite vessels**, so everything is decidable by running it, and small cases can be done exhaustively.

## Nodes

### S — structure (provable now)

- **S1–S4 [proved]** T1–T4; the twist lemma (period = loop × order of closing symmetry).
- **S5 [proved; audited] The threshold lemma** (`threshold.md`). In a finite vessel, gump is the symmetric
  threshold rule "alive next iff n + x ≥ 4" except at *overcrowded* cells (n ≥ 6, where gump says dead). With the
  Goles–Olivos energy E(t) = −x(t)ᵀ(A + I)x(t−1) + 3.5(|x(t)| + |x(t−1)|): the uncapped rule reaches period ≤ 2
  within 26N + 1 steps; for gump **ΔE = D − Q exactly**, with dissipation Q at ordinary cells and drive D only at
  overcrowded cells that were alive two steps before (O1 events). So no O1 events ⇒ period ≤ 2; on any cycle drive
  equals dissipation; every oscillator of period ≥ 3 has O1 events. *Chaos is sustained drive; without it the rule
  is a gradient flow.* Measured: O1 rate 0.115 per cell per generation in bulk chaos, 0.035 at a face about to die,
  0 in period-≤2 debris. False for infinite configurations. Primary citations still unread.
  *Ways on:* is there a critical drive rate below which activity cannot persist (a proof would be a rigorous
  "debris" criterion)? Does the drive rate at a face predict its death better than its population does (M1)?
- **S6 [proved, in a different form than hoped] Why three layers** (`thickness.md`). A set is *sealed* if each of
  its cells has ≤ 3 neighbours outside it; a dead sealed set stays dead whatever happens elsewhere, and the largest
  one, K(t), only grows — the skeleton, made exact. Finite sealed sets exist in one layer (6 cells) and two (36);
  **in three or more layers and in 3D none exists**, so in a hull every sealed set touches the outside. The hoped-for
  "one layer always freezes" is false: one-layer oscillators of periods 3–12 exist.
  *Open:* thin slabs lose chaos because the unsealed region stops percolating (stated precisely in `thickness.md` §4;
  a computer-assisted proof looks possible). And in ≥ 3 layers: bound how fast a face-touching sealed set can grow.
- **S7 [proved in part, 2026-11-14] General confinement.** A half-space is sealed iff no cell outside it has b
  neighbours inside (`research/audit/REVIEW-class.md` Theorem A′, correcting `class.md` Theorem A for several cell
  types); a positively spanning family of sealed half-spaces confines. Open: the converse (does an unconfined
  capped threshold always have unbounded patterns?). The original question: For which lattices, neighbourhoods and rules does "a dead cell sees fewer live
  cells across a plane than birth needs" hold, and what hull shapes result? Relation to Eppstein's classification
  (`PRIOR-ART.md`; his proof still needs reading). A clean general theorem is paper material on its own.
- **S8 [open] Periodic patterns in the large.** Densest still lifes; space-filling periodic textures; whether a hull
  of any size can be filled by a periodic state with all faces occupied; growth rate of the number of still lifes.

### D — definitions to try

- **D1 Debris by dynamics:** eventually free of overcrowding (then period ≤ 2 by S5) — misses the clockwork.
- **D2 Debris by geometry:** the unsealed region V \ K(t) consists of pockets too thin to hold chaos. Exact
  objects now exist for this (S6); what is missing is the percolation step.
- **D1′ Chaos by drive:** a positive rate of O1 events per cell (S5). Cheap to measure, and zero on period-≤2 debris.
- **D3 Chaos by damage:** a single flip's damage spreads linearly (measured 0.85 cube/gen); debris heals or confines it.
- **D4 Chaos by measure:** locally typical for a shift-invariant, mixing invariant measure on the infinite lattice
  (density 0.4155). Existence of invariant measures is free; uniqueness and mixing are the hard part everywhere.
- Worth knowing which of these agree on the data we have, and where they part (compound clocks, P66, firewalled blocks).

### M — metastability (why chaos ends, and how fast)

- **M1 [measured] The face law** and its end-game: death rate ≈ 0.6 × P_qs(one cell left); ln P_qs(k) straight in k.
- **M2 [open] A conditional theorem:** exponential decay of correlations in the quasi-stationary state ⇒ a large-
  deviation principle for the face's population ⇒ exponential-in-area waits. States exactly what is assumed.
- **M3 [open] Noisy gump.** With independent deaths at rate ε, mean wait ≤ ε^(−A) trivially; a matching lower
  bound would be a contact-process-style contour argument. Is the deterministic constant (≈ 0.21) the ε → 0⁺ limit of
  anything? Does a little noise change lifetimes smoothly?
- **M4 [open] Derive the constant (≈ 0.21; first quoted as 0.208).** Local-structure (correlated mean-field) approximations of the stationary state, then
  the cost of emptying a face; or a one-cluster birth–death model for the last cells (ratio 0.65 per cell).
  **Sharpened 2026-11-14** (`research/theory/exponent.md`, reviewed; notebook of that date, "where the exponent
  lives"; the swarm's exam S-E2): the constant is a property of five or six layers of the rule over independent coin
  flips. A face with w ≥ 5 layers on the rule and fresh Bernoulli cells beneath has the deterministic slab's
  lifetime to 0.015 in ln τ (A = 27–60). So M4 is now a question about a probabilistic cellular automaton of finite
  depth: exact at small sizes (transfer matrices, as the swarm's lab did for one row), samplable at large ones
  without the bulk, and open to the tools of M3 (it *has* noise). Not derived: the constant itself. What was tried
  and fell: mean-field large deviations, a Gaussian, a single driven row (all off by 20–50%), the empty-window
  formula as more than a fit, fixed-age exponents (the swarm's counting line), "ln τ = A·∫θ" (path). What stands
  as theorems: the swarm's conditional results (`swarm/critic/board.md`, closing table) and a deterministic
  relative with an exponential law (CLAIMS SW1). The number itself is not fixed either: 0.2088 on slabs to A = 90
  (mixed widths; 0.2072 within a width family), 0.215 ± 0.006 from 108 to 126, 0.216–0.221 on octahedral faces.
  Width moves it (CLAIMS GP9: at equal area a narrower periodic face dies sooner); whether the cost per cell of a
  wide face also rises with area is not decided (0.2072 against 0.2117, GP9).
- **M5 [open] The symmetric collapse:** six lockstep domains minus a mirror-line term; the even/odd factor 1.5.
- **M6 [measured, 2026-11-13] Are single lineages memoryless?** Yes at hull radius 31–38: plateaus of cube-like seeds wait
  like soups and like an exponential (`research/lineage/README.md`; `research/CLAIMS.md` L1). The GPU session's pull
  request 12 extends this to vertex-centred R = 40 (under review, 2026-11-14).
- **M7 [open] Firewall formation** (≈0.12 per cell) in the same language as faces.

### E — end states (what is left)

- **E1 [measured] The ash census** (`research/atlas/`): what a typical seed leaves. No theory of its composition.
- **E2 [heuristic, untested] Random map with killing.** Model: a uniformly random map on M = 2^N states, each step
  independently fatal with probability 1/τ, τ ≪ √M. Then ≈ τ states lie on immortal cycles and a random seed
  reaches one with probability ≈ τ²/M (derivation in `OPEN-PROBLEMS.md`, item 4). Testable in small vessels, where
  it should also predict the *clockwork*: periods, counts and basins of long oscillators (with the twist lemma as
  the birthday paradox modulo symmetry). Links E to M and to `research/clockwork/`.
- **E3 [open] Why does side 15 go extinct and side 16 leave twelve S8b?** What the final collapse selects.

### G — generality (is any of this about gump?)

- **G1 [measured; law checked by the lead] A 2D gump exists** (`research/toy2d/`): B34/S234 on the range-2 cross
  neighbourhood. Box confinement, steady chaos, memoryless edge death with ln τ = 0.73 + 0.416·L, straight tail to
  one cell, T5 and the T6 analogue, symmetric collapse by ½ in the exponent. The Moore neighbourhood is the wrong
  analogue (a line holds too few of its neighbours). *This is now the place to try proofs and exhaustive small
  cases* (M2, M4, E2, S6's percolation step), and the simplest object to put in a paper.
  *Open:* why rotation symmetry that fixes no edge still shortens life; the slope beyond L = 36.
- **G2 Neighbours of gump** (B45/S3457, B45/S3456; the 960-rule survey): which statements survive?
- **G2′ The rule the owner meant to write** (same B45/S345, but the four coplanar neighbours are the edge-sharing
  ones): a quick look says it is a second gump with a box for a hull: confined, chaotic, lifetime climbing steeply
  with box size, dying a slab at a time. Not gump, kept off main (branch `claude/edge-neighbour-tangent`, `research/tangents/edge-neighbours/README.md`).
  It is a fair test for G3 and S7: an example nobody chose to suit the theory. Revisit it when the class is characterised.
  **Done 2026-11-14** (`research/audit/REVIEW-class.md` §2, there called face12e): it is a gump in a box. Walls die whole
  after memoryless waits, ln τ = 6.43 → 14.54 for 16 → 36 wall faces (0.41 per wall face, 0.205 per cell of the layer
  that dies; gump 0.212); boxes 2³…6³ last 10, 60, 439, 9,855, 707,038. class.md as written called it unconfined.
- **G3 Capped-threshold rules as a family:** T5 holds for any "threshold with hysteresis plus exceptions" on any
  graph. Two members now show the whole phenomenon (gump; the 2D cross rule), each the only member of its
  neighbourhood's family that does. What singles them out — the fraction of the neighbourhood lying in a
  confining hyperplane (6/12, 4/8), the threshold near a third, the cap? A statement of the class is open.

## Writing it up (when there is enough)

Candidate papers, roughly independent: (1) the automaton and its structure theorems (S1–S7, fauna, twist lemma);
(2) the metastability study (M1, M5, forecasts and their failures, the tail measured to one cell); (3) chaos versus
debris proper, if S5–S6, D and E2 come together. Venue, authorship and how agent work is disclosed are the owner's call.
