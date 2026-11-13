# Status (overwritten as things change; history is in git and NOTEBOOK.md)

_Last updated 2026-11-13 by the lead._

## Built and verified
- `reference/` oracle — matches the original's logs, sides 8–12 (13 via the engine on the legacy torus).
- `engine/` — Rust, bit-exact vs oracle and all legacy logs; ≈4×10¹⁰ cell-updates/s/core.
  Round two: `gump show` (text renderings, kagome layers), `png`, `describe` (re-derives all 1,307
  atlas objects), packed ensembles (≈4× for small boxes), `--sym` symmetric soups. Not built: a
  symmetry-reduced stepper (would buy closed cubes beyond side 16).
  Round three: `--sym` torus soups fixed, `ensemble --layer-deaths` (exact peel times),
  `gump occupancy` (time-averaged maps), `--checkpoint` for restartable runs.
- `web/` v1 — WebGL2 bit-packed stepper + three.js views; 49/49 tests.
- `research/atlas/` — exhaustive still lifes ≤16 cells, oscillators, vertex star, legacy ash, critical thickness.
- `research/peeling/` — the face law, cuts, symmetric effective area, account of the cube series.
- `web/` rounds two and three — kymograph, `{111}` slicer, editor, atlas gallery, guided tour, static build.
- `research/phase/` — the chaotic state as a phase; 960-rule survey (`research/figures/phase_rulemap.png`).

## In flight (2026-11-13, late)
- A usage limit stopped every agent at about 20:00 UTC on 2026-11-13. State left behind:
  - `research/theory/class.md`: the class agent had finished ("final" in its last commits). Not yet checked by
    the lead or attacked by a second agent.
  - `research/theory/exponent/`: the exponent agent was stopped before writing its report (`exponent.md` is a
    stub). Its forecasts and outcomes are in `exponent/PREDICTIONS.md`, its theorems in `exponent/theorems.md`
    (Lemma A, consequence (c) there is false: swarm board E10). Needs a successor to write it up, then checking.
  - `research/audit/gpu_pr8/`: partial scripts from the reviewer of pull request 8; no review written. Restarted.
- `research/theory/swarm/` (relaunched about 22:05 UTC at the owner's word): four Fable solvers (`probability`,
  `counting`, `path`, and from about 22:20 `source`), a librarian (`library/`: primary papers read, theorems as stated) and a critic on one problem, the area law, by mathematics alone. Problem and rules in
  `swarm/PROBLEM.md`; results in each `journal.md` and `claims.md`; the critic's map is `swarm/critic/board.md`
  (its first pass already corrected several numbers the lead had been quoting: read E1–E11). The lead drives the
  rounds (`LEAD.md`, "The swarm"). Nothing in it is established until a fresh reader has audited it.
- GPU session "Modal API" (see `LEAD.md`): pull request 8 reviewed and merged 2026-11-13 (notebook entry; review in
  `research/audit/REVIEW-gpu-pr8.md`; corrected reading at the top of `research/gpu/README.md`). The fixes the review
  asked for arrived as pull request 10 and are merged (lead spot-checked the diff). Asked next: slab faces at A > 90, octahedral faces at A ≥ 165,
  a longer cube-centred symmetric run (does the death rate really fall with age?).

## Next (lead's list; pick by judgment)
- Lineage study is in (notebook 2026-11-13, `research/lineage/`): cube-like seeds wait like soups at R ≤ 38. Open from it:
  replicate the weak "slow variable" (copies remember their source, ρ ≈ +0.2) on other sources; side 16's own sizes
  (vertex-centred R ≥ 40) need the GPU session.
- Check each report above independently before recording it (see `LEAD.md`, "Resuming").
- Have a fresh agent try to break the two Fable agents' claims once they land.
- Full web test suite has not been re-run since the tour text edits of 2026-11-13 (tour tests pass).
- Put the 2D toy in the web viewer/tour if it becomes the paper's lead example.
- Papers (PROGRAM, "Writing it up"): not started; the owner decides venue, authorship and disclosure.
- Pages deployment still needs the owner: Settings → Pages → Source "GitHub Actions".

