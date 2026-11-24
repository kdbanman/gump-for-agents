# The catalogue's "for every N" laws in Lean (tape files)

Lean arm, 2026-11-24, 11:16–13:15 UTC, 13:16–14:25 UTC, 14:32–15:50 UTC and 16:02–17:10 UTC. Files: `Gump/TapeBase.lean`, `Gump/Tape.lean`, `Gump/TapeSignals.lean`
(+ `TapeSignalsData.lean`), `Gump/Line.lean` (+ `LineData.lean`), `Gump/Clock.lean` (+ `ClockData.lean`),
`Gump/Unzip.lean`, `Gump/UnzipProof.lean`, `Gump/Call.lean` (+ `CallData.lean`), `Gump/CallProof.lean`,
`Gump/CallBox.lean`, `Gump/CallLine.lean`, `Gump/CallUnion.lean` (+ `CallUnionData.lean`), `Gump/CallUnionLocal.lean`,
`Gump/ClockLit.lean` (+ `ClockLitData.lean`), `Gump/ClockLitFirst.lean`, `Gump/ClockLitOdd.lean`, `Gump/LineBeam.lean` (+ `LineBeamData.lean`), `Gump/ClockReader.lean`, `Gump/CallReader.lean` (+ `CallReaderData.lean`), `Gump/LineDivider.lean` (+ `LineDividerData.lean`), `Gump/TapeSuper.lean`, `Gump/TapeMeet.lean`,
`Gump/TapeMeetFront.lean`, `Gump/TapeMeetFronts.lean` (+ `TapeMeetData.lean`);
`AxiomsTape.lean`; scripts `tape_lib.py`, `tape_line.py`, `tape_signals.py`, `tape_clock.py`, `tape_call.py`,
`tape_statements_check.py`, `tape_unzip.py`, `tape_call_front.py`, `tape_callunion.py`, `tape_lit.py`, `tape_beam.py`, `tape_reader.py`, `tape_divider.py`, `tape_meet.py`; rows in `statements_tape.json`. Every result below is in the **kernel tier**: no
`native_decide` anywhere, every base run is `decide +kernel` on `Gump.Bits`' stepper, and every theorem in
`AxiomsTape.lean` rests on at most `propext`, `Classical.choice`, `Quot.sound`. Nothing here is refereed.

## What is proved

| # | law (source) | Lean | status |
|---|---|---|---|
| 1 | the tape: every word over {B, C} moves one unit per 2 generations (§10; REVIEW-signals-2 row 5; REVIEW-signals-9 §3 A) | `Tape.tape_run`, `tape_local_run` | **proved**, whole lattice, every word |
| 2 | a clock of every length: period exactly 4N + 2 for every N ≥ 1 (§11, `prove_clock.py`) | `Clock.clockOf_period` (named), `clock_cycle`, `lit_clock_small`, `X0_lit`; `clock_every_length` (existential, says less) | **proved** for the named cycle, and (third session) **from a single cell for every N**: `ClockLit.lit_clock`, `lit_enters`, `lit_word`; entering exactly at generation N − 2: `lit_enters_at`, `lit_clock_exact` |
| 3 | the gun's line: period exactly 4 from generation 2N, every N ≥ 2 (§21, `prove_line.py`) | `Line.line_orbit`, `line_period_four` | **proved, stronger**: preperiod exactly 2N |
| 4 | nine rigid signals on the rake train (§30–35, `prove_echo.py`, `sig6.py`) | `Tape.Signals.signal_run`, `train_step`, `train_shift` | **proved**, every place, every time |
| 5 | the unzip law (push 8 §5, `prove_unzip8.py`; REVIEW-signals-8 §3) | `Unzip.unzip_law`, `unzip_law_sharp` | **proved**, both the push's bound and the review's sharp one, by a new argument |
| 6 | the call law (REVIEW-signals-9 §3, `proof9.py`) | `Call.call_law : CallLaw` (`call_law_a`, `call_law_b`, `line_rest`) | **proved whole** for every k (second session) |
| – | a stretch d^k f stands (period 2) for every k (push 8 §6, infinite-wire form) | `Unzip.stretch_stands` | proved (a base fact of 5) |
| 7 | the beam: period exactly 4 for every N ≥ 1 (§21, `prove_beam.py`) | `Beam.beam_period` | **proved** (third session) |
| 8 | capL of the clock eats every word and remembers nothing (§15, `prove_reader.py`) | `Clock.reader_run`, `reader_step` | **proved**, every word (third session) |
| 9 | the call line's left cap (call9.json) eats every word (REVIEW-signals-9 §3, left open (ii)) | `Reader.reader9_run`, `reader_run_gen` | **proved**, every word (third session) |
| 10 | the divider: period exactly 8 from generation 2N − 3 for every N ≥ 8 (§21b, `prove_divider.py`) | `Divider.divider_period` | **proved** (third session) |
| 11 | the meetings of §31: one per pair; U–K0 vanish; U–H, E–H, E–K0 fronts for ever; every distance | `Signals.pair_run`, `meet_U_K0`, `meet_UH`, `meet_EH`, `meet_EK`; `run_or_far`, `superpose_units`, `rigid_front` | **proved** (fourth session); the table's E–H row corrected |

