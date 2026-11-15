# How much of its state space does a gump seed explore?

2026-11-15. The owner's question (`docs/OWNER-JOURNAL.md`, first note): within a hull there are finitely many states;
for the longest-lived seeds, how many of them are hit, and is there a pattern as the size goes up? Forecasts written
before any enumeration: `PREDICTIONS.md` (the lead's E1–E7, the investigator's I1–I7), scored below.
Tags: **[proved]** (a theorem, or an exhaustive enumeration whose code was matched to `reference/oracle.py`),
**[measured]** (a sampled number with its error or its convergence shown), **[conjectured]**.

## The answer

1. **A seed visits almost nothing.** A deterministic orbit cannot revisit a state before it reaches its final cycle,
   so the states one seed visits are exactly its settling time plus its final period. That number is tiny next to
   the 2^N states of its vessel, at every size.
2. **Where every state can be listed (vessels of up to 30 cells, about a billion states), a typical seed visits 6–14
   states, and the most patient seed of all visits 46–94.** Against 2^30 ≈ 10⁹ that is about 0.1 bit per cell for
   a typical seed and 0.2 for the record [proved]. A random map on as many states would wander for about 40,000
   before repeating; gump is quicker to settle than chance by a factor of thousands.
3. **At these sizes nothing is chaotic yet.** The typical number of visited states grows only linearly in the size
   (about 0.15–0.5 more per cell), the record a little faster; neither is exponential. The share of the space that is
   ever visited by one seed is 2^-(0.8–0.9 N).
4. **What does shrink fast is what can still happen.** After one generation 6–43% of all states are already
   impossible (no predecessor); after the transient is over, only 2^(0.4–0.57 N) states remain (the states on cycles:
   still lifes and oscillators, thousands of distinct ones; periods up to 70 occur).
5. **For your large runs the count is still exact.** The side-16 closed cube visited 2,919,617,676 ≈ 2^31.4
   distinct states; its hull holds 51,888 cells, so it saw a fraction 2^-51,857 of its hull's states. Every
   closed cube 8–16 visited between 24 and 2^31.4 states, about 0.03 bits per face cell, or 0.15–0.29 bits per cell of
   the symmetry-reduced face.
6. **The pattern that extrapolates is the face law.** An asymmetric seed lives as long as its faces, and a face of A
   cells lives e^(0.209·A) generations: the seed visits 2^(0.30·A) states — 0.30 bits per face cell, a constant from
   A = 27 to 135, a straight line on a log scale.
7. **A share of what?** Most of the 2^N states of a hull are not states a living face can be in. But a living face is
   close to random: its top layer alone carries 0.986 bits per cell, and the whole chaotic face slab
   ENT_SLAB bits per cell [measured]. So a face of A cells has about 2^(0.99·A) states per layer it can be in, and a
   seed sees 2^(0.30·A) of them before the face dies: the share falls as 2^(-0.69·A) per layer, already 10⁻¹⁹ for one
   face layer of a side-13 hull's 570 cells... see section C for the precise statement.
8. **Against chance:** a random map on the face's 2^A states would visit 2^(A/2) before repeating; gump visits
   2^(0.30·A). Gump explores less than chance, by a factor 2^(0.2·A).

(Item 7 is filled from the entropy measurement; see C.)

## A. Exact: vessels whose 2^N states were all listed

### The vessels [proved]

`vessels.py` builds four kinds; for each, every cell outside it is dead forever, so the state space is exactly
{0,1}^N:

- **Diagonal hulls** `hull LO0 HI0 … LO3 HI3`: the cells p (doubled coordinates) with LO_d ≤ d·p ≤ HI_d on the four
  body diagonals d. A seed inside stays inside forever by T2 (`docs/AUTOMATON.md`): a cell beyond a bound has at most
  3 live neighbours. **Every** diagonal hull with 2–29 cells was enumerated (276 hulls, up to translation and O_h;
  `vessels.py hulls 40` lists them, widths ≤ 6 layers per diagonal, which covers every hull of ≤ 29 cells — a hull 7
  layers wide in one diagonal has more cells than that), plus six of the eleven 30-cell hulls in which every cell can
  be born. Small hulls are thin: in many of them some cells have fewer than 4 neighbours inside and can never be born
  (column "born-capable" in `data/tables.md`).
- **Slab tori** `slab p q r m`: m consecutive {111} layers on the in-plane torus (i,j) ~ (i+p,j) ~ (i+q,j+r); closed
  by T4 (a pattern in m consecutive layers stays in them). Families m = 3 (the thinnest slab with no finite sealed
  set, T6; every lattice of index 1–3: 9, 18, 27 cells), m = 2 and m = 1 (the kagome layer; per index the lattice with
  the longest shortest loop, N = 3k up to 30).
- **3D tori** `torus a b c d e f`: Z³ modulo a lattice of index k (3k cells), per index the lattice with the longest
  shortest vector. Tiny tori are multigraphs: a cell can be its own neighbour's neighbour twice (column "multi" in
  `data/vessels.jsonl`); the dynamics is that of the periodic patterns of the lattice, which is what the oracle runs.

### How the enumeration was checked

