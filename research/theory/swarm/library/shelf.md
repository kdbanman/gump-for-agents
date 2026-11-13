# The shelf

_Kept by the librarian. One line per source. "Read" says how far: **whole** / **statements** (the theorems and
the sections around them) / **abstract** / **not obtained**. Notes files are in `notes/`. Nothing here is
from memory: where a fact comes from a secondary source the notes say which._

How to read the notes: each statement is tagged [paper], [secondary: X] or [abstract]. Each file ends with
"Does it apply here?" and "Corrections to this repository".

## 1. Finite contact process and relatives (extinction time exponential in size)

| source | where read | read | notes | why it matters |
|---|---|---|---|---|
| R. Durrett, X.-F. Liu, "The contact process on a finite set", Ann. Probab. 16 (1988) 1158–1173 | https://sites.math.duke.edu/~rtd/reprints/paper39.pdf (author's reprint, scan) | statements + proofs of Thms 1, 2, 4 | `contact-finite.md` §1 | d = 1: log σ_N between (α/2)N and βN; the upper bound uses only monotonicity, the lower bound duality |
| R. Durrett, R. H. Schonmann, "The contact process on a finite set. II", Ann. Probab. 16 (1988) 1570–1583 | https://sites.math.duke.edu/~rtd/reprints/paper42.pdf (scan) | statements + most proofs | `contact-finite.md` §2 | d = 1: (log σ_N)/N → γ₂; σ_N/β_N → exponential; planar duality |
| T. S. Mountford, "A metastable result for the finite multidimensional contact process", Canad. Math. Bull. 36 (1993) 216–226 | https://doi.org/10.4153/CMB-1993-031-3 (open PDF) | whole (one lemma's proof skimmed) | `contact-finite.md` §3 | d ≥ 2: τ/Eτ → exponential; Prop. 1.2 is a general criterion "fast regeneration ⇒ memoryless" |
| T. S. Mountford, "Existence of a constant for finite system extinction", J. Statist. Phys. 96 (1999) 1331–1341 | https://link.springer.com/article/10.1023/A:1004652719999 | abstract (paywalled) | `contact-finite.md` §4 | log Eτ_n / n^d → γ: the "exponential in volume" theorem |
| T. Mountford, J.-C. Mourrat, D. Valesin, Q. Yao, "Exponential extinction time of the contact process on finite graphs", arXiv:1203.2972 | https://arxiv.org/abs/1203.2972 | statements (intro) | `contact-finite.md` §5 | Eτ ≥ e^{cn} on every bounded-degree connected graph with n sites, λ > λ_c(Z) |
| B. Schapira, D. Valesin, "Extinction time for the contact process on general graphs", arXiv:1509.04133 | https://arxiv.org/abs/1509.04133 | statements, tools of §2 | `contact-finite.md` §6 | shortest proof of e^{cn}: coupling + supermultiplicativity over pieces |
| M. Cassandro, A. Galves, E. Olivieri, M. E. Vares, "Metastable behavior of stochastic dynamics: a pathwise approach", J. Statist. Phys. 35 (1984) 603–634 | https://link.springer.com/article/10.1007/BF01010826 | abstract (paywalled) | `contact-finite.md`, corrections | origin of the exponential limit law (d = 1, large λ) |
| R. H. Schonmann, "Metastability for the contact process", J. Statist. Phys. 41 (1985) 445–464 | https://link.springer.com/article/10.1007/BF01009017 | abstract (paywalled) | `contact-finite.md`, corrections | the limit law for all λ > λ_c (d = 1) |
| R. Durrett, R. H. Schonmann, "Large deviations for the contact process and two dimensional percolation", Probab. Theory Related Fields 77 (1988) 583–603 | https://sites.math.duke.edu/~rtd/reprints/paper43.pdf | statements | `ld-contact-percolation.md` | a proved "area above, perimeter below" dichotomy; empty interval costs e^{−cn} under the contact process's stationary law |

## 2. Non-monotone systems with an absorbing state; the block construction

