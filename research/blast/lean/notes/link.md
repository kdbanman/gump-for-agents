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
- Proved for **every wrapped face** `torus H K D` (H, D > 0, any K; third task): everything in `wrapped_full_all`
  (`wrapped_theorems_all` at every 0 < ρ1, ρ2 < 1). Nothing is hypothesis: the bijection is `torusNb_all`.
- Proved for every hull face and every face with all its coins: `survFrom = Face.survival` (`survFrom_cast`).
- Proved for **every hull face** (fourth and fifth tasks), every R with A > 0, no hypothesis: `CellsOK`
  (`cellsOK_hull`), everything in `hull_theorems`, and everything in `hull_full_every` (uniqueness, positivity, decay
  at exactly λ, equal prices along table automorphisms; `Lemma0F (hull R)` is `hull_lemma0`), and equal prices along
  the triangle's six symmetries (`hull_prices_sym`; `rot_aut`, `refl_aut`). The face-by-face certificates
  (`LinkHullCert.lean`, R ≤ 13) are now a second, independent check.
- **Not proved**: a certified λ (hence ln τ to digits) for the 12-cell torus or any torus beyond the certified two;
  Lemma 0 on the strips.

## Third task (2026-11-24, from 14:51 UTC): the generators, survival, every wrapped face

Files (new): `LinkSurv.lean`, `LinkWrapped.lean`, `LinkWrappedFull.lean`, `LinkWrappedCheck.lean`,
`LinkWrappedAll.lean`, `LinkWrappedArea.lean`, the `link_*.py` generators. Imported from the dice agent (read-only, committed and built):
`DiceHull` (`hull_P_empty_row`), `DiceTorusReg` (`Tr`, `Tr_sub`, `torus_red`, `gridCells_nodup`, `axis_abCell`,
`nb_lt'`, `lntau_le_torus`), `DiceHullAll` (`idxOf?_nodup`).

