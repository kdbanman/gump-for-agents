# REVIEW of split-slab's dice-chain sampler (referee ref-slab, 2026-11-18) -- DRAFT, numbers being filled in

Work in progress at 04:56 UTC; see `data/` for raw outputs so far. Own code: `rgeom.py` (graph), `dice.c` (stepper,
brute force), `rvalidate.py` (oracle validation), `graphcheck.py`, `pool.py`, `shares.py`; `ss_diag.c` = split-slab's
`ss.c` with diagnostics added (sampler unchanged).

Preliminary (all [measured], commands in the final version):
- own stepper bit-exact against the oracle on (4,0),(0,4), (1,4),(0,21), (1,8),(0,20), (1,12),(0,28); negative control fails.
- dice chain by own brute force: 48 cells 9.9371 +- 0.0038, 63 cells 13.1541 +- 0.0113 (gump anchors 9.9251, 13.1622).
- half-face-fall share of natural deaths, chain against gump (own code): 48 cells 0.5914 vs 0.5916 (+- 0.0019); 63 cells 0.562 vs 0.558 (+- 0.006).
- sampler with fresh seeds: 48 cells 9.919 +- 0.014 (64 reps), 63 cells 13.227 +- 0.030 (48 reps).
- genealogy: the dying chains of one replication descend from 193 (48 cells), 91 (63), 35 (120), 9.5 (192 wide) initial states.
