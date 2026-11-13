#!/usr/bin/env python3
"""Half-space x < Lx live on an Lx x 4 x 4 cube torus: uncapped rule (fronts advance 1 cube/gen) vs gump (threshold.md section 3).
   python3 research/theory/front.py"""
import numpy as np, sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from energy import OFF, Stepper
def torus(Lx,Ly,Lz):
    M=(2*Lx,2*Ly,2*Lz)
    cells=[(x,y,z) for x in range(M[0]) for y in range(M[1]) for z in range(M[2]) if (x&1)+(y&1)+(z&1)==1]
    idx={c:i for i,c in enumerate(cells)}
    nb=np.array([[idx[tuple((c[k]+o[k])%M[k] for k in range(3))] for o in OFF[[k for k in range(3) if c[k]&1][0]]] for c in cells])
    return cells,nb
for cap in (False, True):
  for Lx in (8,16,32,64):
    cells,nb=torus(Lx,4,4); st=Stepper(nb)
    X=np.array([c[0] for c in cells])
    for name,init in (('slab x<Lx',(X<Lx)),):
        x=init.astype(np.int8); seen={}
        for t in range(20000):
            k=x.tobytes()
            if k in seen: break
            seen[k]=t; x,_=st.step(x,cap)
        print('cap' if cap else 'uncapped', 'Lx',Lx, name, 'settles at', seen[k], 'period', t-seen[k], 'final density', x.mean().round(3))
