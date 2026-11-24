/-
ref-chain, fifth review: `HullGen.hull_lemma0` and `hull_full_every` applied beyond the kernel-certified range, and
`rot_aut`/`refl_aut` for an R with no per-R check.

  cd research/blast/lean/mathlib && lake env lean /home/user/gump-for-agents/research/blast/ref-chain/RefChainHullGen.lean
-/
import GumpMath.LinkHullSym

open Gump.Dice Gump.Link

#check @HullGen.hull_lemma0
#check @hull_full_every
#check @HullGen.rot_aut
#check @hull_prices_sym

/-- R = 15 and R = 21 (108 and 231 cells): no certificate exists for them; the general theorem applies. -/
example : Lemma0F (Gump.Dice.hull 15) := HullGen.hull_lemma0 15 (by decide)
example : Lemma0F (Gump.Dice.hull 21) := HullGen.hull_lemma0 21 (by decide +kernel)
example : autOK (Gump.Dice.hull 21) (HullGen.gList 21 HullGen.rot) = true := HullGen.rot_aut 21
example := hull_full_every 21 (by decide +kernel)

#print axioms HullGen.hull_lemma0
#print axioms HullGen.hull_lemma0_ge3
#print axioms hull_full_every
#print axioms HullGen.rot_aut
#print axioms HullGen.refl_aut
#print axioms HullGen.aut_general
#print axioms hull_prices_sym
