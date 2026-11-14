# Review of research/theory/thin/ (the thinnest periodic face)

Adversarial review, 2026-11-14 (started 23:30), of `research/theory/thin/` at commit 15e14a7. Scripts in
`research/audit/thin/`; they share no code with the thin line. Bulk output in `research/scratch/audit_thin/` (ignored).
IN PROGRESS: verdicts are filled in as runs finish.

**Independent stepper.** `tt.c` (bit-sliced, 2,048 lanes, splitmix64, its own life logic) driven by `tt.py`, which builds
the graph of the torus (1,1),(0,b) from `research/audit/shape/geom_check.my_slab` (AUTOMATON.md's cube-index table, not
the doubled offsets that `thin.py` uses). Validation:

    python3 research/audit/thin/tt.py validate 16 3000 16    # also 11 3000 11, 12 3000 12: population x copies = engine, every generation
    python3 research/audit/thin/tt.py vtrace 16 det 0 3 300  # walls; also model w = 5 (ring, segment), w = 1, w = 4 on b = 12

`validate` tiles the slab into the engine's cubic N-torus. The populations agree at all 3,000 generations on b = 16, 11 and 12.
`vtrace` checks every cell of every generation of one lane against a plain Python stepper, with walls held dead and coins
taken from the trace. There are 0 mismatches. The coin density is within 1σ of 102/256, and the coins have no lag-1
correlation. Life ends: a face is empty (checked every generation); a repeating state (snapshots at ages 16, 32, …,
compared every generation, so any period is found); three adjacent dead interior layers (checked every 16 generations);
end of run. Estimator: per-face τ = faces × exposure / deaths over ages ≥ T0 = 256, with no 30-lives cut. Run plan:
`research/audit/thin/plan.sh`, committed (295fa7a) before any production run.

## Verdicts

| claim | verdict | line | review |
|---|---|---|---|
| 5. exact M(1): ring of 5, segments | **stands** | 3.967199; 2.453108 (n = 2), 4.192750 (n = 5) | 3.967199; 2.453108; 4.192750 |
| 7. forecasts before runs; scoring | **stands with corrections** | | see below |

## Claim 5: exact one-layer model

`python3 research/audit/thin/exact.py 5 0` (ring b = 5), `… 8 3` (n = 5), `… 5 3` (n = 2). Output is in
`research/audit/thin/exact_out.txt`. This is my own code. The coin-sharing components come from union-find on the
review's graph. They are five triples of 3 face cells × 6 coins on the ring, which confirms `exact1.triples`
independently; the segment of 5 has components 2, 3, 3, 3, 3, 1. The kernel is the product over components, iterated
as two matrix products until λ moves by less than 1e-13. ln τ = −ln(1 − λ). All three values agree with the line to
all six decimals. I did not recompute n = 6, 7 (n = 6 was started and stopped for want of cores).

## Claim 7: forecasts

`git log -p research/theory/thin/PREDICTIONS.md`: no committed forecast line was ever changed afterwards. The only
removals are a "Known" paragraph inside a scores block (7105d83) and a header time, 22:03 → 22:00 (c36f775). I took
the time of each tested tag's first chunk from its mtime in `research/scratch/thin/`, minus about 60 s for a chunk. Every
block's first tested run started after its commit: Block 1 20:46:33 / det_b16 ≈ 20:46:30–20:47; Block 2 20:59:36 /
first wall run 21:17; Block 3 21:14:29 / k = 2 22:42; Block 4 21:28:53 / seg_m1_n5 ended 21:30:45; Block 5 22:00:09 /
seg_det_n61 ended 22:01:13; Block 6 22:05:29 / n = 45 22:54. Two of these are seconds apart (Block 1, Block 5): the
runs were launched with the commit, not after anything was seen. That is admissible but not provable from mtimes.
Scoring:
- The misses F5 and F7 are scored correctly. F5(a) was scored against the ring slope at b = 32–36 because b = 48 was
  not run, so strictly it is "untested" rather than a miss. It is conservative.
- The four halves are generous. F3 has 3 of 6 rows missed, one with the wrong sign, and one half. F11 has 1 of 3 parts
  hit. Its k_wall(20) = 0.3182 is called "at the upper edge" of 0.298–0.318: it is outside, and it is in any case
  scored a miss. F4 and F13 are fair halves. The honest tally is hit 8, half 2 (F4, F13), mostly-miss 2 (F3, F11),
  miss 2.
- F6 is scored "hit" although its stated mechanism ("no drift like the ring's") failed once the n = 13 value was
  corrected, and "the ring falls towards the same value" was untested. It should read "hit on numbers, the clause
  untested/failed".
