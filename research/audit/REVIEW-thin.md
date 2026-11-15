# Review of research/theory/thin/ (the thinnest periodic face)

Adversarial review, 2026-11-14 (started 23:30), of `research/theory/thin/` at commit 15e14a7. Scripts in
`research/audit/thin/`; they share no code with the thin line. Bulk output in `research/scratch/audit_thin/` (ignored).
IN PROGRESS: verdicts are filled in as runs finish.

**Independent stepper.** `tt.c` (bit-sliced, 2,048 lanes, splitmix64, its own life logic) driven by `tt.py`, which builds
the graph of the torus (1,1),(0,b) from `research/audit/shape/geom_check.my_slab` (AUTOMATON.md's cube-index table, not
the doubled offsets that `thin.py` uses). Validation:

    python3 research/audit/thin/tt.py validate 16 3000 16    # also 11 3000 11, 12 3000 12: population x copies = engine, every generation
    python3 research/audit/thin/tt.py vtrace 16 det 0 3 300  # walls; also model w = 5 (ring, segment), w = 1, w = 4 on b = 12

`validate` tiles the slab into the engine's cubic N-torus. The populations agree at all 3,000 generations on b = 16, 11 and 12.
`vtrace` checks every cell of every generation of one lane against a plain Python stepper, with walls held dead and coins
taken from the trace. There are 0 mismatches. The coin density is within 1σ of 102/256, and the coins have no lag-1
correlation. Life ends: a face is empty (checked every generation); a repeating state (snapshots at ages 16, 32, …,
compared every generation, so any period is found); three adjacent dead interior layers (checked every 16 generations);
end of run. Estimator: per-face τ = faces × exposure / deaths over ages ≥ T0 = 256, with no 30-lives cut. Run plan:
`research/audit/thin/plan.sh`, committed (295fa7a) before any production run.

## Verdicts

| claim | verdict | line | review |
|---|---|---|---|
| 5. exact M(1): ring of 5, segments | **stands** | 3.967199; 2.453108 (n = 2), 4.192750 (n = 5) | 3.967199; 2.453108; 4.192750 |
| 7. forecasts before runs; scoring | **stands with corrections** | | see below |

## Claim 2: segments

**Construction.** The face cells of sites 0–2 are held dead on both faces, at the same sites. Site s = {Z_s, Y_s,
X_{s+1}}, as in ring.c's NOTCH. Layers 1–6 stay a full ring.
- `tt.py geom 16`: within the face layer, two dead sites already separate the two ends. A face cell reaches at most
  two sites along the ring. The README's "three sites is the least that keeps the two ends from seeing each other
  inside the face" is therefore wrong in its wording: three is a choice, not a minimum.
- The ends still see each other through the substrate, which has no ends. `beneath.py` (6 lanes, b = 32, both faces
  alive, output in `beneath_out.txt`) shows the substrate is not neutral beneath the wall. Layer 1 is denser beneath
  the wall than in the middle (0.456 against 0.413), and so is layer 2 (0.412 against 0.395). Layer 3 is unchanged
  (0.393 against 0.399). The face next to the wall holds 0.384 against 0.441.
- So the "free end" is a dead boundary over a periodic, locally denser support. That is a legitimate and well-defined
  boundary condition, and its effect is an O(1) end term in ln τ, so it does not enter γ. But it is not shown to be the
  free end of a physical strip, and nothing about end costs should be read from it.

**Re-measured** (tags s21, s29; s37 pending):

| n | review | line |
|---|---|---|
| 21 | 9.1719(16) (403k deaths; the two chunks differ by 2.7σ) | 9.1708(15) |
| 29 | 11.5564(18) (312k) | 11.5533(29) |
| slope 21 → 29 per site | 0.29806(30) [0.09935 per cell] | 0.2978(4) |

## Claim 4: noise is enough from five layers

`tt.py` model mode: rule on layers 0..w−1, layers w and w+1 redrawn every generation with density 102/256, one face,
life cut at three adjacent dead layers among 1..w−1. Ring b = 16; tags r16, m16w5, m16w4 (`python3 research/audit/thin/tt.py stats 'm16*' r16`).

| | review | line |
|---|---|---|
| deterministic ring b = 16 | 8.6449(12) (658k deaths) | 8.6470(16); census 8.6426(20) |
| M(5) | 8.6466(13) (550k) | 8.6534(26) |
| M(5) − det | **+0.0017(18)** | +0.006(3) |
| M(4) − det | **+0.0497(23)** | +0.049(3) |

