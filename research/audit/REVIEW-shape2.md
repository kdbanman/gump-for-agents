# Review of research/shape2/: every torus of a given area

Adversarial review, 2026-11-14. Object: `research/shape2/` at 66fef15 (forecasts `PREDICTIONS.md` at 80906fe, write-up
`README.md`, `data/`). Scripts in `research/audit/shape2/`; bulk output in `research/scratch/audit_shape2/` (git-ignored).
The independent stepper is `research/audit/shape/ts.c` (bit-sliced, renewal lives, own RNG, own layer indexing, events
checked every 8 generations, cap 5 × 10⁵), driven through `drv.py`, which only redirects its output. Nothing is
imported from `research/shape2/` or `research/shape/`; `recompute.py` reads their CSVs, raw per-life files and
`predictions.json`.

    python3 research/audit/shape2/geom2.py        # classes at index 16 and 20, layer indexing vs T1, multigraph check (1 s)
    D=research/audit/shape2/drv.py; for L in "1 1 16" "2 0 8" "1 7 16" "1 2 16" "2 2 8" "1 6 16" "1 3 16" "4 0 4" "1 0 16"; do
      python3 $D validate $L 4000 16; done; for L in "1 1 20" "1 9 20" "2 0 10" "1 2 20"; do python3 $D validate $L 4000 20; done
    nohup bash research/audit/shape2/run_all.sh > research/scratch/audit_shape2/run_all.log &   # 3 cores, ~70 min
    python3 research/audit/shape2/compare.py      # this review's values against research/shape2's tables
    python3 research/audit/shape2/recompute.py    # their tables from their raw files; every chi^2, own law code (~10 min)
    python3 research/audit/shape2/law60.py        # forecast laws at A = 60 on independent / pooled values
    python3 research/audit/shape2/capcheck.py; python3 research/audit/shape2/pairage.py   # caps; pair difference by age
    python3 research/audit/shape2/fwcheck.py 2 0 8 2048 6000 7; python3 research/audit/shape2/earlycheck.py 1 1 16 32768 256 21

**Plan fixed before the runs** (`run_all.sh`, committed in 3cf07a5 before any production job): seeds 101–383, 1,024
replicas per job, no stopping rule. Total 1.5 × 10¹¹ life-generations.

**Validation.** On all 13 tori run here ts.c's population times the number of copies equals the engine's (cubic
N-torus, N = 16 or 20) at every one of 4,000 generations; the five thin ones (loop² 3, 4) also for two more soups ×
2,000 generations. `geom2.py`: the index-16 lattices fall into 9 point-group classes equal to the 9 Gram classes, and
each class's members, first six primitive norms and cut equal `classes_A48.csv` / `classes_A60.csv`. The transverse
layer index s = d·p mod P satisfies T1 on every neighbour pair of every torus (0 violations).

## Summary

| claim | verdict |
|---|---|
| 1. Tables | **stands with corrections.** All 24 rows reproduce exactly from the raw files. Independently, 16 rows agree (χ² 25 / 16; |Δ| ≤ 2.3σ). The loop² 4 rows depend on how a face death and a firewall in the same check window are split, by 0.03–0.07, which is 10–20 times their stated error. |
| 2. Cost per cell | **stands.** b(48→60) from this review alone: 0.1144 (loop² 3), 0.1415 (4), 0.1922 (7), 0.2076 (12), 0.2127 (16), against 0.1148, 0.1414, 0.1918, 0.2073, 0.2125. Chaos on the thin cylinders holds: flat hazard, almost no settling, permanent face death. |
| 3. Loop stops mattering at A = 48 | **stands.** The four classes span 0.0156; 4×4 lies 0.0135 ± 0.0021 below (12;19) and 0.0118 ± 0.0021 below (13). 12 → 16 is −0.006 ± 0.002 here, against +0.001 ± 0.003 in shape2. |
| 4. Second variable at equal loop | **stands; the A = 60 part is stronger than written.** A = 48: +0.0156 ± 0.0021 (7σ). A = 60: +0.0132 ± 0.0028 (4.7σ) independently. The fresh run's 0.006 is the outlier. Four runs pooled: 0.0142 ± 0.0019 (χ² 4.7 / 3). The cap does not explain it. |
| 5. Laws | **does not stand as written for A = 60.** The χ² values reproduce, and the forecast parameters were fixed before the runs. But "L3-area passes at A = 60" holds only on the fresh run. With this review's independent values it fails (χ² 22.7 / 5, p 4 × 10⁻⁴), and with all runs pooled it fails again (45.4 / 5). The test was also mostly in-sample: 5 of the 6 classes are the ones it was fitted on. After this correction no law survives at any area. |

