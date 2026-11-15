# Review: signals, third push (README sections 15–19, PREDICTIONS "third push")

Adversarial review, 2026-11-15. Code in `research/audit/signals3/`; commands run from there unless stated. Stepping is
`reference/oracle.py` on a box torus (every generation checked: no live cell outside the pattern's diagonal hull, or
for rings outside the 3 × 3 tube modulo the box, so the box is never felt), or `gs.Dom` of the second review
(oracle-checked, `python3 ../signals2/gs.py`) on the diagonal hull of the starting pattern, which is exact on the
infinite lattice by T2. `r3.py` holds the shared pieces; no study code is imported except in `sat_controls.py` and
`k2_regen.py`, whose job is to test the study's SAT encodings. Bulk output: `research/scratch/signals3/`.

## Verdicts

| # | claim | verdict |
|---|---|---|
| 1 | capL is a perfect reader with no memory; census 17 / 126 / 702 | **stands**. Proof complete (it reduces to 16 local cases; re-derived and checked on the oracle). Census reproduced exactly with our own code; "no memory" reproduced at C = 29, 31 |
| 2 | emitter at the +v end of wire C = writer | **stands with a correction**: exact only for emitters whose output is a train of B/C letters (p< in the 3 × 3 tube); the negatives exclude much less than "emitter" (below) |
| 3 | 8\|C counter | **stands with corrections**: counts every isolated pulse exactly (oracle, new trains); a run of n ≥ 2 adjacent pulses counts **once and is reflected** (BB comes back as exactly one p>); wire 8 is not free-standing (a cut wire 8 burns at one unit per generation) |
| 4 | P ≡ k_R + k_L (mod 4); 3 × 3 forces k = 0; 5 × 5 has k = 2 caps | **stands with corrections**: the bookkeeping is right and the convention consistent (clock-C: k_R = 0, k_L = 2), but "k is a constant of the cap" is proved for a *lone* rake, while in a clock the rake arrives right behind a p> train (gap not closed by the argument; measured to agree for all 33 clock caps at C = 31). **All eight k = 2 caps are destroyed by the turn itself**, with no train and no clock involved (oracle) |
| 5 | negatives inside bounds | **stand as stated**, the SAT encodings pass fixed-cap controls; but what they exclude is narrow (below) |

## 1. The reader (claim 1)

**The argument.** `prove_reader.py` closes a set of states (cells of units ≤ U at even generations) under "append
letters, step 2". Its set is "capL + pure word on units 0..3", hence 16 = 2^4 states: the automaton is trivial,
and the proof amounts to a local statement, which I re-derived: let X(0) = capL + any infinite word w on units ≥ 0.
It suffices that step²(capL + w) = capL + w moved one unit, for every w. Units ≥ 2 of step² depend only on units ≥ 0
(two generations reach two units: the light cone of the second review), which are pure tape, so the tape theorem
gives them. Units ≤ 1 depend only on units ≤ 3, i.e. capL and w[0..3]: 16 cases. Induction does the rest, at every
even generation, for every word and every order of letters. The junction at odd generations needs nothing extra.
One point the study's docstring glosses: its transition fixes the letters at units U+4, U+5 to C; that is harmless
because units U+1, U+2 at generation 2t+2 do not depend on them (by the same light cone, units ≤ U+2 after two
generations see only units ≤ U+4, and unit U+3's odd phase is its own letter's, `sat_writer --selftest`). **The
proof is complete as written.**
`python3 reader_check.py local` (2 s): all 64 words of 6 letters, units ≤ 3 after 2 generations equal capL + word
moved, on gs **and on the oracle**. PASS.

