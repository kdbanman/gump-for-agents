# The Gump Map: refresh history (2026-11-14 to 2026-11-15)

*Moved here from `docs/overview/README.md` when the single page became the site (`site/README.md`). It records, per
refresh, which numbers come from data, which are computed on the page and which are typed. Paths below are as they were:
`docs/overview/data/sources/` is now `site/collect/sources/`, `docs/overview/{collect,record_deaths}.py` are in
`site/collect/`, `src/plates-*.html` and `src/figures*.js` are now one file per plate in `site/plates/`, `gump-core.js` and
`signals-core.js` are in `site/assets/`, `check-*.js` in `site/checks/`, and `data/data.json` is `site/data/<key>.json`.*

A visual, text-light summary of the directions and findings, made for the owner on 2026-11-14 while research was
paused. Published as a private artifact (the link is in `LEAD.md`); `index.html` here is what was published.

    python3 docs/overview/collect.py     # data/sources/*.json  ->  data/data.json
    python3 docs/overview/build.py       # src/ + data/data.json + gump-core.js  ->  index.html
    node docs/overview/check-core.js     # the page's stepper against reference/golden (sides 8, 9, 11)
    node docs/overview/check-signals.js  # the live signal objects against the oracle (about a minute; needs python3 + numpy)

- `gump-core.js` is the small JavaScript stepper behind the live run at the top and the ticking clocks. It is
  bit-exact against the three even-sized golden logs; `check-core.js` is the check.
- `data/sources/` holds what five helper agents gathered from the repository that day: `measurements.json`,
  `structure.json`, `project.json`, `swarm.json` (numbers copied out of the repository, each with a `src`), and
  `series.json` (short real runs of the engine made for the figures, each with a `how`). `scripts/` holds the
  scripts behind `series.json`, the fauna verification and `side11.json`; their `how` lines name a scratch
  directory that no longer exists, so point them at a directory of your own.
- The page is a view, not a source. Where it and `research/CLAIMS.md` or the notebook disagree, they are right.
  The swarm section reports what the swarm's files say; none of it has been audited.
- To refresh it after new results: update or regenerate the files in `data/sources/`, run the two commands, and
  republish `index.html` to the same artifact.

## Refresh of 2026-11-14 (afternoon)

Added the plates "The rule you meant" (face12e, which is not gump), "The family" and "Where the exponent lives"
(`src/plates-new.html`, drawn by `src/figures3.js`); rewrote "The swarm" (closed) and "Open now"; added GPU slab
faces at 108 and 126 sites, the slab slope 108 → 126 and hull faces cut by one mirror to the area-law plate, and
the no-ageing tile to "Luck or lineage".

- Every new number comes from `data/sources/update-2026-11-14.json`. Each item there carries the sentence it was
  copied from (`quote`) and where (`src`: the notebook entry of that date, or a CLAIMS row). `collect.py` refuses to
  run unless each quote occurs, whitespace aside, in `research/NOTEBOOK.md` or `research/CLAIMS.md` and each number
  in `value` occurs in its quote. So a quote that is later edited in the notebook breaks the build: re-copy it.
- `collect.py` now also reads the claim counts from the "Counts" line of `research/CLAIMS.md`, and the commit count,
  last commit and merged pull requests (subjects ending "(#N)") from `git`; the milestones of 2026-11-14 are in the
  update file with their commit hashes.
- Typed into the sources, not drawn from data: the lists of what stands and what fell in the swarm plate
  (`figures3.js`, from the notebook entry "the theory swarm is closed") and the text of "Open now" (from
  `research/STATUS.md` as of this refresh: the GPU width experiment is running).
- Not shown: CLAIMS grades per new number (the cards say "one run" or "one agent" where CLAIMS grades it C);
  the per-line round counts of the swarm (stale since the pause, so dropped).

## Refresh of 2026-11-14 (late afternoon)

