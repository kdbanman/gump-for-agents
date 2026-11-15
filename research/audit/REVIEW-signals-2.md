# Review: signals, second push (README sections 8–14, PREDICTIONS S6–S10 / J1–J10)

Adversarial review, 2026-11-15. Everything below was computed with code in `research/audit/signals2/`, all of
which steps with `reference/oracle.py` or with `gs.py`, a stepper of its own whose neighbour offsets are written
from the text of `docs/AUTOMATON.md` and which is checked cell for cell against `oracle.step` (`python3 gs.py`,
1 s: three box tori, three densities, 30 generations; batched equals unbatched). No study code is imported except
in `sat_compare.py`, whose job is to test the study's SAT encoding. Commands run from `research/audit/signals2/`.
Bulk output: `research/scratch/signals2/`.

Wherever the oracle is run on a non-cubic box `(2L, 16, 2L)` for a ring of L units of the tube (tape, rake), the
box is the ring exactly: the ring's copies on the box differ by 2L >= 12 in x+z and by 16 in y, a neighbour moves
x+z by at most 4 and y by at most 2, and every generation is checked to have no live cell outside the tube taken
modulo the box. Finite objects (clock) are run on a box `(2N+48, 24, 2N+48)` with every generation checked to have
no live cell outside the object's diagonal hull, so by T2 the box is never felt.

## Verdicts

| # | claim | verdict |
|---|---|---|
| 1 | clock: period 4N + 2 for every N | **stands**; proof complete as written; statement true wherever tested (oracle N ≤ 257 at 16 values, gs N ≤ 400 all). Wording corrections below |
| 2 | rake | **stands** (oracle, m ≤ 40, separations 3–22, and the mirror rake against p>, which the study had only on `sg`) |
| 3 | collision gate | not re-run (the lead did twelve separations); naming remark below |
| 4 | register | **stands with a correction**: a bounded up/down counter with 16 positions, not a register; breaks when the wall reaches an operation site |
| 5 | tape theorem | **stands**; proof complete as written; 36 further words on rings of 6–41 units all pass on the oracle |
| 6 | soup-born carriers | **stands with a correction**: numbers reproduce, but 93% of the carriers come from rings of ONE unit, where the soup is translation-invariant by construction; none from rings of 3, 4, 6 units |
| 7 | wire against chaos | **stands with corrections**: "every time" holds at the study's block (and 1,200 more sides); "at pulse speed" holds for wire B at every density tried but not for wire C at low density; "two empty layers isolate it for ever" is exact for the capped end but **false** for a wire running past chaos |
| 8 | negatives | **stand** within the stated bounds; the cap census is confirmed by brute force at C = 25, 27; the reflector UNSATs reproduce with Glucose and extend to odd delays; what they exclude is narrower than the wording |

## 1. The clock (claim 1)

**The proof as mathematics.** Unit u = cells with x in {2u, 2u+1}. An axis-0 cell (x odd, x = 2u+1) has
neighbours at x ± 1, i.e. units u and u+1; an axis-1 or axis-2 cell (x = 2u) has neighbours at x ± 1 and x ± 2,
units u−1, u, u+1. So information moves at most one unit per generation along v, and sideways the whole slab x ∈
{2u, 2u+1} is in the unit, so no sideways radius is needed. The README's light cone is right.
With that, I re-derived the surgery from the README's text: (i) chart i supplies unit m+i; Claim A for the pair
(i, i+1) gives Y on [m+i, m+i+1] = τ^i X(c_i)|[m, m+1], and Claim A for (i−1, i) gives Y on unit m+i−1 =
τ^i X(c_i)|{m−1}; so the 3-unit neighbourhood of every unit is a translate of a base neighbourhood and the light
cone applies. (ii) Time in chart i advances by one except at its j−i loop-backs at ta (B3, units ≤ m+1, covers
unit m and the left half line of chart 0) and its i loop-backs at tb (B4, units ≥ m−1, covers the right half line
of chart j); chart 0 never loops at tb and chart j never at ta, which is what the end charts need. (iii) Minimal
period: Y's strip [m−1, m+1] equals X(c_0(t))'s strip (A with i = 0), c_0 passes tR once per period and tR is not
a loop value, and B5. (iv) For general j, the pair (c_i, c_{i+1}) depends only on t − 2i and on the loop lengths
4(j−i), 4i: long loops only lengthen stretches where both charts are in the same loop (difference ±2 inside
[ta−3, ta] or [tb−3, tb], covered by both B1 and B2), so the finite set of pair types is exhausted at small j.
**I find the argument complete.** The one thing it rests on beyond B0–B5 is the case analysis of Claim A, which
the README gives in words and the script enumerates for j ≤ 40; I enumerated it with my own c_i for j ≤ 150.

