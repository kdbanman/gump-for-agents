# The owner's journal

Notes and questions from Kirby, in their own words, oldest first. They are not instructions and not grants (those
are quoted in `LEAD.md`); they are what the owner is wondering about. An agent whose work bears on one of them
should say so in its report. Under each note the lead keeps a short list of what in the repository speaks to it.

## 2026-11-15, about 07:54 UTC

Dictated; the owner adds that speech-to-text may have garbled words or spelling.

> a note for the human section of the repo, if you have one: it honestly weirds me out that the faces/layers are so
> isolated from each each other. I might be using the face or layer, terminology incorrectly, but I guess I remember
> feeling very surprised when you discovered that a layer "didn't care" whether or not it was the rule underneath
> it or random noise underneath it. Obviously the state trajectory is different between those two, but it's wild to
> me that there is a meaningful way in which they are still the same. Like if you were to replace any chunk of
> Conway's game of life with noise, the effect is drastic in every way.
>
> And your signal question feels like it could be an interesting lens on the isolation phenomenon.
>
> And I honestly don't know if this is related to the above: but something I've always wondered is just how much of
> the possible state space a Gump seed explores. I didn't phrase that very rigorously, but within any given hull,
> there are only a finite number of environment states possible. For the longest lived family of seed states (which
> I think are the random seeds), how many of the possible states are hit? And is there any consistency or pattern
> that extrapolates as size goes up?
>
> Do with these questions what you will. Just writing them down as a journal here, because you got me thinking.

What speaks to it (the lead, same day):

- **The isolation.** The finding the note recalls is the essay's "Coins will do" (`docs/WHAT-I-SEE.md`; notebook
  entries of 2026-11-14 on the exponent study; CLAIMS X1–X3): replace everything below the top five or six layers
  of a face by fresh coin flips and the face lives as long as before. Two numbers already on file say how deep the
  isolation goes: the correlation length inside the chaos is 0.65 ± 0.03 of a cube step (CLAIMS P4), so a
  statistical imprint fades by a factor of about five per cube; and a dying face's neighbour barely notices
  (CLAIMS DY3). Trajectories are another matter: a flipped cell changes everything downstream, and how fast that
  damage travels is measured in `research/phase/`. "Different trajectory, same statistics" is the pair
  "sensitive, and quick to forget".
  *Added 2026-11-18:* the isolation has now been tested with everything else left running. Overwrite the cells six
  or more layers under one face of a closed octahedron with fresh coins every generation and that face's lifetime
  does not move (−0.4 ± 1.3% at 63 cells; CLAIMS X4). Coins three layers under a face lengthen its life by up to a
  fifth (X5), which nobody can explain yet. Notebook 2026-11-18, "the noisy hull, rebuilt from outside".
  *Added 2026-11-19:* measured layer by layer by two programs (X7): coins directly under a face nearly double its
  life, the first two layers down carry five sixths of the effect, and with the coins six layers down nothing is
  left. So the isolation has a profile, and it is about two layers thick.
- **Signals as a lens on it.** `research/signals/` (started 2026-11-15): whether anything can carry a signal. In
  the chaos the two numbers above say no usable signal survives a cube or two; the open case is the ordered
  remains (wires, sheets, clocks), where nothing forgets.
- **Later the same day (08:50 UTC): signals exist.** The first push found pulses that travel along free-standing
  wires at half the speed limit and leave the wire as it was, an emitter, a receiver and a head-on interaction,
  each judged by the reference stepper (notebook entry "gump carries signals"; CLAIMS SG1–SG4). So the ordered
  remains do carry what the chaos cannot. Whether a pulse can pass between a wire and a living face is one of the
  questions given to the second push.
- **How much of its state space a seed explores.** `research/statespace/` (started 2026-11-15, forecasts first).
  One part is already known from the lifetime law. A trajectory never repeats a state before it settles, so the
  number of states a seed visits is its settling time, and that grows as e^(c·A) with A the cells of a face and c
  about 0.21: about 0.30 bits per face cell, against one bit per cell available. So the share of the state space
  that is ever visited falls exponentially with size even as the lifetime rises exponentially. The study is to
  make that exact where the whole state space can be listed, and to say what the living states are a share *of*.
