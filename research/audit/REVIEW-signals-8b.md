# Review of signals push 8b (a read from a second wire)

2026-11-18. Adversarial review of `research/signals/push8b/README.md`. The review was cut short by the session's
usage ceiling: what is below is complete for the checks that were run, and the last section lists what was not
reached. Verdicts: **confirmed**, **corrected**, **refuted**, **not checked**. Commands run from
`research/audit/signals8b/`; times are wall-clock on the shared machine.

Tools of this review, none of them the push's: `q.c` (a sparse stepper written here, neighbour table from the
cube-index form of `docs/AUTOMATON.md`), `qa.py` (the oracle on a box torus, nothing within 4 sites of the seam,
asserted every generation), `rd.py` (stores, readers, probes built from the cells in the push's JSON).
`python3 check_q.py` (18 s, ALL PASS): `q.c` = `oracle.step` = a pure-python set stepper on six soups; `q.c` =
oracle on the line with E and 2 holes for generations 0..400 and on the short store with reader and probe; a wrong
rule is noticed. Oracle runs take from the JSON only start cells, write flips, reader cells and probe cells; no
expected answer is read.

## Verdicts in brief

| claim | verdict |
|---|---|
| echo read with a capped wire B across the line, n = 1..4, whole state restored, tube never touched | **confirmed on the oracle**; restoration generations corrected |
| the same on short stores and in the 128-cell cell | **confirmed on the oracle**; a caveat on the cell's echo |
| wire C read, two pulses three apart | **confirmed on the oracle**; "transparent beside B′" corrected |
| 16 + 8 reading placements, same signals | reader B: **confirmed** by an independent recount (16, the same table); reader C: **not checked** |
| a single pulse never reads | reader B, uniform stores: **confirmed** (recount 280 / 20 / 8, 0 different); the rest **not checked** |
| the read can be repeated | **corrected**: only if the next pair does not meet the returning echo at even separation |
| it reads the stored bit | **corrected in wording**: it reads the letter of one unit; conditions below |
| no write with the reader in place | **not refuted**; no write found in 100,058 events of three kinds with reader b13; bounds below |
| parallel readers, rake train, `survey2`–`survey4`, `junc.py`, `inject.py`, all of `rw.py` | **not checked** |
| forecast score 0.136 | **confirmed** (arithmetic); one scoring choice noted |

## 1. The read, rebuilt

- **Confirmed.** `python3 read_oracle.py read-echo-B-line --long` (165 s; output in `out/read_oracle_echo_line.txt`).
  For n = 1, 2, 3, 4: the store at generation 900 has 419, 420, 420, 420 cells and smallest period 4; store + reader
  is exactly the union of the two alone at every generation 0..8, has period 4, and is the same state 400
  generations later (so for ever); with the probe no cell of the store's tube differs at any generation. n = 1: 30
  generations after the probe the runs differ in exactly (95,18,−84), (96,17,−86). n = 2, 3, 4: in nothing.
- **Corrected (small).** The runs are identical from **50** generations after the probe for n = 1 and from **21**
  for n ≥ 2, on the oracle. The README's "from 52" is the generation its check starts at, not a difference between
  the oracle and `st.c`.
- **Confirmed.** `python3 read_oracle.py read-echo-B-small` (5 s), `… cell-small` (2 s). In the 128-cell cell the
  two values are told apart, and both are restored (from 16 and from 7 generations after the probe).
  **Caveat:** in that cell the echo is never a free pulse on wire. The two cells the object names at its `out_gen`
  map back to the reader's own unit −5, and the reader's wire is units −4..1: the difference is a 2-cell disturbance
  in the reader's cap that lasts about 8 generations. Nothing could be built on that echo without lengthening the
  reader.
- **Confirmed; one statement corrected.** `python3 read_oracle.py read-pair-C-line` (83 s,
  `out/read_oracle_pairC_line.txt`), `… read-pair-C-small` (10 s). Restored from 62 (beside B) and 53 (beside B′)
  generations after the probe; tube never touched. **Beside wire B′ the crossing is not transparent**: at every odd
  generation one reader cell is missing from the union (in the short object's frame (−2,1,0)); beside wire B a cell
  is missing at every generation from 1 on ((−2,1,0) and (1,4,0) alternately). The push's check B looks at
  generation 16 only. The store is untouched in both, so the read stands; the wire C crossing is a junction beside
  both letters.

Beyond the push (`q.c`; lines rebuilt by `lines.py` from the JSON's `line0`):

- `python3 lines.py` (2 s): n = 7, 8, 9 give the n = 6 line. The line allows n ≤ 6.
- `python3 ext1.py units` (15 s): b13 and b8 at every unit 30..56 of the lines n = 1..6. **Confirms the push's
  position map**: b13 does not stand at units 39, 40, 41 and 41 + n; b8 not at 41, 41 + n, 42 + n, 43 + n. Echo at
  every other unit of wire B, nothing at the inner units 42..40 + n.
- `python3 ext1.py phases` (5 s, `out/ext1_phases.txt`): the pair launched at every generation 0..7 from three
  distances, n = 1..6, both readers: echo for n = 1, nothing for n ≥ 2, always restored. From the reader's other
  end the pair passes for every n: no read from that end.
- `python3 ext1.py probes` (`out/ext1_probes.txt`; n = 1 against n = 3, reader of 80 units):
  - one pulse: swallowed beside both (nothing travels; the state is back after 23 and 26 generations);
  - pairs 1..12 units apart: **only the adjacent pair reads**;
  - three pulses: adjacent (`6eef`), and a pair with a third pulse 2, 3, 4 units in front of it or 4 behind, read
    as the pair does. Four and five adjacent pulses do not read. Three pulses at offsets (0, 1, 4) beside wire B
    leave a 3-cell standing mark on the reader;
  - from the other end: one pulse comes out as two adjacent pulses beside both letters; a pair 4 apart passes
    beside B′ and leaves a 7-cell standing change beside B (a read that costs the reader).
- `python3 ext1.py repeat` (29 s, `out/ext1_repeat.txt`): 100 reads 64 generations apart, n = 1, 2, 6, both readers:
  the same output every time, tube never touched, state as unprobed at the end. **Corrected:** with the value B
  stored, a second pair launched 8, 12, …, 44 generations after the first (launch 12 units from the crossing)
  meets the returning echo head-on at even separation: the two stop each other and a 3-cell mark stays on the
  reader (the first push's mark). The store is untouched. "Can be repeated" holds when the echo has cleared the
  wire or the parity is odd; the README's argument from check E covers only a read that has finished.

## 2. Bit or position

- `python3 near.py` (20 s): stretch `d^k f`, k = 1..5, wall at every unit −12..12 from the crossing. Wherever the
  reader stands, the whole history of the difference (every cell, every generation) is exactly the history beside
  plain wire B or exactly the one beside the middle of a long stretch. **The reader senses the letter of the one
  unit it crosses and nothing else**: not a wall three units away, not the length.
- So the cell answers correctly exactly when, with the wall at w and the edge at e = w + k and the crossing at c:
  - "B′" when w + 1 ≤ c ≤ e − 1 (b13 and b8 alike);
  - "B" when c ≤ w − 3 or c ≥ e + 1 (b13); c ≤ w − 1 or c ≥ e + 3 (b8);
  - the reader does not stand at c = w − 2, w − 1, w, e (b13); w, e, e + 1, e + 2 (b8).
  A stretch `df` (k = 1) has no readable unit. The 128-cell cell works because its write puts `ddf` exactly on
  units −1, 0, 1 around a reader at 0; push 7's line works at unit 42 because the wall is at 41 for every n ≥ 2.
  It is a read of the stored bit only under a write that fixes the wall's place; the count n is not read.
- b8 is b13 with the store turned round: the half-turn of wire B composed with b13's map is b8's map up to slides
  along the two wires (by hand; the mirrored dead units above agree).
- Not checked: what is left of store and reader at the dead units.

## 3. No write with the reader in place

**Not refuted. No write found.** A write was defined as: the object stands afterwards, everything outside the
store's tube is as it was, and the reading pair gives the other answer and restores. Reader b13, store a capped wire
B, crossing at unit 0. `census.py`; every `changed` outcome is in `research/scratch/audit8b/`.

| events | command | seeds | events | healed | burn | changed, reader as it was, same answer | changed, something outside the tube changed | writes |
|---|---|---|---|---|---|---|---|---|
| every one-cell flip in the 5 × 5 tubes of both wires within 5 units of the crossing, at generation 0 and 1 | `python3 census.py cells B13 --k 0,1,2,3,4` (375 s) | 55 (plain; `d^k f`, k ≤ 4, wall or edge within 7 units) | 89,650 | 69,586 | 14,420 | 1,751 | 3,893 | **0** |
| 10 right-going and 11 left-going movers of wire B (`6f`, `6ef`, `6eef`, pairs, `d6f`, `cfd6f`, …; `b`, `bb`, `b5f`, `b5f9f`, …) from 18 units away at two delays; a stator removed inside the stretch, either stator, either phase | `python3 census.py movers B13 --k 0,1,2,3` (60 s, `out/census_movers_B13.txt`) | 52 | 2,808 | 0 | 1,358 | 1,449 | 1 | **0** |
| a store pulse or adjacent pair from either side together with a reader pulse or pair from either end, 25 relative delays | `python3 census.py both B13 --k 0,1,2`, **stopped after 19 seeds** (plain and `df`) | 19 | 7,600 | 96 | 4,792 | 2,712 | 0 | **0** |

- On plain wire B all 46 mover events burn: nothing that moves on the store survives the crossing, for every mover
  on file and not only the single pulse of the push's `cross24`.
- The stretch grows and is released on either side of the reader, and grows at its far end with the reader inside
  it, with the reader as it was (the 1,449 and 2,712): the push's "written and erased on one side" is confirmed for
  b13.
- The 128-cell cell's own write (the three removals) with its reader already there burns the object down to 24
  cells; the set alone at seven other places burns too (run inline, no script kept).
- **One lead, not followed.** Four one-cell events (for instance seed `df` at units 4, 5; (0,0,1) made live at
  generation 1) end in a standing object in which the unit under the reader is `4`, the store to the left of it has
  become wire C, and the reading pair then gives "nothing" and restores, where it gave the echo before. The answer
  was changed by one cell with the reader's wire intact, but the store is no longer wire B and cells outside its
  tube changed, so it was not counted. Whether it can be undone was not looked at.
- Not tried: reader b8 (the mirror image), the other reading placements, words of reader pulses as a write
  (`census.py words` is written, not run), pulses from both reader ends at once, a reader with a stretch of its own
  at the crossing, two-cell events, boundaries between B and B′ other than the wall and the edge, a third wire.

## 4. The push's own stepper and its surveys

- `st.c` and `check_st.py` were read, not re-run. No fault found in the code. Indirect agreement: every number of
  the push recomputed here with `q.c` came out the same (position map, restoration generations, placement tallies).
- `python3 place.py count` (2 min): **1056 placements** for reader B and for reader C, as the push, when the
  reader's footprint includes its passing pulses; 1048 and 1024 without them.
- `python3 place.py survey B` (297 s), `python3 place_report.py B` (`out/place_report_B.txt`): own enumeration, own
  stores (a stretch of 40 units as the B′ store). **Confirmed:** one pulse: 308 placements clean beside both =
  280 pass/pass + 20 gone/gone + 8 other/other, 0 with a different signal; pairs 1..8 apart from either end:
  **16 placements read, with exactly the push's table** (g = 8, 13, 11, 14: 2/0; 24, 27, 29, 30: 0/2; 16, 19, 21,
  22: 6/4 and 4/10; 32, 35, 37, 38: 4/6 and 10/4). 412 placements stand beside both by this review's test (the
  push: 416; the tests differ in how a changed store is counted).
- Not checked: reader C's survey, `survey2`, `survey3`, `survey4`, `junc.py`, `inject.py`, `posmap.py` beyond b13
  and b8, and every `rw.py` run. No survey sample was put to the oracle.

## 5. What is new

Not examined beyond the pages read for this review. The second push says of wire C's gate that "no crossing or
corner is known" (`research/signals/README.md` section 10), and push 8 scanned a second wire in parallel only and
lists "wires crossing at an angle" as not tried (its section 7). Against those, a transparent crossing at 60
degrees and a signal that depends on the crossed unit are new. Sections 26 to 35 and the earlier reviews were not
compared.

## 6. Forecasts

**Confirmed:** mean squared error 0.136 over the fifteen (sum 2.0375). Forecast 7 says "the pulse" and is false as
worded for one pulse; counted false it gives 0.109. The push states this choice itself.

## What it means

With push 8's store and this reader, gump has a bit that is written once and then read any number of times without
being changed: written by one-cell removals with no reader present, the reader put in by hand, the answer a pulse
that comes back or does not. The value under the reader is then fixed, while a stretch elsewhere on the same wire
can still be grown and released. The one missing piece is a crossing that survives something moving on the store:
every mover on file burns at it, and a wall or an edge cannot stand within the reader's dead units, so a letter
cannot be carried under a reader that is there.

## Not reached

- Item 3 beyond reader b13 and the three event sets above; the coincidence set is incomplete.
- Item 4 beyond reader B's uniform-store survey: no oracle sample of any survey, no re-run of the push's scripts.
- The oracle for n = 5, 6, for reader b8, and for the findings of `ext1.py` and `near.py` (all `q.c`).
- Item 5 in full.
- The first run of `place.py survey` had a wrong crossing estimate and is void; the figures above are from the
  corrected run.
