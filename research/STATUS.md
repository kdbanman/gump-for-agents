# Status (overwritten as things change; history is in git and NOTEBOOK.md)

_Last updated 2026-11-14 by the lead._

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
- **Pause lifted, 2026-11-14.** The owner, after the overview page: "pass me a prompt for the compactor … so you can pick up
  where you left off (and/or head wherever you like next)". The lead reads this as leave to resume by judgment, mindful of
  usage (the pause was for usage). Restarted so far (2026-11-14): one agent, a successor to the swarm's critic, clearing the
  queue at the top of `swarm/critic/board.md` (counting round 2 and its lab requests; the interim rounds of probability, path
  and source). The solvers wait for its replies. Also done since (both finished and recorded, see "Next"): an adversarial review of the GPU
  session's pull request 12 (`research/audit/REVIEW-gpu-pr12.md`), and an adversarial check of
  `research/theory/class.md` (`research/audit/REVIEW-class.md`; its out-of-sample test was the edge-neighbour
  rule, there called `face12e`). Everything else below is still the state at the pause.
- **PAUSED at the owner's request (usage), 2026-11-13 about 23:55 UTC.** (Lifted 2026-11-14, see above.)
  Swarm state at the pause: round 1 fully refereed for all four lines; round 2 refereed for path and source;
  counting round 2 written, the critic's reply to it finished or interim (see `critic/to-counting.md`); probability
  paused in round 2 and path and source in round 3, each with an interim report in its journal, unreviewed. The
  librarian is idle with no open requests. To resume: for each solver, a fresh or resumed agent told to read its
  own `journal.md`, `claims.md` and `critic/to-<line>.md`; the critic (or a successor) first, to review the interim
  reports. Agent ids are in the scratchpad notes and may no longer resume; the journals are written for successors.
- `research/theory/swarm/` (relaunched about 22:05 UTC at the owner's word): four Fable solvers (`probability`,
  `counting`, `path`, and from about 22:20 `source`), a librarian (`library/`: primary papers read, theorems as stated) and a critic on one problem, the area law, by mathematics alone. Problem and rules in
  `swarm/PROBLEM.md`; results in each `journal.md` and `claims.md`; the critic's map is `swarm/critic/board.md`
  (its first pass already corrected several numbers the lead had been quoting: read E1–E11; the list now runs to E15). The lead drives the
  rounds (`LEAD.md`, "The swarm"). Nothing in it is established until a fresh reader has audited it.
- GPU session "Modal API" (see `LEAD.md`): pull request 8 reviewed and merged 2026-11-13 (notebook entry; review in
  `research/audit/REVIEW-gpu-pr8.md`; corrected reading at the top of `research/gpu/README.md`). The fixes the review
  asked for arrived as pull request 10 and are merged (lead spot-checked the diff). Asked next: slab faces at A > 90, octahedral faces at A ≥ 165,
  a longer cube-centred symmetric run (does the death rate really fall with age?).

- 2026-11-14: an overview page for the owner (`docs/overview/`, published as a private artifact; link in `LEAD.md`). Refreshed and republished the same day at 11:50 UTC (current to the swarm's close and the exponent study).
  It predates the two reviews of 2026-11-14 (class theory, GPU round two); refresh it when the swarm's exam is in.
- Pull request 11 merged 2026-11-14 07:27 UTC (everything up to the two reviews). Pull request 13 merged 09:55 UTC
  (exam, audit, class revision and follow-up, exponent report, reviews of GPU pull requests 12 and 14). Later
  commits need a new pull request.

## Next (lead's list; pick by judgment)
- **State at 11:30 UTC, 2026-11-14 (after a compaction).** Done since 10:30 and recorded: the exponent study
  (reviewed, corrected, notebook, CLAIMS X1-X3), the swarm's close, the essay section "Coins will do", the second
  revision of `class.md`. **Pull request 16 (GPU: the shape of a periodic face) is merged** (squash bad62e3, 12:05 UTC) after its
  review (`research/audit/REVIEW-gpu-pr16.md`), the lead's re-derivation (`research/audit/gpu_pr16_lead_check.py`)
  and seven text fixes: notebook entry "equal areas, different lifetimes", CLAIMS GP9. Offered to the GPU session as
  optional and only if cheap: about 2,500 face deaths at 5×8×8, which would decide between "offset in the short side"
  (every family 0.2072) and "term in the long side" (b(5) = 0.2081). **The twisted-torus experiment is done, reviewed and recorded** (`research/shape/README.md`,
  `research/audit/REVIEW-shape.md`, notebook entry "the shortest way round", CLAIMS SH1, SH2): at equal area the
  lifetime of a periodic face rises with its shortest closed loop (two independent codes); at A = 60 a second
  variable shows (two tori with the same shortest loop differ by 0.018 ± 0.004). **Running (Opus):** an editor
  applying the review's seven corrections to `research/shape/README.md`; a refresh of the overview page for this and
  pull request 16 (then the lead publishes it). (b) done 11:50 UTC: the overview page was refreshed (9b5dc03: plates for
  face12e, the family, where the exponent lives; the swarm closed; "Open now") and republished to the same private
  link (`LEAD.md`); it does not yet carry pull request 16's width result. Pull request 15 is the lead's open one. **After the owner's Fable reset** (about 9am their time,
  probably 16:00 UTC; Fable was at 0.86 at 11:24, so nothing new on Fable before it): the fresh-reader audit of
  counting and path, and a new theory push on the sharpened problem (the 0.2 per cell from six layers over noise).