`python3 prove_check.py 8 4 150 1 2 139` (6 s), all PASS: light cone; the base cycle (N0 = 8, period 34) on the
oracle; B1–B5 recomputed (B1 fails at s = −1..2 and B2 at 16..19, just outside their ranges, so the ranges are
tight but sufficient); each chart steps +1 except j−i loop-backs at ta and i at tb, and c_i(t+P) = c_i(t)+p; Claim
A for every j ≤ 150; Y assembled and stepped for a whole period for j = 1, 2, 139 (N = 9, 10, 147) with exact
period, and the lit clock falls into Y. Also `python3 prove_check.py 12 5 40 9` (base N0 = 12) passes.

**The statement where a wrong proof would show.** `python3 clock_oracle.py N ...` (oracle; seconds to 6 min):
N = 1, 2, 3, 9, 10, 11, 13, 25, 50, 64, 100, 127, 200, 257. For every one: the unlit object has period 2; the lit
object enters a cycle of period exactly 4N + 2 (the first repeat, confirmed cell for cell); no cell is ever alive
outside the diagonal hull of the unlit object. `python3 clock_scan.py 1 400` (gs, 2 min): the same for every N
from 1 to 400.
**The transient is exactly max(N − 2, 0) generations** for every N tested (oracle: all 14 values; gs: 1..400).
"Falls into the cycle" is still measured, not proved, but it now has a clean form that a proof could aim at.

**Other single added cells** (`python3 clock_ignitions.py 5 12 13`, 2 min, gs; every dead cell of the hull and
every dead neighbour of the object, 332 / 521 / 548 candidates): period 4N + 2 from 11 / 25 / 27 cells (two per
unit along the whole wire: lighting works anywhere, not only in the middle); healed back to the unlit object 138 /
187 / 194; other still lifes and period-2 states; small periods 3, 4, 5, 6, 12. One addition at N = 5,
(1,2,4), gives **period 20 = 4N** (oracle: `python3 p20.py 5 20`); it is not a shuttle: the wire breaks, units
2–3 empty, and two separate oscillators of periods 4 and 5 remain (lcm 20). So no period ≡ 0 mod 4 clock here
either.

**Free-standing:** yes, as checked above (hull never left, unlit object stationary, period 2).

## 2. The tape (claim 5)

**The proof.** At an even generation the tape is a union of letter units; step² of a unit depends on the 5 units
around it (light cone, two generations); the claim for one double step is local: the centre unit of every window
of 5 letters becomes the letter to its right. A ring containing all 32 windows checks all of them. The rest is
induction. Complete. `tape-BC.json` does hold all 32 cyclic windows (checked from the file). Nothing about the
odd generation is needed.
**Tested where it would fail:** `python3 tape_check.py` (2 s, oracle): 27 random words on rings of 6, 7, 9, 11, 13,
16, 23, 32, 41 units, a single C in B, a single B in C, B^10 C^10, (BC)^10, (BBC)^7, all B, all C, and two
long-run words; each for a lap plus 4 double steps: whole state equals the start moved j units towards −v, and
nothing leaves the tube. All pass. The consequences drawn (p< is one B in C; a single C in B is a left-going
pulse of wire B; packing at any spacing; a wall is a front) follow and the single-letter cases were run.
Not checked: the half-turn statement for B and C′; what p> does to longer B stretches.

## 3. Rake (claim 2)

