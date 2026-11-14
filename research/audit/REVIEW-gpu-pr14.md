# Review of PR 14: firewall-resolved slab faces (GPU round two, rerun)

Branch `origin/claude/awesome-cray-boq9vz` (2f9b262, 37bf879, 3fa1bf5). It changes `research/gpu/README.md`,
`research/gpu/PREDICTIONS.md` and five `research/data/gpu_facelaw/fwslab*.json`. The code is `research/gpu/fwslab.py`, which is
on main and had not been reviewed before this. The reviewer's scripts are in `research/audit/gpu_pr14/`. Date: 2026-11-14.

## Verdicts

| claim | verdict |
|---|---|
| 1. Validation at 3×6×8 and 4×7×8 | **stands with a correction.** The numbers are reproduced by an independent CPU run. The 12.6% share is not a detection deficit. The "off-direction" firewall counts are a labelling artefact. |
| 2. Production 6×7×8: 92 face deaths / 29 firewalls; ln τ_face = 26.405 ± 0.104; ln τ_fw(216) = 26.866 ± 0.186; forecasts hit | **stands.** The "1.8σ above the line" needs the line's own error added: it becomes about 1.2σ. |
| 3. Control 6×6×8, pooled A = 108, slope 0.215 ± 0.006, "not decided" | **numbers stand; the reading needs a correction.** "Leans toward a mild rise" is not supported over a shape effect. The README's ln τ_fw column mixes a per-slab rate with a per-direction rate. |

Reproduce:

    B=origin/claude/awesome-cray-boq9vz; mkdir -p research/scratch/pr14
    for f in fwslab3x6x8_s601_A10G fwslab4x7x8_s602_A10G fwslab6x6x8_s621_A10G fwslab6x7x8_s611_A10G fwslab6x7x8_s612_A10G; do
      git show $B:research/data/gpu_facelaw/$f.json > research/scratch/pr14/$f.json; done
    python3 research/audit/gpu_pr14/recompute.py research/scratch/pr14        # all table numbers, from raw where it exists
    python3 research/audit/gpu_pr14/cpu_channels.py validate 3 6 8 3000       # rep.c on the skewed slab against the engine
    taskset -c 3 python3 research/audit/gpu_pr14/cpu_channels.py run 3 6 8 400000 14001 8
    for s in 14002 14003 14004 14005 14006 14007; do taskset -c 3 python3 research/audit/gpu_pr14/cpu_channels.py run 3 6 8 400000 $s 64; done
    python3 research/audit/gpu_pr14/cpu_channels.py analyze 3 6 8             # channel-resolved CPU, and fwslab's rules emulated
    python3 research/audit/gpu_pr14/shape.py                                  # face-channel residuals by slab shape

(Seven runs, 25,088 replicas, one life each; about 15 minutes on one core.)

## Recomputation from the JSON files

`recompute.py` has its own unpacking and estimators. It does not use `fwslab.summary`.

- **What can be recomputed.** Only 6×6×8 and the two 6×7×8 files carry `raw`. The validation runs have 2.2 × 10⁶ and
  7.9 × 10⁴ lives, which is over `raw_cap` = 60,000. For those two only the totals can be re-derived.
- **Integrity of `raw`.** Where it exists, the per-life data reproduce every total exactly:
  - lives = replicas + events;
  - Σ age = exposure;
  - counts by kind and by direction match the stored totals;
  - 4,608 open lives in each file.
- **Every number in the README table and in both outcome blocks is reproduced to the last digit**, including:
  - 3×6×8: 11.084 / 12.327 / 12.61%;
  - 4×7×8: 17.465 / 17.106 / 41.72%, first-event statistic 16.925;
  - 6×7×8: 92 / 29 / 23.97%, 26.405 ± 0.104, 26.866 ± 0.186, first-event statistic 26.131;
  - 6×6×8: 592 / 13 / 2.15%, 22.568 ± 0.041, 25.694 ± 0.277, first-event statistic 22.547;
  - pooled A = 108: 22.536 ± 0.031;
  - slope 108 → 126: 0.2149 ± 0.0060, and 0.2186 ± 0.0064 against the unscreened 22.470.
- **The slope error does carry both points' errors:** √(0.104² + 0.031²)/18 = 0.0060. It does not carry the line's error or
  any shape scatter (see claim 3).
- **The two 6×7×8 runs agree.** Seed 611 gives 26.517 ± 0.156 and seed 612 gives 26.304 ± 0.140: a difference of 1.0σ.
- **Firewall lives at 6×7×8 and 6×6×8.** All 29 + 13 firewall lives end exactly on a launch boundary: each was detected
  there, and none at a face death.

**Forecast order** (`git log --format='%h %cI %s' origin/claude/awesome-cray-boq9vz -- research/gpu/PREDICTIONS.md`):

