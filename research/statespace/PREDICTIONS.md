# State space: forecasts written before the study

## The lead, 2026-11-15 07:54 UTC (before any enumeration has been run)

The owner's question (`docs/OWNER-JOURNAL.md`): within a hull there are finitely many states; how many does a seed
visit, and is there a pattern as the size goes up? A trajectory cannot repeat a state before it settles, so the
states visited by one seed number its settling time plus its final period. For small vessels the whole map on
2^N states can be listed. Forecasts, each with the chance I give it:

- **E1 (70%).** Almost every state has no predecessor: the number of states that have one grows as 2^(s·N) with s
  between 0.75 and 0.95 bits per cell over the sizes that can be listed.
- **E2 (55%).** The states that lie on cycles (the end states) number 2^(a·N) with a between 0.2 and 0.5 bits per
  cell, and almost all of them are still (period 1) or period 2.
- **E3 (60%).** The longest transient over *all* seeds of a vessel grows faster with size than the mean transient
  from a random seed: the ratio of longest to mean at least doubles between the smallest and the largest vessel
  listed.
- **E4 (40%).** Already at the listable sizes the mean settling time from a random seed rises exponentially in the
  number of face cells at a rate between 0.15 and 0.25 per cell.
- **E5 (65%).** The champion seed of a vessel (the one with the longest transient) has no symmetry of the vessel.
- **E6 (60%).** The set of states still possible after t generations (the image of the t-th iterate) shrinks fast
  at first and then slowly: more than half of its eventual loss in bits happens in the first three generations.
- **E7 (75%).** At every size where both can be had, a seed visits fewer states than a random map on the same
  number of *living-face* cells would before repeating (2^(A/2)): gump explores less than chance.

## The investigator, 2026-11-15 (before any enumeration of this study has been run)

What I had seen: `research/theory/exhaust_results.txt` (kagome tori of 9–30 cells: max transients 3–28, mean
transients 1.7–6.3, most states without a predecessor) and the face law. Forecasts, each with the chance I give it;
N = cells of the vessel, "listed" = the vessels whose 2^N states are enumerated in this study.

- **I1 (60%).** In every listed vessel the empty state has the largest basin, and it holds more than half of all
  seeds in every listed diagonal hull.
- **I2 (70%).** The mean transient from a uniformly random seed stays below 12 generations in every listed vessel,
  and does not grow exponentially with N over the listed range (E4 fails).
- **I3 (55%).** The longest transient grows at most linearly over the listed range: it is below 2N in every listed
  vessel.
- **I4 (85%).** The share of states with no predecessor exceeds 0.8 in every listed vessel with N ≥ 15 (against
  e⁻¹ = 0.37 for a random map).
- **I5 (60%).** The states on cycles are fewer than a random map's √(πM/2) ≈ 1.25·2^(N/2) in every listed vessel
  with N ≥ 20.
- **I6 (60%).** Visited states per cell, log2(transient + period)/N, for the champion seed is below 0.25 at the
  largest listed N of each family, and for the mean seed below 0.15.
- **I7 (60%).** The Shannon entropy per cell of the long-lived (quasi-stationary) chaotic ensemble lies between
  0.80 and 0.95 bits, both in the bulk and in the top layer of a living face; so a face of A cells (one layer) can
  be in about 2^(0.9·A) states and a seed sees 2^(0.30·A) of them.

## Scored (the lead, 2026-11-15 10:20 UTC, from the README's tables; the investigator's scores agree)

E1 failed: most states have no predecessor (57–98%), but those that have one number 2^(0.95–0.98·N), above the band
0.75–0.95; a constant fraction is lost at the first step, not a rate per cell. E2 half held: the exponent for states
on cycles is in 0.2–0.5 for three families of five (hulls 0.58, 3-layer slabs 0.52 are above); "mostly still or
period 2" held. E3 held in four families of five (the fifth reaches 1.97). E4 failed: settling times rise linearly
in N at these sizes; nothing listed is large enough to be on the face law. E5 held (no champion of a vessel of 19 or
more cells is symmetric). E6 failed as a general rule (true of hulls and kagome tori, not of 2- and 3-layer slabs).
E7 held, with one exception (the 27-cell 3-layer slab's champions visit 53 states, more than 2^4.5). Three and a
half of seven.
