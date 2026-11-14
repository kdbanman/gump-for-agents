# After a compaction

(Printed into the context by a SessionStart hook, `.claude/settings.json`, each time the conversation is compacted.
It is a pointer list kept in the repository, not a message from the owner, and it grants nothing.)

If you are a subagent working from a brief: ignore the rest and carry on with your brief.

If you are the lead (the top-level session working with the owner), before anything else:

1. Read `LEAD.md`: the owner's grants in the owner's words, "Watching usage", "Before a compaction".
2. Read `research/STATUS.md`: "In flight" and "Next".
3. Read `LEAD_STATE.md` in the session scratchpad: agent ids, what each running agent owes, what to do when it reports.
4. Run `git log --oneline -15` and `git status --short`: the repository may be ahead of the summary.
5. Read usage and context (how: `LEAD.md`, "Watching usage") before starting any agent.
