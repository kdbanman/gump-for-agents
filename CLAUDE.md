# gump-for-agents

A rebuild and investigation of **gump**, a 3D cellular automaton whose cells are the faces
of the cubic honeycomb (original: `kdbanman/gump`, a 2012 Processing sketch). The project is
both an engineering build and an open-ended scientific/aesthetic investigation, run mostly
by agents. The owner (Kirby) wants to hear what we find interesting, surprising, beautiful.

## Read first

- `docs/AUTOMATON.md` — the exact rule, coordinates, proven structure theorems, legacy semantics.
- `research/NOTEBOOK.md` — findings so far, open questions. Append to it; date entries;
  give the command that reproduces each claim. Distinguish *proved*, *measured*, *conjectured*.
- `research/OPEN-PROBLEMS.md` — what is not settled. `research/theory/PROGRAM.md` — the theoretical arm
  (chaos, debris and the passage between them), a web of goals to pick from.
- If you are the lead (the top-level session working with the owner), also read `LEAD.md`.

## Layout

- `reference/` — tiny numpy oracle (ground truth, legacy-faithful) + golden logs from the original.
- `engine/` — Rust: fast engine + `gump` CLI for agents (stats, snapshots, analysis).
- `web/` — WebGL2 compute + three.js viewer for humans.
- `research/` — notebook, experiment scripts, small data, figures.

## Working agreements

- Correctness is anchored to `reference/oracle.py` and `reference/golden/`. A faster engine
  is trusted only once it reproduces them bit-for-bit.
- The original repo, if cloned, is at `/home/user/kdbanman/gump` (read-only reference).
  Its data logs are huge — use `head`/`tail`/`wc`/scripts, never `cat` or Read them.
  Do not consult that repo's open pull requests.
- Several agents may share this working tree. Commit only your own paths
  (`git add <dir> && git commit -m "…" -- <dir>`), commit often, don't push — the lead pushes.
  The lead also merges, and is the one who writes `NOTEBOOK.md` and `STATUS.md` once a result is checked.
- Keep large generated data out of git (`research/data/` is for small, curated files;
  put bulk output under `research/scratch/`, which is ignored).
- Persist what was hard to derive; skip what the next capable reader could re-derive in a minute.
- No human reviews the technical work here, so claims are checked by construction: say how a number can be
  reproduced, say what you did *not* check, and expect a second agent to try to break it. A stepper or engine
  is trusted only when bit-exact against the engine/oracle. `research/check.sh` must pass before a merge;
  `research/CLAIMS.md` records how well each headline claim has been verified.
