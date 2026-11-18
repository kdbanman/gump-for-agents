# Audit of `research/blast/` (how a face dies), from outside the session that wrote it

2026-11-18. Subject: branch `claude/exciting-hamilton-0h2tr1` at f7918ca, `research/blast/REPORT.md` and what it
rests on (about 700 files; not merged). The GTX 1080 session's study is read at `origin/claude/gpu-local-1080`
(30d881c). Everything rebuilt here is in `research/audit/blast/` (code, `run.sh` with every command, tables in
`data/`); bulk records are in `research/scratch/audit_blast/`. Marks: **[measured here]** = this audit's own code
and runs; **[read]** = judged from the session's files without a rebuild.

## Verdict in brief

- **The mechanism is confirmed by an independent rebuild, at 63 and 84 cells.** A wrapped face dies through one
  over-full generation and a one-generation crash; a hull face of the same area does not, and dies by a fade twice
  as long. Every number of the report's that the rebuild reaches comes back within its error, several to the third
  digit (launch at 0.7376·A against 0.738; fall 48.79 → 11.24 against 48.83 → 11.18; return map 20.20 and 29.91
  against 20.2 and 29.9; autocorrelations +0.1362 and −0.0314 against +0.136 and −0.031).
- **The cause the report gives for the hull is confirmed cell by cell.** In an over-full generation the interior
  cells of a hull face (9 neighbours inside the vessel) survive as rarely as the cells of a wrapped face (0.34 and
  0.33); its rim row (7 neighbours, 30 of the 63 cells) survives twice as often (0.66).
- **"Everywhere at once" is right for the crash and too strong for what follows.** The two halves of a wrapped
  face crash in the same generation in 88% of deaths at 63 cells and 92% at 84; but the cells' last-alive times
  are patterned in space in about half the deaths (the survivors are clumps).
- **The report explains no price, and says so. Its account of tubes does not survive the 120-cell tube.** All nine
  forecasts on file were high; the local price from 108 to 120 cells (0.1957 ± 0.0016) is below the asymptote its
  one-curve fit gives (0.2004); its surrogate sits 0.12 ± 0.05 above gump there. The report locates the tube's
  discount (after the over-full generation, not before it: confirmed here at 84 cells) and offers a conjecture for
  it whose own test it scored as failed.
- **The exactly solved surrogate is sound.** Six of its rows and four of its bust shares, and two rows of the 2D
  relative's, recomputed here with a dense code to every printed digit.
- **The unreconciled chance of death at k cells is real, not a difference of definitions.** One code and one
  definition on both vessels gives 0.860, 0.643, 0.445 (wrapped) and 0.771, 0.502, 0.300 (hull) at k = 1, 2, 3. It
  is not the bust and not the shared rim row.

## 0. What was rebuilt and how it is anchored

- `geom.py`: the vessels as graphs, from the lattice definition and `reference/oracle.py`'s own offsets: the
  8-layer slab torus (h,k),(0,d) and the octahedral hull of radius R. `fd.c`: a bit-sliced stepper (512 replicas,
  one AVX-512 word a cell) that books face deaths every generation, keeps the last 32 generations of every state,
  and writes for each death the populations of six layers and the cells of three; the same for ordinary moments
  and for non-fatal over-full generations; histograms of the face population in ordinary time, its one- and
  two-step transition counts, and tallies of dips. No file of `research/blast` or of the lead's two check scripts
  is used.
- **Against the oracle** (`python3 research/audit/blast/geom.py check slab 1 4 21 1200`, likewise `hull 11`,
  `slab 1 12 28 1000`, `slab 1 4 28 1000`, `hull 13 1000`, `hull 15 1000`; 5 to 25 s each): the oracle on its
  array-index torus (the slab tiled 21 or 28 times), a plain numpy stepper on the graph and `fd.c`'s trace agree
  state for state over 1,000 to 1,200 generations on all six vessels; with one neighbour entry swapped each fails
  within 3 to 22 generations. All run with the final `fd.c`. Only lane 0 is traced; the other 511 lanes are the same
  word operations.
- **Protocol**: lives from a 0.4 soup; a life ends when any face layer is empty (reseeded) or the state repeats
  after 840 generations; only ages ≥ 1,000 count. ln τ_face = ln(faces × exposure / deaths).

| vessel | cells | replica-generations | face deaths | ln τ_face here | anchor on file |
|---|---:|---:|---:|---|---|
| torus (1,4),(0,21) | 63 | 6.12 × 10¹⁰ | 234,823 | 13.1640 ± 0.0021 | 13.1622 ± 0.0007 |
| hull, radius 11 | 63 | 2.94 × 10¹⁰ | 281,631 | 13.6357 ± 0.0019 | 13.633; the 1080's recorder 13.6429 ± 0.0049 |
| torus (1,4),(0,28) | 84 | 4.71 × 10¹⁰ | 2,263 | 17.5443 ± 0.0210 | 17.5387 ± 0.0031 |
| tube (1,12),(0,28), loop² 12 | 84 | 4.71 × 10¹⁰ | 2,831 | 17.3203 ± 0.0188 | 17.3175 ± 0.0031 |

