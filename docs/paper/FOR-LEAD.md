# For the lead: replacements in files the consistency pass may not edit

2026-11-14, consistency pass over `docs/paper/INCONSISTENCIES.md`. Line numbers are those of the working tree at
commit 7e3e931 (`research/STATUS.md` at 6d4cd33, `research/NOTEBOOK.md` unchanged since c61c101). Each entry says
which item it settles and how the number was traced. Nothing here has been applied.

## 1. `research/NOTEBOOK.md` (append-only): one dated correction note

Suggested text, appended as its own entry (or as a bracketed note under each line named):

> ## 2026-11-14 — consistency corrections (consistency pass; numbers traced to data or scripts)
>
> - **Local slopes of octahedral faces** (entry "GPU ensembles", lines 905–906): "0.201, 0.212, 0.212, 0.218, 0.221"
>   mixes two values of ln τ_face at A = 84: 18.077 (CPU, 342 deaths) for 63 → 84 and 18.141 ± 0.005 (GPU, 34,026
>   deaths) for 84 → 108. With 18.141 throughout: **0.201, 0.212, 0.215, 0.218, 0.221**, the GPU README's table
>   column; with 18.077 throughout, 0.201, 0.212, 0.212, 0.221, 0.221. (Arithmetic on the lifetimes 6.804, 9.819,
>   13.633, ·, 23.376, 29.34 at A = 30, 45, 63, 84, 108, 135.) [INCONSISTENCIES A2]
> - **Vertex/cube factors** (entry "side-16 cube ends", line 710): the six factors "1.51, 1.52, 1.53, 1.60, 1.49,
>   1.31 at A = 360 … 630" have five sources: `sym_residence.csv` has no cube-centred row at A = 360, and no version
>   of the csv ever had one (checked back to d09388a, where the row set was added); `python3 research/fluct/sym_fit.py`
>   prints the five at A = 408 … 630. Where 1.51 came from was not found. The flat ≈1.5 holds over **A = 408–630**;
>   line 739's "A = 360–630" likewise. The 3.1 (ln 1.12 ± 0.29) at A = 693 is right: pooled vertex value (24 copies +
>   5 soups) against the csv's 19.705 for `sym41c`; the fluctuation README's 3.3 used 19.64, a value the csv does not
>   give (now corrected there). [B2, B3]
> - **Density at R = 11** (entry "how chaos dies", line 307): from the regenerated `research/peeling/octa_first.csv`
>   the first-peel means for p = 0.3, 0.4, 0.5, 0.6 are **1.00, 1.08, 1.00, 1.05 × 10⁵** (99,545; 108,090; 100,483;
>   105,280), not 0.91, 1.08, 1.00, 1.04. The conclusion (density does not matter once the hull is filled) stands. [B12]
> - **Thickness at A = 48** (same entry, line 298): `peeling/slab_area.csv` gives 9,878.7, 10,354.1, 10,323.0,
>   10,345.8, 10,346.9, i.e. **9.9, 10.4, 10.3, 10.3, 10.3 × 10³** for m = 7, 8, 9, 10, 12 (the last two were
>   written 10.4). [B13]
> - **Side-16 first-peel forecast** (entry "side 16 loses its first face", line 629): with the committed forecast's
>   inputs (8 deaths in 8.3×10⁹ replica-generations, alive at 1.45×10⁹; `predict.py`'s Lomax law) the outcome
>   2,362,434,048 sits at quantile **0.566, the 57th percentile**, not the 58th. (`fluct/PREDICTIONS.md`'s "≈ 0.55" is
>   the same quantity, rounded down.) [B14]
> - **4 × 6 × 8 slab face** (entry "equal areas, different lifetimes", line 1353): the run's own value is
>   **14.970 ± 0.002** (`python3 research/audit/gpu_pr16/recompute.py research/data/gpu_facelaw`); 14.971 is what one
>   gets by pooling it with the same slab in the other orientation, 6 × 4 × 8 (14.972). The table's row is the width-4
>   family, so 14.970 is the entry. [B6]
> - **Count of claims** (entry "audit corrections", line 802): the ledger had 71 rows on 2026-11-13; it has 108 now.
>   [C2; the same sentence is at `research/AUDIT-2026-11-13.md:4`, which is right for its date]
> - **Index of sources** (entry "supertransients", line 889): `research/theory/swarm/library/shelf.md` now has 73 rows,
>   not 59. [C4]
> - **Exam score** (heading at line 1112 against line 1325): the heading counts the examiner's eight sampled entries
>   (four hold, two fail, two undecided); line 1325 counts every entry of the board's closing table (five hold, four
>   fail or missed, two undecided, three not run). Both are right for their sets. [C5]
> - **Gump's slab slope in comparisons with other rules** (entry "the class theory attacked", line 1034, "gump's 0.212
>   per face cell"): that is the area-only slope of slab faces of mixed widths over A = 27–75 (`theory/class.md`:488–489;
>   0.2121 ± 0.0004 in `audit/REVIEW-class.md`:399). CLAIMS F4 (0.2088, A = 27–90) and GP9 (0.2072 within a width
>   family; 0.2085 area-only over s ≥ 4) are the same kind of slope over other sets of faces. [B11]
> - **Shortest-loop step 12 → 16 at A = 60** (line 1435: 0.051 ± 0.005): `shape/README.md` gives 0.052 ± 0.005 from
>   the same classes (12.481 − 12.429); the census (line 1508, CLAIMS SH4) gives +0.056 to +0.063 with every class.
>   The 0.051/0.052 difference was not traced (rounding of unrounded group means is likely, not checked). [B8]

