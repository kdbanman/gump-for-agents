/- The axioms each headline theorem of the tape files rests on (`Gump/Tape*.lean`, `Gump/Line*.lean`,
`Gump/Clock*.lean`, `Gump/Unzip*.lean`, `Gump/Call*.lean`). `check.sh` fails on anything beyond propext,
Classical.choice, Quot.sound. -/
import Gump.Tape
import Gump.Line
import Gump.TapeSignals
import Gump.Clock
import Gump.Call
import Gump.UnzipProof
import Gump.CallProof
import Gump.CallUnionLocal
import Gump.ClockLit
import Gump.LineBeam
import Gump.ClockReader
import Gump.CallReader
import Gump.ClockLitFirst
import Gump.ClockLitOdd
open Gump Gump.Tape
#print axioms glue_run
#print axioms run_shiftC
#print axioms orbit_classify
#print axioms window_ok
#print axioms tape_local
#print axioms tape_local_run
#print axioms tape_run
#print axioms tape_run_shift
#print axioms Gump.Line.baseCheck_ok
#print axioms Gump.Line.S_succ
#print axioms Gump.Line.S_four
#print axioms Gump.Line.line_orbit
#print axioms Gump.Line.line_period_four
#print axioms Gump.Tape.Signals.train_step
#print axioms Gump.Tape.Signals.train_shift
#print axioms Gump.Tape.Signals.sigCheck_ok
#print axioms Gump.Tape.Signals.signal_step
#print axioms Gump.Tape.Signals.signal_run
#print axioms Gump.Clock.surg_step
#print axioms Gump.Clock.chartA
#print axioms Gump.Clock.chartB
#print axioms Gump.Clock.baseCheck_ok
#print axioms Gump.Clock.litCheck_ok
#print axioms Gump.Clock.clock_cycle
#print axioms Gump.Clock.lit_clock_small
#print axioms Gump.Clock.clock_every_length
#print axioms Gump.Clock.clockOf_period
#print axioms Gump.Clock.X0_lit
#print axioms Gump.Clock.clockY_zero_lit
#print axioms Gump.Unzip.tape_eq_hcfg
#print axioms Gump.Unzip.hex_local
#print axioms Gump.Unzip.storeWinOK_ok
#print axioms Gump.Unzip.stretch_stands
#print axioms Gump.Unzip.glue_run_moving
#print axioms Gump.Unzip.unzipLawSharp_imp
#print axioms Gump.Call.pulses_at
#print axioms Gump.Unzip.zonesOK_ok
#print axioms Gump.Unzip.step_generic
#print axioms Gump.Unzip.step_first
#print axioms Gump.Unzip.countRead_W
#print axioms Gump.Unzip.unzip_law_sharp
#print axioms Gump.Unzip.unzip_law
#print axioms Gump.Call.zonesV_ok
#print axioms Gump.Call.forcedCheck_spec
#print axioms Gump.Call.V0_W
#print axioms Gump.Call.call_law_b
#print axioms Gump.Call.Box.bstep_spec
#print axioms Gump.Call.lineCheck_ok
#print axioms Gump.Call.line_rest
#print axioms Gump.Call.Lf_snap
#print axioms Gump.Call.V_HV
#print axioms Gump.Call.Lf_HL
#print axioms Gump.Call.V_Lf_disjoint
#print axioms Gump.Call.step_or
#print axioms Gump.Call.zone_cover
#print axioms Gump.Call.LC_spec
#print axioms Gump.Call.checkStore_ok
#print axioms Gump.Call.checkStart_ok
#print axioms Gump.Call.checkVW_ok
#print axioms Gump.Call.checkTape_ok
#print axioms Gump.Call.local_union
#print axioms Gump.Call.call_law_a
#print axioms Gump.Call.call_law
#print axioms Gump.Clock.lit_init
#print axioms Gump.Clock.zonesLit_ok
#print axioms Gump.Clock.lit_step_big
#print axioms Gump.Clock.smallOK_ok
#print axioms Gump.Clock.lit_step_small
#print axioms Gump.Clock.lit_step
#print axioms Gump.Clock.lit_word
#print axioms Gump.Clock.baseLitCheck_ok
#print axioms Gump.Clock.chart_entry
#print axioms Gump.Clock.FL_entry
#print axioms Gump.Clock.lit_enters
#print axioms Gump.Clock.exact_period_run
#print axioms Gump.Clock.lit_clock
#print axioms Gump.Beam.glue_beam
#print axioms Gump.Beam.S_step
#print axioms Gump.Beam.baseOK_ok
#print axioms Gump.Beam.seam_facts
#print axioms Gump.Beam.S_all
#print axioms Gump.Beam.beam_period
#print axioms Gump.Clock.readerOK_ok
#print axioms Gump.Clock.reader_step
#print axioms Gump.Clock.reader_run
#print axioms Gump.Reader.reader_step_gen
#print axioms Gump.Reader.reader_run_gen
#print axioms Gump.Reader.cap9OK_ok
#print axioms Gump.Reader.capL9_ucfg
#print axioms Gump.Reader.reader9_run
#print axioms Gump.Clock.firstCheck_ok
#print axioms Gump.Clock.lit_left
#print axioms Gump.Clock.cycle_left
#print axioms Gump.Clock.lit_first_even
#print axioms Gump.Clock.lit_enters_exact
#print axioms Gump.Clock.firstCheckR_ok
#print axioms Gump.Clock.lit_right
#print axioms Gump.Clock.cycle_right
#print axioms Gump.Clock.lit_first_odd
#print axioms Gump.Clock.lit_first
#print axioms Gump.Clock.chart_odd
#print axioms Gump.Clock.oddCheck_ok
#print axioms Gump.Clock.lit_odd_entry
#print axioms Gump.Clock.lit_enters_at
#print axioms Gump.Clock.lit_clock_exact
