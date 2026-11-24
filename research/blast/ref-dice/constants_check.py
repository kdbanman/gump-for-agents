#!/usr/bin/env python3
"""ref-dice: the scalars of the committed certificates (GumpMath/Dice*Data.lean, read as text) against my exact
lambda (numerics.py, Collatz-Wielandt enclosures of width <= 1e-34) and the constants stated in the theorems.
    python3 constants_check.py
"""
import re, os
from fractions import Fraction as Fr
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lean', 'mathlib', 'GumpMath')
# my lambda enclosures (numerics.py FACE; patch13 with ITERS=700), 25 digits
MY = {'Hull3': '0.9165673655948901373589070', 'Torus103': '0.9664099275695942426060723',
      'Torus113': '0.9324323935928482210249284', 'Strip13': '0.9391216736592712685176338',
      'Patch13': '0.8474738060566295030494555'}
# theorem constants (DiceX.lean): lower constant, upper constant, stated lambda interval, start state
TH = {'Hull3': ('0.72', '1384', '0.9165673655948901373', '0.9165673655948901374', 'full'),
      'Torus103': ('0.96', '3.07', '0.9664099275695942426', '0.9664099275695942427', '73'),
      'Torus113': ('0.71', '9.86', '0.9324323935928482210', '0.9324323935928482211', '73'),
      'Strip13': ('0.97', '512', '0.9391216736592712685', '0.9391216736592712686', 'full'),
      'Patch13': ('0.99', '1731', '0.8474738060566295030', '0.8474738060566295031', 'full')}
for f, (clo, cup, slo, sup, x0) in TH.items():
    txt = open(os.path.join(G, 'Dice%sData.lean' % f)).read()
    d = {k: int(v) for k, v in re.findall(r'^def (Lup|Mup|Llo|Mlo|vmin|vmax|wmax|wx|Kg|Ng) : ℕ := (\d+)', txt, re.M)}
    lup, llo, lam = Fr(d['Lup'], d['Mup']), Fr(d['Llo'], d['Mlo']), Fr(MY[f])
    ok_lam = llo <= lam - Fr(1, 10 ** 25) and lam + Fr(1, 10 ** 25) <= lup
    ok_dec = Fr(slo) <= llo and lup <= Fr(sup)
    lo_c = Fr(d['wx'], d['wmax'])
    up_c = Fr(d['vmax'], d['vmin']) + (Fr(d['Kg'], d['Ng']) * d['vmax'] / lup if 'Kg' in d else 0)
    print('%-8s lambda_lo <= my lambda <= lambda_up: %s (gaps %.1e, %.1e); stated decimals enclose: %s; '
          'x0 = %s: w(x0)/wmax = %.4f >= %s: %s; upper constant %.2f <= %s: %s'
          % (f, ok_lam, float(lam - llo), float(lup - lam), ok_dec, x0, float(lo_c), clo, lo_c >= Fr(clo),
             float(up_c), cup, up_c <= Fr(cup)))
