import json, sys, os, glob
import numpy as np
root = sys.argv[1]
sys.path.insert(0, root + '/research/shape')
sys.path.insert(0, root + '/research/gpu')
sys.path.insert(0, root + '/research/gpu-local')
import facelaw

for tag in sys.argv[2:]:
    print('==', tag)
    tot = []
    for f in sorted(glob.glob(root + '/research/scratch/gpu-local/eqtorus_' + tag + '_s*.json')):
        d = json.load(open(f))
        if 'raw' not in d:
            print(os.path.basename(f), 'no raw'); continue
        A, K, B, D = facelaw.unpack(d['raw'])
        G = d['gens']
        dead = K == 1
        t = (B + A)[dead]
        h = np.histogram(t, np.linspace(0, G, 7))[0]
        ages = A[dead]
        # births per replica slot are not stored; look at young deaths and at pairs of deaths close in time
        ts = np.sort(t)
        gaps = np.diff(ts)
        mean_gap = G / max(1, len(ts))
        close = int((gaps < mean_gap / 50).sum())
        print(os.path.basename(f)[-13:-5], 'deaths', int(dead.sum()), 'by sixth of run', h.tolist(),
              'age<1e8:', int((ages < 1e8).sum()), 'age<1e9:', int((ages < 1e9).sum()),
              'gaps < mean/50:', close, 'expected', round(len(gaps) * (1 - np.exp(-1 / 50)), 1),
              'B kinds', sorted(set(np.unique(D).tolist()))[:6])
        tot.append(h)
    if tot:
        print('all seeds by sixth', np.sum(tot, 0).tolist())
