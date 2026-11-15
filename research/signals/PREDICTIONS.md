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

## The second investigator, 2026-11-15 09:05 UTC (after reading the README, the tools and the objects; before any code of mine has run)

Vocabulary: a **cap** is a way for a wire to end in empty space and stay (period ≤ 2 unless said); a **reflector** is
a cap, or a standing defect, that turns an arriving pulse into a pulse going back; a **corner** joins two wire
directions and passes a pulse from one arm to the other.

- **J1 (85%).** Wire B has a cap: a semi-infinite wire B that ends in empty space and is stationary (period ≤ 2).
- **J2 (35%).** A reflector is found for some pulse-carrying wire (the same event as the first half of the lead's S6,
  without the corner): pulse in, pulse out the way it came, reflector as it was or cycling through finitely many
  states, oracle as judge.
- **J3 (30%).** A free-standing finite object in empty space is built whose period is set by its length (a family,
  at least three lengths verified by the oracle, the period linear in the length). This is the second half of S6.
- **J4 (12%).** A corner between two of the six wire directions is found.
- **J5 (30%).** A receiver that stays put and toggles (S8) is found; the search that finds it is a constraint search
  for the pair of states, not a sample of standing defects.
- **J6 (15%).** A gate with an output pulse, a splitter or a duplicator (S7).
- **J7 (40%).** Some wire born from soup carries a pulse (S9); in particular 50% that wire B itself, up to symmetry,
  is among the soup-born wires of the 3 × 3 tube.
- **J8 (65%).** Where wire B meets living chaos the wire burns: a front runs down it and does not stop (so S10 holds
  for the trivial reason). 40% that in at least one trial a clean pulse B is seen leaving the chaos along the wire.
- **J9 (15%).** A proved obstruction of some generality (for example: no cap of a given class reflects; no finite
  free-standing object holds a circulating pulse).
- **J10 (60%).** If a reflector is found, the reflected pulse comes back with a delay that depends on the parity of
  the pulse's arrival time or position (as the head-on meeting does), so that only one parity of length oscillates.

### Scored, 2026-11-15 10:35 UTC (second push; evidence in `README.md` sections 8 to 13)

The lead's:

- **S6 (45%): held, with the object not the one named.** A free-standing object whose period is set by its length
  exists and is on the oracle: the clock, period 4N + 2, proved for every N (`prove_clock.py`). What goes back and
  forth in it is a rake (one added cell that travels and emits pulses), not a pulse. A plain pulse comes back from
  an end of wire C only once, the cap being changed by it; no corner was found or searched for.
- **S7 (25%): held to the letter, not in the sense a circuit needs.** Two pulses of wire C meeting head-on: exactly
  one goes on, which one by parity, so the pulse leaving on one line is (R and not L). The outputs leave along the
  input lines; there is no third line, no crossing.
- **S8 (35%): failed.** No standing defect with two states that a pulse flips: not among 4,192 caps of wire B
  (complete inside the bounds), nor the family's walls. What exists is a register moved one way by pulses from
  one side and back by pulses from the other.
- **S9 (30%): held.** Wires B and C, and a third carrier, are born from soup: 279 of 100,000 soups.
- **S10 (60%): held.** Where chaos touches a wire the wire is destroyed, in every one of 800 sides and 80 capped
  ends tried, at pulse speed. One qualification: in wire C a clean pulse does leave the chaos ahead of the fire on
  about one side in 12. The direction wire-to-chaos was not tested: nothing survives to send or to read.

Mine:

- **J1 (85%): held.** 4,192 caps of wire B inside the planes up to C = 33.
- **J2 (35%): failed as written.** No cap or wall sends pulse after pulse back; reflections of a pulse are one-shot.
  The thing that is reflected for ever is the rake.
- **J3 (30%): held**, and for every length, with a proof.
- **J4 (12%): not found, not searched.**
- **J5 (30%): failed.** And the constraint search for the pair of states was not run; the census of caps was.
- **J6 (15%): held in the sense of S7** (a collision gate; and the rake as a source of pulses, which is not a
  duplicator of an incoming pulse).