## Claim 1: the tables

`recompute.py` rebuilds every row of `A48.csv`, `A60.csv` and `A72x.csv` from `research/scratch/shape2/ch_*.npz` with its own
first-event code. F, W and ln τ_face are identical in all 24 rows.

Independent values (ts.c; ln τ_face = ln(2E/F) ± 1/√F; `compare.py`):

| class | loop² | this review | shape2 | Δ/σ | firewall share (here) |
|---|---:|---|---|---:|---:|
| (1,1,16) | 3 | 8.6436 ± 0.0012 (721,896 F) | 8.6426 ± 0.0020 | +0.4 | 0 (1 tie) |
| (2,0,8) | 4 | 9.4807 ± 0.0018 | 9.4888 ± 0.0030 | −2.3 | 64.8% |
| (1,7,16) | 4 | 9.4782 ± 0.0018 | 9.4856 ± 0.0030 | −2.1 | 64.8% |
| (1,2,16) | 7 | 9.8110 ± 0.0017 | 9.8122 ± 0.0020 | −0.4 | 0 (3 ties) |
| (2,2,8) | 12 | 9.9254 ± 0.0015 | 9.9243 ± 0.0020 | +0.4 | 0.13% |
| (1,6,16) | 12 | 9.9410 ± 0.0015 | 9.9384 ± 0.0020 | +1.0 | 0 (6 ties) |
| (1,3,16) | 13 | 9.9393 ± 0.0015 | 9.9390 ± 0.0020 | +0.1 | 0.14% |
| (4,0,4) | 16 | 9.9275 ± 0.0015 | 9.9324 ± 0.0020 | −2.0 | 0.29% |
| (1,1,20) | 3 | 10.0161 ± 0.0023 | 10.0201 ± 0.0029 | −1.1 | 0 |
| (1,9,20) | 4 | 11.1794 ± 0.0031 | 11.1854 ± 0.0046 | −1.1 | 92.8% |
| (2,0,10) | 4 | 11.1758 ± 0.0031 | 11.1822 ± 0.0046 | −1.2 | 92.7% |
| (1,2,20) | 7 | 12.1175 ± 0.0032 | 12.1133 ± 0.0031 | +1.0 | 0 |
| (1,8,20) | 12 | 12.4220 ± 0.0035 | 12.4148 ± 0.0034 | +1.5 | 0.01% |
| (2,2,10) | 12 | 12.4270 ± 0.0035 | 12.4223 ± 0.0035 | +1.0 | 0 |
| (1,5,20) | 16 | 12.4735 ± 0.0020 | 12.4788 ± 0.0035 | −1.3 | 0.45% |
| (1,4,20) | 16 | 12.4867 ± 0.0020 | 12.4849 ± 0.0035 | +0.5 | 0.44% |

The rows agree with χ² 25 / 16 (p 0.07). Two places need a correction.

- **The loop² 4 rows depend on the check interval.** All four are lower here, by 0.006–0.008. On these tori a face death and
  a firewall often fall into the same check window. Both codes give such ties to the firewall. With shape2's 16-generation
  resolution the ties are 4.8% of face deaths at A = 48, 5.8% at 60 and 6.9% at 72. With ts.c's 8 generations they are
  2.7% and 3.2%. Counting the ties as face deaths gives 9.454 instead of 9.481 at A = 48 and 11.148 instead of 11.179 at
  A = 60 (this review). In shape2's data it would lower the values by 0.046, 0.056 and 0.067. Neither
  convention is right. Resolved per generation (`fwcheck.py`, 2,048 lives of (2,0,8)), 57 face-death/firewall pairs fall
  within 16 generations of each other: the face died first in 16 of them, the firewall first in 37, and 4 were in the
  same generation. About 30% of the ties are therefore face deaths. Add the rounding of each life's end up by 0–15
  generations (+0.004 at a mean life of 2,200), and the per-generation value lies about 0.018 below shape2's table:
  ≈ 9.47 at A = 48, against 9.4888 ± 0.0030 (about 6σ of the stated error). ts.c's value, at half the check interval,
  lies about 0.010 high. The loop² 4 values therefore carry a resolution-dependent bias of 0.01–0.02. The stated
  ± 0.003–0.013 do not cover it. The cost
  per cell b is nearly immune to it, because the shift is about the same at both areas: b(48→60) is 0.1415, or 0.1411 with
  ties counted as face deaths.
