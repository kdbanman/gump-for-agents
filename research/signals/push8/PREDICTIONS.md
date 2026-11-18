# Eighth signals push: forecasts

Written 2026-11-18 03:15 UTC, after reading the earlier pushes and before any run of this push. Not edited
afterwards except for the last column and the section "Scored", which were filled in at the end.

Vocabulary: the *standing line* is push 7's finite object after E and n holes (wire B between two caps, with a
stretch of wire B′ for n ≥ 2). A *read* is a later signal whose outcome depends on the stored state.

| # | forecast | p | outcome |
|---|---|---|---|
| 1 | Push 7's line records (E and n = 1..4 holes; the line alone) pass on the oracle as claimed, and the final objects hold the claimed B′ stretches | 0.90 | true |
| 2 | My own stepper equals the oracle on the push-7 line at every generation, whole state, without a bug that changes any result I had already used | 0.90 | true |
| 3 | The 2-cell pulse of wire B, sent along the standing line at a clean B\|B′ boundary, is swallowed and the boundary moves one unit towards the sender (the register of the second push), at both ends of the stretch | 0.80 | true |
| 4 | The stretch's edge unit (the boundary that is not a clean wall) does something else to a pulse than swallow-and-move (passes it, reflects it, or burns) | 0.45 | false: the edge is the mirror image of the wall |
| 5 | Some rigid signal of wire B crosses a B′ stretch and leaves on the far side as a rigid signal | 0.12 | false |
| 6 | Some signal (single, double or compound) is reflected by a B\|B′ boundary: a rigid signal comes back | 0.25 | false (a pulse BORN at the wall comes back as k pulses; nothing that arrives does) |
| 7 | Both caps of the standing line survive the arrival of a single pulse of wire B (swallow it, with or without moving) | 0.45 | false: capL always, capR at one of two phases |
| 8 | At least one cap of the standing line returns a rigid signal when hit | 0.10 | false |
| 9 | Wire B has at least four different rigid signals reachable by one- or two-cell flips (counting directions separately) | 0.60 | true: R, L, d6f, b5f |
| 10 | A one-bit read with the bit surviving: a later signal's outcome (it arrives somewhere, or comes back, or not) depends on whether a B′ stretch is present, and afterwards a stretch is present if and only if it was before | 0.60 | true |
| 11 | A read of the count beyond one bit that leaves the count unchanged | 0.06 | false |
| 12 | A destructive read of the count: the outcome separates at least three values of n, the store being changed or lost | 0.40 | true: the whole count, as k pulses |
| 13 | A probe from outside (a second wire or object off the line's tube) whose behaviour depends on B against B′, both surviving | 0.10 | false (parallel second wire B only) |
| 14 | Something turns standing wire B back into the rake train (re-arming) | 0.04 | false |
| 15 | A self-contained finite memory cell with a protocol (write by a one-cell flip or a signal, read by a later signal) passes an oracle-only verify script | 0.50 | true: 73 cells |
| 16 | The answer I report is "a read" or "a destructive read" in the brief's sense (not "nothing reads it within bounds") | 0.65 | true: both |

## Scored

Scored 2026-11-18 at the end of the push. True: 1, 2, 3, 9, 10, 12, 15, 16. False: 4, 5, 6, 7, 8, 11, 13, 14.
Brier score (mean of (p − outcome)²) 0.101. Notes on each miss and on what was not foreseen: `README.md`, section 10.
