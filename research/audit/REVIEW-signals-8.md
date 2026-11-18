# Review: signals, eighth push (`research/signals/push8/`: the memory cell, the two reads, the proof, the negatives)

Adversarial review, 2026-11-18. Code in `research/audit/signals8/`; every command below is run from there unless a
path is given. Small outputs: `research/audit/signals8/out/`. Times are wall-clock on the shared machine.

**Steppers.** `a8.Orc` is `reference/oracle.py`'s `step`, unchanged, on a rectangular array in which nothing wraps
(the four outer index planes are asserted dead after every generation; masks by the oracle's formula with the
array's origin). `a8.Box` / `st8.c` is my own stepper (neighbour offsets built from `docs/AUTOMATON.md` §2 and
asserted equal to `oracle.offsets`); no code of `research/signals/` is imported anywhere. `python3 check_st8.py`
(90 s, ALL PASS): st8 equals the oracle on the whole state at every generation on the protocol (520 generations),
nine destroyed or wrecked cells, trains, a pulse sent into a count read, 30 of the 760 census events drawn at random,
the outside cell (1,4,2), push 7's right cap at both phases, and soup against a set stepper. From the push: initial
cells only (`objects/cell8.json`: the two caps, stators, sites; `objects/caps.json`: push 7's right cap;
`objects/line7-read.json`: push 7's line and the cells of its writes).

The push's four headline commands pass as stated: `verify_cell8.py` 6 s, `prove_unzip8.py` 5 s, `verify_read8.py`
48 s, `check8.py` 43 s (run from `research/signals/push8/`).

Notation as in the push: unit u = cells with x in {2u, 2u+1}; letters 7 = wire B, d = wire B′, f = edge unit,
b = one unit of wire C in wire B = a left-going pulse, `6f` = a right-going pulse; R@u / L@u = the stator (0,1,2) /
(0,1,4) of unit u removed. "Place p" = wire place, unit 4 + p; a cell has N wire units (places 0..N−1).

## Verdicts

| # | claim | verdict | in one line |
|---|---|---|---|
| 1 | the cell: capL + 7^N + capL turned round, period 2, 38 + 5N cells | **confirmed** | oracle: period exactly 2 for N = 4..30; N = 7 empty and holding 2: 20,000 generations each |
| 2 | "smallest at 73 cells" (N = 7) | **corrected** | N = 7 is the smallest on which two released pulses are on the wire at once; set, add one and a read that empties the cell all exist at N = 6 (68 cells), set at N = 5 (63) |
| 3 | set: two pulses leave `df`; "u′ − u even: they pass" | **confirmed for u′ − u ≥ 3; corrected below that and at the caps** | u′ − u = 2 burns the whole cell down to 12 cells, u′ − u = 1 wrecks the wire; R@4, R@(N+3), L@4, L@5 do not make a pulse and destroy or wreck the cell |
| 4 | "every later pulse is absorbed and lengthens it by one. So it counts" | **confirmed for pulses two or more units apart; corrected for adjacent pulses** | a block of m pulses one unit apart adds ⌈m/2⌉; the same stator removed twice two generations apart makes such a pair and is counted once |
| 5 | bit read: crosses an empty cell, absorbed by a full one | **confirmed** | oracle, cell and push 7's line at both phases; the answer is the pulse on the far side, which the far cap swallows; a full store gains one |
| 6 | count read: exactly k pulses, the cell empty again | **confirmed, time bound sharpened** | oracle, k = 1..20 in the cell at every even generation from 2k + 6 (the push says 4k + 8), then exactly the empty cell; selected k to 40 |
| 7 | proof for every k | **a proof**; three places it passes over are closed here | finite runs against the infinite wire; H(k+1) at t = 2, 3; the time bound for 11 ≤ k ≤ 24 (section 3) |
| 8 | transfer: k into a store holding 1 gives k + 1 | **confirmed, one condition added** | oracle k = 1..8; the receiver's edge must be at least 2 units from the store's wall (at 1 unit both stores are lost) |
| 9 | "take one off": a stator inside the stretch gives k − 1 | **corrected** | only the first two units ((0,1,2)) or the last unit and the edge ((0,1,4)); the other end's two units empty the store, the middle does nothing |
| 10 | census of 760 one-cell events | **confirmed; one count corrected** | 526 / 134 / 72 / 10 / 8 / 6 / 4 reproduced event by event; the 134 are 66 to the left and 68 to the right, not 67 and 67 |
| 11 | eight release laws to k = 40; catch to k = 12 | **confirmed** | st8 for every k; oracle at k = 5, 17 (laws) and 3, 7, 12 (catch) |
| 12 | caps of push 7's line (section 3) | **confirmed** | oracle: right cap swallows at one phase and the line burns at the other; a stretch against capL is erased in 4k + 4 |
| 13 | the reads on push 7's line | **confirmed, at both phases** | oracle at 882 and 884: (b7)^n out, the n = 1 line left; the count read of the EMPTY line at 884 destroys the line |
| 14 | no read triggered by an arriving pulse | **confirmed within its bounds; the bounds are narrower than the summary reads, and the claim is overtaken** | k = 3: the 48 states replayed with st8 (96 of 96 outcomes equal, six on the oracle): none releases; one six-cell still life BESIDE the wall (push 9's) makes an arriving pulse release the count: oracle run here |
| 15 | no read that keeps the count; no second-wire probe; no re-arming | **not found stands; not rebuilt** | counts of the second-wire scan reproduced with the push's code; nothing independent |
| 16 | "`df` is the first push's mark" and what is new | **confirmed; see section 4** | the absorbing wall and the mark's absorption are the first two pushes'; the release, the transfer, the cell and the line reads are new |
| 17 | forecasts | **arithmetic confirmed (0.101)** | forecast 9 holds by one two-cell event only; README's "No new mover" beside it is wrong |

## 1. The cell and its protocol, rebuilt

`python3 proto8.py` (251 s; oracle only; 27 PASS lines; `out/proto8.txt`).

- **Stands.** The empty cell has 38 + 5N cells and period exactly 2 for N = 4..30. N = 7 (73 cells) empty, and
  holding 2 (`777ddf7`), equal the start at every even generation to 20,000. Every stored state used, and
  `7 d^k f 7^(22−k)` for k = 1..21 on N = 24, is exactly periodic with period 2. Exact period on a finite object is
  for ever, so "how long" has no other answer.
- **Set.** N = 7: R@5 and L@10 give exactly `777df77` from generation 6. N = 9, every pair R@p, L@q in one
  generation (72 pairs, each 240 generations, whole state): exactly the 9 pairs with p ≥ 1, q − p odd and ≥ 3 leave
  one `df`, with d at place (p + q − 1)/2; for 1 ≤ p ≤ N − 2 the cell is empty again exactly when q ≥ 2 and
  (q − p even and ≥ 4, or q ≤ p − 2). **28 pairs burn the cell down to 12 cells**: every q − p = 2 (p ≥ 1), every
  q ≤ 1, every p = N − 1. 15 leave another object (|q − p| = 1; p = 0 with some q). With a delay
  (`tables8.py pairs`, st8, N = 20, L@q at generation dt = 0, 2, 4, 6): the rule is in s = q − p − dt/2, set for s
  odd ≥ 3, pass for s even ≥ 4, no exception in 802 cases; s = 2 burns (50 of 50).
- **Operations next to a cap** (oracle, N = 12): R@place 0 turns the wire into another object (97 cells, still
  changing at 400); R@last place, L@place 0 and L@place 1 burn the cell down to 12 cells. So R@u needs
  5 ≤ u ≤ N + 2 and L@u needs 6 ≤ u ≤ N + 3. The push's own runs stay inside this.
- **Add one, bit read, count read on a cell written by signals only** (N = 24; set by R@8, L@21; adds R@6, L@27,
  R@5; read R@11): counts 1, 2, 3, 4 with the wall or the edge moved on the side hit; during the absorbing bit read
  no unit to the right of the edge ever differs from the standing cell at an even generation; the read gives
  `b7b7b7b` exactly (4 even generations with all four on the wire), then the cell is exactly the empty cell from
  generation +34. On the empty cell R@6 is at place 18 at generation 34 as an exact `6f`, then the right cap
  swallows it.
- **Count read for k = 1..20** (N = 3k + 12, stretch laid from letters): at every even generation from 2k + 6 to
  4k + 20 the whole state is the empty cell with exactly k units b two apart, the leading one at place
  wall + 2 − t/2, and at no even generation before 2k + 6; at 8k + 160 exactly the empty cell.
- **Transfer.** Stores 1 and 3: the left one holds 4 and the right one is gone. k = 1..8 into a receiver four
  units away: k + 1. The receiver grows on the side the pulses come from. Gap between the receiver's edge and the
  store's wall (`tables8.py gap`, st8, k = 1..6): 2 to 6 units: k + 1; **1 unit: both stores are lost**, the cell
  is empty (the removed stator is next to both).

### Beyond the push's runs

`python3 tables8.py` (196 s, st8, ALL PASS; `out/tables8.txt`); one case of each law is on the oracle in
`proto8.py` section G.

- **Adjacent pulses are counted in pairs.** 1,024 runs (k = 1..4, distances 2..9, both sides): a block of m pulses
  one unit apart (`6e^(m−1)f` from the left, `b^m` from the right, m = 1..8) adds ⌈m/2⌉; blocks separated by one
  or more plain units add up. Such blocks are made by ordinary operations: R@8 at generations 0 and 2 puts `6ef` on
  the wire and a store goes from 1 to 2, not 3 (oracle); at generations 0 and 4 (pulses two apart) it goes to 3.
  The push lists `6ef` and `bb` among what a stretch absorbs "by 1" (its section 2) without saying that each is
  two pulses. The count read's own output is two apart, so a transfer is exact. A release as a block is not: the
  law `b^(2k+2)` of section 5 is received as k + 1.
- **Pulses from both sides at once**: a formed pulse 1..12 units from the wall and another 1..12 units from the
  edge, k = 1..4 (576 runs): always count + 2, no exception, also at k = 1.
- **A pulse sent into a count read.** A right-going pulse D units before the wall when the read starts
  (D = 2..45, k = 1..6): D odd (and D = 2): it passes all k pulses and the cell ends empty. **D even ≥ 4: it stops
  the first released pulse, the mark `df` absorbs the other k − 1, and a store with the same count k stands again**
  with its first d at wall − D/2 (oracle: k = 3, D = 4, 5, 8, 9). A left-going pulse behind the edge during a read
  (D = 1..24): it joins the train; a receiver ends with k + 2.
- **Capacity.** Laid from letters, `d^k f` stands at every place from 1 to the last (k ≤ N − 2); with its first
  unit at place 0 capL erases it. Written by signals, senders at place 1 and at the last place (N = 7, 12, 16):
  full at k = N − 4, wall at place 2, edge at place N − 2; the next R@place 1 or L@last place is then the count
  read and the count leaves into the cap. A stretch never reaches a cap by signals.
- **The fixed sender** (oracle): the same operation R@6 six times on a store `df` at place 6 gives `ddf`, `dddf`,
  `ddddf`, empty, empty, empty. The wall walks to the sender and the next shot is the count read. So the reader
  need not know where the stretch begins (README section 6, "What the cell is not"): one fixed stator is add one
  until the store has reached it and then releases everything. It is still a cell changed by hand.
- **Operations at odd generations and on the stretch itself**: `out/tables8.txt`, `singles`. `laws8.py inside`
  (st8, k = 1..7, phase 0): (0,1,2) of the first two units of the stretch gives k − 1 (k ≥ 3; k = 2: the first
  only), of the last unit or the edge unit empties the store, of any unit between does nothing; (0,1,4) is the
  mirror image. The push's table row "take one off" is true for those units only.
- **The smallest cell** (`python3 laws8.py smallest`, 11 s, st8; every placement of every operation): N = 3, 4
  nothing; N = 5 (63 cells) one set; N = 6 (68 cells) 2 sets, 2 adds, 7 single operations that empty a cell
  holding 2; N = 7: 4 sets, 6 adds, 16 emptying operations, of which one shows two separate pulses in an exact
  state. The push's "N = 4, 5, 6: none" is true of its criterion (two pulses seen at once), not of the protocol.
  On the oracle (`python3 extra8.py small6`, 2 s): N = 6, R@5 + L@8 gives `77df77`, L@9 gives `77ddf7`, R@5 gives
  the empty cell, whole states; N = 5, R@5 + L@8 gives `77df7`. Only capL and its image were tried as caps by
  anyone.

## 2. The reads of push 7's line

`python3 line8.py` (4 min, oracle, ALL PASS; `out/line8.txt`). The five written lines are periodic at 882 with
the wire `7^76` (n = 1) and `7^37 d^n f 7^(38−n)` (n = 2..5); none has period 2 (the right cap has period 4), so
each read was run at 882 and at 884.

- Count read (stator (0,1,2) of unit 40), n = 2, 3, 4, both phases: (b7)^n on the wire 40 generations later, the
  whole state the n = 1 line 221 generations later.
- Bit read from the right (stator (0,1,4) of unit 70), both phases: n = 1 crosses and capL swallows it; n = 2, 3,
  4: the whole state is exactly the line of n + 1 holes.
- **The same count read on the empty line (n = 1) at 884 destroys the line** (238 cells and burning 221
  generations later; at 882 it is restored). The bit read from the left destroys the n = 1 line at 884 too and is
  absorbed for n = 2, 3 (`7^36 d^(n+1) f …`, caps intact). The push says this of its right cap (section 3); on the
  line "the same cell for every n" is therefore safe for n = 1 only at generations ≡ 2 mod 4.

## 3. The proof that the count read gives k pulses for every k

`python3 proof8.py --direct 11,12,13,14,15,16,17,18,20,25,30,40` (62 s, oracle, ALL PASS; `out/proof8.txt`).

**It is a proof.** The induction step follows from what is checked. With Y(t) = X_k(t) on units ≤ m(t) + 1 and
τX_k(t − 2) on units ≥ m(t): a unit u ≤ m(t) has its three-unit neighbourhood in the left chart and u ≤ m(t+1) + 1;
a unit u ≥ m(t) + 1 has it in the right chart and u ≥ m(t+1); so |m(t+1) − m(t)| ≤ 1 and agreement on the two
overlap units make Y an orbit. Y(2) = X_{k+1}(2) as the docstring says (the bound m(2) ≥ w + 2 would do). The
condition m(t) ≤ m(t−2) + 1 is what carries H to k + 1. The tape theorem is used inside its hypotheses: for the
infinite wire, at an even generation, for a word over {7, b}; I re-ran its base on the oracle (a ring of 32 units
holding every run of five over {7, b}: moved one unit towards −v every 2 generations, 40 times).

Three places the docstring passes over, each closed:

1. **Finite runs for the infinite wire.** "Within T generations nothing reaches a cap" is not what a light cone
   gives (the caps' cone covers the whole compared window by generation 80), and the script does not check it.
   What is needed: at every generation the finite run equals the standing cell near both caps; then the run glued
   to plain wire across a standing seam is the infinite wire's orbit. Checked at every generation for every k run
   (k = 1..12 and the direct list): equal to the standing cell on all units ≤ lead − 4 and ≥ w + k + 3.
2. **H(k+1) at t = 2 and t = 3.** There τX_{k+1}(t − 2) is not a glued state. It holds because X_{k+1}(0), X_{k+1}(1)
   equal X_k(0), X_k(1) on units ≤ w + k − 1, w + k − 2 and m(3) ≤ w + k − 3. Also checked directly: H(11) and
   H(12) hold along the same path at every t = 2..92, and the direct runs of k = 11, 12 are the glued orbits at
   every generation.
3. **The continuation of the path and the time bound.** The script tests the continuation m = lead + 3 at even
   t only; at odd t it follows from the tape theorem by one step (the state at T is invariant under a move of two
   units on units lead + 1 .. lead + 2k − 1, hence one generation later on lead + 2 .. lead + 2k − 2), and it is
   checked here at both parities for t = 80..92. As written the induction places the seam inside the train only
   at t ≥ T = 80, so it gives the final state of k + 1 from max(80, t_k + 2) on, i.e. from 2k + 58 for k ≥ 11:
   later than the stated 4k + 8 for 11 ≤ k ≤ 24. Closed two ways. (i) Direct runs (k = 11..18, 20, 25, 30, 40:
   exact at every even generation from 2k + 6 to 4k + 12, and not at 2k + 4). (ii) An argument: at an even t at which both charts are final (t ≥ 2k + 8, given
   the claim for k from 2k + 6), they differ exactly at the units lead and lead + 2k, so H excludes
   m − lead in {−1, 0, 1} and m − (lead + 2k) in {−1, 0, 1}; from one even generation to the next m − lead rises
   by at most 2 and falls by at most 1 (m(t) ≤ m(t − 2) + 1, steps ≤ 1, the lead one unit on); so a seam ahead of
   the lead cannot get behind it and a seam behind the last pulse cannot get in front of it; it is inside the
   train at T, hence at every even t from 2k + 8 to T, where the glued state is the k + 1 pulses. With the base
   k = 10 final from 26 this proves **final from generation 2k + 6 for every k**, which is what the runs show.

Base facts with my code: H(10) on t = 2..80 by my own dynamic programme, a path from w + 3 to lead + 3 (it runs
two or three units behind the leading pulse throughout); the agreement sets hold 64 to 66 of the 72 units tested.
Direct oracle runs of the conclusion: k = 11..18, 20, 25, 30, 40. **Sharper than stated:** the state is final
from generation 2k + 6, not 4k + 8, in every run (k = 1..18, 20, 25, 30, 40).

The other seven release laws are measured, not proved (`python3 laws8.py law --K 40 --orc 5,17`, 140 s: all eight
exact for k = 1..40 with st8, k = 5 and 17 on the oracle).

## 4. What is new

Already established:

- First push and its review: a wall between wire B and wire B′ swallows each pulse from the B side and moves one
  unit towards the sender, 35 times in a row (the L2 receiver, "a unary counter"). Two pulses that stop each other
  leave the three-cell mark, and one later pulse from either side is swallowed by it, leaving five cells (on the
  oracle in review 1). In letters these are `df` and `ddf`: the push's identification is right (coordinates checked:
  (28,2,−25), (29,0,−26), (30,2,−27) are site 3 on and site 1 off in unit 14 and site 3 on in unit 15; and set
  gives `df` on the oracle).
- Second push: the wall as a counter written from one side and erased from the other.
- Sixth push and review 6: holes in the rake train write a B′ stretch that stands for ever, one unit per hole.
  Seventh push: the finite line that keeps it.

So "a pulse is absorbed by a mark or a wall and the store grows by one" is not new, and the one-bit read is that
fact read as an answer.

New here: (a) the stretch as one object `d^k f`, symmetric under the half-turn (checked: `extra8.py sym`), push
7's edge unit = f, absorption at the f end for every k; (b) **the release**: one cell beside the wall sends the
whole count out as k pulses and leaves the wire plain, with exact laws and a proof; (c) the transfer; (d) the cell
as a free-standing object of period 2 with a protocol; (e) the reads of push 7's line and what its two caps do;
(f) the compound movers R⁺, L⁺ of wire B (not in the earlier account).

The release was one step away in review 1: its "36th shot, with the wall beside A" is the count-read operation.
On the first push's receiver, which is `df` followed by two units that are not family units (`extra8.py first`,
st8, the receiver laid in a capped cell), shots 1 to 35 add one each and the 36th turns the wire to the left into
wire C (`b^47`); no train of separate pulses comes out, which is why it read as fire.

## 5. The numbers that rest on lab8

- lab8's validation (`check8.py`) covers the 3 × 3 tube with caps, fire, a ring and soup. The censuses flip cells
  of the 5 × 5 tube and never test the box's `touch` flag. That is harmless: by T2 every such run stays in the
  5 × 5 tube and the hull of the caps, which lies inside lab8's box (y in [−6, 10), x + z in [−6, 14), six units
  beyond each cap).
