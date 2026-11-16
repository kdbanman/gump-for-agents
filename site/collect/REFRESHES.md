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

## Refresh of 2026-11-15 (evening): why a tube is cheaper; nothing listens; an echo

Rewrote "What a short way round costs" (`#wrap`, law page) around the density law: a living face is emptier by one term f per
loop, falling smoothly with the loop's length and not ending at 21, and a tube's price discount per cell is κ = 1.85 times it.
Added "An echo" (`#echo`, live) and "Nothing listens" (`#ends`, the census of ends) to the signals page after "A clock that edits
the message". One sentence on "One price per cell?" (`#constant`); the divider's "no reader" tile, the "no corner" tile of
"Signals", "Open now", the map tiles and the signals blurb updated. Two corrections, one audit, two milestones.

- Quoted numbers: `sources/update-2026-11-15f.json` (every item with `src` and `how`), checked by `collect.py` as before against
  NB "why a tube is cheaper", "the fifth signals push", "the fifth signals push reviewed", CLAIMS WL2, WL4-WL6, SG23-SG27, and
  (`file` quotes) `research/wraplocal/data/dens_rho_face.txt` and `research/wrap/PREDICTIONS.md` (W13). `checked()` now also
  accepts a float under 10⁻³ written in fixed notation (0.000029 for 2.9e-05); nothing else about it changed.
- `data/dens.json`: the deficits f(9) … f(28) with their errors are read by `collect.py` from
  `research/wraplocal/data/dens_rho_face.txt` (the study's `dens.py rho_face --price` output, committed) and asserted equal to the
  notebook's quote to 2 × 10⁻⁶, and ρ∞ and κ to that file's. Loops² 31 to 37 are left out (not resolved; 37 comes out negative).
  The tubes' measured discounts (12, 13, 16, 19) are quoted from the same file; the plate divides them by κ. 19's discount is
  negative (−0.00034 ± 0.00120): drawn as the upper end of its bar only, with a marker "measured below zero".
- The lead's re-measurement (five densities, three deficits; `research/audit/wraplocal_lead_check.py`) is quoted from the notebook
  and shown under "How it was checked".
- **A value still to come: `dens.w13measured`** (`sources/update-2026-11-15f.json`, `dens.w13measured`, now `null`): ln τ of the
  84-cell face (1,4),(0,28) with loops of 21 and 28, forecast W13 at 17.534 ± 0.004 if the relation holds and 17.547 ± 0.003 if
  not. **Who fills it in:** whoever records the card's run of that face (the lead, from the card's rows; the notebook entry that
  scores W13). Set `value`, `se`, `src` and a `quote` from that notebook entry (or a `file` quote); `collect.py` then checks the
  quote, and the plate's tile switches from "queued" to the value and its distance in σ from both forecasts. Change the plate's
  chip "loops of 21 and longer: a test queued" by hand then.
