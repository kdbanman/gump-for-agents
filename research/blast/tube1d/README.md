# blast/tube1d: tubes as a one-dimensional problem (agent `tube1d`, 2026-11-18)

Standing account; results, not a diary. Code: `tube1d.c` (own stepper, bit-sliced, 64 lanes), `validate.py`,
`validate_all.sh`. Bulk output is under `research/scratch/blast/tube1d/` (ignored by git); the curated numbers
are copied into `data/`. Build: `gcc -O3 -march=native -o ../../scratch/blast/tube1d/tube1d tube1d.c -lm`.

(Being written; see the git log for the state of each section.)

## 1. Stepper and validation [measured]

`sh validate_all.sh` (2 minutes): the deterministic slab of `tube1d.c` against `reference/oracle.py`, state for
state over 1,500 generations on (4,0),(0,4), (1,4),(0,21), (1,12),(0,28), (1,17),(0,32) (8 layers) and
(1,3),(0,25) (7 layers): all identical; with one wrong neighbour (`bad`) the comparison fails at generation 8 and
5. Output: `validate_log.txt`.