`enum.c` builds the table f(s) for all 2^N states. `validate.py` lifts random states of each vessel into the oracle's
array torus (a padded box for a hull; for a slab or torus a periodic tiling of an n-torus with nZ³ a period of the
vessel and, for a slab, at least three dead layers across the wrap, which T3 keeps dead) and steps them with
`oracle.step`; every copy of every vessel cell must agree with `enum.c` at every generation, and every other cell must
stay dead. Run by `run.py` on **every** vessel: 40 random states × 40 generations, then the first 8 champions over
their whole transient plus one period (`validated` field of each row). A deliberately wrong rule (birth on 4 only) is
caught at generation 1–4 on a hull and a slab. Independent cross-checks that came for free: the 12-cell vertex star
(T10: 2,750 seeds die, 107 nonempty still lifes, 195 two-cycles) is reproduced exactly; lattices equivalent by symmetry
(the three index-2 slabs, three of the four index-3 slabs) give identical maps; the image iteration stops exactly at
t = longest transient, as it must. Every champion file is verified on the oracle alone by `champion.py`.

### Results for the largest vessel of each family [proved]

M = 2^N. "Visited" = transient + period of the final cycle = distinct states on the orbit.

TABLE_LARGEST

Every vessel: `data/tables.md` (`python3 research/statespace/analyze.py tables`). Hull census per N (every hull of N
cells; the record is the hull whose champion is longest): `python3 research/statespace/analyze.py hullsizes`:

TABLE_HULLS

### The image after t generations [proved]

log2 |f^t(S)| / N, the bits per cell of the states still possible after t generations, for every t until it stops
(full lists: `image_t` in `data/vessels.jsonl`):

TABLE_IMAGE

The loss is front-loaded in the hulls (half the eventual loss in bits by t = 3 in 143 of 146 hulls of ≥ 15 cells)
and slow in the 2- and 3-layer slabs (a quarter to a third by t = 3).

### Transients and visited states [proved]

Distributions over all 2^N seeds are in `transient_hist` and `visited_hist`. They are short-tailed: the number of
seeds not yet settled after t generations falls by a roughly constant factor per generation (in the 27-cell slab
2^25.2, 2^22.2, 2^19.1 at t = 10, 20, 30: a factor 2^-0.3 per generation), so there is no long-lived population at
these sizes — the transients are not yet the face law's exponential lives.

### Champions [proved]

The seed with the longest transient, per vessel, is in `data/champions/NAME.txt` with the one command that verifies
it on the oracle (`python3 research/statespace/champion.py data/champions/NAME.txt`). In no vessel of 19 or more
cells is any listed champion fixed by a nontrivial symmetry of the vessel (stabiliser 1 for the first 64 listed;
at 12–18 cells a few are). Champions come in whole orbits of the symmetry group: in the 3-layer 27-cell slab
`slab_3_1_1_3`, the 36 champions are one orbit of its 36 symmetries. What they look like: a population hovering near
half the cells (the 27-cell slab champion: 9–17 live cells for 35 generations), then a collapse over the last 5–10
generations into a still life, a small oscillator or nothing; the 2-layer 30-cell champion wanders for 88 generations
and lands on a period-3 cycle.

### Scaling [proved for the numbers; the extrapolation is conjectured]

SCALING

## B. Vessels too large to list: the owner's closed cubes and the face law

STATES_LARGE

## C. A share of what?

ENTROPY_SECTION

## D. Against chance

RANDOM_SECTION

## E. Forecasts, scored

FORECASTS

## What each number rests on, and what was not checked

NOTCHECKED

## Reproduce

```
cc -O2 -march=native -o research/scratch/ss_enum research/statespace/enum.c -lm
cd research/statespace
python3 vessels.py hulls 40 > ../scratch/ss_hulls40.txt          # every diagonal hull up to 40 cells (1 min)
python3 run.py list hull | while read k a; do python3 run.py one $k $a --family hull; done   # also slab3all slab1 slab2 torus
python3 run.py one hull -1 3 -5 1 -5 1 -3 5 --family hullbig     # one vessel: validate, enumerate, champion file
python3 analyze.py tables; python3 analyze.py hullsizes; python3 analyze.py scaling; python3 score.py
python3 champion.py data/champions/slab_3_1_1_3.txt               # a champion on the oracle alone
python3 large.py                                                  # part B tables (needs research/scratch/ss/cube14.json, cube15.json:
                                                                  #   engine/target/release/gump run --cube 14 --lite | tail -1)
python3 qsd.py validate 16 8 300; python3 qsd.py selftest 16 8    # part C stepper and estimator checks
python3 qsd.py sample 16 8 256000 3 2000 2 ../scratch/ss/qsd_P16_M8_big.npz
python3 qsd.py entropy ../scratch/ss/qsd_P16_M8_big.npz 0,1,2,3,4,5,6,7 24
python3 qsd.py entropy ../scratch/ss/qsd_P16_M8.npz 7 22          # top layer alone (64,000-snapshot sample, seed 1)
python3 figure.py
```
Times on one core: a 27-cell vessel 50–65 s, a 30-cell one 3–4 min (6.4 GB); the hull census ≤ 27 cells about 25 min.
