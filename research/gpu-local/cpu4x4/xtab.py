"""Cross-table of a life's kind under rule A (repository, K = 16) and rule B (same logic per generation)."""
import glob, os, sys, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import w
from analyze import death_times, ring_firewall
OUTD, RAWD = sys.argv[1], sys.argv[2]
def kinds(face, fw, st, ge):
    stop = np.where(st >= 0, st, ge).astype(float); fwm = fw.min(1)
    end = np.minimum.reduce([face, fwm, stop])
    kF = (face == end) & (face < fwm) & (face <= stop); kW = (fwm == end) & (fwm <= face) & (fwm <= stop)
    kS = (stop == end) & ~kF & ~kW & (st >= 0)
    return np.where(kF, 0, np.where(kW, 1, np.where(kS, 2, 3))), end
T = np.zeros((4, 4), np.int64); dE = np.zeros((4, 4))
for f in sorted(glob.glob(os.path.join(OUTD, 'ch_4_0_4_s*.npz'))):
    s = f.rsplit('_s', 1)[1][:-4]
    o = np.load(f); r = np.load(os.path.join(RAWD, f'raw_4_0_4_s{s}_K1_cyc.npz')); ge = int(o['gen_end'])
    keys = [tuple(k) for k in r['keys'].tolist()]
    outer = [keys.index((0, 1)), keys.index((0, 15))]; rings = [[i for i, k in enumerate(keys) if k[0] == d] for d in (1, 2, 3)]
    D1 = death_times(r['la'].astype(np.int64), ge)
    face1 = np.minimum(D1[:, outer[0]], D1[:, outer[1]]); fw1 = np.stack([ring_firewall(D1[:, c], ring=True) for c in rings], 1)
    st = r['st'].astype(np.int64); st1 = np.where(st >= 0, np.minimum(st, r['lc2']), -1)
    kA, eA = kinds(o['face'], o['fw'], o['settle'], ge); kB, eB = kinds(face1, fw1, st1, ge)
    np.add.at(T, (kA, kB), 1); np.add.at(dE, (kA, kB), eA - eB)
n = ['face', 'firewall', 'settled', 'cap']
print('rows: kind under A (K=16); columns: kind under B (per generation); count [exposure A - B]')
print(' ' * 10 + ''.join(f'{x:>24s}' for x in n))
for i in range(4):
    print(f'{n[i]:10s}' + ''.join(f'{T[i, j]:12d} [{dE[i, j]:+10.0f}]' for j in range(4)))
