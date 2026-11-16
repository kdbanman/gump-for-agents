# Status (overwritten as things change; history is in git and NOTEBOOK.md)

_Last updated 2026-11-14 by the lead._

## Built and verified
- `reference/` oracle — matches the original's logs, sides 8–12 (13 via the engine on the legacy torus).
- `engine/` — Rust, bit-exact vs oracle and all legacy logs; ≈4×10¹⁰ cell-updates/s/core.
  Round two: `gump show` (text renderings, kagome layers), `png`, `describe` (re-derives all 1,307
  atlas objects), packed ensembles (≈4× for small boxes), `--sym` symmetric soups. Not built: a
  symmetry-reduced stepper (would buy closed cubes beyond side 16).
  Round three: `--sym` torus soups fixed, `ensemble --layer-deaths` (exact peel times),
  `gump occupancy` (time-averaged maps), `--checkpoint` for restartable runs.
- `web/` v1 — WebGL2 bit-packed stepper + three.js views; web suite 79/79 (`cd web && node test/run.mjs`, re-run 2026-11-14).
- `research/atlas/` — exhaustive still lifes ≤16 cells, oscillators, vertex star, legacy ash, critical thickness.
- `research/peeling/` — the face law, cuts, symmetric effective area, account of the cube series.
- `web/` rounds two and three — kymograph, `{111}` slicer, editor, atlas gallery, guided tour, static build.
- `research/phase/` — the chaotic state as a phase; 960-rule survey (`research/figures/phase_rulemap.png`).

## In flight on 2026-11-13, late (historical; what is running now is in the state block under "Next")
- A usage limit stopped every agent at about 20:00 UTC on 2026-11-13. State left behind:
  - `research/theory/class.md`: the class agent had finished ("final" in its last commits). Not yet checked by
    the lead or attacked by a second agent.
  - `research/theory/exponent/`: the exponent agent was stopped before writing its report (`exponent.md` is a
    stub). Its forecasts and outcomes are in `exponent/PREDICTIONS.md`, its theorems in `exponent/theorems.md`
    (Lemma A, consequence (c) there is false: swarm board E10). Needs a successor to write it up, then checking.
  - `research/audit/gpu_pr8/`: partial scripts from the reviewer of pull request 8; no review written. Restarted.
- **Pause lifted, 2026-11-14.** The owner, after the overview page: "pass me a prompt for the compactor … so you can pick up
  where you left off (and/or head wherever you like next)". The lead reads this as leave to resume by judgment, mindful of
  usage (the pause was for usage). Restarted so far (2026-11-14): one agent, a successor to the swarm's critic, clearing the
  queue at the top of `swarm/critic/board.md` (counting round 2 and its lab requests; the interim rounds of probability, path
  and source). The solvers wait for its replies. Also done since (both finished and recorded, see "Next"): an adversarial review of the GPU
  session's pull request 12 (`research/audit/REVIEW-gpu-pr12.md`), and an adversarial check of
  `research/theory/class.md` (`research/audit/REVIEW-class.md`; its out-of-sample test was the edge-neighbour
  rule, there called `face12e`). Everything else below is still the state at the pause.
- **PAUSED at the owner's request (usage), 2026-11-13 about 23:55 UTC.** (Lifted 2026-11-14, see above.)
  Swarm state at the pause: round 1 fully refereed for all four lines; round 2 refereed for path and source;
  counting round 2 written, the critic's reply to it finished or interim (see `critic/to-counting.md`); probability
  paused in round 2 and path and source in round 3, each with an interim report in its journal, unreviewed. The
  librarian is idle with no open requests. To resume: for each solver, a fresh or resumed agent told to read its
  own `journal.md`, `claims.md` and `critic/to-<line>.md`; the critic (or a successor) first, to review the interim
  reports. Agent ids are in the scratchpad notes and may no longer resume; the journals are written for successors.
- `research/theory/swarm/` (relaunched about 22:05 UTC at the owner's word): four Fable solvers (`probability`,
  `counting`, `path`, and from about 22:20 `source`), a librarian (`library/`: primary papers read, theorems as stated) and a critic on one problem, the area law, by mathematics alone. Problem and rules in
  `swarm/PROBLEM.md`; results in each `journal.md` and `claims.md`; the critic's map is `swarm/critic/board.md`
  (its first pass already corrected several numbers the lead had been quoting: read E1–E11; the list now runs to E15). The lead drives the
  rounds (`LEAD.md`, "The swarm"). Nothing in it is established until a fresh reader has audited it.
- GPU session "Modal API" (see `LEAD.md`): pull request 8 reviewed and merged 2026-11-13 (notebook entry; review in
  `research/audit/REVIEW-gpu-pr8.md`; corrected reading at the top of `research/gpu/README.md`). The fixes the review
  asked for arrived as pull request 10 and are merged (lead spot-checked the diff). Asked next: slab faces at A > 90, octahedral faces at A ≥ 165,
  a longer cube-centred symmetric run (does the death rate really fall with age?).

