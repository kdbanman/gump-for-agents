/- The axioms each headline theorem rests on. `check.sh` fails if `sorryAx` or `Lean.ofReduceBool`
(the compiler trusted as a prover) appears. -/
import Gump
open Gump
#print axioms layer_histogram
#print axioms Sealed.run_dead
#print axioms Sealed.union
#print axioms above_sealed
#print axioms band_sealed
#print axioms confinement
#print axioms hull
#print axioms firewall
#print axioms firewall_separates
#print axioms slab_closed
