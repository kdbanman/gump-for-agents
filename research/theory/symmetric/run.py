#!/usr/bin/env python3
"""run.py: renewal-life runs of sy on the orbit graph of SPEC, and their analysis.

    python3 research/theory/symmetric/run.py run SPEC GENS [SEED=1] [P=0.4] [CHK=4]
        512 replicas, each GENS generations of successive lives from fresh soups (one draw per orbit, density P).
        Writes research/scratch/symmetric/lives_SPEC_sSEED.bin (+ .json with the run's parameters).
    python3 research/theory/symmetric/run.py ana SPEC [SPEC ...]      # table; all seeds of a SPEC pooled
    python3 research/theory/symmetric/run.py csv                      # every SPEC on disk -> data/runs.csv

Estimator. A life ends at a face death F, a transverse firewall W, both at one check X, settled S (ladder of
snapshots, any period; the record of an S life is the age of the snapshot it matched, an upper bound on when it
settled; the rung before it is used as the lower bound), or open at the end of the job. With T0 = 512 generations (fixed before the runs):
exposure E = sum over all lives of max(0, age - T0); deaths D = lives ending F or X at age > T0;
ln tau_face = ln(nf * E / D) +- 1/sqrt(D), nf = number of independent faces (face orbits: 2 for a slab, 8, 2 or 1
for a vessel with group c1, td, d2h/oh). The table also gives T0 = 128 and 2048 (is the hazard flat in age?), the
firewall share W/(D+W), and the share of exposure carried by lives that ended settled (an upper bound on what
undetected settling could add).
"""
import json, os, subprocess, sys, time, glob, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SCR = os.path.join(ROOT, 'research', 'scratch', 'symmetric')
SY = os.path.join(SCR, 'sy')
sys.path.insert(0, HERE)
T0 = 512


def build_sy():
    os.makedirs(SCR, exist_ok=True)
    src = os.path.join(HERE, 'sy.c')
    if not os.path.exists(SY) or os.path.getmtime(SY) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-o', SY, src])


def run(spec, gens, seed=1, p=0.4, chk=4):
    import geom
    build_sy()
    q = geom.build(spec)
    gf = os.path.join(SCR, f'graph_{spec}.txt')
    geom.write_graph(q, gf)
    out = os.path.join(SCR, f'lives_{spec}_s{seed}.bin')
    t = time.time()
    res = subprocess.run([SY, gf, 'run', str(seed), str(p), str(gens), str(chk), out + '.part'], capture_output=True, text=True, check=True).stdout
    os.replace(out + '.part', out)
    meta = json.loads(res.strip().splitlines()[-1])
    meta.update(spec=spec, order=q.order, cells=int(len(q.f.cells)), nf=len(q.faces), triples=len(q.triples), seconds=round(time.time() - t, 1),
                **geom.face_stats(q))
    json.dump(meta, open(out[:-4] + '.json', 'w'))
    print(json.dumps(meta), flush=True)


def load(spec):
    ages, types, meta = [], [], None
    for f in sorted(glob.glob(os.path.join(SCR, f'lives_{spec}_s*.bin'))):
        m = json.load(open(f[:-4] + '.json'))
        r = np.fromfile(f, dtype=np.uint32)
        ages.append((r >> 3).astype(np.int64) * m['chk']); types.append((r & 7).astype(np.int8))
        if meta is None:
            meta = dict(m); meta['jobs'] = 0; meta['total_gens'] = 0
        meta['jobs'] += 1; meta['total_gens'] += m['gens'] * 512
    if meta is None:
        return None
    return np.concatenate(ages), np.concatenate(types), meta


