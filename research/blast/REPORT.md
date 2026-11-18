# Why a face dies at the rate it does: report of the night of 2026-11-18

For Kirby, from the session in charge of the blast. Everything is under `research/blast/`; each agent's directory
has a README with the command for every number, and `research/blast/README.md` is the index. Labels as in the
notebook: **[proved]**, **[measured]**, **[conjectured]**. "Refereed" means a second agent rebuilt the result with
its own code from the oracle; every finding below says whether that happened. The budget, not the clock, ended the
night: the Fable window filled at 30 to 45 points an hour with eight to ten agents, so the work ran from 03:10 to
about 06:25 UTC, not to 10:45. This report was itself refereed against its sources (`ref-report/REVIEW.md`) and
corrected.

## The short version

**A face does not thin out and die. A wrapped face dies of too much life, and a rimmed face cannot.**

- **A wrapped face (a wide torus or a tube) busts.** From an ordinary generation it over-fills in one step, to
  three quarters full (33 → 48.8 of 63 cells), together with the layers beneath it. Then four in five of its live
  cells have six or more live neighbours and die, almost nothing is born, and one generation later about 11
  scattered cells are left over layers that have crashed with them. Usually the fragments rebuild the face; about
  one time in 130 at 63 cells (one in 1,100 at 84, the outside audit's count) none of them is large enough, and
  the face is empty five to seven generations after it was normal. The crash is everywhere on the face at once:
  no hole, no front, no band in it. What it leaves is a dozen cells in clumps, and the order in which those go is
  patterned in space in about half the deaths (the audit's correction to this report's first wording). Nearly
  every death of a wrapped face goes this way.
- **A hull face fades instead.** Its rim cells have 7 neighbours inside the vessel where an interior cell has 9, so
  they are rarely overcrowded; the face lives through an over-full generation and is back to normal one generation
  later. It dies by a lopsided fade of about ten generations (of the cells that die in it, 58% starve and 42% are
  overcrowded: a tilt towards starvation, not pure starvation).
- **This is the rule and the lattice, not the chaos.** A one-layer surrogate with coins in place of the chaos,
  solved exactly, has the same two exits with the same dependence on shape; so has gump's 2D relative.

That is the mechanism in plain words, and it is why the differences between shapes "are not in the living state":
the living states are the same and the exits differ. It is **not** a derivation of 0.2087 or of 0.231, and there
is no formula yet. The 135-cell hull face is **not decided**: a forecast of 29.22 ± 0.02 (conditional on a
four-point straight line) and a first measurement on a coin-driven surrogate (between 29.26 ± 0.06 and 29.34,
depending on how the surrogate's own offset from gump continues) agree within about one error, and "the wrapped
price takes over" (29.163) is 1.5 to 3 errors below each.

**What the second phase added (the same day from 11:00 UTC; three solvers and one referee; details in the next
section).**

- **Boom and bust is confirmed on gump itself by another session's code**: four generations before death a
  wrapped face is at 0.72 to 0.75 of full on four faces (the launch level here: 0.738), and hull faces show no
  such generation. Forecast first; held.
- **The lifetime price is not the cost of a hole in the living state.** That was the PI's idea; it failed at
  every size reached (refereed).
- **The two prices are probably not both asymptotic [conjectured, from three measured facts].** Alive, the
  interior of a hull face is a wrapped face from two rows in (refereed). No row of a corner-free rimmed strip
  costs more than a wrapped row at the same loop (two codes agree). And the hull's 0.231 is a marginal price, a
  second difference, which sits above the average price for as long as the average is still rising with size;
  closed faces show the same. At what size the hull's marginal price comes down is not known.
- **The 120-cell tube is 24.5086 ± 0.0169, below every forecast, this report's included.** A tube's line bends
  (0.2023, 0.2013, 0.1957 per cell from 84 to 120 cells) and the night's fitted tube law is refuted.
- **The 135-cell hull face is still not decided.** A second sampler (gump on the whole hull, coin replacements at
  a low rate deep under the watched face) is exact at zero noise and matches brute force at 45 and 63 cells. Its
  blind test at 108 cells reads 23.422 ± 0.025, 23.228 ± 0.119 and 23.368 ± 0.065 at noise rates 1/16, 1/32, 1/64
  against gump's 23.3392; with every replication weighted equally that is +0.009 ± 0.044 from gump. One
  replication's rate is long-tailed there, so those errors understate, and the +0.083 at 1/16 is most likely a
  tail the sample did not meet, not a property of gump. The lead's independent rebuild confirms the chain and
  the sampler and reaches the same reading. The sampler never moves the initial state, and that is what stops it
  at 108 cells; it does not reach the 135-cell face. The extrapolations stand at 29.20 to 29.22 ± 0.03, against
  29.230 and 29.163.
- **Noise under a face lengthens its life, and only the near layers matter** (63 cells, coins at rate 1/4 from
  depth d down): nothing at d = 6, +0.02 at 5, +0.05 at 4, +0.10 at 3, +0.30 at 2, +0.67 at 1 (in ln τ, each
  ± 0.012 to 0.016; one code, one seed a row). The lead's rebuild has the d = 6 null at 45, 63 and 84 cells.
- New small facts: thin strips and narrow tubes are cut across by firewalls before a face dies; a tetrahedron of
  gump has no steady state (its corners are shaved off); the 18-cell hull face lives 4.855 ± 0.015 and is too
  small to belong to the family.

## Second phase (after the usage reset at 11:00 UTC): additions, newest last

*(The night's report follows unchanged below. What is added here is dated; forecasts for this phase are block 5
of `PREDICTIONS.md`.)*

**11:18 UTC. The card's own recorder sees the over-full generation on gump itself, at the same level, and none on
hull faces [measured by the GTX 1080 session's study, `research/dying2/` on `claude/gpu-local-1080`; read by the PI
after a forecast, block 5b, both parts held].** That study (another code, another machine, 2,500–8,000 natural
deaths per face) tabulates the dying face's population by lag before death. It reports means and medians and does
not mention an over-full face; its quantiles show it. Four generations before death the 90th percentile of the
dying face's population is 1.44, 1.43, 1.43, 1.39 of the living mean on the 63-cell torus, the 84-cell torus and
the 84- and 96-cell tubes, where the living 90th percentile is 1.15–1.20 and the dying median is 0.18–0.34. In
cells that is 47.0 of 63, 62.0 of 84, 62.0 of 84, 69.0 of 96: **0.746, 0.738, 0.738, 0.719 of the face, the launch
level of item 1 below (0.738)**. On the hull faces of 63 and 84 cells the dying face's 95th percentile never
exceeds the living one at any lag from 1 to 12 (1.25 and 1.23 of the mean at most). Reproduce:
`git show origin/claude/gpu-local-1080:research/dying2/data/2_4_14_lags.csv` (columns lag, mean, quantiles; likewise
`1_4_21`, `1_12_28`, `1_17_32`) and `…/research/dying2/hull/data/R13_death_timecourse.csv`. Not checked: nothing
was recomputed from that study's records, which are on the owner's machine. The same study finds that once k
cells are left the chance of death does not depend on the face (0.85, 0.63, 0.42 at k = 1, 2, 3 on four wrapped
faces; 0.77, 0.50, 0.30 on hull faces of 63 and 84 cells), so on gump too the lifetimes differ in how often a face
gets down to a few cells and not in what happens there.

### 12:28 UTC. The price of a hole is not the price of a face (`holes/`; a referee is at work on it)

The PI's idea was that the lifetime price is the cost of emptiness in the living state: −ln P(a region of a living
face is empty at an instant) = c·(cells) + (edge terms), with c = 0.2087, so that the hull's 0.231 could be looked
for in the living state of a large hull face. Forecast frozen first (`PREDICTIONS.md`, block 5). It failed.

- **[measured] A hole costs about 0.26 per cell.** On a 12 × 12 × 8 torus, mixed second differences of −ln P over
  rhombi of a × b unit cells (free of anything that depends on a alone or b alone) are 0.254 to 0.265 per cell
  wherever the short side is 2.5 unit cells or more, flat, from 6.3·10⁹ replica-generations. The smallest follows
  from the table that was already on file: (12.128 − 2·8.793 + 6.254)/3 = 0.265. Closed tori of the same shapes,
  same stepper, give 0.215 ± 0.003 at (3.5, 3.5). Reproduce: `python3 research/blast/holes/ana.py torus
  research/blast/holes/data/slab12_s101.txt`. Not reached: any hole wider than 4 unit cells, so "a wide hole comes
  back to 0.2087" is not excluded; an emptied patch is retaken from its edge at a quarter of a unit per generation.
- **[measured] The interior of a hull face is a wrapped face.** In a hull of radius 29 (360-cell faces), patches of
  12 to 27 cells two or more rows from every rim have the torus's −ln P within 0.002; one row in, a 27-cell patch
  is 0.010 dearer. (`sh research/blast/holes/finalize.sh`.)
- **[measured] The living state has no rim surplus.** A patch on the rim is likelier to be empty (27 cells: by
  0.98 in the logarithm on a rim, 3.21 in a corner), and further rows against the rim cost what the torus's cost.
  The 0.022 per cell between the two lifetime prices is not in the living state's cost of emptiness.
- **[measured] A patch empties by a boom and bust of its own, deeper than a dying face's.** 71% of the emptyings
  of a 27-cell interior patch contain a one-generation fall of half its cells, launched from 0.805 full (a dying
  wrapped face: 0.738) with the layer beneath at 0.67. In corners 23%: corners fade.
- **[measured] A new anchor: the 18-cell hull face, ln τ = 4.855 ± 0.015.** The hull's second differences per cell
  are then 0.355, 0.266, 0.231, 0.230 at sides 4 to 7.

What it changes. (1) [conjectured, the PI's argument] The two prices cannot both be asymptotic. A hull face's
interior is a wrapped face, so a large hull face can die the wrapped way inside while a rim zone of fixed width
dies in step, at a cost proportional to the rim: ln τ_hull ≤ 0.2087·A + (a term linear in the side) for large
faces. The hull's 0.231 is therefore the price of faces that are all rim zone, and the open question is where it
comes down, not whether. (2) The agent's "rows formula" (a price per cell by depth in rows from the nearest rim)
makes the triangle's second difference 3·c_⌊k/3⌋, the same for three consecutive sides. If that reading is right
from side 6 up, **the 135-cell face repeats 0.231 by construction (29.230) whatever deeper rows cost, and cannot
decide the question it was meant to decide; the 165-cell face is the first that can** (35.746 if rows three deep
cost 0.2087, 35.812 if 0.231). The 18-cell face breaks the rows formula at sides 4 and 5, where the corners
overlap. The rival reading puts the surplus in the corners. Triangles cannot separate the two.
**Correction, 12:32 UTC:** when I wrote the sentence above and block 6 of the forecasts I had forgotten that `rim/`
timed exactly such faces last night (strips on a periodic prism, no corners; "What was found", item 6), and that
its numbers already speak against both readings. At a loop of 3 units a row costs the same whether it is the
third, fourth or fifth from a rim (1.525, 1.558, 1.557 per row of 9 cells), so there is no price by depth; and a
strip of 48 to 75 cells shows the hull's excess with no corner anywhere, so corners are not needed. What a strip
has instead is two prices that depend on its loop L: added width costs 0.172, 0.196, 0.2017 per cell at L = 3, 4,
5 (rising), added length 0.2455, 0.2308, 0.2177 at L 3→4, 4→5, 5→6 (falling). They can only meet between 0.202
and 0.218, and the wrapped 0.2087 is inside that; 0.231 is passed on the way down. Block 6 is therefore not blind
and item 1 is withdrawn. The new agent (`strips/`) is now asked to check `rim/`'s table with its own code and to
extend it one step in each direction (4 unit rows at L = 7, 5 unit rows at L = 6), with closed tubes of the same
girth as the control.
**Referee (12:43 UTC; `ref-hull/HOLES.md`, own code, `holes`' code not opened): no number broken, two readings
corrected.**
- The torus values are confirmed (five patch sizes within 1.8 errors; mixed differences 0.2637 ± 0.0005 and
  0.2586 ± 0.0014 against 0.2646 and 0.2595; the errors are honest by seed scatter). **But −ln P is not bulk +
  perimeter + corner at these sizes** (its pure second differences in one side are −0.018, −0.071, −0.103 at
  2, 3, 4 units, where that form gives zero), so the mixed difference is the cost of one more row on a strip 2 to
  4 units wide, not a bulk cost. What stands: at no size reached does a hole cost the lifetime price. What does
  not: "wide holes cost 0.26". The PI's hypothesis is unsupported, not refuted for wide holes.
- Hull interior, rim and corner patches: confirmed at radius 21 (interior minus torus +0.0004 ± 0.0003 and
  +0.0009 ± 0.0010; rim −0.985, corner −3.207).
- The 18-cell face: 4.8526 ± 0.0016 and 4.8570 ± 0.0013 from soups of 0.35 and 0.50, plateau confirmed. But 14.5%
  of its first deaths empty two or more faces at once (2.5% at 30 cells, 0.2% at 45) and the hull lives 16
  generations, about its relaxation time: counted per emptied face it is 4.693, and the rows formula's miss
  falls from 0.27 to 0.10. It is doubtful as a member of the family; fits that lean on it (the agent's price of
  0.223) lean on that.
- The two narrow-torus lifetimes that disagreed with the table on file are a difference of definition: the table
  sets aside face deaths that follow a transverse firewall (65% of deaths on the 2 × 8 torus, 13% on 3 × 6); the
  referee reproduces both ways of counting (9.472 ± 0.007 against the table's 9.4888; 8.464 against `holes`' 8.450).
  `holes`' "a hole is dearer than a closed torus by 0.044 at (3.5, 3.5)" stands (firewall shares 3% or less there);
  its entries for tori two units wide and for 3 × 6 do not.
- The bust statistics on the torus are confirmed to three digits.
Not checked by the referee: the fits, the reading of the extra 0.05, triangles and strips, the radius-29 run.

### 13:21 UTC. The 120-cell tube: below every forecast, and the bend goes on

The card's final value for the loop-12 tube of 120 cells is **24.5086 ± 0.0169** (eight seeds, 3,494 face deaths,
no firewalls; another session's measurement, read from its branch: `git show
origin/claude/gpu-local-1080:research/gpu-local/README.md`, "Chain 3"). The night's forecasts were all high: the
PI's 24.56 ± 0.03, `tube1d/`'s 24.563 ± 0.030 (its three forms spanned 24.53 to 24.61), the dice chain's 24.60 ±
0.07, the card's own 24.576 ± 0.020. Scores in `PREDICTIONS.md`. The chords are 0.2023 ± 0.0004, 0.2013 ± 0.0008,
0.1957 ± 0.0016 per cell from 84 to 120 cells: the last step bends by 2.7 errors of the second difference.
- [measured, the card's] A tube's price is not a constant at any length reached, and `tube1d/`'s saturating form
  with an asymptote of 0.2004 per cell is refuted: the local slope is already below it.
- [conjectured] Two readings, with forecasts for the card's next tubes (126 and 132 cells) frozen in block 7: a
  slow bend with a low fluctuation at 120 cells, or a second way to die whose rate hardly falls with length (a
  local death that spreads along the tube) taking over. The second would make the tube's lifetime stop growing
  with its area, as the lead's open question (l) asks.
- [measured, `rim/`; the comparison is the PI's] A rimmed strip of loop L is a tube of girth L with two ends, and
  its rows cost 0.172, 0.196, 0.2017 per cell at L = 3, 4, 5 with no bend from 4 to 7 rows: less than closed tubes
  of the same girth pay at 54 to 108 cells (0.2072 falling to 0.2057 at loop² 16). If a row's price belongs to the
  girth alone, closed tubes should bend down towards the strip's values (about 0.185 at loop² 12). Not tested;
  `strips/` is measuring closed tubes and strips with one code.
Not checked: nothing of the card's was recomputed here.

### 14:00 UTC. Corner-free strips, checked and extended: no row of a rimmed face costs more than a wrapped row (`strips/`; unrefereed, but itself an independent check of `rim/`)

`strips/` rebuilt `rim/`'s prism with its own code (oracle-exact on ten vessels; octahedron anchors 6.8046 ±
0.0018 and 9.8219 ± 0.0018) and took the table one step further each way. Reproduce every number:
`sh research/blast/strips/collect.sh`.

- **[measured] `rim/`'s nine lifetimes stand** (all within 0.02 but one at +0.038 ± 0.022; χ² 19 on 9). One number
  derived from them does not: the mixed second difference at 4→5 rows, L 4→5 is 0.2486 ± 0.0043, not 0.2262 ±
  0.0078 (the two pooled: 0.2436 ± 0.0037). The night's sentence "0.6 errors from the hull's 0.2307" is withdrawn;
  it is above it.
- **[measured] Thin strips are cut across by firewalls before a face dies**, and that, not the faces, bends their
  lifetimes: 4 rows: 0.2%, 3%, 33% of lives at L = 5, 6, 7; 3 rows: 86% at L = 6. With those lives set aside (the
  lead's booking) the 3-row strip's face lifetime keeps growing where all first deaths saturate at 10.2.
- **[measured] The two new points.** (4 rows, L = 7): 19.111 ± 0.024 with no firewall before (18.716 ± 0.020 by all
  first deaths). (5 rows, L = 6): 20.300 ± 0.022. The price of added length for 4 rows is 0.2450, 0.2301, 0.2210,
  0.2177 ± 0.0021 per cell at L 3→4 … 6→7: flattening near 0.217. The price of added width (4→5 rows) is 0.1702,
  0.1945, 0.2052, 0.2112 ± 0.0013 at L = 3 … 6: still rising, and past 0.2087.
- **[measured] A row of a rimmed strip costs no more than a row of a closed tube of the same girth**: strip minus
  tube, per cell, −0.03, −0.013 ± 0.001, −0.003 ± 0.001, +0.001 ± 0.003 at girth 3, 4, 5, 6. And a row costs the
  same two rows deep and three rows deep (0.1702 against 0.1716; 0.1945 against 0.1947 at L = 3, 4). **No row
  carries a surplus of 0.02.**
- **[proved, algebra] The hull's kind of number is a marginal price.** If ln τ = a(L) + w·3L·p(L), the mixed
  second difference is (L+1)·p(L+1) − L·p(L): the price of the cells added at the margin, above the average row
  price p for as long as p is still rising with size. In a strip a marginal price of 0.24 goes with an average
  row price of 0.21 [measured]; closed faces show the same at girth 4 (0.2276 against 0.2070).
- **[measured, 2.4 errors] A caution of the size of the effect:** the 4-row strip is already thin at L = 5 (from 5
  to 6 rows the row price is 0.1994 ± 0.0023, not 0.2052), so the last width price and mixed difference are
  inflated by an unknown part.
- **[measured; cause from T2] A tetrahedron of gump has no steady state.** Its corners are shaved by the four
  opposite diagonal families (3.3 layers gone by generation 50, 8.0 by 12,800; the octahedron loses none) and its
  faces' hazard climbs with age. There is no tetrahedral face law to compare with.

What it means for the two prices [conjectured]. Three independent lines now say that 0.231 is not a second
asymptotic price: a hull face's interior is a wrapped face in the living state (`holes/`, refereed); no row of a
corner-free rimmed face costs more than a wrapped row (`rim/`, `strips/`); and a second difference is a marginal
price, which sits above the average while the average is still climbing, on closed faces too. What none of them
gives is the size at which the hull's marginal price comes down. The agents' forecasts for the 135-cell face
from this side are 29.20 ± 0.03 (`strips/`), 29.21 ± 0.03 (`holes/`), against 29.230 for "the second difference
repeats"; they are extrapolations and do not decide it. Not checked: second seeds for most long runs; the
thickness of the 4-row strip at L of 6 and more; nobody has rewritten `strips/`' stepper.

### 14:57 UTC. The noisy hull: a sampler with all eight faces real; its blind test at 108 cells is not clean (`noisy/`; unrefereed)

The chain: gump's rule on every cell of the hull, all eight faces real; after each generation the cells 6 or
more layers under the watched face and 3 or more under every other face are hit by darts that set a cell to a
fair coin, at a rate ε per cell and generation. ε = 0 is gump. The sampler is the night's subset simulation, over
the darts; it is exact for the chain at any ε > 0 [proved, standard]. The aim was to extrapolate in ε at the
target size and not in size.
- [measured] At zero noise the stepper is gump bit for bit (`python3 research/blast/noisy/validate.py 1200`), and
  brute force of the chain shows **no offset from gump at 45 and 63 cells at any ε up to 0.3** (63 cells: weighted
  mean +0.003 ± 0.004). The sampler against brute force at 63 cells: −0.024 ± 0.023, +0.019 ± 0.018, +0.003 ±
  0.018 at ε = 1/64, 1/16, 1/4. At 84 cells, ε = 1/16: 18.173 ± 0.029, which is +0.032 ± 0.029 above gump.
- [measured, interim] **108 cells, blind (gump: 23.3392 ± 0.0099).** With about a third of the planned
  replications: 23.433 ± 0.052 at ε = 1/16 (96 replications), 23.49 ± 0.09 at 1/32 (19), 23.39 ± 0.09 at 1/64
  (about 150, scatter 1.0 per replication). Weighted mean **+0.093 ± 0.044 above gump**; the line's intercept at
  ε = 0 is +0.05 ± 0.13. Reproduce: `python3 research/blast/noisy/fit.py` on the rows in
  `research/blast/noisy/data/runs/`.
- What that says: the offset from gump grows with the face (+0.008 ± 0.009, +0.032 ± 0.029, +0.09 ± 0.04 at 63, 84,
  108 cells) as the night's dice chain's did, and at small ε, where the chain is nearest to gump, the sampler's
  replications scatter too much to extrapolate. **The method does not reach the 135-cell face** better than the
  night's surrogate did (29.26 ± 0.06 to 29.34), and the 135-cell runs were not started.
- A fact about the machine: the planned runs were cut at 14:07 UTC because this container is stopped whenever
  the session has no turn, agent or tracked job in flight, and detached processes die with it. The rest of the
  108-cell runs were restarted at 14:57 UTC as a tracked job (`sh research/blast/noisy/pi_resume_B.sh`, four
  cores, 105 minutes); the final numbers are appended below when it ends.
Not checked: no referee has rewritten the chain or the sampler (the window had no room for one); whether the
offset at 108 cells is the chain's or the sampler's (the script `prod_A_brute84.sh`, 10 core-hours, would say at
84 cells); other noise regions.

**Final numbers of the blind test at 108 cells, 16:39 UTC** (the tracked job ended; all planned replications in;
about 10 core-hours in all). [measured] Gump: 23.3392 ± 0.0099.

| ε | replications | ln τ | minus gump | scatter of one replication | largest share of the rate |
|---|---|---|---|---|---|
| 1/16 | 440 | 23.422 ± 0.025 | +0.083 ± 0.027 | 0.52 | 0.015 |
| 1/32 | 300 | 23.228 ± 0.119 | −0.111 ± 0.119 | 2.06 | 0.115 |
| 1/64 | 360 | 23.368 ± 0.065 | +0.029 ± 0.066 | 1.23 | 0.056 |

- Weighted mean over the three: 23.408 ± 0.023, which is **+0.069 ± 0.025 above gump** (2.8 errors; χ² 3.0 on 2).
  **Corrected 20:52 UTC, after the lead's rebuild: this is not a fair summary.** Its weights are 0.15 : 0.04 : 1
  (ε = 1/64 : 1/32 : 1/16): a sample that meets a large replication gets a lower ln τ and a larger error at once,
  hence no weight. With all 1,100 replications weighted equally the value is 23.349 ± 0.043, **+0.009 ± 0.044
  from gump** (`fit.py` now prints both). The line in ε and its intercept below rest on the same errors and are
  withdrawn: the rebuild's bootstrap interval for the intercept is [−0.20, +0.15].
- A line in ε: intercept at ε = 0 **23.314 ± 0.082, which is −0.025 ± 0.083 from gump**; slope +1.7 ± 1.4 per unit
  of ε (χ² 1.6 on 1).
- Reproduce: `python3 research/blast/noisy/fit.py` (rows in `research/blast/noisy/data/runs/`; the runs are
  `sh research/blast/noisy/prod_B_108.sh` as far as it got, then `sh research/blast/noisy/pi_resume_B.sh`).

What the final numbers change, and what they do not. At ε = 1/16 the chain reads above gump by three of its
errors at 108 cells, where it read +0.032 ± 0.029 at 84 cells and nothing at 63: that offset is real for this
chain or for its sampler, and it grows with the face. The extrapolation to zero noise agrees with gump, but only
to ± 0.08, and the two readings of the 135-cell face are 0.067 apart; the slope it rests on is 1.2 errors from
zero. So the interim verdict stands: **the method, as tuned, does not decide the 135-cell face**, and the
135-cell runs were not started. Not checked, beyond the list above: the error bars at ε = 1/32 and 1/64 are not
to be read as Gaussian (at 1/32 the value moved from 23.386 at 200 replications to 23.228 at 300, and one
replication carries 11% of the summed rate); no second set of seeds; no referee.

### 16:40 UTC. The outside audit of the night's report (`research/audit/REVIEW-blast.md`, on `main`; the lead's, not this session's)

The pull request was merged at 14:17 UTC after an audit that rebuilt the night's main claims from the oracle with
its own code (`research/audit/blast/`; 234,823 deaths of a 63-cell wrapped face, 281,631 of a 63-cell hull face,
a wide face and a tube at 84 cells). Read by the PI at 16:40 UTC; nothing below is recomputed here.
- [measured by the audit] **Confirmed:** boom and bust on wrapped faces at 63 and 84 cells (launch at 0.7376·A
  against this report's 0.738; fall 48.79 → 11.24 against 48.83 → 11.18); the fade on the hull face; the cause
  given for it, now cell by cell (in an over-full generation the hull's interior cells survive as rarely as a
  wrapped face's, 0.34 and 0.33, and its rim row twice as often, 0.66); the exactly solved surrogate to every
  digit recomputed; the tilt identity.
- **Three statements of this report it qualifies, and the report now carries the qualification:**
  1. "No hole, no front, no band" holds for the crash (the two halves of the face fall in the same generation in
     88% of deaths at 63 cells, 92% at 84) and is too strong for what follows it: the cells' last-alive times are
     patterned in space in about half the deaths. `anatomy/`'s own table had a plane beating shuffles in 32.5% of
     deaths against 11.9% on a living face, and the report passed over it. The short version is reworded.
  2. "About one bust in 130 kills" is the 63-cell number; at 84 cells it is one in 1,100. Item 1 below should be
     read with that.
  3. "The same number of survivors is deadlier after a bust" (0.334 against 0.236): the direction is confirmed,
     the size is smaller under the audit's definition (0.311 against 0.260).
- **What the audit says is not a result**, and this report agrees: the tube's asymptote 0.2004 and its K = 2 curve
  and 0.0046·L² (refuted at 120 cells, the 13:21 entry above); the 192-cell and staggered-crash statements, which
  rest on a surrogate that is 0.12 ± 0.05 off at 120 cells; "0.079 + 0.136" as parts of the price; the
  living-state estimator beyond 108 cells; the 135-cell forecasts.
- New from the audit: the chance that a face with k cells left dies is lower on the hull than on a wrapped face
  under one definition (0.77, 0.50, 0.30 against 0.86, 0.64, 0.44 at k = 1, 2, 3), and neither the bust nor the
  shared rim row accounts for it. That was "unreconciled" in this report; it is a fact with no explanation.
- Not checked by the audit (its section 9): anything above 84 cells on gump; `rim/`, `split-hull/`, `ref-hull/`,
  the dice chains and their samplers; and the whole of the second phase above, which it predates.

### 18:07 UTC. Gump in Lean: the first theorems are machine-checked (`lean/`; unrefereed)

On the owner's word of about 17:50 UTC ("go ahead and install lean, and start work in its direction"). Lean 4.36.0.
- [proved, machine-checked] In core Lean, no Mathlib: the lattice and the rule; **T1** (layer histogram); "a dead
  sealed set stays dead whatever happens elsewhere" and "unions of sealed sets are sealed" (the opening of **T6**);
  **T2** (octahedral confinement) and the diagonal hull; **T3** (firewall), both halves; **T4** (closed slabs). No
  `sorry`; axioms `propext`, `Classical.choice`, `Quot.sound` only. T2 and T3 are two instances of the sealed-set
  lemma. Reproduce: `sh research/blast/lean/check.sh`.
- [measured] The Lean rule is gump: run by a stepper that evaluates the verified `step`, it prints the four 2012
  closed-cube logs in `reference/golden/` line for line (side 11 through its 4,218 generations, with `--long`) and
  equals `reference/oracle.py` state for state on three soups for 60 generations; a corrupted state is caught.
- The aim and the climb are in `lean/README.md`: every theorem of the project checked, and the measured laws
  turned into theorems, the face law with its constant included.
Not checked: no second agent has read the Lean statements against `docs/AUTOMATON.md`; that the stepper misses no
birth is argued, not yet proved in Lean.

### 19:37 UTC. The noisy hull's sampler under the review's questions: the tail, the families, the odd sweeps (`noisy/`; the lead's rebuild is still to report)

Asked by the lead on pull request 39. Rows: `research/blast/noisy/data/runs_diag/` (from `sh research/blast/noisy/diag.sh`).
- [measured] **The law of one replication has a rare heavy tail at 108 cells** (`python3 research/blast/noisy/tails.py`).
  At 63 and 84 cells the largest replication is 1.4 to 2.5 times the mean; at 108 cells 20, 35 and 7 times at
  ε = 1/64, 1/32, 1/16, with the median at 0.80, 0.73, 0.90 of the mean. An unbiased estimate with such a law reads
  high in ln τ in most samples; its error bar from the scatter knows nothing of the part of the tail it has not
  caught. One replication of 35 times the mean among the 440 at ε = 1/16 would move that value by −0.077.
- [measured] **Ancestry** (`python3 research/blast/noisy/anc.py research/blast/noisy/data/runs_diag`; `nz.c` now
  prints it, with no change to its random numbers). The dying chains of one replication descend from a median of
  47, 54 and 56 distinct initial states at ε = 1/64, 1/32, 1/16 (30 replications each; 130 at 63 cells, 86 at 84),
  and the largest family holds 0.15 to 0.22 of them. So a typical replication is not one start reweighted. The
  tail is: in each set the replication with the largest rate has a largest family of 0.32 to 0.71.
- [measured] **Odd sweeps off** (every sweep proposes anywhere; 420 replications at 108 cells, ε = 1/16):
  **23.330 ± 0.043, which is −0.009 ± 0.044 from gump** and 0.092 ± 0.050 below the value with the odd sweeps on
  (23.422 ± 0.025; 1.8 combined errors). Its replications scatter more (0.88 of the mean against 0.52), its
  families are fewer (median 38), and 32 of its 420 replications have one family holding half or more of the dying
  chains; those 32 carry 0.21 of the summed rate. A fresh 30 replications with the odd sweeps on read 23.339 ± 0.075.
- What this says. Read as code, the odd sweeps leave the conditional law invariant (the window before the first
  minimum always holds the same number of bits, and a move is refused unless its reverse is proposable), so both
  forms estimate the same number without bias and differ by 1.8 errors. [conjectured] The +0.083 of the 14:57 entry
  is the sampler's, not gump's: either a tail not yet caught with the odd sweeps on, or a fault in them that the
  reading missed. Not decided. `diag2.sh` (running) repeats on against off at 84 cells, where the lead's rebuild
  will have the chain by brute force. **The sentence of the 14:57 entry "that offset is real for this chain or for
  its sampler, and it grows with the face" should be read with this: nothing here shows an offset of the chain.**
- What it means for the method: its variance at 108 cells is in the initial states, which the moves never touch.
  A sampler that also moves the initial state (an independence move among stationary snapshots, accepted iff the
  score stays under the level) is the next form to build; forecast in `noisy/PREDICTIONS.md`, block 3, item 5.
Not checked: the brute force of the chain at 84 cells (the rebuild's, and block 3's first two forecasts wait on
it); ancestry with the odd sweeps on beyond 30 replications per ε; no second code for the sampler.

### 20:52 UTC. The lead's rebuild of the noisy hull; on against off at 84 cells; how deep a face's death is decided (`noisy/`)

**The rebuild** (the lead's, read on pull request 39 and not recomputed here; `research/audit/REVIEW-blast-noisy.md`
and `research/audit/blastnoisy/` on its branch). The chain is confirmed from the README alone. Brute force of
the watched face minus gump: 45 cells −0.000 ± 0.003, +0.007 ± 0.004, +0.001 ± 0.003 at ε = 1/16, 1/4, 1; 63 cells
+0.015 ± 0.007, −0.011 ± 0.009, −0.004 ± 0.013; **84 cells +0.027 ± 0.038 at ε = 1/4**. The sampler is exact for
the mean rate at 45 and 63 cells against that brute force. At 108 cells the numbers reproduce to the digit and
the summary did not stand (the correction is written into the 14:57 entry above). Its reading of the +0.083: 65%
the sampler's tail, 20% the chain, 15% a fluctuation. About one replication in 280 has a rate above ten times
the median; those carry 8% of the summed rate; the ε = 1/16 sample met none.
- [measured] **On against off at 84 cells, ε = 1/16** (`sh research/blast/noisy/diag2.sh`; rows in
  `noisy/data/runs_diag/`; `python3 research/blast/noisy/ana.py research/blast/noisy/data/runs_diag`): odd sweeps
  on 18.171 ± 0.020 (250 replications), off 18.144 ± 0.019 (240); gump 18.141 ± 0.005. So on is +0.030 ± 0.021
  from gump, off +0.003 ± 0.020, and on minus off is +0.027 ± 0.028. With the 100 earlier replications, on is
  +0.031 ± 0.017. All within errors of each other and of the rebuild's brute force. Not closed: on sits above off
  at both sizes (1.0 and 1.8 errors) and above gump at 63, 84 and 108 cells. `diag3.sh` (running) brings on
  minus off at 84 cells to about ± 0.014.
- [measured] **The depth series** (63 cells, brute force, coins at rate ε = 1/4 at depth ≥ d under the watched
  face and ≥ 3 under the others; gump 13.633 ± 0.001; `noisy/data/depth.txt`, one seed and 12,000,000 generations
  a row, 3,750 to 7,400 deaths of the watched face):

  | d | 6 | 5 | 4 | 3 | 2 | 1 |
  |---|---|---|---|---|---|---|
  | ln τ of the watched face minus gump | −0.005 ± 0.012 | +0.019 ± 0.012 | +0.054 ± 0.012 | +0.101 ± 0.012 | +0.304 ± 0.014 | +0.674 ± 0.016 |
  | added by layer d alone | | +0.024 | +0.035 | +0.047 | +0.203 | +0.370 |

  Coins under a face lengthen its life, never shorten it. The two layers a face cell touches (T1: two
  neighbours one layer down, one neighbour two layers down) carry +0.37 and +0.20; each layer below adds about
  0.7 of the one above it (+0.047, +0.035, +0.024), and the sixth is at the noise. [conjectured] That is the same
  sign and size as the night's dice chain's offset (coins everywhere under six layers: +0.024 at 63 cells), and it
  says what a surrogate under a face must get right: the first two layers exactly, the next three approximately.
Not checked: the depth series has one code and one seed a row, and the region's size changes with d (57 to 132
cells); the 84-cell brute force at ε = 1/16 (block 3, item 1) has not been run by anyone; no second seeds.

### 22:16 UTC. The odd sweeps are cleared at 84 cells (`noisy/`)

[measured] `sh research/blast/noisy/diag3.sh` added about 800 replications each way at 84 cells and ε = 1/16
(rows in `noisy/data/runs_diag/`; `python3 research/blast/noisy/ana.py research/blast/noisy/data/runs_diag`).
Odd sweeps on: 18.142 ± 0.010 (1,050 replications; 18.145 ± 0.010 with the 100 committed earlier). Odd sweeps
off: 18.146 ± 0.009 (1,040). Gump: 18.141 ± 0.005. **On minus off: −0.001 ± 0.014.** Both forms agree with gump
to ± 0.011, where one replication's law has no long tail. So the +0.027 ± 0.028 of the entry above was a
fluctuation, the fault reading of the odd sweeps is closed, and the +0.083 at 108 cells is left with one
explanation: the tail of one replication's rate. It also says, through a sampler that is exact for the chain,
that the chain at 84 cells and ε = 1/16 is within 0.011 of gump (block 3's first forecast asked for this by brute
force, which nobody has run). Not checked: no second code for the sampler at 84 cells.

## What was found

1. **Boom and bust on wrapped faces [measured by four independent codes: `anatomy/`, `split-slab/`, `tube1d/`,
   `boom/`; refereed by `ref-anatomy/` and `ref-boom/`, which could not break it].**
   - The launch of a death (the last generation with at least half the face alive) has a population in one hump
     at 0.738·A at 48, 57, 63 and 75 cells (referee: 0.7380 ± 0.0002, 0.7386, 0.7375, 0.7381; its width grows like
     A^0.58); the living mean is 0.517·A. On the 63-cell torus the fall is 48.83 → 11.18, and 99.5% of the cells
     that die in it are overcrowded.
   - The face does not breathe: lag-1 and lag-2 autocorrelations of its population are +0.136 and −0.031. The
     over-full generation comes in one step from a normal face. One generation earlier nothing carries the price
     (a static cost of 0.005 per cell): the price is paid in one generation.
   - It is a breath of at least four layers: at the launch layers 1 to 4 hold 0.738, 0.637, 0.562, 0.504 of A
     (normally 0.517, 0.435, 0.406, 0.416), after layers 2 to 4 were slightly under-full one generation before
     (0.400, 0.354, 0.376: real but weak, 0.4–0.6 standard deviations per layer); one generation later 0.222,
     0.152, 0.190, 0.301. (`ref-anatomy/` saw a fifth layer over-full too.) A fatal fall takes the layer beneath
     the face from 39.9 to 9.9 of 63 where a non-fatal fall of half the face takes it to 18.6, so the face
     population is not a Markov state: the same number of survivors is deadlier after a bust (0.334 against 0.236
     from four cells).
   - The kill is a fragmentation: among the survivors of a bust, clusters of 1, 2, 3, 4–6, 7–12 cells fail to
     regrow the face 0.900, 0.634, 0.276, 0.078, 0.0051 of the time. (A different experiment gives a like number:
     one live cell left by hand on an otherwise emptied face over living chaos regrows it 0.138 ± 0.002 of the
     time.)
   - The earlier "57–59% of deaths contain a fall of half the face" was a threshold cutting one hump in two; 84%
     contain a fall of 0.4 of the face. There are not two classes of death on a wrapped face.
2. **The fade on hull faces [measured: `anatomy/`, `model/`, `boom/`, `ref-anatomy/`; the GTX 1080's own study of
   hull deaths on its branch agrees on the time course].** 1.1–1.6% of deaths of the 63-cell hull face contain a
   fall of half the face. Its return map has no cliff: one generation after 48 or more cells a wrapped face is at
   20.2 and a hull face at 29.9. Falls of half the face are 68 times rarer on the hull and, when they happen, as
   deadly. A plane fitted to the last-alive times beats 95% of shuffles in 77% of hull deaths, at 0.6 lattice units
   per generation (this fit and the next number were not refereed); the last cell is on the rim line 54% of the
   time, which is only 1.10 times the rim line's share of live cells. Neighbours inside the vessel, by enumeration:
   interior 9, rim row 7, corner 4 (`python3 research/blast/rim/budget.py`).
3. **The two exits are in the rule, not in the chaos [exact, `rigour/`; refereed: `ref-proofs/` recomputed the
   shares to every digit with its own code].** The one-layer dice surrogate (the face layer on gump's rule, every
   cell drawing private coins for the three cells beneath it) was solved exactly on 25 small faces. The share of
   its death flux through a half-face fall is 0.94, 0.57–0.79, 0.82 on wrapped faces of 9, 12, 15 cells and 0.017,
   0.020, 0.003 on rimmed ones of 9, 12, 18. The referee's rider: a tube one unit cell round falls to 0.21 at 15
   cells, so what matters is whether the cells can be overcrowded, not whether the face is wrapped.
4. **The price of a wrapped face: a split and a static part, not a formula [measured, `boom/`, `model/`;
   refereed by `ref-boom/`].**
   - The rate is exactly a sum over launches, 1/τ = Σ_p ν(p)·d(p): ν the frequency of a generation with face
     population p in the living state, d the chance that it is the launch of a death. At the launch point the two
     slopes in the area are **0.079 for the over-full face and 0.136 ± 0.001 for the rest** (0.147 ± 0.006 between
     63 and 75 cells). `boom` reported their sum, 0.2099, against the measured 0.2087 as if it were a test. The
     referee showed it is not: the sum rule is an identity, so the sum at the hump returns the lifetime slope of
     the very runs used (0.2154 ± 0.0011 from 48 and 63 cells, whose lifetimes have slope 0.2156).
   - The first part is a property of the living state alone: −ln P(population = xA) = 1.9 + ψ(x)·A with ψ = 0.056,
     0.075, 0.098, 0.127 at x = 0.70, 0.73, 0.76, 0.79, from the card's histograms of 16 faces of 54–120 cells; 1.27
     times a Gaussian's; identical on loop-12 tubes and wide faces to 0.001 per cell (`model/`, unrefereed except
     for one row).
   - **Three quarters of the price is static [measured, `ref-boom/STATIC.md`; not refereed].** By plain running on
     tori of 48–108 cells: the living state's frequency of "all four layers at or above the launch profile" falls
     as e^(−0.166 ± 0.003 per cell), and given that state the chance of death is 0.273, 0.162, 0.117, 0.061 at 48,
     57, 63, 75 cells, i.e. e^(−0.057 ± 0.003 per cell). Tightening the state raises the chance of death towards 1
     (0.85 at 48 cells), but the state of near-certain death costs 0.23–0.25 per cell, more than the price: the
     face launches from a shallower state and takes its chance on the kill. Out of sample, with the kill law fitted
     on 48–63 cells and only living-state frequencies at the target size: 15.53 ± 0.16, 17.33 ± 0.10, 22.13 ± 0.11
     at 75, 84, 108 cells against 15.64, 17.54, 22.54; low, and lower with size.
   - **A wide face's lifetime read from its living state, with a fitted kill law [measured, `ref-boom/STATIC.md`,
     second half; not refereed].** No static event whose rarity is the whole price was found: for "at least 0.70
     full now and at most 0.20 full next generation" (a function of the present state) the static rate is 0.150 per
     cell and death given it still falls as e^(−0.068 per cell); a deeper crash costs more than the price. Death is
     decided when about four cells are left (given 2, 4, 6, 8 cells two generations after an over-full face the
     chance of death is 0.81, 0.48, 0.24, 0.11 at every size). What does work is cruder: **ln τ(A) = −ln ν_A(face
     ≥ 0.74·A) + 0.1273·A − 1.37**, the two numbers fitted on 48, 57, 63 cells and the frequency ν measured in the
     living state at the target size, gives 15.676 ± 0.037, 17.568 ± 0.050, 22.575 ± 0.086 at 75, 84, 108 cells
     against 15.6442, 17.5387, 22.5405 (the 108-cell run contained no death). So over wide faces the kill costs a
     fixed 0.127 per cell and the bend of the price with size (0.2158 below 63 cells, 0.2087 above) is all in how
     often the living face is over-full. On the 84-cell tube the same formula returns the wide value, 0.23 too
     high: a tube's face is over-full exactly as often, and its whole discount is in the kill.
     **Applied beyond the reach of deaths (the last run of the night, 07:00 UTC):** on wide tori of 126, 144 and 192
     cells the estimator gives 26.324 ± 0.113, 30.055 ± 0.139, 40.030 ± 0.242 (with the kill law refitted on 1.1
     million deaths: 26.329 ± 0.042, 30.062 ± 0.051, 40.043 ± 0.142), where the wide-face line 13.1623 + 0.20861·(A −
     63) gives 26.305, 30.060, 40.073 and the card's 126-cell face on file is 26.4045 ± 0.1043. A threshold
     systematic of about ± 0.1 at 192 cells is not in those errors. **If the kill law holds beyond the 108 cells
     to which it was checked, a wide face still pays 0.2087 per cell at 192 cells: neither bending nor rising.**
     The dice-chain sampler's 40.49 ± 0.20 for the same face is 1.8 errors above this.
   - **A measured two-layer map finds the wrapped route and falls 23% short of its price; it does not give the
     hull's [computed, `ref-anatomy/THEORY.md`, `boom/`; refereed by `ref-map/`].** Let a face be a Markov chain
     on (face population, population of the layer beneath) with the drift and covariance measured in living gump
     and Gaussian noise. With nothing fitted its cheapest way to an empty wrapped face is one jump up and a crash,
     (33, 25) → (45, 43) → (16, 6), where gump's dying faces go (33.3, 25.2) → (48.6, 39.7) → (12.1, 9.9); its action
     is 0.1606 per cell at 63 cells (three codes: 0.160–0.165) against 0.2087. The shortfall is mostly the
     non-Gaussian tail of the single jump (+0.80 ± 0.03 nats at 63 cells, about +0.025 per cell); with it and
     smaller corrections added linearly the author gets 0.200–0.207 [conjectured: a ledger]. For the hull the same
     chain gave 0.2313 per cell at 63 cells, the rimmed price to three digits, and the referee refuted it as a
     price: it is the action at one size divided by the area (0.209, 0.226, 0.232 at 30, 45, 63 cells), its
     increments per cell are 0.2605, 0.2477 where gump's are 0.2010, 0.2119, and its route depends on what is called
     "the layer beneath". One map does not hold two prices.
5. **Tubes [measured; unrefereed except the sampler; the reading in the last bullet is conjecture].**
   - "1.85" and "3.0" are two slopes of one curve: against the wide-face line the discount of a loop²-12 tube is
     0.0046·L² from 54 to 108 cells (L the tube's length in lattice units).
   - A tube's living state does not depend on its length; at 54–84 cells a tube's face is over-full exactly as
     often as a wide face's of its area and its crash leaves the same survivors; **the discount is in the chance
     of death given the launch** (`boom/`, `model/`). At 72 cells a more frequent four-layer launch state accounts
     for 0.076 ± 0.011 of the tube's 0.164.
   - **A band of a living tube and a whole tube are the same object** (`tube1d/`): the probability that a band of
     width w right round the girth of a long living tube is momentarily empty, times the lifetime of a closed tube
     of length w, is e^(−3.855 ± 0.022), e^(−3.893 ± 0.053), e^(−3.98 ± 0.20) at w = 5, 6, 7 units (loop² 13: the same
     curve, constant 4.06 ± 0.05). The price of one more unit falls with the length already emptied on one curve
     for both: 0.236 per cell at 2 units, 0.219 at 4, 0.206 at 6, 0.2013 at 9. Fitted jointly: ln τ(L) = a + sL −
     ln(1 + K·e^(−L/ξ)) with c∞ = 0.2004 per cell and ξ = 1.95 lattice units at K = 2 (χ² 3.4 on 9; K = 3 fits as
     well, 3.2; K = 1 does not, 11.1). A power of the length in front (τ ∝ L^0.75·e^(0.194·cells)) fits the tubes
     alone.
   - **Beyond brute force, on a surrogate** (`split-slab/`: six layers of the true rule over two layers of coins,
     sampled by subset simulation over the coins; refereed by `ref-slab/`: surrogate and sampler confirmed, exact to
     0.02–0.03 where truth is cheap; whether its 96- and 108-cell calibrations were really blind was not audited).
     **The 120-cell tube: 24.60 ± 0.07** (the referee's pooled value for gump, nine runs, χ² 2.8 on 8). At 192
     cells, the agent's final values for gump with the errors it would defend: **tube 38.85 ± 0.12, wide torus
     40.49 ± 0.20**, wide minus tube 1.65 ± 0.2. The wide-face line gives 40.07: the surrogate is 0.42 above it, two
     of its errors and inside the possible drift of the surrogate's offset beyond 108 cells (the referee's own
     pooling: 40.25 ± 0.26, "above the line not established"). So 0.2087 at 192 cells is neither confirmed nor
     refuted. The tube against `tube1d`'s forecasts (39.17, 39.01, 38.92, 38.86 for K = 1, 2, 3 and the power law):
     K = 1 is disfavoured at 2.7 errors, the others are not separated. The errors at 192 cells are limited by a
     heavy tail: the dying chains of one replication descend from few initial states, and one replication can
     carry a quarter to a half of the summed rate.
   - **A long tube does not stop busting; it stops busting all at once [measured on the surrogate's deaths, with
     gump's natural deaths at 63 and 84 cells matching it row for row; `split-slab/` §9; unrefereed].** The share
     of deaths with a face-wide fall of half the face stays 0.54–0.70 on wide tori to 192 cells and falls on
     loop-12 tubes (about 0.50, 0.50, 0.42–0.45, 0.26, 0.15–0.17 at 84, 108, 120, 144, 192 cells; the last two good
     to ± 0.1). Cut into sections two units long, every section of a dying tube still goes from 0.69–0.73 full to
     0.22 in one generation at every length, and at least one section busts in 95–98% of deaths. What changes is
     the timing: the two halves of a tube crash in different generations in 0.17, 0.21, 0.26, 0.29, 0.65 of deaths
     at 84 … 192 cells; the two halves of a wide torus in 0.03 at 108 and at 192 cells. A wide face is rigid in
     time, a tube is not.
   - [conjectured, the PI; forecast frozen before the measurement, block 3] Each freedom of timing multiplies the
     rate, which is the discount; a boundary between sections that crash at different times costs per unit of its
     length, which is why the discount needs a short girth and ends near loop² 21. Tested the same hour (block 4;
     `split-slab/` §10): if timings formed a simple chain, −ln P(neighbouring sections crash together) per cell
     would be the discount. On the 192-cell tube it is 0.0136 ± 0.0021, 0.0129, 0.0135 for sections of 2, 3, 4 units
     (constant in the section length, as a chain requires), 1.4–1.6 times the measured discount of 0.008–0.010; the
     number is soft (0.008–0.011 with a stricter definition of a crash, 0.019–0.032 with a looser one), and no
     one-parameter chain fits both it and the decay of the timing correlation. On the wide 192-cell torus
     neighbouring quarters crash together in 0.998 of deaths: no discount. **The order of magnitude, not the
     number.**
   - Loop² 16 is a different problem at length: a cut right through the slab neither heals nor spreads, and a
     168-cell tube lives only ln τ = 17.42 ± 0.17 (`tube1d/`). The lifetime saturates.
6. **Rims [measured, `rim/` (unrefereed) and `split-hull/` (dip rates refereed by `ref-hull/`)].**
   - Corner-free strips (prisms bounded by two diagonal families, periodic along their common direction) show an
     excess over the wrapped price with no corner anywhere: their mixed second difference in width and length is
     0.274, 0.259 and 0.2262 ± 0.0078 per cell in three determinations (the last, at the largest sizes, is 0.6
     errors from the hull's 0.2307 and 2.2 from 0.2087). So the excess is not made by corners. But a strip has no
     single price: a cell of added width costs 0.2017 ± 0.0015, a cell of added length 0.2455, 0.2308, 0.2177 as
     the strip grows from 3 to 6 units; its bust share is 0.15–0.20.
   - **Where the hull's rim term lives.** With ν(p) the rate of dips to p times the usual population (plain
     running, radius 7 to 21) and q = 1/(τν): −ln q(0.6) is a straight line in the area with no rim term over 45,
     63, 84, 108 cells, −2.049 + 0.17014·A (χ² 1.1 on 2). About nine tenths of the lifetime's rim term is in how
     often the face dips to 0.6 of its population; from there to empty a hull face pays 0.170 per cell.
   - **Where the 0.022 between rimmed and wrapped faces sits in that decomposition [measured, `ref-hull/WRAPPED.md`;
     one code; lifetimes taken from the anchors].** On wide tori of 63, 84, 108 cells −ln q(0.6) rises 0.157 per
     cell (0.158, then 0.156) against the hull's 0.170; the stretch from 0.6 to 0.4 of the population costs 0.051
     per cell on both, so 0.013 of the difference sits below 0.4 of the population, and the other 0.008 in the
     hull's dip term. A wrapped face dips LESS often than a hull face of its area (by 0.26, 0.37, 0.53 in ln ν at
     63, 84, 108 cells) and dies sooner because its dips are 2 to 3.8 times more often fatal: they are a different
     event. 40–48% of a wrapped face's dips to 0.4 of its population, and 71% of its deaths at 63 cells, come
     within a few generations of an over-full face (1–3% and 5% on the hull). A loop-12 tube against a wide face
     in the same decomposition: it reaches 0.4–0.5 of its population e^0.46 and e^0.85 times more often at 84 and
     108 cells, and those dips are less often fatal by 0.24 and 0.47.
7. **The same two exits in gump's 2D relative, with the prices the other way round [measured and exact, `toy/`;
   unrefereed].** In B34/S234 on the range-2 cross an edge row that is a ring dies by boom and bust (the row
   over-fills to 19.4 of 24 where 13.9 is normal, the cap takes it to one or two cells), and the edge of a box,
   whose end cells are protected, fades over 6–8 generations. There the flash is the DEARER exit per cell: the
   ring's deaths are two exponential laws, flash 0.30 + 0.455·L and no flash 4.03 + 0.327·L, the flash share falls
   from 0.90 at 12 cells to 0.47 at 32 (and, forecast first, 0.290 ± 0.024 at 36 against 0.298), and the ring's
   local price falls with it, 0.441 → 0.384, towards the box's steady 0.34. So the "0.416 against 0.343" on file for
   that rule is a crossover between exits. The exactly solved one-row surrogate has two prices that do not
   converge by 24 cells (open segment 0.4593 ± 0.0003, ring 0.519–0.528), and a control rule whose end cells can be
   overcrowded has one price, the difference dying as e^(−L/2.0). Which shape is dearer depends on which exit is
   cheaper per cell.
8. **Why rare-event sampling fails on gump itself, and what works [measured, four agents].** On wrapped faces
   there is no ladder of levels: the rare step is the over-full generation, the crash jumps every level at once,
   and sixteen clones of one parent count as two, because the fate is sealed at the launch. On hull faces forward
   flux is biased where it is not starved (estimate − anchor = −0.027 ± 0.018, −0.173 ± 0.044, −0.35 ± 0.26 at 45,
   63, 84 cells; `ref-hull/` built a second sampler of another design and met the same wall): a dip lasts ten
   generations and a flip deep in the chaos needs several to reach the face. What works is to put honest dice
   under six layers of rule and sample the dice. Its limit is a heavy tail in the rates of single replications,
   which is the common cause of the soft numbers at 192 cells (item 5) and at 135 cells (below).

## What was proved

- **The tilt identity [proved for the dice surrogate; `rigour/THEOREMS.md`, Theorem 2; refereed: `ref-proofs/`
  found no gap and checked it to 10⁻¹⁴ on ten shapes with its own code].** Let ε_i(x) = −ln P(cell i is dead next |
  x), E = Σ_i ε_i, and μ_s ∝ μ·e^(−sE) with μ the quasi-stationary law. Then ln τ = ∫₀¹ ⟨E⟩_s ds, and ⟨E⟩₁ ≤ ln τ ≤
  ⟨E⟩₀ ≤ 2.509·A (the upper exponential bound, with its constant). The referee's correction to the reading: the
  split into costs per cell is not canonical, and all the non-locality sits in the tilted measures.
- **One price, conditionally [Theorem 3].** If local means along the tilt depend on far geometry only up to
  K·e^(−r/ξ), then wrapped and rimmed faces have one bulk price, loops give discounts per cell, and a discount
  growing like length² cannot persist. The referee: a valid implication (as written it needs a K₀/A added at the
  end of the tilt), whose hypothesis is plausibly false on wide tori "and probably on rimmed faces too". Its
  evidence [measured, exact to 15 cells and by simulation to 30]: on wide tori the tilted law is a mixture of
  sparse faces and over-full faces, the valley between the two humps deepening as 1.2, 3.9, 15 at 12, 18, 27 cells,
  while triangles keep one hump through 30 cells; in both families the steepest slope of ⟨E⟩_s/A rises with size.
  [conjectured, the PI's reading] In the language of the theorem the two exits are a first-order transition in the
  emptying ensemble.
- **The seam identity [proved; `image/README.md`; refereed: `ref-proofs/` enumerated it on gump's own one-layer
  rule to 10⁻¹⁵; a seam one unit thick fails].** A torus is its loop-free cover conditioned on the whole history
  of a seam, two graph steps thick, recurring one loop along, reweighted by one over that history's probability.
  What does NOT follow from it without more: that density deficits add over loops, are per cell and do not depend
  on the tube's length, and that the decay rate is a gap of the transfer matrix. Those are [conjectured]. The
  numbers of the density law were not derived: the picture at one instant carries none of f(9), a cell's own
  six-generation history 10% of it.
- No lower bound e^(cA) was proved for any model with the cap, and no inequality between shapes: the exact rows
  show that "a tube never outlives a wide face" and "a rim always costs" are both false as general statements.

## The 135-cell face: not decided

`split-hull/` built forward-flux sampling for hull faces and it failed calibration (item 8). Two things stand in
its place.

**A forecast, 29.22 ± 0.02, conditional.** The dip rate to 0.6 of the population, measured by plain running at 135
cells, plus the line −2.049 + 0.17014·A, gives 29.223 ± 0.014; `ref-hull/` rebuilt it with its own stepper (dip
rates agree value by value from radius 9 to 21; line slope 0.17016 ± 0.00014) and gets 29.219 ± 0.010, or 29.232 ±
0.023 from a quadratic through the same four values. Its verdict: 29.22 ± 0.02 if the line has no rim term, which
the fit knows only as −0.027 ± 0.043; about that the method is silent. It favours 29.230 over 29.163 half on
evidence (the dip to 0.4 of the population, 14.65 of the 29.2 with all of the rim term, is measured at 135 cells
and sits on trend) and half by construction. Two more forecasts, blind to the samplers, agree: 29.210 ± 0.035
(`rim/`) and 29.215 ± 0.030 (`model/`); mine was 29.22 ± 0.03. They are extrapolations of the same five faces.
Beyond 135 cells the dip rate's own second difference shrinks (−0.176, −0.181, −0.176, −0.168 ± 0.002, −0.160 ±
0.004 from 63 to 198 cells): this route puts the 165- and 198-cell faces at 35.780 ± 0.014 and 43.011 ± 0.019,
below "the second difference repeats" (35.812, 43.085), with levels disagreeing by ± 0.03 and ± 0.05 there.

**A first measurement on a surrogate, 29.30 ± 0.09 after its referee** (`split-hull/README.md`, "Dice under the
hull"; `ref-dicehull/REVIEW.md`). Gump's true rule on every hull cell within five layers of the watched face, fair
coins on the two layers below, sampled by subset simulation over the coins; parameters frozen before any run above
63 cells. The referee confirmed the chain with its own code (chain minus gump −0.003 ± 0.005 at 45 cells, +0.024 ±
0.019 at 63; living state right at 135 cells; coins at density 0.42 or two layers deeper shift ln τ by 0.03 or
less). The sampler's readings, chain minus gump: +0.001 ± 0.019 and −0.044 ± 0.039 at the tuning sizes, +0.047 ±
0.024 at 84 cells and +0.126 ± 0.034 at 108 (both blind; the last without one giant replication, 17 times the
median rate, with which it is +0.05 ± 0.08). At 135 cells the chain reads 29.420 ± 0.042 on 156 replications,
drifting down as replications accumulate (29.453 at 120). The agent first read this as 29.40 for gump, "above
every forecast". The referee's corrections: the ± 0.042 is not an honest error (the dying chains of one
replication descend from 25–44 of 4,096 initial chains; the estimator is unbiased in the rate but heavy-tailed, so
the value can only come down as rare large replications arrive); a constant offset is rejected (χ² 14.2 on 3) and
a line in the area gives +0.147 ± 0.040 at 135 cells. **Gump by this method: 29.30 ± 0.09**, with the offset
extrapolated, not measured: 0.8 errors above 29.230 and 1.5 above 29.163. On the chain a hull face still dies by a
fade at every size (11 generations; a fall of half the face in 0.1%, 1.3%, 0.3% of deaths at 84, 108, 135 cells,
though falls of 0.4 of the face rise from 3% to 9%).

**The last run (`split-hull/`, 06:14 UTC; after the referee, not itself refereed).** With fresh stationary lanes
per seed: 84 cells, 234 replications, chain − gump +0.051 ± 0.026; 108 cells, 460 replications, +0.059 ± 0.046;
**135 cells, 385 replications, chain 29.397 ± 0.037**. The heavy tail has now been met at 135 cells: the running
pooled value fell from 29.498 (first 50) to 29.397, the first large replication arriving between 200 and 250, as
the referee said it would. Less the pooled blind offset (+0.053 ± 0.022): 29.344 ± 0.043; the value the agent
defends for gump is **29.34, +0.06, −0.10**, the downward error wider because the offset may be partly a sampling
bias that grows with size. A first reading at 165 cells: chain 36.09 ± 0.07 on 65 replications, tail not yet met
(so probably 0.05–0.1 high), 36.04 less the offset, against 35.78 by the dip-rate route. Where the chain's excess
over the dip-rate forecast sits: not between 0.6 and 0.5 of the population (gump's own tables are on trend there
at 135 cells, 0.000 ± 0.017), possibly between 0.5 and 0.4 (+0.09 ± 0.07), and on the chain all of it is in the
passage from the last seven or eight cells to none, where plain running cannot check and the sampler scatters
most.

**The deciding test the referee named, run last (`ref-dicehull/REVIEW.md`, "Brute force of the chain at R = 13").**
The chain itself, brute-forced at 84 cells with the referee's own code on four cores: ln τ = 18.2005 ± 0.0223
(2,004 deaths). Chain minus sampler +0.009 ± 0.034: **the sampler is exact at 84 cells**, and the referee
withdraws "unsampled tail" at that size. Chain minus gump +0.060 ± 0.023: **the offset is the chain's own**, and by
brute force it grows with size (−0.003, +0.024, +0.060 at 45, 63, 84 cells). So what the 135-cell chain value
(29.397 ± 0.037) means for gump depends on how that offset continues: held constant it gives 29.34–29.36; continued
as a line in the area, 29.26 ± 0.06. Why six layers of rule over coins sit above gump by an amount that grows on a
hull and not on a slab (where the same construction is within 0.02 to 108 cells) is not known.

So: forecast 29.22 ± 0.02 (conditional); surrogate between 29.26 ± 0.06 and 29.34 (+0.06, −0.10), depending on
the chain's offset; the old GPU value 29.34 ± 0.25. They agree with each other within about one error, and all sit at or
above "the second difference repeats" (29.230); the wrapped price taking over (29.163) is 1.5 to 3 errors below
each, on evidence that is partly by construction in the forecast and partly an extrapolated offset in the
surrogate. That is a lean against "two prices is a small-size effect that ends by 135 cells", not a decision.
The deciding test, named by the referee: brute-force the chain itself at 84 cells (0.03 in about an hour on four
cores), which separates "the chain is not gump" from "the sampler's unsampled tail"; then many more initial states
per replication, and the 165-cell face.

## Forecasts frozen before the data

| what | forecast | by |
|---|---|---|
| 120-cell tube (1,18),(0,40) | 24.56 ± 0.03 | PI, block 0 |
| | 24.563 ± 0.030 | `tube1d` (its later K = 2 fit: 24.571) |
| | 24.575 ± 0.025 | `model` |
| | 24.570 ± 0.025 | `rigour` |
| | 24.59 ± 0.05 | `split-slab`, bookkeeping (blind test on the 108-cell tube: 22.171 ± 0.057 against 22.160) |
| | 24.60 ± 0.07 | `split-slab`'s surrogate sampler as pooled by its referee: the only measurement of anything |
| 135-cell hull face | 29.22 ± 0.02 (conditional); surrogate 29.34 (+0.06, −0.10) and 29.30 ± 0.09 | see above |
| 165-cell hull face | 35.780 ± 0.014 (dip-rate route), 35.79 ± 0.05 (PI), 35.74 ± 0.09 (`rim`), 35.76 ± 0.08 (`model`); surrogate 36.04 ± 0.07, tail not met | |
| 192-cell tube (1,30),(0,64) | 39.17 / 39.01 / 38.92 / 38.86 for K = 1 / 2 / 3 / a power law; surrogate 38.85 ± 0.12 | `tube1d`; `split-slab` |
| wide 192-cell torus | 40.07 (the line); 40.35 ± 0.25 (`split-slab`, for gump) | |
| 240-cell tube | 48.63 (K = 2); 48.40 ± 0.25 (`model`) | |
| 200-cell wide torus | 41.716 ± 0.05 (`model`'s form; the straight line gives 41.742) | |

The first five numbers for the 120-cell tube extrapolate the same three anchors and are not independent; that
face separates only K = 1 (24.608) from the rest. The GPU's value for it lands after this report.

## Referees, in one line each (details in the items above and in each `REVIEW.md`)

- `ref-anatomy/`: boom and bust confirmed with its own code and sharpened (one hump, no breathing, the layer
  beneath as the hidden variable). Not checked: holes, the band test, anything above 63 cells.
- `ref-boom/`: launch hump, four-layer profile and island table confirmed; "0.2099 against 0.2087" refuted as
  evidence. Its sentence for you: there is no formula yet; a formula must produce 0.738, 0.079 and 0.136 from the
  rule.
- `ref-proofs/`: nothing marked proved broke; 14 exact rows recomputed to every digit; the seam identity's
  consequences and Theorem 3's hypothesis are not established.
- `ref-map/`: the two-layer map's wrapped half confirmed at 63 cells; its hull half refuted.
- `ref-slab/`: the dice chain and its sampler confirmed; 120-cell tube 24.60 ± 0.07; 192-cell numbers are not
  measurements to their first quoted errors; long-tube shares are a trend.
- `ref-hull/`: dip rates confirmed; 29.22 ± 0.02 fair and conditional; its own sampler failed like the first.
- `ref-dicehull/`: the hull chain confirmed; the 135-cell reading corrected from "29.40, above every forecast" to
  29.30 ± 0.09, nothing decided. (The agent's later run of 385 replications, 29.34 +0.06 −0.10, came after this
  review and bears it out.)
- `ref-report/`: this report against its sources; its corrections are applied here.
- Unrefereed: `rim/`, `toy/`, `tube1d/`, `model/` (mostly), `split-slab/` §9–§11, `ref-boom/STATIC.md`,
  `ref-anatomy/THEORY.md` beyond what `ref-map/` checked, `pi/`.

## What failed

- **My front gas.** I read the quadratic tube discount as two-stage deaths through a band right round the girth.
  `anatomy` measured it within the hour: no band-first class. With one edge cost for every loop the form has χ²
  3,160 on 49 (`model/`). Dead.
- **"Two prices because two routes", as I first wrote it,** and my forecast that a strip's added width would cost
  nearer 0.231 (it costs 0.2017). On a wrapped face there is one route; a hull face at equal area fades more readily
  than a wrapped face thins, and lives longer only because it cannot bust.
- **Sampling gump itself** with clones and levels: four samplers built, none calibrated (item 8).
- **A formula for the price:** the tangent construction (spread 0.63 in ln τ over 48–66 cells); min over x of
  [boom + tail price × survivors] (0.275 against 0.207); one-variable maps (0.188–0.219, launched from the wrong
  place); the two-layer Gaussian map (0.160–0.165, and nothing for the hull); "every surviving cluster fails on
  its own" (right to a factor 1.5 only by two errors of a factor 2–5 cancelling); the launch split read as a test.
- **The numbers of the density law** from a response round the loop; the simple timing chain as the law of the
  tube's discount.
- **Exact solution at gump's own loop lengths:** a synchronous product costs 2^(A + frontier); exact reach is 18
  cells.
- **My own forecasts** (`PREDICTIONS.md`, blocks 0–4), sixteen scored: 6 held (the two 96-cell faces and the bend
  of loops 13 and 16; wide faces rigid in time; the timing statistic constant in section length on the 192-cell
  tube and absent on the wide torus), 3 half right (boom and bust persisting on wide faces but not tubes; the
  halves of long tubes crashing apart; the size of the timing jitter), 7 failed (band-first deaths; one edge cost
  for patches and tubes; wide tori carrying the front term; the strip's width price; the tube's advantage sitting
  in a more frequent over-fill or fewer survivors; a half of a 192-cell tube busting as one; the timing chain's
  number). Six are still open, the 120-cell tube and the 135-cell face among them.

## What is not known, in order of what I would do next

1. **Settle the 135-cell hull face.** The sampler is now known to be exact at 84 cells; what is missing is the
   chain's own offset from gump at 108 cells by brute force of the chain (about a day of four cores, or an hour of
   the GPU), and why it grows. Then the 165-cell face. The forecast route's own second difference is shrinking beyond 135
   cells; whether "0.231" is a price or a long transient is still the question you asked.
2. **The kill, or: is the price static?** Of the 0.21 per cell, 0.079 is the rarity of an over-full face, 0.166 the
   rarity of an over-full stack of four layers, and the remaining 0.057 is still only measured from deaths. The
   next state to try is one the rule itself names: the number of face cells that will be alive next generation
   (a function of the present state). If "over-full now and nearly empty next" has a static rarity equal to the
   price, the price is a large deviation of the living state, measurable at any size without a death.
   Tried at the end of the night (item 4, last bullet): no such event was found, but a two-number kill law on
   top of a living-state frequency forecasts wide faces to 108 cells. The same estimator reaches 126–192 cells by
   plain running and would say, without a single death, whether the wide price keeps bending.
3. **Whether 0.2087 lasts.** Two indirect readings at 192 cells now disagree by 1.8 errors: the living-state
   estimator puts a wide face on the line (40.03 ± 0.24), the dice-chain sampler 0.42 ± 0.20 above it, with a
   possible drift of the surrogate underneath. On the surrogate the face still busts as one. Nobody has seen gump
   itself die above 126 cells.
4. **A tube's asymptote** (0.2004 with K = 2, or lower with a power in front): tubes of 240–360 cells on the
   surrogate, with the timing of their sections recorded.
5. **The wrapped face's own decomposition by area** (`ref-hull`'s next step): the rate of over-full generations at
   two or three thresholds and the chance that one ends in death, on wide tori of 57–84 cells and on tubes.
6. **A lower bound.** Nothing with the cap in it has one.

## What I found beautiful

A face dies of too much life. For a week the price per cell was read off the lower tail of a face's population,
because a face that is dying is thinning. The route is through the upper tail: the face fills in one step, four
layers together, and the rule's cap turns a full face into an almost empty one in the next. The rim of a hull face
is safe from that for the plainest of reasons, a rim cell can hardly count to six, and so the same rule gives a
hull face a different death. The exactly solved surrogate, which has no chaos in it at all, does the same, and so
does the 2D relative, where the prices come out the other way round.

And one identity nobody had asked for: in a long living tube, the chance that a stretch of it is empty at this
instant is the death rate of a closed tube of that length, up to a constant. The dead tube is already there,
momentarily, inside the living one.
