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
