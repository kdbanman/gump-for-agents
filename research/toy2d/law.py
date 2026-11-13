"""Edge-death law in periodic strips: pooled QSD runs until enough deaths (or a time budget).

python3 law.py RULE LATTICE W L1,L2,... [--deaths 300] [--maxsec 600] [--sym none] [--p 0.4] [--T0 300] [--tag a]
Output: research/scratch/toy2d/law_<lat>_<rule>_W<W>_<sym>_<tag>.json, one record per L (re-running tops up).
Per L: exposure (replica-generations at age >= T0), deaths per event, settles, edge-row histogram (pooled over
both edges), 'from' (edge population one generation before an edge death), hazard by age (log2 bins), and the
list of ages at death (for CV). h = edge deaths / (NE * exposure) is the death rate of one edge (NE = 2 edges in a strip, 4 in a box;
for --vessel box the W argument is ignored except in the file name, L is the box side).
"""
import argparse, json, os, time
import numpy as np
import geom

ap = argparse.ArgumentParser()
ap.add_argument('rule'); ap.add_argument('lat'); ap.add_argument('W', type=int); ap.add_argument('Ls')
ap.add_argument('--deaths', type=int, default=300); ap.add_argument('--maxsec', type=float, default=600)
ap.add_argument('--sym', default='none'); ap.add_argument('--p', type=float, default=0.4)
ap.add_argument('--T0', type=int, default=300); ap.add_argument('--tag', default='a')
ap.add_argument('--chunk', type=float, default=0)
ap.add_argument('--vessel', default='strip')  # strip (2 edges, periodic x) or box (L x L, 4 edges)
a = ap.parse_args()
NE = 2 if a.vessel == 'strip' else 4
fn = os.path.join(geom.SCR, 'law_%s_%s_%s%d_%s_%s.json' % (a.lat, a.rule.replace('/', ''), 'W' if a.vessel == 'strip' else 'box', a.W, a.sym, a.tag))
db = json.load(open(fn)) if os.path.exists(fn) else {}
for L in map(int, a.Ls.split(',')):
    rec = db.get(str(L), dict(exposure=0, deaths_by_event=[], settles=0, early=0, hist=[], frm=[0] * 8,
                              age_exposure=[0] * 64, age_deaths=[0] * 64, ages=[], chunks=0, bulk_flips=0, edge_flips=0, cells=0))
    t0 = time.time()
    gens = a.chunk or 20000
    while time.time() - t0 < a.maxsec:
        ev = rec['deaths_by_event']
        ed = sum(ev[:NE]) if ev else 0
        if ed >= a.deaths:
            break
        seed = 1000 * L + rec['chunks'] + 17
        out = os.path.join(geom.SCR, 'lawtmp_%s_%s_%s_%s%d_%d_%s.txt' % (a.lat, a.rule.replace('/', ''), a.tag, a.vessel, a.W, L, a.sym))
        tc = time.time()
        dims = (a.W, L) if a.vessel == 'strip' else (L,)
        d = geom.qsd(a.rule, a.lat, a.vessel, dims, a.p, seed, a.T0, int(gens), out, sym=a.sym)
        dt = time.time() - tc
        rec['chunks'] += 1
        rec['exposure'] += d['exposure']; rec['settles'] += d['settles']; rec['early'] += d['early']
        de = list(np.atleast_1d(d['deaths_by_event']))
        rec['deaths_by_event'] = [x + y for x, y in zip(rec['deaths_by_event'] or [0] * len(de), de)]
        h = list(d['hist']); rec['hist'] = [x + y for x, y in zip(rec['hist'] or [0] * len(h), h)]
        rec['frm'] = [x + y for x, y in zip(rec['frm'], d['from'])]
        rec['age_exposure'] = [x + y for x, y in zip(rec['age_exposure'], d['age_exposure'])]
        rec['age_deaths'] = [x + y for x, y in zip(rec['age_deaths'], d['age_deaths'])]
        rec['bulk_flips'] += d['bulk_flips']; rec['edge_flips'] += d['edge_flips']; rec['cells'] = d['cells']
        for line in open(out + '.deaths'):
            e, age = map(int, line.split())
            if e < NE:
                rec['ages'].append(age)
        # grow the chunk so that each chunk is ~60 s
        gens = min(max(gens * min(4.0, 60.0 / max(dt, 1e-3)), 2000), 5e7)
    db[str(L)] = rec
    json.dump(db, open(fn, 'w'))
    ev = rec['deaths_by_event']; ed = sum(ev[:NE])
    hh = ed / (NE * rec['exposure']) if rec['exposure'] else float('nan')
    print('L=%d exposure %.3g edge deaths %d firewalls %d settles %d  tau_edge = %.4g (ln %.3f +- %.3f)' %
          (L, rec['exposure'], ed, sum(ev[NE:]), rec['settles'], 1 / hh if hh else float('inf'),
           -np.log(hh) if hh else float('inf'), 1 / np.sqrt(ed) if ed else float('nan')), flush=True)
