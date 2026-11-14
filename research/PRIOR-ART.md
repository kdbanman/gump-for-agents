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

[Narrowed 2026-11-13: deterministic chaos lasting exp(c·size) with memoryless collapse is a known *numerical*
phenomenon, the supertransient. See "Supertransients and stable chaos" at the end of this file.]

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

## Supertransients and stable chaos (added 2026-11-13)

From the swarm's library (`research/theory/swarm/library/shelf.md`, `notes/supertransients.md`; each statement
there is tagged by how far the source was read). The lead re-opened two of the sources to abstract level
(Politi–Torcini, arXiv 0902.2545; Houghton–Knobloch–Tobias–Proctor, Phys. Lett. A 374 (2010) 2030, author
copy at eprints.whiterose.ac.uk/10731): titles, authors and the quoted claims match.

- **The area law is an instance of a named phenomenon.** *Supertransients*: spatially extended deterministic
  systems that are chaotic for a time growing exponentially (or faster) with system size, then collapse abruptly,
  with exponentially distributed lifetimes. Crutchfield–Kaneko 1988 (coupled map lattices; abstract only: "faster
  than exponentially with increasing system volume"); Wackerbauer–Showalter 2003 (reaction–diffusion; not
  obtained); Houghton et al. 2010 (complex Ginzburg–Landau in one dimension: τ(L) = exp(AL + B), "Poisson
  statistics", and the collapse appears only with non-periodic boundaries, through boundary layers of fixed
  thickness); review Tél–Lai 2008 (Phys. Rep. 460; not obtained). *Stable chaos* (Politi–Torcini 2009) is the
  cellular-automaton-like case, with transient time exponential in chain length.
- **Nothing is proved** in anything the librarian could open; every statement is a fit to simulations. The
  standard picture is a non-attracting chaotic set with a small escape rate.
- **No source read treats a deterministic cellular automaton with an absorbing state**, or a law in the area of
  a boundary face rather than the size of the whole system.
- **Revised verdict for §3.** Not new: deterministic chaos with lifetime exponential in size and memoryless
  collapse. Possibly new: (a) an automaton whose confinement and firewall are theorems, so that collapse proceeds
  layer by layer; (b) the exponent set by the area of one face of a three-dimensional vessel; (c) the measured
  tail down to one cell, with the death rate as its next point; (d) the symmetry effects; (e) any proof at all,
  for any member of the class.
- **Corrections to §3's contact-process entry** (`library/notes/contact-finite.md`): Durrett–Liu and
  Durrett–Schonmann are one-dimensional; exponential-in-volume in d ≥ 2 is Mountford 1999 (abstract only);
  Mountford 1993 proves the exponential limit law. No finite-size exponential-lifetime theorem without
  monotonicity was found (`notes/nonmonotone.md`).
- Not obtained (publisher pages refuse automated clients; a person with a browser could fetch them): Tél–Lai 2008,
  Crutchfield–Kaneko 1988, Kaneko 1990, Wackerbauer–Showalter 2003, Bramson–Neuhauser 1994. The shelf ends with
  the full list.

## Third pass, 2026-11-14: boundary layer over noise; shape of a periodic domain; sealed sets

Librarian, one session. Web search plus opening each page; queries generic. Where a fetched PDF came back as binary,
the fetch tool's own saved copy was converted with the installed `pdftotext` and read; "full text" below means that.
Quotes are copied from that text. Nothing was run or downloaded otherwise. Shelf rows: `theory/swarm/library/shelf.md` §10.

### 1. A boundary layer over noise

**Works found**
- R. Carretero-González, S. Ørstavik, J. Huke, D. S. Broomhead, J. Stark, "Thermodynamic limit from small lattices
  of coupled maps", Phys. Rev. Lett. 83 (1999) 3633–3636; https://arxiv.org/abs/chao-dyn/9904009 — **full text**.
  Abstract: "We compare the behaviour of a small truncated coupled map lattice with random inputs at the boundaries
  with that of a large deterministic lattice essentially at the thermodynamic limit. We find exponential convergence
  for the probability density, predictability, power spectrum, and two-point correlation with increasing truncated
  lattice size." Construction: "consider the dynamics at the boundaries x_0 and x_{N+1} to be produced by two
  independent driving inputs. The driving input is chosen to be white noise uniformly distributed in the interval
  [0, 1]." "Other kinds of inputs did not change our observations in a qualitative way." Coupled logistic maps,
  one dimension; statistics of a persistent chaotic state. **No transients, lifetimes or absorbing state.**
