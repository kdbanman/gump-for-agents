# Referee report: the tape files of the Lean arm (`research/blast/lean/`, arm `tape`)

*Referee `ref-tape`, 2026-11-24, about 13:10 to 14:10 UTC. I examined commit `6be19d4` ("lean: tape report, cold
check.sh timing"). Files committed later (`Gump/CallBox.lean`, commit `8d201ea`) and untracked files
(`Gump/CallUnionData.lean`, `tape_callunion.py`) are outside this review. Everything below can be rerun from the
scripts in this directory. Logs are in `logs/`, bulk output in `research/scratch/blast/ref-tape/`. I wrote every
check from `reference/oracle.py`, the catalogue's JSON files and its prose. None of the tape agent's scripts was run
or imported.*

**Verdict.** I did not break any of the theorems. The Lean objects are the catalogue's objects, cell for cell:
119 comparisons, the tape's letters, the line, the clock, the train, the nine signals, the store wire and the call
line. The catalogue's laws hold on the oracle well beyond the base cases, with their sharp boundaries. The line
has preperiod exactly 2N for N = 2…14, 20 and 31. The unzip is final exactly from 2k + 6 for k = 1…20. The call's
part (b) holds exactly from 2k + 34 for k = 1…10, and part (a) holds on the whole torus. The bit-level checkers
reject a false claim built on the stepper's wrong answer at the edge of its box. No constant in the 13 tape modules
or their dependencies rests on anything beyond `propext`, `Classical.choice` and `Quot.sound`. `check.sh` passes on
a clean copy.

The defects are the following. One headline, `clock_every_length`, says less than its row: it is an existential
that does not name the clock, and two short clocks side by side also satisfy it. `STATEMENTS.md` at `6be19d4` lacks
8 of the 17 tape rows. Three passages of prose are stale.

## 1. Defects, ranked by how much they matter

| # | defect | where | how to see it |
|---|---|---|---|
| D1 | **`clock_every_length` says less than its row.** The statement is `∃ c, run c (4N+2) = c ∧ (∀ k, 0<k<4N+2 → run c k ≠ c) ∧ supp c ⊆ {units −4..N+3, \|y\|<32, \|x+z\|<64}`. Nothing ties `c` to capL, N units of wire C and capR. Any oscillator of exact period 4N + 2 inside a tube N + 8 units long satisfies it. **[measured]** The lit clocks of 1 and of 2 units, side by side (the second moved by (0,16,0), 81 cells), form an oscillator of exact period 30 = 4·7 + 2. Every one of its states lies inside the tube that `clock_every_length 7` allows. So that statement does not distinguish the clock of 7 units from two clocks of 1 and 2 units. The period is minimal, not merely a period. The row (`statements_tape.json`) says "Same, with the oscillator's support bounded … For N ≥ 6 it is the source's surgery cycle". The second sentence describes the proof, not the statement. `notes/tape.md` ("Not checked") does disclose that the statement does not identify the object. The theorem that does name the object is `clock_cycle` (`clockY j`, Clock.lean:330, 366). | `Gump/Clock.lean:475`; row `clock_every_length` | `python3 rt_dyn.py twoclocks` (0.3 s) |
| D2 | **`STATEMENTS.md` is stale at `6be19d4`.** It holds 9 of the 17 tape rows of `statements_tape.json`. Missing are `clock_every_length`, `clock_cycle`, `lit_clock_small`, `unzip_law_sharp`, `unzip_law`, `stretch_stands`, `glue_run_moving` and `call_law_b`: the clock, the unzip law and the call law. Rerunning `statements.py` on the commit's sources adds them, together with 74 rows of other arms. Nothing in `check.sh` detects a stale table. | `research/blast/lean/STATEMENTS.md` | `git show 6be19d4:research/blast/lean/STATEMENTS.md \| grep -c clock_every_length` gives 0. The regenerated copy is in `research/scratch/blast/ref-tape/stmt/` (`python3 statements.py` there). |
| D3 | **Stale or inexact prose.** (i) The row `glue_run` says "the moving seam of push 8 and the call law is not formalised", but `glue_run_moving` is proved (Unzip.lean:204) and has its own row. (ii) The header of `Gump/Unzip.lean` (line 15) says the unzip laws are "both stated, not proved", but both are proved in `UnzipProof.lean`. (iii) The row `line_period_four` cites `Gump.Signals.lineC_N_period_four`. No such constant exists: it is schematic for `lineC_{2,3,12,13}_period_four` in `Gump/Signals.lean`. | as named | `lake env lean RtAxioms.lean`: "name lineC_N_period_four: 0 constant(s)" |

These are the only defects. The following are observations, not defects. Each is disclosed by the author.

- `clock_cycle` is about `clockY j`, the surgery built on the base state X0. That X0 and `clockY j` are states of
  the catalogue's lit clock is not proved in Lean. Here they are **[measured]**: X0 is the oracle state of the lit
  clock of 6 units at generation 41, and for j = 0…6 `clockY j` is exactly one state of the oracle cycle of the
  lit clock of 6 + j units.
- `call_law_b` concerns V_k, the store wire alone with e1 forced at generation 29. Part (a) of the call law, which
  says that V_k is what the wire does under the line, is stated (`CallLaw`) and not proved. The row says so. On the
  oracle, (a) holds for k = 1…10 at every generation 0…2k + 38 on the whole torus.

## 2. Verdict for each law

"Same" means the Lean statement says what its row says and what its source says. Each object check compares the
Lean definition, evaluated by `#eval` (`RtDump.lean`), with the object that `rt_objects.py` builds from the JSON
files (`rt_compare.py`).

| law (Lean) | verdict | objects | behaviour on the oracle (beyond the base cases) |
|---|---|---|---|
| `tape_run`, `tape_local_run`, `tape_run_shift`, `wire_two` | **same** for `tape_run`, on the whole lattice for every word. `tape_local_run` says more: its hypothesis is agreement on a stretch. | `cellsOf B`, `cellsOf C` are wire C's unit of `line-C.json`/`clock-C.json` and wire B's unit read off `tape-BC.json` at all of its B's. `tape w` for a test word on units −6…8, all points of the box: equal (75 cells). Negative units included, so `unitOf` = ⌊x/2⌋ as the catalogue has it. | 9 random words on rings of 40, 37 and 23 units, whole torus, every even generation up to 90 (more than two laps): the state at 2n is the word shifted by n. Negative control fails as it should. |
| `line_orbit`, `line_period_four`, `S_succ` | **same as the row; more than the source.** The right-hand side is exact for every s and every p > 0, so the preperiod is exactly 2N and the period exactly 4. `orbit_classify`'s three facts suffice: if the state at s < 2N returned after p, the state at 2N − 1 would return after 4p and equal the state at 2N + 3. I checked that on paper, and the kernel checked it. | `lineList N` is capA + N units + gun moved N, as in the `note` of `line-C.json`, for N = 2, 3, 4, 5, 7, 12, 20 and 31. | N = 2…14, 20, 31: X(2N+4) = X(2N), X(2N+2) ≠ X(2N), X(2N+3) ≠ X(2N−1), and the whole table "X(s+p) = X(s) iff s ≥ 2N and 4 ∣ p" for s ≤ 2N + 10, 1 ≤ p ≤ 12. |
| `clock_every_length` | **less** (D1). | see `clock_cycle` | |
| `clock_cycle`, `surg_step`, `chartA`, `chartB` | **same** as the source's surgery: exact period 26 + 4j, and the support. `chartA` and `chartB` hold for every j, i and t in one period window, which is all `surg_run` needs. | X0 = oracle(lit clock of 6 units, generation 41). `clockY j`, evaluated with Lean's own `chart` and `cidx` through the kernel-proved identity `Xb_frame`, is one state of the lit clock's cycle for N = 6 + j, j = 0…6. | Lit clock of N = 6…13 and 20 units: exact period 4N + 2 from generation N − 2, and generation N − 3 is not on the cycle. |
| `lit_clock_small` | **same** as the row (N = 1…5; "not periodic earlier" not claimed). | `litList N` = capL + N units + capR moved N + (1,0,4) moved ⌊N/2⌋ units (`verify_clock.py`'s convention), for N = 1…12. | Also entry exactly at max(N − 2, 0) and support in units −4…N + 3 for N = 1…5. |
| `train_step`, `train_shift` | **same**, on the whole lattice. | `trainBase t par` = the oracle train (rake5 on even units, rakef on odd units at generation 0, ring of 16 units) at generations 0…3. `train t` (ucfg) on units −4…5 equals the oracle train. | The line of 30 units, generations 60…63: units 4…24 are exactly this train at the matching phase. So it is the line's stream. |
| `signal_run` | **same**: every lowest unit of the kind's parity, every n. | The nine kinds' parity, direction and cells equal `sig6.py`'s `SIGS` (read with `ast`). | Each kind at three places, on a ring of 48 units, whole torus, n = 0…48 (one full lap): train(1+2n) ⊕ the signal moved dir·n. Negative control: moved the wrong way, it fails. |
| `unzip_law_sharp`, `unzip_law` | **same** (the "not at 2k + 4" of REVIEW-signals-8 §3 is the Lean's ≠ with the expected final state). Even generations only, as in the source. Nothing is said about odd ones (2k + 5 is odd). | `hexCells h` for all 16 letters equals cell8.json's stators and sites. `store k` and `countRead k` (stator (0,1,2) of unit −1 removed) on units −5…k + 5, and `tape (pulses k (−3))`, equal for k = 1, 2, 3, 5. | k = 1…20: the state at 2n is `tape (pulses k (2−n))` **exactly** for n ≥ k + 3 (checked n = 1…k + 7). Only units whose light cone sees one copy of the stretch are compared, i.e. units −1−2n…k + 2n, the whole torus in y, z. |
| `stretch_stands`, `hex_local` | **same** (infinite wire; the finite cell is not covered, as the row says). | as above | k = 1…12 and 20: every even generation 0…40 equals the start, and generation 1 differs. |
| `glue_run`, `glue_run_moving`, `orbit_classify` | **same** (lemmas). The row `glue_run` is stale (D3). | | |
| `call_law_b` | **same** as REVIEW-signals-9 §3 (b), for V_k. Part (a) is not proved (disclosed). | `storeAt k` (d^k f on units 36…36+k), the 162 cells of the line (`call9.json` run 0 `extra`), the two CALL cells (run 0 ops[3]), e1 = (71, 2, −70) and cross = 35: equal. | k = 1…10, ring of 76 units, torus (152, 104, 152). (a) X_k = V_k ⊔ Lf and the two are disjoint, whole torus, every generation 0…2k + 38. Not vacuous: the birth of e1 at 29 is needed. (b) V_k(2n) is the k pulses at c + 3 − (n − 14) **exactly** for n ≥ k + 17 (checked n = k + 14…k + 19). The free line is at rest (= `line`) at every even generation from 42. |
| `pieceCheck_spec`, `forcedCheck_spec`, `bstep_spec` | **sound as stated** (§3). | | |

Statement details I checked, all fine:

- Every `Config` equality is a function equality on all of ℤ³, non-cells included. Every object here holds cells
  only (asserted when the oracle loads them), so nothing is trivially unequal at s = 0.
- Natural-number subtraction is harmless where it occurs: 2N − 1 with N ≥ 2, μ − 1 with μ ≥ 1, N − 2 in
  `lit_clock_small` (= max(N − 2, 0)).
- Every `%` on `Int` is `emod`, with the parities and guards as meant.
- The quantifiers are in the right order: `line_orbit` takes ∀ N ≥ 2 ∀ s ∀ p > 0, and `UnzipLawSharp` takes
  ∀ k ≥ 1 (∀ n ≥ k+3 …) ∧ ≠ at k + 2.
- No hypothesis is vacuous.

## 3. The bit-level checker

`bstep_spec` (Bits.lean:379, unchanged since the snapshot that `ref-lean` refereed) is a whole-lattice equality,
`bcfg (bstep S) = step (bcfg S)`, for every S inside the core [−12, 44)³. Each checker carries its core test into
its spec:

- `agree` and `coreRun` check every intermediate state.
- `pieceCheck` is `coreRun` on the piece for k steps plus `eqOn` on the unit mask (units −8…23 of the box).
- `forcedCheck` checks the start in the core and three more steps after the forced cell.

The specs then transfer the result to the infinite configuration on units lo…hi. The hypotheses ask for agreement
on lo − k…hi + k, and that range lies inside the piece. This is the light cone, with the box translated by an even
vector. I read every use in the headline proofs: the train (3-unit pieces), the signals (11-unit pieces, signal
inside units lo + 2…hi − 2 and its image inside lo…hi), the tape windows, the zones and the start of the call. Each
satisfies the side conditions, and the kernel checked them.

**Attempted false certificate** (`RtCert.lean`, all `decide +kernel`). Take the cube still life centred at
(−14, 0, 0). It lies in the box but not in the interior. `bstep` kills its face (−15, 0, 0): the unchecked stepper
is wrong at the edge. The false claim "one generation removes that face" was put to `pieceCheck`, `oscCert` and
`forcedCheck`. **All three reject it.** The true claim at the edge is rejected too, so the checkers are conservative
there. Moved into the core, the true claim is accepted and the false one is rejected. I found no way to make a
checker accept something false. Its spec is a kernel-checked theorem, so the only remaining route would be an
unsound kernel.

## 4. Hygiene

- **grep** of the 13 tape modules and `AxiomsTape.lean` for `sorry`, `admit`, `native_decide`, `axiom`, `unsafe`,
  `implemented_by`, `extern`, `opaque`, `partial`, `macro`, `elab`, `syntax`, `instance`, `ofReduceBool`:
  - nothing beyond `deriving DecidableEq` (derived, not hand-written);
  - 14 `set_option maxHeartbeats … in`, which raise a resource limit and do not weaken checking.
  - The lakefile has no options.
- **Axioms of every constant** (`RtAxioms.lean`, `Lean.collectAxioms`): 2,074 constants declared in the 13 tape
  modules and 795 constants of their `Gump` dependencies. None goes beyond the three standard axioms. None is an
  `axiom` or `opaque`. The axiom sets seen in the tape modules are {} 296, {propext} 218, {propext, Quot.sound}
  1,233 and {propext, Classical.choice, Quot.sound} 327. The controls in `RtCert.lean` show that the tool sees
  `sorry` (`sorryAx`) and `native_decide` (`…native_decide.ax_1_1`).
- **Names.** Every name in `AxiomsTape.lean` resolves, since `check.sh` runs that file. Every row name of
  `statements_tape.json` resolves to exactly one constant, and so do the brief's names: `train_shift`,
  `surg_step`, `chartA`, `chartB`, `hex_local`, `pieceCheck_spec`, `forcedCheck_spec`, `CallLaw`,
  `UnzipLawSharp`, `LineRest`. The one exception is the schematic `lineC_N_period_four` (D3).
- **Rows.** Each row's "difference from the source" is honest except `clock_every_length` (D1) and `glue_run`
  (D3). `lit_clock_small`, `stretch_stands` and `call_law_b` state their restrictions.
- **`check.sh` on a clean copy** (`git archive 6be19d4` of `research/blast/lean`, `reference`, without `.lake` and
  `mathlib/`, under `research/scratch/blast/ref-tape/copy/`): passes, building 82 jobs, with 118 headline theorems,
  the 2012 logs of sides 8, 9 and 10, and 3 soups × 60 generations. It took 331 s on one core (`taskset -c 3`,
  `nice 10`, load about 10). Log: `logs/check_clean.log`.

## 5. Not checked

- **The proofs themselves.** The kernel checked them. I read proofs only where a statement's meaning depended on
  them: `orbit_classify`, the specs, `lit_spec` and `clock_cycle`'s support.
- **The tape agent's scripts** (`tape_*.py`), its `*Data.lean` generators, and its claim that the scripts
  regenerate the data files. I compared the data files with the JSON files directly instead.
- **Sizes beyond those listed:**
  - the line beyond N = 31;
  - the clock beyond N = 20 (`clockY` beyond j = 6);
  - the unzip beyond k = 20;
  - the call beyond k = 10 and beyond generation 2k + 38;
  - signals beyond a ring of 48 units and 96 generations.
  The oracle runs for the unzip, the train, the signals and the call are rings on the array torus. For the unzip
  and the call, only units whose light cone sees a single copy of the defect are compared. The call's (a) is a
  statement about the torus run, which equals the infinite run near the crossing for t ≤ 2k + 38 by the light cone
  with the ring of 76 units.
- **Not tested on the oracle:** whether `pieceCheck` and `forcedCheck` accept every true claim. Only soundness
  matters for the theorems.
- **The finite objects of pushes 8 and 9** (caps, cells). The Lean does not claim them.
- **The Mathlib package and every file outside the tape list.** Commits after `6be19d4`.

## 6. Reproduce

Run these from `research/blast/ref-tape/`, against a built copy (see §4) at `C = research/scratch/blast/ref-tape/copy/research/blast/lean`:

| what | command | time |
|---|---|---|
| Lean objects to cell sets | `cd $C && lake env lean <here>/RtDump.lean > dump.txt` | 4 s |
| compare with the catalogue (119 PASS) | `python3 rt_compare.py dump.txt` (negative control: 5 mutations of the dump, 5 FAIL, `logs/compare_mutated.log`) | 2 s |
| oracle: tape / line / clock / two clocks / train / signals / stands | `python3 rt_dyn.py tape` (and `line`, `clock`, `twoclocks`, `train`, `signals`, `stands`) | 0.3–11 s each |
| oracle: unzip k = 1…10, 11…20 | `python3 rt_dyn.py unzip`, `python3 rt_dyn.py unzip 11-20` | 2 s, 15 s |
| oracle: call k = 1…5, 6…10 | `python3 rt_dyn.py call`, `python3 rt_dyn.py call 6-10` | 19 s, 33 s |
| axiom sweep and names | `cd $C && lake env lean <here>/RtAxioms.lean` | 12 s |
| false certificate at the box edge, audit controls | `cd $C && lake env lean <here>/RtCert.lean` | 2 s |

Files: `rt_lib.py` holds `oracle.step` on an edge-asserted box and on a ring torus; it contains no other stepper.
`rt_objects.py` builds the catalogue's objects from the JSON files. The other scripts are named above.