## 2. `research/STATUS.md`: exact replacements

- **Line 13** [C6]: `- \`web/\` v1 — WebGL2 bit-packed stepper + three.js views; 49/49 tests.` →
  `- \`web/\` v1 — WebGL2 bit-packed stepper + three.js views; web suite 79/79 (\`cd web && node test/run.mjs\`, re-run 2026-11-14).`
- **Line 19** [C7]: `## In flight (2026-11-13, late)` → `## In flight on 2026-11-13, late (historical; finished work is recorded below)`.
  (Or move the section under "Most recent"; the pass did not judge which parts are still live.)
- **Line 68** [B9]: `(two tori with the same shortest loop differ by 0.018 ± 0.004)` →
  `(two tori with the same shortest loop differ by 0.0142 ± 0.0019 over four runs, CLAIMS SH2; first published as 0.019 ± 0.004)`.
- **Line 71** [B9]: `(0.014 ± 0.003 at both\n  areas)` → `(0.0142 ± 0.0019 at A = 60, 0.0151 ± 0.0017 at A = 48; CLAIMS SH2)`.
- **Lines 183–185** [A1, A5]: replace
  `mean wait τ_face ≈ exp(−0.09 + 0.209·A)\n     generations, A = sites in the outer layer; one line over six decades for flat slab\n     faces, octahedral faces (≈1.7–1.9× tougher), symmetric soups and the closed cubes`
  by
  `mean wait τ_face ≈ exp(≈0.21·A)\n     generations, A = sites in the outer layer, over six decades; not one line: the first fit\n     −0.09 + 0.209·A mixes slab widths (within a width family 0.2072, and a narrower face dies sooner; CLAIMS F4, GP9),\n     octahedral faces are 1.7–1.9× tougher at A = 45–84 and 0.84–0.91 nats at A = 108, with local slopes rising to\n     0.221 (GP1, GP7), and symmetric faces follow their own law (S2)`.
- **Line 193** [A1]: `effective face area A/7.7.` → `effective face area roughly A/6 to A/8 (the early fit A/7.7, CLAIMS S1, is superseded beyond A ≈ 460; see S2 below).`
- **Line 200** [B4]: `ln τ ≈ 0.69 + (0.209/6)·A − 0.195·√A` → `ln τ ≈ 0.698 + (0.209/6)·A − 0.196·√A` (what `sym_fit.py` prints; CLAIMS S2).
- **Line 201** [B3]: `(A = 360–630;` → `(A = 408–630;`.
- **Lines 241–242** [A6]: `whether 0.208 per site\n  holds for asymmetric faces beyond A = 84.` →
  `whether the cost per site of asymmetric faces levels off (it rises past A = 84 on octahedral faces, to 0.221 at A = 135, CLAIMS GP1; on slabs width matters, GP9).`
- **C5** (line 103 against lines 155–158): line 103's "five hold" is the board's closing table; lines 155–158 list
  the four of the examiner's eight sampled entries that hold. Suggest adding "(of the eight sampled entries)" after
  "Hold:" at line 155.