Runs: `sh research/audit/blast/run.sh` (one core; 8.5 + 3 × 5 minutes for each 63-cell vessel, 2 × 8.5 for each
84-cell one; tables 0.5 to 2 minutes each). Tables: `data/slab63.txt`, `hull63.txt`, `wide84.txt`, `tube84.txt`.
Single-death records: 84,000 on each 63-cell vessel, all deaths at 84 cells.

## 1. The report's findings, its labels, and the verdict here

Verdicts: **confirmed** (by this audit's rebuild), **supported** (by the session's evidence, read, not rebuilt),
**doubtful**, **wrong**.

| # | finding (the report's label; its evidence) | verdict |
|---|---|---|
| 1a | A wrapped face over-fills in one step from an ordinary generation and crashes in the next; launch at 0.738·A; 48.83 → 11.18 at 63 cells; 99.5% of the cells that die in the fall are overcrowded [measured; `anatomy`, `split-slab`, `tube1d`, `boom`; refereed] | **confirmed** at 63 and 84 cells (§2) |
| 1b | No breathing: autocorrelations +0.136, −0.031 [measured; `ref-anatomy`] | **confirmed** to the fourth digit |
| 1c | Four layers fill and crash together [measured; `boom`, `ref-boom`] | **confirmed** to 0.001 in every entry; a fifth and sixth layer are over-full too |
| 1d | 84% of deaths contain a fall of 0.4 of the face, 57–59% one of half; one hump, one class [measured; `ref-anatomy`] | **confirmed**: 80.5% and 55.3% in the last 12 generations (83.4% within the final dip); one hump |
| 1e | About one bust in 130 kills [measured] | **confirmed at 63 cells** (1 in 128); it is 1 in 1,100 at 84 cells: the number belongs to the size |
| 1f | Everywhere at once: no hole, no front, no band [measured; `anatomy`] | **confirmed for the crash; overstated for the end-game** (§2) |
| 1g | The same number of survivors is deadlier after a bust (0.334 against 0.236 from four cells) [measured; `ref-anatomy`] | **direction confirmed, smaller here**: 0.311 against 0.260 for dips reaching ≤ 4 cells (§5) |
| 1h | The kill is a fragmentation (table of failure by cluster size) [measured; `boom`, `ref-boom`] | supported; not rebuilt |
| 2a | A hull face fades over about ten generations; 1.1–1.6% of its deaths hold a fall of half the face; such falls are 68 times rarer and as deadly [measured; `anatomy`, `model`, `boom`, `ref-anatomy`] | **confirmed** (1.14 ± 0.04%; 69 times; 1 in 143 against 1 in 128) |
| 2b | Its return map has no cliff: 29.9 one generation after ≥ 48 cells, 20.2 on a wrapped face [measured] | **confirmed** (29.91, 20.20) |
| 2c | Because rim cells have 7 neighbours inside the vessel, interior cells 9, corners 4 [enumeration, `rim`] | **confirmed**, count and consequence (§3) |
| 2d | Plane beats shuffles in 77% of hull deaths; last cell on the rim line 54% of the time; 58% of dying cells starve [measured; the first two unrefereed] | **confirmed** in kind: 72.6% (all 63 cells); 54.4% (of the deaths that pass through a single cell; the rim row is 48% of the face); 51% starve (39% in ordinary time) |
| 3 | The one-layer dice surrogate has the same two exits [exact; `rigour`, `ref-proofs`] | **confirmed** for the rows recomputed (§7) |
| 4a | 1/τ = Σ ν(p)·d(p) [identity] | true and empty, as its referee said |
| 4b | At the launch point 0.079 per cell is the rarity of an over-full face and 0.136 the kill; ψ(x) [measured; `boom`, `model`] | **confirmed as a description**: for "face ≥ 0.74·A" 0.083 and 0.126 between 63 and 84 cells here, ψ(0.762) = 0.1008 against 0.0995; the split moves with the threshold (its own table: 0.037 + 0.177 to 0.103 + 0.111) |
| 4c | ln τ = −ln ν(face ≥ 0.74·A) + 0.1273·A − 1.37 reads a wide face's lifetime from its living state [measured; `ref-boom/STATIC.md`; not refereed] | **confirmed at 84 cells** (17.573 against 17.544 ± 0.021); on the tube it returns the wide value, as the report says; it is not a law of hull faces (§4). Its values at 126–192 cells: not rebuilt |
| 4d | Three quarters of the price is static (four-layer state); the two-layer Gaussian map [measured, computed] | supported; not rebuilt |
| 5a | A tube's face is over-full as often as a wide face's; its discount is in the chance of death after the launch [measured; `boom`, `model`] | **confirmed at 84 cells** (§4) |
| 5b | A band of a living tube and a whole tube lie on one curve; c∞ = 0.2004 with K = 2; "it levels at 0.199–0.202" [measured, fitted; `tube1d`; unrefereed] | the band measurements: not rebuilt. **The fit and the levelling: doubtful**, contradicted at 120 cells (§6) |
| 5c | A long tube stops busting all at once [measured on the surrogate; gump at 63 and 84 cells] | **confirmed on gump at 84 cells**, weakly (§4); beyond 84 cells surrogate only, and the surrogate is off at 120 cells (§6) |
| 5d | The discount is the entropy of crash timing [conjectured] | a conjecture; by the report's own scoring its test failed |
| 5e | The discount of a loop-12 tube is 0.0046·L² from 54 to 108 cells | arithmetic, right to 108 cells; **wrong at 120** (0.00544·L²) |
| 6 | Rims: strips without corners; where the rim term sits in dip rates [measured; `rim`, `split-hull`, `ref-hull`] | supported; not rebuilt |
| 7 | The 2D relative has the two exits with the prices reversed [measured and exact; `toy`; unrefereed] | exact one-row surrogate **confirmed** on two rows (§7); the 2D brute force: not rebuilt |
| 8 | Why sampling gump itself fails [measured] | not checked |
| P1 | Tilt identity, ln τ = ∫₀¹⟨E⟩_s ds, with its bounds [proved for the surrogate] | **confirmed**; elementary (§7) |
| P2 | One price under strong spatial mixing along the tilt [proved, conditional] | a valid implication with a hypothesis the session itself believes false: no consequence for gump [read] |
| P3 | Seam identity [proved] | supported [read]: a transfer-matrix identity for histories from a soup; its consequences are conjecture, as stated |
| — | The 135-cell hull face: 29.22 ± 0.02 (conditional); surrogate 29.26 to 29.34 | not checked; the report calls it undecided, and it is |