- A. M. dos Santos, R. L. Viana, S. R. Lopes, S. E. de S. Pinto, A. M. Batista, "Collective behavior in coupled
  chaotic map lattices with random perturbations", Physica A 387 (2008) 1655–1668, doi:10.1016/j.physa.2007.09.051;
  https://ideas.repec.org/a/eee/phsmap/v387y2008i7p1655-1668.html — **abstract only, and only as paraphrased by the
  fetch tool** (it would not quote). Per that paraphrase: small truncated lattices with uniform random inputs at the
  boundaries, said to emulate a "thermal bath", replacing chaotic degrees of freedom by random perturbations;
  used for synchronisation, not lifetimes. Treat as a lead.
- Houghton–Knobloch–Tobias–Proctor 2010 (on the shelf; re-read, **full text** of the White Rose copy). New detail:
  the defect production rate across a Neumann domain is fitted by f(x) = b1 tanh(x/b2) tanh((L−x)/b2); "We interpret
  b2 as the width of each boundary layer and b1 as the production rate in the central part of the domain"; "the
  boundary layer thickness is independent of the domain length and … the defect production rate away from the
  boundaries is essentially the same as when PBC are used." The lifetime fit is τ(L) = exp(AL + B) in the whole
  length L; the paper does not model the lifetime as a property of the boundary layer, and replaces nothing by noise.
  Its reference list (read) adds nothing on noise or boundary models: Shraiman 1986 (KS), Wackerbauer 2007,
  Wackerbauer–Showalter 2003, Crutchfield–Kaneko 1988, Tél–Lai 2008, Hof et al. 2006, Borrero-Echeverry et al.
- R. Mikkelsen, M. van Hecke, T. Bohr, "Universal and non-universal properties of transitions to spatio-temporal
  chaos in coupled map lattices", arXiv:cond-mat/0207208 — **abstract**: "under the appropriate mapping some
  deterministic chaotic systems behave like stochastic models"; "the deterministic model behaves like Directed
  Percolation with infinitely many absorbing states". The general chaos-as-stochastic-model principle, not lifetimes.
- K. Sugimura, H. Kori, "Exponential system-size dependence of the lifetime of transient spiral chaos in excitable
  and oscillatory media", Phys. Rev. E 92 (2015) 062915; https://arxiv.org/abs/1512.08333 — **full text**. See
  "hole probability" below. On boundaries: with Neumann conditions "the steady state can be reached not only from the
  states with m = 2 by annihilation but also from the states with m = 1 through the absorption of a defect by the
  boundary". Boundaries enter only as a second exit channel; nothing replaced by noise.
- Leads seen only as search results (not opened): Wackerbauer and co-author, "Noise can delay and advance the collapse
  of spatiotemporal chaos" (Phys. Rev. E, 2007; only a ResearchGate copy surfaced, not fetched); Shih–Hsieh–Goldenfeld
  stochastic predator–prey model reproducing puff lifetimes (APS DFD 2015 abstract); a search summary of Tél–Lai saying
  "the lifetime increases exponentially with the size for any fixed type of noise" (not verified: PDF not obtained).

**Verdict.** *A new instance of a known principle, as to the method; not found, as to the result.* Replacing the
chaotic surroundings of a region by independent random inputs and checking that the region's statistics are
reproduced is published (Carretero-González et al. 1999, for one-point and two-point statistics of a persistent
state; dos Santos et al. 2008 calls it a thermal bath). The arrangement is the mirror image of ours: they keep a
window and randomise its outside; we keep the boundary layer and randomise the inside. Not found: any work that
replaces the chaotic interior (or neighbour) by noise and compares *transient lifetimes or escape rates*, or that
states the exponent of a supertransient to be a property of a thin stochastic boundary model. Houghton et al. is the
nearest on the boundary side (fixed-thickness boundary layers, death only with non-periodic walls) but stops at the
observation. Queries tried: transient spatiotemporal chaos lifetime boundary layer noise replaced bulk escape rate;
supertransient boundary conditions Neumann periodic boundary-induced collapse; coupled map lattice chaotic transient
lifetime random boundary conditions stochastic boundary; "random boundary conditions" spatiotemporal chaos transient
lifetime; coupled map lattice bulk replaced by random numbers stochastic driving boundary chaotic saddle; "truncated
lattice" "random inputs" transient OR lifetime OR escape; chaos as heat bath Kramers escape spatially extended; CA
chaotic transient random vs deterministic boundary absorbing state; stochastic models of puff lifetimes; works citing
Houghton et al. (the search tool returns no citation lists; none found that way).

### 2. The shape of a periodic domain at fixed size

