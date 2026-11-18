# research/blast: why does a face die at the rate it does? (the night of 2026-11-18)

Standing account of the PI (the session in charge of the blast). One subdirectory per agent, each with its own
README; `BRIEF-COMMON.md` is what every agent was told; `PREDICTIONS.md` holds forecasts frozen before data;
`REPORT.md` is the account for the owner. Written to as results are checked; newest state at the top.

## State (03:20 UTC)

Wave 1 launching: eight Fable agents, one angle each.

## The front gas (the PI's reading at 03:31 UTC; conjecture; forecasts in PREDICTIONS.md block 1)

Arithmetic on anchors already on file (BRIEF-COMMON.md and `research/gpu-local/README.md`, chain 3):

    python3 -c "
    import math
    w=lambda a:13.1623+0.20861*(a-63)
    for a,v in ((54,11.1935),(60,12.4219),(72,14.8755),(84,17.3175),(96,19.7446),(108,22.1599)):
        D=w(a)-v; L=a/12; print(a, round(D,3), round(D/L**2,5), round(math.exp(D)-1,3))"

gives D/L² = 0.0045 … 0.0048 for tubes of loop² 12 over a factor two in length: the tube discount is quadratic in
length, and its coefficient falls with girth as e^(−2σg), σ ≈ 0.66 per lattice unit, the edge cost of an empty
patch. Reading: two-stage deaths through a band right round the girth; a gas of fronts.
