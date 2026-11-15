# Review of research/theory/thin/ (the thinnest periodic face)

Adversarial review, 2026-11-14 (started 23:30), of `research/theory/thin/` at commit 15e14a7. Scripts in
`research/audit/thin/`; they share no code with the thin line. Bulk output in `research/scratch/audit_thin/` (ignored).
The plan was amended once, on wall-clock alone (`plan2.sh`, f6a7530): fewer chunks, and s45 and r36 dropped.
Production used about 1.7 h on two cores.

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
| 1. ring slopes still bending (0.1086, 0.1063 per cell at A ≈ 78, 90) | **stands**; a smaller bend, and the censoring text needs correcting | 0.1086(9) (72→84), 0.1063(13) (84→96) | 0.1081(3), 0.1067(4); ln τ at b = 16 … 32 agrees within 1.3σ |
| 2. segments 0.0993(3) per cell, straight A = 75–135 | **stands with corrections** (wording on the wall; tested to n = 37 only) | 0.2978(4), 0.2964(10) per site (21→29→37) | 0.2981(3), 0.2978(6) per site; 0.0993 per cell |
| 3. long-face limit 0.099 ± 0.004 per cell | **does not stand as an error**; the central value is plausible | 0.099 ± 0.004 | 0.093–0.107 per cell from the routes separately; 0.097–0.102 if they share a limit |
| 4. M(5) − det = +0.006(3) at b = 16 | **stands** | +0.006(3); M(4) +0.049(3) | +0.0017(18); M(4) +0.0497(23) |
| 5. exact M(1): ring of 5, segments | **stands** | 3.967199; 2.453108 (n = 2), 4.192750 (n = 5) | 3.967199; 2.453108; 4.192750 |
| 6. dies by an island shrinking from its ends | **stands**; the half-lag numbers are convention-dependent | profile 1.7, 4.1, 7.3, 10.1, 12.6, 14.8 (b ≥ 20) | 1.70, 4.05, 7.36, 10.14, 12.58, 15.16 (b = 32) |
| 7. forecasts before runs; scoring | **stands with corrections** (tally generous) | | see below |

## Claim 1: ring lifetimes

Tags r16, r24, r26, r28, r30, r32 (`python3 research/audit/thin/tt.py stats 'r*'`). Each is 4–6 chunks of 2,048 lanes. The
estimator is plain faces × exposure / deaths over ages ≥ 256, with no age cut. The hazard is flat across age classes in
every tag, and the chunk χ² is normal.

| b (A) | review | line | census |
|---|---|---|---|
| 16 (48) | 8.6449(12) | 8.6470(16) | 8.6426(20) |
| 24 (72) | 11.3494(19) | 11.3448(63) | 11.3481(40) |
| 26 (78) | 11.9941(20) | — | |
| 28 (84) | 12.6465(25) | 12.6482(83) | |
| 30 (90) | 13.2865(28) | — | |
| 32 (96) | 13.9268(43) | 13.9233(139) | |

Local slopes per cell, review against line:

| A | review | line |
|---|---|---|
| 72 → 78 | 0.1075(5) | |
| 78 → 84 | 0.1087(5) | |
| 84 → 90 | 0.1067(6) | |
| 90 → 96 | 0.1067(9) | |
| 72 → 84 | **0.1081(3)** | 0.1086(9) |
| 84 → 96 | **0.1067(4)** | 0.1063(13) |

**The bend is real.** It is 0.0014(5) per cell between the two 12-cell slopes, 2.9σ, against the line's 0.0023(16).
Every one of my ln τ agrees with the line's and the census's within 1.3σ. My rings alone, b = 24–32, are close to
straight: γ = 0.1076 per cell, χ² 6.8/3. From b = 16 they reject every three-parameter form in `refit.py`
(c/b, ln b, √b; χ² 7.6–11.7/3) except a fast exponential (ξ = 3, limit 0.107 per cell). That bears on claim 3: the
ring route alone does not point to 0.099.

