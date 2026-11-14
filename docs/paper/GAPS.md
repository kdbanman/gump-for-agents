# What an expert referee would ask for that the repository cannot presently supply

2026-11-14, written with `draft.md`. Ordered by how much each gap limits what the paper can claim. "Supply" means:
present in the repository as a checked result, a tracked data file or a runnable command.

## 1. Theory

1. **A proof of the area law for anything run by the rule.** None exists for gump, for the 2D analogue in a
   vessel, or for the finite-depth noise-driven models. The two conditional results (draft §10.2) do not close it:
   (a) rests on hypothesis (R), known only from sampled tables at A = 30–84, with a margin of 0.003 at A = 30;
   (b) is about a constructed automaton fed by a random tape.
2. **A derivation, or even a definition, of the constant.** A referee will ask "0.21 of what?". The repository
   has: 0.2072–0.2125 on periodic faces depending on the family, 0.2146–0.221 and rising on octahedral faces,
   no measurement of a flat face without wrap-around or rim, and no demonstration that a limit exists.
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
    and front speeds (P6) are grade C and were never re-run.
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
22. **The second shape variable** (draft §7.2): two pairs; nothing at A = 72 was rerun for the census; the hint
    that the pair difference grows with age (2σ) is unresolved.
23. **Asymmetric faces with one mirror, the "lockstep" rule for general groups, the thickness transition, the
    firewall cost per cell**: all grade C. The symmetry story in the draft rests on O_h only.

## 4. Statistics and method

24. **Systematic errors are not budgeted.** Quoted errors are 1/√deaths. Known systematics (tie conventions,
    detection-time bias, the soup transient, censoring of settled replicas, cycles longer than the detection
    windows) are bounded case by case in reviews, not propagated into the tables.
25. **Undetected long cycles.** GPU runs detect periods ≤ 128, CPU runs periods dividing 840. A replica in a
    longer cycle with its face occupied would be counted as alive for ever. None has been seen; that is not a
    bound.
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
    slope, which is not known.
38. The ranking in §11 is a judgment by the draft's writer, not a result.