- **Census** (`python3 laws8.py census --k 3 --orc 2`, 87 s): my classes on the whole state: 526 healed, 134
  released, 10 standing, 8 count + 1, 6 count − 1, 76 other (the push's 72 + 4 "a pulse leaves"). Compared event
  by event with `unzip8.census(3)`: the same class for all 760 but those 4. 12 events (two of each class) on the
  oracle: class and whole state at generation 100 equal. The split is 66 left / 68 right (the push's code prints
  that too); to the left: `b7b7b` 13, blocks `b^5..b^8` 24, `b5f(9f)^j` and `bb5f9f9f` 22, `b7b` 4, `b` 3.
- **Laws, catch**: section 3 and `python3 laws8.py catch` (7 s; k = 1..12, three on the oracle).
- **Movers and absorption** (`python3 extra8.py movers`, st8, two on the oracle): `d6f`, `d6ef`, `cfd6f`, `b5f`,
  `bb5f`, `b5f9f`, `b5f5f9f` are rigid and a store gains 2, 2, 3, 2, 2, 3, 4.
- **Two-cell census of wire B** (`python3 extra8.py twocell`, 13 s): 574 events as the push; 149 heal; **60 end
  as a single pulse** (30 each way), not 46; and one event ends as `b5f9f` going left and `d6f` going right with
  plain wire between. README section 2's "No new mover" for two-cell changes is wrong: R⁺ and an L⁺ train are
  already there (its own output line `move: s11(<) + s12(>)`).
- Re-run with the push's code, counts as in the README: `signals8.py wire` (76: 66 / 6 / 2 / 1 / 1), `wire --bg d`,
  `words8.py --K 3` (3,840: 34 vanish, 3,238 other), the two `--mid dddf` runs (3,264 and 2,918 other),
  `unzip8.py absorb`, `unzip8.py caps`, `cell8.py --search`, `probe8.py scan` (3,600: 2,808 / 404 / 36 / 22 / 18;
  440 kept), `probe8.py ride` (320 / 112 / 8), `probe8.py ringstretch` (312 placements unchanged after one lap
  with both pulses, 8 not standing). Not rebuilt.

## 6. The negatives and their bounds

**"Nothing that travels as a signal starts the read."** `python3 latch8.py --k 3 --pairs --words 3 --out F.json`
(the push's code, from its directory; 202 s here): 7,239 candidates, 48 distinct states.
`python3 latch_check.py F.json --orc 6` (60 s; `out/latch_check.txt`): each of the 48 rebuilt from its recorded
event with st8 and sent the pulse at both distances: the letters of the structure and of the outcome equal the
push's in 96 of 96 runs; six rows on the oracle equal st8 on the whole state. Read one by one:

- 9 of the 48 are not structures: the plain line with the stretch already released (1,299 candidates end there)
  and 8 plain stores or pairs of stores with another count or place. 6 are the eaters `6?`, `6??`. 5 are a
  standing `d?` or `d??` with the stretch gone or kept; the pulse makes `dd?`, `dd??`: another absorbing counter.
  In 6 the pulse turns the wire on the left into wire C. 22 burn.
- None releases the stretch. (One state, a standing `c9f` where the stretch had already been released by the
  candidate event itself, ends as family letters without d: the pulse turns the wire on its left into wire C.)
  Confirmed for k = 3. The k = 2, four-unit-word run (148 states, 20 minutes) was not re-run.
- What was searched, exactly: states reached within 200 generations from one- or two-cell flips or family words
  of at most 3 (4) units **inside the wire's tube**, within 12 units of the wall, period dividing 4; one arriving
  signal, the plain right-going pulse, at two distances; one side. Not searched: any object beside the wire, any
  other arriving signal against a structure (pairs, `6ef`, R⁺), structures of longer period, structures the
  census classes call fronts.
- **The place it did not look holds a trigger.** Push 8 itself found that one cell made live outside the tube,
  (1,4,2), releases the count, and named an object beside the wall as a route. Push 9 (a later commit,
  `research/signals/push9/`; not reviewed here) reports a six-cell still life there. `python3 extra8.py beside` (6 s, oracle, my code,
  only those six cells taken from push 9): capL + `7^(2k+20) d^k f 7^6` + right cap + the six cells stands; ONE
  stator removed 12 units before the wall; the first exact state without d or f carries `b^(2k+2)` (k = 1, 3, 6);
  the run ends as the empty cell with the six cells untouched. So "none among 48 standing structures" is true
  and "nothing that travels starts the read" is false as a general statement. A store counts that block as k + 1
  (section 1).

**A read that keeps the count: not found.** Stands as "not found"; no search is behind it beyond the censuses.
Related fact from section 1: a count read met by a pulse at even distance puts the same count back, D/2 units
away, and nothing comes out.

**A probe on a second wire, re-arming.** Bounds as the push states them (second wire B, parallel, 3,600
placements; pulses of the second wire only). Counts reproduced with the push's code; no independent rebuild, no
oracle run of any placement.

## 7. Forecasts

Brier score recomputed from the table: 0.1012. Scoring checked against the evidence: 1, 2, 3, 7, 10, 12, 16 as
scored. Forecast 9 ("four rigid signals reachable by one- or two-cell flips") is true by one event only (the
two-cell event of section 5); R⁺ and L⁺ are otherwise four-cell words. Forecast 15 ("read by a later signal") is
true of the bit read alone: the count read is a cell changed by hand. Forecast 13 was scored on parallel wires
only.

## 8. What it means

- **A memory in the strict sense: for one bit, yes; for the count, not within this push.** Written by signals: yes
  (two pulses set it, each later pulse adds one). Persists: for ever (exact period 2). Read back by a signal: a
  pulse passes an empty wire and is stopped by a store, so the answer is a pulse on the far side; but reading a
  full store changes it (k to k + 1), "empty" is plain wire and not a state of an object, and in the cell the
  answering pulse is swallowed by the cap. The count comes out only by a cell changed by hand.
- **The machine.** Pulses, stores that absorb from both sides, and passage through plain wire make a row of unary
  counters in which every signal ends by adding one to the first store on its way or in a cap. No event of this
  push turns one arriving signal into another signal, so signals alone cannot loop: a finite set of pulses does
  finitely many additions and stops. The hand-triggered release adds "move the count of one store into the next
  store on its left (or right) and clear it", with the +1 of a receiver that has to exist. With the hand as
  control this is addition and clearing on counters; with no hand it is an accumulator and a coincidence detector.
  Limits found here: counting is exact only for pulses two or more units apart; operations within two units of a
  cap, pairs closer than three units, and a release one unit from another store destroy the cell or lose counts;
  capacity is N − 4.
- **The one missing piece** was a release started by an arriving signal: with it a store is read by a pulse and
  answers with pulses that write the next store. Push 9's still life beside the wall is that piece (one oracle
  run here; its own review is owed). Two things would still be open after it: the release it gives is a block,
  counted as k + 1 and only from the left, with the trigger fixed at one unit of the wire; and nothing known
  routes a pulse off the wire or copies one, so a loop in time on a single line still needs a store to be rebuilt
  at the trigger's place.

## 9. Corrections for the push's README (not applied; its files were not edited)

1. Answers and section 6: the count is exact for pulses two or more units apart; adjacent pulses count in pairs.
2. Section 6, table: set needs u′ − u ≥ 3; u′ − u = 2 destroys the cell; R@u needs 5 ≤ u ≤ N + 2, L@u needs
   6 ≤ u ≤ N + 3; "take one off" holds at two units of each end only; the transfer needs a gap of 2 units.
3. Section 6: N = 7 is the smallest for "two pulses seen at once"; the protocol works at N = 6 (68 cells).
4. Section 5: 66 to the left and 68 to the right; the release is complete from generation 2k + 6.
5. Section 5, the proof: add the check that nothing nears a cap at any generation, the two lines for t = 2, 3,
   and the no-crossing argument for the time bound (which then reads 2k + 6).
6. Section 2: 60 single pulses among the two-cell events, and R⁺ with an L⁺ train occurs there.
7. Section 7 and the summary: say that 9 of the 48 states are the plain line or plain stores, and that the
   search is inside the tube with one kind of arriving signal; the fixed sender answers "the reader has to know
   where the stretch begins".
8. Section 4: the count read of the empty line is safe only at generations ≡ 2 mod 4.

## 10. Not checked

- `latch8.py --k 2 --words 4` (65,991 candidates, 148 states); the fronts of every census ("other"); the right-going
  releases law by law (mirror images, seen in the census only).
- The second-wire scans (`probe8.py`) and re-arming: re-run with the push's code or read, not rebuilt.
- Words census in wire B′; the laws beyond k = 40; the count read on the oracle for k not in 1..20, 25, 30, 40.
- Push 7's other gun and end pairs; push 7 itself (under review in `REVIEW-signals-7.md`).
- Push 9's trigger beyond the one run of section 6; push 8b.
- Caps other than capL and its image; cells with a different left cap.
- `tables8.py` and `laws8.py smallest`, `inside` are st8 only apart from the cases repeated in `proto8.py`
  section G and `check_st8.py`.
