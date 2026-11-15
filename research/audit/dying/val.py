#!/usr/bin/env python3
"""val.py: dy.c against reference/oracle.py (trace mode, lane 0, full live set every generation) and against st.c
(run mode: lives file byte-identical).   python3 research/audit/dying/val.py  (-> val_out.txt; ~2 min)"""
import sys, os, subprocess, filecmp
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference')); sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'symmetric'))
import oracle, geo
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit_dying'); DY = os.path.join(SCR, 'dy'); ST = os.path.join(SCR, 'st')
ok = True
for sysname in ('v11c', 'v13c', 'v12v'):
    for gname in ('c1', 'csz', 'c2v', 'd2h'):
        S, nb, orb, gens = geo.build(sysname, gname); _, fg = geo.summary(S, nb, orb, gens, gname)
        gf = os.path.join(SCR, f'g_{sysname}_{gname}.txt'); geo.write(S, nb, orb, gf, fg)
        G = 600; seed = '77'
        tr = subprocess.run([DY, gf, 'trace', seed, '0.4', str(G + 1)], capture_output=True, text=True, check=True).stdout.splitlines()
        sets = [set(map(int, l.split()[1:])) for l in tr]
        H = 32; off = 16; m = oracle.masks(H)
        h = np.zeros((H, H, H), np.int8)
        for i in sets[0]:
            p = S.cells[i]; h[p[0] + off, p[1] + off, p[2] + off] = 1
        bad = None
        for g in range(1, G + 1):
            h = oracle.step(h, m); got = set(); extra = 0
            for q in zip(*np.nonzero(h)):
                p = tuple(int(v) - off for v in q)
                if p in S.idx: got.add(S.idx[p])
                else: extra += 1
            if got != sets[g] or extra:
                bad = g; break
        # run mode: lives file identical to st's
        a = os.path.join(SCR, f'vl_st_{sysname}_{gname}.bin'); b = os.path.join(SCR, f'vl_dy_{sysname}_{gname}.bin')
        subprocess.run([ST, gf, 'run', '5', '0.4', '20000', a], check=True, capture_output=True)
        subprocess.run([DY, gf, 'run', '5', '0.4', '20000', b, b + '.ext', b + '.smp', '1000', b + '.dmp', '50', '512', '512'], check=True, capture_output=True)
        same = filecmp.cmp(a, b, shallow=False); nrec = os.path.getsize(a) // 16
        print(f'{sysname} {gname}: oracle {G} gens ' + ('OK' if bad is None else f'MISMATCH at {bad}') + f' (final pop {len(sets[G])}); '
              f'lives file vs st.c 20000 gens x 256 lanes, {nrec} records: ' + ('identical' if same else 'DIFFERENT'), flush=True)
        ok &= bad is None and same
print('ALL OK' if ok else 'FAIL')
