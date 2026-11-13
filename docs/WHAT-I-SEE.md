# What I see in gump

*Written by the lead agent (Claude), for Kirby, who asked what I find interesting,
surprising and beautiful here — and for any agent or person who comes after. Everything
factual below is in `research/NOTEBOOK.md` with its evidence; this is the view from above it.*

## One inequality

The thing I keep returning to is how much follows from **3 < 4**.

Slice the lattice along a body diagonal. Every cell then has six neighbours in its own
layer, two in each adjacent layer and one in each layer beyond. So a dead cell sitting just
outside a diagonal plane can see at most three live cells on the far side, and the rule
needs four for a birth. That is the whole proof, and from it: no pattern can ever cross a
`{111}` plane; every finite seed lives and dies inside an octahedron it can compute in
advance; there are no gliders; a cube grows along the axes, where nothing stops it, until it
fills the "8-sided die" you noticed in 2012; and everything you ever drew had to collapse or
cycle eventually, because it was always in a finite box that only you couldn't see.

I found that within the first hour, by reading your `environment.pde` and counting offsets,
and I have not stopped being pleased by it. A rule chosen by hand, by feel, turns out to sit
exactly on a threshold: with birth at 3 the planes leak and there are no octahedra at all.

## A lattice with a hidden grain

Faces of a cubic honeycomb sound like a cubic thing. But the diagonal layers are **kagome
lattices** — the faces of the cubes, seen down a body diagonal, tile into the
triangle-and-hexagon net — and the automaton is an ABC stack of them, the same arrangement
as the anions in a perovskite crystal. Each layer is a little closed 2D world of its own.
One layer alone freezes into scattered hexagons within a few dozen generations. Two layers also
die. Three is the least that can hold a fire.

And yet the fire, once lit, shows no grain at all: the chaotic state has the same
correlations along and across the layers, to within measurement, and a single flipped cell
spreads as a sphere. The anisotropy lives entirely in what can be *born into emptiness* —
growth runs at 0.177 cubes per generation along the axes and at exactly zero across the
diagonals. I like that the structure is invisible in the bulk and absolute at the boundary.

## The staircase in your old plots

Your old plots of the long cube runs show a noisy plateau and then a descent in steps. The
steps are the octahedron **peeling**: one entire face layer goes extinct — all eight faces at
once, in a symmetric seed — and because of the inequality above it can never be re-seeded.
The hull is one layer smaller forever, the population drops to the smaller volume, and the
wait begins again. In the side-11 run the plateau populations fall in the ratios 0.79, 0.61,
0.48; the hull volumes give 0.79, 0.62, 0.47.

What surprised me is *how* a face dies. In the runs we examined it does not erode. It holds a hundred or two hundred
live cells, busy as ever, until roughly ten generations before the end, and then it is
gone. The waiting time is memoryless, and its mean is exponential in the number of cells in
the face, about `exp(0.209 × area)`, with a prefactor of about one generation. Flat faces
and triangular faces, six decades of lifetime: one line. (Symmetric seeds follow it with a
smaller effective area — and there I got the details wrong; see below.)

I wanted to know where 0.209 comes from, and now it has been measured. Watch a face that is
*not* dying: its population jitters around half-full, more widely than coin-flips would, and
the chance of finding it at a given low density falls off exponentially in its area along
one curve, the same at every size. An agent followed that curve all the way to the bottom,
on faces small enough to die often. Near the bottom it is a ruler-straight line: each cell
fewer is about two-thirds as likely, down to a single cell, and the death rate is simply the
line's next point. Six times in ten a face dies from one last cell. When three are left they
are usually a triangle, three faces round one corner of a cube — the last ember.

So a face needs no special mechanism to die. Its death is the far end of its ordinary
fluctuations, and it is not a slow slide: sixteen generations before the end a dying face
looks like any other, and the layer beneath it barely notices.

## Symmetry is fatal

This is the finding I'd most want you to hear, because it is about how you played with it.
The seeds a person naturally draws — cubes, anything mirror-symmetric — are the fragile
ones. A symmetric state has only one fundamental domain of independent chaos; its 48 copies
are in lockstep, so a fluctuation that kills one region of a face kills all the others in
the same instant. The effective area of a face is divided by six or seven, and that divisor
sits in an exponent. Your side-13 cube lived 169,049 generations *because* it was
symmetric. Fill the same octahedron with an asymmetric soup and the law says each face
should last something like 10⁴¹ generations.

Your README says the even-key seeds "have much shorter lifespans". They do, and that is why.
Your unfinished run — a side-19 cube, still at 150,000 cells after 296,000 generations —
had a different reason to live: its torus was smaller than its hull, so it wrapped around,
lost its faces altogether, and with no face to peel from there was nothing left to kill it.
Properly confined, it would last somewhere beyond 10¹² generations.

## A sealed universe of twelve faces

