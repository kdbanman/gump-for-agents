# Seventh signals push: a census of ends of the rake train beyond the closed bounds

2026-11-17 to 18. The standing account of push 7 (the lead's brief: look for a listener among ends of the rake train
beyond the bounds already closed). Everything here was run on the owner's Windows machine (8 worker processes at
most, below-normal priority, no GPU). Numbers carry the command that reproduces them; run times are wall-clock on
the loaded machine.

## Answers

**(a) A listener: none within the bounds below.** **(b) An end that answers a hole with U: none.**
**(c) Yes for the wire-B edge, at both ends, and with it a finite line that keeps a count.** Nothing absorbs E.
**(d) The census and its bounds are in the tables below.**

### (c) Ends that stop a wire-B edge, and a line that keeps a count

When E meets a hole, the stream between two edges becomes wire B (sixth push, section 31 of
`research/signals/README.md`). The lower edge runs down into the receiving end and the upper edge runs up into the
gun.

- **Receiving ends.** Of the 741 ends of the 3 x 3 tube at C <= 37 (period dividing 4), **125 stop the lower edge
  and stand as an end of wire B**: the end region is periodic (period dividing 8) on generations 200..216, and the 14
  units in front of it are wire B, cell for cell, at every one of those generations (`census7.py`, outcome
  `wireB:cap`). 103 others stand but send a front up that turns the wire B into a different wire (`wireB:wall`),
  509 are destroyed, and 4 leave periodic debris without a wire. The 125 include all 113 ends that heal both a hole
  and K0, plus 12 others.
- **Guns.** Of the 67 guns of the 3 x 3 tube at C <= 37 (period dividing 4; the sixth push's list, recounted:
  68 entries, 67 distinct), **5 stop the upper edge and stand as an end of wire B** (`census7.py --guns`). All five
  are among the 11 guns that absorb U.
- **A count that lasts, on the infinite train.** Put E and n holes 3 rakes apart in front of the 20-cell end #70.
  For n = 1, 2, 3, 4 it leaves a standing wire B capped by the end, with a B' stretch of 0, 3, 4, 5 units (counting
  the edge unit). The four final states differ pairwise. Each is periodic on generations 150..166 and 250..266, and
  equal at 158 and 258 (`record7.py c37.json`, 3 s).
- **A finite line that keeps a count.** One of the five guns, 80 units of train, and one of the 125 ends mirrored to
  the -v end (M(x, y, z) = (z - 4, y, x + 4), README section 9) make a free-standing oscillator of period 4: 419
  cells for gun #4 and end #70. Put E on its stream at generation 1 (train phase 1) at unit 32, and n holes at units
  48, 54, ... (3 rakes apart).
  - E meets the first hole. The lower edge of the wire B runs into the end and the upper edge into the gun; both
    stop.
  - The later holes write wire B' into the wire B.
  - **The whole line becomes a standing oscillator of period 4: wire B capped at both ends.** For n >= 2 holes it
    holds n units of wire B' (B with (1,0,2) off and (0,2,3) on, read cell for cell at n = 2, 3, 4, 6) and one unit
    of its edge. For n = 1 it is plain wire B. The object is different for each n.
  - Command: `line7.py gc37.json c37.json --N 80 --n 1,2,3,4` (2 s).
  - Robustness: all 45 pairs of the 5 guns with 9 sampled ends of the 125 keep the count (n = 1..4, spacing 3).
    Spacings 4 and 5 do too. Spacings 1 and 2 leave the same plain wire B for every n.
  - **On the oracle (`verify7.py`, records `line-*`):** the line alone has period 4; after E and 1, 2, 3, 4 holes the
    whole object (a finite pattern on a ring torus with dead margin, so the statement is exact for the infinite
    lattice) has period dividing 8 on generations 880..896. That makes it periodic for ever. PASS.
  - E alone, with no hole, destroys the line: E kills every gun on file.
  - What this is not: the count cannot be read or reset. It is written once, because after it the train is gone
    (the line is wire B). And E has to be put on the stream from outside; one cell removed anywhere on the stream
    makes one (section 30).

### (a), (b): nothing listens, nothing answers

