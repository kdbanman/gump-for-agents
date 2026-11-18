#!/usr/bin/env python3
"""Extras for THEORY.md: (a) tube against wide torus at the same size, (b) the 84-cell faces with their own map
where it is populated (n >= 200) and the 63-cell torus map, carried at equal fillings, elsewhere.
   python3 theory2.py -> out/theory2.txt"""
import os
os.environ['THEORY_OUT'] = 'theory2.txt'
import theory as th
D = {n: th.load(n) for n in ('t63', 't84', 'tube60', 'tube84', 't48', 'h63')}
q63, qtube = th.qtable('t63'), th.qtable('tube60')
th.pr('== tube against wide torus at the same size (each map at A = 60)')
th.chain(D['t63'], 60, label='t63 map at A = 60', qt=q63)
th.chain(D['tube60'], 60, label='tube60 map at A = 60', qt=qtube)
th.pr('== 84 cells: own map where populated, the 63-cell torus map elsewhere')
th.chain(D['t84'], 84, label='t84 own map + t63 map below', qt=q63, fb=D['t63'])
th.chain(D['tube84'], 84, label='tube84 own map + tube60 map below', qt=qtube, fb=D['tube60'])
th.chain(D['tube84'], 84, label='tube84 own map + t63 map below', qt=q63, fb=D['t63'])
th.pr('== 48 cells: own map in the living and over-full cells (x >= 0.35), the 63-cell torus map below (settled replicas spoil the low cells of t48)')
import numpy as np
d = dict(D['t48']); n = d['n'].copy(); n[:17, :] = 0; d['n'] = n
th.chain(d, 48, label='t48 own map (P >= 17) + t63 map below', qt=q63, fb=D['t63'])
th.out.close()
