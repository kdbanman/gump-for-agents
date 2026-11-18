# Push 8b: reading a standing line from a second wire

2026-11-18. The standing account of push 8b. Question: can a signal on a second, separate wire tell whether the
unit of push 7's standing line it passes is wire B or wire B′, with the line left unchanged? Tags: **[proved]** (a
construction the oracle has stepped, or an exact argument), **[measured]** (counts, with the command; the stepper is
`st.c`, checked against the oracle by `check_st.py`), **[conjectured]**. Commands run from this directory; times are
wall-clock on a shared 4-core machine. Forecasts: `PREDICTIONS.md`. Push 8 (`../push8/README.md`) read along the line
itself and looked at a second wire only in parallel; nothing here relies on it except where named.

## Answer

**A non-destructive read: yes, with a pair of pulses.** A second wire B is laid across the line at 60 degrees and two
pulses of wire B in adjacent units are sent along it.

- beside a unit of **wire B** one pulse **comes back** to the sender and nothing goes on;
- beside a unit of **wire B′** nothing comes back and nothing goes on.

In both cases the line and the second wire are afterwards cell for cell what they were, and no cell of the line's
tube differs at any generation from the run without the probe. On the oracle, on push 7's own lines written with E
and 1, 2, 3 and 4 holes. A second read of the same kind uses a wire C and two pulses three units apart (beside B′
they pass; beside B a different train goes on and one pulse comes back).

**With a single pulse there is no such read** on wire B or wire C as the second wire, in any orientation, at any
interacting distance, in either phase (section 3).

**What it is not: a cell that can be written with the reader in place.** The reader has to be put beside the store
after the write. No pulse of the store passes under any of the 24 reading placements, no wall or edge of a stretch
can stand under one, and push 7's write burns at them (section 5). The unit under the reader is read-only.

| what | command (prints PASS lines and `ALL PASS`) | time |
|---|---|---|
| the stepper `st.c` equals the oracle, every generation: soups, a register write, a pulse on a ring, push 7's line with E and 2 holes for 920 generations | `python3 check_st.py` | 18 s |
| the echo read on push 7's line, n = 1, 2, 3, 4 holes, oracle only | `python3 verify_read.py objects/read-echo-B-line.json` | 88 s |
| the pair read with a wire C on push 7's line, n = 1..4, oracle only | `python3 verify_read.py objects/read-pair-C-line.json` | 91 s |
| the same two reads beside a short capped wire B / wire B′ | `python3 verify_read.py objects/read-echo-B-small.json`, `… objects/read-pair-C-small.json` | 3 s, 4 s |
| the smallest cell found: 128 cells, written by three one-cell removals, read by the echo | `python3 verify_read.py objects/cell-small.json` | 1 s |

`verify_read.py` imports numpy, json and `reference/oracle.py` only. For every stored value in the file it checks:
A the store, built from its start cells and the write, stands (repeats after 4 generations); B store and reader
together are, 16 generations on, exactly the two alone (minus the listed junction cell, where there is one) and
stand; C with the probe, no cell of the store's tube ever differs from the run without it; D at a given generation
the two runs differ in exactly the listed cells (the signal); E from a given generation on the two runs are
identical; F the stores differ pairwise and the signal differs exactly between the two stored values. All boxes are
tori large enough that no live cell comes within 4 sites of the seam (asserted every generation).

## 1. The store, rebuilt

- **[proved by the oracle run]** Push 7's line (record `line-N80-gun4-end70-n1` of `../push7/objects7.json`, 419
  cells at generation 0) with E = (65,2,−62), (66,0,−63), (66,0,−61) and n holes (99,2,−96) + 6j·(2,0,−2), j < n,
  flipped at generation 1, is at generation 900 a standing object (repeats after 4 generations), different for
  n = 1, 2, 3, 4 (`verify_read.py`, checks A and F; n = 2 also cell for cell against `st.c` at every generation
  0..920, `check_st.py`).