**Census.** `python3 reader_check.py census C [--closure]` builds each left cap as the mirror of (wire C + right
cap) one generation on, re-anchored (checked: clock-C's capR gives capL exactly), and calls it a sink when the 16-case
check passes. C = 29: 17 sinks / 117 not; C = 31: 126 / 1,367; C = 33: 702 / 6,944 — exactly the study's numbers
(6 s, 90 s, about 8 min). With `--closure` (states = units ≤ 3, closed under two more letters; "disturbs" = units
4, 5 not the pure tape for some reachable state and letters): **all 117 and all 1,367 non-sinks disturb; none has a
memory** at C = 29, 31. Not run at C = 33, with U = 6, or with `--nobb`.

## 2. Writers and emitters (claim 2)

"A periodic emitter at the +v end is exactly a writer whose word is periodic and not constant" is true when
the emitter's output is a stream of p< (one B unit each) inside the 3 × 3 tube: by the tape theorem the region to its
left is then a word over {B, C} and everything there is fixed by the word. `sat_writer.py` then also requires the
writer to fit in units ≥ 6 of the tube, cut by the planes (at C = 29 that is units 6..10, 33 cells), with units 4, 5
exactly the tape at every generation. What the negatives exclude, exactly: a *stationary periodic* object of period
dividing T (T = 4, 6, 8 at C = 29; 4, 6 at C = 31, 33; 4 at C = 35), inside the 3 × 3 tube and those planes, at the
+v end of wire C (or of wire B: the word is free), writing a non-constant word, which means word periods 2, 3, 4 only
(word period divides T/2). By the mirror, the same for p>-writers at the −v end. **Not excluded:**
- word periods ≥ 5 (T ≥ 10), which is where a clock-made gun would be (the README says so);
- emitters reaching outside the 3 × 3 tube, in particular of the **wide pulses** of section 10 (not B/C letters);
- emitters of **moving objects** that are not letters: a gun at the +v end emitting mirror rakes (`5f`, which emit
  p> back into the gun), or at the −v end emitting rakes; the composite right-going objects found below at the 8|C
  wall (`9fb7bf`, `9d…df`) are of this kind too;
- emitters beside a wire, or in its middle (two-sided), and emitters on any wire other than the B/C tape;
- emitters at the end of the tape whose junction disturbs the two units in front of the search region.
**Controls** (`cd research/signals && python3 ../audit/signals3/sat_controls.py`, 5 s): capR of clock-C fixed as
the writer at unit 6, C = 31: SAT with word C at T = 2 and 4 (a known writer of the constant word is accepted);
UNSAT at T = 4, 6 with the word free and non-constant (a known non-writer is not mistaken for a writer). A planted
non-constant writer was not constructed: none is known, so the positive side of the encoding is tested only on the
constant word.

## 3. The counter (claim 3)

`python3 counter_check.py` (7 s, oracle, ring of 64 units of the tube; wire 8 on units 0..7, wire C on the rest,
so walls 8|C at 8 and C|8 at 64|0; my kymographs and final states). Final state equals the ring with the wall moved
by the number of pulses, cell for cell, for: 12 pulses at spacing 2 and 3; 9 at spacing 4 and 5 at spacing 7 (the
ring held that many: my first run expected 12 and "failed" because pulses past unit 63 were not placed — a fault of
the test, not of the counter); an irregular train with spacings 2,3,2,5,2,2,4,3,2,6 (11 pulses); 20 pulses at
spacing 2; 27 pulses at spacing 2 filling units 10..62 (wall 8 → 35). The wall moves 2 generations after each
pulse reaches it. A B placed directly against the wall (unit 8) is not a pulse arriving: it sets the ring on fire.
**Spacing 1** (oracle, exact for BB; kymographs for the others, `counter_s1.txt`):
- **BB: the wall moves exactly one unit and exactly one p> leaves towards +v; the rest of the ring is exactly as it
  was** (state at t = 100, 120 equals the ring with wall at 9 plus one p>, for BB at units 30 and 40). So the wall
  counts the run once and **reflects** the second pulse.
- BBB: wall +1 and a right-going composite `9fb7bf` leaves (2 units per 4 generations); B^4: wall +1 and `9ddf`
  leaves; B^10: wall +1 and `9ddddddddf` leaves. So a run of n ≥ 2 counts once and the rest comes back; for
  n ≥ 4 as n − 2 units of B′ (= d) between p>-like ends. The wall itself is clean (all `8` up to the new wall
  position), not "a mixed region" as README section 17 says from `sg`. (n ≥ 3: kymographs only, not cell for cell.)
- BB C BB: wall +2, nothing leaves (the reflected p> of the first pair meets the second pair).
**Wire 8** is the stators plus (0,2,3), stationary on a ring; it is **not free-standing**: a finite piece with cut
ends burns from both ends at one unit per generation (40 units gone by generation 40), and attached to wire C it
sets that burning (gs). So the counter exists on a ring only, or with a cap for wire 8, which nobody has. Where the
wall ends up when it reaches the source cannot be tested without a source; on a ring a train can at most move the
wall by half the C stretch (pulses are a unit wide at spacing ≥ 2).

## 4. Turn classes (claim 4)

**The mathematics.** With a = t − 2u for the rake at unit u and b = t + 2u for the mirror rake (`5` at unit u),
P = (b − a) + (a′ − b) *exactly*, so P ≡ k_R + k_L is bookkeeping; the content is that each bracket equals 4 × (the
cap's first unit) + a constant of the cap. For a **lone** rake meeting a period-2 cap this is proved: rake-at-u at t
and rake-at-u at t+2 are the same picture against the same cap, and translation by one unit changes b − a by 4.
In a clock, though, the rake does not arrive alone: it arrives one unit behind the tail of the p> train it follows
(clock-C, N = 9: row `f9f9f9f9f9` at t = 30), while the cap is digesting that train, and what is directly ahead of
the rake was set by the other cap's turn. The in-clock constant is still independent of N and of the time class
(same argument, applied to the cap plus the incoming pattern), but it need not equal the lone constant, and the
README's step "if every right cap that turns the (lone) rake has the same k, every clock has the same P mod 4" does
not follow. **Measured, not proved, that it does not matter:** `python3 turn_check.py clockC 3 5 6 9 17` and
`python3 turn_check.py table ../../scratch/signals/clocks_31.json` (1 min): for clock-C and for all 33 clock caps of
C = 31, lone constant c_R = (b − a) − 4K = 0, and in clocks with N = 5, 8 (and 3..17 for clock-C) the in-clock c_R =
0 and c_L = 2, P = 4N + 2.
**Convention.** All right caps measured have k_R = 0 and capL has k_L = 2 (the mirror of a k = 0 right cap is a
k = 2 left cap; it shifts time by one generation). capL's lone constant measured directly: a lone mirror rake
started at units 10, 11, 20 comes back as a rake with a′ − b = 2 each time (`python3 turn_check.py capL`, gs), equal to its in-clock value. So "all caps have k = 0 and P ≡ k_R + k_L ≡ 2" reads as a
contradiction unless the README says that k_L of capL is 2. A period-0-mod-4 clock with capL needs a right cap
with k_R = 2, as `k2caps.py` assumes.
**Census of lone turns** (`python3 lone_census.py 29 31`, 30 s): 15 of 134 and 186 of 1,493 cap states turn a lone
rake, all with k = 0 and in fact c_R = 0 exactly (study: 201, all k = 0). `turnclass.py`'s "restored" flag is
False for every cap including clock-C's own capR (`scratch/signals/turnclass.txt`): its criterion compares the cap
units while p> pulses are still arriving and is meaningless; the README does not use it, but k2caps.py's output
"(2, False, 64)" should not be read as evidence either way.
**SAT controls** (`sat_controls.py`): clock-C's capR fixed as the cap in `sat_turn.py` at KS = 10, C = 47: SAT at
T = 14 (class 0, which our measured c_R = 0 predicts: T + 8 + 18 = 40), UNSAT at T = 12, 16, 18. k = 2 cap #7 fixed
in the 5 × 5 tube: SAT at T = 16, UNSAT at T = 14. So the encoding accepts the turns that exist, at the right time.

**The k = 2 caps of the 5 × 5 tube** (`python3 k2_oracle.py`, 7 s, oracle; also `python3 turn_check.py k2`, gs;
the eight caps are those `k2caps.py` wrote to `scratch/signals/k2caps_16_47.json`, the stored object is #0;
`cd research/signals && python3 ../audit/signals3/k2_regen.py` re-ran the enumeration and returned the same caps in
the same order as far as it got, see `scratch/signals3/k2_regen.txt`):
- all 8 are stationary (period 2) on the oracle, and each turns a lone rake into a mirror rake with **k = 2**
  (oracle = gs cell for cell for 60 generations; mirror rake at t = 20, one generation-pair later than capR's);
- **all 8 are destroyed by that lone turn**: within ~10 generations the cap and the wire between it and the mirror
  rake are eaten (kymograph of #2: `5f9f82`, `5f9f80`, `5f9f8?..`); the mirror rake runs on towards −v with a fire
  following it, its p> train eaten. At t = 60 the kymograph rows show the cap units dead or as debris (`?`), for
  all 8. No train or clock is needed for this.
- in the clock (capL + 9 units + cap, lit at unit 4, oracle): six caps give rake → mirror rake and then death; caps
  #2 and #3 give rake → mirror rake → rake with a′ − a = 40 = 4N + 4, i.e. **one round of a period ≡ 0 mod 4**
  (c_R = 2, c_L = 2, as the class arithmetic predicts), and then the burning wire reaches capL and the object dies
  (period 1 from t ≈ 46).
So "in the 5 × 5 tube eight k = 2 caps exist ... each turns a lone rake with k = 2" is true, but these are
self-destroying turns, and "each dies when put in a clock" happens for a reason the README does not give: they die
in the turn. "The 3 × 3 tube was the obstruction to a period-4N clock, not the rake" (section 18) and "fails one
size up" (PREDICTIONS K4) do not follow: no k = 2 cap that survives a single turn is known in any tube. (The 3 × 3
k = 0 turners are a fair comparison in one respect: their census also counts turns without asking for survival;
only 33 of 186 at C = 31 make clocks.)

## 5. The negatives (claim 5)

- **Writers**: above. The bounds are small (writer within about 5 units).
- **Turners, 3 × 3, k = 2 UNSAT**: condition = period-2 (4, 6) cap on units ≥ 10, a *lone* rake from far away
  writing (BC)^∞, the mirror rake exactly at units 4, 5 at T ≤ 28 (32 at C = 55), unit 2 untouched. Excludes
  fast lone turns of class 2, including self-destroying ones (no survival is asked), which makes it stronger than
  the clock needs in that respect; but it says nothing about a turn of a rake arriving behind a p> train (the clock's
  case, section 4 above), slow turns, or caps beyond the planes.
- **Back-to-back** (8,184) and **side kick** (5,625 placements): not re-run (cut). From the code: the side-kick
  test lights only the 150 + 55 placements that are stationary unlit (96% of the 5,625 are discarded at that step),
  uses only placements with a wire cell adjacent to the clock (N = 3, 3 periods + 20 generations), and counts any
  difference 14–40 units out as a candidate (so even a fire would have been seen). The README states the stationary
  counts; its "5,625 placements ... carries nothing away" should say 205 were tested lit. No positive control is
  possible for either scan without a known positive; none was attempted.
- **Two-sided turners**: the defect list was cut at 3,000 (README says so). Not re-run.

## Overstatements in the wording

- §18 "[proved] The period of a shuttle clock mod 4 is the sum of two cap constants" with k defined by a lone rake:
  proved for in-clock constants; equal to the lone ones only as measured (33 caps).
- §18 and the third-push summary: "in the 5 × 5 tube a cap of the other class exists, though not yet one that
  survives in a clock"; "the 3 × 3 tube was the obstruction to a period-4N clock, not the rake": the k = 2 caps do not
  survive one lone turn. Nothing shows the tube is the obstruction.
- §17 "s = 1 ... does not count (the wall becomes a mixed region)": on the oracle a run of B counts once, the wall
  stays clean, and the rest is reflected.
- Headline row "counter": add "on a ring; wire 8 has no cap and burns from a cut at one unit per generation".
- §15 "A periodic emitter (gun) at the +v end is exactly a writer": "a gun whose output is a train of p< in the 3 × 3
  tube". §16 "No writer of small period" is about word periods 2–4.
- §16 side kick "5,625 placements": 205 were lit.
- §18 "P ≡ k_R + k_L ... for clock-C the pair gives 2" next to "every right cap ... k = 0": say k_L(capL) = 2.

## Corrections the README needs (for an editor)

1. §18: state the convention: right caps measured have k_R = 0, capL has k_L = 2 (mirror shifts by one generation),
   so a period-4N clock with capL needs k_R = 2. Add: "k is proved to be a constant of the cap for a lone rake; in a
   clock the rake arrives directly behind a p> train, and the in-clock constant equals the lone one for all 33 clock
   caps at C = 31 (measured, second review 3, `turn_check.py`); so the SAT negative bounds lone turns, not clock
   turns."
2. §18, k = 2 caps: "all 8 are destroyed by the lone turn itself (oracle, `research/audit/signals3/k2_oracle.py`):
   the cap and the wire behind the mirror rake burn; two of them (#2, #3) complete one round of 4N + 4 in a clock
   before dying." Delete "So the 3 × 3 tube was the obstruction to a period-4N clock, not the rake"; in the summary,
   "a cap of the other class exists" → "a stationary cap that turns the rake once with the other class, and is
   destroyed doing it, exists".
3. §17: replace the s = 1 sentence: "a run of n ≥ 2 adjacent pulses moves the wall one unit and is reflected:
   BB returns exactly one p> (oracle, exact); B^n returns a right-going object (`9fb7bf` for n = 3, `9d…df` with
   n − 2 units of B′ for n ≥ 4)". Note it bears on the reflector question: the 8|C wall is a stationary reflector of double pulses (not of
   single ones). Add that wire 8 burns from a cut end at one unit per generation; the counter is shown on a ring.
4. §17: `verify_counter.py` row: oracle confirms trains of up to 27 pulses and irregular spacings (this review).
5. §15: qualify "exactly a writer" (p< trains in the 3 × 3 tube); list what the writer negatives do not cover (wide
   pulses, rakes or mirror rakes as output, word periods ≥ 5, emitters beside or inside a wire).
6. §16: side kick: 205 placements lit (the stationary ones).
7. PREDICTIONS K4 scoring "fails one size up": the k = 2 caps self-destruct; nothing about clocks fails one size up.
8. `turnclass.py`'s "restored" flag is False for clock-C's own capR; it should not be quoted (k2caps output).

## Not checked / cut

The back-to-back and side-kick scans (not re-run; no positive control); `turners.py`, `wallturn.py`, `sat_defects.py`;
the SAT negatives themselves beyond the fixed-cap controls (no re-solve of the UNSAT instances, no second solver);
completeness of the 8 k = 2 caps (the re-run reproduces the first caps in order; see `k2_regen.txt` for how far it
got); the reader census with U = 6 and `--nobb`, and its closure at C = 33; survival of the 186 lone 3 × 3 turners
outside clocks; the lone left-turn constant of capL measured directly (only in clocks); `sat_turn --eat`; whether
the BB reflection at 8|C can be made into a shuttle. Time: about 90 minutes, two cores.
