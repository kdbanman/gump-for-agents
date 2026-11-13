# Prior art survey (2026-11-13)

Method: web search plus opening each cited page. "Opened" = fetched and read (abstract page, or full text
where stated). Items marked **snippet only** were seen in search results but not opened; treat as leads, not
citations. Where nothing close was found this is said. Searches used generic terms only.

## 1. Convex-hull confinement for Life-like rules

**Exists (2D, directly analogous).**
- Eppstein, *Growth and Decay in Life-Like Cellular Automata*, https://arxiv.org/abs/0911.2890 (full text
  read). Defines a rule as *fertile* if some finite pattern escapes every bounding box; non-fertile means every
  finite pattern becomes periodic. States: no B1/B2/B3 implies not fertile (cells outside a bounding box see
  at most 3 live neighbours, so none are born) — this is the axis-aligned, Moore-neighbourhood version of T2.
  Also proves, for some B3 rules (no births on 1,2,4,5; no survival with at most 5), a **bounding-diamond**
  argument: the first cell born outside the diamond would need live neighbours closer to it, contradiction.
  That is the 2D analogue of our {111} half-space proof. Same paper notes the bounding box/diamond can never
  shrink only in some cases; it discusses immortal rules and "Anneal"-type diamond-shaped growth.
- Wikipedia, *Life-like cellular automaton*, https://en.wikipedia.org/wiki/Life-like_cellular_automaton
  (opened): states the no-B0-B3 bounding-box fact.
- Conway-life wiki snippet says rules with lowest birth >= 4 never grow beyond the bounding box (**snippet
  only**, not opened).

**3D / other lattices.** Wikipedia "3D Life" (https://en.wikipedia.org/wiki/3D_Life, opened) discusses Bays'
rules on the 26-cell Moore neighbourhood and says nothing on confinement. I found no statement of the
theorem for a 3D lattice, for a non-Moore neighbourhood, or in terms of a *non-axis-aligned* half-space on a
non-hypercubic lattice.

**Verdict.** The principle (a half-space argument showing births cannot cross a boundary, hence
non-fertility and eventual periodicity) is **known** in 2D, and Eppstein's diamond argument is the same
shape of proof. Our specific statements are **new instances**: the {111} half-space on the face lattice, the
octahedral hull, T3 (firewall of 3 dead layers: two sides decouple forever), and "hull only shrinks". Do not
claim the method as new; cite Eppstein as the model. Worth checking: does Eppstein's diamond remark say the
diamond cannot shrink? (our hull can).

## 2. Kagome / rectified cubic / face-cell automata

**Geometry check (our reading, verified against sources below).** Face centres of the cubic honeycomb
= edge midpoints of the dual cubic lattice = vertex set of the **rectified cubic honeycomb**
(cuboctahedra and octahedra; Wikipedia states the rectified cubic honeycomb is made of octahedra and
cuboctahedra 1:1; the "edge midpoints" identification is standard geometry, not stated on the fetched page).
Crystallographically it is the **anion sublattice of ReO3 / cubic perovskite** and equally the **Cu sites of
Cu3Au (L1_2), i.e. the Mn sites of IrMn3**. Caveat: the rectified honeycomb's *edges* give only 8 neighbours
per vertex; our 12-neighbour rule adds the 4 coplanar corner-touching faces (distance 2 sqrt2), so the
neighbourhood is edges plus a second shell, not the edge graph.
- Cubic Crystals and Vertex-Colorings of the Cubic Honeycomb, https://arxiv.org/pdf/1204.1906 (**snippet
  only**): models ReO3/perovskite as vertex colourings of {4,3,4}.
- Monte Carlo Simulations of ABC Stacked Kagome Lattice Thin Films, https://arxiv.org/abs/1510.05924
  (abstract opened): ABC-stacked kagome layers as the Mn sublattice of IrMn3 — the same lattice as ours,
  studied as an antiferromagnet, not a CA.
