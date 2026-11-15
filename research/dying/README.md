# How a hull face dies: c1, csz, c2v, D2h at R = 11 cube-centred (A = 63)

2026-11-15. Follow-up to `research/theory/symmetric/` (the edge ladder: ln τ_face 13.634, 11.456, 9.291, 7.168 for
0, 1, 2, 3 edges of a face shared with a face in lockstep). That study read the ladder as "an asymmetric face is held
up along each edge by an independently living neighbour face". Here the faces were looked at in the generations
before they die. Forecasts and every definition: `PREDICTIONS.md` (committed 75e5212 before any run). Tags:
**[measured]** (number, error, command), **[conjectured]**.

## Short answer

- **[measured] A death is a fast collapse of the whole face, and it keeps the face's stationary profile.** In every
  group the face is at its stationary population until about 20 generations before death (c1: 0.98 of P̄ at lag
  20, 0.95 at lag 16, 0.67 at lag 8, 0.31 at lag 4); it falls from half its stationary population to empty in a median
  of 6–7 generations. Measured against its own stationary value, every band and the interior empty together within a
  few per cent at every lag (figure panel B). The rim rows linger slightly at the very end (lags 1–4, by 7–16% relative
  to the interior), and they do so *as much on a tied edge as on a free one*.
- **[measured] What a tied edge changes is the stationary face, not the dying.** The shared rim row of a tied edge
  is depleted at all times: stationary occupancy 0.51 on a free edge (c1), 0.35 / 0.32 / 0.30 on a tied edge in csz /
  c2v / D2h; row 2 is depleted less (0.43 → 0.39 / 0.37 / 0.34), row 3 a little (panel C). The face's stationary
  population falls in equal steps: P̄ = 31.29, 28.83, 26.29, 23.77 ± 0.03–0.15 live cells (steps 2.46, 2.54, 2.52), as
  equal as the ln τ steps.
- **[measured] In c1 the living neighbour does not hold the edge up; it is dragged down with it.** The adjacent face's
  band along the shared edge falls with the dying face's own (0.71 of stationary at lag 8, 0.42 at lag 4, 0.21 at lag
  0; the shared row is empty at lag 0 by definition), and the whole neighbour face loses 23% of its population by lag 0.
- **So:** the pictures do not show the dynamical form of the reading (free rims outlasting the interior because a
  live neighbour feeds them; tied rims going first). They are consistent with a static form of it **[conjectured]**:
  a face sharing an edge with its lockstep partner has a thinner rim at all times (its rim cells see pairs of equal
  states, so their counts move in steps of 2), sits closer to empty, and so needs a smaller fluctuation to die. Nothing
  here measures that this is the *cause* of the −2.17 per edge.

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

| | said | found [measured] | |
|---|---|---|---|
| L1 | death is an event of the whole face (deduction from the ladder) | the whole face collapses together, relative to its stationary profile, within ~20 generations | consistent (not a numerical forecast) |
| L2 | c1 band/interior ratio at lag 4 ≥ 1.5 | 1.076 ± 0.018 (x 1.061, y 1.074, z 1.092); stationary 0.924 ± 0.002 | **failed** |
| L3 | csz tied ratio < 1.2, free/tied ≥ 1.3 | tied 0.810 ± 0.017 (held); x/z 1.164 ± 0.027, y/z 1.153 ± 0.027 | **failed** (second part). Stationary: tied 0.700, free 0.880, free/tied 1.26 already |
| L4 | D2h ratio in 0.8–1.2 on all edges | 0.715, 0.721, 0.697 ± 0.017 | **failed** (stationary 0.61–0.62) |
| L5a | c1 neighbour population within 10% of P̄, lags 1–16 | 0.893 ± 0.001 | **failed**, narrowly (0.98 at lag 16, 0.82 at lag 4, 0.77 at lag 0) |
| L5b | c1 neighbour band on the shared edge within 15%, lags 1–16 | 0.668 ± 0.003 | **failed** |
| L6 | csz: emptying begins nearest the tied edge in 45–70%; c1 one third each | csz 0.211 ± 0.007; c1 0.338, 0.330, 0.332 ± 0.009 | csz **failed**; c1 held (forced by symmetry: a code check) |
| L7 | median plunge shrinks ≥ 25% from c1 to D2h | c1 6, csz 6, c2v 7, D2h 7 generations (quartiles 4–8, 4–9, 4–11, 4–12); D2h/c1 = 1.17 | **failed** (the plunge does not shrink; the run-up lengthens) |
| "against the reading" | c1 ratio below 1.1; csz no tied/free difference | 1.076 ± 0.018 (below 1.1 by 1.3σ); csz raw ratios differ (0.81 vs 0.94) but relative to stationary the tied band lingers *more* (1.16 vs 1.07) | first criterion met; second met only after normalising by the null |
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
| stationary face population P̄ | 31.29 ± 0.03 | 28.83 ± 0.04 | 26.29 ± 0.07 | 23.77 ± 0.15 |
| stationary band occupancy, free / tied | 0.483 | 0.459 / 0.364 | 0.436 / 0.338 | — / 0.316 |
| stationary interior occupancy | 0.522 | 0.520 | 0.516 | 0.514 |
| face at lag 16, 8, 4 (/ P̄) | 0.95, 0.67, 0.31 | 0.93, 0.65, 0.32 | 0.84, 0.57, 0.30 | 0.75, 0.52, 0.30 |
| live cells at lag 1 | 1.61 | 1.61 | 1.56 | 1.54 |
| lag-4 ratio over stationary ratio, free / tied | 1.16 | 1.07 / 1.16 | 1.08 / 1.10 | — / 1.16 |
| layer beneath (s = 9) at lag 4 / at lag 0 (/ own stationary) | 0.72 / 0.88 | 0.70 / 0.79 | 0.63 / 0.63 | 0.54 / 0.45 |

