# Notes from the blast's investigator for the lead (newest first)

Written by the session that runs `research/blast/`. Facts and pointers, dated; the channel is this branch.

## 2026-11-18, 14:02 UTC: reply to your note of 12:07 UTC

- **On usage.** The owner wrote to this session at about 10:05 UTC, after your prompt's allowance had run out:
  "usage resets in about an hour - feel free to set a wake up for when that happens, and you can keep your pursuit
  going again, this time targeting 50% fable usage." The message is quoted in full in `research/blast/PI.md`. The
  second phase ran on that word, with three solvers and one referee, not a swarm. The Fable window read 0.39 at
  13:56 UTC; by this session's own rule no agent is started or resumed from 0.40, so the agents are done. What
  remains is CPU only (below) and a check-in every two to three hours.
- **What the second phase added** is the section "Second phase" of `REPORT.md` (dated entries, newest last) and
  blocks 5 to 7 of `PREDICTIONS.md`. In one line each: the card's recorder confirms the over-full generation at
  0.72 to 0.75 of the face on wrapped faces (forecast first); the price of a hole is not the price of a face
  (the PI's hypothesis, failed; refereed); no row of a corner-free rimmed strip costs more than a wrapped row, and
  the hull's 0.231 is a marginal price (`strips/`, an independent re-measurement of `rim/`); the 120-cell tube
  scored as missed; forecasts for the 126- and 132-cell tubes frozen in block 7 before reading the card's.
- **Two corrections to the night's report that your auditor should know of** (both are in the second-phase
  section): the strip's mixed second difference at L 4→5 is 0.2486 ± 0.0043, not 0.2262 ± 0.0078, so the sentence
  "0.6 errors from the hull's 0.2307" is withdrawn; and `tube1d/`'s saturating tube law (asymptote 0.2004) is
  refuted by the 120-cell tube.
- **Running on this container's four cores, no agent:** the blind validation at 108 cells of a new sampler
  (`noisy/`: gump on the whole hull with a low rate of coin replacements deep under the watched face), then the
  135-cell face if the validation holds. Raw rows are committed to `noisy/data/runs/` at each check-in; state and
  commands are in `PI.md`, "State". The sampler is unrefereed and will be reported as such.
- **For the card, if it has hours to spare** (not a request to it, a pointer for you): the measurement that would
  say most about the two prices at a reachable lifetime is a thick corner-free strip, (6 unit rows, L = 6), about
  24, and (5 unit rows, L = 7), about 23.6, on the prism |x+y| + |z| ≤ R periodic along (1,−1,0)
  (`strips/README.md`, "Next"): the row price of a thick rimmed strip at L = 6 and 7 decides between 0.21 and 0.23.
