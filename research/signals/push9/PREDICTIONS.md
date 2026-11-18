# Push 9 (a trigger that travels): forecasts

Written 2026-11-18, after reading the accounts of pushes 1 to 8 and before any run of this push. Only the last column
and the section "Scored" were filled in afterwards.

Vocabulary. The *stretch* is `d^k f` on wire B (push 8). A *release* is the stretch leaving as a rigid train of
pulses with the wire plain where it stood. A *converter* is a finite standing object (still or periodic) beside or in
the wire. *Signal-triggered*: the only thing done by hand is to make a pulse (one cell removed) at least 10 units
from the stretch and from the converter. *Reusable*: after the release the converter is cell for cell what it was.

| # | forecast | p | outcome |
|---|---|---|---|
| 1 | The stepper I use equals the oracle cell for cell on wire B with an object standing outside its tube, at the first complete comparison | 0.85 | **true**: `check9.py` parts A and B (lab8, box and ring, with still lifes and oscillators beside the wire) equal the oracle at every generation on the first run |
| 2 | Some finite standing object outside the 3 × 3 tube is coupled to plain wire B (a cell with neighbours in both), stands with it, and both pulses pass it with everything restored | 0.90 | **true**: 62,094 of 73,553 standing still-life placements pass both pulses with everything restored |
| 3 | Some such object stands beside wire B and does not stand when a unit of the stretch (wire B′ or its wall) is beside it | 0.85 | **true**: 59 placements of still lifes of at most 8 cells (498 of 9 to 11 cells) beside which `d^3 f` falls |
| 4 | A signal-triggered release of any kind: a pulse arriving on the same wire, the whole count out as a rigid train, the wire plain; the converter may be changed or destroyed (one shot) | 0.45 | **true**: S6b at the wall, block `b^(2k+2)`, on the oracle |
| 5 | A reusable signal-triggered release | 0.20 | **true** by the definition above (the still life is unchanged), and in use for the call line (`cycle` on the oracle: called twice); the still life's own wire is single use |
| 6 | A release triggered by a pulse that arrives on a second wire (its end or a crossing) | 0.15 | **true**: the call line (a pair of pulses at a crossing, the line kept); with one pulse only the fuse, which destroys the second wire |
| 7 | A catalogue oscillator that stands beside plain wire B unchanged and releases a stretch brought next to it (a stroked site) | 0.35 | **true**: P3.15f passes both pulses on plain wire at the timing tried and `d^3 f` falls beside it (6 placements); also 110 falls of 17 other oscillators that do not pass both pulses |
| 8 | At a stroked site, two pulses that would stop each other on plain wire come out as one or more pulses, with the site restored (a map from arrivals to departures that is not the identity and not absorption) | 0.25 | **not tested** (`site9.py` not run); scored false |
| 9 | The constraint search with the known release as target returns a model that re-steps correctly | 0.15 | **false**: not attempted |
| 10 | A loop on the oracle: store, signal-triggered release, second store; a count moved by a pulse made at least 10 units away | 0.30 | **true**: `loop`, `smallest-loop` (still life) and `move`, `chain` (call line) on the oracle |
| 11 | If 4 holds: the number of pulses released is an exact function of k (k, k + 1 or k − 1) for every k = 1..10 | 0.75 | **true**: the call line gives exactly k pulses; the still life a block worth k + 1; k = 1..40 |
| 12 | An operation on counts beyond moving and adding (a copy, a doubling, a halving, a subtraction, a comparison) with a verifier | 0.10 | **true by the letter**: clear (k → 0) and constant (k → 1) on the oracle; **none of the five named** (copy, doubling, halving, subtraction, comparison) |
| 13 | The main answer I report is negative: no signal-triggered release inside the bounds searched | 0.50 | **false** |

## Scored

Brier score over the 13 forecasts: 0.295 with forecast 12 counted true, 0.234 with it counted false (0.25 = every
forecast at one half). Ten or eleven of thirteen came out true.

- Where the forecasts were wrong: 4, 5, 6 and 10 (a trigger, a reusable one, one on a second wire, a loop) were given
  0.45, 0.20, 0.15 and 0.30 and all four hold; 13 (a negative main answer) was given one half. The pessimism came from
  push 8's census of words and one-cell changes, which found no release by anything that travels; that census did not
  cover objects outside the tube or pairs of pulses on a crossing wire, and both work.
- 7 is true on thin evidence: one oscillator (P3.15f), one arrival timing on plain wire.
- 8 and 9 were not tested; both are counted false.
- Not foreseen: that the release by a still life comes out as one block worth k + 1 and not as k pulses; that the
  call on a second wire needs two adjacent pulses and that one pulse destroys line and store; that the CALL is
  exactly push 8's hand release delivered by the pair (`reduce9.py`).
