# Timestamped predictions (append-only)

## 2026-11-13T01:28:41Z — side-16 first plateau (preliminary)
Side-16 checkpoint at this moment: `gen 1500000000`, alive (hull radius 42, A = 693).
Method: 64 copies of `research/data/cube16_gen1025000000.gump`, each diversified by one O_h-orbit flip, run on the
validated orbit-reduced stepper (`research/fluct/qsd.py snap ... v`), Fleming-Viot restarts, T0 = 1000.
8 face-family deaths in 8.3e9 replica-generations: **mean residence 1.04e9 (90% CI 0.63e9 .. 2.1e9)**.
Predicted death generation of the running cube (alive at 1.45e9): median **2.2e9**, 90% interval 1.50e9 .. 5.2e9.
(`python3 research/fluct/predict.py snap_cube16_gen1025000000 --now 1.45e9`). Will be refined with more deaths.