- Co-deaths: two face orbits first empty in the same generation in 0 (c1), 1 (csz), 3 (c2v) of ~3,000 deaths.
- The layer beneath the face dips with it (c1 to 0.72 at lag 4) and partly recovers at the moment of death; the layer
  two below (s = 7) barely moves in c1 (0.96–1.14). With more tied edges the run-up is longer and deeper and reaches
  further in: in D2h, where all eight faces die together, the layers beneath are at 0.45 and 0.66 at death.

## What the pictures show (`research/figures/dying_face.png`)

Top: the mean canonical face, stationary and at lags 16, 8, 4, 2, 1, for the four groups, one log colour scale, tied
edges marked by an orange bar. Bottom: A, face population over its stationary mean against lag (and c1's neighbour);
B, csz and D2h bands and interior each over their own stationary value; C, stationary occupancy by row from a free and
a tied edge.

In plain words: a face does not erode from one side. It stays at its usual density until about twenty generations
before the end, then fades everywhere at once, reaching one or two scattered live cells a generation before it is
gone; the fade takes about as long as a signal needs to cross the face (one cube per generation, the face is about
six cubes across). The tied edges are visibly paler in every column including the stationary one: the difference
between a tied and a free edge is there all the time, not something that happens at death. The neighbour of a
dying asymmetric face loses the strip along the shared edge as the face dies. The more tied edges, the earlier the
fade starts (panel A); its last few generations look the same in all groups.

Surprises, and what would pin them down:
1. The final plunge does not depend on the symmetry (median 6–7 generations everywhere) while lifetimes differ by
   e^6.5. Whatever makes a tied face die sooner acts on how often a collapse starts, not on how it runs. A test: the
   distribution of the face population's excursions (how often P drops below, say, 0.7 P̄ and recovers) in each group
   from long stationary traces, against the ln τ ladder.
2. The stationary population falls by the same 2.5 cells per tied edge as ln τ falls by the same 2.17. Whether the
   ladder is a function of the stationary state (mean and width of P; c1 σ_P 5.24 → D2h 6.37) could be tested by
   the same comparison at A = 84, where the ln τ steps are −2.64, −2.65, −2.84.

## Not checked

- One size (A = 63) and one centring; nothing at A = 84 or vertex-centred, nothing for c2e (the rotated edge, where a
  mirror is absent) or O_h.
- The mechanism suggested for the tied-row depletion (paired counts) is not tested; nor whether the depletion causes
  the shorter life.
- The engine check covers 48 of 11,930 histories (511 generations each); the rest rest on the byte-identical lives
  files plus the same stepper code. No independent stepper (the review's `st.c`) was used.
- Only the dying face of c1 has its neighbours measured; in csz and c2v the free neighbours were not.
- Null samples of the symmetric groups exclude lives that end settled (27% of D2h exposure is in such lives), so the
  D2h null describes lives that go on to die.
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
