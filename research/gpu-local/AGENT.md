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

## Current state (2026-11-17, about 12:00Z)

- Branch `claude/gpu-local-1080`, pushed. Reviews of this work are on main under `research/audit/REVIEW-gpu-local-*.md`.
  The lead takes no turn before the usage reset (2026-11-18 11:00Z) and reads this branch then: do not message it
  before that unless something cannot wait.
- Done and written up: queue items 2 and 3; the tube and wrapped faces, thicker slabs, the 6 × 6 to ten seeds; the
  first five faces of chain 3 (README "Chain 3"; `PREDICTIONS.md` block 8 scores block 7 so far).
- **Three things are running:**
  1. GPU, until about 13:00Z on 2026-11-18: the last job of `research/scratch/gpu-local/chain3.sh` (log `chain3.log`):
     the 120-cell 12-tube (1,18),(0,40), eight runs of 180 minutes. The script commits and pushes its rows itself at
     the end. Owed then: `eq_analyze.py 1 18 40 save`; score the 120-cell forecast of block 7 (24.576 ± 0.020) in a
     new block; a row and a sentence in README "Chain 3"; commit, push, a `USAGE.md` line; one message to the lead.
  2. CPU, 4 threads, until about 19:30Z on 2026-11-18: `research/scratch/gpu-local/chain_cpu.sh` (log
     `chain_cpu.log`): the second code `research/gpu-local/cpu/fr.py` on the 96-cell tube (17 h), then (1,4),(0,28)
     (8 h), then the tube again (12 h). Rows append every 15 minutes to `research/data/gpu_local_cpu/`; commit them
     with any push. Owed: the comparison with the GPU values in the README (`fr.py summary`).
  3. CPU, 8 threads: an Opus subagent on the lead's seventh signals push (`research/signals/push7/`, its own README
     and commits; it must finish by 09:30Z on 2026-11-18). Owed when it reports: read its hand-back, check that its
     verify script prints PASS here, push, and pass the summary to the lead in the same message as the 120-cell tube.
- **After that:** fetch `research/GPU-QUEUE.md` first. The lead will brief a CPU study of how rimmed, wrapped and
  long-tube faces die (open problem 9 (k), (l)). The ribbon faces (note of 06:21Z, 2026-11-15) are still mine to
  design or refuse; queue items 4 to 7 when briefed; the lead's optional longer run at 111 cells.
- **Usage:** the last reading is in `USAGE.md`. The owner allowed a few turns before the reset (2026-11-17, "feel
  free to take a few turns until the reset") and offered the CPU ("leave a core free, but the rest is yours").

### Addendum, 2026-11-18 03:15Z (the owner's message, with a brief drafted by the lead)

- The owner reset the Fable window on 2026-11-18 and asked this session to be the measurement side of a theory
  swarm (branch of its own, `research/blast/`) that runs until 2026-11-18 11:00Z on why each kind of face dies at
  its rate. Heavy work goes to Opus subagents ("Stay on Opus").
- Two Opus subagents started at 03:10Z on "how each kind of face dies, watched": wrapped faces and tubes
  (`research/dying2/`, 4 threads) and the rimmed hull face at R = 11 and 13 (`research/dying2/hull/`, 3 threads).
  They commit their own paths at least hourly and must finish by 10:30Z. A background loop here pushes the branch
  every hour until about 12:15Z. The signals subagent was cut to 2 threads and may close period 8 if it can.
- Still running: the 120-cell tube on the card (until about 13:00Z on the 18th; the script pushes its rows) and the
  CPU second code on 4 threads (`chain_cpu.sh`, until about 19:30Z).
- Owed: a row in `USAGE.md` at every turn, pushed (the lead goes by those rows); when the subagents report, read
  the hand-backs, push, and tell the lead in one message; then what the state above lists for the 120-cell tube.

## Addendum, 2026-11-18 09:00Z

- All three Opus subagents have finished and their work is pushed (branch at d241ef8 or later): research/dying2/ (wrapped
  faces and tubes, head fcc27ac), research/dying2/hull/ (4727bf3), research/signals/push7/ (d34dbf5). Checked by this
  session: the commits and files exist; verify7.py objects7.json --maxL 260 was rerun here and printed ALL PASS (52 min).
  Not checked by this session: any number in the two dying2 READMEs; the heavy verify pass (--minL 261).
- A cross-reading nobody has checked: the chance that a dip reaching k live cells ends in death is lower on the hull face
  (0.77, 0.50, 0.30 at k = 1, 2, 3) than on the wrapped faces (0.85, 0.63, 0.42). The two subagents may not define q(k)
  identically: compare research/dying2/hull/condq.py with research/dying2/dyan.py before using it.
- The lead has NOT been messaged about any of this. Weekly Fable usage was 99% at 08:52Z, and a message could cost the
  lead a turn before the reset at 11:00Z; everything is on the branch. Owed when chain 3 ends (about 13:00Z): one message
  to the lead (Orchestrator) covering the 120-cell tube (interim, six of eight runs: 24.497 +- 0.019 against the forecast
  24.576), the three subagents, and the CPU second code; then the scoring block and README row as listed above.
- Threads now: the CPU second code uses 4 of 16; nothing else of ours is running on the CPU.