**[proved within the bounds, by complete enumeration and exact runs]** In the bounds of the table below, every
(end, event) pair has one of the outcomes listed there:
- healed: the whole window equal to the undisturbed run;
- dead: the end not restored when the difference has run 80 units up the stream;
- for the wire-B edge, one of the four wireB classes.

**No end is left alive and changed** by any word of holes or any down-running signal (no listener). **No end
returns a signal**, U or any other (no safe up-channel). **No gun survives E or N1**. The dichotomy of the fifth push
(heal or burn) holds for every signal kind at C <= 39. Which kinds an end forgives is a property of the end. Only 9
outcome vectors occur among the 6,196 ends, and the same 9 occur among the 741. "Proved within the bounds" here
means the following:
- The lists are complete: every cube DONE.
- Each end is checked against the same per-signal tests: placement 24 units upstream, the arrival phases listed,
  runs to 1,500 generations.
- Each outcome is an exact computation of step7, which is checked against the oracle.
- A sample of each outcome class is re-run on the oracle.

## Bounds and census

The ends of the rake train, period dividing 4 unless stated otherwise. A cell bound C means everything inside the
planes x+y-z, x-y-z <= C of `sat_gun.build`'s region, with units < 6 the plain train. Counts are of distinct ends
up to translation and time shift. Each list contains every end of the smaller C.

| tube | ends | C | list entries | distinct ends | complete | enumeration (cdcl7 via pool7) |
|---|---|---|---|---|---|---|
| 3 x 3 | receiving | <= 35 | 90 | 89 | yes | 147 s, 1 core |
| 3 x 3 | receiving | <= 37 | 753 | 741 | yes | 43 min, 5 workers |
| 3 x 3 | receiving | <= 39 | 6,286 | 6,196 | yes | 50 min, 4 workers |
| 3 x 3 | guns | <= 37 | 68 | 67 | yes | ~10 min, 1 core |
| 3 x 3 | guns | <= 39 | 873 | 867 | yes | 34 min, 1 worker |
| 5 x 5 | receiving | <= 23, 25 | 0 | 0 | yes | 0.1 s, 1.8 s |
| 5 x 5 | receiving | <= 27 | 3 | 3 | yes (787 leaves) | 5.1 h, 3 to 5 workers |
| 3 x 3 | receiving, period dividing 8 | <= 35 | 90 | 89 | **no**: 374 of 403 leaves | stopped at 06:30 UTC on 2026-11-18 after about 19 h, 1 to 2 workers |

**The 5 x 5 tube at C <= 27** (64 free cells; every end of period dividing 4 inside it): **3 ends**, of 14, 14
and 15 cells. They are shorter than any end of the 3 x 3 tube, whose smallest is at C = 31, and two of their
generation-0 cells lie outside the 3 x 3 tube. One heals every word and H and dies on K0, and walls the wire-B
edge. One does the same but dies on the edge. One dies on every word, heals K0, D3 and D4, and **caps wire B**. None
listens or echoes (`summary7.py c_fb27_5.json`). C <= 25 holds no end.

**Period dividing 8 (3 x 3, C <= 35): not closed.** In the 374 of 403 leaves searched, the 90 solutions are the 89
ends of period 4 already known at C <= 35. No end of period exactly 8 was found, and their census outcomes are those
of the period-4 census. The 29 open leaves were never searched, so "no period-8 end" is not proved.

Receiving ends of the 3 x 3 tube at C <= 39: 6,196, all of period 4. Sizes at generation 0 of the list entry run
from 17 to 38 cells, mode 27. Outcomes per event (`summary7.py c39_p0.json c39_p1.json c39_p2.json`):

| event | healed | dead |
|---|---|---|
| each of the 8 words of holes, H, and D5 (= two H) | 5,141 | 1,055 |
| K0, D3, D4 (= two K0) | 1,212 | 4,984 |
| D6 | 1,223 | 4,973 |
| D7 | 1,115 | 5,081 |
| N4 | 24 | 6,172 |
| lower edge of wire B | cap 1,223, wall 695, periodic debris 36, dead 4,242 | |

At C <= 37 (741 ends), in the same order: 599 / 142 (holes, H, D5); 130 / 611 (K0, D3, D4); 125 / 616 (D6);
113 / 628 (D7); 1 / 740 (N4); wire-B edge: cap 125, wall 103, debris 4, dead 509.

