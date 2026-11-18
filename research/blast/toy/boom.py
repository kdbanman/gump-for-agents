"""Second classifier of the flash exit: 'boom' = the row was at least 0.8 L full in one of its last 6 living
generations (deaths) / in a window of 6 generations (living).  Usage: python3 boom.py [L ...]  -> data/boom.json (no arguments: L = 12..32)"""
import os, json, math, re, sys
LS = [int(z) for z in sys.argv[1:]] or [12, 16, 20, 24, 28, 32]
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, '..', '..', 'scratch', 'blast', 'toy')
J = {}
for g in 'rb':
    for L in LS:
        fn = f'{S}/{g}{L}.rec'
        if not os.path.exists(fn) or not os.path.exists(f'{S}/{g}{L}.out') or 'lntau' not in open(f'{S}/{g}{L}.out').read(): continue
        thr = math.ceil(0.8 * L - 1e-9); nd = bd = nv = bv = 0; both = 0; fallonly = 0
        for line in open(fn):
            t = line.split()
            if len(t) != 18: continue
            p = [bin(int(z, 16)).count('1') for z in t[2:]]
            if t[0] == 'D':
                nd += 1; bo = max(p[-6:]) >= thr; bd += bo
                q = p[-6:] + [0]; fall = max(q[i] - q[i + 1] for i in range(6)) >= (L + 1) // 2
                both += bo and fall; fallonly += fall and not bo
            else: nv += 1; bv += max(p[-6:]) >= thr
        m = re.search(r'lntau (\S+)', open(f'{S}/{g}{L}.out').read()); lt = float(m.group(1))
        b = bd / nd; J[f'{g}{L}'] = dict(deaths=nd, boom=b, living=bv / max(nv, 1), boom_and_fall=both / nd, fall_without_boom=fallonly / nd)
        print(f"{'ring' if g == 'r' else 'box '} L={L:2d} deaths {nd:5d} boom share {b:.3f}±{math.sqrt(b * (1 - b) / nd):.3f} (living windows {bv / max(nv, 1):.4f}); boom and half-row fall {both / nd:.3f}; fall without boom {fallonly / nd:.3f}; ln tau - ln b = {lt - math.log(b):.3f}; ln tau - ln(1-b) = {lt - math.log(1 - b):.3f}; logit {math.log(b / (1 - b)):+.3f}")
if not sys.argv[1:]: json.dump(J, open(f'{H}/data/boom.json', 'w'), indent=1)
