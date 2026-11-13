# Review of pull request 8 (research/gpu: GPU ensembles on Modal)

Adversarial review, 2026-11-13. Branch `claude/awesome-cray-boq9vz` at **be7b01d** (unchanged at fetch time).
Worktree used read-only; no GPU, no Modal. Scripts: `research/audit/gpu_pr8/` (some written by an earlier reviewer
that stopped before writing a verdict; each is re-read and its use stated below).

Status: in progress. Verdicts are written as they are reached.

## Files touched outside research/gpu/ and research/data/gpu_facelaw/

## Claim 2: asymmetric face law curves upward (A = 108, 135)

**Verdict: the numbers are confirmed as far as the committed data can confirm them; the headline framing ("0.39 nats,
13σ above the line this repo had extrapolated") is wrong as a measure of anything and must be restated.** What
survives: the local slope keeps rising past A = 84, and A = 108 sits 0.21 ± 0.04 nats above the straight line through
the *verified* CPU points A = 45–84. What does not: that this is a new upward bend, or a 13σ effect.

Ran:

    python3 research/audit/gpu_pr8/rederive.py PR8      # earlier reviewer's script; read and kept: own unpacking, own sums
    python3 research/audit/gpu_pr8/dupcheck.py PR8      # new: repeated death ages vs a chance estimate
    python3 research/audit/gpu_pr8/curvature.py         # new: fits to verified CPU and GPU points

(PR8 = the worktree at be7b01d.) Findings:

1. **The table re-derives exactly** from the committed JSON with independent code: ln τ_face = ln(8 · exposure /
   deaths) after T0 = 200 gives 13.635 (764,941), 18.141 (34,026), 23.376 ± 0.031 (1,059), 29.341 ± 0.250 (16, three
   runs). The stored aggregates agree with the stored per-bin hazards and, where raw lives are stored, with the raw
   lives (sum of all ages = replicas × generations to 1.5 × 10⁻³ or better).
2. **Definition is the repo's.** τ_face = 8 × (mean wait from age 200 to the first extinct face layer of 8) in the
   exact hull of an asymmetric p = 0.35 soup on |p|₁ ≤ R; lives ending before 200 are excluded with their exposure;
   lives open at the end are censored (exposure counted, no death); estimator exposure/deaths. Same as
   `research/fluct/` and `verify_face_law.py`. Calibration holds: A = 63 GPU 13.635 ± 0.001 vs CPU-verified
   13.633 ± 0.008; A = 84 GPU 18.141 ± 0.005 vs CPU 18.077 ± 0.054 (1.2σ). The result is independent of T0
   (60, 200, 1000, 10⁴ all give 23.376 at A = 108; 18.141–18.142 at A = 84).
3. **Start of clock / censoring.** Birth is the end of the launch at which the replica was reseeded; the death age
   is exact to the generation (launch start + in-launch generation − birth). Frozen time after a death is not
   counted. Correct.
4. **No sign of stuck (settled, never-dying) replicas inflating exposure.** These runs predate period-3+ detection,
   so "no settles recorded" is evidence only for period 1–2 (kind 2 was detected and is 0 in 800,000 lives). The
   evidence for period ≥ 3 is indirect but adequate: a stuck fraction f would make the hazard fall at old ages.
   R = 11 (ages to 15τ): hazard flat to 6–15τ (3,305 deaths vs 3,238 expected), f ≲ 10⁻⁵. R = 13: ages ≥ 3τ give
   626 deaths vs 655 expected (0.96 ± 0.04), f ≲ 0.4%. R = 15: deaths after age 1.8 × 10⁸ 211 vs 200 expected —
   flat. To inflate A = 108 by 0.39 nats a third of the replicas would have to be stuck; excluded.
5. **Error bars** are 1/√deaths in ln τ, right for an exponential wait with independent lives (each life a distinct
   soup; see claim 6). Not inflated by duplicates: repeated death ages within the R = 13 run are 37 pairs vs 34.6
   expected by chance (estimated from near-coincidences, `dupcheck.py`); the earlier reviewer's "~8.5" chance figure
   was a crude uniform-density estimate and is wrong.
6. **The 13σ is not a test of curvature.** The line 0.2077·A + 0.55 is the endpoint of a quasi-stationary
   distribution fit (fluct README correction 1), not a fit to lifetimes, and it already misses verified lifetimes:
   A = 45 by −0.08 nats (28σ, critic board E2) and A = 84 by +0.08. The σ quoted is the GPU point's alone. Measured
   against lifetimes:
   - local slopes, verified CPU then GPU: 0.2010 (30→45), 0.2119 (45→63), 0.2116 ± 0.0026 (63→84),
     0.2208 ± 0.0026 (84→108, CPU 84) or 0.2181 ± 0.0013 (GPU 84), 0.221 ± 0.009 (108→135). Rising — but it was
     already rising from A = 30 to 63, so the bend is not new beyond A = 84;
   - the straight line through verified A = 45, 63, 84 predicts 23.167 ± 0.028 at A = 108: GPU is +0.21 (≈5σ);
   - curved fits (a + bA + c√A or quadratic) through verified A = 45–84 predict 23.15 ± 0.16–0.19: GPU is +0.23
     (≈1.2σ), i.e. consistent with the curvature already present; through A = 30–84 they predict 23.59 / 23.93,
     *above* the GPU value (but no 3-parameter form fits A = 30–84 well: χ² 7.9 and 19.5 for 1 dof);
   - GPU points alone (63, 84, 108): quadratic coefficient 2.6σ; with A = 135 2.8σ. With CPU 45–84 + GPU 108:
     4.9σ in either curved form.
   **Dropping subsets:** without A = 135 nothing changes; without A = 30 the curvature is 4.9σ; with only GPU points it
   is 2.6σ. The curvature survives every cut; its size is model-dependent.
7. **The conjecture "0.208–0.209 per site extrapolations are lower bounds"** follows from rising local slopes
   (all ≥ 0.211 from A = 45 on), so it is plausible; note that the rim-free slab slope is 0.2088 ± 0.0009, so
   octahedral faces at A ≥ 45 cost *more* per site than slab faces, which the PR does not discuss. Free 3-parameter
   fits give asymptotic slopes 0.23–0.26 for a + bA + c√A, which shows the extrapolation is not determined by
   these data; the PR should not quote a single asymptotic number and does not.
8. **R = 17:** 16 deaths in three runs at ages ≤ 0.0015τ; it rests entirely on the hazard being flat over three
   more decades (the PR says so). The seed-3 run was kept from a batch whose three containers ran the same initial
   soups (permuted; see claim 6); keeping one of three is legitimate as long as the choice was not made by outcome.
   Whether it was is not checkable (the other two files are not committed); immaterial at ±0.25.

Not checked: the kernel's correctness at R = 15 and 17 on a GPU (see claim 1); an independent CPU measurement at
A = 108 (≈ 1 death per 6 minutes on one core; not enough in the time available to test a 0.2-nat effect).
An independent CPU measurement at A = 84 is below (filled in when the run ends).

## Claim 6: seed-collision bug found and fixed

**Verdict: confirmed — the bug is as described, the fix removes it, and no committed result is contaminated.** One
weakness in the guard that was added (below).

Ran `python3 research/audit/gpu_pr8/seedhash.py` (new: a Python copy of `soup_bit`'s seed/replica hashing, old and
new, fed the seeds exactly as `facelaw.py` and `postpeel.py` pass them: `(s << 32) + rnd`, rnd = 0 for the initial
soups and +1 per reseed round) and `dupcheck.py` (above).

- Old hash `mix64(seed ^ (r << 32))`: seeds 1, 2, 3 in parallel → 409,600 of 614,400 (seed, round, replica)
  streams collide (the runs are permutations of each other); a single seed → 0 collisions. So the R = 11, 13, 15
  runs (single seed 1, old hash) contain no internal duplicates, as the PR says, and R17_s3 (old hash) is internally
  clean.
- New hash `mix64(mix64(seed) + r)`: 0 collisions for seeds (1, 2, 3) and (3, 11, 12); old-s3 vs new-s11/s12
  streams share nothing. A collision now needs `mix64(s) + r = mix64(s') + r'` mod 2⁶⁴, chance ~ (runs² × replicas) /
  2⁶⁴: nil. Lanes of one 32-bit word are distinct replicas r, so they cannot collide; containers differ by seed
  (`copies` gives seed, seed+1, …).
- Committed data: no death age > 10⁴ is shared between the three R = 17 runs; within runs, repeated ages match
  chance (R = 13: 37 pairs vs 34.6; vertex R = 40: 8 vs 6.7, and the raw births of those 8 pairs are all different,
  so they are different soups). Runs with > 50,000 deaths (R = 11, vertex R = 36, 38) store no ages and cannot be
  checked this way; they are single-seed runs, clean by the argument above.
- Every committed file has a distinct seed per (vessel): 1 (R = 11, 13, 15), 3/11/12 (R = 17), 101–103, 201–203,
  301–302.

Weakness: the duplicate guard in `facelaw.py summary` keys shared ages by `r['seed']`, so two files **with the
same seed** (the realistic mistake: re-running `--seed 12`) produce one seed per age and **no warning**; it also
only prints, and is blind to runs with > 50,000 deaths. Fix: refuse to merge two runs with equal (vessel, seed), and
key the age check by file.

## Claim 3: symmetric faces at A = 759, 828 against forecasts

**Verdict: the three numbers are confirmed from the committed data and the forecasts were committed first; the
pipeline agrees with independent CPU data where sizes overlap. One unflagged caveat: in both cube-centred runs the
hazard falls with age (p = 0.04 and 0.01), so "τ = mean residence" there is a rate over the observed window.**

Ran `rederive.py`, `agetrend.py` (new: Weibull fit with right censoring, likelihood-ratio test of a constant hazard,
on every run with raw lives; a power-law-in-age fit on the age bins otherwise), and `git log`/`git show --stat` on the
PR branch.

- **Order of commits:** forecasts `0171bd9` (18:01:46Z, PREDICTIONS.md only); settle detection to period 128
  `d67ad50` (18:13Z); R = 36/38 vertex data `2cd7142` (18:25Z); R = 43c, 45c, 44v, 40v data and outcomes `be7b01d`
  (19:01Z). The outcome section only appends (`git diff 0171bd9 be7b01d -- PREDICTIONS.md` has no removed lines).
  Commit times are the author's own clock, so this shows order, not wall time. Supporting evidence that the
  symmetric runs came after the forecasts: they used the period-128 settle test (`kind 3` counts are present in
  their JSON) that was committed only at 18:13, after the forecast commit. The A = 108/135 "expectation" is honestly labelled as recorded
  after the fact.
- **Re-derived** (T0 = 1000, τ = exposure/deaths): 43c 21.903 ± 0.031 (1,057), 45c 24.175 ± 0.072 (192), 44v
  22.409 ± 0.040 (637). No settles of any kind in these runs (kind 3 active); no replica censored before the end
  except by the end of the run; no repeated death ages.
- **Forecasts:** 43c forecast was 21.8 ± 0.2 (the lead's 21.6–22.0): hit. 44v 22.3 ± 0.4: hit. 45c 24.0 ± 0.4
  (lead) / 24.2 ± 0.4 (author's lean): hit. The forecasts are wide (±0.2–0.4 nats), so these hits test little.
- **Cross-check with independent CPU data** (`research/fluct/data/sym_residence.csv`, orbit stepper; and the
  engine-only soup lineages, `lineage_check.py`): only the vertex-centred sizes overlap, through the same GPU
  pipeline: 36v GPU 2.247e6 vs CPU 2.235e6 ± 2.1% (2,177 deaths) and engine lineages 2.485e6 ± 5.8% (300) — 1.75σ;
  38v 1.254e7 vs 1.174e7 ± 6% (279) — 1.1σ; 40v see claim 4. The single CPU death at 43c (ln 22.6 ± 1.0) is
  uninformative. No CPU data at 44v or 45c.
- **Age dependence (new):** cube-centred 43c: Weibull shape k = 0.94 (0.915–0.969), LR test p = 0.04; deaths in
  the last quarter of the age range 188 vs 222 expected. 45c: k = 0.84 (0.78–0.90), p = 0.01. Vertex 44v: k = 0.97,
  p = 0.5; all asymmetric runs and vertex 36/38: flat. Two cube-centred runs, both falling, is suggestive, not
  conclusive (post hoc, 12 runs tested). Either the fresh cube-centred soups die faster when young (then the long-run
  mean residence is *larger* than quoted, e.g. side 17's 3.2 × 10¹⁰ is low), or some replicas get stuck in debris
  the period-128 test misses (then the quoted τ is slightly *high*). It is in the direction of OPEN-PROBLEMS 6
  (cube plateaus over-dispersed), which the PR says soup lineages do not show — but it tested only vertex-centred
  lineages. Worth a dedicated run; not a merge blocker if the README says so.

Not checked: anything at 44v/45c against a second implementation (none exists); the kernel at these sizes on a GPU.

## Claim 4: O_h vertex lineages R = 36, 38, 40 memoryless; tau(40) 21% above the file

**Verdict: memorylessness confirmed from the data; τ(40v) = 8.63 × 10⁷ is right for fresh soups, and the 7.1 × 10⁷
"on file" is not a soup value — it pools 46 soup deaths with 96 deaths of copies of the side-16 cube's own states.
The "aftershock" is real but misdescribed: it is near-simultaneous double peels within ~20 generations, not a
fragile layer over 0.01τ.**

Ran `lineage_r40.py` and `postpeel_check.py` (earlier reviewer's; read, both use their own unpacking), and
`research/experiments/cube_vs_ensemble.py`.

- 40v from raw lives (own code): τ = 8.63e7 (45,785 deaths); complete lives with a 5τ window: 27,294, CV 0.966
  (exponential 0.972), P(> 4τ) 0.0169 (0.0183), P(< 0.05τ) 0.0480 (0.0488); hazard × τ by age flat from 0.001τ to
  10τ within Poisson error (first 0.001τ: 35 deaths vs 50 expected, young soups slightly *safer*). Settled lives
  (33) carry 0.08% of the exposure; excluding them changes τ by 0.1%. The PR's numbers reproduce. The 10τ-window
  statistics in the committed JSON for 40v are empty (`complete_lives: 0`); the 5τ numbers in PREDICTIONS.md come
  from an analysis step not committed in the PR (`lineage_r40.py` here reproduces it).
- 36v, 38v: the JSON lineage blocks (computed on the GPU host from all lives) give CV 0.998 / 1.002, KS 0.0045 /
  0.0020 (5% critical 0.0054 / 0.0052), hazard flat to 10τ. Cannot be recomputed here (no raw lives stored).
- **τ(40v) against the file:** `sym_residence.csv` at A = 630 v has sym40v (fresh soups) 8.18e7 ± 15% (46 deaths)
  — agrees with the GPU (0.4σ) — and two rows of copies of the side-16 cube (`snap_cube16_gen2525000000`, 31
  deaths, 8.2e7; `snap_cube16_gen2875000000`, 65 deaths, 5.73e7). `cube_vs_ensemble.py` pools all three:
  142 deaths, 7.06e7. The GPU soup value is 2.4σ above the pool and 3.3σ above the 2875M copies. So the "21%" is
  not a discrepancy between two soup measurements; it is copies vs soups — itself evidence that the cube's states
  are not typical soup states (the PR's own conjecture).
- **Consequence for `cube_vs_ensemble.py`:** with the GPU soup τ at 513v, 570v, 630v, side 16's R = 40 plateau is
  T/τ = 6.07 (P = 0.0023) instead of 7.41 (P = 0.0006); the 16-plateau sum is 25.6 instead of 27.2 (P = 0.016
  instead of 0.008); three plateaus beyond 4τ either way (P = 0.003). OPEN-PROBLEMS 6 survives, a little weaker.
  Pooling cube copies into the reference τ, as that script does, is the wrong reference for testing the cube.
- **Post-peel waits:** mean / stationary τ = 0.989 ± 0.010 (38→36) and 0.998 ± 0.010 (40→38): reproduced. The
  excess early deaths are almost all in the first 10⁻⁵τ (≈ 20 generations): 37 and 27 deaths where ≈ 0.1 are
  expected, many at a wait of 1–2 generations; from 10⁻⁴τ on the hazard is stationary (e.g. [10⁻³, 10⁻²)τ: 87 vs 82,
  84 vs 82). That is the next layer dying together with the old one (double peels, ≈ 0.3–0.4% of peels), not a
  layer that "starts slightly fragile". README and PREDICTIONS should say so.
- Stage A collects the first 9,216 peels in time, so lineages with long first plateaus are under-represented; if
  consecutive plateaus were correlated this would bias the post-peel mean low. Moot given the result, but it should
  be stated.

## Claim 4: O_h vertex lineages R = 36, 38, 40 memoryless; tau(40) 21% above the file

## Claim 1: kernels bit-exact against the engine; settle detection

**Verdict: the production kernel's logic is confirmed on the CPU (bit-exact against `fl.c` and the engine, events
and settling exact, including R = 15 in the exact shape of the committed A = 108 run); the GPU runs themselves
are not checkable here. The claimed negative controls are not in the committed code (I supplied three of my own,
all caught).**

Code read against `docs/AUTOMATON.md`:
- `rule12` is a carry-save adder over the 12 neighbours giving a 4-bit count; `~b3 & ((b2 & ~b1) | (me & ~b2 & b1 &
  b0))` is alive iff count ∈ {4, 5} or (alive and count = 3): B45/S345. Correct for counts 0–12.
- Outside the vessel is a sentinel row that is never written (zero forever; exact by T2). Neighbour indices are
  16-bit (asserted n < 65535).
- Face reductions: each face's entry list is padded with the sentinel to a multiple of 32 and T is a multiple of
  32, so every warp's 32 entries in a slot belong to one face and lane 0's face index is the right one (a mixed warp
  would credit one face's cells to another and *miss* deaths, i.e. inflate lifetimes; it cannot happen with this
  layout). Rotating reduction buffers (t mod 3) are zeroed and read in different phases; no race found.
- Kind 2 compares the new state with the state two generations back (carried across launches in GB); after a
  reseed both buffers hold the soup, so the first-generation test is "period 1", never a false period 2. Kind 3
  compares with the launch-start state for the first 128 generations of each launch; a match means a true cycle (the
  dynamics are deterministic), so kind 3 has no false positives, and catches every period ≤ 128 within one launch of
  entering the cycle.
- Events are recorded at generation t − 1 at the start of iteration t, and the freeze takes effect from generation
  t: same as kernel A (event and freeze in the same iteration). Frozen replicas are zeroed (or kept, `K_KEEP`).

Ran (one core): `taskset -c 3 python3 research/audit/gpu_pr8/shared_cpu_check.py PR8 --prod15`. This compiles the
PR's `kernel_shared.cuh` unchanged except the `extern __shared__` declaration, with `shared_shim_uc.cpp` (new:
user-level threads, a block's threads run round-robin between barriers; warp shuffles through a buffer between two
barriers; the shim aborts if threads of a block ever disagree on the number of barriers passed). The earlier
reviewer's pthread shim (`shared_shim.cpp`) is the same design but too slow on one core; superseded. Host layout
from the PR's own `gsim.shared_layout`. Results:

- stepping, every replica's full state equal to `fl.c`'s after launches of 1, 7, 250, 1000, 1, 250 generations:
  R = 7 (production J, T = 160), R = 9 (J = 8, T = 64, 2 blocks), R = 7 (WB = 1), and **R = 15 in the exact shape
  of the committed A = 108 run (n = 2,064, J = 6, T = 352, WB = 2)** — all equal;
- face-death generation of every replica equal to `fl.c`'s, launches of 100 and 1,000: R = 7 (64 deaths), R = 9
  (93), R = 15 (no deaths within 3,000 generations, so at R = 15 only stepping is really tested);
- settling: 60 R = 7 soups that the engine runs into cycles of period 1–5: kind 2 at cycle start + 2 and kind 3 at
  (first launch start ≥ cycle start) + period, all 60 exact;
- engine: asymmetric R = 11 soup and O_h vertex R = 24 soup, 4 lanes each, state after 3,000 generations equal to
  `gump run`'s;
- `ALL OK`, exit 0. The same with the block's threads scheduled in reverse order (`ORDER=rev`, all but the R = 15
  case): `ALL OK` — no dependence on thread order between barriers was found.

Negative controls (mine): `MUTANT=neighbour|lastface|period2 python3 research/audit/gpu_pr8/shared_cpu_check.py PR8`
builds a kernel broken in one token — one neighbour read twice (wrong rule); the last face never checked (missed
deaths, the failure that would inflate lifetimes); "two back" replaced by "now" (false settles). All three are
caught (stepping, face-death and settle checks fail respectively).

On the PR's own validation: the every-generation engine comparison (`check_engine_every`) hashes the full live-cell
set of five lanes every generation for 2,000–3,000 generations (64-bit order-independent sum of a mixing hash; a
wrong state passes with probability ~2⁻⁶⁴ per comparison) against `gump run --trace`; the expected hashes are not
committed but are regenerated from the engine by a committed command, which is better. It runs with freezing
off, so events are validated only against `fl.c` (R = 7, 9, 13 and the R = 15 reseed check) — adequate, since
`fl.c` is itself engine-validated. The **negative controls the README describes are not in `check.py` or
`modal_app.py`**; they must be committed or the sentence removed. The 373-soup settle validation
(`check_periodic`) reads a file built outside the PR (`research/scratch/...`); its builder is not committed.

Not checked: anything executed on a GPU (warp-synchronous behaviour, NVRTC compilation, real shared-memory
races that a sequential emulation cannot exhibit, e.g. a missing `__syncthreads` that happens to be harmless in
round-robin order). I found no such missing barrier by reading; the emulation runs threads in a fixed order, so it
would not reveal one.

## Claim 5: qsd.py's settle flaw matters at R = 36

**Verdict: wrong as stated about `qsd.py`; right about a detector that only sees periods 1–2. No number recorded in
this repo is shown to be biased by it, and the bias at R = 36 is bounded well below the quoted errors.**

Read `research/fluct/fl.c` (`fl_run`, used by `qsd.py` for soup ensembles) and the GPU data.

- The PR's evidence is a 90-second GPU run *before kind 3 existed*, i.e. with a settle test for periods 1–2 only
  (hazard 0.61 ± 0.05 per τ at 6–10τ, CV 1.012). That run is not committed. It shows that a period-≤2 test is not
  enough at R = 36; it says nothing about `qsd.py`, whose `fl_run` reseeds replicas that repeat with period 1–2
  every generation **and with any period dividing 840 (1–8, 10, 12, 14, 15, …) at every multiple of 840
  generations** (present since `c77cd7f`, the first QSD commit, so in every soup row of `sym_residence.csv`).
  `qsd.py` misses only periods that do not divide 840 (9, 11, 13, 16, …). The cube-copy ("snap") rows run with
  `reseed_p = 0`, i.e. with no settle test at all; that does not affect any soup value.
- Size of the effect at R = 36 (GPU, kind 3 active): 286 settles in ≈ 100,000 lives after T0, of which 35 (0.035%)
  have period 3–128. A replica stuck with its face alive adds at most the rest of the run to the exposure, so the
  relative bias in τ is ≲ (stuck fraction per life) × (run length / τ): ≲ 0.035% × 30 ≈ 1% even if every period-3+
  cycle were missed. The recorded orbit-stepper value agrees with the GPU's: 36v 2.235 × 10⁶ ± 2.1% vs
  2.247 × 10⁶ ± 0.3%; 38v 1.174 × 10⁷ ± 6% vs 1.254 × 10⁷ (the CPU value is *lower*, the opposite of inflation).
- So: the R = 24–30 problem noted in the notebook (debris of periods `qsd.py` misses) is real there; at R = 36 the
  recorded numbers are not measurably biased. The GPU kernel itself needs kind 3 at R = 36, which the PR added.
  The README sentence should say "a period-1/2 test is not enough at R = 36", not that `qsd.py`'s flaw applies there.

Not checked: which periods the 35 kind-3 settles at R = 36 had (the JSON does not record periods).

## General code review

- **Files outside `research/gpu/` and `research/data/gpu_facelaw/`:** none in the net diff. `research/NOTEBOOK.md`
  was edited in `258978d` and reverted in `fa1e067`; net zero. (Squash or leave; harmless.)
- **Secrets:** none found (searched the full patch history of the branch for token/key/secret patterns and Modal
  token variables).
- **Checks that exit 0 on failure:** `research/gpu/check.py` (prints `FAILURES`, exits 0) and every Modal
  entrypoint in `modal_app.py` (`check`, `check_every`, `check_periodic`, `check_keep`, `check_defaults`: print
  only). A caller or `check.sh` cannot detect a failure from the exit status. Fix: `sys.exit(1)` / raise.
- **Results that depend on uncommitted state:** (a) the engine reference cases
  (`research/scratch/gpu/engine_cases.npz`) are regenerated from the engine by a committed command — fine;
  (b) the **negative controls** claimed in the README ("expected hashes shifted by one generation; one orbit flipped
  at the start fail as they should") are **not in the committed code** — no function in `check.py` or
  `modal_app.py` does either; (c) the 5τ-window lineage numbers for R = 40 in PREDICTIONS.md come from an analysis
  not in the PR (reproduced here by `lineage_r40.py`); (d) the 90-second R = 36 run behind claim 5 is not committed;
  (e) the R = 17 seed-1/2 containers are discarded and not committed (fine, but say the choice of s3 was made before
  looking at its result, if it was); (f) throughput rows are in `research/scratch/gpu/` (ignored) — the table is not
  reproducible from the repo without re-running on Modal.
- **Duplicate guard** in `facelaw.py summary` keyed by seed: silent on a repeated seed (claim 6).
- `facelaw.py`'s `SLAB_LAW` comment cites `research/STATUS.md` for e^(−0.09 + 0.209A); the asymmetric octahedral
  comparisons in the README use 0.2077A + 0.55 instead. Two different "the repo's law" lines are in play; the
  README should name which one each comparison uses and why.

## Fixes required before merge / things to note
