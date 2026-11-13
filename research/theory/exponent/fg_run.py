"""Run fg (exact functional graphs) over a list of small vessels; results in research/scratch/exponent/fg_*.txt,
summary table in data/fg_summary.json.   python3 fg_run.py run [maxN] | table"""
import json, math, os, subprocess, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, '..', '..', 'scratch', 'exponent')
VESSELS = [('strip', 2, L) for L in range(5, 15)] + [('strip', 3, L) for L in range(5, 11)] + \
          [('strip', 4, L) for L in range(5, 9)] + [('strip', 5, 5), ('strip', 5, 6)] + \
          [('box', 4, 4), ('box', 4, 5), ('box', 5, 5), ('box', 4, 6), ('box', 5, 6), ('box', 4, 7), ('box', 4, 8), ('strip', 2, 16)]

def parse(fn):
    d = {}
    for l in open(fn):
        k, *v = l.split(); d[k] = v
    return d

def group_order(kind, H, L):
    return (8 if H == L else 4) if kind == 'box' else 4 * L

def summarize(kind, H, L):
    d = parse(os.path.join(SCR, 'fg_%s_%dx%d.txt' % (kind, H, L)))
    N = H * L; M = 2.0 ** N
    hist = np.array([float(v) for v in d['death_hist']])
    basin = float(d['immortal_basin'][0]); mortal = hist.sum()
    surv = hist[::-1].cumsum()[::-1]                       # mortal states with T >= t
    mean_T = (hist * np.arange(len(hist))).sum() / mortal
    # hazard among mortal states that start alive
    haz = hist / np.maximum(surv, 1)
    imm = {}
    for tok in d['immortal_by_period']:
        p, c = tok.split(':')[:2]; imm[p] = int(c)
    states_p = lambda lo: sum(int(p) * c for p, c in imm.items() if p != 'big' and int(p) >= lo)
    cyc = {}
    for tok in d['cycles_by_period']:
        a = tok.split(':'); cyc[a[0]] = (int(a[1]), int(a[2]))
    tr = np.array([float(v) for v in d['transient_hist']])
    out = dict(kind=kind, H=H, L=L, N=N, G=group_order(kind, H, L), basin_frac=basin / M, dead_at_0=hist[0] / M,
               immortal_cycles=int(d['immortal_cycles'][0]), immortal_states=int(d['immortal_cyclic_states'][0]),
               immortal_states_p12=states_p(1) - states_p(3), immortal_states_p3plus=states_p(3), immortal_states_p8plus=states_p(8),
               immortal_max_period=int(d['immortal_max_period'][0]), cycles=int(d['cycles'][0]), cyclic_states=int(d['cyclic_states'][0]),
               max_period=int(d['max_period'][0]), max_death_time=len(hist) - 1, mean_T_mortal=mean_T,
               mean_transient=float((tr * np.arange(len(tr))).sum() / tr.sum()), max_transient=len(tr) - 1,
               hazard=[float(h) for h in haz[:80]], surv=[float(s) for s in surv[:400]], imm_by_period=imm,
               cyc_by_period={k: list(v) for k, v in cyc.items()})
    return out

if __name__ == '__main__':
    if sys.argv[1] == 'run':
        maxN = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        for kind, H, L in VESSELS:
            fn = os.path.join(SCR, 'fg_%s_%dx%d.txt' % (kind, H, L))
            if H * L > maxN or os.path.exists(fn): continue
            t = time.time(); subprocess.check_call([os.path.join(SCR, 'fg'), kind, str(H), str(L), fn + '.tmp']); os.replace(fn + '.tmp', fn)
            print(kind, H, L, 'N', H * L, '%.0f s' % (time.time() - t), flush=True)
    rows = []
    for kind, H, L in VESSELS:
        if os.path.exists(os.path.join(SCR, 'fg_%s_%dx%d.txt' % (kind, H, L))):
            rows.append(summarize(kind, H, L))
    json.dump(rows, open(os.path.join(HERE, 'data', 'fg_summary.json'), 'w'))
    print('%-6s %2s %2s %2s %4s | %9s %9s | %8s %8s %8s %6s | %9s %6s | %6s %6s' % ('kind', 'H', 'L', 'N', '|G|', 'basin', 'dead@0', 'imm.st', 'p<=2', 'p>=8', 'maxP', 'cyc.st', 'maxP', '<T>', 'maxT'))
    for r in rows:
        print('%-6s %2d %2d %2d %4d | %9.3e %9.3e | %8d %8d %8d %6d | %9d %6d | %6.2f %6d' % (r['kind'], r['H'], r['L'], r['N'], r['G'], r['basin_frac'], r['dead_at_0'],
              r['immortal_states'], r['immortal_states_p12'], r['immortal_states_p8plus'], r['immortal_max_period'], r['cyclic_states'], r['max_period'], r['mean_T_mortal'], r['max_death_time']))
