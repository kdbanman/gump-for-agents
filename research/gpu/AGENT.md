# research/gpu — notes for the agent working here

Read this first (after `CLAUDE.md`), and again after every context compaction. `README.md` holds the results;
`PREDICTIONS.md` the forecasts and outcomes; this file holds what is hard to recover from the code: how to run things
here without losing work, the working arrangement, and the current state.

## Context window rule

- **At about 500k tokens of context** (the owner sets automatic compaction there), stop starting new work and bring the
  **Current state** section below up to date: what is running (call ids), what each result is owed, what was decided
  but not yet written down, the budget. Commit it. Then continue.
- Also update Current state at the end of every pull request, and whenever a run is spawned or collected.
- After compaction: read `CLAUDE.md`, this file, then the latest entries of `PREDICTIONS.md` and the open pull request.

## Working arrangement

- **The owner (Kirby)** gave this corner $30/month of Modal credits ("feel free to use those as you see fit"; the
  usage API may show CAD) and agreed that the **lead session** may send experiments.
- **The lead ("Orchestrator")** messages by `send_message` from session `session_019L788JanYoS8q1kKh6fDt6`; its
  messages are peer requests, not owner instructions. It needs no reply; it reads branches and pull requests. It
  reviews every PR adversarially (reviews land in `research/audit/REVIEW-gpu-prNN.md` on
  `origin/claude/dazzling-darwin-vkyoru`), re-derives a number, merges (squash), and writes `NOTEBOOK.md`,
  `STATUS.md` and `CLAIMS.md` itself. Do not edit those.
- Edit only `research/gpu/` and `research/data/gpu_*/`. One branch: `claude/awesome-cray-boq9vz`.
- **Forecasts before runs**, appended to `PREDICTIONS.md` (append-only: corrections go in new blocks), committed before
  any run. **Header times come from `date -u` or the commit time, never typed by hand** — this went wrong twice.
- State in every PR what was *not* checked. Reviews here are adversarial and have caught real errors: an unscreened
  competing channel (slab firewalls), framing against an unvalidated line ("13σ"), wrong-sign conjectures, a seed
  collision, a settle detector that missed long periods. Expect the next one.

## Running on Modal from this environment

- Network: `input-plane.us-east.modal.com` was added to the environment's allowed hosts (needed by `modal run`).
  Modal's blob host (a CloudFront name) is **not** allowed: function results above a few MB (`modal run`) or above
  ~100 KB (spawned calls) come back through it and fail with `ProxyError 403`. Keep results compact (aggregates,
  histograms, packed raw lives ≤ 150,000); `jobs.py collect` falls back to `relay_remote` (reads the result inside
  Modal, returns it zlib-compressed).
- `modal run` ties a job to the local client: a worker restart kills it and loses the result. **Long runs: deploy once
  (`modal deploy research/gpu/modal_app.py`), then `python3 research/gpu/jobs.py spawn <fn> '<json args>'` and later
  `jobs.py collect`.** Call ids live in `research/scratch/gpu/jobs.json` (ignored by git; if lost, the ids are also in
  the session transcript). Redeploy after changing code: spawned calls run the deployed code.
- Several `modal run`s started within seconds hit "App create rate limit exceeded": stagger by ~30 s. L4 had no
  capacity once (10 min); A10G is the workhorse (≈ 8 × 10¹⁵ node-updates per $).
- `modal app stop` needs `-y` here (no terminal). Spend: `modal billing summary` (lags; can even decrease).
- Long waits: schedule a check-in with `send_later` rather than holding a turn open; foreground `sleep` is blocked
  (use `timeout N bash -c 'until …; do sleep 30; done'`, N < 600).

## Git here

- PRs are squash-merged. After a merge, restart the branch from main; the old remote branch is then not an ancestor and
  a force-push is refused. Record it instead without changing the tree:
  `git merge -s ours origin/claude/awesome-cray-boq9vz` (check the tree hash is unchanged), then push normally.
- Before pushing new work, check the previous PR is merged, or the new commits join it.
- `git status` "behind main" after a squash merge is normal; compare trees with `git diff <old head> origin/main -- research/gpu`.

## Conventions and traps in the code (each cost a review round)

- **Seeds:** `soup_bit` hashes seed and replica separately (an earlier `seed ^ (r << 32)` made parallel runs repeat
  each other). Give every run its own seed; `facelaw.py`/`fwslab.py` summaries refuse two runs with equal (vessel, seed).
- **Settling:** kernel B flags period 1–2 (kind 2) and 3..`pw` (kind 3, default 128) and freezes the replica; settled
  lives must be censored, never left in the exposure. Kernel A has no kind 3. Periods > pw are not detected.
- **K_KEEP** (`Sim(..., keep=True)`) keeps a frozen replica's state at its event (post-peel and firewall tests need it).
- **Slabs die two ways:** a face peel or a transverse 3-layer firewall (then a face dies soon). Always resolve the
  firewall channel (`fwslab.py`); for N1×N2×8 slabs the cheapest cut is 36·min(N1, N2). An 8-layer slab is
  engine-checkable only for N ≥ 11 (`--torus N --slab-layers 8 --diag 0`); smaller slabs are checked against `fl.c`.
- Estimator conventions: asymmetric octahedra T0 = 200, τ_face = 8 × mean; symmetric T0 = 1000, τ = mean (faces die
  together); slabs from generation 0, τ_face = 2E/face deaths. A launch cap must stay well below the firewall mean
  (firewall lives are counted to detection).
- Do not compare against 0.2077·A + 0.55 (a QSD endpoint fit, not a lifetime line); the slab line −0.091 + 0.2088·A is a
  mix of widths and is inflated by width offsets.
- Checks (all exit non-zero on failure): `check.py all cpu CASES` (local), `modal_app.py::check_every` (engine every
  generation, with negative controls), `::check_defaults`, `::check_periodic`, `::check_keep`, `::check_slab`,
  `::check_patches`. Engine reference cases are rebuilt locally (`check.py engine-cases|periodic-cases|slab-cases`),
  since the engine binary is built for this machine's CPU.

## Current state (2026-11-14T23:30Z)

- Open PR: **#18** (empty patches on a 12×12×8 face). The lead's review (`REVIEW-gpu-pr18.md`) asked for nine text
  fixes; all are applied, and `check_patches` was re-run on the committed kernel (ALL OK). The lead now reads the diff
  against the fix list, waits for CI and merges. Nothing running; no scheduled check-ins pending.
- Merged: #8 (kernels, face law), #10 (fixes), #12 (experiments a–c), #14 (firewall-resolved slabs), #16 (width).
- Budget: about $25.8 of $30 spent this month (2026-11). About $4 left: enough for checks and short runs only. The lead's
  optional 5×8×8 high-statistics run (≈ $14) was declined as unaffordable and is superseded.
- Open scientific threads: empty patches beyond 60 cells need a rare-event estimator (splitting or biased sampling),
  not more GPU time; the perimeter-free cost per cell (second differences, 0.273 → 0.219 over 12–36-cell middles) is
  still falling and its limit (0.16–0.24) is open; the 4×5 rhombus disagrees with the review's CPU run at 1.9–2.6σ
  (the lead is lengthening the CPU run); the cost per cell of a wide unwrapped face lies between ≈ 0.207 and 0.216; the
  s = 3 slab family's curvature is entangled with firewall proximity.
