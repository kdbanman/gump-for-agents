"""Rigidity of the edges left by the meetings E-H, E-K0, U-H (README section 31): S(t + per) = S(t) moved per/2 units
down (lower edge) or up (upper edge) on a window of 12 units round each edge, t = 60..120 - per.
    python3 echo_rig.py   (about 1 min)"""
import sys
import echo6 as E, sg, meet6
for sigs in ([('E', 0), ('H', 21)], [('E', 0), ('K0', 20)], [('U', 1), ('H', 21)]):
    Ss, D, A = meet6.run(sigs, 120)
    for per in (4, 8, 12, 16):
        v = per // 2
        okl = oku = True
        for t in range(60, 120 - per + 1):
            ul = min(E.unit_of(c) for c in D[t]); uh = max(E.unit_of(c) for c in D[t])
            okl &= E.units(Ss[t + per], ul - v - 6, ul - v + 6) == E.units(E.trs(Ss[t], -v), ul - v - 6, ul - v + 6)
            oku &= E.units(Ss[t + per], uh + v - 6, uh + v + 6) == E.units(E.trs(Ss[t], v), uh + v - 6, uh + v + 6)
        print(sigs, 'period', per, 'lower rigid', okl, 'upper rigid', oku)
