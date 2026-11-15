# Review: signals, fourth push (README sections 20–25 and 21b)

Adversarial review, 2026-11-15, of commits 4a10c4e … f6ec867. Code in `research/audit/signals4/`; commands are run
from there unless stated. Bulk output: `research/scratch/signals4/`.

**Stepper.** `st.py` is a sparse stepper on the infinite lattice written from `docs/AUTOMATON.md` §2 alone (no code
shared with `sg.py`). `python3 oracle_check.py` (3 s) compares it with `reference/oracle.py` cell for cell at every
generation on line N = 9, beam N = 9, 10, divider N = 12, 13, a beam with two holes and the divider with a second
oscillator (24–52 generations each): ALL PASS. `c824b.py --oracle`, `clock_tail.py --oracle` and `hole_oracle.py`
add oracle comparisons or oracle runs for the objects they use. The SAT checks below reuse the study's encoders
(`sat_gun.py`, `sat_two.py`, `sat_div.build`) on purpose: their job is to test those encodings.

## Verdicts

| # | claim | grade | reason |
|---|---|---|---|
| 1 | gun-5f; census 0 / 1 / 1 / 6 at C = 29..35 | **B** | gun reproduced with `st` for N = 10..40; census reproduced, but two of the six at C = 35 are the C = 31 gun and its translate |
| 2 | line, period exactly 4 from 2N for every N ≥ 2 | **A** | gluing proof checked step by step and holds as written; direct runs N = 2..60 agree (onset exactly 2N) |
| 3 | beam, period exactly 4, 33 + 5N cells, every N ≥ 1 | **A** | proof holds as written (both parities in the base); direct runs N = 1..60 agree, cell count included |
| 4 | holes heal | **A** | exhaustive instead of sampled: all 4,096 words on the beam N = 25 that keep the first rake heal, all 764 words on the line N = 16 heal |
| 5 | divider, period exactly 8 from 2N − 3, every N ≥ 8; stroke one cell | **B** | period, oscillator, word and stroke reproduced for N = 3..60; but "nothing on the wire changes the oscillator" holds for the orbit only (one removed cell at the stroke site kills both), and the place-and-phase claim gives no command and leaves its j undefined |
| 6 | clock with a tail, period 4N + 2 | **A** | N = 2..40, unlit stationary, lit period exactly 4N + 2 (`st`, oracle-checked on N = 5) |
| 7 | turn class 2 without planes, T ≤ 36; eat_direct | **B** | the encoding is a sound relaxation for every U (so the light-cone argument is right and not needed); T = 4 (missing from the list) is UNSAT too; but the push's intro says it holds "for caps of every length and shape" without the T bound. eat_direct: **C**, not checked |
| 8 | negatives with bounds | **B** | positive control added (the gun comes out of the period-8 encoding); "a sparser train" is one train; the divider and two-sided searches fix the wire's phase on both sides (closed here for the divider at W ≤ 3, see §5); the step_set scans: **C**, not checked |

## 1. The three "for every N" proofs

Read as a hostile reader, with the scripts open beside the text.

**Units.** All three scripts take unit u to be the slab x >> 1 = u and τ = (+2, 0, −2). Neighbour offsets change x by
at most 2, so a cell of unit u sees only units u − 1..u + 1, as the text says; τ is a lattice translation. Correct.

**The line (section 21, `prove_line.py`): holds as written.** Each step of the induction was re-derived:
- Y is well defined: P2 at u = m, m + 1 for all t (checked to 2N + 12; both sides have period 4 from t = 2N + 2, and
  P1 periodicity checked over 40 generations is periodicity for ever by determinism).
- The left chart is an orbit on units ≤ m: for t ≥ 2 it is X_N delayed; 0 → 1 is X_N; 1 → 2 needs X_N(2) = X_N(0) on
  units ≤ m, which is P3. The right chart reads units ≥ m. Unit m sees m − 1..m + 1 (left), unit m + 1 sees m..m + 2
  (right).
- Y(0) = Object(N + 1) needs capA inside units < m − 1 and the gun inside units > m + 1; neither is checked as a
  separate statement, but both are forced by P2 at t = 0 (units m − 1, m, m + 1 are then translates of each other,
  i.e. bare wire) and the gun sits at units ≥ N > m + 1.