**Stands.** The two M(5) values differ by 0.007(3), 2.3σ. The differences agree within 1.3σ. At b = 16, M(5) is equal to
the deterministic ring within 0.004. b = 24 and segments were not rerun. M(4) reproduces exactly. The hazard is flat in
age in all three tags (by-age columns of `stats`).

## Claim 3: the headline 0.099 ± 0.004 per cell

`python3 research/audit/thin/refit.py` (lifetimes; output in `refit_out.txt`) and `python3 research/audit/thin/refit_win.py`
(routes 3 and 4 from the line's `data/windows.json`; output in `refit_win_out.txt`). γ is per site; per cell is in brackets.

- **Segments (route 2).** Every form below fits the line's own data acceptably, yet γ ranges from 0.279 to 0.305:
  - a + γn + c/n: 0.2920(3) [0.0973], χ² 17/15 from n ≥ 13. This is the best-fitting simple form over the widest
    range. It gives 0.2937 from n ≥ 17 and 0.2949 from n ≥ 21.
  - a + γn + c ln n: 0.2889(12) [0.0963], χ² 9/11 from n ≥ 17.
  - a + γn + c√n: 0.2793(23) [0.0931], χ² 10.6/11 from n ≥ 17. This form was not tried by the line on lifetimes. It
    fits as well as the others.
  - a + γn + c/n + d/n²: 0.2954 from n ≥ 13 and 0.2974 from n ≥ 17.
  - a + γn + c ln n + d/n: 0.3019–0.3048.
  - The straight line from n ≥ 25 (0.2970(4), χ² 1.7/4) holds only because n = 37 and 45 carry errors of 0.007 and
    0.020. Every curved form also fits n ≥ 25 (χ² 1.5–1.6/3), with γ = 0.298–0.301 and errors of 0.003–0.010.
- **Rings (route 1).** Contrary to "no stable fit", the line's six rings are fitted well by:
  - a + γb + c ln b: 0.2817(38) [0.0939], χ² 0.8/3; 0.2809 from b ≥ 20.
  - a + γb + c/b: 0.3061(20) [0.1020], χ² 2.0/3.
  - a + γb + c√b: 0.233(7), χ² 0.7/3.
  - The data cannot tell these apart.
- **Front from a wall (route 4).** ln W(x) = c − γx − p ln x is the line's form and gives 0.3031–0.3038 on every range.
  Adding a third term moves γ:
  - + q/x: 0.3032–0.3060;
  - + q ln x/x: 0.304–0.309;
  - with −a√x − p ln x: 0.304–0.316.
  - −a√x alone fits worse but not badly (rms residual 8e-4 against 5e-4) and gives 0.285–0.293. "The same g on every
    range" holds only within the one two-term form.
- **Windows (route 3)** depend wholly on the form, for example 0.270–0.297 with √l and 0.311–0.318 with ln l, and
  drift with the range. The upper end of the line's interval (0.309) comes from this route. It does not constrain γ.

**Verdict: does not stand as an error bar.** ±0.004 per cell (±0.011 per site) is the spread of the forms the line chose.
Forms it did not use fit its data equally well and fall outside the interval: √n on segments (0.279), ln b on rings
(0.282), a third term on the wall (up to 0.31). My range from the routes that constrain anything (segments, rings,
wall): **γ = 0.28–0.31 per site, 0.093–0.104 per cell, centre about 0.098**. That is ±0.006 per cell, and it is still a
spread of forms rather than a confidence interval. "0.0993(3) per cell between A = 75 and 135" is fine as a mean local
slope; its (3) is statistical only. The ordering "the segment slope is the lowest and flat since n ≈ 25" stands. Its
flatness is within errors that grow from 0.0004 to 0.003 per site over that range.

## Claim 6: how the face dies

`tt.c -P` records, at a face death, the face's cells over the 32 generations before it. `python3 research/audit/thin/prof.py s29 32 3`
(segment n = 29, 2,994 deaths) and `… r32 32 0` (ring b = 32) analyse them. The output is in `prof_*.txt`. For each lag k
(generations before the empty one) they give the mean population, the occupied sites, the span of the live region,
the islands (runs separated by ≥ 2 empty sites), and the extent of the live region to the left and to the right of
the site of the last live cell.

Segment n = 29, lags 1, 2, 3, 4, 6, 10, 20, 31:

| | k = 1 | 2 | 3 | 4 | 6 | 10 | 20 | 31 |
|---|---|---|---|---|---|---|---|---|
| population | 1.71 | 4.11 | 7.11 | 9.35 | 12.96 | 18.70 | 27.62 | 32.38 |
| span (sites) | 2.7 | 5.4 | 7.4 | 9.0 | 11.5 | 15.1 | 20.5 | 23.3 |
| islands | 1.22 | 1.47 | 1.57 | 1.63 | 1.75 | 1.89 | 2.10 | 2.25 |
| extent left / right of the last site | 1.4 / 0.4 | 2.8 / 1.8 | 3.8 / 2.9 | 4.6 / 3.7 | 5.9 / 5.0 | 7.6 / 6.9 | 10.4 / 9.6 | 11.6 / 11.1 |

- The population falls 1.7, 4.1, 7.1, 9.4, 11.3, 13.0 at k = 1–6. The line gives 1.7, 4.1, 7.0, 9.2, 11.0, 12.5 at
  n = 21, a close match.
- The live region contracts on both sides of the place where the last cell dies, almost symmetrically. Its span falls
  from 23 sites to 3 over about 30 generations. In the last 5 generations it loses about 1.3 sites per end per
  generation; at k = 10–30 it loses about 0.4. Two islands are common at k > 10, one at the end.
- That is the line's picture, an island shrinking from its ends, and it **stands**.
- The half-collapse lag depends on the reference population. Against the segment's own living population (32.4 at
  k = 31, which equals 0.371 × 87) the lag is 8.2 generations at n = 29. The line gives 9.8. The line's segment lags
  appear to take the ring density 1.33 per site as the reference, which lengthens them. I inferred this from the
  numbers and did not read it in the code.