| source | where read | read | notes | why it matters |
|---|---|---|---|---|
| R. Durrett, "Ten lectures on particle systems", Saint-Flour 1993, Lecture Notes in Math. 1608 (1995) 97–201 | https://sites.math.duke.edu/~rtd/reprints/paper85.pdf (author's reprint) | §4 statements | `nonmonotone.md` §1 | the comparison theorem with oriented percolation, stated without monotonicity; what it needs instead |
| M. Bramson, C. Neuhauser, "Survival of one-dimensional cellular automata under random perturbations", Ann. Probab. 22 (1994) 244–263 | https://doi.org/10.1214/aop/1176988858 | **not obtained** (Project Euclid refuses automated clients); two secondary accounts | `nonmonotone.md` §2 | survival of the mod-2 automaton with small deaths: the one non-monotone CA survival theorem on the list |
| M. Bramson, W.-D. Ding, R. Durrett, "Annihilating branching processes", Stochastic Process. Appl. 37 (1991) 1–17 | https://sites.math.duke.edu/~rtd/reprints/paper59.pdf | §1–2 | `nonmonotone.md` §3 | a non-monotone process shown to survive by a block construction; cancellative duality; product measure ½ stationary |
| S. Chatterjee, R. Durrett, "Persistence of activity in threshold contact processes, an 'annealed approximation' of random Boolean networks", Random Structures Algorithms 39 (2011) 228–246; arXiv:0911.5339 | https://arxiv.org/abs/0911.5339 | §1 (theorems) | `nonmonotone.md` §4 | lifetime e^{cn} for a dice model of a deterministic network; the model is monotone |
| T. Mountford, D. Valesin, "Supercriticality of annealed approximations of Boolean networks", arXiv:1007.0862 | https://arxiv.org/abs/1007.0862 | abstract, §1 | `nonmonotone.md` §4 | the same with the sharp condition qr > 1 |
| R. Durrett, "Interacting particle systems: ideas, techniques, applications" (book draft, 2 Sept 2026) | https://sites.math.duke.edu/~rtd/PASTA/PASTAcon.html | contents; text searched for two topics | `nonmonotone.md`, last section | current textbook account of block constructions; nothing found on finite non-attractive lifetimes |

## 5. Algebraic and permutive automata as random sources

| source | where read | read | notes | why it matters |
|---|---|---|---|---|
| M. A. Shereshevsky, "Ergodic properties of certain surjective cellular automata", Monatsh. Math. 114 (1992) 305–316 | https://eudml.org/doc/178592 (scan at GDZ Göttingen) | abstract, §1–2 statements | `algebraic-ca.md` §1a | bipermutative ⇒ conjugate to one-sided full shift (credited to Shereshevsky–Afraimovich); Bernoulli, K, k-mixing; a non-ergodic permutative example |
| M. Sablik, "Measure rigidity for algebraic bipermutative cellular automata", Ergodic Theory Dynam. Systems 27 (2007) | https://www.math.univ-toulouse.fr/~msablik/article/2007-etds.pdf (author's copy) | §1, part of §2 | `algebraic-ca.md` §1b, §6 | writes the conjugacy out: columns of width t = r − l |
| M. Pivato, "Invariant measures for bipermutative cellular automata", arXiv:math/0306211 | https://arxiv.org/abs/math/0306211 | §1–2, conclusion | `algebraic-ca.md` §1b, §6 | one-sided column conjugacy (Lemma 8); rigidity of the uniform measure |
| D. A. Lind, "Applications of ergodic theory and sofic systems to cellular automata", Physica D 10 (1984) 36–44 | https://sites.math.washington.edu/~lind/Papers/ApplicationsToCA.pdf (author's copy, scan) | §1–4 | `algebraic-ca.md` §2 | mod-2 rule: exact pattern frequencies a.e.; Cesàro convergence of Bernoulli measures to Haar, no plain convergence |
| P. A. Ferrari, A. Maass, S. Martínez, P. Ney, "Cesàro mean distribution of group automata starting from measures with summable decay", Ergodic Theory Dynam. Systems (2000); arXiv:math/9912135 | https://arxiv.org/abs/math/9912135 | abstract, §1 | `algebraic-ca.md` §3 | randomisation from non-product initial laws under a ratio-type decay condition |
| M. Pivato, R. Yassawi, "Limit measures for affine cellular automata", Ergodic Theory Dynam. Systems 22 (2002) 1269–1287; arXiv:math/0108082 | https://arxiv.org/abs/math/0108082 | §1, definitions, Thms 12, 15 | `algebraic-ca.md` §4 | harmonic mixing + diffusion ⇒ convergence to Haar, in every dimension D ≥ 1 |
| I. Marcovici, M. Sablik, S. Taati, "Ergodicity of some classes of cellular automata subject to noise", Electron. J. Probab. 24 (2019) paper 41; arXiv:1712.05500 | https://arxiv.org/abs/1712.05500 | §1–2, statements of Thms 3.16, 5.1 | `algebraic-ca.md` §5, `pca.md` | permutive rule + doubly stochastic noise is exponentially ergodic in every window; secondary source for Bramson–Neuhauser |
| M. A. Shereshevsky, V. S. Afraimovich, "Bipermutative cellular automata are topologically conjugate to the one-sided Bernoulli shift", Random Comput. Dynam. 1 (1992) | — | **not obtained** | `algebraic-ca.md` §1a | the original of the conjugacy theorem |
| R. Kleveland, "Mixing properties of one-dimensional cellular automata", Proc. Amer. Math. Soc. 125 (1997) 1755–1766 | ams.org | **not obtained** (AMS site refuses automated clients) | `algebraic-ca.md`, corrections | listed by the lead; content unverified |
| M. Pivato, "Ergodic theory of cellular automata", in Encyclopedia of Complexity and Systems Science (Springer 2009) | DOI 10.1007/978-0-387-30440-3_178 | **not obtained** (not open) | `algebraic-ca.md`, corrections | the survey; primary papers used instead |

