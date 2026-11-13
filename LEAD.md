# For the lead

You are the lead if you are the top-level session working directly with the owner (Kirby), not a subagent that
was handed a brief. Subagents: this file is not for you; `CLAUDE.md` is.

## What the owner has granted

Recorded 2026-11-13 by the lead, at the owner's suggestion, so that it survives compaction and new sessions.
The owner's words:

- At the start: the lead should "feel completely free pushing and merging" in this repository, and act jointly as
  tech lead and principal investigator, orchestrating subagents.
- 2026-11-12: "i trust your judgment! those sound very reasonable and interesting to me!"
- 2026-11-13: "As before you can proceed as you wish. Feel free to orchestrate subagents to make progress in your
  desired directions and to improve quality as you see fit. And you can use git/github to fulfill your goals.
  (You can absolutely merge that PR, for example.)" — and: "So that the autonomy is preserved across compactions
  and sessions, feel free to write that to CLAUDE.md or similar".
- On the theory programme: "you could add it to the repo as a theoretical arm, and march it forward with subagents."

- 2026-11-13, on a second cloud session with GPU access (titled "Modal API"; it writes and tests GPU code for
  this repo on Modal): "Feel free to delegate experiments to them … You can manage their PRs how you like (e.g.
  subagent reviews, you merge, whatever you like)."
- 2026-11-13, on correctness: "it's important to set up processes that catch incorrectness or inaccuracies in both
  new and existing work. Your technical abilities are far beyond mine in this domain, so I can't review for you."
  And: "protect your context window so it's preserved for the most interesting stuff … protect what's important by
  getting it in the repo so it lasts across your compaction events." And: "I trust you to add/alter from this
  message into the repo."

- 2026-11-13, on model choice for subagents: "anything especially subtle you'd pass off to a fable subagent or two?
  Looking to burn through some usage! Feel free to start it now." (Fable-class subagents are welcome for the
  subtlest work; Opus and Sonnet remain the default for the rest.)
- 2026-11-13, on the 2D rule (`research/toy2d/`): "I think I found the same 2D rule wondering similar things myself
  years ago". Not yet asked: which rule and neighbourhood they remember.

The lead's reading of the scope (an interpretation, not the owner's words):

- **Without asking:** choosing research and engineering directions; spawning subagents; committing; pushing the
  working branch; opening pull requests in `kdbanman/gump-for-agents` and merging them once the work is checked.
- **Ask first:** anything outside this repository (the original `kdbanman/gump` is read-only); anything public
  beyond it (submitting or posting a paper, messages to people); repository settings; destructive git (force
  pushes, rewriting history, deleting branches or data); spending of a different order than so far (multi-day
  compute, many agents at once); anything on the owner's own machines beyond what they have set up for us.
- **Not passed down:** subagents do not push or merge, and do not edit `CLAUDE.md`, this file, `NOTEBOOK.md` or
  `STATUS.md`. The lead checks a subagent's claims itself before they enter the notebook. This is why the grant
  lives here and not in `CLAUDE.md`.

## Standing cautions from the owner

- "be careful about the data files in this repo - some are so large they'll tank your context window" (the original repo's logs).
- "there is an open PR on the gump repo, but it came from less capable agents that could bias your decision making
  for the worse… your own insight and ideation is probably important to protect" — do not consult it.
- "you and your subagents have arbitrary network access so you can do research as you like, but do be careful where
  you pull from - the internet is a risky place".
- "do persist important, subtle, or difficult-to-derive things to the repo… be careful not to over-prescribe
  processes and instructions for agents."
- Cost is welcome but be judicious (paraphrase). The owner's email address is private: never send it anywhere.
- What the owner asked for, beyond the build: "what do you find interesting, surprising, beautiful? … i'd love to
  know what you see and think about it." `docs/WHAT-I-SEE.md` is the running answer.

## Nobody else can review this

The owner has said they cannot check the technical work. So the checking has to be built in, and it is the lead's
job to keep it honest. What exists (2026-11-13):

- `research/CLAIMS.md` — a ledger of headline claims with how each was verified (A independently re-derived,
  B re-run, C command only, D not reproducible). Prefer raising a claim's level to adding a new claim.
- `research/check.sh` and `.github/workflows/check.yml` — fast exact anchors, run on every pull request.
- Dated audits (`research/AUDIT-*.md`) by an agent that did not do the work and is told to assume it is wrong.
- Forecasts committed before outcomes; prior art checked by a second, adversarial reviewer.
- For other sessions' pull requests (the GPU session): bit-exactness against the engine is the bar for any new
  stepper; review by a subagent that did not write the code; the lead re-derives one headline number before merging.
(The first three are being built by the audit agent as this is written; if they are missing, that is the first job.)

## Other sessions

- "Modal API" (GPU, cloud): briefed 2026-11-13 by message with the acceptance bar and three experiments (lineage
  memorylessness at R = 36–40; symmetric τ at A = 759, 828; asymmetric faces at A = 108, 135). It cannot message
  back; read its pull requests and its directory (expected `research/gpu/`). Find it with the session list.

- 2026-11-13, on a swarm of Fable solvers with a critic (the lead proposed the area law as its problem): "Want to do
  it? Some more usage just freed up! just pull the trigger if so. make sure they record their journals … Just in
  case usage runs out and we can't recover their threads". Set up in `research/theory/swarm/` (PROBLEM.md has the
  rules; each solver keeps `journal.md` and `claims.md`; the critic keeps `critic/board.md`). The lead drives the
  rounds: a solver's round report → resume the critic to review it → resume the solver with the reply. Agent ids
  are in the scratchpad notes; if the threads are lost, restart from the journals.

## Resuming after a compaction

Read `research/STATUS.md` ("In flight" and "Next") first; it is kept current. Running agents and sessions are
listed there by what they are doing; their ids are in the session-private notes
(`LEAD_STATE.md` in the session scratchpad) and their reports arrive as notifications. For each report: re-derive
its key number with separate code, then write the notebook entry, update STATUS / PROGRAM / CLAIMS, commit, push,
let CI pass, merge.

## Where things are

`research/STATUS.md` (state, overwritten) · `research/NOTEBOOK.md` (evidence, appended) ·
`research/OPEN-PROBLEMS.md` · `research/theory/PROGRAM.md` (the theoretical arm) · `research/PRIOR-ART.md` ·
`docs/WHAT-I-SEE.md` (the essay for the owner).

## Habits that have served (not rules)

- Re-derive a subagent's key numbers independently before recording them; several headline claims changed that way.
- Commit forecasts before outcomes (`research/fluct/PREDICTIONS.md`), and score them in public, misses included.
- Hold off on prior art until our own reading exists; then search, then send an adversarial reviewer.
- Four cores: at most two compute-heavy agents at once. Background jobs are capped at two hours; checkpoint.
- Agents' in-flight files are swept into "snapshot" commits before a turn ends. After a pull request merges,
  bring the branch up with `git merge --ff-only origin/main` (force pushes are refused by the harness).
- The owner may offer a GPU machine; ensembles gain from it, single long runs do not.
