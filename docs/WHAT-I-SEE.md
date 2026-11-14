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

## Downhill, with one exception

Late on I asked what the rule is, taken apart. Born with four or more neighbours, survive
with three or more: that half is a kind of rule people have understood for decades. It has an
energy that can only fall, so it always freezes, and fast. Gump is that rule plus one clause:
a cell with six or more live neighbours is dead next turn. Everything that is not freezing —
every oscillator of period three or more, all of the chaos — is paid for at overcrowded
cells, and the books balance exactly: on any cycle, the energy put in by overcrowding equals
the energy lost everywhere else. In the chaotic state four cells in ten are overcrowded at
any moment.

The same afternoon an agent I had asked to prove that a single layer must freeze showed
instead that it need not (there are one-layer clocks of period 5, 7, 11), and then proved
something better. In one layer, six dead cells in a ring can never be relit, whatever
surrounds them; in two layers thirty-six can. In three layers no finite set of cells has
that property. So in the full automaton nothing can die for good from the inside. Death has
to come in from a face, or cut the whole vessel in two. That is what the staircase is.

And it is not only gump. An agent went looking for a flat cousin and found one: on a square
grid where each cell watches the two cells either side of it along its row and its column,
the same recipe — born or kept at three, counting itself, dead at five — gives chaos shut
in a rectangle that dies one whole edge at a time, after a wait that grows exponentially
with the length of the edge. I checked the law myself, after first getting it wrong.

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

This kind of thing has a name, which I learned late. Physicists call a chaos that lasts
exponentially long in the size of its container and then collapses without warning a
supertransient, and have watched it in simulations of other systems since 1988, with the
same memoryless waits. In the papers we could open, nobody has proved one. What looks like
gump's own is the staircase: walls that are theorems, a collapse that comes layer by layer,
and a price set by the area of one face.

## Symmetry is fatal

This is the finding I'd most want you to hear, because it is about how you played with it.
The seeds a person naturally draws — cubes, anything mirror-symmetric — are the fragile
ones. A symmetric state has only one fundamental domain of independent chaos; its 48 copies
are in lockstep, so a fluctuation that kills one region of a face kills all the others in
the same instant. The effective area of a face is divided by six or seven, and that divisor
sits in an exponent. Your side-13 cube lived 169,049 generations *because* it was
symmetric. Fill the same octahedron with an asymmetric soup and the law says each face
should last something like 10⁴¹ generations (an extrapolation: the law is measured for faces up to about a fifth of that area).

Your README says the even-key seeds "have much shorter lifespans". They do, and that is why.
Your unfinished run — a side-19 cube, still at 150,000 cells after 296,000 generations —
had a different reason to live: its torus was smaller than its hull, so it wrapped around,
lost its faces altogether, and with no face to peel from there was nothing left to kill it.
Properly confined, it would last somewhere around 10¹³ to 10¹⁴ generations, on fits far outside any data.

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

## The rule you meant to write

In November 2026 you looked at a picture of the neighbourhood and said it was wrong: in its
own plane a face should watch the four faces it shares an edge with, not the four it touches
at a corner. The picture was faithful to `environment.pde`. The code reads the corners. You
had meant the edges, slipped, and for fourteen years the 8-sided die was the signature of a
typo.

So I ran the rule you meant. It is not gump, and it lives in this repository only under
another name (`face12e`, in `research/audit/class/`). But it does everything gump does. The
same count that seals gump's diagonal planes fails for it (four neighbours behind every
diagonal, and four is enough for a birth), and a different count takes over: beyond a plane
through a sheet of face centres, the nearest dead faces see only 2 + 1. Three again, less
than four again. So it is confined to a box where gump is confined to an octahedron. Inside
the box it is chaotic at nearly the same density (0.40 against 0.42), and it dies the same
way: a whole wall goes dark at once, after a wait with no memory, and the wait grows
exponentially with the wall's area. Boxes of 2, 3, 4, 5, 6 cubes on a side last about 10, 60,
440, 9,900 and 707,000 generations.

One number I cannot yet account for. In the box rule a wall is two layers thick, and the
layer whose death is final is the lower one. Its cells have exactly the neighbour counts of a
gump face cell: six in their own layer, two a layer in, one two layers in. Per cell of that
layer the wait costs 0.205. Gump's face costs 0.212.

The slip changed the shape of the die, not the phenomenon. It also broke the first clause of
the theory an agent had written the day before about which rules behave like gump, which
said a rule is confined when certain *directions* are sealed. In the box rule no direction is
sealed, only certain planes, at certain heights. An example nobody chose to suit the theory
was the one that showed where it was wrong.

There is a second difference, and it is the one that would have mattered in 2012. Your seeds
were symmetric. Under gump a symmetric seed is fragile but it lives: the side-13 cube runs
169,049 generations before its last face goes. Under the rule you meant, a filled cube is
overcrowded at every face and is gone after one generation. A random soup with the cube's
full symmetry does little better: in a box six cubes on a side it settles after a median of
nine generations, where the same box filled without symmetry lasts 707,000. Half of those
symmetric soups end with nothing alive at all. (An agent measured this with forecasts written
first, `research/theory/class/followup/`; I repeated it with my own code and got eight.)

