# blast/ref-proofs: referee of `rigour` (theorems, exact numbers) and `image` (seam identity)

Standing account of agent `ref-proofs` (2026-11-18). **The verdicts, claim by claim, are in `REVIEW.md`.**
This file says what is here and how to rerun it.

## Result in five lines

1. [measured, exact] 12 rows of `rigour/data/exact.csv` (9, 12, 15 cells; triangle, tubes, tori, strips, patches)
   reproduced to every printed digit by an independent dense code; bust shares reproduced on 8 faces to 6 digits
   and on 2 by simulation (0.9365 ± 0.0004, 0.0170 ± 0.0002).
2. [proved, checked] Theorem 2 (tilt identity), Theorem 1, Lemma 0, (K), Lemma R, the covering relation: correct.
   ε_max = 2.509462. The reading "ln τ is exactly a sum of local costs" is corrected: the price map is not
   canonical (the chain rule gives another exact one) and the non-locality is all in the tilted measures.
3. [proved] Theorem 3 is a valid but nearly empty implication. Its hypothesis as written is false at s = 1
   (local means are Θ(1/A) there, not exponentially close to a limit); repaired by an additive K₀/A.
   Its "refinement" (additivity over loops) is not proved by the same proof.
4. [measured, exact, new] On wrapped faces of 9, 12, 15 cells the tilted law μ_s is a mixture of a sparse and an
   over-full face for s ≳ 0.1 (valley deepening with size); on rimmed faces it has one hump. rigour's test for the
   failure of its hypothesis (variance of E) cannot see this, because E ≈ 0 on both humps.
5. [proved, enumerated on gump's rule] image's seam identity (★) is correct; with a soup start Z = 1 exactly.
   "Loops add, per cell, independent of tube length" does not follow from it: it is a first-order ansatz.

## Files and commands (all from this directory; numpy only)

| file | what | command | output |
|---|---|---|---|
| `ref.py` | graphs from the 12 offsets; coins enumerated; dense 2^A kernel; quasi-stationary law; tilt identity, two price maps, population law along the tilt; bust shares; Lemma 0 by reachability; simulation | `python3 ref.py hull 3 --eig --tilt --bust`; `python3 ref.py torus 1 1 4 --tilt --bust --lemma0`; `python3 ref.py torus 1 1 3 --mc 300000` | `data/exact9.txt`, `data/exact12.txt`, `data/eig12.txt`, `data/mc_*.txt` |
| `ref15.py` | the same kernel lumped over the translations of a tube (1,K),(0,D) | `python3 ref15.py 1 5`; `python3 ref15.py 0 5` (40 s, 2 GB) | `data/exact15_*.txt` |
| `seam.py` | seam identity on one layer of gump's rule, tube (1,0),(0,4) against its double cover, with a negative control | `python3 seam.py` (6 s) | `data/seam.txt` |
| `seam3.py` | the same for a threefold cover and a rest band one unit cell thick | `python3 seam3.py` (4 s) | `data/seam3.txt` |
| `lemmaR.py` | branch rates of rigour's tube rows | `python3 lemmaR.py` | `data/lemmaR.txt` |
| | covering relation; living baselines | inline scripts, results kept | `data/cover.txt`, `data/living_baseline.txt` |

Shapes: `torus H K D`, `hull R`, `strip W D`, `patch W D` (rigour's names; conventions in the header of `ref.py`).
`ref15.py 1 4` reproduces `ref.py torus 1 1 4` to all digits (the check of the lumping).

## Not checked

18 cells and beyond; every Monte Carlo row of rigour (`mc.c` not read); fair coins; the 18-cell triangle's price
map and bust share (0.0030); image's measurements; the seam identity on more than one layer or girth > 1; whether
the two-humped tilted law persists in large faces. No stepper of gump was used: `ref.py` is the surrogate's kernel
and `seam.py` runs only the one-layer rule (B45/S345 on the six in-layer neighbours, closed by T4), neither was
compared with `reference/oracle.py` (rigour's graph was; my kernel agrees with rigour's solver to 12–13 digits on
12 shapes, which ties my graphs to theirs).
