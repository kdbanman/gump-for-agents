/-
**Nine rigid signals on the rake train** (`research/signals/README.md` sections 30 to 35, `prove_echo.py`,
`echo_kinds.py`; the five further signals of `research/audit/REVIEW-signals-6.md`, `research/audit/signals6/sig6.py`).

The plain rake train of the line (rake5 on the even units and rakef on the odd units at generation 0, in the
frame of `research/signals/objects/line-C.json`) is a configuration of the whole lattice, infinite along the
wire: `train t` holds on unit u the cells `trainBase (t mod 4) (u mod 2)` moved u units.
`train_step`: it is an orbit, `step (train t) = train (t + 1)`; `train_shift`: two generations move it one unit
towards −v.

A signal of kind K with lowest unit u (of K's parity) is the finite set of cells `sig K u` flipped at phase 1.
`signal_run`: for each of the nine kinds, every such u and every n,

  run (train 1 ⊕ sig K u) (2n) = train (1 + 2n) ⊕ sig K (u + dir K · n),

so each signal rides the infinite train for ever, rigidly, one unit per two generations (up the stream for E, U,
N1; down with it for H, K0, K3, N2, N3, N4). The proof is the source's: a finite piece around the signal is
stepped twice by the kernel (`decide +kernel`, bit-parallel stepper); away from the signal the state is the train,
an orbit; translation along the wire carries the base case to every u and every n.
-/
import Gump.TapeSignalsData

namespace Gump.Tape
open Gump Gump.Bits

/-! ### Configurations given unit by unit -/

/-- Unit u holds the cells f u (cells of unit 0), moved u units. -/
def ucfg (f : Int → List Pt) : Config := fun p => lcfg (f (unitOf p)) (shiftPt (-unitOf p) p)

/-- The units a .. a + n − 1 of `ucfg f`, as a list. -/
def piece (f : Int → List Pt) : Int → Nat → List Pt
  | _, 0 => []
  | a, n + 1 => (f a).map (shiftPt a) ++ piece f (a + 1) n

theorem lcfg_append' (A B : List Pt) (p : Pt) : lcfg (A ++ B) p = (lcfg A p || lcfg B p) := by
  simp [lcfg]

theorem lcfg_piece (f : Int → List Pt) (hf : ∀ u, ∀ q ∈ f u, unitOf q = 0) :
    ∀ n a p, lcfg (piece f a n) p = (decide (a ≤ unitOf p ∧ unitOf p < a + n) && ucfg f p)
  | 0, a, p => by simp only [piece]; simp [lcfg]; omega
  | n + 1, a, p => by
    rw [piece, lcfg_append', lcfg_map_shiftPt, lcfg_piece f hf n (a + 1) p]
    simp only [shiftC, ucfg]
    by_cases hu : unitOf p = a
    · have e1 : decide (a + 1 ≤ unitOf p ∧ unitOf p < a + 1 + (n : Int)) = false := by
        simp only [decide_eq_false_iff_not]; omega
      have e2 : decide (a ≤ unitOf p ∧ unitOf p < a + ((n + 1 : Nat) : Int)) = true := by
        simp only [decide_eq_true_eq]; omega
      rw [e1, e2, Bool.false_and, Bool.or_false, Bool.true_and, hu]
    · have h0 : lcfg (f a) (shiftPt (-a) p) = false := by
        cases e : lcfg (f a) (shiftPt (-a) p)
        · rfl
        · have := hf a _ ((lcfg_iff _ _).mp e)
          simp only [unitOf_shiftPt] at this
          omega
      rw [h0, Bool.false_or]
      by_cases hr : a + 1 ≤ unitOf p ∧ unitOf p < a + 1 + (n : Int)
      · have hr' : a ≤ unitOf p ∧ unitOf p < a + ((n + 1 : Nat) : Int) := by omega
        simp only [hr, hr']
      · have hr' : ¬ (a ≤ unitOf p ∧ unitOf p < a + ((n + 1 : Nat) : Int)) := by omega
        simp only [hr, hr', decide_false, Bool.false_and]

/-- A configuration that repeats every two units is unmoved by a move of an even number of units. -/
theorem shiftC_ucfg_even (f : Int → List Pt) (hper : ∀ u v, u % 2 = v % 2 → f u = f v) (k : Int)
    (hk : k % 2 = 0) : shiftC k (ucfg f) = ucfg f := by
  funext p
  simp only [shiftC, ucfg, unitOf_shiftPt, shiftPt_shiftPt]
  rw [hper (unitOf p + -k) (unitOf p) (by omega), show -(unitOf p + -k) + -k = -unitOf p by omega]

/-- Pointwise exclusive or. -/
def xorC (c d : Config) : Config := fun p => xor (c p) (d p)

theorem bcfg_xor (S T : Nat) (p : Pt) : bcfg (S ^^^ T) p = xor (bcfg S p) (bcfg T p) := by
  simp only [bcfg, Nat.testBit_xor]
  cases inBox p <;> simp

theorem shiftC_xorC (k : Int) (c d : Config) : shiftC k (xorC c d) = xorC (shiftC k c) (shiftC k d) := rfl

/-! ### A two-generation check on a finite piece -/

/-- The symmetric difference of two lists, as a list. -/
def symDiff (A B : List Pt) : List Pt := A.filter (fun p => !B.contains p) ++ B.filter (fun p => !A.contains p)

theorem lcfg_filter (A : List Pt) (f : Pt → Bool) (p : Pt) : lcfg (A.filter f) p = (lcfg A p && f p) := by
  apply Bool.eq_iff_iff.mpr; simp [lcfg_iff, List.mem_filter]

theorem lcfg_symDiff (A B : List Pt) (p : Pt) : lcfg (symDiff A B) p = xor (lcfg A p) (lcfg B p) := by
  rw [symDiff, lcfg_append', lcfg_filter, lcfg_filter]
  show (lcfg A p && !lcfg B p || lcfg B p && !lcfg A p) = _
  cases lcfg A p <;> cases lcfg B p <;> rfl

theorem lcfg_nil' (p : Pt) : lcfg [] p = false := rfl

theorem zero_even : (⟨0, 0, 0⟩ : Pt).even := by
  show (0 : Int) % 2 = 0 ∧ (0 : Int) % 2 = 0 ∧ (0 : Int) % 2 = 0
  decide

theorem unitOf_add_even (p V : Pt) (hV : V.even) : unitOf (p + V) = unitOf p + V.x / 2 := by
  obtain ⟨h, -, -⟩ := hV; simp only [unitOf, Pt.add_x]; omega

/-- The piece of f on the units a .. a + n − 1, exclusive-or σ, after k generations, agrees on the units lo .. hi
with the piece of g exclusive-or σ'; computed in the box after the even translation V. -/
def pieceCheck (f g : Int → List Pt) (a : Int) (n : Nat) (σ σ' : List Pt) (k : Nat) (lo hi : Int) (V : Pt) :
    Bool :=
  ((symDiff (piece f a n) σ).map (· + V)).all inBox && ((symDiff (piece g a n) σ').map (· + V)).all inBox &&
    coreRun (ofList ((symDiff (piece f a n) σ).map (· + V))) k &&
    eqOn (unitMask (lo + V.x / 2) (hi + V.x / 2)) (brun (ofList ((symDiff (piece f a n) σ).map (· + V))) k)
      (ofList ((symDiff (piece g a n) σ').map (· + V)))

theorem pieceCheck_spec {f g : Int → List Pt} (hf : ∀ u, ∀ q ∈ f u, unitOf q = 0)
    (hg : ∀ u, ∀ q ∈ g u, unitOf q = 0) {a : Int} {n : Nat} {σ σ' : List Pt} {k : Nat} {lo hi : Int} {V : Pt}
    (hV : V.even) (h : pieceCheck f g a n σ σ' k lo hi V = true) (hb1 : -8 ≤ lo + V.x / 2)
    (hb2 : hi + V.x / 2 ≤ 23) (hlh : lo ≤ hi + 1) (hlo : a ≤ lo - k) (hhi : hi + k < a + n) (c : Config)
    (hc : ∀ q, lo - k ≤ unitOf q → unitOf q ≤ hi + k → c q = xorC (ucfg f) (lcfg σ) q) :
    ∀ p, lo ≤ unitOf p → unitOf p ≤ hi → run c k p = xorC (ucfg g) (lcfg σ') p := by
  simp only [pieceCheck, Bool.and_eq_true] at h
  obtain ⟨⟨⟨h1, h3⟩, h5⟩, h6⟩ := h
  intro p hp1 hp2
  have core := coreRun_spec _ _ h5
  have hu := unitOf_add_even p V hV
  rw [run_eq_of_units (c' := lcfg (symDiff (piece f a n) σ)) k (fun q q1 q2 => by
      rw [hc q (by omega) (by omega), lcfg_symDiff, xorC, lcfg_piece f hf]
      have : a ≤ unitOf q ∧ unitOf q < a + (n : Int) := by omega
      rw [decide_eq_true this, Bool.true_and]),
    ← run_lcfg_map_add _ hV, ← bcfg_ofList _ h1, run_bcfg_of_core (fun j hj => core j (by omega)),
    eqOn_spec hb1 hb2 (by omega) h6 (p + V) (by omega) (by omega), bcfg_ofList _ h3, lcfg_map_add,
    lcfg_symDiff, lcfg_piece g hg, xorC]
  have : a ≤ unitOf p ∧ unitOf p < a + (n : Int) := by omega
  rw [decide_eq_true this, Bool.true_and]

namespace Signals

/-! ### The train -/

/-- The train at generation t, unit by unit. -/
def trainF (t : Nat) (u : Int) : List Pt := trainBase (t % 4) (u % 2).toNat

/-- **The plain rake train** at generation t: a configuration of the whole lattice, infinite along the wire. -/
def train (t : Nat) : Config := ucfg (trainF t)

theorem trainBase_unit : ∀ t par, ∀ q ∈ trainBase t par, unitOf q = 0 := by
  intro t par
  match t, par with
  | 0, 0 => decide | 0, 1 => decide | 1, 0 => decide | 1, 1 => decide
  | 2, 0 => decide | 2, 1 => decide | 3, 0 => decide | 3, 1 => decide
  | t + 4, _ => simp [trainBase]
  | 0, par + 2 => simp [trainBase] | 1, par + 2 => simp [trainBase]
  | 2, par + 2 => simp [trainBase] | 3, par + 2 => simp [trainBase]

theorem trainF_unit (t : Nat) : ∀ u, ∀ q ∈ trainF t u, unitOf q = 0 := fun _ => trainBase_unit _ _

theorem trainF_per (t : Nat) : ∀ u v, u % 2 = v % 2 → trainF t u = trainF t v := by
  intro u v h; simp only [trainF, h]

theorem train_shift_even (t : Nat) (k : Int) (hk : k % 2 = 0) : shiftC k (train t) = train t :=
  shiftC_ucfg_even _ (trainF_per t) k hk

theorem trainF_mod (t : Nat) : trainF (t % 4) = trainF t := by
  funext u; simp only [trainF, Nat.mod_mod]

/-- One generation of the train, on a piece of three units around unit par. -/
def trainCheck (t par : Nat) : Bool :=
  pieceCheck (trainF t) (trainF (t + 1)) ((par : Int) - 1) 3 [] [] 1 par par ⟨0, 0, 0⟩

theorem trainCheck_ok : ∀ t, t < 4 → ∀ par, par < 2 → trainCheck t par = true := by
  intro t ht par hp
  match t, par with
  | 0, 0 => decide +kernel | 0, 1 => decide +kernel | 1, 0 => decide +kernel | 1, 1 => decide +kernel
  | 2, 0 => decide +kernel | 2, 1 => decide +kernel | 3, 0 => decide +kernel | 3, 1 => decide +kernel

theorem ofList_nil : ofList [] = 0 := rfl

/-- **The train is an orbit** of the whole lattice. -/
theorem train_step (t : Nat) : step (train t) = train (t + 1) := by
  have key : ∀ t, t < 4 → ∀ p, (unitOf p = 0 ∨ unitOf p = 1) → step (train t) p = train (t + 1) p := by
    intro t ht p hp
    have hpar : unitOf p = (((unitOf p).toNat : Nat) : Int) := by omega
    have spec := pieceCheck_spec (trainF_unit t) (trainF_unit (t + 1)) zero_even
      (trainCheck_ok t ht (unitOf p).toNat (by omega)) (by simp; omega) (by simp; omega) (by omega)
      (by omega) (by omega) (train t) (fun q _ _ => by
        simp only [xorC, lcfg_nil', Bool.xor_false]; rfl) p (by omega) (by omega)
    rw [show step (train t) p = run (train t) 1 p from rfl, spec]
    simp only [xorC, lcfg_nil', Bool.xor_false]
    rfl
  have key4 : ∀ p, (unitOf p = 0 ∨ unitOf p = 1) → step (train t) p = train (t + 1) p := by
    intro p hp
    have e1 : train t = train (t % 4) := by simp only [train, trainF_mod]
    have e2 : train (t + 1) = train (t % 4 + 1) := by
      simp only [train]; congr 1; funext u; simp only [trainF]; congr 1; omega
    rw [e1, e2]
    exact key _ (Nat.mod_lt _ (by decide)) p hp
  funext p
  let e := unitOf p - unitOf p % 2
  have he : e % 2 = 0 := by omega
  rw [← train_shift_even t e he, ← train_shift_even (t + 1) e he]
  have := congrFun (run_shiftC e (train t) 1) p
  simp only [run] at this
  rw [this]
  simp only [shiftC]
  exact key4 _ (by simp only [unitOf_shiftPt]; omega)

theorem train_run (t n : Nat) : run (train t) n = train (t + n) := by
  induction n with
  | zero => rfl
  | succ n ih => rw [run, ih, train_step, Nat.add_assoc]

/-- The phases two apart are moved by one unit (four finite equalities). -/
theorem trainBase_two : ∀ t par, t < 4 → par < 2 →
    lcfg (trainBase ((t + 2) % 4) par) = lcfg (trainBase t (1 - par)) := by
  intro t par ht hp
  match t, par with
  | 0, 0 => exact (sameL_iff _ _).mp (by decide) | 0, 1 => exact (sameL_iff _ _).mp (by decide)
  | 1, 0 => exact (sameL_iff _ _).mp (by decide) | 1, 1 => exact (sameL_iff _ _).mp (by decide)
  | 2, 0 => exact (sameL_iff _ _).mp (by decide) | 2, 1 => exact (sameL_iff _ _).mp (by decide)
  | 3, 0 => exact (sameL_iff _ _).mp (by decide) | 3, 1 => exact (sameL_iff _ _).mp (by decide)

/-- **Two generations move the train one unit towards −v.** -/
theorem train_shift (t : Nat) : train (t + 2) = shiftC (-1) (train t) := by
  funext p
  simp only [train, ucfg, shiftC, unitOf_shiftPt, shiftPt_shiftPt, trainF]
  rw [show -(unitOf p + - -1) + - -1 = -unitOf p by omega, show (t + 2) % 4 = (t % 4 + 2) % 4 by omega]
  have := trainBase_two (t % 4) ((unitOf p % 2).toNat) (Nat.mod_lt _ (by decide)) (by omega)
  rw [this, show (unitOf p + - -1) % 2 = ((1 - (unitOf p % 2).toNat : Nat) : Int) by omega, Int.toNat_natCast]

theorem train_one_add (n : Nat) : train (1 + 2 * n) = shiftC (-n) (train 1) := by
  induction n with
  | zero => funext p; simp [shiftC]
  | succ n ih =>
    rw [show 1 + 2 * (n + 1) = (1 + 2 * n) + 2 by omega, train_shift, ih]
    funext p
    simp only [shiftC, shiftPt_shiftPt]
    congr 2
    push_cast; omega

/-! ### The nine signals -/

/-- The cells of signal K with lowest unit u, at train phase 1. -/
def sig (K : Kind) (u : Int) : List Pt := K.cells.map (shiftPt u)

/-- The finite piece of each check: units lo − 2 .. hi + 2 around the signal, compared on lo .. hi. -/
def Kind.lo (K : Kind) : Int := K.par - 2
def Kind.hi (K : Kind) : Int := K.par + 4

/-- The translation into the box for the signal checks. -/
def sigFrame : Pt := ⟨8, 8, 24⟩

theorem sigFrame_even : sigFrame.even := by
  show (8 : Int) % 2 = 0 ∧ (8 : Int) % 2 = 0 ∧ (24 : Int) % 2 = 0
  decide

/-- Two generations of train(1) ⊕ the signal at its base unit, on a finite piece. -/
def sigCheck (K : Kind) : Bool :=
  pieceCheck (trainF 1) (trainF 3) (K.lo - 2) 11 (sig K K.par) (sig K (K.par + K.dir)) 2 K.lo K.hi sigFrame &&
    (sig K K.par).all (fun q => decide (K.lo + 2 ≤ unitOf q ∧ unitOf q ≤ K.hi - 2)) &&
    (sig K (K.par + K.dir)).all (fun q => decide (K.lo ≤ unitOf q ∧ unitOf q ≤ K.hi))

theorem sigCheck_ok (K : Kind) : sigCheck K = true := by
  cases K <;> decide +kernel

theorem lcfg_sig_shift (K : Kind) (u k : Int) : shiftC k (lcfg (sig K u)) = lcfg (sig K (u + k)) := by
  rw [← lcfg_map_shiftPt]
  simp only [sig, List.map_map]
  congr 2
  funext q
  simp only [Function.comp, shiftPt_shiftPt]
  congr 1
  omega

theorem dir_cases (K : Kind) : K.dir = 1 ∨ K.dir = -1 := by cases K <;> simp [Kind.dir]
theorem par_cases (K : Kind) : K.par = 0 ∨ K.par = 1 := by cases K <;> simp [Kind.par]

/-- **One double step of a signal at its base unit.** -/
theorem signal_step_base (K : Kind) :
    run (xorC (train 1) (lcfg (sig K K.par))) 2 = xorC (train 3) (lcfg (sig K (K.par + K.dir))) := by
  have h := sigCheck_ok K
  simp only [sigCheck, Bool.and_eq_true, List.all_eq_true, decide_eq_true_eq] at h
  obtain ⟨⟨hc, hs⟩, hs'⟩ := h
  have hp := par_cases K
  funext p
  by_cases hin : K.lo ≤ unitOf p ∧ unitOf p ≤ K.hi
  · exact pieceCheck_spec (trainF_unit 1) (trainF_unit 3) sigFrame_even hc
      (by simp only [Kind.lo, sigFrame]; omega) (by simp only [Kind.hi, sigFrame]; omega)
      (by simp only [Kind.lo, Kind.hi]; omega) (by simp only [Kind.lo]; omega)
      (by simp only [Kind.lo, Kind.hi]; omega) _ (fun q _ _ => rfl) p hin.1 hin.2
  · -- away from the signal: the train alone
    have away : ∀ q, unitOf p - 2 ≤ unitOf q → unitOf q ≤ unitOf p + 2 →
        xorC (train 1) (lcfg (sig K K.par)) q = train 1 q := by
      intro q q1 q2
      simp only [xorC]
      cases e : lcfg (sig K K.par) q
      · simp
      · have := hs q ((lcfg_iff _ _).mp e); omega
    rw [run_eq_of_units 2 away, train_run]
    simp only [xorC]
    cases e : lcfg (sig K (K.par + K.dir)) p
    · simp
    · have := hs' p ((lcfg_iff _ _).mp e); omega

/-- **One double step of a signal anywhere** (lowest unit u of the kind's parity). -/
theorem signal_step (K : Kind) (u : Int) (hu : u % 2 = K.par % 2) :
    run (xorC (train 1) (lcfg (sig K u))) 2 = xorC (train 3) (lcfg (sig K (u + K.dir))) := by
  let e := u - K.par
  have he : e % 2 = 0 := by omega
  have h1 : xorC (train 1) (lcfg (sig K u)) = shiftC e (xorC (train 1) (lcfg (sig K K.par))) := by
    rw [shiftC_xorC, train_shift_even 1 e he, lcfg_sig_shift]
    congr 3; omega
  have h3 : xorC (train 3) (lcfg (sig K (u + K.dir))) =
      shiftC e (xorC (train 3) (lcfg (sig K (K.par + K.dir)))) := by
    rw [shiftC_xorC, train_shift_even 3 e he, lcfg_sig_shift]
    congr 3; omega
  rw [h1, h3, run_shiftC, signal_step_base]

/-- **Each of the nine signals rides the infinite train for ever, rigidly**: after 2n generations the state is
the train at generation 1 + 2n with the signal moved dir · n units (up the stream for E, U, N1; down for the
others), for every lowest unit u of the kind's parity. -/
theorem signal_run (K : Kind) (u : Int) (hu : u % 2 = K.par % 2) (n : Nat) :
    run (xorC (train 1) (lcfg (sig K u))) (2 * n) = xorC (train (1 + 2 * n)) (lcfg (sig K (u + K.dir * n))) := by
  induction n generalizing u with
  | zero =>
    rw [Nat.mul_zero, Nat.add_zero, show u + K.dir * ((0 : Nat) : Int) = u by omega]
    rfl
  | succ n ih =>
    rw [show 2 * (n + 1) = 2 + 2 * n by omega, run_add, signal_step K u hu]
    -- train 3 ⊕ sig (u + dir) is train 1 ⊕ sig (u + dir + 1), moved one unit back
    have e : xorC (train 3) (lcfg (sig K (u + K.dir))) =
        shiftC (-1) (xorC (train 1) (lcfg (sig K (u + K.dir + 1)))) := by
      rw [shiftC_xorC, ← train_shift, lcfg_sig_shift]
      congr 3; omega
    have hu' : (u + K.dir + 1) % 2 = K.par % 2 := by rcases dir_cases K with h | h <;> omega
    rw [e, run_shiftC, ih _ hu', shiftC_xorC, lcfg_sig_shift, train_one_add,
      show 1 + (2 + 2 * n) = 1 + 2 * (n + 1) by omega, train_one_add]
    congr 1
    · funext p; simp only [shiftC, shiftPt_shiftPt]; congr 2; push_cast; omega
    · congr 2; push_cast; rcases dir_cases K with h | h <;> rw [h] <;> omega

end Signals
end Gump.Tape
