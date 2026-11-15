# How a hull face dies: c1, csz, c2v, D2h at R = 11 cube-centred (A = 63)

2026-11-15. Follow-up to `research/theory/symmetric/` (the edge ladder: ln τ_face 13.634, 11.456, 9.291, 7.168 for
0, 1, 2, 3 edges of a face shared with a face in lockstep). That study read the ladder as "an asymmetric face is held
up along each edge by an independently living neighbour face". Here the faces were looked at in the generations
before they die. Forecasts and every definition: `PREDICTIONS.md` (committed 75e5212 before any run). Tags:
**[measured]** (number, error, command), **[conjectured]**.

## Reviewed (2026-11-15)

An adversarial review, `research/audit/REVIEW-dying.md` (round 1 part), reran the study with its own stepper
(`research/audit/dying/dy.c`: the full, unreduced system, events every generation, a Brent settled test, matched to
`reference/oracle.py` at every generation on twelve systems) on fresh seeds. Commands: `bash
research/audit/dying/plan.sh 1`, `2`, `3`, then `python3 research/audit/dying/ana.py` (→ `ana_out.txt`; every
review number below unless marked). Ledger: CLAIMS DY1–DY3.

**Confirmed:** the mean curves and plunge medians (6, 6, 7, 7), the rim-row depletion to three digits, no edge going
first, the neighbour numbers, and every forecast score (definitions fixed before the data).

**What the review changed, applied below** (each place is marked "corrected 2026-11-15"):
1. The stationary population does **not** fall in equal steps: −2.35, −2.62, −2.77 cells per tied edge (review),
   growing along the ladder while the ln τ steps (−2.18, −2.17, −2.12) do not. The "mirroring" of the ln τ ladder is
   withdrawn. What generalises is the loss per tied *rim cell*, the same at R = 11 and 13.
2. "Fades everywhere at once" is true of the **mean** face only. Single deaths are uneven: at half population a third
   (32–39%) are more lopsided than 95% of equally thinned stationary faces (9–11% in a control 64 generations
   earlier), with no preference for the tied edge.
3. The neighbour effect is real only in the neighbour's **own row 2** along the shared edge (0.56–0.61 of
   stationary); the rest of the neighbour stays at 0.95. The band (0.21) and whole-face (0.77) figures include the
   shared rim row, whose 12 cells are the dying face's own.
4. ln τ is not a function of the mean population: a cell lost at a tied edge costs 0.64–1.00 in ln τ, a cell gained
   by growing the untied face buys 0.40, one gained by re-centring 0.23. (The reading "0.86 per live cell, twice the
   0.436 per live cell of the untied face", which was the lead's and not this README's, is withdrawn: 0.436 is an
   average, ln τ/P̄, not a marginal.)
5. The lag-4 band/interior ratios mean something only over the same ratio of the stationary state; they are now
   given that way beside the raw ones. The 16-cell band includes corner cells, and the first "against the reading"
   criterion flips with the band.
6. The D2h stationary values leave out the lives that settle (36.5% of old living D2h states in the review; 27% of
   exposure here), which the ln τ rung counts.

## Short answer

- **[measured] On average a death is a fast collapse of the whole face, and the mean face keeps its stationary
  profile.** In every
  group the face is at its stationary population until about 20 generations before death (c1: 0.98 of P̄ at lag
  20, 0.95 at lag 16, 0.67 at lag 8, 0.31 at lag 4); it falls from half its stationary population to empty in a median
  of 6–7 generations. Measured against its own stationary value, every band and the interior empty together within a
  few per cent at every lag (figure panel B). The rim rows linger slightly at the very end (lags 1–4, by 7–16% relative
  to the interior), and they do so *as much on a tied edge as on a free one*. *Corrected 2026-11-15 (review): this is
  the mean. Single deaths are uneven: at half population 32–39% of them are more lopsided than 95% of stationary
  faces thinned at random to the same count (9–11% in a control 64 generations earlier). The depleted side is set
  early, wanders a little more than thinning alone would make it, and is not the tied edge.*
- **[measured] What a tied edge changes is the stationary face, not the dying.** The shared rim row of a tied edge
  is depleted at all times: stationary occupancy 0.51 on a free edge (c1), 0.35 / 0.32 / 0.30 on a tied edge in csz /
  c2v / D2h; row 2 is depleted less (0.43 → 0.39 / 0.37 / 0.34), row 3 a little (panel C). The face's stationary
  population falls by 2.35, 2.62, 2.77 cells per tied edge (review: P̄ = 31.25, 28.90, 26.28, 23.50 ± 0.004–0.02;
  this study 31.29, 28.83, 26.29, 23.77 ± 0.03–0.15). The steps grow along the ladder; the ln τ steps (−2.18, −2.17,
  −2.12) do not. *Corrected 2026-11-15 (review): this README first said "falls in equal steps … as equal as the ln τ
  steps"; this study's own errors (steps 2.46 ± 0.05, 2.54 ± 0.08, 2.52 ± 0.17) could not show that, and the review's
  steps are not equal.* What does generalise is the loss per tied rim cell: the rim row loses 0.148, 0.167, 0.185 per
  tied rim cell at R = 11 and 0.149, 0.167, 0.186 at R = 13 (the whole face 0.19–0.22), so the loss per tied edge
  grows with the rim's length. "Almost all in the rim row" holds cube-centred only; vertex-centred faces (R = 12)
  carry it on rows 1 and 2. The D2h value leaves out lives that settle (see the D2h caveat under the numbers table).
- **[measured] In c1 the living neighbour does not hold the edge up; its own row next to the edge is dragged down.**
  The adjacent face's band along the shared edge falls with the dying face's own (0.71 of stationary at lag 8, 0.42
  at lag 4, 0.21 at lag 0), and the whole neighbour face loses 23% of its population by lag 0. *Corrected 2026-11-15
  (review): adjacent faces share their rim row (the same 12 cells), so the band's 16 cells hold 10 of the dying
  face's own cells, empty at lag 0 by definition, and 17.5 of the whole face's 23.5 points of loss are those shared
  cells. What survives is a local drag: the neighbour's own row 2 along the edge (6 cells) falls to 0.56–0.61 of
  stationary (0.613 at lag 0, 0.559 at lag 1), and the rest of the neighbour stays at about 0.95.* Free neighbours in
  csz and c2v behave the same (row 2 at 0.52–0.57; review).
- **So:** the pictures do not show the dynamical form of the reading (free rims outlasting the interior because a
  live neighbour feeds them; tied rims going first). They are consistent with a static form of it **[conjectured]**:
  a face sharing an edge with its lockstep partner has a thinner rim at all times (its rim cells see pairs of equal
  states, so their counts move in steps of 2), sits closer to empty, and so needs a smaller fluctuation to die. Nothing
  here measures that this is the *cause* of the −2.17 per edge, and the mean population alone cannot be the cause:
  ln τ is not a function of P̄ (review: a cell lost at a tied edge costs 0.64–1.00 in ln τ, a cell gained by growing
  the untied face from 63 to 84 cells buys 0.40, one gained by re-centring at equal area 0.23; the vertex-centred csz
  face has more live cells, 31.60, than the cube-centred untied one, 31.25, and lives 1.45 shorter in ln τ).

## What was measured

