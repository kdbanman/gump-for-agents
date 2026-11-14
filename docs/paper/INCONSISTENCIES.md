# Inconsistencies met while writing `draft.md`

2026-11-14. Places where two files of the repository disagree, or where a number in a write-up does not match the
ledger (`research/CLAIMS.md`), the notebook or the data. Listed, not fixed: other agents own those files. Line
numbers are those of the working tree at commit ff40bf9. "Draft uses" says which value `draft.md` took and why.
Items marked (in place) are already annotated in the file itself and are listed only because a reader who quotes
the unannotated line will be wrong.

34 items: 6 that could mislead a reader about a result (section A), 17 numerical disagreements (section B),
11 stale statements or bookkeeping problems (section C).

**Outcomes** (consistency pass, 2026-11-14; one "Outcome" line under each item): 24 fixed in the files this pass may
edit (in 11 of them a part in NOTEBOOK, STATUS or other files is left for the lead), 7 left wholly for the lead, 3 need no change.
Three sub-points are undecided (B3's 1.51, B7's 0.88, B8's 0.051 against 0.052). Replacement text for NOTEBOOK.md and
STATUS.md, and the references in files outside the pass's list: `docs/paper/FOR-LEAD.md`.

## A. Could mislead a reader about a result

A1. **The single face-law line and "A/7.7" are still presented as current.**
`research/STATUS.md:180-184` ("τ_face ≈ exp(−0.09 + 0.209·A) … one line over six decades for flat slab faces,
octahedral faces (≈1.7–1.9× tougher), symmetric soups and the closed cubes") and `:189-190` ("effective face area
A/7.7"); `docs/WHAT-I-SEE.md:74-76` ("Flat faces and triangular faces, six decades of lifetime: one line") and
`:105`; `web/src/layers.js:170-173`, `web/src/main.js:763-764`, `web/src/tour.js:120`. Against: CLAIMS S1 is
superseded (`research/CLAIMS.md:77`); GP7 puts an octahedral face 0.91 ± 0.06 above a slab face at A = 108
(`:137`); GP9 and SH3 show no single slope for periodic faces (`:139`, `:142`); GP1 has the octahedral slope
rising to 0.221 (`:131`). STATUS's own bracketed notes further down (`:195-198`, `:202-203`) contradict its
lines 180–190. Draft uses: no single line; Tables 2, 3, 6–8.
**Outcome (A1):** fixed in `docs/WHAT-I-SEE.md`, `web/src/tour.js`, `web/src/layers.js` (comment), `web/src/main.js` (caption), CLAIMS F4/F6; STATUS lines for the lead (`FOR-LEAD.md` §2).

A2. **The list of local slopes "0.201, 0.212, 0.212, 0.218, 0.221" cannot come from one set of lifetimes.**
`research/NOTEBOOK.md:905-906`, `research/fluct/README.md:47-49`, `research/gpu/README.md:13` and `:139-140`,
`research/OPEN-PROBLEMS.md:66`. The third slope (63 → 84) uses ln τ_face(84) = 18.077 (the CPU value, 342
deaths); the fourth (84 → 108) uses 18.141 (the GPU value). With 18.141 throughout the list is 0.201, 0.212,
0.2146, 0.2181, 0.221, which is what the GPU README's own table says (`research/gpu/README.md:131-134`, column
"local slope": 0.2119, 0.2146, 0.2181, 0.221). With 18.077 throughout it is 0.201, 0.212, 0.2116, 0.2208, 0.221.
Four values of ln τ_face at A = 84 are in circulation: 18.077 (`NOTEBOOK.md:905`), 18.141 ± 0.005
(`gpu/README.md:132`), 18.154 ± 0.025 (`gpu/README.md:9`), 18.148 ± 0.028 (`NOTEBOOK.md:1255`). They agree within
errors; the slope list mixes them. Draft uses: 18.141 ± 0.005 and the slopes computed from Table 2.
**Outcome (A2):** fixed in `research/fluct/README.md`, `research/gpu/README.md`, `research/OPEN-PROBLEMS.md` (one A = 84 value, 18.141, throughout: 0.201, 0.212, 0.215, 0.218, 0.221); NOTEBOOK for the lead (`FOR-LEAD.md` §1).

A3. **Ledger ids collide and theorem numbers differ between files.** `research/CLAIMS.md` uses K1, K2, K3 twice:
`:112-114` (thickness: one or two layers; transverse firewall; one-layer oscillators) and `:145-147` (half-space
sealing; face12e slabs; face12e boxes). `docs/AUTOMATON.md:98` and `:108` call the threshold lemma T5 and the
sealed-set theorem T6; `research/CLAIMS.md:35-36` use T5 for "axis-aligned half-spaces do not confine" and T6 for
the cube's cell count, with the threshold lemma at T8 (`:38`) and sealed sets at T9 (`:39`).
`research/NOTEBOOK.md:828-829` and `research/theory/class.md:44` use the AUTOMATON numbering. Draft uses: its own
theorem numbers, with the ledger row named each time.
**Outcome (A3):** fixed in `research/CLAIMS.md` (later K1–K3 renamed K9–K11; T5, T6, T8, T9 and G2 cross-labelled, legend note); `draft.md` and `docs/overview` references for the lead (`FOR-LEAD.md` §3).

A4. **Grade "B−" is used in the ledger and not defined in it.** `research/CLAIMS.md:9-11` define A, B, C, D and
"B (table)"; rows GP1, GP2, GP5, GP6 (`:131`, `:132`, `:135`, `:136`) are graded "B−". The legend also defines B
as "re-run by the auditor on 2026-11-13", which cannot be what B means on the rows dated 2026-11-14. Draft uses:
B− = B, with the runs on a GPU that no second implementation has repeated.
**Outcome (A4):** fixed in `research/CLAIMS.md` (B redefined to name the checker and date; B− defined; no row regraded).

A5. **F4 is not marked as affected by GP9.** `research/CLAIMS.md:62` grades the flat-face law
"−0.09 + 0.209·A" B with its slope at A; `:139` (GP9) says "F4's 0.2088 is inflated by mixed widths", and the
counts line (`:177-178`) lists four superseded rows without F4. A reader of row F4 alone would take 0.209 as a
verified constant. Related: `README.md:29-31` keeps "about e^0.21 per cell … across six decades" but adds the
caveat; STATUS does not (A1).
**Outcome (A5):** fixed in `research/CLAIMS.md` (F4 marked qualified by GP9; tally line lists it); STATUS part as A1.

A6. **`research/OPEN-PROBLEMS.md` items 3, 8, 9 are behind the ledger.** `:12` "−ln(death rate)/A → 0.208"
(the limit is withdrawn, CLAIMS GP4, `CLAIMS.md:134`; the same item's own postscript at `:26` says so);
`:63-65` "In the two cube-centred runs the death rate falls with age (p = 0.04, 0.01): unexplained" (GP5,
`CLAIMS.md:135`: at R = 43 it was noise; only R = 45 is unresolved); `:68` "Needs slab faces at A > 90" (done:
GP7, GP8). Also `research/STATUS.md:238-239` "whether 0.208 per site holds for asymmetric faces beyond A = 84"
(answered: it rises, GP1).
**Outcome (A6):** fixed in `research/OPEN-PROBLEMS.md` (items 3, 8, 9); STATUS 241–242 for the lead.

## B. Numbers that differ between files

B1. Cube-centred O_h soups at A = 693 (R = 41, 20 deaths): `research/fluct/README.md:24` and `:181` give
3.4 × 10⁸ and ln τ = 19.64 ± 0.22; `research/fluct/data/sym_residence.csv` (row `sym41c`) gives 3.613 × 10⁸ and
19.705; `research/NOTEBOOK.md:680` gives 19.71. Draft uses: the csv, pooled with the second run (58 deaths,
19.68 ± 0.13).
**Outcome (B1):** fixed in `research/fluct/README.md` (19.71, 3.6×10⁸, from the csv).

B2. Vertex/cube factor at A = 693: 3.3 (ln 1.19 ± 0.28) in `research/fluct/README.md:26`; 3.1 (ln 1.12 ± 0.29)
in `research/NOTEBOOK.md:710-711`; 2.0 (ln 0.70 ± 0.20) for fresh soups and 2.39 pooled in
`NOTEBOOK.md:739-741` and CLAIMS S3. The first two are superseded (in place, by notes at
`fluct/README.md:39-45`); they differ from each other all the same. Draft uses: 2.0 ± 0.4, fresh soups.
**Outcome (B2):** fixed in `research/fluct/README.md`: traced; the 3.3 was computed against 19.64 (B1), the 3.1 against the csv's 19.705.

B3. Vertex/cube factors below A = 693: `research/NOTEBOOK.md:710` lists six ("1.51, 1.52, 1.53, 1.60, 1.49,
1.31 ± 0.17 at A = 360 … 630"); `python3 research/fluct/sym_fit.py` prints five (A = 408 … 630: 1.52, 1.53, 1.60,
1.49, 1.31), as does CLAIMS S3 (`CLAIMS.md:79`). There is no cube-centred measurement at A = 360 in
`sym_residence.csv`; where the 1.51 comes from is not stated.
**Outcome (B3):** fixed in `research/CLAIMS.md` S3 and `research/fluct/README.md` (range A = 408–630); the 1.51 at A = 360 has no source in any version of the csv: undecided where it came from, NOTEBOOK/STATUS for the lead.

B4. Fit to cube-centred symmetric faces: "0.69 + (0.209/6)·A − 0.195·√A" in `research/STATUS.md:197` and in the
claim text of CLAIMS S2 (`CLAIMS.md:78`); `sym_fit.py` prints 0.698 and −0.196 (CLAIMS S2's own level column
says so). Draft uses: 0.698, −0.196.
**Outcome (B4):** fixed in `research/CLAIMS.md` S2 (0.698, −0.196); STATUS 200 for the lead.

B5. Pooled 6 × 6 × 8 face value: 22.536 ± 0.031 in `research/gpu/README.md:257`; 22.537 ± 0.031 in
`research/NOTEBOOK.md:1222`, `:1238` and CLAIMS GP8. Draft uses: 22.537.
**Outcome (B5):** fixed in `research/gpu/README.md` (`gpu_pr14_lead_check.py` prints 22.537).

B6. 4 × 6 × 8 face value: 14.971 ± 0.002 in `research/NOTEBOOK.md:1353`; 14.970 in `research/gpu/README.md:276`
and 14.970 ± 0.002 in `research/shape/README.md:104`. Draft uses: 14.971 (the notebook's table).
**Outcome (B6):** for the lead: the run's value is 14.970 (`gpu_pr16/recompute.py`); 14.971 is the pool with 6 × 4 × 8; the NOTEBOOK carries it.

B7. Octahedral against periodic face at A = 108: 0.91 ± 0.06 (CLAIMS GP7, `CLAIMS.md:137`); "0.88 after the
firewall correction" (`research/theory/class.md:78`); 0.84 ± 0.04 "with the pooled slab value"
(`research/STATUS.md:132`). Three numbers for one comparison, depending on which slab value is subtracted. Draft
gives 0.91 and 0.84 and says which is which.
**Outcome (B7):** fixed in `research/CLAIMS.md` GP7 (gives 0.91 ± 0.06 against 22.470 and 0.84 ± 0.04 against the pooled 22.537); class.md's 0.88: undecided (not traced; file not this pass's).

B8. Step in ln τ_face from shortest loop² 12 to 16 at A = 60: 0.052 ± 0.005 (`research/shape/README.md:128`,
`:164`); 0.051 ± 0.005 (`research/NOTEBOOK.md:1435`); +0.064 ± 0.004 (`research/shape2/README.md:29`);
"+0.056 to +0.063" (`research/NOTEBOOK.md:1508`, CLAIMS SH4). Different runs and poolings; no file reconciles
them. Draft uses: SH4's range.
**Outcome (B8):** fixed by cross-reference in `research/shape/README.md` and `research/shape2/README.md` to SH4's range; the runs are not reconciled number by number, and 0.051 against 0.052 (NOTEBOOK against shape README) is undecided.

B9. The pair of equal-shortest-loop tori at A = 60: 0.019 ± 0.004 (`research/NOTEBOOK.md:1420-1421`,
`research/shape/README.md:17-18`, `research/shape2/README.md:5`); 0.018 ± 0.004 (`research/STATUS.md:68`);
0.0142 ± 0.0019 over four runs (CLAIMS SH2; `NOTEBOOK.md:1512-1513`); "0.014 ± 0.003 at both areas"
(`research/STATUS.md:71`, where the ledger has 0.0142 ± 0.0019 and 0.0151 ± 0.0017). The notebook entry at
`:1513-1514` says the later value replaces the earlier one; `shape/README.md` and STATUS line 68 still carry the
earlier. Draft uses: the ledger's.
**Outcome (B9):** fixed in `research/shape/README.md`, `research/shape2/README.md`; STATUS 68, 71 for the lead.

B10. Twisted torus (4,1),(0,6) at A = 72: 15.066 ± 0.014 (experiment; `research/shape/README.md:94`, CLAIMS
SH1's claim text) against 15.035 ± 0.009 (independent rerun; `NOTEBOOK.md:1413`, CLAIMS SH1's level column):
1.9σ apart; pooled 15.043 ± 0.007 (`shape/README.md:99`). CLAIMS SH1 quotes the unpooled experiment value in
the claim. Draft gives all three.
**Outcome (B10):** fixed in `research/CLAIMS.md` SH1 (states rerun and pooled values next to the experiment's).

B11. "Gump's" slab slope in comparisons with other rules: 0.212 per face cell in `research/NOTEBOOK.md:1034`,
`research/OPEN-PROBLEMS.md:88` and `research/theory/class.md:128` (0.2121 ± 0.0004,
`research/audit/REVIEW-class.md:399`); 0.2088 ± 0.0009 in CLAIMS F4 and `class.md:489` ("notebook 0.208");
0.2072 ± 0.0001 within a width family and 0.2085 area-only over s ≥ 4 (CLAIMS GP9). All are area-only or
family slopes over different sets of mixed-width faces; none of the comparisons says which.
**Outcome (B11):** fixed in `research/OPEN-PROBLEMS.md` 15b and `docs/WHAT-I-SEE.md` (the 0.212 is now scoped: slabs of mixed widths, A = 27–75); NOTEBOOK 1034 and class.md for the lead.

B12. Octahedral first-face-death means by soup density at R = 11: `research/NOTEBOOK.md:307` gives 0.91, 1.08,
1.00, 1.04 × 10⁵ for p = 0.3, 0.4, 0.5, 0.6; the regenerated `research/peeling/octa_first.csv` has 99,545,
108,090, 100,483, 105,280. The audit note at `NOTEBOOK.md:306` gives the new R = 11 value (9.95 × 10⁴) but the
next bullet was not annotated.
**Outcome (B12):** for the lead (NOTEBOOK; csv gives 1.00, 1.08, 1.00, 1.05 ×10⁵).

B13. Thickness independence at A = 48: `research/NOTEBOOK.md:298` "9.9, 10.4, 10.3, 10.4, 10.4 × 10³ for
m = 7, 8, 9, 10, 12"; `research/peeling/slab_area.csv` has 9,878.7, 10,354.1, 10,323.0, 10,345.8, 10,346.9, i.e.
9.9, 10.4, 10.3, 10.3, 10.3 (a rounding slip). Draft uses: the csv.
**Outcome (B13):** for the lead (NOTEBOOK; csv gives 9.9, 10.4, 10.3, 10.3, 10.3 ×10³).

B14. Side-16 first-face forecast percentile: "58th percentile" (`research/NOTEBOOK.md:629`, CLAIMS C4);
"quantile ≈ 0.57" (`research/fluct/README.md:204-205`).
**Outcome (B14):** fixed in `research/CLAIMS.md` C4 and `research/fluct/README.md`: recomputed with `predict.py`'s law from the committed forecast, quantile 0.566 (57th); NOTEBOOK 629 and PREDICTIONS.md for the lead.

B15. The 2D edge law at L = 12: 5.85 in the independent check that earns G1 its grade A
(`research/NOTEBOOK.md:831-832`, 108–415 deaths per size), 5.72 from the fitted law (same lines), 5.644 from the
later deterministic strips and 5.654 from the model (`NOTEBOOK.md:1259`). The first differs from the last two
by about 0.2, some two of its own standard errors; G1's A therefore rests on the slope (0.42), not on the
values.
**Outcome (B15):** fixed in `research/CLAIMS.md` G1 (the grade is stated to rest on the slope; values cross-referenced to X2).

B16. First-face-death mean at R = 13 (A = 84): 8.86 × 10⁶ ± 0.48 × 10⁶ (`research/fluct/README.md:22`);
9.45 × 10⁶ ± 0.5% (`research/gpu/README.md:132`); 9.41 × 10⁶ (`research/peeling/octa_first.csv`).
`gpu/README.md:136` says the GPU value "reproduces" the first; they are 1.2σ apart, which is agreement, but it
is the source of A2.
**Outcome (B16):** no change needed (agreement within errors); the GPU value is cross-referenced in `research/fluct/README.md`; the slope list it fed is A2.

B17. Lifetime convention: `research/CLAIMS.md:81-82` (C1, C2) quote 4,460,298 and 2,919,617,676 as lifetimes;
`docs/AUTOMATON.md:143-145` says those two are the engine's `detected_gen`, one or two generations after the
final state is entered, unlike the other rows of its table. Draft's Table 1 says so.
**Outcome (B17):** fixed in `research/CLAIMS.md` C1, C2 (side 14: cycle_start 4,460,296 re-run with the engine; side 16: 2,919,617,675 from `cube16_summary.json`; side 15: both 37,367,092).

## C. Stale statements and bookkeeping

C1. `research/peeling/README.md:34` says `figures.py` writes `research/figures/peel_slabs.png`; the script
(`research/peeling/figures.py:2`, `:77`) and the notebook (`NOTEBOOK.md:292`) say `peel_cuts.png`, which is the
file that exists.
**Outcome (C1):** fixed in `research/peeling/README.md`.

C2. `research/NOTEBOOK.md:802` and `research/AUDIT-2026-11-13.md:4` speak of 71 headline claims; the ledger has
108 rows (`research/CLAIMS.md:176`). True at the time; a reader of the notebook alone gets the old number.
**Outcome (C2):** for the lead (NOTEBOOK 802; `AUDIT-2026-11-13.md` is right for its date).

C3. The ledger's own tally (`research/CLAIMS.md:176-177`: A 43, B 36, C 28, D 1) could not be reproduced
mechanically: taking the best letter that appears in each row's level column gives A 43, B 37, C 27, D 1. The
difference is one row whose level reads "C (…: B)" (C8 or Z11); which way such rows count is not stated.
**Outcome (C3):** fixed in `research/CLAIMS.md`: recounted mechanically with the rule stated (A 40, B 40, C 27, D 1); the earlier 43 took the areas "A = 84/828/693" in GP1, C9, S3 for grades.

C4. `research/NOTEBOOK.md:889` "index of 59 sources"; `research/theory/swarm/library/shelf.md` now has 73 rows.
**Outcome (C4):** for the lead (NOTEBOOK 889; shelf.md has 73 data rows, checked).

C5. Exam scores of the theory effort: "four hold, two fail, two undecided" in the heading at
`research/NOTEBOOK.md:1112` (the eight sampled entries); "five entries hold, four fail or missed, two undecided,
three not run" at `NOTEBOOK.md:1325` and `research/STATUS.md:100` (all entries, from the board's closing table).
Both are right for their own sets; `research/STATUS.md:152-156` lists four holds a few lines after line 100
says five.
**Outcome (C5):** for the lead (`FOR-LEAD.md` §1, §2: both counts are right for their sets; a qualifier suggested).

C6. `research/STATUS.md:13` "49/49 tests" for the web app and CLAIMS R6 (`CLAIMS.md:23`), against "web suite
79/79" at `research/STATUS.md:88`.
**Outcome (C6):** fixed in `research/CLAIMS.md` R6 (web suite re-run: 79/79); STATUS 13 for the lead.

C7. `research/STATUS.md:19-51` ("In flight (2026-11-13, late)") describes agents, pauses and pull requests that
the same file's later sections say are finished; the section order makes the file read as if the pause were
current.
**Outcome (C7):** for the lead (STATUS section order).

C8. `research/NOTEBOOK.md:148` "(≈ 0.30)" for the bulk density and `:477` "e^−5.3 ≈ 0.5%" (in place: corrected
by bracketed notes on the following lines; the uncorrected figures remain in the sentences).
**Outcome (C8):** no change needed (annotated in place; the notes on the following lines give the corrected figures).

C9. `research/fluct/README.md:19` and `:111` still print "I(0) = 0.2077 ± 0.0014 + 0.55/A" in bold, each with a
bracketed retirement note; `docs/WHAT-I-SEE.md:279` recounts the same number as a past error (consistent, listed
for completeness). `research/STATUS.md:202-203` likewise (in place).
**Outcome (C9):** fixed in `research/fluct/README.md` (the retired fit is no longer in bold; the bracketed notes stay); STATUS in place.

C10. `research/fluct/README.md:20-21` attributes the lead's high R = 9 value to an earlier start time; the note
at `:43-45` and `NOTEBOOK.md:663` say the cause was sampling noise (in place).
**Outcome (C10):** fixed in `research/fluct/README.md` (inline pointer to the audit note at the attribution).

C11. `research/peeling/face_law_fit.py` prints "9 slab batches"; `research/NOTEBOOK.md:296` says "8 near-square
tori". Both are right (the 3 × 3 torus has two batches) but the fit's unit is the batch.
**Outcome (C11):** no change needed (both counts are right; the 3 × 3 torus has two batches).
