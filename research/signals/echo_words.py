"""E against two holes s rakes apart (s = 3, 4, 5, 8): the units of the wire B that are not wire B, at generations
100..160 (README section 31: a stretch of wire B' at units s + 8 .. s + 10).
    python3 echo_words.py   (about 1 min)"""
import sys
import echo6 as E, sg, meet6
WB = [frozenset([(0,1,2),(0,1,4),(1,0,0),(1,0,2),(1,0,4)]), frozenset([(0,0,1),(0,0,5),(0,1,2),(0,1,4),(1,2,2)])]
for s in (3, 4, 5, 8):
    Ss, D, A = meet6.run([('E', 0), ('H', 21), ('H', 21 + 2 * s)], 160)
    for t in (100, 120, 140, 160):
        St = Ss[t]
        us = sorted({E.unit_of(c) for c in D[t]}); lo, hi = us[0], us[-1]
        # which phase of wire B matches most units
        bad = {}
        for ph in (0, 1):
            bad[ph] = [u for u in range(lo + 3, hi - 3) if frozenset(E.tr(c, -u) for c in E.units(St, u, u + 1)) != WB[ph]]
        ph = min(bad, key=lambda p: len(bad[p]))
        print(s, t, 'edges', lo, hi, 'wire B phase', ph, 'units not wire B:', bad[ph])
