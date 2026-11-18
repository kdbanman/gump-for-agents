# Check of the card's chain 3 and its CPU second code (2026-11-18)

Rows at HEAD 2364fd5 (the card's branch merged at 6a197ba; chain 3 rows from 3fb4ec0 and 03904b2). Arithmetic and
logic from rows only; nothing re-run.

    python3 research/audit/gpu_chain3_lead_check.py      # under 1 s; prints every number below, ends PASS

Estimator as `gpu_tubes_lead_check.py`: ln τ_face = ln(2 ΣE / ΣF) over a face's seeds, error 1/√F, seeds' χ² from the
per-seed values. Firewalls as `eq_analyze.py`: fw + fw_settled, ln τ_fw = ln(E / that). CPU rows are per thread per
chunk; a seed is the sum of its chunks. Tube lines: `wrap_haz_lead.py --tube`, refitted on the data as they stood
when the lines were quoted (the card's nine faces then on file; every other source unchanged since 953c28f). The
refit reproduces 0.20437 ± 0.00016, 0.20602 ± 0.00033, 0.20717 ± 0.00011 and the frozen 19.7791 ± 0.0055 exactly.

## 1. Every face whose rows changed since 0345df0

| torus (H, K), (0, D) | cells | seeds | face deaths | ln τ_face | seeds' χ² | firewalls (fw + on-firewall settled) | settled lives | at 0345df0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| (1, 17), (0, 32) | 96 | 8 | 56,775 | 19.7446 ± 0.0042 | 10.0 on 7 | 0 | 0 | 19.7405 ± 0.0059 (4) |
| (1, 16), (0, 36) | 108 | 8 | 13,641 | 22.1599 ± 0.0086 | 6.8 on 7 | 0 | 0 | 22.1557 ± 0.0121 (4) |
| (4, 0), (0, 8) | 96 | 4 | 24,796 | 19.9366 ± 0.0064 | 2.2 on 3 | 238,631 + 99; ln τ_fw 16.979 ± 0.002 | 99, all on a firewall | new |
| (1, 8), (0, 32) | 96 | 4 | 25,054 | 19.9284 ± 0.0063 | 5.0 on 3 | 239,318 + 84; ln τ_fw 16.978 ± 0.002 | 84, all on a firewall | new |
| (1, 3), (0, 32) | 96 | 4 | 25,797 | 19.8109 ± 0.0062 | 2.8 on 3 | 0 | 0 | new |
| (6, 0), (0, 6) | 108 | 10 | 18,394 | 22.5405 ± 0.0074 | 6.0 on 9 | 298 + 0; ln τ_fw 25.970 ± 0.058 | 0 | 22.5600 ± 0.0222 (4) |

All values, deaths, seed counts, χ², firewall counts and ln τ_fw equal the card's README and `chain3_summary.txt`. No
kind-5 life anywhere. The card's firewall column is fw alone; its ln τ_fw includes the on-firewall settled lives
(both as `eq_analyze.py` does). The four new seeds agree with the four old: +0.0083 (1.0 combined errors) at 96
cells, +0.0085 (0.5) at 108.

The 120-cell tube (1, 18), (0, 40) has **no rows** on file; only `checks/check_1_18_40.txt`, committed four minutes
after the check started, holding the lattice part (passed) and none of the GPU-against-engine comparison lines the
other faces' checks have. No value can be given, partial or otherwise.

## 2. The long tubes of loop² 12

| cells | ln τ_face | the frozen tube line (54–84) | measured − line | POW | measured − POW |
|---:|---:|---:|---:|---:|---:|
| 84 | 17.3175 ± 0.0031 | | | | |
| 96 | 19.7446 ± 0.0042 | 19.7791 ± 0.0055 | −0.0345 (5.0; 4.6 inflated for seed scatter) | 19.7618 ± 0.0075 | −0.0172 (2.0) |
| 108 | 22.1599 ± 0.0086 | 22.2316 ± 0.0074 | −0.0717 (6.3; χ² below its dof, no inflation) | 22.1969 ± 0.0115 | −0.0370 (2.6) |

Chords 0.20227 ± 0.00043 (84 → 96) and 0.20127 ± 0.00079 (96 → 108); second difference −0.0119 ± 0.0124; weighted line
through the three 0.20198 ± 0.00031 per cell (χ² 0.9 on 1). Against 0.20437 ± 0.00016: −0.00239 ± 0.00035, 6.8 combined
errors. With the 84-cell value pooled over both codes (17.3191 ± 0.0027) the chord 84 → 96 is 0.20213 ± 0.00042 and the
second difference −0.0103 ± 0.0123.

**The bend of WL7 is still there and sharper:** 5.0 and 6.3 combined errors below the tube line at 96 and 108 cells
(it was 4.8 and 5.4), still below POW (2.0, 2.6). The long tubes are straight among themselves within one error; a bend
that goes on and a second straight line are still not told apart. **The seed scatter has gone:** χ² 16.8 on 14 for the
two faces together (was 11.8 on 6).

## 3. Loops² 16 and 13 at 96 cells against their tube lines

| loop² | line on file (faces, cells) | line at 96 cells | measured at 96 | measured − line | slope past the line's end minus the line's slope |
|---:|---|---:|---:|---:|---:|
| 12 | 0.20437 (8, 54–84) | 19.7791 ± 0.0055 | 19.7446 ± 0.0042 | −0.0345 (5.0) | −0.00239 ± 0.00035 (84–108 line) |
| 13 | 0.20602 (7, 57–75) | 19.8628 ± 0.0113 | 19.8109 ± 0.0062 | −0.0519 (4.0) | −0.00193 ± 0.00046 (75 → 96 chord, 4.2) |
| 16 | 0.20717 (7, 60–108) | 19.9446 ± 0.0034 | (4,0),(0,8) 19.9366 ± 0.0064 | −0.0080 (1.1) | |
| 16 | | | (1,8),(0,32) 19.9284 ± 0.0063 | −0.0162 (2.3) | |
| 16 | | | pooled 19.9325 ± 0.0045 | −0.0121 (2.2) | −0.00151 ± 0.00055 (84 → 96 chord, 2.7) |

Forecast errors include the covariance of each line's intercept and slope. **Tubes of loop² 13 bend: the 96-cell face
is 4.0 combined errors below the 57–75 line. Tubes of loop² 16 lean the same way at about 2σ; not established.** The
fall of the slope past each line's end is ordered 12 > 13 > 16 (0.0024, 0.0019, 0.0015 per cell), but no two of
them are resolved apart. For loop² 16, 96 cells lies inside the line's own range (60–108; the 96- and 108-cell faces
on it are from `research/constant/out/points.txt`, ± 0.018 and ± 0.042), so the line there is held mostly by the
faces of 60 to 84 cells.

Discounts against 13.1623 + 0.20861 (A − 63) recompute as the card's table: loop² 12 0.2256, 0.3018, 0.3898 (84, 96,
108); loop² 13 0.1406, 0.2356 (75, 96); loop² 16 0.0786, 0.1140 (84, 96 pooled); loop² 19 0.0214 (75). The twist does
not matter for a loop of 16: the two lattices differ by +0.0082 ± 0.0090.