- **[measured]** `python3 line.py` (1 s) prints the lines in letters, `python3 posmap.py --ns 1,2,3,4,5,6` (56 s)
  for n up to 6: n = 1 is plain wire B on units 4..79; n ≥ 2 has wire B′ on units 41..40+n and the edge unit f (all
  four family sites) on unit 41+n. Units: unit u holds the cells with x in {2u, 2u+1}; one unit on is (2,0,−2).
- The wires (`lab.py`, even generation, unit 0): wire B (0,1,2), (0,1,4), (1,0,0), (1,0,2), (1,0,4); wire B′
  (0,1,2), (0,1,4), (0,2,3), (1,0,0), (1,0,4). No symmetry maps B onto B′ at the same generation;
  (x,y,z) ↦ (−z, y, 6−x) maps B at an even generation onto B′ at an odd one (`python3 wires.py`, 1 s, ALL PASS:
  the capped wires B, B′, C stand, their pulses run rigidly both ways and the caps swallow them).

## 2. The read

**The reader** (`cell.READERS['b13']`): a capped wire B (`wires.capped_B(-14, 14)`: the eater cap of the register, 28
units, the half-turn image of the cap; 169 cells, period 2) mapped by (x,y,z) ↦ (82−x, z, −84−y). Its axis is
(−1,−1,0), at 60 degrees to the line's (1,0,−1); it crosses the line at line unit 42, at its own unit −1. Store and
reader together are exactly the union of the two alone at every generation, although cells of each have neighbours
in the other (a *transparent* crossing).

**The probe**: the two cells of a pulse B flipped in each of the reader's units −10 and −11 at an even generation
(in the object: (100,21,−86), (101,20,−84), (102,23,−86), (103,22,−84)).

**[proved by the oracle run]** (`objects/read-echo-B-line.json`; probe at generation 20 after the reader is put in)

| line | 30 generations after the probe, the run differs from the unprobed run in | identical to the unprobed run |
|---|---|---|
| E and 1 hole (unit 42 is wire B) | exactly 2 cells, (95,18,−84), (96,17,−86): one left-going pulse B, 6 reader units back from the crossing | from 52 generations after the probe (st: from 50) |
| E and 2, 3, 4 holes (unit 42 is wire B′) | nothing | from 52 generations after the probe (st: from 21) |

- **[measured]** A single pulse on this reader is swallowed at the crossing beside either unit, everything restored
  (`python3 survey.py B`: the class `gone/gone`). The read is in the second pulse, one unit behind: beside B it is
  turned round, beside B′ it is swallowed too. Nothing goes on past the crossing in either case, which is why the
  reader's far half can be cut to two units (section 6).
- **[measured]** Repeats, and either launch phase: `python3 cell.py repeat` (3 s): for n = 1..6, launched at a
  generation divisible by 4 or 2 later, and again after the first read, the same outcome and exact restoration each
  time. (That a read can be repeated also follows from check E: the state after it is the state without it.)
- **The mirror reader** `b8`: (x,y,z) ↦ (84+x, 2+z, y−78), axis (1,−1,0), same probe, same outcomes (identical
  from 52 generations after the probe for n = 1).
- **The wire C read** (`cell.READERS['r246']`, `objects/read-pair-C-line.json`): a capped wire C (clock caps, 172
  cells) at the same place; beside wire B the crossing is a *junction* (one reader cell, (85,4,−84), is missing,
  the store untouched). Probe: two pulses p> three units apart. Beside B′: both pass unchanged. Beside B: 40
  generations after the probe the difference is 9 cells, a changed train going on and one p< going back. Restored
  in both cases (oracle: identical from 70 generations after the probe; st: from 62).

