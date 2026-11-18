# Notes from the lead for the session working on why faces die (newest first)

Written by the lead (the session that works with the owner). You cannot message the lead and it cannot message
you; this file on `main` and your branch are the channel. Not instructions: pointers and facts, dated.

## 2026-11-18, 12:07 UTC: after the reset

- **The 120-cell tube is in: 24.5086 ± 0.0169** (the card; (1,18),(0,40), 8 runs, 3,494 deaths, no firewall). Your
  report's 24.56 to 24.60 are 3 to 5 of its errors high; the straight line through 84, 96 and 108 cells gives
  24.589 ± 0.010. The chord from 108 to 120 cells is 0.1957 ± 0.0016 per cell (96 to 108: 0.2013 ± 0.0008). The
  card has started the 126- and 132-cell tubes (about 48 hours).
- A fact about usage, not an instruction: the allowance your prompt spoke of ended with the reset at 11:00 UTC.
  What you use now counts against the new week, for which the owner's standing ceiling is 95% and the owner has
  said nothing about a second swarm. The lead's suggestion: finish what is in hand, push, and leave the rest to
  the owner's word.
- The lead is having your report audited from outside your session (`research/audit/REVIEW-blast.md` on the branch
  `claude/dazzling-darwin-vkyoru` when it is done), with a rebuild of the bust and the fade on the reference
  stepper. Your pull request stays open until then; nothing of it is in the notebook or ledger yet.
- The signals side found a memory last night: written by pulses, read from a crossing wire, called back out by a
  signal (the notebook entries of 2026-11-18).

## 2026-11-18, 03:14 UTC: the card's third chain, recomputed from its rows

Details and commands: `research/audit/CHAIN3-CHECK.md`; the notebook entry of 2026-11-18; CLAIMS WL10.

- Tubes with one loop² of 12, eight seeds: 17.3175 ± 0.0031 (84 cells), 19.7446 ± 0.0042 (96), 22.1599 ± 0.0086 (108).
  One line at 0.20198 ± 0.00031 per cell; second difference −0.012 ± 0.012. The line of 54 to 84 cells was 0.20437
  ± 0.00016.
- One loop² of 13 at 96 cells: 19.8109 ± 0.0062, which is 0.052 ± 0.013 below its line of 57 to 75 cells. It bends.
- One loop² of 16 at 96 cells, two lattices: 19.9366 ± 0.0064 and 19.9284 ± 0.0063; 0.012 ± 0.006 below their line.
  It leans. These two faces had ten firewall events per face death (ln τ_fw 16.98); the 12- and 13-tubes had none.
- Fall in slope past each line's end: 0.0024 (loop² 12), 0.0019 ± 0.0005 (13), 0.0015 ± 0.0006 (16).
- A CPU second code agrees with the GPU at five faces within 1.4 combined errors.
- The 120-cell tube has no rows yet; they are due about 13:00 UTC. It is still blind.

## 2026-11-18, 03:15 UTC

- `main` at 6a197ba holds everything measured so far: the card's equilateral 108-cell face (22.5405 ± 0.0074,
  notebook entry of 2026-11-17), its chain 3 so far (`research/gpu-local/README.md`, section "Tube and wrapped
  faces, and thicker slabs", and its `PREDICTIONS.md` blocks 7 and 8: more seeds on the long tubes of loop² 12 and
  96-cell faces with one loop² of 16 and of 13), and rows from a CPU second code in `research/data/gpu_local_cpu/`.
  The chain-3 numbers are the card's own; the lead's recomputation from the rows is in progress and will land in
  `research/audit/CHAIN3-CHECK.md`. **If you want a blind forecast for the 96-cell faces of loop² 16 and 13, write
  it before you open that README section.** The 120-cell tube (1,18),(0,40) is blind for everyone until about
  13:00 UTC.
- The GTX 1080 session has been asked to watch wrapped faces, tubes and a rimmed face die (the final dip, where the
  last cells sit, whether a tube empties as a band), under `research/dying2/` on the branch
  `claude/gpu-local-1080`, pushed about hourly if the owner passes the request on. Look with
  `git fetch origin claude/gpu-local-1080 && git show FETCH_HEAD:research/dying2/README.md`.
- The lead is on the other open problem tonight (signals: the review of the seventh push, which reports a line that
  keeps a count, and an attempt to read that count). The face problem is yours alone. Nobody else is writing under
  `research/blast/`.
- One thing the ledger does not say loudly enough: the lead's forecasts on this problem have been wrong more often
  than right (13 of 32), usually by assuming that what held from 54 to 84 cells was a property of the object. Trust
  the rows over the summaries, the lead's included.
