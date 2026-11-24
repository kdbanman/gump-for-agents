# The link: the chain theorems for the dice agent's `Face.P`

Agent `chain`, 2026-11-24, 13:58 UTC onwards, on the PI's second message. Files (all new): `mathlib/GumpMath/Link*.lean`
(Bridge, Unique, Sym, Faces, NoCert, Torus202, and per face `Link<Face>.lean`, `Link<Face>Sym.lean` for Hull3,
Torus103, Torus113, Strip13, Patch13), `mathlib/AxiomsLink.lean`, `statements_link.json`, this note. Imported from the dice agent (its
finished modules, read-only): `DiceDef`, `DiceLife`, `DiceCert`, `DiceBound`, `DiceBound2`, `DiceSym`, and the five certified
9-cell face files `DiceHull3`, `DiceTorus103`, `DiceTorus113`, `DiceStrip13`, `DicePatch13` (with their `*Data`).
Kernel tier only: every check is `decide +kernel`; no `native_decide`, no `sorry`; `#print axioms` gives the standard
three for every theorem in `AxiomsLink.lean`.

## The headline (one theorem per face; `GumpMath/LinkFaces.lean`)

For F = `hull 3` (and likewise `torus 1 0 3`, `torus 1 1 3`, `strip 1 3`, `patch 1 3` with their numbers):

```lean
theorem hull3_full :
    ∃ μ lam, (chain (hull 3) sdens.dens).IsDominantQSD μ lam ∧ IsQSD (hull 3) ρ1 ρ2 (extend (hull 3) μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (hull 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (0.9165673655948901373 : ℝ) ≤ lam ∧ lam ≤ 0.9165673655948901374 ∧
      2.4837157463 < Real.log ((chain (hull 3) sdens.dens).lifetime μ) ∧
      Real.log ((chain (hull 3) sdens.dens).lifetime μ) < 2.4837157464 ∧
      (∀ i x, L.dc i x = 1 - (((hull 3).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (hull 3) sdens.dens).lifetime μ) = ∑ i, L.price μ i ∧
      (∀ i j : Fin (hull 3).A, cls.getD i 0 = cls.getD j 0 → L.price μ i = L.price μ j) ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (hull 3) sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (hull 3) sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (hull 3) sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t))
```

Read: `chain F hd` is the killed chain of `Face.P` itself (`ofStochastic` of `(F.P ρ1 ρ2 : ℝ)` at `F.empty`); its
dominant quasi-stationary law μ (λ maximal among all QSDs, λ ≥ Q u u, the decay rate of the longest-lived start) is
the dice agent's `IsQSD` (extended by 0 at the empty face), has λ > 0, charges every living state, and is the only
QSD with λ > 0; λ lies in the dice agent's certified interval and ln τ (τ = E_μ T = ∑_t P_μ(T > t)) to ten digits;
L is the local factorisation by each cell's own death probability 1 − F.a x i, and ln τ = ∑_i c_i (the tilt
identity) with c_i equal within each class of the face's table symmetries; and from every state that can survive,
P_x(T > t) is between (m/M) λ^t and (M/m) λ^(t−1).

| face (A) | λ ∈ | ln τ ∈ | living states (die surely) | u | classes of equal price (automorphisms) |
|---|---|---|---|---|---|
| hull 3 (9) | [0.9165673655948901373, …374] | (2.4837157463, 2.4837157464) | 511 (none) | 207 | corners {0,3,8}; the other six (12) |
| torus (1,0),(0,3) (9) | [0.9664099275695942426, …427] | (3.3935247190, 3.3935247191) | 510 (the full face) | 10 | {0,1,3,4,6,7}, {2,5,8} (12) |
| torus (1,1),(0,3) (9) | [0.9324323935928482210, …211] | (2.6946266059, 2.6946266060) | 510 (the full face) | 3 | all nine (1296) |
| strip 1×3 (9) | [0.9391216736592712685, …686] | (2.7988780569, 2.7988780570) | 511 (none) | 14 | {0,2,3,5,6,8}, {1,4,7} (6) |
| patch 1×3 (9) | [0.8474738060566295030, …031] | (1.8804189341, 1.8804189342) | 511 (none) | 73 | {0,8}, {1,7}, {2,6}, {3,5}, {4} (2) |