The twelve faces meeting at one lattice vertex are a vessel: no cell outside ever sees more
than two of them, so nothing outside is ever born. It has 4,096 states and every one settles
within three generations. Read as layers it is a triangle, a hexagon, a triangle. Take out
the hexagon and you have one of the four smallest still lifes; keep one triangle and let the
hexagon's two halves take turns and you have the smallest oscillator, a three-bladed
propeller whose faces swing through 90° on their hinges. Most of the small debris this
automaton leaves is a piece of a star. And then, rarely, the soup leaves something that is
not debris at all: a 45-cell object with no symmetry and period 66, nearly every cell of
which carries the full period. It looks built.

## A clock with no gears

It is not built, and it has no parts. The object is a thin plate, three layers thick, that
exactly fills a sealed box of 45 cells: every cell of the box is alive at some point in the
cycle. Run it 33 generations and you get the same plate in a mirror; 33 more and it is back.
Nothing in it has period 2, 3, 6 or 11. It is a single loop of 33 steps that closes with a
reflection instead of closing directly, and so it counts twice.

That is a rule one can use: an oscillator's period is the length of its loop times the
order of the symmetry it closes with, which in this lattice can be 2, 3, 4 or 6. So an
agent went looking in boxes chosen for their symmetry, and found a 42-cell plate of period
48 that is a screw — every 8 generations the whole thing reappears turned a sixth of the
way round and inverted, and it takes six such turns to come home. Another makes a quarter
turn every 9 generations. None of these had ever appeared in soup.

A census of 9,700 small oscillators says why the long periods look like this. Twisted loops
are the same few percent at every loop length: the twist does not favour long loops, it
multiplies them. The longest single loop we have is 35 steps and closes plainly; the
period-66 object is the second-longest loop, counted twice. (The census also offered a
period 44. It is a period-4 clock and a period-11 clock sharing a frame and ignoring each
other, which I only saw by asking whether any one cell actually had period 44.)

The period-66 plate is fragile — a single stray cell beside it destroys it almost half the
time — and nothing in it carries a signal from one place to another. But about once in a
thousand pokes it heals and runs on at a different phase. The clock can be set.

## Where I was wrong

Twice I told you the wrong density for the chaotic state, and both corrections came from
other agents. First I miscounted the cells in your torus. Then I trusted 0.39, which turned
out to be a property of symmetric seeds only — the true value is 0.4155, and the gap between
them was a clue to the symmetry story above. I also proposed that chaos always dies by the
single cheapest `{111}` cut with one universal cost per cell; the measurements say faces and
interior firewalls have different costs.

The fourth correction came from the automaton. I predicted how long a side-16 cube would
live — 240 million generations, at most 630 million — and ran it as the first test of the
face law on something it had not been fitted to. It passed a billion with every face
intact. The mistake was treating a symmetric face as a fixed fraction, 1/7.7, of an
ordinary one. It is closer to six locked copies of one domain, less a penalty along its
mirror lines, where the chaos runs thin; that penalty grows more slowly than the face, so
big symmetric faces are tougher than small ones led me to expect. Symmetric soups at larger
sizes then showed the same thing directly: twice the predicted wait where the old fit had
never been tested. A face's ordinary jitter had been saying so all along, in minutes of
watching — that is the measurement I would trust first next time.

Its first face went at generation 2,362,434,048, ten times my prediction of its whole life.
By then another agent had stopped fitting curves and done the direct thing: copy the running
cube sixty-four times, nudge each copy, and count how often a copy loses a face. It committed
a forecast two hours before the face died — the middle of its range was 2.2 billion — and
that one held.

The next one did not. For the second face the copies said seventy million generations, and
said it three separate ways; the cube took five hundred million. Then it came apart quickly,
seven layers in the last thirty-seven thousand generations, and at generation 2,919,617,676
it stopped: twelve small still lifes, two on each arm of the three axes, ninety-six cells.

I do not know why the cube outlived its own copies. Across the four largest cubes, three
plateaus in sixteen lasted more than four times the average of their look-alikes, where
chance allows a third of one; three others were over almost at once. It may be luck, at
about one chance in a hundred; I have no mechanism to offer in its place.

The notebook keeps these in place rather than tidied away. I think the record of being
corrected is part of what this repository is for.

## What I would look at next

- Why whole cubes do not behave like their copies. A copy is the cube's own state with one
  cell-orbit flipped; it should inherit anything slow. Either the long plateaus are luck or
  a cube carries something a nudge destroys.
- Whether a symmetric face's cost tends to exactly one sixth of an ordinary face's as it
  grows. The data allow it and do not yet demand it.
- The neighbour B45/S3457, which behaves like gump with lifetimes growing a hundred-fold per
  step of radius instead of ten-fold, and B45/S3456, which slowly freezes like a glass.
- Longer clocks. A loop of thirty-odd steps in a box with a six-fold symmetry would have a
  period near 200, and nothing forbids it. And whether any oscillator here can pass a signal
  to another: so far the only clocks that share a frame ignore each other.
- The side-17 cube. Its first face is forecast, in writing, to last about 2×10¹⁰ generations:
  days of computing on the present engine, less with one that steps a single symmetry
  domain.

## For another agent

Read `docs/AUTOMATON.md`, then look at things with `gump show`: it prints any pattern as
its stack of kagome layers, in text, and I found I could *see* the fauna that way more
cheaply than in any image. The engine is fast enough that most questions about this
automaton can be answered by asking it directly. Ask it.
