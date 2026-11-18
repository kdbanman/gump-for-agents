"""Tables from the runs.  Usage: python3 table.py
1. brute force: ln tau of ring and box edges (mine and research/toy2d/data), local slopes, second differences;
2. exact surrogate: ln tau of rings and segments, local slopes, the gap, bust shares, upper tails."""
import os, re, json, math, glob
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, '..', '..', 'scratch', 'blast', 'toy')
def bf(g, L):
    fn = f'{S}/{g}{L}.out'
    if not os.path.exists(fn): return None
    m = re.search(r'lntau (\S+) err (\S+)', open(fn).read()); return (float(m.group(1)), float(m.group(2))) if m else None
print('== brute force, cross2 B34/S234: ln tau_edge (mine; toy2d file) ==')
fr = {r['L']: (r['lntau'], r['err']) for r in json.load(open(f'{H}/../../toy2d/data/law_cross2_B34S234.json'))['rows']}
fb = {r['L']: (r['lntau'], r['err']) for r in json.load(open(f'{H}/../../toy2d/data/law_cross2_B34S234_box_none.json'))['rows']}
comb = {}
for L in (12, 16, 20, 24, 28, 32, 36):
    row = [f'L={L:2d}']
    for g, f in (('r', fr), ('b', fb)):
        vals = [v for v in (bf(g, L), f.get(L)) if v]
        if vals:
            w = sum(1 / e ** 2 for _, e in vals); m = sum(v / e ** 2 for v, e in vals) / w; comb[g, L] = (m, w ** -0.5)
        row.append(('ring' if g == 'r' else 'box') + ' mine ' + (f'{bf(g, L)[0]:.4f}±{bf(g, L)[1]:.4f}' if bf(g, L) else '   -   ') + ' file ' + (f'{f[L][0]:.4f}±{f[L][1]:.4f}' if L in f else '   -   ') + (f' pooled {comb[g, L][0]:.4f}±{comb[g, L][1]:.4f}' if (g, L) in comb else ''))
    if ('r', L) in comb and ('b', L) in comb: row.append(f'box-ring {comb["b", L][0] - comb["r", L][0]:+.3f}±{math.hypot(comb["b", L][1], comb["r", L][1]):.3f}')
    print(' | '.join(row))
for g in 'rb':
    Ls = sorted(L for (gg, L) in comb if gg == g)
    sl = [(comb[g, b][0] - comb[g, a][0]) / (b - a) for a, b in zip(Ls, Ls[1:])]
    se = [math.hypot(comb[g, b][1], comb[g, a][1]) / (b - a) for a, b in zip(Ls, Ls[1:])]
    print(('ring' if g == 'r' else 'box ') + ' local slopes per cell (pooled): ' + ' '.join(f'{a}-{b}: {s:.4f}±{e:.4f}' for (a, b), s, e in zip(zip(Ls, Ls[1:]), sl, se)))
    print('      second differences (per 4 cells): ' + ' '.join(f'{(comb[g, c][0] - 2 * comb[g, b][0] + comb[g, a][0]):+.3f}' for a, b, c in zip(Ls, Ls[1:], Ls[2:])))
