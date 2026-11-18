# REVIEW (referee `ref-report`): `research/blast/REPORT.md` against its sources

2026-11-18, 05:45 to 06:00 UTC. No simulation run; every item is the report's sentence against the named file.
"Paste:" is the sentence I propose. Not read: anything under `research/scratch`; `gpu-local`; agents' code.

State of `ref-dicehull/`: an interim `REVIEW.md` is committed (3128836; written 05:23 to 05:50). Its five-line
verdict and section (d) are complete; five table placeholders (GUMPROWS, VARROWS, TAILROWS, POOLROWS, DURROWS) are
still unfilled. Its verdict changes the report's headline on the 135-cell face (A1).

## (A) Wrong or overstated, most serious first

1. **The 135-cell "measurement" (short version; "The 135-cell face"; "What is not known" 1).** Report: "reads
   **29.398 ± 0.048**: 3.5 errors above ... 4.9 above", "about 29.40, +0.06, −0.15", "disagree by about 0.18 ...
   the hull's second difference growing (0.86 ± 0.05)", "no clear drift with size". Source, `ref-dicehull/REVIEW.md`:
   chain value reproduced (29.420 ± 0.068 fresh, pooled 29.447 ± 0.036), but "(d) 'R = 17 is above both' **REFUTED
   as a claim; not excluded as a fact**. Gump at 135 cells from this method: **29.30 ± 0.09**"; like with like the
   sampler-minus-gump offset GROWS (+0.001, −0.044, +0.053, +0.120 ± 0.040 at 45, 63, 84, 108 cells; a constant
   rejected, χ² 11.5 on 3; +0.14 ± 0.08 at 135); "29.230 is 0.8 errors below, 29.163 is 1.5 errors below ...
   **Nothing is decided** ... 'above them by 5 and 7 errors' should not be repeated". Also `split-hull/README.md`
   itself gives a third reading the report drops (offset linear in the area: 29.364 ± 0.070, +1.9 / +2.9 errors).
   Paste (replacing the paragraph after the table, the "So the forecast and the first measurement disagree"
   paragraph, PENDING_DICEHULL_FINAL, and the last two sentences of the short version): "The chain's value
   reproduces with fresh seeds (29.447 ± 0.036, 146 replications), but its referee (`ref-dicehull/REVIEW.md`,
   interim) finds the replications heavy-tailed and the sampler's offset from gump growing with size (+0.12 ± 0.04
   at 108 cells once the one giant replication is set aside; +0.14 ± 0.08 extrapolated to 135): **for gump 29.30
   ± 0.09 by this method**, 0.8 errors above the forecast 29.22 and 'the second difference repeats' (29.230), 1.5
   above 'the wrapped price takes over' (29.163). Nothing is decided at 135 cells; the surrogate does not show a
   growing second difference, and it does not exclude one."
2. **"My own forecasts, 14 scored: 7 held ..., 7 failed or half failed."** `PREDICTIONS.md` blocks give: held 4
   (the two 96-cell faces, the bend of loops 13 and 16, block 3 item 3); "counted held" with no table read 1
   (block 4 item 3); half right 2 (block 3 items 1 and 4); failed 6 (block 1 items 1 and 4, block 2 item 3, block 3
   item 2, block 4 items 1 and 2). Block 4's two failures are not in the report's count. Block 2 item 5, which the
   report counts as held, is "open" in the file, and as worded (more frequent over-full generations or fewer
   survivors account for more than half the discount) it failed: `boom/README.md` item 6, "over-full exactly as
   often ... the same survivors", four-layer share 0.076 of 0.164 (46%). "The staggered crash in substance" is
   scored "half right" there. Paste: "My own forecasts, 13 scored: 4 held, 1 counted held without a measurement, 2
   half right, 6 failed (band-first deaths; wide tori carrying the front term; the strip's width price; the halves
   of the 192-cell tube; both numbers of the timing chain, block 4); block 2 item 5 failed as worded (the tube
   does not boom more often or leave fewer survivors); blocks 1.3, 2.2, 2.4 unscored."
3. **Item 5 and "not known" 3, the 192-cell surrogate numbers.** Report: "38.71 ± 0.18 for the 192-cell tube and
   40.59 ± 0.19 for a wide 192-cell torus", "sits at or above the line". `split-slab/README.md` l.264: 40.588 is
   the raw chain (40.536 after the offset; the other two numbers are after the offset). `ref-slab/REVIEW.md`:
   "The 192-cell numbers may not be quoted as measurements"; wide 192: fresh 39.75 ± 0.46, all 26 pooled **40.25 ±
   0.26**, line 40.07, "above the line NOT ESTABLISHED". The "two wide runs −0.33 and +0.51" are at 144 and at 192
   cells. Paste: "38.73 ± 0.18 for the 192-cell tube and 40.25 ± 0.26 for the wide 192-cell torus as pooled by
   the referee (line 40.07); neither is a measurement to its quoted error" and, in "not known" 3, "sits within
   its error of the line".