## 2. A wrapped face of 63 cells: 234,823 deaths [measured here]

`data/slab63.txt`. "Ordinary" = replicas of age ≥ 1,000 at arbitrary moments (1.5 × 10¹⁰ face-generations).
Lag = generations before the first empty one.

**The living face.** Mean 32.584 (0.5172·A), s.d. 4.942. P(population ≥ 45, 47, 48, 50) = 4.9 × 10⁻³, 1.10 × 10⁻³,
4.8 × 10⁻⁴, 7.2 × 10⁻⁵. A generation with ≥ 48 cells was preceded by one with 32.97 on average: the over-full
generation comes in one step from an ordinary face. One generation after ≥ 48 cells the face holds 20.20
(11.7% of the time at most a quarter of the face); after 50–52 cells, 17.4 (31%).

**The dying face, by lag** (all deaths; population over the ordinary mean; share of deaths at or above 0.70·A):

| lag | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 12 | ordinary |
|---|---|---|---|---|---|---|---|---|---|
| mean / P̄ | 0.052 | 0.132 | 0.328 | 0.568 | 0.711 | 0.785 | 0.899 | 0.980 | 1 |
| 90th percentile, cells | 3 | 9 | 32 | 47 | 46 | 44 | 40 | 39 | 39 |
| share ≥ 45 cells | 0 | 0.007 | 0.089 | 0.170 | 0.143 | 0.092 | 0.052 | 0.017 | 0.0049 |

**Single deaths** (84,000 records; "window" = the last 12 generations before the empty one; in brackets the same
for 118,449 ordinary windows):

- An over-full generation in the window: ≥ 0.70·A (45 cells) in 71.5% of deaths (6.2%); ≥ 0.746·A (47) in 50.9%
  (1.4%); ≥ 48 cells in 39.5% (0.6%).
- Largest one-generation fall: ≥ 0.3·A in 93.1% (10.1%), ≥ 0.4·A in 80.5% (1.3%), ≥ 0.5·A in 55.3% (0.16%), ≥ 0.6·A
  in 24.5% (0.02%). One hump, mode 30–39 cells; 4% of deaths have no fall above 9 cells in the window.
- Launch (the last generation with at least half the face alive): mean 46.47 = **0.7376·A**, s.d. 3.63. Mean
  population from three generations before the launch to four after: 33.90, 31.08, 33.04, **46.47, 13.99**, 7.50,
  3.96, 2.22. With the report's definition (largest fall ≥ 0.5·A): 33.17 → **48.79 → 11.24**.
- From the launch to the empty face: median 5 generations (quartiles 4–8; 5–95%: 3–12).
- Layers 1 to 6 as fractions of a layer, all deaths: one generation before the launch 0.524, 0.400, 0.354, 0.377,
  0.391, 0.395; at the launch 0.738, 0.636, 0.561, 0.503, 0.465, 0.431; one generation after 0.222, 0.153, 0.190,
  0.301, 0.362, 0.380; ordinary 0.518, 0.434, 0.406, 0.416, 0.416, 0.405.
