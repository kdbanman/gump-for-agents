# The gump automaton

Source of truth for *what the automaton is* and *what is proven about it*.
Everything here was either read directly from the original source
(`kdbanman/gump`, `dev/gump/environment.pde`) or proved below and then checked by
brute force (`reference/check_theory.py`). Empirical findings live in
`research/NOTEBOOK.md`, not here.

## 1. Lattice

Cells are the **faces of the cubic honeycomb**. Three equivalent coordinate pictures:

**Doubled coordinates (the original's).** `p = (x, y, z) ∈ Z³` with *exactly one odd
coordinate*. Cubes have side 2 and all-even centres; the odd coordinate is the face's
normal axis. (Two odd = an edge midpoint, three odd = a vertex; neither is a cell.)

**Cube-index coordinates (good for storage).** Three bit-volumes `X, Y, Z` indexed by
cube `(i, j, k)`: `A[i,j,k]` is the face on the `+a` side of cube `(i,j,k)`, i.e. doubled
`2(i,j,k) + e_a`. Three cells per cube.

**Dual picture.** Faces of the cubic honeycomb = edges (bonds) of the dual cubic lattice
= the anion sites of the ReO₃ / perovskite structure. The two cubes a face separates
are the bond's two endpoints.

## 2. Neighbourhood and rule

A face with normal axis `a` (other axes `b, c`) has **12 neighbours**, at doubled offsets

- `±2e_b ± 2e_c` — the 4 coplanar faces that touch it only at a **corner**;
- `±e_a ± e_b`, `±e_a ± e_c` — the 8 **perpendicular** faces that share an **edge** with it
  (equivalently: every face of the two adjoining cubes except itself and the two opposite ones).

Not neighbours: the 4 coplanar edge-sharing faces, the 2 parallel faces across the adjoining cubes.

In cube-index form (cyclic in X→Y→Z, i→j→k):

    X[i,j,k]:  X[i, j±1, k±1]
               Y[i,j,k]  Y[i,j-1,k]  Y[i+1,j,k]  Y[i+1,j-1,k]
               Z[i,j,k]  Z[i,j,k-1]  Z[i+1,j,k]  Z[i+1,j,k-1]
    Y[i,j,k]:  Y[i±1, j, k±1]
               Z[i,j,k]  Z[i,j,k-1]  Z[i,j+1,k]  Z[i,j+1,k-1]
               X[i,j,k]  X[i-1,j,k]  X[i,j+1,k]  X[i-1,j+1,k]
    Z[i,j,k]:  Z[i±1, j±1, k]
               X[i,j,k]  X[i-1,j,k]  X[i,j,k+1]  X[i-1,j,k+1]
               Y[i,j,k]  Y[i,j-1,k]  Y[i,j,k+1]  Y[i,j-1,k+1]

**Rule (outer-totalistic, synchronous): B45/S345.** With `n` = number of live neighbours:
a dead cell becomes live iff `n ∈ {4,5}`; a live cell stays live iff `n ∈ {3,4,5}`.

The neighbourhood is invariant under the full symmetry group of the lattice
(translations by cube steps × the 48-element octahedral group O_h), so the dynamics is too.
A seed's symmetry is preserved forever.

## 3. Structure theorems

Let `d ∈ {±1}³` be a body diagonal and `s = d·p` (doubled coords). `s` is odd for every
cell, so each diagonal slices the lattice into **layers** `s = …, -3, -1, 1, 3, …`.
There are 4 diagonal axes (8 signed directions).

**T1 (layer histogram).** For every cell and every `d`, its 12 neighbours are distributed
over layers as `Δs = -4: 1, -2: 2, 0: 6, +2: 2, +4: 1`.
*(Direct enumeration of the offsets.)*

**T2 (octahedral confinement).** If every cell with `s > C` is dead, that stays true forever.
*Proof.* A dead cell in layer `C+2` has at most `1 + 2 = 3` neighbours in layers `≤ C`;
in layer `C+4`, at most 1. Birth needs 4. ∎
Hence any finite pattern stays forever inside its **diagonal hull** — the intersection of
the 8 tightest half-spaces `d·p ≤ C_d` containing it (an octahedron, possibly truncated) —
and the hull can only shrink. Consequences: no spaceships, no unbounded growth, every finite
seed is eventually periodic, and *the environment needed to hold a finite seed forever is
computable from the seed alone*. Axis-aligned half-spaces do **not** confine (a cell just
outside can have 4 neighbours inside), which is why cubes grow into octahedra.

**T3 (firewall).** If three consecutive layers `C+2, C+4, C+6` (w.r.t. some `d`) are all
dead, they stay dead forever, and the two sides never influence each other again.
*Proof.* Layer `C+2` sees ≤ 3 live neighbours (from `C-2`, `C`), layer `C+6` likewise from
the other side, layer `C+4` sees ≤ 2. ∎ Two dead layers are *not* enough (`1+2` from one side
plus `1` from the other = 4). Applies to infinite and toroidal patterns too.

**T4 (closed sub-automata).** By T2 applied from both sides, a pattern contained in `m`
consecutive layers stays in those layers. In particular each single layer is a closed
**2D automaton**: the cells of one `{111}` layer form a **kagome lattice** (the 4 in-layer
perpendicular neighbours are the kagome nearest neighbours; the 2 in-layer coplanar-diagonal
neighbours sit across the hexagons), running B45/S345 on those 6 neighbours.
The full automaton is an ABC stack of kagome layers, each cell coupled 6 / 2+2 / 1+1 to
its own / adjacent / next-adjacent layers.

**Speed limit.** Information moves at most 2 doubled units per generation in max-norm
(one cube per generation), via the in-plane diagonal neighbours.

**Smallest still life found by hand:** the 6 faces of a single cube (each sees exactly 4).

T2–T3 hold for any outer-totalistic rule on this neighbourhood whose smallest birth count is ≥ 4.

## 4. Legacy semantics (for reproducing the original's runs)

- State is an `H×H×H` int array over doubled coordinates `0..H-1`; only exactly-one-odd
  sites are ever written. Neighbour indices wrap mod `H` (**array-index torus**).
  For even `H` this is a proper torus of `(H/2)³` cubes. For **odd `H`** the seam flips
  parity: most wrapped reads land on never-live sites (reads 0), a few land on a valid cell of
  the wrong orientation. New engines need not reproduce the odd-`H` seam;
  `reference/oracle.py` does, by construction.
- Closed-cube seed (`generate`, mode 1, `seedFraction = 0.38`): every valid cell with all
  coordinates in `[lo, hi]`, both odd. A "side `n`" cube is an `n×n×n` block of cubes
  with all internal faces live: `3n²(n+1)` cells, centred on a cube centre (`n` odd) or
  a vertex (`n` even), full O_h symmetry. Its hull radius is `3n − 2` (L1, doubled units,
  about its centre), i.e. the hull is **3× wider than the seed**.
- Number-key seeds (`generateFull`, key `K ∈ 1..9`, `H = 50`): every valid cell with all
  coordinates in `[lo, lo + K + 8]`, `lo = H/2 − (K+8)/2` (integer division). At `H = 50`:
  `K = 4, 8` have both ends odd — **closed** cubes of side 6 and 8 (key 8 is exactly the
  golden side-8 run, ending static at 384 cells). `K = 2, 6` have both ends even — "open"
  cubes (no caps; O_h-symmetric). Odd `K`: one end odd, one even — symmetric only under
  permutations of the axes (C₃ᵥ about the `(1,1,1)` diagonal); these flatten into `{111}` slabs.
- Logs are `generation population` lines; line 0 is `0 0` (the seed's population was never
  recorded), line `g ≥ 1` is the population after `g` iterations. Logs stop when the
  state went static.

Legacy closed-cube runs (`dev/cubic_init_results` in the original repo):

| side n | H   | span (lo..hi) | generations | final population | status here |
|-------:|----:|:-------------:|------------:|-----------------:|:------------|
| 8      | 40  | 13..29        | 23          | 384              | oracle matches every generation |
| 9      | 50  | 17..35        | 71          | 54               | oracle matches every generation |
| 10     | 55  | 17..37        | 65          | 264              | oracle matches every generation |
| 11     | 60  | 19..41        | 4,218       | 36               | oracle matches every generation |
| 12     | 65  | 21..45        | 24,286      | 288              | see notebook |
| 13     | 70  | 23..49        | 169,049     | 108              | see notebook |
| 19     | 100 (inferred) | 31..69 | unfinished at 295,971 | ≈150,000 | hull radius 55 > torus half-width 50: confinement broken by wraparound, the torus fills with soup |

The first four logs are copied to `reference/golden/`. The larger ones stay in the original
repo (`population24.txt`, `population26.txt`, `population38.txt` — megabytes; never read them
whole into an agent's context).