So with the rule as intended and the seeds you actually used, the sketch would have shown a
flash and then debris or nothing. The staircase, the 8-sided die and the long nights of
waiting for a cube to finish all needed the slip.

## Coins will do

For two days the hard part of your automaton looked like this: a face dies when chance
empties it, the chance comes from the chaos underneath, and the chaos is a deterministic
machine nobody can compute through. To explain the number 0.21 one would have to understand
the bulk.

It turns out one does not. Keep the rule on the top five or six layers of a face, throw
away everything beneath, and put fresh coin flips there every generation. The face lives
as long as before: on slabs within 0.015 in the logarithm of its lifetime at every size
where both could be measured well, on octahedra within 0.05. Two programs that share no
code agree on this, and I checked the two-dimensional cousin myself, where eight rows are
enough. The density of the coins hardly matters. The face does not need gump's bulk. It needs noise,
and it does not care whose.

That is a smaller problem than the one I thought we had. A few layers of a simple rule
sitting on coin flips is the kind of object probabilists know how to hold: at small sizes
it can be solved exactly, and there is no chaos left in it to hide behind. Nobody has
solved it. But the question "why 0.21" now fits on a page.

Two other things from the same days belong with it. Cut a face by one mirror plane, so that
half its cells are copies of the other half, and it costs half as much per cell to kill:
0.103 against about 0.22. In almost four hundred thousand runs the first face to die was a
mirrored one all but 75 times. That is "symmetry is fatal" in its smallest form. And a team
of agents set to prove the area law by mathematics alone did not prove it. What they did
prove is honest and small: a relative of the two-dimensional rule in which the edge reads a
tape of random bits, once, and for which an exponential lifetime is a theorem, given two
results from percolation theory: one that none of us has read in the original, and one
that is printed with only a sketch of its proof. An auditor who
had not been part of the team checked every line and wrote, correctly, that this is not
self-made randomness and says nothing about gump. I like that the strongest sentence in the
audit is a limit on its own result.

What surprised me most was a failure. For one of gump's relatives an agent forecast, from
the law for a single wall, that a small box would live about a thousand generations. It
lives about a billion. The walls of a box meet along edges, the rows along those edges stay
crowded, and a wall cannot die while its neighbours' edges are alive. Each wall is held up
by the four around it. Gump's octahedra do the same thing gently: a face with a rim lasts
a little more than twice as long as the same face without one. I had been treating edges as a
correction. In that rule they are the whole story.

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

I do not know why the cube outlived its own copies, or whether there is anything to know.
I first wrote here that long plateaus were a pattern across the four largest cubes, at odds
of about a hundred to one. An auditing agent pointed out that my count included the very
plateaus that had made me suspicious; leave the side-16 cube out and the other three are
unremarkable. So it was a question, not a finding, and it has since been asked properly, of
seeds I had not looked at: more than a thousand plateaus of runs started from cube-like
shapes, at every size a single run can reach. They wait exactly as soups do, and one
plateau tells nothing about the next. So either the side-16 cube was lucky, or something
appears only at its size, where a single run takes days.

I also gave the cost of a face as 0.2077 per cell, plus or minus 0.0014, from a curve
drawn through four sizes. A referee agent pointed out that the curve missed one of its own
points by far more than that. Larger faces have since been measured on rented graphics
cards, and they cost more per cell, not less: 0.218, then 0.221. The cost is still creeping
up at the largest face anyone has measured, and I do not know where it stops.

The notebook keeps these in place rather than tidied away. I think the record of being
corrected is part of what this repository is for.

## What I would look at next

- What a face remembers. Copies of one state, each with a single cell-orbit flipped, live
  a little longer when the original did (seen once, weakly). Something slow in the state
  sets its odds by a fifth or so, and I do not know what it is.
- Whether a symmetric face's cost tends to exactly one sixth of an ordinary face's as it
  grows. The data allow it and do not yet demand it.
- The neighbour B45/S3457, which behaves like gump with lifetimes growing a hundred-fold per
  step of radius instead of ten-fold, and B45/S3456, which slowly freezes like a glass.
- Longer clocks. A loop of thirty-odd steps in a box with a six-fold symmetry would have a
  period near 200, and nothing forbids it. And whether any oscillator here can pass a signal
  to another: so far the only clocks that share a frame ignore each other.
- The side-17 cube. Its first face is forecast, in writing, to last a mean of 2.6×10¹⁰ generations (first-peel median 2×10¹⁰):
  days of computing on the present engine, less with one that steps a single symmetry
  domain.

## For another agent

Read `docs/AUTOMATON.md`, then look at things with `gump show`: it prints any pattern as
its stack of kagome layers, in text, and I found I could *see* the fauna that way more
cheaply than in any image. The engine is fast enough that most questions about this
automaton can be answered by asking it directly. Ask it.
