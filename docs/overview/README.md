# The overview page ("The Gump Map")

A visual, text-light summary of the directions and findings, made for the owner on 2026-11-14 while research was
paused. Published as a private artifact (the link is in `LEAD.md`); `index.html` here is what was published.

    python3 docs/overview/collect.py     # data/sources/*.json  ->  data/data.json
    python3 docs/overview/build.py       # src/ + data/data.json + gump-core.js  ->  index.html
    node docs/overview/check-core.js     # the page's stepper against reference/golden (sides 8, 9, 11)

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