- **B7** (line 135, "0.84 ± 0.04 nats at A = 108 with the pooled slab value"): correct as worded; CLAIMS GP7 now gives both 0.91 ± 0.06
  (against 22.470) and 0.84 ± 0.04 (against GP8's pooled 22.537). `theory/class.md`:78's "0.88 after the firewall
  correction" was not traced.
- **C9** (lines 205–206): already annotated in place; nothing to do.

## 3. Other files outside this pass's list

- `docs/paper/draft.md:182` and `:784` say "ledger K1 of the class study": that row is now **K9** (the class rows K1–K3
  were renamed K9–K11 because the ids were used twice; `draft.md:246` "K1 of the thickness" is unchanged).
- `docs/overview/data/sources/update-2026-11-14.json:20` ("CLAIMS K3") and `:96` ("CLAIMS K2") cite the class rows:
  now **K11** and **K10**. Its `structure.json` cites the thickness K1, K3 and is unchanged. (Not edited: data files.)
- `research/fluct/PREDICTIONS.md:14` "predictive quantile ≈ 0.55": 0.566 by the file's own method (see §1); an
  append-only file, so a dated note if anything.
- `research/theory/class.md:128`, `:488–489` (B11), `:78` (B7): see §1 and §2.
- Grades not changed but worth a look: GP1, GP2, GP5, GP6 are "B−" (now defined in the ledger's legend) while GP7 and
  GP8, also GPU runs with no second implementation at the claimed sizes, are "B". The pass defined B− from the rows'
  own wording and did not regrade.

## After the fact-check

Written by the subagent that carried out the lead's decisions on `docs/paper/FACTCHECK.md` items 15–30. Nothing
below has been applied to the files it names.

### `research/NOTEBOOK.md` (append-only): one dated entry, text to append

> ## 2026-11-14 — corrections from the paper's fact-check (subagent; for the lead to check)
>
> - **Memoryless slab faces (entry of 2026-11-12, "how chaos dies"; ledger F5).** "CV 0.96–1.05, KS p 0.5–0.96 for
>   A ≥ 36" is what the four m = 8 batches of the face-law fit (`research/peeling/face_law_fit.py`'s selection) with
>   A ≥ 36 and a test give: 3×4, 3×5, 4×4, 4×5 (A = 36–60), CV 0.964–1.045, KS p 0.519–0.96; the fit's batches at
>   A ≥ 72 have no test (censored). Over all 14 batches of `research/peeling/slab_area.csv` with A ≥ 36 and a test,
>   p runs 0.042–0.974 (one below 0.05, 4×5×10) and CV 0.962–1.06. `python3 -c "import csv; [print(r['N1'],r['N2'],r['m'],r['cv'],r['ks_p']) for r in csv.DictReader(open('research/peeling/slab_area.csv')) if r['ks_p']!='nan' and int(r['A'])>=36]"`.
> - **SH4 (entry "every torus of a given area").** The 0.0135 ± 0.0021 by which 4×4 lies below the (12; 19) class at
>   A = 48 is the review's value; the census (`research/shape2/data/A48.csv`, 9.93842 − 9.93237, each ± 1/√F) gives
>   0.0061 ± 0.0028. Pooled by inverse variance: 0.0108 ± 0.0017 (6.4 SE); agreement χ² = 4.4 on 1 (p = 0.036); with
>   the error scaled by √χ², 3.0 SE. "Not ordered by shortest loop" stands.
> - **Table 8 of the shape2 study, loop² 4, 60 → 72:** `research/shape2/data/explore_report.txt` and
>   `python3 research/audit/shape2_lead_check.py` give 0.1353 (± 0.0008); `research/shape2/README.md`:189 prints
>   0.1346 ± 0.0010.
> - **Engine-only R = 9 (entry "a face dies off the end of a straight line").** Re-running
>   `python3 research/experiments/face_endgame_check.py 9 16000` reproduces 13,765 peels, exposure 31,826,744,
>   mean 2312.1 ± 19.7, −ln h/A = 0.2183, so ln τ_face = ln(8 × 2312.1) = 9.825 ± 0.009.
> - **Twist lemma (entry of 2026-11-13).** The step giving m ∈ {1, 2, 3, 4, 6} is now written out in
>   `research/clockwork/README.md`: G (the box's lattice symmetries p ↦ Rp + t, R ∈ O_h) embeds in O_h by linear
>   part (a translation fixing a finite set is trivial), elements of O_h have orders 1, 2, 3, 4, 6 (R^c diagonal for
>   c the order of R's permutation), and m divides the order of any g with k(g) = P/m. The hypothesis that G
>   consists of lattice symmetries was implicit before.
> - **Side-16 face deaths** 2,362,434,048 and 2,886,100,480 are last-alive generations (checks every 64); by the
>   first-empty definition they lie in 2,362,434,049–112 and 2,886,100,481–544 (`research/data/cube16_events.jsonl`).

### `research/STATUS.md`

No change found to be needed: none of the corrected wordings (F5's range, SH4's 0.0135, Table 8's 0.1346, the
2 × 0.208 remark, "lucky at the 1% level") occurs in it (`grep`).

### Other files outside this pass's list

- `research/shape2/README.md`:189: b(60→72) for loop² 4 should read 0.1353 ± 0.0008 (its own `data/explore_report.txt`).
- `research/fluct/README.md`:47 prints 6.804, 9.819, 13.633; `research/fluct/data/qsd_summary.json` gives 6.8054,
  9.8202, 13.6317 (ln(8 × first_peel_mean)).
- `research/theory/swarm/exam/OUTCOMES.md` path E3 (failed, gump) has no ledger row; the paper now lists it in
  Table 5 as ungraded. A ledger row (grade C) would make the table and the ledger agree.
- Tracked forecast files not searched for the paper's Table 5 (named in its caption): `research/shape3/PREDICTIONS.md`,
  `research/theory/thin/PREDICTIONS.md`, `research/theory/exponent/PREDICTIONS.md` (entry by entry),
  `research/theory/class/PREDICTIONS.md`, `research/theory/class/followup/PREDICTIONS.md`, `research/toy2d/PREDICTIONS.md`,
  `research/audit/class/PREDICTION-*.md`.
