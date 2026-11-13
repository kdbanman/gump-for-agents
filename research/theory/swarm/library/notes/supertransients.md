# Supertransients: chaotic transients whose lifetime grows exponentially with system size

Request (lead, item 3): what is claimed, what is proved, the standard heuristic, and whether any of it
concerns cellular automata or confined systems. Tags: **[paper]**, **[secondary: X]**, **[abstract]**.

**Short answer.** The phenomenon the repository calls the area law (a spatially extended deterministic system
is chaotic for a time exponential in its size, then collapses abruptly, with an exponential distribution of
lifetimes) is a named, twenty-five-year-old **numerical** observation in physics: *supertransients*
(coupled map lattices, reaction–diffusion systems, Ginzburg–Landau, Kuramoto–Sivashinsky, pipe flow) and
*stable chaos* (cellular-automaton-like coupled maps). In what I could read, **nothing is proved**; every
statement is a fit to simulations. The primary sources the lead listed are all behind publisher walls; I read
one author's abstract and two open papers that report them.

---

## 1. Crutchfield and Kaneko 1988

J. P. Crutchfield and K. Kaneko, "Are attractors relevant to turbulence?", Phys. Rev. Lett. 60 (1988),
2715–2718. **Abstract only**, from the first author's page
(https://csc.ucdavis.edu/~chaos/chaos/pubs/aart-title.html); the article is at journals.aps.org, which
refuses automated clients.

**[abstract]** "Spatially extended systems generically exhibit long transients that preclude observation of
the behavior governed by the asymptotic invariant measure. Even if the local dynamics is periodic, when it is
coupled into a spatial system complex 'turbulent' behavior can exist for times that grow faster than
exponentially with increasing system volume. The nature of the attractor is irrelevant to the observed
behavior when such systems are of even moderate size."

Note "faster than exponentially" and "volume". A companion abstract on the same page (Crutchfield, "Subbasins,
portals, and mazes: transients in high dimensions", Nucl. Phys. B (Proc. Suppl.) 5A (1988), 287–292) says the
observed complexity "depends on the basin structure in a high-dimensional state space" and distinguishes
stationary from non-stationary transients.

## 2. Politi and Torcini 2009 (review of "stable chaos"): the cellular-automaton connection

A. Politi and A. Torcini, "Stable chaos", arXiv:0902.2545v1 (2009; a chapter in *Nonlinear Dynamics and Chaos:
Advances and Perspectives*, Springer). Read: arXiv PDF, §1, the start of §3, §4 (first page), conclusions.

**[paper]**
- Stable chaos: "stochastic-like behaviour accompanied by a negative maximum Lyapunov exponent" in coupled-map
  lattices, first seen in Crutchfield–Kaneko 1988 and Politi–Livi–Oppo–Kapral (Europhys. Lett. 22 (1993) 571).
  "The irregular behaviour is a transient phenomenon … the transient duration diverges exponentially with the
  system size and is therefore infinite in the thermodynamic limit." It is "a generalization of the chaotic
  behaviour exhibited by cellular automata to continuous-variable systems".
- §3: "long-lasting transients followed by a sudden convergence towards some periodic orbit"; "the average
  (over different choices of the initial conditions) transient time may increase exponentially with the chain
  length" (their Fig. 1, a fit); during the transient "temporal correlations decay exponentially".
- §4: "in a finite lattice, any CA rule must eventually produce a periodic orbit, since the number of distinct
  states is finite … What makes a chaotic rule different from an ordered one is precisely the time needed to
  cycle through previously visited states: such a time is exponentially long in chaotic rules" (citing
  Wolfram's collection; no theorem).
- On mechanism: "chaotic transients are almost by definition the manifestation of trajectories evolving in
  the vicinity of a repeller, possibly characterized by a small escape rate" (citing Tél–Lai); for stable
  chaos "one must still heavily rely on direct numerical simulations". Standard chaotic transients (positive
  Lyapunov exponent) and stable chaos (negative) are distinguished.

## 3. Houghton, Knobloch, Tobias and Proctor 2010: exponential lifetimes, Poisson statistics, and boundaries

S. M. Houghton, E. Knobloch, S. M. Tobias and M. R. E. Proctor, "Transient spatiotemporal chaos in the complex
Ginzburg–Landau equation on long domains", Phys. Lett. A 374 (2010), 2030–2034. Read: authors' version in the
White Rose university repository, https://eprints.whiterose.ac.uk/10731/ (abstract, introduction, results on
lifetimes, conclusion).

**[paper]** (all numerical)
- With periodic boundary conditions the chaos persists; with Neumann (non-periodic) boundary conditions, in the
  same parameter regime, "chaos takes the form of a long-lived transient decaying to a spatially uniform
  oscillatory state. The lifetime of the transient has Poisson statistics and no domain length is found
  sufficient for persistent chaos."
- Survival function P(t, L) = exp(−(t − t₀)/τ(L)) fits each L; least squares gives τ(L) = exp(AL + B) with
  A = 0.066, B = 3.036 at one parameter value (L = domain length; one space dimension).
- The defect production rate "falls to zero at each boundary"; the boundary layer has a thickness independent
  of L. At other parameters the transient time grows only algebraically with L.
- **[secondary: this paper on the literature]** In reaction–diffusion systems (Wackerbauer and Showalter,
  "Collapse of spatiotemporal chaos", Phys. Rev. Lett. 91 (2003) 174103; Wackerbauer, Phys. Rev. E 76 (2007)
  056207) "detailed simulations have revealed that observed spatio-temporal chaos in one spatial dimension has
  a lifetime that increases exponentially with domain length but apparently remains finite for all domain
  lengths … a super-transient and is never an attractor." "The trajectory in the system phase space eventually
  finds its way close to the stable manifold for the competing homogeneous (laminar) state and
  spatio-temporal chaos ceases abruptly." The same for Kuramoto–Sivashinsky (Shraiman 1986), lattice models
  (Crutchfield–Kaneko), pipe flow (Hof et al. 2006: decay time exponential in Reynolds number) and
  Taylor–Couette flow (super-exponential). Review: T. Tél and Y.-C. Lai, "Chaotic transients in spatially
  extended systems", Phys. Rep. 460 (2008), 245–275.

## 4. Not obtained

- **Tél and Lai 2008** (Phys. Rep. 460, 245–275): ScienceDirect refuses automated clients; no author copy
  reachable (the authors' university hosts did not answer). Title and data confirmed by two reference lists
  (§2, §3). Another paper (Rempel, Lesur, Proctor, arXiv:1006.5669, abstract) uses its terminology: a
  "type-II supertransient law" is a lifetime growing exponentially in the control parameter.
- **Kaneko 1990** ("Supertransients, spatiotemporal intermittency and stability of fully developed
  spatiotemporal chaos", Phys. Lett. A 149, 105): not obtained; title and data are the lead's, unverified.
- **Wackerbauer and Showalter 2003**: not obtained; see §3 for what is reported of it.
- Lai and Winslow 1995 (chaotic saddles behind supertransients): not obtained; not verified.

---

## What is claimed, what is proved, the heuristic

- **Claimed (numerically):** (i) mean lifetime τ(L) ≈ exp(AL + B) in one-dimensional systems of length L, or
  faster than exponential in the volume (Crutchfield–Kaneko); (ii) exponential ("Poisson") distribution of
  lifetimes at fixed L; (iii) abrupt collapse; (iv) statistical stationarity during the transient.
- **Proved:** nothing, in anything I could open.
- **Heuristic, as far as stated in what I read:** the transient lives near a non-attracting chaotic set (a
  "repeller"/"chaotic saddle") with a small escape rate; collapse happens when the trajectory comes near the
  stable manifold of the absorbing (laminar, homogeneous, periodic) state. The step from this picture to
  "exponential in L" (the absorbing configuration must be approached everywhere at once, by roughly
  independent regions) is the folk argument; I did not find it written out in the sources I could read, and
  it is presumably in Tél–Lai.
- **Cellular automata:** only through the stable-chaos analogy (§2) and the remark that chaotic rules on
  finite lattices have cycle times exponential in size. No source read treats a deterministic cellular
  automaton with an absorbing state.
- **Confinement / boundaries:** §3 is the one case: chaos persistent under periodic boundary conditions
  becomes a supertransient under non-periodic ones, the collapse being associated with boundary layers of
  fixed thickness. That is a one-dimensional PDE; the exponent is the length of the whole domain, not the
  size of a boundary.

## Does it apply here?

There are no hypotheses to check: these are observations. What matters for a paper:

1. The area law is **not a new kind of phenomenon**. Deterministic chaos lasting exp(c·size) with memoryless
   collapse is the supertransient scenario; `PRIOR-ART.md` §3 ("what I found no precedent for: applying it to
   a deterministic CA …") should cite this literature and narrow the claim.
2. What may be new: (a) a cellular automaton with a proved absorbing structure (T2, T3) in which the
   collapse proceeds by peeling layers; (b) the exponent proportional to the **area of a face** of a
   three-dimensional vessel rather than to the volume or length of the whole system; (c) the precision of the
   measured law; (d) the symmetry effects. On (b), note that Crutchfield–Kaneko's "faster than exponentially
   with … volume" is the opposite deviation from what the repository reports.
3. A proof for any member of this class, even a contrived one, would itself be new as far as these sources
   show.

## Corrections to this repository's citations

- `requests.md` item 3: Crutchfield–Kaneko 1988, Tél–Lai 2008 (Phys. Rep. 460, 245–275) and
  Wackerbauer–Showalter 2003 (Phys. Rev. Lett. 91, 174103) are confirmed in title and data from reference
  lists I read. "Kaneko 1990" is unverified.
- `requests.md` item 3 describes supertransients as "lifetime grows exponentially with system size".
  Crutchfield–Kaneko's own abstract says "faster than exponentially with increasing system volume"; the
  exponential-in-length statements are for one-dimensional reaction–diffusion and Ginzburg–Landau systems.
- `PRIOR-ART.md` has no entry for any of this; its §3 verdict needs the revision in point 1 above.
