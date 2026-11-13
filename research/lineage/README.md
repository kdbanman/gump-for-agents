# Lineages: do runs started from structured seeds wait differently?

_2026-11-13, lineage agent. Everything here is engine-only (`gump run`, single lineages, events every 8 generations);
no orbit-stepper ensembles were run. Tags: [measured] = numbers from runs listed here; [conjecture] = not tested._

## Question

The plateaus of the legacy closed cubes 13–16 look over-dispersed against the memoryless ensemble means
(`python3 research/experiments/cube_vs_ensemble.py`: of 16 plateaus with A ≥ 408, 3 beyond 4τ, 3 under 0.05τ,
sum of T/τ = 27.2 against 16). Is that luck, or do lineages started from structured (cube-like) seeds really
wait differently from soups and perturbed copies?

## Verdict

**Luck, as far as can be tested at hull radii 31–37 (cube-centred) and 32–38 (vertex-centred).** Over two thousand
lineages, 1,248 of them from deterministic cube-like seeds, wait exactly like O_h soups and exactly like Exp(τ),
with no memory from one plateau to the next. The cubes' 16 plateaus still form a 1%-level outlier against
that distribution (it does not go away when τ's uncertainty or the measured shape of the null are used), but nothing
in the structured lineages reproduces it, and a structured-seed tail even at 5% beyond 4τ is excluded at
P = 2×10⁻⁷. What remains untested is the regime where most of the anomaly sits — vertex-centred R ≥ 40,
i.e. side 16 itself — which is out of reach of single engine lineages.

## Method

- **Seeds** (`seeds.py`, all exactly O_h-symmetric, deterministic). Small decorations are useless: removing an
  interior orbit of the closed cube, or adding cells outside it, gives a bit-identical history (the cube's interior
  dies at generation 1 whatever it contained; `nest:13:63`, nested hollow shells of sides 13, 11, …, 1, is also
  the cube's lineage exactly). Removing an orbit within one cube-width of the surface does change the lineage. Families:
  `cube:N:0`; `notch:N:K` (cube minus one surface orbit); `notch2:N:A:B` (minus two); `hollow:N:K`; `nest:N:K`
  (nested shells); `sc:13:K` and `sc2:13:A:B` (cube 13 inside a hollow shell of side 15, one or two shell orbits removed;
  starts at r = 37 or 39). Many seeds still give identical lineages; `analyze.py` keeps one per schedule signature.
- **Runs** (`run_lineages.py`): each lineage is run to its end (cap 4×10⁷), and every residence at one hull radius is a row:
  first plateau (idx 0) or after a peel (idx ≥ 1); censored if the run hit the cap or chaos settled first. Same radius
  convention as `cube_vs_ensemble.py`. Layers lost in the first 1000 generations (the seed's own burst) are not plateaus.
- **Controls**: O_h soups (density 0.35, `--sym oh`) at R = 33, 37 (cube centre) and 32, 36 (vertex), one lineage per rng.
- **References**: τ_q = orbit-stepper ensembles (`research/fluct/data/sym_residence.csv`, soups only, pooled);
  τ_e = engine soup lineages here (exposure / deaths).

| batch | lineages (distinct) | starting radius | cost |
|---|---|---|---|
| `struct 13` (800 seeds) | 490 | 33c (some 35c) | 25 min × 3 cores |
| `struct 12` (600 seeds) | 284 | 30v | 10 min |
| `struct 14` (180 seeds) | 144 | 36v (some 34, 38) | 2 h |
| `sc 13` (56 seeds) | 52 | 37c, 39c | 1 h |
| `soup 33`, `soup 32`, `soup 36`, `soup 37` | 800, 600, 300, 60 | as named | 2.5 h |
| perturbation, `perturb.py 13 20000 150 4` and `… 40000 150 4` | 2 × 150 sources × 5 continuations | 33c (some 31, 35) | 1 h |

Reproduce: `research/lineage/batch1.sh`, `batch2.sh`, then `python3 research/lineage/run_lineages.py sc 13 100 3 4e7 2`,
`… soup 37 60 3`, `python3 research/lineage/perturb.py 13 40000 150 4 3`. Rows go to `research/scratch/lineage/`;
the curated copy of all of them is `data/plateaus.csv.gz` (17,195 plateaus, 2,728 distinct lineages), and every
script falls back to it when the scratch files are absent.

## Results

### 1. Structured lineages wait like soups, like Exp(τ) [measured]

`python3 research/lineage/analyze.py` (section "pooled over reliable radii"; x = T/τ_q, plateaus ending in a peel,
r ≥ 31c / ≥ 32v):

| sample | n | mean x | CV | > 4τ (expected) | < 0.05τ (expected) | KS p |
|---|---|---|---|---|---|---|
| structured, all | 1,248 | 0.990 | 1.02 | 27 (22.9) | 60 (60.9) | 0.52 |
| structured, first plateau | 612 | 1.016 | 1.02 | 15 (11.2) | 26 (29.8) | 0.37 |
| structured, after a peel | 636 | 0.965 | 1.02 | 12 (11.6) | 34 (31.0) | 0.28 |
| soups, all | 3,261 | 0.984 | 1.00 | 60 (59.7) | 159 (159.0) | 0.36 |
| the 16 cube plateaus, sides 13–16 | 16 | 1.70 | — | 3 (0.29) | 3 (0.78) | 0.27 |

Two-sample structured vs soup: KS p = 0.98, Mann–Whitney p = 0.96, log ratio of means +0.006.
Fraction beyond 4τ among structured plateaus: 2.2% (95% 1.4–3.1%; e⁻⁴ = 1.8%). Cubes 3/16 against structured 27/1,248:
Fisher p = 0.005. If structured lineages had even a 5% tail beyond 4τ, seeing ≤ 27 would have probability 2×10⁻⁷.

Per radius against the engine soups (section "against engine soup lineages", T/τ_e, 95% interval):
33c 1.07 [0.96, 1.20] (299 deaths); 31c 0.97 [0.88, 1.07] (444); 36v 0.96 [0.80, 1.18] (101);
34v 1.08 [0.91, 1.29] (128); 32v 1.08 [0.93, 1.27] (153); 30v 1.15 [1.02, 1.30] (279); 37c 0.74 [0.55, 1.06] (36);
35c 0.77 [0.62, 0.97] (77; τ_e itself rests on 58 soup deaths). Pooled over radii with τ_e ≥ 10⁴: 1,983 plateaus,
mean 0.991, CV 1.03, > 4τ 38 (36.3), < 0.05τ 94 (96.7), KS p 0.24. If anything the cube-in-shell lineages at 35–37c
are a little *shorter*-lived (their after-peel plateaus at 35c: 35 deaths, mean 0.57 τ_q), the opposite of the cube
puzzle; with ~20 radius/family comparisons made, a 2–2.7σ deviation in one of them is not a finding.

The engine soups also confirm the orbit-stepper means at these radii: late-hazard τ_e/τ_q = 0.93–1.14 at 31–37c and
32–36v (e.g. 33c 0.93 ± 0.03, 32v 0.99 ± 0.03).

### 2. No lineage carries a persistent toughness [measured]

If a lineage (rather than the state) had a slow "toughness", successive plateaus of one run would correlate.
They do not: Spearman ρ between consecutive T/τ_e of one lineage (both peeled, τ_e ≥ 10⁴) is −0.013 (p 0.65; 1,201 pairs)
for structured lineages and −0.021 (p 0.24; 3,143) for soups; the variance of per-lineage mean ln x equals that of
shuffled data (structured p 0.36, soups p 0.32). (`analyze.py`, section "persistent toughness".) The cube 15 / 16
schedules (4.2, 0.35, 4.2; 2.8, 7.4, 2.6, 1.2) are what looked like such persistence.

### 3. The wait after a peel is exponential from the start, apart from ~1% immediate double peels [measured]

Hazard as a function of age within a plateau, in units of 1/τ_q (section "hazard vs age"):

| age / τ_q | 0–0.002 | 0.002–0.005 | 0.005–0.01 | 0.01–0.02 | 0.02–0.05 | 0.05–0.1 | 0.1–0.2 | 0.2–0.5 | 0.5–1 | 1–2 | 2–4 | > 4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| soups, after a peel (1,542) | 2.61 | 2.18 | 0.53 | 1.06 | 1.13 | 0.99 | 0.94 | 1.06 | 0.99 | 1.01 | 0.95 | 0.75 |
| structured, after a peel (645) | 4.69 | 2.09 | 0.95 | 1.59 | 0.60 | 0.94 | 1.02 | 1.13 | 1.01 | 0.97 | 0.98 | 1.13 |
| soups, first plateau (1,746) | 0 | 0 | 0.46 | 0.58 | 1.11 | 0.79 | 1.09 | 1.08 | 1.02 | 0.95 | 1.05 | 1.72 |

After a peel the hazard is 2–5× the stationary rate for the first 0.005 τ (a few hundred to ten thousand
generations), then flat at 1.0 to the end. The excess is 18 deaths where 8 were expected among 1,542 soup plateaus,
10 vs 3 among 645 structured ones: about **1% of peels are followed by an immediate second peel** (the new outer layer
inherits the depletion of the dying one). Fresh soups show the opposite at small ages (they need ~0.02 τ to
fill the hull). Neither touches the 0.05τ tail: under-0.05 counts are 88 vs 74 (soups after a peel, p 0.06),
34 vs 31 (structured after a peel). The cubes' three short plateaus (0.018, 0.037, 0.046 τ) sit in the flat region.

### 4. Unperturbed continuation vs one-orbit-flip copies, many sources [measured]

`python3 research/lineage/perturb.py 13 TS 150 4 3`; `python3 research/lineage/analyze_perturb.py [CSV] [R]`. For each
of 150 structured lineages alive at TS, the state at TS was continued unperturbed (it reproduces the lineage's own
remaining wait exactly in all 150 cases — a check of `--cells` restarts) and as 4 copies each with one distinct live
orbit killed. Residual waits (time from TS to the death of that plateau's layer) in units of τ_e. The two batches
use the same lineages at TS = 20,000 and 40,000, so their unperturbed residuals are not independent (they differ by
20,000 generations); they are shown separately.

| | sources | unperturbed: mean, CV, > 4τ (exp.) | copies: n, mean, CV, > 4τ (exp.) | KS p (unpert. / copies) | Spearman(own, mean of copies) | copies: Kruskal–Wallis over sources, ICC of ln x |
|---|---|---|---|---|---|---|
| TS = 20,000 | 148 | 1.03, 1.22, 6 (2.7) | 592, 1.00, 0.94, 8 (10.8) | 0.26 / 0.87 | +0.20 (p 0.016) | p 0.054, +0.06 |
| TS = 40,000 | 149 | 1.10, 1.20, 8 (2.7) | 596, 1.05, 0.96, 13 (10.9) | 0.33 / 0.06 | +0.23 (p 0.005) | p 0.12, +0.03 |
| both, sources at r = 33 only | 215 | 1.14, 1.14, 11 (3.9) | 860, 1.05, 0.94, 16 (15.8) | 0.52 / 0.14 | +0.17 (p 0.011) | p 0.043, +0.05 |

(`python3 research/lineage/analyze_perturb.py research/scratch/lineage/perturb_13_20000.csv`, `… perturb_13_40000.csv`,
`… --r=33`; the curated CSVs are in `data/`.)

- **Copies are exponential and statistically identical to fresh lineages** (mean 1.00–1.05, CV 0.94–0.96, tails as expected).
- **The lineage's own continuation is mildly long-tailed in this sample** (6 and 8 beyond 4τ where 2.7 were expected;
  P = 0.06 and 0.006 for each batch alone, not independent). But these unperturbed residuals are simply the
  lineages' own first plateaus, and over all 612 structured first plateaus the tail is 15 vs 11.2 (§1): this sample
  of 150 is not representative of anything special. [measured]
- **Surprise: copies remember their source a little.** The mean residual of a source's four copies rises with the
  source's own residual: by tertile of the own residual (means 0.17, 0.61, 2.3 τ), the copies' means are 0.89, 0.98, 1.13
  (TS = 20,000) and 0.90, 1.03, 1.21 (TS = 40,000). The rank correlation survives dropping all waits under 0.2 τ
  (ρ = +0.30 and +0.29, p = 0.001 each), so it is not the shared first few hundred generations after TS (a face
  already in its final plunge); and it does not depend on seed family (Kruskal–Wallis over families p 0.44, 0.96).
  So a state carries a slow variable that sets its hazard to within roughly ±15–25% and outlives a one-orbit flip
  for at least ~0.2 τ ≈ 5×10⁴ generations. [measured] What it is (debris in the face layer's corners and edges?
  a slow mode of the layer-population profile?) is not known. [conjecture] It resets, or is too weak to see, across
  a peel (§2: consecutive plateaus uncorrelated).
- **It is far too weak for the cube puzzle.** A hazard multiplier spread of ±25% that held for a whole plateau would raise
  the CV of residences only to 1.04–1.06 and the fraction beyond 4τ from 1.8% to 2.1–2.3% (lognormal spread σ = 0.2–0.25,
  simulated); the cubes need ≈ 19%.

### 5. The cube anomaly itself, re-tested [measured]

`python3 research/lineage/cube_recheck.py` (200,000 Monte Carlo replicas of 16 plateaus):
- with each τ drawn from its posterior (deaths, exposure; the ×1.6 vertex factor with 15% spread):
  P(sum ≥ 27.2) = 0.009, P(≥ 3 beyond 4τ) = 0.011;
- with the null taken as the empirical shape of 4,517 lineage plateaus instead of an exact exponential:
  P(sum ≥ 27.2) = 0.008, P(≥ 3 beyond 4τ) = 0.004, P(≥ 3 under 0.05) = 0.039, both together 0.0001;
- look-elsewhere over the four statistics (sum, > 4, < 0.05, KS): the smallest p (0.003) is reached by chance
  with probability 0.008.

So the 16 cube plateaus remain a ~1% outlier on their own terms; the lineage data do not explain it, and the
"structured seeds differ" explanation is ruled out where it can be tested. Most of the weight is side 16: its six plateaus sum to 14.4 τ against 6; the other ten (sides 13–15) sum to
12.8 against 10 (P = 0.18); dropping only the R = 40 plateau (7.4 τ) leaves 19.8 against 15 (P = 0.11).
Remember also that the statistic was chosen after side 16 finished.

## What could not be settled

- **Vertex-centred R ≥ 40 (side 16's own sizes)** — τ ≥ 7×10⁷: a single lineage takes hours. Only 5 structured
  plateaus at 38v and none above. [conjecture] A size-specific lineage effect appearing only above R = 38 is not excluded,
  but there is no mechanism for it, copies of the side-16 state at R = 40 and 42 agree with soups
  (`research/fluct/`), and nothing at 31–38 trends toward it.
- The slow variable of §4: what it is, how long it lasts (≥ 0.2 τ; the test here cannot see beyond the plateau), and
  whether it is larger in bigger faces. A cheap next step: copies made at several lags after a common source, to
  measure the decay of the own/copy correlation; and a search for what distinguishes high- from low-hazard states
  (`gump occupancy` maps of the outer layer for the top and bottom tertile).
- The cube-in-shell lineages at 35c (after a peel from 37c) ran short, 0.57 τ_q (35 deaths); probably one of many
  comparisons, not followed up.