4. **Item 5, "24.64 ± 0.07 for the 120-cell tube" in bold.** The referee's corrected pooling is 24.60 ± 0.07
   (`ref-slab/REVIEW.md` verdict 4), which the report itself uses in two other places. Paste: "24.60 ± 0.07 (the
   referee's pooling of 102 replications; the agent's own 24.64 ± 0.07)".
5. **"What is not known" 4: "The dip rate keeps its second difference to 198 cells."** `ref-hull/REVIEW.md`: "the
   second difference in k of ln ν(0.6 P̄) is not constant", −0.176 → −0.160 ± 0.004, and the report's own 135
   section says it shrinks. Paste: "The dip rate's second difference shrinks from 135 to 198 cells at one level
   (not at the next), so even the measured half does not say that 0.231 lasts."
6. **Short version: "almost every live cell has six or more live neighbours and dies."** `ref-anatomy/REVIEW.md`
   table: "every live cell is then overcrowded" CORRECTED, "80.3% ... four in five"; 99.5% is the share of the
   cells that die. Paste: "Then four live cells in five have six or more live neighbours and die".
7. **Theorem 3: "its hypothesis is failing, visibly [measured ...]" and "a first-order transition ... which a
   rimmed face does not have".** `ref-proofs/REVIEW.md` §3: "Is the hypothesis plausibly false? Yes: on wrapped
   faces ..., **and probably on rimmed faces too**": the 30-cell triangle has "a flat plateau from 5 to 12 live
   cells at s = 0.2", and the slope criterion "rises in both families" (tori 1.5, 2.5, 3.3; triangles 2.6, 2.7,
   3.6). "First-order transition" is not the referee's phrase. Paste: "its hypothesis is plausibly false (the
   referee's words), on wrapped faces visibly and probably on rimmed ones too (a plateau at 30 cells; the
   variance criterion rises in both families) ... [conjectured, the PI's reading] the two exits are a first-order
   transition in the emptying ensemble, clear on wrapped faces to 27 cells."
8. **Item 6: strips "have the hull's number in their mixed second difference, 0.2262 ± 0.0078".** `rim/README.md`
   §3 gives three values: 0.2741 ± 0.0029, 0.2590 ± 0.0087, 0.2262 ± 0.0078, and "one step earlier the same
   quantity is 0.27 ... cannot tell a plateau at 0.231 from a slow bend to 0.209". Paste: "their mixed second
   difference passes through the hull's number (0.274, 0.259, then 0.2262 ± 0.0078 at the largest step), with no
   corner anywhere; whether it stops there is not measured."
9. **Forecast table: "200-cell wide torus 41.716 ± 0.05 (the line)".** `model/PREDICTIONS.md` l.97: the wide line
   is 41.742; 41.716 is model's bent form (slope 0.2069). Paste: "41.716 ± 0.05 (0.026 below the line's 41.742)".
10. **"Four forecasts, by different routes, all frozen before any of the others was read."** `PREDICTIONS.md`
    block 2 says only that rim's and model's were "both blind to the samplers"; I found no statement that
    split-hull's dip-rate route was frozen unread. The report's next paragraph ("one extrapolation seen four
    ways") is the accurate one. Paste: "all frozen before any sampler reported".

## (B) Missing caveats

1. Short version, "a forecast of 29.22 ± 0.02 that four routes agree on": the ± 0.02 is `ref-hull`'s figure for one
   route and is "conditional ... nothing if it does not [stay on its line]"; "excludes 29.163 by 2.8 errors
   conditionally, and is silent unconditionally". Paste: "a conditional forecast of 29.22 ± 0.02 (if a four-point
   straight line continues)".
2. Short version, "**A hull face starves**": `ref-anatomy/REVIEW.md` CORRECTED "deaths are starvation" to a tilt:
   of the face cells dying in the last 8 generations 57.8% starved, 42.2% overcrowded (living hull face 39.3 /
   60.7). Paste after "the slow way": "(a tilt, not a pure starvation: 58% of the cells of a dying hull face
   starve, against 39% on a living one)".
3. Item 5, long-tube shares "0.50, 0.50, 0.38, 0.26, 0.17": `ref-slab` CORRECTED the 120-cell value to 0.42–0.45
   and "at 144–192 cells the shares are good to ± 0.1 at best". Paste: "(120 cells: 0.42–0.45 by the referee; the
   last two ± 0.1)". Also "the last three blind": the referee did "NOT TEST" the blindness (commit times not
   audited), and the surrogate's offset is brute-forced only to 84 cells.
4. Item 5, "a tube booms exactly as often ... the same survivors": `boom/README.md` item 6 marks it "[measured,
   54–84 cells]" and continues "about half of it is that the four-layer over-fill is more frequent on the tube".
   The report puts that half only under "What failed". Paste: add "(54–84 cells; the face alone: the four-layer
   launch state is more frequent on the tube and is about half the discount at 72 cells)".
5. Item 5, "K = 2": `tube1d/README.md`: K = 3 fits as well (χ² 3.2), K free = 2.5, "tubes alone do not separate
   K", K = 1 "not excluded on its own". The PI's "K = 2 is a count of timings" rests on it. Paste: "K = 2 or 3".
