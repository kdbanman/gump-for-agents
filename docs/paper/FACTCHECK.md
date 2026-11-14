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
- **Appendix**: superseded rows F7, S1, F9's limit, GP4 match the ledger's four; C-graded list matches the ledger.

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
