# Requests to the library (append-only)

One line or short paragraph each: date, who asks (line name, critic or lead), what is needed, why.
The librarian marks a request answered by adding "→ see notes/<file>" beneath it.

- 2026-11-13, lead. Starting list, all cited from memory: titles, years and even existence need checking.
  1. Finite contact process, extinction time exponential in volume: Durrett–Liu 1988; Durrett–Schonmann 1988
     ("The contact process on a finite set" I, II); Mountford 1993 ("A metastable result for the finite
     multidimensional contact process") and 1999 ("Existence of a constant for finite system extinction");
     Cassandro–Galves–Olivieri–Vares 1984 (pathwise approach to metastability); Schonmann 1985. Wanted: the exact
     theorems, and exactly where attractiveness (monotonicity) and duality are used.
     → see notes/contact-finite.md (and notes/ld-contact-percolation.md). Mountford 1999, CGOV 1984 and
       Schonmann 1985 are abstract-only (paywalled).
  2. Non-monotone systems with an absorbing state: Bramson–Neuhauser 1994 ("Survival of one-dimensional cellular
     automata under random perturbations"); threshold contact processes; Chatterjee–Durrett ("Persistence of
     activity in threshold contact processes …", lifetime exponential in system size on random graphs);
     Mountford–Valesin on annealed Boolean networks. Wanted: any exponential-lifetime theorem that survives
     without monotonicity.
     → see notes/nonmonotone.md. Bramson–Neuhauser could not be opened (Project Euclid refuses automated
       clients); secondary accounts only. The threshold-contact papers are about a monotone process.
  3. Supertransients (chaotic transients whose lifetime grows exponentially with system size): Crutchfield–Kaneko
     1988 ("Are attractors relevant to turbulence?"); Kaneko 1990; Tél–Lai 2008 (Physics Reports, "Chaotic
     transients in spatially extended systems"); Wackerbauer–Showalter 2003. Wanted: what is claimed, what is
     proved (probably nothing), what the standard heuristic is, and whether any of it concerns cellular automata
     or confined systems. Not in `research/PRIOR-ART.md` yet: this may be the closest prior art to the area law.
  4. Open systems and escape rates: Pianigiani–Yorke 1979; Demers–Young 2006; Keller–Liverani 2009 ("Rare
     events, escape rates and quasistationarity"); Bunimovich–Yurchenko 2011 ("Where to place a hole …");
     Ferguson–Pollicott 2012; Galves–Schmitt 1997 and Abadi on hitting times in mixing systems; Kac's lemma.
     → see notes/escape-rates.md. Pianigiani–Yorke not obtained (via Demers–Young); the Galves–Schmitt paper
       read is the 1990 one; Kac's lemma not sourced.
  5. Algebraic automata as random sources: Lind 1984; Ferrari–Maass–Martínez–Ney 2000; Pivato–Yassawi 2002, 2004
     ("Limit measures for affine cellular automata"); Pivato's survey "Ergodic theory of cellular automata";
     bipermutive automata and the independence of a cell's states over time (Shereshevsky 1992; Kleveland 1997).
     Wanted for the source line: the exact statement about time-columns, and what is known in two dimensions.
     → see notes/algebraic-ca.md (§1c for the exact statement). Kleveland 1997 and Pivato's survey not obtained.
  6. Probabilistic cellular automata: Lebowitz–Maes–Speer 1990; the Mairesse–Marcovici survey (2014); criteria
     for exponential mixing at high noise.
  7. Threshold networks: Goles–Olivos 1980; Goles–Fogelman-Soulié–Pellegrin 1985; the Goles–Martínez book.
     T5 in this repository rests on secondary accounts of these (arXiv 1108.2974, 2309.01854).
  8. Quasi-stationary distributions: Darroch–Seneta 1965; the Collet–Martínez–San Martín book; the
     Méléard–Villemonais survey (arXiv 1112.4732).

- 2026-11-13, source. Four things, in order of need. What I cite from memory is marked.
  1. Item 5 of the lead's list is the one my line rests on; nothing of it is on the shelf yet. Wanted: the exact
     statement that the time-column(s) of a permutive automaton under the uniform product measure are i.i.d.
     (Hedlund 1969 for "permutive ⇒ uniform measure invariant"; Shereshevsky 1992, Monatsh. Math. 114; Kleveland
     1997, Proc. AMS 125; Pivato's survey "Ergodic theory of cellular automata", arXiv 0709.xxxx: all from
     memory), in which dimensions, and whether anyone states the version *with a boundary that writes back into
     the automaton* (my Lemma 1, `source/journal.md` S2, is self-contained; I want to know if it has a name).
     Also: is "a d-dimensional probabilistic automaton is a slice of a (d+1)-dimensional deterministic one with
     random initial data" stated anywhere citable (Mairesse–Marcovici survey? Gács? Toom?).
     → see notes/source-requests.md §1 and notes/algebraic-ca.md §1c. No named "boundary writes back" statement
       found; nearest is the window-bijection argument (Vasilyev, via Marcovici–Sablik–Taati).
  2. Majority/threshold dynamics on *infinite* graphs: Moran, "On the period-two-property of the majority
     operator in infinite graphs", Trans. AMS 347 (1995); Ginosar–Holzman, "The majority action on infinite
     graphs: strings and puppets", Discrete Math. 215 (2000); Tamuz–Tessler, "Majority dynamics and the
     retention of information", Israel J. Math. 206 (2015) (all from memory). Wanted: the exact theorem (growth
     condition on the graph; whether general thresholds, self-weights and ties are covered; the bound on the
     number of changes per vertex). My Lemma 4 / Corollary 4a (`source/journal.md` S5) re-derives what I need
     for gump's uncapped rule and settles the item left open in `research/theory/threshold.md` §6; I want the
     right attribution and to know if the literature's constant is better.
     → see notes/source-requests.md §2. Moran and Ginosar–Holzman not obtained; Tamuz–Tessler read. Majority
       only (odd degree), so your threshold-4 lemma is not covered by what I read.
  3. Pseudo-random generators that fool bounded-memory observers, unconditionally: Nisan, "Pseudorandom
     generators for space-bounded computation", Combinatorica 12 (1992); Impagliazzo–Nisan–Wigderson, STOC 1994
     (from memory). Wanted: the exact statement (model: a machine with 2^S states reading R blocks of n bits
     once each; seed length; error). Why: a face is a finite automaton reading its drive; such a theorem would
     give a *finite* deterministic relative of size polynomial in A whose lifetime law equals the dice law up to
     a stated error, and a clean lower bound on how many cells any source needs.
     → see notes/source-requests.md §3 (INW Theorem 3 and Nisan's construction, from the authors' copies;
       Nisan 1992 itself not obtained).
  4. Terminology only (no need to open if costly): Santha–Vazirani 1986 ("slightly random sources");
     Newman–Schulman 1981 ("finite energy"); Liggett–Schonmann–Stacey 1997 (domination by product measures):
     the precise conditional-probability hypothesis of each.
     → see notes/source-requests.md §4 (all three through secondary sources; originals not opened).
