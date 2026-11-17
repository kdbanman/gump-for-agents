# Seventh signals push: a census of ends of the rake train beyond the closed bounds

2026-11-17. The standing account of push 7 (the lead's brief: look for a listener among ends of the rake train
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

[filled in below from the census tables]

## Bounds and census

[filled in from the runs]

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

[filled in]

## Not checked

[filled in]

## Forecasts scored

[filled in]
