# research/gpu-local — results on the owner's GTX 1080

Tags as elsewhere: **[measured]** (with the command that reproduces it), **[conjecture]**. Agents: read `AGENT.md`
first. Commands run from the repository root with the venv python of `AGENT.md`
(`python` below), after `python -u research/gpu-local/acceptance.py cases`.

## Correctness on this card [measured]

All acceptance checks of `research/gpu/README.md` "Correctness" were ported to a local runner that calls the same
`check.*` functions with the same arguments as the Modal entry points (`research/gpu-local/acceptance.py`, one group
per entry point). Reference cases rebuilt here with the Windows build of the engine; the settle-test set again has
253 cycles of period 3-66 and 120 others, as on the machine that built the originals.

| group (Modal entry point) | what | result |
|---|---|---|
| `every` (`check_every`) | engine every generation, 5 cases × 5 lanes, 2,000-3,000 gens; kernel B default, kernel B J=3 WB=2 blocks=6, kernel A | all equal |
| `every` | negative controls (engine one generation later; deepest node flipped) | every case fails from generation 1, as required |
| `periodic` (`check_periodic`) | settle detection on the 373 engine-run soups, pw = 128, 32, 1024, and a non-default shape | all as expected (pw = 32: the period-48 and -66 soups unflagged) |
| `patches` (`check_patches`) | 12 × 12 × 8 slab every generation (2 seeds); patch counter vs brute force on 24 states | all equal / identical |
| `check` (`check_remote`) | final states vs the engine (3 kernel shapes); vs `fl.c` every 250 gens and face-death generations, R = 7, 9, 13 | all equal, event generations identical |
| `defaults` (`check_defaults`) | production shape on R = 13-17 vs `fl.c`, sparse soups; reseed (2 kernels) | all equal |
| `keep` (`check_keep`) | K_KEEP vs `fl.c` | all equal |
| `slab` (`check_slab`) | 11 × 11 × 8 slab every generation vs the engine; 6 × 6, 6 × 7 slabs vs `fl.c` | all equal |
| `cpu` (`check.py all cpu`) | the CPU build of kernel A (`cpu.c`) vs the engine and `fl.c` | all equal |

Commands: `python -u research/gpu-local/acceptance.py every periodic patches` (about 2.5 min on this card) and
`python -u research/gpu-local/acceptance.py check defaults keep slab cpu` (needs gcc on PATH; about 5.5 min).
`fl.c` and `cpu.c` were built with MinGW-w64 gcc 16.2 (`-O3`/`-O2 -march=native -shared -fPIC`, a DLL under a `.so`
name). Not checked here: the Modal entry points themselves (unchanged; they need Modal), and `check_engine_every` for
kernel A on the CPU beyond what `cpu` runs.

## Throughput and shared-memory fit [measured]

`python -u research/gpu-local/bench_local.py` → `research/data/gpu_local_bench/bench_shared_GTX1080.jsonl` (every row;
same 12 kernel-B shapes per vessel as `modal_app.SHARED_CONFIGS`, and kernel A at three widths). Node-updates/s:

| vessel (nodes) | kernel B, gsim defaults | kernel B, best shape | kernel A | A10G kernel B (on file) |
|---|---:|---:|---:|---:|
| asym R = 15 (2,064) | 7.2 × 10¹¹ | 7.5 × 10¹¹ (WB 2, J 3) | 7.4 × 10¹⁰ | 2.4 × 10¹² |
| asym R = 19 (4,020) | 7.8 × 10¹¹ | 8.6 × 10¹¹ (WB 1, J 4) | 7.3 × 10¹⁰ | 2.5 × 10¹² |
| O_h vertex hull 45 (1,366) | 7.5 × 10¹¹ | 9.1 × 10¹¹ (WB 2, J 2, 2 blocks/SM) | 7.7 × 10¹⁰ | 2.7 × 10¹² |
| slab 6 × 6 × 8 (864) | 6.4 × 10¹¹ | 1.0 × 10¹² (WB 4, J 2, 2 blocks/SM) | 7.4 × 10¹⁰ | |
| torus (1,5),(0,31) × 8 (744) | 6.3 × 10¹¹ | 9.7 × 10¹¹ (WB 2 or 4, J 2, 2 blocks/SM) | 7.5 × 10¹⁰ | |

- Kernel B here is about a T4 (8.7-9.4 × 10¹¹ on file) and 30-40% of an A10G. Kernel A is a third of a T4's.
- **Two blocks per SM (`minb=2, blocks=40`) help on this card for vessels under about 1,400 nodes** (+50% on the
  slabs), where on the A10G they did not; for 2,064 nodes and more they spill registers and lose up to 4×.
  The torus runs use WB 2, J 2, 2 blocks/SM (`eqtorus.sim_cfg`; with K_KEEP: 1.29 × 10⁹ replica-generations/s at
  A = 93, 2,560 replicas, no spills; `python -u research/gpu-local/eqtorus.py tune 1 5 31`).
- **Fit in 48 KB per block:** kernel B needs 4·WB·(n + 31) bytes, so WB = 1 holds n ≤ 12,257 nodes, WB = 2 n ≤ 6,113,
  WB = 4 n ≤ 3,041 (R = 19 with WB = 4 is refused: 64,816 bytes). gsim's default WB already adapts to the card's
  limit. Two blocks per SM need 2 × that within 96 KB per SM, the same bound.
- `bench.bench_gpu` (used by `modal_app.bench`) no longer measures kernel A: `gsim.Sim`'s default kernel on the GPU is
  B, which ignores `WT`. `bench_local.bench_global` passes `kernel='global'`.

## The torus driver, calibrated on 4 × 4 [measured] — and a disagreement with the value on file

`research/gpu-local/eqtorus.py`: `fwslab.py`'s driver for any lattice (a, k), (0, b) of `research/shape/tslab.py`,
with the guard. `eqtorus.py check A K B` = `tslab.check`, then the GPU against the engine every generation (the torus
tiled into the engine's cubic torus; engine cells reduced to torus nodes, the engine state required to be
lattice-periodic), in the shape the runs use, gsim's default shape and kernel A, with the two negative controls.
Passed for (1,5),(0,31) and (4,0),(0,4): 2,000 generations × 5 lanes × 3 kernels all equal, controls fail from
generation 1.

