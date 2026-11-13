"""Rule search: Moore (or other) lattice, births >= bmin, any survival set; soups in an L x L box.

Stage 1  python3 search.py stage1 moore OUT.jsonl [shard nshards]
         every rule B (non-empty subset of {bmin..K}) x S (any subset of {0..K}); box L = 10, soup p = 0.3 and
         0.5, 256 soups each, cap 4000 generations. Records median lifetime (settle gen; capped runs count as
         cap) and fraction still running.
Stage 2  python3 search.py stage2 moore IN.jsonl OUT.jsonl [minmed]
         rules whose stage-1 median at either p is >= minmed (default 300): box L = 8, 10, 12, 14, 16, at
         the better p, cap 5*10^4, 256 soups; plus the first edge-death time.
"""
import json, sys, time
import numpy as np
import geom

KMAX = {'moore': 8, 'vn': 4, 'hex': 6, 'cross2': 8}
BMIN = {'moore': 4, 'vn': 2, 'hex': 3, 'cross2': 3}


def rulestr(B, S):
    return 'B' + ''.join(str(k) for k in range(16) if B >> k & 1) + '/S' + ''.join(str(k) for k in range(16) if S >> k & 1)


def stats(a, cap):
    life = np.where(a[:, 0] < 0, cap, a[:, 0]).astype(float)
    return dict(med=float(np.median(life)), mean=float(life.mean()), run=float((a[:, 0] < 0).mean()),
                pop=float(a[:, 1].mean()))


def stage1(lat, out, shard=0, nsh=1):
    K = KMAX[lat]; bmin = BMIN[lat]
    rules = [(B, S) for B in range(1, 1 << (K + 1)) if B & ((1 << bmin) - 1) == 0 for S in range(1 << (K + 1))]
    rules = rules[shard::nsh]
    with open(out, 'a') as f:
        for i, (B, S) in enumerate(rules):
            rec = dict(rule=rulestr(B, S), B=B, S=S)
            for p in (0.3, 0.5):
                a = geom.life((B, S), lat, 'box', (10,), p, 1000 + i, 4000)
                rec['p%g' % p] = stats(a, 4000)
            f.write(json.dumps(rec) + '\n')


def stage2(lat, inp, out, minmed=300):
    recs = [json.loads(l) for l in open(inp)]
    sel = [r for r in recs if max(r['p0.3']['med'], r['p0.5']['med']) >= minmed]
    print(len(sel), 'rules', file=sys.stderr)
    with open(out, 'a') as f:
        for r in sel:
            p = 0.3 if r['p0.3']['med'] >= r['p0.5']['med'] else 0.5
            rec = dict(rule=r['rule'], B=r['B'], S=r['S'], p=p, L={})
            t0 = time.time()
            for L in (8, 10, 12, 14, 16):
                cap = 50000
                a = geom.life((r['B'], r['S']), lat, 'box', (L,), p, 7 + L, cap)
                st = stats(a, cap)
                ev = a[:, 2:6].astype(float); ev[ev < 0] = np.inf
                first = ev.min(1)
                st['edge_first_med'] = float(np.median(first)) if np.isfinite(np.median(first)) else -1
                st['frac_edge_before_settle'] = float(np.isfinite(first).mean())
                rec['L'][L] = st
                if st['run'] > 0.5:
                    break
            rec['secs'] = time.time() - t0
            f.write(json.dumps(rec) + '\n'); f.flush()


if __name__ == '__main__':
    if sys.argv[1] == 'stage1':
        a = sys.argv[2:]
        stage1(a[0], a[1], int(a[2]) if len(a) > 2 else 0, int(a[3]) if len(a) > 3 else 1)
    else:
        a = sys.argv[2:]
        stage2(a[0], a[1], a[2], float(a[3]) if len(a) > 3 else 300)
