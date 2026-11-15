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
- **Signals as a lens on it.** `research/signals/` (started 2026-11-15): whether anything can carry a signal. In
  the chaos the two numbers above say no usable signal survives a cube or two; the open case is the ordered
  remains (wires, sheets, clocks), where nothing forgets.
- **How much of its state space a seed explores.** `research/statespace/` (started 2026-11-15, forecasts first).
  One part is already known from the lifetime law. A trajectory never repeats a state before it settles, so the
  number of states a seed visits is its settling time, and that grows as e^(c·A) with A the cells of a face and c
  about 0.21: about 0.30 bits per face cell, against one bit per cell available. So the share of the state space
  that is ever visited falls exponentially with size even as the lifetime rises exponentially. The study is to
  make that exact where the whole state space can be listed, and to say what the living states are a share *of*.
