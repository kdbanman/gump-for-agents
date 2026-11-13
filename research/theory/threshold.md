# S5 — the threshold lemma: proof, audit, measurements

*2026-11-13, theory agent (S5/S6). Scripts in this directory; every number below has its command.
Tags: **[proved]** complete argument here; **[measured]** with n and command; **[conjecture]**.*

## Summary

- The lemma is **correct as stated**, with three clarifications (ordered pairs in the energy; finite vessels only;
  time indices in (c)) and one strengthening: (c) is an **exact identity**, ΔE = D − Q, not just an inequality, and
  over any periodic orbit **total drive = total dissipation**. (b) sharpens to: every oscillator of period ≥ 3 has an
  overcrowded cell that was **live two generations earlier** (an "O1 event"); overcrowded cells that were dead at
  t−1 inject nothing.
- It does **not** extend to infinite configurations: the uncapped rule has fronts that advance forever.
- Chaos is not "occasionally overcrowded": in bulk chaos **40% of cells are overcrowded every generation** and
  11.5% are O1 events. Activity is ≈ 3.9 mismatches per O1 event against a proved ceiling of 20.
- Citations: I opened two secondary sources that state the Goles–Olivos theorem; the primary papers and the
  Goles–Martínez book I could **not** open (paywall / blocked). Details at the end.

## 1. Setting and notation

Let V be a finite set of cells: a torus, or a vessel whose outside is dead forever (an octahedral hull, a `{111}`
slab; T2–T4 make those exact). A = adjacency of gump's 12-neighbour graph restricted to V (symmetric, 0/1; on very
small tori a multigraph — still symmetric), W = A + I. For a state x ∈ {0,1}^V write

- n_i(t) = (A x(t))_i, h_i(t) = (W x(t))_i = n_i(t) + x_i(t)  (integers);
- gump: x_i(t+1) = 1 iff 4 ≤ h_i(t) and n_i(t) ≤ 5  (check: dead cell, h = n ∈ {4,5}; live cell, h = n+1 ∈ {4,5,6});
- uncapped rule U: x_i(t+1) = 1 iff h_i(t) ≥ 4, i.e. W x ≥ θ with θ = 3.5;
- cell i is **overcrowded at t** if n_i(t) ≥ 6. Gump and U agree at every cell that is not overcrowded and disagree
  at every overcrowded one (gump 0, U 1: h ≥ 6 ≥ 4).

Energy, for t ≥ 1, **sum over ordered pairs**:

  E(t) = − x(t)ᵀ W x(t−1) + θ (|x(t)| + |x(t−1)|) = − Σ_i x_i(t) h_i(t−1) + 3.5 Σ_i (x_i(t) + x_i(t−1)).

*Audit note 1.* PROGRAM.md writes Σ_{i~j or i=j} x_i(t) x_j(t−1). That is right only if read as a sum over
**ordered** pairs (each edge twice, once each way) plus the diagonal once — i.e. x(t)ᵀ W x(t−1). Summing each
unordered edge once picks an arbitrary orientation and the identity below fails.

## 2. The identity [proved]

Since W is symmetric, x(t)ᵀ W x(t−1) = x(t−1)ᵀ W x(t) = Σ_i x_i(t−1) h_i(t). Hence

  E(t+1) − E(t) = −Σ_i x_i(t+1) h_i(t) + Σ_i x_i(t−1) h_i(t) + θ Σ_i (x_i(t+1) − x_i(t−1))
               = − Σ_i (x_i(t+1) − x_i(t−1)) (h_i(t) − 3.5).                                   (★)

Each term is zero unless x_i(t+1) ≠ x_i(t−1) (a **mismatch**: the cell breaks period 2 there).

- *Non-overcrowded cell* (the rule there is U): if x_i(t+1) = 1 > x_i(t−1) then h_i(t) ≥ 4 and the term is
  −(h−3.5) ≤ −½; if x_i(t+1) = 0 < x_i(t−1) then h_i(t) ≤ 3 and the term is (h−3.5) ≤ −½. In both cases the
  term is exactly −|h_i(t) − 3.5|.
- *Overcrowded cell*: x_i(t+1) = 0, so the term is x_i(t−1)(h_i(t) − 3.5): zero if x_i(t−1) = 0, and
  h_i(t) − 3.5 = n_i(t) + x_i(t) − 3.5 ∈ [2.5, 9.5] if x_i(t−1) = 1 (an **O1 event**; it is itself a mismatch).