### Headline statements, verbatim

```lean
theorem tape_run (w : Int → Letter) (n : Nat) : run (tape w) (2 * n) = tape (fun u => w (u + n))
theorem line_orbit (N : Nat) (hN : 2 ≤ N) (s p : Nat) (hp : 0 < p) :
    run (lineC N) (s + p) = run (lineC N) s ↔ 2 * N ≤ s ∧ p % 4 = 0
theorem clock_every_length (N : Nat) (hN : 1 ≤ N) :
    ∃ c : Config, run c (4 * N + 2) = c ∧ (∀ k, 0 < k → k < 4 * N + 2 → run c k ≠ c) ∧
      ∀ q, c q = true → -4 ≤ unitOf q ∧ unitOf q ≤ N + 3 ∧ -32 ≤ q.y ∧ q.y < 32 ∧
        -64 ≤ q.x + q.z ∧ q.x + q.z < 64
theorem signal_run (K : Kind) (u : Int) (hu : u % 2 = K.par % 2) (n : Nat) :
    run (xorC (train 1) (lcfg (sig K u))) (2 * n) = xorC (train (1 + 2 * n)) (lcfg (sig K (u + K.dir * n)))
theorem unzip_law_sharp : UnzipLawSharp
theorem call_law_b (k : Nat) (hk : 1 ≤ k) (n : Nat) (hn : k + 17 ≤ n) :
    V k (2 * n) = tape (pulses k (cross + 3 - ((n : Int) - 14)))
theorem call_law : CallLaw
theorem clockOf_period (N : Nat) (hN : 1 ≤ N) :
    run (clockOf N) (4 * N + 2) = clockOf N ∧ (∀ k, 0 < k → k < 4 * N + 2 → run (clockOf N) k ≠ clockOf N) ∧ …
theorem reader_run (w : Int → Letter) : ∀ n : Nat, run (readerC w) (2 * n) = readerC (fun u => w (u + n))
theorem divider_period (N : Nat) (hN : 8 ≤ N) :
    run (divC N) (2 * N - 3 + 8) = run (divC N) (2 * N - 3) ∧
    (∀ k, 0 < k → k < 8 → run (divC N) (2 * N - 3 + k) ≠ run (divC N) (2 * N - 3)) ∧
    run (divC N) (2 * N - 4 + 8) ≠ run (divC N) (2 * N - 4)
theorem beam_period (N : Nat) (hN : 1 ≤ N) :
    run (beam N) 4 = beam N ∧ ∀ k, 0 < k → k < 4 → run (beam N) k ≠ beam N
theorem lit_enters_at (N : Nat) (h6 : 6 ≤ N) :
    (∃ s, run (lcfg (litList N)) (N - 2) = run (clockOf N) s) ∧
    ∀ g, g < N - 2 → ∀ k, run (lcfg (litList N)) g ≠ run (clockOf N) k
theorem lit_word (N : Nat) (h6 : 6 ≤ N) : ∀ m, m ≤ mmax N → run (lcfg (litList N)) (2 * m) = ucfg (FL N m)
theorem lit_enters (N : Nat) (h6 : 6 ≤ N) :
    run (lcfg (litList N)) (2 * mmax N) = run (clockOf N) (2 * (N - 6) + 3)
theorem lit_clock (N : Nat) (hN : 1 ≤ N) (g : Nat) (hg : litEntry N ≤ g) :
    (∃ s, run (lcfg (litList N)) g = run (clockOf N) s) ∧
    run (run (lcfg (litList N)) g) (4 * N + 2) = run (lcfg (litList N)) g ∧
    ∀ k, 0 < k → k < 4 * N + 2 → run (run (lcfg (litList N)) g) k ≠ run (lcfg (litList N)) g
def UnzipLawSharp : Prop :=
  ∀ k : Nat, 1 ≤ k → (∀ n : Nat, k + 3 ≤ n → run (countRead k) (2 * n) = tape (pulses k (2 - n))) ∧
    run (countRead k) (2 * (k + 2)) ≠ tape (pulses k (2 - (k + 2)))
```

