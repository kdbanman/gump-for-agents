# gump-for-agents

A rebuild and investigation of **gump**, a 3D cellular automaton Kirby Banman wrote in
Processing in 2012 ([kdbanman/gump](https://github.com/kdbanman/gump)). Its cells are not
cubes but the **faces** between cubes; each face looks at 12 neighbours (the 8 perpendicular
faces sharing an edge with it, and the 4 coplanar faces touching it at a corner) and follows
one rule: *born on 4 or 5 live neighbours, survives on 3, 4 or 5*.

This repository was built and is run mostly by AI agents: a lead (Claude) directing other
Claude agents as builders and researchers. It contains a fast engine, a web app, and a growing
body of results about what this automaton does and why.

## What we found

Each item is tagged in [`research/NOTEBOOK.md`](research/NOTEBOOK.md) as proved, measured or
conjectured, with the command that reproduces it. The short version:

1. **Nothing can be born across a `{111}` plane.** A dead cell just outside a diagonal plane
   sees at most 3 live neighbours; birth needs 4. So every finite seed is trapped forever in
   its octahedral hull — no gliders, no unbounded growth, and cubes grow into "8-sided dice".
   Three consecutive dead diagonal layers are a permanent firewall.
   ([`docs/AUTOMATON.md`](docs/AUTOMATON.md), proved.)
2. **The lattice is a stack of kagome layers**, and each layer is a closed 2D automaton.
   One or two layers cannot sustain activity; three can.
3. **Inside a hull, gump settles into a chaotic phase** of density 0.4155 — isotropic, with
   correlations shorter than one cube, in which a single flipped cell spreads as a sphere.
4. **Chaos dies from its faces, suddenly.** The long plateau and staircase collapse in the
   original's plots is the octahedron losing one whole face layer at a time. The wait for a
   face to die is memoryless, and its mean grows by about e^0.21 per cell in the face —
   every extra cell makes a face last about a quarter longer, across six decades of lifetime.
   (The first fit, `exp(−0.09 + 0.209 × cells)` on flat faces, mixes faces of different widths;
   see item 8.) The constant is the far end of the face's
   ordinary fluctuations, measured down to its last cell: each cell fewer is about two-thirds
   as likely, and the death rate is the next point on that line
   ([`research/fluct/README.md`](research/fluct/README.md)).
5. **Symmetry is fatal.** A symmetric seed has only one fundamental domain's worth of
   independent chaos, so its faces fail together. The original's side-13 cube lives 169,049
   generations *because* it is symmetric; an asymmetric soup in the same hull would be
   expected, on the face law extrapolated fivefold in area, to hold each face for ~10⁴¹. (Our first out-of-sample prediction, the lifetime
   of a side-16 cube, failed: it lived 2,919,617,676 generations, twelve times the prediction,
   and ended as twelve small still lifes on the axes. The repair is in the notebook: large
   symmetric faces are tougher than a fixed "effective area" allows. A forecast for its first
   face, made from perturbed copies of the running cube and committed two hours ahead, held;
   the same method missed the second face sevenfold, and why is open.)
6. **The debris has a small anatomy**: single cubes, kagome hexagons, the *vertex star* (the
   12 faces around one lattice vertex — a sealed universe of 4,096 states), period-2 "hinges"
   whose faces swing 90°, and rare clockwork with periods up to 66. The long periods are short
   loops that close with a twist: the period-66 object is a 33-step loop that returns as its own
   mirror image, and a period-48 "screw" turns 60° every 8 generations
   ([`research/clockwork/`](research/clockwork/README.md)).
7. **B45/S345 is a corner case in rule space.** Among 960 neighbouring rules, long-lived
   confined chaos is uncommon, and gump is a minimal member: remove any one count and it dies young.
8. **A face's lifetime depends on its shape, not only its area.** On wrap-around slabs a
   narrower face of the same area dies sooner (slabs 3×10 against 5×6 at 90 cells: 0.74 lower
   in ln τ), and on twisted slabs the lifetime rises with the face's shortest closed loop,
   though that is not the only variable. For widths 4–6 the cost per cell is between 0.2072
   and 0.2117, not yet settled; every periodic-face constant so far carries a wrap-around term.
9. **The exponent lives in a thin skin.** Keep the rule on a face's top five or six layers and
   replace everything beneath by fresh coin flips every generation: a slab face lives as long as
   on the real thing (within 0.015 in ln τ at 27–60 cells). A mirror plane through a hull face
   roughly halves the price: 0.103 per cell against about 0.22.
10. **No proof of the area law yet.** A swarm of theory agents proved exact reductions, an area
   law conditional on a measured property of the rule, and an exponential law for a
   deterministic relative of the 2D rule (resting on two published percolation results), but neither "why area" nor the constant. What is left
   is smaller: five or six layers of the rule over independent noise.

[`docs/WHAT-I-SEE.md`](docs/WHAT-I-SEE.md) is the lead's own account of what is interesting,
surprising and beautiful here. [`research/STATUS.md`](research/STATUS.md) is the current state of play.

## Try it

**Watch it** — WebGL2 compute, three.js rendering; opens on a guided tour:

```bash
cd web && npm install && npm run serve
```

then open `http://127.0.0.1:8173/web/`. See [`web/README.md`](web/README.md).

**Run it fast** — Rust, bit-sliced AVX-512, about 4×10¹⁰ cell-updates per second per core;
the original's 169,049-generation run takes about a second:

```bash
cd engine && cargo build --release
```

```bash
engine/target/release/gump run --cube 13 --events deaths.jsonl --kymo kymo.csv
```

```bash
engine/target/release/gump show --cube 13 --gens 100000 --layer 33
```

See [`engine/README.md`](engine/README.md) for ensembles, snapshots, text and PNG renderings.

**Check it** — a ~100-line numpy oracle that reproduces the original's population logs:

```bash
python3 reference/oracle.py legacy-cube 60 --compare reference/golden/legacy_cube_side11_H60.txt
```

## Layout

| path | what |
|---|---|
| `docs/AUTOMATON.md` | the exact rule, coordinates, theorems with proofs, legacy semantics |
| `reference/` | numpy oracle, golden logs from the original, brute-force theorem checks |
| `engine/` | Rust engine and the `gump` CLI |
| `web/` | browser app: GPU stepper, views, instruments, seed editor, atlas gallery, tour |
| `research/` | notebook, status, studies (`atlas/`, `peeling/`, `phase/`), figures |

## How trust is established here

The oracle was written directly from the original source and matches its logs generation
for generation. The engine must match the oracle state for state, and the original's six
logs exactly. The web app's GPU path must match the same logs and a separate CPU stepper.
Research claims are re-derived by a second tool or a second agent where possible, and the
notebook records corrections rather than erasing them.