- **Loop² 1.** Lives last 17–22 generations, and the face "rate" is meaningless there: 7.57 in shape2's CSV against 6.97
  here, with ties outnumbering face deaths 3 : 1. The README rightly prints only "thin". The CSV's `ln_tau_face` for
  these rows should be blanked.

## Claim 2: cost per cell, and chaos on thin cylinders

From this review's runs alone, b(48→60) is 0.1144 (loop² 3), 0.1415 (4), 0.1922 (7), 0.2076 (12) and 0.2127 (16).
shape2's numbers are 0.1148, 0.1414, 0.1918, 0.2073 and 0.2125, and `recompute.py` reproduces the whole README table,
b(60→72) included. The b(60→72) entries for loop² ≥ 9 rest on research/shape's single A = 72 runs, which I did not rerun.

**Is it chaos in the same sense?**

- *Hazard flat in age.* For loop² 3, the equal-exposure thirds are 8.643, 8.644, 8.643 (± 0.002) at A = 48 and 10.017,
  10.013, 10.018 at A = 60. For loop² 4 they are 9.486, 9.480, 9.476 (± 0.003): a 2σ downward drift. At A = 60 they are
  flat. On every torus the hazard is raised in the first ~32 generations (the soup transient). Exactly, per generation
  (`earlycheck.py`, 32,768 lives of (1,1,16)): 8.52 in ages 0–32, then 8.60–8.70. Dropping ages below 256 moves
  ln τ_face by at most +0.002. (A first comparison of age bins between the codes showed a large disagreement at ages below
  64. It was an artefact of binning shape2's timestamps, which are ≡ 1 mod 16; per 16-generation slot the two codes agree.)
- *Settling.* At loop² 3, 58 of 724,003 lives settled before the face died at A = 48 and 1 of 185,039 at A = 60. At
  loop² 4, none of 1.8 × 10⁶ did. Censoring cannot bias these values.
- *Face death is the same event.* On any torus an empty boundary layer stays empty: a dead face cell has at most 3 live
  neighbours (T1/T2). `fwcheck.py` confirms 0 revivals. One real difference has not been reported: **the loop² 4 tori
  (and loop² 1) are multigraphs.** On (2,0,8), (1,7,16), (2,0,10) and (1,9,20), one cell in three has two of its 12
  neighbour slots on the same cell, and that cell is counted twice. On loop² 1 every cell does. On loop² 3 none does
  (`geom2.py`). This is the rule as coded (the engine tiling counts the slots, and both steppers match it). But on these
  tori a cell sees fewer than 12 distinct cells, so "a narrow cylinder of the same automaton" is literally true only for
  loop² 3.
- *Loop² 3 firewall channel.* It is not absent; it is closed in practice. (1,1,16) has a 4-layer diagonal (96 cells a
  layer, cut 288). Three of its four layers were dead once in 2.0 × 10⁹ life-generations, at the same check as a face
  death, and two adjacent layers were dead at 8 checks. (1,1,20) shows none. "No firewall channel (cut ≥ 288)" should
  read "no firewall observed (one tie in 2 × 10⁹ life-generations)". The same goes for (1,2,16) (3 ties) and (1,6,16)
  (6 ties).
- *Firewall detection on loop² 4* (own indexing, every generation, `fwcheck.py` on (2,0,8)). Three adjacent dead
  layers never revived (0 violations over 1,258 firewalls × the rest of 6,000 generations). The face-first share is
  0.342 ± 0.011 here, against 0.348 in ts.c and 0.346 in shape2. A face death hardly ever coincides with the whole slab
  dying (3 of 1,897 face deaths are followed by extinction within 16 generations). So on these tori a face death is not
  a global collapse. The detection is right; only the tie assignment (claim 1) is a convention. On (1,1,16) the same check (2,048
  lives, 3,000 generations) finds no firewall, no tie, and 8.655 ± 0.027.

## Claim 3: A = 48, loop² 12–16

This review's four values are 9.9254, 9.9410, 9.9393 and 9.9275 (± 0.0015), so the spread is 0.0156 (shape2: 0.0147).
The hexagonal 4×4 lies below (12;19,19) by 0.0135 ± 0.0021 and below (13) by 0.0118 ± 0.0021, so the classes are not
ordered by loop. Both runs say so: in shape2, 0.006 ± 0.003 and 0.007 ± 0.003. From pooled loop² 12 to 16 the change is
−0.0057 ± 0.0018 here and +0.0011 ± 0.0025 in shape2. Combined it is about −0.003 ± 0.0015: "about 0" stands, against
+0.056 ± 0.003 at A = 60 here (shape2 +0.063) and +0.10 at 72. "Within 0.015" should read "within 0.016". The verdict
still rests on four lattices only.

## Claim 4: a second variable at equal shortest loop

| pair | shape2 fresh | this review | other runs | pooled |
|---|---|---|---|---|
| A = 48 (12;16) → (12;19,19) | +0.0141 ± 0.0028 | **+0.0156 ± 0.0021** | — | +0.0151 ± 0.0017 |
| A = 60 (16;19) → (16;21) | +0.0061 ± 0.0049 | **+0.0132 ± 0.0028** | shape +0.0186 ± 0.0041, review +0.0177 ± 0.0042 | +0.0142 ± 0.0019 (χ² 4.7 / 3) |
| A = 60 (12;25) → (12;28) | +0.0075 ± 0.0049 | +0.0050 ± 0.0049 | — | +0.0063 ± 0.0035 (1.8σ) |

The A = 48 effect is confirmed at 7σ. At A = 60 the independent run is 4.7σ by itself. The fresh run (1.2σ) is the low
one of four, 1.3σ below this review's. The README's three-run mean is 0.0150 ± 0.0025 by my arithmetic (χ² 4.5 / 2),
not 0.014 ± 0.0026. The A = 60 loop² 12 pair is not significant (1.8σ pooled). "Three pairs, one sign" is true, but only
two of the three pairs are measured effects.

**The cap does not explain the fresh 0.006.** On research/shape's raw A = 60 data recensored at 65,536 (`capcheck.py`),
the pair difference is 0.021 ± 0.006. On this review's data truncated at 65,536 it is 0.006 ± 0.004, uncapped
0.013 ± 0.003. Binned by age over all three data sets (`pairage.py`), the difference is +0.010 ± 0.005 for ages
[0, 16k), +0.009 ± 0.004 for [16k, 65k), +0.017 ± 0.005 for [65k, 131k), +0.018 ± 0.005 for [131k, 262k) and
+0.020 ± 0.007 beyond. That is consistent with a constant 0.0134 ± 0.0021 (χ² 4.2 / 4). Young lives against old ones,
0.009 ± 0.003 against 0.018 ± 0.003, is a 2σ hint that the difference grows with age. If it does, a cap at 65,536 halves
the effect. Pooling the runs is justified at present precision. A cap-free rerun of the pair at ± 0.002 would settle
the hint (about 2 core-hours).

## Claim 5: the laws

- **Bookkeeping is right.** `predictions.json` has not changed since 80906fe (15:56:55). The first production file
  (`ch_1_0_16_s1000000.npz`) is from 15:56:56. `laws_report.txt` uses the json's B, K, E and nothing refitted. The degrees
  of freedom are distinct classes minus 1 (5, 6 and 11 classes). My own implementation of L1–L4 reproduces every χ² from
  the raw values: L3-area 134.6 / 4, 5.4 / 5, 28.2 / 10, against the README's 132.5, 5.4, 28.2. The small differences come
  from the CSV's errors being rounded to 4 decimals. The refits reproduce too: L3-area 22.1 / 2, 3.0 / 3 and 66.5 / 17;
  L1-area 33.6 / 2, 6.6 / 3; L2-area 33.0 / 2, 4.1 / 3.
- **"L3-area passes at A = 60" is a fluctuation, and it was in-sample.** The forecast parameters were fitted on
  research/shape's values of five of the six A = 60 classes; the fresh run re-measures the same five. The only
  out-of-sample class is loop² 7, which L3-area does predict well (forecast 12.108; shape2 12.113, this review 12.118).
  It passes on the fresh run because that run's pair difference is the low one.
  - With this review's independent values: χ² 22.7 / 5 (p 4 × 10⁻⁴).
  - Pooled with research/shape's values: 25.1 / 5.
  - Everything pooled: 45.4 / 5 (`law60.py`, `recompute.py`).
  So L3-area is refuted at A = 60 too.
- **The L1/L2 refutation at A = 60 rests on the loop² 7 class, on the fresh data.** Restricted to loop² ≥ 12, the fresh
  run gives L1-area 7.3 / 4 (p 0.12) and L1-const 8.2 / 4 (p 0.09), which is not refuted. With the independent or pooled
  values it is refuted even there (48 / 4 and 99 / 4). The pair difference above also refutes L1 at 60 by the committed
  ordering criterion (> 3σ at equal s₁).
- Caveat on the criterion: PREDICTIONS counted loop² 7 as "chaotic, ≥ 7", although every law was fitted on loop² ≥ 9. The
  huge χ² of L1, L2 and L3p come from that one extrapolation, so they measure the tail of the functional form. At loop²
  ≥ 12, L1–L4 fail at A = 48 anyway (χ² 26–857 on 3), because of the 5–7σ pair.

## Corrections the write-up needs

1. Verdict and the laws table: "L3-area passes at A = 60" → it passes on the fresh run only, whose pair difference is
   low; with independent or pooled values it fails (22.7 / 5, 45.4 / 5). Say also that 5 of the 6 A = 60 classes are the
   ones the parameters were fitted on. No candidate law survives at any area.
2. Claim 4: replace "0.006 ± 0.005 … pooled 0.014 ± 0.0026, χ² 4.6 / 2" with the four-run value 0.0142 ± 0.0019 (χ²
   4.7 / 3; this review independently 0.0132 ± 0.0028). The three-run mean is 0.0150 ± 0.0025. Mention the 2σ hint that
   the difference grows with age.
3. "Three pairs, one sign": the A = 60 loop² 12 pair is 1.8σ pooled. Say two measured pairs and one of the same sign.
4. Loop² 4 rows (A48, A60, A72x): add that ties between face death and firewall go to the firewall (5–7% of face
   deaths at 16-generation resolution), although about 30% of them are face-first when resolved per generation. With
   the rounding of life ends, the values are about 0.018 too high at A = 48 (≈ 9.47, not 9.489). The stated
   ± 0.003–0.013 do not cover this. b is robust to it (≤ 0.0005).
5. Loop² 3: "no firewall channel (cut ≥ 288)" → "no firewall observed; the 4-layer diagonal exists (one firewall, tied
   with a face death, in 2 × 10⁹ life-generations of (1,1,16))".
