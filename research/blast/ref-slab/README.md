# research/blast/ref-slab: referee of split-slab's dice-chain sampler (2026-11-18)

The standing account is **`REVIEW.md`** (verdicts claim by claim, numbers, errors, commands). Raw outputs: `data/`
(`final.txt` = every table, made by `bash final.sh`; `validate.log`, `graphcheck.log`; `sub_*.txt` = fresh sampler
replications; `brute_*.txt` = own brute force). Bulk (dying paths) under `research/scratch/blast/ref-slab/out/`.

Files (all the referee's own, except `ss_diag.c`):
- `rgeom.py`: slab graph of the torus (H,K),(0,D) from `docs/AUTOMATON.md` (own numbering, own canonical form).
- `dice.c`: own bit-sliced stepper; `dump` (validation), `brute WD SEED GENS [PATHS]` (WD = 6 dice chain, one face;
  WD = 0 gump, two faces). `rvalidate.py H K D GENS [N]`: state for state against `reference/oracle.py`, with a
  negative control. `graphcheck.py`: split-slab's graph files are the same graphs as mine.
- `ss_diag.c`: split-slab's `ss.c` with diagnostics added to mode `sub` (acceptance per level and sweep kind,
  distinct ancestors); the sampler itself is unchanged (`diff ss_diag.c ../split-slab/ss.c`).
- `pool.py` (replications -> ln tau, bootstrap, tail diagnostics), `shares.py` (boom-and-bust shares from paths,
  plain and rate-weighted), `runs.py` (run against run), `final.sh` (all tables).
- `runner.sh`, `direct48.sh`: copies of the queue runner and of the direct-count test as run from `R`
  (`R/runner.log` has every command with its start time; seeds 7101-7106, 7150, 7190, 7201-7206, 7250, 7260,
  7301-7302, 7401-7402, 7501-7540).

Build and run (R = research/scratch/blast/ref-slab, G = research/scratch/blast/split-slab):

    gcc -O3 -march=native -o R/dice dice.c -lm;  gcc -O3 -march=native -o R/ss_diag ss_diag.c -lm
    python3 rvalidate.py 1 4 21 1200;  python3 rgeom.py 1 4 21 R/r_1_4_21.graph
    R/dice R/r_1_4_21.graph brute 6 12 8000000 R/out/bpaths_dice_63.txt
    WD=6 R/ss_diag G/g_1_18_40.bin sub SEED NREP 44 3 8 20 4 32 24 PATHS 12      # 120-cell tube, split-slab's frozen parameters
    bash final.sh > data/final.txt