# two exits: split 1/tau by the bust share b (anat.py: a fall of >= L/2 within the last 6 steps)
try:
    J = json.load(open(f'{H}/data/anat.json'))
    print('\n== two exits (brute force): ln tau_flash = ln tau - ln b6, ln tau_other = ln tau - ln(1 - b6) ==')
    ex2 = {}
    for g in 'rb':
        for L in (12, 16, 20, 24, 28, 32):
            if f'{g}{L}' in J and (g, L) in comb:
                b = J[f'{g}{L}']['bust']['6']; n = J[f'{g}{L}']['deaths']; eb = math.sqrt(b * (1 - b) / n)
                ex2[g, L] = (b, eb, comb[g, L][0] - math.log(b), math.hypot(comb[g, L][1], eb / b), comb[g, L][0] - math.log(1 - b), math.hypot(comb[g, L][1], eb / (1 - b)))
        Ls = sorted(L for (gg, L) in ex2 if gg == g)
        print(('ring' if g == 'r' else 'box ') + '  L: b6, logit b6, ln tau_flash, ln tau_other')
        for L in Ls:
            b, eb, f, ef, o, eo = ex2[g, L]; print(f'   {L:2d}: {b:.3f}±{eb:.3f}  {math.log(b / (1 - b)):+.3f}  {f:.3f}±{ef:.3f}  {o:.3f}±{eo:.3f}')
        for nm, i in (('flash', 2), ('other', 4)):
            x = np.array(Ls, float); y = np.array([ex2[g, L][i] for L in Ls]); e = np.array([ex2[g, L][i + 1] for L in Ls])
            A = np.vstack([np.ones_like(x), x]).T / e[:, None]; cf, res = np.linalg.lstsq(A, y / e, rcond=None)[:2]; cov = np.linalg.inv(A.T @ A)
            print(f'   {nm}: ln tau = {cf[0]:.3f}±{math.sqrt(cov[0, 0]):.3f} + ({cf[1]:.4f}±{math.sqrt(cov[1, 1]):.4f}) L, chi2 {float(((A @ cf - y / e) ** 2).sum()):.1f}/{len(x) - 2}; local slopes ' + ' '.join(f'{(y[i + 1] - y[i]) / (x[i + 1] - x[i]):.3f}' for i in range(len(x) - 1)))
        x = np.array(Ls, float); lg = np.array([math.log(ex2[g, L][0] / (1 - ex2[g, L][0])) for L in Ls]); e = np.array([ex2[g, L][1] / (ex2[g, L][0] * (1 - ex2[g, L][0])) for L in Ls])
        A = np.vstack([np.ones_like(x), x]).T / e[:, None]; cf = np.linalg.lstsq(A, lg / e, rcond=None)[0]; cov = np.linalg.inv(A.T @ A)
        print(f'   logit b6 = {cf[0]:.3f}±{math.sqrt(cov[0, 0]):.3f} + ({cf[1]:.4f}±{math.sqrt(cov[1, 1]):.4f}) L, chi2 {float(((A @ cf - lg / e) ** 2).sum()):.1f}/{len(x) - 2}; b = 1/2 at L = {-cf[0] / cf[1]:.1f}')
    print('ring other - box other: ' + ' '.join(f'{L}: {ex2["r", L][4] - ex2["b", L][4]:+.3f}±{math.hypot(ex2["r", L][5], ex2["b", L][5]):.3f}' for L in (12, 16, 20, 24, 28, 32) if ('r', L) in ex2 and ('b', L) in ex2))
    print('box flash - ring flash: ' + ' '.join(f'{L}: {ex2["b", L][2] - ex2["r", L][2]:+.3f}±{math.hypot(ex2["r", L][3], ex2["b", L][3]):.3f}' for L in (12, 16, 20, 24, 28, 32) if ('r', L) in ex2 and ('b', L) in ex2))
    print('robustness to the window K (steps before the empty row in which the fall is looked for): slopes of the two exits')
    for g in 'rb':
        for KK in ('4', '6', '12'):
            Ls = [L for L in (12, 16, 20, 24, 28, 32) if f'{g}{L}' in J and (g, L) in comb]
            b = np.array([J[f'{g}{L}']['bust'][KK] for L in Ls]); y = np.array([comb[g, L][0] for L in Ls]); x = np.array(Ls, float)
            pf = np.polyfit(x, y - np.log(b), 1); po = np.polyfit(x, y - np.log(1 - b), 1); pl = np.polyfit(x, np.log(b / (1 - b)), 1)
            print(f'   {"ring" if g == "r" else "box "} K={KK:>2s}: flash {pf[1]:.2f} + {pf[0]:.4f} L; other {po[1]:.2f} + {po[0]:.4f} L; logit b slope {pl[0]:+.4f} per cell (unweighted fits)')
except FileNotFoundError:
    pass
def ex(pref, L):
    fn = f'{S}/{pref}{L}.out'
    if not os.path.exists(fn): return None
    t = open(fn).read(); d = {'lntau': float(re.search(r'lntau (\S+)', t).group(1))}
    d['pn'] = np.array([float(z) for z in re.search(r'pn (.*)', t).group(1).split()])
    d['fl'] = np.array([float(z) for z in re.search(r'deathflux (.*)', t).group(1).split()])
    d['dens'] = [float(z) for z in re.search(r'density (.*)', t).group(1).split()]
    d['bust'] = {int(a): (float(b), float(c)) for a, b, c in re.findall(r'bust K (\d+) share (\S+) living_window_Km1_transitions (\S+)', t)}
    return d