**All the reads found** [measured; `python3 junc2.py B` 168 s, `python3 junc2.py C` 112 s: every non-parallel
placement of section 3 in which the reader stands beside both a capped wire B and a capped wire B′, two pulses 1 to
8 units apart from either end; a read = both objects exactly restored 240 generations later and different signals
travelling 44 generations after the launch]: 16 placements of a reader B and 8 of a reader C, of 416 and 316 that
stand beside both. In `lab.SYMS` numbering (g, phase, t; t up to sliding along either wire):

| reader | placements | probe | signal beside B / beside B′ (cells differing 44 generations on) |
|---|---|---|---|
| B | g = 8, 13 (from the left end), 11, 14 (from the right end), phase 0 | 2 adjacent pulses | 2 (the echo) / 0 |
| B | g = 24, 29 (left), 27, 30 (right), phase 1 | 2 adjacent pulses | 0 / 2 |
| B | g = 16, 21 (right), 19, 22 (left), phase 0 | 2 adjacent; 2 pulses 2 apart | 6 / 4; 4 / 10 |
| B | g = 32, 37 (right), 35, 38 (left), phase 1 | 2 adjacent; 2 pulses 2 apart | 4 / 6; 10 / 4 |
| C | g = 8, 13, phase 0 | 2 pulses 3 apart | 9 / 4 from the left end, 12 / 6 from the right end |
| C | g = 32, 37, phase 1 | 2 pulses 3 apart | 9 / 6 left, 12 / 4 right |
| C | g = 16, 21, phase 0 | 2 pulses 3 apart | 6 / 9 left, 4 / 12 right |
| C | g = 24, 29, phase 1 | 2 pulses 3 apart | 4 / 9 left, 6 / 12 right |

The translations are in `research/scratch/signals/p8b/junc2_{B,C}_0of1.jsonl` after the two runs (for instance
g = 13: t = (−2,0,0), crossing at store unit 0; g = 8: t = (2,2,4), crossing at store unit 1).

## 3. A single pulse does not read (bounds)

Placements: the reader is x ↦ g(x) + t, g one of the 40 signed permutations that do not map the wire's axis to ±
itself, t every even translation up to sliding along either wire for which some cell has neighbours in both
footprints, at both relative phases: **1056 placements** per reader (the same number for search radius 6, 7 and
9). Stores: a capped wire B and a capped wire B′, 28 units; then push 7's line.

- **[measured] Uniform stores, one pulse** (`python3 survey.py B`, 76 s; `python3 survey.py C`, 58 s). *clean*
  = the pulse's fate is known and store and reader are exactly restored.

  | reader | burn beside both | clean beside both | of those: pass/pass, gone/gone, other/other (equal) | clean beside both and different |
  |---|---|---|---|---|
  | wire B, pulse B | 600 | 308 | 280, 20, 8 (the pulse is doubled) | **0** |
  | wire C, pulse p> | 712 | 292 | 284, 4, 4 | **0** |
  | wire C, wide pulse (`survey.py Cw`, 58 s) | 712 | 0 (the clock caps do not take the wide pulse) | | 0 |

  The remaining placements burn beside one store or leave something changed beside at least one.
- **[measured] On the line, by position** (`python3 survey2.py B --part 0/2`, `… 1/2`, about 300 s each;
  `python3 survey2.py C --part i/2`, 193 s each; then `python3 reads.py FILES`): every one of the 1056 placements at
  each crossing unit 37..49 of the n = 3 line (B, wall, B′, edge, B), one pulse at two launch delays, 13,728 runs
  per reader. Placement classes with two different clean outcomes at two positions: **0** for either reader.
- **[measured] Parallel readers** (`python3 survey3.py B`, 73 s; `python3 survey3.py C`, 71 s): the 8 symmetries
  with g(v) = ±v, every transverse offset, two alignments, both phases, beside the n = 1 and the n = 3 line, 1888
  placements each: the pulse passes beside both, or something burns. Reader C has 16 placements that stand beside
  both lines where the pulse passes for n = 1 and burns the n = 3 line. Push 8's ring scan of a parallel wire B
  found the same nothing.
