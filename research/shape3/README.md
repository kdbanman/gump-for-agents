# The second variable: equal area, equal shortest loop, different lifetime

2026-11-14. research/shape2 found that two periodic slab faces with the same area A and the same shortest loop can
differ in ln τ_face (by 0.015 at A = 48 and 0.014 at A = 60, the one with the shorter second loop dying sooner).
This experiment asks what the second variable is: five candidate formulas, each fitted on the three known pairs
only, forecast every new equal-area, equal-loop pair (`PREDICTIONS.md`, committed in 46baf66 before any production
run; amendments f645b13, 43a5e0e, ffcaf36, also before the results they concern). Statements are marked [proved],
[measured] or [conjectured]; "post hoc" means looked for after the data.

VERDICT_PLACEHOLDER

## Why the experiment can only separate candidates by size [proved]

Reduced Gram matrix of the period lattice (Q1, 2B, Q2): Q1 = shortest loop², Q2 = second loop², 0 ≤ B ≤ Q1/2
(Q = x² + xy + y², research/shape/lattice.py). The determinant Q1·Q2 − B² = 0.75 n² (n = A/3) is fixed by the area.
So within a group of equal A and Q1 the lattice up to isometry is fixed by one number, Q2, or B, or the angle, or
the third loop Q3 = Q1 + Q2 − 2B (which falls as Q2 rises), or x = Re τ = B/Q1 of the shape modulus
τ = (B + i√D)/Q1, whose imaginary part h = √D/Q1 is fixed. Every candidate that sees only the flat torus (loop
lengths, theta series, angle, number of shortest loops) is a function of x within a group. More: at every index
n ≤ 28 (A ≤ 84) no two classes share a Gram matrix (checked by enumeration), so the class itself, and with it every
lattice-scale quantity (rows, transverse layers, firewall cuts), is a function of the Gram matrix. At these sizes
no experiment can separate "metric" from "lattice-scale" candidates; only the form of the function of x (and of A
and h) can be tested. And the equal-loop groups with Q1 ≥ 12
are few: at A ≤ 84 they occur only at A = 48, 60, 72 and 84 (none at 54, 63, 66 or 75), two pairs and one triple
at 72. Below saturation, Q1 = 9 groups exist at A = 36, 45, 54, 63, 72.

## Set-up

- **Stepper.** `ts3.c` is the review's independent stepper (`research/audit/shape/ts.c`: bit-sliced, renewal lives,
  own RNG and layer indexing) with two changes: a carry-save AVX-512 step kernel (4.4× faster; the rule is the
  same), and a stronger settled test (below). **Validation [measured]**: on all 19 tori of the plan, population ×
  copies equals the engine's on the cubic N-torus (N = index) at each of 4,000 generations, through the vector
  kernel; and ts3 built with ts.c's settled test writes event files identical to the unmodified ts.c (512 replicas,
  60,000 generations, every torus). A negative control (rule broken in the vector kernel) fails at generation 1.
  `bash research/shape3/validate3.sh` → `data/validate.log`.
- **Lives.** 512 replicas, each running successive lives from a fresh 0.4 soup; a life ends at its first event (face
  death F, transverse firewall W, both at the same check X), or is censored when it settles (S) or when its job
  ends (open). **No cap on age.** Events every 8 generations. ln τ_face = ln(2E/F) ± 1/√F; "ties as face" counts X
  as face deaths too.
- **Zombie lives (found here).** Without a cap, lives that settle into a state whose period does not divide 840
  (ts.c compares only with the state 840 generations earlier) keep adding exposure until the end of the job. In
  the first cap-free job of (1,4,12) at A = 36, 14 of 512 replicas held such a life at the end, with ages up to
  7 × 10⁶ against a mean life of 800, carrying 1.7% of the exposure. Earlier work never saw this because its caps
  (6.5 × 10⁴, 5 × 10⁵) censored them. ts3 compares the state with snapshots 840·m generations back in the same
  life, m = 1 … 128, and censors at the first match. Exact equality proves periodicity, so no chaotic life is cut.
  After the change, no torus has an open life older than about 12 mean lives (`data/runs.csv`, column `open`; the
  oldest ages were checked from the event files).
- **Plan** (`run3.py list`): seeds 31001–31062, fixed before the runs. Wall time is the only stopping rule. The
  machine was shared with other jobs and gave each of the two lanes 20–60% of a core, so the plan was cut short:
  see "What was run".

TABLES_PLACEHOLDER

## Reproduce

    bash research/shape3/validate3.sh > research/scratch/shape3/validate.log 2>&1          # ~5 min
    python3 research/shape3/predict3.py --write                                            # forecasts (before the runs)
    nohup python3 research/shape3/run3.py lane 0 0-3 > research/scratch/shape3/lane0.log 2>&1 &
    nohup python3 research/shape3/run3.py lane 1 0-3 > research/scratch/shape3/lane1.log 2>&1 &
    python3 research/shape3/analyze3.py collect     # scratch event files -> data/runs.csv, data/agebins.csv
    python3 research/shape3/analyze3.py report      # every table above, from the two CSVs (-> data/report.txt)
    python3 research/shape3/explore3.py             # post hoc invariants table (-> data/explore.txt)

`data/runs.csv` holds the raw counts per job (exposure, F, X, W, S, open, near-firewall checks);
`data/agebins.csv` exposure and face deaths per job in age bins. Event files are in `research/scratch/shape3/`
(git-ignored).

NOTCHECKED_PLACEHOLDER