**Works found**
- M. Caselle, F. Gliozzi, S. Vinti, "Finite-size effects in the interface of 3D Ising model", Phys. Lett. B 302
  (1993) 74–79; https://arxiv.org/abs/hep-lat/9212013 — **full text**. Abstract: "these finite-size corrections depend
  rather strongly on the shape of the lattice". Setting: 3D Ising, box L1 × L2 × L3 with L3 long; the measured
  quantity is the tunnelling energy splitting E0 between the two magnetised vacua (an inverse tunnelling time) with
  the interface spanning the periodic L1 × L2 cross-section, "a rectangle of lengths L1, L2 with opposite edges
  identified (hence a torus)". Capillary-wave result, eq. (4): F_cw/k_BT = log(√(−iτ)|η(τ)|²) + c, τ = i L1/L2,
  η the Dedekind eta function, L1 ≥ L2; eq. (13): "E0(L1, L2) = Zcw(L1, L2) e^{−σ L1 L2}", with
  Zcw = C̃ √(L2/L1) q^{−1/12}(1 + q + 2q² + …), q = exp(−2π L1/L2). "Eq. (7) is scale invariant, indeed it only depends
  on the asymmetry parameter L1/L2 … it cannot be observed … if one measures the interface tension on square lattices
  of different sizes". They test it at **equal area**: R ≡ E0(L1, L2)/E0(L̃, L̃) with L̃ = √(L1 L2), eq. (14),
  parameter-free, "The agreement between numerical data and theoretical prediction is rather impressive". The form is
  credited to Lüscher–Symanzik–Weisz (Wilson loops; not obtained) and called "rather well known … in conformal field
  theories and in lattice gauge theories".
  *Our reading, not the paper's words:* q^{−1/12} = exp(π L1/(6 L2)), so at fixed area A = L1 L2,
  log E0 ≈ −σA + (π/6)(L1/L2) − ½ log(L1/L2) + const: the rate rises, and the cost per unit area falls, as the torus
  thins, by an amount set by the short side L2 (here the systole). The paper treats only rectangular (untwisted)
  tori; a twist would enter through Re τ, which this paper does not discuss.
- T. Neuhaus, J. S. Hager, "2D crystal shapes, droplet condensation and exponential slowing down in simulations of
  first-order phase transitions", J. Stat. Phys. 113 (2003) 47–83; https://arxiv.org/abs/cond-mat/0201324 —
  **abstract**: the exponential slowing down comes from "discontinuous droplet shape transitions between various
  classical crystal shapes obeying geometrical constraints" on tori and cube surfaces; finite-size corrections to the
  toroidal droplet free energy. The abstract does not mention aspect ratio.
- Leads seen only as search results: plane-Couette lifetime papers (arXiv:2011.08914, 1109.0889) that compare median
  lifetimes in a few box sizes; Webb–Ansell–Sussman, Soft Matter 2026 (active matter on a torus; band wrapping the
  minor circumference at high aspect ratio); metastability of Ising on the hexagonal-lattice torus (arXiv:2101.11894:
  "plus strip" = a cluster wrapping the torus). None opened.

**Verdict.** *A new instance of a known principle* for "at fixed area the rate depends on how the torus closes":
in equilibrium tunnelling through an interface on a periodic cross-section, the rate is e^{−σA} times a universal
factor of the modular parameter, tested at equal area (Caselle–Gliozzi–Vinti 1993, after Lüscher–Symanzik–Weisz), and
on thin tori that factor lowers the cost per unit area through the short side. The differences matter: theirs is an
equilibrium interface with Gaussian capillary waves, the shape enters only the prefactor (sub-leading, O(L1/L2) in the
log), and it is not a transient lifetime. **Not found:** any dependence of a *chaotic-transient, turbulent, nucleation
or extinction lifetime* on the aspect ratio or twist of a periodic domain at fixed size; any use of the systole as the
controlling length for a lifetime; minimal-flow-unit lifetime versus box shape at fixed area; contact-process
extinction on tori of different shape. Queries tried: turbulence lifetime vs domain aspect ratio periodic box minimal
flow unit plane Couette; metastable lifetime nucleation periodic boundary aspect ratio elongated torus Ising strip;
contact process extinction torus shape aspect ratio thin cylinder; Binder interface free energy rectangular
L1 × L2 tunnelling shorter side; droplet-to-strip transition torus aspect ratio (Leung–Zia not reached); plane Couette
lifetime vs domain size spanwise; shortest non-contractible loop torus relaxation/tunnelling/lifetime twisted
boundary conditions; Ising metastability rectangular torus strip barrier side lengths.

### 3. Sealed sets and firewalls