The outcome vectors over the 17 events (h healed, d dead). The columns: the 8 words of holes; then K0, H, N4, D3,
D4, D5, D6, D7; then the wire-B edge.

| ends (C <= 39) | ends (C <= 37) | words | K0 H N4 D3 D4 D5 D6 D7 | wire-B edge |
|---|---|---|---|---|
| 4,002 | 485 | h | d h d d d h d d | dead |
| 1,115 | 113 | h | h h d h h h h h | cap |
| 651 | 93 | d | d d d d d d d d | wall |
| 163 | 16 | d | d d d d d d d d | dead |
| 108 | 12 | d | d d d d d d h d | cap |
| 53 | 7 | d | h d d h h d d d | dead |
| 44 | 10 | d | h d d h h d d d | wall |
| 36 | 4 | d | d d d d d d d d | debris |
| 24 | 1 | h | d h h d d h d d | dead |

Guns of the 3 x 3 tube at C <= 39: 867, all of period 4. Every one dies on E, N1 and EE. 89 absorb U exactly; the
rest die on it. On the upper edge of wire B: 78 cap it, 21 become walls, 33 leave debris, 735 die. At C <= 37 (67
guns): U absorbed by 11, wire-B edge capped by 5.

## Method, and how each tool was checked

No SAT solver is installed on this machine (pysat is absent and nothing was installed), so:

- **`cdcl7.cpp`**: a small CDCL solver written for this push.
  - Two watched literals, 1UIP learning with minimisation, VSIDS, phase saving with default phase false, Luby
    restarts, LBD clause deletion.
  - Projected all-solutions enumeration: blocking clauses on the generation-0 free cells, which determine the orbit.
  - Checkpoint and resume.
  - Every model is checked against every original clause before it is written.
  - Checked by reproducing the fifth push's enumerations, which were made with CaDiCaL: 90 solutions at C = 35 and
    753 at C = 37 (3 x 3, period dividing 4); also 68 guns at C = 37.
  - Built with `g++ -O3 -march=native -std=c++17 -o cdcl7.exe cdcl7.cpp -static` (WinLibs gcc 16.2).
- **`cnf7.py`**: writes the fifth push's instance as DIMACS, using `sat_gun.build` unchanged. The instance: ends of
  period dividing T = 4 mult in the tube [lo, hi] and the planes x+y-z, x-y-z <= C, with units < 6 tied to the
  train. `cnf7.py` also decodes solutions; each decoded end is re-stepped (`restep`, the test of
  `sat_gun.check_gun`). `shim.py` stands in for pysat so that the signals library imports; nothing calls a solver
  through it.
- **`pool7.py`**: runs one instance as a tree of cubes.
  - A cube is split on two more projection variables when its run passes 240 s.
  - The children of a cube partition it, so the deduplicated union of every cube's solutions is the instance's list.
  - It resumes from `tree.json` and the cube files.
- **`step7.c` / `step7.py`**: a stepper on a window of the 5 x 5 tube. Modes: the plain train below the window and
  dead above it; dead on both sides; or a ring.
  - **Checked bit for bit against `reference/oracle.py` by `check7.py`: ALL PASS.** The train, the four signals of
    `objects/echo-train.json`, its four one-cell events and its six meetings were run on the oracle's ring torus
    H = 96 and compared on the whole state at every generation. The gun of the json with U in front of it was run on
    a torus H = 128 for 60 generations.
- **`signals7.py`**: the train's rigid signals, found from scratch.
  - Inputs: every one-cell flip in the 5 x 5 tube on two units at four phases, and every two-cell flip in the
    3 x 3 tube.
  - Each kind is proved to ride for ever by the two-generation identity of `prove_echo.py`.
  - It reproduces the sixth push's one-cell census (24 vanish / 66 break / 22 ride: 8 up, 14 down) in both frames.
  - In the gun frame (the line frame of `echo-train.json`) the kinds are K0, H, N4, U, E, N1 with the json's own
    cells.
  - Written to `signals7.json` (absorber frame; 8 down kinds: K0, H, N4, D3, D4 = two K0, D5 = two H, D6, D7) and
    `signals7_5f.json` (gun frame).