- 2026-11-14: an overview page for the owner (`docs/overview/`, since 2026-11-15 the multi-page `site/`; published as a private artifact; link in `LEAD.md`). Refreshed and republished the same day at 11:50 UTC (current to the swarm's close and the exponent study).
  It predates the two reviews of 2026-11-14 (class theory, GPU round two); refresh it when the swarm's exam is in.
- Pull request 11 merged 2026-11-14 07:27 UTC (everything up to the two reviews). Pull request 13 merged 09:55 UTC
  (exam, audit, class revision and follow-up, exponent report, reviews of GPU pull requests 12 and 14). Later
  commits need a new pull request.

## Next (lead's list; pick by judgment)
- **Read this first (02:25 UTC, 2026-11-15): the lead cannot read usage any more, and cannot message the cloud GPU
  session.** The owner approved a trust card so that this session could answer a ping from a local GPU session on
  their machine (a GTX 1080); since then `list_events` and `send_message` to cloud sessions are refused. The rule for
  working without readings (reckon from the last one, 01:21 UTC: weekly 0.27, Fable 0.27; no new agent past an
  estimated 0.70) is in `LEAD.md`, "Watching usage"; the sessions and what may be done with them, "Other sessions".
  The owner has been told and asked for the figures from their screen.
- **GPU work moves to the owner's GTX 1080 (their words of about 03:30 UTC, 2026-11-15, in `LEAD.md`, "Other
  sessions"): no budget, no limit.** **Its session reported ready at about 03:38 UTC and was briefed at 03:45 UTC; the
  brief is `research/GPU-QUEUE.md`** (jobs 0 and 1, then queue items (2) and (3) without waiting for the lead's
  review; a message to the lead after each job). Each message the lead sends it costs the owner an approval prompt
  that no allow rule answers, so further briefs and review findings go into that file, which it fetches after each
  job. It writes under `research/gpu-local/`; it has no gcc and no `gh`, and whether it may push is the owner's to
  tell it; if it pushes a branch the lead opens the pull request. Readiness details: `LEAD.md`, "Other sessions". **Jobs 0 and 1 reported at 04:41 UTC** (branch `claude/gpu-local-1080` at 34cd2d3, **pull request 23**,
  opened by the lead): acceptance passes on the card; the guard is `research/gpu/guard.py` (host side, kind 5, off by
  default); a 4 × 4 torus calibration gives ln τ_face = 9.9251 ± 0.0004 against 9.9324 ± 0.0020 on file (3.6σ,
  unresolved; it anchors `research/constant/PREDICTIONS.md` part C); `fwslab.py` undercounts firewalls where lives
  settle. **Review started 04:43 UTC (Opus)** -> `research/audit/REVIEW-gpu-local-pr23.md`, with a third,
  independent CPU measurement of the 4 × 4 torus. The lead recomputed 9.9251 from the branch's csv row. A = 93 is
  running on the card. The lead's reply is the top note of `research/GPU-QUEUE.md` (re-measure the 5 × 5 anchor on
  the card; a stationary-dip measurement on big faces is proposed for later). **The review is in (05:25 UTC) and
  recorded** (notebook entry "a second card", CLAIMS GL1, GL2, notes on SH3, SH4, a dated note under part C): the
  GPU's 4 × 4 value stands (best 9.9249 ± 0.0003 from three codes; the file's 9.9324 was a high draw); the guard is
  sound, with one false latency claim. Five must-fix items are the top note of `research/GPU-QUEUE.md` (05:30 UTC).
  Merge pull request 23 when the 1080 session has pushed them (CI, full head sha).
  **Dying faces, round 3: reviewed and recorded 05:49 UTC** (notebook entry "what the dips say about the price of a
  cell", CLAIMS DY8–DY12, 147 claims): the dips give c = 0.215 ± 0.005 and cannot separate 0.207 from 0.219; the
  end effect is 0.2125·A − 2.07; a depleted face is at half density near its survivors and not emptied elsewhere;
  **the equilateral torus n = 21 is 13.176 ± 0.011, above every part-C forecast** (queued on the card with n = 19;
  the lead's forecasts N1–N4 under part C). **Round 4** (the lead's two-phase reading, forecasts F1–F6 in
  `research/dying/PREDICTIONS.md`) is the next CPU experiment. Owed: the README's seven round-3 corrections, the
  essay, the overview and the draft for round 3.
  **The card's A = 93 result (seen 05:54 UTC on its branch at dcb61c8, no message): 19.4141 ± 0.0053**, below the
  flat and rising readings of part C (both refuted) and on the low side of the massive one; notebook entry "the
  93-cell torus lands below every reading", CLAIMS GL3 (C until reviewed), scoring note under part C; the lead's
  N1 failed. It also found a +0.0016 bias in `rep.c` at A = 48. It is now running n = 19, 21 and 5 × 5; n = 21 is
  the open comparison (CPU 13.176 ± 0.011 against its forecast 13.124). **Fetch its branch at every wake-up**
  (`git fetch origin claude/gpu-local-1080`; usage figures are asked for in `research/gpu-local/USAGE.md` there).
  **Its message of 06:15 UTC (branch at b843883):** n = 19 11.8756 ± 0.0006, n = 21 13.1622 ± 0.0007 (confirms the
  CPU's 13.176), 5 × 5 15.6630 ± 0.0023; slopes 0.2167, 0.2144, 0.2084, 0.2084: one line from 63 cells up, the small
  tori below it; no reading of part C survives; recorded (notebook "five wrapped faces on one driver", GL3,
  DY12 to A, scoring note; the lead's N2 held). It is running 81, 84, 108, 111 (about 5 h), then the hull face.
  Usage read by it at 06:15 UTC: weekly 0.40, Fable 0.44. **The review of the five tori is in (08:10 UTC) and
  recorded** (`research/audit/REVIEW-gpu-local-tori.md`; notebook "the five tori, reviewed"; GL3 regraded: A at
  48, 57, 63, 75 cells, C at 93): the values stand; no smooth correction fits, only a kink near 61 cells; the
  census pipeline's 16-generation rule reads loop² 4 classes high by 0.017–0.018. Six must-fix items for the card
  are the top note of `research/GPU-QUEUE.md` (08:15 UTC); pull request 23 waits on them.
  **SIGNALS EXIST (first push reported 08:45 UTC):** pulses on free-standing wires (half the speed limit), an
  emitter, a transmission (receiver creeps one cube per signal), a head-on interaction; the lead re-ran every
  verifier and wrote `research/audit/signals_lead_check.py` from the oracle alone (pulses pass); recorded as
  notebook "gump carries signals", CLAIMS SG1 (B), SG2–SG4 (C), OPEN-PROBLEMS 13, the owner's journal. **Running
  since 08:52 UTC: an Opus adversarial review** (-> `research/audit/REVIEW-signals.md`) **and the second Fable
  push** (bounded or closed tracks, a receiver that stays put, a gate, soup-born wires, wire meets chaos; the
  lead's forecasts S6–S10). On the review: regrade SG rows, essay section, overview plate (a pulse running live),
  draft. On the second push: lead's oracle check of each new object, then review, then record, then a third push
  if work remains and Fable usage is under 0.85.
  **Dying faces, round 4: recorded 09:43 UTC** (notebook "a depleted face thins as one thing", CLAIMS DY13 at C,
  153 claims; essay corrected): the lead's two-phase reading failed (F1–F5; no remnant at fixed density; a caught
  face is one loose cluster, 1.15 to 2.4 times the company of a randomly thinned one); the big-face dip job is
  withdrawn from the card's queue. **Review started 09:46 UTC (Opus)** -> "Round 4" in
  `research/audit/REVIEW-dying.md` and `research/audit/dying4/`; on its report: regrade DY13, corrections to the
  study's README, the essay if "no remnant" has to be narrowed. Usage reckoned at 09:46 UTC from the 06:15
  reading: weekly about 0.50, Fable about 0.64 (no newer reading; the card's branch is still at b843883).
  **Round 4 reviewed and re-recorded 10:15 UTC**: the numbers stand; "no remnant" is withdrawn (an exact
  fixed-density patch reads the same on faces this small, so the lead's tests could not tell); what fails is the
  construction's end point, by 1.07–1.34 nats (notebook "round 4 reviewed"; CLAIMS DY13–DY15; the study's README
  corrected by its author at 7b15db2; essay corrected).
  **State space (the owner's journal question): reported 10:13 UTC and recorded 10:20** (notebook "how much of its
  state space a seed explores", CLAIMS SS1–SS3, 158 claims, a line in `docs/OWNER-JOURNAL.md`, a new essay section):
  states visited = settling time + period; 301 vessels of up to 30 cells listed exactly (the lead re-enumerated one
  16-cell hull from the oracle alone: equal); side-16 cube 2,919,617,676 states of 2^51,888; 0.30 bits per face
  cell; a living face carries about 0.95–0.99 bits per cell. **Review started 10:17 UTC (Opus)** ->
  `research/audit/REVIEW-statespace.md` and `research/audit/statespace/`; on its report: regrade SS1–SS3, README
  corrections, the essay's hedge on the entropy sentence. **The lead's own check of the shuttle clock** from the
  second signals push (period 4N + 2 at N = 1, 2, 3, 4, 7, 12): `research/audit/signals_clock_lead_check.py`.
  **Pull request 24 merged 10:23 UTC (e4295e8); pull request 25 is open.**
  **Second signals push reported 10:25 UTC and recorded 10:30** (notebook "a clock of every length", CLAIMS
  SG5–SG10, 164 claims, OPEN-PROBLEMS 12 and 13, the owner's journal): a clock of period 4N + 2 for every N (proof
  claimed), a rake, a collision gate, a register, a tape of B and C units, soup-born carrier wires, chaos destroys
  a wire on contact and two empty layers isolate it. The lead re-ran every verifier and wrote own oracle checks
  of the clock, the gate, the C pulses and the tape ring (`research/audit/signals_*_lead_check.py`). **Review
  started 10:28 UTC (Opus)** -> `research/audit/REVIEW-signals-2.md`, `research/audit/signals2/` (the two proofs
  first). A third push (the tape as a shift register; wide pulses; a period 0 mod 4; a corner) waits for a usage
  reading or for the first review to finish.
  **State-space review in and recorded 10:48 UTC** (notebook "the state-space study reviewed"; SS1–SS3 regraded:
  A on seventeen vessels, B for the cubes 8–15 and the entropy): counts stand; the ranges, "linear not
  exponential", the share and the random-map yardstick corrected; **one layer of the chaos is within about 1% of
  coin flips, the slab at least 2.7% short** (the number behind "coins will do"; written under the owner's
  journal note and into the essay). The study's author is applying the review's seven README corrections.
  **Overview editor started 10:31 UTC (Opus)**: plates for signals (live pulse, clock, gate, with a node check of
  the page's stepper), the state-space answer, dying rounds 3–4, the five tori; the lead publishes after reading
  it. **Third signals push started 10:50 UTC (Opus, since no usage reading has come since 06:15)**: a machine made
  of parts (a periodic emitter, a clock driving a counter, a corner); the lead's forecasts S11–S15 are in
  `research/signals/PREDICTIONS.md`. Essay updated (signals section, the five tori, the state-space answer).
  **First signals review in and recorded 10:53 UTC** (notebook "the first signals push reviewed"; SG1–SG3 to A,
  SG4 A/B; 164 claims: A 78, B 72, C 13, D 1): everything stands on a third code; the transmission has a capacity
  (35 shots over 36 cubes, the 36th burns the wire); nine README corrections handed to the third investigator.
  The state-space author applied its review's seven corrections (281cf02). Still running: the review of the second
  signals push, the overview editor, the third signals push.
  **Overview published 10:59 UTC (version 12)**: new plates "Signals" (a live pulse, the gate, the clock with a
  slider for N; `site/checks/check-signals.js` checks the page's stepper against the oracle) and "How much of
  the room a seed sees" (the owner's question, with the coin-flip tile); "How a face dies" brought to rounds 3–4
  with the withdrawn sentence shown; the five wrapped faces from the owner's card on "One price per cell?"; map
  and "Open now" rewritten. The lead rebuilt it, ran both checks, loaded it headless (no script errors) and read
  four of the new plates before publishing; two captions corrected.
  **Second signals review in and recorded 11:26 UTC** (notebook "the second signals push reviewed"; SG5–SG7 to A,
  SG8–SG10 to B with corrected wording; 164 claims: A 78, B 75, C 10, D 1): the clock's and the tape's proofs are
  complete (clock on the oracle to N = 257); the register is a 16-position counter; **corrected: the isolating gap
  is three layers (T3), not two; "born from soup" was nearly all one-unit rings; the fire's speed depends on
  density.** Essay, owner's journal, OPEN-PROBLEMS corrected; the overview's Signals plate is being corrected by
  its editor, then republished; six README corrections go to the third investigator.
  **Overview version 13 published 11:30 UTC** with the Signals plate corrected (three empty layers; a repeated
  random unit, not soup; "every time" with the speeds; a few in a hundred; the 16-position counter; both proofs
  marked checked). The third investigator has applied both reviews' README corrections (6c32bfc and before).
  Running: the third signals push (since 10:50 UTC), the manuscript editor (fifth update of `docs/paper/`).
  **Manuscript draft brought up to date 11:44 UTC** (fifth update, commits 5daa37f … b1c807b: rounds 3–4 in §5.6,
  a new §6.1 on the state space, §7.5 rewritten round the 0.2084 line and the kink, a new §8.1 on signals with
  the clock and tape as Theorems 8 and 9; both number scripts pass). Its eleven items for the lead are applied
  (notebook entry "corrections found by the fifth pass"; SG11 added, 165 claims): **the lead's conjecture about
  the kink is withdrawn** (it used cube steps where round 3 had doubled units). Prior art for the signal objects
  has not been searched (`docs/paper/GAPS.md` item 50).
  **Pull request 25 merged 11:48 UTC (46e5a29; check.sh 20/20, CI green).** Running: the third signals push (since
  10:50 UTC; forecasts S11–S15). On its report: re-run its verifiers, the lead's own oracle check of each new
  object, an adversarial review, then the record. The card in the owner's house is still on the wrapped faces of
  81, 84, 108, 111 cells (its branch has not moved since 06:15 UTC; fetch at every wake-up).
  **The card's message of 12:01 UTC (branch at 16271f3): wrapped faces of 81, 84, 108, 111 cells** = 16.9222 ±
  0.0031, 17.5467 ± 0.0031, 22.5600 ± 0.0222, 23.2032 ± 0.0231; one line from 63 to 111 cells, 0.20867(9) per cell,
  χ² 7.8 on 5; its five-face line was low at all four; the 81-cell face lies between that line and the smooth
  forms. The lead recomputed all nine from the rows (notebook "nine wrapped faces on the owner's card"; GL3
  extended, B− above 75 cells; N3 held by its letter). It says both fix lists are closed; its hull face of 108
  cells (two 7-hour seeds) ends about 02:00 UTC on the 16th, forecasts written first. **Usage read by it at 12:01
  UTC: weekly 0.54, Fable 0.61** (the lead's reckoning had been 0.60 / 0.73); readings are now in
  `research/gpu-local/USAGE.md` on its branch. **Review started 12:04 UTC (Opus)** ->
  `research/audit/REVIEW-gpu-local-tori2.md`: the hull driver first, the fix lists, the nine faces as science, a
  CPU value at 81 cells if affordable. Merge pull request 23 when it confirms the lists and CI is green.
  **12:48 UTC: the review is in (interim on one point) and pull request 23 is MERGED (0b294fa; both fix lists
  closed, CI green on 16271f3); the working branch has main merged in (8606999).** Review recorded: notebook "the
  nine wrapped faces reviewed"; GL3 extended; a note of 12:50 to the card in `research/GPU-QUEUE.md` (six wording
  corrections, the age table to commit after the hull run, an optional longer run at 111 cells). Findings: errors
  honest (seeds' χ² 19.0 on 16); only the broken line fits all nine and that choice rests on 48, 57, 63 cells;
  price per cell 0.2087–0.2090, no rising slope preferred; the 81-cell face could not have been a sharp test; the
  hull driver is sound. Owed: the reviewer's CPU value at 81 cells (its two runs were still going at 12:50; it
  resumes itself and hands back) -> add to GL3 and the notebook entry's last bullet. New commits on the card's
  branch need a new pull request (opened by the lead).
  **The third signals push reported about 12:40 UTC** (README §15–19): no emitter, corner, clock-driven counter or
  period-4N clock; the clock's left cap eats every word and keeps no trace (proved; the lead's own oracle check
  `research/audit/signals_reader_lead_check.py`); P ≡ k_R + k_L (mod 4) and the 3 × 3 / 5 × 5 turn-class results; a
  second counter (8|C). Recorded provisionally: notebook "the third signals push"; CLAIMS SG12–SG15 (169 claims);
  OPEN-PROBLEMS 13 (four sharpened questions a–d); the owner's journal; the lead's note in
  `research/signals/PREDICTIONS.md`. **Its adversarial review is running** (Opus, since 12:44 UTC) ->
  `research/audit/REVIEW-signals-3.md`. On its report: regrade SG12–SG15, corrections to the README (by the
  third investigator or a successor), essay, overview, draft. Not yet updated for the nine faces or the third push:
  `docs/WHAT-I-SEE.md` (the five-tori paragraph), the overview (version 13), `docs/paper/`.
  **13:05 UTC: two new lines of work started.** (1) **A fourth signals push** (Fable, since 12:55 UTC; forecasts
  S16–S21 in `research/signals/PREDICTIONS.md`): emitter, corner, period-4N clock, or a proved obstruction; it will
  also apply the third review's README corrections. On its report: the lead's own oracle check of any new object,
  an adversarial review, record. (2) **The wrapping law** (the lead's fit, 13:00 UTC; notebook "the kink is the
  wrapping"; CLAIMS WL1 at C; `research/audit/wrap_law_lead.py`; frozen parameters and forecasts W1–W6 in
  `research/wrap/PREDICTIONS.md`): every wide wrapped face on file (32) fits one line less a discount per cell for
  each closed loop of squared length 12, 13, 16, 19, none from 21; it forecasts the equilateral "kink" from other
  faces. **An Opus tester is trying to break it** (since 13:03 UTC; new classes at 51 to 69 cells, forecast first)
  -> `research/wrap/README.md`. On its report: regrade WL1, rewrite GL3/GP9/SH rows that the law subsumes, essay,
  overview, draft (§7.5), and redo CN1's joint fits. A note of 13:05 in `research/GPU-QUEUE.md` gives the card five
  tori at 75 and 84 cells with frozen forecasts, for after its hull run. The essay's wrapped-face paragraph already
  describes the law as unreviewed. Ledger: 170 claims (`python3 research/audit/claims_tally.py`).
  **13:19 UTC: both reviews are in and recorded.** (a) Nine faces: the reviewer's CPU value at 81 cells is 16.9386 ±
  0.0124 (card 16.9222; 1.3σ); GL3 is B at 81 cells, B− above. Nothing more is owed on that review. (b) **Third
  signals push reviewed** (`research/audit/REVIEW-signals-3.md`; notebook "the third signals push reviewed"; SG12
  A, SG13 B, SG14 A/B, SG15 B−/C; 170 claims, A 81, B 77, C 11, D 1): the reader proof is complete; the 8|C wall
  reflects a double pulse (two in, one count, one back; the lead's own oracle check
  `research/audit/signals_reflect_lead_check.py`); wire 8 is not free-standing (ring only); the eight k = 2 caps
  destroy themselves in a lone turn; "every clock is 4N + 2" is measured, not proved; the emitter negatives exclude
  only word periods 2 to 4 near the end of the 3 × 3 tube. Corrections to the README were applied by the fourth
  push (e082fe1). OPEN-PROBLEMS 13 now lists questions (a) to (f). **Still running:** the fourth signals push
  (Fable, since 12:55) and the wrapping-law tester (Opus, since 13:03).
  **14:57 UTC: the wrapping-law test is in and recorded** (`research/wrap/README.md`; notebook "the wrapping law
  tested"; the lead's refit `python3 research/audit/wrap_haz_lead.py`; CLAIMS WL1 rewritten to B/B−, WL2 B, WL3 C;
  172 claims, A 81, B 79, C 11, D 1). The law held W1, W2, W3, W4 and failed W5, W6, and is the wrong form (χ² 120
  on 41 with the precise values it left out; 4–16σ off below 48 cells). Stands: short loops discount, the effect
  ends between loop² 19 and 21, 0.2086 ± 0.0001 per cell with no short loop. Open: how one loop's discount grows
  with area; the tester's "second way to die" form, a straight line per loop length and a power form fit equally
  below 80 cells (the lead's refit; this narrows the tester's reading). **Owed:** the card's 84-cell face with one
  loop of 12, torus (1, 12), (0, 28): forecasts 17.3604 / 17.3361 / 17.3207 / 17.2941 (old law / lines / power /
  exponential), frozen in `research/wrap/PREDICTIONS.md` (W7–W10) and queued in `research/GPU-QUEUE.md` (14:55
  UTC) with a 96-cell face and three faces that cross-check the tester's stepper. No second agent has reviewed the
  tester's new faces; the card's three are that check. **Still running:** the fourth signals push (Fable, since
  12:55). **Not yet done:** overview version 14 and the draft (nine tori, the wrapping result, signals pushes 3–4).
  **15:16 UTC: the fourth signals push reported** (README sections 20–25, 21b; notebook "the fourth signals
  push", provisional). A gun (15 cells, period 4, writes a rake onto bare wire every period), a line and a beam
  (gun + wire + receiver, free-standing, period 4), a divider (catalogue oscillator C8.24a beside the stream turns
  every second rake into a hole, period 8, the oscillator never changed). All its verifiers and proof scripts pass
  here; the lead's own oracle checks of the gun and the divider pass
  (`research/audit/signals_gun_lead_check.py`, `signals_divider_lead_check.py`). Forecasts S16–S21 scored in
  `research/signals/PREDICTIONS.md`. **Running:** the adversarial review of it (Opus, since 15:16; →
  `research/audit/REVIEW-signals-4.md`) and the lead's CPU run of the 84-cell face with one loop of 12 (since
  14:58, about 80 minutes). **Owed on the review:** CLAIMS rows SG16 on, OPEN-PROBLEMS 13, the owner's journal
  (the note that nothing ordered speaks onto a wire no longer holds), the essay; then overview 14 and the draft.
  **15:21 UTC: the overview is being rebuilt as a multi-page site** (the owner's request, quoted in `LEAD.md`,
  "The overview page"): an Opus agent is writing `site/` (sources per page, data fetched per page, the web app
  mounted under `app/`, one build to `site/dist`, deployable to GitHub Pages by the manual workflow and
  publishable as a private multi-file artifact). Phase 1 keeps the content of version 13 exactly; the new
  findings (nine tori, the wrapping result, signals pushes 3–4) go in afterwards, page by page. **Owed on its
  report:** the lead looks at the built pages, runs `bash site/check.sh`, fixes the references to
  `docs/overview` in `LEAD.md`, `CLAUDE.md`, STATUS and `research/check.sh`, publishes the folder to the private
  artifact, and tells the owner what to click to put it on Pages. Usage reading from the owner at about 15:18
  UTC: 62% weekly, 73% Fable.
  **15:58 UTC: done.** `site/` is merged into this branch (commits 3dbc359 … dbc88e9; 29 plates byte-identical to
  version 13 apart from three sentences that named a place on the old page; `bash site/check.sh` and
  `bash site/check.sh --artifact` pass for the lead), and the private artifact is now the multi-page site
  (version 14, 84 files; how to republish: `LEAD.md`, "The overview page"). Not yet seen rendered on the host by
  anyone. **Next for the site:** the new findings, page by page (nine tori, the wrapping result, signals pushes 3
  and 4), after the fourth push's review is recorded; the owner's two clicks for the public site.
  **16:03 UTC: the fourth signals push is reviewed and recorded** (`research/audit/REVIEW-signals-4.md`; notebook
  "the fourth signals push reviewed"; CLAIMS SG16–SG22; 179 claims, A 86, B 81, C 11, D 1; OPEN-PROBLEMS 13
  questions (g)–(k); the owner's journal and the essay updated; the review's 14 README corrections applied by the
  reviewer, 96123e0). Stands: the gun (A), the line and the beam for every length (A, proofs re-derived), every
  word of holes heals (A, exhaustive), the divider (A; proof and place-and-phase B), the clock with a tail (A).
  Narrowed: the gun census at C = 35 double-counted; the divider's oscillator can be destroyed from the wire by
  one cell (the lead re-ran `research/audit/signals4/hole_oracle.py`); a second divider never divides again; the
  turn-class negative is for period-2 ends, T ≤ 36; the SAT negatives hold one wire phase unless stated.
  **Running:** only the lead's CPU run of the 84-cell face. **Next:** site content (nine tori, the wrapping
  result, signals pushes 3–4) and the draft, one Opus agent each; merge of pull request 26 at that checkpoint.
  **16:04 UTC:** the site agent is adding that content now (plates for the nine tori, the cost of a short way
  round, the gun, the divider, the third push; record and landing pages). **The draft (`docs/paper/`) is
  deliberately not updated yet:** the wrapping question turns on the 84-cell face and the card's runs, and the
  fourth push is a day old; update it once those settle.
  **16:22 UTC: the 84-cell face is measured and recorded** (the lead's CPU run; notebook "the 84-cell face with one
  loop of 12"; CLAIMS WL3 rewritten; forecasts W7 scored, W11 and W12 frozen; GPU-QUEUE note): 17.3248 ± 0.0058;
  the exponential form and the first law are refuted, the power form held, and each girth has its own straight
  line (0.2044, 0.2060, 0.2072 per cell against 0.2086). **Owed:** the card's 84-cell value as the cross-check
  and its 108-cell face as the test of a bend; the site agent's report on the new plates, then rebuild, check
  and republish the private artifact.
  **16:34 UTC: the overview is version 15** (nine tori, the new plate "What a short way round costs", live plates
  for the gun and the divider, third-push tiles, record and landing pages; the site agent's commits f2f7b66 …
  10f7a40; both check suites pass for the lead; 89 files on the private artifact). The ledger's count paragraph
  is corrected to the tally: 179 claims, A 86, B 82, C 10, D 1 (WL3's best grade is now B). **Nothing is running.**
  **Waiting on:** the card (hull face of 108 cells, about 02:00 UTC on the 16th; then the 84-cell tube as the
  cross-check and the 108-cell tube); the owner's two clicks if the site is to be public.
  **16:37 UTC: pull request 26 is merged** (main at 1a7ac0a; `research/check.sh` 20 of 20 and CI green at the
  merged head). The next pull request from this branch starts with this line.
  **16:39 UTC: pull request 27 is open (the lead's), and a fifth signals push is running** (Opus, about two and a
  half hours; the one question is a listener: a standing object left in a different lasting state by a gap in
  the stream than by none; the lead's forecasts S22–S26 are in `research/signals/PREDICTIONS.md`; it writes
  README sections 26 on). **Owed on its report:** re-run its verifiers, the lead's own oracle check of any new
  object, an adversarial review, notebook, CLAIMS rows, score S22–S26, OPEN-PROBLEMS 13, journal, essay, site.
  Usage: the owner's reading at 15:18 UTC was 62% weekly, 73% Fable; reckoned now about 67% and 78%. The Fable
  window moves only with the lead's own turns (every agent since 15:15 is Opus).
  **18:26 UTC: the fifth push has reported: no listener.** (README sections 26–29, commits d9ee117 … e340fa0.) A
  three-copy SAT search is UNSAT in the 3 × 3 tube (planes C = 29 … 39); a census of 741 ends of the stream:
  599 heal every word of holes, 142 die on every word, nothing else; beside the stream (samples, and the divider
  at every place and phase for N = 16) a gap heals or destroys. **Running:** the lead's own check
  (`research/audit/signals_ends_lead_check.py all i/3`: every end, three words, `reference/oracle.py` only,
  whole-state equality; output `research/scratch/audit/ends/part*.txt`), and an Opus adversarial review
  (`research/audit/REVIEW-signals-5.md`, code `research/audit/signals5/`), which also sends the ends every other
  one-unit change of a rake. **Owed when both are in:** notebook entries, CLAIMS rows SG23 on, the lead's scoring
  of S22–S26, OPEN-PROBLEMS 13, the owner's journal, the essay, the site's signals page and a republish.
  **18:28 UTC: a study of the living state on tubes is running** (Opus, about two hours, `research/wraplocal/`):
  which local property of a living tube tracks its lower price per cell, and why the effect ends between loop² 19
  and 21 (open problem 9 (a), (b)). The lead's forecasts L1–L5 are at the end of `research/wrap/PREDICTIONS.md`.
  **Owed on its report:** the lead's own check of its key number, a review if it claims an explanation, notebook,
  CLAIMS, score L1–L5, OPEN-PROBLEMS 9, the essay, the site's "What a short way round costs" plate.
  **20:27 UTC: the fifth push, its review and the tube study are recorded** (notebook: "the fifth signals push",
  "why a tube is cheaper", "the fifth signals push reviewed"; CLAIMS WL4–WL6 and SG23–SG27, 187 claims: A 89,
  B 84, C 13, D 1; open problems 9 and 13; the owner's journal; the essay). In short: no listener among 741 ends
  (the lead ran every end on the oracle, for holes and for the second kind of gap); the review found an **echo**
  (the receiving cap with an oscillator beside it sends a hole back up the stream as a three-cell signal; the
  lead's own oracle check passes); a living face is less dense for every loop round it, smoothly in the loop's
  length, and the tube discount is 1.85 times the deficit (the lead re-measured five densities). **W13 is frozen
  and queued for the card** (the 84-cell face with loops of 21 and 28). **Running:** the sixth signals push (the
  echo: meetings with holes at every phase, a gun that survives it; the lead's forecasts S27–S32), and a site
  agent (the density-law plate, a live echo plate, tiles and counts). **Owed:** on the site agent's report, both
  site check suites, a look at the screenshots, and a republish (version 16); on the push's report, its
  verifiers, the lead's own oracle check, an adversarial review, the records; then `research/check.sh`, CI and a
  merge of pull request 27. Usage is reckoned near 74% weekly and 82% Fable (no reading since 15:18 UTC).
  **21:00 UTC: the overview is version 16** (the site agent's commits 343555c, 29e5482: the plate "What a short
  way round costs" rewritten around the density law with a new figure and the W13 tile as queued; a live plate
  "An echo"; a plate "Nothing listens" with the four kinds of end; tiles, the record's counts and "Open now";
  both check suites pass for the lead, who looked at the three plates; 93 supporting files on the private
  artifact). To fill in later: `dens.w13measured` in `site/collect/sources/update-2026-11-15f.json` when the card
  has measured the face. **Running:** the sixth signals push only.
  **21:50 UTC: the sixth push has reported; nothing is running; no agent may be started.** Its account is README
  sections 30–35 (four signals on the stream, two each way; U meets K0 cancels exactly; E or U meeting a hole
  turns the stream into wire B, spreading; no gun survives an echo within bounds; no loop, no listener). Its
  verifier and the lead's own oracle check (`research/audit/signals_meet_lead_check.py`) pass; the notebook has a
  provisional entry and the lead's scoring of S27–S32. **`get_session` showed `rate_limit_info.status`
  "allowed_warning", type `seven_day_overage_included` (the Fable window), at 21:50 UTC**: by the rule in
  `LEAD.md` no agent is started until the owner gives a reading or uses the second Fable reset. **Owed, in
  order, once usage allows:** (1) an Opus adversarial review of the sixth push (`research/audit/REVIEW-signals-6.md`,
  code `research/audit/signals6/`; brief as for the fifth: own encoding of the gun and reflector SAT negatives,
  the meeting table by its own stepper, the 68 guns, the "for ever" argument for the fronts, wording); (2)
  CLAIMS rows SG28 on, open problem 13, the owner's journal, the essay, the site's signals page, a republish;
  (3) the card's results (fetch `origin/claude/gpu-local-1080`: the hull face of 108 cells about 02:00 UTC on the
  16th, then the 84-cell tube, W13's face, the 108- and 96-cell tubes) with a new pull request for its branch;
  (4) `research/check.sh`, CI, merge pull request 27.
  **22:13 UTC: the owner's reading is 72% weekly, 84% Fable; the adversarial review of the sixth push is
  running** (Opus, about two hours; `research/audit/REVIEW-signals-6.md`, `research/audit/signals6/`; its first
  item re-examines the events the fifth review classed as breaking the train that in fact make an up-signal).
  Items (2) to (4) above follow its report. The lead keeps its own turns to that work and stops near 90% Fable.
  **23:08 UTC: the sixth push is reviewed and recorded** (notebook "the sixth signals push reviewed"; CLAIMS
  SG28–SG32; open problem 13 (q)–(t); the owner's journal; the essay). Nine rigid signals; the meetings and the
  endless fronts proved; no gun survives an echo; the fifth review's unfollowed events leave every end equal;
  no listener, no loop. `research/check.sh` 20 of 20 at 23:08. **Still owed:** the site's signals page (the nine
  signals, the meeting table) and a republish; merge of pull request 27; the card's results.
  **01:01 UTC (2026-11-16): the overview is version 17** (the site agent's commits 2a778c4, b3b3e49: a live plate
  "When signals meet" on a ring of the plain train with four experiments, the nine signals, the echo and "Nothing
  listens" plates brought up to date, the record's counts at 192; both suites pass for the lead; 95 supporting
  files). **Nothing is running.** Next: merge pull request 27; then the card's results.
  **01:06 UTC (2026-11-16): pull request 27 is merged** (main at ec358d9; `research/check.sh` 20 of 20 and CI
  green at the merged head 5d5d033). The next pull request from this branch starts with this line. **Nothing is
  running. Waiting on the card:** the hull face of 108 cells (due about 02:00 UTC), the 84-cell tube (W11), the
  84-cell face with loops of 21 and 28 (W13; then fill `dens.w13measured` for the site), the 108- and 96-cell
  tubes (W12). At each wake-up: `git fetch origin claude/gpu-local-1080`, read its new rows, score, record, and
  open a new pull request for its branch. Usage at the owner's last reading (22:10 UTC on the 15th): 72% weekly,
  84% Fable; since then one Opus review, one Opus site update and the lead's turns for them.
  **A sustained Fable agent on open problem 13 (can anything carry a signal?) was started 07:16 UTC** at the
  owner's suggestion (`research/signals/`: README is its standing account, the lead's forecasts S1–S5 in
  PREDICTIONS.md). When it hands back: read its README, have a second agent try to break any positive finding,
  record, and start a successor from its README if work remains and usage allows.
  **The owner's journal** (`docs/OWNER-JOURNAL.md`, first note 07:54 UTC) asks how much of its state space a seed
  explores: **a state-space study was started 07:56 UTC (Opus)** -> `research/statespace/README.md` (exact maps
  for listable vessels, the 2012 cubes, entropy per cell of a living face, against a random map; the lead's
  forecasts E1–E7). On its report: lead's check of one exact count, an adversarial re-enumeration, then the
  record, an essay paragraph and a line under the journal note.
  **Round 4 of the dying-face study is running** (experimenter started 05:50 UTC; also applies the seven round-3
  README corrections). **Overview published 05:52 UTC (version 11)** with the plate "How a face dies, watched".
  Owed on each message from it: the lead's recomputation, an adversarial review with independent code, then the
  record. Queue for
  it, in this order, each with forecasts already committed where noted: (0) the acceptance bar of
  `research/gpu/README.md` (bit-exact against the engine every generation) on that card; (1) the guard against
  unrecognised settled replicas (`research/gpu/AGENT.md`, "To do"), tested on a planted long-period cycle, before
  any lifetime run; (2) equilateral tori at constant shape, A = 93 first (`research/constant/PREDICTIONS.md` part C);
  (3) the hull face at A = 108 to 10⁴ deaths; (4) T_d faces at A = 759 (`research/theory/symmetric/PREDICTIONS.md`,
  S3 and S5); (5) the 4×5 and 5×5 empty patches on different hardware; (6) the equal-loop pairs at A = 84 (the
  lead's conjecture in the notebook entry "the second variable"); (7) the runs that have no bound on unrecognised
  settled replicas, repeated with the guard (R15, R17 first). Each result needs the same checks as a Modal one: the
  lead's recomputation, an adversarial review, then the record.
- **State at 11:30 UTC, 2026-11-14 (after a compaction).** Done since 10:30 and recorded: the exponent study
  (reviewed, corrected, notebook, CLAIMS X1-X3), the swarm's close, the essay section "Coins will do", the second
  revision of `class.md`. **Pull request 16 (GPU: the shape of a periodic face) is merged** (squash bad62e3, 12:05 UTC) after its
  review (`research/audit/REVIEW-gpu-pr16.md`), the lead's re-derivation (`research/audit/gpu_pr16_lead_check.py`)
  and seven text fixes: notebook entry "equal areas, different lifetimes", CLAIMS GP9. Offered to the GPU session as
  optional and only if cheap: about 2,500 face deaths at 5×8×8, which would decide between "offset in the short side"
  (every family 0.2072) and "term in the long side" (b(5) = 0.2081). **The twisted-torus experiment is done, reviewed and recorded** (`research/shape/README.md`,
  `research/audit/REVIEW-shape.md`, notebook entry "the shortest way round", CLAIMS SH1, SH2): at equal area the
  lifetime of a periodic face rises with its shortest closed loop (two independent codes); at A = 60 a second
  variable shows (two tori with the same shortest loop differ by 0.0142 ± 0.0019 over four runs, CLAIMS SH2; first published as 0.019 ± 0.004). The review's seven corrections are applied to the write-up (6f995a2). (i) **the census of tori is done** (`research/shape2/README.md`; every class at A = 48 and
  60, five more at 72; forecasts first): none of the candidate laws holds at all three areas; the cost per cell
  depends on the shortest loop (0.11, 0.14, 0.19 at loop² 3, 4, 7; 0.205-0.21 from 12 up); at A = 48 the shortest
  loop stops mattering above √12; a second variable at equal shortest loop shows again (0.0142 ± 0.0019 at A = 60, 0.0151 ± 0.0017 at A = 48; CLAIMS SH2). Lead's check of the tables: `research/audit/shape2_lead_check.py`. **Reviewed (18:05 UTC) and recorded**:
  `research/audit/REVIEW-shape2.md` (independent stepper; claims 1-4 stand with corrections; no law passes at any
  area; the A = 60 pair is 0.0142 ± 0.0019 over four runs); notebook entry "every torus of a given area"; CLAIMS
  SH2 (corrected), SH3-SH5. The review's corrections are applied to `research/shape2/README.md` (9ffb393) and the
  overview carries the census (ab66ba7; published 18:20 UTC, version 6). **Overview refreshed and published again 01:48 UTC
  2026-11-15 (version 7, 705f59d):** new plates for the second variable, the thinnest face, the one-constant
  question with the empty patches, and lives that settle unrecognised (the period-16 state ticks on the page);
  prior art, swarm, checks, milestones and "Open now" brought up to date. `docs/paper/draft.md` is now
  draft 2 with the same results (4008b80, e88f889, bb22eda; its number check: 263 of 270 numbers in the cited row
  or entry, 7 from the earlier draft, none unsourced); the six disagreements it traced are applied (notebook entry
  "corrections found while the manuscript draft was brought up to date"; CLAIMS TH7, CN2; ledger 126 rows).
  **The audit of the C-graded ledger rows is done and applied (03:57 UTC, 13f8732):** 28 rows re-run, 26 matched;
  ledger now A 57, B 65, C 10, D 1; P4 restated (ξ = 0.65 ± 0.03 cube; refitted by a second agent, `research/audit/REVIEW-p4.md`), a sentence of ZL2 corrected; notebook
  entry "the audit of the rows nobody had re-run"; the lead's own checks: `research/audit/p4_lead_check.py` and
  Z10's basin count. The overview's counts and "Open now" list are updated and republished (version 10, e126a10).
  **Started 04:02 UTC (Opus), two agents:** (1) an editor bringing `docs/paper/draft.md` in line with the audit's
  grades (releases "preliminary" markers on rows now B; P4, P6, F2, F11 wordings; items for the lead in
  `docs/paper/FOR-LEAD.md`); (2) an experimenter looking at dying faces, `research/dying/` (occupancy of a face
  and its neighbours in the generations before it dies, c1, csz, c2v, D2h at A = 63; the lead's forecasts L1-L7
  are in its `PREDICTIONS.md`, committed before the runs; figure `research/figures/dying_face.png`). On (2)'s
  report: the lead recomputes one number from its data, an adversarial review with independent code, then the
  notebook, the ledger and the overview. **(1) is done** (f96774d, 23258d7; its items applied; P4 then refitted by
  a second agent, `research/audit/REVIEW-p4.md`: ledger A 57, B 65, C 10, D 1). **(2) reported at 04:18 UTC
  (75e5212, 616212f), not yet recorded:** a face does not erode from an edge; it fades everywhere at once in the
  last 20 generations; a tied edge is thinner at all times (rim-row occupancy 0.51 free, 0.30-0.35 tied; the
  stationary population falls 2.5 cells per tied edge, as ln τ falls 2.17); the lead's forecasts L2-L7 failed.
  The lead's recomputation: `python3 research/audit/dying_lead_check.py` (same populations; 0.86 in ln τ per
  stationary live cell lost, twice the untied face's 0.436). **Started 04:23 UTC (Opus):** the adversarial review
  of round 1 -> `research/audit/REVIEW-dying.md`, `research/audit/dying/`; and round 2 by the same experimenter
  (what starts a collapse: excursion rates and committor by level, single deaths uniform or holes, births or
  deaths first, the same at A = 84; the lead's forecasts A1-D2 in its `PREDICTIONS.md`; figure
  `research/figures/dying_excursions.png`). Owed after both: notebook entry, ledger rows, the essay's "Where I was
  wrong", an overview plate with the figure. **Round 2 reported at 04:35 UTC (6d40e72, 3bf2f21, 4b41de0), not yet
  reviewed or recorded:** ln τ = −ln(ν q) at every level, where ν(p) is the rate of dips of a face's population to
  the fraction p of its mean and q(p) the fraction of those that end in death; dips to 0.7 are equally frequent in
  all four groups; the point of no return is at about 2.5 live cells in c1; ln ν is Gaussian down to about half
  the mean and then falls in a straight line (the lead's recomputation, `python3 research/audit/dying_lead_check.py`:
  0.499 per live cell lost in c1, 0.436, 0.350, 0.231 with one, two, three tied edges, that is 5.5 + 3.4 per free
  edge per unit p); births fail before survival; depleted faces are lopsided whether or not they die; adjacent
  faces share their rim row, so round 1's "neighbour dragged down" is mostly the same cells; ln τ = 3.43 +
  0.582·P̄²/(2σ_P²) fits the eight lifetimes at A = 63 and 84 within 0.31. Of the lead's round-2 forecasts one of
  seven held. **The round-1 review is in and recorded (04:41 UTC):** `research/audit/REVIEW-dying.md`, confirmed with corrections (the population steps are not equal; "0.86 per live cell" is not a constant; single deaths are lopsided; the neighbour finding is mostly shared cells; 36.5% of old living D2h states are settled); notebook entry "how a face dies (the first look, reviewed)", ledger DY1-DY3 (136 claims: A 60, B 65, C 10, D 1). The same reviewer was resumed for round 2 at 04:39 UTC. **The round-2 review is in and recorded (04:53 UTC):** "Round 2" of `research/audit/REVIEW-dying.md` (e5153ea): the dip bookkeeping, the equal shallow-dip rates and the point of no return (0.079 of the mean in c1) confirmed by a second stepper; the lead's straight-line tail and "5.5 + 3.4 per free edge" not confirmed; the stationary-state fit is a description, not a law; notebook entry "a death is a dip that keeps going", ledger DY4-DY7 (140 claims: A 64, B 65, C 10, D 1). **Round 3 reported at 04:57 UTC (27890b4, aef6d86), not yet reviewed or recorded:** the dip curve per cell of face is one curve across A = 63, 84, 108 for p ≥ 0.4 once a size-independent rate of shallow dips (about one per ten generations per face) is taken out ([ln ν(0.9) − ln ν(0.5)]/A = 0.068, 0.067, 0.065, 0.066 at A = 45-108); the tail's price per live cell lost is 0.50-0.51 at A = 63-108; extrapolated to p = 0 the dips give 0.19-0.20 per site, below c, with end points still rising with size (the lead's reading, unreviewed: an end effect of about 2.4 in ln τ at every size); a depleted face is one loose patch; a thin csz face holds on away from its tied edge; a rim-free face torus of 63 cells lives 13.13 ± 0.04 against 13.64. Lead's forecasts: T3, T4 held; T1a, T1b, T2 failed. Figure `research/figures/dying_ratefunction.png`. **Its review started 05:00 UTC (Opus, a fresh reviewer reusing the earlier review's steppers)** -> "Round 3" of `research/audit/REVIEW-dying.md`. **Owed:** an editor applies the reviews' README corrections (twelve so far) once round 3's are in; the round-3 record; the essay, the overview plate and the draft. **A third round
  was started at 04:38 UTC** (same experimenter; the lead's forecasts T1-T4 in its `PREDICTIONS.md`; figure
  `research/figures/dying_ratefunction.png`): the same ν(p) curves at other sizes, to see whether −ln ν / A is one curve (then
  the constant is its value at zero and can be read on faces too big to die), and maps of deeply depleted faces
  (a live clump and a hole?). Earlier, **started 02:04 UTC (Opus):** that audit ->
  `research/AUDIT-2026-11-15.md`; a naturalist identifying the 37 long-period
  settled states of `research/audit/shape3/zombie_states.txt` against the catalogue -> `research/clockwork/`. **The owner reset the Fable
  window at about 20:28 UTC** (0.00 at 20:29; words in `LEAD.md`, "Watching usage"). **Started 20:33 UTC:**
  (1) Fable, **done 21:36 UTC**: second-reader audit of the counting line, `research/theory/swarm/audit/AUDIT-counting.md`:
  nothing tagged proved is wrong (19 correct, one gap filled, two wordings narrowed; one constant corrected,
  c₂(0.472) = 0.466846); notebook entry and CLAIMS SW6 written; an Opus editor is pasting the corrected wordings into
  `swarm/counting/claims.md`;
  (2) Fable, **reported 23:26 UTC, reviewed 01:30 UTC 2026-11-15 and recorded** (`research/theory/thin/README.md`;
  `research/audit/REVIEW-thin.md`: own stepper; six claims stand, some with corrections; the headline's error bar
  does not: the limit is about 0.099 per cell, 0.093–0.107 depending on the correction form; seven corrections being
  applied by an Opus editor; notebook entry of 2026-11-15 "the thinnest face"; CLAIMS TH1–TH6, ledger 124 rows): no
  number was derived from the rule. Measured instead: the
  census's 0.115/0.111 are local slopes of a ring law that is still bending (0.1086, 0.1063, 0.1034 at A = 78, 90,
  102); four routes extrapolate to 0.099 ± 0.004 per cell; noise is enough on the thin torus from five layers
  (+0.006 ± 0.003); every exactly solvable closure is wrong in slope (one layer over coins +22%); the face dies by
  an island shrinking from its ends. The lead checked the ring slopes by arithmetic from the line's lifetimes. It
  also reports two bugs of the "life that stops dying unrecognised" kind in its own stepper (fixed there): the same
  failure must be ruled out for the census, the pairs and the GPU kernel (settled states of long period);
  (3) Fable, **done 20:52 UTC**: a manuscript-style draft for an outside reader, `docs/paper/draft.md` (results graded
  A or B only; section "What is new here and what is not"), with `INCONSISTENCIES.md` (34 places where the repository
  disagrees with itself) and `GAPS.md` (38). Nothing leaves the repository. An Opus editor is resolving the
  inconsistencies (items in STATUS/NOTEBOOK come back as `docs/paper/FOR-LEAD.md` for the lead to apply); done 21:22 UTC
  (24 fixed, the lead applied the STATUS/NOTEBOOK parts from `docs/paper/FOR-LEAD.md`; notebook entry "consistency
  corrections"; the ledger's class rows K1-K3 are now K9-K11 and its tally was recounted: 108 rows, A 40, B 40,
  C 27, D 1). The Opus fact-check of the draft is done (`docs/paper/FACTCHECK.md`: 30 discrepancies, 14 fixed there; the lead's
  decisions on the other 16 are applied, e2fd0ed…5123855: the twist lemma's missing step is written out and read by
  the lead, F5 and SH4 reworded, a failed forecast added as SW7; notebook entry "corrections from the fact-check"). It found that three results called "apparently new" (the boundary layer over noise,
  the shape dependence, sealed sets) never had a prior-art search: the librarian's third pass is done
  (`research/PRIOR-ART.md`, "Third pass"; notebook entry "prior art, third pass": the noise method is known from
  coupled-map lattices but no lifetime comparison was found; the shape dependence has an equilibrium analogue in
  Ising interface tunnelling; sealed sets are blocking words; the tail formula exists, Sugimura–Kori 2015). The Opus
  adversarial pass is done (notebook entry "what the adversarial review changed": the shortest loop of a torus
  controlling a lifetime is proved for Ising tunnelling, Nardi–Zocca; boundary-controlled death and the tail formula
  are known; sealed sets are a 9-core, added to `docs/AUTOMATON.md` as a remark). The draft's novelty section and `GAPS.md` now follow
  both passes (aa1ea02; ranking unchanged, claims narrower). The lead's conjecture from it (wrap-around = a sum over period
  vectors, decaying over a correlation length) is in the notebook and was sent to the analyst of (6) with a blind
  test on the pairs of (4);
  (4) Opus, **reported 00:15 UTC 2026-11-15, reviewed 00:53 UTC and recorded** (`research/shape3/README.md`;
  `research/audit/REVIEW-shape3.md`: own stepper, the sign change confirmed, "survives out of sample" struck, seven
  corrections being applied to the write-up by an Opus editor; notebook entries of 2026-11-15 "the second variable"
  and "lives that settle and are not recognised"; CLAIMS SH6–SH9, ZL1, ZL2; ledger now 118 rows,
  `python3 research/audit/claims_tally.py`): the second variable was not found. At A = 72
  the differences at equal shortest loop are zero within 1.5σ (−0.006, +0.001, +0.002, each ± 0.004–0.006) where
  A = 48 and 60 gave +0.015 and +0.007; below saturation (shortest loop² 9) the sign changes (A = 36: −0.0223 ±
  0.0007; A = 45: +0.0076 ± 0.0013). The three size-free candidates are refuted; the two that decay with the second
  direction forecast "nearly zero" at 72 and cannot be told from zero. Proved along the way: at equal area and equal
  shortest loop one number fixes the lattice, so candidates can differ in size only. The lead recomputed the pair
  table from the raw counts (`python3 research/audit/shape3_lead_check.py`). It also met "zombie lives" (a settled
  state whose period does not divide 840 is never recognised; +0.017 in ln τ at A = 36 with no age cap; fixed by a
  multi-lag test): the reviewer bounded the bias in the capped census and pairs runs (≤ 0.0007 in ln τ, below every error), and the GPU session was asked
  (00:20 UTC, code reading only, no Modal spend) how its kernels treat such replicas. **Answered and merged as pull
  request 20 (text only; squash fc1383b, 00:31 UTC):** its kernel detects periods 1–2 and, in most runs, up to 128;
  no age cap; bounds on undetected exposure from the committed logs by run (`python3 research/gpu/zombies.py`;
  weakest: R13 ≤ 6.7e-3 against ± 0.005, symc R43 s501, slab 4×8×8; runs shorter than one mean life, R15 and R17
  among them, rest on a rate argument marked not proven); no published number changes. The lead recomputed the R11
  and R13 bounds (`python3 research/audit/gpu_pr20_lead_check.py`). Recorded in the notebook (2026-11-15) and as CLAIMS ZL2. Owed before any
  further GPU lifetime run: the guard described in `research/gpu/AGENT.md` (needs the GPU to test).
  (6) Fable, **reported 22:10 UTC, reviewed 22:30 UTC, recorded** (`research/constant/README.md`,
  `research/audit/REVIEW-constant.md`; notebook entry "is there one asymptotic cost per cell"; CLAIMS CN1): the
  data allow one asymptotic constant anywhere from about 0.207 to 0.219 and do not fix it; the analysis's "two
  families in tension" did not survive review (a single constant passes with a 1/A or saturating hull correction).
  The lead's image-sum conjecture is refuted as a law. The analyst applied the review's corrections (3fbd2a1; notebook addendum: readings
  with c ≤ 0.214 need a two-term hull correction, readings with c ≥ 0.2155 need a 1/s approach on periodic faces). The lead re-ran `fit.py` and
  checked the inputs (width slopes, hull local slopes). Its three proposed measurements: equilateral tori at constant
  shape (about 3 GPU-hours; to be asked of the GPU session once its forecasts are committed), hull faces of equal
  area and different rim, the width-6 slope. Original brief: is there one asymptotic constant? Joint analysis of every family of lifetimes
  (periodic by width, twisted, hull, symmetric), models stated before fitting, out-of-sample scores, a blind forecast
  for the GPU patch experiment -> `research/constant/`.
  **Dropped from the queue (01:05 UTC 2026-11-15):** the CPU run of the equilateral tori at A = 57 and 63 described
  next. The pairs experiment (4) shows irregular differences of 0.007–0.02 between tori of equal area and equal
  shortest loop at A ≤ 60, the size of the signal that run was to detect (+0.013), so it could not decide between
  the readings; the decisive point is A = 93 on the GPU. As queued before:
  Queued for when two cores are free (the pairs experiment or the thin line ends): the equilateral tori
  (1,7),(0,19) and (1,4),(0,21), A = 57 and 63, to ± 0.003 on the CPU. The analyst's forecasts for the whole family
  under three readings are committed (`research/constant/PREDICTIONS.md` part C, 6c21dbd); these two points are the
  part of that test a CPU can reach (massive reading: both about +0.013 above the 4×4–5×5 chord; flat: on it;
  rising: below). A = 93, the most decisive point, needs the GPU and the owner's word on the Modal budget.
  **Started 01:05 UTC 2026-11-15 (Fable):** a line on the symmetric collapse (PROGRAM M5: derive 1/6, the
  −0.196·√A term and the factor 1.5 between centres from the asymmetric law; forecasts first; CPU only) ->
  `research/theory/symmetric/`. **Reviewed 03:15 UTC and recorded** (`research/audit/REVIEW-symmetric.md`: own
  stepper on the unreduced system; the edge ladder and the centring pairs confirmed; "rim, not mirror" stands only
  in a weaker form, "bends" is open, the √A agreement is not a test; notebook entry "the symmetric collapse";
  CLAIMS S5–S9 and notes on S2, S3; essay paragraph in "Where I was wrong"; an Opus editor is applying eleven
  corrections to the write-up). Still owed: overview plate and draft section for this result. As first reported
  (02:50 UTC): no derivation of the O_h law. Proved: a symmetric state is gump on the
  orbit graph; inside a {111} face only diagonal mirrors exist; a coordinate mirror swaps two hull faces and fixes
  their shared rim row. Measured: the deficit is **not** a mirror-line term (a mirror or threefold axis on a rim-free
  slab face lengthens life); it sits on the rim, where edge-sharing faces die together (one, two, three edges in
  lockstep at A = 63: −2.18, −4.34, −6.47; inversion −0.056); rim cost 0.45–0.55 per period, which gives a √A
  coefficient of −0.19 to −0.22 without the fit; the rim term may bend, so −0.196·√A may not be asymptotic; the
  factor between centrings has a fixed part present with no symmetry and a growing part. 40 forecast statements scored, 25
  held. The lead re-ran `validate.py` (ALL OK) and `report.py` (table D reproduces; the asymmetric A = 63 value
  13.634 agrees with the known 13.632). **If this stands, the essay's and the notebook's "penalty along its mirror
  lines" is wrong and must be corrected** (essay section "Where I was wrong"; notebook entries of 2026-11-12).
  Owed after the review: notebook, CLAIMS (S rows qualified), essay correction, overview, draft. The 37 settled states of period 9–52 kept in
  `research/audit/shape3/zombie_states.txt` are identified (02:22 UTC; `research/clockwork/README.md`, "Found by
  accident"; notebook entry "what the unrecognised settled states are"; CLAIMS Z12, Z13; lead's check
  `python3 research/audit/clockwork_zombies_lead_check.py`): five new finite clocks, one a 4 × 13 compound of
  period 52; 21 wires and 2 sheets that exist only because a small torus lets a line close on itself.
  (5) GPU session, asked 21:22 UTC: empty patches on a face too large to die (12×12×8). **Pull request 18 arrived
  21:48 UTC** (head fcb3f39): the two-term fit gives c = 0.264 and fails (χ² 3,369/3), so the lead's forecast as
  stated is missed; cost per cell 0.42 → 0.32 over 12–60 cells, still falling; no hits above 75 cells. Lead's
  recomputation done (`research/audit/gpu_pr18_lead_check.py`: table reproduced; post hoc second differences give
  0.273, 0.252, 0.237, 0.2185 ± 0.008). Opus adversarial review running -> `research/audit/REVIEW-gpu-pr18.md`. Then:
  fixes by message, CI, merge (full sha), fetch main, notebook, CLAIMS. **The GPU session's Modal budget is nearly
  spent (about $25.80 of $30 this month): no further GPU request without asking the owner.**
  Reviewed 23:25 UTC (`research/audit/REVIEW-gpu-pr18.md`: merge after eight text fixes; the table is confirmed by an
  independent CPU stepper up to 4×4; the 4×5 rhombus is 1.9–2.6σ lower on the CPU, and the reviewer is lengthening
  that run; "well above the lifetime range" compared an incremental cost that includes perimeter). Fixes applied by the
  GPU session (de00831), read against the list by the lead, CI green, **merged 23:31 UTC (squash 5d62eae)**; main
  merged into the branch; notebook entry "empty patches on a face too large to die"; CLAIMS GP10. **The 4×5
  point is settled (05:15 UTC 2026-11-15):** the reviewer's CPU rerun at 0.9 of the GPU's exposure gives −23.412 ±
  0.049 against −23.318 ± 0.047 (1.4σ); the last cost per cell becomes 0.226 ± 0.006 with both combined, about 1σ
  above the lifetime range ("already inside it" withdrawn); notebook addendum of 2026-11-15, CLAIMS GP10 (now A to
  4×5), two sentences of `research/gpu/README.md` corrected by the lead. Owed: the overview's patch plate and
  "Open now" item, and the draft (§7.5), still carry the old figures.
  Owed for each when it reports: the lead's own check of one key number, an adversarial review (Opus) for (2) and (4),
  notebook, CLAIMS, STATUS. Usage timer every 60 minutes while Fable agents run.
  (ii) done: `README.md` (item 4 reworded; new items 8-10) and the web tour and
  face-table note now agree with today's entries (f4410be; web suite 79/79, check.sh 20/20; the lead read the diff).
  Left as they are: the "~10⁴¹" extrapolation (labelled as one), "twelve times" (lifetime) and "ten times" (first
  face) for side 16, which are different quantities. The audit's corrected wordings are in `path/claims.md` (a0508c8; one number
  in P's illustration stays in the journal as written, corrected in the audit). Owed: the same audit for counting and the theory push on the
  constant (Fable, after the owner's reset; Fable was 0.90 at 15:22). (b) the overview page is current to the entry "the shortest way round": refreshed
  twice today (9b5dc03, 010c908) and republished to the same private link (`LEAD.md`) at 14:59 UTC. Pull request 15 (the lead's) was merged at 15:01 UTC (merge commit dd66e9e); pull request 17 (census, audits, draft, prior art, the constant) was merged at 22:18 UTC (merge commit 47af1a6); pull request 19 (the constant, the second variable, lives that settle unrecognised) was merged at 00:59 UTC 2026-11-15 (merge commit 0e3b642); pull requests 18 and 20 were the GPU session's (empty patches; bounds on unrecognised settled replicas), both merged. Pull request 21 (the symmetric collapse corrected, the new clocks, the audit of unchecked rows, the GTX 1080 queue) was merged at 04:00 UTC 2026-11-15 (merge commit 0d47928); later work on the branch goes to a new pull request. **After the owner's Fable reset** (about 9am their time,
  probably 16:00 UTC; Fable was at 0.86 at 11:24, so nothing new on Fable before it): the fresh-reader audit of
  counting and path, and a new theory push on the sharpened problem (the 0.2 per cell from six layers over noise).
- **Swarm: closed 2026-11-14** (`research/theory/swarm/critic/board.md`, closing table at the top; notebook entry
  "the theory swarm is closed"). No proof of the area law and no derivation of the constant. Stands: a deterministic
  relative with an exponential law (audited; CLAIMS SW1); exact reductions and a conditional area law for gump
  (path's P̄ and Theorem Q on a measured hypothesis; one critic, no second reader); the fixed-age theory of soups
  (counting). Exam: five hold, four fail or missed, two undecided, three not run (C-E3, path E4, P-E4). **Owed, and
  worth Fable after the owner's reset:** a fresh-reader audit of counting's and path's proved claims; then, as a new
  effort, the sharpened problem (the constant from five or six layers over noise: transfer matrices at finite depth,
  the committor of the population table).
- **`research/theory/class.md`**: attacked 2026-11-14 (`research/audit/REVIEW-class.md`; notebook entry of that date).
  Its theorems stand; its first clause does not (sealing is a property of a half-space, not a direction), and the
  edge-neighbour rule the owner meant to write in 2012 (there called `face12e`; not gump) turned out to be a gump in a
  box, which class.md as written called unconfined. **Revised 2026-11-14** (commit 569be8d, an Opus successor; all
  twelve items of the review's §5.2 applied; every change listed in the file's last section; the lead read the new
  summary, Theorem A′ with its proof and the change list, and ran nothing). The class is now seven tagged clauses:
  confinement by sealed half-spaces, no finite sealed set, no armoured set, the two-sided drive (all proved; armour
  conditional), whole-wall death and hull lifetimes (measured), and one conjecture; the old fifth clause is withdrawn.
  Two tallies the reviser could not reconcile are flagged in its §10 (26/29 against 23/27 for b/K ≤ 3/8).
  **To do:** run what the repaired clause newly admits and nobody has run
  (kagome8 and hex9 at b = 4; whether bond10's b = 3 boxes ever die; kagome B2/S12 with transverse cuts censored);
  face12e with symmetric seeds and beyond 6³. The owner's quick-look branch `claude/edge-neighbour-tangent` stays
  unmerged; the audited face12e results live in `research/audit/class/` under that name.
- **`research/theory/exponent.md`**: written, reviewed (`research/audit/REVIEW-exponent.md`, 10:45 UTC) and in the
  notebook (2026-11-14, "where the exponent lives"; CLAIMS X1–X3). Stands: five or more layers of gump over coin flips
  reproduce a slab face's lifetime to 0.015 at A = 27–60 and 0.02 ± 0.04 at A = 75 (reviewer's own code), eight rows of the 2D rule likewise (lead's own
  code). Does not stand as written: the empty-window formula as more than a fit, "coincidence", the per-live-cell
  cost, the small-vessel inference. The review's thirteen corrections are applied (commit 0e8e5ec, an Opus editor; its §14 lists every change and two
  inconsistencies in the review itself). To do: update `research/theory/PROGRAM.md` (M1–M4: the problem is now a
  finite-depth probabilistic automaton) and `research/OPEN-PROBLEMS.md` items 3–4.
- **Class follow-up: done 2026-11-14** (`research/theory/class/followup/`; notebook entry of that date; CLAIMS K6–K8;
  the lead re-derived the symmetric face12e boxes). Half-space confinement holds out of sample; hex9 B456/S3456 is a
  new gump-type rule with a concave wall law; bond10's box walls hold each other up along the edges (boxes of 4³ live
  ≈ 10⁹ against 10³ forecast from the slab law); face12e with full cubic symmetry settles in tens of generations.
  **Folded into class.md** (second revision of 2026-11-14, commit 7d4cb8a, an Opus editor; the lead read the new
  clause 6; three small inconsistencies are listed in its last section, among them that the follow-up's and the
  lead's symmetric-box medians differ by one generation, probably a definition of "lifetime"). **Open question it
  raises:** an edge term for box walls (bond10 columns give 0.52–0.66 nats per edge cube; gump's octahedral rim is
  0.84 ± 0.04 nats at A = 108 with the pooled slab value).
- **GPU session:** pull request 12 reviewed 2026-11-14 (`research/audit/REVIEW-gpu-pr12.md`; notebook entry of that
  date). Stands: symmetric soups do not age at R = 43 (Weibull k = 1.02); cube-like seeds at vertex-centred R = 40 wait
  exponentially; rim-free slab faces are on the old line through A = 108, and an octahedral face there is 0.91 nats
  tougher. Does not stand: "the rise is a rim effect" and the slope 0.204 from 108 to 126 (the 6×7×8 run counts
  firewalls as peels; about a fifth of its deaths). The session made the five wording fixes (its commit 3cfab59; the
  lead read the diff) and **pull request 12 was merged 2026-11-14 (time of the merge commit: `git log -1 --format=%cI 07743dd`)**. It is now running the same slab with
  firewalls detected (`research/gpu/fwslab.py`; forecast and two validation targets committed first in
  `research/gpu/PREDICTIONS.md`: firewall-first share 10–30%, ln τ_face(126) = 26.30 ± 0.15). Expect a pull request;
  review it as before (does its validation at 3×6×8 and 4×7×8 reproduce `slab_fw.csv`?), re-derive one number, merge.
  At about 07:50 UTC the session was idle (its runs were due about 07:45); the lead messaged it: restart its branch from
  main, score the run against the forecast, data per death in `research/data/gpu_facelaw/`, censor every period,
  then a control at 6×6×8 with the firewall channel resolved. It cannot reply: look at its branch
  `claude/awesome-cray-boq9vz` and the pull request list from time to time.
  **Pull request 14 merged 2026-11-14, 09:50 UTC** (firewall-resolved slabs; review `research/audit/REVIEW-gpu-pr14.md`;
  notebook entry of that date; CLAIMS GP8): 6×7×8 face 26.405 ± 0.104 (all three forecasts hit), 6×6×8 22.568 ± 0.041,
  slope 108 → 126 0.215 ± 0.006, not decided between a rising cost per cell and a *width* effect (the review's post hoc
  fit with a short-side term). **Running at the GPU session (asked 09:40 UTC):** the pair 4×9×8 against 6×6×8 at
  A = 108 (a width effect predicts 0.23 ± 0.08 lower), and width families s = 3 … 6 at A ≤ 96 with ≥ 2,000 deaths
  each; forecasts first. Expect pull request 16 (15 is the lead's own, opened 09:57 UTC); review as before.
- **Exam (swarm): done 2026-11-14** (`swarm/exam/OUTCOMES.md`; notebook entry of that date; CLAIMS SW2–SW4). Hold (of the examiner's eight sampled entries):
  path E1 (notched edge 0.346), source S-E1 and S-E2 (faces over dice; six layers suffice for gump), counting C-E1
  (one mirror halves the price, 0.1026 per cell). Fail: counting C-E2, path E3. Undecided: P-E1 (0.512 ± 0.012 on its
  refutation line 0.51; needs about 3.5 core-hours more at L = 38), path E2. New entries filed by the solvers since
  and not yet run: C-E3, path E4, P-E4.
- **Prior art:** Tél–Lai 2008 and Bramson–Neuhauser 1994 are unread (publisher pages refuse agents); the owner was
  told they could fetch them. `PRIOR-ART.md`'s older sections still hold "snippet only" items the library now covers.
- Lineage study: replicate the weak "slow variable" (copies remember their source, ρ ≈ +0.2) on other sources.
- The web viewer still quotes the flat-face law exp(−0.09 + 0.209·A) (`web/src/layers.js`, `main.js`, `tour.js`):
  true for slab faces at the sizes measured; octahedral faces cost up to 0.221 per cell. Decide whether to say so.
- Full web test suite has not been re-run since the tour text edits of 2026-11-13 (tour tests pass).
- Put the 2D toy in the web viewer/tour if it becomes the paper's lead example.
- Papers (PROGRAM, "Writing it up"): not started; the owner decides venue, authorship and disclosure.
- Pages deployment still needs the owner: Settings → Pages → Source "GitHub Actions".
- Not yet answered by the owner (asked once, in passing): which 2D rule and neighbourhood they found years ago.

## The storyline so far
1. Birth cannot cross a `{111}` plane (T2) ⇒ finite seeds are trapped in octahedral hulls; no
   spaceships. Measured front speeds into vacuum: 0.177 cube/gen on {100}, 0.165 on {110},
   exactly 0 on {111} — the octahedron is the growth shape.
2. The lattice is an ABC stack of kagome layers; ≥3 layers are needed to sustain chaos.
3. The chaotic state is a genuine phase: bulk density **0.4155** (tori of any size), isotropic,
   correlation length ≈0.7 cube, damage spreads as a sphere at ≈0.85 cube/gen. Mean field
   alone gives a 4-cycle; a small neighbour–neighbour correlation stabilises it.
   **O_h-symmetric seeds are different**: cells on mirror planes are depleted (≈0.31), so
   symmetric octahedra run at ≈0.39. Every legacy cube run is of this kind.
4. Chaos is metastable and dies only by irreversible `{111}` events, each a rare, sudden,
   memoryless collapse whose cost is exponential in the number of cells that must die:
   - **a face layer goes extinct (peeling)** — mean wait τ_face ≈ exp(≈0.21·A)
     generations, A = sites in the outer layer, over six decades; not one line: the first fit
     −0.09 + 0.209·A mixes slab widths (within a width family 0.2072, and a narrower face dies sooner; CLAIMS F4, GP9),
     octahedral faces are 1.7–1.9× tougher at A = 45–84 and 0.84–0.91 nats at A = 108, with local slopes rising to
     0.221 (GP1, GP7), periodic faces carry a shape term that depends on how the face closes on itself (SH1–SH5),
     and symmetric faces follow their own law (S2)
     (`research/figures/peel_face_law.png`; independently re-checked by the lead,
     `research/experiments/face_endgame_check.py`: −ln h/A = 0.2183 at A = 45, engine only);
   - **an interior 3-layer firewall** — ≈0.12 per cell of the band (≈0.36 per unit of
     cross-section), so it wins only where a cross-section is much smaller than a face:
     thin slabs (crossover at thickness ≈ width), never octahedra;
   - the bulk without faces (whole torus) is effectively immortal above ≈600 cells.
   **Symmetry is fatal**: an O_h-symmetric state has one fundamental domain of independent
   chaos (regions die in lockstep), effective face area roughly A/6 to A/8 (the early fit A/7.7, CLAIMS S1, is superseded beyond A ≈ 460; see S2 below). The side-13 cube lasts ~10⁵
   generations because it is symmetric; the same hull filled asymmetrically would hold each
   face ~10⁴¹ (the face law extrapolated fivefold in area; not measured). The legacy cube lifetimes n = 11–15 fall at unremarkable quantiles of the law's
   prediction. **n = 16 was predicted at 2.4×10⁸ (90%: 3.9×10⁷–6.3×10⁸) and lived
   2,919,617,676** (first face 2.36×10⁹, second 5.2×10⁸; ends as 12 × S8b on the axes;
   `research/data/cube16_*`). What was wrong: the cost per site in a symmetric face rises with
   face size, so "A/7.7" under-predicts beyond its fitted range; cube-centred O_h faces follow
   ln τ ≈ 0.698 + (0.209/6)·A − 0.196·√A to A = 693 (`research/fluct/sym_fit.py`), and
   vertex-centred ones (even cubes) are ≈1.5× tougher (A = 408–630; 2.0 ± 0.4 at A = 693 for fresh soups only; `sym_fit.py` prints 2.39 when the cube's own copies are pooled in).
   **Face death is the stationary tail, measured to one cell** (`research/fluct/README.md`):
   ln P(n = k) is straight down to k = 1, the death rate is its next point (h ≈ 0.6·P(n = 1)),
   62% of deaths are from a single cell, the usual 3-cell ember is one kagome triangle;
   −ln h/A → 0.2077 ± 0.0014 + 0.55/A [retired 2026-11-13: the fit missed its own data; measured local
   slopes rise to 0.221 at A = 135, limit unknown]. Path-splitting (FFS) does not help: the plunge takes
   ~10 generations. Brute force on an O_h orbit-reduced stepper (`research/fluct/fl.c`) does.
5. Debris is built from a small fauna: cubes, kagome hexagons, vertex stars (a sealed
   12-cell universe), hinged period-2 flippers, and rare clockwork up to period 66.
   **Long periods are short loops closed by a symmetry of their own box** (period = twist ×
   loop, twist ∈ {2, 3, 4, 6}): P66.27a = 2 × 33 (mirror), C48.24a = 6 × 8 (a screw),
   C36.33a = 4 × 9. Twisted loops are a steady 3–8% at every loop length, so the twist
   multiplies rather than selects; the longest plain loop is 35. Compound objects (249 of
   9,700 in the box census) are non-communicating sub-clocks on one frame
   (`research/clockwork/README.md`; notebook 2026-11-13).
6. In rule space (960 rules, B ⊆ {4..7}, S ⊆ {2..7}) torus chaos is common, but long-lived
   *confined* chaos is not, and gump is a **minimal** member of that region: remove any one
   count from B45/S345 and lifetimes collapse; add S2 or S7 and they grow ≥29× (those medians sit at the 10⁵ cap).

## Most recent
- PR #1 merged to main (everything above). The lead measured the fluctuations of living faces
  (`research/experiments/face_fluct.py`): the face law's 0.209 looks like the value at zero of
  a size-independent large-deviation curve (≈0.20 by extrapolation) — notebook, last entry.

- Side 16 is finished (2026-11-13). Forecasts from perturbed copies of the running cube
  (`research/fluct/PREDICTIONS.md`): first peel hit (median 2.2×10⁹, actual 2.362×10⁹);
  second peel missed by the clone run (mean 7×10⁷ confirmed three ways, actual stay 5.2×10⁸)
  and caught at the 95th percentile by the fit-only forecast. Side 17 is forecast at a
  first-plateau mean of 2.6×10¹⁰ (not run).
- **Open question, not a finding:** side 16's largest plateaus ran 2.8, 7.4, 2.6 and 1.2 ensemble means (the 7.4 is against
  the pooled 7.1×10⁷, which includes the cube's own copies; against fresh soups alone, 8.6×10⁷, it is 6.1). The
  "over-dispersion, P ≈ 0.01" over cubes 13–16 (`research/experiments/cube_vs_ensemble.py`) is post hoc — it
  includes the side-16 plateaus that suggested it; sides 13–15 alone give P ≈ 0.18 (audit, finding 1). The
  proper test is on fresh lineages: `research/lineage/`, and the GPU session's experiment 1. Hull radius 42
  itself is an ordinary size (fresh soups: τ = 7.1×10⁸, 45 deaths).
- `research/fluct/qsd.py` is unreliable for symmetric soups below R = 30 (settled debris
  counted as a living face); use the engine there.
- Clockwork study done (2026-11-13): 94 new oscillators in `research/clockwork/objects/`
  (ids `C<period>.<minpop><letter>`, not merged into the atlas catalogue); 22 of them are
  compound. Open: periods beyond 66 via 4- or 6-fold boxes; anything that carries a signal.
- Open: the asymptotic symmetric slope (is it exactly 0.209/6?); whether the cost per site of asymmetric faces levels off (it rises past A = 84 on octahedral faces, to 0.221 at A = 135, CLAIMS GP1; on slabs width matters, GP9).

- 2026-11-13: prior-art survey and adversarial second pass (`research/PRIOR-ART.md`): no automaton on this
  lattice found, no lifetime-versus-symmetry result found; cite Eppstein (arXiv 0911.2890) for confinement.
  Open problems consolidated in `research/OPEN-PROBLEMS.md`. Theory programme started
  (`research/theory/PROGRAM.md`); first result, the threshold lemma: gump is a symmetric threshold automaton
  except at overcrowded cells (n ≥ 6), so all non-period-2 behaviour needs overcrowding.

## Ideas not yet started
- Web: a gallery of atlas objects; a guided tour of the storyline.
- A write-up for humans (and one for agents) once the peeling law is quantitative.
- Side 17 closed cube (forecast written down; days on the engine, or a single-state
  symmetry-reduced stepper — `fl.c` is fast only for 64 states at once).
- B45/S3457 ("super-gump": ~100× lifetime per radius step) and glassy B45/S3456 as rules worth their own look.
