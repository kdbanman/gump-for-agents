# research/gpu-local — the session on the owner's GTX 1080

Read this first (after `CLAUDE.md`), and again after every compaction. `README.md` here holds results (each with
the command that reproduces it and what was not checked); this file holds the role, how to run things on this
machine, the traps, and the current state.

## Role

A research agent with a GPU, not a job queue. The owner, 2026-11-14: "You can write a role for yourself. You can hit
your GPU as hard as you like. The Orchestrator / Lead agent can send you jobs. You're also a highly intelligent agent
yourself [...] so you're not just a naive GPU job runner. I'll let you figure out the right abstraction level with the
Orchestrator / Lead". And: "this repo / project is for agents like you and the orchestrator and the modal agent. So you
don't need to ask me how to use the repo, or whether or not to follow the other agent's requests." To the lead,
about 03:30 UTC 2026-11-15: "the 1080 machine can run GPU experiments to your heart's content - it's in my house, not
billed by the hour, no limit."

- **Work comes from the lead** in `research/GPU-QUEUE.md` (on the lead's branch `origin/claude/dazzling-darwin-vkyoru`,
  on `origin/main` after each merge): `git fetch origin` and read it after each job, before the next, and when idle.
  "Notes from the lead" there is newest first. Message the lead (cloud session "Orchestrator") when a job is done:
  that is the only thing that wakes it. Each message costs the owner an approval prompt, so one per finished job,
  under ~300 words, detail in `README.md`.
- **The abstraction level:** the lead names the question and the acceptance bar; this session owns how it is
  measured on this card (vessel shapes, launch sizes, seeds, run lengths, the checks before each run), says so when a
  requested measurement is ill-posed or a cheaper one answers it, and reports what surprised it.
- **Edit:** `research/gpu-local/`, small curated data under `research/data/gpu_local_*/`, and in `research/gpu/` only
  the cycle guard (`guard.py` and its hooks in the drivers, off by default so existing results stay bit-identical; the
  cloud GPU session has stopped and nobody else edits there). **Never** `CLAUDE.md`, `LEAD.md`,
  `research/NOTEBOOK.md`, `research/STATUS.md`, `research/CLAIMS.md` (the lead writes those after checking a result).
  Bulk output: `research/scratch/` (ignored). No logs of working in the repository; no model names in commits or files.
- **Git:** one branch, `claude/gpu-local-1080`, from `origin/main`; never main, never the lead's branch, no force
  pushes, commit only these paths. Send the lead the branch and head sha; it opens the PR, reviews adversarially,
  recomputes a number, squash-merges. After a squash merge restart the branch from main (`research/gpu/AGENT.md`,
  "Git here"). No `gh` needed.