## 4. The CPU second code (`research/gpu-local/cpu/`, fr.c + fr.py)

| face | layers | CPU (seeds, deaths) | GPU | CPU − GPU |
|---|---:|---:|---:|---:|
| (1, 17), (0, 32), 96 cells | 8 | 19.7231 ± 0.0160 (8, 3,899; χ² 4.8 on 7) | 19.7446 ± 0.0042 | −0.0215 (1.3) |
| (1, 4), (0, 21), 63 cells | 8 | 13.1607 ± 0.0017 (8, 361,543; χ² 10.6 on 7) | 13.1622 ± 0.0007 | −0.0016 (0.9) |
| (1, 4), (0, 21), 63 cells | 16 | 13.1619 ± 0.0025 (4, 156,800; χ² 4.1 on 3) | 13.1589 ± 0.0013 | +0.0030 (1.1) |
| (1, 4), (0, 28), 84 cells | 8 | 17.6002 ± 0.0436 (4, 527; χ² 0.3 on 3) | 17.5387 ± 0.0031 | +0.0615 (1.4) |
| (4, 0), (0, 4), 48 cells | 8 | 9.9252 ± 0.0006 (3, 3,009,239; χ² 1.5 on 2) | 9.9251 ± 0.0004 | +0.0002 (0.3) |

All five agree within 1.4 combined errors. The 96-cell row is partial (chunks to 11:20Z on the 17th; the run was
to continue).