Definitions to read them by: a unit of the wire is u = ⌊x/2⌋ (`unitOf`), the move along the wire is
τ = (2, 0, −2) (`shiftPt`, `shiftC`); `tape w` holds on unit u the five cells of wire `w u` (B: (0,1,2), (0,1,4),
(1,0,0), (1,0,2), (1,0,4); C: (0,2,3) in place of (1,0,4)); `lineC N` is capA + N units of wire C + the gun moved N
units, in the coordinates of `objects/line-C.json`; `hcfg w` is a word of push 8's hex letters (stators (0,1,2),
(0,1,4) and the sites (1,0,0), (1,0,2), (1,0,4), (0,2,3) of the bits); `store k` is wire B with d^k f on units
0 .. k; `countRead k` is `store k` without the stator (0,1,2) of unit −1; `pulses k lead` puts C on units
lead, lead + 2, …, lead + 2k − 2 and B elsewhere; `train t` is the rake train of the line at phase t (from
rake5/rakef of line-C.json, computed by the oracle in `tape_signals.py`); `sig K u` the cells of signal K
(`research/audit/signals6/sig6.py`'s table) moved u units. All configurations are of the whole lattice: the
line and the clock have finite support; the tape, the train and the store wire are infinite along the wire.

## How each is proved, and what differs from the source

**Tools** (`TapeBase.lean`). `run_eq_of_units`: n generations of a point read only the n units on either side
(from `light_cone`). `run_shiftC`: τ commutes with `run` (from `run_act`). `glue_run`: two orbits that agree on
units m, m + 1, one obeying the rule on units ≤ m and the other on units > m, glue to an orbit. `orbit_classify`:
X(μ+4) = X(μ), X(μ+2) ≠ X(μ), X(μ+3) ≠ X(μ−1) give "X(s+p) = X(s) iff s ≥ μ and 4 ∣ p". Kernel certificates on
ranges of units: `unitMask`, `eqOn_spec`, `neqOn_spec`, `agree` (two orbits agree on a mask for n generations),
`coreRun`. `TapeSignals.lean`: `ucfg` (a configuration given unit by unit), `piece`, and `pieceCheck_spec`: a
finite piece (xor a finite list), moved by an even frame into the bit box, stepped k times by the kernel, gives the
infinite configuration's k-th generation on a range of units. `Unzip.lean`: `hex_local` (one double step of a hex
word, read off its 5-unit window), `glue_run_moving` (a seam that moves one unit per generation; proved, used by
no proof here). `Clock.lean`: `surg_step` (j + 1 charts glued unit by unit).

1. **Tape.** As the source: the claim is local (two generations read five units), the 32 windows of five letters
   are each run by the kernel (`window_ok`, <3 s), translation carries a window to any unit. The source used one
   ring of 40 units holding all 32 windows; here each window is its own 5-unit run in empty space. Stronger than
   stated: `tape_local_run` is about any configuration that is a tape word on a stretch of units.
2. **Clock.** The source's surgery (README §11), formalised as `surg_step`: unit 3 + i of the clock of 6 + j units
   shows the base's unit 3 at the base's time `chart j i t`, moved i units. The chart arithmetic (A: neighbouring
   charts differ by ±2 generations in a range where the base checks the strip; B: a chart advances by one or loops
   back by three at ta = 11 or tb = 24) is proved for **every** j, i, t by `omega` (`chartA`, `chartB`: the
   source enumerated j ≤ 40). Base N0 = 6, cut at unit 3, tR = 5, ta = 11, tb = 24, period 26 (the source used
   N0 = 8 or 12; `tape_clock.py` found that 6 works). B0–B5 and "every state lies in units −4 .. 9" are one kernel
   Boolean (`baseCheck_ok`). N = 1 .. 5: the lit clock from generation max(N−2, 0) has exact period 4N + 2
   (`lit_clock_small`, direct). **Says what the source says and no more**: for N ≥ 6 the oscillator is the surgery's
   cycle, not the lit clock; that one cell lights it into this cycle is not proved (measured to N = 400).
3. **Line.** The source's induction S(N, m) → S(N+1, m+1) (`S_succ`), with the base S(4, 1) (the source: S(8, 3);
   4 is the smallest base that works, found by `tape_line.py`) and N = 2, 3 direct. Stronger than the source: the
   statement carries witnesses of "not period 2" (right of the seam) and of "not periodic from 2N − 1" (left of
   it), so `line_orbit` gives the preperiod exactly 2N for every N; the source measured the 2N − 1 clause for five N.
4. **Signals.** As the source: train(1) ⊕ the signal on an 11-unit piece is stepped twice by the kernel and equals
   train(3) ⊕ the moved signal on 7 units; away from it the state is the train, itself proved an orbit of the
   whole lattice (`train_step`, 8 one-step checks) that moves one unit per two generations (`train_shift`).