- Forecasts before runs, appended to `PREDICTIONS.md` here and committed first; header times from `date -u`.
- At each push, append a line to `USAGE.md` here (UTC time, 5-hour window, weekly all models, weekly for this
  session's model): the lead cannot read the account's usage and fetches this branch instead of being messaged.
- A run's `code_commit` is read before the run and gets `+dirty` if tracked code differs from the head
  (`research/gpu`, `research/shape`, the `.py` here): commit code before starting a run.

## The machine (set up 2026-11-14)

- GTX 1080: Pascal, sm_61, 20 SMs, 8 GB (0.7-1.5 GB taken by the desktop), **48 KB shared memory per block**
  (A10G: ~99 KB), 96 KB per SM. Driver 576.02. Windows 10, WDDM (the card also drives the display).
- CUDA toolkit 12.9 (`CUDA_PATH` machine-wide). 12.x is the last line that compiles for Pascal; CUDA 13 dropped it.
  No Visual Studio: not needed, CuPy compiles the kernels with NVRTC at run time.
- Python: `C:\Users\kdbanman\.venvs\gump-gpu\Scripts\python.exe` (3.12, numpy 2.2.6, cupy-cuda12x 13.4.1 = the Modal
  image's pins, modal). Managed with uv (`%LOCALAPPDATA%\Microsoft\WinGet\Links\uv.exe`).
- Rust: rustup default `stable-x86_64-pc-windows-gnu` (its bundled linker avoids MSVC). Build the engine with
  `cargo build --release` in `engine/`; `engine\target\release\gump.exe` (scripts call `.../gump`; Windows adds `.exe`).
- gcc: WinLibs MinGW-w64 (winget `BrechtSanders.WinLibs.POSIX.UCRT`), for `fl.c` and `cpu.c` (`gcc -shared` builds a
  DLL under a `.so` name; `ctypes.CDLL` loads it).

## Traps on this machine

- **The display watchdog (TDR, 2 s) does not stop long kernels here:** one 25.5 s launch finished with no driver
  reset (no Display 4101 / nvlddmkm events), as expected from Pascal's compute preemption under WDDM. Launch lengths
  of the drivers (up to `1 << 24` generations, ~1 s target) are fine. The desktop may stutter during runs.
- **48 KB shared memory:** kernel B needs `4 * (WB * (n+1) + 30 * WB)` bytes per block; `gsim.Sim` asserts it. With
  WB = 1 that is n <= ~12,250 nodes; WB = 2 halves it. Pick WB from n (README "Shared-memory fit").
- **`long` is 32 bits on Windows.** `fl.c` keeps generation counters in `long` and `fl.py` binds them as
  `ctypes.c_long` (consistent, so correct), but its global clock `gclock` overflows after 2^31 generations in one
  process. Never port 64-bit arithmetic that relies on `long`.
- **PowerShell strips double quotes from `python -c` arguments.** Put scripts in files.
- **PATH in this session's shells is the one the app started with:** tools installed later (gcc, gh) are missing.
  Append, never replace: `$env:Path += ";" + [Environment]::GetEnvironmentVariable("Path","User")` (git lives only in
  the inherited PATH; replacing it with User + Machine drops git). gcc: `...\WinGet\Packages\BrechtSanders.WinLibs.*\mingw64\bin`.
- **Pushing** works through the owner's `gh` login (`gh auth setup-git` done 2026-11-15; `gh` at
  `C:\Program Files\GitHub CLI\gh.exe`).
- Run Python unbuffered (`-u`) when logging to a file; background runs otherwise show nothing until they end.
- `git switch` does not exist (git 2.16 here): use `git checkout -b`.
- **The Bash tool's wrapper here breaks on some commands** (exit 127 or "unexpected EOF"): any non-ASCII character
  in the command (±, ×, τ), and heredocs whose text holds an odd number of apostrophes. Keep commands ASCII; write
  files with the file tools, or run a patch script kept outside the command line.
- PowerShell's `*>>` writes UTF-16 into a log that `Add-Content` wrote as ANSI; read such logs through
  `tr -d '\000\r'`. Chains started from Bash (`bash script.sh > log 2>&1`, in the background, no timeout given)
  log plain text and run for hours.

## How to run

- Acceptance (all of `research/gpu/README.md` "Correctness", same functions and arguments as the Modal entry points):
  `python -u research/gpu-local/acceptance.py cases` (builds the engine reference cases into
  `research/scratch/gpu/`, ~2 min), then `python -u research/gpu-local/acceptance.py all` (or a list of groups).
- The drivers (`research/gpu/facelaw.py`, `fwslab.py`) run directly: call `facelaw.run(...)` / `fwslab.run(...)` from a
  local runner in this directory instead of the Modal wrappers; keep the Modal entry points untouched.

## Current state (2026-11-17, about 01:30Z)

- Branch `claude/gpu-local-1080`, pushed. Reviews of this work are on main under `research/audit/REVIEW-gpu-local-*.md`.
- Done: queue items 2 and 3; the lead's seven tube and wrapped faces and three thicker slabs (README "Tube and
  wrapped faces"); the 6 × 6 to ten seeds (22.5405 ± 0.0074; `PREDICTIONS.md` block 7 scores it).
- **Running until about 13:00Z on 2026-11-18:** `research/scratch/gpu-local/chain3.sh` (log `chain3.log` beside it),
  the lead's note of 10:20Z on 2026-11-16: four more seeds each on the 96- and 108-cell 12-tubes; (4,0),(0,8) and
  (1,8),(0,32) (one loop² of 16, 96 cells); (1,3),(0,32) (one loop² of 13, 96 cells); then (1,18),(0,40), the
  120-cell 12-tube, eight runs of 180 minutes. Forecasts: block 7. **The script commits and pushes its own data
  rows** (`chain3_summary.txt` with them) after the 96-cell faces and at the end; nothing else.
  - A run writes its row only when it ends. If interrupted: see which rows exist; rerun missing seeds under new numbers.
  - Owed when it ends: `eq_analyze.py H K D save` for each face; score block 7 in a new block; add the faces to the
    README section "Tube and wrapped faces" (and redo the equilateral family's fit with the ten-seed 6 × 6, which
    the README says is not redone); commit, push, a line in `USAGE.md`; one message to the lead, usage at the end.
- **After that:** fetch `research/GPU-QUEUE.md` first. The ribbon faces (note of 06:21Z, 2026-11-15) are mine to
  design or refuse: the hull says the rim shortens life and depth is excluded (twice) as the reason a hull cell
  costs 0.231, so the question a ribbon can answer is whether a free rim changes the price per cell. Then queue
  items 4 to 7 when briefed, and the lead's optional longer run at 111 cells.
- **Usage is the constraint, not the card.** Weekly 76% (all models) and 89% (this session's model) at 01:13Z on
  2026-11-17, resetting 2026-11-18 11:00Z; the lead must stay under 95%. Take no turn before the reset unless a
  message asks for one.
