/-
**Meetings of signals on the rake train** (`research/signals/README.md` section 31; REVIEW-signals-6 §3).
-/
import Gump.TapeSignals
import Gump.TapeSuper

namespace Gump.Tape.Signals
open Gump Gump.Tape Gump.Bits

/-- The highest unit of a signal's cells, relative to its lowest unit. -/
def Kind.top : Kind → Int
  | .E => 1 | .U => 0 | .H => 0 | .K0 => 0 | .K3 => 2 | .N1 => 1 | .N2 => 2 | .N3 => 2 | .N4 => 0

theorem cells_units (K : Kind) : ∀ q ∈ K.cells, 0 ≤ unitOf q ∧ unitOf q ≤ K.top := by
  cases K <;> decide

theorem sig_units (K : Kind) (u : Int) : ∀ q ∈ sig K u, u ≤ unitOf q ∧ unitOf q ≤ u + K.top := by
  intro q hq
  simp only [sig, List.mem_map] at hq
  obtain ⟨c, hc, rfl⟩ := hq
  have := cells_units K c hc
  simp only [unitOf_shiftPt]; omega

theorem lcfg_sig_off (K : Kind) (u : Int) (q : Pt) (h : unitOf q < u ∨ u + K.top < unitOf q) :
    lcfg (sig K u) q = false := by
  cases e : lcfg (sig K u) q
  · rfl
  · have := sig_units K u q ((lcfg_iff _ _).mp e); omega

/-- **Two signals on the train**: A with lowest unit a and B with lowest unit b, flipped at train phase 1. -/
def pair (A B : Kind) (a b : Int) : Config := xorC (train 1) (lcfg (sig A a ++ sig B b))

theorem train_shift_one (t : Nat) : shiftC 1 (train t) = train (t + 2) := by
  rw [train_shift]
  funext p
  have := congrFun (train_shift_even t 2 (by decide)) (shiftPt 1 p)
  simp only [shiftC, shiftPt_shiftPt] at this ⊢
  rw [show (-2 : Int) + 1 = -1 by omega] at this
  rw [this, show - -(1 : Int) = 1 by omega]

theorem train_shift_nat (t : Nat) : ∀ n : Nat, shiftC n (train t) = train (t + 2 * n)
  | 0 => by funext p; simp [shiftC]
  | n + 1 => by
    have : shiftC ((n + 1 : Nat) : Int) (train t) = shiftC 1 (shiftC n (train t)) := by
      funext p; simp only [shiftC, shiftPt_shiftPt]; congr 2; push_cast; omega
    rw [this, train_shift_nat t n, train_shift_one]; congr 1

