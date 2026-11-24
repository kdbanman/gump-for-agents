/-
**The call line's left cap eats every word too** (`research/audit/REVIEW-signals-9.md` section 3, "What is left" (ii):
"whether the third push's reader theorem covers this cap was not checked"). The left cap of push 9's call line
(`call9.json` `capL`, 18 cells on the units 0 .. 3, the store wire from unit 4 on) is not the clock's capL (16 cells),
so section 15's theorem does not cover it; this file proves the same law for it: capL9 and any word over {B, C} on the
units ≥ 4 is, at generation 2n, capL9 and the word moved n units (`reader9_run`). So any train of pulses that reaches
this cap along a bare store wire is swallowed letter by letter, nothing comes back, and the cap is unchanged.

The proof is `ClockReader`'s, written once for any cap on the units −4 .. −1 that passes the 16 zone checks
(`reader_run_gen`), applied to this cap moved four units (`cap9OK_ok`), and moved back.
-/
import Gump.ClockReader
import Gump.CallReaderData

namespace Gump.Reader
open Gump Gump.Tape Gump.Bits Gump.Unzip Gump.Clock

/-- A cap on the units < 0 (given unit by unit) and the word w in hex letters on the units ≥ 0. -/
def RG (capU : Int → List Pt) (w : Int → Letter) (u : Int) : List Pt :=
  if u < 0 then capU u else hexCells (hexOf (w u))

def rgN (capU : Int → List Pt) (σ : List Nat) (v : Int) : List Pt :=
  if v < 0 then capU v else hexCells (σ.getD v.toNat 11)
def rgT (capU : Int → List Pt) (σ : List Nat) (v : Int) : List Pt :=
  if v < 0 then capU v else hexCells (σ.getD (v + 1).toNat 11)

/-- The zone at the cap for the letters σ on the units 0 .. 3. -/
def zoneC (capU : Int → List Pt) (σ : List Nat) : Bool :=
  pieceCheck (rgN capU σ) (rgT capU σ) (-8) 12 [] [] 2 (-6) 1 litFrame

set_option maxHeartbeats 1000000 in
/-- Two generations of a cap that passes the 16 zone checks, on any word: the cap, and the word moved one unit. -/
theorem reader_step_gen (capU : Int → List Pt) (hu : ∀ u, ∀ q ∈ capU u, unitOf q = 0)
    (hnil : ∀ u, u < -4 → capU u = [])
    (hz : ∀ a0 a1 a2 a3 : Bool, zoneC capU [b2h a0, b2h a1, b2h a2, b2h a3] = true) (w : Int → Letter) :
    run (ucfg (RG capU w)) 2 = ucfg (RG capU (fun u => w (u + 1))) := by
  have RG_unit : ∀ w', ∀ u, ∀ q ∈ RG capU w' u, unitOf q = 0 := by
    intro w' u; unfold RG; split; exact hu u; exact hexCells_unit _
  have rgN_unit : ∀ σ, ∀ u, ∀ q ∈ rgN capU σ u, unitOf q = 0 := by
    intro σ u; unfold rgN; split; exact hu u; exact hexCells_unit _
  have rgT_unit : ∀ σ, ∀ u, ∀ q ∈ rgT capU σ u, unitOf q = 0 := by
    intro σ u; unfold rgT; split; exact hu u; exact hexCells_unit _
  funext p
  by_cases hA : unitOf p ≤ -7
  · have off : ∀ (w' : Int → Letter) (q : Pt), unitOf q < -4 → ucfg (RG capU w') q = false := by
      intro w' q hq; simp only [ucfg, RG, if_pos (show unitOf q < 0 by omega), hnil _ hq]; rfl
    rw [run2_empty _ p (fun q _ _ => off w q (by omega)), off _ p (by omega)]
  by_cases hB : unitOf p ≤ 1
  · obtain ⟨b0, e0⟩ := b2h_of (hexOf_cases (w 0))
    obtain ⟨b1, e1⟩ := b2h_of (hexOf_cases (w 1))
    obtain ⟨b2, e2⟩ := b2h_of (hexOf_cases (w 2))
    obtain ⟨b3, e3⟩ := b2h_of (hexOf_cases (w 3))
    have hzz := hz b0 b1 b2 b3
    unfold zoneC at hzz
    refine step_zoneU (RG capU w) (RG capU (fun u => w (u + 1))) 0 (-6) 1 (-8) _ _ (rgN_unit _) (rgT_unit _) 12
      litFrame litFrame_even (by decide) (by decide) hzz (by decide) _ ?_ ?_ (fun _ _ _ => rfl) p (by omega) (by omega)
    · intro v h1 h2
      simp only [RG, rgN, Int.add_zero]
      by_cases hv : v < 0
      · simp only [if_pos hv]
      · simp only [if_neg hv]
        congr 1
        rcases (show v = 0 ∨ v = 1 ∨ v = 2 ∨ v = 3 by omega) with rfl | rfl | rfl | rfl
        · exact e0
        · exact e1
        · exact e2
        · exact e3
    · intro v h1 h2
      simp only [RG, rgT, Int.add_zero]
      by_cases hv : v < 0
      · simp only [if_pos hv]
      · simp only [if_neg hv]
        congr 1
        rcases (show v = 0 ∨ v = 1 by omega) with rfl | rfl
        · exact e1
        · exact e2
  · have h0 : ∀ (w' : Int → Letter) (q : Pt), 0 ≤ unitOf q →
        ucfg (RG capU w') q = hcfg (fun u => hexOf (w' u)) q := by
      intro w' q hq; simp only [ucfg, hcfg, RG, if_neg (show ¬ unitOf q < 0 by omega)]
    rw [h0 _ p (by omega)]
    apply step_left (fun u => hexOf (w u)) (fun u => hexOf (w (u + 1))) _ p
    · intro i _ _; exact hexOf_cases _
    · rfl
    · intro q h1 _; exact h0 w q (by omega)

