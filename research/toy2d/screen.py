"""Strip screen: is the edge row a living, fluctuating boundary that dies by fluctuation?

[LAT=moore|cross2] [MAXSIZE=k] python3 screen.py IN.jsonl OUT.jsonl [shard nshards]
For every rule in IN (stage-1 records with median >= 300 at L = 10), periodic strips W = 10, L = 12 and 20,
soup p = the better stage-1 density, 256 replicas, 20000 generations of QSD with restarts (T0 = 200).
Records per size: edge deaths and mean wait per edge, interior firewalls, settles (period <= 4096), the
non-period-2 activity (fraction of cells with x(t+1) != x(t-1)) in the bulk and in the edge rows.
"""
import json, os, sys
import geom

inp, out = sys.argv[1], sys.argv[2]
LAT = os.environ.get('LAT', 'moore')
MAXSIZE = int(os.environ.get('MAXSIZE', '99'))  # only rules with |B| + |S| <= MAXSIZE
sh, nsh = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (0, 1)
recs = [json.loads(l) for l in open(inp)]
recs = [r for r in recs if max(r['p0.3']['med'], r['p0.5']['med']) >= 300
        and bin(r['B']).count('1') + bin(r['S']).count('1') <= MAXSIZE][sh::nsh]
done = set()
if os.path.exists(out):
    done = {json.loads(l)['rule'] for l in open(out)}
with open(out, 'a') as f:
    for r in recs:
        if r['rule'] in done:
            continue
        p = 0.3 if r['p0.3']['med'] >= r['p0.5']['med'] else 0.5
        rec = dict(rule=r['rule'], B=r['B'], S=r['S'], p=p)
        for L in (12, 20):
            fn = os.path.join(geom.SCR, 'screen_tmp_%s_%d_%d.txt' % (LAT, sh, os.getpid()))
            d = geom.qsd((r['B'], r['S']), LAT, 'strip', (10, L), p, 11 + L, 200, 20000, fn)
            e = d['exposure']; ev = d['deaths_by_event']
            edge = ev[0] + ev[1]; fw = ev[2:].sum()
            rec[str(L)] = dict(exposure=e, edge_deaths=float(edge), firewalls=float(fw), settles=d['settles'],
                               tau_edge=2 * e / edge if edge else None,
                               act_bulk=d['bulk_flips'] / e / d['cells'] if e else None,
                               act_edge=d['edge_flips'] / e / (2 * L) if e else None,
                               edge_mean=float((d['hist'] * range(len(d['hist']))).sum() / d['hist'].sum()) / L if d['hist'].sum() else None)
        f.write(json.dumps(rec) + '\n'); f.flush()
