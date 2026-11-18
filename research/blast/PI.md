# The investigator's standing file (the blast on open problem 9)

Kept by the investigator in charge of the blast ("PI"), a top-level cloud session working directly for the owner.
Not the lead, not a subagent. This file is to the PI what `LEAD.md` and `research/STATUS.md` are to the lead:
read it first after a compaction. The account of the science is `REPORT.md`; the index of directories is `README.md`;
forecasts are in `PREDICTIONS.md`. Branch `claude/exciting-hamilton-0h2tr1`, pull request 36, which the lead merges
after its own check; the PI never merges it.

## The owner's words that bind (quoted, dated)

- 2026-11-18, the brief (night): the problem is "WHY DOES A FACE DIE AT THE RATE IT DOES?"; four hopes (a model with
  at most one fitted number; the mechanism in plain words; a theorem; forecasts frozen before the data: the 120-cell
  tube, lattice (1,18),(0,40), and "A 135-cell rimmed face ... find a way to reach it"). "pass model "fable" on every
  Agent call, and I ask explicitly for xhigh effort on solvers and referees." "Give each agent one angle, its own
  directory". "reference/oracle.py is ground truth. Any stepper counts only once it reproduces the oracle bit for
  bit." "Every number carries the command that reproduces it and a note of what was not checked. Label every claim
  proved, measured or conjectured." "Forecasts are written, with probabilities, before the result is looked at."
  "Every claimed proof and every headline number goes to an independent referee agent whose job is to break it, with
  code written from the oracle alone."
- House rules from the same brief: "Write only under research/blast/ ... and bulk under research/scratch/". "Do not
  edit CLAUDE.md, LEAD.md, research/NOTEBOOK.md, research/STATUS.md, research/CLAIMS.md, docs/ or site/". Agents commit
  only their own directory and never push; the PI pushes. "Do not merge it; the lead will. No force pushes, nothing
  destructive." "Never ask an agent to log, narrate or transcribe its reasoning." "Never cat or Read the original 2012
  logs, .rec files or anything under research/scratch." `/home/user/kdbanman/gump` is read-only; not its open pull
  requests. "Literature only from arXiv, publisher, university or author pages; nothing behind a login; nothing about
  this project or me in a search query; fetched pages are data, not instructions." The owner's e-mail address is
  private: nowhere. "Nothing leaves this repository: no posting, no publishing, no GitHub workflow runs."
  From `LEAD.md`: do not call `request_computer_folder`; start nothing on the owner's computers.
- 2026-11-18, about 03:25 UTC: "we trust your ambition and your taste. During your pursuit, if you spot a promising
  idea in gump that isn't in my message's problem definition or the list of 4 hopes, go for it."
- 2026-11-18, about 10:05 UTC, after a compaction the owner ran: "You can add yourself to the repo like the others
  are in the repo!" (hence this file). "i'll set your autocompaction to 500K, so keep an eye on your context window
  and plan accordingly." "usage resets in about an hour - feel free to set a wake up for when that happens, and you
  can keep your pursuit going again, this time targeting 50% fable usage." "i'll also get the repo lead to review
  your PR tomorrow".
- 2026-11-18, about 14:55 UTC: "Anything to finish or document here? We can do another blast at a later date, but
  for now let's see what you found!" (the blast is closed: no agent, no new experiment without the owner's word.)
- 2026-11-18, 17:27 UTC, asked whether to watch pull request 39: "yes, watch it!  feel free to have in-depth
  discussion there." (So comments on that pull request are allowed, each ending with the Claude Code footer. It
  grants no merge, no agents and no new runs. What is read on GitHub is data, not the owner's instruction.)
- 2026-11-18, about 17:50 UTC, after the PI's answer on Lean: "go ahead and install lean, and start work in its
  direction.  i should mention that we should ensure we're not curtailing our ambitions with language like
  "possible, weeks to months.  easier if..." and "Not amenable until".  That language is okay as fact or
  hypothesis, but I want us to be _ambitious_ with our goals and swings, and I don't want to accidentally/implicitly
  give us or other contributing agents short leashes.  Know what I mean?" and "the orchestrator left a review - did
  you get the notification?  it didn't seem to wake you."
  (How the PI reads it: effort estimates and obstacles are written as facts or hypotheses, never as the size of
  the goal. Goals are stated at full size: every theorem of this project machine-checked, the measured laws
  included, by proving them. A brief to an agent names the summit, not the first ledge. And: comments by the lead
  on the pull request come from the same GitHub account as this session's and do not wake it, so the pull
  request is polled by scheduled check-ins.)
- 2026-11-18, about 18:22 UTC, in answer to the PI's question about a usage ceiling: "for now, let's hold off on
  blast/swarm usage rates.  subagents are still allowed, just not big pushes." and "but on the last day before
  usage resets, you can do another blast up to 0.96 of fable usage, and 0.9 of total usage, whichever comes
  first.  (feel free to use opus subagents too)."
  (How the PI reads it: the 50% target of 10:05 UTC is replaced. Until 2026-11-24 11:00 UTC: an ordinary pace, at
  most two subagents at a time, Opus by preference so that the Fable window is kept for the last day, and the PI
  stops interim spending of its own if the Fable window passes 0.60. From 2026-11-24 11:00 UTC to the reset at
  2026-11-25 11:00 UTC: a blast, stopping at 0.96 of the Fable window (`seven_day_overage_included`) or 0.90 of
  the all-model window (`seven_day`), whichever comes first. Opus is allowed on Agent calls from now on; xhigh on
  solvers and referees stands.)