6. 135 section, "no sign of the hull crossing to the other exit": `split-hull/README.md` same line: "falls of 0.4 A
   go from 3% to 9%" from 84 to 135 cells. Paste: add "(falls of 0.4 of the face rise from 3% to 9%)".
7. Item 2, "the last cell is on the rim line 54% of the time": the rim line is about half the face's cells; the
   enrichment is 1.10 (`anatomy/README.md` §4 table). Paste: "54% of the time (1.10 times its share of the cells)".
8. Not refereed, and the report does not say so although its first paragraph promises to: `tube1d/` (band = tube
   identity, the K fit, loop² 16), `rim/` strips, `toy/` (item 7), `model/` forms, `image/`'s measured statements,
   `split-slab/` §9–§10 (the staggered crash), `boom/`'s tube results. Paste one line in "Referees": "Not
   refereed: items 5 (except the sampler), 6 (strips), 7, and the timing statistics."
9. Item 3, "recomputed the shares to every digit": exact to 15 cells; the 18-cell rimmed share 0.003 was checked
   by simulation only (0.0028 ± 0.0001, 1.9σ; `ref-proofs/REVIEW.md` l.84).
10. Item 4, "0.136 ± 0.001": `ref-boom/REVIEW.md` by pairs: J = 0.136, 0.136, **0.147 ± 0.006** and I_up 0.079,
    0.080, 0.076 for 48→57, 57→63, 63→75 cells: steady only to 63 cells.
11. 135 section, the shrinking second difference: `ref-hull` adds "a drift seen at one level and one density, 3.6
    errors at its last point, not yet a law"; level 0.5 gives 43.080 ± 0.039 at 198 cells (on "repeats").
12. "Not known" 2, "the remaining 0.05": `ref-boom/STATIC.md` has 0.057 ± 0.003, and the total of those runs is
    0.2174 (48–63 cells), not 0.21. Paste: "the remaining 0.06".

## (C) Important omissions

1. `ref-dicehull`'s verdict (A1), and what it says would decide: a brute-force value of the chain at 84 cells
   (separates "the chain is not gump" from "the sampler's tail"), not only more replications.
2. The surrogate's 192-cell tube (38.73 ± 0.18, ± 0.3 for drift) is never set against `tube1d`'s frozen 39.17 /
   39.01 / 38.92 / 38.86 in the forecast table: it lies below all four and, at ± 0.3, decides none.
3. `ref-hull`'s next step: measure the dip rates ν(0.6), ν(0.4) on wrapped faces by plain running; cheap, and it
   says whether the 0.022 per cell between rimmed and wrapped lives in ν or in q. Absent from "what I would do".
4. `ref-slab`: the sampler's weakness is a heavy-tailed estimator (dying chains descend from 9.5 ancestors at 192
   cells wide); `ref-dicehull` finds the same on the hull (5 to 13). This is the common cause of A1 and A3.
5. Block 2 item 4 (bust share above 40% at 108–240 cells) is unscored: held on wide tori, failed on tubes.

## (D) Internal contradictions and wording

1. Placeholders left in the text: `PENDING_DICEHULL_FINAL` (l.238), `PENDING_REFEREES_6` (l.309).
2. "(item 7)" for the failed samplers, twice (l.193, l.319): it is item 8.
3. The 120-cell tube is 24.64 ± 0.07 (item 5), 24.60 ± 0.07 (forecast table, Referees) and "still blind" ("What
   failed"); say once: surrogate 24.60 ± 0.07, gump itself not yet measured.
4. Stale: "being refereed by `ref-slab/`" (item 5) and "`ref-hull/` checking the second" (item 6); both verdicts
   are in "Referees".
5. "four fifths of its price" against "23% short" in the same paragraph: 0.1606 / 0.2087 is three quarters.
6. Item 5 "a tube booms exactly as often" against "What failed": "a more frequent four-layer launch state
   accounts for 0.076 ± 0.011 of the tube's 0.164" (see B4).
7. Item 1 "one cell alone regrows it 0.138" against Referees "clusters of 1 ... fail 0.900": different
   quantities (a face down to one cell; a one-cell cluster among others). Say so in one of the two places.
8. Item 2 "1.1–1.6%" against `ref-anatomy`'s "CORRECTED to 1.1–1.5%" and the Referees' 0.0108 ± 0.0014.
9. Item 1 "a breath of four layers" beside `ref-anatomy`'s "five layers deep" and the short version's "the three
   layers beneath": pick one count.

## Clean

Item 4's numbers and the two-layer map against `ref-boom/REVIEW.md` and `ref-map/REVIEW.md`; item 7 against
`toy/README.md`; item 8's sampler biases; the tilt and seam identities against `ref-proofs/REVIEW.md`; `tube1d`'s
band numbers and forecasts; `ref-hull`'s numbers in the 135 section; the static-rarity paragraph against
`ref-boom/STATIC.md` (except B12): every number I checked matches its source.

## Not checked

`pi/`, `gpu-local`, the GTX 1080 sentence in item 2, the 12-cell rows of item 3, `split-slab` §10's four numbers,
whether the 15-cell girth-1 share is 0.21, the layer and autocorrelation numbers of item 1 beyond `ref-boom`'s
confirmation, commit times of any forecast.