- **Swarm: closed 2026-11-14** (`research/theory/swarm/critic/board.md`, closing table at the top; notebook entry
  "the theory swarm is closed"). No proof of the area law and no derivation of the constant. Stands: a deterministic
  relative with an exponential law (audited; CLAIMS SW1); exact reductions and a conditional area law for gump
  (path's P̄ and Theorem Q on a measured hypothesis; one critic, no second reader); the fixed-age theory of soups
  (counting). Exam: five hold, four fail or missed, two undecided, three not run (C-E3, path E4, P-E4). **Owed, and
  worth Fable after the owner's reset:** a fresh-reader audit of counting's and path's proved claims; then, as a new
  effort, the sharpened problem (the constant from five or six layers over noise: transfer matrices at finite depth,
  the committor of the population table).
- **`research/theory/class.md`**: attacked 2026-11-14 (`research/audit/REVIEW-class.md`; notebook entry of that date).
  Its theorems stand; its first clause does not (sealing is a property of a half-space, not a direction), and the
  edge-neighbour rule the owner meant to write in 2012 (there called `face12e`; not gump) turned out to be a gump in a
  box, which class.md as written called unconfined. **Revised 2026-11-14** (commit 569be8d, an Opus successor; all
  twelve items of the review's §5.2 applied; every change listed in the file's last section; the lead read the new
  summary, Theorem A′ with its proof and the change list, and ran nothing). The class is now seven tagged clauses:
  confinement by sealed half-spaces, no finite sealed set, no armoured set, the two-sided drive (all proved; armour
  conditional), whole-wall death and hull lifetimes (measured), and one conjecture; the old fifth clause is withdrawn.
  Two tallies the reviser could not reconcile are flagged in its §10 (26/29 against 23/27 for b/K ≤ 3/8).
  **To do:** run what the repaired clause newly admits and nobody has run
  (kagome8 and hex9 at b = 4; whether bond10's b = 3 boxes ever die; kagome B2/S12 with transverse cuts censored);
  face12e with symmetric seeds and beyond 6³. The owner's quick-look branch `claude/edge-neighbour-tangent` stays
  unmerged; the audited face12e results live in `research/audit/class/` under that name.
- **`research/theory/exponent.md`**: written, reviewed (`research/audit/REVIEW-exponent.md`, 10:45 UTC) and in the
  notebook (2026-11-14, "where the exponent lives"; CLAIMS X1–X3). Stands: five or more layers of gump over coin flips
  reproduce a slab face's lifetime to 0.015 at A = 27–60 and 0.02 ± 0.04 at A = 75 (reviewer's own code), eight rows of the 2D rule likewise (lead's own
  code). Does not stand as written: the empty-window formula as more than a fit, "coincidence", the per-live-cell
  cost, the small-vessel inference. The review's thirteen corrections are applied (commit 0e8e5ec, an Opus editor; its §14 lists every change and two
  inconsistencies in the review itself). To do: update `research/theory/PROGRAM.md` (M1–M4: the problem is now a
  finite-depth probabilistic automaton) and `research/OPEN-PROBLEMS.md` items 3–4.