5. **Unzip.** *Not the source's argument.* The kymograph (oracle, `tape_statements_check.py` and the formula check
   in this session) shows that from generation 2 on the store wire is at every even generation a hex word: plain
   wire B with pulses `b7b7…b` behind a front `f 9` that moves one unit towards +v per double step through the
   standing stretch. `W k n` (UnzipProof.lean) is that word; it was checked against the oracle for k = 1 .. 10 at
   every even generation. The proof is an induction on time: a double step of `W k n` is `W k (n+1)` because on
   the units left of the front the word is a tape word (the 32 tape windows, moved), on the units right of it the
   stretch stands (78 canonical stretch windows, `stretch_stands`), and on six units at the front one piece, moved
   to the front, is stepped by the kernel; its content depends on n and k only through min(n, 5) and min(k − n, 3),
   so 16 generic checks + 8 at the start + 8 at the edge (`zonesOK_ok`) cover every k. From n = k + 3 on the word
   is the tape of the k pulses (`tape_run`). This proves the review's sharp form (final from 2k + 6, not at 2k + 4)
   and hence the push's (from 4k + 8). The source's seam path, its gaps closed by REVIEW-signals-8, is not needed;
   `glue_run_moving` (its gluing step) is proved anyway.

**Oracle ties** (ground truth for every base run; each kernel run is also an oracle run): `tape_line.py` (S(4,1),
N = 2, 3, and the glued orbit equal to the oracle's for N = 5 .. 12), `tape_signals.py` (the train's phases, the
nine signals for 24 generations, the signal table equal to sig6.py's), `tape_clock.py` (B0–B5, the support, the
lit clocks N ≤ 5, the surgery formula equal to the oracle orbit for j = 1 .. 4 over a whole period, earlier run
also j = 5, and the lit clock of 6 + j units falling into it), `tape_statements_check.py` (the Lean statements of
the unzip law, the sharp law, the stretch and the call law transcribed and checked on the oracle for k = 1 .. 3,
resp. k = 1: ALL PASS). The scripts regenerate the four `*Data.lean` files exactly (checked by diff for the clock).

## The call law: proved whole

**(b), proved** (`CallProof.lean`, `call_law_b`): with the crossing moved to unit 0, V_k at generation 28 + 2n is,
for n ≥ 2, the hex word `VW k n`: pulses behind a front `f b 9` (one unit wider than the count read's `f 9`) moving
one unit per double step through the stretch (`tape_call_front.py`: equal to the oracle for k = 1 .. 8 at every
even generation to 2k + 40). Steps as for the unzip law: 20 generic zone checks, 4 + 5 + 5 at the edge, and the start
(generation 28: the store, one generation, e1 made live, three more) as one forced run on 15 units for each
min(k, 7) (`forcedCheck_spec`); from n = k + 3 on the tape theorem. So V_k is the k pulses from 2k + 34 on, for
every k. The review's seam path (part E) and its tape continuation (part A) are not needed for (b).

`Call.CallLaw` is the statement of REVIEW-signals-9 §3, (a) and (b), on the whole lattice:

```lean
def CallLaw : Prop :=
  ∀ k : Nat, 1 ≤ k →
    (∀ t : Nat, run (callStart k) t = (fun p => V k t p || Lf t p) ∧ ∀ p, ¬ (V k t p = true ∧ Lf t p = true)) ∧
    (∀ n : Nat, k + 17 ≤ n → V k (2 * n) = tape (pulses k (cross + 3 - ((n : Int) - 14))))
```

with `callStart k` = store wire (d^k f on units c+1 .. c+k+1, c = 35) ∪ line (162 cells of call9.json run 0) ∪
the two CALL cells; `Lf t` the line with the CALL alone; `V k t` the store wire alone with e1 = (1,2,0) of unit c
made live at generation 29. `tape_statements_check.py` checks the transcription on the oracle for k = 1 (t ≤ 42).
**(a), proved** (second session, 13:16–14:20 UTC; `CallBox.lean`, `CallLine.lean`, `CallUnion.lean`,
`CallUnionLocal.lean`; `call_law_a`, and with (b) `call_law : CallLaw`). The proof is the review's, every step a
theorem:
- *A second box.* `Gump/CallBox.lean` is `Gump.Bits`' stepper on the box 128 × 128 × 16 (the same 2^18 bits, shaped
  for the line, which spans 65 doubled units in x and in y and five in z): the geometry (index, masks, neighbour
  shifts) is new, the counter and the rule formula are reused; `Gump.Call.Box.bstep_spec` proves it equal to
  `Gump.step` in the core. `Gump.Bits` and its dependents are unchanged.