**Censoring and lives that stop dying.** `python3 research/audit/thin/tailcheck.py` reads the line's raw chunk files.
For each tag it compares the deaths observed in the old-age tail (> 4 and > 8 mean lane-lives) with those a flat hazard
predicts. The output is in `tailcheck_out.txt`.
- No tag in use for the ring or segment lifetimes (det_b*, seg_det_n13 … n45) has excess exposure in the tail.
- Two model tags do, which is the signature of undetected stuck lives:
  - mod_b16_w6: ages > 11 lives, 1 death against 29.5 expected; exposure out to 23 lives.
  - seg_m5_n13: ages > 9.8 lives, 74 against 202; exposure out to 20 lives.
- Both stay inside the line's cut, because the cut is at the first power of two above 30 τ, so they enter the quoted
  values. Their size is small: about 2 × 10⁻⁴ and 1.4 × 10⁻⁴ in ln τ, far below the quoted errors.
- **The 30-mean-lives rule is not the protection the write-up suggests.** Chunks are 5–10 lane-lives long (det_b36:
  2 × 10⁷ generations, about 5τ), so no age ever reaches 30τ, and the rule could not have caught a stuck life in a
  large tag. What protects the deterministic tags is the any-period repetition test, which is airtight for a
  deterministic finite state. The tail test confirms there is no excess.
- **Bias of the rule itself:** for a flat hazard, truncating at an age the chaotic state does not reach (survival
  e^-30) changes neither deaths nor exposure, so it cannot bias ln τ.
- The README's claim (ii) ("none in any tag in use") is true of exposure *beyond the cut*. It is not true of stuck
  exposure below it, as the two model tags show. The wording should say so.
- Small segments (n ≤ 9): with the firewall looked for only every 840 generations, most firewalls in lives of about
  100 generations are never seen. The isolated face then dies, and its death is counted. My stepper looks every 16
  generations and finds a firewall in 22% of the ends at n = 7 (a 200k-generation test, not kept). The line's
  "deterministic values at n ≤ 6 are rough" understates this. It does not touch n ≥ 13.

**Old firewall rule (det_b16, det_b20).** The review's r16 uses the three-dead-layer rule, checked every 16 generations.
It agrees with det_b16 within 1.0σ (−0.0021(20)), so the old rule does not matter at b = 16, where firewalls are
commonest. b = 20 was not rerun, but its effect can only be smaller there (4 firewalls per 75k deaths).

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

**Re-measured** (tags s21, s29, s37):

| n | review | line |
|---|---|---|
| 21 | 9.1719(16) (403k deaths; the two chunks differ by 2.7σ) | 9.1708(15) |
| 29 | 11.5564(18) (312k) | 11.5533(29) |
| 37 | 13.9390(48) (43k) | 13.9246(73) |
| slope 21 → 29 per site | 0.2981(3) [0.0994 per cell] | 0.2978(4) |
| slope 29 → 37 per site | 0.2978(6) [0.0993 per cell] | 0.2964(10) |

**Stands with corrections.** The segment law is straight within 0.0003(7) per site between n = 21–29 and n = 29–37,
and the cost per cell 0.0993 reproduces. n = 45 was not rerun, so "to A = 135" rests on the line's 16.32(2) alone.
Corrections: the wording on the wall (above), and a statement that the wall perturbs the substrate.

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

The review's own rings (claim 1) add a fact: from b = 24 to 32 they fit a straight line at 0.1076 per cell, and
a fast-decaying correction extrapolates to 0.104–0.107. So the ring route allows limits up to about 0.107.

**Verdict: does not stand as an error bar.** ±0.004 per cell (±0.011 per site) is the spread of the forms the line chose.
Forms it did not use fit its data equally well and fall outside the interval: √n on segments (0.279), ln b on rings
(0.282), a third term on the wall (up to 0.31). My range, route by route:
- segments: 0.093–0.102 per cell;
- rings: 0.094–0.107;
- wall: 0.095–0.105;
- all routes together, without assuming a common limit: **0.093–0.107**;
- if the routes share a limit (the line's conjecture), the overlap is **0.097–0.102**.

So "0.099 ± 0.004" should become "≈ 0.099, between 0.093 and 0.107 depending on the unknown correction form (0.097–0.102
if the four routes share one limit)". This is still a spread of forms rather than a confidence interval. "0.0993(3) per cell between A = 75 and 135" is fine as a mean local
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
- Ring b = 32 (4,497 deaths): the population looking back is 1.70, 4.05, 7.36, 10.14, 12.58, 15.16 against the line's
  1.7, 4.1, 7.3, 10.1, 12.6, 14.8. The live region's span falls from 27 sites to 2.7, and it shrinks from both sides of
  the last site at similar rates (extents left/right 1.0/0.8 at k = 2, 3.1/2.8 at k = 6). There are often two islands
  (2.4 on average at k = 31, 1.24 at k = 1). The half-lag against 1.33 × 32 = 42.6 cells is 8.9 generations. The
  line's 7.8 matches it if the line counts the lag from the last non-empty generation.