## 4. Escape rates, holes, hitting times

| source | where read | read | notes | why it matters |
|---|---|---|---|---|
| A. Galves, B. Schmitt, "Occurence times of rare events for mixing dynamical systems", Ann. Inst. H. Poincaré Phys. Théor. 52 (1990) 267–281 | https://www.numdam.org/item/AIHPA_1990__52_3_267_0/ | statement, start of proof | `escape-rates.md` A1 | deterministic map + ratio (ψ) mixing ⇒ hitting time of D_n is exponential in law with scale e^{θn}: the published form of the board's lemma |
| M. Abadi, B. Saussol, "Hitting and returning into rare events for all alpha-mixing processes", arXiv:1003.4856 | https://arxiv.org/abs/1003.4856 | §1–3 statements | `escape-rates.md` A2 | exponential law under α-mixing alone; the scale is λ(A)μ(A) |
| M. Abadi, J.-R. Chazottes, F. Redig, E. Verbitskiy, "Exponential distribution for the occurrence of rare patterns in Gibbsian random fields", arXiv:math/0310355 (Commun. Math. Phys.) | https://arxiv.org/abs/math/0310355 | abstract, §2 to Remark 2.8 | `escape-rates.md` A3 | d ≥ 2: pattern probabilities ≤ e^{−c n^d} by the Gibbs property; ψ-mixing is too strong in 2D |
| M. Demers, L.-S. Young, "Escape rates and conditionally invariant measures", Nonlinearity 19 (2006) 377–397 | https://www.cims.nyu.edu/~lsy/papers/holes.pdf (author's copy) | §1–3, part of §5 | `escape-rates.md` B1 | definitions; non-uniqueness; existence criterion ⇒ none in a finite deterministic system |
| G. Pianigiani, J. A. Yorke, "Expanding maps on sets which are almost invariant: decay and chaos", Trans. Amer. Math. Soc. 252 (1979) 351–366 | ams.org | **not obtained** (AMS site refuses automated clients); via Demers–Young | `escape-rates.md` B1 | origin of conditionally invariant measures |
| G. Keller, C. Liverani, "Rare events, escape rates and quasistationarity: some exact formulae", arXiv:0810.2229 | https://arxiv.org/abs/0810.2229 | §1–3.1, §5.2 | `escape-rates.md` B2 | escape rate = μ(hole) × (1 − immediate-return factor) to first order |
| L. A. Bunimovich, A. Yurchenko, "Where to place a hole to achieve a maximal escape rate", arXiv:0811.4438 | https://arxiv.org/abs/0811.4438 | abstract, statements | `escape-rates.md` B3 | full shift, word holes: equal measure, different rates, ordered by recurrence time, at all finite times |
| A. Ferguson, M. Pollicott, "Escape rates for Gibbs measures", arXiv:1009.0086 | https://arxiv.org/abs/1009.0086 | §1, Thms 5.1, 5.3, Cor. 5.4 | `escape-rates.md` B4 | the same for subshifts of finite type with Gibbs measures; entropy drop |

## Requests from the source line (2026-11-13)

