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
- **S5 [proved; proof below, to be audited] The threshold lemma.** Gump is a symmetric threshold automaton with one
  exception. Let n be a cell's live-neighbour count and x its state. The *uncapped* rule "alive next iff n + x ≥ 4"
  (birth at ≥ 4, survival at ≥ 3) is a threshold network with symmetric weights, so by the Goles–Olivos argument it
  has the non-increasing energy E(t) = −Σ_{i~j or i=j} x_i(t) x_j(t−1) + 3.5 Σ_i (x_i(t) + x_i(t−1)), which drops by
  ≥ ½ for every cell with x(t+1) ≠ x(t−1). Hence it reaches period ≤ 2 within O(N) steps. Gump differs from it
  exactly at *overcrowded* cells (n ≥ 6, where gump says dead). So:
  **(a)** any orbit of gump with no overcrowded cell from some time on has period ≤ 2;
  **(b)** every oscillator of period ≥ 3 has an overcrowded cell at some phase;
  **(c)** along any gump orbit, ΔE ≤ −½·#{cells with x(t+1) ≠ x(t−1), not overcrowded} + Σ_{overcrowded i, x_i(t−1)=1} (n_i + x_i − 3.5).
  Energy enters only at overcrowded cells. *Chaos is sustained overcrowding; without it the rule is a gradient flow.*
  Checked (`python3 research/theory/check_threshold.py`): all 329 catalogued objects of period ≥ 3 have an overcrowded
  cell; the uncapped rule on 80 soups (hulls of 264 and 876 cells) always freezes, in ≤ 8 steps.
  *Ways on:* audit the proof and the citation; turn (c) into bounds (how much overcrowding does sustained activity
  need per unit volume?); measure the overcrowding rate in chaos, at a dying face, in debris, as an order parameter.
- **S6 [open] Critical thickness as a theorem.** Measured: one or two `{111}` layers cannot sustain activity, three
  can. In one isolated layer a cell has ≤ 6 neighbours, so it is overcrowded only when completely surrounded — the
  energy budget (c) may be enough to prove freezing outright. Two layers: ≤ 8 neighbours. A proof would make
  "a vessel too thin for chaos" rigorous, and with the skeleton give a *definition of debris by geometry*.
- **S7 [open] General confinement.** For which lattices, neighbourhoods and rules does "a dead cell sees fewer live
  cells across a plane than birth needs" hold, and what hull shapes result? Relation to Eppstein's classification
  (`PRIOR-ART.md`; his proof still needs reading). A clean general theorem is paper material on its own.
- **S8 [open] Periodic patterns in the large.** Densest still lifes; space-filling periodic textures; whether a hull
  of any size can be filled by a periodic state with all faces occupied; growth rate of the number of still lifes.

### D — definitions to try

- **D1 Debris by dynamics:** eventually free of overcrowding (then period ≤ 2 by S5) — misses the clockwork.
- **D2 Debris by geometry:** every component of the skeleton's complement is too thin to hold chaos (needs S6).
- **D3 Chaos by damage:** a single flip's damage spreads linearly (measured 0.85 cube/gen); debris heals or confines it.
- **D4 Chaos by measure:** locally typical for a shift-invariant, mixing invariant measure on the infinite lattice
  (density 0.4155). Existence of invariant measures is free; uniqueness and mixing are the hard part everywhere.
- Worth knowing which of these agree on the data we have, and where they part (compound clocks, P66, firewalled blocks).

### M — metastability (why chaos ends, and how fast)

- **M1 [measured] The face law** and its end-game: death rate ≈ 0.6 × P_qs(one cell left); ln P_qs(k) straight in k.
- **M2 [open] A conditional theorem:** exponential decay of correlations in the quasi-stationary state ⇒ a large-
  deviation principle for the face's population ⇒ exponential-in-area waits. States exactly what is assumed.
- **M3 [open] Noisy gump.** With independent deaths at rate ε, mean wait ≤ ε^(−A) trivially; a matching lower
  bound would be a contact-process-style contour argument. Is the deterministic constant 0.208 the ε → 0⁺ limit of
  anything? Does a little noise change lifetimes smoothly?
- **M4 [open] Derive 0.208.** Local-structure (correlated mean-field) approximations of the stationary state, then
  the cost of emptying a face; or a one-cluster birth–death model for the last cells (ratio 0.65 per cell).
- **M5 [open] The symmetric collapse:** six lockstep domains minus a mirror-line term; the even/odd factor 1.5.
- **M6 [in progress] Are single lineages memoryless?** `research/lineage/`.
- **M7 [open] Firewall formation** (≈0.12 per cell) in the same language as faces.

### E — end states (what is left)

- **E1 [measured] The ash census** (`research/atlas/`): what a typical seed leaves. No theory of its composition.
- **E2 [heuristic] Random map with killing.** Treat chaos in a vessel of N cells as a random map killed at rate
  1/τ: ≈ τ states on immortal cycles; a seed reaches one with probability ~τ²/2^N. Testable in small vessels, where
  it should also predict the *clockwork*: periods, counts and basins of long oscillators (with the twist lemma as
  the birthday paradox modulo symmetry). Links E to M and to `research/clockwork/`.
- **E3 [open] Why does side 15 go extinct and side 16 leave twelve S8b?** What the final collapse selects.

### G — generality (is any of this about gump?)

- **G1 A 2D toy.** Moore-neighbourhood rules with no birth below 4 are confined to their bounding box. Is there
  one with long-lived confined chaos that dies edge by edge? Edges of length L instead of faces of area A: cheap,
  exhaustive at small sizes, easy to draw. If the area law, the straight tail and the symmetric collapse all
  reappear, the phenomenon is a class, and the 2D case is where proofs should be tried first.
- **G2 Neighbours of gump** (B45/S3457, B45/S3456; the 960-rule survey): which statements survive?
- **G3 Capped-threshold rules as a family:** S5 holds for any rule of the form "threshold with hysteresis, plus an
  upper cap", on any graph. How much of gump's behaviour is a property of that family?

## Writing it up (when there is enough)

Candidate papers, roughly independent: (1) the automaton and its structure theorems (S1–S7, fauna, twist lemma);
(2) the metastability study (M1, M5, forecasts and their failures, the tail measured to one cell); (3) chaos versus
debris proper, if S5–S6, D and E2 come together. Venue, authorship and how agent work is disclosed are the owner's call.