- The half-collapse lag depends on the reference population. Against the segment's own living population (32.4 at
  k = 31, which equals 0.371 × 87) the lag is 8.2 generations at n = 29. The line gives 9.8. Its segment lags seem to
  take the ring density 1.33 per site as the reference: against 38.6 my lag is 10.5, or 9.5 with the same off-by-one.
  The "0.39 per site" for segments is therefore a convention, not a second rate. I inferred this from the numbers and
  did not read it in the code.
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

## Corrections the write-up needs

1. §1, §3, the headline: replace 0.099 ± 0.004 by the range in claim 3, and say it is a spread over correction forms.
   It is 0.093–0.107 route by route, and 0.097–0.102 only under the common-limit conjecture. Route 3 (windows) gives no
   bound. The c√n form fits the segment lifetimes as well as the others (χ² 10.6/11 from n ≥ 17) and gives 0.093.
2. §3, route 1, "no stable fit": c ln b fits the six rings (χ² 0.8/3, 0.094). The review's sharper rings b = 24–32 are
   near-straight at 0.1076. Say that the ring route allows limits from 0.094 to 0.107.
3. §8 (ii): the 30-mean-lives cut cannot act in any large tag, because chunks are shorter than 30τ. The protection is
   the any-period repetition test. Two model tags (mod_b16_w6, seg_m5_n13) do hold undetected stuck exposure below the
   cut, worth ≤ 2 × 10⁻⁴ in ln τ. "none in any tag in use" should be qualified.
4. §2 / ring.c comment: "three sites is the least that keeps the two ends from seeing each other inside the face".
   Two suffice; three is a choice. Add that the substrate beneath the wall is denser in layers 1–2 (0.456 and 0.412,
   against 0.413 and 0.395), so a segment end is a specific boundary condition.
5. §5: say which reference population and which origin the half-collapse lags use. The segment value 0.39 per site
   against the ring's 0.29 seems to come from using the ring density for the segment. Two islands are common in the
   last 30 generations of a ring, so it is not a single island throughout.
6. §8: at n ≤ 9, firewalls checked every 840 generations are mostly missed, and the isolated face's death is counted.
   About 22% of life ends at n = 7 are firewalls when checked every 16 generations.
7. PREDICTIONS tally: F3 and F11 are mostly misses, not halves. F6's "no drift" clause failed. F11(b)'s 0.3182 is
   outside 0.298–0.318, not "at the edge".

## Not checked

- The review did not rerun rings of b = 20 or 36, segments of n = 45 or 61, the windows on b = 64 (route 3 was refit
  from the line's curated histogram only), the wall statistics (route 4 likewise), M(w) at b = 24 or on segments, the
  density dependence (F4), the 12-layer slab, the closures of §6b (pca, knowing coins), or the wider torus (1,2),(0,b).
- The exact M(1) at n = 3, 4, 6, 7 (only n = 2, 5 and the ring of 5) was not recomputed.
- The under.py statement about layers 1–3 thinning *before* a gap opens was not checked; only gaps already open were
  (`gap.py`).
- The line's `analyze.py` and `run.py lntau` were read, not executed. Their numbers were taken from `data/*.json` and
  the raw chunk files.
- My stepper's life logic (settled, firewall, exposure) was checked by agreement with the line on 12 tags and by
  flat hazards. There is no separate test of it like the line's `validate_dump`.
- The RNG is splitmix64 with one stream per process. It was not cross-checked with a second generator.
