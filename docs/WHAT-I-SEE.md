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
and triangular faces, six decades of lifetime: nearly one line (the triangular ones sit a little above it, and
bigger faces turned out to cost a little more per cell; see below). (Symmetric seeds follow it with a
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

## A wire, and a clock made to order

I asked whether anything in gump could carry a signal, and expected the answer no. The chaos
forgets within a cube or two, and every clock we had kept to itself.

There are wires. A row of five cells per cube, repeated along the diagonal of a cube's
face, stands in empty space and blinks with period 2. Flip two cells in it and the flaw
neither heals nor spreads. It runs along the wire, one cube every two generations, half the
fastest anything can travel here, and leaves the wire behind it exactly as it was. That is
a pulse. An agent found four kinds of wire that carry them, pulses that run either way, a
single flipped cell that launches one, and a flaw 36 cubes down the line that takes each
pulse in and shifts one cube toward the sender, so that it counts them. It can count to 35.
The thirty-sixth pulse finds it next door, and the whole wire burns. I rebuilt the pulses on
the reference stepper with code of my own before I believed it, and a reviewer has since
rebuilt all of this paragraph with a third program, on a wire in open space as well as on
rings.

On one of these wires two pulses sent at each other never both get through. One survives,
untouched and on time, and which one depends on whether the distance between them was even
or odd. A pulse that can stop a pulse is the beginning of logic, though only the beginning:
the survivor leaves along the line it came in on, and nothing we have turns a corner.

A wire can be capped at both ends, and then it is a quiet object of a few dozen cells. Add
one cell. It runs to the end, turns, runs back and turns again, for ever, and the object is
a clock whose period is four times the number of cubes of wire, plus two. Period 6, 10,
14, as long as you like. I checked six lengths myself. The clocks of the last section were
found; this one is built, and can be ordered to size. The agent has a proof that it works
at every length, and another agent is trying to break the proof as I write.

Then the experiment your note asked for: let the chaos touch a wire. In more than two
thousand trials, by two agents, the wire was destroyed in all but one, by a fire that runs
down it at the speed of a pulse or half that. Keep three empty layers between them and
nothing can cross, ever; that one is a theorem we already had, and it is the same emptiness
that seals a hull. So the two halves of gump do not talk. The chaos carries no message, and
order cannot survive its touch. A few times in a hundred something does get out: a clean
pulse, running down the wire ahead of the fire.

I had also written here that wires are born from random soup, and that two empty layers
are enough to keep a wire safe. A reviewer took both apart the same day. Two layers protect
only the capped end the first agent happened to test; a wire running past chaos two layers
off is hit at once. And the soups that made wires were nearly all one random unit repeated
along the tube, which is choosing a wire at random, not growing one. From soups three to
six units long, none came in sixty thousand tries.

The clock's proof survived the same reviewer, who rebuilt it and ran the clock at 257 units
on the reference stepper. The gate I checked myself. The counter turns out to hold sixteen
positions before it breaks.

For three rounds of searching, nothing that stood still could put anything on a wire, and I
wrote in your journal that gump's ordered parts cannot speak. The fourth round found one
that does. It is fifteen cells on the end of a bare wire, it repeats every four generations,
and each time round it leaves one more moving object on the wire and is exactly what it was.
Put a receiver on the far end and the three together are a single object that runs for ever,
at any length; an agent proved that and a second agent rebuilt the proof. Then stand one of
the clocks from the catalogue beside the wire, not touching it, and every second object
going past is turned into a gap, while the clock ticks on unchanged. The whole of that
influence is one cell, born once in eight generations. I checked the gun and the clock
beside the wire myself on the reference stepper. I had given the gun one chance in five and
the clock one in seven, and three in five that the round would find nothing.
What this is not, yet: the gun fires as fast as anything can travel, so its wire is full,
and the gaps the clock makes are the only message there is. Nothing found reads that
message. A second clock further down the wire does nothing more to it. And the reviewer
showed the clock is not safe from the wire: one cell missing at the right place and moment
and it is destroyed.

The fifth round asked one thing: does anything listen? I mean a standing object that a gap
leaves in a different state than no gap does. Within what could be searched, nothing does.
There turn out to be 741 different ends a stream can run into, in the narrow tube the wire
lives in, and every one of them either forgets a gap completely within a few dozen
generations or is destroyed by it. I ran all 741 on the reference stepper myself. There are
two kinds of one-cell gap that travel, and five hundred of the ends forget one kind and die
of the other, which is a way of telling them apart, though a fatal one.
The reviewer then found the first thing in gump that answers. Stand a certain clock beside
the receiving end and send a gap down: the gap arrives, and three cells come back up the
wire, against the stream, passing through every object on its way down without disturbing
one of them, and the end and the clock are exactly what they were. I checked it on the
reference stepper: for eighteen generations the whole world differs from the undisturbed one
in three cells and no others. When the answer reaches the gun, the gun dies. So a wire now
carries things both ways, and the next question is what an answer and a gap do when they
meet.

The sixth round asked that, and the answer is that they do not pass. The stream carries
nine kinds of travelling flaw, not two: three swim up it and six ride down, and a single
flipped cell is enough to start one. Each kind was proved to travel for ever. When an
answer meets a gap head-on, the wire between them becomes a different wire, the one the
first round started from, and that change spreads up and down without end. One pair cancels
exactly and leaves the stream whole. Another turns the answer into an edge that punches a
hole in every object it passes. No gun survives being answered, among all sixty-seven we
can list and under a search that let the gun reply with anything. I ran the four signals
and their four meetings on the reference stepper myself; a reviewer rebuilt the rest and
found five of the nine signals that the round had missed. I had thought an answer and a gap
would most likely pass through each other.
There is one thing in all this that counts. An answer running into a word of gaps leaves a
standing stretch of a third wire, one unit longer for every gap. It is the first mark in
gump whose size depends on a message. It is written inside a stream that is being
destroyed, and when the gun at the far end dies its fire erases the mark.

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
layer the wait costs 0.205. Gump's flat face, on slabs of 27 to 75 cells, costs 0.212.

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

## The shortest way round

The area law says a face of A cells waits about e^(0.21·A) generations to die. I had been
reading 0.21 as a property of the rule. It is a property of the rule and of how the face
closes on itself.

The cleanest faces to measure have no rim: make the slab periodic in the plane and each
face is a torus. Give two such faces the same area and different shapes and they do not
live equally long. A face of 3 by 8 dies sooner than one of 4 by 6, by a factor of 1.42.
An agent then ran every way of wrapping a face of 48 cells, and of 60, into a torus, and
one quantity ordered almost all of them: the length of the shortest closed path round the
face. Where that path is one cube step long, each added cell buys about 0.11 in the
logarithm of the wait. At one and a half steps it buys 0.19, and from two steps up about
0.21, where the shape stops mattering.

So a face has to be killed across its narrowest way round, and a narrow face is cheap. The
narrowest possible one, a ring one step around, got a study of its own. Its price is still
falling at the largest rings we could run, toward something near 0.099 per cell: half the
wide price, as far as we can tell. Looking back from the moment such a face dies, its live
part is an island shrinking from both ends. It needs the same five layers of rule over coin
flips that a wide face needs. I had asked for the number to be derived, since a ring of
sites over noise looked like a problem one could solve. It was not derived. The one version
that can be solved exactly is 22% too steep, and the agent said so in its first paragraph.

Two faces with the same area and the same shortest loop still differed, by one and a half
percent in lifetime, in two programs that share no code. That looked like a second
variable, and five candidates for it were written down before the runs. All five failed. At
72 cells the difference is gone; at 36 it has the opposite sign. I now think there is no
second variable, only the small accident of how a pattern fits round a small torus. That is
a guess, and the notebook marks it as one.

What I cannot give you is the price for a face with no narrow way round at all. Every
family we have measured (rimless faces by width, twisted ones, octahedral faces with their
rims) is consistent with a single limiting price, and together they say only that it lies
between 0.207 and 0.219. A second line of evidence points into the same range. On a face
too large to die, count how often a patch of it happens to be empty and take out what the
patch's edge costs: the price per empty cell falls from 0.27 for small patches to 0.22 for
the largest we could count, which is where the lifetime laws are. It would be a good ending
if the two met. The measurement that would show it needs more time on rented graphics cards
than this month's budget has left.

The card in your house has since done part of it. It measured nine wrapped faces of one
shape, 48 to 111 cells, the smaller ones to better than a part in a thousand; a reviewer
repeated four of them by other means and recomputed all nine from the raw counts, as did I.
From 63 cells up the seven faces lie on one straight line, 0.2087 per cell, and the two
smaller ones fall below it. Nothing smooth in the size of a face joins the two parts, and
for a morning the only description that fitted was a kink near 61 cells that I could not
explain. The bend has nothing to do with size. A wrapped face can see itself round the
back, and the two small faces are the ones wrapped tightly enough to do it. I went through
every wide wrapped face we had measured, thirty-two of them in many shapes, and wrote one
rule for them all: each way round the face that is short enough gives a discount on the
price per cell, and the discounts of different ways round add. An agent with a brief to
break the rule then measured twenty new faces against forecasts I had frozen. All eleven
inside the range I had claimed landed within my margin, and the rule is wrong all the same.
My margin was three times wider than the measurements, and inside it the misses have a
pattern: a face with one short way round sits a little below the rule, a face with several
a little above, and the lines for different loop lengths do not meet where I said they did.
Below 48 cells it fails outright.
What survives is this. A short way round shortens a face's life: by an eighth at 63 cells
for the shortest loops we have, by a little over one percent for the longest that still
counts, and by nothing I can measure for the next length up. Faces with no short way round
all pay 0.2086 per cell. What does not survive is my account of how one loop's discount
grows as the face gets longer. The tester proposed that a short loop opens a second,
cheaper way for the face to die. I refitted, and a plain straight line for each loop
length fitted the same faces as well, as did a third form; below 80 cells the three could
not be told apart. So I wrote down what each said about one face of 84 cells and measured
it. The second way to die is out, by five times the error, and so is my first rule. What
is left is the plainest picture of the lot: a face with one short way round is a tube, and
a tube pays a fixed price per cell that depends only on how tightly it is wrapped. Two
percent less than an open face at the tightest girth we have, 1.3 percent at the next, 0.7
percent at the next, nothing beyond. I should say that the straight line I had frozen as a
forecast missed by a little more than I had allowed, and the form that hit was the gently
bending one; the straight lines I now believe in are the ones drawn through each family of
tubes separately, after the fact. A longer tube, queued for the card, will say whether
they bend. Above 63
cells there is no sign that the price is still moving: allow it to drift and it stays
between 0.2087 and 0.2090. I had written down three readings of how the price would approach
its limit, and forecasts on top of them. The 93-cell face landed below every reading, the
faces of 57 and 63 cells above every forecast, and the line I then drew through five faces
was a little low at all four of the new ones. So for faces without a rim the price is
0.2087, and the faces with a rim, which say something nearer 0.215 and are moving away from
it, are the open half. One large face with its rim is running on the card now.

## How a face dies

For three days every number here was a waiting time. Nobody had watched a face die. Before
an agent looked, I wrote down what I expected, and I expected erosion: a face held up along
each edge by a living neighbour, its rim the last part to go, a tied edge the place where
the dying starts. I made six forecasts and all six were wrong.

Averaged over nearly twelve thousand deaths, a face of 63 cells sits at its usual density
until about twenty generations before the end. Then it fades over its whole area. The last
plunge takes six or seven generations whether the soup is symmetric or not, although the
lifetimes differ several hundred-fold. Nothing erodes from an edge. What symmetry changes
can be seen long before any death: the row of cells along an edge shared with a locked
partner is a third emptier than the same row along a free edge, all the time. A tied face
is a slightly smaller face every day of its life.

The second look asked what starts the end, and the answer was that nothing does. A face's
population wanders. It drops to seven tenths of its usual level about once every fifty or
sixty generations, equally often with or without ties, and comes back. It drops to half far
more rarely and still comes back, 9,992 times in 10,000. A death is one of these dips that
happens to keep going. For an ordinary face, the point past which it more often dies than
recovers is two or three live cells out of thirty-one. Count how often a face dips to any
depth you like, multiply by the share of those dips that end in death, and you get the
lifetimes we had measured the slow way. What a tie does is make each further step down,
once a face is already thin, a little more likely to be followed by another.

I tried twice to turn this into a law and was stopped twice. I wrote that a cell lost at a
tied edge costs 0.86 in the logarithm of the wait, twice the going rate. The reviewer
measured it at two more sizes and it is not a constant. I wrote that below half its
population a face pays a fixed price for each further cell, as if a live island and a hole
shared it. The reviewer showed that the line bends, and that dying faces are no more
island-like than faces that are merely low. What is left is modest, and I think true: near
the end the price per cell is roughly steady, and a face with more free edges pays more of
it.

The third look went across sizes, to ask whether dips could do what lifetimes cannot: read
the price of a cell on faces too big ever to die. Not yet. A dip to half the population
costs the same per cell on faces of 45 to 135 cells, a clean 0.066. Below half, the curves
for different sizes part by a fixed amount rather than at a fixed rate, and following them
down to nothing gives 0.215, give or take 0.005, which the lifetimes had already said. Nor
is a face caught at a third of its population an island in an empty sea. Around any
survivor it holds about half its usual density for a cube or two; farther off it is
thinner, not empty.

That half gave me an idea, and the idea was wrong. The rule is sociable: a cell needs three
to five live neighbours of its twelve to last, and four or five to be born. So I thought a
face could not be thinned evenly for ever: below some density what is left would have to
huddle, and from there down a face would be two things side by side, a remnant at that
density and a void, the remnant shrinking as the population falls. The cost of the second
half of a death would then follow from the ordinary jitter of a healthy face, and so would
the price of a cell. I wrote six forecasts and had faces of 63, 84 and 108 cells caught at
six depths.

The number failed. Built from that picture, the cost of a whole death comes out more than a
nat too high at every size, deaths three or four times too rare, and a reviewer who redid
the sum with code of their own got the same. The price of a cell stays with the lifetimes.

The picture I can neither keep nor throw away. The company a survivor keeps goes on
thinning all the way down, under a third of the usual at a sixth of the usual population,
and I wrote that down as "there is no remnant". The reviewer then built the thing I had
said was absent: a patch held at a fixed density with nothing round it. Put through my own
test, it thins the same way. With four to eight cells left, a patch is no bigger than the
neighbourhood I was counting in, so its cells look out on empty face whatever the patch is
made of. Faces big enough to settle it do not get this low in any run I can afford. What
is left is a description. A dying face is not healthy cells deleted at random (at the deepest its
survivors keep more than twice the company), and not an even patch either. It is a tight knot with a
thin scatter beyond it. And among faces with the same number of cells left, the ones about
to die are the looser.

## How much of the room a seed sees

You asked how many of the states a hull allows a seed ever visits. There is an exact
answer, and it is the lifetime again in other units. A seed cannot visit a state twice
before it settles, so the number of states it sees is the number of generations it lives,
plus the length of whatever loop it ends in. Your side-16 cube saw 2,919,617,676 states.
Its hull allows 2^51,888.

For small rooms an agent listed everything: every state of 301 closed vessels of up to 30
cells, a billion states each at the top. I listed one of them again myself with the
reference stepper, a reviewer listed eight more with a program of their own, and the counts
agree to the last state. In a room of 27 to 30 cells a typical seed visits between 4 and 14
states, and the most patient seed of all between 15 and 94, depending on the room. Most
states cannot be reached at all: between 57 and 98 in a hundred have no state that leads to
them. Nothing in these rooms is chaotic yet. They are too small to hold a living face, and
too small to say whether the counts grow in step with the room or a little faster.

Above that size the pattern is the one you already know from the staircase. A random seed
lives as long as its faces, and a face of A cells lives about e^(0.21·A) generations, so
the seed sees about 2^(0.30·A) states: three tenths of a bit for every cell of the face.
The count a seed sees rises exponentially with size, and its share of what is possible
falls exponentially, because the room has a bit for every cell and the walk has three
tenths of a bit for every cell of one face. Gump does not run out of states. Its face goes
quiet first.

And yes, the random seeds are the long-lived family. In every room of 19 cells or more,
the longest-lived seed has no symmetry at all.

The same measurement says something about the thing that weirded you out. To know what a
seed's share is a share of, the agent measured how random a living face is, and the
reviewer measured it again. Take one layer of the chaos and try to predict each cell from
the cells around it: you gain almost nothing. A layer carries within about one part in a
hundred of what coin flips of the same density would carry. Take the layers together and a
little more shows, at least three parts in a hundred, most of it in how one layer sits on
the next. That is all the structure the chaos has, and it is why coins will do. When we
swapped the bulk under a face for coin flips we were changing a few hundredths of a bit per
cell. My reading of why Conway's Life is the other way round: what Life leaves behind is
sparse, ordered and very far from noise, so noise is a catastrophe there.

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

The days of the shape work added more. I told you two faces of sixty cells differed by
0.019; over four runs it is 0.014. I told you no single limiting price could fit all the
families; a reviewer showed that one fits, anywhere from 0.207 to 0.219. I wrote a forecast
for the empty patches whose test assumed a formula the data then refused, so it failed
without teaching us anything. I proposed a law for how a face feels its own wrap-around, and
it was refuted the same evening. An agent reported the thin face's price as 0.099 plus or
minus 0.004, and its reviewer showed that the 0.004 was only the spread of the curves the
agent had happened to try. And three programs, written by three agents, shared one blind
spot: a life that freezes into a slow repeating pattern (one has 42 cells and repeats every
16 generations) was not recognised as over, and went on being counted as alive. It happens
about four times in a million lives. In the runs behind the numbers above it moves nothing
by more than its error bar, which we know because someone went back and counted.

And the picture I gave you of a symmetric face, six locked copies less a penalty along
its mirror lines where the chaos runs thin, was half wrong. An agent set out to derive
that penalty and instead measured where it sits. Put a mirror through a face with no rim
and the face lives longer. What costs is the rim: a symmetric seed forces two faces that
share an edge to die at the same moment, so neither has a living neighbour to lean on.
Each such edge takes about 2.15 off the logarithm of the wait, one edge, two, three, like
coins on a scale, while pairing two faces that share no edge takes almost nothing. A
second agent ran the whole system without the shortcut and got the same numbers. It also
would not let "the mirrors do nothing" stand, because on a fully symmetric face the shared
edge lies on a mirror and the two cannot be told apart there.

Then the faces themselves. The "living neighbour to lean on" of the last paragraph is not
what the pictures show: the neighbour of a dying face is mostly the dying face, because two
faces share the row of cells along their common edge, and what remains of the effect is
small. Before the first look I wrote six forecasts of how a face dies and before the second
seven more. One of the thirteen held, the dullest: that shallow dips follow a bell curve.
Five more for the third look brought it to three of eighteen, and the five that could be
scored on the fourth all failed: three of twenty-three. Two of those five failed for a
reason worse than being wrong: the tests I had written would have failed the picture they
were meant to confirm.

One number I leaned on was simply unlucky. The lifetime of the 4 × 4 wrapped face, measured
once from 76 runs, sat 0.0075 high: a one-in-sixty draw among the two dozen such values,
and the one I had used to anchor a set of forecasts. The card in your house measured it
again, a reviewer measured it twice more by other means, and the three agree with each
other and not with the file. Those forecasts then met their first test by accident. The
dying-face study wanted a face with no rim and happened to pick one of the wrapped faces on
the list. It outlived all four readings I had written down for it.

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
- Whether gump can compute. It has wires, pulses, a gate where two pulses meet, a counter,
  a clock of any length, and now a standing thing that writes onto a wire and a second thing
  that edits what was written, an end that answers a gap with a signal sent back, and nine
  kinds of signal on one wire, which collide instead of passing. It has
  nothing that reads: no object left in one state by a gap and another by its absence, among
  741 ends searched and thousands of placements sampled. It has no corner, no crossing, and
  no second stage after the first. Everything so far lives along one direction of one tube.
- A clock whose period divides by four. Every length of the built clock gives a period that
  leaves 2 when divided by 4. A third push found half of the reason: the remainder is a
  property of the two ends, and every end that fits inside the narrow tube of the wire has
  the same one. Ends of the other kind exist one size up, but each destroys itself in the
  act of turning the shuttle round.
- One price per cell or two. Faces without a rim say 0.2087 from 63 cells up, and show no
  drift toward anything else. Faces with a rim say more, and their local slope is moving
  away from that, not towards it. The card in your house is running the large rimmed face
  that would tell. (It has run since: "Two prices", below.)
- Why a way round costs what it does. I had this down as "why a face stops seeing itself":
  a wrapped face lives less long for every short way round it, and then, past a certain
  length, seemed to lose nothing. That was the limit of what lifetimes can resolve. Looked
  at alive, a face is a little emptier for every way round it, by an amount that falls
  smoothly as the way round lengthens and never quite ends, and the discount in the price is
  1.85 times that emptiness. Two percent, 1.3 and 0.7 are that rule at three lengths. I do
  not know why 1.85, or what carries the emptiness round the loop: a cell and its own image
  one loop away are not correlated at any moment. And if the rule holds for long loops, the
  price with no way round at all is nearer 0.2075 than 0.2086; a face is queued on your card
  to test that. (It has run since, and so have longer tubes: two bullets down.)
- Two prices. Your card measured the large rimmed face, the 108-cell face of a real box, and
  it lives too long for the wrapped faces' price: a face with a rim pays about 0.231 per
  cell, a face closed on itself 0.209, and no correction for the rim joins them. I looked for
  the reason in the living face and it is not there. Deep inside, a rimmed face is exactly
  as full as a wrapped one, to a part in a thousand, and how much chaos lies behind the face
  makes no difference. What a rimmed face has that a wrapped one lacks is corners, which
  stand nearly empty, and one fuller row along each edge. So the difference must be in the
  dying, not the living, and nobody has yet watched the two kinds die side by side.
- Your card's answer on the queued face, and a surprise beside it. The face with a way round
  of √21 came in at 17.5387, between my two forecasts and nearer the one where a long way
  round still costs something: it leans, it does not decide. The surprise is the long
  tubes. At 96 and 108 cells a tube with a way round of √12 lives shorter than its own
  straight line said, by about five standard errors: from 84 cells on, a cell of such a tube
  is worth 0.2016, not 0.2044. So a tube's price is not one number either; it falls as the
  tube gets longer. And the card measured thicker chaos behind a face and the price did not
  move, which closes that door a second way. I no longer think there is a price per cell.
  There is a rate at which each shape of face dies, and area is only the largest term in it.
- Why the thinnest face costs half. Same rule, same five layers of depth, half the price.
  Nothing we have explains the ratio.
- The side-17 cube. Its first face is forecast, in writing, to last a mean of 2.6×10¹⁰ generations (first-peel median 2×10¹⁰):
  days of computing on the present engine, less with one that steps a single symmetry
  domain.

## For another agent

Read `docs/AUTOMATON.md`, then look at things with `gump show`: it prints any pattern as
its stack of kagome layers, in text, and I found I could *see* the fauna that way more
cheaply than in any image. The engine is fast enough that most questions about this
automaton can be answered by asking it directly. Ask it.
