# Timestamped predictions (append-only)

## 2026-11-13T01:28:41Z — side-16 first plateau (preliminary)
Side-16 checkpoint at this moment: `gen 1500000000`, alive (hull radius 42, A = 693).
Method: 64 copies of `research/data/cube16_gen1025000000.gump`, each diversified by one O_h-orbit flip, run on the
validated orbit-reduced stepper (`research/fluct/qsd.py snap ... v`), Fleming-Viot restarts, T0 = 1000.
8 face-family deaths in 8.3e9 replica-generations: **mean residence 1.04e9 (90% CI 0.63e9 .. 2.1e9)**.
Predicted death generation of the running cube (alive at 1.45e9): median **2.2e9**, 90% interval 1.50e9 .. 5.2e9.
(`python3 research/fluct/predict.py snap_cube16_gen1025000000 --now 1.45e9`). Will be refined with more deaths.

## Outcome of the preliminary side-16 prediction (appended 2026-11-13T04:08Z)
Reported by the lead: the first face family (R = 42, A = 693) died at last_alive = **2,362,434,048**
(`research/scratch/cubes/ev16.jsonl`, sampled every 64 gens). Prediction above: median 2.2e9, 90% interval
1.50e9 .. 5.2e9 — **inside the interval** (predictive quantile ≈ 0.55). By then the ensemble estimate had become
1.16e9 (90% CI 0.85e9 .. 1.7e9) from 20 deaths in 2.3e10 replica-generations (side-16 copies + R = 42 vertex soups).

## 2026-11-13T04:08Z — side-16 second plateau (R = 40, vertex-centred, A = 630), from fits only
Made without looking at the cube's event log after the first peel. Inputs: cube-centred O_h soups at A = 630
(R = 39): ln tau = 17.80 +- 0.10 (96 deaths, this directory); vertex/cube factor measured ln 0.47 +- 0.04 at A = 513,
≈ 0.82 +- 0.27 at A = 693 (vertex measured / cube-centred fit), interpolated to **0.70 +- 0.25** at A = 630.
=> **mean residence at R = 40: tau ≈ 1.1e8 (ln 18.50 +- 0.27)**. Memoryless; the cube was alive at the 2,525,000,000
checkpoint, so (predictive, uncertainty of tau folded in as ~14 effective deaths):
**second peel at generation median 2.60e9, 50% interval 2.556e9 .. 2.68e9, 90% interval 2.531e9 .. 2.89e9.**
A direct clone run from `research/data/cube16_gen2525000000.gump` follows (next entry) but this entry stands as the prediction.

## 2026-11-13T04:18:44Z — side-16 second plateau, direct clone run (supplements the fit-only entry above)
64 copies of `research/data/cube16_gen2525000000.gump` (R = 40, vertex-centred, A = 630), one orbit flip each,
Fleming-Viot restarts, T0 = 1000: **31 deaths in 2.54e9 replica-generations, tau = 8.2e7 (ln 18.22 +- 0.18)**,
consistent with the fit-only 1.1e8. Predictive, alive at 2,525,000,000: median **2.58e9**, 50% 2.549e9 .. 2.64e9,
90% **2.529e9 .. 2.78e9** (`python3 research/fluct/predict.py snap_cube16_gen2525000000 --now 2.525e9`).
Still made without looking at the cube's event log after the first peel.

## 2026-11-13T04:50Z — side-17 closed cube, first plateau
The cube series loses its two outermost layers by generation ~64 (sides 13–16: hull 3n−2 → plateau 3n−6), so side 17
plateaus at hull radius 45, cube-centred, **A = 828**. O_h soups, cube-centred, brute force on the orbit stepper:
ln tau = 10.99, 12.47, 14.15, 15.88, 17.80, 19.64 (A = 408 … 693; 1087 … 20 deaths) and one death at A = 759
(ln 22.5 +- 1.0). Fits a + bA (+ c sqrt(A) | + cA^2 | slope pinned to 0.209/6) give ln tau(828) = 23.7 / 24.3 / 24.4 / 23.9
(`python3 research/fluct/sym_fit.py`). Taking **ln tau = 24.0 +- 0.4: mean first-plateau residence ≈ 2.6e10
(68%: 1.8e10 .. 4.0e10)**. As a single run (memoryless, tau uncertainty folded in): first peel at generation
**median 2.0e10, 50% 0.8e10 .. 4.1e10, 90% 1.4e9 .. 1.0e11**. (No vertex factor applies: 17 is odd.)

## Outcome of the side-16 second-plateau predictions (appended by the lead, 2026-11-13)
The R = 40 face family died at last_alive = **2,886,100,480** (`research/data/cube16_events.jsonl`). Fit-only entry
(04:08Z; 90% 2.531e9 .. 2.89e9): **inside**, at its 95th percentile. Clone-run entry (04:18Z; 90% 2.529e9 .. 2.78e9):
**missed** (the cube stayed 4.4 clone-means beyond the checkpoint). The clone mean itself was confirmed twice more
(copies of the 2.875e9 state: 5.7e7, 65 deaths; fresh vertex-centred O_h soups at R = 40: 8.2e7, 46 deaths).
The cube ended at generation 2,919,617,676 (still life, 96 cells). See NOTEBOOK.md, 2026-11-13.