- S(N + 1, m + 1): P2 at u = m + 1, m + 2 reduces, in the right chart, to P2 of S(N, m) at u − 1 ∈ {m, m + 1},
  including at t = 0, 1 where L is not a delay. P3 on unit m + 2 is P3 of S(N, m) moved. The bound m ≤ N − 4 is kept.
- "Exactly 4" (not 2) comes from the gun's cells in the right chart. The onset "not from 2N − 1" is not part of the
  induction; it is verified directly only, which is all the README claims for it.
- Transient: handled by L(t) = X(t − 2) for t ≥ 2 and P3 for the first two generations. Parity of N: the step is
  N → N + 1, one base N0 = 8 suffices.

**The beam (`prove_beam.py`): holds as written.** Q2 for t = 0..3 is Q2 for all t because Q1 gives period 4 from 0.
Y(0) = Object(N + 2) uses Q3 and the assertion that b0, b1 are one unit each; the move by two units keeps the b0/b1
alternation and the parity of the right end. "Not period 2" holds because units ≤ m + 1 and ≥ m − 2 of X_N cover
everything. Both parities are based (N0 = 8, 9).

**The divider (`prove_divider.py`): holds as written.** Same argument as the line; the extra condition (the
oscillator's eight phases lie in units > m + 2, P3) is what keeps it out of the left chart at Y(0); nothing else about
the oscillator enters the left chart, since the left chart only has to be an orbit restricted to units ≤ m + 1.
The onset 2N − 3 is odd and the left chart's delay of 2 gives 2(N + 1) − 3, as stated.

**Direct runs past the push's N** (`python3 scan_N.py line 2 60`, `beam 1 60`, `divider 1 60`; 16 s together;
infinite lattice, hull checked every generation):
- line N = 2..60: onset of period 4 exactly 2N, period exactly 4, gun cells period exactly 4 from 0, hull kept. All.
- beam N = 1..60: 33 + 5N cells, period exactly 4 from 0, hull kept. All.
- divider N = 3..60: onset of period 8 exactly 2N − 3, period exactly 8, oscillator support equal to the free
  oscillator at every generation, gun period 4, hull kept, word 5f9f on units 2..N − 7 for N ≥ 10. All. (N = 1, 2:
  period 8 but from generation 2 and 4.) So the "N ≥ 8" of the proof is conservative: the statement holds from N = 3.
- The three prove scripts themselves: `python3 prove_line.py`, `prove_beam.py`, `prove_divider.py` (in
  `research/signals/`): ALL PASS.

## 2. The gun and its census

- **Gun** (`python3 gun_check.py`, 10 s): Object(N) = capL + N units + gun for N = 10..40: at generation 4j the state is
  capL + bare wire + j mirror rakes + gun, cell for cell, for every j up to (N − 2)//2 − 1; the gun's cells (x ≥ 2N)
  have period exactly 4 from generation 0. All pass.
- **Census** (`python3 sat_gun.py 5f 31 --all`, 1 s; `... 5f 35 --all --out ../scratch/signals4/gun35.json`, 7 s; run in
  `research/signals/`): 1 at C = 31, 6 at C = 35, as stated. But the six are not six guns. The encoding fixes the
  train's phase at generation 0, so a gun's τ-translate taken two generations on is again a solution and needs the
  planes 4 further out. `python3 census_translate.py` (1 s): **#4 of the
  C = 35 list is the C = 31 gun itself, and #5 (19 cells) is the C = 31 gun moved one unit towards +v and two
  generations on.** At most four new guns at C = 35, up to translation and phase.
- **Positive control for the period-8 encoding** (`python3 sat_gun.py 5f5f 31`, 12 s): the dense train written with a
  repeat of 4 units (T = 8) is SAT and returns the 15-cell gun, re-stepped OK. So the UNSAT answers for `5fbb` (T = 8,
  L = 4) are not an artefact of the longer repeat.

## 3. Holes

