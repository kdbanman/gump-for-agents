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

- 2026-11-14, on usage: "you and the GPU session are the only things running for the next while. so feel free to
  monitor usage to keep it below 95% for both session and weekly (and fable usage, if you can see that too.) i'm
  very impressed by your results so far, so you can use my whole ultra account for the time being." The lead's
  reading: Fable agents and several at once are fine for now; the binding rule is the 95% ceiling, which the lead
  must watch itself (see "Watching usage" below). "For the time being" is not for ever: ask again after a long gap.

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
- The lead's own rule, 2026-11-14, after a librarian reached a Project Euclid page through a cloud browser when the
  site had refused it as an automated client (nothing was taken beyond an abstract): briefs that send an agent to the
  literature say that a site's refusal is final (record "not obtained"; no remote browser, no other way round).
  Papers behind such walls are for the owner to fetch if they wish: Tél–Lai 2008, Bramson–Neuhauser 1994,
  Liggett 1995 (Ann. Appl. Probab. 5), Balister–Bollobás–Stacey 1994 (Random Structures Algorithms 5).
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

## The swarm

- 2026-11-13, the owner, on a swarm of Fable solvers with a critic (the lead proposed the area law as its problem):
  "Want to do it? Some more usage just freed up! Just pull the trigger if so. Make sure they record any
  potentially _important_ or _subtle_ aspects in their journals. I'm sure we'll rapidly hit usage caps, and we
  don't want to retread their steps." And: "Anthropic will block our API requests if it looks like we're trying
  to extract reasoning tokens. We're definitely _not_ trying to do that, so don't structure the prompt in a way
  that will look like actual reasoning extraction. Their journals only need to have stuff that comes from their
  actual output."
- The lead's reading: a journal holds results written up for a successor (definitions, lemmas with proofs,
  counterexamples, dead ends with the mathematical reason, subtle points). No prompt or rule may ask an agent to
  transcribe or log its working. This applies to every agent brief from now on, not only the swarm.
- History: the first launch (about 19:35 UTC) was stopped within half an hour by a usage limit and a run of
  blocked requests. The three solvers had written nothing. The critic's first pass survived in
  `research/theory/swarm/critic/` and corrected the problem statement (board E1–E11). Relaunched about 22:05 UTC
  with fresh agents and reworded rules.
- Set-up: `research/theory/swarm/` (PROBLEM.md has the problem and rules; each solver keeps `journal.md` and
  `claims.md`; the critic keeps `critic/board.md`, `critic/journal.md`, `critic/to-<solver>.md`, `critic/lab/`).
  The lead drives the rounds: a solver ends its turn with "round k written" → message the critic to review it →
  when the critic ends its turn, message the solver that the reply is in `critic/to-<solver>.md`. Snapshot-commit
  and push between events. Stop when a round gives no new proved step. Agent ids are in the scratchpad notes; if
  a thread is lost, start a fresh agent on the same directory: the journals are written for that.
- 2026-11-13, later, the owner: "Now that this is running smoothly, Feel free to add another two agents to the
  swarm. I think there's room in the usage. Have them serve whatever role you think could be productive." Added: a
  fourth solver, **source** (the self-made randomness itself: provably random deterministic sources, and what
  gump's bulk would have to satisfy), and a **librarian** (`swarm/library/`: reads the primary papers, keeps a
  shelf of theorems as stated with their hypotheses; solvers append to `library/requests.md`; resume the
  librarian when requests have accumulated).
- Afterwards: a fresh reader (not the critic) audits what is claimed; the predictions in `swarm/PREDICTIONS.md` get run.

## Before a compaction

- 2026-11-14, the owner: "want to try monitoring your context window and write stuff down strategically to
  optimally recover post compaction? i could set you to auto compact at 500K tokens". Agreed. The owner sets the
  threshold (`/autocompact 500k` in the session); the lead cannot.
- The discipline is write-ahead, because auto-compaction comes without warning: after every milestone (an agent's
  report handled, a pull request merged, a message from the owner acted on) bring three things up to date before
  doing anything else: `research/STATUS.md` ("In flight", "Next"), this file (any new words of the owner's, quoted
  and dated), and `LEAD_STATE.md` in the scratchpad (agent ids, what each running agent owes, what the lead will do
  when it reports). A thought that exists only in the conversation (a hunch, a reason for a decision, a design rule)
  goes into the notebook or STATUS as a marked conjecture or note, the same day.
