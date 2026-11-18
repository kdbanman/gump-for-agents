# research/blast/ref-boom

Referee's rewrite and attack of `research/blast/boom` (blast of 2026-11-18). The standing account is `REVIEW.md`.
Files: `rb.c` (stepper + statistics; `rbi` is the same source built after the island mode was added), `val.py`
(validation against `reference/oracle.py`), `run.sh` (what was run), `an.py`, `ani.py` (analysis), `PREDICTIONS.md`.
Build: `gcc -O3 -march=native -o rb rb.c`. Bulk output: `research/scratch/blast/ref-boom/`.
