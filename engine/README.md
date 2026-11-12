# gump engine

Rust library + `gump` CLI for the gump automaton (faces of the cubic honeycomb, rule
B45/S345; see `docs/AUTOMATON.md`). Built for agents: every command prints machine-readable
JSON (JSONL time series, one JSON summary line at the end of every run). No dependencies.

## Build

```sh
cd engine
cargo build --release          # binary: engine/target/release/gump
cargo test --release           # fast-vs-scalar, properties (T2, T3, halting, snapshots)
```

`engine/.cargo/config.toml` builds with `-C target-cpu=native` and asks LLVM for 512-bit
vectors (the "unknown feature `prefer-256-bit`" warning is expected). Run cargo from
`engine/` so that config applies; without it the kernel still works but is ~3× slower.

## CLI examples

```sh
G=engine/target/release/gump
$G help                                            # all options
$G run --cube 13                                   # side-13 closed cube, open space, until halt
$G run --legacy-cube 70 --poplog pop.txt           # the original's side-13 run, legacy log format
$G run --cube 11 --every 10 --out ts.jsonl \
       --kymo kymo.csv --events deaths.jsonl       # time series + kymograph + layer deaths
$G run --soup 0.3 --radius 20 --rng 7 --gens 100000 --every 1000 --format csv --out ts.csv
$G run --soup 0.3 --torus 128 --gens 1000 --threads 4   # whole-torus soup
$G run --soup 0.5 --torus 32 --slab-layers 3 --diag 1   # 3-layer {111} slab on a torus
$G run --cells pattern.txt --rule B4/S345 --torus 20,20,40
$G run --snapshot state.gump --gens 500 --snapshot-out later.gump
$G info --legacy-key 9                             # seed/box/hull, no stepping
$G ensemble --soup 0.3 --radius 10 --runs 100 --vary density=0.2,0.3,0.4 > runs.jsonl
$G bench                                           # performance suite
```

Coordinates are always **doubled** (`docs/AUTOMATON.md` §1): a cell is a point with exactly
one odd coordinate. Diagonal axes are `0:[111] 1:[-1,1,1] 2:[1,-1,1] 3:[1,1,-1]`; the layer
coordinate along axis `d` is `s = d·p` (odd).

**Space.** Default is open (infinite) space: the box is sized to the seed's diagonal hull
plus one cube of margin, which is exact forever by T2 (tested against a padded box). The
kernel additionally skips rows that miss the hull (tightened whenever a sample sees the
hull shrink). `--torus N|NX,NY,NZ` is a proper torus of that many cubes (doubled period
2N); on a torus, layers are taken mod `2·gcd(NX,NY,NZ)`. `--box` gives an explicit
dead-outside box. The legacy odd-H seam is not reproduced (the numpy oracle does it).

**Rules.** `--rule B45/S345` (default), any birth/survival sets over 0..12 (`B4,10/S3,11`
for counts ≥ 10). B45/S345 has a hand-specialised kernel; others use a generic
multiplexer kernel (about 2× slower: 1.3–1.4 × 10¹⁰ vs 2.6 × 10¹⁰ cell-updates/s on a 64³ torus, same run). Hull restriction / T2 claims apply only when min birth ≥ 4.

### Outputs