theorem reader_run_gen (capU : Int → List Pt) (hu : ∀ u, ∀ q ∈ capU u, unitOf q = 0)
    (hnil : ∀ u, u < -4 → capU u = [])
    (hz : ∀ a0 a1 a2 a3 : Bool, zoneC capU [b2h a0, b2h a1, b2h a2, b2h a3] = true) (w : Int → Letter) :
    ∀ n : Nat, run (ucfg (RG capU w)) (2 * n) = ucfg (RG capU (fun u => w (u + n)))
  | 0 => by
    show ucfg (RG capU w) = _
    rw [show (fun u => w (u + ((0 : Nat) : Int))) = w from funext fun u => by congr 1; omega]
  | n + 1 => by
    rw [show 2 * (n + 1) = 2 * n + 2 by omega, run_add, reader_run_gen capU hu hnil hz w n,
      reader_step_gen capU hu hnil hz]
    congr 2; funext u
    show w (u + 1 + (n : Int)) = w (u + ((n + 1 : Nat) : Int))
    congr 1; push_cast; omega

/-! ### The call line's left cap -/

theorem cap9U_unit : ∀ u, ∀ q ∈ cap9U u, unitOf q = 0 := by intro u; unfold cap9U; split <;> decide
theorem cap9U_nil {u : Int} (h : u < -4 ∨ -1 < u) : cap9U u = [] := by unfold cap9U; split <;> first | rfl | omega

theorem cap9OK_ok (a0 a1 a2 a3 : Bool) : zoneC cap9U [b2h a0, b2h a1, b2h a2, b2h a3] = true := by
  cases a0 <;> cases a1 <;> cases a2 <;> cases a3 <;> decide +kernel

/-- call9's capL is its four units, the unit 4 + u holding `cap9U u` (u = −4 .. −1). -/
theorem capL9_ucfg : lcfg capL9 = ucfg (fun u => cap9U (u - 4)) := by
  have h1 : ∀ q ∈ capL9, shiftPt (-unitOf q) q ∈ cap9U (unitOf q - 4) := by decide +kernel
  have h2 : ∀ u : Int, 0 ≤ u → u ≤ 3 → ∀ c ∈ cap9U (u - 4), shiftPt u c ∈ capL9 := by
    intro u a b
    rcases (show u = 0 ∨ u = 1 ∨ u = 2 ∨ u = 3 by omega) with rfl | rfl | rfl | rfl <;> decide +kernel
  funext p
  apply Bool.eq_iff_iff.mpr
  simp only [ucfg, lcfg_iff]
  constructor
  · exact h1 p
  · intro h
    by_cases hu : 0 ≤ unitOf p ∧ unitOf p ≤ 3
    · have := h2 _ hu.1 hu.2 _ h; rwa [shiftPt_shiftPt_neg] at this
    · rw [cap9U_nil (by omega)] at h; simp at h

/-- capL9 on the units < 4, the tape of w on the units ≥ 4 (call9's coordinates). -/
def readerCall (w : Int → Letter) : Config := fun p => if unitOf p < 4 then lcfg capL9 p else tape w p

theorem readerCall_eq (w : Int → Letter) :
    readerCall w = shiftC 4 (ucfg (RG cap9U (fun u => w (u + 4)))) := by
  funext p
  simp only [readerCall, shiftC, capL9_ucfg, tape_eq_hcfg]
  rw [ucfg_shift]
  by_cases h : unitOf p < 4
  · rw [if_pos h]; simp only [ucfg, RG, if_pos (show unitOf p - 4 < 0 by omega)]
  · rw [if_neg h]; simp only [hcfg, ucfg, RG, if_neg (show ¬ unitOf p - 4 < 0 by omega),
      show unitOf p - 4 + 4 = unitOf p by omega]

/-- **The call line's left cap eats every word and remembers nothing**: at generation 2n the state is capL9 and the
word moved n units. -/
theorem reader9_run (w : Int → Letter) (n : Nat) : run (readerCall w) (2 * n) = readerCall (fun u => w (u + n)) := by
  rw [readerCall_eq, run_shiftC, reader_run_gen cap9U cap9U_unit (fun u hu => cap9U_nil (Or.inl hu)) cap9OK_ok,
    readerCall_eq]
  congr 3; funext u
  show w (u + (n : Int) + 4) = w (u + 4 + n)
  congr 1; omega

end Gump.Reader
