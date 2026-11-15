# For the lead: replacements in files the consistency pass may not edit

## For the lead, 2026-11-15 04:08 UTC (draft pass after the audit of the C rows)

Found while bringing the draft in line with `research/CLAIMS.md` after 13f8732. Nothing here has been applied
outside `docs/paper/`.

1. **P4's snapshot density.** The ledger's reproduce cell says the snapshots are "12 at N = 64, soup 0.4", but the
   audit's command and `research/phase/README.md` (line 10) make them with `--soup 0.3`. One of the two is wrong;
   the draft states no density.
2. **Notebook and ledger disagree on which rows keep a C part.** The notebook entry "the audit of the rows nobody had
   re-run" lists Z8 and Z9 among the rows with a C part; their level cells are "A … + B" and "B … + A", with no C.
   The same list names only "TH5's segment n = 7", while TH5's cell keeps the 22%, 11% and 5.6% at C as well (the
   draft keeps those three marked preliminary).
3. **P4's restated ξ is the lead's own fit.** The draft now gives ξ = 0.65 ± 0.03 as grade B, as the ledger does;
   the fit window (k ≤ 2.5 per cube) and the value come from `research/audit/p4_lead_check.py`, which no third
   agent has re-run. If the lead does not count as the second party for its own fit, the value belongs under C.
4. **Snapshot commits of this pass's files.** c96f57a and c3049c0 ("snapshot: in-flight files", not made by this
   pass) committed `docs/paper/draft.md` half-edited, with a model name in their attribution line; this pass's
   own commits complete the edit.

## Consistency pass, 2026-11-14

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
>   A ≥ 72 have no test (55–475 of 512 runs censored at the cap). Over all 14 batches of `research/peeling/slab_area.csv` with A ≥ 36 and a test,
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

## For the lead, 2026-11-15

From the update of the draft to draft 2 (`docs/paper/FACTCHECK.md`, "Update of 2026-11-15"). Each item is a place
where the ledger, the notebook and the files they cite do not say the same thing; the draft follows the version
named. Nothing outside `docs/paper/` was edited.

1. **CN1, the octahedral local slope 84 → 108.** `research/CLAIMS.md` CN1 and the notebook entry "is there one
   asymptotic cost per cell?" (its "Measured, model-free" bullet) print 0.2182 ± 0.0013; the same entry's own
   check line and draft Table 2 give 0.2181, and (23.3761 − 18.1407)/24 = 0.21814 (error
   √(0.031² + 0.005²)/24 = 0.0013). The draft uses 0.2181. Proposed replacement in CN1:
   > hull local slopes at A = 63–108 (0.2146, 0.2181 ± 0.0013)

   and in the notebook, as a dated correction note (append-only): "2026-11-14, 'is there one asymptotic cost per
   cell?': the hull local slope 84 → 108 is 0.2181 ± 0.0013, not 0.2182 (arithmetic on 18.1407 and 23.3761)."
2. **ZL2, "others ≤ 2 × 10⁻³".** CLAIMS ZL2 and the notebook entry "lives that settle and are not recognised" say
   the remaining bounded GPU runs are ≤ 2 × 10⁻³; `research/gpu/README.md` ("Zombie lives") gives symv R38 at
   ≤ 2.1 × 10⁻³ (all ages). Proposed replacement in ZL2 and in a notebook correction note:
   > others ≤ 2.1 × 10⁻³ (symv R38; the rest ≤ 2 × 10⁻³)
3. **ZL2 omits fwslab 4×7×8** (A = 84, Table 6's s = 4 row). It is neither in the bounded list nor in the
   "no bound" list of ZL2, the notebook or the GPU README; `python3 research/gpu/zombies.py` prints "no age bins in
   this file" for `fwslab4x7x8_s602_A10G.json`. The draft marks it † (no bound). Proposed addition to ZL2's
   unbounded list:
   > …, five wider slabs, and fwslab 4×7×8 (A = 84; its log has no age bins)
4. **GP10's grade for the 4 × 5 point.** CLAIMS GP10 grades "4×5 and beyond" B with "GPU only"; by the legend at
   the top of `research/CLAIMS.md` a value recomputed only from one GPU implementation's committed output is B−.
   Proposed: "B− (4×5 and beyond: GPU only; the CPU's 4×5 is 1.9–2.6σ lower, unresolved)". The draft says
   "B and GPU-only", which the brief's convention (B− counts as B, said to be GPU-only) covers either way.
5. **CN1 does not carry its addendum.** The notebook's addendum (36 of 84 pairings pass at p ≥ 0.01 with
   c = 0.2072 to 0.2190; readings with c ≤ 0.214 need a two-term hull correction, those with c ≥ 0.2155 a 1/s
   approach on periodic faces) is not in the row. Not a disagreement; the draft cites those numbers to the
   notebook entry. Proposed addition to CN1's claim: "Over 84 pairings 36 pass at p ≥ 0.01 (c = 0.2072–0.2190);
   c ≤ 0.214 needs a two-term hull correction, c ≥ 0.2155 a 1/s approach of periodic faces (addendum)".