`holes.py` removes the README's own one-cell holes; `holes2.py` writes holes in family letters (a unit reading 5
rewritten to 9 at an even generation, the README's "on the mirror-rake stream a hole reads 9f").
- `python3 holes.py beam 25` (6 min): the 13 rakes of the beam N = 25 one generation after the stored phase, **every**
  one of the 8,192 subsets removed: the 4,096 that keep the rake at unit 0 heal exactly; the 4,096 that remove it all
  change the gun. (`beam 12`: 32 / 32, 1 s.)
- `python3 holes.py line 16 41` and `python3 holes2.py line 16` (both under a minute): every word on the line N = 16,
  at one odd generation (256 words) and at the four even generations of a period (764 words): all heal, **including
  the words that remove the rake next to the gun** (unit 15 of 16). The README's condition "as long as the rake next
  to the gun is left alone" belongs to the beam, where the rake at unit 0 is part of the gun's own state.
- `python3 holes2.py divider 16`, `17`, `28` (2 s, 2 s, 35 s): every word of holes on the divider's wire at the four
  even generations of a period, upstream of the oscillator (unit N − 1, the one unit there that decodes) and
  downstream: 40, 44 and 348 words, **all heal**. A divider fed a stream that already has holes passes them on and is
  restored.
- But a cell removed *at the stroke site* is fatal. `python3 single_holes.py 16`, `17`: the cell hole_start removed
  from each unit where it is live, at each odd generation of a period: every case heals except one per period, unit
  N − 3 at generation 8k + 7, one generation before the stroke. On the oracle (`python3 hole_oracle.py`, 17 s): N = 16,
  that removal at generation 39 changes the oscillator at generation 43 and the object ends with 32 live cells instead
  of 147; the controls (unit 15 at 35, unit 14 at 33, unit 10 at 41) heal exactly.
- `python3 holes.py divider 16 33 47` (1 min) removes hole_start in every subset of units where it is live; downstream
  of the oscillator that cell is live in hole units too, so these words are not all holes; recorded only because it
  finds the same fatal case. `python3 holes.py divflip 12 21 28` (about 5 min): every one-cell flip of the divider N = 12
  (live cells of units 0..N + 2 outside the oscillator's support, dead tube cells of units 1..N − 1), at each of the 8
  generations of a period, 1,222 runs: 273 heal; in none are both the gun and the oscillator alive in a changed state.

## 4. The divider beyond what was sampled

- **The stroke** (`python3 stroke.py`, 2 s; N = 12, 16, 17, 32 generations each): step(X) and step(wire part) ∪
  step(oscillator part) differ in exactly one cell, once per 8 generations, gun frame (−5, 4, 10), unit N − 3,
  x + y + z = 9, born with 3 live neighbours in the oscillator and 1 in the wire, alive at generations ≡ 0 (mod 8) of
  the run (born in the step from 8k + 7). Reproduced.
- **Two oscillators** (`python3 twodiv.py 24`, 13 s): the divider N = 24 and a second C8.24a moved d = 3..17 units
  further from the gun, every phase k = 0..7 (104 non-overlapping placements): in 84 both oscillators keep their free
  orbit, the gun lives, the period is 8 and the word downstream is still `5f9f` (checked letter by letter: rakes and
  holes alternate); in the other 20 something is destroyed. **No second division**: a second C8.24a never writes one
  rake per 16 generations here.
- **C8.24b is a divider too** (`python3 c824b.py --oracle`, 7 s). The clockstream placement of C8.24b (its cells read
  from `research/scratch/signals/p4/clockstream.jsonl`) added to the line already in its cycle, moved with the gun to
  N = 10..30: period 8, the oscillator equal to its free orbit at every generation, gun alive, word `5f9f`, for every
  N. It stands at units N − 6, N − 5, outside the tube (x + y + z ≥ 9). `st` matches the oracle on N = 12, 13 for 160
  generations. Started from **bare** wire (`python3 c824b_bare.py 16`, 15 s; every shift and phase with the oscillator
  in units 3..N + 3) it gives the divider in only 4 placements, all with the oscillator in units 12..16 (N = 16): the
  README's "only when it stands next to the gun" is true of the bare-wire start, not of an oscillator put beside a
  running stream.
- **Place and phase of C8.24a** (same run, C8.24a part): from bare wire, dividers at shifts j = −6..+1 from the stored
  place with exactly one phase each, phase ≡ 2j (mod 8), plus two phases (0, 4) at j = +2, where the oscillator reaches
  the gun's unit. The README's formula "phase ≡ 2(j − N) + 4" fits this only if j is the oscillator's highest unit;
  the README does not say, and gives no command for the 47 s run.

## 5. The SAT negatives and section 22

**Section 22, `sat_two.py T --open`.** The instance is a relaxation: for any real period-2 end Z* in the tube and the
real orbit X* of the lone rake, the restriction to units ≤ U satisfies every clause (rule only on units ≤ U − 1; X* = Z*
at units > 5 + t because the rake and its tape differ from Z* only on units ≤ 5 at t = 0 and influence moves one unit
per generation; the guard and the mirror rake are the definition of the turn). This holds for **every** U, so the
light-cone choice U = T/2 + 6 is not needed for soundness; it only makes the instance tighter. (So the README's
UNSAT with the end cut at unit 11 for T = 16 is a *stronger* statement than the one at U = 14.) The "cannot fake"
arithmetic is right with a margin of two generations: unit U free from U − 5 reaches unit 5 at 2U − 10 = T + 2.
Phase: the wire on units < 6 is fixed at the phase the rake forces; no loss. Reproduced (in `research/signals/`):
`sat_two.py 8 --open` UNSAT (0 s), control `sat_two.py 6 --open` SAT (class 0), and **`sat_two.py 4 --open` UNSAT**
(0 s): T = 4 is a class-2 time the README's list (8..36) leaves out. Not done: an encoding of my own, T > 8,
Glucose. The containment of section 18's T′ ≤ 28 checks out (a rake on bare wire is rigid, so the cap is untouched
until it arrives; tape phases agree).

