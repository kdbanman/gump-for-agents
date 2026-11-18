# Push 9 (a trigger that travels): forecasts

Written 2026-11-18, after reading the accounts of pushes 1 to 8 and before any run of this push. Only the last column
and the section "Scored" were filled in afterwards.

Vocabulary. The *stretch* is `d^k f` on wire B (push 8). A *release* is the stretch leaving as a rigid train of
pulses with the wire plain where it stood. A *converter* is a finite standing object (still or periodic) beside or in
the wire. *Signal-triggered*: the only thing done by hand is to make a pulse (one cell removed) at least 10 units
from the stretch and from the converter. *Reusable*: after the release the converter is cell for cell what it was.

| # | forecast | p | outcome |
|---|---|---|---|
| 1 | The stepper I use equals the oracle cell for cell on wire B with an object standing outside its tube, at the first complete comparison | 0.85 | |
| 2 | Some finite standing object outside the 3 × 3 tube is coupled to plain wire B (a cell with neighbours in both), stands with it, and both pulses pass it with everything restored | 0.90 | |
| 3 | Some such object stands beside wire B and does not stand when a unit of the stretch (wire B′ or its wall) is beside it | 0.85 | |
| 4 | A signal-triggered release of any kind: a pulse arriving on the same wire, the whole count out as a rigid train, the wire plain; the converter may be changed or destroyed (one shot) | 0.45 | |
| 5 | A reusable signal-triggered release | 0.20 | |
| 6 | A release triggered by a pulse that arrives on a second wire (its end or a crossing) | 0.15 | |
| 7 | A catalogue oscillator that stands beside plain wire B unchanged and releases a stretch brought next to it (a stroked site) | 0.35 | |
| 8 | At a stroked site, two pulses that would stop each other on plain wire come out as one or more pulses, with the site restored (a map from arrivals to departures that is not the identity and not absorption) | 0.25 | |
| 9 | The constraint search with the known release as target returns a model that re-steps correctly | 0.15 | |
| 10 | A loop on the oracle: store, signal-triggered release, second store; a count moved by a pulse made at least 10 units away | 0.30 | |
| 11 | If 4 holds: the number of pulses released is an exact function of k (k, k + 1 or k − 1) for every k = 1..10 | 0.75 | |
| 12 | An operation on counts beyond moving and adding (a copy, a doubling, a halving, a subtraction, a comparison) with a verifier | 0.10 | |
| 13 | The main answer I report is negative: no signal-triggered release inside the bounds searched | 0.50 | |

## Scored

[at the end]