/-- One double step of a meeting while the two signals are at least five units apart: each moves one unit. -/
theorem pair_step (A B : Kind) (hA : A.dir = 1) (hB : B.dir = -1) (a b : Int) (ha : a % 2 = A.par % 2)
    (hb : b % 2 = B.par % 2) (hab : a + A.top + 5 ≤ b) : run (pair A B a b) 2 = shiftC 1 (pair A B a (b - 2)) := by
  let m := a + A.top + 2
  have hglue : pair A B a b = glue m (xorC (train 1) (lcfg (sig A a))) (xorC (train 1) (lcfg (sig B b))) := by
    funext q
    simp only [pair, glue, xorC, lcfg_append']
    split
    · rw [lcfg_sig_off B b q (by omega), Bool.or_false]
    · rw [lcfg_sig_off A a q (by omega), Bool.false_or]
  rw [hglue, superpose_units (train 1) _ _ (a + A.top + 1) (b - 1) m 2
    (fun q hq => by simp only [xorC]; rw [lcfg_sig_off A a q (by omega), Bool.xor_false])
    (fun q hq => by simp only [xorC]; rw [lcfg_sig_off B b q (by omega), Bool.xor_false])
    (by omega) (by omega), signal_step A a ha, signal_step B b hb, hA, hB]
  funext q
  simp only [glue, pair, shiftC, xorC, lcfg_append']
  have e1 : train 1 (shiftPt (-1) q) = train 3 q := by
    have := congrFun (train_shift_one 1) q; simp only [shiftC] at this; exact this
  have e2 := congrFun (lcfg_sig_shift A a 1) q
  have e3 := congrFun (lcfg_sig_shift B (b - 2) 1) q
  simp only [shiftC] at e2 e3
  rw [e1, e2, e3, show b - 2 + 1 = b + -1 by omega]
  split
  · rw [lcfg_sig_off B (b + -1) q (by omega), Bool.or_false]
  · rw [lcfg_sig_off A (a + 1) q (by omega), Bool.false_or]

/-- **One meeting per pair**: two signals moving towards each other from any distance b − a + 2n are, after 2n
generations, the pair at distance b − a moved n units. So each ordered pair of kinds has one meeting at each parity
of the distance, up to translation and time. -/
theorem pair_run (A B : Kind) (hA : A.dir = 1) (hB : B.dir = -1) (a b : Int) (ha : a % 2 = A.par % 2)
    (hb : b % 2 = B.par % 2) (hab : a + A.top + 3 ≤ b) :
    ∀ n : Nat, run (pair A B a (b + 2 * n)) (2 * n) = shiftC n (pair A B a b)
  | 0 => by
    funext q
    show pair A B a (b + 2 * ((0 : Nat) : Int)) q = pair A B a b (shiftPt (-((0 : Nat) : Int)) q)
    simp
  | n + 1 => by
    rw [show 2 * (n + 1) = 2 + 2 * n by omega, run_add,
      pair_step A B hA hB a _ ha (by omega) (by push_cast; omega),
      show b + 2 * ((n + 1 : Nat) : Int) - 2 = b + 2 * (n : Int) by push_cast; omega, run_shiftC,
      pair_run A B hA hB a b ha hb hab n]
    funext q; simp only [shiftC, shiftPt_shiftPt]; congr 1; congr 1; push_cast; omega

/-- A run of k generations of train(1) ⊕ σ checked on a finite piece, read on the whole lattice. -/
theorem diff_run (σ σ' : List Pt) (k : Nat) (lo hi a : Int) (n : Nat) (V : Pt) (hV : V.even)
    (h : pieceCheck (trainF 1) (trainF (1 + k)) a n σ σ' k lo hi V = true) (hb1 : -8 ≤ lo + V.x / 2)
    (hb2 : hi + V.x / 2 ≤ 23) (ha : a ≤ lo - k) (hn : hi + k < a + n)
    (hσ : ∀ q ∈ σ, lo + k ≤ unitOf q ∧ unitOf q ≤ hi - k) (hσ' : ∀ q ∈ σ', lo ≤ unitOf q ∧ unitOf q ≤ hi) :
    run (xorC (train 1) (lcfg σ)) k = xorC (train (1 + k)) (lcfg σ') := by
  funext p
  by_cases hin : lo ≤ unitOf p ∧ unitOf p ≤ hi
  · exact pieceCheck_spec (trainF_unit 1) (trainF_unit (1 + k)) hV h hb1 hb2 (by omega) ha hn _
      (fun q _ _ => rfl) p hin.1 hin.2
  · have away : ∀ q, unitOf p - k ≤ unitOf q → unitOf q ≤ unitOf p + k → xorC (train 1) (lcfg σ) q = train 1 q := by
      intro q q1 q2
      simp only [xorC]
      cases e : lcfg σ q
      · simp
      · have := hσ q ((lcfg_iff _ _).mp e); omega
    rw [run_eq_of_units k away, train_run]
    simp only [xorC]
    cases e : lcfg σ' p
    · simp
    · have := hσ' p ((lcfg_iff _ _).mp e); omega

/-- The pair moved by an even number of units. -/
theorem pair_shift (A B : Kind) (a b e : Int) (he : e % 2 = 0) :
    shiftC e (pair A B a b) = pair A B (a + e) (b + e) := by
  funext q
  have h1 := congrFun (train_shift_even 1 e he) q
  have h2 := congrFun (lcfg_sig_shift A a e) q
  have h3 := congrFun (lcfg_sig_shift B b e) q
  simp only [shiftC] at h1 h2 h3
  simp only [pair, shiftC, xorC, lcfg_append']
  rw [h1, h2, h3]

theorem train_shift_int (t : Nat) (e : Int) (he : e % 2 = 0) : shiftC e (train t) = train t :=
  train_shift_even t e he

/-- The translation into the box for the meeting checks. -/
def meetFrame : Pt := ⟨8, 8, 16⟩

theorem meetFrame_even : meetFrame.even := by
  show (8 : Int) % 2 = 0 ∧ (8 : Int) % 2 = 0 ∧ (16 : Int) % 2 = 0
  decide

/-! ### U meets K0: both vanish -/

def checkUK0 : Bool := pieceCheck (trainF 1) (trainF (1 + 4)) (-7) 20 (sig .U 1 ++ sig .K0 4) [] 4 (-3) 8 meetFrame

theorem checkUK0_ok : checkUK0 = true := by decide +kernel

theorem UK0_base : run (pair .U .K0 1 4) 4 = train 5 := by
  have h := diff_run (sig .U 1 ++ sig .K0 4) [] 4 (-3) 8 (-7) 20 meetFrame meetFrame_even checkUK0_ok
    (by decide) (by decide) (by decide) (by decide)
    (fun q hq => by
      rcases List.mem_append.mp hq with h | h
      · have := sig_units .U 1 q h; simp only [Kind.top] at this; omega
      · have := sig_units .K0 4 q h; simp only [Kind.top] at this; omega)
    (fun q hq => by simp at hq)
  rw [pair, h]
  funext q; simp [xorC, lcfg_nil']

/-- **U meets K0: both vanish.** For every odd a and every n, the up-signal U at unit a and the down-signal K0 at unit
a + 3 + 2n (any distance ≥ 3 of the right parity) meet, and from generation 2n + 4 on the configuration is exactly
the plain train. -/
theorem meet_U_K0 (a : Int) (ha : a % 2 = 1) (n t : Nat) (ht : 4 ≤ t) :
    run (pair .U .K0 a (a + 3 + 2 * n)) (2 * n + t) = train (1 + 2 * n + t) := by
  rw [run_add, pair_run .U .K0 rfl rfl a (a + 3) (by simp [Kind.par]; omega) (by simp [Kind.par]; omega)
    (by simp [Kind.top]) n, run_shiftC]
  have e : pair .U .K0 a (a + 3) = shiftC (a - 1) (pair .U .K0 1 4) := by
    rw [pair_shift _ _ _ _ _ (by omega)]; congr 1 <;> omega
  rw [e, run_shiftC, show t = 4 + (t - 4) by omega, run_add, UK0_base, train_run, train_shift_int _ _ (by omega),
    train_shift_nat]
  congr 1; omega

end Gump.Tape.Signals