So, exactly,

  **E(t+1) − E(t) = D(t) − Q(t)**,  D(t) = Σ_{O1 events at t} (n_i(t) + x_i(t) − 3.5),
                                     Q(t) = Σ_{non-overcrowded mismatches at t} |h_i(t) − 3.5| ≥ ½ · M_n(t),

where M_n(t) counts non-overcrowded mismatches. This is (c) of PROGRAM.md with equality restored; (c) as
written is correct (time indices: n_i, x_i at t; the condition x_i(t−1) = 1; mismatch means x(t+1) ≠ x(t−1)).

**Bounds on E** [proved]. 0 ≤ x(t)ᵀ W x(t−1) ≤ 13 · min(|x(t)|, |x(t−1)|), so
−6 · min(|x(t)|, |x(t−1)|) ≤ E(t) ≤ 3.5 (|x(t)| + |x(t−1)|), hence **−6N ≤ E ≤ 7N** (N = |V|).

## 3. Consequences [proved]

- **(U) Uncapped rule.** D ≡ 0, so E is non-increasing and drops by ≥ ½ per mismatch. Total mismatches over
  the whole orbit ≤ 2 · 13N = 26N; a step with no mismatch continues a period-≤2 orbit forever. So every orbit
  of U on a finite vessel reaches period ≤ 2 within 26N + 1 steps. (This is the Goles–Olivos theorem for W = A + I;
  the self-weight is harmless: (★) uses only symmetry of W, diagonal included.)
- **(a)** If no cell is overcrowded from time T on, the orbit from T on is an orbit of U: period ≤ 2, reached
  within 26N + 1 further steps. *Weaker hypothesis suffices:* if from T on there is no **O1 event**, D ≡ 0 and the
  same conclusion holds (overcrowded cells that were dead at t−1 cause no mismatch and no energy).
- **(b′)** Every orbit of period P ≥ 3 has an O1 event at some phase. Sharper, summing (★) over a period:
  **Σ_period Q = Σ_period D** (energy is periodic). Since every cell whose own period is ≥ 3 mismatches at
  least twice per period (its even- and odd-time subsequences are not both constant, and a non-constant cyclic
  0/1 sequence changes value an even, nonzero number of times), with R₃ = number of such cells:
  2 R₃ ≤ Σ_period M ≤ Σ_period (M_n + O1) ≤ Σ_period (2D + O1) ≤ 20 · Σ_period O1.
  **Every oscillator has ≥ R₃/10 O1 events per period.**
- **Budget for any window** [proved]. For any T₀ < T₁, with T = T₁ − T₀:
  Σ M_n ≤ 2 Σ Q = 2 Σ D + 2(E(T₀) − E(T₁)) ≤ 19 Σ O1 + 26N, so the activity rate obeys
  **M/(N·T) ≤ 20 · O1/(N·T) + 26/T.** Sustained activity needs overcrowding (O1 events) at a rate at least 1/20 of
  the activity; in one `{111}` layer (h ≤ 7, D per event ∈ {2.5, 3.5}) the constant 20 improves to 8.
- **Infinite configurations: false as stated.** On the infinite lattice E diverges and the argument says nothing.
  It is not a technicality: under U the half-space x < 0 (all cells live) advances one cube per generation forever
  and never becomes periodic. Measured on Lx × 4 × 4 tori (two fronts): U settles at exactly Lx/2 generations for
  Lx = 8, 16, 32, 64 (front speed 1 cube/gen; also shows the O(N) transient bound is sharp in order).
  (`python3 research/theory/front.py`.) Each cell
  is eventually constant there; whether *every cell* of an infinite configuration of U is eventually period ≤ 2 I
  did not settle.

## 4. Numerical audit [measured]