- **The forecasts' text is unchanged.** The production forecast is 60846f8 (06:42:25Z). The only later edit before the
  outcome is fc699f8, 15 s later, which changes headers only.
- **The order is consistent with the commit times but cannot be proved from the data.** The JSON records `wall_s` but no
  start time.
  - Production: the outcome commit is 37bf879 (07:51:51Z), 69.4 min after the forecast, for two 60-min runs.
  - Control: the forecast is 2f9b262 (07:51:27Z) and the outcome is 3fa1bf5 (08:07:22Z), 15.9 min apart, for a run of
    900.3 s. The run would have to have started within about 55 s of the forecast commit.
- **The control's forecast was written after the 6×7×8 result was known.** It says so ("while 126 stays at 26.405"), and
  that is fine. It forecasts A = 108 only.

## Claim 1: validation — stands, with a correction

**Independent CPU check, channel-resolved.**

- **Stepper.** `research/peeling/rep.c` on `geom.slab`; neither is PR 14's code.
- **Bit-exactness on this vessel.**
  - The slab is tiled 8× into an engine 12-torus. The population trace matches the engine's, × 8, every generation for
    3,000 generations.
  - The same holds for 6×7×8 (42-torus, × 42) and 4×7×8 (28-torus, × 28), 2,000 generations each.
  - The neighbour table equals the one built from `docs/AUTOMATON.md`'s offsets for every cell.
- **Run.** 25,088 lives at 3×6×8, p = 0.4. Times are exact to 16 generations. Each life ends at its first event:
  - a face death, the earlier of the two face layers' last-alive times;
  - a firewall, at its formation, which is the latest death of three cyclically consecutive transverse layers;
  - or settling, censored.

| 3×6×8 | face / firewall (share) | ln τ_face | ln τ_fw | first-event |
|---|---|---:|---:|---:|
| CPU, truth (firewall at formation) | 21,896 / 3,188 (12.71 ± 0.21%) | 11.076 ± 0.007 | 12.310 ± 0.018 | 10.940 |
| CPU histories with `fwslab.py`'s rules applied (launches of 2¹⁸) | 21,896 / 3,160 (12.61%) | 11.082 | 12.325 | 10.947 |
| **GPU (PR)** | 1,917,760 / 276,769 (12.61 ± 0.02%) | **11.084 ± 0.001** | **12.327 ± 0.002** | 10.950 |
| CPU table `slab_fw.csv` (512) | 438 / 74 (14.45%) | 11.098 ± 0.048 | 12.18 ± 0.12 | — |

- **The GPU agrees with its own rules applied to independent histories** within 0.002 in ln τ_face, 0.002 in ln τ_fw and
  0.00 in share.
- **The CPU table's 14.45% is a fluctuation, not a detection deficit.** Against 12.7% it is 1.2σ (binomial, n = 512). The other
  CPU samples of 512 give 65/512 (PR 12 review, `fwrun.py`), 58/512 (`fl.c`, quoted in 60846f8) and 69/512 (seed 14001,
  here).
- **What the attribution rules cost at 3×6×8.**
  - **Firewall to face death.** A firewall-first life's face dies a median of 1,088 generations after the firewall: mean
    1,346, 90% quantile 2,960. Only 18 of 3,188 face deaths come after the cap.
  - **Exposure.** Counting a firewall life's exposure to its *detection* rather than its *formation* adds 0.6% to the
    exposure.
  - **Firewalls labelled settled.** 28 of 3,188 firewall lives (0.9%) settle before their face dies. Inside one launch
    `fwslab.py` would label them settled, because it remaps only kind 1. This is an upper bound: a period-> 2 cycle is
    caught only at the next launch start, after the boundary's firewall test.
  - **Net effect:** +0.006 on ln τ_face and +0.015 on ln τ_fw at 3×6×8. That is below the validation tolerance and below
    all quoted errors at 6×7×8.
- **At 6×7×8 the rules cost nothing measurable.** Every firewall life ended at a boundary, so the overcount is at most
  29 × 2¹⁸ = 7.6 × 10⁶ generations, which is 6 × 10⁻⁷ of the exposure.
- **The `fwslab.py` docstring is wrong for 3×6×8.** It says "resolution one launch … against means of 10⁷ and more". At
  3×6×8 the mean life is 2.8 × 10⁴ and K reaches 2¹⁸. The argument is not true there; the conclusion survives only
  because the face dies soon after a firewall.

**Correction (direction labels).** `firewalled()` labels a replica with the lowest-numbered diagonal that has a firewall
*at detection*. It does not label the diagonal that formed one first.

- **What the CPU histories show.** All 3,188 firewall-first lives formed their firewall on the cheapest diagonal (d = 2)
  first. Diagonals 1 and 3 (cut 216, equivalent under x ↔ z in this slab) gain firewalls only later, as the slab dies
  down. By the cap, 2,692 of 4,096 replicas in one run have one on d = 1, always together with d = 2.
