import GumpMath.ChainTilt
import GumpMath.ChainPerron
import GumpMath.ChainExist
import GumpMath.ChainLemma0
import GumpMath.ChainCoins
import GumpMath.ChainRoutes
import GumpMath.ChainSeam
import GumpMath.ChainSSM
import GumpMath.ChainPrice
import GumpMath.ChainInst
import GumpMath.ChainTiltLimit
import GumpMath.ChainBits
import GumpMath.ChainKagome
open Gump.Chain
-- Theorem 2 (the tilt identity) and its analytic core
#print axioms neg_log_Z_one
#print axioms tiltMean_antitone
#print axioms integral_tiltMean_bounds
#print axioms KilledChain.IsQSD.survival_eq
#print axioms KilledChain.IsQSD.lifetime_eq
#print axioms KilledChain.IsQSD.last_living_law
#print axioms KilledChain.tilt_identity
#print axioms KilledChain.price_mem
#print axioms KilledChain.exists_qsd
#print axioms KilledChain.tilt_identity_exists
#print axioms ProductKernel.tilt_identity_product
-- Theorem 1 (the upper bound) and its constant
#print axioms KilledChain.upper_bound
#print axioms aliveNext_eq_rule
#print axioms threeCoins_death_ge
#print axioms twoCoins_death_ge
#print axioms KilledChain.upper_bound_coins
#print axioms emax_main
#print axioms emax_fair
-- Perron-Frobenius, built here
#print axioms exists_pos_eigenvector
#print axioms exists_pos_left_eigenvector
#print axioms left_eigen_pos
#print axioms left_eigen_unique
#print axioms KilledChain.qsd_exists_unique
#print axioms KilledChain.price_invariant
-- Lemma 0
#print axioms SubsetChain.death_pos
#print axioms SubsetChain.lemma0
#print axioms SubsetChain.lemma0_qsd
#print axioms ProductKernel.supp
#print axioms ProductKernel.total
-- Lemma R
#print axioms Routes.routes_first
#print axioms Routes.routes_second
#print axioms Routes.log_odds
#print axioms Routes.routes_concave
#print axioms Routes.two_routes_step
-- the seam identity
#print axioms Seam.sum_pathF
#print axioms Seam.coverW_eq_ringL
#print axioms Seam.coverZ
#print axioms Seam.cover_marginal
#print axioms Seam.seam_identity
#print axioms Seam.seam_identity_obs
#print axioms Seam.seam_sharp
-- Theorem 3 under (SSM)
#print axioms SSM.toIntSSM
#print axioms thm3a
#print axioms thm3b
#print axioms thm3c
#print axioms thm3d
-- the price per cell
#print axioms Price.price_exists_of_sub
#print axioms Price.price_exists_of_super
#print axioms Price.price_interval
-- the instantiation interface and Lemma 0 in abstract form
#print axioms KilledChain.ofStochastic_death
#print axioms KilledChain.isQSD_of
#print axioms KilledChain.one_class
#print axioms surrogate_theorems
-- Theorem 3 without (SSM): monotonicity of the tilt
#print axioms tilt_riemann_bounds
#print axioms price_of_pointwise
-- the surrogate's kernel on bit masks (the shape of GumpMath/DiceDef.lean)
#print axioms Bits.sum_bits
#print axioms Bits.bitP_row
#print axioms Bits.bitP_pos_iff
#print axioms Bits.one_sub_aliveProbR_three
#print axioms Bits.one_sub_aliveProbR_two
#print axioms Bits.bit_surrogate
#print axioms Bits.bit_one_class
-- Lemma 0 in full on the kagome layer (every wrapped face)
#print axioms Kagome.window_iff
#print axioms Kagome.M_uX
#print axioms Kagome.singleton_reach
#print axioms Kagome.grow_iter_univ
#print axioms Kagome.kagome_lemma0
#print axioms Kagome.kagome_one_price
#print axioms Kagome.nbrs_rot_perm
#print axioms Kagome.kagome_rotation
#print axioms Kagome.kagome_upper_bound
