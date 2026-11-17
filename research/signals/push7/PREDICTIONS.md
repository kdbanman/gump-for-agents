# Seventh signals push: forecasts, written before any census result

Written 2026-11-17 05:15 UTC, before the enumerator was compiled or run. Not edited afterwards; outcomes are
scored in `README.md` (section "Forecasts scored").

Method chosen (because no SAT solver is installed on this machine): a transfer-matrix enumeration. A periodic
orbit of period dividing T inside the tube is a bi-infinite sequence of unit "columns" (one unit's cells over T
generations); the rule couples only neighbouring units, so ends are paths in a finite graph from the train's
state to the dead state. Time is re-gauged by two generations per unit so that the train is a fixed point and a
translation by one unit is a symmetry; ends up to translation and time shift are then exactly paths.

| # | forecast | p |
|---|---|---|
| 1 | The enumerator, run on the 3 x 3 tube at period dividing 4 and filtered to the planes C <= 37, reproduces exactly the 741 ends of the fifth push (after fixing whatever bugs the first run shows) | 0.85 |
| 2 | In the 3 x 3 tube at period dividing 4 the set of all ends (no plane bound) is infinite: the useful part of the graph has a cycle other than the train's and the dead state's self-loops | 0.55 |
| 3 | The 5 x 5 tube at period dividing 4 can be closed by this method for some length bound of at least 6 units beyond the train within the time available | 0.5 |
| 4 | The 5 x 5 census, where closed, has more than ten times as many ends as the 3 x 3 census at the same bound | 0.6 |
| 5 | (a) A listener (survives a hole, K0 or another down-signal, durably changed, train in front plain) is found in the new bounds | 0.07 |
| 6 | (b) An end that answers a hole with U and survives is found | 0.08 |
| 7 | (c) A gun in the 5 x 5 tube that survives the echo E is found (if the gun census is run at all) | 0.05 |
| 8 | (c) An end that stops the arriving lower edge of wire B and stands (a cap of wire B formed from an end of the train) is found | 0.15 |
| 9 | Every 5 x 5 end found heals or is destroyed by H (the dichotomy of the 3 x 3 tube persists) | 0.8 |
| 10 | Period 8 (ends of period exactly 8) adds no end in the 3 x 3 tube beyond C = 33 that is not of period 4 | 0.6 |
| 11 | At least one 5 x 5 end answers some down-signal with an echo (E, U or N1 sent up, end restored) | 0.35 |