- **[measured] The rake train as the signal** (`python3 survey4.py --part 0/2`, `… 1/2`, 740 s and 796 s, over the
  10-minute guide: split further if rerun): the beam (`../objects/beam-5f.json`) in 2112 classes at 13 positions
  of the n = 3 line, 27,456 runs: 7,806 no effect, 19,567 burn, 83 a flicker or a burnt store; no train modulated
  with both surviving.
- **[measured] Words of up to three single pulses from both ends** (`python3 junc.py B`, 98 s; `python3 junc.py C`,
  76 s): of the placements standing beside both stores (416, 316), 16 each leave a *mark* (a standing change at the
  crossing, the store untouched); no word of ≤ 3 pulses ends with both objects restored and different outputs.

## 4. Reads that cost something

- **[measured] A reader that latches** (`python3 cell.py table`, 2 s; wire C at `r246`, `r132`, single pulses on
  push 7's line, n = 1..6). Beside B′ every pulse passes and everything is restored. Beside B the first pulse
  passes, 8 cells go back and a 7-cell mark stays in the reader; every later pulse is swallowed and everything is
  restored. The store is never changed, so from the second pulse on this too is a read (a pulse arrives or does
  not) that leaves the store alone; the reader is not what it was before its first use. A marked reader moved
  beside B′ stands, and the next pulse converts 152 cells of it. **[conjectured]** The wire C pair read of section 2
  is this mechanism with the second pulse close enough to take the mark away again.
- **[measured] Destructive reads** (`python3 reads.py FILES --all` on the `survey2.py` output): for instance reader
  B, g = 3, phase 0, t = (−2,6,2) at unit 0: transparent at every position, the pulse passes at wire B positions
  and burns the store at positions 40..44 of the n = 3 line. Reader B, g = 19, phase 0: beside B′ the pulse is
  doubled and all is restored; beside B the reader is converted into another wire, the store intact.
- **[measured] Dead positions** (`python3 posmap.py`, 27 s; all 24 reading placements at every crossing unit
  34..52 of the lines n = 1, 2, 3, 5; `--ns 1,2,3,4,5,6`, 56 s). On the line every placement gives the same two
  signals as beside the uniform stores. Each reads correctly at every unit of plain wire B away from the stretch and
  at the inner units of the stretch, and each has units next to the wall and next to the edge where it does not
  stand (the store or the reader is changed within 160 generations). With w the first unit of wire B′ and e the
  edge unit: `b13` (and C at g = 13) fails at w−2, w−1, w and e; `b8` (and C at g = 8) fails at w, e, e+1, e+2.
  No placement is free of dead units at either end. On push 7's line unit 42 = w+1 is safe for every n ≥ 1 (n = 1
  has no stretch); a reader at unit 41+j compares n with j but destroys the store when n = j (b13) [checked n ≤ 6].

## 5. The reader freezes the unit it reads

All [measured], `st.c`.

- **Store pulses do not pass under a reader** (`python3 rw.py cross24`, 2 s): for each of the 24 reading placements
  beside a plain capped wire B, a right-going and a left-going pulse of the store, at two delays: 96 runs, the
  object is permanently changed in all 96 (fire on both wires in most).
- **Push 7's write does not pass a reader** (`python3 rw.py train`, 13 s; `python3 rw.py early`, 13 s). Beside the
  line before the write (the rake train running), 22 of the 24 placements burn at every unit 38..49; reader B at
  g = 21 and g = 22 stands beside the train at the odd units. With either of those in place, or `b13`/`b8` at unit
  42, E and n = 1..6 holes do not produce the standing line: the front that turns the train into wire B burns at
  the crossing (60 + 12 runs, none written).
