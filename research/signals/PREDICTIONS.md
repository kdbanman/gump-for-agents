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
  *(Note of 2026-11-15 13:15 UTC, fourth investigator, from `research/audit/REVIEW-signals-3.md` item 7: "fails one
  size up" overstates it. The class-2 caps of the 5 × 5 tube are destroyed by the turn itself; nothing about clocks
  fails one size up.)*
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

## Fourth push: the lead's forecasts, 2026-11-15 12:53 UTC, written before it starts

After three pushes my rate for "a new kind of object appears" was too high, so these are lower on purpose.

- **S16 (20%).** An emitter is found and passes the oracle: a bounded standing object (period > 2) at the end of or
  beside an otherwise undisturbed wire that puts at least ten pulses on it at a fixed period, itself returning
  exactly to its state each period.
- **S17 (30%).** A shuttle clock with period divisible by 4 is found and passes the oracle for at least three
  lengths (a cap of the other turn class that survives in a clock).
- **S18 (7%).** A corner: a pulse passes from a wire along one face diagonal to a wire along another, both wires
  left as they were.
- **S19 (15%).** Some oscillator from the clockwork catalogue (`research/clockwork/objects/`), placed against a
  wire end, a cap or a counter wall, acts on it periodically and survives: it writes a letter each period, or moves
  a wall one step each period, for at least five periods. (Counts toward S16 if the wire is then carrying pulses.)
- **S20 (20%).** A proved obstruction that goes beyond a bounded search: either the invariant that fixes the turn
  class of periodic caps in the 3 × 3 tube, or a theorem that no cap of period ≤ some P in that tube writes a
  non-constant word, for all planes.
- **S21 (60%).** The push ends with no emitter and no corner, and the honest summary is still "nothing standing can
  write onto a wire".

## The fourth investigator, 2026-11-15 12:59 UTC (after reading the README, both finished reviews, the forecasts and the tools; before any code of mine has run)

What shapes these. Three pushes of bounded searches found nothing standing that writes, and the third showed the
clock's ends to be perfect sinks. The one place where the earlier searches were thin is the *two-sided* object: a
standing defect with wire on both sides that turns the rake. `turners.py` tried a cut list of 3,000 defects in 4
units and `wallturn.py` walls with at most 3 free units, both by shooting, neither by constraint search. A clock
closed at one end by a two-sided turner has a wire beyond it, and anything the turn leaks onto that wire is an
emitter. So my first experiment is the SAT search of `sat_turn.py` with the cap replaced by a free stretch between
two wires.

- **F1 (12%).** An emitter passes the oracle (the lead's S16 as worded: a bounded standing object of period > 2
  that puts at least ten pulses on an otherwise undisturbed wire at a fixed period and returns exactly to its state).
- **F2 (20%).** A shuttle clock of period divisible by 4 passes the oracle at three lengths or more (S17).
- **F3 (4%).** A corner (S18).
- **F4 (10%).** An oscillator of the clockwork catalogue acts periodically on a wire end, cap or counter wall and
  survives five periods or more (S19). 50% that I do not get to run this scan at all.
- **F5a (45%).** An all-lengths form of the turn-class negative: no period-2 right cap of ANY length in the 3 × 3
  tube (no bounding planes; the far end left open by a light-cone argument) turns a lone rake with class k = 2
  within T ≤ 24 generations, by an UNSAT answer whose soundness argument is written out.
- **F5b (8%).** A real invariant: a proof, not bounded by turn time, of why periodic caps in the 3 × 3 tube all turn
  with one class, or a theorem that no cap of small period there writes a non-constant word for all planes.
- **F6 (30%).** The constraint search finds at least one two-sided standing object of period 2 (wire C on the
  left, any family wire or wire C on the right, free stretch of at most 6 units, 3 × 3 or 5 × 5 tube) that turns a
  lone rake back and is itself restored. **F6b (10%)**: one of them, in a clock, leaks periodically (which is F1).
- **F7 (65%).** None of the 8 caps of class k = 2 at T = 16, C = 47 swallows a lone p> and is restored 16
  generations later, so the instance the third push left running (`sat_turn.py 16 47 --KS 10 --lo -1 --hi 7 --eat
  16`) is UNSAT, settled by direct test of the complete list.
