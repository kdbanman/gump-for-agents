#!/usr/bin/env python3
"""The skin-depth table: rate and way of dying of the watched face when every cell at depth >= d is a fresh coin at its
layer's mean density in gump (full replacement).

    python3 research/blast/density/skin.py [DIR ...]        (row files; default data/rows)

Rows: tags R9_skinA_d*, R9_skinB_d* (45 cells), skinA_d*, skinB_d* (63 cells); column A = depth >= d under the watched
face and >= 3 under the others; column B = depth >= d under every face (B with d = 3 is A with d = 3). Against the gump
rows of the same size (63: gump_d1, lay_gump*; 45: R9_gump): Delta = ln tau - gump's (13.633 +- 0.001; 9.8177 +-
0.0036), and from the excursion counts: dips = descents from >= H to <= H - 1 per hull-generation (H = 16 at 63 cells,
11 at 45 cells: a quarter of the face), their deadliness = the share that end in death before the face is back at H,
and P1 = the share of descents to <= 1 cell that die. d ln are differences of logarithms from gump's; errors from counts.
"""
import glob, math, os, re, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
dirs = sys.argv[1:] or [os.path.join(HERE, 'data', 'rows')]
def load(f):
    t = open(f).read()
    br = [l for l in t.splitlines() if l.startswith('BRUTE')][0]
    rec = [l for l in t.splitlines() if l.startswith('REC')][0].split()
    H = int(rec[2]); R = {}
    for tok in rec[4:]:
        k, v = tok.split(':'); R[int(k)] = tuple(int(x) for x in v.split('/'))
    return dict(A=int(re.search(r' A (\d+)', br).group(1)), E=float(re.search(r'exposure ([0-9.e+]+)', br).group(1)),
                n0=int(re.search(r' watched (\d+)', br).group(1)), H=H, rec=R,
                Pbar=float(re.search(r'Pbar ([0-9.]+)', br).group(1)))
rows = {}; gump = defaultdict(list); seen = set()
for d in dirs:
    for f in sorted(glob.glob(os.path.join(d, '*.txt'))):
        b = os.path.basename(f); tag = re.sub(r'_s\d+\.txt$', '', b)
        if b in seen or '\nREC' not in '\n' + open(f).read(): continue
        seen.add(b)
        r = load(f)
        if tag in ('gump_d1', 'R9_gump') or tag.startswith('lay_gump') or tag.startswith('lay2_gump') or tag.startswith('lay3_gump'):
            gump[r['A']].append(r)
        if re.match(r'(R9_)?skin[AB]_d\d$', tag):
            rows[b] = (tag, r)
GREF = {63: (13.633, 0.001), 45: (9.8177, 0.0036)}
def agg(rs):
    E = sum(r['E'] for r in rs); N = defaultdict(int); D = defaultdict(int)
    for r in rs:
        for k, (a, b, c) in r['rec'].items(): N[k] += a; D[k] += b
    return E, N, D
print(f'{"row":14s} {"A":>3s}  {"Delta ln tau":>16s}  {"d ln dips":>10s} {"d ln deadliness":>15s}  {"P1":>14s}  {"mean face":>9s}')
for A in (45, 63):
    gE, gN, gD = agg(gump[A]); H = gump[A][0]['H']; k = H - 1
    print(f'{"gump":14s} {A:3d}  {GREF[A][0]:8.4f} (ref)      {"":10s} {"":15s}  {gD[1] / gN[1]:.4f} +- {math.sqrt(gD[1] * (1 - gD[1] / gN[1])) / gN[1]:.4f}   '
          f'(H = {H}; gump rows: {len(gump[A])}, dips {gN[k] / gE:.3e}, deadliness {gD[k] / gN[k]:.4f})')
    for b, (tag, r) in sorted(rows.items(), key=lambda x: x[1][0]):
        if r['A'] != A: continue
        E, N, D = agg([r]); v = math.log(r['E'] / r['n0']) - GREF[A][0]; e = math.hypot(1 / math.sqrt(r['n0']), GREF[A][1])
        dlf = math.log(N[k] / E) - math.log(gN[k] / gE); dlp = math.log(D[k] / N[k]) - math.log(gD[k] / gN[k])
        P1 = D[1] / N[1]; e1 = math.sqrt(P1 * (1 - P1) / N[1])
        print(f'{tag:14s} {A:3d}  {v:+8.4f} +- {e:.4f}  {dlf:+10.3f} {dlp:+15.3f}  {P1:.4f} +- {e1:.4f}  {r["Pbar"]:9.3f}')