- **`census7.py`**: dedups ends up to translation and time shift (the key of `census_ends.py`). Then:
  - **Receiving ends** are sent the eight words of holes of `census_ends.py`, every down-running kind (both arrival
    phases for ends of period 8), and the lower edge of wire B.
  - **Guns** (`--guns`) are sent U, N1, E, the pair EE, and the upper edge of wire B.
  - **Outcomes:** healed (whole window equal to the undisturbed run), echo:K (end restored, one rigid signal of a
    known kind leaving), up:other, dead (the end not restored when the difference reaches 80 units upstream),
    alive (candidate). For the edge: wireB:cap, wireB:wall, wireB:periodic-no-wire, wireB:dead.
  - Checked by reproducing the fifth push's census of the 741 ends exactly: 599 heal every word and 142 die on
    every word; hole against K0, 113 / 486 / 17 / 125. It also reproduces the sixth push's gun results: U absorbed
    by exactly 11 guns, E and N1 killing all.
- **`record7.py`, `line7.py`**: the count, on the infinite train and in the finite line.
- **`make7.py`, `merge7.py`, `verify7.py`**:
  - `make7.py` builds oracle records for every candidate and ten ordinary (end, event) samples per outcome class
    (three for the slow wire-B classes).
  - The finite train of each record is placed by the speed limit, so that its tail cannot reach the compared units
    within the claim's generations.
  - `merge7.py` writes `objects7.json`.
  - `verify7.py` checks the records with `reference/oracle.py` and numpy alone and prints PASS or FAIL per record.
- **`ends7.cpp`**, a transfer-matrix enumerator (paths in a graph of unit columns), was tried first and dropped.
  The train alone has 2.8 million successor states even with one unit of lookahead. Nothing here rests on it.

## Runs (reproduction)

Every command below runs from `research/scratch/signals/p7` (not in git), with
`PY=C:\Users\kdbanman\.venvs\gump-gpu\Scripts\python.exe` and `S=../../../signals/push7`. Build `cdcl7.exe` (in
p7) as in the Method section; step7.dll is built by step7.py on first use, which needs WinLibs gcc in
`%LOCALAPPDATA%\Microsoft\WinGet\Packages`.

- **Stepper check.** `$PY $S/check7.py fb37_3.list.json`: ALL PASS. Parts R and G are the oracle comparisons
  (about 4 min); part W compares train mode with dead mode on 20 ends.
- **Signals.** `$PY $S/signals7.py --two` and `$PY $S/signals7.py --two --train5f`: 1.5 min each.
- **An enumeration.**
  - `$PY $S/cnf7.py write fb C LO HI MULT STEM`.
  - `$PY $S/pool7.py STEM 5 W 240 2`; the 5 x 5 and period-8 trees were later re-run with split 900.
  - `$PY $S/cnf7.py decode STEM`.
  - The stems used: `fb35_3` (`fb 35 1 5 1`), `fb37_3`, `fb39_3`, `g37_3` / `g39_3` (`5f 37 1 5 1` / `5f 39 1 5 1`),
    `fb27_5` (`fb 27 -1 7 1`), `fb35_3p8` (`fb 35 1 5 2`).
- **Census.**
  - `$PY $S/census7.py c37.json fb37_3.list.json`: 10 min.
  - `$PY $S/census7.py c39_pI.json fb39_3.list.json --part I/3` for I = 0, 1, 2: about 25 min each, in parallel.
  - `$PY $S/census7.py gc37.json g37_3.list.json --guns` and the same for g39: 20 s and 3 min.
  - Tables: `$PY $S/summary7.py CENSUS.json ...`.
- **The count.**
  - `$PY $S/record7.py c37.json` (3 s).
  - `$PY $S/line7.py gc37.json c37.json --N 80 --n 1,2,3,4 [--gun g --end e] [--s s]` (2 s).
- **Oracle.**
  - `$PY $S/verify7.py $S/objects7.json --maxL 260` (210 records, about 80 min on the loaded machine): ALL PASS.
  - `--minL 261` (40 records with long rings, the wire-B classes and the record runs, about 10 min each): 41 PASS,
    0 FAIL (`final7.txt`).
  - `objects7.json` holds:
    - the line records (`line-*`), including `distinct` claims between consecutive n;
    - the record runs (`record-*`);
    - for the C <= 37 and C <= 39 receiving ends and guns, ten samples per outcome class (three for the wire-B
      classes) plus an `orbit` record for each sampled end;
    - the 5 x 5 C = 27 end.