Systems `oct_11_c_{c1,csz,c2v,d2h}` (`research/theory/symmetric/geom.py`). Runs: the symmetric study's own tabulated
jobs, same seed and length (c1 s1 600,000; csz s1 400,000; c2v s1 200,000; D2h s2 400,000 generations × 512
replicas, soup 0.4, checks every 4), stepped by `sd.c`, a copy of `research/theory/symmetric/sy.c` that adds a ring
buffer of each replica's last 512 generations and writes it out at a death, plus null-control samples. Deaths used:
every F/X life at age > 512 generations, first 3,000 per run (c1: all 2,930). Faces are put in one canonical frame
(the +++ face, p → σ⊙p); the "band" of edge a is rows 1–2 along it (16 cells, apexes excluded), the interior the 18
cells with min(x, y, z) ≥ 2; lag ℓ is ℓ generations before the first generation with the face empty (found to the
generation from the history). Null control: states sampled at fixed times in lives older than 512 generations that
then lived at least 64 more generations and did not end settled (c1 36,720 faces, csz 18,044, c2v 8,238, D2h 1,815).

**What each number rests on.**
- `sd.c`'s lives file is **byte-identical** to the study's `research/scratch/symmetric/lives_oct_11_c_G_sN.bin` for all
  four runs (`cmp`), so every death time is the one `run.py` counted; `analyze.py` checks that each dumped history is
  the n-th F/X late life of that file with the same age, in order.
- From each history the death generation is found and checked to lie inside the last check interval with no face
  empty one generation earlier (all 11,930 histories pass; `load.py` asserts it).
- 48 histories (12 per group, spread over each dump) were stepped by the Rust engine (`gump run`, full symmetric cell
  set, open space) for 511 generations: the population matches at every generation and the final cell set matches
  the history's state at the check (`validate.py` → `ALL OK`).
- Everything else is counting on those arrays (`load.py`, `analyze.py`, `explore.py`). Errors are bootstrap over
  deaths (1,000 resamples) or binomial.

## Forecasts, scored

The ratios of L2–L4 are raw (band over interior at lag 4); the forecasts were stated that way and are scored that
way. What they mean is the ratio over the same ratio of the stationary state, given in square brackets: the
16-cell band includes the two cells at each end next to the corner, which have low stationary occupancy and pull
every raw ratio down by about 0.12. *Added 2026-11-15 after the review*, which also scored each forecast with a
12-cell band without the corner cells (`ana.py`, "band/interior ratio at lag 4").

| | said | found [measured] | |
|---|---|---|---|
| L1 | death is an event of the whole face (deduction from the ladder) | the mean face collapses together, relative to its stationary profile, within ~20 generations (single deaths are uneven, see the short answer) | consistent (not a numerical forecast) |
| L2 | c1 band/interior ratio at lag 4 ≥ 1.5 | 1.076 ± 0.018 (x 1.061, y 1.074, z 1.092); stationary 0.924 ± 0.002 [over stationary 1.16; review 1.11–1.20 by edge, 1.13–1.24 with the 12-cell band] | **failed** (review: failed with either band, raw 1.063 and 1.222) |
| L3 | csz tied ratio < 1.2, free/tied ≥ 1.3 | tied 0.810 ± 0.017 (held); x/z 1.164 ± 0.027, y/z 1.153 ± 0.027 [over stationary: tied 1.16, free 1.07] | **failed** (second part). Stationary: tied 0.700, free 0.880, free/tied 1.26 already (review: failed with either band) |
| L4 | D2h ratio in 0.8–1.2 on all edges | 0.715, 0.721, 0.697 ± 0.017 [over stationary 1.16; review 1.16–1.24] | **failed** (stationary 0.61–0.62). Review: with the 12-cell band 0.790 ± 0.028, 0.801, 0.843, so **undecided** under the registered rule (flips within 1σ) |
| L5a | c1 neighbour population within 10% of P̄, lags 1–16 | 0.893 ± 0.001 | **failed**, narrowly (0.98 at lag 16, 0.82 at lag 4, 0.77 at lag 0). Caveat (review, 2026-11-15): decided partly by the shared rim row, which is the dying face's own; without those cells the neighbour's mean is 0.951 and L5a would hold |
| L5b | c1 neighbour band on the shared edge within 15%, lags 1–16 | 0.668 ± 0.003 | **failed**. Same caveat: 10 of the band's 16 cells are the dying face's; on the neighbour's own row 2 alone the mean is 0.778, still a failure |
| L6 | csz: emptying begins nearest the tied edge in 45–70%; c1 one third each | csz 0.211 ± 0.007; c1 0.338, 0.330, 0.332 ± 0.009 | csz **failed**; c1 held (forced by symmetry: a code check) |
| L7 | median plunge shrinks ≥ 25% from c1 to D2h | c1 6, csz 6, c2v 7, D2h 7 generations (quartiles 4–8, 4–9, 4–11, 4–12); D2h/c1 = 1.17 | **failed** (the plunge does not shrink; the run-up lengthens) |
| "against the reading" | c1 ratio below 1.1; csz no tied/free difference | 1.076 ± 0.018 (below 1.1 by 1.3σ); csz raw ratios differ (0.81 vs 0.94) but relative to stationary the tied band lingers *more* (1.16 vs 1.07) | first criterion met; second met only after normalising by the null. *Review, 2026-11-15: the first criterion is met only because of the corner cells; with the 12-cell band the c1 ratio is 1.222 and it is not met* |
| K1 (mine) | L5b fails, L5a holds | L5b failed, L5a failed by 0.007 | half |
| K2 (mine) | L2 fails | 1.076 | held |
| K3 (mine) | c1 median plunge 8–64 | 6 | **failed** |
| K4 (mine) | D2h ratio < 1 on all three edges | 0.70–0.72 | held (but it is the stationary 0.61 with a slight late excess, not an early rim death) |

L6 caveat: the pre-registered centroid weights the deficit by ρ_i − x_i, so a face emptying in proportion to its
stationary profile has its centroid pulled away from a depleted (tied) edge; csz's 0.211 partly measures that. The
version added afterwards (which band has the largest deficit relative to its own stationary value at t_h;
`explore.py`, the stationary band value pooled over edges of one kind so that equal counts tie and ties break at
random) gives csz tied 0.290 ± 0.008, free 0.366, 0.344; c1 0.335, 0.337, 0.328 ± 0.009 (equal, as symmetry demands);
mean relative deficit at t_h in csz 0.548 on the tied band against 0.61 on the free ones and 0.69 in the interior.
Either way emptying does not begin at the tied edge; if anything the tied band is the last to go, relative to its
(already low) stationary value.

## Numbers behind the pictures [measured]

Command: `python3 research/dying/analyze.py` (L2–L7, tables; ~30 s) and `python3 research/dying/explore.py`.

| | c1 | csz | c2v | D2h |
|---|---|---|---|---|
| stationary face population P̄ | 31.29 ± 0.03 | 28.83 ± 0.04 | 26.29 ± 0.07 | 23.77 ± 0.15 * |
| P̄, review (`ana.py`) | 31.25 ± 0.004 | 28.90 ± 0.01 | 26.28 ± 0.01 | 23.50 ± 0.02 * |
| stationary band occupancy, free / tied | 0.483 | 0.459 / 0.364 | 0.436 / 0.338 | — / 0.316 |
| stationary interior occupancy | 0.522 | 0.520 | 0.516 | 0.514 |
| face at lag 16, 8, 4 (/ P̄) | 0.95, 0.67, 0.31 | 0.93, 0.65, 0.32 | 0.84, 0.57, 0.30 | 0.75, 0.52, 0.30 |
| live cells at lag 1 | 1.61 | 1.61 | 1.56 | 1.54 |
| lag-4 ratio over stationary ratio, free / tied | 1.16 | 1.07 / 1.16 | 1.08 / 1.10 | — / 1.16 |
| layer beneath (s = 9) at lag 4 / at lag 0 (/ own stationary) | 0.72 / 0.88 | 0.70 / 0.79 | 0.63 / 0.63 | 0.54 / 0.45 |