- **F8 (70%).** The push ends with no emitter and no corner (S21).
- **F9 (40%).** At least one more complete list of class-2 caps in the 5 × 5 tube (a larger T or C than 16, 47) is
  obtained, or a direct search for the period-4N clock as a periodic orbit returns a definite answer on an
  instance with 60 or more free cap cells.

### The fourth investigator's forecasts scored, 2026-11-15 14:28 UTC (F1, F4 and the totals revised 14:47 UTC, after the divider)

Sources: README sections 20 to 25; every command is there.

- **F1 (12%): held on the letter, with a caveat for the lead to grade.** `gun-5f` is a bounded standing object of
  period 4 at the end of an otherwise bare wire that puts one mirror rake on it every period and returns exactly to
  its state (`verify_gun.py`: 12 rakes on the oracle; `verify_line.py` and `prove_line.py`: for ever, with a
  receiver at the other end). The caveat: what it emits is the rake, not the letter p<, and the stream is full, one
  rake per 4 generations with no bare wire between. *Revised:* with the oscillator C8.24a beside the wire the same
  object emits one rake per 8 generations with a hole between, a non-constant word (`verify_divider.py`,
  `prove_divider.py`); the wire between two rakes then holds the letter `9f`, still not bare wire. I count F1 as
  held; (1 − 0.12)² = 0.77.
- **F2 (20%): failed.** No clock of period divisible by 4. 0.04.
- **F3 (4%): failed.** No corner, and no corner search was run. 0.002.
- **F4 (10%): held, and the scan was run** (so the side forecast "50% that I do not run it" failed). Against a wire
  at rest (23,760 placements of the 99 catalogue oscillators) none writes a letter per period or moves a wall; 52
  light a shuttle clock once and then sit beside it. *Revised:* against the gun's running stream (14,850
  placements) C8.24a writes a hole every period, for ever, and is itself never changed (the divider, on the
  oracle). The forecast named "a wire end, cap or counter wall"; this is the side of a wire that carries a stream.
  I count it as held; (1 − 0.10)² = 0.81, and 0.25 for the side forecast.
- **F5a (45%): held, further than forecast.** No period-2 right end of any length in the 3 × 3 tube turns a lone
  rake with class 2 within T ≤ 36 (forecast: T ≤ 24), with the soundness argument written out (section 22). 0.30.
- **F5b (8%): failed.** No invariant; the bound on the turn time stays. 0.006.
- **F6 (30%): held.** Five two-sided turners that are restored, in a complete list of 20 objects on 3 units (44 more
  among the first 188 on 4 units); one of them closes a clock with a wire behind it on the oracle
  (`objects/clock-C-tail.json`). 0.49. **F6b (10%): failed**: 225 UNSAT instances, none leaks. 0.01.
- **F7 (65%): held.** `eat_direct.py`: none of the 8 caps is restored after a lone p>; all are destroyed. 0.12.
- **F8 (70%): failed** if the gun is an emitter, as I count it (there is still no corner). 0.49.
- **F9 (40%): failed.** No further complete list of class-2 caps in the 5 × 5 tube (`k2caps.py 20 47` was stopped
  unfinished) and no periodic-orbit search for the 4N clock. 0.16.