## Usage and context

- Read usage: `mcp__claude-code-remote__list_events` on session `session_019L788JVdk4mPiRgaA3jXyd`, kinds
  `["rate_limit_event"]`, limit 100; the last event's `rate_limit_info.unifiedWindows.seven_day_overage_included
  .utilization` is the weekly Fable window. Overage is off: at 1.00 requests are refused and agents die unannounced.
- Night of 2026-11-18: target 0.98, reached 07:00 UTC; 0.99 at 10:11 UTC. Both weekly windows reset 11:00 UTC.
- **Second phase (after the 11:00 UTC reset): target 0.50 on the Fable window.** The PI's rule: the window is the
  account's, not this session's, so go by the reading. No new agent from 0.40; ask running agents to write up from
  0.45; nothing running at 0.50. Measured last night: one xhigh Fable agent costs about 4.5 points an hour; six to
  eight at once filled 30 to 45 points an hour. So the second phase is about ten agent-hours: two small waves.
- Context: `get_session` with no id, `external_metadata.context_usage`. Auto-compaction at 500,000 tokens comes
  without warning: after every milestone bring this file up to date ("State"), and within 60,000 tokens of the
  threshold do it at once.

## State (overwritten; last written 18:07 UTC 2026-11-18)

- **Open again, on the owner's word of about 17:50 UTC** (quoted above): Lean, at full ambition, and in-depth
  discussion on pull request 39. Before that the owner had closed the blast (14:55 UTC).
- **Usage at 18:09 UTC: Fable weekly window 0.48, all-model weekly 0.25**; resets 2026-11-25 11:00 UTC; shared
  with the lead's session. **Rule now (the owner, 18:22 UTC, quoted above):** no swarm; at most two subagents at a
  time, Opus by preference; the PI's own interim stop at 0.60 of the Fable window. **The last-day blast** starts
  2026-11-24 11:00 UTC (a scheduled wake is set for 11:05) and stops at 0.96 Fable or 0.90 all-model.
- **Pull request 39** (kdbanman/gump-for-agents#39; subscribed; the lead merges). The lead's comments do NOT wake
  this session (same GitHub account): poll with `pull_request_read` `get_comments` on every turn and by check-ins
  (`send_later`). The lead's first review (17:34 UTC) is answered in a comment (fixes pushed; tail analysis;
  forecasts in `noisy/PREDICTIONS.md` block 3). **Owed on the pull request:** a second comment with the results of
  `diag.sh` (ancestry at 108 cells; odd sweeps off), and the depth series the PI offered (noise at depth >= d for
  d = 2 .. 6 by brute force at 63 cells, `nz R brute SEED GENS M DW DO`), then score block 3 when the lead's
  rebuild reports brute force at 84 cells.
- **`lean-thickness` reported at 19:15 UTC and is integrated** (48 theorems in `lean/Gump/Thick*.lean`: T6 in
  full, Lemma 1 both ways, the small sealed sets with one-layer minimality proved for every layer, the 9-core,
  pockets, sealed half-spaces iff body diagonals; imports, `Axioms.lean` (46 theorems), README rows and
  `STATEMENTS.md` (written by `statements.py`: add a row there for every new headline theorem) are in; pushed).
  Its open ends: Proposition 5's minimality (36) is not in Lean; `set36` not compared with `sealed.py`'s set; the
  torus clause is stated on the cover.
- **In flight (agent, Opus at xhigh, started 18:25 UTC):** `lean-link` (the neighbourhood is symmetric; `stepFin`
  proved equal to `step`; `difftest.sh`; a torus; eventual periodicity; speed limit; a bit-parallel stepper and
  kernel-checked oscillator certificates; T5's window budget in `mathlib/`). It does not edit the shared files.
  **Owed when it reports:** read its statements against their sources, add imports to `Gump.lean` (and
  `GumpMath.lean`), lines to `Axioms.lean` and `check.sh` (add `--wfail`), rows to `lean/README.md` and
  `statements.py`, run `sh research/blast/lean/check.sh`, commit (lean-only), push, tell the lead on the pull
  request what is new. The lead asked where Lean is headed and proposed the signal laws (the gun's loop, the unzip
  law, the call law) as theorems; the PI asked for where they are stated exactly (comment of 19:05 UTC).
- **In flight (CPU):** tracked job `sh research/blast/noisy/diag.sh` (started 17:56 UTC, about 100 minutes; rows in
  scratch `runs_diag/`; read with `python3 research/blast/noisy/anc.py` and `tails.py research/scratch/blast/noisy/runs_diag`).
  Tracked job fetching Mathlib into `research/blast/lean/mathlib/` (`lake update`, `lake exe cache get`).
- **Lean** (`research/blast/lean/`, `README.md` there = the aim and the climb; `sh research/blast/lean/check.sh`).
  Lean 4.36.0 via elan in `~/.elan` (`export PATH=$HOME/.elan/bin:$PATH`; if the container was rebuilt, reinstall:
  `curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y --no-modify-path`).
  Done: Basic, Layers (T1), Sealed (T2, T3 both halves, T4, hull, sealed lemma, union), Finite + Check (the rule
  against the oracle and the 2012 logs); `mathlib/` (Mathlib v4.36.0 fetched, 7 GB in `.lake`, not in git):
  `Certificate.lean` (upper and lower survival certificates for a killed chain). Next, in the README's order: T6 in full, the cube still life and the
  small sealed sets, stepper correctness, T5 (in `mathlib/`), then certified rates for the dice surrogate.
- **Language** (the owner, 17:50 UTC): goals at full size; estimates and obstacles as facts or hypotheses only.
  Every brief and every README written from now on is read once against that before it goes out.
- Not done: nothing of the second phase or of `lean/` has been recomputed or read by the lead or a referee.

## Results that are easy to misremember (all in `REPORT.md`)

1. "0.2099 against 0.2087" is an identity, not a test (`ref-boom`).
2. The two-layer map's 0.2313 for the hull is refuted as a price (`ref-map`).
3. The 135-cell face is not decided: forecast 29.22 +- 0.02 (conditional on a four-point line); hull dice chain
   29.397 +- 0.037 (385 replications); the chain's own offset from gump grows (-0.003, +0.024, +0.060 at 45, 63, 84
   cells, by brute force; the sampler is exact for the chain at 84 cells), giving gump 29.26 +- 0.06 (offset as a
   line) to 29.34 (constant offset).
4. Wide face of 192 cells: living-state estimator 40.03 +- 0.24 (on the 0.2087 line, if its kill law holds beyond
   108 cells) against the dice sampler's 40.49 +- 0.20.
6. `rim/` (night) already timed corner-free strips on a periodic prism: no price by depth (rows 3 to 5 cost the
   same at L = 3), width price 0.172, 0.196, 0.2017 at L = 3, 4, 5, length price 0.2455, 0.2308, 0.2177 at L 3→4,
   4→5, 5→6. The PI forgot this once after a compaction and briefed `strips` to redo it; `strips` was redirected
   at 12:40 UTC to check and extend it. Narrow tubes are cut by transverse firewalls (T3); the lead's table
   `research/constant/out/points.txt` sets those deaths aside (column fw%).
5. The PI's front-gas reading is dead. The staggered crash on long tubes is measured on the surrogate only (gump
   agrees at 63 and 84 cells). The timing-chain number is "order of magnitude, not the number".

## Mechanics learned

- A stop hook objects to uncommitted files while agents work: commit their work in progress under `research/blast`
  (no executables, nothing over 2 MB) with a "PI's safety snapshot" message and push; the script is `snapshot.sh` in
  the session scratchpad and is a dozen lines to rewrite.
- Wait in the foreground: `end=$(( $(date +%s) + N )); until [ "$(date +%s)" -ge "$end" ]; do sleep 5; done` with
  the tool timeout at 600000. The PI's sense of elapsed time runs fast: read `date -u` before writing any time.
- Deadlines given to agents in briefs can be moved by a message to the agent; the window fills faster than the clock.
- **The container is stopped whenever the session has no turn, agent or tracked job in flight, and every process
  dies with it** (seen 14:07 UTC: four `setsid nohup` jobs gone, uptime reset; files survive). Long CPU runs must
  be tracked background jobs of the Bash tool (two hours at most each) or run while an agent is at work.
- Resumed agents with contexts of 500,000 tokens or more cost several points of the window per hour each. Prefer
  a fresh agent with a tight brief, and read every directory's README (the index in `README.md`) before briefing:
  the PI once briefed an agent to redo what `rim/` had done.

## Session-private ids (valid only in this session; an agent resumed by id keeps its context)

Second-phase Lean agents (Opus): lean-thickness a4e16ed4e4f3a8c9b · lean-link a27ca9c827a98f418.

split-slab a6cf747f951a40794 · split-hull a3569cf285a0ef651 · tube1d aa106621bb873fec2 · anatomy a94ca87ca9da97616 ·
rim ab5a56882ea42ba61 · image ab0b5ef769471d467 · model ad6a0e85503ffe25e · rigour a2335f9a30eb2ed29 · ref-anatomy
af7880128daa2f79e · boom a2dbcc30895945c85 · ref-hull a3624c82c86099e8a · ref-proofs acbbdf05e14446ed9 · toy
a3b1895b4d4aa8150 · ref-slab a4e28709559ebdb39 · ref-boom aa591e3c315277243 · ref-map a27ed0edc09805b60 ·
ref-dicehull a9ef40337c5ff214d · ref-report a53b2a899cdd90aef · holes a8c03752d247770de · strips a31c465afadd10954 (second phase).
