/-
**The call law, part (a), at the interaction set, and the whole call law** (`call_law_a`, `call_law`). At the 44
cells of Z (`Gump/CallUnion.lean`) the union law is checked by the kernel on `Gump.Bits`' box at every generation,
from V_k's state on units 32 .. 39 (or 28 .. 43 at the start) and the line's state on NZ (`Gump/CallLine.lean`):
`LC_spec` turns one Boolean check into the union law at Z. The checks: t ≤ 27 (the standing store, k through
min(k, 4)), t = 28 .. 31 (the start: the birth of e1 at 28 is the one exception to the union law, and it is V_k's
forcing; k through min(k, 8)), t = 32 .. 43 (the words `VW k n`, k through min(k, 8)), t ≥ 44 (all 256 words of
{7, b} on the eight units, with the line at rest: the review's lemma T).
-/
import Gump.CallUnion

namespace Gump.Call
open Gump Gump.Tape Gump.Bits Gump.Unzip

/-! ### One local check -/

/-- The translation of the crossing's neighbourhood into `Gump.Bits`' box. -/
def uF : Pt := ⟨-54, 0, 86⟩

theorem uF_even : uF.even := by
  show (-54 : Int) % 2 = 0 ∧ (0 : Int) % 2 = 0 ∧ (86 : Int) % 2 = 0
  decide

/-- S and T agree on the points of M. -/
def eqL (M : List Pt) (S T : Nat) : Bool := S &&& ofList M == T &&& ofList M

theorem eqL_spec {M : List Pt} (hM : M.all inBox = true) {S T : Nat} (h : eqL M S T = true) :
    ∀ p ∈ M, bcfg S p = bcfg T p := by
  intro p hp
  have hb : inBox p = true := by simp only [List.all_eq_true] at hM; exact hM p hp
  have hm : (ofList M).testBit (idx p) = true := by
    rw [ofList, testBit_foldl]
    simp only [Nat.zero_testBit, Bool.false_or, List.any_eq_true, beq_iff_eq]
    exact ⟨p, hp, rfl⟩
  have e := congrArg (fun n => n.testBit (idx p)) (eq_of_beq h)
  simp only [Nat.testBit_and, hm, Bool.and_true] at e
  simp only [bcfg, hb, Bool.true_and, e]

theorem bcfg_or' (S T : Nat) (p : Pt) : bcfg (S ||| T) p = (bcfg S p || bcfg T p) := by
  simp only [bcfg, Nat.testBit_or]; cases inBox p <;> simp

theorem step_translate (c : Config) (v : Pt) (hv : v.even) (p : Pt) :
    step (fun q => c (q + v)) p = step c (p + v) := congrFun (run_translate c hv 1) p

/-- The union law on Z, as one Boolean. -/
def LC (Vb : Nat) (Ls ex : List Pt) : Bool :=
  inCore (Vb ||| ofList (Ls.map (· + uF))) && inCore Vb && inCore (ofList (Ls.map (· + uF))) &&
    (Ls.map (· + uF)).all inBox && (ex.map (· + uF)).all inBox &&
    eqL (zoneZ.map (· + uF)) (bstep (Vb ||| ofList (Ls.map (· + uF))))
      (bstep Vb ||| bstep (ofList (Ls.map (· + uF))) ||| ofList (ex.map (· + uF)))

theorem zoneZ_box : (zoneZ.map (· + uF)).all inBox = true := by decide +kernel
theorem zoneZ_N : ∀ p ∈ zoneZ, ∀ q ∈ p :: nbrs p, q ∈ zoneNZ := by decide +kernel

/-- **The local check.** -/
theorem LC_spec {Vb : Nat} {Ls ex : List Pt} (h : LC Vb Ls ex = true) (Vc Lc : Config)
    (hV : ∀ q ∈ zoneNZ, bcfg Vb (q + uF) = Vc q) (hL : ∀ q ∈ zoneNZ, lcfg Ls q = Lc q) :
    ∀ p ∈ zoneZ, step (fun q => Vc q || Lc q) p = (step Vc p || step Lc p || lcfg ex p) := by
  simp only [LC, Bool.and_eq_true] at h
  obtain ⟨⟨⟨⟨⟨h1, h2⟩, h3⟩, h4⟩, h5⟩, h6⟩ := h
  intro p hp
  have hN := zoneZ_N p hp
  have lb : ∀ q, bcfg (ofList (Ls.map (· + uF))) (q + uF) = lcfg Ls q := by
    intro q; rw [bcfg_ofList _ h4, lcfg_map_add]
  have e1 : step (fun q => Vc q || Lc q) p = step (fun q => bcfg (Vb ||| ofList (Ls.map (· + uF))) (q + uF)) p :=
    step_congr_N (fun q hq => by rw [bcfg_or', hV q (hN q hq), lb, hL q (hN q hq)])
  have eV : step Vc p = bcfg (bstep Vb) (p + uF) := by
    rw [bstep_spec _ ((inCore_iff _).mp h2), ← step_translate _ _ uF_even]
    exact step_congr_N (fun q hq => (hV q (hN q hq)).symm)
  have eL : step Lc p = bcfg (bstep (ofList (Ls.map (· + uF)))) (p + uF) := by
    rw [bstep_spec _ ((inCore_iff _).mp h3), ← step_translate _ _ uF_even]
    exact step_congr_N (fun q hq => by rw [lb, hL q (hN q hq)])
  rw [e1, step_translate _ _ uF_even, ← bstep_spec _ ((inCore_iff _).mp h1),
    eqL_spec zoneZ_box h6 (p + uF) (List.mem_map.mpr ⟨p, hp, rfl⟩), bcfg_or', bcfg_or', eV, eL,
    bcfg_ofList _ h5, lcfg_map_add]

/-! ### V_k's state as a number -/

/-- Vb holds c on the units a .. b. -/
def RepU (Vb : Nat) (c : Config) (a b : Int) : Prop := ∀ q, a ≤ unitOf q → unitOf q ≤ b → bcfg Vb (q + uF) = c q

/-- Vb holds c on NZ. -/
def RepZ (Vb : Nat) (c : Config) : Prop := ∀ q ∈ zoneNZ, bcfg Vb (q + uF) = c q

theorem unitOf_uF (q : Pt) : unitOf (q + uF) = unitOf q - 27 := by
  simp only [unitOf, uF, Pt.add_x]; omega

/-- A window of a hex word on the units a .. a + n − 1, in the box. -/
def win8 (w : Int → Nat) (a : Int) (n : Nat) : Nat := ofList ((piece (fun u => hexCells (w u)) a n).map (· + uF))

def winOK (w : Int → Nat) (a : Int) (n : Nat) : Bool := ((piece (fun u => hexCells (w u)) a n).map (· + uF)).all inBox

theorem win_rep (w : Int → Nat) (a : Int) (n : Nat) (h : winOK w a n = true) :
    RepU (win8 w a n) (hcfg w) a (a + n - 1) ∧ ∀ q, (unitOf q < a ∨ a + n ≤ unitOf q) → bcfg (win8 w a n) (q + uF) = false := by
  have e : ∀ q, bcfg (win8 w a n) (q + uF) = (decide (a ≤ unitOf q ∧ unitOf q < a + n) && hcfg w q) := by
    intro q
    rw [win8, bcfg_ofList _ h, lcfg_map_add, lcfg_piece _ (fun u => hexCells_unit _)]
    rfl
  refine ⟨fun q h1 h2 => ?_, fun q hq => ?_⟩
  · rw [e]; have : a ≤ unitOf q ∧ unitOf q < a + n := by omega
    rw [decide_eq_true this, Bool.true_and]
  · rw [e]; have : ¬ (a ≤ unitOf q ∧ unitOf q < a + n) := by omega
    rw [decide_eq_false this, Bool.false_and]

theorem NZ_units : ∀ q ∈ zoneNZ, 31 ≤ unitOf q ∧ unitOf q ≤ 38 := by decide +kernel
theorem NZ_tube : ∀ q ∈ zoneNZ, HV q → 33 ≤ unitOf q ∧ unitOf q ≤ 38 := by decide +kernel

theorem repU_repZ {Vb : Nat} {c : Config} {a b : Int} (h : RepU Vb c a b) (ha : a ≤ 31) (hb : 38 ≤ b) : RepZ Vb c :=
  fun q hq => h q (by have := NZ_units q hq; omega) (by have := NZ_units q hq; omega)

/-- An eight-unit window on 32 .. 39 holds c on NZ, if c lies in the tube. -/
theorem win_repZ (w : Int → Nat) (h : winOK w 32 8 = true) (c : Config) (hc : ∀ q, 32 ≤ unitOf q → unitOf q ≤ 39 → hcfg w q = c q)
    (hcV : ∀ q, c q = true → HV q) : RepZ (win8 w 32 8) c := by
  obtain ⟨r1, r2⟩ := win_rep w 32 8 h
  intro q hq
  by_cases hu : 32 ≤ unitOf q
  · have := NZ_units q hq
    rw [r1 q hu (by omega), hc q hu (by omega)]
  · rw [r2 q (Or.inl (by omega))]
    cases e : c q
    · rfl
    · have := NZ_tube q hq (hcV q e); omega

theorem repU_step {Vb : Nat} {c : Config} {a b : Int} (h : RepU Vb c a b) (hc : inCore Vb = true) :
    RepU (bstep Vb) (step c) (a + 1) (b - 1) := by
  intro q h1 h2
  rw [bstep_spec _ ((inCore_iff _).mp hc), ← step_translate _ _ uF_even]
  apply step_eq_of_units
  intro r r1 r2
  exact h r (by omega) (by omega)

theorem repU_e1 {Vb : Nat} {c : Config} {a b : Int} (h : RepU Vb c a b) (he : inBox (e1 + uF) = true) :
    RepU (Vb ||| ofList [e1 + uF]) (fun q => c q || q == e1) a b := by
  intro q h1 h2
  rw [bcfg_or', h q h1 h2, bcfg_ofList _ (by simp [he]), show [e1 + uF] = [e1].map (· + uF) from rfl,
    lcfg_map_add, lcfg_single]

/-- NZ's points outside the tube. -/
def NZout : List Pt := zoneNZ.filter (fun q => !HVb q)

/-- One generation from an eight-unit window, cleared outside the tube on NZ. -/
def oddB (Vb : Nat) : Nat := andNot (bstep Vb) (ofList (NZout.map (· + uF)))

theorem NZout_box : (NZout.map (· + uF)).all inBox = true := by decide +kernel

theorem oddB_rep {Vb : Nat} {c : Config} (h : RepU Vb c 32 39) (hc : inCore Vb = true)
    (hcV : ∀ q, step c q = true → HV q) : RepZ (oddB Vb) (step c) := by
  have hs := repU_step h hc
  intro q hq
  have mem : ∀ q, (bcfg (ofList (NZout.map (· + uF))) (q + uF) = true ↔ q ∈ NZout) := by
    intro q; rw [bcfg_ofList _ NZout_box, lcfg_map_add, lcfg_iff]
  have e : bcfg (oddB Vb) (q + uF) = (bcfg (bstep Vb) (q + uF) && !bcfg (ofList (NZout.map (· + uF))) (q + uF)) := by
    simp only [oddB, bcfg, testBit_andNot]; cases inBox (q + uF) <;> simp
  rw [e]
  by_cases hv : HV q
  · have hout : q ∉ NZout := by simp [NZout, List.mem_filter, HVb, hv]
    have := NZ_tube q hq hv
    have hb : bcfg (ofList (NZout.map (· + uF))) (q + uF) = false := by
      cases e' : bcfg (ofList (NZout.map (· + uF))) (q + uF)
      · rfl
      · exact absurd ((mem q).mp e') hout
    rw [hb, Bool.not_false, Bool.and_true, hs q (by omega) (by omega)]
  · have hin : q ∈ NZout := by simp [NZout, List.mem_filter, HVb, hv, hq]
    rw [(mem q).mpr hin, Bool.not_true, Bool.and_false]
    cases e' : step c q
    · rfl
    · exact absurd (hcV q e') hv

/-! ### The checks -/

/-- The store with the stretch's first unit at 36 (the crossing at 35). -/
def sW (j : Nat) (u : Int) : Nat := storeWord j (u - 36)

def evenOdd (Vb : Nat) (t : Nat) : Bool := LC Vb (lineSnap t) [] && LC (oddB Vb) (lineSnap (t + 1)) []

def checkStore : Bool :=
  (List.range 4).all fun j => winOK (sW (j + 1)) 32 8 && inCore (win8 (sW (j + 1)) 32 8) &&
    (List.range 14).all fun m => evenOdd (win8 (sW (j + 1)) 32 8) (2 * m)

def start4 (V : Nat) : Bool := inCore V && LC V (lineSnap 31) []
def start3 (V : Nat) : Bool := inCore V && LC V (lineSnap 30) [] && start4 (bstep V)
def start2 (V : Nat) : Bool := inCore V && LC V (lineSnap 29) [] && start3 (bstep V)
def start1 (W : Nat) : Bool := inCore W && LC W (lineSnap 28) [e1] && start2 (bstep W ||| ofList [e1 + uF])

def checkStart : Bool :=
  inBox (e1 + uF) && (List.range 8).all fun j => winOK (sW (j + 1)) 28 16 && start1 (win8 (sW (j + 1)) 28 16)

def vwC (j n : Nat) (u : Int) : Nat := VW j n (u - 35)

def checkVW : Bool :=
  (List.range 8).all fun j => (List.range 6).all fun m =>
    winOK (vwC (j + 1) (m + 2)) 32 8 && inCore (win8 (vwC (j + 1) (m + 2)) 32 8) &&
      evenOdd (win8 (vwC (j + 1) (m + 2)) 32 8) (28 + 2 * (m + 2))

def tW (bs : List Bool) (u : Int) : Nat := b2h (bs.getD (u - 32).toNat false)

def checkTape : Bool :=
  (boolLists 8).all fun bs => winOK (tW bs) 32 8 && inCore (win8 (tW bs) 32 8) &&
    LC (win8 (tW bs) 32 8) (lineSnap 42) [] && LC (oddB (win8 (tW bs) 32 8)) (lineSnap 43) []

theorem checkStore_ok : checkStore = true := by decide +kernel
theorem checkStart_ok : checkStart = true := by decide +kernel
theorem checkVW_ok : checkVW = true := by decide +kernel
theorem checkTape_ok : checkTape = true := by decide +kernel

/-! ### V_k generation by generation -/

theorem storeAt_shift (k : Nat) : storeAt k = shiftC 36 (store k) := by
  rw [store, hcfg_shift, storeAt]; rfl

theorem V_store (k : Nat) (hk : 1 ≤ k) (m : Nat) (hm : 2 * m < 29) : V k (2 * m) = storeAt k := by
  simp only [V, hm, ite_true]
  rw [storeAt_shift, run_shiftC, stretch_stands k hk m]

theorem V_succ (k t : Nat) : V k (t + 1) = fun p => step (V k t) p || (decide (t = 28) && p == e1) := by
  funext p
  simp only [V]
  by_cases h1 : t + 1 < 29
  · simp only [h1, show t < 29 by omega, ite_true, show ¬ t = 28 by omega, decide_false, Bool.false_and,
      Bool.or_false]
    rfl
  · by_cases h2 : t = 28
    · subst h2
      simp only [show ¬ (28 + 1 < 29) by decide, show (28 : Nat) < 29 by decide, ite_true, ite_false,
        decide_true, Bool.true_and]
      rfl
    · simp only [h1, show ¬ t < 29 by omega, ite_false, h2, decide_false, Bool.false_and, Bool.or_false]
      rw [show t + 1 - 29 = (t - 29) + 1 by omega]
      rfl

theorem Vf_hex (k n : Nat) : Vf k n = fun u => hexOf (pulses k (3 - (n : Int)) u) := by
  funext u; simp only [Vf, pulses, hexOf]; split <;> simp_all

theorem V_word (k : Nat) (hk : 1 ≤ k) (n : Nat) (hn : 2 ≤ n) :
    V k (28 + 2 * n) = hcfg (fun u => VW k n (u - 35)) := by
  rw [V_eq]
  have h0 : V0 k (28 + 2 * n) = hcfg (VW k n) := by
    by_cases h : n ≤ k + 3
    · exact V0_W k hk n hn h
    · rw [V0_final k hk n (by omega), VW_f (by omega), Vf_hex, tape_eq_hcfg]
  rw [h0, hcfg_shift]; rfl

theorem hcfg_congr_units {w w' : Int → Nat} {q : Pt} (h : w (unitOf q) = w' (unitOf q)) : hcfg w q = hcfg w' q := by
  simp only [hcfg, ucfg, h]

/-! ### The union law at Z, generation by generation -/

theorem storeWord_congr (k j : Nat) (v : Int) (h1 : (0 ≤ v ∧ v < k) ↔ (0 ≤ v ∧ v < j)) (h2 : v = k ↔ v = j) :
    storeWord k v = storeWord j v := by
  simp only [storeWord]
  by_cases c1 : 0 ≤ v ∧ v < k
  · rw [if_pos c1, if_pos (h1.mp c1)]
  · rw [if_neg c1, if_neg (fun h => c1 (h1.mpr h))]
    by_cases c2 : v = k
    · rw [if_pos c2, if_pos (h2.mp c2)]
    · rw [if_neg c2, if_neg (fun h => c2 (h2.mpr h))]

theorem lc_of_store (k : Nat) (hk : 1 ≤ k) (j : Nat) (hj : j = min k 4) :
    ∀ q, 32 ≤ unitOf q → unitOf q ≤ 39 → hcfg (sW j) q = storeAt k q := by
  intro q h1 h2
  apply hcfg_congr_units
  simp only [sW]
  rw [show unitOf q - (cross + 1) = unitOf q - 36 from rfl]
  exact (storeWord_congr k j _ (by omega) (by omega)).symm

theorem lc_of_vw (k n : Nat) (hn : n ≤ 7) (hn2 : 2 ≤ n) (j : Nat) (hj : j = min k 8) :
    ∀ q, 32 ≤ unitOf q → unitOf q ≤ 39 → hcfg (vwC j n) q = hcfg (fun u => VW k n (u - 35)) q := by
  intro q h1 h2
  apply hcfg_congr_units
  simp only [vwC]
  by_cases h8 : k ≤ 8
  · have : j = k := by omega
    rw [this]
  · have : j = 8 := by omega
    rw [this, VW_g (show n ≤ 8 by omega), VW_g (show n ≤ k by omega)]
    simp only [Vg]
    repeat' split
    all_goals omega

theorem vw_tape (k n : Nat) (hk : 1 ≤ k) (hn : 8 ≤ n) (u : Int) (hu : u ≤ 4) : VW k n u = 7 ∨ VW k n u = 11 := by
  simp only [VW]
  split
  · simp only [Vg]; repeat' split
    all_goals omega
  · split
    · simp only [Ve1]; repeat' split
      all_goals omega
    · split
      · simp only [Ve2]; repeat' split
        all_goals omega
      · simp only [Vf]; split <;> omega

theorem b2h_dec {x : Nat} (h : x = 7 ∨ x = 11) : b2h (decide (x = 11)) = x := by
  rcases h with rfl | rfl <;> rfl

theorem L_rep (t : Nat) : ∀ q ∈ zoneNZ, lcfg (lineSnapAt t) q = Lf t q := fun q hq => (Lf_snap t q hq).symm

theorem lineSnapAt_lt {t : Nat} (h : t < 44) : lineSnapAt t = lineSnap t := by simp [lineSnapAt, h]
theorem lineSnapAt_ge {t : Nat} (h : 44 ≤ t) : lineSnapAt t = lineSnap (42 + t % 2) := by
  simp [lineSnapAt, show ¬ t < 44 by omega]

/-- **The union law at the interaction set, at every generation** (with the birth of e1 at generation 28). -/
theorem local_union (k : Nat) (hk : 1 ≤ k) (t : Nat) : ∀ p ∈ zoneZ, step (fun q => V k t q || Lf t q) p =
    (step (V k t) p || step (Lf t) p || lcfg (if t = 28 then [e1] else []) p) := by
  have hcs := checkStore_ok
  have hct := checkStart_ok
  have hcv := checkVW_ok
  have hca := checkTape_ok
  simp only [checkStore, checkStart, checkVW, checkTape, evenOdd, List.all_eq_true, List.mem_range,
    Bool.and_eq_true] at hcs hct hcv hca
  have hV : ∀ s, ∀ q, V k s q = true → HV q := fun s q h => V_HV k s q h
  have hVs : ∀ s, ∀ q, step (V k s) q = true → HV q := by
    intro s q h
    have : V k (s + 1) q = true := by rw [V_succ]; simp [h]
    exact V_HV k _ q this
  by_cases h27 : t ≤ 27
  · -- the standing store
    obtain ⟨⟨w1, w2⟩, w3⟩ := hcs (min k 4 - 1) (by omega)
    rw [show min k 4 - 1 + 1 = min k 4 by omega] at w1 w2 w3
    obtain ⟨m, r, hr, rfl⟩ : ∃ m r, r < 2 ∧ t = 2 * m + r := ⟨t / 2, t % 2, by omega, by omega⟩
    have e := w3 m (by omega)
    have hW := (win_rep _ _ _ w1).1
    have rep : RepU (win8 (sW (min k 4)) 32 8) (V k (2 * m)) 32 39 := by
      intro q h1 h2
      rw [hW q h1 (by omega), lc_of_store k hk _ rfl q h1 h2, V_store k hk m (by omega)]
    rcases (show r = 0 ∨ r = 1 by omega) with rfl | rfl
    · rw [Nat.add_zero, if_neg (by omega)]
      exact LC_spec e.1 _ _ (win_repZ _ w1 _ (fun q h1 h2 => by rw [← rep q h1 h2, hW q h1 (by omega)])
        (hV _)) (by rw [← lineSnapAt_lt (by omega)]; exact L_rep _)
    · rw [if_neg (by omega), V_succ, show (fun p => step (V k (2 * m)) p || (decide (2 * m = 28) && p == e1)) =
        step (V k (2 * m)) by funext p; simp [show ¬ 2 * m = 28 by omega]]
      exact LC_spec e.2 _ _ (oddB_rep rep w2 (hVs _)) (by rw [← lineSnapAt_lt (by omega)]; exact L_rep _)
  · by_cases h31 : t ≤ 31
    · -- the start
      obtain ⟨he, hj⟩ := hct
      obtain ⟨w1, w2⟩ := hj (min k 8 - 1) (by omega)
      rw [show min k 8 - 1 + 1 = min k 8 by omega] at w1 w2
      simp only [start1, start2, start3, start4, Bool.and_eq_true] at w2
      obtain ⟨⟨c28, l28⟩, ⟨⟨c29, l29⟩, ⟨⟨c30, l30⟩, ⟨c31, l31⟩⟩⟩⟩ := w2
      have hW := (win_rep _ _ _ w1).1
      have r28 : RepU (win8 (sW (min k 8)) 28 16) (V k 28) 28 43 := by
        intro q h1 h2
        rw [hW q h1 (by omega), show (28 : Nat) = 2 * 14 from rfl, V_store k hk 14 (by decide)]
        apply hcfg_congr_units; simp only [sW]
        rw [show unitOf q - (cross + 1) = unitOf q - 36 from rfl]
        exact (storeWord_congr k _ _ (by omega) (by omega)).symm
      have r29 := repU_e1 (repU_step r28 c28) he
      have e29 : V k 29 = fun q => step (V k 28) q || q == e1 := by
        rw [show (29 : Nat) = 28 + 1 from rfl, V_succ]; funext q; simp
      have r29' : RepU (bstep (win8 (sW (min k 8)) 28 16) ||| ofList [e1 + uF]) (V k 29) 29 42 := by
        rw [e29]; exact r29
      have r30 := repU_step r29' c29
      have e30 : V k 30 = step (V k 29) := by
        rw [show (30 : Nat) = 29 + 1 from rfl, V_succ]; funext q; simp
      have r30' : RepU (bstep (bstep (win8 (sW (min k 8)) 28 16) ||| ofList [e1 + uF])) (V k 30) 30 41 := by
        rw [e30]; exact r30
      have r31 := repU_step r30' c30
      have e31 : V k 31 = step (V k 30) := by
        rw [show (31 : Nat) = 30 + 1 from rfl, V_succ]; funext q; simp
      have r31' : RepU (bstep (bstep (bstep (win8 (sW (min k 8)) 28 16) ||| ofList [e1 + uF]))) (V k 31) 31 40 := by
        rw [e31]; exact r31
      rcases (show t = 28 ∨ t = 29 ∨ t = 30 ∨ t = 31 by omega) with rfl | rfl | rfl | rfl
      · rw [if_pos rfl]
        exact LC_spec l28 _ _ (repU_repZ r28 (by decide) (by decide)) (by rw [← lineSnapAt_lt (by decide)]; exact L_rep _)
      · rw [if_neg (by decide)]
        exact LC_spec l29 _ _ (repU_repZ r29' (by decide) (by decide)) (by rw [← lineSnapAt_lt (by decide)]; exact L_rep _)
      · rw [if_neg (by decide)]
        exact LC_spec l30 _ _ (repU_repZ r30' (by decide) (by decide)) (by rw [← lineSnapAt_lt (by decide)]; exact L_rep _)
      · rw [if_neg (by decide)]
        exact LC_spec l31 _ _ (repU_repZ r31' (by decide) (by decide)) (by rw [← lineSnapAt_lt (by decide)]; exact L_rep _)
    · rw [if_neg (by omega)]
      obtain ⟨n, r, hr, rfl⟩ : ∃ n r, r < 2 ∧ t = 28 + 2 * n + r := ⟨(t - 28) / 2, (t - 28) % 2, by omega, by omega⟩
      have hodd : ∀ c : Config, r = 1 → V k (28 + 2 * n + r) = step (V k (28 + 2 * n)) := by
        intro _ h; subst h; rw [V_succ]; funext q
        rw [show decide (28 + 2 * n = 28) = false from decide_eq_false (by omega), Bool.false_and, Bool.or_false]
      by_cases h43 : 28 + 2 * n + r ≤ 43
      · -- the words VW k n
        obtain ⟨⟨w1, w2⟩, w3⟩ := hcv (min k 8 - 1) (by omega) (n - 2) (by omega)
        rw [show min k 8 - 1 + 1 = min k 8 by omega, show n - 2 + 2 = n by omega] at w1 w2 w3
        have hW := (win_rep _ _ _ w1).1
        have rep : RepU (win8 (vwC (min k 8) n) 32 8) (V k (28 + 2 * n)) 32 39 := by
          intro q h1 h2
          rw [hW q h1 (by omega), lc_of_vw k n (by omega) (by omega) _ rfl q h1 h2, V_word k hk n (by omega)]
        rcases (show r = 0 ∨ r = 1 by omega) with rfl | rfl
        · rw [Nat.add_zero]
          exact LC_spec w3.1 _ _ (win_repZ _ w1 _ (fun q h1 h2 => by rw [← rep q h1 h2, hW q h1 (by omega)]) (hV _))
            (by rw [← lineSnapAt_lt (by omega)]; exact L_rep _)
        · rw [hodd (fun _ => false) rfl]
          exact LC_spec w3.2 _ _ (oddB_rep rep w2 (hVs _)) (by rw [← lineSnapAt_lt (by omega)]; exact L_rep _)
      · -- every tape word, the line at rest
        let bs : List Bool := (List.range 8).map (fun i : Nat => decide (VW k n ((i : Int) + 32 - 35) = 11))
        have hbs : bs ∈ boolLists 8 := by
          have := mem_boolLists bs; simp only [bs, List.length_map, List.length_range] at this; exact this
        obtain ⟨⟨⟨w1, w2⟩, w3⟩, w4⟩ := hca bs hbs
        have hW := (win_rep _ _ _ w1).1
        have rep : RepU (win8 (tW bs) 32 8) (V k (28 + 2 * n)) 32 39 := by
          intro q h1 h2
          rw [hW q h1 (by omega), V_word k hk n (by omega)]
          apply hcfg_congr_units
          simp only [tW, bs]
          rw [List.getD_eq_getElem?_getD, List.getElem?_map, List.getElem?_range (by omega)]
          simp only [Option.map_some, Option.getD_some]
          rw [show (((unitOf q - 32).toNat : Nat) : Int) + 32 - 35 = unitOf q - 35 by omega]
          exact b2h_dec (vw_tape k n hk (by omega) _ (by omega))
        rcases (show r = 0 ∨ r = 1 by omega) with rfl | rfl
        · rw [Nat.add_zero]
          exact LC_spec w3 _ _ (win_repZ _ w1 _ (fun q h1 h2 => by rw [← rep q h1 h2, hW q h1 (by omega)]) (hV _))
            (by rw [show lineSnap 42 = lineSnapAt (28 + 2 * n) by rw [lineSnapAt_ge (by omega)]; congr 1; omega]
                exact L_rep _)
        · rw [hodd (fun _ => false) rfl]
          exact LC_spec w4 _ _ (oddB_rep rep w2 (hVs _))
            (by rw [show lineSnap 43 = lineSnapAt (28 + 2 * n + 1) by rw [lineSnapAt_ge (by omega)]; congr 1; omega]
                exact L_rep _)

/-! ### The call law -/

theorem e1_zone : e1 ∈ zoneZ := by decide +kernel

/-- **The call law, part (a)**: for every k ≥ 1, at every generation, the store wire, the line and the CALL are
exactly V_k and the free line, side by side. -/
theorem call_law_a (k : Nat) (hk : 1 ≤ k) : ∀ t, run (callStart k) t = fun p => V k t p || Lf t p
  | 0 => by funext p; simp [callStart, V, Lf, run]
  | t + 1 => by
    funext p
    rw [run, call_law_a k hk t, V_succ]
    show step (fun q => V k t q || Lf t q) p = ((step (V k t) p || (decide (t = 28) && p == e1)) || step (Lf t) p)
    by_cases hz : p ∈ zoneZ
    · rw [local_union k hk t p hz]
      by_cases h28 : t = 28
      · subst h28; simp only [ite_true, lcfg_single, decide_true, Bool.true_and]
        cases step (V k 28) p <;> cases step (Lf 28) p <;> simp
      · simp only [h28, ite_false, decide_false, Bool.false_and, Bool.or_false]
        simp [lcfg]
    · have hne : (p == e1) = false := by
        cases e : (p == e1)
        · rfl
        · simp only [beq_iff_eq] at e; subst e; exact absurd e1_zone hz
      rw [hne, Bool.and_false, Bool.or_false]
      by_cases hc : p.isCell = true
      · apply step_or
        by_cases hA : ∃ q ∈ p :: nbrs p, HV q
        · right
          intro q hq
          cases e : Lf t q
          · rfl
          · exact absurd (zone_cover p hc hA ⟨q, hq, Lf_HL t q e⟩) hz
        · left
          intro q hq
          cases e : V k t q
          · rfl
          · exact absurd ⟨q, hq, V_HV k t q e⟩ hA
      · have : ∀ c : Config, step c p = false := fun c => by simp [step, show p.isCell = false by simpa using hc]
        rw [this, this, this]; rfl

/-- **The call law, whole** ( section 3): for every k ≥ 1, (a) at every
generation the state is the disjoint union of V_k and the free line, and (b) from generation 2k + 34 on V_k is plain
wire B carrying exactly k pulses two units apart. -/
theorem call_law : CallLaw := fun k hk =>
  ⟨fun t => ⟨call_law_a k hk t, V_Lf_disjoint k t⟩, call_law_b k hk⟩

end Gump.Call
