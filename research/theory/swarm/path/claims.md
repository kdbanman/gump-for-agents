# path: claims (current list, after round 2)

Notation as in `journal.md`, entry 1: face F of A cells, in-face neighbours N_F, m cells beneath (3 gump, 2 toy),
θ = m + 1 the smallest birth count, n_t the face population, h the hazard among living unsettled replicas
(deaths / exposure). "Lab Lx.y" = the board's lab table.

| id | claim | tag | where | smallest case worked by hand |
|---|---|---|---|---|
| L1 | Rim lemma: if a set D of face cells is dead at t, every cell of D all of whose in-face neighbours are in D is dead at t + 1, whatever lies beneath. So (a) the live set of a face spreads at in-face speed ≤ 1, (b) a hole of in-radius ρ keeps its centre dead for ρ generations, (c) a one-step death is one constraint for each cell of N_F[supp ξ]; by the cube lemma the constraints couple only inside cube triples | **proved** (c reworded in entry 7) | entries 2, 7 | gump, one live interior cell: n_{t+1} ≤ 7; the face dies iff each of seven triples beneath contains a dead cell |
| L1′ | Rim lemma for any sealed set W: a dead cell of W all of whose neighbours in W are dead stays dead; life in W spreads only from life in W | **proved** | entry 9 | middle layer of a three-layer band: 10 neighbours in the band, 2 outside |
| S | The skeleton K(t) is the union of the sealed sets that have gone extinct; the first permanent loss is the extinction of an inclusion-minimal sealed set, and needs all its cells dead at one time | **proved** | entry 9 | a hull: the face (smallest sealed set, exact R ≤ 10, critic) |
| P | Theorem P: a one-step inequality (∗) for a statistic at every time of a window bounds the instantaneous hazard by ε(1 − s̄)/(1 − s̄ − a) after a burn-in. No Markov property | **proved** (critic checked) | entry 3 | walk on {0,1,2}: bound 3/4, exact 0.0522 |
| P̄ | Theorem P̄ (pooled form): Deaths ≤ D(𝓛ᶜ) + Σ_{entries into 𝓛} ψ + boundary, for every ψ ≥ 0 superharmonic for the pooled one-step table on a low set 𝓛; identity for the table's committor ψ*. No Markov property, no uniformity in time, no constant, censoring free | **proved** | entry 8 | same walk, 𝓛 = {1}: ψ* = 1/4, entry flux 0.1978, 0.0495/(1 − 0.0522) = 0.0522 = h |
| H′ | For the population of a gump hull face, ψ*_K(k) ≤ C e^{−θk} at the entry rows with K = κA; then ln τ ≥ θ(κA − J) − const | **hypothesis** (replaces H, which was false: lab L1.1). Consistent with lab L1.2 on rows < A/2, A ≤ 84. Missing: universality of ψ* in A (LR4); any argument | entry 8 | — |
| L3 | Sealed ⟺ complement closed under θ-bootstrap percolation; V \ K(t) = bootstrap closure of the live set | **proved** (critic checked) | entry 4 | kagome hexagon ring |
| L4, 4a | Top-layer rigidity; a d-deep top cell of a sealed set drags in its whole deep sheet and what lies under it | **proved** | entries 4, 12 | hull minus its two outer d-layers; a T3 band |
| R5 | The sealed-set facts do not imply the law: B45/S34, B45/S35, B45/S45, B4/S345 share gump's graph and θ = 4 (so every sealed-set statement and its converse), are chaotic on a torus, and have median hull lifetimes 20–104 where gump has 3,420 | **proved** as a statement about which facts are shared; the lifetimes are the survey's (`research/phase/rules.csv`) | entries 4, 7, 13 | — |
| R | Biased voter dynamics on any finite graph: λ^{−n} is a martingale; a set of n sites dies out before filling the graph with probability (λ^{−n} − λ^{−N})/(1 − λ^{−N}) | **proved** | entry 10 | one edge, one occupied vertex: 1/(1 + λ) |
| Dr | Gump's death is a shrinking droplet: looking back from death √n falls by ≈ 0.59 per generation at every size; half-way lag = (√(n̄/2) − 0.68)/0.586 (3.3, 4.5, 5.6, 6.7 against 3.2, 4.7, 5.9, 6.8) | **data reading** (lab L1.3) | entry 11.1 | — |
| Th | The committor slope (0.55 per cell) and the tail slope (0.46) are one exponent θ ≈ 0.50 ± 0.03 with power-law prefactors (remnant's rate ∝ √k) | **guessed** | entry 11.2 | — |
| M | γ = θρ − θ²σ²/2, local slope of ln τ = that + 1/(2A): 0.213, 0.220, 0.226 from the measured tail slopes against 0.212, 0.212, 0.221 | **sketched**; assumptions M1–M3 (a parabola joined tangentially to a line); slopes only, the remainder is vessel-dependent; M3 unchecked (LR7) | entries 11.3, 13 | — |
| A | In the hull of every radius a non-empty sealed set has at least A(R) cells | **guessed** beyond R = 10 (exact to R = 10: critic). Not pursued further: the induction needs a stability statement | entry 12 | R = 3: 9 cells |
| G1 | The 2D rule has one exponent ≈ 0.345 in every geometry; segments show it (0.34 ± 0.01 per orbit, four geometries, measured); a ring carries a power ≈ L^{+1} | **guessed**. The ring's limit is 0.35–0.37 from the window statistics (lab L1.6); D2 exact: same sign, undecided (lab L1.5). C4 (0.277) contradicts every local picture | entries 5, 7 | — |
| E1–E3 | Exam entries: notched ring slope 0.345 ± 0.020; remnant 9.8 ± 1.0 cells at lag 2, L = 32, 36; gump's remnant curve and tail ratio on a rim-free slab face equal the hull's | filed in `swarm/PREDICTIONS.md` | entries 6, 14 | — |

**Withdrawn.** H (Theorem P's hypothesis with φ = r^{min(n,K)}): false, lab L1.1 (entry 7). G2, gump half ("gump's
data cannot tell a flash from a front"): the data can, lab L1.3 (entry 7). L1(c) "each constraint involves a
private cell": false at the three corners of a hull face (entry 7). R5's first example (the rule "born iff 12
alive"): it has birth count 12, not θ (entry 7).