**Works found**
- F. Blanchard, P. Tisseur, "Some properties of cellular automata with equicontinuity points", Ann. Inst. H. Poincaré
  Probab. Statist. 36 (2000) 569–582; https://arxiv.org/abs/math/0312137 — **full text, §2.2**. Definition: "A word
  B ∈ A^{2k+1} is called a blocking word for (X, F) if there is an infinite sequence of words v_n, |v_n| = 2i + 1 ≥ r
  such that for any x ∈ A^Z with x(−k, k) = B one has F^n(x)(−i, i) = v_n". "An occurrence of a blocking word in a
  configuration x completely disconnects coordinates to its right and left for the action of the automaton; hence
  the name." Prop. 2.1, "essentially due to Kůrka": every equicontinuity point contains a blocking word; points with
  infinitely many occurrences on both sides are equicontinuity points.
- M. Sablik, G. Theyssier, "Topological dynamics of cellular automata: dimension matters", Theory Comput. Syst.
  (2011); https://arxiv.org/abs/0811.2731 — **abstract**: in dimension ≥ 2 there are "non sensitive CA without
  equicontinuous points"; the 1D picture breaks.
- N. Ait Sadi, R. Chemlal, "Irrational eigenvalues of D-dimensional cellular automata", arXiv:2509.00933 (HTML v1) —
  **definitions and the attributions**: d-dimensional (r1, …, rd)-blocking patterns with an offset; "fully blocking"
  when the offset is 0; Theorem 6 (from E. G. Burkhead, the thesis below): "If there exists a fully blocking pattern of
  size k^d for F where k ≥ r then F is almost equicontinuous"; "This equivalence do not hold in higher dimension".