6. Thin tori: state that loop² 1 and 4 tori are multigraphs (a third of the cells count one neighbour twice on loop² 4),
   loop² 3 is not. The rule is the coded one, but the "narrow cylinder" comparison is cleanest at loop² 3.
7. "Hazard flat in every chaotic class": add the soup transient (hazard raised about 13% in the first 32 generations).
   Its effect on ln τ is ≤ 0.002.
8. Minor: A = 48 spread "within 0.015" → 0.016; blank `ln_tau_face` for the loop² 1 rows of the CSVs.

## Not checked

- A = 72: not rerun here, neither shape2's five new classes nor research/shape's ten. So b(60→72), the A = 72 law χ²,
  and the "fails at A = 72" verdict rest on their runs (± 0.004–0.014), plus the earlier review's for five classes.
- The A = 60 loop² 13 class (1,3,20) was not rerun.
- `explore.py`'s post-hoc loop sums (e^{−K|v|}/|v|, |v|^{−K}, Gaussian) and the residual analysis were not recomputed.
  Only L1–L4, with forecast parameters and refits, were.
- Event detection was not validated against the engine, only the stepping was. The face and firewall detectors are
  checked by agreement between the codes and by `fwcheck.py` (numpy, every generation) on (2,0,8) and (1,1,16).
- Whether the pair difference really grows with age (2σ).
- Near-firewall states on loop² 4 (two adjacent dead transverse layers at a large share of checks) and whether they
  change the face hazard, as the README also leaves open.