## The storyline so far
1. Birth cannot cross a `{111}` plane (T2) ⇒ finite seeds are trapped in octahedral hulls; no
   spaceships. Measured front speeds into vacuum: 0.177 cube/gen on {100}, 0.165 on {110},
   exactly 0 on {111} — the octahedron is the growth shape.
2. The lattice is an ABC stack of kagome layers; ≥3 layers are needed to sustain chaos.
3. The chaotic state is a genuine phase: bulk density **0.4155** (tori of any size), isotropic,
   correlation length ≈0.7 cube, damage spreads as a sphere at ≈0.85 cube/gen. Mean field
   alone gives a 4-cycle; a small neighbour–neighbour correlation stabilises it.
   **O_h-symmetric seeds are different**: cells on mirror planes are depleted (≈0.31), so
   symmetric octahedra run at ≈0.39. Every legacy cube run is of this kind.
4. Chaos is metastable and dies only by irreversible `{111}` events, each a rare, sudden,
   memoryless collapse whose cost is exponential in the number of cells that must die:
   - **a face layer goes extinct (peeling)** — mean wait τ_face ≈ exp(−0.09 + 0.209·A)
     generations, A = sites in the outer layer; one line over six decades for flat slab
     faces, octahedral faces (≈1.7–1.9× tougher), symmetric soups and the closed cubes
     (`research/figures/peel_face_law.png`; independently re-checked by the lead,
     `research/experiments/face_endgame_check.py`: −ln h/A = 0.2183 at A = 45, engine only);
   - **an interior 3-layer firewall** — ≈0.12 per cell of the band (≈0.36 per unit of
     cross-section), so it wins only where a cross-section is much smaller than a face:
     thin slabs (crossover at thickness ≈ width), never octahedra;
   - the bulk without faces (whole torus) is effectively immortal above ≈600 cells.
   **Symmetry is fatal**: an O_h-symmetric state has one fundamental domain of independent
   chaos (regions die in lockstep), effective face area A/7.7. The side-13 cube lasts ~10⁵
   generations because it is symmetric; the same hull filled asymmetrically would hold each
   face ~10⁴¹ (the face law extrapolated fivefold in area; not measured). The legacy cube lifetimes n = 11–15 fall at unremarkable quantiles of the law's
   prediction. **n = 16 was predicted at 2.4×10⁸ (90%: 3.9×10⁷–6.3×10⁸) and lived
   2,919,617,676** (first face 2.36×10⁹, second 5.2×10⁸; ends as 12 × S8b on the axes;
   `research/data/cube16_*`). What was wrong: the cost per site in a symmetric face rises with
   face size, so "A/7.7" under-predicts beyond its fitted range; cube-centred O_h faces follow
   ln τ ≈ 0.69 + (0.209/6)·A − 0.195·√A to A = 693 (`research/fluct/sym_fit.py`), and
   vertex-centred ones (even cubes) are ≈1.5× tougher (A = 360–630; 2.0 ± 0.4 at A = 693 for fresh soups only; `sym_fit.py` prints 2.39 when the cube's own copies are pooled in).
   **Face death is the stationary tail, measured to one cell** (`research/fluct/README.md`):
   ln P(n = k) is straight down to k = 1, the death rate is its next point (h ≈ 0.6·P(n = 1)),
   62% of deaths are from a single cell, the usual 3-cell ember is one kagome triangle;
   −ln h/A → 0.2077 ± 0.0014 + 0.55/A [retired 2026-11-13: the fit missed its own data; measured local
   slopes rise to 0.221 at A = 135, limit unknown]. Path-splitting (FFS) does not help: the plunge takes
   ~10 generations. Brute force on an O_h orbit-reduced stepper (`research/fluct/fl.c`) does.
5. Debris is built from a small fauna: cubes, kagome hexagons, vertex stars (a sealed
   12-cell universe), hinged period-2 flippers, and rare clockwork up to period 66.
   **Long periods are short loops closed by a symmetry of their own box** (period = twist ×
   loop, twist ∈ {2, 3, 4, 6}): P66.27a = 2 × 33 (mirror), C48.24a = 6 × 8 (a screw),
   C36.33a = 4 × 9. Twisted loops are a steady 3–8% at every loop length, so the twist
   multiplies rather than selects; the longest plain loop is 35. Compound objects (249 of
   9,700 in the box census) are non-communicating sub-clocks on one frame
   (`research/clockwork/README.md`; notebook 2026-11-13).
6. In rule space (960 rules, B ⊆ {4..7}, S ⊆ {2..7}) torus chaos is common, but long-lived
   *confined* chaos is not, and gump is a **minimal** member of that region: remove any one
   count from B45/S345 and lifetimes collapse; add S2 or S7 and they grow ≥29× (those medians sit at the 10⁵ cap).

## Most recent
- PR #1 merged to main (everything above). The lead measured the fluctuations of living faces
  (`research/experiments/face_fluct.py`): the face law's 0.209 looks like the value at zero of
  a size-independent large-deviation curve (≈0.20 by extrapolation) — notebook, last entry.

- Side 16 is finished (2026-11-13). Forecasts from perturbed copies of the running cube
  (`research/fluct/PREDICTIONS.md`): first peel hit (median 2.2×10⁹, actual 2.362×10⁹);
  second peel missed by the clone run (mean 7×10⁷ confirmed three ways, actual stay 5.2×10⁸)
  and caught at the 95th percentile by the fit-only forecast. Side 17 is forecast at a
  first-plateau mean of 2.6×10¹⁰ (not run).
- **Open question, not a finding:** side 16's largest plateaus ran 2.8, 7.4, 2.6 and 1.2 ensemble means. The
  "over-dispersion, P ≈ 0.01" over cubes 13–16 (`research/experiments/cube_vs_ensemble.py`) is post hoc — it
  includes the side-16 plateaus that suggested it; sides 13–15 alone give P ≈ 0.18 (audit, finding 1). The
  proper test is on fresh lineages: `research/lineage/`, and the GPU session's experiment 1. Hull radius 42
  itself is an ordinary size (fresh soups: τ = 7.1×10⁸, 45 deaths).
- `research/fluct/qsd.py` is unreliable for symmetric soups below R = 30 (settled debris
  counted as a living face); use the engine there.
- Clockwork study done (2026-11-13): 94 new oscillators in `research/clockwork/objects/`
  (ids `C<period>.<minpop><letter>`, not merged into the atlas catalogue); 22 of them are
  compound. Open: periods beyond 66 via 4- or 6-fold boxes; anything that carries a signal.
- Open: the asymptotic symmetric slope (is it exactly 0.209/6?); whether 0.208 per site
  holds for asymmetric faces beyond A = 84.

- 2026-11-13: prior-art survey and adversarial second pass (`research/PRIOR-ART.md`): no automaton on this
  lattice found, no lifetime-versus-symmetry result found; cite Eppstein (arXiv 0911.2890) for confinement.
  Open problems consolidated in `research/OPEN-PROBLEMS.md`. Theory programme started
  (`research/theory/PROGRAM.md`); first result, the threshold lemma: gump is a symmetric threshold automaton
  except at overcrowded cells (n ≥ 6), so all non-period-2 behaviour needs overcrowding.

## Ideas not yet started
- Web: a gallery of atlas objects; a guided tour of the storyline.
- A write-up for humans (and one for agents) once the peeling law is quantitative.
- Side 17 closed cube (forecast written down; days on the engine, or a single-state
  symmetry-reduced stepper — `fl.c` is fast only for 64 states at once).
- B45/S3457 ("super-gump": ~100× lifetime per radius step) and glassy B45/S3456 as rules worth their own look.
