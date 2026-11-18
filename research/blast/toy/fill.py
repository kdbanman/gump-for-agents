"""Fill the EXACT_TABLE / OTHER_TABLE blocks of README.md from the exact outputs (markdown).  Usage: python3 fill.py"""
import os, re, math
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, '..', '..', 'scratch', 'blast', 'toy')
def ex(pref, L):
    fn = f'{S}/{pref}{L}.out'
    if not os.path.exists(fn): return None
    t = open(fn).read(); m = re.search(r'lntau (\S+)', t)
    if not m: return None
    return float(m.group(1)), {int(a): (float(b), float(c)) for a, b, c in re.findall(r'bust K (\d+) share (\S+) living_window_Km1_transitions (\S+)', t)}
def table(pr, ps, Ls):
    out = ['| L | ln τ ring | ln τ segment | segment − ring | slope ring | slope segment | flash share (6 steps) ring | segment |', '|---|---|---|---|---|---|---|---|']
    prev = None
    for L in Ls:
        r, s = ex(pr, L), ex(ps, L)
        if not r and not s: continue
        f = lambda v: f'{v[0]:.4f}' if v else '—'
        sl = lambda v, p: f'{(v[0] - p[0]) / (L - prev[0]):.4f}' if v and p else '—'
        b = lambda v: f'{v[1][6][0]:.3f}' if v and 6 in v[1] else '—'
        out.append(f'| {L} | {f(r)} | {f(s)} | ' + (f'{s[0] - r[0]:+.4f}' if r and s else '—') + ' | ' + (sl(r, prev[1]) if prev else '') + ' | ' + (sl(s, prev[2]) if prev else '') + f' | {b(r)} | {b(s)} |')
        prev = (L, r, s)
    return '\n'.join(out)
t = open(f'{H}/README.md').read()
t = re.sub(r'<!--EX-->.*?<!--/EX-->|EXACT_TABLE', lambda m: '<!--EX-->\n' + table('xr', 'xs', range(8, 27)) + '\n<!--/EX-->', t, flags=re.S)
A = table('oAr', 'oAs', range(8, 18, 2)); B = table('oBr', 'oBs', range(8, 18, 2))
t = re.sub(r'<!--OT-->.*?<!--/OT-->|OTHER_TABLE', lambda m: '<!--OT-->\n**Rule A** (range 3, 3 coins of density 0.5, alive iff n + x ≥ 4 and n ≤ 6; a segment\'s end cell has n ≤ 6: never overcrowded):\n\n' + A + '\n\n**Rule B** (range 1, 2 coins of density 0.5, alive iff n + x ≥ 2 and n ≤ 2; a segment\'s end cell has n ≤ 3: it CAN be overcrowded):\n\n' + B + '\n<!--/OT-->', t, flags=re.S)
open(f'{H}/README.md', 'w').write(t)
