"""Where the last live cells of a dying outer face sit: run to T0, then every gen until the d0 face s=C dies;
print the edge-distance (min coordinate in the face octant) of the face's live cells over its last few gens."""
import os, subprocess, sys, tempfile, numpy as np
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine', 'target', 'release', 'gump')
T0, T1, C = map(int, sys.argv[1:4]); args = sys.argv[5:]
tmp = tempfile.mkdtemp(); tr = os.path.join(tmp, 't.txt'); snap = os.path.join(tmp, 's.gump')
subprocess.run([G, 'run', *args, '--gens', str(T0), '--no-halt', '--snapshot-out', snap], check=True, capture_output=True)
subprocess.run([G, 'run', '--snapshot', snap, '--gens', str(T1 - T0), '--no-halt', '--trace', tr], check=True, capture_output=True)
hist = []
for line in open(tr):
    g, *cs = line.split()
    P = np.array([list(map(int, c.split(','))) for c in cs]).reshape(-1, 3)
    face = [tuple(p) for p in P if p.sum() == C] if len(P) else []
    hist.append((int(g), face))
last = [i for i, (g, f) in enumerate(hist) if f]
i = last[-1]
from collections import Counter
for g, f in hist[max(0, i - 60): i + 1: 6]:
    print(g, len(f), dict(sorted(Counter(int(min(p)) for p in f).items())))