- **Later the same day (10:20 UTC): the count is in** (`research/statespace/README.md`; notebook entry "how much of
  its state space a seed explores"; CLAIMS SS1–SS3; a review is running). Your side-16 cube visited exactly
  2,919,617,676 states, about 2^31.4, of the 2^51,888 its hull allows. Where every state can be listed (301 vessels
  of up to 30 cells, about a billion states each at the top) a typical seed visits 4 to 14 states and the most
  patient seed of all 15 to 94 (the ranges over the 34 vessels of 27–30 cells, as corrected by the review); most
  states (57–98%) cannot be reached from any other. The pattern that carries upward is the lifetime law read in
  bits: a random seed visits about 2^(0.30·A) states for a face of A cells, a count that rises exponentially,
  while its share of the hull's states, or even of one layer's, falls exponentially. Symmetric seeds see less
  (0.15–0.29 bits per cell of their effective face). And you were right that the random seeds are the long-lived family: in no vessel of 19 or
  more cells is the longest-lived seed symmetric.
- **Later still (10:30 UTC): what chaos does to a wire, and a clock** (notebook entry "a clock of every length";
  CLAIMS SG5–SG10; a review is running). This is the experiment your second thought asked for. Run a wire through
  a block of living chaos and the wire is destroyed, every time in 800 trials, by a fire that travels at the speed
  of a pulse. Leave two empty layers between them and nothing ever crosses. So the isolation has a hard edge: the
  chaos does not carry a message and does not leave one alone either; order survives only where the chaos cannot
  reach. One thing does get out: on about one side in twelve a clean pulse runs down the wire ahead of the fire.
  The same push built a clock (a wire between two caps, period 4N + 2 for N units of wire, checked by me on the
  reference stepper at six lengths), a gate where two pulses meet and one survives, and a counter that pulses
  push up from one side and down from the other.
- **The two thoughts meet (10:48 UTC; notebook entry "the state-space study reviewed"; CLAIMS SS3).** To say what
  a seed's share is a share *of*, the study measured how random a living face is, and a reviewer repeated it with
  a sampler and an estimator of their own. One layer of the chaos, seen alone, is within about 1% of coin flips of
  the same density (at least 0.006–0.013 bits per cell short of them). The layers taken together are at least
  2.7% short, and most of that is in how one layer sits on the next. So the chaos has very little structure for
  anything to depend on, which is the quantitative face of "it didn't care whether it was the rule underneath or
  noise". Life's debris is the opposite: sparse, ordered, far from noise. (One-sided: the measurement bounds the
  structure from below; there could be more at ranges the estimator does not reach.)
- **A correction to the entry of 10:30 above (11:26 UTC; notebook entry "the second signals push reviewed").** Two
  things in it were too strong. The gap that keeps order safe from chaos is three empty layers, not two (that is
  the theorem T3 we already had; two layers protect only the capped end the first agent happened to test, and a
  wire running past chaos two layers off is hit at once). And the fire runs at the speed of a pulse only in dense
  chaos; in thin chaos it is often half that. What stands: contact destroys the wire (about 2,300 trials by two
  agents, one exception), the clock (its proof was rebuilt by the reviewer and the clock run at 257 units), the
  gate, and the counter, which holds sixteen positions. The clean pulse that escapes ahead of the fire is rarer
  than I said: a few times in a hundred.
