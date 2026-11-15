# The Gump Map site

The project's overview for the owner, as a static multi-page site: a landing page (the live side-11 run and the map of
every plate), one page per topic, and the interactive web app (`web/`) mounted under `app/`. One build command writes
the whole deployable tree to `site/dist/` (git-ignored), which is served as it is by GitHub Pages under a subpath and
can be published as a multi-file claude.ai artifact.

The site is a view, not a source: where it and `research/CLAIMS.md` or `research/NOTEBOOK.md` disagree, they are right.
How each number on each plate was obtained (quoted, computed on the page, typed) is recorded per refresh in
`collect/REFRESHES.md`; keep adding to it.

## Commands

    python3 site/build.py              # site/ + web/  ->  site/dist/   (builds the app with node web/tools/build.mjs)
    python3 site/build.py --no-app     # the same, copying web/dist as it is
    bash site/check.sh                 # build + every check below; --quick skips the signals check, --no-app as above
    python3 site/collect/collect.py    # collect/sources/*.json + repository files  ->  data/<key>.json

Preview, as GitHub Pages would serve it under `/<repo>/`:

    mkdir -p research/scratch/site/serve && ln -sfn "$PWD/site/dist" research/scratch/site/serve/gump-for-agents
    python3 -m http.server 8000 --directory research/scratch/site/serve     # http://127.0.0.1:8000/gump-for-agents/

Pages fetch their data, so opening `dist/index.html` as a file does not work; use a server.

