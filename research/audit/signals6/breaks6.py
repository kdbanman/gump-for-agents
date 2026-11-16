"""A, rest: the scan's events that 'break' on the bare train (scan6a.bare at G = 102), followed to G = 202: do any
become signals later, and which way do they spread?  Prints, per class, the range of the difference relative to
the event's unit (review-5 frame: downstream = increasing unit) at G.

    python3 breaks6.py          (~1 min)
"""
from collections import Counter
import numpy as np
import scan6a as S6
from st6 import unit_of

ev = S6.events()
r1 = S6.bare(ev)
br = [j for j, r in enumerate(r1) if r[0][0] == 'break']
print(len(br), 'break at G = 102')
sub = [ev[j] for j in br]
r2 = S6.bare(sub, G=202, A=330)
print('at G = 202:', Counter(r[0] for r in r2))