- I did not obtain a source explicitly saying perovskite O3 layers along [111] are kagome (one search result
  describes alternating kagome/triangular planes along [111]); this is standard crystallography but unsourced here.

**Cellular automata on kagome.**
- *Game of Life on Archimedean Lattices: Glider Guns and Phase Dynamics*, https://arxiv.org/abs/2608.27622
  (abstract opened): Life on six composite Archimedean lattices incl. kagome; gliders, puffers, a glider gun
  (period 276) on kagome. The abstract does not state the rule or neighbourhood; this is single-layer 2D,
  growth-capable, so it is a different regime from ours (our single layer is B45/S345 on 6 neighbours, no
  births across layers' boundary).
- Bays: triangular and hexagonal Life (Complex Systems 15(3) 2005, https://complex-systems.com/?p=2198,
  **search listing only**; Wikipedia Life-like CA, opened, confirms Bays studied triangular/hexagonal).
- Nothing found on CA on the rectified cubic honeycomb vertex set, on ReO3/perovskite anion lattices, or any
  "face-cell"/"edge-cell" automaton in 3D. **Our lattice + rule appears to be new as a CA** (absence of
  evidence from a limited search).

## 3. Metastability, QSDs, extinction times

- Collet, Martinez, San Martin, *Quasi-Stationary Distributions* (Springer 2013),
  https://www.springer.com/book/9783642428883 (catalogue page seen via search; **book not read**). Standard
  statement: for a chain with an absorbing state, the killing time started in a QSD is exactly exponential
  with rate = escape rate of the QSD, memoryless. This is the formal content of our "memoryless collapse".
- Asselah, Ferrari, Groisman, *Quasi-stationary distributions and Fleming-Viot processes in finite spaces*,
  https://arxiv.org/abs/0904.3039 (abstract opened): FV particle system's empirical measure converges to the
  QSD; the basis for a Fleming-Viot QSD estimator. Direct tool for our measurement; not used by us yet.
- Contact process, finite volume: exponential-in-volume extinction and exponential limit law (Durrett-Liu,
  Durrett-Schonmann, Mountford; Mountford-Mourrat-Valesin-Yao on trees). **Snippet only** (a search summary
  of surveys, https://arxiv.org/pdf/1810.06040 appeared among results; Mountford's paper PDF fetched but
  unreadable). Lifetime ~ exp(c*volume) with c depending on the model is the same form as our
  exp(0.209*A), where A is a face area rather than a volume.
- Reia, Kinouchi, *Conway's game of life is a near-critical metastable state in the multiverse of cellular
  automata*, https://arxiv.org/abs/1407.1006 (abstract opened): 6,144 outer-totalistic rules, transition
  region looks like a discontinuous absorbing-state transition, metastable states, nucleation. Closest
  CA-specific framing; ours is a different regime (confined, deterministic, finite).
- Decay of Life from random soups: arXiv 1809.03266 (abstract opened): tail of the quiescence time is
  exponential, density relaxation exponential, time scale ~L^1.66. Bagnoli et al 1992 and the Bak
  power-law-vs-exponential dispute are cited there (not opened).
- Bays, 3D Life (Complex Systems 1987 etc.), https://complex-systems.com/?p=1882 listing only; Wikipedia 3D
  Life opened. Bays' rules are on the 26-cell neighbourhood; none touches confined rules.
- Large deviations: Buca, Garrahan, Prosen, Vanicat, rule 54 (https://arxiv.org/abs/1901.00845, **snippet
  only**) and others — large deviations in CA exist but I found nothing on the density tail of a
  *deterministic chaotic* CA used as a QSD / extinction-rate predictor.

**Verdict.** The *structure* (exponential survival time, memoryless, extinction rate = QSD escape) is
**standard** Markov/IPS theory; exponential-in-size lifetimes of metastable CA/IPS are **known**. What I found
no precedent for: applying it to a **deterministic** CA with the boundary-layer area as the exponent, the
exact per-site slope 0.209 with face death = tail of the stationary density distribution to one cell,
and "forward flux fails because the plunge takes about 10 generations". Treat the deterministic-chaos-as-
effective-Markov-chain claim as the novelty; its justification (why an effective memoryless description holds)
has no citation I found.

## 4. Symmetry shortens lifetimes

- No source found that states or measures it. Lexicon pages (playgameoflife.com/lexicon/symmetric, soup;
  snippet only) say that symmetric soups produce large symmetric objects at higher rates, and apgsearch has
  C2/C4 symmetric soup censuses (symmetry preserved by the rule, trivially known). Nothing on lifetimes
  or on "lockstep fluctuations".
- The conceptual ingredient (symmetric states fluctuate as one coupled domain, so the effective number of
  independent degrees of freedom is area/|G|) is a standard large-deviation / symmetry-reduction idea but I
  found no explicit statement for CA.

**Verdict.** **Appears new** as a quantified result (A/7.7 with a sqrt correction, and the n=16 failure).
Absence of evidence only. Related general claim to check against: symmetry-reduced simulation of Life
soups (apgsearch) exploits the same lockstep property for speed, not for lifetime.

## 5. Oscillators: period = loop x twist

- LifeWiki "Mod" (read via the mirror https://conwaylife.njohnston.ca/wiki/Mod, because conwaylife.com
  returned 403): mod = smallest number of generations to reappear in original form possibly after
  rotation or reflection. Square grid: mod is period, period/2 (180 deg rotation or flip), or period/4 (90
  deg). **Hexagonal/triangular grid: period, period/2, period/3 (120 deg), period/6 (60 deg).**
  So 3- and 6-fold twists are **known** on hex/triangular Life, and our twist set {2,3,4,6} matches.
- LifeWiki "Oscillator" (https://conwaylife.njohnston.ca/wiki/Oscillator): defines period, rotor, stator.
  It does not define "trivial" or "compound" oscillators on that page; mentions that non-trivial
  oscillators need at least one cell oscillating at full period. The Compound oscillator page was 404 in the
  mirror. So use "compound" as our own term or check LifeWiki directly (not verified).

**Verdict.** Period/mod terminology confirmed; our "twist x loop" is a re-expression of period/mod. Our
contributions are the 3D screw-type twists (C48.24a = 6 x 8) and the statistics (twisted loops about 3-8% at
every loop length), which I found no precedent for.

## Gaps and cautions
- Several sources were seen only as search summaries; the search tool is lossy. Re-open before citing in a
  write-up: 1204.1906, 1810.06040, Mountford, Collet et al., Bays 1987/2005.
- Eppstein's diamond-hull proof is the key related result; if we write up T2/T3, cite it prominently.

## Adversarial review (second pass)

Date 2026-11-13. Goal: refute verdicts (a) and (b). Only pages I opened are cited; "search summary" = seen only in
a search result and NOT usable as a citation. Many conwaylife.com pages return 403 to the fetcher (use the
conwaylife.njohnston.ca mirror); several arXiv PDFs return unreadable compressed text (Eppstein 0911.2890,
Guttesen 2608.27622, 1203.1644), so claims about their bodies could not be re-verified.

### (a) "No cellular automaton has been studied on this lattice" -- STANDS (with caveats)

Refutation attempt failed. Searched: rectified cubic honeycomb / cuboctahedral lattice, ReO3/perovskite, Cu3Au,
kagome / hyperkagome / pyrochlore, FCC 12-neighbour, face/edge-cell CA, Golly/LifeWiki/forum threads. Nothing on
this vertex set. Nearest misses (none is our lattice + dynamics):
- LifeWiki Cubic honeycomb (mirror, https://conwaylife.njohnston.ca/wiki/Cubic_honeycomb), opened: "Using only
  "edge" cells corresponds to operating on an A3≅D3 root lattice" and "Combinations of layers can also be
  considered". These are sub-neighbourhoods of the Moore neighbourhood on Z^3 (the 12 edge-diagonal offsets =
  FCC), so a 12-neighbour FCC CA is conceptually on LifeWiki. It is a different graph from ours (cells here
  are the 3 sites per cube, not one), so this WEAKENS only the statement "12-neighbour 3D automata are unstudied",
  not our lattice claim. Our paper-style claim should say "on this lattice", not "with 12 neighbours".
- Wolfram NKS note (https://wolframscience.com/nks/notes-5-2--other-geometries-for-cellular-automata/), opened:
  "the rhombic dodecahedron (12) (e.g. face-centered cubic crystals)"; the page does not mention kagome,
  rectified, octahedral or cuboctahedral lattices. Shape list only.
- ConwayLife forum "Breeders and such like" (mirror https://conwaylife.njohnston.ca/forums/viewtopic.php?t=471),
  opened: apg, 19 Jul 2010, lists 3D lattice options including "The face-centred cubic lattice (12 neighbours)"
  and notes "lots of options as you move to three dimensions". A list of options, no rule run on ours.
  (Claims in a search summary that the thread says only Moore was explored: not seen in the opened text.)
- Guttesen, Game of Life on Archimedean Lattices (https://arxiv.org/abs/2608.27622), abstract opened: "explore
  Conway's Game of Life (GoL) on six composite Archimedean lattices". 2D; no 3D lattice. Body unreadable.
- Hyperkagome/pyrochlore: search found only physics lattice-model pages, no CA. ABC kagome IrMn3 (1510.05924)
  stays as the physics (Monte Carlo) neighbour, as in section 2.
Residual risk: paywalled or non-indexed physics/materials literature (lattice-gas or Ising dynamics on the
anion sublattice of perovskite) was not searched exhaustively; "absence of evidence" stands.

### (b) "Symmetric ICs shorten lifetimes exponentially appears new" -- STANDS

Refutation attempt failed. Searched Catagolue/apgsearch symmetric soups, methuselah/lifespan by symmetry,
extinction time with symmetry, QSD with symmetry reduction, effective system size.
- Life Lexicon "soup" (https://playgameoflife.com/lexicon/soup), opened: "symmetric soups tend to create large
  symmetrical objects at a much higher rate" and "The results for these two types of soups can differ". About
  object content, not lifetimes. (Upgrades the earlier "snippet only" note to opened.)
- Catagolue/apgsearch pages came only as search summaries: symmetric censuses are kept in separate symmetry
  classes; no lifespan statistics by symmetry were seen. Not opened, so not citable.
- Extinction-time results found (e.g. Battle of the Sexes, arXiv 0709.0225, SIS QSD papers) were search
  summaries only; they give exponential-in-N extinction but nothing about symmetric starts. Not opened.
Nothing found stating that symmetry reduces effective size to A/|G| for lifetimes. Note the idea is mathematically
close to standard "symmetry-reduced" invariant-subspace dynamics, so "new" should be worded "not found".

### Snippet-only items: confirmed or struck
- Conway-life "lowest birth >= 4 never grows beyond bounding box": CONFIRMED via
  https://conwaylife.njohnston.ca/wiki/Outer-totalistic , quote "since no patterns can ever grow beyond their
  initial bounding box" (rules whose lowest birth condition is 4 or more; 16384 rules).
- arXiv 1204.1906 (vertex-colorings of cubic honeycomb): opened abstract. Quote: "we discuss vertex-colorings of
  the cubic honeycomb"; "demonstrate the structure and symmetries of certain cubic crystals". It does NOT mention
  ReO3 or perovskite in the abstract. STRIKE the ReO3/perovskite attribution (keep only as vertex-colourings of
  {4,3,4}).
- arXiv 1810.06040: opened. It is "The Contact Process on Random Graphs and Galton-Watson Trees", NOT a survey of
  finite-volume extinction and says nothing about exponential-in-volume extinction. STRIKE. Replace with
  Mountford, Mourrat, Valesin, Yao, https://arxiv.org/abs/1203.2972 (opened): "uniformly over all trees of degree
  bounded by a given number, the expectation of tau grows exponentially with the number of vertices" and tau over
  its mean "converges in distribution to the unitary exponential distribution". (Bounded-degree trees, not
  lattices; Durrett-Liu / Durrett-Schonmann remain unopened.)
- Buca et al. rule 54, https://arxiv.org/abs/1901.00845: opened. Title "Exact large deviation statistics and
  trajectory phase transition of a deterministic boundary driven cellular automaton"; stochastic boundary driving,
  time-extensive observables. Fine as "large deviations in CA exist"; it is not about QSD or density tails.
- Collet-Martinez-San Martin book: Springer page redirected to a login wall; NOT opened. STRIKE as citation (leave
  as "standard textbook, unverified"). The memoryless-exponential statement is nonetheless standard QSD theory.
- Bays 2005 (complex-systems.com/?p=2198): fetch returned HTTP 500; unopened. Triangular/hexagonal Bays work is
  supported instead by Wikipedia Life-like CA (opened): "Bays has also studied two-dimensional life-like CA with
  triangular or hexagonal neighborhoods." Drop the Complex Systems 15(3) citation or mark unverified.
- Bays 1987: search results show the abstract and a later retrospective naming the 1987 rules 4,5/5 and 5,6,7/6
  (search summary, not opened). Wikipedia: "Carter Bays has proposed a variety of generalizations of the Game of
  Life to three-dimensional CA". Keep Wikipedia as the citation.
- Playgameoflife lexicon "symmetric": now opened, see (b).
- Guttesen kagome paper: the abstract confirms "six composite Archimedean lattices" only. The survey's "glider gun
  (period 276)" and "puffer" details, and the statement that it is "growth-capable" with Conway's neighbourhood,
  come from search summaries and could not be verified (PDF unreadable). Mark "period 276" UNVERIFIED.
- Eppstein 0911.2890: PDF unreadable to the fetcher this time; the section-1 claims about the bounding-diamond
  argument and "can the diamond shrink" are NOT re-verified. Wikipedia's no-B0..B3 bounding-box statement is
  confirmed (opened).

### Corrections to Mod / trivial-oscillator statements
- conwaylife.com/wiki/Mod still returns 403; the mirror https://conwaylife.njohnston.ca/wiki/Mod was re-read.
  Confirmed quotes: hex/triangular grid: "The mod of an oscillator can be identical to its period, but it can also
  be half of its period", "a third of its period (for oscillators that rotate 120 degrees a third of the way
  through their evolution)", "or a sixth of its period (for oscillators that rotate 60 degrees a third of the way
  through their evolution)", plus "Oscillators with a mod one sixth of their period must be centered around either
  a hexagonal cell or a triangular grid's vertex". So period/2, /3, /6 are stated as above.
  Corrections: (i) the half case on the hex page is attributed to a FLIP, not a 180-degree rotation; (ii) the
  page's own 60-degree wording ("a third of the way") is odd (internally inconsistent with a sixth) and should
  not be quoted as a derivation; (iii) for the square grid, the page gives only "may be a quarter of the period"
  and half via examples (Clock, Phoenix 1; Sixty-nine = quarter) -- it does not spell out "180 degrees or flip" for
  half or "90 degrees" for a quarter, so those parentheticals in section 5 are our gloss, not the page's.
  (iv) "mod" is also described as sometimes meaning ordinary modulus, not to be confused with the mod of a pattern.
- Trivial oscillators: the survey said LifeWiki's Oscillator page "does not define trivial or compound". That is
  right for that page, but LifeWiki does define it elsewhere: https://conwaylife.njohnston.ca/wiki/Non-trivial ,
  quote "A period-n oscillator is considered non-trivial if it contains at least one cell that oscillates at the
  full period ... if it is not made up solely of separate oscillators with smaller periods". The Life Lexicon
  (https://playgameoflife.com/lexicon/trivial_(2)) says "A trivial period-N oscillator is one in which every cell
  oscillates at some smaller factor of N". Neither page uses the word "compound". So "trivial/non-trivial" is
  established LifeWiki terminology (use it); "compound" remains unsourced (our own term).
