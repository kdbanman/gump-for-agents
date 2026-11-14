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
