# Push 8b (a read from outside): forecasts

Written 2026-11-18 03:20 UTC, after reading the earlier pushes and push 7's account, before any run of this push.
Only the last column and the section "Scored" were filled in afterwards.

Vocabulary. The *store* is a stretch of wire B or of wire B′ (finally: a unit of push 7's standing line). A
*reader* is a second, separate wire that carries a signal. A *placement* is a lattice symmetry, a translation
and a relative phase of the reader. A placement is *transparent* if store and reader together are exactly the union
of the two alone at every generation although some cell has neighbours in both; a *junction* if they settle into
a standing state that differs near the crossing only. A *read* is a placement where the fate of the reader's signal
differs between a B store and a B′ store; it is *non-destructive* if afterwards the store is cell for cell what it
was.

| # | forecast | p | outcome |
|---|---|---|---|
| 1 | Push 7's line (gun 4, end 70, N = 80) with E and n = 2, 3, 4 holes is, on the oracle, a standing object holding a stretch of wire B′ that differs with n | 0.85 | true: n = 1, 2, 3, 4 stand and differ pairwise on the oracle (`verify_read.py`, checks A and F) |
| 2 | My stepper equals the oracle cell for cell on the push-7 line and on a pulse of a capped wire at the first complete comparison (no bug found by the check) | 0.80 | true (`check_st.py` passed when first complete) |
| 3 | Some reader wire (B or C, any of the 48 orientations) crosses wire B transparently at interacting distance (a cell with neighbours in both) | 0.90 | true: 280 placements of a reader B pass a pulse beside both stores untouched |
| 4 | Among non-parallel placements at interacting distance, more than half destroy at least one of the two wires | 0.60 | true: 620 of 1056 (reader B), 728 of 1056 (reader C) burn beside wire B |
| 5 | Some transparent or junction placement in which a pulse on the reader is affected at all by the store (absorbed, changed, delayed, reflected, or the store hit), for wire B as store | 0.75 | true |
| 6 | Some placement in which the pulse's fate differs between store B and store B′ (any read, destructive or not) | 0.55 | true |
| 7 | A non-destructive read on uniform stores: store B and store B′ both cell for cell unchanged, reader restored, fate of the pulse differs | 0.30 | true for a pair of pulses (16 + 8 placements); false as worded for one pulse (0 of 1056, either reader) |
| 8 | If 7 holds, the reader of the first such read is non-parallel to the store (crosses it at 60 or 90 degrees) | 0.60 | true: 60 degrees |
| 9 | If 7 holds, the same reader read at a unit of push 7's standing line (B unit against B′ unit of the actual objects for two different n) is non-destructive on the oracle | 0.80 | true: `objects/read-echo-B-line.json`, n = 1..4 |
| 10 | A complete cell with push 7's write: the reader stands beside the line from the start, the train, E, the holes and the edges pass it, and a later pulse tells two values of n apart with the line unchanged | 0.10 | false: every reading placement burns beside the train or at the write's front |
| 11 | A complete rewritable cell on the second push's B\|B′ register: store pulses pass the reader's crossing, the wall is written and erased as before, and the reader tells on which side of it the wall is, repeatedly | 0.15 | false: no store pulse passes any of the 24 reading placements (0 of 96) |
| 12 | Only destructive reads are found (6 holds, 7 fails) | 0.25 | false |
| 13 | Nothing: within the bounds searched no placement makes the pulse's fate depend on B against B′ (6 fails) | 0.45 | false |
| 14 | A pulse on the reader makes a pulse (or any travelling signal) on the store in some placement (crosstalk) | 0.25 | false: no pulse of the store from 3,056 probes; 254 start fire on it |
| 15 | The answer I report is "a non-destructive read" | 0.30 | true |

## Scored

Scored 2026-11-18 at the end of the push. True: 1 to 9 and 15. False: 10 to 14. Mean squared error over the fifteen
0.136 (always saying 0.5 would give 0.25; 8 and 9 were conditional on 7, which held).

- Most wrong: a non-destructive read (7 and 15, given 0.30) exists, and "nothing" (13) was given 0.45.
- 7 needs its caveat: the forecasts spoke of "the pulse". With one pulse there is no read in any placement of a
  wire B or a wire C; the reads are of a pair of pulses one unit (wire B) or three units (wire C) apart. I did not
  foresee that the number of pulses would be the variable that matters.
- Right and fairly confident: the line reproduces (1), the stepper (2), transparent crossings exist (3), the read
  carries over from uniform stores to push 7's line (9).
- Low and false, as forecast: a cell with the reader present during the write (10), a rewritable cell (11),
  crosstalk into the store (14). What I did not foresee is how complete the obstruction is: the crossing is
  transparent to the standing store and to nothing that moves on it.
