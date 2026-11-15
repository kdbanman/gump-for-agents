#!/usr/bin/env python3
"""validate4.py (round 4): ex4.c against reference/oracle.py and against the review's r3_ex.c, on the three vessels.

    python3 research/dying/validate4.py        # -> research/dying/validate4_out.txt (a few minutes)

1. Trace mode (lane 0's whole live set at every generation) against oracle.step on the vessel in an open box:
   v11c (600 generations), v13c (600), v15c (400), c1 soups. (The trace code is r3_ex's, unchanged.)
2. Run mode, 20,000 generations x 256 lanes: ex4's lives file, excursion table (EXOUT) and stationary samples (SAMP)
   byte-identical to r3_ex's for the same arguments.
3. Catches (a run of 2,500 generations x 256 lanes, seed 6): r3_ex dumps every generation of every excursion that reaches L(0.9) (M3 = L_0); for each
   of ex4's records (all keep probabilities 1) the record of r3_ex with the same lane, orbit and start must exist, and
   ex4's state at every kept catch must equal r3_ex's state at the first dumped generation with popcount <= L_j, its
   catch offset and P likewise, its bottom state the first dumped state with popcount = minP; end type, minP and
   length must agree. Every record's catch P equals the popcount of its stored state.
Graphs: research/audit/symmetric/geo.py (the review's builder), written to research/scratch/dying/r4/g_*.txt.
"""
import sys, os, subprocess, filecmp
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference')); sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'symmetric'))
import oracle, geo
SCR = os.path.join(ROOT, 'research', 'scratch', 'dying', 'r4'); os.makedirs(SCR, exist_ok=True)
EX4 = os.path.join(SCR, 'ex4'); R3 = os.path.join(SCR, 'r3_ex')
subprocess.run(['gcc', '-O3', '-march=native', '-o', EX4, os.path.join(HERE, 'ex4.c')], check=True)
subprocess.run(['gcc', '-O3', '-march=native', '-o', R3, os.path.join(ROOT, 'research', 'audit', 'dying', 'r3_ex.c')], check=True)
out = open(os.path.join(HERE, 'validate4_out.txt'), 'w')
PBAR = {'v11c': 31.29, 'v13c': 42.49, 'v15c': 55.14}
PS = [0.9, 0.75, 0.6, 0.45, 0.3, 0.15]


def say(s):
    print(s, flush=True); out.write(s + '\n'); out.flush()


def graph(name):
    gf = os.path.join(SCR, f'g_{name}_c1.txt')
    S, nb, orb, gens = geo.build(name, 'c1'); _, fg = geo.summary(S, nb, orb, gens, 'c1'); geo.write(S, nb, orb, gf, fg)
    return S, gf


def read_r3(fn):
    raw = open(fn, 'rb').read(); i = 0; recs = []
    while i < len(raw):
        h = np.frombuffer(raw, np.int32, 8, i); i += 32; n = int(h[4])
        st = np.unpackbits(np.frombuffer(raw, np.uint8, 16 * n, i).reshape(n, 16), axis=1, bitorder='little'); i += 16 * n
        recs.append((h.copy(), st))
    return recs


def read_ex4(fn):
    raw = np.fromfile(fn, np.uint8).reshape(-1, 200)
    hd = raw[:, :88].copy().view(np.int32)
    st = np.unpackbits(raw[:, 88:].reshape(-1, 7, 16), axis=2, bitorder='little')
    return hd, st


