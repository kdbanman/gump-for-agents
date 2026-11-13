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
