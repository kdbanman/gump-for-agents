#!/usr/bin/env python3
"""Driver for qs.c (audit of research/theory/exponent.md, verdict 1).  Results appended to
research/scratch/audit_exponent/results.jsonl; the curated table is in research/audit/REVIEW-exponent.md.

  python3 run.py validate                     qs.c (bit-sliced) against graphs.np_step, which matches oracle.py
  python3 run.py hull R SECONDS [T0] [SEED]   deterministic octahedral hull, 8 faces, settled states censored
  python3 run.py model R w SECONDS [T0] [SEED]        top w layers of the hull face on two Bernoulli(0.4155) layers
  python3 run.py slab a b SECONDS [T0] [SEED]         deterministic 12-layer slab, periodic a x b face (A = 3ab)
  python3 run.py slabmodel a b w SECONDS [T0] [SEED]  top w layers of a periodic face on two Bernoulli(0.4155) layers
"""
import json, os, subprocess, sys
import numpy as np
import graphs

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = graphs.SCR
EXE = os.path.join(SCR, 'qs')


def build():
    src = os.path.join(HERE, 'qs.c')
    if not os.path.exists(EXE) or os.path.getmtime(EXE) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-o', EXE, src, '-lm'])


def trace(g, name, gens):
    fn = graphs.save(g, name)
    out = subprocess.run([EXE, fn, '0', '7', '0', str(-gens)], capture_output=True, text=True, check=True).stdout.split()
    a = np.array([[int(c) for c in row] for row in out[:4]], np.uint8)
    b = np.array([[int(c) for c in row] for row in out[4:8]], np.uint8)
    st = np.zeros((4, g['N'] + g['M'] + 1), np.uint8); st[:, :g['N']] = a      # noise cells read as 0 in trace mode
    for _ in range(gens):
        st = graphs.np_step(st, g['nb'])
    assert (st[:, :g['N']] == b).all(), name
    return int(b.sum())


def validate():
    build()
    for g, name in ((graphs.hull_graph(9), 'hull9'), (graphs.slab_graph(4, 4, 12), 'slab4x4'),
                    (graphs.hull_model(11, 5), 'model11_5'), (graphs.slab_model(4, 5, 5), 'slabmodel4x5_5')):
        pop = trace(g, name, 200)
        print('%-16s qs.c = numpy stepper for 200 generations, 4 replicas (final population %d)' % (name, pop))
    print('ALL OK')


def go(kind, g, name, sec, T0, seed, extra):
    build()
    fn = graphs.save(g, name)
    out = subprocess.run([EXE, fn, str(T0), str(seed), str(sec), str(10 ** 9)], capture_output=True, text=True,
                         check=True).stdout
    r = json.loads(out); r.update(kind=kind, name=name, A=g['A'], seed=seed, **extra)
    with open(os.path.join(SCR, 'results.jsonl'), 'a') as f:
        f.write(json.dumps(r) + '\n')
    print('%-22s A=%3d T0=%d seed=%d  ln tau = %.3f +- %.3f  deaths %d  exposure %.3g  cens settle %d cut %d  <n> %.2f'
          '  CV %.2f' % (name, g['A'], T0, seed, r['lntau'], r['err'], r['deaths'], r['exposure'], r['censored_settled'],
                         r['censored_cut'], r['mean_face_pop'], r['death_age_sd'] / max(1e-9, r['death_age_mean'] - T0)))
    return r


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'validate':
        validate()
    elif a[0] == 'hull':
        R, sec = int(a[1]), float(a[2]); T0 = int(a[3]) if len(a) > 3 else 200; seed = int(a[4]) if len(a) > 4 else 1
        go('hull', graphs.hull_graph(R), 'hull_R%d' % R, sec, T0, seed, dict(R=R))
    elif a[0] == 'model':
        R, w, sec = int(a[1]), int(a[2]), float(a[3]); T0 = int(a[4]) if len(a) > 4 else 200
        seed = int(a[5]) if len(a) > 5 else 1
        go('model', graphs.hull_model(R, w), 'model_R%d_w%d' % (R, w), sec, T0, seed, dict(R=R, w=w))
    elif a[0] == 'slab':
        x, y, sec = int(a[1]), int(a[2]), float(a[3]); T0 = int(a[4]) if len(a) > 4 else 300
        seed = int(a[5]) if len(a) > 5 else 1
        go('slab', graphs.slab_graph(x, y, 12), 'slab_%dx%d' % (x, y), sec, T0, seed, dict(a=x, b=y))
    elif a[0] == 'slabmodel':
        x, y, w, sec = int(a[1]), int(a[2]), int(a[3]), float(a[4]); T0 = int(a[5]) if len(a) > 5 else 300
        seed = int(a[6]) if len(a) > 6 else 1
        go('slabmodel', graphs.slab_model(x, y, w), 'slabmodel_%dx%d_w%d' % (x, y, w), sec, T0, seed,
           dict(a=x, b=y, w=w))
