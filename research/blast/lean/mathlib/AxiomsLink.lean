import GumpMath.LinkBridge
import GumpMath.LinkUnique
import GumpMath.LinkSym
import GumpMath.LinkFaces
import GumpMath.LinkNoCert
import GumpMath.LinkTorus202
import GumpMath.LinkHull3Sym
import GumpMath.LinkTorus103Sym
import GumpMath.LinkTorus113Sym
import GumpMath.LinkStrip13Sym
import GumpMath.LinkPatch13Sym
import GumpMath.LinkSurv
import GumpMath.LinkWrappedAll
import GumpMath.LinkWrappedArea
import GumpMath.LinkHullCert
import GumpMath.LinkHullGen
import GumpMath.LinkHullSym
open Gump.Link
-- the bridge
#print axioms aliveProb_cast
#print axioms P_cast
#print axioms aliveProb_mem
#print axioms toDice
#print axioms ofDice
#print axioms face_theorems
#print axioms face_theorems_allcoins
#print axioms aliveProbR_pos_iff
#print axioms Q_pos_iff
#print axioms survD_of_canSurvive
#print axioms face_class
#print axioms one_class'
#print axioms log_lifetime_eq
#print axioms face_lifetime
#print axioms price_sym
-- one lifetime theorem per certified face
#print axioms Hull3.hull3_link
#print axioms Hull3.hull3_prices
#print axioms Hull3.hull3_full
#print axioms Torus103.torus103_link
#print axioms Torus103.torus103_prices
#print axioms Torus103.torus103_full
#print axioms Torus113.torus113_link
#print axioms Torus113.torus113_prices
#print axioms Torus113.torus113_full
#print axioms Strip13.strip13_link
#print axioms Strip13.strip13_prices
#print axioms Strip13.strip13_full
#print axioms Patch13.patch13_link
#print axioms Patch13.patch13_prices
#print axioms Patch13.patch13_full
-- the 12-cell torus (2,0),(0,2), without a certified λ
#print axioms face_classF
#print axioms face_unique
#print axioms Torus202.tab
#print axioms Torus202.price_all
#print axioms Torus202.torus202_full
-- survFrom is Face.survival; hull 3 with the dice agent's constants
#print axioms survFrom_cast
#print axioms absorbing_hull
#print axioms absorbing_of_coins
#print axioms Hull3.hull3_complete
-- every wrapped face
#print axioms Wrapped.torusNb_of
#print axioms Wrapped.kIdx_map
#print axioms Wrapped.Q_eq
#print axioms Wrapped.transport_price
#print axioms Wrapped.wrapped_theorems
#print axioms Wrapped.wrapped_full
#print axioms Wrapped.torusNb_2_0_2
#print axioms Wrapped.torusNb_3_1_3
#print axioms Wrapped.nb_eq
#print axioms Wrapped.torusNb_all
#print axioms Wrapped.wrapped_theorems_all
#print axioms Wrapped.wrapped_full_all
#print axioms Wrapped.wrapped_area
-- every hull face
#print axioms cellsOK_hull
#print axioms hull_theorems
#print axioms Q_pos_iffF
#print axioms face_full_of
#print axioms hull_full_all
#print axioms lemma0_of_cert
#print axioms price_aut
#print axioms hull_full_sym
#print axioms hull1_lemma0
#print axioms hull3_lemma0
#print axioms hull13_lemma0
#print axioms hull13_rot
#print axioms hull13_refl
-- Lemma 0 and the symmetries on every hull face, general proofs
#print axioms HullGen.k_mask
#print axioms HullGen.stepN_mask
#print axioms HullGen.kc_le_four
#print axioms HullGen.kc_le_one
#print axioms HullGen.kc_le_five
#print axioms HullGen.kc_two
#print axioms HullGen.descent
#print axioms HullGen.enterT
#print axioms HullGen.walk_all
#print axioms HullGen.grow
#print axioms HullGen.step_TZ
#print axioms HullGen.step_U
#print axioms HullGen.aliveF_u
#print axioms HullGen.hull_lemma0
#print axioms hull_full_every
#print axioms HullGen.aut_general
#print axioms HullGen.rot_aut
#print axioms HullGen.refl_aut
#print axioms hull_prices_sym