- **What that means for the GPU counts.** The 229 (3×6×8) and 23 (4×7×8) "off-direction" firewalls are late detections
  labelled 1 because 1 is checked first. The 0 on the symmetric diagonal 3 is the tell.
- **So the forecast holds.** "Firewalls by direction: all in the cheapest one" holds by formation. The README's "276,540
  of 276,769" understates it.
- **For 6×6×8** (3 / 4 / 6 over three equivalent directions) the labels are uninformative, and the claim does not use them.

**Other checks:**

- **Settled replicas.** At 3×6×8 only 4 of 25,088 CPU lives settle or stay open with the face alive before their first
  event. The CPU detects any period dividing 840, and censors the rest at a cap of 14 mean lives. So undetected long cycles
  (period > 128) are below 0.02% of lives there. The GPU's 1,127 settled lives (0.05%) are of the same order.
- **4×7×8.** It was not re-run channel-resolved here, because τ ≈ e¹⁷. Its totals reproduce. The CPU table's event share
  is 85/214 = 39.7 ± 3.3%, against the GPU's 41.7%. Its first-event statistic 16.925 matches the earlier review's CPU
  16.934 ± 0.068.

## Claim 2: production 6×7×8 — stands

- **Recomputed from `raw`.** Exposure 1.349 × 10¹³, 92 face deaths and 29 firewalls, all on diagonal 2. Diagonal 3's ring
  has 2 layers (gcd(6, 7) = 1) and cannot hold a T3 firewall. 0 settled and 9,216 open.
- **Detection logic.**
  - A face death that follows a firewall inside one launch is attributed to the firewall: the kept state at the death
    still contains it (T3; frozen replicas keep their state under `K_KEEP = 1`).
  - A face death that comes first freezes the replica, so no later firewall can be credited to it.
  - The rings' moduli (4N₁, 4N₂, 4·gcd) equal the transverse periods of the slab lattice ⟨(N₁,0,−N₁), (0,N₂,−N₂)⟩.
  - All positions of all three oblique families are tested; a ring with fewer than 3 layers is skipped, which is correct.
  - `K_KEEP` drops nothing. It freezes a replica at its event generation, and every frozen replica is reseeded at the next
    boundary.
- **The stepper is the validated one.** `kernel.cuh`, `kernel_shared.cuh`, `gsim.py`, `vessels.py` and
  `research/peeling/geom.py` are unchanged since 3b3ceb7, the engine-checked slab commit (`git diff 3b3ceb7 origin/main --
  <those files>` is empty). `fwslab.py` calls `gsim.Sim(v, backend='gpu', keep=True)` with the default configuration. The
  `keep` path was checked against `fl.c` on octahedral vessels (`check_keep`), not on slabs; the kernel code is the same.
- **Burn-in.** Exposure counted from generation 0 is the CPU table's convention, and the transient (about 10³ generations)
  is 10⁻⁸ of τ.