**The 12-cell torus (2,0),(0,2)** (`LinkTorus202.lean`, `torus202_full`): the dice agent's certificate for it was not
built, so there is no certified λ interval; proved for `Face.P`: the dominant QSD is unique among λ > 0 and positive
on every living state (4,094 living states can survive, the full face dies surely; u = 7, every state within two
steps); all twelve prices are equal (3 of the 48 table automorphisms, acting transitively), so ln τ = 12·c exactly;
ln τ < 1.9228·12 (the dice agent's `lntau_le_regular` with its `regular_torus202`); and the decay rate from every
start. The tables are mine (`Torus202.data`), checked by the kernel against `Face.nb`, `Face.m1/m2` and `aliveNum`
(`Torus202.tab`); the reachability certificate is two trees of depth 12; the file takes 3–4.5 minutes to build.

The torus (1,0),(0,3) has two price classes, as the referee measured (c_X = c_Y = 0.37976, c_Z = 0.37166): its
lattice is not rotation-invariant. The torus (1,1),(0,3) has one (0.29940 each).

## What each piece proves

- `LinkBridge.lean`: `aliveProb_cast`, **`P_cast`** ((F.P ρ1 ρ2 x y : ℝ) = bitP F.A (aR F ρ1 ρ2) x y, every face, all
  ρ); `aliveProb_mem` (0 ≤ aliveProb ≤ 1 for ρ ∈ [0,1], any coins, by the binomial theorem); `chain`; `toDice`,
  `ofDice` (the two notions of QSD agree); `localDeath` (cell i's factor 1 − F.a x i, with (K) from the coins);
  **`face_theorems`** (Theorems 1 and 2 for `Face.P`: dominant QSD, ln τ = ∑ c_i with the named factors,
  ln τ ≤ ε_max·A, τ ≥ 1/(1 − Q u u)) for every face satisfying `CellsOK` (coins (2,1), or (2,0) with at most two
  neighbours — every face of `geom.py`), and `face_theorems_allcoins` for every face with all its coins.
- `LinkUnique.lean`: `aliveProbR_pos_iff` (a cell can be alive next iff some coin outcome puts k + heads in the
  window), `Q_pos_iff` (the support of `Face.P` decided on the dice agent's checked tables), `face_class` (Lemma 0
  from a certificate: u with every cell alive-able, and for every state that can survive a possible next state
  closer to u, checked by `uOK`/`reachOK`), `one_class'` (with irreducibility exported), **`face_lifetime`** (the
  assembly; it uses `decay_bounds` for the rate and the dice agent's λ interval as a hypothesis).
- `LinkSym.lean`: **`price_sym`** (a permutation preserving the tables, `Data.symOK`, preserves the chain and the
  local factors, so c_{σi} = c_i, through the chain arm's `price_invariant` and the dice agent's `P_sym`,
  `alpha_sym`, `act_bij`).
- `Link<Face>.lean` (generated by the chain agent's script from the dice tables): the certificate (u, nxt, dist),
  checks `cells`, `uok`, `reach` by `decide +kernel` (65–95 s per face), and `<face>_link`.
  `Link<Face>Sym.lean`: the automorphisms used (σ_k with `symOK` by `decide +kernel`), `<face>_prices`.
  `LinkFaces.lean`: `<face>_full`, the conjunction.

## Exactly which sentence is proved for which face, and what is hypothesis

- Proved for **every** `Gump.Dice.Face` (all ρ): `P_cast`, `aliveProb_mem`, `toDice`, `ofDice`.
- Proved for every face with `CellsOK` (and 0 < ρ1, ρ2 < 1; for all faces with all coins via `coins_of_all`):
  existence of the dominant QSD, the tilt identity with named per-cell factors, Theorem 1 (ε_max·A), τ ≥ 1/(1−Q u u).
  `CellsOK` for hull faces of every size is not proved (per face it is `cellsD` by the kernel).
- Proved for the five certified 9-cell faces: everything in `<face>_full`. Nothing is hypothesis there: the λ interval
  is the dice agent's theorem (`hull3_tau` etc., every QSD, with λ > 0 on the tori), uniqueness is from the
  kernel-checked certificate, the symmetry classes from kernel-checked table automorphisms.
- Proved for the 12-cell torus (2,0),(0,2): everything in `torus202_full` (no λ interval: not certified by anyone in
  Lean).
- **Not proved**: a certified λ (hence ln τ to digits) for the 12-cell torus; Lemma 0 for `Face.P` on every wrapped face (my `wrapped_lemma0` is on the
  kagome model; the bijection between the dice agent's `torus H K D` cell lists and `Orient × Torus H K D` carrying
  `Face.nb` to `nbrs` is not done), hence `kagome_sharp_bound` is not yet a theorem about `Face.P`; Lemma 0 on every
  hull triangle or strip by a general argument (only per face). The survival in the decay clause is the killed
  chain's `survFrom` (∑ over living y of (Q^t)(x, y)); that it equals the dice agent's `Face.survival` (through
  (P^t) and the absorbing empty state) is not stated here (the dice agent's own `<face>_lifetime` bounds
  `Face.survival` directly).

## Reproduce

    cd research/blast/lean/mathlib
    lake build GumpMath.LinkBridge GumpMath.LinkUnique GumpMath.LinkSym     # quick
    for f in Hull3 Torus103 Torus113 Strip13 Patch13; do lake build GumpMath.Link$f GumpMath.Link${f}Sym; done
    lake build GumpMath.LinkFaces && lake env lean AxiomsLink.lean          # one at a time: ~1-1.5 min per face file
    lake build GumpMath.LinkNoCert GumpMath.LinkTorus202                    # the 12-cell torus: 3-4.5 min

The generators (committed; each regenerates its modules **byte for byte**, checked with `LINK_OUT=<dir>` and `cmp`
against the committed files at 9fde4a9; set `LINK_OUT` to write elsewhere, the default is `mathlib/GumpMath/`):
- `link_reach.py` — writes nothing; the reachability certificate (u, nxt, dist) from the dice tables, imported by the
  generators; `python3 research/blast/lean/link_reach.py DiceHull3 DiceTorus103 …` prints u and the distances.
- `link_gen_faces.py` — writes `LinkHull3.lean`, `LinkTorus103.lean`, `LinkTorus113.lean`, `LinkStrip13.lean`,
  `LinkPatch13.lean`: `python3 research/blast/lean/link_gen_faces.py`.
- `link_gen_sym.py` — writes the five `Link<Face>Sym.lean`: `python3 research/blast/lean/link_gen_sym.py`.
- `link_gen_full.py` — writes `LinkFaces.lean`: `python3 research/blast/lean/link_gen_full.py`.
- `link_torus202.py` — writes `LinkTorus202.lean` (tables, trees, generators): `python3 research/blast/lean/link_torus202.py`.
The hand-written modules are `LinkBridge`, `LinkUnique`, `LinkSym`, `LinkNoCert` (and those added later).

## Not checked

- The generators write Lean that the kernel checks; nothing they compute is trusted.
- No second reader has gone through these statements.
