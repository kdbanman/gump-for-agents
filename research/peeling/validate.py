"""Bit-exact check of rep.c against gump (torus soup, slab-in-torus, octahedral soup) + slab neighbour counts."""
import sys, subprocess, numpy as np
import os; os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,'.')
import geom
G='../../engine/target/release/gump'; S='../scratch/peeling'
def check(v, gargs, gens):
    subprocess.run([G,'convert',*gargs,'--cells-out',f'{S}/c.txt'],check=True,capture_output=True)
    pts=[tuple(map(int,l.split())) for l in open(f'{S}/c.txt') if l.strip() and not l.startswith('#')]
    idx={p:i for i,p in enumerate(v.cells)}
    if 'torus' in v.name:
        N=int(gargs[gargs.index('--torus')+1]); pts=[tuple(x%(2*N) for x in p) for p in pts]
    open(f'{S}/ci.txt','w').write('\n'.join(str(idx[p]) for p in pts))
    geom.build_rep(); v.write(f'{S}/vv.bin')
    out=subprocess.run([geom.REP,f'{S}/vv.bin','1','0.3','1',str(gens),'8','-i',f'{S}/ci.txt','-t'],capture_output=True,text=True).stdout
    mine=[int(l.split()[2]) for l in out.splitlines() if l.startswith('T')]
    subprocess.run([G,'run',*gargs,'--gens',str(gens),'--no-halt','--poplog',f'{S}/pl.txt'],check=True,capture_output=True)
    ref=[int(l.split()[1]) for l in open(f'{S}/pl.txt')]
    n=min(len(mine),len(ref)); print(v.name, n, 'match' if mine[:n]==ref[:n] else 'MISMATCH', mine[:5], ref[:5], mine[n-1], ref[n-1])
check(geom.torus(6), ['--soup','0.4','--torus','6','--rng','3'], 3000)
check(geom.torus(9), ['--soup','0.4','--torus','9','--slab-layers','5','--rng','4'], 3000)
check(geom.octa(15), ['--soup','0.3','--radius','15','--rng','5'], 3000)
v=geom.slab(5,6)
cnt=(v.nb>=0).sum(1); import collections
t=[(sum(p)-1)//2 for p in v.cells]
print(collections.Counter(zip(t,cnt)))