**`sat_div.py` fixes the wire's phase.** Wire C has period 2 (`st`: unit 0 differs at t = 0, 1, equal at t = 2), and
`sat_div.build` puts both trains at the same ring parity, so "all four relative phases" are the four relative
*positions* of the out-train with the wire **in the same phase on both sides**. An object joining wire C to wire C one
generation out of step is not covered. Closed here for small W: `python3 sat_div_parity.py 5fbb 5f W` (the left
pattern advanced by one generation, everything else `sat_div.build` unchanged): UNSAT at all four shifts for W = 1, 2,
3 (under 3 s each) and, in the 5 × 5 tube (`--lo -1 --hi 7`), W = 1. W = 4: see the end of this section. Control of
the advance: advancing both sides gives SAT at shift 0 for `5f`/`5f` (the train itself) and UNSAT for `5fbb`, as in
step; `5f`/`5f` with only the left advanced: UNSAT for W = 1, 2 (no phase-slip object of that width).
The same fixing applies to `sat_two.py --w W --V m` (the far wire V is at the one phase `wire_phases` gives): the 225
leaky-turner instances and the two-sided census exclude only objects with the far wire in that phase. Not closed.

**Wording.** `sat_gun.py 5fbb C` is one sparser train (5f9f, one rake per 8 generations), not "a sparser train" in
general. The three UNSATs (C = 29, 31, 33) were not rerun (the last took 29 min).

W = 4 out of step: RESULT_W4

## 6. Clock with a tail