\* **D2h caveat (added 2026-11-15 after the review).** The stationary control leaves out lives that end settled.
None are found in c1 and csz and 1.2% of old living states in c2v, but in D2h 36.5% of old living states are in
settled lives (review, Brent test; 27% of exposure in this study's protocol), with 15.45 ± 0.07 live face cells.
Counting them, D2h's P̄ is 20.40 and its step is −5.76. Deaths come only from lives that do not settle, so the control
is the right comparator for the death curves; but the D2h rung of the ln τ ladder counts the exposure of settled
lives (its estimator spread 7.02–7.29 is that), so the D2h point of the P̄ ladder and the D2h rung of the ln τ ladder
are not taken over the same lives. Every D2h figure "over stationary" in this README carries this. Conditioning the
control on 64 more generations of life raises P̄ by < 0.01 (c1, csz), 0.03 (c2v) and 0.26 (D2h; 23.24 → 23.50), so
"relative to stationary" numbers are biased up by at most about 1%, and only in D2h (`ana.py`, "Null control").

- Co-deaths: two face orbits first empty in the same generation in 0 (c1), 1 (csz), 3 (c2v) of ~3,000 deaths.
- The layer beneath the face dips with it (c1 to 0.72 at lag 4) and partly recovers at the moment of death; the layer
  two below (s = 7) barely moves in c1 (0.96–1.14). With more tied edges the run-up is longer and deeper and reaches
  further in: in D2h, where all eight faces die together, the layers beneath are at 0.45 and 0.66 at death.

## What the pictures show (`research/figures/dying_face.png`)

Top: the mean canonical face, stationary and at lags 16, 8, 4, 2, 1, for the four groups, one log colour scale, tied
edges marked by an orange bar. Bottom: A, face population over its stationary mean against lag (and c1's neighbour);
B, csz and D2h bands and interior each over their own stationary value; C, stationary occupancy by row from a free and
a tied edge.

In plain words: a face does not erode from one side. On average it stays at its usual density until about twenty
generations before the end, then fades everywhere at once, reaching one or two scattered live cells a generation
before it is gone; the fade takes about as long as a signal needs to cross the face (one cube per generation, the face
is about six cubes across). *Corrected 2026-11-15 (review): "everywhere at once" is a property of the mean maps.
A single death is a fast, uneven collapse: its depleted side is set early and shifts a little as cells are reborn
(per death, cells on the rich side of the 0.75 P̄ state outlive those on the poor side, correlation 0.16–0.20), and
that side is not the tied edge.* The tied edges are visibly paler in every column including the stationary one: the
difference between a tied and a free edge is there all the time, not something that happens at death. The neighbour
of a dying asymmetric face loses its own strip next to the shared edge as the face dies (its row 2, to about 0.56 of
stationary; the shared row itself is the dying face's own; review, 2026-11-15). Panel A's dashed curve ("c1
neighbour: its band on the shared edge") is mostly the dying face's own rim. The more tied edges, the earlier the
fade starts (panel A); its last few generations look the same in all groups.

Surprises, and what would pin them down:
1. The final plunge does not depend on the symmetry (median 6–7 generations everywhere) while lifetimes differ by
   e^6.5. Whatever makes a tied face die sooner acts on how often a collapse starts, not on how it runs. A test: the
   distribution of the face population's excursions (how often P drops below, say, 0.7 P̄ and recovers) in each group
   from long stationary traces, against the ln τ ladder.
2. The stationary population falls by about 2.5 cells per tied edge while ln τ falls by about 2.17. Whether the
   ladder is a function of the stationary state (mean and width of P; c1 σ_P 5.24 → D2h 6.37) could be tested by
   the same comparison at A = 84, where the ln τ steps are −2.64, −2.65, −2.84. *Corrected 2026-11-15 (review):
   the population steps are not equal (−2.35, −2.62, −2.77 at A = 63; −2.64, −2.94, −3.59 at A = 84), so they do not
   mirror the ln τ steps, and at the level of the mean the answer is no: ln τ is not a function of P̄ (short answer,
   last bullet). Round 2 below takes up the mean and width together.*

## Not checked

- One size (A = 63) and one centring; nothing at A = 84 or vertex-centred, nothing for c2e (the rotated edge, where a
  mirror is absent) or O_h.
- The mechanism suggested for the tied-row depletion (paired counts) is not tested; nor whether the depletion causes
  the shorter life.
- The engine check covers 48 of 11,930 histories (511 generations each); the rest rest on the byte-identical lives
  files plus the same stepper code. No independent stepper (the review's `st.c`) was used.
- Only the dying face of c1 has its neighbours measured; in csz and c2v the free neighbours were not.
- Null samples of the symmetric groups exclude lives that end settled (27% of D2h exposure is in such lives; 36.5%
  of old living D2h states in the review's protocol), so the D2h null describes lives that go on to die, while the
  D2h ln τ rung it is set beside counts settled lives (caveat under the numbers table; added 2026-11-15).
- Lopsidedness of single deaths was measured by the review with one statistic (the distance of the live-cell
  centroid from the stationary profile's); other shapes of depletion were not tested for. The review did not
  recompute the layers beneath, the last-alive maps or the relative-deficit L6 (`explore.py`), and it ran deaths
  only at R = 11 cube-centred (its R = 13 and vertex-centred R = 12 numbers are stationary sampling). Its 1.7–1.8σ
  differences from this study in the csz and D2h populations and 2.7σ in L6 (0.236 ± 0.006 against 0.211 ± 0.007)
  are unresolved; the protocols differ (events every generation against every 4, Brent against ladder snapshots).
- Bulk histories (≈ 0.6 GB) are in `research/scratch/dying/` and not in git; the curated tables are in `data/`.

## Data (`research/dying/data/`)

`occupancy_by_lag.csv` (face population and band/interior/apex occupancy, lags 0–507 and the null, per group);
`occupancy_by_cell.csv` (each of the 63 canonical cells, null and lags 0–32 and beyond); `neighbour_c1.csv` (c1
neighbours by lag, over their null); `relative_by_lag.csv` (`explore.py`'s relative curves); `deaths.csv` (one row
per death sample: life index in the lives file, replica, age, check generation, j_d, face, t_h lag, centroid,
nearest edge, populations at lags 1 and 4).

## Reproduce

```sh
gcc -O3 -march=native -o research/scratch/dying/sd research/dying/sd.c
cd research/scratch/dying && S=../symmetric
for a in "c1 1 600000" "csz 1 400000" "c2v 1 200000" "d2h 2 400000"; do set -- $a
  ./sd $S/graph_oct_11_c_$1.txt run $2 0.4 $3 4 lives_$1.bin dump_$1.bin null_$1.bin 3000 512 512; done   # ~2 min
cmp lives_c1.bin $S/lives_oct_11_c_c1_s1.bin     # likewise csz s1, c2v s1, d2h s2 (graphs from run.py; ~0.6 GB of dumps)
cd ../../..
python3 research/dying/load.py        # canonical arrays (~1 min)
python3 research/dying/validate.py    # 48 histories against the engine: ALL OK
python3 research/dying/analyze.py     # forecasts L2-L7, tables, data/*.csv
python3 research/dying/explore.py     # relative curves, layers beneath, relative-deficit L6
python3 research/dying/figure.py      # research/figures/dying_face.png
```

(The graph files are written by `python3 research/theory/symmetric/run.py run oct_11_c_G …` or
`geom.py write oct_11_c_G FILE`.)

# Round 2: excursions, single deaths, births or deaths, A = 84 (2026-11-15)

Forecasts and definitions: `PREDICTIONS.md`, "Round 2" (committed 6d40e72 before any round-2 run). Fresh seeds
throughout. Figure: `research/figures/dying_excursions.png`. Tables: `data/r2_excursions.csv`, `data/r2_runup.csv`,
`data/r2_stationary.csv`. Commands at the end of this section.

## Reviewed (2026-11-15)

The round-2 part of `research/audit/REVIEW-dying.md` reran the excursions with its own stepper (`ex2.c`: round 1's
validated `dy.c` plus an online excursion table kept per life, so that settled lives can be put in or left out) on
fresh seeds, and reanalysed births, survival and lopsidedness from round 1's own death histories. Commands:
`bash research/audit/dying/plan.sh 4`, `5`, then `python3 research/audit/dying/ana2.py` (→ `ana2_out.txt`) and
`python3 research/audit/dying/ana2b.py` (→ `ana2b_out.txt`). Ledger: CLAIMS DY4–DY7. Every forecast score
reproduces; the definitions were fixed before the data.

**What the review changed, applied below** (marked "corrected 2026-11-15" where they fall):
1. **Every D2h quantity that involves exposure depends on how settled lives are treated:** ln τ_face is 7.32 with
   them (Brent detection), 6.86 without them, 7.168 with this study's ladder detection; likewise ln ν, q, p*, the last
   step of the ladder, the per-edge tail increments and the A = 63 D2h point of the fit.
2. **The lopsidedness claim splits by group.** In c1 dying faces are no more lopsided than chance-low ones, and at
   equal count less; in D2h they are more. "The same ratio" compared faces of different counts.
3. **The tail of ln ν** below about 0.45 P̄ is close to straight, not straight, with no break at half the mean;
   "5.5 + 3.4 per free edge" (the lead's reading, not this README's) holds for one window and one estimator only.
4. **Births fail first mostly because the face has fewer cells:** stationary births depend strongly on the face's
   own population and survival does not. The excess beyond that is smaller (c1 lag 8: 0.61 against 0.77 predicted).
5. **The (P̄, σ_P) fit:** leave-one-out residual 0.50; a form without σ fits as well; the D2h estimator moves it.
6. **The dip rates cross over:** at 0.9 P̄ the untied face dips most often and D2h least, the reverse of 0.7 P̄.

## Short answer

- **[measured] Ties change how deep a dip goes, not how often a dip starts, and the deciding passage is very late.**
  Excursions to 0.7 P̄ happen at nearly the same rate in all four groups (ln ν = −4.16, −3.80, −3.77, −3.74 per face
  per generation for c1, csz, c2v, D2h; review −4.164, −3.802, −3.779, and for D2h −3.883 with settled lives and
  −3.714 without). The groups separate only below about 0.6 P̄. *Corrected 2026-11-15 (review): shallower, the order
  reverses. At 0.9 P̄ the untied face dips most often and D2h least (ln ν = −2.31, −2.53, −2.62, −2.64 here; review
  −2.311, −2.527, −2.620, −2.785).* A face that has reached half its stationary population almost always recovers
  (q(0.5) = 0.0008 in c1, 0.107 in D2h). The point of no return (q = 1/2) is at p* = 0.08 P̄ in c1, i.e. about 2.5 live
  cells, and 0.12, 0.15, 0.25 P̄ for csz, c2v, D2h (review 0.079, 0.114, 0.152, 0.245; D2h 0.265 without settled
  lives). Every D2h figure here depends on the treatment of settled lives (see "What each number rests on").
- **[measured] The survivors at the start of the plunge are clumped, and so are those of any depleted face; whether
  dying faces are more clumped depends on the group.** Their centroid sits 1.61× (c1) and 1.76× (D2h) further from
  the face centre than for a stationary face thinned at random to the same count. Stationary faces whose population is
  low by chance (P ≤ 0.6 P̄) give 1.59 ± 0.04 (c1), 1.51 ± 0.06 (D2h; `round2_lowp.py`, added afterwards). *Corrected
  2026-11-15 (review): this README first called these "the same ratio" in both groups. In c1 they are close (review
  1.60 ± 0.02 against 1.53 ± 0.03). In D2h they are not (1.73 against 1.51; this study's own pair differs by 0.25). And the comparison is
  at different counts: about 16 live cells for chance-low faces against about 12 (c1) and 9 (D2h) for dying faces at
  t_h, and lopsidedness grows as a face thins. At matched count (5–9 live cells, `ana2b.py` part 3) dying c1 faces are
  less lopsided than chance-low ones (S = 2.47 ± 0.08 against 3.09; csz 2.41 against 2.97), dying D2h faces more (2.94
  ± 0.04 against 2.70).* So in c1 a depleted face is lopsided whether or not it then dies, and a thin face that keeps
  a clump tends to come back; in D2h lopsidedness does go with dying. The mean maps of round 1 hide all of this.
- **[measured] Births fail first.** On the dying face, births per empty cell are already 10% below stationary at lag
  16 (c1) while survival is 2% below. By lag 8 births are at 0.45 and survival at 0.88. Survival collapses only in
  the last 5 generations. With more tied edges the birth deficit starts earlier: D2h is at 0.93 already at lag 40.
  *Corrected 2026-11-15 (review): most of this is the face's own lower population. In stationary faces births per
  empty cell depend strongly on the face's population (0.60 of the mean rate at 0.6 P̄, 0.86 at 0.8 P̄, 1.15 at
  1.2 P̄) and survival does not (0.98–1.02), so any face that has lost cells already shows "births failing first".
  Measured against what its own population predicts, the dying face is still low, births more so: c1 at lag 8 births
  0.61 observed against 0.77 predicted, survival 0.89 against 1.00; at lag 16 births 0.927 against 0.968 (D2h 0.632
  against 0.698), survival 0.988 against 1.001.* The excess is what points to the surroundings (the layer beneath)
  thinning first.
- **[measured] At A = 84 a two-parameter function of the stationary state fits all eight lifetimes within 0.31.**
  The fit is ln τ = 3.43 + 0.582·P̄²/(2σ_P²). That is a fit with two free constants, not a derivation. *Corrected
  2026-11-15 (review; own fit 3.42 + 0.584): leaving each point out in turn, the worst prediction misses by 0.50
  (it predicts c1 at A = 84 as 18.33 against the GPU's 18.141). The competing forms: a + b·P̄/σ fits to 0.42,
  a + b·P̄ alone to 2.60, a + b·P̄ + c·σ to 0.47, and a + b·A + c·P̄, with no width in it, to 0.27 (leave-one-out
  0.50). The eight points form two clusters of nearly collinear rungs, so any form with a size term that orders them
  does almost as well. The worst point is always D2h at A = 63: with its lifetime taken as 7.318 (settled lives in) the
  maximum residual is 0.23, as 6.855 (out) 0.50. A description, not a law.*

**The answer about shared cells.** Yes. In these face definitions adjacent faces share their common rim row: the 10
non-apex cells with a = 0 (and the two apexes at its ends) are the *same cells* in both faces. The neighbour's
"band on the shared edge" (16 cells) therefore contains 10 of the dying face's own cells, which are empty at lag 0
by definition. Round 1's "the neighbour is dragged down" mostly restates that:
- the c1 neighbour loses 0.229 × 31.29 = 7.2 cells by lag 0, of which the shared row and its apexes account for
  about 5.5 (stationary 10 × 0.513 + 2 × 0.17);
- the neighbour's own cells next to the edge (its row 2) are at 0.62 of stationary at lag 0 and 0.77 at lag 8
  (`data/neighbour_c1.csv`), a real but modest drag;
- away from the edge the neighbour is about 1.7 cells down.

## What each number rests on

- `ex.c` (copy of `sy.c` plus a bit-sliced count of each face orbit's population every generation and an online
  excursion table) gave lives files byte-identical to `sy`'s for all four runs. Its time-averaged P over the
  exposure, 31.25 ± ~0.03 (c1), matches round 1's null 31.29, which was counted by independent Python code. Its face
  death rates give ln τ_face = 13.632 ± 0.013, 11.454 ± 0.011, 9.274 ± 0.008, 7.168 ± 0.003, which agree with the
  symmetric study's 13.634, 11.456, 9.291, 7.168.
- ν·q equals the death rate at every level by construction (every death ends an excursion). The check returns 1.000
  for c1 at every level. Where it departs from 1, the departure is the censored share: up to 12.5% of excursions in
  D2h at p = 0.2, mostly lives that settle at low P. 27% of D2h exposure is in lives that end settled, and those are
  inside ν; they are not removed. *Added 2026-11-15 (review): so for D2h the identity is bookkeeping within one
  estimator and cannot say which estimator is right. With settled lives counted (Brent detection) ln(E/D) = 7.318 and
  −ln(νq) wanders over 7.20–7.34 because up to 12.8% of excursions are censored; without them the identity is exact
  and ln τ_face = 6.855; this study's 7.168 lies between because its ladder detects settling sooner. Time-averaged P
  over the D2h exposure is 20.31 with settled lives, 23.25 without. Every D2h number of this round that involves
  exposure (ln ν, q, p*, ln τ, the c1 → D2h fall of 6.46, the last step of the ladder, the A = 63 D2h point of the
  fit) carries this 0.2–0.45 ambiguity.*
- B and C use new `sd.c` histories (seeds 21/22). Their lives files are byte-identical to `sy`'s, and they pass the
  same internal death-time checks as round 1 (`load.py`). These histories were not stepped by the engine again;
  they rest on the round-1 engine check of the same code.
- D uses `sd.c` null samples at R = 13 (seed 31, 200,000 generations). The ln τ values at A = 84 are the symmetric
  study's, and c1's (18.141) is the GPU's, with a different protocol (soup 0.35).

## Forecasts, scored

| | said | found [measured] | |
|---|---|---|---|
| A1 | c1 q = 1/2 at 0.25–0.5 P̄ | p* = 0.079 (q(0.1) = 0.300 ± 0.003, q(0.05) ≈ 0.8) | **failed** |
| A2 | c1 ln ν Gaussian within 1.0 to 0.6 P̄ | residuals −0.15, −0.43, −0.27 at 0.8, 0.7, 0.6 (then +0.08, +0.65, +1.50, +2.65, +4.15 at 0.5…0.1: fatter tail below 0.45) | **held** |
| A3 | at 0.5 P̄: q within ×3, ν differs by > e^4 | q c1/D2h = 0.008 (ln −4.88); ln ν D2h − c1 = 1.59 (review 1.45 with settled lives, 1.62 without) | **failed** both parts: at this level the ladder is mostly in q |
| B1 | concentration within 15% of stationary (c1, D2h) | S ratio 1.611 ± 0.014 (c1), 1.758 ± 0.015 (D2h); live-live adjacency 1.74, 1.82 | **failed**; naturally low-P stationary faces give 1.59, 1.51 (not forecast; at a higher count, and in D2h not the same as the dying faces' ratio: see the short answer, corrected 2026-11-15) |
| C1 | at t_8: births ≤ 0.70, survival ≥ 0.85 of stationary (c1) | births 0.377 ± 0.004, survival 0.639 ± 0.004 (t_8 is a median 8 generations before death) | **failed** (survival clause); births do fail first (lag 16: 0.90 vs 0.98; lag 8: 0.45 vs 0.88) |
| D1 | A = 84 steps each 2.8–3.1 cells; Δln τ/ΔP̄ each 0.76–0.96 | steps 2.68, 2.95, 3.38 (± ~0.13); per cell 0.983, 0.898, 0.838 | **failed** |
| D2 | no function of (P̄, σ_P) fits all eight within 0.5 | a + b·P̄²/(2σ²): max residual 0.31; a + bP̄ + cσ: 0.52 | **failed** (the first fit stays within 0.5; its leave-one-out residual is 0.50, and a + b·A + c·P̄ without σ fits to 0.27: review, 2026-11-15) |
| K5 (mine) | c1 p* in 0.4–0.7 | 0.079 | **failed** |
| K6 (mine) | A2 fails, ν above the Gaussian at 0.6 | −0.27 (below, within 1) | **failed** |
| K7 (mine) | B1 fails in c1 (> 1.15) | 1.61 | held, but not for the reason given (see low-P control) |
| K8 (mine) | A3 holds both parts | failed both | **failed** |

## Numbers [measured]

ln ν(p) per face orbit per generation and q(p) (Poisson/binomial errors under 0.01 in ln ν; q errors in the csv):

| p | c1 ln ν, q | csz | c2v | D2h |
|---|---|---|---|---|
| 0.9 | −2.31, 1.0e−5 | −2.53, 9e−5 | −2.62, 1.3e−3 | −2.64, 0.011 |
| 0.7 | −4.16, 8e−5 | −3.80, 5e−4 | −3.77, 4.1e−3 | −3.74, 0.032 |
| 0.5 | −6.51, 8.1e−4 | −5.82, 3.6e−3 | −5.18, 0.017 | −4.92, 0.107 |
| 0.3 | −9.37, 0.014 | −8.31, 0.043 | −7.21, 0.128 | −5.89, 0.298 |
| 0.1 | −12.43, 0.300 | −10.95, 0.607 | −8.95, 0.726 | −7.05, 0.892 |
| ln τ_face = −ln(ν q) | 13.632 | 11.454 | 9.274 | 7.168 |

The D2h column is this study's protocol (settled lives inside the exposure, ladder detection). The review's D2h
column moves by 0.15–0.4 in ln ν with the treatment of settled lives (at 0.5: −5.059 with them, −4.890 without;
ln τ 7.318 and 6.855); *note added 2026-11-15.*

Split of the ladder by level: from c1 to D2h ln τ falls by 6.46 (with this study's D2h value; 6.30 or 6.76 with
the review's two). At p = 0.5 that is 1.59 in ν and 4.88 in q; at
p = 0.3, 3.48 and 3.07; at p = 0.1, 5.38 and 1.09. Where the ladder "is" depends on the level chosen. What does not
depend on it: the rates of shallow dips (to 0.7 P̄) are equal across the groups within 0.4, and the groups part in
the passage from about 0.6 P̄ down to a few cells.

The tail of ln ν below the Gaussian part (added 2026-11-15 from the review; not in this round's first text, but the
lead's reading of it circulated). An unweighted straight line through ln ν(p) for p = 0.10, 0.15, …, 0.45 has slope
15.6, 12.6, 9.2, 5.5 per unit p (c1, csz, c2v, D2h; review on fresh seeds 15.55, 12.57, 9.19, 5.51), that is 0.50,
0.44, 0.35, 0.23 per live cell. The tail is **close to straight, not straight**: in c1 the line leaves residuals of
+0.13 at both ends and −0.25 in the middle (ln ν errors 0.001–0.009), and the local slope per live cell, from the
density of excursion minima, drifts smoothly: 0.62 (1–4 cells), 0.51–0.49 (3–10 cells), 0.48–0.45 (9–14), 0.42–0.39 (13–18), 0.34 (17–20
cells) (review, `ana2.py`, "tail shape"; other groups alike). There is no break at half the mean. The reading "a constant price per cell, 5.5 + 3.4 per unit p per
free edge" (the lead's line through the four slopes) holds for that window and estimator only: the step per free
edge ranges over 3.0–4.5 with the fit window (0.05–0.30, 0.10–0.45, 0.20–0.50) and with whether settled D2h lives
are counted (D2h slope 5.51 with them, 4.99 without). What is robust is the order: the price per further cell lost
is highest in c1 and falls with each tied edge.

Stationary state (A = 63 from round 1's null; A = 84 new):

| | c1 | csz | c2v | D2h |
|---|---|---|---|---|
| A = 84: P̄ | 42.49 ± 0.09 | 39.81 ± 0.09 | 36.86 ± 0.10 | 33.48 ± 0.12 |
| A = 84: σ_P | 5.96 | 6.18 | 6.50 | 7.05 |
| A = 63: P̄, σ_P | 31.29, 5.24 | 28.83, 5.56 | 26.29, 5.96 | 23.77, 6.37 |

Births and survival on the dying face over stationary (pooled; stationary from lags 256–500 of the same
histories: births per empty cell 0.321, 0.288, 0.253, 0.220; survival 0.674, 0.661, 0.647, 0.632 for c1…D2h):

| | at t_8 (median lag 8, 8, 10, 12) | at t_h | lag 16 | lag 8 | lag 4 |
|---|---|---|---|---|---|
| c1 | 0.377 / 0.639 | 0.177 / 0.539 | 0.903 / 0.983 | 0.454 / 0.877 | 0.132 / 0.625 |
| csz | 0.411 / 0.652 | 0.201 / 0.552 | 0.837 / 0.983 | 0.436 / 0.884 | 0.148 / 0.636 |
| c2v | 0.453 / 0.683 | 0.229 / 0.592 | 0.746 / 0.990 | 0.391 / 0.893 | 0.158 / 0.653 |
| D2h | 0.468 / 0.709 | 0.233 / 0.624 | 0.617 / 0.980 | 0.360 / 0.928 | 0.169 / 0.700 |

(Births are a deterministic function of the neighbour count, so a birth deficit says the empty cells' neighbourhoods
thinned first, including the layer beneath the face, which round 1 saw dip with it.)

## What the excursion picture says about what starts a collapse

Nothing special starts it. The face makes dips of all depths all the time. Those to 0.7 P̄ are about equally
frequent whatever the symmetry, about once per 60 generations per face (shallower, at 0.9 P̄, the untied face dips
the most often; review, 2026-11-15). A death is a dip that keeps going, and in c1
it is decided only when two or three live cells are left. Ties make the descent easier at every level below about
0.6 P̄: the q curves of the four groups are roughly parallel on a log scale from 0.9 to 0.4 P̄ (panel B), offset by
about 1.5–2.7 in ln q per tied edge. A tied face is easier to push down at every step of the way. It is not a face
that starts collapses more often, and not one with a different collapse once started. The survivors of a deep dip
are clumped, as in any depleted face (in c1 at equal count less clumped than faces that recover, in D2h more;
corrected 2026-11-15); whether the clump's position matters was not examined.
**[conjectured]** The births-first run-up and the equal shallow-dip rates fit a picture in which the rim deficit of a
tied face (round 1) costs it support only once the face is already thin. (Review, 2026-11-15: most of the births-first
run-up is the face's own lower population, so it is weaker evidence for that picture than it first looked; and a
birth–death chain whose down/up ratio does not depend on P also gives a nearly straight log-tail, so the tail is no
evidence for any particular spatial picture.)

## Not checked (round 2)

- One protocol (soup 0.4, T0 = 512). Settled D2h lives are inside ν, as they are inside the study's ln τ; the
  review gives every D2h exposure figure both ways, and they differ by 0.2–0.45 (added 2026-11-15).
- The review reran excursions only at R = 11 cube-centred (one seed per group); A = 84 was sampled stationary only.
  It did not rerun `round2.py`, `round2_lowp.py` or the r2 histories, did not split births by neighbour count, and
  did not compute errors on its matched-count null (about ±0.05).
- B's comparison is uniform thinning. The low-P stationary control (added afterwards, `round2_lowp.py`) is the
  fairer one; it was not used to decide B1. Whether the position of the clump (rim or centre, tied edge or free)
  predicts recovery was not measured.
- C: a per-neighbour-count breakdown was not made. Neither was a measurement of whether the layer beneath falls
  before the face's own births do.
- D: one seed per group at A = 84, no engine check of those runs beyond the shared code. The D2 fit has two free
  constants on eight points. c1 at A = 84 uses the GPU's ln τ (another protocol). No other size.
- The excursion tables count per face orbit; for csz and c2v that is per pair or quadruple of faces in lockstep, as
  in the study's nf.

## Reproduce (round 2)

```sh
bash research/dying/round2.sh 1 & bash research/dying/round2.sh 2 & wait   # builds ex, sd; runs; checks lives files against sy (~10 min, 2 cores)
python3 research/dying/round2.py        # A-D tables, data/r2_*.csv, research/figures/dying_excursions.png (~2 min)
python3 research/dying/round2_lowp.py   # the low-P stationary control for B (added after the forecasts)
```

# Round 3: one curve across sizes? What a depleted face looks like (2026-11-15)

Forecasts and definitions: `PREDICTIONS.md`, "Round 3" (committed 27890b4 with `ex3.c`, before any round-3 run).
Figure: `research/figures/dying_ratefunction.png`. Tables: `data/r3_excursions.csv` (ν, q by level for every
size and the slab), `data/r3_clump_profile.csv`.

## Reviewed (2026-11-15)

The round-3 part of `research/audit/REVIEW-dying.md` reran every size with its own stepper (`r3_ex.c`: round 2's
`ex2.c` with 7-bit face counts and a dump of every deep excursion, matched to `reference/oracle.py` at every
generation on each vessel) on fresh seeds 9411–9419, added A = 135, and measured the depleted face without aligning
on its own centroid. Commands: `bash research/audit/dying/r3_plan.sh 1`, `2`, `3`, then
`research/audit/dying/r3_ana.py` (→ `r3_ana_out.txt`) and `r3_dump.py` (→ `r3_dump_out.txt`). "Threshold-free"
there means ln ν(min ≤ y) interpolated linearly between integers y and read at y = pP̄ − ½. Ledger: CLAIMS
DY8–DY12. Every forecast score reproduces; the definitions were fixed before the data.

**What the review changed, applied below** (marked "corrected 2026-11-15" where they fall):
1. **The end point at p = 0.** The end points follow ln τ + ln ν(0.9) = 0.2125·A − 2.07 to 0.01 nats over
   A = 45–108: the shortfall below the slope is a fixed 2.1 nats, spread below p ≈ 0.55 (half of it below 0.15), not
   in the last cells. The slope depends on which dip rate is the attempt (0.218 for every crossing of P̄, 0.213 for
   ν(0.9)). The dips at p ≥ 0.2 alone give c = 0.215 ± 0.005, which cannot separate 0.207 from 0.219. "Levelling off
   near 0.19–0.20, below c" is withdrawn: the end points follow c − K/A and still rise at A = 135 (0.1985).
2. **The slab lives longer:** ln τ_face = 13.176 ± 0.011 (review, two seeds), above every part-C forecast for this
   torus (the flat reading by 5σ). No transverse firewall can form on it.
3. **The depleted face** is at about half its stationary density near the survivors (0.46–0.54 by alignment-free
   measures; aligning on a face's own centroid lifts even random points by a quarter), and the rest of the face is at
   0.15–0.2 of stationary, not emptied.
4. **Refill** is the rule: a rule-aware baseline gives 0.991 against the observed 0.994.
5. **The tail price** is 0.50–0.52 per cell at A ≥ 63 over 0.1–0.45 P̄, rising slowly with A (0.44–0.47 at A = 45;
   locally 0.53 deep, falling to 0.40 by P̄/2). The weighted fit's spread and most residuals of both fits are
   integer thresholds.
6. **The shallow-dip rate is not size-independent:** threshold-free ln ν(0.9) falls by about 0.002 per cell; the
   rate of all crossings of P̄ rises slowly.
7. **The collapse for p ≥ 0.4** is the 1/A convergence seen at every p, with an offset K(p) that vanishes above
   p ≈ 0.55, not a regime. (The review's other point under this item, that the lead's formula for c from ρ and the
   Fano factor is not evidence about c, concerns a formula this README did not give.)

## Short answer

- **[measured] Once the rate of shallow dips is taken out, the dip curve is one curve per cell of face for
  p ≥ 0.4; the raw curve is not.** −ln ν(0.5)/A is 0.120, 0.103, 0.093, 0.089 at A = 45, 63, 84, 108, so T1a fails.
  The cause is a nearly size-independent rate of shallow dips: ln ν(0.9) = −2.34, −2.31, −2.35, −2.51, about one dip
  every ten generations per face whatever its size. Measured from there, [ln ν(0.9) − ln ν(0.5)]/A = 0.068, 0.067,
  0.065, 0.066, equal within 3%. Deeper the curves fan slightly: at p = 0.3 they read 0.108, 0.112, 0.117, 0.116; at
  p = 0.1 they read 0.151, 0.161, 0.167 (figure panel B). `round3_persite.py` was added after the forecasts.
  *Corrected 2026-11-15 (review): the rate of shallow dips is not size-independent. The jumps in the study's values
  are integer thresholds (0.9P̄ means P ≤ 19, 28, 38, 49); threshold-free ln ν(0.9) is −2.34, −2.38, −2.40, −2.48
  (−2.53 at A = 135), a steady fall of about 0.002 per cell, mostly a part of ν(0.9) proportional to A. The rate of
  every downward crossing of P̄ instead rises slowly (ln ν = −1.90 → −1.70). The 3% equality at 0.9 was partly luck
  of the thresholds (threshold-free 0.0648, 0.0646, 0.0654, 0.0660, 0.0666 at A = 45 … 135). "One curve for
  p ≥ 0.4, a fan below" is one effect: at every p the curves converge as 1/A to a limit f∞(p), with an offset K(p)
  that is zero above p ≈ 0.55 and grows below it; "p ≥ 0.4" marks where K(p)/A drops below the noise, not a regime.*
- **[measured] The tail has a price per live cell, and that price does not depend on size.** An unweighted line
  (the lead's fit) over 0.1 ≤ p ≤ 0.45 has slope 0.437, 0.499, 0.506, 0.508 per live cell at A = 45, 63, 84, 108
  (max residual 0.03–0.22). The pre-registered fit is weighted by counts, so the curved shallow end dominates it. It
  gives 0.431, 0.537, 0.566, 0.432 (A = 108 over 0.2–0.45 only), and on it T1b fails (0.566/0.499 = 1.13).
  *Corrected 2026-11-15 (review): "does not depend on size" is too strong. Supported: 0.50–0.52 per live cell at
  A ≥ 63 over 0.1–0.45 P̄, rising slowly with A (integer-grid fits 0.498, 0.513, 0.519 at A = 63, 84, 108), and
  0.44–0.47 at A = 45. Locally the price is about 0.53 per cell in the deep part, falling to about 0.40 by P̄/2 (the
  last three cells 0.39–0.42). The weighted fit's spread (and most of the residuals of both level fits) is integer
  thresholds: the 0.45 level carries most of the weight and falls a different fraction of an integer below 0.45P̄ at
  each size. On the integer grid the tail is straight to 0.02–0.08 nats.*
- **[conjectured] What it points to at p = 0.** Per site, without the shallow-dip constant, the straight tail
  extrapolated to p = 0 reaches 0.172, 0.188, 0.193, 0.194 at A = 45 → 108. The true end point,
  [ln ν(0.9) + ln τ_face]/A, is 0.166, 0.180, 0.189 at A = 45, 63, 84 (no deaths to speak of at 108).
  *Corrected 2026-11-15 (review). Withdrawn: "levelling off near 0.19–0.20 … So the stationary dips point to a
  per-site price near 0.19–0.20, below c". The end points follow ln τ + ln ν(0.9) = 0.2125·A − 2.07 to within 0.01
  nats over A = 45–108 (with the GPU's lifetimes), i.e. c − K/A with K = 2.1 nats, and are still rising at A = 135
  (0.1985). The shortfall K is a fixed number of nats spread over p below about 0.55 (half of it below p = 0.15), not
  a price paid in the last few cells. The slope c of this form depends on which dip rate is called the attempt:
  0.218 with every crossing of P̄, 0.213 with ν(0.9), 0.204 with ν(0.8), because each shallow rate has a part
  proportional to A; "c is the p = 0 limit of the collapsed curve" holds only with the crossing rate. The dips at
  p ≥ 0.2 alone, extrapolated in size and then to p = 0, give c = 0.215 ± 0.005 (error from the fit windows): they
  cannot separate 0.207 from 0.219.*
- **[measured] A depleted face is a single loose patch, not a uniform haze, and not a full-density clump.** Take c1
  faces caught at P ≤ 0.3 P̄ (mean 8.3 live cells; 419,556 faces).
  - Around the survivors' centroid, occupancy is 0.58–0.61 of stationary out to about 2.5 doubled units (just over
    a cube).
  - It falls to 0.20 by 5 units, 0.09 by 7, and is nearly empty beyond 9.
  - A stationary face thinned at random to the same count gives 0.34 flat, then a slow fall from geometry alone.
  - So: one patch about two cubes across at 60% of the usual density, in an otherwise emptied face (panels C, D).
    The patch sits on the rim side of its centroid more often than on the centre side (panel C). I have not
    quantified that.
  - *Corrected 2026-11-15 (review): the levels above are inflated by aligning each face on its own centroid, which
    lifts even ρ-weighted random points from their true 0.264 to 0.33 at the centre. Without alignment the face is at
    about half its stationary density near the survivors (0.46–0.48 split-half, 0.54 around a live cell within 2.5
    doubled units), the excess reaches about 3.5 units (under two cubes), and the rest of the face sits at 0.15–0.20
    of stationary, about 0.7 of a uniformly thinned face: thinner far away, not emptied. Thinner faces have a
    looser patch (0.54 at 7–9 live cells, 0.38 at 3–6). The caught/control contrast (1.75 aligned, 2.0 around a live
    cell) stands; the absolute 0.6 and "otherwise emptied" do not.*
- **[measured] A thin face refills from its patch, and a thin csz face holds on away from its tied edge.**
  - 99.4% of the first ten births after the bottom of a dip are within two cells of a survivor, against 68.4% if
    births fell at random on empty cells. *Corrected 2026-11-15 (review): this is the rule, not a finding. A face
    cell has only 3 neighbours off the face, so a birth (4 or 5 live neighbours) needs a live in-face neighbour;
    every birth has one (1.00000). Random over empty cells with at least one live in-face neighbour gives 0.991
    against the observed 0.994.*
  - In csz, the stationary-corrected centroid of a caught face is nearest the tied edge in 22.3% of faces. Random
    thinning of stationary csz faces gives 29.9% under the same correction; the correction leaves a bias, so
    compare 22.3 with 29.9 rather than with 33.3.

## Forecasts, scored

| | said | found [measured] | |
|---|---|---|---|
| T1a | −ln ν(0.5)/A at 84 within 5% of 63 | 0.0926 vs 0.1034 (ratio 0.896) | **failed** (by 10%; not the 15% the lead set as "against") |
| T1b | tail slope at A = 84 within 7% of 0.499 | pre-registered weighted fit 0.566 ± 0.024 (×1.13) | **failed**; the unweighted fit gives 0.506 (×1.01). Review, 2026-11-15: the weighted fit tests where 0.45P̄ falls between integers |
| T2 | inner occupancy ≥ 0.8 of stationary and below 0.2 within 2 rows | inner 0.513; shells 0.421, **0.184**, 0.080 | **failed** (plateau at about 0.6, not 0.8; the edge clause holds) |
| T3 | csz nearest the tied edge < 25% | 0.223 ± 0.001 (control 0.299) | **held** |
| T4 | ≥ 70% of first ten births within 2 cells of the bottom's survivors | 0.994 (random 0.684) | **held** (review, 2026-11-15: forced by the rule; rule-aware baseline 0.991) |
| "against the reading" | T1a off by > 15%; T2 falls smoothly | 10%; T2 has a plateau and an edge | neither met |
| K9 (mine) | T1a holds | 0.896 | **failed** |
| K10 (mine) | slope at 84 more than 7% below 0.499 | 0.566 (weighted), 0.506 (unweighted) | **failed** |
| K11 (mine) | T2 no plateau of 0.8 | 0.513 | held |
| K12 (mine) | T4 excess over random < 0.10 | 0.31 | **failed** |

## The slab (no forecast)

`hex_4_1_c1` is a face torus of area 63 (8 layers, two faces, no rim). It was validated bit-exact against the
engine for 1,500 generations (`validate.py 1500 hex_4_1_c1` → ALL OK), with seed 55 and 400,000 generations.
- Stationary: P̄ = 32.57, σ_P = 4.94.
- ln τ_face = 13.13 ± 0.04 (814 deaths), against 13.64 for the hull face of the same area. *Corrected 2026-11-15
  (review): 13.176 ± 0.011 (two seeds, 9416 and 9418, 7,746 deaths; 1.1σ from this study's value). That lies above
  every forecast of `research/constant/PREDICTIONS.md` part C for this torus: the flat reading's 13.115 ± 0.004 by
  5σ, the massive reading's 13.128 ± 0.006 by 3.8σ. The vessel is part C's n = 21 torus (the lattice here is its
  mirror image under x ↔ y), equilateral, shortest loops √21 = 4.58 cube steps.*
- Its shallow dips are slightly costlier per cell than the hull face's ([ln ν(0.9) − ln ν(0.5)]/A = 0.077 against
  0.067), but its tail is cheaper: 0.427 per live cell against 0.499. At A = 63 the rim-free face dies sooner
  overall.
- *Corrected 2026-11-15 (review). Withdrawn: "This system has no transverse-firewall test …, so a life could in
  principle continue past a firewall; firewall lives were not counted." The transverse layer period of this torus is
  4 in all three directions, so each direction has only two layer classes; three consecutive dead layers would mean
  every cell dead. No firewall can form, and there was nothing to count.*

## What each number rests on

- `ex3.c` reproduces `ex.c`'s lives file, excursion table and P histogram exactly on a test run. All six production
  lives files are byte-identical to `sy`'s (`round3.sh` checks each).
- Every one of the 419,694 c1 deep-excursion records passes the popcount checks: first state ≤ 9 cells; minimum
  equal to the recorded one; recovered records end ≥ P̄, dead records end at 0. These checks test the face-state
  extraction against the independent bit-sliced count.
- P̄ at R = 9 and 15 come from `sd.c` null runs (21.67 and 55.14, σ_P 4.52 and 6.73). The time-mean P over the
  exposure agrees (21.60, 55.19).
- ln τ_face from these runs: 9.811 (A = 45), 13.644 ± 0.013 (63), 18.20 ± 0.13 (84, 61 deaths; the GPU's 18.141).
  A = 108 had one death.

## Not checked (round 3)

- One seed per size. A = 108 reaches only p ≥ 0.2 with 20 or more excursions. The deep tail (p < 0.1), where the
  per-site curves still differ, is measured only where faces die (A ≤ 84).
- Which fit of the tail is "the" slope. The weighted and unweighted fits differ by 7–13% at A ≥ 63; the line is not
  straight to better than 0.2 in ln ν.
- T2's patch: whether it sits at the rim or in the interior was seen in the aligned map, not measured. Nor was its
  shape in csz or D2h, or how its density changes with depth.
- T3's correction (1/ρ weights) leaves a bias of its own (control 0.299, not 0.333).
- T4's "within two cells" is nearly forced by the rule: a birth needs four live neighbours. The 0.6% of births
  further away are fed from the layer beneath or by cells born since the bottom; they were not separated. *Review,
  2026-11-15: every birth has a live in-face neighbour; the rule-aware baseline is 0.991.*
- The slab is one torus shape at one size. The shape dependence of periodic faces (CLAIMS SH1–SH9) is known to be
  large. *Review, 2026-11-15: its lifetime is 13.176 ± 0.011 on two seeds of one stepper; the tension with part C
  was not chased (other tori of the family, other soups, the engine).*

## Reproduce (round 3)

```sh
bash research/dying/round3.sh 1 & bash research/dying/round3.sh 2 & wait   # null runs for P̄, ex3 runs, lives checks (~20 min, 2 cores)
python3 research/dying/round3.py          # T1-T4, data/r3_*.csv, research/figures/dying_ratefunction.png (~3 min)
python3 research/dying/round3_persite.py  # unweighted slopes and the per-site curve without the shallow-dip constant (added afterwards)
python3 research/theory/symmetric/validate.py 1500 hex_4_1_c1             # the slab against the engine
```
