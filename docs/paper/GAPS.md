# What an expert referee would ask for that the repository cannot presently supply

2026-11-14, written with `draft.md`. Ordered by how much each gap limits what the paper can claim. "Supply" means:
present in the repository as a checked result, a tracked data file or a runnable command.
Updated 2026-11-15 with draft 2: gaps 2, 22 and 25 revised, 39–43 added (section 7).

## 1. Theory

1. **A proof of the area law for anything run by the rule.** None exists for gump, for the 2D analogue in a
   vessel, or for the finite-depth noise-driven models. The two conditional results (draft §10.2) do not close it:
   (a) rests on hypothesis (R), known only from sampled tables at A = 30–84, with a margin of 0.003 at A = 30;
   (b) is about a constructed automaton fed by a random tape.
2. **A derivation, or even a definition, of the constant.** A referee will ask "0.21 of what?". The repository
   has: 0.2072–0.2125 on periodic faces depending on the family, 0.2146–0.221 and rising on octahedral faces,
   no measurement of a flat face without wrap-around or rim, and no demonstration that a limit exists.
   *Update 2026-11-15:* a joint analysis (CN1, draft §7.5) shows the families allow one asymptotic constant
   anywhere from about 0.207 to 0.219 and do not fix it; the measurement is now gap 42. The derivation is still
   missing.
3. **The two percolation statements under §10.2(b) at the source.** Balister–Bollobás–Stacey 1994 is known
   second-hand; Liggett 1995 by its abstract and a secondary quotation; the proof of Hartarsky–Szabó Cor. 4.8 is
   a sketch in the paper as read.
4. **A second reader for the "counting" line** of the theory effort (its audit was started on 2026-11-14 and is
   not in the tree this draft was written from), and any human reader for any proof. Every proof here was
   written, checked and re-derived by automated agents; the audits are careful and used independent code, but a
   mathematician has not read Theorems 5 and 6, the twist lemma, or the conditional theorems.
5. **Prior art for the hazard identity** (entry flux × committor). The library has nothing on transition-path
   theory or committor identities; the draft carries a `[citation needed]`. *Update 2026-11-14:* the Markov
   quasi-stationary flux identity 1/τ = Σ W_r π_r is now cited (Assaf–Meerson 2017, eq. 6, §2 read); the committor
   and transition-path part is still unsearched and keeps its `[citation needed]`.

## 2. Literature