`python3 research/theory/energy.py selftest` — the identity 2ΔE = 2D − 2Q (integer arithmetic) and (c) hold at
every step of 5,683 steps: gump and U on a 3,072-cell 3D torus (ρ = 0.1–0.8), 1-, 2-, 3-layer slabs, an octahedral
vessel R = 13; U never increased E. The stepper is checked against `research/atlas/lattice.py` (oracle-verified).
`python3 research/theory/overcrowd.py bulk 12 1500 300 1` re-asserts the identity at every one of 1,500 steps of
bulk chaos. `python3 research/theory/overcrowd.py catalogue`: for all 1,307 catalogued objects
Σ_period D = Σ_period Q holds exactly; all 329 objects of period ≥ 3 have an O1 event (978 of period ≤ 2: none, as
they must). Exhaustive check of (U) on small closed vessels (`exhaust.c -u`, all 2^n states, n ≤ 24): every
orbit of U ends in period 1 or 2, max transient 11.

## 5. What the budget buys: overcrowding rates [measured]

Rates per cell per generation. O1 = overcrowded and live two generations before (the only energy source);
M = mismatches x(t+1) ≠ x(t−1) (activity beyond period 2).

| where | density | overcrowded | O1 | M | command |
|---|---|---|---|---|---|
| bulk chaos, 3D torus 12³ cubes (5,184 cells), gens 300–1500 | 0.416 | 0.402 | 0.115 | 0.453 | `overcrowd.py bulk 12 1500 300 1` |
| 3-layer slab, outer layers (N = 16) | 0.500 | 0.273 | 0.117 | 0.461 | `overcrowd.py slab 16 3 3000 1` |
| 3-layer slab, middle layer | 0.446 | 0.343 | 0.123 | 0.455 | same |
| 4-layer slab, outer / inner | 0.517 / 0.423 | 0.261 / 0.393 | 0.115 / 0.122 | 0.469 / 0.455 | `overcrowd.py slab 16 4 3000 1` |
| final cycles (debris) | — | — | 0 for period ≤ 2 | 0 | identity |

In bulk chaos: D = Q = 0.443 per cell per gen (balance, as it must on average); mean drive per O1 event 3.85 (so
O1 events typically have n ≈ 7); 29% of overcrowded cells are O1 events; M/O1 = 3.9 (proved ceiling 20); mean
dissipation per non-overcrowded mismatch Q/M_n = 1.31. E/N = 0.90 ± 0.04. In the 329 catalogued period-≥3
objects M/O1 per period ranges 2.5–6.0 (median 3.2): the drive is used about 4–6× more efficiently than the
ceiling allows, in chaos and clockwork alike.

**Faces and the run-up to a face death** (octahedral soups, cube-centred, ρ = 0.4; 'face' = outermost live
`{111}` layer in each of 8 directions; 'pre-death' = that layer in the 50 generations before it empties):
`python3 research/theory/overcrowd.py octa 9 30 2 200000` (510-cell vessel, 30 soups, lifetimes 1,153–15,580,
773 layer deaths after generation 51; chaos = generations 21 … μ−100):

| where | overcrowded | O1 | M |
|---|---|---|---|
| whole vessel, chaos | 0.255 | 0.097 | 0.384 |
| outermost live layer (8 directions), chaos | 0.135 | 0.073 | 0.343 |
| that layer, 50 generations before it empties | 0.065 | 0.035 | 0.169 |
| final cycles (all 30 of period ≤ 2) | 0.004 | 0 | 0 |

A face is driven at ~¾ of the vessel's rate (its cells miss 3 of their 12 neighbours), and in the 50 generations
before it dies its drive has already halved: a dying face is a starved face, not a face killed in full activity.
E per hull cell: 0.89 ± 0.17 in chaos, 0.047 in the final cycles.

**Thin slabs** (time course, mean over 40 soups, N = 16, ρ = 0.4, `overcrowd.py timecourse 16 m 40 1001 7`):
| t | 1 | 5 | 10 | 20 | 50 | 100 | 1000 |
|---|---|---|---|---|---|---|---|
| m = 1: O1 | 0.0127 | 0.0017 | 0.0002 | 0.0000 | 0 | 0 | 0 |
| m = 1: M | 0.29 | 0.043 | 0.0064 | 0.0002 | 0 | 0 | 0 |
| m = 2: O1 | 0.126 | 0.083 | 0.071 | 0.055 | 0.012 | 0.0007 | 0.0006 |
| m = 2: M | 0.41 | 0.33 | 0.28 | 0.21 | 0.050 | 0.0034 | 0.0021 |
| m = 3: O1 | 0.197 | 0.116 | 0.120 | 0.118 | 0.114 | 0.114 | 0.117 |
| m = 3: M | 0.49 | 0.46 | 0.46 | 0.46 | 0.46 | 0.46 | 0.46 |

