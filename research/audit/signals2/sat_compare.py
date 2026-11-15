"""The study's SAT cap census (caps.enumerate_caps, research/signals/caps.py) against cap_brute.py's brute force.

    python3 sat_compare.py WIRE C [C ...]

This script imports the study's code ON PURPOSE: it is the encoding under test.  The brute force is this
directory's own.  Both lists are compared as sets of generation-0 cell sets on units >= KS = 6.
"""
import json, os, sys
import gs, cap_brute
sys.path.insert(0, os.path.join(gs.ROOT, 'research', 'signals'))
os.chdir(os.path.join(gs.ROOT, 'research', 'signals'))
import caps, scat  # noqa: E402  (the study's)
w = sys.argv[1]
ob = json.load(open(f'objects/pulse-{w}.json'))
wire = scat.Wire(ob, None)
for C in map(int, sys.argv[2:]):
    sat, status, nfree = caps.enumerate_caps(wire, C, 1, 5, 6, verbose=False)
    brute, nf = cap_brute.census(w, C, verbose=False)
    a = {frozenset(map(tuple, c)) for c in sat}; b = {frozenset(c) for c in brute}
    print(f'wire {w} C={C}: SAT {status}, {len(a)} caps ({nfree} free cells); brute force {len(b)} caps ({nf} free cells); '
          f'identical lists: {a == b}', flush=True)
    if a != b:
        print('   only SAT:', [sorted(x) for x in a - b][:3]); print('   only brute:', [sorted(x) for x in b - a][:3])