- E. Gamber (Burkhead), *A topological classification of D-dimensional cellular automata*, thesis (UNC Chapel Hill,
  dir. J. Hawkins) — **not obtained** (the only copy surfaced is on the core.ac.uk aggregator, not fetched); contents
  known from search results and the paper above ("A Blocking Pattern for a 2D Cellular Automaton", "A Pattern Blocking
  a Cross").
- J. A. H. Audouard, G. Theyssier, "On Kůrka's dichotomy for cellular automata on groups", arXiv:2602.20623 —
  **abstract**: the sensitivity / equicontinuity-point dichotomy "holds on any virtually-Z group but not on free groups
  with 2 or more generators".
- B. Bollobás, P. Smith, A. Uzzell, "Monotone cellular automata in a random environment", Combin. Probab. Comput. 24
  (2015); https://arxiv.org/abs/1204.3980 — **full text, §1**. Definition 1.2: u is a stable direction if
  [H_u] = H_u, where H_u = {x : ⟨x, u⟩ < 0} and [·] is the bootstrap closure (an infected half-plane does not
  grow). And: "Suppose that u and
  −u are stable directions, and that the initial set A ⊂ Z² does not intersect an infinite strip with sides orthogonal
  to u of at least a certain width depending only on U. Then [A] cannot intersect that strip either." Also reports
  Gravner–Griffeath's subcritical class as those with "closed cofinite proper subsets of Z²".
- E. Goles, D. Maldonado, P. Montealegre, N. Ollinger, "On the complexity of the stability problem of binary freezing
  totalistic cellular automata", arXiv:1912.02953 — **abstract**: freezing automata ("the active cells remain
  unchanged"); STABILITY = "deciding whether an inactive cell becomes active". V. Salo, G. Theyssier, I. Törmä,
  "Cellular automata and bootstrap percolation", arXiv:2110.00656 — **abstract**: freezing + monotone = bootstrap
  percolation. Here the set of fixed cells only grows by definition of the class.

**Verdict.** *A new instance of a known principle.* The firewall (three consecutive dead layers that stay dead and
decouple the two sides for ever) is a blocking word in the sense of Kůrka / Blanchard–Tisseur, of the simplest kind
(constant image v_n = dead), read along one lattice direction with whole layers as letters; it is also the
non-monotone, three-dimensional counterpart of the bootstrap-percolation fact that an empty strip of width depending
only on the rule, orthogonal to a pair ±u of stable directions, stays empty (Bollobás–Smith–Uzzell 2015). Possibly
new in its own terms: a blocking set for a *non-monotone* rule whose blocking letter is the quiescent state itself, in
3D on this lattice, and its use to make collapse layer by layer. "The largest sealed set only grows": **not found**
stated anywhere; in freezing automata the analogous monotonicity is built into the class, and for blocking words it
is immediate from the definition (images of a blocking occurrence are determined for all n), so it should be
presented as an easy consequence, not as a result. Queries tried: Kůrka blocking word almost equicontinuous
classification; 2D CA equicontinuity blocking patterns Sablik Theyssier; freezing CA stable sets frozen cells threshold
automata Goles bootstrap percolation; Bollobás–Smith–Uzzell stable directions half-plane; Gamber thesis.

### Also: probability of an (almost) empty state as the predictor of the lifetime

**Exists (numerical, heuristic).** Sugimura–Kori 2015 (full text): the number of spiral defects m in the transient
state is Gaussian with mean αN and variance βN, rationalised by approximately independent subsystems larger than the
correlation length; assuming a Markov chain on m, "The expected value of lifetime T is the inverse of the probability λ
to obtain S. Because S is obtained only when the previous number is 2, λ = Zp(2)", eq. (7) T(N) = 1/(Z p(2)), and with
the Gaussian tail eq. (9) T(N) ∼ exp((α²/2β) N). Fit "well for parameter sets near the onset of transient chaos". This
is the same structure as our "death rate = next point of the stationary tail" (rate = probability of the last state
before absorption × an exit rate), stated for defect counts in a 2D PDE, with a Gaussian tail assumed rather than
measured. The proved stochastic analogue already on the shelf is Durrett–Schonmann 1988 (empty interval cost under the
contact process's stationary law). "Emptiness formation" in the integrable-systems sense was not searched.

### Not obtained this pass
- Tél, Lai, "Chaotic transients in spatially extended systems", Phys. Rep. 460 (2008) 245–275: an author copy exists at
  https://chaos1.la.asu.edu/~ylai1/papers/PRep_2008_TL.pdf but returned HTTP 503 three times; still not read.
- Tél, "The joy of transient chaos", Chaos 25 (2015; volume from the file name, unverified), author copy http://theorphys.elte.hu/tel/pdf_pub/Chaos25.pdf:
  HTTP 503.
- Gamber (Burkhead) thesis (aggregator copy only); dos Santos et al. 2008 full text (ScienceDirect); Wackerbauer et al.
  2007 noise paper (ResearchGate only); Lüscher–Symanzik–Weisz 1980; Kůrka 1997 (ETDS) — not attempted, Blanchard–Tisseur
  used for the definition; Leung–Zia 1990 not reached.

### Not searched
Citation lists (the search tool gives none, so "what cites Houghton et al." was done only by keyword); quantum-memory
lifetimes of topological codes on tori (code distance = systole; a plausible analogue for item 2, not opened);
anisotropic-Ising metastability on rectangular tori; pipe-flow puff lifetime versus pipe length; Kuramoto–Sivashinsky
lifetime papers beyond Houghton's citation of Shraiman 1986; non-English literature.

### Adversarial review of the third pass (2026-11-14)

Second librarian, one session; goal: refute each "not found" and re-check the citations. Same method as the third pass:
web search, then opening each page; where a PDF came back as binary, the fetch tool's saved copy was converted with
`pdftotext` and read ("full text" below). Queries generic. Shelf rows: `theory/swarm/library/shelf.md` §11.
Semantic Scholar's public API gave one citation list (Carretero-González et al. 1999) and then HTTP 429 four times;
the citation lists of Houghton et al. 2010 and Sugimura–Kori 2015 are therefore **not obtained**.

#### Citations re-checked
- Carretero-González et al. 1999 (abstract re-opened): the quoted abstract is exact. Its 12 citing works (Semantic
  Scholar list, read as titles) are on embedding, Lyapunov spectra, fractional CMLs, synchronisation, one on transient
  ratchet transport; **none on lifetimes or escape rates**. dos Santos et al. 2008 is among them, as the pass said.
- Caselle–Gliozzi–Vinti 1993 (abstract re-opened): "these finite-size corrections depend rather strongly on the shape
  of the lattice" is exact. Body not re-read.
- Blanchard–Tisseur 2000 (full text, §2.2): the blocking-word definition and "completely disconnects coordinates to its
  right and left for the action of the automaton; hence the name" are exact.
- Bollobás–Smith–Uzzell 2015 (full text, §1): the strip sentence and the Gravner–Griffeath quote are exact; the full
  sentence is "to be subcritical if there exist closed cofinite proper subsets of Z², and to be critical otherwise".
- Sugimura–Kori 2015 (ar5iv HTML): quotes (7), (9), "λ = Zp(2)", the boundary sentence and "fits well for parameter
  sets near the onset" are exact. **Mis-description corrected:** the pass says "with a Gaussian tail assumed rather
  than measured". In fact they *measure* the distribution of m ("we confirm that the probability distribution approaches
  the following Gaussian distribution as the system size increases"), and in Fig. 9 they plot T against "C1/p(2) with
  numerically obtained p(2)" and against C2/p(2) with the Gaussian p(2); C1 and C2 are "fitting parameters". So the
  lifetime is tested against a **measured** probability of the last state, up to a fitted constant. What they extrapolate
  is the N-dependence of p(2) through the Gaussian, with Z assumed independent of N. Markov assumption: "We assume that
  the process illustrated in Fig. 6 is Markovian." This narrows our claim (c) of the supertransients section: the
  measured-tail-gives-the-lifetime check has a precedent in a 2D PDE. What stays ours is the tail measured down to one
  cell, and the exit rate measured rather than fitted.

#### 1. A boundary layer over noise: STANDS WITH CAVEATS
Nothing found that replaces a chaotic bulk (or neighbour) by noise and compares transient lifetimes or escape rates.
Closest, newly found:
- D. Vidmar, W.-J. Rappel, "Extinction dynamics of cardiac fibrillation" (arXiv title; published as "Extinction
  dynamics of spiral defect chaos"), Phys. Rev. E 99 (2019) 012407; https://arxiv.org/abs/1808.01991. Read: **abstract
  + the relevant sections in ar5iv HTML, through the fetch tool**. Square domains, periodic or non-conducting walls.
  "the W±1 rates scale with the perimeter L", which "implies that the death rate is proportional with the length of
  the non-conducting boundary". Tips are "removed through collisions with other spiral waves or with non-conducting
  boundaries". So the boundary is identified as the place where defects are lost, and the rates are rescaled by its
  length. No noise model of the bulk, and no thin-layer model of the exponent.
- W.-J. Rappel et al., "Stochastic termination of spiral wave dynamics in cardiac tissue", Front. Netw. Physiol. 2 (2022)
  809532; https://www.frontiersin.org/journals/network-physiology/articles/10.3389/fnetp.2022.809532/full —
  **full text, via the fetch tool**: "rescaling the ±1 rates by the total length L of the non-conducting boundary".
  Same caveat.
- Strain–Greenside (arXiv:chao-dyn/9710006, transient times exponential in size with no-flux walls) seen only as a
  search result.
Caveat for the write-up: the open-boundary death channel scaling with perimeter is published (Vidmar–Rappel), so "death
enters through the boundary" is not ours. What is still not found is the reduction itself (a thin boundary model
with a random interior that reproduces the lifetime).
Queries: works citing Carretero-González 1999 (Semantic Scholar list); "Noise can delay and advance the collapse" (not
found as such); chaotic transient lifetime stochastic model replacing chaotic dynamics with noise escape rate; "stable
chaos" CML transient random boundary noise injected; Lilienkamp–Parlitz transients; Vidmar–Rappel extinction.

#### 2. Shape of a periodic domain at fixed size: STANDS WITH CAVEATS (the systole sub-claim REFUTED)
"No dependence of a chaotic-transient, turbulent, nucleation or extinction lifetime on aspect ratio or twist at fixed
size" stands: nothing found. But "**any use of the systole as the controlling length for a lifetime**: not found" is
refuted, by a theorem and by a coding-theory result:
- F. R. Nardi, A. Zocca, "Tunneling behavior of Ising and Potts models in the low-temperature regime", arXiv:1708.09677
  (v2 2018; published in Stoch. Proc. Appl. per our memory, **not checked**). **Full text, §1–2.** Theorem 1.1: zero-field
  q-state Potts (q = 2: Ising) Metropolis dynamics on the K × L grid, β → ∞: lim β⁻¹ log E τ = Γ(Λ) with
  "Γ(Λ) := 2 min{K, L} + 2 if Λ has periodic boundary conditions, min{K, L} + 1 if Λ has open boundary conditions", and
  τ/Eτ → Exp(1). "the mixing time ... depends up to a constant factor on the smaller side length of Λ"; for
  semi-periodic boundaries "the exponent Γ(Λ) would be min{K + 2, 2L + 1}"; they "expect that analogous results hold
  also for rectangular regions Λ of other lattices (e.g. triangular, hexagonal, Kagome lattices)". On a rectangular
  torus the shorter side is the systole, so this is a proved, memoryless, exponential lifetime whose exponent is the
  systole, not the area: at fixed area K·L the lifetime grows as the torus is made squarer. It is the leading-order
  version of what Caselle–Gliozzi–Vinti see in the prefactor. Differences: reversible, zero temperature limit, the
  barrier is a straight interface across the short side; no twist; untwisted rectangles only.
- D. K. Tuckett, A. S. Darmawan, C. T. Chubb, S. Bravyi, S. D. Bartlett, S. T. Flammia, "Tailoring surface codes for highly
  biased noise", Phys. Rev. X 9 (2019) 041031; https://arxiv.org/abs/1812.08186 — **abstract**: under pure dephasing,
  for rectangular surface codes with open boundaries "it is controlled by the parameter g = gcd(j, k), where j and k are
  dimensions of the surface code lattice"; "the same logical failure rate achievable with a square surface code and n
  physical qubits can be obtained with a co-prime or rotated surface code using only O(√n) physical qubits". So the
  failure rate of a memory at (about) fixed size depends on the arithmetic of the lattice's shape, which is the nearest
  published analogue of a *twist* effect. Open boundaries, not a torus; logical failure, not a chaotic lifetime.
- Bombin–Martin-Delgado, Phys. Rev. A 76 (2007) 012305, arXiv:quant-ph/0703272 (ar5iv HTML, partly read): optimal toric
  codes with n/d² = 1 against the typical 2; the fetched text does not describe the construction as a twisted torus, so
  that reading is **not supported** by what was read.
- T. Lilienkamp, J. Christoph, U. Parlitz, "Features of chaotic transients in excitable media governed by spiral and
  scroll waves", Phys. Rev. Lett. 119 (2017) 054101; https://bmp.ds.mpg.de/publication/item-2471932/ — **abstract**:
  "In 3D, simulations exhibit an increase of transient lifetimes and filament lengths only above a critical thickness."
  A slab-thickness threshold for long transients, the same shape of statement as our conjecture that thin slabs cannot
  sustain chaos. Not a fixed-area shape test.
- Vidmar–Rappel 2019 and Rappel et al. 2022 (above): "the mean termination time depends on the geometry of the domain"
  (Rappel 2022), through the length of non-conducting boundary. Non-periodic; aspect ratio not studied ("The paper uses
  only square domains", per the fetch of Vidmar–Rappel).
- P. Manneville, "Spatiotemporal perspective on the decay of turbulence in wall-bounded flows", Phys. Rev. E 79 (2009)
  025301(R), arXiv:1102.5703 (ar5iv, via the fetch tool): domains "of various aspect ratios"; Lx and Lz are not separated
  for lifetimes and area is not held fixed. A miss.
Queries: Nardi–Zocca tunnelling torus; contact process extinction torus aspect ratio / thin torus / cylinder (nothing:
only random graphs and stars); plane Couette lifetime vs streamwise and spanwise size; transient chaos lifetime aspect
ratio same area spiral chaos; twisted toric codes / coprime surface codes; Lilienkamp thickness.

#### 3. Sealed sets: STANDS WITH CAVEATS (the object is classical)
No sentence found that states "the largest sealed set only grows" for a non-monotone rule. But the third pass missed
that the object is standard. Sealed = each cell has ≤ 3 of its 12 neighbours outside = each cell has ≥ 9 inside, so
**the largest dead sealed set K(t) is the 9-core of the dead cells**, equivalently the complement of the closure of the
live set under 4-neighbour bootstrap percolation (our reading, from the definitions). The k-core/bootstrap
complementarity is published:
- J. C. Miller, "Equivalence of several generalized percolation models on networks", Phys. Rev. E 94 (2016) 032313;
  https://arxiv.org/abs/1505.01396 — **full text, k-core and bootstrap sections**: with thresholds r_u = d_u − k + 1,
  "the set of activated nodes in the WTM is the set of deleted nodes in k-core percolation", "They are complementary
  processes", "This equivalence is previously known [2]".
- With it, T6's "no finite set is sealed" is the statement that 4-neighbour bootstrap percolation on this lattice has no
  closed cofinite proper subset, which is Gravner–Griffeath's defining property of *subcritical* (quoted above via
  Bollobás–Smith–Uzzell). The one-layer hexagon ring and two-layer 36-cell set make the thin slabs subcritical in that
  sense; thick slabs and 3D are not. And "K(t) only grows" is the usual comparison with the dominating monotone rule
  (our T5's uncapped "n + x ≥ 4"): the live set at t + 1 lies inside the bootstrap closure of the live set at t. These
  identifications are ours, not read anywhere; they are one line each from the definitions.
Recommendation: present T6 as "the 9-core of the dead set / the complement of the threshold-4 bootstrap closure", cite
Miller and Gravner–Griffeath (via Bollobás–Smith–Uzzell), and keep only the lattice-specific facts (hexagon ring,
36-cell set, three-layer threshold) as ours. Gravner–Griffeath's own papers and Balister–Bollobás–Przykucki–Smith
(arXiv:1311.5883, abstract only: does not define the classes) were not read in full.
Queries: bootstrap percolation complement k-core duality never-infected set; subcritical bootstrap closed cofinite;
plus the third pass's blocking-word queries re-run in part.

#### Also: lifetime from a stationary tail probability: STANDS, and much more widely known than said
"Lifetime = inverse of (exit rate × QSD mass of the last state)" is textbook in population extinction and has been used
on transient turbulence with a measured histogram:
- M. Assaf, B. Meerson, "WKB theory of large deviations in stochastic populations", J. Phys. A 50 (2017) 263001;
  https://arxiv.org/abs/1612.01470 — **full text, §2**: after relaxation "P_{n>0}(t ≫ t_r) ≃ π_n e^{−t/τ}", and "Once the
  QSD is known ... obtain the MTE from the relation 1/τ = Σ_{r>0} W_r(r) π_r" (eq. 6), with refs [27, 30, 32, 33, 35].
  The general form of our statement, for birth–death populations.
- I. Nåsell, *Extinction and Quasi-Stationarity in the Stochastic Logistic SIS Model* (Springer LNM 2022, 2011), ch.
  "Approximation of the time to extinction for the SIS model": per a search result, "the time to extinction from
  quasi-stationarity ... has an exponential distribution with expectation equal to" 1/(μ₁q₁). **Not obtained** (Springer
  login redirect); Nåsell's arXiv:2201.11118 (ar5iv) does not state it.
- Vidmar–Rappel 2019 (above), eq. (2): "1/τ = Σ_{r<0} W_r(−r) P_qs(−r)", i.e. W₋₁(1)P_qs(1) + W₋₂(2)P_qs(2), for the
  number of spiral tips of a deterministic reaction–diffusion system, with τ "exponentially" growing "with the area".
  The same structure as Sugimura–Kori, made a birth–death master equation, and **validated against direct simulation**.
- T. Nemoto, A. Alexakis, "Do extreme events trigger turbulence decay? A numerical study of turbulence decay time in pipe
  flows", J. Fluid Mech. 912 (2021) A38; https://arxiv.org/abs/2005.03530 — **full text, §3**: with P(h) the measured
  probability that the maximum turbulence intensity is ≤ h, "the number of decay events n_d is equal to N P(h_th)",
  so "the decay time τ_d ≡ (Nδt)/n_d is expressed as (Nemoto & Alexakis 2018) τ_d = δt / P(h_th)" (eq. 3.5). This is the
  closest precedent to our measured statement: a deterministic chaotic transient whose lifetime is the inverse of the
  measured probability of the last state below threshold, and they then study the shape of that tail
  (Gumbel) in a Re-independent "hovering" region. Differences: a continuous intensity, not a count down to one cell;
  an empirical identity on the sampled distribution rather than a separate check of rate against tail.
- N. Goldenfeld, N. Guttenberg, G. Gioia, "Extreme fluctuations and the finite lifetime of the turbulent state", Phys. Rev.
  E 81 (2010) 035304(R); https://arxiv.org/abs/0906.3572 — **abstract**: "the transition to turbulence is controlled by
  large amplitude events that follow extreme distribution theory"; the lifetime as set by the maximum fluctuation falling
  below a threshold (as summarised by Nemoto–Alexakis).
Consequence: our "death rate = the next point of the stationary tail" should be presented as an instance of the
QSD-flux identity, with Sugimura–Kori, Vidmar–Rappel and Nemoto–Alexakis as precedents in deterministic spatially
extended systems. What is left as ours is the lattice count measured to one cell with the exit rate measured, in a
deterministic automaton.

#### Not obtained
Citation lists of Houghton et al. 2010 and Sugimura–Kori 2015 (Semantic Scholar HTTP 429, four tries); Nåsell's book
chapter (Springer login); Lilienkamp et al. 2017 full text (no open copy found); Nemoto–Alexakis 2018 (cited, not
sought); Wackerbauer–Kobayashi 2007 (title not found by search); Tél–Lai 2008 and Tél 2015 (not retried).

#### Not searched
Pipe-flow puff lifetime against periodic pipe length; Kuramoto–Sivashinsky lifetime papers; Gray–Scott beyond
Wackerbauer–Showalter; anisotropic-Ising and in-field nucleation on rectangular tori (the Nardi–Zocca reference list
was not followed: Borgs–Chayes–Tetali 2012 on Swendsen–Wang mixing "for a more general d-dimensional grid" is the next
lead); quantum-memory lifetime reviews (Brown et al.); Boolean-network frozen cores and trap spaces (a probable further
home for sealed sets); emptiness formation; non-English literature.
