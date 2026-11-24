/-
**The beam for every N** (`research/signals/README.md` section 21, "The beam has period exactly 4 for every N ≥ 1";
the base facts of `research/signals/prove_beam.py`). The beam of N units (`objects/beam-5f.json`) is the mirror-image
gun (left, units −3 .. −1), N units of rake train (b0 on the even, b1 on the odd units 0 .. N − 1) and the SAT
absorber (R_even or R_odd by the parity of N, moved N units): a finite configuration of the whole lattice, given
here unit by unit (`beamU`, from `tape_beam.py`, which checks that it reassembles to the catalogue's Object(N)).

`beam_period`: for every N ≥ 1 the beam is an oscillator of exact period 4.

The proof is the source's induction from N to N + 2 with the gluing made a theorem (`Gump.Tape.glue_run`): `S N`
says period 4, not period 2, and that on the units 4, 5 the orbit is its own move by two units at every
generation. Then the orbit on the units ≤ 4 glued to its move by two units on the units ≥ 5 is an orbit whose start
is the beam of N + 2 units (`glue_beam`), so it is that beam's orbit, and `S (N + 2)` follows (`S_step`). The bases
S 8, S 9 and the cases N = 1 .. 9 are kernel runs on the bit-parallel stepper (`decide +kernel`), also checked on
`reference/oracle.py` by `tape_beam.py`.
-/
import Gump.LineBeamData
import Gump.TapeSignals

namespace Gump.Beam
open Gump Gump.Tape Gump.Bits

/-- The absorber for the parity of N. -/
def RU (N : Nat) : Int → List Pt := if N % 2 = 0 then evenU else oddU

/-- The beam of N units, unit by unit (each unit moved to unit 0). -/
def beamU (N : Nat) (u : Int) : List Pt :=
  if u < 0 then leftU u else if u < N then (if u % 2 = 0 then b0 else b1) else RU N (u - N)

/-- **The beam of N units**, a finite configuration of the whole lattice. -/
def beam (N : Nat) : Config := ucfg (beamU N)

theorem leftU_unit : ∀ u, ∀ q ∈ leftU u, unitOf q = 0 := by intro u; unfold leftU; split <;> decide
theorem evenU_unit : ∀ u, ∀ q ∈ evenU u, unitOf q = 0 := by intro u; unfold evenU; split <;> decide
theorem oddU_unit : ∀ u, ∀ q ∈ oddU u, unitOf q = 0 := by intro u; unfold oddU; split <;> decide
theorem RU_unit (N : Nat) : ∀ u, ∀ q ∈ RU N u, unitOf q = 0 := by
  intro u; unfold RU; split; exact evenU_unit u; exact oddU_unit u

theorem beamU_unit (N : Nat) : ∀ u, ∀ q ∈ beamU N u, unitOf q = 0 := by
  intro u; unfold beamU; split
  · exact leftU_unit u
  · split
    · split
      · exact (by decide : ∀ q ∈ b0, unitOf q = 0)
      · exact (by decide : ∀ q ∈ b1, unitOf q = 0)
    · exact RU_unit N _

theorem leftU_nil {u : Int} (h : u < -3 ∨ 0 ≤ u) : leftU u = [] := by unfold leftU; split <;> first | rfl | omega
theorem RU_nil (N : Nat) {v : Int} (h : v < 0 ∨ 2 < v) : RU N v = [] := by
  unfold RU; split
  · unfold evenU; split <;> first | rfl | omega
  · unfold oddU; split <;> first | rfl | omega

theorem RU_two (N : Nat) : RU (N + 2) = RU N := by
  unfold RU; rw [show (N + 2) % 2 = N % 2 by omega]

/-! ### The gluing step -/

/-- The beam on the units ≤ 4 and the beam moved two units on the units ≥ 5 is the beam of N + 2 units. -/
theorem glue_beam (N : Nat) (hN : 5 ≤ N) : glue 4 (beam N) (shiftC 2 (beam N)) = beam (N + 2) := by
  funext p
  simp only [glue, beam, shiftC, ucfg, unitOf_shiftPt, shiftPt_shiftPt]
  by_cases h : unitOf p ≤ 4
  · rw [if_pos h]
    congr 1
    simp only [beamU]
    by_cases h0 : unitOf p < 0
    · simp only [if_pos h0]
    · simp only [if_neg h0, if_pos (show unitOf p < (N : Int) by omega),
        if_pos (show unitOf p < ((N + 2 : Nat) : Int) by push_cast; omega)]
  · rw [if_neg h, show -(unitOf p + -2) + -2 = -unitOf p by omega]
    congr 1
    simp only [beamU, if_neg (show ¬ unitOf p + -2 < 0 by omega), if_neg (show ¬ unitOf p < 0 by omega)]
    by_cases h1 : unitOf p < ((N + 2 : Nat) : Int)
    · rw [if_pos (show unitOf p + -2 < (N : Int) by push_cast at h1; omega), if_pos h1,
        show (unitOf p + -2) % 2 = unitOf p % 2 by omega]
    · rw [if_neg (show ¬ unitOf p + -2 < (N : Int) by push_cast at h1; omega), if_neg h1, RU_two,
        show unitOf p + -2 - (N : Int) = unitOf p - ((N + 2 : Nat) : Int) by push_cast; omega]

/-- **The statement of the induction**: period 4, not period 2, and on the units 4, 5 the orbit is its own move by
two units at every generation. -/
def S (N : Nat) : Prop :=
  run (beam N) 4 = beam N ∧ run (beam N) 2 ≠ beam N ∧
    ∀ t q, 4 ≤ unitOf q → unitOf q ≤ 5 → run (beam N) t q = run (beam N) t (shiftPt (-2) q)

theorem S_step (N : Nat) (hN : 5 ≤ N) (h : S N) : S (N + 2) := by
  obtain ⟨h4, h2, hs⟩ := h
  have hg : ∀ t, run (beam (N + 2)) t = glue 4 (run (beam N) t) (shiftC 2 (run (beam N) t)) := by
    intro t
    rw [← glue_beam N hN]
    exact glue_run 4 (fun t => run (beam N) t) (fun t => shiftC 2 (run (beam N) t)) (fun _ _ _ => rfl)
      (fun t p _ => by
        show step (shiftC 2 (run (beam N) t)) p = shiftC 2 (run (beam N) (t + 1)) p
        rw [← run_shiftC, ← run_shiftC]; rfl)
      (fun t p h1 h2 => hs t p h1 h2) t
  refine ⟨?_, ?_, ?_⟩
  · rw [hg, h4, glue_beam N hN]
  · intro e
    apply h2
    rw [hg, ← glue_beam N hN] at e
    funext p
    by_cases hp : unitOf p ≤ 4
    · have := congrFun e p
      simp only [glue, if_pos hp] at this
      exact this
    · have := congrFun e (shiftPt 2 p)
      simp only [glue, unitOf_shiftPt, if_neg (show ¬ unitOf p + 2 ≤ 4 by omega), shiftC, shiftPt_shiftPt,
        show (-2 : Int) + 2 = 0 from rfl, shiftPt_zero] at this
      exact this
  · intro t q h1 h2
    rw [hg]
    simp only [glue, unitOf_shiftPt]
    by_cases hq : unitOf q ≤ 4
    · rw [if_pos hq, if_pos (show unitOf q + -2 ≤ 4 by omega)]
      exact hs t q h1 h2
    · rw [if_neg hq, if_pos (show unitOf q + -2 ≤ 4 by omega)]
      rfl

/-! ### The base, by the kernel -/

/-- The translation into the box (units move by 4). -/
def bframe : Pt := ⟨8, 8, 24⟩
def bunframe : Pt := ⟨-bframe.x, -bframe.y, -bframe.z⟩

theorem bframe_even : bframe.even := by
  show (8 : Int) % 2 = 0 ∧ (8 : Int) % 2 = 0 ∧ (24 : Int) % 2 = 0
  decide

theorem bunframe_bframe (p : Pt) : p + bunframe + bframe = p := Tape.Pt.add_add_neg p bframe

/-- The beam of N units as a list. -/
def beamList (N : Nat) : List Pt := piece (beamU N) (-3) (N + 6)

theorem beam_eq (N : Nat) : beam N = lcfg (beamList N) := by
  funext q
  rw [beamList, lcfg_piece _ (beamU_unit N)]
  by_cases h : -3 ≤ unitOf q ∧ unitOf q < -3 + ((N + 6 : Nat) : Int)
  · rw [decide_eq_true h, Bool.true_and]; rfl
  · rw [decide_eq_false h, Bool.false_and]
    simp only [beam, ucfg, beamU]
    by_cases h0 : unitOf q < 0
    · rw [if_pos h0, leftU_nil (by omega)]; rfl
    · rw [if_neg h0, if_neg (show ¬ unitOf q < (N : Int) by push_cast at h; omega), RU_nil N (by push_cast at h; omega)]
      rfl

def boxed (N : Nat) : Nat := ofList ((beamList N).map (· + bframe))
def boxedS (N : Nat) : Nat := ofList (((beamList N).map (shiftPt 2)).map (· + bframe))

/-- Period 4 and not 2, in the box. -/
def directCheck (N : Nat) : Bool :=
  ((beamList N).map (· + bframe)).all inBox && coreRun (boxed N) 4 && brun (boxed N) 4 == boxed N &&
    brun (boxed N) 2 != boxed N

/-- The seam: on the units 4, 5 the beam's run is its move by two units, generations 0 .. 3. -/
def seamCheck (N : Nat) : Bool :=
  (((beamList N).map (shiftPt 2)).map (· + bframe)).all inBox && agree (unitMask 8 9) 3 (boxedS N) (boxed N)

def baseOK : Bool := (List.range 9).all (fun i => directCheck (i + 1)) && seamCheck 8 && seamCheck 9

theorem baseOK_ok : baseOK = true := by decide +kernel

theorem run_box (L : List Pt) (hb : (L.map (· + bframe)).all inBox = true) (n : Nat)
    (hc : ∀ j, j < n → inCore (brun (ofList (L.map (· + bframe))) j) = true) (q : Pt) :
    run (lcfg L) n q = bcfg (brun (ofList (L.map (· + bframe))) n) (q + bframe) := by
  rw [← run_lcfg_map_add L bframe_even n q, ← bcfg_ofList _ hb, run_bcfg_of_core hc]

theorem direct_facts (N : Nat) (h : directCheck N = true) : run (beam N) 4 = beam N ∧ run (beam N) 2 ≠ beam N := by
  simp only [directCheck, Bool.and_eq_true, bne_iff_ne, ne_eq] at h
  obtain ⟨⟨⟨hb, hc⟩, h4⟩, h2⟩ := h
  have core := coreRun_spec _ _ hc
  have h4' : brun (boxed N) 4 = boxed N := eq_of_beq h4
  rw [beam_eq]
  refine ⟨?_, fun e => h2 ?_⟩
  · funext q
    rw [run_box _ hb 4 (fun j hj => core j (by omega)), show ofList ((beamList N).map (· + bframe)) = boxed N from rfl,
      h4', boxed, bcfg_ofList _ hb, lcfg_map_add]
  · apply bcfg_inj ((inCore_iff _).mp (core 2 (by omega))) ((inCore_iff _).mp (core 0 (by omega)))
    funext p
    have := congrFun e (p + bunframe)
    rw [run_box _ hb 2 (fun j hj => core j (by omega)), bunframe_bframe] at this
    show bcfg (brun (ofList ((beamList N).map (· + bframe))) 2) p = bcfg (ofList ((beamList N).map (· + bframe))) p
    have e2 := lcfg_map_add bframe (beamList N) (p + bunframe)
    rw [bunframe_bframe] at e2
    rw [this, bcfg_ofList _ hb, e2]

theorem run_four (N : Nat) (h4 : run (beam N) 4 = beam N) : ∀ t, run (beam N) t = run (beam N) (t % 4) := by
  have hm : ∀ n, run (beam N) (4 * n) = beam N := by
    intro n; induction n with
    | zero => rfl
    | succ n ih => rw [Nat.mul_succ, run_add, ih, h4]
  intro t
  have e : run (beam N) t = run (beam N) (4 * (t / 4) + t % 4) := congrArg (run (beam N)) (Nat.div_add_mod t 4).symm
  rw [e, run_add, hm]

theorem seam_facts (N : Nat) (hd : directCheck N = true) (h : seamCheck N = true) : S N := by
  obtain ⟨h4, h2⟩ := direct_facts N hd
  refine ⟨h4, h2, ?_⟩
  simp only [seamCheck, Bool.and_eq_true] at h
  obtain ⟨hbS, hag⟩ := h
  simp only [directCheck, Bool.and_eq_true] at hd
  have hb := hd.1.1.1
  have ag := agree_spec _ 3 _ _ hag
  intro t q h1 h2
  rw [run_four N h4 t]
  have ht : t % 4 ≤ 3 := by omega
  obtain ⟨cS, cB, e⟩ := ag (t % 4) ht
  have e' := eqOn_spec (by decide) (by decide) (by decide) e (q + bframe)
    (by rw [unitOf_add_even _ _ bframe_even]; simp only [bframe]; omega)
    (by rw [unitOf_add_even _ _ bframe_even]; simp only [bframe]; omega)
  have shifted : run (beam N) (t % 4) (shiftPt (-2) q) = run (lcfg ((beamList N).map (shiftPt 2))) (t % 4) q := by
    rw [lcfg_map_shiftPt, run_shiftC, ← beam_eq]; rfl
  rw [shifted, beam_eq, run_box _ hb _ (fun j hj => (ag j (by omega)).2.1),
    run_box _ hbS _ (fun j hj => (ag j (by omega)).1)]
  exact e'.symm

/-! ### Every N -/

theorem S_all : ∀ k, S (8 + k) := by
  have hz := baseOK_ok
  simp only [baseOK, Bool.and_eq_true, List.all_eq_true, List.mem_range] at hz
  obtain ⟨⟨hd, s8⟩, s9⟩ := hz
  have b8 := seam_facts 8 (hd 7 (by decide)) s8
  have b9 := seam_facts 9 (hd 8 (by decide)) s9
  intro k
  induction k using Nat.strongRecOn with
  | _ k ih =>
    match k with
    | 0 => exact b8
    | 1 => exact b9
    | k + 2 => exact S_step (8 + k) (by omega) (ih k (by omega))

/-- **The beam has period exactly 4 for every N ≥ 1** (section 21): it returns after 4 generations and after no
fewer. -/
theorem beam_period (N : Nat) (hN : 1 ≤ N) :
    run (beam N) 4 = beam N ∧ ∀ k, 0 < k → k < 4 → run (beam N) k ≠ beam N := by
  have h42 : run (beam N) 4 = beam N ∧ run (beam N) 2 ≠ beam N := by
    by_cases h9 : N ≤ 9
    · have hz := baseOK_ok
      simp only [baseOK, Bool.and_eq_true, List.all_eq_true, List.mem_range] at hz
      have := hz.1.1 (N - 1) (by omega)
      rw [show N - 1 + 1 = N by omega] at this
      exact direct_facts N this
    · have := S_all (N - 8)
      rw [show 8 + (N - 8) = N by omega] at this
      exact ⟨this.1, this.2.1⟩
  obtain ⟨h4, h2⟩ := h42
  refine ⟨h4, fun k hk0 hk4 e => ?_⟩
  have one : run (beam N) 1 ≠ beam N := by
    intro e1; apply h2; rw [show 2 = 1 + 1 from rfl, run_add, e1, e1]
  rcases (show k = 1 ∨ k = 2 ∨ k = 3 by omega) with rfl | rfl | rfl
  · exact one e
  · exact h2 e
  · apply one
    have : run (beam N) (3 + 1) = run (beam N) 1 := by rw [run_add, e]
    rw [← this]; exact h4

end Gump.Beam