6. **The supertransient literature has not been read.** Tél–Lai 2008 (the review), Crutchfield–Kaneko 1988
   (abstract only), Kaneko 1990, Wackerbauer–Showalter 2003: not obtained. The draft's claims that "area of a
   boundary face, not volume" and "the bulk can be replaced by noise" are new within that literature rest on the
   absence of evidence in the few sources opened. A person with library access must read these before any
   novelty claim.
   *Update 2026-11-14 (third pass and its adversarial review, `research/PRIOR-ART.md`; shelf §§10–11).* Obtained
   since: Houghton et al. 2010 in full; Carretero-González et al. 1999 in full (noise at the edges of a window, the
   mirror of the draft's §6) and its citing works as titles; Sugimura–Kori 2015, Nemoto–Alexakis 2021 and
   Assaf–Meerson 2017 in the parts named on the shelf (the tail formula, now presented as known); Vidmar–Rappel
   2019 in its relevant sections and Rappel et al. 2022 in full (boundary-controlled death, now presented as
   known); Caselle–Gliozzi–Vinti 1993 in full and Nardi–Zocca in §§1–2 (shape of a torus in equilibrium; the
   shortest loop as controlling length is a theorem there). Abstract only: dos Santos et al. 2008 (as paraphrased by
   a fetch tool), Mikkelsen–van Hecke–Bohr, Goldenfeld et al. 2010, Lilienkamp et al. 2017, Tuckett et al. 2019,
   Neuhaus–Hager 2003. Still not obtained: Tél–Lai 2008 (author copy, HTTP 503 three times), Tél 2015, Crutchfield–
   Kaneko 1988 beyond its abstract, Kaneko 1990, Wackerbauer–Showalter 2003, a 2007 Wackerbauer paper on noise and
   the collapse of spatiotemporal chaos (search result only), Nåsell 2011 (Springer login), Lilienkamp et al. full
   text, Nemoto–Alexakis 2018, Lüscher–Symanzik–Weisz 1980, Leung–Zia 1990, the citation lists of Houghton et al.
   and Sugimura–Kori (citation index refused). Not searched: pipe-flow puff lifetime against pipe length;
   Kuramoto–Sivashinsky lifetimes; Gray–Scott beyond Wackerbauer–Showalter; anisotropic-Ising and in-field
   nucleation on rectangular tori (Borgs–Chayes–Tetali 2012 is the next lead); quantum-memory lifetime reviews;
   emptiness formation; non-English literature. The "not found" statements of draft §11 for the boundary layer over
   noise and for fixed-area shape of a chaotic transient survive two searches, one adversarial, and no more.
7. **Eppstein's paper was read once and could not be re-read.** Whether its bounding-diamond argument is the same
   method as Theorem 2, and what it says about shrinking hulls, is unverified (OPEN-PROBLEMS 16).
7a. **Sealed sets and firewalls: the classical sources are known but partly unread.** Since 2026-11-14 the draft
   presents the largest dead sealed set as a 9-core / the complement of a threshold-4 bootstrap closure (Miller 2016,
   k-core and bootstrap sections read) and the firewall as a blocking word (Blanchard–Tisseur 2000, §§1, 2.2 read;
   Bollobás–Smith–Uzzell 2015, §1 read). Not obtained: Kůrka 1997 (not attempted), the Gamber (Burkhead) thesis on
   d-dimensional blocking patterns (aggregator copy only), Gravner–Griffeath's own papers on the subcritical class
   (known through Bollobás–Smith–Uzzell); abstract only: Sablik–Theyssier 2011, Audouard–Theyssier, Goles et al. on
   freezing automata, Salo–Theyssier–Törmä, Balister–Bollobás–Przykucki–Smith. The reviewer's reading of Theorem 6
   as "not subcritical" in Gravner–Griffeath's sense is not checked. Not searched: Boolean-network frozen cores and
   trap spaces (a probable further home for sealed sets).
8. **Goles–Olivos 1980/81 and Goles–Fogelman-Soulié–Pellegrin 1985 are unread**; the transient bound 26N + 1 has
   not been compared with theirs; whether energy identities with a drive term for capped rules are known is not
   checked.
9. **Citation data are incomplete** for items PRIOR-ART records only by arXiv number or surname (arXiv:1510.05924,
   arXiv:1809.03266, Reia–Kinouchi, Guttesen, Buca et al.), and the crystallographic statement that perovskite
   anion {111} layers are kagome is unsourced. Nothing in the reference list has been checked by a person.
10. **No search of the physics literature on dynamics on the ReO₃ anion / Cu₃Au lattice** beyond web search
   (PRIOR-ART says so).

## 3. Measurements a referee would want and that do not exist

11. **A second implementation at A ≥ 108.** Table 2's last two rows, the firewall-resolved slabs at A ≥ 90
    (except one pair at A = 72) and the symmetric rows at A ≥ 759 come from one GPU code path on one provider,
    checked by CPU emulation only. No second GPU run, no CPU run at those sizes.
12. **More than 16 deaths at A = 135**, with replica ages reaching only 1/900 of the mean lifetime; the
    exponential-wait assumption is doing the work there.
13. **A chaos diagnostic.** No Lyapunov exponent or entropy rate. Damage spreading (P5), correlation length (P4)
    and front speeds (P6) are grade B since the audit of 2026-11-15, but only one size (N = 64) was examined:
    P5 and P6 were re-run on the producer's own seeds, which checks code and transcription, not the statistics;
    ξ = 0.65 ± 0.03 rests on the window where the Ornstein–Zernike form fits (k ≤ 2.5 per cube; windows from
    k ≤ 1.5 to 2.5 give 0.61–0.69), and anisotropy at larger k was not looked at. The {110} front slows (0.165 early, 0.154 over generations 60–110) and nobody has
    asked why or where it ends.
14. **Independence of the faces of one vessel.** τ_face = 8 × (mean first wait) assumes it. The 0.84–0.91 excess
    of octahedral over periodic faces at A = 108 says faces of an octahedron are not simply eight slab faces;
    no joint statistics (which face dies, correlations between adjacent faces' populations) are recorded. On
    another lattice (grade C) adjacent walls hold each other up by a factor 10⁶.
15. **What makes an octahedral face tougher**: rim, shared edges, interior thickness and shape are not separated.
    No vessel with a flat face and open (non-periodic, non-octahedral) boundary has been run.
16. **Thickness dependence at large area.** Independence of m is measured at A = 48 only (m = 7–12); all slabs at
    A ≥ 90 have m = 8.
17. **Dependence on the initial density and on T₀** beyond R = 11 (densities 0.3–0.6, not a ledger row) and the
    checks listed in the reviews.
18. **Relaxation time against extinction time.** "Quasi-stationary" is asserted from flat hazards; no
    measurement of the time to reach the quasi-stationary law, and so no stated separation of scales, except
    informally (correlations gone by ~20 generations).
19. **Rule-space survey robustness.** One vessel radius (10), 16 soups per rule, cap 10⁵, table re-derived but
    the survey not re-run (Q1 is "B (table)").
20. **The side-16 run is a single trajectory that nobody repeated** (days of CPU); its event log is tracked and
    its schedule re-derived from it, which is not a replication. Side 17 is forecast, not run.
21. **Stability in infinite volume.** Whole-torus lifetimes exist for N ≤ 5 only (none of 512 ended at N = 6–8
    within 10⁶); no scaling statement can be made.
22. ~~**The second shape variable**~~ *Closed as a search, 2026-11-15* (SH6–SH9, draft §7.2): the equal-loop
    difference is zero within error at A = 72, of the opposite sign at A = 36, five committed candidates are
    refuted, and one number fixes the lattice at equal area and shortest loop (proved). What remains: the
    commensurability reading is a conjecture, tested only by equal-loop pairs at A = 84 (two exist with
    loop² ≥ 12), which have not been run; Q54, Q63, P3, N72 and two of the triple tori were not rerun by a second
    code; the 2σ age hint on the A = 60 loop² 16 pair was not retested (that pair was not rerun); the per-job
    counts of unrecognised settled lives on (1,3,12) are overdispersed and unexplained.
23. **Asymmetric faces with one mirror, the "lockstep" rule for general groups, the thickness transition, the
    firewall cost per cell**: all grade C when this was written. *Update after the audit of 2026-11-15:* the
    thickness transition (K1) is now B on fresh seeds; the one-mirror faces (SW3) are B on the examiner's own seed
    sequence, with no second code; the firewall cost (F11) is B (table), rebuilt from raw slab records that are not
    in git, with a weighting the claim did not state. The lockstep rule for general groups (S4) is still C. The
    symmetry story in the draft rests on O_h only.
    *Update 2026-11-15 (second):* the edge ladder in one octahedral vessel at A = 63 (S6, two codes) and the slab
    faces with a mirror or threefold axis (S7, one pair rerun) now cover subgroups of O_h; everything beyond A = 63
    there rests on one code, one job and one seed per size (gap 44).

## 4. Statistics and method

24. **Systematic errors are not budgeted.** Quoted errors are 1/√deaths. Known systematics (tie conventions,
    detection-time bias, the soup transient, censoring of settled replicas, cycles longer than the detection
    windows) are bounded case by case in reviews, not propagated into the tables.
25. ~~**Undetected long cycles.**~~ *Found and partly bounded, 2026-11-15* (ZL1, ZL2; draft §12): such cycles
    exist (period 16 on a CPU-missed state, periods 9–52 seen), every capped CPU run is bounded below its errors,
    and the long GPU runs are bounded by deaths at old ages. What remains is gap 41.
26. **Post hoc statistics.** The "cubes outlive their ensembles" count (C6) was chosen after the data; several
    fits in §7 are post hoc and are marked so in their sources. A referee would ask for the pre-registered
    analysis plan for each table; it exists for some (Table 5) and not for others (the width families' two
    competing fits).
27. **Random number generation.** The generators and seeding of each stepper are in the code but not described
    in one place; one seed-collision bug was found and fixed in the GPU driver (documented in
    `research/gpu/README.md`), which a referee will want stated with the check that excludes others.
28. **Multiple estimates of one number are not pooled by rule.** E.g. four values of ln τ_face at A = 84
    (INCONSISTENCIES A2). The draft picks the most precise; a paper needs a stated rule.

## 5. Reproducibility and presentation

29. **Bulk data are not tracked.** Scripts that need untracked scratch output include
    `research/fluct/analyze_qsd.py` (the QSD tallies behind §5.3), `research/experiments/census_twist.py` (the
    9,700-object census), `research/experiments/cube_vs_ensemble.py`, `research/phase/sk.py`. The GPU
    experiments need a commercial GPU service to re-run. A data deposit would be needed.
30. **Figures.** No figure exists for anything measured after 2026-11-13: octahedral faces beyond A = 84, the
    width families, the twisted tori, the census, the symmetric table, the forecast scorecard, the neighbourhood,
    P66.27a. `research/figures/peel_face_law.png` predates the corrections and plots symmetric faces at a
    rescaled area the draft does not use. The draft marks five placeholders.
31. **Length.** The draft is about 15,000 words, well over an 18-page paper. Sections 8 and 9 and Table 5 are
    the natural cuts; or the material splits into the three papers suggested in `research/theory/PROGRAM.md`
    ("Writing it up").
32. **Terminology** ("soup", "peel", "firewall", "vessel", "ash") is the project's own and is only partly
    defined in the draft.
33. **Authorship, disclosure of automated work, licence and venue** are the owner's decisions and are blank.

## 6. Things the draft says that a referee could attack

34. "Chaotic" is used without a quantitative definition (see 13).
35. "A new instance of a known phenomenon" for the area law depends entirely on gap 6. Since 2026-11-14 two parts
    once offered as possibly new are presented as instances of known results (the tail formula; death through the
    boundary); the remaining "not found" statements are only as strong as the searches in gap 6.
36. The claim that the exponent is "made in a boundary layer" is established to 0.015 in ln τ only for periodic
    faces at A ≤ 75; for octahedral faces there is a 4–5σ offset of 0.03–0.04, and the adequate depth was chosen
    after seeing the data.
37. The symmetric fit with slope 0.209/6 uses a periodic-face slope that §7 says is inflated by mixed widths;
    the fit is offered as a description, but its motivation ("six images") would need the right asymmetric
    slope, which is not known. *Update 2026-11-15 (second):* the review of the symmetric-collapse line shows how much this
    matters: the fitted √A coefficient moves by −8.1 per unit of the assumed slope (−0.127 with 0.2035), so it is
    not evidence for any account of the √A term (draft §5.5).
38. The ranking in §11 is a judgment by the draft's writer, not a result.

## 7. Opened by the results of 2026-11-14 and 2026-11-15 (draft 2)

39. **The limit of the thin face's cost per cell** (TH1–TH3, draft §7.4). About 0.099, but 0.093–0.107 is a
    spread of correction forms, not a confidence interval, and a √b form that would allow 0.08 is excluded only by
    the review's rings. Wanted: rings well beyond b = 36 (A = 108) with an independent stepper, and the segments of
    45 and 61 sites and the rings at b = 20 and 36 rerun (grade C or not rerun now); a stated rule for which
    correction forms are admissible.
40. **What sets the ratio of thin to wide** (about 0.099 against about 0.21 per cell). No derivation: the exactly
    solvable one-layer closure is 22% off (grade C, as are the two better closures at 11% and 5.6%), noise is
    enough only from five layers, and the face dies by fronts. A referee would want either a computed front
    large-deviation rate or a statement that the ratio is not expected to be simple.
41. **The GPU runs with no bound on unrecognised settled replicas** (ZL2, draft §12, marked † in Tables 2, 3, 6):
    octahedral A = 108 and 135, symmetric R43 s201, R44, R45, slabs 6×6×8 and 6×7×8, fwslab 5×6, 5×7, 5×8, 6×6,
    6×7 (×8), and fwslab 4×7×8 (A = 84), whose log has no age bins and which ZL2 does not list. Their correctness
    rests on the rate not rising with size (conjecture). Wanted: the guard described in `research/gpu/AGENT.md`
    (doubling snapshots, or an age cap) and a rerun of at least A = 108, or a second implementation at those sizes
    (gap 11). The bounds other than R11 and R13 are grade C (the GPU session's script, re-run, not re-derived);
    the audit of 2026-11-15 found fwslab 4×9×8 bounded by 4.2 × 10⁻³, which the ledger had left out of its
    summary.
42. **The asymptotic constant, and the measurements that would decide it** (CN1, draft §7.5). Proposed and not
    made: the octahedral face at A = 108 with 10⁴ deaths (about 4 GPU-hours), which the analysis says would
    eliminate 35 of 36 single-constant readings if its value holds and the review calls not decisive; equilateral
    periodic tori (single-constant forecast: local slopes 0.2117 → 0.2136, with the existing 6×6 run already
    2.7–3.2σ below); octahedral faces of equal area with different rims, only with matched corners. Both GPU
    measurements need the guard of gap 41 first. A flat face with neither wrap-around nor rim is still unmeasured.
43. **The empty-patch cross-check** (GP10, draft §7.5). The last perimeter-free cost per cell (0.2185 ± 0.008)
    rests on the 4×5 point, which the independent CPU run puts 1.9–2.6σ lower; a ten-times-longer CPU run is in
    progress. Not checked at all: dependence on slab thickness, density and face size, and whether a 12×12 face is
    in the same state as a small dying one.
44. **The symmetric collapse beyond A = 63** (S6–S9, draft §5.5, second update of 2026-11-15). The edge ladder
    (about 2.15 in ln τ per tied edge) is measured in one vessel at one size by two codes; nothing beyond A = 63
    was rerun by the review, and each T, T_d and O_h number is one job with one seed. Open: whether slope × order
    is exactly c (0.2091 for T, 0.2035 for T_d, "within 5%"); whether the rim term bends, so whether −0.196·√A is
    asymptotic at all (the fall in marginal cost rests on the two smallest sizes); a T_d ensemble at A = 759 would
    speak to it (forecasts 26.2–26.4 if linear, 25.65 ± 0.25 otherwise, only 1.9σ apart) and needs a GPU and the
    guard of gap 41. Unexplained in the line's data: group O far below T_h, T_d's two sub-series moving apart,
    mirror strips two cells wide keeping a slope of 0.186.
45. **The mechanism of the edge cost, and the mirror share.** That faces tied across an edge cannot hold each other
    up is a conjecture: no occupancy maps of dying tied faces exist. In a fully symmetric face rim and mirror cannot
    be separated, and a diagonal-mirror share of up to about a third of the √A term is not excluded. Wanted: the
    maps, and a construction that separates a tied rim from a diagonal mirror.
46. **Wires and sheets** (Z13, grade C, draft §12). Of 37 unrecognised settled states, 21 were classified as wires
    and 2 as sheets by one agent; whether a wire's moving part could be held by a finite stator, whether wires of
    one period and direction are the same wire, and sheets on covers beyond 3 × 3 were not checked. The five new
    finite clocks (Z12) have no stability or basin measurements.
47. **Window choices the claims did not record** (audit of 2026-11-15). F2's plateau heights move by about 0.03
    with the averaging window (0.770, 0.604, 0.454 over whole plateaus against the quoted 0.79, 0.61, 0.48); P6's
    {110} speed depends on where the fit window ends; F11's coefficients need a weighting by firewall-first counts.
    A referee would want each analysis committed as a script with its window. Still with no re-run at all: F12
    (the plunge before death; its inputs are not in the repository), S4, Q4, G3, G4, K5, K7, K8, Z13, Z2 at
    n = 16 and Z4's period-3 search; L2 has only been recomputed from its committed tables.