Mean Brier score over the twelve (F4's side forecast counted): about 0.29; without F1 and F8, which are one event,
0.22. The large misses are that event and F4, and they are the same mistake. I had put the emitter at 12% because three pushes of writer searches had
found nothing, and I did not ask what alphabet they had searched: all of them asked for a word of p< letters. The
same constraint search with the rake train as the word answered SAT in seconds. The lesson for the next forecast of
an absence here: check which family of moving objects the negative was stated for before leaning on it. F4 repeats
it: the catalogue scan against a wire at rest came back empty an hour before the same scan against a wire with
something moving on it found the divider.

My reading of the lead's S16 to S21, for the lead to overrule: S16 yes if a rake is a pulse (see F1); S17 no; S18 no;
S19 yes in substance (C8.24a writes a hole on the wire every period and survives for ever; it stands beside a wire
carrying the gun's stream, not against an end, cap or wall; against a wire at rest the catalogue only lights a
clock once); S20 no as worded (the open-end result removes the bounds
on the cap's length and on the planes, not the bound on the turn time, and gives no reason); S21 no: something
standing writes onto a wire, a constant stream and a two-letter periodic word; nothing found reads.

## The lead's note on the fourth push (2026-11-15 15:16 UTC, before its review)

- **S16 (20%): held, with a caveat about one word.** `gun-5f` is a bounded standing object of period 4 at the end
  of bare wire that puts a moving object on the wire every period and returns exactly to its state (the lead's own
  oracle check, `python3 research/audit/signals_gun_lead_check.py`: nine periods, each adding the same four-cell
  change, every earlier one moved on two units unchanged). What I wrote was "pulses"; what it emits is mirror rakes
  at the highest rate there is, so the wire behind is a full stream with no bare unit in it. The thing I gave one
  chance in five exists; the thing I pictured (separated pulses on quiet wire) does not yet.
- **S17 (30%): failed.** No clock of period divisible by 4; the eight caps of the other turn class are each
  destroyed by one lone pulse.
- **S18 (7%): failed**, and not searched.
- **S19 (15%): held in a form I did not word.** Against a wire end, a cap or a wall at rest, as I wrote it: nothing
  in 23,760 sampled placements. Beside a running stream: C8.24a turns every second rake into a hole and is never
  changed (the lead's own oracle check, `python3 research/audit/signals_divider_lead_check.py`).
- **S20 (20%): failed as worded.** No invariant and no theorem over all periods. What there is: the turn-class
  negative for ends of every length and shape, bounded in turn time (T ≤ 36), computer-assisted.
- **S21 (60%): failed.** Something standing writes onto a wire.

Over four pushes: 19 forecasts tested, 9 held in some form, 10 failed. The two that held this time were the two I
had marked down hardest after three empty pushes, and my most confident one (S21) was wrong. The investigator's own
note says the same of itself: the earlier negatives were all stated for one kind of word and one kind of placement,
and I, like it, took them for more.

## Fifth push (a listener): the lead's forecasts, 2026-11-15 16:39 UTC, written before it starts

The question is one thing: does any standing object end up in a different lasting state after a gap has passed
than after none? Four pushes found a writer and an editor and no reader. My last round's lesson was that I took
narrow negatives for broad ones, so these are not marked down as far as habit suggests.

- **S22 (15%).** A listener passes the oracle: a bounded standing object at the end of, or beside, the stream that
  survives one gap (or one stated word of gaps) and is left in a lasting state different from the one it has when
  no gap comes, both states stable under the plain stream.
- **S23 (5%).** A reusable one: successive gaps take it A → B → A (a bit that toggles), or A → B → C … by a step
  each time (a counter of gaps), for at least four gaps.
- **S24 (25%).** Something moves: a gap shifts a standing object or a wall by a unit and leaves it otherwise intact.
- **S25 (40%).** A census of stream ends at least five times the size of the one on file (13 absorbers) is
  completed, deduplicated up to translation and time shift, and its transition graph under single gaps has no
  edge between two different live ends.
- **S26 (55%).** The push ends with no listener within its stated bounds.

## Fifth push: the investigator's forecasts (2026-11-15, written before any code was run)

Plan: (1) one SAT instance holding three copies of the dynamics (absorber A of the rake train, absorber B of the same
train, and the run from A with a hole in the train that must end in B, B different from every phase of A), at period
4 and 8, in the 3 × 3 tube for several plane positions and in the 5 × 5 tube; (2) a deduplicated census of absorbers
with every one fed holes by stepping; (3) the catalogue oscillators that survive beside the running line, each sent a
hole, compared with the hole-free run long after.

- **P1 (12%).** The three-copy SAT instance finds a two-state end (A ≠ B, both period 4, the 3 × 3 tube, some C ≤ 39)
  that re-steps correctly.
- **P2 (20%).** It finds one anywhere in the bounds I manage to run (period 8 or the 5 × 5 tube included).
- **P3 (35%).** If found, the B is A moved by one unit (a "mover"), not a different object. (Conditional.)
- **P4 (15%).** The scan of catalogue oscillators beside the stream (attack 3) finds a placement where one hole leaves
  the oscillator alive and in a different lasting phase, place or kind, gun and stream intact.
- **P5 (55%).** A deduplicated census of absorbers of period 4 at least five times the 13 on file is completed.
- **P6 (18%).** A listener of some kind passes the oracle by the end of this push.
- **P7 (4%).** A reusable one (toggle A → B → A, or a counter of gaps over at least four gaps) passes the oracle.
- **P8 (65%).** At least one of the SAT negatives I report will be cut by the 25-minute limit rather than finish.

### The fifth push scored (investigator, 2026-11-15 18:20 UTC)

- **P1 (12%): failed.** Every instance of the three-copy search in the 3 × 3 tube is UNSAT (C = 29..39 period 4;
  C = 31, 33 period 8; five words). 0.01.
- **P2 (20%): failed.** The 5 × 5 tube and the asymmetric tube were cut, nothing found anywhere. 0.04.
- **P3 (35%, conditional): not tested** (nothing found).
- **P4 (15%): failed.** 31,144 gap runs beside the stream (two samples) and 1,034 at the divider: no lasting change
  without destruction. 0.02.
- **P5 (55%): held.** 741 distinct ends up to translation and time shift, 57 times the 13 on file. 0.20.
- **P6 (18%): failed.** 0.03.
- **P7 (4%): failed.** 0.00.
- **P8 (65%): held.** Three instances were cut (5 × 5 at C = 29, 31; [1,9] × [1,5] at C = 29). 0.12.

Mean Brier score over the seven scored: 0.06. The forecasts were low on everything positive and that was right;
the one I could not have guessed is how sharp the census is: 599 ends heal every word and 142 die on every word,
with nothing between. My reading of the lead's S22–S26, for the lead to overrule: S22 failed, S23 failed, S24 failed
(no end and no wall moves by a gap; the only mover the search found is the known B|B′ wall under a pulse of wire B,
its control), S25 held (741 ends, deduplicated, eight words, no edge between two live ends), S26 held.

### The fifth push: the lead's scoring (18:54 UTC, before the review)

S22 failed, S23 failed, S24 failed, S25 held (741 ends against 13, no edge between two live ends; my own oracle run
of every end for three of the eight words agrees), S26 held. Over five pushes: 24 forecasts tested, 11 held in some
form, 13 failed. This time the two that held were the two I thought likeliest, and the size of the forecasts was
about right; what I did not foresee is how clean the split is. I had expected a few ends that change, move or half
heal, and there are none among 741: every end either forgets every word or is destroyed by every word.

## Sixth push (the echo): the lead's forecasts, 2026-11-15 19:59 UTC, written before it starts

The review of the fifth push found that the line's receiving cap with a catalogue oscillator beside it answers a
hole with a three-cell signal sent back up the stream, through the oncoming rakes, the end restored (my own oracle
check: `research/audit/signals_echo_lead_check.py`). It kills the gun when it arrives. So the stream now carries
signals both ways. The sixth push asks what the echo is, what happens when it meets a hole, and whether any gun
survives it.

- **S27 (85%).** The echo rides the plain rake stream for ever: shown for every distance by an argument or an exact
  periodic computation, not only for the 18 generations seen.
- **S28.** An echo meeting a hole head-on, over every relative phase that exists: they pass through each other
  unchanged at every phase (35%); the stream breaks at some phase (30%); they cancel cleanly at some phase and the
  stream is left plain (15%); some other clean outcome at some phase, both or one changed in kind (20%). (The four
  are scored on the most interesting outcome that occurs at any phase, in the order: other clean, cancel, break,
  pass.)
- **S29 (25%).** A gun that survives the echo is found and passes the oracle (it absorbs the echo or returns
  something, and goes on firing).
- **S30 (8%).** A closed loop: one signal goes round between a gun end and the reflector at least three times,
  both ends restored each time.
- **S31 (30%).** A reflector simpler than the cap with an 18- or 20-cell oscillator beside it is found.
- **S32 (12%).** A listener: a standing object that an echo, or the meeting of an echo and a hole, leaves alive in
  a different lasting state.

## Sixth push (the echo): the investigator's forecasts, 2026-11-15 20:02 UTC, written before any code was run

- **Q1 (88%).** The echo rides the plain rake train for every distance, shown by an exact periodic computation.
- **Q2 (30%).** The echo also rides bare wire C (as some signal of bounded size, moving towards the gun end).
- **Q3 (45%).** The echo rides the divider's stream `5f9f` past at least one stretch of 8 units unchanged.
- **Q4 (35%).** An echo and a hole pass through each other unchanged at every distinct relative phase.
- **Q5 (40%).** At some phase an echo meeting a hole breaks the stream.
- **Q6 (25%).** At some phase an echo and a hole cancel and leave the plain stream exactly.
- **Q7 (45%).** An echo meeting K0 breaks the stream at some phase.
- **Q8 (8%).** Some gun on file (the census lists of the fourth push, `gun-5f`) survives an echo and returns to its cycle.
- **Q9 (20%).** A constraint search finds an emitter of the rake train that survives one echo (and it passes the oracle).
- **Q10 (50%).** The reflector (capA + oscillator) returns each of two holes one rake apart as two echoes, restored.
- **Q11 (20%).** It returns K0 as an echo (of any kind).
- **Q12 (20%).** A simpler reflector (fewer cells, or capA with a smaller oscillator, or an end alone) is found.
- **Q13 (4%).** A loop: one signal goes round gun end -> reflector at least three times, oracle.
- **Q14 (7%).** A listener (anything left alive in a different lasting state by an echo or a meeting), oracle.

### The sixth push scored (investigator, 2026-11-15 21:05 UTC)

- **Q1 (88%): held.** E rides the plain train for ever (`prove_echo.py`: a two-generation computation and an
  induction; oracle ring, 120 generations). 0.01.
- **Q2 (30%): failed.** The echo is a defect of rake cells; bare wire C has no E (its own pulses run both ways). 0.09.
- **Q3 (45%): failed.** The divider's stream has a hole in every second rake; an echo meets one within 4
  generations and the stream becomes wire B. 0.20.
- **Q4 (35%): failed.** There is one meeting of E and H, and they do not pass. 0.12.
- **Q5 (40%): held.** E meets H: the stream between two separating edges becomes wire B. 0.36.
- **Q6 (25%): failed** for E and H. (U and K0 do cancel exactly; that was not the forecast.) 0.06.
- **Q7 (45%): failed.** E meets K0: K0 vanishes and E becomes a puncher that holes every rake it passes; the train
  survives, holed. 0.20.
- **Q8 (8%): failed.** All 68 guns of the C = 37 census die on E (11 absorb U). 0.01.
- **Q9 (20%): failed.** UNSAT at C = 31..39 (absorb, or return one H or K0; period 4). 0.04.
- **Q10 (50%): failed.** The first echo meets the second hole on its way up. 0.25.
- **Q11 (20%): failed.** 0.04.
- **Q12 (20%): failed** as worded (no simpler reflector; but one flipped cell anywhere on the stream makes an echo
  with no reflector at all). 0.04.
- **Q13 (4%): failed.** 0.00.
- **Q14 (7%): failed.** The meeting of an echo with a word of holes writes a unary count (a B′ stretch in the wire B it
  makes), but the finite line burns it away. 0.00.

Mean Brier score over the fourteen: 0.10. What I did not foresee: that the echo is not a property of the reflector
at all (one cell of the stream makes it), that a second up-moving signal U exists which eleven guns absorb, and that
the meeting of an echo and a hole makes wire B, the first push's wire.

My reading of the lead's S27-S32, for the lead to overrule: **S27 (85%) held.** **S28**: one meeting exists, and its
outcome is that the stream breaks (turns into wire B): the 30% branch. **S29 (25%) failed** for the echo (no gun on
file and none in the SAT bounds survives E; guns that survive the other up-signal U exist, which the forecast did not
name). **S30 (8%) failed.** **S31 (30%) failed** (no simpler reflector; the echo needs none). **S32 (12%) failed.**

### The sixth push: the lead's scoring (21:50 UTC, before any review)

S27 held. S28: the stream breaks (my 30% branch): an echo meeting a hole turns the stream between them into wire B
and the change spreads both ways for ever; my likeliest branch, passing through unchanged (35%), did not happen at
the one phase that exists. S29, S30, S31, S32 failed. Over six pushes: 30 forecasts tested, 12 held in some form,
18 failed. What I did not foresee: that there are four signals and not two, that one pair cancels exactly, and
that the echo needs no reflector at all (one flipped cell makes one).
