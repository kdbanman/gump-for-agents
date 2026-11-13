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
