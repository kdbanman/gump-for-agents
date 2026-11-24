/- The axioms each headline theorem of the tape files rests on (`Gump/Tape*.lean`, `Gump/Line*.lean`,
`Gump/Clock*.lean`, `Gump/Unzip*.lean`, `Gump/Call*.lean`). `check.sh` fails on anything beyond propext,
Classical.choice, Quot.sound. -/
import Gump.Tape
import Gump.Line
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
