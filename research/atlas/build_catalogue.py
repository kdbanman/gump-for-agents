#!/usr/bin/env python3
"""Assemble research/atlas/catalogue.jsonl from the search/soup outputs in research/scratch/atlas.
Every entry is re-stepped with reference/oracle.py (field "oracle_ok") before it is written.
  build_catalogue.py [--still-max N]
Entry fields: id, family (3d|kagome), period, pops (per phase), union (cells live in some phase),
cells (phase 0, doubled coordinates, canonical orientation; later phases follow by stepping), sym (stabiliser of phase 0 in
translations x O_h), spacetime_sym (pairs (g, shift) mapping the orbit to itself), layers (number of
{111} layers spanned along d=(1,1,1),(1,1,-1),(1,-1,1),(-1,1,1), of the union), strict (still lifes),
nbr_components, sources (exhaustive search / soup counts / legacy run), oracle_ok.
"""
import glob, json, os, re, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lattice import *  # noqa

SCR = os.path.join(HERE, '..', 'scratch', 'atlas')
STILL_MAX = 12
objs = {}   # key -> dict(phases, sources)


def add(phases, src, family='3d', count=1):
    phases = [frozenset(p) for p in phases]
    key = min(canon(p) for p in phases)
    o = objs.setdefault(key, dict(phases=phases, sources=Counter(), family=family))
    if family == 'kagome': o['family'] = 'kagome'
    o['sources'][src] += count


def read_osc(fn):
    for line in open(fn):
        head, body = line.split(' :', 1)
        per = int(head.split()[0])
        cells = [t.rsplit(':', 1) for t in body.split()]
        yield [frozenset(parse(c)[0] for c, b in cells if int(b) >> t & 1) for t in range(per)]


# 1. still lifes: strict ones up to STILL_MAX, all one-layer ones up to 16 (strong-mode search to 16)
for line in open(os.path.join(SCR, 'sl_strong_16.txt')):
    t = line.split(); n = int(t[0]); cells = parse(' '.join(t[1:]))
    if n <= STILL_MAX and is_strict_still(cells):
        add([cells], 'exhaustive-strict-still<=16')
    elif min(thickness(cells)) == 1 and is_strict_still(cells):
        add([cells], 'exhaustive-strict-still<=16', family='kagome')
# 2. exhaustive oscillators (largest N per period)
best = {}
for fn in glob.glob(os.path.join(SCR, 'osc_P*_N*.txt')):
    P, N = map(int, re.findall(r'P(\d+)_N(\d+)', fn)[0])
    if os.path.exists(fn.replace('.txt', '.err')) and 'axis 2 done' in open(fn.replace('.txt', '.err')).read():
        if N > best.get(P, (0,))[0]: best[P] = (N, fn)
for P, (N, fn) in best.items():
    for ph in read_osc(fn):
        add(ph, f'exhaustive-osc-P{P}-union<={N}')
for fn in glob.glob(os.path.join(SCR, 'kag_osc_P*_N*.txt')):
    P, N = map(int, re.findall(r'P(\d+)_N(\d+)', fn)[0])
    for ph in read_osc(fn):
        add(ph, f'exhaustive-kagome-osc-P{P}-union<={N}', family='kagome')
# 3. soups: oscillators of period >= 3, p2 seen twice or with <= 20 cells, still lifes seen >= 3 times
#    with <= 30 cells (aggregated over all harvest files)
agg = Counter()
for fn in glob.glob(os.path.join(SCR, 'harvest_*.json')):
    for per, key, c in json.load(open(fn))['objects']:
        agg[(per, key)] += c
for fn in glob.glob(os.path.join(SCR, 'harvest_*.json')):
    d = json.load(open(fn))
    for per, key, c in d['objects']:
        if per < 0: continue
        tot, n = agg[(per, key)], len(key.split())
        if per == 1 and (tot < 3 or n > 30): continue
        if per == 2 and tot < 2 and n > 20: continue
        S = frozenset(parse(key)); ph = [S]
        for _ in range(per - 1): ph.append(step(ph[-1]))
        add(ph, f'soup-octa-{d["centre"]}-R{d["R"]}-rho{d["rho"]}', count=c)
for line in open(os.path.join(SCR, 'kagome_soup.jsonl')):
    d = json.loads(line)
    for per, key, c in d['objects']:
        if per < 0 or len(key.split()) > 40: continue
        if per == 1 and (c < 3 or len(key.split()) > 20): continue
        if per == 2 and len(key.split()) > 24: continue
        S = frozenset(parse(key)); ph = [S]
        for _ in range(per - 1): ph.append(step(ph[-1]))
        add(ph, f'soup-kagome-N{d["N"]}', family='kagome', count=c)
# 4. legacy ash pieces (neighbour components and whole R-components)
la = json.load(open(os.path.join(SCR, 'legacy_ash.json')))
for side, r in la.items():
    for o in r['objects']:
        add([parse(o['key'])], f'legacy-side{side}')
        for k in o['sub_keys']:
            add([parse(k)], f'legacy-side{side}-piece')

def compact_sources(src):
    out = {}
    for k, c in src.items():
        if k.startswith('soup-octa'): out['soup_octa'] = out.get('soup_octa', 0) + c
        elif k.startswith('soup-kagome'): out['soup_kagome'] = out.get('soup_kagome', 0) + c
        elif k.startswith('legacy'): out.setdefault('legacy', []).append(k[7:])
        else: out.setdefault('exhaustive', []).append(k[11:])
    return out


# assemble
entries = []
for key, o in objs.items():
    ph = canonical_orbit(o['phases'])
    per = len(ph); U = frozenset().union(*map(frozenset, ph))
    th = thickness(U)
    fam = 'kagome' if min(th) == 1 else '3d'
    e = dict(family=fam, period=per, pops=[len(p) for p in ph], union=len(U),
             sym=sym_order(ph[0]), spacetime_sym=spacetime_sym(ph),
             layers=[(max(sum(a*b for a, b in zip(d, c)) for c in U) - min(sum(a*b for a, b in zip(d, c)) for c in U)) // 2 + 1 for d in DIAGS],
             strict=(is_strict_still(ph[0]) if per == 1 else None),
             nbr_components=len(components(U, 1)),
             sources=compact_sources(o['sources']),
             cells=[list(c) for c in ph[0]], phases=ph)
    e['oracle_ok'] = bool(oracle_verify(ph[0], per))
    entries.append(e)
entries.sort(key=lambda e: (e['family'] != '3d', e['period'], min(e['pops']), e['union'], -e['sym'], e['cells']))
cnt = Counter()
for e in entries:
    pre = ('K' if e['family'] == 'kagome' else '') + ('S' if e['period'] == 1 else f'P{e["period"]}.')
    base = f'{pre}{min(e["pops"])}'
    cnt[base] += 1
    e['id'] = f'{base}{"abcdefghijklmnopqrstuvwxyz"[cnt[base]-1] if cnt[base] <= 26 else "_" + str(cnt[base])}'
with open(os.path.join(HERE, 'catalogue.jsonl'), 'w') as f:
    for e in entries:
        f.write(json.dumps({k: e[k] for k in ['id', 'family', 'period', 'pops', 'union', 'sym', 'spacetime_sym', 'layers',
                                               'strict', 'nbr_components', 'sources', 'oracle_ok', 'cells']},
                           separators=(',', ':')) + '\n')
bad = [e['id'] for e in entries if not e['oracle_ok']]
print(f'{len(entries)} entries; oracle failures: {bad}')
print(Counter((e['family'], e['period']) for e in entries))