- **A stretch cannot be released under a reader** (`python3 rw.py erase`, 3 s): push 8's one-cell release (the
  stator (0,1,2) of the unit before the wall removed; without a reader it leaves plain wire B, reproduced here) with
  `b13`, `b8`, `r246`, `r132` beside an inner unit of `d^k f`, k = 2, 3, 4, 6: 44 arrangements in which the reader
  stands, 0 end with a store (41 burn, in 3 the store burns away whole and the reader survives).
- **A stretch cannot be grown over a reader** (`python3 rw.py grow`, 10 min for the four readers; one reader:
  `python3 rw.py grow b13`): stretch `d f` or `d d f` with its wall 1..6 units to the right of the crossing or its
  edge 1..6 units to the left, pulses born (one stator removed) at every unit on the reader's side of it and up to
  4 units beyond the crossing, 1 to 6 times, every 4, 6 or 8 generations: 2484 runs per reader. In 178 to 183 the
  store changes and still stands with the reader as it was: the stretch grows towards the reader (144), is
  released whole (34), or the store burns away whole (0, 3 or 5). In none does the stretch reach the crossing; where
  a store is left the reader afterwards still reads "B". The other 2,301 to 2,306 burn.
- **A probe on the reader puts no signal on the store** (`python3 inject.py B`, 68 s; `python3 inject.py C`, 60 s):
  one pulse, or two pulses 1, 2, 3 apart, on every placement standing beside plain wire B (436 and 328): 1522 of
  1744 and 1280 of 1312 leave the store's tube untouched away from the crossing; the other 222 and 32 start fire.
  No probe makes a pulse of the store. So a second wire of these two kinds reads but does not write.

Together: within these placements a stretch can be written and erased on one side of a reader with the reader in
place, but the unit under the reader keeps the value it had when the reader was put there.

## 6. The cell, as far as it goes

`objects/cell-small.json` (`python3 small.py make 4 4 4 2 2` writes it, `python3 small.py search`, 9 s, finds the
sizes). **[proved by the oracle run]** `python3 verify_read.py objects/cell-small.json`.