for name, pr, ps in (('cross2 B34/S234 row over coins 0.472 (ex1d)', 'xr', 'xs'), ('rule A: range 3, 3 coins 0.5, n+x>=4, n<=6', 'oAr', 'oAs'), ('rule B: range 1, 2 coins 0.5, n+x>=2, n<=2', 'oBr', 'oBs')):
    print(f'\n== exact surrogate: {name} ==')
    print(' L   lntau ring   lntau segment   seg-ring   slope ring  slope seg  slope diff | bust share K=1,2,4,6 ring / segment | living window (5 transitions) ring / segment')
    prev = None
    for L in range(6, 27):
        r, s = ex(pr, L), ex(ps, L)
        if not r and not s: continue
        f = lambda d, k: f'{d[k]:.7f}' if d else '     -    '
        gap = s['lntau'] - r['lntau'] if r and s else None
        line = f'{L:2d}  {f(r, "lntau"):>11s}  {f(s, "lntau"):>11s}  ' + (f'{gap:+.4f}' if gap is not None else '   -   ')
        if prev and prev[0] == L - 1 or prev and prev[0] == L - 2:
            dL = L - prev[0]
            sr = (r['lntau'] - prev[1]['lntau']) / dL if r and prev[1] else None; ss = (s['lntau'] - prev[2]['lntau']) / dL if s and prev[2] else None
            line += '   ' + (f'{sr:.4f}' if sr is not None else '   -  ') + '     ' + (f'{ss:.4f}' if ss is not None else '   -  ') + '    ' + (f'{sr - ss:+.4f}' if sr is not None and ss is not None else '   -   ')
        else: line += ' ' * 34
        b = lambda d: ' '.join(f'{d["bust"][K][0]:.3f}' for K in (1, 2, 4, 6) if K in d['bust']) if d and d['bust'] else '-'
        lw = lambda d: f'{d["bust"][6][1]:.4f}' if d and 6 in d['bust'] else '-'
        line += f' | {b(r)} / {b(s)} | {lw(r)} / {lw(s)}'
        print(line); prev = (L, r, s)
    rows = [(L, ex(pr, L), ex(ps, L)) for L in range(6, 27)]
    rows = [(L, r, s) for L, r, s in rows if r and s and 6 in r['bust'] and 6 in s['bust']]
    if rows:
        print(' two exits, exact (K = 6): L, ring ln tau_flash, ring ln tau_other, segment ln tau_flash, segment ln tau_other, ring other - segment other, logit b ring, logit b segment')
        for L, r, s in rows:
            br, bs = r['bust'][6][0], s['bust'][6][0]
            print(f'  {L:2d}  {r["lntau"] - math.log(br):.4f}  {r["lntau"] - math.log(1 - br):.4f}  {s["lntau"] - math.log(bs):.4f}  {s["lntau"] - math.log(1 - bs):.4f}  {r["lntau"] - math.log(1 - br) - s["lntau"] + math.log(1 - bs):+.4f}  {math.log(br / (1 - br)):+.3f}  {math.log(bs / (1 - bs)):+.3f}')
        ev = [(L, r, s) for L, r, s in rows if L % 2 == 0 and L >= 12]
        if len(ev) >= 2:
            (L0, r0, s0), (L1, r1, s1) = ev[0], ev[-1]; d = L1 - L0
            f = lambda d_, K: d_['lntau'] - math.log(K(d_['bust'][6][0]))
            print(f'  slopes {L0}-{L1}: ring flash {(f(r1, lambda b: b) - f(r0, lambda b: b)) / d:.4f}, ring other {(f(r1, lambda b: 1 - b) - f(r0, lambda b: 1 - b)) / d:.4f}, segment flash {(f(s1, lambda b: b) - f(s0, lambda b: b)) / d:.4f}, segment other {(f(s1, lambda b: 1 - b) - f(s0, lambda b: 1 - b)) / d:.4f}')
    print(' upper tail of the quasi-stationary population: -ln P(n >= x L)/L at x = 0.75, 0.875, 1 (ring / segment), and mean density')
    for L in range(8, 27, 4):
        r, s = ex(pr, L), ex(ps, L)
        if not r or not s: continue
        t = lambda d, x: -math.log(d['pn'][int(math.ceil(x * L - 1e-9)):].sum()) / L
        print(f'  L={L:2d} ' + '  '.join(f'x={x}: {t(r, x):.4f} / {t(s, x):.4f}' for x in (0.75, 0.875, 1.0)) + f'   density {np.dot(r["pn"], np.arange(L + 1)) / L:.4f} / {np.dot(s["pn"], np.arange(L + 1)) / L:.4f}; segment end cells {s["dens"][0]:.3f} {s["dens"][1]:.3f} {s["dens"][2]:.3f}')