1. **`survFrom` is `Face.survival`** (`LinkSurv.lean`, `survFrom_cast`): on every face whose empty state is absorbing,
   `(chain F).survFrom t x = (F.survival ρ1 ρ2 t x : ℝ)` for every t and living x (by induction on t; the
   empty state contributes 0 since `Face.survival t ∅ = 0`, `survival_empty_of`). Absorbing: every hull face
   (`absorbing_hull`) and every face with all its coins (`absorbing_of_coins`). **`hull3_complete`**: every clause of
   `hull3_full`, plus `survFrom = Face.survival`, `0.72·λ₋^t ≤ P_full(T > t)` and `P_x(T > t) ≤ 1384·λ₊^t`
   (the dice agent's `hull3_lifetime`) with λ₋ ≤ λ ≤ λ₊, in one theorem.
2. **Every wrapped face** (`LinkWrapped*.lean`). The hypothesis was first named `TorusNb H K D`: (torus H K D).A = 3HD
   and `nb i` is a permutation of `kIdx i` (the kagome neighbours of cell i = 3(aD + b) + o, reduced by the dice
   agent's `Tr`). `kIdx_map` (every torus): `(kIdx i).map phi = Kagome.nbrs (phi i)`, phi i = (o, [a, b]).
   `cellEquiv` (Fin A ≃ Orient × Torus H K D, from `torusRep_bijective` and the cardinality), `stateEquiv`
   (bits ↔ subsets), **`Q_eq`**: `Face.P` *is* the kagome kernel along these. The relabelling lemmas
   (`transport_qsd`, `transport_survFrom`, `transport_canSurvive`, `transport_price`: the price is an explicit
   integral of a Gibbs tilt of μ, so it transports by reindexing sums) carry `wrapped_lemma0`,
   `wrapped_one_price_HD`, `wrapped_rotation_HD` and `decay_bounds` to `Face.P`; `face_theorems_allcoins` gives the
   dominant QSD and the tilt identity; `lntau_le_torus` gives 1.9228·A. `wrapped_full` (under `TorusNb`) and
   `wrapped_theorems` (any densities). `TorusNb` is kernel-checked (`decide +kernel`, each under a second) on
   (1,0,1), (2,0,2), (1,0,2), (2,0,1), (1,0,3), (3,0,1), (2,1,2), (2,0,3), (3,1,3), (3,0,3).
   **Then proved for every H, D > 0** (`LinkWrappedAll.lean`, `torusNb_all`): `grid_getElem?` (cell i of
   `gridCells H D` is (i mod 3, ⌊i/3⌋ div D, ⌊i/3⌋ mod D)), `idxOf_grid` (its index), `inlayer` (the six in-layer
   neighbours of (o, a, b) in `Gump.offsets` order, `DL o`), `nb_eq` (nb i = `DL` mapped by the reduced index),
   `DL_perm` (`DL o` is a permutation of the kagome `offs o`, decided). Hence **`wrapped_full_all`** and
   `wrapped_theorems_all`, no hypothesis.
   **`wrapped_area`** (`LinkWrappedArea.lean`): for that law, ln τ = H·D·(c₀ + c₁ + c₂) with c_o the price of cell o
   (orientation o at the origin), and ln τ = A·c₀ on a rotation-invariant torus: ln τ is exactly linear in the
   area at fixed shape class, with one constant per orientation.
   One price per orientation is stated on the face as: cells i ≡ j (mod 3) have equal prices; one per cell when
   (K, −H−K) and (D, −D) are periods (the lattice of `ChainTorus.lean`).

## Fourth task (2026-11-24, from 15:23 UTC): every hull face

Files (new): `LinkHull.lean`, `LinkFaceAut.lean`, `LinkHullCert.lean`, `link_hull_cert.py`.
Imported from the dice agent (read-only): `DiceHullAll` (`hull_type`, `lntau_le_hull_all`), `DiceHull`
(`hull_P_empty_row`, via `LinkSurv`).

1. **`cellsOK_hull R`** for every R, from `hull_type`; hence **`hull_theorems R`** (no hypothesis): the dominant
   law, the tilt identity with named per-cell factors, ln τ < 2.2165·A, survFrom = Face.survival.
2. **Lemma 0, named and density-free**: `Lemma0F F` := a living u with every cell able to be alive next
   (`aliveF`: `canB` of the cell's coins, k and state), and from every living state some cell of which can be alive
   next a chain of possible transitions (`StepN`) to u. `Q_pos_iffF` (0 < Q x y ↔ `stepF F x y`, every face with its
   coins) and `rtg_pow` turn it into `one_class'`'s hypotheses; **`face_full_of`** (any face) and
   **`hull_full_all R (hA) (h0 : Lemma0F (hull R))`**. `lemma0_of_cert`: Lemma0F from a certificate of polynomial size
   (`certOK`: u, a growth path from one cell c0 to u, a walk of single cells from every cell to c0).
   `link_hull_cert.py` builds it the same way for every R: u = every cell whose normal is not z (every cell can be
   alive next from it: an interior cell sees k = 4, every z cell has a live x and a live y neighbour, the z-corner
   both its neighbours alive, the x- and y-corners one; a reading of the construction, the kernel checks it); walks by breadth-first search over single cells (a
   non-corner cell can be born next to a lone live cell; a corner passes to its neighbour); growth inside the
   non-corner x- and y-cells (no z alive keeps every k ≤ 4), then the two z-cells beside the x- and y-corners, then u.
   Checked by the kernel for R = 3, …, 13 (`LinkHullCert.lean`, 86 s; a module for R = 15, 17 passed 10 GB of
   memory and was stopped, not committed; the generator still writes it with `LINK_FILE`);
   `hull1_lemma0` (three corners: u = the full face, entered in one step) by `decide +kernel`.
3. **Prices along symmetries**: `price_aut` (any face, any `autOK` automorphism: a permutation of the cells carrying
   `nb` to `nb` up to order and keeping m1, m2; the state map relabels the live set, `price_invariant`), and
   **`hull_full_sym R`**: `hull_full_all` plus c_{π i} = c_i for every such π. `hull<R>_rot` ((x,y,z) ↦ (y,z,x)) and
   `hull<R>_refl` ((x,y,z) ↦ (y,x,z)) are kernel-checked automorphisms for R = 3, …, 13; they generate the six
   symmetries of the triangle.

**Where the general proof stops.** `Lemma0F (hull R)` and `autOK` for the rotation and reflection are not proved for
every R. The certificate is uniform in R (the same u, the same three phases), so the general proof is the
formalisation of that construction in the hull's coordinates, and is not done: (a) aliveF u i for every cell, by
orientation and boundary, as in `hull_type`'s case analysis; (b) a walk of single cells from every cell to c0, by
induction on the coordinates; (c) the growth inside the x/y cells, by connectivity of the non-corner x/y cells and
the monotone step s ↦ M(s) ∩ T (every k ≤ 4 while no z cell is alive); (d) the two z-cell step. For the symmetries,
`Gump.offsets` permuted by a coordinate permutation is a permutation of the permuted axis's offsets (finite), and
`hullCells` is invariant (index map by `idxOf?`); not written.

## Fifth task (2026-11-24, from 16:04 UTC): Lemma 0 and the symmetries on every hull face, general proofs

Files (new): `LinkHullGen.lean`, `LinkHullSym.lean`. The fourth task's "where the general proof stops" is closed: the
certificate's construction written out in the hull's coordinates.

- **States as masks of point sets** (`mask R S`, through `LinkWrapped`'s bit/subset bijection): `mask_bit`,
  `mask_congr`, `single_eq` (2^j is the mask of cell j). **`k_mask`**: the number of live neighbours of cell i is
  `kc R S (cell i)`, a count over the cell's six in-layer offsets (`kc_eq`, `inl_X/Y/Z`) of the neighbours in the
  hull and in S. `m2_eq` (no coin two layers in exactly at the corners), `aliveF_mask`, **`stepN_mask`** (a possible
  transition is a check, cell by cell, in coordinates), `canB_*` (the coin rule as arithmetic).
- **Counting lemmas** (every R, by the six offsets): `kc_le_four` (no z-cell alive: k ≤ 4), `kc_le_five` (live
  cells with z even or z = 1: k ≤ 5 at x- and y-cells), `kc_le_one` (one live cell: k ≤ 1), `kc_pos`, `kc_two`.
- **The geometry**: T = the non-corner x- and y-cells, φ = 3(R − 1 − z) + [stuck] (stuck: an x-cell with y = 0, or a
  y-cell with x = 0 below the top row), c0 = (0, 1, R − 1). `descent`: every cell of T but c0 has an in-layer
  neighbour in T of smaller φ, which has it as an in-layer neighbour (an x-cell with y ≥ 2 moves up in z, one with
  y = 0 moves to the y-cell beside it; likewise for y-cells; four cases). `enterT`: every other cell has an in-layer
  neighbour in T (a z-cell moves to the x- or y-cell below it; the x- and y-corners along their edge). `phi_zero`:
  φ ≤ 0 on T only at c0.
- **The reach**: `walk_step`, `walk_T`, `walk_all` (a lone live cell walks to c0, by induction on φ); `grow_step`,
  `grow` ({c0} grows through the sublevel sets G n of φ: each new cell is born next to its descent neighbour, every
  k ≤ 4 since no z-cell is alive), `G0`, `GN`; `step_TZ` (T, then T with the z-cells (R−1, 0, 1), (0, R−1, 1));
  `step_U` (then u: the corners are born from two live neighbours, `kc_two`; every other cell has k ≤ 5);
  `aliveF_u` (every cell can be alive next from u). **`hull_lemma0 R (hA : 0 < A)`** (R = 1 from `hull1_lemma0`) and
  **`hull_full_every R hA`**.
- **The symmetries** (`LinkHullSym.lean`): `aut_general` (an additive, injective map keeping d·p, the hull and the
  corners and carrying each cell's offsets to its image's is an `autOK` automorphism; the neighbour lists are carried
  by `List.Perm.filterMap`), **`rot_aut`**, **`refl_aut`** (every R; the offset permutations decided per orientation),
  **`hull_prices_sym`**: c_j = c_i when cell j is the rotation or the reflection of cell i, for the unique QSD.

Each module builds in under a minute; no `decide` over states (the only `decide`s are on the twelve-offset lists).

## Reproduce

    cd research/blast/lean/mathlib
    lake build GumpMath.LinkBridge GumpMath.LinkUnique GumpMath.LinkSym     # quick
    for f in Hull3 Torus103 Torus113 Strip13 Patch13; do lake build GumpMath.Link$f GumpMath.Link${f}Sym; done
    lake build GumpMath.LinkFaces && lake env lean AxiomsLink.lean          # one at a time: ~1-1.5 min per face file
    lake build GumpMath.LinkNoCert GumpMath.LinkTorus202                    # the 12-cell torus: 3-4.5 min
    lake build GumpMath.LinkSurv GumpMath.LinkWrapped GumpMath.LinkWrappedFull   # third task: ~10 s each
    lake build GumpMath.LinkWrappedCheck GumpMath.LinkWrappedAll GumpMath.LinkWrappedArea   # ~10-20 s each
    lake build GumpMath.LinkHull GumpMath.LinkFaceAut                       # fourth task: ~30 s each
    lake build GumpMath.LinkHullCert                                        # R = 1..13: ~90 s
    lake build GumpMath.LinkHullGen GumpMath.LinkHullSym                    # fifth task: under a minute each

The generators (committed; each regenerates its modules **byte for byte**, checked with `LINK_OUT=<dir>` and `cmp`
against the committed files at 9fde4a9; set `LINK_OUT` to write elsewhere, the default is `mathlib/GumpMath/`):
- `link_reach.py` — writes nothing; the reachability certificate (u, nxt, dist) from the dice tables, imported by the
  generators; `python3 research/blast/lean/link_reach.py DiceHull3 DiceTorus103 …` prints u and the distances.
- `link_gen_faces.py` — writes `LinkHull3.lean`, `LinkTorus103.lean`, `LinkTorus113.lean`, `LinkStrip13.lean`,
  `LinkPatch13.lean`: `python3 research/blast/lean/link_gen_faces.py`.
- `link_gen_sym.py` — writes the five `Link<Face>Sym.lean`: `python3 research/blast/lean/link_gen_sym.py`.
- `link_gen_full.py` — writes `LinkFaces.lean`: `python3 research/blast/lean/link_gen_full.py`.
- `link_torus202.py` — writes `LinkTorus202.lean` (tables, trees, generators): `python3 research/blast/lean/link_torus202.py`.
- `link_hull_cert.py` — writes `LinkHullCert.lean` (`python3 research/blast/lean/link_hull_cert.py TABLES 1 3 5 7 9 11 13`)
  byte for byte (`LINK_FILE=<name>` writes another module, e.g. for R = 15, 17: too heavy, see the fourth task); TABLES is the output of
  the `#eval dump R` given in its docstring (cells, `Face.nb`, `m1`, `m2` of `hull R`).
The hand-written modules are `LinkBridge`, `LinkUnique`, `LinkSym`, `LinkNoCert` (and those added later).

## Not checked

- The generators write Lean that the kernel checks; nothing they compute is trusted.
- No second reader has gone through these statements (the referee reads the modules at 9fde4a9; the third task's
  files are later).
- `kIdx`/`offs` were matched to the dice geometry by `#eval` before the proof (orientation o ↔ X, Y, Z, e1 along a,
  e2 along b); the proof does not depend on that run.