6. **Table 5 and the forecast files.** The draft now lists SH9 (`research/shape3/PREDICTIONS.md`, its five
   candidates only) and the lead's patch forecast (GP10). Still not searched for the table:
   `research/constant/PREDICTIONS.md` (part A, for the patches, scored in the notebook as low by 1.3, 2.6, 4.1 in
   −ln P; part B not refuted; part C not run) and `research/theory/thin/PREDICTIONS.md` (14 forecasts, whose tally
   the review calls generous). Whether either should get ledger rows, and so table rows, is yours to decide.

**Applied (2026-11-15, by the lead; draft followed in the same day's follow-up):**
1. Applied: CN1 reads 0.2181 ± 0.0013; the draft already used it.
2. Applied: ZL2 reads "others ≤ 2.1 × 10⁻³ (symmetric R38; the rest ≤ 2 × 10⁻³)"; the draft quotes no "others" figure.
3. Applied: fwslab 4×7×8 is in ZL2's unbounded list; Table 6 and §12 now cite ZL2 for it.
4. Applied: GP10's GPU-only part is B−; §7.5 and Table 5 row 16 say B−.
5. Applied: CN1 carries the addendum (36 of 84 pairings, c = 0.2072–0.2190).
6. Applied: TH7 and CN2 are new rows; Table 5 has them as rows 17 and 18 (CN2 flagged as grade C).

## For the lead, 2026-11-15 (second update: the symmetric collapse and the new clocks)

From bringing the draft up to date with the notebook entries "the symmetric collapse" and "what the unrecognised
settled states are" (CLAIMS S2, S3, S5–S9, Z12, Z13). Nothing outside `docs/paper/` and `docs/overview/` was edited.

1. **S7, "2.6σ apart".** CLAIMS S7's level column reads "one slab pair rerun by the reviewer: +0.926 ± 0.014 against
   +0.872 ± 0.013, 2.6σ apart". In `research/audit/REVIEW-symmetric.md` (section 1a) the 2.6σ is a different
   comparison: the mirror case alone, 10.846 ± 0.010 against the line's 10.807 ± 0.011 (+0.039 ± 0.015). The two
   differences quoted are 0.054 apart, √(0.014² + 0.013²) = 0.019, about 2.8σ. The notebook gives the two values
   and no σ. The draft quotes the two values and "the sign stands", no σ. Proposed replacement in S7:
   > +0.926 ± 0.014 against +0.872 ± 0.013 (the mirror case alone 2.6σ from the line's)
2. **S2's 2026-11-15 note is stronger than the notebook.** S2 says "the term is mainly a rim cost, not a
   mirror-line cost: S6–S8". The notebook (and S7, in the review's wording) say that in a fully symmetric face
   rim and mirror cannot be separated, and that a diagonal-mirror share of up to about a third of the −0.196 is
   not excluded; the "mainly" is said of the cost of symmetry as a whole (edge-sharing faces dying together), not
   of the √A term. The draft follows the notebook. Proposed replacement in S2's note:
   > the term is not shown to be a mirror-line cost; in fully symmetric faces rim and mirror cannot be separated
   > and a mirror share of up to about a third is not excluded (S6–S8)
3. **Not a disagreement, for information.** S6's inversion "−0.056 ± 0.023" is in the ledger only; the notebook
   gives the two values (13.578 ± 0.014, 13.634 ± 0.018), from which it follows. The draft cites S6 for it.
4. **`research/STATUS.md` (state block under "Next", the first report of 02:50 UTC)** still says "38 forecasts
   scored, 23 held" and "rim cost 0.4–0.55 per period" where the notebook says 40 statements, 25 held, 1 on its
   limit, 14 failed, and 0.45–0.55. It is marked as the line's first report, so this may be intended; the draft
   and the overview follow the notebook.

## For the lead, 2026-11-15 (fourth update: how a face dies, the 4 × 5 patch rerun, the second card)

From bringing the draft in line with CLAIMS DY1–DY7, GP10, GL1, GL2 and the SH3/SH4 notes (`docs/paper/FACTCHECK.md`,
"Update of 2026-11-15 (fourth)"). Nothing outside `docs/paper/` and `research/dying/README.md` was edited.

1. **SH4 and GL1, the census gap "0.0138".** The ledger's SH4 note, the notebook entry "a second card" and
   `research/audit/REVIEW-gpu-local-pr23.md` (section 2, "CLAIMS SH4") all give 0.0138. That is 9.9384 − 9.9246, the
   reviewer's own stepper value. Against the best value the same entry and GL1 give, 9.9249 ± 0.0003, the gap is
   9.93842 − 9.9249 = 0.0135 ± 0.0020 (`research/shape2/data/A48.csv`, class 1 6 16: ln(2·2.55834e9/247051) =
   9.93842). Either way the tension with the shape2 review's 0.0135 ± 0.0021 is gone. The draft gives "0.0135–0.0138"
   and names both subtrahends. Proposed replacement in SH4's note:
   > with 9.9249 the census gap is 0.0135 ± 0.0020 (0.0138 against the reviewer's own 9.9246)
2. **DY5, "over the last 3–12 cells … nearly constant (local slope 0.51 → 0.34 per cell in c1)".** In the review's
   table (`research/audit/dying/ana2_out.txt`, "tail shape", c1) the local slope is 0.51, 0.51, 0.49, 0.48 over
   windows from 3–6 to 9–12 cells, and 0.34 only at 17–20 cells. The row puts the drift to 0.34 inside "the last
   3–12 cells". The draft says "drifts from 0.51 to 0.34" without the 3–12 qualifier; the README gives the table.
   Proposed:
   > over the last 3–12 cells the price per further cell lost is nearly constant (0.51–0.48 per cell in c1),
   > drifting to 0.34 at 17–20 cells
3. **GP10, "at equal exposure".** The row says the CPU's 4 × 5 was "at equal exposure"; its own level cell, the
   notebook entry "the 4 × 5 empty patch, rerun" and `followup.py` (2.76 × 10¹⁰ against the GPU's 3.04 × 10¹⁰) say
   0.9 of the GPU's exposure. The draft says 0.9. Proposed: "4×5 on the CPU at 0.9 of the GPU's exposure".
4. **Notebook entry "the 4 × 5 empty patch, rerun": "1.13–1.28 hits per event".** `followup.py` prints 1.19–1.40
   hits per event (all groups, 4×5 to 3×4) and √(Σs²/Σs) = 1.13–1.28 for the pull request's groups; the 1.13–1.28
   is the factor on the Poisson error, as the same sentence goes on to use it. The draft says "the true error is
   1.13–1.28 times the Poisson one" and no hits-per-event figure. A dated correction note in the notebook would fix it.
5. **`research/constant/PREDICTIONS.md` has no dated note on part C yet.** The notebook entry "a second card" says
   the part C forecasts "keep their committed text, with a dated note giving what they become with the anchor
   replaced"; no such note is in the file (no "9.9249", "anchor … high draw" in it). The draft cites the review's
   section 2 for the shifts (−0.005 to +0.010 in ln τ, +0.0003 to +0.0004 on the slope 48 → 57).
6. **CN1 includes the high draw.** `research/constant`'s pooled periodic table (`load.periodic`) uses the census's
   4 × 4 row (review section 2, last bullet); CN1's range 0.207–0.219 was not refitted. The draft says so in §7.5 and
   in gap 42. Whether to refit is yours.
7. **SW2's "deterministic 9.936" at A = 48** (§6 of the draft) is a 4 × 4 slab value from the exponent study's
   protocol (soup 0.35, T₀ = 300; `research/theory/swarm/exam/OUTCOMES.md`, S-E2), not the census anchor. It is
   0.011 above GL1's 9.9249 (soup 0.4). Left unchanged; whether the difference is the protocol or another draw was
   not checked.
8. **No ledger rows for the dying-face forecast tallies.** Table 5 rows 20 and 21 (round 1: L2–L7 failed, L4
   undecided with the other band; round 2: one of seven held) cite the notebook entries, as row 19 does. A row
   would let the table cite the ledger.
9. **The dying README: two readings that were never in it.** The review asks the README to drop "twice the 0.436"
   and "5.5 + 3.4 per free edge"; neither was in `research/dying/README.md` (both are the lead's, in the notebook).
   The corrected README now states them as the lead's readings, withdrawn, so that a reader of the README alone is
   not misled by the notebook. If the lead prefers the README not to mention them, delete those two sentences
   (round-1 "Reviewed" item 4; round-2 tail paragraph under "Numbers").