- **Class follow-up: done 2026-11-14** (`research/theory/class/followup/`; notebook entry of that date; CLAIMS K6–K8;
  the lead re-derived the symmetric face12e boxes). Half-space confinement holds out of sample; hex9 B456/S3456 is a
  new gump-type rule with a concave wall law; bond10's box walls hold each other up along the edges (boxes of 4³ live
  ≈ 10⁹ against 10³ forecast from the slab law); face12e with full cubic symmetry settles in tens of generations.
  **Folded into class.md** (second revision of 2026-11-14, commit 7d4cb8a, an Opus editor; the lead read the new
  clause 6; three small inconsistencies are listed in its last section, among them that the follow-up's and the
  lead's symmetric-box medians differ by one generation, probably a definition of "lifetime"). **Open question it
  raises:** an edge term for box walls (bond10 columns give 0.52–0.66 nats per edge cube; gump's octahedral rim is
  0.84 ± 0.04 nats at A = 108 with the pooled slab value).
- **GPU session:** pull request 12 reviewed 2026-11-14 (`research/audit/REVIEW-gpu-pr12.md`; notebook entry of that
  date). Stands: symmetric soups do not age at R = 43 (Weibull k = 1.02); cube-like seeds at vertex-centred R = 40 wait
  exponentially; rim-free slab faces are on the old line through A = 108, and an octahedral face there is 0.91 nats
  tougher. Does not stand: "the rise is a rim effect" and the slope 0.204 from 108 to 126 (the 6×7×8 run counts
  firewalls as peels; about a fifth of its deaths). The session made the five wording fixes (its commit 3cfab59; the
  lead read the diff) and **pull request 12 was merged 2026-11-14 (time of the merge commit: `git log -1 --format=%cI 07743dd`)**. It is now running the same slab with
  firewalls detected (`research/gpu/fwslab.py`; forecast and two validation targets committed first in
  `research/gpu/PREDICTIONS.md`: firewall-first share 10–30%, ln τ_face(126) = 26.30 ± 0.15). Expect a pull request;
  review it as before (does its validation at 3×6×8 and 4×7×8 reproduce `slab_fw.csv`?), re-derive one number, merge.
  At about 07:50 UTC the session was idle (its runs were due about 07:45); the lead messaged it: restart its branch from
  main, score the run against the forecast, data per death in `research/data/gpu_facelaw/`, censor every period,
  then a control at 6×6×8 with the firewall channel resolved. It cannot reply: look at its branch
  `claude/awesome-cray-boq9vz` and the pull request list from time to time.
  **Pull request 14 merged 2026-11-14, 09:50 UTC** (firewall-resolved slabs; review `research/audit/REVIEW-gpu-pr14.md`;
  notebook entry of that date; CLAIMS GP8): 6×7×8 face 26.405 ± 0.104 (all three forecasts hit), 6×6×8 22.568 ± 0.041,
  slope 108 → 126 0.215 ± 0.006, not decided between a rising cost per cell and a *width* effect (the review's post hoc
  fit with a short-side term). **Running at the GPU session (asked 09:40 UTC):** the pair 4×9×8 against 6×6×8 at
  A = 108 (a width effect predicts 0.23 ± 0.08 lower), and width families s = 3 … 6 at A ≤ 96 with ≥ 2,000 deaths
  each; forecasts first. Expect pull request 16 (15 is the lead's own, opened 09:57 UTC); review as before.
- **Exam (swarm): done 2026-11-14** (`swarm/exam/OUTCOMES.md`; notebook entry of that date; CLAIMS SW2–SW4). Hold:
  path E1 (notched edge 0.346), source S-E1 and S-E2 (faces over dice; six layers suffice for gump), counting C-E1
  (one mirror halves the price, 0.1026 per cell). Fail: counting C-E2, path E3. Undecided: P-E1 (0.512 ± 0.012 on its
  refutation line 0.51; needs about 3.5 core-hours more at L = 38), path E2. New entries filed by the solvers since
  and not yet run: C-E3, path E4, P-E4.
- **Prior art:** Tél–Lai 2008 and Bramson–Neuhauser 1994 are unread (publisher pages refuse agents); the owner was
  told they could fetch them. `PRIOR-ART.md`'s older sections still hold "snippet only" items the library now covers.
- Lineage study: replicate the weak "slow variable" (copies remember their source, ρ ≈ +0.2) on other sources.
- The web viewer still quotes the flat-face law exp(−0.09 + 0.209·A) (`web/src/layers.js`, `main.js`, `tour.js`):
  true for slab faces at the sizes measured; octahedral faces cost up to 0.221 per cell. Decide whether to say so.
- Full web test suite has not been re-run since the tour text edits of 2026-11-13 (tour tests pass).
- Put the 2D toy in the web viewer/tour if it becomes the paper's lead example.
- Papers (PROGRAM, "Writing it up"): not started; the owner decides venue, authorship and disclosure.
- Pages deployment still needs the owner: Settings → Pages → Source "GitHub Actions".
- Not yet answered by the owner (asked once, in passing): which 2D rule and neighbourhood they found years ago.

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
- **Open question, not a finding:** side 16's largest plateaus ran 2.8, 7.4, 2.6 and 1.2 ensemble means (the 7.4 is against
  the pooled 7.1×10⁷, which includes the cube's own copies; against fresh soups alone, 8.6×10⁷, it is 6.1). The
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
