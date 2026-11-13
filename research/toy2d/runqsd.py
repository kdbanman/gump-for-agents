"""Quasi-stationary runs in periodic strips: one edge row = the 2D analogue of a gump face.

python3 runqsd.py RULE W L GENS [--sym S] [--p P] [--T0 T] [--seed K] [--tag X]
  -> research/scratch/toy2d/qsd_<rule>_<W>x<L>_<sym>_<tag>.txt (+ .deaths: event, age at death)
256 replicas; a replica whose edge row empties (events 0, 1) or which forms an interior two-row firewall
(events >= 2) or settles is recorded and reseeded; ages < T0 are not measured.
"""
import argparse, os
import geom

ap = argparse.ArgumentParser()
ap.add_argument('rule'); ap.add_argument('W', type=int); ap.add_argument('L', type=int); ap.add_argument('gens', type=float)
ap.add_argument('--sym', default='none'); ap.add_argument('--p', type=float, default=0.5)
ap.add_argument('--T0', type=int, default=200); ap.add_argument('--seed', type=int, default=1); ap.add_argument('--tag', default='a')
ap.add_argument('--lat', default='moore')
a = ap.parse_args()
name = 'qsd_%s_%s_%dx%d_%s_%s.txt' % (a.lat, a.rule.replace('/', ''), a.W, a.L, a.sym, a.tag)
out = os.path.join(geom.SCR, name)
d = geom.qsd(a.rule, a.lat, 'strip', (a.W, a.L), a.p, a.seed, a.T0, int(a.gens), out, sym=a.sym)
h = d['deaths']; e = d['exposure']
print(name, 'exposure', e, 'deaths', h, 'by event', d['deaths_by_event'][:4], 'settles', d['settles'], 'early', d['early'],
      'tau_first', e / h if h else float('inf'))
