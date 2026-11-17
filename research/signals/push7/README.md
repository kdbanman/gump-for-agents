# Seventh signals push: a census of ends of the rake train beyond the closed bounds

Draft, 2026-11-17 07:00 UTC; being updated as runs finish (see "Runs" at the end for what is still open).

Question (the lead's brief): is there a **listener** (an end of the rake train that survives a signal and is durably
changed by it), (b) an end that answers a hole with **U**, (c) an end that absorbs **E** or **stops a wire-B edge**
and survives, or, failing all three, (d) the census itself with exact bounds.

## Results so far

- **(c) is answered yes for the wire-B edge, at the receiving end.** Of the 741 ends of the 3 x 3 tube at C <= 37
  (period dividing 4), **125 stop the arriving lower edge of wire B and stand**: after E has met a hole upstream and
  the stream between the two edges has become wire B (sixth push, section 31), the lower edge runs down into the
  end and the end becomes a standing end (period dividing 8) of wire B, with wire B in front of it equal cell for
  cell to the wire B of the meeting (`census7.py`, outcome `wireB:cap`). 103 others stand too but turn the wire B in
  front of them into a different wire behind a front that runs up (`wireB:wall`), 509 are destroyed, 4 leave
  periodic debris without a wire. **So the B' count of the sixth push lasts:** E against a word of n holes 3 rakes
  apart, in front of the 20-cell end #70, leaves for n = 1, 2, 3, 4 a standing wire B capped by the end, with a
  B' stretch of 0, 3, 4, 5 units at units -29..-25 (the four final states differ pairwise, each periodic on
  generations 150..166 and 250..266 and equal at 158 and 258; `record7.py c37.json`, 3 s). This holds on the
  infinite train; in the finite line the upper edge still reaches the gun.
- **Validation of the new tools against the fifth and sixth pushes** (all exact):
  the C = 35 and C = 37 enumerations give 90 and 753 solutions, as CaDiCaL did; the 753 are 741 distinct ends; their
  census reproduces the fifth push's outcome vectors (599 heal every word of holes, 142 die on every word; hole x K0:
  113 / 486 / 17 / 125); the one-cell flip census of the train reproduces the sixth push's 24 vanish / 66 break /
  22 ride (8 up, 14 down) in this frame and in the line frame.
- **(a), (b) at C <= 37, 3 x 3, period dividing 4:** no end is left alive and changed by any of the eight
  down-running signal kinds found here (K0, H, N4 and five more made by two-cell flips), and no end returns any
  signal (E, U, N1 or other) for any of them: every (end, signal) pair heals or dies. (The fifth push had this for
  words of holes; K0 healed or killed; the other kinds are new.)

## Method

No SAT solver is installed on this machine (pysat absent; nothing installed). So:

- `cdcl7.cpp`: a small CDCL solver written for this push (two watched literals, 1UIP with minimisation, VSIDS, phase
  saving with default phase false, Luby restarts, LBD clause deletion), with projected all-solutions enumeration
  (blocking clauses on the generation-0 free cells) and checkpoint/resume; every model is checked against every
  original clause before it is written.
- `cnf7.py`: writes the fifth push's instance (`sat_gun.build`, unchanged: ends of period dividing T = 4 mult inside
  the tube and the planes x+y-z, x-y-z <= C, units < 6 tied to the train) as DIMACS, and decodes solutions; every
  decoded end is re-stepped (`restep`, the test of `sat_gun.check_gun`).
- `pool7.py`: one instance as a tree of cubes (splitting a cube on two more projection variables when its run passes
  240 s), 3 to 8 worker processes, resumable at any point; the union of the leaves' lists is the instance's list.
- `step7.c` / `step7.py`: a stepper on a window of the 5 x 5 tube (the plain train below the window, dead above; or a
  ring). Checked bit for bit against `reference/oracle.py` by `check7.py` (ALL PASS: the train, the four signals of
  `objects/echo-train.json`, its four one-cell events and six meetings on the oracle's ring torus H = 96, whole
  state at every generation; the gun of the json with U in front of it on a torus H = 128, 60 generations).
- `signals7.py`: the train's rigid signals from scratch (every one-cell flip in the 5 x 5 tube on two units at four
  phases, every two-cell flip in the 3 x 3 tube), each proved to ride for ever by the two-generation identity of
  `prove_echo.py`. Written to `signals7.json` (absorber frame) and `signals7_5f.json` (gun frame = the line frame).
- `census7.py`: dedup up to translation and time shift (key of `census_ends.py`), then each end is sent the eight
  words of holes of `census_ends.py`, every down-running kind of `signals7.json` (and both arrival phases for ends
  of period 8), and the lower edge of wire B; outcomes healed / echo:K / dead / alive (candidate) and, for the edge,
  wireB:cap / wall / periodic-no-wire / dead (definitions in the docstring).
- `verify7.py`: oracle-only check of saved records (initial cells, flips, claim), PASS / FAIL.

The transfer-matrix enumerator `ends7.cpp` (paths in a graph of unit columns) was tried first and abandoned: the
train alone has 2.8 million successor states (one unit of lookahead), so the state space is far too loose; it is kept
for the record but nothing here rests on it.

## Runs

(to be completed)