- Beneath gaps (`gap.py`, ring b = 48, 3 lanes, output in `gap_out.txt`), at the middle of a maximal empty run:

  | run | layer 1 | layer 2 | layers 3–4 |
  |---|---|---|---|
  | 4 sites | 0.194 | 0.337 | 0.39–0.41 |
  | 8 sites | 0.317 | 0.362 | 0.39–0.41 |
  | mean of the layer | 0.414 | 0.395 | 0.400 |

  This agrees qualitatively with under.py: layers 1–2 thin, layer 3 does not. Layer 1 is thinner here at a run of 4
  (0.19 against 0.26), possibly because the definitions differ (maximal runs here).

## Claim 5: exact one-layer model

`python3 research/audit/thin/exact.py 5 0` (ring b = 5), `… 8 3` (n = 5), `… 5 3` (n = 2). Output is in
`research/audit/thin/exact_out.txt`. This is my own code. The coin-sharing components come from union-find on the
review's graph. They are five triples of 3 face cells × 6 coins on the ring, which confirms `exact1.triples`
independently; the segment of 5 has components 2, 3, 3, 3, 3, 1. The kernel is the product over components, iterated
as two matrix products until λ moves by less than 1e-13. ln τ = −ln(1 − λ). All three values agree with the line to
all six decimals. I did not recompute n = 6, 7 (n = 6 was started and stopped for want of cores).

## Claim 7: forecasts

`git log -p research/theory/thin/PREDICTIONS.md`: no committed forecast line was ever changed afterwards. The only
removals are a "Known" paragraph inside a scores block (7105d83) and a header time, 22:03 → 22:00 (c36f775). I took
the time of each tested tag's first chunk from its mtime in `research/scratch/thin/`, minus about 60 s for a chunk. Every
block's first tested run started after its commit: Block 1 20:46:33 / det_b16 ≈ 20:46:30–20:47; Block 2 20:59:36 /
first wall run 21:17; Block 3 21:14:29 / k = 2 22:42; Block 4 21:28:53 / seg_m1_n5 ended 21:30:45; Block 5 22:00:09 /
seg_det_n61 ended 22:01:13; Block 6 22:05:29 / n = 45 22:54. Two of these are seconds apart (Block 1, Block 5): the
runs were launched with the commit, not after anything was seen. That is admissible but not provable from mtimes.
Scoring:
- The misses F5 and F7 are scored correctly. F5(a) was scored against the ring slope at b = 32–36 because b = 48 was
  not run, so strictly it is "untested" rather than a miss. It is conservative.
- The four halves are generous. F3 has 3 of 6 rows missed, one with the wrong sign, and one half. F11 has 1 of 3 parts
  hit. Its k_wall(20) = 0.3182 is called "at the upper edge" of 0.298–0.318: it is outside, and it is in any case
  scored a miss. F4 and F13 are fair halves. The honest tally is hit 8, half 2 (F4, F13), mostly-miss 2 (F3, F11),
  miss 2.
- F6 is scored "hit" although its stated mechanism ("no drift like the ring's") failed once the n = 13 value was
  corrected, and "the ring falls towards the same value" was untested. It should read "hit on numbers, the clause
  untested/failed".