## Layout

    pages.json          the pages, in order: slug, nav label, <title>, blurb, the line to the next page, and the plates
                        (id + its tile on the landing map: k, v, status class and text, "new")
    layout.html         the shell of every page: head, header with the page list, footer, the four scripts
    plates/<id>.html    one plate: <section class="plate" id="<id>"> ... </section>, exactly as on the old page
    plates/<id>.js      that plate's figures, if any (one or more IIFEs reading D.<key> and filling #ids of the plate)
    plates/run.*        the landing page's live run; plates/map.js fills the landing map's "Built, and when" tile
    assets/site.css     all styles: the old page's tokens and plate styles, then the site shell at the end
    assets/kit.js       shared helpers: $, S, E, tipOn, responsive, frame, dot, iso, numTile, band, ...
    assets/boot.js      per page: fetch data/<key>.json for each key into D, then run the plate scripts in order
    assets/stamp.js     the footer's "Repository state of ..." line (reads D.project, so every page fetches project)
    assets/gump-core.js the stepper (bit-exact against reference/golden); signals-core.js lays out the signal objects
    data/<key>.json     one file per data key, written by collect/collect.py (42 keys, the largest 21 kB)
    collect/            collect.py, record_deaths.py, sources/ (what the helper agents gathered, with src/how), REFRESHES.md
    checks/             check-core.js, check-signals.js, check-parity.py, check-links.py, smoke.js
    dist/               the build (git-ignored): index.html, <slug>/index.html, assets/, plates/*.js, data/*.json, app/

The pages and their plates are in `pages.json`; at the time of the split (2026-11-15) they were: the map (landing),
the rule, how faces die, the area law, debris and clocks, signals, relatives, the record.

## How a page is built

`build.py` reads `pages.json`, and for each page concatenates its plates' HTML into `layout.html`, adds a page head
(eyebrow, title, blurb, "On this page" chips) and previous/next links, and rewrites `href="#<plate>"` to the plate's
page when the plate lives elsewhere. It finds the data a page needs by scanning that page's plate scripts for `D.<key>`
(plus `project`, for the footer), and writes both lists onto the boot.js tag: `data-data="law tail project"`,
`data-plates="law shape ..."`. It stops with a message on a missing plate file, a key with no data file, or a script
that looks up `'#some-id'` which is not on its page. Only the data files some page reads are copied to `dist/data/`.

## Adding things

- **A plate**: write `plates/<id>.html` (one `<section class="plate" id="<id>">`, using the classes already in
  `site.css`), and if it draws anything `plates/<id>.js` (start with `'use strict';`, wrap the code in an IIFE, read
  data as `D.<key>`, use the helpers in `kit.js`). Add `{"id": "<id>", "k": "...", "v": "...", "stc": "st-meas",
  "st": "measured"}` to its page's `plates` in `pages.json`, where it should appear; `"new": true` marks the tile. A
  plate that needs a new data key needs `data/<key>.json` (see next). New styles go at the end of `site.css`.
  Link to another plate with `href="#<id>"`; the build points it at the right page.
- **A data file**: add the key to `out` in `collect/collect.py` (with the checks of its quotes, as the other keys
  have), run it; or, for a hand-made file, put `data/<key>.json` in place and say in `collect/REFRESHES.md` where
  it came from. A plate script that reads `D.<key>` gets it on its page automatically.
- **A page**: add an entry to `pages.json` (slug: a short folder name; title: two to four words, no colon; blurb: one
  or two sentences; connects: the line shown on the "Next" link to the following page). It appears in the header,
  the landing map and the previous/next chain in that order.
- Then `bash site/check.sh` and look at the screenshots (`node site/checks/smoke.js --shots DIR`).

## Checks (`bash site/check.sh`)

- `checks/check-core.js`: the stepper every page loads (`assets/gump-core.js`) against `reference/golden` for the
  closed cubes of side 8, 9 and 11 (every generation), and the two ticking states the pages draw, read from the
  served `data/zombie.json` and `data/c52.json` (period 16; period 52 and its split by cell period). A few seconds.
- `checks/check-signals.js`: the signal layouts (`assets/signals-core.js`) and the stepper against the rules and
  against `reference/oracle.py`; also that `data/signals.json` holds the object files. About 35 s on one core.
- `checks/check-parity.py`: nothing of the last single page (`git show 2f0868d:docs/overview/index.html`) is lost:
  every plate once and byte-identical (links aside), all figures, canvases, buttons and headings counted again, every
  `#id` its scripts used still used on the plate's page, every data key it read still read and served with the same
  content, every map tile on the landing page. It compares against that fixed version: when a plate is changed on
  purpose, expect it to report that plate, and move `OLD_REV` (or pass a file) once the change is checked.
- `checks/check-links.py`: every relative href/src, CSS url(), import, import map entry, `new URL(…, import.meta.url)`
  and boot.js data/plate list in `dist/` resolves to a file (anchors on overview pages to an id); no root-absolute
  path; external scripts only from cdnjs / jsDelivr npm / unpkg with an exact version, stylesheets only Google Fonts;
  at most 255 files.
- `checks/smoke.js` (pre-installed Playwright): serves `dist/` under `/gump-for-agents/`, opens every page and the app at
  1280 px and 390 px, fails on console errors, page exceptions, failed or 4xx/5xx requests, a missing plate, an empty
  figure container (`#f-*`, `#c-*`), horizontal page overflow. `--shots DIR` saves full-page screenshots of each in
  light and dark.

## Link form, and the two hosts

Every link between pages is relative and names the file: `law/index.html`, `../signals/index.html#signals`,
`../index.html`; never a bare folder (`law/`) and never a root-absolute path (`/law/`). GitHub Pages serves both
forms, but the claude.ai artifact host serves published files by their exact paths and is not known to map a folder to
its `index.html`, and a file opened locally does not either; the explicit form works on all of them. The folder-style
URL (`…/law/`) still works on GitHub Pages for a link someone types or shares.

- **GitHub Pages**: `.github/workflows/pages.yml` (manual trigger only) runs `npm ci` in `web/` and
  `python3 site/build.py`, and uploads `site/dist`. `dist/.nojekyll` is written for Pages.
- **claude.ai artifact**: publish `dist/index.html` as the page and every other file of `dist/` through `files`
  (paths as in `dist/`; 123 files, about 3.4 MB, at the split). Each page is a complete document with its own
  `<title>`, theme tokens for light and dark, and the viewport meta; data is fetched with relative URLs, which the
  artifact host allows for published files. `.nojekyll` is only for Pages and can be left out. Not tested on the
  artifact host: whether it maps `law/index.html` and the app's ES-module imports and import map as plain static
  files do, and how its skeleton treats a page that is already a full document.
- The app (`app/`) is `web/dist` unchanged: it has its own single dark look, a one-word title ("gump") and no link
  back to the map; the map links to it from the header ("App") and the landing page.
