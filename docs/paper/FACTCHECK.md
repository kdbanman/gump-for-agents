# Fact-check of `docs/paper/draft.md`

2026-11-14, by a subagent that did not write the draft. Draft as of commit 736b891, checked against
`research/CLAIMS.md` (after the consistency pass: K9–K11, R6 = B), the latest notebook entries on each matter
(including "consistency corrections"), the audits, `research/PRIOR-ART.md` and
`research/theory/swarm/library/shelf.md`, and scripts that run in under a few minutes on tracked data (commands below).
Line numbers are those of the draft **after** this pass's fixes (commit 367f5b8).

Severity: **wrong** (the source gives a different value or contradicts the statement), **stale** (superseded by a
newer source), **imprecise** (right in substance, but a number, hypothesis or scope differs from the source),
**unsupported** (no source in the repository supports the statement as worded).
"Fixed" = corrected in the draft by this pass; "for the lead" = needs judgment, left as is.

## Discrepancies

| # | line | draft says | source says | source | severity | action |
|---|---|---|---|---|---|---|
| 1 | 502 | forecast 2 held "at about the 58th percentile" | quantile 0.566, the 57th percentile | NOTEBOOK "consistency corrections" (side-16 first-peel forecast); CLAIMS C4 | stale | fixed |
| 2 | 595 | Table 6, s = 4 at A = 72: 14.971 ± 0.002 | the run's own value 14.970 ± 0.002; 14.971 pools it with 6 × 4 × 8 (14.972) | `python3 research/audit/gpu_pr14_lead_check.py research/data/gpu_facelaw` prints 14.970 (4x6x8) and 14.972 (6x4x8); NOTEBOOK "consistency corrections" | stale | fixed |
| 3 | 1036 | R6 listed under "graded C and not mentioned" | R6 is B (79/79 re-run 2026-11-14) | CLAIMS R6 | stale | fixed |
| 4 | 491 | Table 4: "30 and below: 1,792 in all" | 1,792 is the sum through R = 22 (to the last hull-layer death, last alive 2,919,617,536); from R = 30 to the end (2,919,617,676) is 1,932 | `research/data/cube16_events.jsonl` (last_alive of the layer deaths along axis 0) and `cube16_summary.json`; NOTEBOOK 2026-11-13 "side-16 cube ends" table | wrong | fixed ("1,932 in all (1,792 to the last layer death)") |
| 5 | 819–821 | (W) in the conditional area law: "… with censoring at most c times the hazard and a stated bound on the low-set weight" | the audit's hypothesis (b) states the bound: w = Σ_{z<K} p_z ψ(z) ≤ 1/(2(1 + c)), ψ(k) = e^{−θ₀(k−k₀)⁺}, quasi-stationary over the window | `research/theory/swarm/audit/AUDIT-path.md` §0 item 3 | imprecise (hypothesis not stated as the audit words it) | fixed |
| 6 | 766 | G1 "A for the central law" | the ledger scopes the A to the slope; the check's values lie 0.1–0.2 above the law's intercept | CLAIMS G1 | imprecise (grade scope) | fixed |
| 7 | 711–712 | O1 cells "are overcrowded after having been alive two generations earlier" | an O1 event is a cell overcrowded at t with x(t−1) = 1: alive one generation earlier | draft Theorem 5; `docs/AUTOMATON.md` T5; `research/theory/threshold.md` | wrong (wording) | fixed |
| 8 | 568–569 | the cube on the face is a fixed point "once w ≥ 4–5" | w ≥ 4 for a cube at a hull vertex, w ≥ 5 for a cube anywhere on the face | NOTEBOOK 2026-11-14 "where the exponent lives" | imprecise | fixed |
| 9 | 843 | τ_L ≤ 3·8^L; τ_L ≥ lifetime of OP₅(½) | Theorem U: the upper bound for L ≥ 5; the comparison with row 0 started full | `research/theory/swarm/audit/AUDIT-theoremA.md` §1.3 | imprecise (hypotheses) | fixed |
| 10 | 893 | "the one recorded non-monotone survival theorem is [BN94]" | BN94 is "the one non-monotone CA survival theorem on the list"; the shelf also records Bramson–Ding–Durrett 1991, a non-monotone process shown to survive | `shelf.md` §2 | imprecise | fixed ("cellular-automaton survival theorem") |
| 11 | 48 | "In everything recorded in this project's literature notes … nothing is proved" | the "nothing is proved" verdict is about the supertransient / stable-chaos sources; the same notes record theorems (finite contact process, QSDs) | `research/PRIOR-ART.md` last section; `shelf.md` §1, §8 | imprecise (scope) | fixed (scoped to supertransient and stable-chaos sources) |
| 12 | 119 | engine matches the logs "on the 2012 code's torus" | for even H only | CLAIMS R3 | imprecise | fixed |
| 13 | 534–535 | side-17 mean 3.2 × 10¹⁰ cited to C9 | C9 gives the forecast mean 2.6 × 10¹⁰; 3.2 × 10¹⁰ comes from the measured GP2 value 24.175 | CLAIMS C9, GP2; `research/gpu/PREDICTIONS.md` | imprecise (citation) | fixed |
| 14 | 250 | one-layer oscillators of periods 3–12, no ledger id | ledger K3 (thickness study), grade C | CLAIMS K3 | imprecise | fixed (id added) |
| 15 | 334 | slab faces A ≥ 36: KS p = 0.5–0.96 (CV 0.96–1.05) | in `slab_area.csv` the m = 8 rows with A ≥ 36 have KS p 0.126 (2 × 8), 0.519, 0.683, 0.69, 0.811, 0.96, 0.974 and CV 0.964–1.045; with all thicknesses p goes down to 0.042 (4 × 5 × 10) and CV up to 1.06. The ledger F5 has the same "0.5–0.96", so the set of slabs meant is not recorded | `research/peeling/slab_area.csv` columns cv, ks_p; CLAIMS F5 | wrong as worded (ledger too) | **for the lead** (draft and F5 need the same correction; which slabs F5 meant is not recorded) |
| 16 | 367 | Table 2, R = 7: ln τ_face = 6.804 ± 0.003, "F9, tabulated value" | the tabulated file gives 6.8054 (8 × first_peel_mean 112.84; also −ln h); the fluctuation README and notebook print 6.804. Same at R = 11 (CPU 13.633 in the draft and README, 13.6317 in the file) and R = 9 (9.8202 file, 9.819 README/notebook, 9.820 draft) | `research/fluct/data/qsd_summary.json`; `research/fluct/README.md`:47 | imprecise (≤ 0.4σ; sources disagree in the last digit) | for the lead |
| 17 | 368 | engine-only R = 9: 9.824 | ln(8 × 2,312) = 9.825 from the notebook's 2312 ± 20 (unrounded mean not recorded) | NOTEBOOK 2026-11-13 "a face dies off the end of a straight line" | imprecise (0.001) | for the lead |
| 18 | 458 | the two GPU points lie "0.16 and 0.27" above the S2 curve | the fit printed by `sym_fit.py` (0.698134, −0.195996) gives 21.737 at A = 759 and 23.900 at 828: 0.166 and 0.275 against 21.903 and 24.175 (0.15 against the pooled 21.889) | `python3 research/fluct/sym_fit.py` | imprecise | for the lead |
| 19 | 662 | Table 8, loop² 4, 60 → 72: 0.1346 ± 0.0010 | `shape2_lead_check.py` prints 0.1353 (the README table, which the draft copies, has 0.1346); other entries agree | `python3 research/audit/shape2_lead_check.py`; `research/shape2/README.md`:189 | imprecise (sources disagree) | for the lead |
| 20 | 675–676 | SH4: 4 × 4 lies 0.0135 ± 0.0021 below a loop² 12 class, "A, two codes" | 0.0135 is from the reviewer's runs only; the census values (`shape2_lead_check.py`) put 4 × 4 0.006 ± 0.003 below (1,6),(0,16) and above (2,2),(0,8); span 0.0147 in the census, 0.0156 in the review | `python3 research/audit/shape2_lead_check.py`; `research/audit/REVIEW-shape2.md`:35, 123 | imprecise (the number is one code's) | for the lead |
| 21 | 486, 502, 504 | first and second face deaths of the side-16 cube "2,362,434,048", "2,886,100,480" | these are the last generations at which the layer was seen alive (events sampled every 64); §5.1 defines a face death as the first generation with the layer empty (≤ 2,362,434,112 and ≤ 2,886,100,544). The ledger C2 uses the same numbers | `research/data/cube16_events.jsonl` (gen vs last_alive) | imprecise (convention differs from §5.1's definition by < 64 generations) | for the lead |
| 22 | 531 | "the side-16 cube was lucky at about the 1% level" (not marked preliminary) | the 1% is CLAIMS L3, grade C, post hoc | CLAIMS L3; C6 | unsupported as a graded result | for the lead (mark preliminary or drop) |
| 23 | 496–516 | Table 5 "lists every one we found" of forecasts committed before outcomes, omitting other rules and grade-C results | the swarm exam's gump forecast path E3 (remnant on a slab face equals the hull's) failed; it has no ledger row, so it is neither graded C nor listed | NOTEBOOK 2026-11-14 "the swarm's predictions examined" | unsupported ("every") | for the lead |
| 24 | 780–781 | "the 2D slope 0.416 is twice the periodic-face slope of the 3D rule to three figures" | 2 × 0.2088 = 0.4176, 2 × 0.2072 = 0.4144; the exponent review lists "0.416 ≈ 2 × 0.208" as not established either way (ratio range 1.6–2.0) | NOTEBOOK 2026-11-14 "where the exponent lives" ("Does not stand as written"); CLAIMS F4, GP9, G1 | imprecise | for the lead |
| 25 | 802–804 | "Proved without conditions: … the exhaustive enumerations of Section 8 within their stated sizes" | parts are grade C: Z2 for n = 14–16, Z3 for unions 12–13 and the hinge-flip property, Z4 entirely (Section 8 itself marks them preliminary) | CLAIMS Z2–Z4 | imprecise | for the lead |
| 26 | 122–124 | "Every other stepper … (numpy, bit-sliced C …, symmetry-reduced, GPU) was required to agree bit for bit … (R7; B)" | R7 covers gl.py, rep.c, fl.c; the GPU kernels were matched only by CPU emulation (GP1 B−) | CLAIMS R7, GP1 | imprecise (citation) | for the lead (§12 says it correctly) |
| 27 | 718–724 | twist lemma proof | the proof does not derive m ∈ {1,2,3,4,6} (a cyclic quotient of a subgroup of O_h has order dividing an element order, and O_h's element orders are 1,2,3,4,6), nor that L is the least positive element of the image; the repository's proof (`research/clockwork/README.md`:23–27) has the same gap | `research/clockwork/README.md` | imprecise (step not written out; the statement is true) | for the lead |
| 28 | 882, 885, 888, 889, 890 (+ 886, 922) | novelty judgments "Appears new", "probably new", "Possibly new" | the strongest supported form is "not found in our search". For rows 885 (sealed sets), 888 (noise boundary layer) and 890/922 (shape dependence) `PRIOR-ART.md` records **no search at all**; the shelf lists related work (BY08, KL08, CD11, MV10) but no verdict. Rows 882 and 889 match PRIOR-ART's own "appears new", which the second pass says should be worded "not found" | `research/PRIOR-ART.md` §§2, 4, second pass (b); `shelf.md` | unsupported (885, 888, 890, 922); imprecise (882, 886, 889) | for the lead |
| 29 | 887 | "large deviations in cellular automata exist [BGPV19] but not for a density tail used as an extinction-rate predictor" | PRIOR-ART: "I found nothing on the density tail … used as a QSD / extinction-rate predictor" (absence in a search, not a fact) | `research/PRIOR-ART.md` §3 | imprecise | for the lead |
| 30 | 889 | "symmetric soup censuses exist" | Catagolue/apgsearch pages were seen only as search summaries, "not opened, so not citable" | `research/PRIOR-ART.md` second pass (b) | unsupported (uncited, and the survey says not citable) | for the lead |

Counts (30 rows): wrong 3 (#4, #7, #15), stale 3 (#1–#3), imprecise 20, unsupported 4 (#22, #23, #28, #30; #28
is counted once, as unsupported, though some of its rows are only imprecise). Fixed 14 (#1–#14); for the lead 16
(#15–#30).

## Outcomes of the items for the lead (2026-11-14, a second subagent carrying out the lead's decisions)

- **#15** Applied. The notebook entry behind F5 (2026-11-12, "how chaos dies") is about the m = 8 near-square tori
  of the face-law fit; its numbers are exactly those of the fit's batches with A ≥ 36 and a test: 3×4, 3×5, 4×4,
  4×5 (CV 0.964–1.045, KS p 0.519–0.96). Draft and F5 now say so, and also give the whole table (14 batches with
  A ≥ 36 and a test: p 0.042–0.974, one below 0.05, CV 0.962–1.06). Grade not changed.
- **#16** Applied: Table 2 now 6.805 and CPU 13.632 (R = 9 stays 9.820), and the local slope 0.2011 → 0.2010; the
  note names `qsd_summary.json`.
- **#17** Applied: re-ran `face_endgame_check.py 9 16000` (exact reproduction, mean 2312.1 ± 19.7); Table 2 now
  9.825 ± 0.009, named in the note.
- **#18** Applied: 0.166 and 0.275 (0.152 against the pooled 21.889), naming `sym_fit.py`'s coefficients.
- **#19** Applied: 0.1353 ± 0.0008 from `shape2/data/explore_report.txt` (the lead check prints 0.1353); the README's
  0.1346 noted in the caption and in `FOR-LEAD.md`.
- **#20** Applied: census 0.0061 ± 0.0028, review 0.0135 ± 0.0021, pooled 0.0108 ± 0.0017 (6.4 SE), χ² 4.4/1
  (p 0.036); "not ordered" stands (3.0 SE even with the error scaled by √χ²). Draft and SH4.
- **#21** Applied in the draft (§5.6, covering Table 5 too) and as a note in C2.
- **#22** Applied: marked preliminary and post hoc in the sentence (L3; C).
- **#23** Applied: Table 5 row 14 (path E3, failed); caption names the sources searched and the forecast files not
  searched; the exam's 2D-rule failures and undecided entries and C-E1 are named in the caption.
- **#24** Applied: plain numbers 0.416 and 0.414–0.425; "whether this is more than a coincidence is not established".
- **#25** Applied: §10.1 keeps Z1, Z2 (n ≤ 13), Z3 (unions ≤ 11); the grade-C enumerations are a separate
  preliminary paragraph.
- **#26** Applied: §2.3 cites R7 for numpy/bit-sliced/orbit-reduced steppers and GP1 (B−), GP7 for the GPU kernels'
  CPU emulation.
- **#27** Applied: the step is written in full in the draft and in `research/clockwork/README.md`; the hypothesis it
  uses (G = lattice symmetries p ↦ Rp + t, R ∈ O_h) is now stated; T7 annotated. The lemma's tag stays [proved].
- **#28** Applied: "not found in our search" where `PRIOR-ART.md` records a search (rows 882, 886, 887, 889, 891);
  "no prior-art search has been made yet" for 885, 888, 890 and the sentence at 922; abstract reworded.
- **#29** Applied: "our search found nothing on …".
- **#30** Applied: kept, marked as seen in search results only, not opened, not citable.

## Checked and found right (by section; counts are of distinct numbers or statements)

- **Abstract, §1** (12): density 0.41552 ± 0.00002; e^{0.21}; ln τ range 5.6 (slab fit at A = 27: 2 × 139 = 278) to
  29.3; side-16 2,919,617,676 and factor 12; SH5 refutation; 0.015 in ln τ (X1, SW2); the conditional results'
  hypotheses as summarised; supertransient citations [CK88, WS03, HKTP10, TL08, PT09] against PRIOR-ART and shelf.
- **§2** (18): coordinates, 3N³ cells, offsets and non-neighbours (AUTOMATON §2); 2√2 shell (PRIOR-ART §2); B45/S345
  and the threshold-with-cap form; O_h invariance; the owner's intended variant (AUTOMATON §2); R1–R4, R7 grades;
  T6 (3n²(n+1), 3n − 2); Table 1 all nine rows (AUTOMATON §4, CLAIMS C1, C2, Z11); the detected_gen convention.
- **§3** (30): Theorems 1–4 and their proofs line by line against AUTOMATON §3 (T1 enumeration recomputed by hand:
  Δs = 4:1, 2:2, 0:6, −2:2, −4:1; T2 1 + 2 = 3; T3 3, 2 and the 1 + 2 + 1 counterexample); K9 against
  REVIEW-class §1.2 Theorem A′; Theorem 5 statement and proof step by step (symmetry step, both non-overcrowded cases,
  the overcrowded term in [2.5, 9.5]), consequences (i)–(iv) and the bound −6N ≤ E ≤ 7N, 26N + 1, R₃/10, 5,683 steps,
  1,307 / 329 / 978 objects (`research/theory/threshold.md`:68–99); Theorem 6 statement and proof of (b) line by
  line against `research/theory/thickness.md` §2 (e + 2(a + b) = 4d, the ≥ 5 / ≥ 4 counts, torus and hull lifts),
  (c) and the 36-cell set's grade; K1 thickness means; Proposition 7 (`python3 research/atlas/vertex_star.py`;
  NOTEBOOK lines 104–108, 189–192).
- **§4** (14): P1, P2 with rerun values; P3 recomputed (fixed points 0.1785, 0.4438, slope −1.553, 4-cycle 0.3185 →
  0.4860 → 0.3688 → 0.5112, mean 0.4211); P7; P8 incl. "N = 6, 7, 8" (NOTEBOOK 333); P4–P6 marked preliminary.
- **§5.1** (10): F1 recomputed (`gump run --cube 11 --events`: 31 → 27 by generation 5, deaths at 3290, 3477, 3796);
  F3; F2 preliminary; face area A = 3k(k + 1)/2 for R = 7…17; slab A = 3n.
- **§5.2** (22): F4 fit recomputed (`python3 research/peeling/face_law_fit.py`: −0.091 ± 0.047, 0.2088 ± 0.0009,
  residual 0.18; eight lattices, nine batches; τ 278 to 1.6 × 10⁸); thickness at A = 48 (9.9, 10.4, 10.3, 10.3,
  10.3 × 10³); GP5 (k = 1.020, 5,971 deaths, 2.6 τ; R = 45 k = 0.84 on 192 deaths); F6 1.7–1.9; GP7 0.91 ± 0.06 and
  GP8 0.84 ± 0.04 (arithmetic); local slopes 0.2011, 0.2119, 0.2146, 0.2181 ± 0.0013, 0.2209 ± 0.0093 recomputed
  from Table 2; Table 2 deaths and values at R = 9…17 against `research/gpu/README.md`:132–136 and
  `qsd_summary.json`; CPU values at A = 84 (18.154, 18.148, 18.077); withdrawn 0.2077.
- **§5.3** (12): F8 ratios, h/p₁, 62–63 / 23–25 %, 0.67–0.72, engine-only values (NOTEBOOK 646–658); F9 endpoints
  0.2268, 0.2182, 0.2164, 0.2152 (`qsd_summary.json`); 0.5–0.8 miss; F10, F12 preliminary.
- **§5.4** (9): GP8 firewall rates and counts (13, 29), 3 × 6 × 8 validation 11.084 / 12.327 (one GPU run; the
  pooled 11.082 / 12.323 is what Table 6 uses) and CPU 11.076 / 12.310 (NOTEBOOK 1212–1234, REVIEW-gpu-pr14); F11
  preliminary.
- **§5.5** (34): Table 3, every entry against `research/fluct/data/sym_residence.csv` and `sym_fit.py` (pooled
  A = 693 rows 19.676 ± 0.131 from 58 deaths and 20.380 from 45 deaths recomputed; ratios 0.42, 0.42, 0.47, 0.40,
  0.42 / 0.47, 0.70, 0.51; the caption's 0.27 and 0.87); GPU rows against `research/gpu/README.md`:172–174; S2 fit and
  χ² 4.0/4; free slopes 0.024–0.044 (`research/fluct/README.md`:200); 759 → 828 slope 0.0329 ± 0.0011; S3 1.5,
  1.66 ± 0.08, 2.0 ± 0.4; side-13 hull A = 459 and 2.6 × 10⁵; L1, GP3, GP6 numbers; S4, SW3 preliminary.
- **§5.6** (30): Table 4 recomputed from the event log (2.362 × 10⁹, 5.237 × 10⁸, 3.08 × 10⁷, 2.71 × 10⁶, 7,040,
  27,712); Table 5 rows 1–13 against CLAIMS C3–C5, C9, GP2, GP8, GP9, SH1, SH2, SH5, SW2, the three PREDICTIONS files
  and `research/theory/exponent.md`:39, 358 (outcomes and verdicts, incl. "missed by 0.01" = 0.008); C8 3.3 means,
  P = 0.036; C5 7.4 means, 6 × 10⁻⁴, and 6.1 means, P = 0.002; C6 and P ≈ 0.18; C10, F13 and "fivefold".
- **§6** (12): X1 (A = 27, 48, 60, 75; 15.660; w = 4 0.06–0.07; octahedral 9.823, 13.644, 18.148; 0.03–0.04, 4–5σ);
  SW2; X2; X3 6.94 / 6.54.
- **§7** (40): Table 6 every entry and firewall share recomputed (`gpu_pr14_lead_check.py`); fits recomputed
  (`python3 research/audit/gpu_pr16/fits.py research/data/gpu_facelaw`: 0.2072 ± 0.0001, intercepts 0.053, 0.121,
  0.203, χ² 8.4/8; 0.2117, −0.054, χ² 5.6/9; 0.2085, χ² 512/10; s = 5 0.2082; s = 6 0.213); width differences
  −0.349, −0.740, −0.196, −0.002 ± 0.003; Table 7 against `research/shape/README.md`:80–100 (presentations, pooled
  values, reruns, 1.9σ, 15.043); 0.096 and 0.052; SH2; Table 8 against `research/shape2/README.md`:188–189 and the
  lead check (all but #19); SH4 +0.056 to +0.063 and +0.10; SH5 χ² 5.4, 22.7, 45.4.
- **§8** (20): Z1–Z4 numbers and grades; Theorem 5 link and the 329 objects; twist lemma statement and homomorphism
  step (G commutes with F, so k(gh) = k(g) + k(h)); [LW-Mod] period/mod sets (PRIOR-ART §5 and second pass); Z6 incl.
  "three kagome layers" and "no cell of period 2, 3, 6, 11, 22" (`research/clockwork/README.md`:9, 31–32); Z7; Z8
  (9,700 objects of period ≥ 3, 402 boxes); Z9 counts; Z10 preliminary; [LW-NT].
- **§9** (22): Q1 (960, 421 on 24³, 146, radius 10, 16 soups, 142, 3,420, 50 minimal, five collapse medians); Q2
  ≥ 29×; Q3 and gump's 28, 254, 3,420 (NOTEBOOK 253); K4 slopes 0.2156, 0.2121, within 0.2, fcc 0.181, 42 of 50;
  G1 0.472, 0.73 + 0.416·L, 286 to 5.8 × 10⁶ (`research/toy2d/README.md`:15); G2–G4, SW4 preliminary; K10, K7
  (10⁹ against 600–1,500), K8.
- **§10** (18): 10.2(a) against AUDIT-path §0 (objects, (R), (Φ), (W) after fix #5, the bound and liminf, P̄'s four
  terms, non-Markov remark, θ₀ = 0.40, κ = 0.35, k₀ = 5, block minima 0.4034–0.4261, margin 0.003, θ₀κ = 0.13–0.14,
  S′); 10.2(b) against AUDIT-theoremA §1.3–1.4 (F1, F2, BBS94 0.7491, L95 route, HS22 Cor. 4.8 sketch; ln τ_L at
  L = 8, 12, 16, 18 from its table at line 415); 10.3 V = 0.2191 (NOTEBOOK 1319).
- **§11** (rows not listed above): each "nearest known work" entry against PRIOR-ART and the shelf (E09 and LW-OT
  content, HKTP10's content, contact-process sources, MV12, GO/GFP85 via KMMK11 and GMRS23, LW-Mod / LW-NT, RK14's
  6,144 rules, "no finite-size exponential-lifetime theorem without monotonicity"); the twist and threshold verdicts.
- **§12** (8): check.sh has 20 checks in its default run (counted in `research/check.sh`); GPU 128 and CPU 840
  period windows (`research/gpu/README.md`:54–63); 6.2 × 10⁴ against 630 (NOTEBOOK 725); tie bias ≈ 0.02 (SH3);
  not-repeated list.
- **References** (35 entries): every one is recorded in PRIOR-ART or the shelf with the same authors, title, venue,
  volume, year and pages where given, and the "how far read" note is no stronger than the record.
- **Appendix**: superseded rows F7, S1, F9's limit, GP4 match the ledger's four; C-graded list matches the ledger. (As of 2026-11-14; rebuilt after the audit of 2026-11-15, see the third update below.)

## Not checked

- Anything that needs a run longer than a few minutes or bulk data under `research/scratch/`: P1–P8 runs, the
  survey, any GPU run, the side-16 run, F2's ratios, C6/C7 statistics, the lineage and exam runs. Numbers from these
  were checked against their committed tables and the ledger only.
- `research/check.sh` was not run (other agents' simulations); `docs/paper/check_face_area.py` was run (vertex-centred
  sizes only print; cube-centred A = 30–135 checked by the formula).
- Table 3's "states older than 1,000 generations"; the fresh-soup / copy split of every vertex row other than
  A = 630 and 693.
- The vertex/cube "equal numbers of orbits" remark (§5.5, flagged by the draft as not in the ledger).
- The theory statements behind Theorem 6 (a) minimality claims, Proposition 7 beyond the script's output, P̄ and
  Theorem U proofs themselves (I checked the draft's wording against the audits, not the audits' proofs).
- Whether Table 5 omits other ledger-graded forecasts besides #23 (only the PREDICTIONS files named in the draft,
  the exam entry and `exponent.md` were searched).
- Figures (`research/figures/*.png`, `web/docs/*.png`): every path the draft names exists; their content was not examined.
- Prose, structure and the ranking's judgments (not asked).

## Update of 2026-11-15

By a subagent bringing the draft up to date with the results recorded after it was written (draft 2). Base: commit
98a66d8. Sources: `research/CLAIMS.md` rows CN1, GP10, SH2, SH6–SH9, TH1–TH6, ZL1, ZL2 and the notebook entries
"is there one asymptotic cost per cell?" with its addendum, "empty patches on a face too large to die: the forecast
missed …", "a forecast before the run: empty patches …", "the second variable at equal shortest loop: not found",
"lives that settle and are not recognised", "the thinnest face".

**What changed in the draft** (words by `wc -w`; the draft grew from 18,662 to 20,527, +1,865, of which about
+1,350 are words containing letters and the rest numbers and symbols).

- *Abstract*: the equal-loop differences (SH6–SH9), the range 0.207–0.219 (CN1), the thin face's 0.099 (TH3); one
  sentence on unbounded GPU runs (ZL2).
- *§5.2*: † on Table 2 at A = 108, 135 with the ZL2 bounds at A = 63, 84; GP7/GP8 comparisons marked; pointer to §7.5.
- *§5.5*: † on Table 3's GPU rows at A = 759 (1,057-death run, R = 44) and 828; R43 s501 bound marked preliminary.
- *§5.6, Table 5*: rows 15 (SH9, five candidates, refuted) and 16 (GP10 forecast, missed as stated); caption names
  `research/shape3/PREDICTIONS.md` (the five candidates only) and the notebook forecast entry as searched, and
  `research/constant/PREDICTIONS.md` as not searched (its part A, for the patches, is scored in the notebook as
  low by 1.3, 2.6, 4.1 in −ln P and is not in the table).
- *§6*: a bullet for the thin face (TH4).
- *§7.1*: † on Table 6 (s = 5 at A ≥ 90, s = 6, and s = 4 at A = 84, see below); pointer to §7.5.
- *§7.2*: SH2 shortened; SH6, SH7 (difference gone at A = 72, opposite sign at A = 36), SH8 (proved identity),
  SH9 (five candidates refuted), and the commensurability reading as a conjecture.
- *§7.3*: Table 8 caption says the loop² 3 entries are local slopes (TH1); the superseded "Two consequences" of
  the reading (±0.004, "nothing connecting the two", "within reach of a transfer-matrix calculation") cut.
- *§7.4 (new)*: the thinnest face, TH1–TH6; TH5's 22%/11%/5.6% marked preliminary (C); the retracted ± 0.004 stated
  as such, since its retraction is the finding.
- *§7.5 (new)*: CN1 with the addendum's split; the two refuted wrap-around laws; the disputed deciding
  measurements; GP10 with its failed forecast, post hoc second differences, and the unresolved 4×5 cross-check.
- *§10.3*: items 2 and 3 rewritten. *§11*: shape row (five candidates; no variable found); ranking unchanged, with
  the reason, and item 1's and 2's "missing" updated; the shape paragraph says why it stays outside.
- *§12*: trap (i)'s "none has been seen" (now false) cut; a "threat to validity" paragraph for ZL1 and ZL2.
- Header: draft 2.

**Number check.** `python3 docs/paper/check_numbers.py` lists every number in each changed passage (22 passages)
and looks for it as a token in the ledger rows and notebook entries the passage cites. Result: 248 distinct numbers
per passage; 242 in the cited sources; 6 only in the earlier draft (43, 96, 16, 0.2191, and the section number 7.4
twice; sizes and values the passage refers back to); 0 unsourced. During the edit it found nothing to fix; one
number was chosen against the ledger on purpose: the octahedral slope 84 → 108 is written 0.2181 ± 0.0013 (the
notebook's lead check, Table 2, and the arithmetic (23.3761 − 18.1407)/24 = 0.21814) where CN1 and the notebook's
"measured" bullet print 0.2182 (see FOR-LEAD). Negative control: on a copy with 0.0993 → 0.0995, 0.2179 → 0.2178
and one 6.7 × 10⁻³ → 6.9 × 10⁻³, the script reports all three UNSOURCED. **What the script does not check**: that
a number is attached to the right quantity (a token match only), and signs (the notebook's d is a difference whose
sign I checked by eye against the notebook table for SH6 and SH7). I read each new passage against its row and
entry once for pairing.

**Could not source from the ledger or notebook.**
- The run list behind † in Tables 3 and 6 (which slabs are "five of the wider slabs"; that R43 s501 is Table 3's
  longer run of 21.889 ± 0.012) comes from `research/gpu/README.md`, "Zombie lives", which ZL2 cites as "where".
- Table 6's s = 4 run at A = 84 (fwslab 4×7×8) is in neither ZL2 nor that README's table; `python3
  research/gpu/zombies.py` prints "no age bins in this file" for it, so the draft marks it † on that basis.
- "the vertex-centred GPU rows by about 2 × 10⁻³" was drafted and then cut: the README gives 2.1 × 10⁻³ at R38 where
  ledger and notebook say "≤ 2 × 10⁻³" (FOR-LEAD).
- Not checked: any run; the GPU README's bounds other than by running `zombies.py` once (output not compared line by
  line); the claims' underlying reviews.

*Follow-up, 2026-11-15, after the lead applied the FOR-LEAD items (CLAIMS CN1, ZL2, GP10 changed; TH7, CN2 added;
notebook entry "corrections found while the manuscript draft was brought up to date").* Draft: Table 5 rows 17 (TH7,
B) and 18 (CN2, flagged unverified, grade C) and its caption; GP10's 4 × 5 grade now B− in §7.5 and row 16; the
fwslab 4×7×8 note in Table 6 and §12 now cites ZL2 rather than `zombies.py` (the "could not source" item above on it
is resolved); CN1's 0.2181 already matched. The draft does not state the ledger's size, so nothing changed for it.
`python3 docs/paper/check_numbers.py` (now 24 passages): 270 numbers, 263 in the cited sources, 7 only in the
earlier draft, 0 unsourced.

## Update of 2026-11-15 (second): the symmetric collapse and the new clocks

By a subagent, base bb22eda. Sources: CLAIMS S2, S3, S5–S9, Z12, Z13 and the notebook entries "the symmetric
collapse: pairing faces across an edge is what costs" and "what the unrecognised settled states are". Changed:
the header; the abstract (the edge cost, the mirror-line account corrected); §5.5 (the S2 qualification on the
√A coefficient; "Centre matters, but not by a constant factor" with S9, its D2h and O_h parts flagged C; a new
part "Why symmetric faces die sooner" with S5, Table 3a (the edge ladder, both codes), S7, S8, "What this
corrects" and "What remains preliminary"); Table 5 row 19 (the line's forecasts; no ledger row for the tally)
and its caption; §8 (Z12, one sentence); §10.1 (S5); §10.3 item 4; §11's table row and ranking item 3; §12's
threat to validity (Z13, flagged preliminary). `GAPS.md`: items 23 and 37 annotated, items 44–46 added. Draft
20,639 → 22,058 words (`wc -w`). Hedges kept as the notebook states them: "corrected, not reversed", "up to about a
third … is not excluded", "a coincidence of ranges, not a test", "exactly c/6 is not shown", the mechanism a
conjecture. **Number check:** `python3 docs/paper/check_numbers.py` now covers 41 passages (17 new, compared with
the draft at bb22eda): 437 numbers, 419 in the cited sources, 18 only in the earlier draft, 0 unsourced. Negative
control on a copy (9.291 → 9.219 in Table 3a, 0.2035 → 0.2053 in S8, a period 13 → 137 in Z12): all three
UNSOURCED; a changed number that happens to occur elsewhere in the cited entry (13 → 31) or in the earlier draft
(13 → 61) is not caught, the known limit of a token match. Removed while checking: S7's "2.6σ apart" for the rerun
slab pair, which the review attaches to a different comparison (FOR-LEAD, second update, item 1). Not checked:
any run; the review itself; that each number is attached to the right quantity beyond one reading of each passage
against its row and entry.

## Update of 2026-11-15 (third): after the audit of the rows nobody had re-run

Base e126a10. Sources: `research/CLAIMS.md` as changed by 13f8732 (133 claims: A 56, B 66, C 10, D 1,
`python3 research/audit/claims_tally.py`), `research/AUDIT-2026-11-15.md` and the notebook entry "the audit of
the rows nobody had re-run". Every *preliminary* marker and every place the draft names grade C was matched to its
row's level cell as it now stands.

- **Released** (row now B; the sentence says what was repeated): T9's minimality (still within the patch, still
  not claimed beyond it), K1 (fresh seeds), K3, P4 (restated: ξ = 0.65 ± 0.03 cube, Ornstein–Zernike form for
  k ≤ 2.5 per cube, the old 0.68 ± 0.01 explained), P5 (producer's seeds), P6 (the {110} front slows: 0.165 in
  windows ending by generation 80, 0.154 over 60–110), F2 (heights to ±0.03; whole-plateau ratios 0.770, 0.604,
  0.454 given), F10 (producer's seeds), F11 (B (table), with the weighted and unweighted fits), SW3 (§5.5 and the
  Table 5 caption), SW4, G2 (brute-force checks), Z5, Z10, L3 (the post hoc caveat kept), CN2 (Table 5 row 18, the
  "unverified" flag removed), SW7 (Table 5 row 14 now cites its row, which it said did not exist).
- **Narrowed** (part still C): F10/F12 (F12 kept), Z2 (n = 14, 15 released; 16 kept), Z3 (unions 12–13 released;
  the hinge-flip property kept), Z4 (period 4 released; period 3 kept), X3 (fixed point and the censored 6.542 ±
  0.001 released; the uncensored 6.94 kept), G2–G4/SW4 split; §10.1 and its preliminary paragraph follow Z2–Z4.
- **Kept** (row or part still C): F12, S4, Q4, G3, G4, K7/K8 (now named in §9), Z13, S9's D2h and O_h parts, Z12's
  absence from the census lists, TH2 (45, 61 sites), TH5's percentages, ZL2 beyond R11/R13 (§5.5, Table 6, §12),
  C4's wall-clock time, and "volume over group order" (S4) in §11.
- **Legend** (line 11): B now reads as the ledger's ("by someone other than the producer"); the old "from the
  committed data" did not cover F11, S1, C7, L3, rebuilt from raw records that are not in git.
- **Appendix**: its lists were rebuilt from the ledger's level cells; L3 had been listed as "not mentioned" though
  §5.6 cites it. The draft still does not state the ledger's totals.
- **Number check**: 18 passages added to `check_numbers.py` (base e126a10, the audit's notebook entry as source),
  and the Table 5 row 18 marker updated; markers now match across line breaks. Result: 602 numbers, 575 in the
  cited sources, 27 only in the earlier draft, 0 unsourced. Negative control on a copy (0.154 → 0.155 in §4):
  UNSOURCED.

Not checked: any run or fit (this is a text pass against the ledger); the audit's own numbers beyond reading them
against the ledger; `research/figures/phase_spread.png`, which may show the {110} front's old single speed.

## Update of 2026-11-15 (fourth): how a face dies, the 4 × 5 patch rerun, the second card

By a subagent, base 67e0371. Sources: `research/CLAIMS.md` rows DY1–DY7, GP10, GL1, GL2 and the dated notes in SH3
and SH4 (142 claims: A 65, B 66, C 10, D 1, `python3 research/audit/claims_tally.py`, run for this pass); notebook
entries "how a face dies (the first look, reviewed)", "a death is a dip that keeps going", "the 4 × 5 empty patch,
rerun on the CPU", "a second card"; `research/audit/REVIEW-dying.md` (rounds 1 and 2) and
`research/audit/REVIEW-gpu-local-pr23.md`. Draft 22,526 → 24,974 words (`wc -w`).

**Changed.** Header; abstract (one sentence on how a tied face dies, DY1/DY2/DY5); §1 (the cubes' section is now
5.7); §5.5 (S7's "Nobody has looked at the dying faces" replaced by a pointer); **§5.6 new**, "How a face dies"
(DY1–DY7 with grades and what the review did not confirm, the withdrawn readings, the forecasts, not checked; round
3 named as under review, no numbers); the old §5.6 renumbered 5.7; Table 5 rows 20 and 21 and its caption; §7.3
Table 8 (loop² 16, 48 → 60: 0.2125 → 0.2131 ± 0.0002, footnote ‡) and SH4 (census gap 0.0135–0.0138, the
χ² 4.4 tension and the pooled 0.0108 ± 0.0017 removed as resting on the high draw); §7.5 (equilateral forecasts and
CN1 rest on the old anchor; GP10 rewritten: CPU −23.412 ± 0.049 on 541 hits, combined −23.364 ± 0.034, cost
0.226 ± 0.006 combined, "falling into the range" withdrawn, grade A to 4 × 5); §9 (twice 0.2072–0.2131 is
0.414–0.426: arithmetic, 2 × 0.2131 = 0.4262); §10.3 item 4 (also its pointer for the side-16 plateaus, which said Section 5.5 and now says 5.7); §11
ranking items 1 and 3; §12 (the second card in
"Implementations"; new paragraphs "A guard, and its limit" (GL2) and "Errors of the census pipeline" (GL1);
"Verification" gives the ledger counts). `GAPS.md`: header; items 2, 11, 14, 24, 41, 42, 43 (closed as a
cross-check), 45 annotated; 48 and 49 added.

**Checked against files, not notebook prose.**
- GP10: `python3 research/audit/gpu_pr18/followup.py research/scratch/pr18 research/data/gpu_patches/patches_s81*_A10G.csv`
  run for this pass (scratch runs present): 18 runs, 2.76 × 10¹⁰ replica-generations, 4×5 pool −23.4124 ± 0.0485
  (541 hits) against GPU −23.3180 ± 0.0473, z −1.39; second differences 2x3 3x4 4x5 CPU 0.2349 ± 0.0082, GPU
  0.2185 ± 0.0079. Combined by inverse variance (my arithmetic): −23.363 ± 0.034 and 0.2264 ± 0.0057.
- GL1: ln(2 × 76,418,398,524 / 7,478,823) = 9.92505, error 1/√F = 0.00037; pooling 9.9246 ± 0.0006, 9.9251 ± 0.0004,
  9.9240 ± 0.0014 gives 9.92490 ± 0.00032. Census values from `research/shape2/data/A48.csv` (ln(2E/F) recomputed for
  every class: 4 0 4 → 9.93237, 1 6 16 → 9.93842) and `research/shape2/data/explore_report.txt` (loop² 16, A = 60:
  12.4818 ± 0.0025). Slope (12.4818 − 9.9249)/12 = 0.21308, error √(0.0025² + 0.0003²)/12 = 0.0002; the file's
  0.2125 is (12.4818 − 9.9324)/12. Census gap 0.0135 against 9.9249, 0.0138 against 9.9246 (FOR-LEAD item 1). The
  A = 48 span of the loop² 12–16 classes (0.016 in the draft, 0.0147 from the file) does not involve the 4 × 4
  value either way and was left as written.
- DY1–DY7: every number in §5.6 against its ledger row and the two notebook entries; the review numbers the rows
  quote against `research/audit/dying/ana_out.txt` and `ana2_out.txt` (lag-4 ratios, neighbour rows, tail slopes);
  the round-1 forecast outcomes against `research/dying/README.md` (L5a 0.893).
- Counts: `claims_tally.py` output as above.

**Number check.** `docs/paper/check_numbers.py` now covers 22 more passages (base 67e0371, the commit before this
pass; the existing GP10 passage also cites the rerun entry) and may cite a tracked file directly (`file:PATH`; used for `explore_report.txt`, the dying README and the
pr23 review). Result: 851 numbers, 809 in the cited sources, 42 only in the earlier draft, 0 unsourced. Among the
"earlier draft only": the §7.5 shifts (0.005, 0.010, 0.0003, 0.0004), which are in the pr23 review but also occur
elsewhere in the old draft, and the ledger counts (142, 65, 66, 10, 1), which have no source file and were checked by
running the tally. Negative control on a copy (0.298 → 0.289 in DY2, 0.226 → 0.227 in GP10, Table 8's 0.2131 →
0.2137): all three UNSOURCED (the Table 8 row needed its own passage, added). Two numbers were reworded to match
their sources (0.9992 → "99.92% of the time"; neighbour 0.89 → 0.893).

Not checked: any run other than `followup.py`; the reviews' own code; the 0.414–0.426 range has no passage in the
script (arithmetic above); that each number is attached to the right quantity beyond one reading of each passage
against its row and entry; the overview (`docs/overview/`), which another editor is changing.

## Update of 2026-11-15 (fifth): dying rounds 3 and 4, the wrapped faces on the second card, signals, the state space

By a subagent, base a8e925a. Sources: `research/CLAIMS.md` rows DY5 (revised), DY8–DY15, GL1–GL3, SG1–SG10, SS1–SS3
and the dated notes in SH3, SH4, CN1 (164 claims: A 78, B 75, C 10, D 1, `python3 research/audit/claims_tally.py`,
run for this pass); notebook entries of 2026-11-15 "what the dips say about the price of a cell", "a depleted face
thins as one thing", "round 4 reviewed", "the 93-cell torus lands below every reading", "five wrapped faces on one
driver", "the five tori, reviewed", "gump carries signals", "the first signals push reviewed", "a clock of every
length …", "the second signals push reviewed", "how much of its state space a seed explores", "the state-space study
reviewed"; `research/signals/README.md` (§§4, 8–14), `research/audit/REVIEW-signals.md` and `REVIEW-signals-2.md`
(verdict tables, §1), `research/constant/PREDICTIONS.md` part C with its dated blocks, `research/signals/PREDICTIONS.md`
(scores), `research/OPEN-PROBLEMS.md` 12–13. Draft 24,974 → 32,313 words (`wc -w`).

**Changed.** Header. Abstract: the "0.207 to 0.219" sentence replaced by the wrapped-face line (0.2084 from 63 cells,
a kink near 61, hull slopes 0.2119–0.2181 moving away, one price or two open); one sentence on signals (pulses,
transmission to a counter, inhibition element measured; the clock and the tape proved). §1: one sentence each; the
proved and measured lists. §5.5 (S8): "c is only known to 0.207–0.219" replaced. §5.6: intro grades; DY5 tail
(0.51–0.48 over 3–12 cells, 0.34 by 17–20); **round 3** (DY8–DY11) and **round 4** (DY13–DY15) added, with "no remnant
at fixed density" withdrawn after the review's null, the construction's overshoot 1.07, 1.21, 1.34 nats, what a
caught face is and is not, forecasts and not-checked. Table 5: row 18 points to row 24; rows 22–27 (dying rounds 3
and 4; part C; N1–N4; S1–S10; E1–E7); caption's sources and not-searched list. **§6.1 new** (SS1–SS3; the deficit
against coin flips and its bearing on §6). §7.1: pointer to 0.2084. §7.3: Table 8 caption, the 16-generation stamping
(GL3) in place of "a tie-resolution bias of about −0.018"; SH4 gap 0.0135 ± 0.0020. **§7.5 rewritten** after the CN1
paragraphs: CN1 dated; Table 8a (five tori, second codes, grades; 93 cells *preliminary*, C); the line and the kink
(GL3, B); against the hull family; part C scored; the old "two measurements proposed" paragraph removed (the tori
are made; the A = 108 hull run is still not). §8: Z10's "no object carries a signal" scoped to the censuses. **§8.1
new**, Signals (SG1–SG10; Theorems 8 and 9 with outlines and where the full proofs are; the two README §4 remarks
marked "no ledger row"; the reviews' corrections: the receiver's capacity d − 1, three layers not two, one random unit
repeated not soup, fire speed depends on density; absent inside bounds; open). §10.1: Theorems 8, 9, the remarks,
SS1's seventeen vessels; the ignition as not proved. §10.3: item 2 rewritten (one price or two), item 7 (open
problem 12 answered; the new open items), items 9 and 10 new. §11: two table rows (signals, state space: **not
searched**); ranking item 1; a paragraph saying why signals and state space are not ranked. §12: the second card
(five tori; the 5 × 5 repeat of a GP9 value), the oracle-judged verifiers and the enumerator, the census's stamping
bias (GL3), the guard used once (93 cells), the counts 164 / 78 / 75 / 10 / 1, the reviews named, "not repeated".
Appendix: GL3 (93 cells) and SS2 (side 16) as C parts; the new rows all used. `GAPS.md`: 42, 46, 48 annotated; 50–55
added. `FOR-LEAD.md`: fifth section, 11 items.

**Checked against files, not only notebook prose.**
- Part C of `research/constant/PREDICTIONS.md`: the three readings' constants (flat 0.21214, massive 0.2069 ± 0.0023,
  rising c_h 0.2226, 0.2317), the A = 93 forecasts and refutation lines (19.479 ± 0.010 below 19.445; 19.506–19.530
  below 19.488; 19.437 ± 0.019), the shortest loops of Table 8a (4.00, 4.36, 4.58, 5.00, 5.57) and which tori have
  no cut; the dated scoring blocks ("no reading of part C survives"; N1, N4 failed, N2 held, N3 open).
- Side 16's state count against `research/data/cube16_summary.json`: cycle_start 2,919,617,675, period 1,
  detected 2,919,617,676, so 2,919,617,676 states; consistent with SS2 and Table 1.
- `research/signals/README.md` §11 for the proof outline (B1–B5, m = 4, base 8, bases 12 and 20, j ≤ 40 enumerated,
  j ≤ 6 stepped), §10 for the tape argument and the gate's logic table, §4 for the two remarks;
  `REVIEW-signals-2.md` §1 for the light cone and what the review re-derived; `REVIEW-signals.md` verdict table for
  the remarks (corollary 1 incomplete as first written; corollary 2 valid; pulse S's O1 count 2 or 9).
- The ledger's SG row "where" cells against the README's headings (FOR-LEAD item 7).
- The 15.6614 "on file" against GP9 and the notebook's 2026-11-14 shape entry: a GPU value (FOR-LEAD item 4).
- Counts: `claims_tally.py` output as above.

**Number check.** `docs/paper/check_numbers.py` covers 70 more passages (base a8e925a) under twelve new notebook keys
(each keyed by date and heading, so that a mention of a heading inside another entry is not matched); three
passages removed with their text (the old §7.5 equilateral note, the old "second card" and "142 claims" sentences);
three earlier passages given the new sources their text now needs (the abstract's shape sentence, §5.5 S8, §12
census errors). Result: 1,538 numbers, 1,469 in the cited sources, 69 only in an earlier draft, 0 unsourced.
Negative control on a copy (Table 8a 13.1622 → 13.1623; SS3 0.9585 → 0.9586; SG8 12,780 → 12,781; DY14 1.21 → 1.22):
the first three UNSOURCED; the fourth passes as "in the earlier draft only", because 1.22 occurs in the earlier
draft (Table 5 row 20, "1.06–1.22"). That fallback is a known weakness of the script: a changed number that happens
to occur anywhere in the earlier draft is not caught. `check_face_area.py` run: every A as before.

Not confirmed against the record: the round-3 tally "three of eighteen" (it requires L1 not to be counted; FOR-LEAD
item 11); the lead's conjecture about the kink with the remnant's width (FOR-LEAD item 5; stated without the number);
that the five tori used soup 0.4 and 8 layers is taken from part C's protocol and GL1/GL3, not from the card's rows
(not fetched: the branch is not merged and was not read); nothing was run but the two scripts, the tally and a JSON
read; the reviews' and the study's code were not run; the overview (`docs/overview/`), which another agent is
changing, was not looked at. The third signals push, running, is not described anywhere in the draft.