`python3 clock_tail.py --oracle` (11 s): N = 2..40, Object(N) unlit has period dividing 2; lit by the one cell
(ignite moved N//2 units) its period after the transient is exactly 4N + 2. All. The turner occupies units 0..2 of
capR with 4 + 3 + 4 = 11 cells at generation 0 (README: 11; the JSON note says "a 12-cell object").

## 7. Wording of the headlines

- *"A standing object writes onto a wire."* Fair for the gun in the sense stated in §20 (bounded, periodic, the wire
  beyond changes), but what is written is the constant maximal stream, and the same object is a moving boundary
  between two wires. One sentence: **a 15-cell object of period 4 at the end of wire C restores itself every 4
  generations and leaves the densest train of mirror rakes behind it.**
- *"The divider emits a two-letter word."* What is shown: **beside the running line, the period-8 oscillator C8.24a,
  outside the tube and never changed in the undisturbed orbit, deletes every second rake by one born cell per 8
  generations, so the wire beyond carries the period-8 train 5f9f.** The writing is done by gun and oscillator
  together; the oscillator alone writes nothing on a wire at rest (section 23's scan), and a second one does not
  divide again (§4). "Emits a non-constant word" is fair if "word" means the unit letters; it is not a word of
  separated pulses on bare wire, as §21b itself says.
- *"One-way"* (§21b) is a property of the orbit, not of the coupling (§3).

## 8. Corrections the README needs

1. Fourth-push intro (lines ~713–714): "the negative of section 18 now holds for caps of every length and shape
   (section 22)" → "for every period-2 right end of wire C in the 3 × 3 tube, of any length and shape, for turns
   with T ≤ 36 (section 18's T′ ≤ 28, not its T′ = 32), the guard included".
2. §20 census: "C = 35: exactly 6" → "6 solutions, of which one is the C = 31 gun and one is the C = 31 gun moved one
   unit towards +v and two generations on: at most four further guns". (The absorber census of §21, 1 at C = 31 and
   12 at C = 33, presumably contains the C = 31 absorber among the twelve; not checked.)
3. §23 first item: "No gun for a sparser train" → "No gun for the train 5f9f"; cite the positive control
   `sat_gun.py 5f5f 31` (SAT, the gun).
4. §23 divider: "all four relative phases" → "all four relative positions, the wire in the same phase on both sides";
   add the out-of-step case (§5 here).
5. §22 two-sided objects and the 225 leaky instances: say that the far wire is in one fixed phase relative to wire C.
6. §22: add T = 4 (UNSAT, 0 s) to the class-2 list; note that the "cannot fake" paragraph is not needed for the UNSAT
   direction (every U is a relaxation).
7. §21 holes: "as long as the rake next to the gun is left alone" is the beam's condition; on the line every word
   heals (764 words, N = 16). "Measured on 200 random words" can be replaced by the exhaustive counts of §3.
8. §21b "What it is": "nothing on the wire changes the oscillator (check C)" → "in the undisturbed orbit nothing on
   the wire changes the oscillator; holes arriving in the stream pass and the object is restored, but one cell removed
   from the rake at the stroke site one generation before the stroke destroys oscillator and gun". §25 item 1: "the
   wire cannot change that phase" → the same qualification.
9. §21b proof: holds from N = 3 (direct runs N = 3..60), not only N ≥ 8; optional.
10. §21b place and phase: give the command; say what j is (with j the shift from the stored place, the phase is
    2j mod 8; at shift +2 two phases work).
11. §21b C8.24b: "not put to the oracle" → it is a divider beside the running line at units N − 6, N − 5 for N =
    10..30 (oracle-checked stepper; oracle cell for cell at N = 12, 13); "only next to the gun" holds for the bare-wire
    start.
12. §21b stroke: "the cell (1, 2, 2) of that unit at an odd generation" → "born in the step from generation 8k + 7 to
    8k + 8" (unambiguous).
13. `objects/clock-C-tail.json` note: "12-cell object" → 11 cells (generation 0).
14. Line 711: drop "found in the last hour".

## 9. Not checked

- `eat_direct.py` (one p> destroys the 8 class-2 caps); `gunlab.py start / capL / mirror / off / split / duel /
  obstacle / readers`; `beamcaps.py`; `clockscan.py`; `clockstream.py` counts (only its C8.24b row was used);
  the absorber census and the period-8 end negatives; Glucose agreement.
- No SAT encoding of my own; the UNSATs of §§22–23 were rerun only where stated (T = 4, 6, 8 open; gun census
  C = 31, 35; 5f5f control); the sparse-gun UNSATs at C = 29..33 and the divider W = 4 in-step runs were not rerun.
- Holes on the divider upstream of the oscillator: only one unit there decodes as a family letter, so "upstream
  words" are words on that unit at four phases.
- Placements of two oscillators other than two copies of C8.24a at N = 24.