In one layer the drive is starved from the start: a cell is overcrowded only with all six neighbours live, and O1
events are 1% of cells at t = 1 (ρ = 0.4; 16% at ρ = 0.7) and gone by t ≈ 20. Two layers start like chaos
(O1 ≈ 0.1) and decay over ~50 generations. Residual M at late times is clockwork (kagome oscillators, see
thickness.md).

**E as an order parameter** [measured]: E/N is 0.90 in bulk chaos and ≈ 0.07 in the final cycles of octahedral
soups, but mostly because E tracks density (a still life has E = Σ_live (7 − h_i), 1–3 per live cell). The clean
separator is the **drive rate** D (equivalently O1): positive and steady in chaos (≈ 0.44 per cell per gen),
identically zero in period-≤2 debris, and in clockwork a few events per period localised on the rotor.

## 6. What remains open

- A *lower* bound on dissipation that would force chaos to die (e.g. "an O1 event cannot recur at a site
  without Ω(1) dissipation nearby") cannot be local and unconditional: clockwork exists with exact balance.
- Whether E per cell has a deterministic large-N limit in chaos, and how its fluctuations relate to face deaths.
- Infinite configurations (cellwise eventual period ≤ 2 for U).

## Citations (what I actually opened)

- **Opened:** C. J. Kuhlman, H. S. Mortveit, D. Murrugarra, V. S. A. Kumar, *Bifurcations in Boolean networks*,
  arXiv:1108.2974 (DMTCS proc. 2012), https://arxiv.org/abs/1108.2974 . Its Appendix A gives a condensed English
  translation of the Goles–Olivos proof: for any **real symmetric** matrix A (diagonal unrestricted) and thresholds
  θ, the synchronous map x ↦ 1[Ax ≥ θ] satisfies F^{s+2}(x) = F^s(x) (Theorem A.1) — proved there by the
  Goles–Olivos cycle operator L(z_i, z_j) = a_ij Σ_l (z_j(l+1) − z_j(l−1)) z_i(l), not by an energy. Its reference
  list: E. Goles, J. Olivos, *Comportement périodique des fonctions à seuil binaires et applications*, Discrete
  Appl. Math. 3 (1981) 93–105; and Goles-Chacc, Fogelman-Soulié, Pellegrin (1985). They also prove the same for
  *bi-threshold* synchronous networks (separate up/down thresholds) — gump's uncapped rule is in fact of that form
  without the self-loop (birth at n ≥ 4, death at n < 3), so their Theorem 3.1 also covers it.
- **Opened:** E. Goles, P. Montealegre, M. Ríos-Wilson, S. Sené, *Dynamical stability of threshold networks over
  undirected signed graphs*, arXiv:2309.01854, https://arxiv.org/html/2309.01854v3 . States "every initial
  configuration of a threshold network converges to either a fixed point or a limit two-cycle" (their Prop. 1),
  attributed to E. Goles, J. Olivos, *Periodic behaviour of generalized threshold functions*, Discrete Math. 30(2)
  (1980) 187–189; energy monotonicity attributed to E. Goles, *Fixed point behavior of threshold functions on a
  finite set*, SIAM J. Algebraic Discrete Methods 3(4) (1982) 529–531 (a sequential-update energy).
- **Not opened** (paywalled at sciencedirect; bibliographic data confirmed via OpenAlex/zbMATH metadata only):
  Goles & Olivos, Discrete Math. 30 (1980) 187–189, doi:10.1016/0012-365X(80)90121-1; Goles-Chacc,
  Fogelman-Soulié, Pellegrin, *Decreasing energy functions as a tool for studying threshold networks*, Discrete
  Appl. Math. 12(3) (1985) 261–277, doi:10.1016/0166-218X(85)90029-0 (zbMATH keywords: "spin glass energy",
  "transient length" — this is the paper the two-time energy E(t) is usually credited to); and Goles &
  Martínez, *Neural and Automata Networks* (Kluwer, 1990). The proof in §2 is self-contained, so nothing here
  depends on their exact statements. Recommended citation: Goles & Olivos 1980/1981 for period ≤ 2, Goles,
  Fogelman-Soulié & Pellegrin 1985 for the energy — once someone has checked the latter's form.