| source | where read | read | notes | why it matters |
|---|---|---|---|---|
| O. Tamuz, R. J. Tessler, "Majority dynamics and the retention of information", Israel J. Math. 206 (2015) 483–507; arXiv:1307.4035 | https://arxiv.org/abs/1307.4035 | §1, §3.1 | `source-requests.md` §2 | majority dynamics on infinite graphs of slow growth: period ≤ 2, explicit bound on the number of changes per vertex |
| G. Moran, "On the period-two-property of the majority operator in infinite graphs", Trans. Amer. Math. Soc. 347 (1995) 1649–1667 | ams.org | **not obtained** (bot wall); via Tamuz–Tessler | `source-requests.md` §2 | the original infinite-graph theorem |
| Y. Ginosar, R. Holzman, "The majority action on infinite graphs: strings and puppets", Discrete Math. 215 (2000) 59–72 | sciencedirect.com | **not obtained** (bot wall); via Tamuz–Tessler | `source-requests.md` §2 | the strengthened theorem |
| R. Impagliazzo, N. Nisan, A. Wigderson, "Pseudorandomness for network algorithms", STOC 1994 | https://www.cs.huji.ac.il/~noam/prcc.ps (author's copy; text extracted crudely from PostScript) | §1, §4.1 | `source-requests.md` §3 | generator with seed O((S + log(n/ε)) log n) fooling space-S machines that read their random tape boundedly often |
| N. Nisan, "RL ⊆ SC", Comput. Complexity 4 (1994) 1–11 | https://www.cs.huji.ac.il/~noam/sc.ps (author's copy; same) | §2, §4.1 | `source-requests.md` §3 | restates the 1992 generator and its hashing lemma |
| N. Nisan, "Pseudorandom generators for space-bounded computation", Combinatorica 12 (1992) 449–461 | — | **not obtained**; via the two above and Vadhan | `source-requests.md` §3 | the original |
| S. Vadhan, *Pseudorandomness*, Found. Trends Theor. Comput. Sci. 7 (2012) | https://people.seas.harvard.edu/~salil/pseudorandomness/ (author's copy) | §6.1, §8.2.1 | `source-requests.md` §3–4 | statements of Nisan's theorem and of Santha–Vazirani sources |
| O. Häggström, J. Jonasson, "Uniqueness and non-uniqueness in percolation theory", Probab. Surv. 3 (2006) 289–344; arXiv:math/0612812 | https://arxiv.org/abs/math/0612812 | Definition 12.1 and footnote | `source-requests.md` §4 | definition of finite energy, insertion and deletion tolerance |
| C. Temmel, "Shearer's measure and stochastic domination of product measures", J. Theoret. Probab. (2012); arXiv:1105.1683 | https://arxiv.org/abs/1105.1683 | §1–2, Theorem 5 | `source-requests.md` §4 | states the Liggett–Schonmann–Stacey hypothesis and theorem |
| A. Bušić, J. Mairesse, I. Marcovici, "Probabilistic cellular automata, invariant measures, and perfect sampling", arXiv:1010.3133 | https://arxiv.org/abs/1010.3133 | Definition 2.2, algorithm data | `source-requests.md` §1 | a PCA as a deterministic local function of an i.i.d. space-time array |

## 3. Supertransients and stable chaos (closest prior art to the phenomenon; all numerical)

| source | where read | read | notes | why it matters |
|---|---|---|---|---|
| J. P. Crutchfield, K. Kaneko, "Are attractors relevant to turbulence?", Phys. Rev. Lett. 60 (1988) 2715–2718 | https://csc.ucdavis.edu/~chaos/chaos/pubs/aart-title.html (author's page) | abstract (article behind APS bot wall) | `supertransients.md` §1 | origin: turbulent transients lasting "faster than exponentially" in the system volume |
| A. Politi, A. Torcini, "Stable chaos", arXiv:0902.2545 | https://arxiv.org/abs/0902.2545 | §1, §3 (start), §4 (start) | `supertransients.md` §2 | CA-like coupled maps: transient exponential in size; explicit analogy with chaotic cellular automata |
| S. M. Houghton, E. Knobloch, S. M. Tobias, M. R. E. Proctor, "Transient spatiotemporal chaos in the complex Ginzburg–Landau equation on long domains", Phys. Lett. A 374 (2010) 2030–2034 | https://eprints.whiterose.ac.uk/10731/ (university repository) | abstract, intro, lifetime results, conclusion | `supertransients.md` §3 | τ(L) = exp(AL + B), Poisson lifetimes, collapse only with non-periodic boundaries; reports Wackerbauer–Showalter and Tél–Lai |
| T. Tél, Y.-C. Lai, "Chaotic transients in spatially extended systems", Phys. Rep. 460 (2008) 245–275 | sciencedirect.com | **not obtained** | `supertransients.md` §4 | the review; presumably where the heuristic is written out |
| R. Wackerbauer, K. Showalter, "Collapse of spatiotemporal chaos", Phys. Rev. Lett. 91 (2003) 174103 | journals.aps.org | **not obtained**; via Houghton et al. | `supertransients.md` §3–4 | exponential lifetime in reaction–diffusion systems |
| K. Kaneko, "Supertransients, spatiotemporal intermittency and stability of fully developed spatiotemporal chaos", Phys. Lett. A 149 (1990) 105 | — | **not obtained**; citation unverified | `supertransients.md` §4 | origin of the word |