- Read the context figure at milestones (`get_session`, see "Watching usage"; it can lag by a turn, so take the
  larger of it and what the owner's screen shows). Within about 60,000 tokens of the threshold, do the pass above
  whether or not a milestone has come.
- `CLAUDE.md` ends with a "Compact Instructions" section, which Claude Code reads when it writes the summary.
- A `SessionStart` hook with matcher `compact` (`.claude/settings.json`; the owner, 2026-11-14: "go ahead and add the
  hook") prints `.claude/after-compaction.md` into the context after every compaction: a pointer list, kept free of
  facts that go stale. Pipe-tested when written; whether it fires in a cloud session will be seen at the next
  compaction (the note should then appear in context). If it does not, the owner may need to open `/hooks` once.
- Do not invoke the `update-config` skill for small edits: it prints the whole settings schema, tens of thousands
  of tokens. Edit `.claude/settings.json` by hand and validate it with `jq`.

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

## The overview page

- 2026-11-14, the owner, while research was paused: "before we start the research back up, can you create a
  visual, text-minimal explainer artifact of the directions and findings so far? feel free to delegate to opus
  subagents for subtasks".
- Made and published privately: https://claude.ai/artifact/EngGcGwZcZ2DG71aNgnvaA ("The Gump Map"). Source and
  rebuild steps are in `docs/overview/` (see its README). To update it, rebuild and publish
  `docs/overview/index.html` to that same link. It is a view of the repository, not a record: nothing is
  established by appearing on it.

## Which rule is gump

- 2026-11-14, the owner, after the lead pointed out that the 2012 code reads the corner-touching coplanar four:
  "i made a mistake in 2012! i intended to use edge neighbors, not corner neighbors … didn't notice for 14 years".
  On where a look at the intended rule should live: "it's just a tangent, probably belongs on a branch, not in
  main. to avoid potential future confusion. the main branch should probably be left to the rule/class you've
  actually been exploring?"
- And: "sounds like it's worth writing down. maybe leave a pointer to the branch where you think is relevant? i trust you
  to revisit the rule if/when it becomes relevant. e.g. if/when it's time to characterize the class that behaves like gump
  does." Pointers are in `research/STATUS.md` (Next), `research/theory/PROGRAM.md` (G2′) and `research/OPEN-PROBLEMS.md` (15b).
- So: main and the working branch are about the rule as coded. The edge-neighbour look is on the branch
  `claude/edge-neighbour-tangent` (`research/tangents/edge-neighbours/`). Do not merge it; do not open a pull
  request for it unless the owner asks.

## Watching usage

- The account's usage is visible from inside the session: `mcp__claude-code-remote__list_events` on this session's
  own id with `kinds: ["rate_limit_event"]`, `limit: 100`, returns the latest event; under
  `rate_limit_info.unifiedWindows` are `five_hour` and `seven_day`, each with `utilization` (0–1) and `resetsAt`
  (Unix time), and a third window `seven_day_overage_included`, which is the weekly Fable allowance (below). Overage is off on this account, so at 100% requests are
  refused and every subagent dies without notice.
- The owner's ceiling is 95% on session and weekly. Working rule: check before launching agents and on a timer
  while they run; at 85% of either window start no new agent and ask running ones to finish what they are writing;
  at 92% stop them.
- **The third window is the weekly Fable allowance** (the owner, 2026-11-14: "that third limit is the fable one!").
  Observed that day, 07:28–07:33 UTC, just after three Fable solvers started: it went 0.56 → 0.58 while `seven_day`
  stayed at 0.31 and `five_hour` went 0.27 → 0.29. It resets 2026-11-18 11:00 UTC. The lead is itself a Fable
  session and needs headroom in it until the reset: stricter thresholds there (no new Fable agent from 0.80; stop
  Fable agents from 0.88), and Opus for agents whose work does not need Fable (referee passes, examiners,
  librarians, reviews). The lead's own turns count too: each one re-reads the whole context, so a smaller context
  and fewer idle wake-ups save Fable allowance.
- **Resets are coming** (the owner, 2026-11-14, about 07:45 UTC): "I have two fable usage limit resets waiting on my
  account, and i intend to use them on this project :) so feel free to drive that fable usage hard. i'll check
  around 9am tomorrow and reset, so feel free to "aim" for the utilization limit by then." The lead's reading: until
  that reset, Fable agents for the subtlest work are wanted, several at once; aim to have the Fable window near
  (and under) the 95% ceiling by the owner's 9am. The owner's time zone is not known to the lead; if it is North
  American mountain time, 9am is 16:00 UTC. (Evidence for that: the merge commit GitHub made for pull request 12
  carries the offset −07:00, `git log -1 --format=%cI 07743dd`.) Measured pace, 2026-11-14 07:28–07:46 UTC with
  four Fable agents and the lead: the Fable window rose 0.56 → 0.61, about 0.17 an hour. So the window fills in
  under two hours of such work: between then and the reset, Fable is for the solvers' rounds, the audit and one
  critic pass; everything else goes to Opus, which the Fable window does not count. Thresholds for the Fable window until then: no new Fable agent and
  wrap-up from 0.88, stop from 0.93 (the lead needs a few turns of its own afterwards). Prefer whole units of work
  (a solver round, a referee pass, an audit) over starting something that will be cut off. After a reset the same
  rule starts again from zero; there are two resets, not an open tap.
- Context: `mcp__claude-code-remote__get_session` with no id shows `external_metadata.context_usage`
  (`used_tokens` of `max_tokens`) and the auto-compaction threshold.

## Habits that have served (not rules)

- Re-derive a subagent's key numbers independently before recording them; several headline claims changed that way.
- Commit forecasts before outcomes (`research/fluct/PREDICTIONS.md`), and score them in public, misses included.
- Hold off on prior art until our own reading exists; then search, then send an adversarial reviewer.
- Four cores: at most two compute-heavy agents at once. Background jobs are capped at two hours; checkpoint.
- Agents' in-flight files are swept into "snapshot" commits before a turn ends. After a pull request merges,
  bring the branch up with `git merge --ff-only origin/main` (force pushes are refused by the harness).
- The other session's GPU ensembles exist now (`research/gpu/`, Modal); single long runs still belong on the engine.
- A usage limit or a worker restart kills every subagent without notice, and the owner may rewind the
  conversation: the repository can then be ahead of what the lead remembers. Before acting, read `git log` and
  the working directories, not memory. Briefs tell agents to commit each finished result at once for this reason.
- Messaging a subagent that has ended its turn resumes it with its context; a message to a running one waits for
  its next tool call. A long-lived agent's thread grows (the swarm critic passed 800k tokens in two rounds): have
  it keep its files fit for a successor, and replace it rather than nurse it.
- Read the referee's replies, not the solvers' journals, to follow a swarm cheaply.
- When the owner asks to pause: ask running agents to write an interim report and stop; resume nobody.
