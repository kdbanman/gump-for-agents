# What an expert referee would ask for that the repository cannot presently supply

2026-11-14, written with `draft.md`. Ordered by how much each gap limits what the paper can claim. "Supply" means:
present in the repository as a checked result, a tracked data file or a runnable command.
Updated 2026-11-15 with draft 2: gaps 2, 22 and 25 revised, 39–43 added (section 7). Updated again 2026-11-15
(how a face dies, the 4 × 5 patch rerun, the second card): gaps 11, 14, 24, 41–43 and 45 annotated, 48 and 49 added.
Updated a third time 2026-11-15 (dying rounds 3 and 4, the wrapped faces on the second card, signals, the state
space; draft §§5.6, 6.1, 7.5, 8.1): gaps 42, 46 and 48 annotated, 50–55 added (section 8).

## 1. Theory

1. **A proof of the area law for anything run by the rule.** None exists for gump, for the 2D analogue in a
   vessel, or for the finite-depth noise-driven models. The two conditional results (draft §10.2) do not close it:
   (a) rests on hypothesis (R), known only from sampled tables at A = 30–84, with a margin of 0.003 at A = 30;
   (b) is about a constructed automaton fed by a random tape.
2. **A derivation, or even a definition, of the constant.** A referee will ask "0.21 of what?". The repository
   has: 0.2072–0.2131 on periodic faces depending on the family (0.2125 before the 4 × 4 anchor was corrected, GL1), 0.2146–0.221 and rising on octahedral faces,
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
    checked by CPU emulation only. No second GPU run, no CPU run at those sizes. *Update 2026-11-15:* a second
    card exists (GTX 1080, pull request 23, not merged); its 4 × 4 torus agrees with two CPU codes (GL1), but none
    of these runs has been repeated on it.
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
    another lattice (grade C) adjacent walls hold each other up by a factor 10⁶. *Update 2026-11-15:* in one
    symmetric vessel at A = 63 the neighbour of a dying untied face loses only its own row along the shared edge
    (DY3, draft §5.6); nothing comparable exists for asymmetric octahedra.
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
    windows) are bounded case by case in reviews, not propagated into the tables. *Update 2026-11-15:* the census
    pipeline's per-job scatter is mildly above Poisson (χ² 100/75 and 169/151), so its quoted errors are 5–15%
    small (GL1); no other pipeline's per-job scatter has been tested this way.
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
    (gap 11). *Update 2026-11-15:* the guard exists (GL2, grade B; draft §12), off by default, and no run has used
    it. Its limit: for an odd period above 128 the delay between settling and recognition can exceed a mean life at
    A ≤ 93, so guarded runs must cut censored exposure at the snapshot age or report both figures. The bounds other than R11 and R13 are grade C (the GPU session's script, re-run, not re-derived);
    the audit of 2026-11-15 found fwslab 4×9×8 bounded by 4.2 × 10⁻³, which the ledger had left out of its
    summary.
42. **The asymptotic constant, and the measurements that would decide it** (CN1, draft §7.5). Proposed and not
    made: the octahedral face at A = 108 with 10⁴ deaths (about 4 GPU-hours), which the analysis says would
    eliminate 35 of 36 single-constant readings if its value holds and the review calls not decisive; equilateral
    periodic tori (single-constant forecast: local slopes 0.2117 → 0.2136, with the existing 6×6 run already
    2.7–3.2σ below); octahedral faces of equal area with different rims, only with matched corners. Both GPU
    measurements need the guard of gap 41 first (it now exists, unused). The equilateral forecasts are anchored on
    the census's 4 × 4 value, a high draw (GL1); the CN1 fits include it and were not redone. A flat face with neither wrap-around nor rim is still unmeasured.
    *Update 2026-11-15 (fifth draft update):* the equilateral tori are measured at 48, 57, 63, 75 and 93 cells on the
    second card (GL3; draft §7.5, Table 8a); every reading of part C failed, and the family is a line of slope
    0.2084 above a kink near 61 cells. The hull face at A = 108 with 10⁴ deaths is still not run, and is now the
    measurement that bears on one price or two (gap 52).
43. ~~**The empty-patch cross-check**~~ *Done, 2026-11-15* (GP10, draft §7.5): 18 CPU runs at 0.9 of the GPU's
    exposure give the 4×5 point at −23.412 ± 0.049 (541 hits) against the GPU's −23.318 ± 0.047, combined −23.364 ±
    0.034; the last perimeter-free cost per cell is 0.226 ± 0.006 at 36 cells (CPU 0.2349 ± 0.0082, GPU 0.2185 ±
    0.0079), about 1σ above the lifetime range 0.205–0.221 rather than inside it, and still falling. What remains:
    5×5 and larger patches are GPU only; the asymptote (0.16–0.24) is not established; run-to-run scatter per
    orientation class was not examined; the CPU runs have no firewall test. Not checked at all: dependence on slab
    thickness, density and face size, and whether a 12×12 face is in the same state as a small dying one.
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
    maps, and a construction that separates a tied rim from a diagonal mirror. *Update 2026-11-15:* the maps exist
    for one vessel (A = 63, c1–D2h; DY1–DY7, draft §5.6): they show no dynamical holding-up, only a tied rim that is
    thinner at all times, and nothing that shows the thinner rim causes the cost (gap 48). The separating
    construction is still wanted.
46. **Wires and sheets** (Z13, grade C, draft §12). Of 37 unrecognised settled states, 21 were classified as wires
    and 2 as sheets by one agent; whether a wire's moving part could be held by a finite stator, whether wires of
    one period and direction are the same wire, and sheets on covers beyond 3 × 3 were not checked. The five new
    finite clocks (Z12) have no stability or basin measurements. *Update 2026-11-15:* the signal wires of draft §8.1
    (B, C, A, S) are a different set, found by constraint search; whether any of Z13's wires is among them, or
    carries a pulse, was not checked.
47. **Window choices the claims did not record** (audit of 2026-11-15). F2's plateau heights move by about 0.03
    with the averaging window (0.770, 0.604, 0.454 over whole plateaus against the quoted 0.79, 0.61, 0.48); P6's
    {110} speed depends on where the fit window ends; F11's coefficients need a weighting by firewall-first counts.
    A referee would want each analysis committed as a script with its window. Still with no re-run at all: F12
    (the plunge before death; its inputs are not in the repository), S4, Q4, G3, G4, K5, K7, K8, Z13, Z2 at
    n = 16 and Z4's period-3 search; L2 has only been recomputed from its committed tables.
48. **How a face dies, beyond one vessel** (DY1–DY7, draft §5.6). Deaths were followed only at R = 11
    cube-centred (A = 63); at A = 84 and vertex-centred there is stationary sampling only, and no excursion table.
    Every D2h quantity involving exposure moves by 0.2–0.45 with the treatment of settled lives (ln τ 7.32, 6.86 or
    7.168), and no estimator is shown to be the right one. Unresolved: 1.7–1.8σ differences between the two codes in
    the csz and D2h stationary populations and 2.7σ in one forecast's fraction (L6). Not measured: births by
    neighbour count; the layer beneath directly; whether the surviving clump's position (rim or centre, tied or free
    edge) predicts recovery, the test the clump-and-hole picture needs; c2e and O_h. *Update 2026-11-15:* rounds 3
    and 4 (sizes, the shape of a depleted face) are reviewed and in the draft; their own gaps are gap 55.
