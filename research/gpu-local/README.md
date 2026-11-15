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
  (2^21 gens, 979,357 lives; also with pw = 32), R = 11 (pw = 16, K = 997, FIRST = 1000). No natural kind-5 life
  occurred in these runs (pw ≥ 16 already catches what R = 9-11 soups settle into before a face dies).

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

**[conjecture]** For the measurements queued (τ ≈ 10^8-10^10 generations, launches of 10^5-10^6 generations on this
card), both delays are small against a mean life except the snapshot delay of lives that settle very old. If kind-5
lives turn up in numbers, exact entry ages can be recovered offline: every life is a deterministic function of
(seed, reseed round, replica), so it can be re-run from its birth.
