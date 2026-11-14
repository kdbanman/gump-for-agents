# Review of `research/theory/exponent.md` (adversarial, 2026-11-14)

Object: `research/theory/exponent.md` and `research/theory/exponent/` (theorems.md, PREDICTIONS.md, data, drivers),
as committed in 1d82192. Reviewer's code: `research/audit/exponent/` (all of it new and sharing no code with
`drv.c`, `xp.py`, `fg.c`, `game_check.py`; `lead_check.py` there is the lead's and was not used). Bulk output:
`research/scratch/audit_exponent/` (`results.jsonl` holds every run below with its seed, exposure, deaths,
censoring counts and hazard by age). Commands run from `research/audit/exponent/`.

Tags as in the report: [proved], [exact], [measured]. "Mine" = this review's runs, own seeds, own RNG.

## 0. Validation of the reviewer's tools

| check | command | result |
|---|---|---|
| graph builder (doubled coordinates, AUTOMATON §2) against `reference/oracle.py` | `python3 graphs.py validate` | torus H = 10, 60 generations equal; hull R = 9 in a padded oracle box, 60 generations equal; 12-layer slab 4 × 3 lifted periodically into a 64³ oracle box, 4,728 interior cells equal after 6 generations |
| bit-sliced C stepper `qs.c` against the numpy stepper of `graphs.py` | `python3 run.py validate` | hull R = 9, slab 4 × 4 × 12, hull model R = 11 w = 5, slab model 4 × 5 w = 5: 200 generations, 4 replicas each, identical |
| toy strip stepper `toygap.c` against a naive stepper written from theorems.md's definition | `python3 toycheck.py` | 16 × 128 and 7 × 128 strips, 40–300 generations, identical |
| the model graphs are the report's graphs | (one-off comparison with `xp.gump_model`, read only) | R = 7 w = 4, 5; R = 9 w = 4: same cells, same neighbour sets, same layers |

Death and censoring rules in `qs.c` (written from the report's definitions, §1 and board "Definitions"): a replica
starts from a soup of density 0.35 on the dynamic cells; a transition is *exposed* if the replica's age before it is
≥ T0 (200 for hulls and hull models, 300 for slabs); a death is a face layer empty after the step (each face that
dies counts); censored and reseeded, not counted: states equal to the state two generations back or to a snapshot
taken at every power-of-two age (Brent: catches every period), three consecutive dead layers inside the vessel, and
in slabs the three-layer oblique firewalls of the three other diagonals that wrap the torus (when the family has ≥ 4
distinct layers). ln τ = −ln(deaths / (faces × exposure)); error 1/√deaths (deaths are from independent replicas,
each death followed by a fresh soup, so this error is the right one here).

PLACEHOLDER
