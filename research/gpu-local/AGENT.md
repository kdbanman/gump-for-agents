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

## How to run

- Acceptance (all of `research/gpu/README.md` "Correctness", same functions and arguments as the Modal entry points):
  `python -u research/gpu-local/acceptance.py cases` (builds the engine reference cases into
  `research/scratch/gpu/`, ~2 min), then `python -u research/gpu-local/acceptance.py all` (or a list of groups).
- The drivers (`research/gpu/facelaw.py`, `fwslab.py`) run directly: call `facelaw.run(...)` / `fwslab.run(...)` from a
  local runner in this directory instead of the Modal wrappers; keep the Modal entry points untouched.

## Current state (2026-11-15)

- Branch `claude/gpu-local-1080` created from `origin/main` 0e3b642. Job 0 (acceptance) and job 1 (cycle guard) in
  progress; see the queue for the order after that (equilateral tori of `research/constant/PREDICTIONS.md` part C,
  then the hull face at A = 108).