def ladder_prev(chk):
    """map: snapshot age (checks) -> previous rung (checks), for the ladder of sy.c"""
    prev = {0: 0}; a = 0; nxt = 1
    while a < (1 << 28):
        prev[nxt] = a; a = nxt; nxt = a + max(1, a // 8)
    return prev


_LP = ladder_prev(4)


def estimate(ages, types, nf, t0, chk=4, s_low=False):
    if s_low:                                   # settled lives counted only up to the rung before the matching snapshot
        ages = ages.copy(); sel = np.nonzero(types == 4)[0]
        ages[sel] = np.array([_LP[int(a) // chk] * chk for a in ages[sel]], dtype=np.int64)
    E = np.clip(ages - t0, 0, None).sum()
    late = ages > t0
    D = int(((types == 1) | (types == 3)) & late).sum() if False else int((((types == 1) | (types == 3)) & late).sum())
    F = int(((types == 1) & late).sum()); Wn = int(((types == 2) & late).sum()); X = int(((types == 3) & late).sum())
    S = int(((types == 4) & late).sum())
    ES = np.clip(ages[types == 4] - t0, 0, None).sum()
    lt = math.log(nf * E / D) if D else float('nan')
    return dict(E=float(E), D=D, F=F, W=Wn, X=X, S=S, lntau=lt, se=1 / math.sqrt(D) if D else float('nan'),
                fw_share=(Wn / (D + Wn) if D + Wn else 0.0), settled_expo_share=float(ES / E) if E else 0.0)


def row(spec):
    L = load(spec)
    if L is None:
        return None
    ages, types, m = L
    e = estimate(ages, types, m['nf'], T0); e1 = estimate(ages, types, m['nf'], 128); e2 = estimate(ages, types, m['nf'], 2048)
    elow = estimate(ages, types, m['nf'], T0, m['chk'], s_low=True)
    op = ages[types == 5]
    return dict(spec=spec, order=m['order'], area=m['area'], face_nodes=m['face_nodes'], nf=m['nf'], jobs=m['jobs'], lives=len(ages),
                E=e['E'], D=e['D'], W=e['W'], X=e['X'], S=e['S'], lntau=e['lntau'], se=e['se'], lntau_Slow=elow['lntau'], lntau_T128=e1['lntau'],
                lntau_T2048=e2['lntau'], se_T2048=e2['se'], fw_share=e['fw_share'], settled_expo_share=e['settled_expo_share'],
                mean_life=float(ages[types != 5].mean()) if (types != 5).any() else float('nan'),
                oldest_open_over_tau=float(op.max() / (math.exp(e['lntau']) / m['nf'])) if e['D'] else float('nan'))


def show(specs):
    print(f'{"spec":20s} {"|G|":>3s} {"A":>4s} {"nodes":>5s} nf {"deaths":>8s} {"ln tau_face":>11s} {"+-":>6s} {"S-low":>7s} {"T0=128":>7s} {"T0=2048":>8s} {"+-":>6s} {"fw":>6s} {"S":>6s} {"S-expo":>7s} {"old/tau":>7s}')
    for s in specs:
        r = row(s)
        if r is None:
            print(f'{s:20s} (no data)'); continue
        print(f'{r["spec"]:20s} {r["order"]:3d} {r["area"]:4d} {r["face_nodes"]:5d} {r["nf"]:2d} {r["D"]:8d} {r["lntau"]:11.4f} {r["se"]:6.4f} {r["lntau_Slow"]:7.3f} '
              f'{r["lntau_T128"]:7.3f} {r["lntau_T2048"]:8.3f} {r["se_T2048"]:6.4f} {r["fw_share"]:6.4f} {r["S"]:6d} {r["settled_expo_share"]:7.4f} {r["oldest_open_over_tau"]:7.1f}')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'run':
        a = sys.argv[2:]
        run(a[0], int(float(a[1])), int(a[2]) if len(a) > 2 else 1, float(a[3]) if len(a) > 3 else 0.4, int(a[4]) if len(a) > 4 else 4)
    elif cmd == 'ana':
        show(sys.argv[2:])
    elif cmd == 'csv':
        specs = sorted(set(os.path.basename(f)[6:].rsplit('_s', 1)[0] for f in glob.glob(os.path.join(SCR, 'lives_*.bin'))))
        os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
        keys = None
        with open(os.path.join(HERE, 'data', 'runs.csv'), 'w') as fh:
            for s in specs:
                r = row(s)
                if keys is None:
                    keys = list(r.keys()); fh.write(','.join(keys) + '\n')
                fh.write(','.join(f'{r[k]:.6g}' if isinstance(r[k], float) else str(r[k]) for k in keys) + '\n')
        show(specs)
