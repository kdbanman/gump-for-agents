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