- **Correction to the strength statement.** The README quotes "+0.19 above the slab line (1.8σ)" with the statistical
  error only.
  - The line extrapolated to A = 126 has its own error: ±0.074 from the fit covariance, ±0.124 after scaling by
    √(χ²/dof) = √(19.5/7). (`recompute.py`; `face_law_fit.py`'s selection.)
  - With that error the offset is +0.19 ± 0.13–0.16, about 1.2–1.5σ.

## Claim 3: control 6×6×8, pooling, slope — numbers stand; the reading is corrected

- **The two A = 108 runs agree.** Their first-event counts against exposure give z = −1.24.
- **Pooling is legitimate.** Scaling the earlier run's 447 deaths by (1 − 0.0215) uses the control's own measured share.
  The share's error (±0.6%) moves the pooled value by about 0.003. It slightly overcounts the old run's exposure (its
  firewall lives ran on to their face deaths), but by under 10⁻⁵ of the exposure.
- **The forecast miss is honestly reported.** The forecast was 22.49 ± 0.07 and the result is 22.568, outside by 0.008.
- **The README's ln τ_fw column mixes two rates.**
  - For 6×6×8 the entry 25.694 is per slab, summed over three cheapest directions. Per direction it is 26.79 ± 0.28.
  - That agrees with 6×7×8's single-direction 26.87 ± 0.19 at the same cut of 216, which is itself a check that the cut
    sets the firewall rate. The table should say which rate each entry is.
- **"Leans toward a mild rise" is not supported over the alternative.** The firewall-resolved CPU face channels
  (`slab_fw.csv`, `shape.py`) show the residual from the line rising with the slab's *short side*:

  | short side | slabs (residual, nats) |
  |---:|---|
  | 3 | 3×3 +0.07/+0.00, 3×4 −0.07, 3×5 −0.01, 3×6 −0.09 (GPU −0.10), 3×8 −0.31 ± 0.12 |
  | 4 | 4×4 +0.01, 4×5 +0.05, 4×6 −0.05, 4×7 −0.02 (GPU +0.02) |
  | 5 | 5×5 +0.11, 5×6 +0.24 ± 0.17 |
  | 6 | 6×6 +0.08 (pooled) / +0.11, 6×7 +0.19 ± 0.10 |

  - **A short-side term fits the CPU data.** Fitting a + b·A + c·(short side) to the CPU rows (short side 3–5, without the
    elongated 2×8 and 3×8) gives:
    - c = 0.114 ± 0.038, with χ² falling from 17.2/9 to 8.2/8;
    - b = 0.2057 ± 0.0014;
    - predictions of **22.564 ± 0.059 for 6×6×8** (observed 22.568, pooled 22.536) and **26.267 ± 0.068 for 6×7×8**
      (observed 26.405 ± 0.104, +0.14, 1.1σ).
  - **This model is post hoc** (one parameter chosen after looking), so I do not claim it.
  - **What it does show.** Both points sit above the A-only line by an amount that a constant per-cell cost plus a
    short-side effect explains as well as a rising per-cell cost does. "Not decided" is the right strength; "leans toward a
    mild rise" is not.
- **Square against non-square, for the face channel.**
  - **The firewall side is settled.** The concern was that the number of cheapest directions differs, which affects only
    the firewall channel, and that channel is now resolved.
  - **What remains is the in-plane shape.** It acts on the face channel through the torus's side lengths. 6×6 → 6×7 keeps
    the short side, so on the evidence above it is the gentler kind of shape change.
  - **How one would tell:**
    - same-A pairs of different shape, firewall-resolved, as above;
    - better, fixed short side with growing A, for example 6×6, 6×7, 6×8 (A = 144, far too slow);
    - or fixed A with short sides 5 and 6.
  - None of these is cheap at A ≥ 108.

## Required fixes before merge (text only; no rerun needed)

1. **Direction labels** (README and PREDICTIONS outcome).
   - Replace "Firewalls in the cheapest direction: 276,540 of 276,769 and 32,817 of 32,840" with: *labels are the
     lowest-numbered diagonal holding a firewall at detection; the 229 and 23 labelled d = 1 are late detections; an
     independent CPU run (`research/audit/gpu_pr14/cpu_channels.py`) finds 3,188 of 3,188 firewalls formed first on the
     cheapest diagonal at 3×6×8.*
   - Optionally, record the formation-order direction in future runs by testing the rings in cut order.
2. **README table, ln τ_fw column.** Mark 6×6×8's 25.694 as *per slab, three directions*, and add the per-direction value
   26.79 ± 0.28, to compare with 6×7×8's 26.87 ± 0.19.
3. **The reading** (README paragraph and the 08:07Z outcome block).
   - Drop "leans toward a mild rise", or put beside it that a short-side effect at constant per-cell cost fits equally
     well (this review, `shape.py`).
   - Quote the offsets above the line with the line's extrapolation error: A = 108, +0.08 ± 0.03 (stat) ± 0.06–0.10
     (line); A = 126, +0.19 ± 0.10 ± 0.07–0.12. "1.8σ" becomes about 1.2σ.
4. **`fwslab.py` docstring.** The resolution argument ("against means of 1e7 and more") is false at 3×6×8: mean life
   2.8 × 10⁴, K = 2¹⁸. State the measured effect of detection-time exposure and of settle-after-firewall instead: +0.006
   (face) and +0.015 (firewall) at 3×6×8, negligible at A ≥ 84.

Not blocking, for future runs:

- record the UTC start time in each JSON, so that a forecast's order can be checked against the data;
- keep `raw` for validation runs, compressed or subsampled, or at least age histograms by kind.

## Not checked

- The GPU runs themselves: there is no Modal access, and no GPU run was repeated.
- The two validation runs' per-life data, which are not stored.
- A channel-resolved CPU check at 4×7×8 or larger.
- Bit-exactness of `keep = True` on slab vessels specifically.
- Long cycles (period > 128) at 6×6×8 and 6×7×8. They are bounded only at 3×6×8: below 0.02% of lives.
- How often interior {111} firewalls (along the slab normal) precede the face deaths counted at 6×7×8. The convention is
  the same as the CPU line's, so the comparison is like with like, but the face channel includes such deaths.
- The short-side model beyond the existing CPU table. No new shape runs were made.
- The `rep.c` check compares population traces, not states.

## Recommendation

**Merge after fixes 1–4.** They are text only. All the numbers stand, and the 3×6×8 validation is independently confirmed.