- **J7 (40%; 50% for wire B itself): held, both.**
- **J8 (65%; 40% for a clean pulse B leaving the chaos): the first held** (wire B burned on 400 of 400 sides);
  **the second failed for wire B** (0 of 400) and would have held for wire C (33 of 400).
- **J9 (15%): failed.** Negatives are exhaustive only inside bounds; nothing general was proved against reflectors.
  (The exact isolation of section 13 is T3, which was already on file.)
- **J10 (60%): failed.** Every length oscillates. Parity shows elsewhere: every period is 2 mod 4, and which of two
  meeting objects survives is a matter of parity.

What I got wrong in kind: I expected the pieces of machinery to be a pulse and a cap that handles it. The pieces
turned out to be a rake (one cell that travels and keeps emitting) and a tape (wires B and C are two letters, and
every word in them travels). Both were sitting in data I already had; I saw the rake only when a cap sent one back,
and the tape only when a control run without chaos cut a wire. And the two pulses that reach outside the tube were
found by the chaos, not by me: the closed 3 x 3 tube was too tight a place to search.

## The lead's own scores for S6–S10 (2026-11-15 10:30 UTC, after re-running the verifiers and his own oracle checks)

S6 half held: the free-standing object whose period is set by its length exists at every length, but what comes
back from a cap is a rake, not a pulse (reflections of a pulse are one-shot), and no corner was found or sought.
S7 held to the letter: in the collision gate the surviving pulse depends on both inputs; it is not a circuit
element with an output line of its own. S8 failed. S9 held. S10 held: every contact between a wire and living
chaos ended the wire; the qualification that chaos sometimes sends a clean pulse down wire C ahead of the fire
does not touch the forecast, which was about a pulse passing through. Over both pushes: S1 failed, S2 held, S3
held with a caveat, S4 and S5 untested, S6 half, S7 held, S8 failed, S9 held, S10 held.

## The lead's forecasts for the third push (2026-11-15 10:49 UTC, before it starts)

The aim of the third push is a machine made of parts: the literal form of open problem 13, one object passing a
signal to another again and again.

- **S11 (40%).** A periodic emitter is found: a bounded object in empty space on the end of a long wire that sends
  a pulse down the wire once per period, indefinitely, and returns to its own state each time.
- **S12 (30%).** With it, a clock drives a counter: a compound object in which a register's wall moves one unit
  per period of the emitter for at least ten periods, judged by the oracle.
- **S13 (15%).** A corner is found: a pulse passes from a wire along one face diagonal to a wire along another.
- **S14 (35%).** A free-standing oscillator of the clock family with period divisible by 4 is found (caps that
  turn the rake with a different delay).
- **S15 (50%).** No reusable reflector for a pulse is found in this push either, in any tube up to one size larger
  than the 3 × 3 tube.

## The third investigator, 2026-11-15 (after reading the README, the forecasts, the objects and the tools; before any code of mine has run)

A thought that shapes these: by the tape theorem, wire C with left-going pulses on it is a word over {B, C} moving
rigidly towards −v. So at the +v end of such a tape, the cap is a *writer*: everything to its left is the word it
has output, one letter per 2 generations. A uniform cap writes CCCC…; a gun is exactly a cap of period T whose
output word has period T/2 and is not constant. That turns the gun into a bounded constraint search with T/2 letter
variables in place of a whole semi-infinite wire.

- **K1 (45%).** A periodic emitter (S11) is found and passes the oracle: a bounded object at the end of a wire that
  writes a non-constant periodic word, returning to itself each period. 60% of that chance on its being found by a
  writer-cap search rather than built from the clock.
- **K2 (35%).** Emitter, wire and a moving wall (a register or a counter wall such as 8|C) in one free-standing
  object, the wall moving one unit per period for at least ten periods, oracle as judge (S12).
