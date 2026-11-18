# research/blast/boom: the death rate of a wrapped face in two factors (boom, then bust)

Agent `boom` of the blast of 2026-11-18. Standing account; work in progress (first commit 04:02 UTC).

Method. `boom.c` (kernel of ../anatomy/an.c, validated again here against reference/oracle.py by `validate.py` on
every vessel) runs renewal lives of an 8-layer slab and books, exactly:

    1/tau = sum_{p >= L} nu(p) d(p),  L = ceil(A/2)
    nu(p) = share of face-generations with population p
    d(p)  = chance that a generation with population p is the *launch* of a death: the last generation with
            P >= L before the face is empty (every death has exactly one).

d is measured three ways: from the natural deaths, from clones of stored states with P = p (one flipped cell in
layers 4-5 of the 8), and from the one-variable Markov chain built on the run's own transition counts.

`sh run_a.sh` (steps 1-2), `python3 analyse.py NAME` -> `out/NAME.txt`. Results below are filled in as they arrive.