Calibration on the 4 × 4 torus (A = 48; on file 9.9324 ± 0.0020, 247,338 face deaths, `research/shape2/data/A48.csv`,
CPU, cap 16,384): `python -u research/gpu-local/eqtorus.py run 4 0 4 3 48002 max_launch=2048 raw_cap=20000000`

| | this card | on file (CPU) |
|---|---:|---:|
| face deaths | 7,478,823 | 247,338 |
| ln τ_face = ln(2E/F) | **9.9251 ± 0.0004** | 9.9324 ± 0.0020 |
| the same, lives censored at age 10,000 / 17,783 / 31,623 | 9.9237 / 9.9247 / 9.9249 | (cap 16,384) |
| hazard of a face death by age, ×10⁵ per generation | 12.47 (0-60), then 9.76 to 9.79 in every bin from 60 to 100,000 | |
| ln τ_fw, fwslab's convention (face death on a firewalled state) | 15.384 ± 0.008 | 15.128 ± 0.038 |
| ln τ_fw, also counting lives that settle on a firewalled state | 15.189 ± 0.007 | |

- **ln τ_face differs by 0.0073, 3.6σ of the file's error. Resolved: the file's value is high** (a draw of its 76
  seeds, plus a rule bias of the CPU pipeline), and the value here stands. Confirmed by
  `research/audit/REVIEW-gpu-local-pr23.md` section 2 (a third stepper: 9.9246 ± 0.0006; research/shape2's pipeline
  on 152 fresh seeds: 9.9240 ± 0.0014; **best pooled value 9.9249 ± 0.0003**) and by
  `research/audit/REVIEW-gpu-local-tori.md` section 2 (of the file's excess, +0.0017 is the rule and +0.0058 the
  draw, 2.9σ). `research/gpu-local/cpu4x4/` (scripts,
  results; a subagent's work, whose result files I read; I did not rerun its 4.2 M lives) reruns research/shape2's
  own pipeline on this machine (`rep.c` built with gcc, validated against the engine, and reproducing the file's
  row exactly from its seeds: 311,296 lives, E, F = 247,338, W = 685, settled 139):

  | CPU, `rep.c` | lives | ln(2E/F) |
  |---|---:|---:|
  | the file's 76 seeds, the repository's rule | 311,296 | 9.9324 ± 0.0020 |
  | the same lives, per-generation rule (the GPU's) | | 9.9308 ± 0.0020 |
  | 1,024 fresh seeds, the repository's rule | 4,194,304 | 9.9270 ± 0.0005 |
  | **the same lives, per-generation rule** | | **9.9255 ± 0.0005** (this card: 9.9251 ± 0.0004) |
  | 304 seeds next to the originals, the repository's rule | 1,245,184 | 9.9267 ± 0.0010 |

  - *The draw:* the file sits 2.6σ above fresh seeds under its own rule; no single job is an outlier (47 of 76 low,
    per-job χ² 100 on 75); blocks of 76 fresh jobs scatter with sd 0.0021 and one reads 9.9317. The shape2 review's
    independent stepper had 9.9275 ± 0.0015 (`research/audit/REVIEW-shape2.md`).
  - *The rule bias, +0.0016 at this size* [measured on the same lives, `cpu4x4/xtab.py`]: `rep.c` records a layer's
    last-alive generation only every 16 generations, so ends are rounded up by 7.5 generations on average
    (exposure +0.074%), and 0.088% of face deaths are booked as something else: a firewall forming in the same
    16-generation window (1,521 of 3.34 M: ties go to the firewall), a death in the last 15 generations before the
    cap (1,192, booked as capped), an extinction in the same window (219, booked as settled). **It does not scale
    with the mean life alone** (an earlier version here said "16 generations over the mean life, negligible from
    A ≈ 60 up"; `research/audit/REVIEW-gpu-local-tori.md` section 2 measured it on the same lives at both
    resolutions and refuted that). The exposure part is 7.5 generations over the mean life; the count part depends
    on ties with firewalls, the cap and settling. The review's table (bias of ln τ_face, K = 16 against K = 1):

    | A | class (shortest loop²) | mean life | bias |
    |---:|---|---:|---:|
    | 48 | (4,0,4) (16) | 10,265 | +0.00167 ± 0.00006 |
    | 48 | (2,0,8) (4) | 2,280 | +0.0174 ± 0.0005 |
    | 60 | (1,1,20) (3) | 11,250 | +0.00076 ± 0.00003 |
    | 60 | (1,9,20) (4) | 2,584 | +0.0184 ± 0.0011 |
    | 60 | (1,4,20) (16) | 131,347 | +0.0003 ± 0.0001 |

    So +0.017 to +0.018 for the loop² 4 classes at 48 and 60 (ties with firewalls; first estimated in
    `research/audit/REVIEW-shape2.md` claim 1), +0.0008 to +0.0017 for classes with mean lives near 10⁴, and
    ≤ 0.0003 for the long-lived classes at 60.
  - The hazard by age on the CPU lives (per-generation rule) is the one measured here: 12.57 ± 0.07 (ages 0-60),
    then 9.74 to 9.77 × 10⁻⁵ in every bin to the cap.
  - Consequence for `research/constant/PREDICTIONS.md` part C: its 4 × 4 anchor should be 9.925, not 9.932. I have
    not recomputed the forecasts with it (they are the lead's, committed, and stay as written).
- **`fwslab.py` undercounts firewalls where lives can settle.** A firewalled slab often settles (period 1-2) before a
  face dies; the kernel then reports kind 2 and the driver keeps it as "settled". Here 3,420 of 5,023 settled lives
  were on a firewalled state: 18% of all firewalls, and ln τ_fw moves by 0.20. `eqtorus.py` counts them
  (`fw_settled`); ln τ_face is unaffected (both kinds are censored for it). Found first at 3 × 6 × 8 (0.9% of
  firewalls) in `research/audit/REVIEW-gpu-pr14.md`, "Firewalls labelled settled". On the values on file it touches
  only small-slab ln τ_fw, by at most 0.034 (4 × 5 × 8; `REVIEW-gpu-local-pr23.md` section 3).
- **Launch length matters when lives are short.** The first calibration run (launches up to 2¹⁸ = 26 mean lives) had
  39 lives that sat to a launch boundary (firewalled without a face death, or in a cycle of period 3-128, which
  kernel B only recognises at the next launch start): 0.16% of the exposure, +0.0016 on ln τ. The cap `max_launch`
  must stay well below the mean life (the queued tori have mean lives ≥ 10⁷, so 2¹⁸ is safe there).

## Equilateral face tori (research/constant/PREDICTIONS.md part C) [measured]

8-layer slabs, soup 0.4, lives from generation 0, guard on (thresholds 16 · 2^j), ln τ_face = ln(2E/F) ± 1/√F.
In `research/data/gpu_local_eqtorus/`:
- `eqtorus_A_K_B.csv`: one row per run (seed, exposure, ends by kind, command, commit);
- `checks/check_A_K_B.txt`: the output of `eqtorus.py check A K B` for that torus (`tslab.check`, the GPU against the
  engine every generation in three kernel shapes, the two negative controls). For 57 to 111 it is the check that ran
  just before the runs; for 4 × 4 and 93 it is a rerun of 2026-11-15 after them (the originals were not saved);
- `hist_A_K_B.json`: per run, exposure and ends by kind in age bins, and the guard's lives. `eq_analyze.py` falls
  back to it where the per-run json (raw lives, `research/scratch/gpu-local/` on this machine only) is absent.

Analysis: `python research/gpu-local/eq_analyze.py A K B` (one torus), `python research/gpu-local/eq_fit.py` (the
family). Reviewed at five tori in `research/audit/REVIEW-gpu-local-tori.md` (b843883); the rows for 81 to 111 and
everything said about them here are later than that review.

| A | lattice | transverse layers | runs | face deaths | firewalls | settled | kind 5 | ln τ_face | seeds χ² | a second code |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 48 | (4,0),(0,4) | 8 | 1 | 7,478,823 | 15,925 + 3,420 | 5,023 | 0 | 9.9251 ± 0.0004 | | 9.9246 ± 0.0006 (pr23 review) |
| 57 | (1,7),(0,19) | 2 | 4 | 6,579,101 | none possible | 1,640 | 0 | 11.8751 ± 0.0004 | 9.25 on 3 | 11.8744 ± 0.0015 (tori review) |
| 63 | (1,4),(0,21) | 2 | 2 | 1,811,510 | none possible | 236 | 0 | 13.1622 ± 0.0007 | 0.07 on 1 | 13.176 ± 0.011 (`REVIEW-dying.md`, round 3) |
| 75 | (5,0),(0,5) | 10 | 2 | 183,954 | 468 + 2 | 2 | 0 | 15.6630 ± 0.0023 | 0.39 on 1 | 15.667 ± 0.010 (tori review); file 15.6614 ± 0.0026 |
| 81 | (3,3),(0,9) | 6 | 2 | 103,883 | 0 + 1 | 2 | 0 | **16.9222 ± 0.0031** | 0.53 on 1 | none |
| 84 | (2,4),(0,14) | 4 | 2 | 106,629 | 0 | 1 | 0 | **17.5467 ± 0.0031** | 3.05 on 1 | none |
| 93 | (1,5),(0,31) | 2 | 4 | 35,521 | none possible | 0 | 0 | 19.4141 ± 0.0053 | 0.70 on 3 | none |
| 108 | (6,0),(0,6) | 12 | 10 | 18,394 | 298 | 0 | 0 | **22.5405 ± 0.0074** (four seeds: 22.5600 ± 0.0222) | 6.0 on 9 | file 22.568 ± 0.041 (592 deaths, A10G, `fwslab.py`) |
| 111 | (1,10),(0,37) | 2 | 4 | 1,875 | none possible | 0 | 0 | **23.2032 ± 0.0231** | 3.60 on 3 | none |

- Firewalls: face deaths on a firewalled state + lives that settled on one. A firewall needs three dead transverse
  layers in a row, so none can form with 2.
- **No kind-5 life in any row**, so the two exposure conventions for a guard-recognised life (its whole age, or its
  age cut at the snapshot) give the same value everywhere in this table.
- Launch caps 2,048 (A = 48, 57), 8,192 (63), 65,536 (75), 2¹⁸ (81 and up): 20%, 2.9%, 3.2%, 2.1%, then 2.3% (81),
  1.3% (84) and under 0.3% of the mean life.
- `code_commit` in the rows up to here is the head when the run ended, with no dirty mark (the review's finding);
  the stepping and counting code did not change from 95fc5bf to the rows of 111. `eqtorus.py` now reads the head,
  with a dirty mark, before a run. The 4 × 4 row was made on an uncommitted tree that became 95fc5bf; its field says so.
- A = 57, 63, 75 were added by this session. Forecasts: `PREDICTIONS.md` block 2 (57, 63, 75) and block 3 (81, 84,
  108, 111), each committed before its runs; scored in blocks 3 and 4.

**The family** (`eq_fit.py`):

| A → A | local slope | | A | ln τ − [13.1623 + 0.20861 (A − 63)] |
|---|---:|---|---:|---:|
| 48 → 57 | 0.2167 ± 0.0001 | | 48 | −0.108 |
| 57 → 63 | 0.2145 ± 0.0001 | | 57 | −0.036 |
| 63 → 75 | 0.2084 ± 0.0002 | | 63 | −0.0001 (0.1σ) |
| 75 → 81 | 0.2099 ± 0.0007 | | 75 | −0.0026 (1.1σ) |
| 81 → 84 | 0.2082 ± 0.0015 | | 81 | +0.0050 (1.6σ) |
| 84 → 93 | 0.2075 ± 0.0007 | | 84 | +0.0037 (1.2σ) |
| 93 → 108 | 0.2084 ± 0.0006 | | 93 | −0.0064 (1.2σ) |
| 108 → 111 | 0.221 ± 0.008 | | 108 | −0.0091 (1.2σ) |
| | | | 111 | +0.028 (1.2σ) |

(Refit on 2026-11-17 with the ten-seed 6 × 6. With its four-seed value the line was 13.1621 + 0.20867 (± 0.00009)
(A − 63), χ² 7.8 on 5, and the slope 93 → 108 read 0.2097 ± 0.0015.)

- **One straight line fits the seven tori from 63 to 111 cells: ln τ_face = 13.1623 (± 0.0007) + 0.20861
  (± 0.00008)·(A − 63), χ² 9.6 on 5.** The price per cell of a wrapped face is 0.2086 ± 0.0001 over that range.
  The fit through 75 to 111 alone has slope 0.2086 ± 0.0002 and puts the line at 13.164 ± 0.004 at A = 63, where
  the torus measures 13.1622: **any deficit at 63 cells is below 0.009** (2σ), against 0.036 at 57 and 0.108 at 48.
  From 81 cells up the slope is 0.2081 ± 0.0003 (χ² 3.7 on 3): with the longer 6 × 6 the local slope no longer
  rises toward 108 cells (93 → 108 is 0.2084 ± 0.0006), and the only high point left is the 111-cell face.
- **The forecast of block 3 (slope 0.2084 from A = 63) was low at all four new tori**, by 0.009, 0.008, 0.020 and
  0.038 (0.8 to 1.4 of its stated errors each; 2.5 and 1.8 errors at 81 and 84 with the fit's own smaller errors).
  Its first criterion holds, its second (the slope 93 → 111) fails by its letter; `PREDICTIONS.md` block 4. The
  agreement of the two local slopes 63 → 75 → 93 to 10⁻⁵ was luck: 93 lies 1.5σ low and 75 lies 1.4σ low.
- **The bend is a break, not a fading correction** (the review's finding at five tori, section 3; the bend still
  rests on the faces at 48, 57 and 63 cells, three kinds of lattice, and without 48 no form can be told from a line;
  what the four new faces add is the straightness above 63): the deficit falls by a factor of 3 over the 9 cells from 48 to 57 and then by more than 5
  over the next 6. No correction decaying smoothly in the loop or in 1/A does that (`REVIEW-gpu-local-tori2.md` section 3: on
  five faces χ² 113 to 117 on 1 for the four decaying forms, 59 to 70 with the 57-cell error inflated, 15 for the
  stretched one; on nine faces 164 to 177 on 5, stretched 31, one-sided quadratic 77); a line with a kink near A ≈ 61 does. Either something changes between shortest loops √19 and
  √21, or the 57 or 63 torus is off by 0.01 to 0.03 for a reason of its own lattice; a second code agrees at both
  (to 0.0007 ± 0.0016 at 57, 0.014 ± 0.011 at 63). [conjecture, untested] A wrapped face shorter than some length
  near 4.5 can die by a route that a longer one cannot (a void that closes on itself around the loop).
  Since then the lead has read the bend as the wrapping across every wrapped face on file: each closed loop of
  loop² 19 or less lowers the price per cell and the discounts add (`research/wrap/`; notebook, "the kink is the
  wrapping").
- **Lattice direction and the firewall channel matter by less than about 0.01 from 63 cells up.** Residuals from
  the line by kind of lattice: along the cube axes with a firewall channel (75, 108) −0.003 ± 0.002 and +0.008 ±
  0.022; in between (81, 84: 6 and 4 transverse layers) +0.004 and +0.002 ± 0.003; rotated with 2 layers (63, 93,
  111) 0.000, −0.008 ± 0.005, +0.025 ± 0.023. χ² 7.8 on 5 allows a scatter between lattices of 0.004 (median) and up
  to 0.014 (95% bound; `REVIEW-gpu-local-tori2.md`).
- Against the lead's readings in part C (theirs to score): the flat one is 0.011 (3.5σ), 0.023, 0.101 and 0.095
  too high at 81, 84, 108, 111. The massive one is within 1.7σ at those four (16.923, 17.552, 22.568, 23.194) but
  0.023 (4.3σ) high at 93 and 0.021 and 0.034 low at 57 and 63.
- **Hazard by age** (`eq_analyze.py`):
  - A = 57, 63, 75: flat from age 60 on (57: within 0.3% in 11 bins from 200 to 5.6 × 10⁵; 63: within 1.1% from
    1,000 to 3 × 10⁶; 75: within 1.5% to 1.8 × 10⁷). Ages 0 to 60 carry 1.6 to 2.0 times the hazard (soups that
    lose a face at once): 0.14% of deaths at 57, 0.05% at 63.
  - A = 81, 84: flat within 1.6% and 2.4% in every bin of 2,000 deaths or more (each within 1.5σ of 1), from age
    3 × 10⁵ to five mean lives (5.6 × 10⁷ and 10⁸); the runs are 20 mean lives long.
  - Lives older than 8 mean lives, against the count for memoryless lives allowing for the end of the run: 2,148
    / 593 / 59 / 28 / 18 against 2,184 / 596 / 50 / 22 / 23 at A = 57 / 63 / 75 / 81 / 84. No excess of old lives
    (the signature of unrecognised cycles).
  - A = 93, 108, 111: the runs are 3.5, 0.2 and 0.2 mean lives long, so the age test has no power there and the
    guard is what excludes cycles. Within that reach the hazard at 108 is flat within errors (four bins, 0.92
    to 1.05, errors 0.04 to 0.08). At 111 it is not: 0.87 ± 0.05 of its mean below 0.03 mean lives and 1.06 ± 0.04
    later, χ² 8.9 on 2 (`REVIEW-gpu-local-tori2.md`); the rise of the local slope from 93 to 111 cells rests on
    that face.
- **Firewalls at 6 × 6:** 44, ln τ_fw = 25.70 ± 0.15 per slab (file: 25.694 ± 0.277). At 81 and 84 cells (6 and 4
  transverse layers) no face died on a firewalled state in 210,512 deaths; one life at 81 settled on one.
- **A = 57, one seed in four is high.** The first two seeds differed by 0.0029 ± 0.0011 (2.6σ), so two more were
  run (57003, 57004, after the review). Seeds 57001, 57003, 57004 give 11.8742, 11.8748, 11.8742 (± 0.0008 each);
  57002 gives 11.8771, 3.0σ above their mean, and the four have χ² 9.25 on 3. The review's own stepper gives
  11.8744 ± 0.0015, the value of the three. Nothing marks 57002 as faulty (same code, same check, hazard flat), so
  it stays in the pooled 11.8751 ± 0.0004; with the error scaled by the seeds' scatter that is ± 0.0007. One 3σ
  seed among the 25 run on these tori is a one-in-fifteen event, not evidence of a fault by itself; a defect of
  the soup hash for particular seeds is the alternative, and it was not tested.
- **Not checked:** a second code at 81, 84, 93, 108, 111 (each kernel is engine-exact on its torus for 2,000
  generations in 5 lanes; the driver's counting is checked by second codes only at 48, 57, 75); whether the
  soup hash is sound for every seed (the A = 57 item above); the raw lives
  behind the old-life counts, which are on this machine only; whether tori of the same area and another
  equilateral lattice agree (there is none at these areas).

**A = 93** (`eqtorus.py run 1 5 31 16 SEED`, seeds 93001-93004, launch cap 2¹⁸):
- Hazard of a face death by age: flat within errors in 11 bins from 0 to 5.6 × 10⁸ generations (ratios to the mean
  0.94 to 1.04, each within 1.5σ of 1); no burn-in is visible (first bin, ages below 1.8 × 10⁶: 0.985 ± 0.041).
- No life settled in any way (kinds 2, 3, 5 all zero in 45,761 lives).
- Against the forecasts committed before the run (`research/constant/PREDICTIONS.md` C): flat 19.479 ± 0.010
  (measured is 0.065 below; its stated refutation line was "below 19.445"), massive 19.437 ± 0.019 (0.023 below),
  rising 19.506 to 19.530 (refutation line "below 19.488"), single-c readings 19.488 to 19.497. Those forecasts
  are anchored on the 4 × 4 value 9.9324, which is 0.0075 too high (above).
- **The 6 × 6 with ten seeds (2026-11-17):** six more runs of 150 minutes give, with the four above, **22.5405 ±
  0.0074** (18,394 deaths; seeds' χ² 6.0 on 9; 298 firewalls, ln τ_fw = 25.970 ± 0.058; no settled or kind-5 life).
  It is 0.012 ± 0.007 below the line 13.1621 + 0.20867 (A − 63) (1.6σ). The family table and the line under it are refit
  with it; the other bullets of this section (residuals by kind of lattice, the lead's readings, the score of block
  3) keep the four-seed value 22.5600 ± 0.0222 they were written with. Hazard by age: nine bins from 0 to 3.3 × 10⁹ (1.07 mean lives), 0.92 to
  1.15, χ² 16.0 on 8; the low bin is ages 3 × 10⁷ to 10⁸ (0.919 ± 0.031), as at 111 cells. Scored in `PREDICTIONS.md`
  block 7.

## Tube and wrapped faces, and thicker slabs (the lead's W11 to W13) [measured]

Asked in `research/GPU-QUEUE.md` (notes of 2026-11-15, 13:05Z to 20:10Z); the lead's forecasts by form are frozen in
`research/wrap/PREDICTIONS.md`, mine in `PREDICTIONS.md` block 5 here, scored in block 6. Driver and estimator as for
the equilateral tori; `eqtorus.py check` passed on each face first (`checks/`); loops² from `loops.py`. No kind-5 life.

| torus (H, K), (0, D) | cells | loops² | seeds | face deaths | firewalls | ln τ_face | seeds' χ² | CPU value on file |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| (1, 3), (0, 25) | 75 | 13, 37, 43 | 2 | 130,931 | 0 | 15.5250 ± 0.0028 | 0.02 on 1 | 15.5363 ± 0.0104 |
| (1, 9), (0, 25) | 75 | 19, 25, 39 | 2 | 110,874 | 92 | 15.6442 ± 0.0030 | 0.09 on 1 | 15.6575 ± 0.0106 |
| (1, 4), (0, 26) | 78 | 21, 28, 31 | 2 | 92,089 | 0 | 16.2884 ± 0.0033 | 0.91 on 1 | 16.2769 ± 0.0120 |
| (1, 12), (0, 28) | 84 | 12, 49, 61, 61 | 2 | 107,478 | 2 | 17.3175 ± 0.0031 | 0.01 on 1 | 17.3248 ± 0.0058 |
| (1, 4), (0, 28) | 84 | 21, 28, 49, 49 | 2 | 105,583 | 0 | 17.5387 ± 0.0031 | 0.03 on 1 | none |
| (1, 17), (0, 32) | 96 | 12, 67, 67 | 8 | 56,775 | 0 | 19.7446 ± 0.0042 (four seeds: 19.7405 ± 0.0059) | 10.0 on 7 | CPU `fr.c`, in progress |
| (1, 16), (0, 36) | 108 | 12, 81, 93, 93 | 8 | 13,641 | 0 | 22.1599 ± 0.0086 (four seeds: 22.1557 ± 0.0121) | 6.8 on 7 | none |

- **The four CPU values repeat** on independent code: differences (CPU − here) +0.007, +0.011, +0.013, −0.012, each
  within 1.2 of its combined error.
- **Tubes of girth² 12 are straight from 84 to 108 cells, at 0.2017 ± 0.0004 per cell.** Second difference of the
  three −0.008 ± 0.017; chords 0.2019 ± 0.0006 and 0.2013 ± 0.0011. That is 0.0070 per cell below the wide faces'
  0.2087, and below the 0.2044 fitted to tubes of 48 to 84 cells (the lead's note of 16:22Z): the tube's slope falls
  with length up to about 84 cells and is steady after. The discount against the wide-face line 13.1621 +
  0.20867 (A − 63) is 0.227, 0.308, 0.397 at 84, 96, 108 cells.
- Against the forms of the lead's table (theirs to score): at 96 and 108 cells the values are 0.039 and 0.076
  below the per-girth straight line (4.8 and 5.3 combined errors), 0.021 and 0.041 below the power form (2.2 and
  2.5), 0.056 and 0.119 above the exponential. Between the power form and the exponential at all three sizes.
- The two long tubes' seeds scatter (χ² 11.8 on 6 together, one seed in each 2σ low). The hazard by age at 108 cells
  is uneven without a trend (six bins 0.95 to 1.06, χ² 11.7 on 5). Those runs are 0.7 and 2.8 mean lives long.
- **One loop of 19** at 75 cells costs 0.019 ± 0.004 ((1, 9), (0, 25) against the 5 × 5); **one loop of 13** costs
  0.138 ± 0.004.
- **A loop of 21: about 0.005, at 2σ.** (1, 4), (0, 26) is 0.004 ± 0.003 below the wide-face line and (1, 4), (0, 28)
  is 0.006 ± 0.003 below it (0.008 ± 0.004 below the equilateral 84-cell face); together 0.0047 ± 0.0023. The
  lead's W13 values for the second: 17.534 if the density relation holds, 17.547 if the effect ends before 21;
  measured 17.5387, 0.9 and 1.9 errors from them. It leans to "still discounts" and does not decide.
- Old lives (older than 8 mean lives) on the five faces whose runs are 18 to 26 mean lives long: 22, 29, 34, 27, 22
  against 23.5, 22.8, 31.5, 24.7, 18.2 for memoryless lives. Age tables: `hist_H_K_D.json`.
- **Thicker slabs** (`eqtorus.py ... m=N`; rows in `research/data/gpu_local_thick/`, checks beside them):

  | torus | cells | layers | face deaths | ln τ_face | minus the 8-layer value |
  |---|---:|---:|---:|---:|---:|
  | (1, 4), (0, 21) | 63 | 12 | 660,097 | 13.1596 ± 0.0012 | −0.0026 ± 0.0014 |
  | (1, 4), (0, 21) | 63 | 16 | 564,434 | 13.1589 ± 0.0013 | −0.0033 ± 0.0015 |
  | (2, 4), (0, 14) | 84 | 16 | 52,480 | 17.5401 ± 0.0044 | −0.0066 ± 0.0054 |

  The price per cell at 16 layers is 0.20863 ± 0.00022 (63 → 84), the 8-layer price. **Depth behind the face does
  not explain the hull's 0.231.** Thicker slabs live shorter by about 0.003 if anything (2.6σ at 63 cells, the two
  thicknesses pooled). Settled lives at 63 cells: 236 in 1,811,510 deaths at 8 layers, 30 in 660,097 at 12 layers
  (23 of period 1 or 2), 1 in 564,434 at 16; settling falls steeply with thickness (not looked into further).
- Not checked: no second code at 96 and 108 cells or on (1, 4), (0, 28); the thicker slabs have one seed each; the
  engine comparison covers the dynamics at 12 and 16 layers, and the face-death test there is the same code as at 8.

### Chain 3 (2026-11-17): more seeds on the tubes, loops of 16 and 13 at 96 cells

Asked in the lead's note of 10:20Z on 2026-11-16; forecasts in `PREDICTIONS.md` block 7, scored in block 8. The 96-
and 108-cell tube rows of the table above now hold eight seeds each.

| torus (H, K), (0, D) | cells | loops² | seeds | face deaths | firewalls | ln τ_face | seeds' χ² |
|---|---:|---|---:|---:|---:|---:|---:|
| (4, 0), (0, 8) | 96 | 16, 48, 64, 64 | 4 | 24,796 | 238,631 | 19.9366 ± 0.0064 | 2.2 on 3 |
| (1, 8), (0, 32) | 96 | 16, 49, 57, 73 | 4 | 25,054 | 239,318 | 19.9284 ± 0.0063 | 5.0 on 3 |
| (1, 3), (0, 32) | 96 | 13, 61, 64 | 4 | 25,797 | 0 | 19.8109 ± 0.0062 | 2.8 on 3 |

- **The 12-tube's low price is real.** With eight seeds each: 17.3175 ± 0.0031, 19.7446 ± 0.0042, 22.1599 ± 0.0086 at
  84, 96, 108 cells; chords 0.2023 ± 0.0004 and 0.2013 ± 0.0008; second difference −0.012 ± 0.012; one line of slope
  **0.2020 ± 0.0003** per cell. The seeds now scatter as they should (χ² 10.0 on 7 and 6.8 on 7).
- **Every short loop bends, the loop of 13 as much as the loop of 12.** Against the wide-face line 13.1623 +
  0.20861 (A − 63) the discounts are:

  | loop² | at 75 cells | at 84 cells | at 96 cells | at 108 cells | discount gained per cell |
  |---:|---:|---:|---:|---:|---:|
  | 12 | | 0.226 | 0.302 | 0.390 | 0.0064 (84 → 96), 0.0073 (96 → 108) |
  | 13 | 0.141 | | 0.236 | | 0.0045 (75 → 96) |
  | 16 | | 0.079 (the 4 × 7 on the slab driver, 17.4645 ± 0.0047) | 0.114 (the two faces pooled, 19.9324 ± 0.0045) | | 0.0030 (84 → 96) |
  | 19 | 0.021 | | | | |

  The loop-13 face is 0.040 ± 0.007 below its short-tube line (my 75-cell value plus 21 × 0.20602) and has slope
  0.2041 ± 0.0003 from 75 to 96 cells. The loop-16 faces are 0.014 to 0.019 below theirs (19.946 to 19.951) and have
  slope 0.2057 ± 0.0005 from 84 to 96.
- **The twist does not matter for a loop of 16:** the two lattices differ by 0.008 ± 0.009, and their firewall rates
  are the same (ln τ_fw 16.979 and 16.978).
- A caution on the two 16-loop faces: firewalls end ten lives for every face death there, so the mean life is 2 × 10⁷
  generations, a tenth of the face time, and the face hazard is sampled on young lives only (oldest 1.1 face times).
  The big faces' hazard has a dip at ages 3 × 10⁷ to 10⁸ (6 × 6: 0.92 ± 0.03), so a value from a firewall-prone
  lattice may sit a little above what long lives would give. Not measured.
- **A CPU second code now exists** (`research/gpu-local/cpu/`: `fr.c`, `fr.py`, its README; written by a subagent,
  not yet reviewed by the lead). Engine-exact every generation on five tori; events equal life by life to a numpy
  implementation on four small vessels; 4 × 4: 9.9252 ± 0.0006. At 63 cells it gives 13.1607 ± 0.0017 at 8 layers
  (here 13.1622 ± 0.0007) and 13.1619 ± 0.0025 at 16 layers (here 13.1589 ± 0.0013: +0.0030 ± 0.0028). On the 96-cell
  tube it has 19.723 ± 0.016 so far (3,899 deaths; the run continues to about ± 0.007), 1.3σ below the value here.
  `python research/gpu-local/cpu/fr.py summary`.
- Not checked: no second code on the loop-16 and loop-13 faces at 96 cells; hazard by age on the five faces was
  saved (`hist_H_K_D.json`) and not read.

## The asymmetric hull face (queue item 3) [measured]

`research/gpu-local/hullface.py`: a local runner around `facelaw.run` (soup 0.35 in |p|₁ ≤ R, exact hull, 8 faces,
T0 = 200, τ_face = 8 × exposure / deaths), guard on (thresholds 16 · 2^j). Rows:
`research/data/gpu_local_hull/hull_R{R}.csv`; `python research/gpu-local/hullface.py summary R`.

- **Kernel shape** (`hullface.py tune 15`; R = 15 has 2,064 nodes): 2 columns per block, one block per SM, the fewest
  thread groups: 3.5 × 10⁸ replica-generations/s in 1,280 replicas, 2.7 × 10⁵ generations/s each. Four columns give
  3.8 × 10⁸ in 2,560 replicas at half the speed each; the slower shape was not taken because the point of the run
  is old ages. Two blocks per SM lose (1.8 to 3.5 × 10⁸): the vessel is past the size where they pay.
- **Engine comparison in that shape** (`hullface.py check`): the five reference vessels of the acceptance bar,
  every generation, 2,000 to 3,000 generations × 5 lanes, all equal; both negative controls fail at generation 1.
- **Calibration at R = 11 (A = 63)**, as `REVIEW-gpu-local-pr23.md` asked before this driver is used here:
  `hullface.py run 11 5 11001` gives **13.6362 ± 0.0013** (614,098 deaths), against 13.6347 ± 0.0011 on file (A10G,
  `research/gpu/README.md` "First use"): +0.0016 ± 0.0017. Hazard by age flat within 2.2% in 13 bins from 200 to 10⁶
  (the largest departure 0.978 ± 0.011). No life settled, no kind-5 life.
- **Hull against torus at 63 cells:** 13.6362 − 13.1622 = 0.474 ± 0.002 (the free face lives 1.6 times longer).
- **A = 108 (R = 15):** `hullface.py run 15 420 SEED`, seeds 15001 and 15002 (2026-11-15 12:00Z to 2026-11-16 02:00Z, 7
  hours each): **ln τ_face = 23.3392 ± 0.0099** (10,187 deaths; seeds 23.3364 ± 0.0138 and 23.3422 ± 0.0142, χ² 0.09 on
  1). No life settled and no kind-5 life, so both exposure conventions give the same value. Lanes reached ages 7.0
  and 6.6 × 10⁹, 4.1 and 3.9 first-death means (τ_face / 8 = 1.71 × 10⁹); the second seed ran 5.6% slower in the same
  wall time (cause not looked for). The run on file (1,059 deaths, ages to 6 × 10⁸) gave 23.376 ± 0.031, 1.1σ above.
- **Hazard by age at A = 108: flat over four first-death means.** Nine bins from age 200 to 7 × 10⁹, ratios to the
  mean rate 0.95 to 1.09, χ² 9.9 on 8. Below 5.6 × 10⁷ (449 deaths) 1.094 ± 0.052; beyond 10⁹ (4,876 deaths) 0.997 to
  1.017 with errors 0.02 to 0.04. So the young ages of the old run and the old ages of this one measure one rate.
  Per-run age tables: `research/data/gpu_local_hull/hist_R15_s*.json` (`hullface.py summary 15 save` writes them;
  `summary` reads them where the scratch json is absent).
- **Scored against `PREDICTIONS.md` block 4** (scored in its block 5): my forecast 23.35 ± 0.02, off by −0.011.
  "One price of 0.2087 per cell plus a term linear in the rim" (23.273 ± 0.010) is refuted at 4.7 combined errors;
  "the second difference repeats" (23.338 ± 0.012) is hit to 0.001.
- **What the four hull faces say** (A = 45, 63, 84, 108, edges k = 5 to 8; 9.820, 13.6353 ± 0.0008 pooling this card
  with the A10G value, 18.141 ± 0.005, 23.3392 ± 0.0099). [measured] The second differences in k are 0.691 ± 0.006
  and 0.692 ± 0.014: the same. [a description, not a law] One quadratic in the edge fits all four:

      ln τ_face = 1.144 + 0.23083·A − 0.3418·k,   A = 3k(k + 1)/2

  (through the last three; it gives 9.822 at k = 5). Read as a price, 0.231 ± 0.002 per cell (0.2301 ± 0.0020 from
  the first three faces, 0.2308 ± 0.0047 from the last three), **0.022 above the wrapped faces' 0.2087**, with a rim
  that shortens life: the face lives like a rimless face of edge k − 0.49 (96 cells at k = 8). The local slopes 0.212,
  0.2146, 0.2166 that have been quoted for hull faces are this form's chords and rise toward 0.231.
- **Hull against torus at equal area** grows: 0.474 ± 0.002 at 63 cells, 0.594 ± 0.006 at 84, 0.779 ± 0.024 at 108.
- **Not established:** that 0.231 is a price. Four values fix a quadratic with one to spare. The tori's price with
  a rim term survives only if small hull faces live longer than that form by 0.197 or more at 45 cells and 0.066 at
  63 and by nothing from 84 on (the opposite sign to the tori's small-size deficit). The 135-cell face separates
  the two (29.230 against 29.163; on file 29.34 ± 0.25) and is beyond this card (about 40 deaths a day). What makes
  a hull cell dearer than a torus cell is open: depth behind the face (8 layers on the tori; tested next, `PREDICTIONS.md`
  block 5), the wrapping itself, or the seven other faces.

## The cycle guard [measured]

`research/gpu/guard.py`, hooked into `facelaw.run(..., guard=FIRST)`; off by default (`guard=0`), and with the guard
off the driver's code path is the previous one. Rule (`research/gpu/AGENT.md` "To do", option (i)): one snapshot per
replica, taken at the first launch boundary at which its age is ≥ FIRST · 2^j, j = 0, 1, …; at every launch boundary a
live replica equal to its snapshot ends as **kind 5** (censored, like kinds 2 and 3), at the boundary generation.
Results with the guard state the thresholds (`out['guard']`: `first`, and per kind-5 life the replica, the age at
recognition and the snapshot's age).

Tests, `python -u research/gpu-local/guard_test.py all` (about 3 min):

- **Planted cycles, exact.** The 373 engine-run R = 9 soups (cycle start c and period P from `gump ensemble`, P = 1 to
  66), tiled over all 1,280 lanes, faces off, the kernel's own freezing off. Two states at generations s < b are equal
  iff s ≥ c and P | (b − s), so the guard's detection boundary is a function of (c, P, boundaries, thresholds),
  computed in plain Python (`predict`). Launch lengths 1024, 1000, 997 (prime) and a mixed cycle 997, 1024, 4096;
  FIRST = 16 and 1000: **every lane recognised exactly at the predicted boundary** (8 settings × 1,280 lanes).
- **As in production** (freezing on, pw = 32, K = 1000 and 4096): the 7 lanes holding the period-48 and -66 soups end
  as kind 5 exactly at the predicted boundary; the other 1,273 end by the kernel (kind 2 at c + 2, kind 3 at L + P,
  as `check_periodic` requires) and none as kind 5.
- **Negative controls** (each must fail the exact test): snapshot taken before the comparison (1,280 lanes wrong),
  comparison with the neighbouring column's snapshots (1,277 wrong), thresholds that never double (1,082 wrong):
  all caught.
- **Guard on vs off, same seed, fixed launch length and generation cap** (`facelaw.run(..., launch_gens=K,
  max_gens=G, keep_reps=True)`): lives (age, kind, birth, replica) equal lane for lane on R = 15 (2^20 gens), R = 9
  (2^21 gens, 979,357 lives; also with pw = 32 and pw = 1), R = 11 (pw = 16, K = 997, FIRST = 1000). No kind-5 life
  occurred in these runs: at R = 9-11 a face dies long before a soup settles into a long cycle.
- **The driver's kind-5 path, on natural cycles** (R = 9, faces off, pw = 1, so a life ends only by settling and the
  kernel recognises only periods 1-2): 7,851 lives recognised by the guard in 2^19 generations; guard off, the same
  lanes are held to the end by those cycles (19,260 lives against 125,107). 1,272 lanes agree exactly up to their
  first kind-5 life, and guard off that life (same birth) is still running at the age the guard ended it.

**A guarded run is not bit-identical to an unguarded one after the first kind-5 life.** The drivers draw each reseed
from (seed, a counter that advances at every boundary where some life ended). The first time the guard ends a life at
a boundary where the kernel ended none, the counters part and every later soup differs (same distribution, different
draws). The test above compares lives born before that boundary. A run with no kind-5 life is bit-identical to the
unguarded run.

**Detection latency (a property of option (i), measured in the exact test).** A replica that enters a cycle of
period P at age e is recognised at the first boundary b with a snapshot s on the cycle (s ≥ e) and P | (b − s).
Two delays add:
- *Snapshot delay* s − e: snapshots are taken at doubling ages, so s − e is up to about e (+ one launch). A life
  that settles at age e can therefore stay unrecognised for up to about e more generations.
- *Grid delay* b − s: comparisons happen only at boundaries, so b − s runs over the launch grid. With a fixed launch
  length K a match comes within lcm(K, P) of s; if the snapshot interval is shorter than that, the next (doubled)
  snapshot is needed. In the test, horizon 2^17 left 4-25 lanes unrecognised for K = 997 or mixed launches (as the
  prediction said), 2^19 found all. The drivers' launches are powers of two (K doubles from 1024), so for odd P
  (the clockwork objects' 9, 11, 13) the grid delay is P launches, about P × K generations.
So the guard turns zombie exposure from "until the run ends" into "at most about the settling age plus P launches"
per recognised life. Both terms are bounded per life by what is recorded: zombie time ≤ b − birth, and the
snapshot age shows how much of it can be grid delay. Not removed: lives still open at the end of a run.

**How large the latency can be, and the exposure convention** (corrected after
`research/audit/REVIEW-gpu-local-pr23.md` section 1; an earlier version here conjectured that both delays are small
against a mean life, which is false). The guard matters only for periods above the kernel's 128. For an odd period P
the grid delay is P·K: at least 3.4 × 10⁷ generations at the launch cap K = 2¹⁸ of the torus and hull runs here, and
at least 2.2 × 10⁹ at `facelaw.py`'s own cap of 2²⁴. That is a mean life or more for the tori up to 93 cells (2% of a
first-death mean for the hull at R = 15). So one kind-5 life can carry more than a mean life of exposure spent inside
its cycle.
- **Convention.** Every guarded result states its kind-5 count. Where it is not zero, ln τ is given both ways: with
  kind-5 lives counted to the age at recognition (the rows' `exposure`), and with their exposure cut at the snapshot
  age. The snapshot state is on the cycle (it is the state that recurred), so the cut removes only time spent in the
  cycle; what remains is the time from entering the cycle to the snapshot, at most about one doubling. The cut value
  is the one to quote. `eq_analyze.py` and `hullface.py summary` print both; the hull rows carry
  `exposure_guard_past_snapshot`, the torus tables `hist_A_K_B.json` carry each kind-5 life's two ages.
- In every result so far the kind-5 count is zero and the two values coincide.
- Exact entry ages can be recovered offline if kind-5 lives turn up in numbers: every life is a deterministic
  function of (seed, reseed round, replica), so it can be re-run from its birth.
