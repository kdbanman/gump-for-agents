import json, sys
from collections import Counter
import numpy as np
import sg, plab, scat, caps, caps_any
obs = [json.loads(l) for l in open('../scratch/signals/survey.jsonl')]
C = int(sys.argv[1]); ws = [int(a) for a in sys.argv[2:]]
for w in ws:
    wire = scat.Wire(obs[w], None)
    cs, status, nfree = caps.enumerate_caps(wire, C, 1, 5, 6, wire.P, 60, 300, verbose=False)
    lab = caps_any.RawLab(wire, 1, 5, C, L=260)
    g = lab.g; res = Counter(); ex = None
    for cap in cs[:60]:
        z = g.state(lab.body[0] | frozenset(cap)); x = z.copy()
        for c in wire.pulse_cells('R', 0, -20):
            x[g.index[c]] ^= 1
        x = g.run(x, 120, sparse=True); z = g.run(z, 120, sparse=True)
        # period of the cap region (units >= -12) over the next 400 generations
        keep = np.array([scat.unit(c) >= -12 for c in g.cells] + [False] * (len(x) - g.n))
        seq = []; y = x.copy()
        for t in range(400):
            seq.append(y[keep].tobytes()); y = g.run(y, 1, sparse=True)
        per = next((p for p in range(1, 200) if all(seq[t] == seq[t + p] for t in range(400 - p))), None)
        d = sorted(set(scat.unit(g.cells[i]) for i in np.nonzero((x != z)[:g.n])[0] if scat.unit(g.cells[i]) >= -100))
        res[(per, (min(d), max(d)) if d else None)] += 1
    print('wire', w, 'C', C, len(cs), 'caps;', '(period of the cap end after the hit, units that differ from the unhit run):', res.most_common(8), flush=True)
