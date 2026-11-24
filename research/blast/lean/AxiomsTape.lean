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