- The echo: `data/echo.json` is the first record of `research/audit/signals5/end_echo.json` (C18.23a, tg = 45, the hole),
  copied by `collect.py`; `assets/signals-core.js` (`echo`) places it by an even shift in a torus of side 64 (the lead's check
  uses 96; the page's stepper gives the same difference counts for 110 generations after the hole on both).
  `checks/check-signals.js` (section 6) checks the copy against the record, then on the page's layout and stepper: the hole
  cell alive at tg, exactly three cells differing at 18 generations, 23 to 42 after the hole, the difference two generations
  later the same three moved (2, 0, −2), 61 to 65 cells differing at 80; and both runs (with and without the hole) against
  `reference/oracle.py`, every generation to tg + 80. The quiet wire used to tell rakes from wire is line-C's cap and units.
- Computed on the pages, not quoted: discount ÷ κ; the cells in which the two echo runs differ, and the generations with exactly
  three (shown with ✓ against the ledger's); the row and column totals of the four kinds of end.
- `update-2026-11-15e.json`'s essay quote `signals4.nothing` was re-copied: the essay's sentence now adds "among 741 ends
  searched and thousands of placements sampled" (the words checked are unchanged).
- Claim counts: 187 (A 89, B 84, C 13, D 1), read from `research/CLAIMS.md` by `collect.py` as before.
- Typed, not drawn from data: "Open now" (from `research/STATUS.md` at 20:27 UTC and the essay's "What I would look at next":
  the sixth push running, W13 and the 96- and 108-cell tubes queued; its "1.85" and "0.2075" are WL5's); the map labels; the
  plates' prose (√21, √31: the loop lengths of the quotes).
- Not shown: the statistics table of `research/wraplocal/README.md` (only its conclusion, "occupation, not turnover"); the loop-9
  discount (0.0142, curved) as a point; the wall and fire kinds of gun death as drawings; the second echo clock C20.33c.

## Refresh of 2026-11-15 (night): the sixth signals push and its review; when signals meet

Added "When signals meet" (`#meetings`, live) to the signals page after "An echo". "An echo" (`#echo`): its open chip and
"running" tile became the result (no gun survives an echo; the reflector works once) and one clause of its heading. "Nothing
listens" (`#ends`): the events the fifth review had not followed, a paragraph on the count an echo writes, six pushes' forecasts.
"Open now" (`#next`) first item, the map tiles for `echo`, `meetings` and `next`, the signals blurb. Three corrections, one audit,
two milestones.

- Quoted numbers: `sources/update-2026-11-15g.json` (sections `meet`, `echo6`, `ends6`; every item with `src` and `how`), checked by
  `collect.py` as before against NB "the sixth signals push", "the sixth signals push reviewed", CLAIMS SG28-SG32 and (`file`
  quote) `research/OPEN-PROBLEMS.md` item 13 (q). `collect.py` also asserts 112 = 24 + 66 + 22, 16 = 14 + 2, 10,374 = 14 × 741,
  1,482 = 2 × 741, 30 = 12 + 18, and that the 426 events are the fifth push's.
- New key `data/meet.json`: the plain rake train's unit cells at four phases, wire B's two units, `v` and `unit`, copied from
  `research/signals/objects/echo-train.json`; the nine signals (parity, cells at train phase 1, direction) read by `collect.py`
  with `ast` from the literal `SIGS` of `research/audit/signals6/sig6.py`, asserted equal to the train file's for E, U, H, K0 and
  to "six down and three up"; "made by" for each is typed from the table of `research/audit/REVIEW-signals-6.md` section 2.
  Also `flips`, `offsets`, `lead` (80 generations, 48 units), `steppers` (1,050) from the quotes.
- Changed keys: `echo` gains `sixth` (`guns` 67, 11; `sat` 4, 3, 52; `once` 1, 20); `ends` gains `followed`, `rows`, `count` and
  its `pushes` is now 30, 12, 18 (was 24, 11, 13 from `update-2026-11-15f.json`, still in that file).
- The demo: `assets/signals-core.js` (`train`) lays the train on a ring of L units in a torus of side 2L, moved (0, L, 0), as
  `research/audit/signals_meet_lead_check.py` does. Page choices, typed in `plates/meetings.js`: L = 48 (the lead's ring), the
  run to generation 56 (the train file's sample meetings are read at 56; the change does not reach round the ring by then), and
  the placements: the train file's sample meetings moved 10 units (the echo alone at unit 8).
- `checks/check-signals.js` section 7 reads L, the run length and the four placements from `plates/meetings.js` and checks, on
  `sigCore.train` and `gump-core.js`: `data/meet.json` equals the train file; one step of each phase is the next; E, U, H, K0 alone
  rigid with the stated cell count and direction for 80 generations; the page's four runs (the echo alone rigid; U against K0 the
  plain train from generation 20; E against H never back to the train, every unit more than 7 inside the span wire B's cells at
  generation 56 (the units that are not: three at each end); E against K0 one differing cell in every second unit inside); and
  E against H and U against K0 against `reference/oracle.py`, every generation to 56.
- Computed on the page, not quoted: the cells differing from the plain train and their units, the history strip, the readings
  (three cells; the generation from which nothing differs; whether the inner units all hold one cell set, and its size; the
  alternation of one differing cell). The count of signals moving up (3) and of the nine is counted from `meet.sig`.
- Claim counts: 192 (A 91, B 87, C 13, D 1), read from `research/CLAIMS.md` by `collect.py` as before.
- Typed, not drawn from data: "Open now"'s first item, from `research/OPEN-PROBLEMS.md` item 13 (q)-(t) and NB "the sixth signals
  push reviewed" ("nine", "three", "six", "eleven" are SG28's and SG30's; the wrapped-face items unchanged); the map labels; the
  plates' prose.
- Not shown: the meetings with K3 and N1-N4 as runs (K3's two outcomes are named in words); the B′ stretch as a drawing; the
  constraint problems' planes (C = 31 … 37) beyond "within bounds"; U absorbed by a gun (echo-train.json `gun_absorbs_U`).

## Refresh of 2026-11-16 (morning): one price per cell? No; the card's tubes and the loop of √21

"One price per cell?" (`#constant`) rewritten around the answer no: a new figure of the price per cell by kind of face
(`#f-prices`), three tiles (the 108-cell rimmed face, the rimmed price, the long tubes), "where the difference is not" (occupation,
the rim, depth) and "how far it is checked, and what is open"; the old figures kept below, the ranges figure retitled "before the
108-cell rimmed face", the GPU-hours tile and the nine-faces caption and tile told that the face has run. "What a short way round
costs" (`#wrap`): W13 measured, the card's seven faces drawn (squares) and tabled, the long tubes and their line, κ 3.0 on long
tubes in the heading and tiles, chips and check list updated. "Open now" (`#next`): items 3 and 4 rewritten. Map tiles for `wrap`,
`constant`, `next`. Two corrections, three forecasts, three milestones.

- Quoted numbers: `sources/update-2026-11-16a.json` (sections `price`, `wrap16`; every item with `src` and `how`), checked by
  `collect.py` against NB "the hull face of 108 cells", "a living hull face is occupied …", "the card's tube and wrapped faces",
  CLAIMS CN2-CN4, WL3, WL7, WL8, and (`file` quotes) `research/wrap/PREDICTIONS.md`, `research/OPEN-PROBLEMS.md` item 9 (j)-(m),
  `docs/WHAT-I-SEE.md` ("Two prices", "Your card's answer on the queued face").
- **W13 filled in here, not in `update-2026-11-15f.json`** (which keeps `w13measured` null): `wrap16.w13measured` (17.5387 ±
  0.0031, CLAIMS WL8) overrides `dens.w13measured`; `collect.py` asserts the plate's own distances (+0.9σ, −1.9σ) equal the quote's.
- The card's seven tube and wrapped faces: each row quoted from the notebook's table. Where `research/data/gpu_local_eqtorus/<file>.csv`
  is in the tree (it is, since the merge of 2026-11-16), `collect.py` recomputes ln(2 Σexposure / Σface) and its error and asserts them
  equal to the quote; the site does not need the files. The nine equilateral faces of `data/tori.json` are now read by name (the
  folder holds sixteen files).
- New key `data/prices.json`; changed keys `dens` (`w13measured`, `loop21`, `two21`, `kappa3`, `kappafit`), `wrap` (`card`,
  `long`, `pow`, `repeat`), `forecasts`, `corrections`, `project`.
- Computed on the pages, not quoted: the W13 distances (checked in `collect.py`); the long tubes' line in the tube figure, drawn at
  the quoted slope 0.2016 through the weighted mean of the three card faces (not a fit); each card face's distance below the line.
- Typed, not drawn from data: the grades in the price figure's tooltips and table (from the CLAIMS level columns: CN2 B, CN3 B + C,
  CN4 C, WL3's line fits C, WL7 C at 96 and 108); the "not checked" sentences (NB's "Not checked" lines of the three entries);
  "Open now" items 3 and 4 (from OPEN-PROBLEMS 9 (k)-(m) and the essay; their 0.231, 0.2087, 3.0, 0.0047 ± 0.0023 are CN2, WL7, WL8's);
  the map labels; the plates' prose.
- Claim counts: 197 (A 91, B 91, C 14, D 1), read from `research/CLAIMS.md` by `collect.py` as before.
- Not shown: the hull face's hazard by age; the rim profile beyond three rows and the depth profile by radius (`research/hulllocal/README.md`);
  the card's settled lives by thickness; the 75-cell repeats as points (they are in the card's table).
