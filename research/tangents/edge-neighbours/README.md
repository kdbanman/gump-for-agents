# A tangent: the rule the owner meant to write

**This is not gump.** Gump, everywhere else in this repository, is the rule as coded and run in 2012: B45/S345
where a face's four coplanar neighbours are the ones that touch it at a corner. The owner intended the four that
share an edge with it, and said so on 2026-11-14 (`research/NOTEBOOK.md`, that date; `LEAD.md`, "Which rule is
gump"). This directory is a quick look at that intended rule, at the owner's request. It lives on the branch
`claude/edge-neighbour-tangent` only, so that nobody later mistakes its numbers for gump's. Do not merge it.

Everything below is from `edge.py` (numpy; run from the repository root) on 2026-11-14. Quick tests, by the lead,
not audited and not re-run by anyone else.

    python3 research/tangents/edge-neighbours/edge.py check      # seconds
    python3 research/tangents/edge-neighbours/edge.py torus      # about a minute
    python3 research/tangents/edge-neighbours/edge.py confine    # seconds
    python3 research/tangents/edge-neighbours/edge.py boxes      # several minutes
    python3 research/tangents/edge-neighbours/edge.py trace 5 2  # one run in a box of 5 x 5 x 5 cubes

**The stepper is trusted because** with the corner neighbours it reproduces the golden side-8 log at every
generation, and with either neighbourhood it agrees with `reference/oracle.py`'s `step` (given the same offsets)
on a random torus state for 60 generations.

## What the intended rule does

- **Neighbourhood.** All twelve faces that share an edge with a face: 8 perpendicular, 4 coplanar. (Gump swaps
  the 4 coplanar edge-sharers for the 4 coplanar corner-touchers.)
- **Counted (two lines, not audited).** Along a body diagonal the twelve fall 4, 4, 4 over three layers, so
  diagonal planes leak and there is no octahedron. Across an axis plane through face centres (`x = c`, `c` odd,
  everything beyond empty) a face at `c+1` sees at most 2 + 1 = 3 and a face at `c+2` sees none. So a pattern
  never leaves its bounding **box** (closed at the next odd plane). Measured: 16 soups in a box, 400 generations,
  none left it.
- **A filled closed cube dies in one generation** (every face is overcrowded). In 2012 the cubes would simply have
  vanished: no growth, no 8-sided die.
- **It is chaotic in the bulk.** Torus of 16³ cubes, soups started at density 0.15, 0.3 and 0.5 all settle at
  density about 0.40 with about 42% of cells changing each generation and 37% overcrowded (gump, same test: 0.415,
  42%, 40%). Started at 0.7, both rules collapse to sparse debris.
- **Shut in a box, the chaos lasts longer the bigger the box, steeply.** Soups at density 0.4 in a closed box of
  k × k × k cubes; lifetime is known to within 256 generations:

  | box | cells | soups | lifetime |
  |---|---:|---:|---|
  | 2³, 3³ | 36, 108 | 64 each | under 256 |
  | 4³ | 240 | 64 | median about 500 (quartiles 450 to 770) |
  | 5³ | 450 | 48 | median 8,700 (quartiles 5,800 to 15,100) |
  | 6³ | 756 | 32 | none finished in 60,000 |
  | 7³ | 1,176 | 24 | none finished in 40,000 |

- **It dies a slab at a time.** Three runs in a 5³ box (seeds 1, 2, 3): the population sits near 193, then near
  156, then near 120, then collapses. Those are the ratios 0.8 and 0.64 of a box that has lost one layer of cubes
  and then another (5×5×4, 5×4×4). So there is a staircase here too, with the six faces of a box in place of the
  eight faces of an octahedron.

## What this does not show

No law was fitted: four box sizes, two of them only lower bounds. Whether the wait is memoryless, what the cost
per cell of a face is, whether there is a firewall theorem, what the debris looks like, and whether symmetric
seeds are fragile were not looked at. The live-box read-out in `trace` flickers at even coordinates and is only a
rough guide; the plateaus in population are the evidence for the staircase.

## So is the mistake the more interesting rule?

On this evidence, both rules are "gumps": chaos that cannot leave a vessel it can compute in advance, lasting
steeply longer in bigger vessels, dying one face at a time. What the slip changed is the picture. The intended
rule never grows: a seed stays in its own bounding box, and the cubes the owner drew would have died at once.
The coded rule grows along the axes into an octahedron three times as wide as the seed, which is what there was
to look at in 2012.