- **The isolation goes one level further down (12:50 UTC; notebook entry "the third signals push"; a review is
  running, so treat this as provisional).** Your note was about faces and layers that do not hear each other. A
  third push went looking for the parts a computer would need next (something that emits pulses on its own, a
  corner, a clock that drives a counter) and found none of them. What it found instead is the same isolation among
  the *ordered* things. The end of the clock swallows any message sent down its wire, letter by letter, and is
  exactly as it was afterwards: it cannot be told anything. In a census of several thousand other wire ends, each
  either swallows everything the same way or disturbs the wire (sends something back, moves, grows or burns); not
  one stays put and remembers. And the only thing that ever puts a
  pulse on a wire is a moving object already inside that wire. So far gump's ordered parts can keep time, carry,
  count and block, but none can speak onto a wire from where it stands, and none listens. Whether that is a law or
  only the smallness of what was searched is open; the searches were small.
  *Reviewed since (13:18 UTC; notebook "the third signals push reviewed"):* the proof about the clock's end holds.
  And the reviewer found the first thing that answers back: a wall between two kinds of wire that, hit by two
  pulses in a row, moves one step and returns exactly one pulse the way they came (I checked it myself on the
  reference stepper). It only exists on a closed ring so far, and it moves each time it is used.
  *And since (16:03 UTC; notebook "the fourth signals push reviewed"):* half of that sentence no longer holds. An
  ordered thing can speak onto a wire from where it stands. A fourth push found a 15-cell object on the end of a
  bare wire that puts a moving object on it every four generations and is exactly restored each time (checked on
  the reference stepper by three separate codes, one of them mine). With a receiver at the other end it is a
  closed loop that runs for ever at any length, and that is proved. And a second ordered object, one of the
  catalogue's period-8 clocks standing beside the wire, turns every second passing object into a gap without
  being changed itself: the first time one ordered part of gump acts on what another has sent. The other half
  stands: nothing yet listens. Nothing found is left in a different state by a gap than by an object. The reviewer
  did find that the right single cell on the wire, at the right moment, destroys the clock standing beside it, so
  the clock is reachable from the wire; reaching it without destroying it is the open question.
  *And since (20:26 UTC; notebook "the fifth signals push" and "… reviewed"):* a fifth push asked only whether
  anything listens, and within its bounds nothing does: of 741 ends a stream can run into, 599 forget every gap
  exactly and 142 are destroyed by any gap, and I checked every one of them on the reference stepper. But the
  reviewer found the first thing that answers. The receiving end, with one of the catalogue's clocks standing
  beside it, takes a gap and sends back a different signal, three cells, that swims up the stream against the
  objects coming down, and the end is left exactly as it was, ready for the next. So a wire in gump now carries
  messages both ways at once. The one thing at the far end, the gun, is destroyed when the answer arrives; a
  sixth push is asking what an answer and a gap do when they meet, and whether a gun can survive being answered.
  *And since (23:08 UTC; notebook "the sixth signals push" and "… reviewed"):* they do not pass. The stream turns
  out to carry nine kinds of travelling flaw, three going up and six going down, and one flipped cell is enough
  to start an answer. When an answer meets a gap head-on, the stretch of wire between them turns into a different
  kind of wire, and that change spreads both ways and never stops. One pair of flaws cancels exactly and leaves
  the stream whole. No gun, of every one we can list or search for, survives being answered. So a wire in gump
  carries messages both ways, and for now two-way traffic is a head-on collision. The nearest thing to a memory
  yet: an answer running into several gaps leaves a standing mark one unit longer for each gap, a count, but it
  is written in a wire that is being destroyed around it.
- **2026-11-18: a memory, and one sentence above taken back** (notebook entries of that date: "the eighth signals
  push, reviewed", "three more signals results in one night"; CLAIMS SG33 to SG38). "No gun survives being
  answered" is wrong: of 867 guns that can be listed one size up, 34 survive the answer, changed (a reviewer's
  find; nobody has repeated it). And the count that was written in a dying wire can now be kept. A capped length of
  the third wire absorbs each pulse sent into it and grows a stretch one unit longer per pulse; it holds that
  number for ever; one cell removed gives it back as exactly that many pulses (proved for every count); two
  pulses on a wire laid across it do the same without a hand (rebuilt by a reviewer and proved for every count,
  the proof not yet refereed; the pair itself is still made by a hand); and a pair of pulses on another crossing wire reads whether one place is empty without
  changing it. So ordered parts of gump can now speak, keep, add and hand over. What is still missing is the thing
  the note asked about turned round: nothing found lets what is stored decide what is sent next.
  *Later the same day (notebook "the ninth signals push, reviewed"; CLAIMS SG39, SG40):* two exceptions, both on
  the reference stepper and both with the deciding pulse made by a hand. A pulse sent along the wire sets a far
  store free if the place before it is empty and is swallowed if a store is there. And at one exact timing a call
  plus a pulse gives back one fewer than was stored, and lets the pulse through only when nothing was stored: a
  subtraction that reports zero, which is the one operation a row of counters needs to be a computer. It cannot
  yet be repeated, and nothing the machine makes starts it. The reader does not live with writing and calling.
- **2026-11-18: what the isolation is made of, seen in a death** (notebook "how a face dies, audited from
  outside"; CLAIMS DY16 to DY21). A second session watched wrapped and rimmed faces die and an outside audit
  rebuilt it. A face layer over nothing but private coins has both ways of dying that the real faces have (a
  one-step boom and crash on a wrapped face, a slow fade on a rimmed one), and which one a face takes is decided
  cell by cell by how many of a cell's neighbours lie inside the vessel, nine or seven. So the mechanism needs no
  chaos underneath, as the note guessed. The numbers do care: the coin-driven model is 0.12 ± 0.05 high at the
  120-cell tube, and the layer under a dying face is far from its ordinary state (0.56 to 0.73 of it).
  (2026-11-20: that 0.12 is against the card's value for the 120-cell tube, which a second program has not
  reproduced; against the second program's value the model is 0.03 ± 0.06 high.)