| option | content |
|---|---|
| (stdout, last line) | `{"type":"summary", status: extinct/still/periodic/running, period, cycle_start, detected_gen, gen, pop, pop_axis, seed_pop, peak_pop, peak_gen, hull_initial, hull_final, firewalls_final, layer_events, theorem_violations, hash, rule, seed, boundary, dims, origin, packing, threads, elapsed_s, gens_per_s, cell_updates_per_s}` |
| `--every K [--out F] [--format jsonl\|csv]` | sample every K gens: gen, hash, pop, pop_axis, changed (cells changed by the last step), bbox, hull (4 × [lo,hi] layer ranges; open space), firewalls (per axis, runs of ≥3 dead layers strictly inside the hull / anywhere on a torus ring), `--layers`: full per-layer populations. `--lite` skips the layer pass. |
| `--kymo F` | CSV kymograph: header `gen,axis,<s values>`; one row per (sample, axis) with the population of every layer of the initial hull |
| `--events F` | JSONL `layer_death` records: `{gen, axis, dir, s, last_alive, cause}` — the sample at which a layer became *provably* dead forever (`hull`: outside the hull, T2; `firewall`: inside ≥3 dead layers, T3), and the last sampled generation it had a live cell. Resolution = `--every` (default 1 when `--events`/`--kymo` is given). Proven-dead layers coming back alive would be counted in `theorem_violations` (never seen). |
| `--poplog F` | `generation population` every generation (the original's log format, line 0 = seed) |
| `--trace F` | every generation, all live cells (small patterns / cross-checks only) |
| `--snapshot-out F`, `--cells-out F` | final state |

**Halting.** Every generation the kernel also accumulates a 64-bit position-dependent state
hash, the population per orientation, and a changed flag (≈15% of kernel time). Still life
= no cell changed; extinction = population 0; a cycle = first repeat of a hash within the
window (`--hash-window`, default 2²⁰ gens; 2¹⁶ in ensembles), which gives the period and
the exact generation the cycle was entered (all earlier states are distinct). Every hash
cycle is verified exactly by stepping a copy `period` generations and comparing states.
Tested against brute-force cycle finding on small tori.

**Ensembles.** `gump ensemble` runs independent runs over all cores (one run per thread),
RNG seeds `rng, rng+1, …`, optional parameter grid (`--vary density=…`, `radius`, `half`,
`rule`, `slab-layers`); one summary line per run (with `run`, `rng`, `params`) plus a final
`ensemble_summary` (runs/s). Default cap 10⁶ gens per run.

**Soups.** `--soup P` with `--radius R` (octahedron Σ|p−c| ≤ R), `--half H|HX,HY,HZ` (box),
`--slab-layers M [--diag D]` (M consecutive {111} layers; bounded by `--half` in open space,
wrapping on a torus), or the whole torus. `--center`, `--rng`. Each cell of the region, in
order z, y, x (doubled coordinates), draws one xoshiro256** value: a soup is a function of
(region, P, rng) only, independent of the box it is placed in.

## Snapshot format (`.gump`, version 1)

Text header, a blank line, then the payload:

```
GUMP-SNAPSHOT 1
boundary open            (or torus)
dims 40 40 40            box size in cubes NX NY NZ
origin -20 -20 -20       local cube (i,j,k) is absolute cube (i+OX, j+OY, k+OZ)
rule B45/S345
gen 169050
population 108
encoding rle0
bytes 205
                          <- empty line
<205 payload bytes>
```

Local cell `(a,i,j,k)` (face on the +a side of cube (i,j,k)) has doubled coordinates
`2(i+OX, j+OY, k+OZ) + e_a`. The state is the bitmap with bit `t = ((a·NZ + k)·NY + j)·NX + i`,
LSB-first in `ceil(3·NX·NY·NZ/8)` bytes. `rle0` encodes those bytes as repeated records
`varint(zero-byte run) varint(literal length) literal…` (LEB128) until the full length is
reached (`encoding raw` = the bitmap itself is also accepted). Readers ignore unknown keys.
The final side-13 ash: 205 payload bytes. Cell lists (`--cells`, `--cells-out`) are text:
`x y z` per line, `#` comments.

## Engine design

Cube-index bit-volumes X, Y, Z (`docs/AUTOMATON.md` §1–2). Along x, cube `i = b·W + w`
lives in bit `b` of word-plane `w` (`W` words per row, `B = NX/W ≤ 64` bits used): then
`i±1` is the same word in the neighbouring word-plane, `j±1`/`k±1` are word offsets, and
only the seam between plane W−1 and plane 0 needs a one-bit shift (5 seam planes are
precomputed per generation; a rotate on a torus). The kernel is a flat loop over words
with fixed offsets: 31 loads → three carry-save adder trees (8 full + 2 half adders each,
12 inputs → 4 count bits) → rule as a boolean function → 3 stores, written on `[u64; 8]`
blocks so LLVM emits AVX-512 (`vpternlogq`). Halos (one word in j and k) are copied on a
torus and stay zero in open space. Multi-threading splits rows across a persistent team
synchronised by a spin-then-block barrier (`--threads`, auto for boxes over ~1.5M cells).
`src/scalar.rs` is the plain doubled-coordinate stepper used as the reference in tests.

Files: `src/fast.rs` (kernel), `src/scalar.rs`, `src/lattice.rs` (coordinates, hull),
`src/instruments.rs` (samples, layers, firewalls, layer tracker, halting),
`src/run.rs` (driver + outputs), `src/seeds.rs`, `src/snapshot.rs`, `src/main.rs` (CLI).

## Validation status

| check | command | result |
|---|---|---|
| golden logs, sides 8–11, every generation, open space and (even H) legacy torus | `python3 engine/scripts/check_golden.py` | 7/7 exact |
| original's side-12 (24,286 gens) and side-13 (169,049 gens) logs | `python3 engine/scripts/check_golden.py $L/population24.txt 65 $L/population26.txt 70` (`L=/home/user/kdbanman/gump/dev/cubic_init_results`) | exact at every generation, open space (and torus 35 for side 13); halt detected at exactly the log's last generation |
| state-for-state vs `reference/oracle.py`: random soups, 5 rules, tori 4–12 and open octahedra | `python3 engine/scripts/check_oracle.py --cases 15 --gens 40` | all exact |
| fast vs scalar: torus/open, box shapes incl. 1×1×1, 63/64/65/67/96/128/130/140-wide (word seams, prime widths), 5 rules, threaded | `cargo test --release --test fast_vs_scalar` | pass |
| T2 (hull never grows; auto box = padded box; hull-restricted kernel), T3 (3 dead layers stay dead on tori, 4 axes), layer tracker never sees a proven-dead layer revive, snapshot round trip, halting vs brute force | `cargo test --release --test properties` | pass |

## Performance

Measured on the 4-vCPU Xeon (Granite Rapids, AVX-512) **while other agents kept 2–3 of the
4 cores busy** (load average 4–9; four independent copies of one single-threaded benchmark
together ran only 1.2–2× faster than one copy). Single-thread numbers are reproducible to
~±20%; multi-thread numbers reflect the contention. Cell-updates = 3 × cubes in the box ×
generations. `gump bench` reproduces the table (`--threads 1,2,4`).

| workload | threads | gens/s | cell-updates/s |
|---|---:|---:|---:|
| side-13 closed cube in its 40³ hull box, full kernel | 1 | 1.2–1.3 × 10⁵ | 2.3–2.4 × 10¹⁰ |
| same, kernel restricted to rows meeting the hull (default in `run`) | 1 | 2.2–2.4 × 10⁵ | 4.3–4.5 × 10¹⁰ box-equivalent |
| the whole legacy side-13 run, 169,049 gens, with per-generation halting detection | 1 | 0.84 s total (2.0 × 10⁵) | |
| soup p=0.3, 64³ torus | 1 | 5.0–5.2 × 10⁴ | 3.9–4.1 × 10¹⁰ |
| soup p=0.3, 128³ torus | 1 / 2 | 7.0 × 10³ / 1.1 × 10⁴ | 4.4 / 7.0 × 10¹⁰ |
| soup p=0.3, 256³ torus | 1 / 2 | 850 / 1,320 | 4.3 / 6.7 × 10¹⁰ |
| 64³ torus without in-kernel hash/population (library, `kernel_stats = false`) | 1 | 5.8–6.4 × 10⁴ | 4.6–5.1 × 10¹⁰ |
| non-default rule (multiplexer kernel), 64³ torus | 1 | 2.4–2.9 × 10⁴ | 1.9–2.3 × 10¹⁰ |
| ensemble: octahedral soups R=20, p=0.3 (box 22³; B=22 of 64 bits used), 20,000-gen cap | 1 / 4 | 6.4 × 10⁵ / 1.2 × 10⁶ aggregate | 32 / 59 runs/s |

Octahedral soups of radius 20 do not halt within 3 × 10⁶ generations, hence the cap.
With 4 threads per generation the busy machine made things slower than 2; on an idle machine
expect near-linear scaling for ≥128³ (the team claims row chunks dynamically, no serial
phase). The default is 1 thread per run; ensembles use one run per core.

**Profile (from the hot loop's instruction mix; no `perf` here).** Per block of 8 words
(512 cells × 3 orientations): 31 unaligned 512-bit loads, 3 stores, 57 `vpternlogq` + 12
other logic ops (three 12-input carry-save trees at 2 ternary ops per full adder, rule in
3 ops), ~24 register copies (ternlog overwrites an input), and ~30 ops of per-generation
reductions (hash: one `vpmullq` per word; popcounts; changed flag). The kernel is bound by
the two 512-bit ALU ports, not by memory, even at 256³ (12.6 MB per generation). Letting
LLVM lower the same boolean expressions produced ~2× the ops; the hand-written ternary-logic
path gave ~1.3×.

**Next steps, by expected gain.** (1) Ensembles of small boxes: pack 2–3 runs side by side
in each 64-bit word (R=20 boxes use 22 of 64 bits) — ~2.5× runs/s. (2) Share partial sums
across orientations and neighbouring words (`X[i]+X[i−1]` feeds both Y and Z,
`Y[j]+Y[j−1]` feeds X and Z) — maybe −20% ops. (3) Hash every K generations and recover the
exact cycle start by re-simulation from a checkpoint — removes most of the 20–25% stats
cost. (4) Temporal blocking (several generations per pass over a tile) for tori beyond L2;
the halo is already per-chunk. (5) O_h-reduced stepper for symmetric seeds (48×).