- **WL7 rests on two codes at 96 cells**, weakly: the CPU value alone is 3.3 combined errors below the frozen tube
  line (−0.0560 ± 0.0169) and 2.2 below POW. At 108 cells it is one code.
- **WL8 does not:** the CPU's 527 deaths at (1, 4), (0, 28) (± 0.044) cannot speak to a 0.013 question.
- **CN4 rests on two codes for the 63-cell value at 16 layers only.** The CPU's own thickness difference at 63 cells
  is +0.0013 ± 0.0030 where the GPU's is −0.0033 ± 0.0015 (1.4σ apart): the CPU neither repeats nor excludes
  "thicker slabs live about 0.003 shorter". The 84-cell 16-layer value, and so the 16-layer price 0.20863, is one code.
- **What the codes share:** the vessel (`research/shape/tslab.py`: cells, neighbour graph, `periods` for the firewall
  rings, `reduce_ij` in the engine comparison), the definitions of face death, firewall and settling, soup density 0.4,
  the estimator, the engine `gump` they are each validated against, the machine, and the session that wrote both
  (the CPU code by a subagent of the card's session; not yet reviewed by the lead). They share no stepper, kernel,
  driver, random-number stream or event bookkeeping. An error in tslab's lattice would be common to both, but each
  face's check shows the lattice periodic and neighbour-consistent and the engine state lattice-periodic.

## 5. What in the card's write-up does not follow from its rows

1. **The loop-13 bend's error is understated.** "0.040 ± 0.007 below its short-tube line (my 75-cell value plus 21 ×
   0.20602)": the ± 0.007 omits the slope's error (21 × 0.00033 = 0.0069); with it ± 0.0097. Against the lead's line
   itself (not re-anchored on the card's 75-cell value, which is 0.011 below it) the shortfall is 0.052 ± 0.013.
2. **"The loop of 13 bends as much as the loop of 12" compares unlike things.** 0.040 at 96 cells is 21 cells past the
   13-line's end; 0.039 (now 0.0345) is 12 cells past the 12-line's. In slope the 13-tube falls by 0.0019 ± 0.0005 and
   the 12-tube by 0.0024 ± 0.0004: not resolved apart, but not "as much" either.
3. **The loop-16 comparison leaves out the face already on file.** The lead's 16-line (60–108) gives 19.9446 ± 0.0034
   at 96 cells and already contains a 96-cell face of the same lattice class as (4, 0), (0, 8) (19.943 ± 0.018, points
   file); (4, 0), (0, 8) repeats it (−0.006 ± 0.020). The card's anchors "19.946 to 19.951" and "0.014 to 0.019 below"
   carry no error; 19.9505 is the 4 × 7 value plus 12 × 0.20717, and 19.946 is not reproduced from anything on file.
   Against the line with errors the pooled shortfall is 0.012 ± 0.006 (2.2σ): "every short loop bends" is
   established for 12 and 13, not for 16.
4. **Not-checked list.** The README's earlier "no second code ... on (1, 4), (0, 28)" is no longer true in the strict
   sense: CPU rows exist there (527 deaths), too few to matter. Block 7 lists loops² of (4, 0), (0, 8) as "16, 48, 64";
   the table and `loops_hnf` give 16, 48, 64, 64.

Everything else in the chain-3 section and blocks 7 and 8 recomputes: values, chords, second difference, the slope
0.2020 ± 0.0003, the discount table, slopes 0.2041 ± 0.0003 and 0.2057 ± 0.0005, the twist difference, the CPU values
and the scoring of block 8.

## Not checked

- Nothing was re-run; the runs and the GPU-against-engine checks are taken from the card's files.
- Hazard by age (`hist_*.json`) on the chain-3 faces, and the card's note that firewall-prone lattices sample the
  face hazard on young lives only.
- The CPU code itself (fr.c, its validation logs, which are not kept), and whether its partial 96-cell row is the
  final one.
- The fit-time reconstruction of the tube lines assumes `points.txt`, `shape3/data/runs.csv` and `wrap/data/runs.csv`
  are as they were at 953c28f (their git logs end at or before it); it reproduces the three quoted slopes and the frozen
  forecast exactly.
- The wide-face line 13.1623 + 0.20861 (A − 63) was used as the card gives it, not refitted.
