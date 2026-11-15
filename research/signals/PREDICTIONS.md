# Signals: forecasts written before the search

## The lead, 2026-11-15 07:16 UTC (before any search for signal carriers has been run)

The question is open problem 13 of `research/OPEN-PROBLEMS.md`: can anything in gump carry a signal from one place
to another? A finite pattern in empty space cannot move (the hull theorem), so a signal needs a medium: a wire, a
sheet, a row of clocks. Forecasts, with the chance I give each:

- **S1 (60%).** None of the wires and sheets already on file (`research/clockwork/`, the notebook entry of
  2026-11-15 on unrecognised settled states) carries a travelling defect under any one- or two-cell perturbation:
  each perturbation heals, freezes where it is, or wrecks the wire locally, and nothing moves more than six cells
  from where it was made.
- **S2 (35%).** A travelling defect exists in some periodic background found by a constraint search (a pattern
  that after p generations is itself shifted along the background), and its speed is at most half a cell per
  generation.
- **S3 (20%).** A transmission is built in this push: a change made at one place alters, repeatably, the state of
  an object at least ten cells away, through a medium that is left as it was.
- **S4 (70%).** In two-dimensional backgrounds (sheets) a perturbation either dies or spreads; it does not travel
  as a localised pulse.
- **S5 (50%).** The pattern that circulates in a clock of the "short loop that closes with a twist" kind does not
  survive unrolling: laid on a straight periodic track three or more loop-lengths long, a single copy of it does
  not keep travelling.

## The investigator, 2026-11-15 07:40 UTC (before any search of mine has returned a result)

Written after reading `docs/AUTOMATON.md`, the clockwork README and the three notebook entries, and before any
code of mine has run. Vocabulary used below: a **fuse** or **front** is a boundary between two different
spatially periodic states (one of which may be empty space or ash) that moves at a steady speed; it satisfies
"after p generations the state is itself shifted by s cells" but uses the medium up. A **pulse** is a localised
defect with the *same* background on both sides, so the medium is left as it was.

- **I1 (55%).** At least one of the 21 wires on file is a fuse: cut it (a semi-infinite copy, or a gap of one
  unit in a long copy) and the damage runs along it at a steady speed for at least ten units, rather than
  stopping at a cap. Reason for more than a half: each of these wires fails to exist as a finite lift, so each
  unit needs its neighbours.
- **I2 (55%), the same event as the lead's S1 but stated on my trials:** no one- or two-cell flip of any of the
  21 wires and 2 sheets produces a *pulse* (same background on both sides) that moves more than six cells.
  (S1 as the lead wrote it also excludes fuses started by a flip; to that stricter event I give 40%.)
- **I3 (25%).** In some oscillating wire, on file or newly found, a boundary between two phases of the same wire
  (units on the left at phase 0, on the right at phase k) moves steadily. If clocks along a wire were
  independent it could not move at all.
- **I4 (60%).** A steady front of some kind (fuse, growth front along an existing medium, or conversion between
  two periodic states) is found and passes the oracle for ten periods. This would reach L1 only in the weak
  sense; I will say which sense.
- **I5 (20%).** A pulse is found (L1 in the strict sense): same background before and behind.
- **I6 (10%).** L2 as the lead defines it (medium left as it was and reusable). One-shot transmission down a
  fuse to a detector at least ten cells away: 45%.
- **I7 (15%).** Random soups on closed rings (a thin tube or strip, periodic along its length, several lengths)
  settle into some state whose period grows in proportion to the ring length, i.e. a pulse found by sampling
  rather than by constraint search.
- **I8 (35%).** A proved obstruction for a non-trivial class of carriers comes out of the push (for example: no
  pulse without overcrowded cells; no pulse in one kagome layer; a speed bound below one cell per generation
  for some class).
- **I9 (30%).** L3 in any form (two fronts or pulses meeting and doing something lawful, verified).

## Scores, 2026-11-15 (the investigator; evidence and commands in `README.md`)

The lead's forecasts:

- **S1 (60%): failed.** One-cell flips start fronts that run the whole length of the wire in 17 of the 21 wires on
  file (11,544 of 57,150 flips). What does hold is the narrower statement that no one-cell flip of a wire on file
  makes a *pulse* (0 of 57,150). Two-cell flips and the two sheets were not run.
- **S2 (35%): held.** Pulses were found by constraint search in periodic backgrounds (wires A, B, S and at least 27
  more), and every one found moves exactly one cube per two generations, half the speed limit.
- **S3 (20%): held, with a caveat to be judged by the reader.** One flipped cell at A changes a standing defect 36
  cubes away, six times in a row, through a wire that is left exactly as it was between A and the defect; but the
  defect advances one cube towards A with each pulse, so one cube of wire is used up at the receiving end per signal.
- **S4 (70%): not tested** (no sheet was perturbed).
- **S5 (50%): not tested** (no clock was unrolled; the pulses came from a search that does not start from a clock).

Mine:

- **I1 (55%): held.** 12 of the 21 wires burn from a cut for the whole ring; W00's front passed the oracle for ten periods.
- **I2 (55%): held as far as it was run** (one-cell flips: no pulse in 57,150); two-cell flips and sheets not run.
- **I3 (25%): failed on the wires on file** (no phase boundary travels: walls or fronts); not tested on new wires.
- **I4 (60%): held.**
- **I5 (20%): held** (three pulses verified by the oracle).
- **I6 (10%): held, with the caveat under S3.** The one-shot version by fuse was not built (no detector).
- **I7 (15%): not tested as stated** (no soups on long rings); the nearest test, 21,000 soup hits on 875 sampled
  wires, found no pulse.
- **I8 (35%): held in a small way.** Two short corollaries, not a new lemma: a wire cannot grow at its end (T2), and
  a pulse on an undriven wire must carry an overcrowded cell (T5). No class of carriers was shown impossible.
- **I9 (30%): held** (pass or stop by parity, on the oracle).

What I got wrong in kind: I expected the answer to turn on the wires already on file and on sampling. Both gave only
fuses. The pulses were sitting in the smallest tube the constraint search was pointed at, and the search took under a
second.

## The lead, 2026-11-15 08:51 UTC: forecasts for the second push (written after the first push reported pulses, a transmission and an interaction, and before any of the work below)

- **S6 (45%).** A reflector or a corner for a pulse-carrying wire is found in this push: a pulse that comes back,
  or turns into another wire direction, with the oracle as judge; and with it a free-standing object whose period
  is set by its length.
- **S7 (25%).** A gate with an output is found: two incoming pulses produce an outgoing pulse that depends on both.
- **S8 (35%).** A receiver that toggles is found: a standing defect with two states that each pulse flips and
  leaves in place.
- **S9 (30%).** Some wire that arises from random soup carries a pulse.
- **S10 (60%).** A pulse cannot pass between a wire and living chaos as a pulse: where a wire meets a chaotic
  face, the wire burns or the pulse is absorbed with no repeatable effect on the other side.