- Of the cells that die in the fall after the launch (deaths launched from ≥ 0.65·A with a fall ≥ 0.4·A: 82.9% of
  deaths), **99.24% have six or more live neighbours**. Over the whole window 64.8% of dying cells are overcrowded
  and 35.2% starved (ordinary time: 70.9% and 29.1%).

**How often an over-full generation does not kill.** Falls of ≥ 0.5·A occur 1.350 × 10⁻⁴ times per face-generation,
70 per death; 55.3% of deaths hold one: **1 such fall in 128 is fatal**. For falls of ≥ 0.4·A: 559 per death, 1 in
695. A generation with p cells lies within 12 generations before that face's death with probability 1.3 × 10⁻⁵
(p = 31–33), 2.3 × 10⁻⁴ (46–47), 9.8 × 10⁻⁴ (48–49), 3.8 × 10⁻³ (50–51), 1.6 × 10⁻² (≥ 52): 99.84% of the generations
with ≥ 48 cells are not followed by a death.

**Whether the death is everywhere at once.**
- The two halves of the face have their largest one-generation fall in the same generation in 88.1% of deaths
  (93.4% of the 83% launched from ≥ 0.65·A; 63% of the rest). With the report's definitions (last 16 generations):
  halves crash in different generations in 0.122 ± 0.002 of deaths (its 0.11 ± 0.01 on 774 deaths) against 0.875 in
  ordinary windows; at least one quarter of the face busts locally in 0.944.
- The cells' last-alive generations within one death have s.d. 1.81 (median 1.69; the report: 1.85).
- **They are not unpatterned.** The lowest Fourier modes of the last-alive generation over the torus beat 95% of
  200 shuffles of the cells in 49.1% of deaths (44.8% of bust deaths, 69.1% of the others; 5% expected with no
  pattern). `anatomy`'s own table has a plane beating shuffles in 32.5% of deaths against 11.9% on a living face,
  which the report's "no hole, no front, no band" passes over. The crash is simultaneous; the dozen cells it
  leaves are clumps, and where the clumps sit shows in the order of the last deaths.

## 3. A hull face of 63 cells: 281,631 deaths [measured here]

`data/hull63.txt`, `data/rimtest.txt`.

- Living face: mean 31.253 (0.4961·A), s.d. 5.242; lag-1 and lag-2 autocorrelations **+0.517 and +0.340** (wrapped:
  +0.136, −0.031): its population is a slow variable. P(population ≥ 45, 48) = 3.1 × 10⁻³, 3.0 × 10⁻⁴: it is
  over-full 0.63 times as often as the wrapped face, not never. A generation with ≥ 48 cells was preceded by one
  with 36.8 (it builds up), and is followed by one with **29.91** (at most a quarter of the face 0.08% of the
  time).
- Dying face by lag 1, 2, 4, 6, 8, 12: 0.052, 0.114, 0.315, 0.511, 0.678, 0.876 of the mean. The share of deaths
  with ≥ 45 cells at one lag is at most 0.75% (lag 8), twice the ordinary 0.31%; on the wrapped face it reaches 17%.
- Single deaths (84,000): a generation ≥ 0.746·A in the window in 2.4% of deaths (0.9% of ordinary windows);
  largest fall ≥ 0.3·A in 27.5%, ≥ 0.4·A in 6.9%, **≥ 0.5·A in 1.14 ± 0.04%**. Launch 37.37 = 0.593·A; mean from the
  launch on: 37.4, 22.3, 17.3, 14.4, 11.9. **From the launch to the empty face: median 10 generations** (quartiles
  7–14; 5–95%: 5–20).
- Falls of ≥ 0.5·A: 1.955 × 10⁻⁶ per face-generation, 69 times rarer than on the wrapped face; 1 in 143 is fatal.
- Dying cells in the window: 49% overcrowded, 51% starved (53% starved from the launch on; ordinary time 39%).
- A plane fitted to the last-alive generations beats 95% of shuffles in 72.6% of deaths; s.d. of the last-alive
  generations 2.61; the halves' largest falls coincide in 39%.
- **Why it does not bust** (`python3 research/audit/blast/rimtest.py hull_11 hull63_s21 48`; 3,216 non-fatal
  generations with ≥ 48 cells, against 2,826 on the wrapped face). Neighbours inside the vessel: 30 cells with 9, 30
  with 7 (the rim row), 3 with 4 (corners).

  | cells | occupancy in the over-full generation | live cells with ≥ 6 live neighbours | live cells alive next generation |
  |---|---|---|---|
  | wrapped face, all 63 | 0.772 | 0.659 | 0.333 |
  | hull face, the 30 interior | 0.755 | 0.651 | 0.342 |
  | hull face, the 30 of the rim row | 0.816 | 0.306 | 0.661 |
  | hull face, the 3 corners | 0.513 | 0 | 0.846 |

  The interior of a hull face busts exactly as a wrapped face does. Half the face is rim row and keeps two thirds
  of its cells; the face is at 30.1 cells one generation later where the wrapped face is at 20.1. Not checked: a
  larger hull face, where the rim row is a smaller share (about a third at 135 cells).