`python3 rake_check.py` (11 s, oracle): R1 rake alone, the exact state (rake at u0+m, p< at u0+m−2, .., u0−m) for
m = 1..40 (study: 10). R2 against p< at separations 3..22: even eaten (state = rake alone), odd stops (no rake,
the state moves rigidly) — all twenty as claimed. R3 (the study had it on `sg` only): the mirror rake, built as the
image of the rake one generation on under (x,y,z) ↦ (z−4, y, x+4), runs towards −v emitting p> every 2
generations, and against p> at separations 3..20 obeys the same parity. R4 rake against mirror rake (kymographs
printed): one survives, by parity (separation 10, 12: the mirror rake; 11, 13: the rake), **but the collision is
not clean**: a two-unit mark travels on with the survivor's train (`dd` in the p> train, or `77`, two adjacent
B units, in the p< train). The README's "one of the two survives" should say so.

## 4. Register (claim 4)

`python3 register_check.py` (1 min, oracle), on the study's object and operations:
- long runs one way: W×1..8 match (wall 6 → −2); **W×9 and W×10 do not** (29 and 136 cells differ): the wall has
  reached the write site's unit (−3). E×1..7 match (wall → 13); **E×8..11 do not**: the wall is at the erase
  site's unit (13). The caps are never reached; the operation sites bound it. **16 positions, w = −2..13.**
- alternation WEWEWEWEWE and EEEEWWWWWWWWEEEE: match.
- a pulse arriving while the wall is still moving: W then E 1..31 generations later, E then W 1..27 later: all
  match (wall back at 6). W then W 4..30 later and four W's 4 apart: match.
- **W then W 2 generations later, and four W's 2 apart: do not** (2 and 4 cells differ): the emitter cannot fire
  twice in two generations.
