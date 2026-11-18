# research/blast/ref-boom

Referee's rewrite and attack of `research/blast/boom` (blast of 2026-11-18). **The standing account is `REVIEW.md`**
(verdict on each claim, numbers, errors, commands, what was not checked, forecasts scored).

In one paragraph [measured unless said]: boom's route is confirmed with an independent stepper (one hump of launches
at 0.738·A at 48, 57, 63, 75 cells; the four-layer breath and its weak precursor; the island table), its numbers
I_up(0.74) = 0.078 and J(0.74) = 0.132 are confirmed (0.079, 0.136), and its headline "min [I_up + J] = 0.2099
against the price 0.2087" is refuted as evidence: Σ ν·d = 1/τ is an identity [proved], so I_up + J at the hump is
the lifetime slope of the sizes used (mine: 0.2154 ± 0.0011 against 0.2156 ± 0.0005 for 48–63 cells), and 0.2099 is
0.212 ± 0.004. The launch hump narrows in θ nearly like 1/√A (s.d. ∝ A^0.58±0.03 cells), not at a fixed share of A.

Second task (05:20–05:45 UTC): **`STATIC.md`** — is the price the static rarity of the four-layer over-full state?
No: at the launch profile I₄ = 0.166 ± 0.003 per cell is static and J₄ = 0.057 ± 0.003 is still in the kill
(`rb.c` mode `static`, binary `rbs`; `run5.sh`; `st.py` → `out_static.txt`).
Third task (05:46–06:05 UTC), second half of `STATIC.md`: look-ahead events of the face (`rb.c` mode `ahead`,
binary `rba`; `run6.sh`, `run7.sh`; `ah.py` → `out_ahead.txt`, `out_ahead_tube.txt`). No static event whose rarity is
the price; but ln τ(A) = −ln ν_A(face ≥ 0.74·A) + 0.1273·A − 1.37, fitted on 48–63 cells, gives 75, 84 and 108 cells
to 0.03 without a death, and misses the 84-cell tube by its whole discount (0.22).
Wide faces of 126–192 cells (last section of `STATIC.md`; `run8.sh`, binary `rbw`, `out_wide_*.txt`): the estimator
sits on the wide-face line (0.2087 per cell) at 126, 144 and 192 cells.

Files:
- `rb.c`: stepper for the 8-layer slab torus (64 replicas, bit-sliced) with the statistics; modes `dump`, `run`,
  `island`. Build: `gcc -O3 -march=native -o rb rb.c` (`rbi`, `rbt` are builds of later states of the same file;
  the final source does everything and reproduces the first build's `run` output byte for byte).
- `val.py`: validation against `reference/oracle.py` (`python3 val.py H K D gens [neg]`).
- `run.sh`, `run2.sh`, `run3.sh`, `run4.sh`: what was run, with seeds. Bulk output: `research/scratch/blast/ref-boom/`.
- `pool.py` (sum the counts of several runs of one vessel), `an.py` (launches, ν, d, two-term price, layer
  profiles → `out_all.txt`), `ani.py` (islands → `out_islands.txt`), `life.py` (slab lifetimes → `out_life.txt`).
- `PREDICTIONS.md`: forecasts frozen before any run (commit 782d9f5), scored at the end.