## 6. Probabilistic cellular automata

| source | where read | read | notes | why it matters |
|---|---|---|---|---|
| J. L. Lebowitz, C. Maes, E. R. Speer, "Statistical mechanics of probabilistic cellular automata", J. Statist. Phys. 59 (1990) 117–170 | https://link.springer.com/article/10.1007/BF01015566 | abstract (paywalled) | `pca.md` §1 | space-time histories of a PCA as a Gibbs state in d + 1 dimensions; large deviations; high-noise uniqueness |
| I. Marcovici, M. Sablik, S. Taati (as in section 5) | https://arxiv.org/abs/1712.05500 | §2.2–2.4, §3.2 | `pca.md` §2 | explicit high-noise criterion p_? < p_c(N) by comparison with directed percolation |
| J. Mairesse, I. Marcovici, "Around probabilistic cellular automata", Theoret. Comput. Sci. 559 (2014) | sciencedirect.com; hal-01194762 (no file) | **not obtained** | `pca.md` §3 | the survey |

## 7. Threshold networks

| source | where read | read | notes | why it matters |
|---|---|---|---|---|
| C. J. Kuhlman, H. S. Mortveit, D. Murrugarra, V. S. A. Kumar, "Bifurcations in Boolean networks", arXiv:1108.2974 | https://arxiv.org/abs/1108.2974 | intro, §3.1, appendix (statement) | `threshold-networks.md` | English statement of the Goles–Olivos period-two theorem for a real symmetric matrix; bi-threshold extension |
| E. Goles, P. Montealegre, M. Ríos-Wilson, S. Sené, "Dynamical stability of threshold networks over undirected signed graphs", arXiv:2309.01854 | https://arxiv.org/abs/2309.01854 | §4.1 | `threshold-networks.md` | attributions of period two and of the energy |
| E. Goles, J. Olivos, "Periodic behaviour of generalized threshold functions", Discrete Math. 30 (1980) 187–189; and "Comportement périodique des fonctions à seuil binaires et applications", Discrete Appl. Math. 3 (1981) 93–105 | sciencedirect.com | **not obtained** (bot wall) | `threshold-networks.md` | the primaries behind T5 |
| E. Goles-Chacc, F. Fogelman-Soulié, D. Pellegrin, "Decreasing energy functions as a tool for studying threshold networks", Discrete Appl. Math. 12 (1985) 261–277 | sciencedirect.com | **not obtained** | `threshold-networks.md` | the energy and transient bounds; the 26N + 1 bound in T5 is unverified against it |
| E. Goles, S. Martínez, *Neural and Automata Networks* (Kluwer 1990) | — | **not obtained** (book) | `threshold-networks.md` | — |

## 8. Quasi-stationary distributions

| source | where read | read | notes | why it matters |
|---|---|---|---|---|
| S. Méléard, D. Villemonais, "Quasi-stationary distributions and population processes", Probab. Surv. 9 (2012) 340–410; arXiv:1112.4732 | https://arxiv.org/abs/1112.4732 | §2.1, §3 | `qsd.md` | QSD ⇔ QLD; exact exponential law from a QSD; finite-state existence and uniqueness; relaxation versus extinction time |
| J. N. Darroch, E. Seneta, "On quasi-stationary distributions in absorbing discrete-time finite Markov chains", J. Appl. Probab. 2 (1965) 88–100 | — | **not obtained**; via Méléard–Villemonais | `qsd.md` | the original finite-chain theorem |
| P. Collet, S. Martínez, J. San Martín, *Quasi-Stationary Distributions* (Springer 2013) | — | **not obtained** (book) | `qsd.md` | — |

## Could not be reached at all (for whoever has a browser)

Project Euclid (bot wall): Bramson–Neuhauser 1994; Liggett–Schonmann–Stacey 1997; Abadi 2004.
ams.org (bot wall): Pianigiani–Yorke 1979; Kleveland 1997; Moran 1995.
sciencedirect.com (bot wall): Tél–Lai 2008; Kaneko 1990; Goles–Olivos 1980, 1981; Goles et al. 1985;
Ginosar–Holzman 2000; Mairesse–Marcovici 2014. journals.aps.org (bot wall): Crutchfield–Kaneko 1988;
Wackerbauer–Showalter 2003. Paywalled: Mountford 1999; Cassandro et al. 1984; Schonmann 1985;
Lebowitz–Maes–Speer 1990; Nisan 1992; Pivato's survey; the books. The first three groups are open access to a
person; I did not try to get round the walls.