Added the plate "The shortest way round" (`src/plates-shape.html`, drawn by `src/figures4.js`; placed after the
area law through the `<!--SHAPE-->` marker in `plates-law.html`) from the notebook entries "equal areas, different
lifetimes" (GPU pull request 16, CLAIMS GP9) and "the shortest way round" (CLAIMS SH1, SH2). Revised the area-law
plate (width matters; the old 0.2088 mixed widths; a wide periodic face costs 0.2072–0.2117 per site, undecided; the
slope chart now shows the width-4 and width-5 family slopes and that range as a band), the map, and "Open now" (the
wrap-around term; the fresh-reader audit of path running, per `research/STATUS.md`).

- New numbers come from `data/sources/update-2026-11-14b.json`, checked by `collect.py` exactly as the first update
  file. The six points of the shortest-loop chart are the notebook's table at A = 72, rows copied whole.
- Typed, not drawn from data: the twisted-face picture (4 × 6 against (4,1),(0,6); both are the same a × b block of
  rhombi, glued differently), and the placement of the width-4 and width-5 family lines (A = 60–108 and 75–120,
  from the notebook's table).

## Refresh of 2026-11-14 (evening)

Added the plate "Every torus of a given area" (`src/plates-census.html`, drawn by `src/figures5.js`; placed right
after "The shortest way round" through the `<!--CENSUS-->` marker at the end of `plates-shape.html`), a map entry,
the census forecast (missed), its review in the audit list and a milestone (c9d2596). The shortest-way-round plate's
60-cell tile now shows the four-run pool, 0.014 ± 0.002 (CLAIMS SH2), in place of the first run's 0.019 ± 0.004.

- New numbers come from `data/sources/update-2026-11-14c.json`, checked by `collect.py` as the earlier update files
  (notebook entry "every torus of a given area"; CLAIMS SH2, SH3, SH5). The chart's six points are the notebook's
  48 → 60 costs per cell, copied whole; the rings are the review's own runs (no loop² 13 there).
- Typed, not drawn from data: "three cells around" for loop² 3 and "½" (0.115 / 0.2125 = 0.54), both from the
  notebook's reading of that entry.

## Refresh of 2026-11-15

Added four plates: "Equal area, equal shortest loop", "The thinnest face" and "One price per cell?"
(`src/plates-r15.html`, placed after the census through the `<!--R15-->` marker at the end of `plates-census.html`), and
"Lives that settle unrecognised" (`src/plates-zombie.html`, before "How it is checked" through `<!--ZOMBIE-->` in
`plates-rest.html`); all drawn by `src/figures6.js`. Map entries for the four; the earlier "new" marks removed.

- Sources: notebook entries "is there one asymptotic cost per cell" and its addendum (CLAIMS CN1), "empty patches on a
  face too large to die" (GP10), "the second variable at equal shortest loop: not found" (SH6–SH9), "the thinnest face"
  (TH1–TH6), "lives that settle and are not recognised" (ZL1, ZL2), "prior art, third pass" and "what the adversarial
  review changed", "the counting line's proofs read a second time" and the path audit. Every number is in
  `data/sources/update-2026-11-15.json`, checked by `collect.py` as before; negative values are stored unsigned with a
  `sign`, as the quotes carry a typographic minus.
- The ticking state on the zombie plate is the review's period-16 state (`research/audit/shape3/zombie_1_4_12_p16.txt`),
  lifted to the cubic torus of doubled side 24 by the review's own `geom.py`/`validate.py`
  (`data/sources/scripts/zombie.py` -> `data/sources/zombie.json`) and stepped by `gump-core.js`; three repeats of the
  slab are drawn. `check-core.js` now also checks that the page's stepper returns it to its start after 16
  generations and not before.
- Changed on existing plates: census and shortest-way-round (the second variable is gone by 72 cells; the thinnest
  face's 0.115 is a local slope), area law (a pointer to the joint range 0.207–0.216 for periodic forms), prior art
  (lists replaced by the third pass's "not found" / "not new"; five works added to the reading list), swarm (both
  proof lines read by a second reader), "How it is checked" (eight audits, five forecasts), milestones, "Open now".
- `collect.py`'s reader of the ledger's "Counts" paragraph still matches after today's rewording (124; A 52, B 43,
  C 28, D 1, as `python3 research/audit/claims_tally.py` prints).
- Typed, not drawn from data: the text of "Open now" (from `research/STATUS.md`, state block under "Next", as of
  01:35 UTC: the constant waits on GPU budget, the symmetric-collapse line and the 4 × 5 CPU rerun are running, the
  GPU guard is owed); the two "also known" items kept from the first pass (Eppstein, LifeWiki); the one-line
  summaries of the five added prior-art works and of the eight audits; the year 2017 for Nardi–Zocca (from the arXiv
  number); the last ring step of the thin-face chart drawn over 96 → 108 cells (the notebook's "about 0.103 at 108";
  (15.1644 − 13.9233)/12 = 0.1034); the centring of the island bars (a picture of "shrinks from both ends").
- Not shown: the grades per number (cards say "two codes", "one point being cross-checked", "assumed" where the
  ledger grades B or C or the notebook marks a conjecture); the draft in `docs/paper/` appears only as a milestone.

## Refresh of 2026-11-15 (second)

Revised the symmetry plate (`#sym` in `src/plates-law.html`) for the notebook entry "the symmetric collapse" (CLAIMS
S5–S9, notes on S2 and S3): new headline, the edge-ladder chart (`#f-ladder`, four rungs at A = 63 with both codes, the
inversion point beside the unsymmetric one, the review's values and the rotation, slab, slope × order and centring
numbers in its "Numbers" table), a "what was said / what stands" panel, six tiles, and the fit's key and caption
(the √A coefficient depends on the assumed price; the factor between centrings changes with size). Added to the fauna
plate (`src/plates-fauna2.html` through `<!--FAUNA2-->` in `plates.html`) C52.33a ticking, each cell coloured by its own
period, with a dial for each clock, and tiles for the wires and the five new clocks (entry "what the unrecognised
settled states are"; Z12, Z13). Both drawn by `src/figures7.js`. Map ("new" marks moved to these two), "Open now",
a correction, two forecasts, two audits and two milestones.

- Every number is in `data/sources/update-2026-11-15b.json`, checked by `collect.py` as before. The inversion's
  −0.056 ± 0.023 is the ledger's (S6); the notebook gives the two values only.
- C52.33a's cells are read by `collect.py` from `research/clockwork/objects/C52.33a.cells` (its header must say
  period 52, union 42 and the split {1: 24, 4: 4, 13: 14}). The page finds each cell's period with its own stepper and
  says so on the page if the split ever differs; `check-core.js` checks that the stepper brings the clock back after
  52 generations and not before (to 208) and gives the recorded split.
- Computed on the page, not quoted: the differences between rungs (−2.18, −2.16, −2.12, tooltips and labels) from the
  plotted values; the per-cell periods of C52.33a.
- Typed, not drawn from data: the text of "Open now" (from `research/STATUS.md`, state block under "Next", as of about
  03:20 UTC: the C-row audit running, the 4 × 5 rerun open, the GPU guard owed, the constant waiting); the wording
  "what was said / what stands" (from the entry's own sentences and CLAIMS S7).
- Not changed: the area-law plate's "a mirror through a face halves its price" and the swarm plate's list (CLAIMS SW3,
  a different vessel, grade C). The clock chart ("every saved clock of period 20 or more") does not include C52.33a, a
  compound with no loop.
- Screenshots of the changed plates: `research/scratch/overview/r15b-*.png` (script `shoot-r15b.js` there).

## Refresh of 2026-11-15 (third)

Added the plate "How a face dies, watched" (`#dying`, `src/plates-dying.html` through `<!--DYING-->` after `#death` in
`plates.html`; drawn by `src/figures8.js`) from the notebook entries "how a face dies (the first look, reviewed)" and "a
death is a dip that keeps going" (CLAIMS DY1-DY7; ledger wording where the study README differs). Corrected the
empty-patch chart and tiles on "One price per cell?" for the CPU rerun of the 4 × 5 patch (GP10), the census plate for
the corrected 4 × 4 anchor (GL1; SH3 and SH4 notes), "Open now", the map, a "GTX 1080" tile under "Built", four
milestones, two audits, one forecast, five corrections. Round 3 of the dying-face study is under review: nothing of it
is shown (no `r3_*` table, not `dying_ratefunction.png`); "Open now" only says it exists.

- Quoted numbers are in `data/sources/update-2026-11-15c.json`, checked by `collect.py` as before. An item may now
  carry `file` (a repository path) and is then checked against that file: used once, for the essay's "One of the
  thirteen held" (`docs/WHAT-I-SEE.md`).
- The curves are the study's tables, read by `collect.py` straight from `research/dying/data/`: `r2_excursions.csv`
  (ν and q against depth; checked against the ledger's ln ν at 0.7 and q(0.5)), `occupancy_by_lag.csv` (population
  over its null, lags 0–40), `occupancy_by_cell.csv` (the mean maps, c1 and D2h, null and lags 16, 8, 4, 2, 1, put in the
  films' cell order); `r2_runup.csv` only as a check of the quoted 0.45 and 0.88 at lag 8.
- The eight real deaths: `python3 docs/overview/record_deaths.py` (about two seconds) compiles the study's stepper
  `research/dying/sd.c` unchanged into `research/scratch/overview/deaths/`, runs `oct_11_c_c1` (seed 20261115, 8,000
  generations) and `oct_11_c_d2h` (seed 20261116, 4,000) with soup 0.4, checks every 4, the first four deaths at age
  > 512 of each (not chosen), finds the dying face and the death generation as `research/dying/load.py` does, keeps
  the last 80 generations of its 63 cells (canonical frame of `load.geometry`), and checks every recorded life
  against `reference/oracle.py`: the whole vessel, expanded from the orbit graph, is stepped by the oracle in a padded
  box for 79 generations and must equal the recording at every generation (a flipped cell 39 generations before death
  is caught). Output: `data/sources/deaths.json` (8 KB; frames as base64 bits). `collect.py` checks that each life
  ends on its first empty frame.
- Computed on the page, not quoted: each face's population (from its frames), the point-of-no-return line in cells
  (p* × the ledger's P̄: 0.079 × 31.25, 0.245 × 23.50), "1,249 in 1,250" (1/q(0.5) with q = 0.0008), e^6.5 ≈ 665,
  the largest gap between −ln(νq) and the lifetimes (0.02), the mean populations under the maps (sums of the map).
- Typed, not drawn from data: "Open now" (from `research/STATUS.md` and the notebook as of about 05:40 UTC: A = 93
  running on the GTX 1080, the 5 × 5 anchor to be re-measured there, the guard built and checked on the CPU, five
  corrections owed before the merge of pull request 23, round 3 under review); the GTX 1080 tile; "1 of 13" and "the
  other twelve failed" (from the essay's sentence).
- Screenshots: `research/scratch/overview/r16-*.png` (script `shoot-r16.js` there).

## Refresh of 2026-11-15 (late morning)

Added the plates "Signals" (`#signals`) and "How much of the room a seed sees" (`#statespace`), both in
`src/plates-signals.html` through the `<!--SIGNALS-->` marker after the fauna plate in `plates.html`; brought "How a face
dies" up to rounds 3 and 4 (a block at the end of `src/plates-dying.html`); added the five wrapped faces measured on the
owner's GTX 1080 to "One price per cell?" (a figure row at the end of `#constant` in `src/plates-r15.html`, new headline;
a pointer in the area-law plate's wide-face tile); map ("new" marks on signals, state space, the dying plate and the
constant), "Open now", corrections, forecasts, audits, milestones. All drawn by `src/figures9.js`.

- Quoted numbers: `data/sources/update-2026-11-15d.json`, checked by `collect.py` as before. Sources: NB "gump carries
  signals", "the first signals push reviewed", "a clock of every length…" (SG1–SG10); "how much of its state space a
  seed explores" and "the state-space study reviewed" (SS1–SS3; the reviewed wording replaces the first entry's
  ranges, share and random-map yardstick, which are not shown); "what the dips say…", "a depleted face thins…", "round 4
  reviewed" (DY8–DY15); "five wrapped faces on one driver", "the five tori, reviewed", "the 93-cell torus…" (GL1, GL3).
  A `file` quote may now come from a block-quoted file: `checked()` drops `> ` at line starts (the owner's journal).
- Read straight from the repository by `collect.py`, with asserts against the quotes: `research/signals/objects/`
  (pulse-C, clock-C, gate-C; copied into `data.json`), `research/statespace/data/` (`vessels.jsonl`: per vessel the
  most patient seed's states, the mean seed's and the states with a predecessor, as log2; `large_facelaw.csv` measured
  rows; `large_cubes.csv`; `entropy.json`), `research/dying/data/r4_company.csv` (caught and randomly thinned faces,
  rows with at least 200 faces) and the review's finite-face null `research/audit/dying4/null_r1{1,3,5}.txt` (parsed as
  `research/dying/round4_figure.py` parses it; the bars span p_t 0.45–0.8).
- Live on the page: a pulse of wire C (ring of 20 units, 12 below 520 px), the clock (slider N = 1–12; the page finds
  the period by comparing whole states and prints whether it is 4N + 2), the gate (separations 10 and 11, ring of 24,
  a window of units 2–18 below 520 px; the survivor's direction is read from how its cells move). The layouts are in
  `signals-core.js` (inlined after `gump-core.js`), written to mirror `research/audit/signals_lead_check.py`,
  `signals_clock_lead_check.py` and `signals_gate_lead_check.py`. Only even generations are drawn (the wire's phase);
  cells off the bare wire are orange.
- `check-signals.js` checks exactly what the page uses: pulses B, B-left, C, C-left on rings of 40, 20 and 12 (bare
  wire period 2; the start moved j units after 2j generations, j = 1..60; exactly the defect's cells off the wire); the
  clock for N = 1..12, 16, 17 (unlit period 2; lit cycle of exactly 4N + 2 by whole-state comparison; entry generations
  0, 0, 1, 2, …; compared by hand once with the lead's script at N = 1, 3, 4, 7: equal); the gate on rings of 48 and 24 at separations 6–21 (the
  survivor's run equals the single-pulse run, left at even, right at odd); and, through `python3` and
  `reference/oracle.py`, per-generation hashes of the whole state equal to the page's stepper for a pulse, the clock at
  N = 3 and 4, and the gate at 10 and 11. It also checks that `data.json`'s copies equal the object files.
- Computed on the page, not quoted: the clock's period; the gate's reading; "about 1 in 12" (400 / 33); the state-space
  points (log2 of the study's counts); each wrapped face's and each old forecast's distance from the line
  0.033 + 0.2084·A (the quoted deficits 0.111 and 0.036 are checked against it on the page).
- Typed, not drawn from data: "Open now" (from `research/STATUS.md` as of about 10:50 UTC: the second signals review
  running, a third push started, the card running 81, 84, 108, 111 cells then the 108-cell rimmed face); the map
  labels; "deaths three or four times too rare" and "one nat is a factor e" on the dying plate (the essay); "the GTX
  1080 in your house".
- Not shown: the transmission as a drawing (a tile only); the register, tape, rake and wide pulses as drawings; the
  round-3 dip curves (`r3_*.csv`) and the round-4 void and profile panels; the state-space study's image-after-t panel;
  the first state-space entry's "8–14 / 40–94", "linear, not exponential", "less than chance" and share against a face
  (all corrected by the review).
- Screenshots: `research/scratch/overview/r17-*.png` (script `shoot-r17.js` there: `node shoot-r17.js ids modes`).

- Correction pass after the second signals review (NB "the second signals push reviewed…", SG5–SG10 regraded): new items in
  `update-2026-11-15d.json` (`clock_proof`, `clock_review`, `tape`, `counter`, `soup2`, `soup_read`, `chaos2`, `speed`, `gap`,
  `escape2`), two corrections, an audit and a milestone; the old "under review" quote of SG8 is dropped.
- Signals tiles now say: three empty layers isolate order (T3; two only for the tested capped end); a random unit repeated makes
  a carrier about once in a few hundred, soup proper never yet; destroyed every time over about 2,300 sides, one exception;
  escapes 5 of 200 (reviewer) and 15 of 200 (first agent); the counter has sixteen positions. Header chips and "Open now" say
  both reviews are done; the clock's and the tape's proofs are "checked". Screenshots: `research/scratch/overview/r18-*.png`.

## Refresh of 2026-11-15 (afternoon; the site's phase 2)

Added the plates "What a short way round costs" (`#wrap`, law page, between the thinnest face and "One price per cell?"),
"A gun" (`#gun`) and "A clock that edits the message" (`#divider`, signals page, after "Signals"); rewrote the wrapped-face
figure and tiles of "One price per cell?" for nine faces and "Open now"; two tiles for the third signals push and a reworded
"no corner" tile on "Signals"; four corrections; map tiles for the three new plates. Paths from here on are the site's.

- Quoted numbers: `sources/update-2026-11-15e.json`, checked by `collect.py` as before. Sources: NB "the nine wrapped faces
  reviewed", CLAIMS GL3; NB "the wrapping law tested", CLAIMS WL1-WL3; NB "the third signals push reviewed", "the fourth
  signals push", "the fourth signals push reviewed", CLAIMS SG12, SG14, SG16-SG19, SG22; the essay's "What I would look at
  next" (one sentence, `file` quote).
- The nine wrapped faces are recomputed by `collect.py` from `research/data/gpu_local_eqtorus/eqtorus_*.csv` (ln τ_face =
  ln(2·Σexposure/Σface), error 1/√Σface, all rows of a torus pooled) and asserted equal to the ledger's values to 1.5e-4.
- The wrap plate's faces and frozen forms: `sources/wrap.json`, written by `python3 site/collect/sources/scripts/wrap.py`
  (needs numpy and scipy) from the lead's refit `research/audit/wrap_haz_lead.py` (its loader, the faces of `--single`, its
  LINES/POW/HAZ_FROZEN). The zero line is the weighted line through the 14 faces with no short loop, computed there
  (0.20864 ± 0.00009, asserted within 0.0002 of WL2's 0.2086). `collect.py` checks that the frozen parameters give the
  quoted 84-cell forecasts. **The 84-cell face** (17.3248 ± 0.0058, the lead's run on the tester's runner, rows A = 84 of
  `research/wrap/data/runs.csv`; NB "the 84-cell face with one loop of 12") is in `sources/update-2026-11-15e.json`,
  `wrap.measured84`, and `collect.py` checks it against the recomputed face. With it the plate became "a tube pays less per
  cell the tighter it is wrapped": each girth's own straight line (`wrap.py` computes them as `wrap_haz_lead.py --tube`
  does; `collect.py` checks the slopes against the quote from `research/wrap/PREDICTIONS.md`), the four 84-cell forecasts
  as ticks (two crossed out, NB's scoring), and the tube line's and power form's forecasts for 96 and 108 cells (W11, W12).
  The card's own run of the 84-cell face, when it comes, would be a second code: add it as a second point or replace the
  value, and say which.
- The gun's line and the divider: `research/signals/objects/line-C.json` and `divider-C8.json`, copied into
  `data/signals4.json`; laid out by `assets/signals-core.js` (`line`) as the lead's oracle checks lay them out, stepped by
  `gump-core.js` and drawn by `assets/kit.js` (`sigLine`), live (the oscillator is in the same torus; nothing precomputed).
  `checks/check-signals.js` checks the layouts' onset and period at N = 2, 3, 8, 12, 16 (line) and 3, 8, 12, 16 (divider),
  the oscillator against its free orbit from N = 8, and the page's stepper against `reference/oracle.py` at N = 12.
- Computed on the page, not quoted: each face's and each girth line's distance from the line of faces with no short loop,
  the nine wrapped faces' distances from the ledger's line, the period and onset of the line and the divider (by comparing whole states).
- `project.gathered` (the footer's "up to" date) is the newest date among `sources/update-*.json`; the claim counts (179; A 86,
  B 81, C 11, D 1) and the timeline are read from the repository as before.
- Typed, not drawn from data: "Open now" (from the essay's "What I would look at next" and OPEN-PROBLEMS 9 and 13 as of
  about 16:30 UTC; "running" for the 84-cell face and the rimmed face, per the essay); the plates' prose.
- Not shown: the beam (SG17's second half), the clock with a tail (SG20), the turn-class negatives (SG21, SG13), C8.24b.