- **K3 (8%).** A corner (S13).
- **K4 (25%).** A clock-family oscillator with period ≡ 0 mod 4 (S14). If not, 30% that a reason for 4N + 2 is
  proved (for example a parity invariant of the rake's turn).
- **K5 (55%).** At least one exhaustive negative with stated bounds about writers/emitters (no writer of period
  ≤ T inside given planes and tube), whether or not a gun is also found.
- **K6 (30%).** A reader: a cap at the −v end of the tape that absorbs every arriving letter and stays as it was
  (an eater for any word), or that changes by a word-dependent amount.
- **K7 (70%).** No reusable reflector for a single pulse is found (S15).

**After the review of the second push (the lead, 2026-11-15 11:26 UTC; `research/audit/REVIEW-signals-2.md`):** S9
is re-scored as held only in a weak sense. The carrier wires came almost entirely from rings of one unit, where
the "soup" is one random unit repeated; on rings of 3, 4 or 6 units none appeared in 60,000 soups. S6, S7, S8 and
S10 stand as scored (S10 with the review's correction that the isolating gap is three layers, not two).

### Scored, 2026-11-15 12:05 UTC (third push; evidence in `README.md` sections 15 to 19)

The lead's:

- **S11 (40%): failed.** No periodic emitter. The question was made exact (a gun at the end of the tape is a
  *writer* with a periodic non-constant word) and small writers were excluded: none of period dividing 4, 6 or 8 at
  C = 29, 4 or 6 at C = 31, 33, 4 at C = 35 (SAT, 3 × 3 tube). Back-to-back caps (8,184 arrangements), a second wire
  beside the clock (5,625 placements in all six directions) and two-sided turners gave nothing.
- **S12 (30%): failed** (no emitter). The counting part exists: the 8|C wall moves one unit per pulse of a train
  of spacing ≥ 2 [sg only].
- **S13 (15%): failed.** No corner; the side-kick scan is the only search of two directions, and it found nothing.
- **S14 (35%): failed, and the reason found in part.** P ≡ k_R + k_L (mod 4) with a turn class k of each cap
  [proved]; inside the 3 × 3 tube every cap that turns the rake has k = 0 (201 of 201 measured; k = 2 UNSAT by SAT
  for caps of period 2, 4, 6 within the bounds), so there 4N + 2 is forced; in the 5 × 5 tube a period-2 cap with
  k = 2 exists (re-stepped) but does not survive in a clock.
- **S15 (50%): held**, cheaply: no reusable reflector was found, but this push did not search for one beyond what
  the readers census says (a left cap either eats everything or disturbs the tape).

Mine:

- **K1 (45%): failed.** (The sub-forecast was right in kind: the writer search is where the question became exact.)
- **K2 (35%): failed.**
- **K3 (8%): failed** (no corner).
- **K4 (25%): failed**; the 30% on a proved reason: **half**: the reduction to a cap constant is proved, the
  constancy of that constant holds only inside the 3 × 3 tube, and fails one size up.
- **K5 (55%): held** (writers of period dividing 4, 6, 8 excluded in stated planes).
- **K6 (30%): held.** capL eats every word and is exactly as it was at every even generation, proved for all words
  by a closed automaton and checked on the oracle; the census adds that no left cap in the tables has a memory.
- **K7 (70%): held** (none found; little searched).

What I got wrong in kind: I expected the gun to be found by a constraint search once the problem was put as a
writer; instead the search showed that small writers do not exist and grew too fast to reach clock-sized ones.
What surprised me: capL, the end that makes the clock, is a perfect sink with no memory at all, and every cap in the
3 × 3 tube that turns the rake turns it with the same delay mod 4 (one size up, not). The clock's ends are as simple as ends can be, which is
exactly what keeps the clock from talking to anything else.

### The lead's note on the third push, 2026-11-15 12:50 UTC

I accept the scoring above. Of my five forecasts the four that asked for a new kind of object (emitter 40%,
clock-driven counter 30%, corner 15%, period 4N 35%) all failed, and the one that held (no reusable reflector, 50%)
was hardly tested. Taken together those four probabilities expected 1.2 new objects and got none: I was
over-confident that the second push's rate of invention would continue. Over three pushes: 13 of my forecasts
tested, 7 held in some form (S6 and S9 weakened afterwards by review), 6 failed. What I did not foresee at all was
the form the negative took: that the clock's end is a perfect sink, and that the period's residue mod 4 is a
property of the cap that the 3 × 3 tube pins and the 5 × 5 tube frees.