ok = True
for name, G in [('v11c', 600), ('v13c', 600), ('v15c', 400)]:
    S, gf = graph(name)
    tr = subprocess.run([EX4, gf, 'trace', '77', '0.4', str(G + 1)], capture_output=True, text=True, check=True).stdout.splitlines()
    sets = [set(map(int, l.split()[1:])) for l in tr]
    H = 2 * (int(name[1:3]) + 6); H += (-H) % 4; off = H // 2
    m = oracle.masks(H); h = np.zeros((H, H, H), np.int8)
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
    say(f'{name}: oracle {G} gens ' + ('OK' if bad is None else f'MISMATCH at {bad}') + f' (final pop {len(sets[G])}, cells {len(S.cells)})')
    ok &= bad is None
    pb = PBAR[name]; L = [int(np.floor(p * pb)) for p in PS]
    a = os.path.join(SCR, f'vl_r3_{name}'); b = os.path.join(SCR, f'vl_ex4_{name}')
    subprocess.run([R3, gf, 'run', '5', '0.4', '20000', a + '.lives', '/dev/null', a + '.smp', '1000', '/dev/null', '0', '1', '512', str(pb), a + '.x', str(L[0]), a + '.dx'],
                   check=True, capture_output=True)
    subprocess.run([EX4, gf, 'run', '5', '0.4', '20000', b + '.lives', '/dev/null', b + '.smp', '1000', '/dev/null', '0', '1', '512', str(pb), b + '.x', b + '.cat',
                    ','.join(map(str, L)), '1,1,1,1,1,1', '12345'], check=True, capture_output=True)
    same = all(filecmp.cmp(a + e, b + e, shallow=False) for e in ('.lives', '.x', '.smp'))
    say(f'{name}: lives, excursion table, samples vs r3_ex (20000 gens x 256 lanes): ' + ('identical' if same else 'DIFFERENT'))
    ok &= same
    # catch check on a shorter run (r3_ex's every-generation dumps at M3 = L(0.9) are large)
    subprocess.run([R3, gf, 'run', '6', '0.4', '2500', a + '.lives', '/dev/null', '/dev/null', '100000', '/dev/null', '0', '1', '512', str(pb), a + '.x', str(L[0]), a + '.dx'],
                   check=True, capture_output=True)
    subprocess.run([EX4, gf, 'run', '6', '0.4', '2500', b + '.lives', '/dev/null', '/dev/null', '100000', '/dev/null', '0', '1', '512', str(pb), b + '.x', b + '.cat',
                    ','.join(map(str, L)), '1,1,1,1,1,1', '12345'], check=True, capture_output=True)
    r3 = read_r3(a + '.dx'); hd, st = read_ex4(b + '.cat')
    key = {}
    for h3, s3 in r3:
        key[(int(h3[0]), int(h3[1]), int(h3[6]))] = (h3, s3)   # lane, orbit, generation of first dumped state
    nchk = 0; nbad = 0; nlev = [0] * 6
    for r in range(len(hd)):
        lane, orb, end, minp, cm, km, ln, bo, a0, g0 = hd[r, :10]; cP = hd[r, 10:16]; cg = hd[r, 16:22]
        # popcount of stored states
        for j in range(6):
            if (km >> j) & 1:
                if st[r, j].sum() != cP[j]: nbad += 1
                nlev[j] += 1
        if not (km & 1):
            nbad += 1; continue        # probabilities all 1: every caught excursion is kept at every level it reaches
        # r3_ex's record starts at the first generation with P <= L0 = the 0.9 catch
        k = (int(lane), int(orb), int(g0 + cg[0]))
        if k not in key: nbad += 1; continue
        h3, s3 = key[k]; pc = s3.sum(1)
        if int(h3[2]) != end or int(h3[3]) != minp: nbad += 1
        if h3[5] == 0 and int(h3[4]) != ln - cg[0]: nbad += 1
        for j in range(6):
            if (cm >> j) & 1:
                t = int(np.argmax(pc <= L[j]))
                if not (pc[t] <= L[j]) or t != cg[j] - cg[0] or pc[t] != cP[j] or not np.array_equal(s3[t], st[r, j]): nbad += 1
        if h3[5] == 0:
            t = int(np.argmax(pc == minp))
            if t != bo - cg[0] or not np.array_equal(s3[t], st[r, 6]): nbad += 1
        nchk += 1
    # 4. subsampling: probabilities < 1 with the same KSEED give exactly the full records restricted to the kept levels
    c = b + '_sub'; PRs = [0.05, 0.1, 0.2, 0.4, 0.7, 1.0]
    subprocess.run([EX4, gf, 'run', '6', '0.4', '2500', c + '.lives', '/dev/null', '/dev/null', '100000', '/dev/null', '0', '1', '512', str(pb), c + '.x', c + '.cat',
                    ','.join(map(str, L)), ','.join(map(str, PRs)), '12345'], check=True, capture_output=True)
    hs, ss = read_ex4(c + '.cat'); fk = {(int(x[0]), int(x[1]), int(x[9])): r for r, x in enumerate(hd)}; sb = 0
    for r in range(len(hs)):
        q = fk.get((int(hs[r, 0]), int(hs[r, 1]), int(hs[r, 9])))
        if q is None or not np.array_equal(hs[r, [0, 1, 2, 3, 4, 6, 7, 8, 9]], hd[q, [0, 1, 2, 3, 4, 6, 7, 8, 9]]) or not np.array_equal(hs[r, 10:22], hd[q, 10:22]): sb += 1; continue
        for j in range(6):
            if (hs[r, 5] >> j) & 1 and not np.array_equal(ss[r, j], st[q, j]): sb += 1
            if not (hs[r, 5] >> j) & 1 and ss[r, j].any(): sb += 1
        if not np.array_equal(ss[r, 6], st[q, 6]): sb += 1
    kept = [int(((hs[:, 5] >> j) & 1).sum()) for j in range(6)]
    say(f'{name}: subsample run (probabilities {PRs}): {len(hs)} records, kept per level {kept} of {nlev} '
        f'(ratios {[round(k / max(n, 1), 3) for k, n in zip(kept, nlev)]}), failures {sb}')
    ok &= sb == 0
    say(f'{name}: {len(hd)} ex4 records ({len(r3)} r3_ex dumps), {nchk} matched, catches per level {nlev}, failures {nbad}')
    ok &= nbad == 0 and nchk == len(hd) and len(r3) == len(hd)
say('ALL OK' if ok else 'FAIL')