- **Store**: a capped wire B on units −4..3 (push 8's cell: cap, 8 units, the cap turned round), 69 cells, period 2.
- **Write 1**: remove three live cells: (−6,1,8) and (4,1,0) at generation 0 (push 8's *set*: a right-going and a
  left-going pulse stop each other and leave `d f` on units −1, 0), and (4,1,0) again at generation 40 (push 8's
  *add one*: `d d f` on units −1, 0, 1; 70 cells, standing by generation 120). **Write 0**: nothing.
- **Reader**: a capped wire B on its own units −4..1, 59 cells, mapped by (x,y,z) ↦ (−2−x, z, −y); crossing at
  store unit 0, the second unit of wire B′. It is put in when the store stands (generation 120 of the store).
- **Read**: flip the four cells of two pulses B in the reader's units −3 and −4 at an even generation. 12
  generations later the run differs from the unprobed run by one left-going pulse B (stored 0) or by nothing
  (stored 1); 36 generations after the probe the cell is exactly as it was, for both values.
- 128 cells in all. The search took the shortest reader first (own units −a..b−1, launch d units before the
  crossing: a = 4, b = 2, d = 2 is the first that works) and then the shortest store for this write.
- **On push 7's line** the same protocol is `objects/read-echo-B-line.json`: write = E and n holes at generation
  1; the reader (169 cells) is put in at generation 900; stored 0 is n = 1, stored 1 is n ≥ 2.

What is missing from a memory cell: the reader cannot be there during the write (section 5), so the protocol has a
step that is not a signal (putting 59 cells in place); once the reader is in, the value under it cannot be
changed; and the echo ends in the reader's own cap: nothing was built that makes the pair of pulses or uses the
echo.

## 7. Tools, and how each was checked

| file | what | check |
|---|---|---|
| `st.c`, `lab.py` | sparse hash stepper on the infinite lattice (or a ring along (1,0,−1)); `lab.py` builds it with gcc on first use | `python3 check_st.py`: equal to `oracle.step` cell for cell at every generation on three soups, a register write, a pulse on a ring of wire B, and push 7's line with E and 2 holes for 920 generations |
| `wires.py`, `line.py` | capped wires B, B′, C; push 7's lines and their letters | `python3 wires.py` (ALL PASS); the lines by `verify_read.py` check A |
| `verify_read.py` | the judge: oracle only | reads nothing of this directory but the object file |
| `make_read.py`, `small.py` | write the objects (expected cells computed with `st.c`, then judged by the oracle) | the five objects PASS |
| `survey.py`, `survey2.py`, `survey3.py`, `survey4.py`, `reads.py`, `show.py`, `show3.py` | section 3; kymographs of one placement | `st.c` only |
| `junc.py`, `junc2.py`, `posmap.py`, `cell.py`, `rw.py`, `inject.py` | sections 2, 4, 5 | `st.c` only; the reads they found are the objects |
| `survey5.py` | the other 30 pulse-carrying wires of the first push as readers | written, **not run** |

`posmap.py`, `rw.py cross24` and `rw.py train` read the output of the two `junc2.py` runs (280 s together), and
`reads.py` that of `survey2.py`; all bulk output goes to `research/scratch/signals/p8b/`.

## 8. Not checked

- On the oracle: the five objects only (reader `b13` and `r246` at unit 42, n = 1..4; the short stores; the small
  cell). Everything else is `st.c`: n = 5, 6, the mirror readers `b8`, `r132`, the other 20 reading placements, other
  crossing units, the second launch phase, all of sections 3, 4, 5.
- Only the line of gun 4 and end 70 at N = 80.
- Readers: straight capped wires B and C with their own pulses, and the rake train. Not the other pulse-carrying
  wires (`survey5.py`), not wire B′ or C′ as the reader, no bent or branching reader.
- Probes: one pulse; two pulses up to 8 units apart from one end; words of up to three single pulses from both
  ends. Not three or more pulses close together, not pulses from both ends at once, not the doubled pulse.
- Section 5 is a list of what was tried, not a proof that the unit under a reader cannot be changed. `rw.py erase`
  and `rw.py grow` cover four of the 24 placements; pulses were born by removing one stator, at three spacings.
  `inject.py` sends its probes from the reader's left end only and looks at the store 40 generations on.
- Why the pair reads: no mechanism beyond the kymographs (`cell.kymo`, `show.py`).
- Two readers on one line, and a reader beside the gun or the mirrored end, were not tried.

## 9. Forecasts scored

Fifteen forecasts (`PREDICTIONS.md`, written before the first run). True: 1 to 9 and 15; false: 10 to 14. Mean
squared error 0.136 (always 0.5 would give 0.25).

- Most wrong: "a non-destructive read" was given 0.30 (forecasts 7 and 15), and "nothing at all" 0.45.
- Not foreseen: that single pulses read nothing anywhere and a pair one unit apart reads cleanly; the forecasts
  spoke of "the pulse". Forecast 7 is counted true for the pair; for one pulse it is false.
- As forecast: no cell with the reader present during push 7's write (10), no rewritable cell (11), no clean
  signal put on the store (14; 254 probes start fire there).

## 10. Where I would go next

1. **A write that passes a reader.** The obstruction is the same in all 24 placements: the crossing is transparent
   to the standing wire and to nothing that moves on it. Other reader wires (`survey5.py`), or a reader beside the
   store rather than across it that needs three or more pulses, are untried.
2. **Use the echo.** The read returns a pulse on the wire it was sent on. A wire-B gun that makes adjacent pairs
   and a stretch on the reader itself that counts returned pulses (push 8's add one) would turn "store holds B"
   into a count kept elsewhere, with signals only.
3. **Why a pair.** The first pulse leaves the crossing in a state that lasts a few generations and differs between
   B and B′; the second pulse meets it. Working that state out would say which other wires can read.
4. **The latch of section 4** is a one-bit store in the reader set by the store's value: a copy operation.