- **Data in git.** `wireB_caps.json` lists the 125 receiving ends and 5 guns of C <= 37 that cap wire B, with their
  outcome vectors. The full tables (`ends_3x3_C37.json`, `ends_3x3_C39.json`, 3.3 MB) are in p7 only; regenerate them
  with `summary7.py ... --out`.
- **Wrap-up.** `bash $S/finish7.sh "2026-11-18 06:30"` waits for the open trees and checks, stops them at that
  time, then decodes, runs the census, and writes and checks records into `final7.txt`.

## Not checked

- No second SAT solver and no UNSAT certificate. The completeness of every list rests on `cdcl7` and on the cube
  partition in `pool7`.
  - The solver was checked only by reproducing the CaDiCaL lists of earlier pushes: 90 solutions at C = 35, 753 at
    C = 37 (741 ends), 68 guns at C = 37.
  - No list at C = 39 was produced by another solver.
- The outcomes are exact runs of step7, which is oracle-checked, under the census's definitions. Several things
  are outside them:
  - transients longer than 1,500 generations;
  - signals placed other than 24 units upstream;
  - arrival phases other than the ones listed;
  - two different signals in succession, other than the words of holes;
  - the upper part of a run after the difference has gone 80 units up the stream ('dead' means the end was not
    restored by then, not that it was watched burning);
  - other events: one-cell changes of an arriving rake beyond those that make the listed kinds (the fifth review's
    418 events per end were not re-run), and the five composite kinds are pairs of signals, not new signals.
- The wire-B classes are read at generations 200..216 only. That the 125 caps stand for ever, and the count on the
  infinite train, are measured (to 266 generations), not proved. The finite line is proved periodic for ever on the
  oracle (a finite object, whole state).
- The 5 x 5 tube was closed only to C <= 27, and period 8 not at all (29 open cube leaves at C = 35). No 5 x 5 guns
  were enumerated.
- The tables count ends by C, the plane bound of `sat_gun.build`, for the 3 x 3 tube. Ends longer than C <= 39 are
  not seen, nor ends outside the tube.
- Oracle records are samples (ten per outcome class), not every pair.

## Forecasts scored

(`PREDICTIONS.md`, written before any census result.)

1. 0.85, enumerator reproduces 741: the transfer-matrix enumerator was abandoned. The CDCL route reproduced 741
   exactly, so the forecast is scored as true in substance.
2. 0.55, the 3 x 3 set is infinite: not tested (the transfer graph was abandoned).
3. 0.5, the 5 x 5 tube closed to a bound of at least 6 units: no. It closed at C <= 27, about 2 units beyond the
   train.
4. 0.6, more than ten times as many 5 x 5 ends: no (3 ends at C <= 27; the 3 x 3 tube has none there).
5. 0.07, a listener: no, within the bounds.
6. 0.08, an end answering a hole with U: no.
7. 0.05, a 5 x 5 gun surviving E: no 5 x 5 gun census was run; no 3 x 3 gun survives E at C <= 39.
8. 0.15, an end that stops the lower edge of wire B: **yes** (125 at C <= 37; 1,223 at C <= 39).
9. 0.8, the 5 x 5 ends heal or die on H: true (all 3).
10. 0.6, period 8 adds nothing at C = 35: none was found in 374 of 403 leaves; not closed.
11. 0.35, some end echoes: no (3 x 3, C <= 39).

## Final state (2026-11-18 08:00 UTC)

Nothing of push 7 is running. `final7.txt` is the wrap-up log (`finish7.sh`).
- Oracle (`verify7.py`): 210 PASS with rings of at most 260 units. The heavy run (`--minL 261`) gave 41 PASS. The
  new 5 x 5 and period-8 records with short rings gave 39 PASS. **0 FAIL** in all three (`final7.txt`). Whether the
  long-ring part of the 47 new records is wholly inside the heavy 41 was not cross-checked.
- The cube trees in p7 are resumable: re-run `pool7.py fb35_3p8 4 W 900 2` to close period 8.
