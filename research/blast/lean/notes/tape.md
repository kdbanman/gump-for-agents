# The catalogue's "for every N" laws in Lean (tape files)

Lean arm, 2026-11-24, 11:16–13:15 UTC and 13:16–14:25 UTC. Files: `Gump/TapeBase.lean`, `Gump/Tape.lean`, `Gump/TapeSignals.lean`
(+ `TapeSignalsData.lean`), `Gump/Line.lean` (+ `LineData.lean`), `Gump/Clock.lean` (+ `ClockData.lean`),
`Gump/Unzip.lean`, `Gump/UnzipProof.lean`, `Gump/Call.lean` (+ `CallData.lean`), `Gump/CallProof.lean`,
`Gump/CallBox.lean`, `Gump/CallLine.lean`, `Gump/CallUnion.lean` (+ `CallUnionData.lean`), `Gump/CallUnionLocal.lean`;
`AxiomsTape.lean`; scripts `tape_lib.py`, `tape_line.py`, `tape_signals.py`, `tape_clock.py`, `tape_call.py`,
`tape_statements_check.py`, `tape_unzip.py`, `tape_call_front.py`, `tape_callunion.py`; rows in `statements_tape.json`. Every result below is in the **kernel tier**: no
`native_decide` anywhere, every base run is `decide +kernel` on `Gump.Bits`' stepper, and every theorem in
`AxiomsTape.lean` rests on at most `propext`, `Classical.choice`, `Quot.sound`. Nothing here is refereed.

## What is proved

| # | law (source) | Lean | status |
|---|---|---|---|
| 1 | the tape: every word over {B, C} moves one unit per 2 generations (§10; REVIEW-signals-2 row 5; REVIEW-signals-9 §3 A) | `Tape.tape_run`, `tape_local_run` | **proved**, whole lattice, every word |
| 2 | a clock of every length: period exactly 4N + 2 for every N ≥ 1 (§11, `prove_clock.py`) | `Clock.clockOf_period` (named), `clock_cycle`, `lit_clock_small`, `X0_lit`; `clock_every_length` (existential, says less) | **proved** for the named cycle; that one cell lights the lit clock into it is proved for N ≤ 6 only |
| 3 | the gun's line: period exactly 4 from generation 2N, every N ≥ 2 (§21, `prove_line.py`) | `Line.line_orbit`, `line_period_four` | **proved, stronger**: preperiod exactly 2N |
| 4 | nine rigid signals on the rake train (§30–35, `prove_echo.py`, `sig6.py`) | `Tape.Signals.signal_run`, `train_step`, `train_shift` | **proved**, every place, every time |
| 5 | the unzip law (push 8 §5, `prove_unzip8.py`; REVIEW-signals-8 §3) | `Unzip.unzip_law`, `unzip_law_sharp` | **proved**, both the push's bound and the review's sharp one, by a new argument |
| 6 | the call law (REVIEW-signals-9 §3, `proof9.py`) | `Call.call_law : CallLaw` (`call_law_a`, `call_law_b`, `line_rest`) | **proved whole** for every k (second session) |
| – | a stretch d^k f stands (period 2) for every k (push 8 §6, infinite-wire form) | `Unzip.stretch_stands` | proved (a base fact of 5) |

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

## Not checked, and caveats

- The objects: the Lean cell lists are written by the scripts from the JSON files (`line-C.json`, `clock-C.json`,
  `cell8.json`, `call9.json`), and the scripts assert the unit alphabet against `Gump/Tape.lean`; I read the Lean
  definitions of `countRead`, `pulses`, `V`, `e1`, `storeAt` against the sources myself; nobody else has.
- `clock_every_length` is an existential and says less than its row did: referee ref-tape (D1) found that the lit
  clocks of 1 and 2 units side by side satisfy it for N = 7. `clockOf_period` names the object: the lit clock at
  generation max(N − 2, 0) for N ≤ 5, the surgery's cycle `clockY (N − 6)` for N ≥ 6. `X0_lit` proves the base X0 is
  the lit clock of six units at generation 41, so `clockOf 6` is the lit clock's state at 53 (`clockY_zero_lit`).
- **The PI's second item, not done**: that one cell lights the clock of N ≥ 7 units into the surgery's cycle. Where
  it stops: a proof needs (1) the lit clock's transient for every N as a word family (a rake `f` running from unit
  N/2 towards capR, its train of B units behind it reaching capL near generation N; the method of UnzipProof applies,
  with zones at both caps), and (2) the identification of the state at generation N − 2 with `clockY (N − 6)` at
  some time, which means reading the base's unit 3 at every chart time as a letter and matching the chart formula.
  Neither is written. Measured: the lit clock enters its cycle at max(N − 2, 0) (to N = 400, second review), and the
  referee found `clockY j` to be one state of the lit clock's cycle for j ≤ 6.
- `line_orbit` is about line-C exactly as in the JSON (capA and gun of that file), not about other caps or guns.
- Nine signals: that these are all the rigid signals of the train is not claimed.
- `glue_run_moving` and `Call.pulses_at` are proved but not used by any headline proof.
- Referee ref-tape (`research/blast/ref-tape/REVIEW.md`) read the modules at `6be19d4`: no theorem broken, objects
  equal to the catalogue's; its D1 and D3 are repaired (rows, the Unzip header); D2 (`STATEMENTS.md`) is the PI's.
  The call law's part (a) and the second box are after that review and unrefereed.
- Timing: `sh check.sh` passes in 10 s with everything built, and in 291 s from scratch (all 82 modules, a copy of
  the workspace with an empty `.lake`, machine load about 7 on 4 cores). Cold times of the tape files under that
  load: Clock 123 s (mostly `omega` on the charts), CallProof 50 s, UnzipProof 49 s, Unzip 47 s, TapeSignals 38 s,
  Tape 20 s, Line 13 s, the rest under 10 s.

## Bearing on the owner's journal

The journal's 10:30 entry of 2026-11-15 ("a clock (a wire between two caps, period 4N + 2 for N units of wire)") and
its correction (the clock stands, its proof rebuilt by a reviewer): the clock of every length is now checked by
Lean's kernel, and so is the tape that the signals rest on, the gun's line, the train's nine signals, push 8's
count read ("the count leaves as a train of pulses") for every k, and push 9's call, whole. The unzip proof found something small and
pretty: the count read is a front of fixed shape, `f 9`, sweeping through the stretch at the speed of a pulse while
the pulses it sheds run the other way, so the whole release for every k is three local pictures.