49. **Single values used as anchors.** The census's 4 × 4 torus value was a 3.4σ high draw used as an anchor (GL1).
    A referee would want every value that anchors a forecast or a fit measured twice, by independent seeds at
    least; no list of such anchors exists.

## 8. Opened by the fifth update of 2026-11-15 (dying rounds 3–4, wrapped faces, signals, state space)

50. **Prior art for the signal objects and for the state-space counts has not been searched at all** (draft §8.1,
    §6.1, §11). No pass of `research/PRIOR-ART.md` addressed signals on wires, collision logic, constructions of
    oscillators of every period, or transient lengths and in-degree statistics of finite automata and random maps.
    A referee would ask first whether the pulses, the clock of period 4N + 2, the tape and the inhibition element
    are instances of known constructions in other automata. Until a search is made, the draft claims nothing new
    for them and does not rank them.
51. **Signals: what a referee would ask for** (SG1–SG10, draft §8.1).
    - The proofs are computer-assisted: Theorem 8 rests on `prove_clock.py`'s five checks on one oracle-computed
      cycle and its enumeration of chart pairs (redone by the reviewer to 150 inserted units), Theorem 9 on one
      oracle run of a 40-unit ring. No proof assistant, no second derivation by a person. The two remarks of §8.1
      (no growth at a wire's end; a pulse carries its drive) have no ledger row.
    - The one-cell ignition of the clock is measured (N ≤ 400), not proved.
    - The negatives (no reflector, no toggling cap, the 3 × 3 tube rows) rest on SAT encodings with no UNSAT
      certificates; they hold only for period-2 caps inside the 3 × 3 tube, and wider pulses of wire C exist outside
      it. Caps of period above 2, wider tubes, backgrounds of repeat 2, other wire directions and the undecided rows
      of the bounds table were not searched.
    - Not found: a corner, a closed polygon, a crossing, a reusable reflector, a gate with its own output line, a
      stationary source, a same-side toggle, a clock of this kind with period divisible by 4. A referee would ask
      whether any of these is excluded in principle; nothing bears on it.
    - The soup and chaos counts (SG8, SG9) rest on two steppers but one block shape and a few densities; whether
      unrepeated soup ever makes a carrier is untested beyond 60,000 soups on rings of 3, 4 and 6 units.
    - The reviews did not re-run the gate (the lead did), the wide pulses, the scattering tables at the larger
      planes, or the reflector search at plane 37.
52. **The kink in the wrapped-face line, and one price or two** (GL3, draft §7.5). The line (0.2084 per cell
    through 63, 75, 93 cells) and the kink near 61 cells are fitted on one degree of freedom; the 93-cell value has
    one code (grade C); the two seeds at 57 cells differ by 2.6σ; lattice direction is confounded with size in this
    family. A referee would want: a second code at 93 cells; the four running tori (81, 84, 108, 111) scored against
    the committed forecasts; a torus family of another shape through the same range, to see whether the kink sits
    at a shortest loop or an area; hull faces at A ≥ 108 with a second implementation and the guard (gap 41), since
    one constant for both families now needs the hull slope to fall by about 0.01 beyond 108 cells. The lead's
    account of the kink (the remnant's width plus its reach) is a conjecture with no test designed. The CN1 joint
    fits have not been redone with the corrected 4 × 4 anchor or the new tori.
53. **The census pipeline's 16-generation stamping** (GL3, draft §12). Measured on the same lives at 4 × 4 and for
    a few classes at A = 48 and 60 only; the bias at A = 72 and for the classes not run is not measured. Every value
    taken from the `research/shape2` census (SH3–SH5) inherits it; the draft states it at Table 8 and in §12 and
    corrects no other value.
54. **State-space counts** (SS1–SS3, draft §6.1). The census covers hulls at most 6 layers wide; at least 325 more
    hulls of 1–29 cells are wider and unlisted, and none above 30 cells exactly. The sizes listed cannot tell linear
    from slowly exponential growth of the visited counts; where the small-vessel regime joins the face law is not
    known. The entropy figures are upper bounds with no lower bound, from one large slab standing in for small faces
    conditioned on survival. Side 16's count (SS2) is not re-run (it rests on `research/data/cube16_summary.json`:
    cycle start 2,919,617,675, period 1, so 2,919,617,676 states, which is consistent). A referee would also
    ask for the comparison with random maps to be simulated rather than estimated.
55. **The dying face, rounds 3 and 4** (DY8–DY15, draft §5.6). One fresh seed per hull size in both reviews (two
    for the torus); the lifetimes at 108 and 135 cells are the GPU's; the review's null is one patch shape (a
    ball); at 84 cells 82 deaths, so the dying-against-recovering comparison is tested only at 63 cells; the patch
    in tied faces (csz, D2h) and its change with depth are not measured. No model exists for the dip curve below
    half the population, and whether a remnant in a looser sense exists cannot be reached at sizes where faces can
    be caught that deep; a referee would ask what measurement on larger faces could decide it.