## 4. A tube against a wide torus at 84 cells [measured here]

`data/tube84.txt`, `data/wide84.txt`, `data/estimator.txt`. Both on gump, 2,831 and 2,263 natural deaths (the
session had 111 and 109 at this size).

| | wide (1,4),(0,28) | tube (1,12),(0,28) |
|---|---|---|
| living mean; lag-1 autocorrelation | 43.473; +0.124 | 43.296; +0.165 |
| ln frequency of a face ≥ 0.74·A | −8.2498 | −8.2325 |
| one-generation falls of ≥ 0.5·A per face-generation | 1.569 × 10⁻⁵ | 1.623 × 10⁻⁵ |
| deaths per face-generation | 2.402 × 10⁻⁸ | 3.005 × 10⁻⁸ |
| launch | 0.7375·A (s.d. 4.47) | **0.7263·A** (s.d. 5.33) |
| launch to empty, median (quartiles) | 6 (5–8) | 6 (5–9) |
| deaths with a fall of ≥ 0.5·A / ≥ 0.4·A in the window | 0.593 ± 0.010 / 0.837 ± 0.008 | 0.532 ± 0.009 / 0.775 ± 0.008 |
| cells dying in the fall after the launch that are overcrowded | 99.2% | 99.1% |
| halves crash in different generations (report's definition) | 0.072 ± 0.005 | **0.135 ± 0.006** |
| at least one quarter busts locally | 0.939 | 0.967 |
| chance of death once ≤ 1, 2, 3, 4 cells are left | 0.842, 0.627, 0.420, 0.278 | 0.856, 0.627, 0.421, 0.276 |
| the report's estimator | 17.573 | 17.556 |
| ln τ_face here | 17.544 ± 0.021 | 17.320 ± 0.019 |

- **The living tube is over-full as often as the living wide face** (1.7% more often at ≥ 0.74·A; −ln P(population =
  64) = 10.260 against 10.282), and falls of half the face are 3.4% more frequent. The end-game is the same (q
  equal to 0.01). **The whole of the tube's 0.224 ± 0.028 is between the launch and the last few cells**, as the
  report says.
- The tube's extra deaths are of both kinds. Deaths that hold a face-wide fall of ≥ 0.5·A are 1.12 ± 0.04 times as
  frequent on the tube; deaths that do not, 1.44 ± 0.06 times (with 0.4·A: 1.16 ± 0.04 and 1.72 ± 0.11). So 29% of
  the extra deaths hold a face-wide half-fall and 71% do not (53% and 47% with 0.4·A).
- On gump at 84 cells the halves of a tube crash apart about twice as often as the halves of a wide face (0.135
  against 0.072; the report had 0.17 ± 0.04 against a wide value known only at 63 cells and on the surrogate), and
  the tube launches lower and from a broader hump. That is consistent with "sections out of step" and is all that
  gump itself says about it: every statement about 108 to 192 cells is on the surrogate.
- The estimator of finding 4c reproduces the wide face (17.573 against 17.544 ± 0.021 here and the anchor 17.5387)
  and returns the same for the tube (0.236 too high). On hull faces it gives 13.628, 17.792, 22.570 at 63, 84, 108
  cells against 13.633, 18.141, 23.339: the agreement at 63 cells is an accident. Its ν is log-interpolated between
  two whole numbers of cells, which matters (one cell of threshold is a factor 2.2 at 63 cells).

**Does a bust explain why a tube is cheaper, and why its price falls with length?** The report does not reach
that. It establishes where the discount is not (the living state, the over-full generation, the last cells) and so
where it is; it then conjectures that freedom of timing between sections multiplies the rate. Its own test of the
simplest form of that (block 4) came out 1.4 to 1.6 times the discount it compared with, on a statistic that
moves by a factor three with the definition of a crash.

## 5. The GTX 1080 study (`research/dying2/`, `research/dying2/hull/`)

`python3 research/audit/blast/dying2_cmp.py` → `data/dying2_cmp.txt` sets its tables by lag beside this audit's.

- **It shows what the report says it shows.** Four generations before death its 90th percentile is 1.442, 1.426,
  1.432, 1.395 of the living mean on W63, E84, T84, T96 (47.0, 62.0, 62.0, 69.0 cells; 0.746, 0.738, 0.738, 0.719 of
  the face) where the living 90th percentile is 1.16–1.20 and the dying median 0.18–0.34; on the hull faces the
  95th percentile at lags 1–12 never passes 39 of 63 and 52 of 84 cells, the living value. All recomputed from its
  CSVs.
- **And this audit's code reproduces its tables.** W63: mean/P̄ at lags 1, 2, 3, 4, 6, 8, 12 there 0.052, 0.131,
  0.323, 0.567, 0.776, 0.894, 0.977, here 0.052, 0.132, 0.328, 0.568, 0.785, 0.899, 0.980; 90th percentile at lags
  4, 6, 8, 12 the same cell (47, 44, 40, 39). Hull R = 11: mean/P̄ equal to 0.005 and the 95th percentile the same
  cell at all nine lags. T84 and the 84-cell wide face likewise within their errors. Layer beneath at lag 2: 0.55
  there, 0.558 here.
- **What its tables cannot show**: the share of deaths that pass through an over-full generation. A quantile at
  one lag sees only the deaths that are over-full at that lag (12.5% at lag 4 with ≥ 47 of 63 cells); over the last
  12 generations it is 51% (and 71% with ≥ 45). The agreement of its 0.746, 0.738, 0.738 with the launch level
  0.738 is a consequence of that tail, not a second measurement of the launch.

**The chance of death once k cells are left: the two definitions agree, and the difference is real.**

- Both studies define a dip as the stretch from the first generation below U cells (after one at or above U) to the
  next at or above U, U = P̄ rounded up, and q(k) = deaths / (deaths + recovered dips with minimum ≤ k). They differ
  in soup density (0.4, 0.35) and in the age from which they count (512, 200).
- `fd.c` tallies the same quantity on both vessels with one soup (0.4), one age (1,000) and U = 32 and 33 at once
  [measured here; 146,982 wrapped and 174,683 hull deaths; U changes nothing in the fourth digit]:

  | k | 1 | 2 | 3 | 4 | 5 |
  |---|---|---|---|---|---|
  | wrapped 63 here (the 1080's W63) | 0.8601 (0.860) | 0.6431 (0.641) | 0.4445 (0.447) | 0.3006 (0.304) | 0.1996 (0.201) |
  | hull 63 here (the 1080's R = 11) | 0.7709 (0.769) | 0.5024 (0.499) | 0.3003 (0.298) | 0.1816 (0.180) | 0.1081 |
  | wide 84 / tube 84 here | 0.842 / 0.856 | 0.627 / 0.627 | 0.420 / 0.421 | 0.278 / 0.276 | 0.181 / 0.180 |

  So the gap is not the recorder, the soup or the threshold. The report's sentence that "the chance of death does
  not depend on the face" holds inside each family and not between them: a hull face down to k cells dies 0.90,
  0.78, 0.68, 0.60 times as often as a wrapped one at k = 1 … 4. At 63 cells ln(0.3006 / 0.1816) = 0.50, the whole
  of the difference between the two lifetimes (0.47), as `anatomy` found; q does not move with size in either
  family, so this is a constant factor and no part of a price per cell.
- **It is not the bust.** Split by whether the dip held a one-generation fall of ≥ 0.4·A:

  | | deaths | q(1) | q(2) | q(3) | q(4) |
  |---|---:|---|---|---|---|
  | wrapped 63, dips with such a fall | 82,072 | 0.861 | 0.648 | 0.453 | 0.311 |
  | wrapped 63, dips without | 16,295 | 0.862 | 0.630 | 0.411 | 0.261 |
  | hull 63, dips with such a fall | 9,070 | 0.768 | 0.507 | 0.312 | 0.199 |
  | hull 63, dips without | 107,385 | 0.771 | 0.502 | 0.299 | 0.180 |

  A bust makes the same remnant deadlier by a factor 1.03 to 1.20 on either vessel (the report's 1.41 is for
  another definition); the vessel makes it deadlier by 1.3 to 1.6.
- **It is not the shared rim row.** Dips that came down to exactly one live cell, by where that cell is: wrapped
  face 0.8002 ± 0.0020 end in death; hull face, cell in the interior (9 neighbours) 0.6861 ± 0.0029, in the rim row
  (7) 0.6927 ± 0.0027, at a corner (4) 0.836 ± 0.031. An interior last cell of a hull face recovers as often as a
  rim one, and more often than the last cell of a wrapped face.
- What does differ under a nearly empty face: the layer beneath it holds 0.56–0.59 of its ordinary population at
  lags 2 and 1 on the wrapped face and 0.70–0.73 on the hull face (the third layer 0.83–0.89 and 0.95–0.96). Not
  tested as the cause.

## 6. Scored against the 120-cell tube: 24.5086 ± 0.0169 (8 runs, 3,494 deaths)

| forecast in the report | value | measured − forecast | in combined errors |
|---|---|---|---|
| PI, block 0 | 24.56 ± 0.03 | −0.051 | −1.5 |
| `tube1d` | 24.563 ± 0.030 | −0.054 | −1.6 |
| `model` | 24.575 ± 0.025 | −0.066 | −2.2 |
| `rigour` | 24.570 ± 0.025 | −0.061 | −2.0 |
| `split-slab`, bookkeeping | 24.59 ± 0.05 | −0.081 | −1.5 |
| `split-slab`'s surrogate, for gump (its referee's pool) | 24.60 ± 0.07 | −0.091 | −1.3 |
| the surrogate chain itself (its referee) | 24.63 ± 0.05 | −0.121 | −2.3 |
| `tube1d`'s one-curve fit, K = 2 / K = 1 | 24.571 / 24.608 | −0.062 / −0.099 | −3.7 / −5.9 (the measurement's error) |
| the line through 84, 96, 108 cells (recomputed here) | 24.5892 ± 0.0098 | −0.081 | −4.1 |

What the miss says:

- **Nine forecasts, nine high, by 0.05 to 0.12.** The first five are one extrapolation, as the report says. Each
  assumes that the tube's local price has nearly stopped falling (0.2019, 0.2013 from 84 to 108 cells). The chord
  from 108 to 120 cells is **0.1957 ± 0.0016**.
- **The one-curve fit and its asymptote are contradicted.** With c∞ = 0.2004 and ξ = 1.95 the form a + sL − ln(1 +
  K·e^(−L/ξ)) puts the chord from 9 to 10 units at 0.2007–0.2014 for K = 1, 2, 3 and approaches 0.2004 from above.
  The measured chord is 3 errors below the asymptote itself. So is `tube1d`'s "it levels at 0.199–0.202", and its
  power law (p = 0.75, c = 0.194) gives 0.2006 at this length. "The discount is 0.0046·L²" fails the same way
  (0.00460, 0.00472, 0.00481, then 0.00544). The emptiness relation (a band of a living tube against a closed
  tube) was measured to 7 units and is untouched as a measurement; as a law for tubes of 10 units it predicted
  wrongly.
- **The surrogate does not follow gump here.** Six layers of rule over two of coins read 24.63 ± 0.05 where gump is
  24.509 ± 0.017: +0.12 ± 0.05, against the offset of +0.01 to +0.05 it was calibrated with at 84–108 cells. Its
  referee had warned that this estimator can only come down as rare replications arrive. Either way the readings
  it gives for longer tubes (144 and 192 cells: 38.85 ± 0.12, the shares of staggered crashes) are statements about
  the chain, and at 120 cells the chain is not gump to its quoted error.
- **It does not test the bust.** How a face dies and what a tube of ten units costs are separate claims; the first
  is confirmed above, the second was never derived. One observation, after the fact and no more than that: the
  chord implies a discount of 0.0129 ± 0.0016 per cell against the wide price, which is the size of the report's
  timing statistic (0.0136 ± 0.0021 per cell for sections of two units on the 192-cell surrogate tube) that it
  scored as failed because it then compared it with 0.008–0.010. That statistic ranges from 0.007 to 0.03 with the
  definition of a crash, so this is not a confirmation.
- The 120-cell value rests on one code and one lattice (the lead's check, `CHAIN3B-DYING2-CHECK.md`).

## 7. The surrogate and the proofs

`python3 research/audit/blast/dice.py` (3 s) → `data/dice.txt`: a dense solver written here (the kernel built
cell by cell on all 2^A states, power iteration, the bust share by powers of the kernel with the half-face falls
deleted), on graphs from this audit's `geom.py`.

| face (cells) | ln τ here | `rigour` | bust share here | `rigour` | ⟨E⟩₁ ≤ ln τ ≤ ⟨E⟩₀ |
|---|---|---|---|---|---|
| hull triangle R = 3 (9) | 2.4837157463 | 2.4837157463 | 0.0170 | 0.0170 | 0.73 ≤ 2.48 ≤ 8.62 |
| torus (1,1),(0,3) (9) | 2.6946266059 | 2.6946266059 | 0.9369 | 0.9369 | 0.83 ≤ 2.69 ≤ 9.02 |
| torus (1,0),(0,3) (9) | 3.3935247191 | 3.3935247191 | 0.6466 | | 1.42 ≤ 3.39 ≤ 7.19 |
| torus (2,0),(0,2) (12) | 3.9818365883 | 3.9818365883 | 0.5675 | 0.5675 | 1.37 ≤ 3.98 ≤ 10.08 |
| torus (1,1),(0,4) (12) | 3.7118338988 | 3.7118338988 | 0.7909 | 0.7909 | 1.12 ≤ 3.71 ≤ 10.91 |
| torus (1,0),(0,4) (12) | 4.1330124063 | 4.1330124063 | 0.4466 | 0.4466 | 1.63 ≤ 4.13 ≤ 9.10 |
| 2D relative, ring of 12 over two coins | 6.4169049205 | 6.4169049205 (`toy`) | 0.9560 | 0.9560 | |
| 2D relative, segment of 12 | 7.7401917480 | 7.7402 | 0.7046 | 0.7046 | |

- **The exact numbers are right** (three codes now: theirs, their referee's, this one).
- **The tilt identity is right and elementary**: with a product kernel, P(x → empty) = e^(−E(x)), so h = Σ μ e^(−E) and
  ln τ = −ln⟨e^(−E)⟩_μ; the integral form is the derivative of that in s (checked to ten digits on six faces). Its
  two bounds are loose by a factor 2.5 to 3.5 on either side at 9 and 12 cells. It holds for the surrogate
  because the surrogate has private coins; nothing of it is known for gump.
- **"The same two exits" is a fair reading with three limits**, all in the session's own files: the faces are 9 to
  18 cells exact (to 36 by simulation), where "half the face" is 5 to 9 cells; the surrogate outlives gump's
  wrapped faces by 1.8 to 2.6 nats and its rimmed faces are shorter-lived than its wrapped ones unless the rim is
  given coins of face density, the reverse of gump; and a wrapped tube one unit cell round has a low bust share
  (0.45 at 12 cells here), so the variable is whether cells can be overcrowded, not wrapping. What it does show:
  the two exits need no chaos beneath.
- Theorem 3 and the seam identity: read, not rebuilt; no error found in what is marked proved; neither says
  anything about gump's prices.
- `model/`: its law of the over-full face, −ln P(population = xA) = 1.9 + ψ(x)·A, is reproduced at x = 0.762 from
  this audit's histograms at 63 and 84 cells (8.165 and 10.282: ψ = 0.1008; its table interpolates to 0.0995), and
  "the same on tubes and wide faces to 0.001 per cell" holds at 84 cells (0.0003). Its fits of lifetimes: not
  examined.

## 8. What the lead could enter in the ledger, and how well each is verified

1. **A wrapped face of 63 or 84 cells dies through one over-full generation and a crash.** From an ordinary
   generation (33 of 63) it fills in one step to 0.738·A with at least five layers beneath it over-full, 99% of the
   cells that then die are overcrowded, about 0.2·A is left, and the face is empty a median 5 to 6 generations
   after the launch. 80% of deaths hold a one-generation fall of 0.4·A, 55–59% one of half the face; one hump.
   *Verified:* four codes of the session, its referee, and this audit's rebuild from the oracle (234,823 deaths at
   63 cells, 2,263 and 2,831 at 84); the 1080's tables by lag agree with the rebuild to the cell. Sizes seen on
   gump: 48 to 84 cells. Nothing above 84 cells is on gump.
2. **A hull face of 63 cells does not: it fades over a median 10 generations** (1.14% of its deaths hold a fall of
   half the face; such falls are 69 times rarer than on the wrapped face and as deadly). **Its interior cells are
   overcrowded in an over-full generation as a wrapped face's are; its rim row, with 7 neighbours inside the vessel
   against 9, is not, and survives twice as often.** *Verified:* the session's codes and referee; this audit
   (281,631 deaths; the cell-class table is this audit's alone, one code). One size.
3. **A bust is usually survived**: 1 fall of half the face in 128 is fatal at 63 cells, 1 in 1,100 at 84. *Verified:*
   this audit and the session at 63 cells; this audit alone at 84.
4. **At 84 cells a loop-12 tube is over-full as often as a wide face (within 2%) and dies 1.25 times as often; the
   end-game is the same; the halves of the tube crash in different generations in 13.5% of deaths against 7.2%.**
   *Verified:* this audit (two faces, one code); the first two parts also by the session and by the 1080's study.
5. **Once k cells are left a hull face dies less often than a wrapped one (0.77, 0.50, 0.30 against 0.86, 0.64,
   0.44), under one definition; neither a bust nor the shared rim row accounts for it.** *Verified:* the totals by
   three codes (the 1080's two recorders, this audit's); the two exclusions by this audit alone, at 63 cells.
6. **The one-layer dice surrogate, solved exactly, has both exits** (bust share 0.57–0.94 on wrapped faces of 9–15
   cells, 0.003–0.02 on rimmed ones). *Verified:* three codes for the rows above. A statement about a surrogate.
7. **Not for the ledger as results:** the tube's asymptote 0.2004 and the K = 2 curve (contradicted at 120 cells);
   0.0046·L²; the emptiness relation as a law beyond 7 units; staggered crashes beyond 84 cells and the 192-cell
   values (surrogate, off by 0.12 ± 0.05 at 120 cells); "0.079 + 0.136" as the parts of the price (a description
   at one threshold); the living-state estimator beyond 108 cells and anywhere off wide tori; the 135-cell
   forecasts; "no hole, no front, no band" without the qualification of §2.

## 9. Not checked

- Anything above 84 cells on gump; the 48-, 57- and 75-cell faces; any tube but (1,12),(0,28).
- The table of failure by cluster size; "three quarters of the price is static"; the two-layer map; the estimator at
  126–192 cells; `model`'s fits.
- `rim/` (strips), `split-hull/` and `ref-hull/` (dip rates, the 135- and 165-cell forecasts), the dice chains
  under six layers and their samplers, `tube1d`'s bands, `image`'s measurements, the 2D relative by brute force,
  the PI's scoring of its own forecasts.
- Whether the fuller layer beneath a nearly empty hull face is what makes its remnant recover (§5).
- In this audit's own code: lanes 1–511 against the oracle directly (lane 0 only; the four lifetimes within 1.3
  errors of their anchors are the end-to-end check); errors on shares are binomial, with no account of deaths
  sharing a replica; the first 4,000 records of each vessel carry the shuffle tests.