- *The free line* (`CallLine.lean`): the kernel runs the line with the CALL 45 generations: `line_rest` (it is the line
  at rest at 42 and 44: the statement `LineRest`), `Lf_period` (period 2 from 42), `Lf_snap` (its state on NZ at every
  generation, from 44 snapshots that `tape_callunion.py` takes from the oracle and the kernel re-checks).
- *Supports and disjointness* (`CallUnion.lean`): V_k stays in the tube H_V = {1 ≤ x+y+z ≤ 5, −1 ≤ x−y+z ≤ 5}
  (`V_HV`, by `confinement` on four diagonals: the store and e1 lie in it) and the free line in its diagonal hull H_L
  (`Lf_HL`, by `hull`), where x − y + z ≤ −5; so they never share a point (`V_Lf_disjoint`).
- *The union law off Z*: at a cell whose closed neighbourhood misses one part the union steps to the union (`step_or`);
  the cells whose neighbourhood meets both H_V and H_L are the 44 cells of Z (`zone_cover`: an `omega` box, then one
  kernel enumeration of it).
- *At Z* (`CallUnionLocal.lean`): `LC_spec` turns one Boolean (in `Gump.Bits`' box) into the union law at Z, given
  V_k's state on NZ (from its state on units 32 .. 39) and the line's snapshot. The families (`checkStore_ok`,
  `checkStart_ok`, `checkVW_ok`, `checkTape_ok`, 54 s together): t ≤ 27, the standing store, k through min(k, 4);
  t = 28 .. 31, the start from a 16-unit window (at 28 the union law fails at exactly one cell, e1, which is V_k's
  forcing); t = 32 .. 43, the words `VW k n`, k through min(k, 8); t ≥ 44, every word of {7, b} on the eight units
  (256 words, the review's lemma T), even and odd phase, the line at rest. Odd generations are one bit-step of the
  even window, cleared at NZ's points outside the tube.
- `call_law_a` is then an induction on t (`local_union` at Z, `step_or` elsewhere).

So **the call law stands whole for every k ≥ 1** (`call_law : CallLaw`). Not covered, as in the review's "what is
left": the finite cell (the left cap taking a train of any length), other seed places, and "at no earlier
generation".

## The clock from a single cell (third session)

`Gump/ClockLit.lean`. The lit clock of N units is `litList N`: capL, N units of wire C, capR moved N units, and the
cell (1,0,4) of unit N / 2 (`objects/clock-C.json`). Its transient is a word of push 8's hex letters between the two
caps (`FL N m`, given unit by unit, caps as `capLU`/`capRU` from `tape_lit.py`): **at generation 2m the rake f is at
unit N/2 + m, units of wire B (the pulses p<) at N/2 − m, N/2 − m + 2, …, N/2 + m − 2, wire C elsewhere**, for
m ≤ mmax N = ⌈N/2⌉ − 1, when the rake reaches unit N − 1 (`lit_word`; the formula checked on the oracle for
N = 6 .. 30 by `tape_lit.py`). So the one cell is a rake that runs right at the speed of a pulse, shedding one pulse per double step, while the
pulses it shed run left at the same speed: the train's head stays two units behind the rake and its tail moves left
one unit per double step, so the train spreads at both ends.

- One double step (`lit_step`): for N ≥ 16 by the method of `UnzipProof`: tape windows on the wire, and three zone
  families normalised and checked by the kernel at once (`zonesLit_ok`: the left cap with the train's tail at
  a = min(N/2 − m, 9), 9 checks; the right cap with the rake at distance b = min(d, 9), 9 checks; the rake itself
  with c = min(m, 2) pulses behind it, 3 checks); for 6 ≤ N ≤ 15 the whole clock in one box per (N, m)
  (`smallOK_ok`, 45 checks, the box moved by 2N in z because the wire runs along (2, 0, −2)). `step_zoneU` is
  `UnzipProof.step_zone` for words given unit by unit; `run2_empty` is the light cone on empty units.
- The match (`FL_entry`): at time 2j + 8 every chart of the surgery shows base time 8 or 10
  (`chart_entry`: chart j i (2j + 8) = 8 + 2((j − i) mod 2), by omega), and three kernel facts about the base
  (`baseLitCheck_ok`): Xb 8 and Xb 10 on the units ≤ 3 are capL then wire B on the odd (resp. even) units, and Xb 8 on
  the units ≥ 3 is B, C, f, capR. So the last word `FL N (mmax N)` is `Y_{N−6}` at time 2(N − 6) + 8, which is
  `run (clockOf N) (2(N − 6) + 3)` by `clockY_run` (`lit_enters`).
- `lit_clock`: from `litEntry N` on, every state of the lit clock is on the cycle of `clockOf N` and has exact
  period 4N + 2 (`exact_period_run`: the states of an exact-period orbit have that exact period); N ≤ 5 is
  `clockOf`'s definition.
- **At no earlier generation** (`Gump/ClockLitFirst.lean`, `Gump/ClockLitOdd.lean`, `lit_first`): for every N ≥ 6 no state before generation
  N − 2 is any state of the cycle. It is enough to show the state at N − 3 is not (a later state of an orbit that met
  the cycle is on it). Every state of the cycle shows on its units ≤ 3 a state of the base (chart 0), and on its units
  ≥ N − 3, moved back N − 6 units, the units ≥ 3 of a state of the base (chart j) (`cycle_left`, `cycle_right`). Even
  N: the lit clock's units ≤ 2 at N − 3 are one generation of capL + C C B C, the same for every even N, and differ
  from all 26 base states (`firstCheck_ok`, one witness cell each, from `tape_lit.py`). Odd N: that left end equals
  the base's at times 4, 8, 12, 16 (Lean's `Xb` convention; 11, 15, 19, 23 counted from X0, `Xb_nat`), so the witness is the right end instead: at N − 3 (an even generation for odd
  N, so a word) the units ≥ N − 3 are C, f, C, capR, the right end of no base state (`firstCheckR_ok`).
  `lit_enters_exact`: for even N the entry is exactly N − 2.
- **Odd N at N − 2** (`Gump/ClockLitOdd.lean`, `lit_odd_entry`): generation N − 2 is odd for odd N, one generation
  after the word `FL N (mmax N − 1)`. At surgery time 2j + 7 chart i shows base time 9 or 11 by the parity of j − i and
  chart j shows 7 (`chart_odd`, omega), and one generation of the word matches the base there on three local pieces
  (`oddCheck_ok`): the left end (capL C B C B C → Xb 9 on the units ≤ 3), a three-unit window of the wire in each
  parity (C B C → Xb 9, B C B → Xb 11 on unit 3), the right end (B C f C capR → Xb 7 on the units ≥ 3). So the state
  at N − 2 is `clockOf N` at generation 2(N − 6) + 2. `lit_enters_at`: for every N ≥ 6 the lit clock is on the cycle
  at generation N − 2 and at no earlier one; `lit_clock_exact`: from then on, exact period 4N + 2.

## The beam (third session)

`Gump/LineBeam.lean`: the mirror-image gun, N units of rake train and the SAT absorber (`objects/beam-5f.json`),
given unit by unit (`beamU`; `tape_beam.py` checks it reassembles to `prove_beam.py`'s Object(N) for N = 1 .. 30).
`beam_period`: for every N ≥ 1 it returns after 4 generations and after no fewer. The proof is the source's
induction N → N + 2: `S N` is period 4, not period 2, and the seam (on the units 4, 5 the orbit is its own move by
two units at every generation); the orbit on the units ≤ 4 glued (`glue_run`) to its move by two units on the units
≥ 5 starts at the beam of N + 2 units (`glue_beam`, unit-by-unit list equality), so it is that beam's orbit
(`S_step`). Bases S 8, S 9 and N = 1 .. 9 by one kernel check (`baseOK_ok`, the box moved by (8, 8, 24)).
Unlike the line there is no delay: the stream crossing the seam is the train itself, already periodic.

## The reader (third session)

`Gump/ClockReader.lean`: `readerC w` is capL on the units < 0 and the tape of any word w on the units ≥ 0.
`reader_step`: two generations later it is capL and the word moved one unit, cell for cell; `reader_run`: at
generation 2n, capL and w moved n units. So the cap swallows every word letter by letter, sends nothing back into the
tape and keeps no trace (the source's (i) and (ii) at once: the state is never anything but capL + the pure word).
The proof is local, like the transient's: tape windows on the units ≥ 2, empty space on the units ≤ −7, and on the
units −6 .. 1 one kernel check for each of the 16 words on the units 0 .. 3 (`readerOK_ok`), the source's closed set
of 16 cap states.

The same proof, written once for any cap on the units −4 .. −1 that passes the 16 zone checks (`Gump/CallReader.lean`,
`reader_run_gen`), covers the left cap of push 9's call line (`call9.json` `capL`, 18 cells, a different cap from the
clock's): `reader9_run`, in call9's coordinates (cap on the units 0 .. 3, the store wire from unit 4). The second
review of push 9 had left open whether section 15's theorem covers this cap (its "what is left" (ii)); it does not
literally (another cap), and the law holds for it all the same. What this does not give: the finite cell during a
call (the call line crosses the cell; the cap is reached by the train only once the wire in front of it is plain tape).

## The catalogue's next laws: how they were ranked (third session)

Read for laws stated for every size or every word and not yet in Lean: `research/signals/README.md` and the reviews in
`research/audit/REVIEW-signals*.md`. Ranked by what they say and how much of the catalogue rests on them:

1. **The clock from a single cell** (the brief's first item; §11 lists it as "not proved"; the owner's journal).
   Done: `lit_enters_at`, `lit_clock_exact`.
2. **capL eats every word** (§15, `prove_reader.py`): the only remaining law quantified over all words, the tape's
   −v end as a perfect sink; and the second review of push 9 left open whether it covers the call line's cap.
   Done: `reader_run`, and `reader9_run` for the call line's (different) cap.
3. **The beam** (§21, `prove_beam.py`): emitter, stream and receiver as one standing object at any distance, the
   catalogue's L3 answer as a theorem for every N. Done: `beam_period` (taken first in time, being the cheapest:
   the line's gluing with no delay).
4. **The divider** (§21b, `prove_divider.py`: period exactly 8 from generation 2N − 3 for every N ≥ 8): the first
   emitter of a non-constant word. Done: `divider_period` (`Gump/LineDivider.lean`), `Line.lean`'s induction with the
   oscillator in the right chart: `S N m` has period 8 from 2N − 3, "not period 4" at every later generation (seen
   right of the seam, so it moves one unit per step), "not periodic from 2N − 4" (seen left of it), the window and
   the rest; base S 14 3 (37 generations in the box) and N = 8 .. 13 directly. A return after k < 8 would give one
   after 4, since k·a ≡ 4 (mod 8) for some a (`S_facts`).
5. **The meetings** (§31; REVIEW-signals-6 §3): exactly one meeting per ordered pair of opposite kinds (a
   translation argument on the infinite train), and the four outcomes for ever (U–K0 both vanish; E–K0 a puncher;
   E–H, U–H wire B between two rigid edges, `glue6.py`). Not done: the reduction needs a superposition lemma for
   two far-apart signals (local, from `signal_run`), and the outcome runs at offset 19 for 20 generations span more
   than the 32 units of the 64-box once the light cone is added, so they need the 128-box of `CallBox` or a moving
   window.
6. Single-instance results (the collision gate and the rake against a pulse of §10, the register of §9, the counter
   of §17, the stream's one-cell hole of §21) are oracle runs of one object, not laws for every size: nothing to
   lift beyond re-running them.

No law attempted failed as the catalogue states it. One detail found on the way: for odd N the lit clock's left end at
generation N − 3 is that of the base at times 4, 8, 12, 16 in `Xb`'s convention (11, 15, 19, 23 counted from X0), so "not yet on the cycle" there is seen only at the right
end (`lit_first_odd`).

## The meetings of §31 (fourth session)

- **Superposition** (`Gump/TapeSuper.lean`): `run_or_far`: configurations whose live cells are more than 4n apart
  (max norm) run independently for n generations; `superpose_units`: along the wire, on any background X, a
  modification below unit a and one above unit b run as their own runs glued at any seam a + n − 1 ≤ m ≤ b − n.
  Both from the light cone alone.
- **One meeting per pair** (`Gump/TapeMeet.lean`, `pair_run`): `pair A B a b` is train(1) with the up-signal A at
  unit a and the down-signal B at unit b. While b − a ≥ top(A) + 5 a double step is each signal's own double step
  (`pair_step`, by `superpose_units` and `signal_step`), i.e. the pair at distance b − a − 2 moved one unit; so from
  distance d + 2n the meeting is, after 2n generations, the one from distance d moved n units. Base distances: 3
  (U–K0), 4 (U–H, E–K0), 5 (E–H), the smallest of each parity the reduction reaches.
- **U meets K0** (`meet_U_K0`): from every distance 3 + 2n, exactly the plain train from generation 2n + 4 (one
  kernel run of 4 generations).
- **The fronts** (`Gump/TapeMeetFront.lean`, `Gump/TapeMeetFronts.lean`, generated by `tape_meet.py --fronts`):
  `rigid_front` is the chart argument of §21 as a theorem: if at some generation g the state four generations on is
  `front m` of it (units ≤ m moved two units down, units > m two up) and the units m − 2 .. m + 3 hold, at g .. g + 3,
  a medium unchanged by moves of two units and of period 4 in time, then that holds at every later generation (the
  two moves agree at the seam because the medium does not see them; `glue_step` does the rest). The kernel supplies
  the chain from the meeting to g + 4 (`chain*_ok`: 10 to 15 steps of 1 or 2 generations, each a box check) and
  the facts at g (`facts*_ok`). `meet_UH` (distance 4 + 2n, from 2n + 12, seam 4 + n, wire B), `meet_EH` (5 + 2n,
  from 2n + 22, seam 1 + n, wire B), `meet_EK` (4 + 2n, from 2n + 12, seam 1 + n, the holed train `medEK`); the
  states at 2n + g .. 2n + g + 4 are `state*`. So each meeting's configuration is known exactly at every later
  generation: the kernel's state at g + r moved, below the seam, down and, above it, up.
- **A correction to the table**: "U meets H: the same: wire B between the same two edges" holds for the lower edge
  (the lowest H, then two units of plain train, then wire B, in both) but not for the upper one: E–H's upper edge
  carries for ever a three-unit inclusion (`X.X`: two altered units around one of plain train) just below its four
  topmost units of wire B, rigid with the edge, which U–H's upper edge has not (`tape_meet.py` prints both pictures,
  e.g. at generation 26 of E–H `......h..oooooooooooX.Xoooo......` against U–H at 16 `.........h..oooooooooo...`).
  The section's remark that E–H's edge is "wider" at generation 56 is this inclusion. The rest of the table (E–H and
  U–H wire B, E–K0 the holed train behind a puncher, U–K0 vanish) holds as stated, now for every distance and for
  ever.
- Not covered: the same-direction pairs of §31, words of several holes against E, and the review's K3 (E–K3 gives
  the puncher, U–K3 one H; oracle only).

## Not checked, and caveats

- The objects: the Lean cell lists are written by the scripts from the JSON files (`line-C.json`, `clock-C.json`,
  `cell8.json`, `call9.json`), and the scripts assert the unit alphabet against `Gump/Tape.lean`; I read the Lean
  definitions of `countRead`, `pulses`, `V`, `e1`, `storeAt` against the sources myself; nobody else has.
- `clock_every_length` is an existential and says less than its row did: referee ref-tape (D1) found that the lit
  clocks of 1 and 2 units side by side satisfy it for N = 7. `clockOf_period` names the object: the lit clock at
  generation max(N − 2, 0) for N ≤ 5, the surgery's cycle `clockY (N − 6)` for N ≥ 6. `X0_lit` proves the base X0 is
  the lit clock of six units at generation 41, so `clockOf 6` is the lit clock's state at 53 (`clockY_zero_lit`).
- The lit clock from one cell (third session, `Gump/ClockLit*.lean`): proved for every N, entering the cycle exactly
  at generation N − 2 for every N ≥ 6 (`lit_enters_at`); for N ≤ 5 from max(N − 2, 0) (`lit_clock_small`, minimality
  not claimed there).
- `line_orbit` is about line-C exactly as in the JSON (capA and gun of that file), not about other caps or guns.
- Nine signals: that these are all the rigid signals of the train is not claimed.
- `glue_run_moving` and `Call.pulses_at` are proved but not used by any headline proof.
- Referee ref-tape (`research/blast/ref-tape/REVIEW.md`) read the modules at `6be19d4`: no theorem broken, objects
  equal to the catalogue's; its D1 and D3 are repaired (rows, the Unzip header); D2 (`STATEMENTS.md`) is the PI's.
  The call law's part (a) and the second box are after that review and unrefereed.
- Timing: `sh check.sh` passes in about 10 s with everything built. From scratch (a copy of the workspace with an empty
  `.lake`, all modules of every arm): 291 s at 13:15 (load about 7 on 4 cores), and **852 s at 14:15 with the call
  law's modules added, at load 12 to 14 on 4 cores**, so over the ten-minute target on a machine three times
  oversubscribed. Cold times of the tape files in that run: Clock 314 s (mostly `omega` on the charts), UnzipProof
  137 s, CallProof 131 s, Unzip 107 s, CallUnionLocal 104 s (the 752 local checks), TapeSignals 80 s, CallBox 52 s,
  CallLine 51 s, Tape 44 s, the rest under 35 s. The cheapest cut, if needed: split `chartA`'s case analysis by
  period in Clock.lean.

## Bearing on the owner's journal

The journal's 10:30 entry of 2026-11-15 ("a clock (a wire between two caps, period 4N + 2 for N units of wire)") and
its correction (the clock stands, its proof rebuilt by a reviewer): the clock of every length is now checked by
Lean's kernel, and since the third session as the journal has it, from a single cell: one added cell lights the
clock of N units, for every N, into an oscillator of exact period 4N + 2 (`lit_clock`), and for N ≥ 6 it reaches
the cycle exactly at generation N − 2 (`lit_enters_at`), as measured to N = 400. The transient is itself a
small picture: the cell is a rake that runs to the right cap shedding pulses that run left, the train widening at
both ends; when
the rake reaches the cap the clock is on its cycle. Also checked by the kernel: the tape that the signals rest on, the gun's line, the train's nine signals, push 8's
count read ("the count leaves as a train of pulses") for every k, and push 9's call, whole. The unzip proof found something small and
pretty: the count read is a front of fixed shape, `f 9`, sweeping through the stretch at the speed of a pulse while
the pulses it sheds run the other way, so the whole release for every k is three local pictures.
