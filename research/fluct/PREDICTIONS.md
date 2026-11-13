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
