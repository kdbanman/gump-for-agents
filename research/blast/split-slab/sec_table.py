#!/usr/bin/env python3
"""Tables of README section 9 from the per-cell path records in G/cells/ (see sections.py for the definitions).

    python3 sec_table.py            # prints markdown; also writes data/sections_full.txt (sections.py's full output)
"""
import contextlib, io, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sections  # noqa
C = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-slab', 'cells'))
TUBES = [(1, 12, 28), (1, 16, 36), (1, 18, 40), (1, 22, 48), (1, 30, 64)]
WIDE = [(1, 4, 21), (6, 0, 6), (8, 0, 8)]
KINDS = [('cells_%d_%d_%d_s5.txt', 'dying, dice chain (sampler)'), ('gump_%d_%d_%d.txt', 'dying, gump (natural deaths)'), ('null_%d_%d_%d.txt', 'LIVING, gump (null)')]
full = io.StringIO()
res = {}
for L in TUBES + WIDE + [(4, 0, 4)]:
    for pat, kind in KINDS:
        f = os.path.join(C, pat % L)
        if os.path.exists(f) and os.path.getsize(f) > 0:
            with contextlib.redirect_stdout(full):
                r = sections.analyse(*L, [f])
                print()
            if r.get('units', 0) > 0:
                res[(L, kind)] = r
open(os.path.join(HERE, 'data', 'sections_full.txt'), 'w').write(full.getvalue().replace(C + '/', 'G/cells/'))


def v(r, part, key, d=2):
    x = r.get(part, {}).get(key)
    if x is None:
        return 'n/a'
    return f'{x[0]:.{d}f} ± {x[1]:.{d}f}' if x[1] == x[1] else f'{x[0]:.{d}f}'


def rms(r, part, sep, key='msd'):
    x = r.get(part, {}).get(f'{key}{sep}')
    return f'{math.sqrt(x[0]):.2f}' if x else 'n/a'


name = lambda L: f'({L[0]},{L[1]}),(0,{L[2]})'
print('**9a. Tubes cut into sections of 2 lattice units (24 cells; 21 and 27-30 cells at 84 and 108 cells).**\n')
print('| cells | ensemble | units (deaths) | face-wide half-fall | sections with a half-fall | sections busting locally | section before -> after | busting sections per death | >= 1 section busts | spread of crash generations | distinct crash generations | r.m.s. difference, neighbours (2 units) | at 4 units | at half the tube |')
print('|---:|---|---:|---|---|---|---|---|---|---|---|---:|---:|---:|')
for L in TUBES:
    for pat, kind in KINDS:
        r = res.get((L, kind))
        if not r:
            continue
        ns = r['sec_ns']
        print(f'| {r["A"]} | {kind} | {r["units"]} ({r["deaths"]}) | {v(r, "face", "half")} | {v(r, "sec", "sec_half")} | {v(r, "sec", "sec_bust")} | {v(r, "sec", "sec_before")} -> {v(r, "sec", "sec_after")} | '
              f'{v(r, "sec", "nbust")} of {ns} | {v(r, "sec", "anybust")} | {v(r, "sec", "spread")} | {v(r, "sec", "distinct")} | {rms(r, "sec", 1)} | {rms(r, "sec", 2)} | {rms(r, "sec", ns // 2)} |')
print('\n**9b. Two halves (tubes: along the length; wide tori: across one period).**\n')
print('| cells | torus | ensemble | units | halves crash in different generations | spread 0 / 1 / 2 / >= 3 generations | r.m.s. difference | a half with a half-fall: at least one | both | half before -> after |')
print('|---:|---|---|---:|---|---|---:|---|---|---|')
for L in TUBES + WIDE:
    for pat, kind in KINDS:
        r = res.get((L, kind))
        if not r:
            continue
        print(f'| {r["A"]} | {name(L)} {"tube" if L in TUBES else "wide"} | {kind} | {r["units"]} | {v(r, "half", "differ")} | {v(r, "half", "d0")} / {v(r, "half", "d1")} / {v(r, "half", "d2")} / {v(r, "half", "d3")} | '
              f'{rms(r, "half", 1)} | {v(r, "half", "anyhalf")} | {v(r, "half", "allhalf")} | {v(r, "half", "sec_before")} -> {v(r, "half", "sec_after")} |')
print('\n**9c. Wide tori cut into four quarters.**\n')
print('| cells | torus | ensemble | units | quarters crash in different generations | spread 0 / 1 / 2 / >= 3 | distinct crash generations | quarters with a half-fall | all four | quarter before -> after |')
print('|---:|---|---|---:|---|---|---|---|---|---|')
for L in WIDE:
    for pat, kind in KINDS:
        r = res.get((L, kind))
        if not r or 'quarter' not in r:
            continue
        print(f'| {r["A"]} | {name(L)} | {kind} | {r["units"]} | {v(r, "quarter", "differ")} | {v(r, "quarter", "d0")} / {v(r, "quarter", "d1")} / {v(r, "quarter", "d2")} / {v(r, "quarter", "d3")} | '
              f'{v(r, "quarter", "distinct")} | {v(r, "quarter", "sec_half")} | {v(r, "quarter", "allhalf")} | {v(r, "quarter", "sec_before")} -> {v(r, "quarter", "sec_after")} |')
print('\n**9d. Deaths with NO face-wide fall of half the face: are they staggered busts? (tubes, sections of 2 units)**\n')
print('| cells | ensemble | share of deaths without a face-wide half-fall | their sections: half-fall | busting locally | section before | >= 1 section busts | >= half of the sections bust | spread of crash generations |')
print('|---:|---|---|---|---|---|---|---|---|')
for L in TUBES:
    for pat, kind in KINDS:
        r = res.get((L, kind))
        if not r:
            continue
        print(f'| {r["A"]} | {kind} | {v(r, "sec", "noface")} | {v(r, "sec", "nf_sec_half")} | {v(r, "sec", "nf_sec_bust")} | {v(r, "sec", "nf_sec_before")} | {v(r, "sec", "nf_any_bust")} | {v(r, "sec", "nf_halfplus_bust")} | {v(r, "sec", "nf_spread")} |')
print('\n**9e. Timing of the sections that do bust (pairs of sections that both have a half-fall): r.m.s. difference of crash generations by separation.**\n')
print('| cells | ensemble | ' + ' | '.join(f'{2 * k} units' for k in range(1, 5)) + ' |')
print('|---:|---|' + '---:|' * 4)
for L in TUBES:
    for pat, kind in KINDS:
        r = res.get((L, kind))
        if not r:
            continue
        ns = r['sec_ns']; ln = r['sec_len']
        print(f'| {r["A"]} | {kind} (sections of {ln:.2f} units) | ' + ' | '.join((rms(r, 'sec', k, 'msdb') if k <= ns // 2 else '') for k in range(1, 5)) + ' |')
print('\n**9f. Share of pairs of busting sections (both with a half-fall) that crash in the SAME generation, by separation.**\n')
print('| cells | ensemble | ' + ' | '.join(f'{2 * k} units' for k in range(1, 5)) + ' |')
print('|---:|---|' + '---|' * 4)
for L in TUBES:
    for pat, kind in KINDS:
        r = res.get((L, kind))
        if not r:
            continue
        ns = r['sec_ns']; ln = r['sec_len']
        print(f'| {r["A"]} | {kind} (sections of {ln:.2f} units) | ' + ' | '.join((v(r, 'sec', f'sameb{k}') if k <= ns // 2 else '') for k in range(1, 5)) + ' |')