So: a reversible up/down counter of range 16 with this placement of the sites, robust to timing at the wall. Not
a register in the usual sense (no addressable bit, nothing read out, no same-side toggle); "counter" is the word.
The README's "the state after any sequence depends only on the difference" needs "while the count stays in
range (−8 ≤ #E − #W ≤ 7 here)".

## 5. Soups (claim 6)

`python3 soups_check.py 20000 11` (5 min; own stepper, checked against the oracle on a ring of 12 and against lifts
for L = 1, 2, 3, 4, 6): 100,000 soups (20,000 per ring length), density 0.4, 3,000 generations. Uniform wires of
period ≤ 2: **12,789** (study 12,780); **368** distinct (366); **10** carry a 2-cell pulse, born in **305** soups
(279). The proportions hold. But by ring length: uniform wires 11,604 / 913 / 254 / 18 / **0** for L = 1, 2, 3, 4, 6,
and the carriers **284 from L = 1, 21 from L = 2, none from L = 3, 4, 6**. On a ring of one unit the soup is a
pattern of period one unit to begin with: 14 random bits repeated. So what is shown is that a random
*translation-invariant* (or period-2-unit) pattern of the tube settles into a carrier about once in 70; a soup with
no imposed periodicity of 3 or more units never did (0 of 60,000). "Pulse-carrying wires are born from random soup"
and "about one soup in 360" overstate this. (I did not identify my 10 carriers with B/C/the third wire; all have 5
cells per unit and pulses both ways, as the study's.)

## 6. Wire against chaos (claim 7)

`python3 chaos_check.py WIRE SOUP RHO W NRUN SEED` (own stepper; ring of 400 units in the 11 × 11 tube instead of a
capped wire, block of the study's shape; probes 40 and 80 units out; 400 generations; my "clean thing ahead": the
far probe bare for ≥ 6 generations between its first change and the front). `bash chaos_batch.sh` (20 min),
output in `research/scratch/signals2/chaos_batch.txt`; sides on which the far probe was reached, speed in
generations per unit between the probes, clean ahead:

| wire, soup, ρ, W | sides reached | speed 2 / 4 | clean ahead | wire bare at end |
|---|---|---|---|---|
| C all 0.4 12 (100 runs) | 200/200 | 199 / 1 | 5 | 0 |
| B all 0.4 12 (100) | 200/200 | 200 / 0 | 0 | 0 |
| C outside 0.4 12 (50) | 100/100 | 100 / 0 | 4 | 0 |
| B outside 0.4 12 (50) | 100/100 | 100 / 0 | **1** | 0 |
| C all 0.2 12 | 100/100 | **56 / 44** | 5 | 0 |
| C all 0.6 12 | 100/100 | 100 / 0 | 0 | 0 |
| C all 0.1 12 | 100/100 | **23 / 77** | 5 | 0 |
| C all 0.4 4 | 100/100 | 98 / 2 | 3 | 0 |
| C all 0.4 24 | 100/100 | 98 / 2 | 2 | 0 |
| C all 0.4 1 (71 cells) | 100/100 | 95 / 4 | 1 | **1** |
| B all 0.2, 0.1 12; B all 0.4 4, 1 | 400/400 | 400 / 0 | 0 | 0 |

So: destruction on every side survives (1,500 of 1,500 sides here, except one side of a 71-cell block where the far
probe was bare again at the end). The speed is the pulse speed for wire B at every density and size (the leading
edge is the B|C wall, the tape), but for wire C at low density the fire is mostly the slow 4-generation burn of a
cut wire C: "destroyed at pulse speed" is a statement about ρ = 0.4 and wire C. Clean things ahead: 5 of 200 sides
for wire C at the study's setting (study 15 of 200 by its criterion; the rate depends on the criterion), and one
on wire B with soup round an unbroken wire (study: 0 of 400). Not checked: what they are.

**Isolation.** `python3 isolation.py` (5 s). (1) The capped end, the study's geometry, recounted: G = 0: 4 live
wire cells touch the block and 11 outside cells could be born, per phase; G = 1: 0 and 1 (study: 28 touching
cells, 2 can be born, both phases together: same); **G = 2: 0 and 0** (1 touching cell per phase, as the study);
G = 3: nothing touches. Max block neighbours of an outside cell is 3 (T2). These counts are sufficient: by induction
the soup stays in its planes (an outside cell sees ≤ 3 block cells and, with "could be born" = 0, not enough wire
cells to reach 4), no block cell ever sees a live wire cell (the touching-live count is 0 and adjacency is
symmetric), and every outside cell sees what the wire alone shows it. **So the isolation at G = 2 is exact for
this cap.** (The study's count omits the block cells next to live wire cells, but that number is the same as its
"live ones" by symmetry, so nothing is missing.)
(2) **A wire running past a slab of soup** (ring of wire C, soup in x+y+z ≥ 5 + 2(G+1), G empty layers between):
G = 2: 72 outside cells per phase could be born, and **the wire is changed in 20 of 20 soups at generation 2**;
G = 1: 20 of 20 at generation 1; G = 3: 0 of 20 (T3). Two empty layers isolate the capped END of wire C; they do
not isolate a wire from chaos in general. Three do (T3), always.

## 7. Negatives and the SAT encoding (claim 8)

`python3 cap_brute.py WIRE C` (brute force over all 2^nfree generation-0 states; 10 s at C = 25, 20 min at 27) and
`python3 sat_compare.py WIRE C` (the study's `caps.enumerate_caps` against it):
- wire B, C = 25: 19 free cells, 0 caps by both; C = 27: 26 free cells, **2 caps by both, the same two cell sets**
  (one is the 8-cell eater). Wire C, C = 25: 0 by both; C = 27: **3 caps by both, the same three cell sets** (brute
  force 20 min; SAT list printed by `caps.enumerate_caps(wire, 27, 1, 5, 6)`). So the census encoding finds every
  cap and only caps on four instances with a known answer (two of them non-empty).
- reflectors: `sat_reflect.py T 29 --solver glucose4` reproduces UNSAT for pulse B at T = 8, 10, 12 and for pulse C
  at T = 8, 10; the encoding's positive control (`--absorb`, T = 12, C = 29) is SAT and the eater it returns steps
  correctly. Odd delays, which the study did not search: pulse B, T = 9, 11, 13, 15 at C = 29 and 33, all UNSAT.
What the negatives exclude, exactly:
- "No cap of wire B reflects or toggles": complete census of period-2 caps inside the 3 × 3 tube and the planes
  C ≤ 33, each hit by the pulse in simulation. Not excluded: caps of period > 2, caps reaching outside the tube
  (the wide pulses of section 10 show the tube is too tight a space for this wire family), caps beyond C = 33.
- "No restoring reflector" (`sat_reflect.py`): the reflected pulse must be exactly the left-moving pulse, at unit
  3 at generation T, AND the cap must be exactly restored at that same generation, only three units from the cap's
  first unit. A reflector whose cap is still settling when the returning pulse passes unit 3 is not excluded at any
  T. For C ≤ 33 the result also follows from the census plus the shooting test, independently of T.
- "Every reflecting cap of wire C is changed": C = 29, 31 complete; C = 33 the first 4,000 caps only.

## Overstatements in the wording

- "**register**": it is a bounded up/down counter (16 positions here), written and erased only from opposite ends;
  no bit is addressable or read. Call it a counter.
- "**gate**" / "collision gate": an inhibition element whose outputs are the input lines; the README says so in
  section 10, but the headline table and the summary say "gate" bare.
- "**clock**": an oscillator with no output line; fine as a name if "oscillator of every period 4N+2" is the claim.
- "**answers open problem 12**": problem 12 asks for periods beyond 66; the family gives every period ≡ 2 mod 4,
  proved; that answers "are periods bounded" (no). It does not touch periods ≡ 0 mod 4 or odd, as OPEN-PROBLEMS
  already says.
- "**pulse-carrying wires are born from random soup** ... about one soup in 360": almost all from rings of one unit.
- "**contact destroys the wire every time at pulse speed**": at ρ = 0.4; for wire C at ρ ≤ 0.2 mostly at half that.
- "**two empty layers isolate it for ever**" (section 13, the summary at line 219, OPEN-PROBLEMS 13, OWNER-JOURNAL
  10:30 entry "Leave two empty layers between them and nothing ever crosses"): true for the capped end tested,
  false for a wire passing chaos at two layers. *This bears on the owner's isolation note*: the hard edge is three
  layers in general (T3), two only at that end.

## Corrections the README needs (for an editor)

1. §9 register: "the state after any sequence depends only on the difference" → add "while the wall stays between
   the write and erase sites (here 16 positions, w = −2..13); beyond that it breaks; two writes 2 generations apart
   do not make two pulses". Consider "counter" for "register" throughout.
2. §10, rake against rake: "one of the two survives, by parity" → add "and a two-unit mark (dd or 77) travels on
   with its train" [oracle, `rake_check.py` R4]. Mirror rake against p> is now on the oracle (R3).
3. §11: add "the lit clock enters its cycle after exactly max(N−2, 0) generations (oracle N ≤ 257 at 14 values,
   gs N ≤ 400)"; "lit by adding (1,0,4) of the middle unit" → any of two cells per unit lights it.
4. §12: report the soups by ring length; "born from soup" → "born from soups of period one or two units (284 and 21
   of 305); none in 60,000 soups on rings of 3, 4, 6 units".
5. §13 and the opening summary: "two empty layers isolate it for ever" → "two empty layers isolate the capped end of
   wire C (exact, by the count); a wire running past chaos at two layers is struck at once; three always isolate
   (T3)". "At pulse speed" → "at pulse speed at ρ = 0.4 (and for wire B at every density tried); wire C at
   ρ = 0.1–0.2 mostly burns at 4 generations per unit".
6. §8: state the reflector search's real exclusion (cap restored by the time the pulse is back at unit 3; only the
   exact left pulse); add the odd delays now searched (UNSAT, pulse B, T = 9..15, C = 29, 33) and the second solver.
7. §11 proof text is fine; optional: say that Claim A was enumerated by an independent script for j ≤ 150.

## Not checked / cut

The gate (lead did it); the wide pulses; the scattering table at C = 31, 33 and `clocks.py`'s other caps; walls.py
and the static pairs of `tapes.py`; `caps_any.py` (the other 29 wires); `sat_reflect.py` at C = 37 and with pulse C
beyond T = 10; the half-turn statement of the tape; identification of my soup carriers with B/C; the life-time of
the block alone (`chaoswire.py life`); PREDICTIONS.md scoring was read but not audited forecast by forecast.
