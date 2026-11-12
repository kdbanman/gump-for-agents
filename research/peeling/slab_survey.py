import geom, numpy as np, sys
m=int(sys.argv[1]); cap=int(sys.argv[2])
for N in map(int, sys.argv[3].split(',')):
    v=geom.slab(N,m); st,pop,la=v.run(8,0.4,N*100+m,cap,16)
    keys=[k for k,_ in v.layers]; ge=v.gen_end
    f0=la[:,keys.index((0,1))]; f1=la[:,keys.index((0,2*m-1))]
    dead0=f0<ge; dead1=f1<ge
    first=np.where(dead0|dead1, np.minimum(np.where(dead0,f0,ge),np.where(dead1,f1,ge)), -1)
    print(f"N={N} m={m} A={3*N*N} cells={len(v.cells)} end={ge} settled={np.sum(st>=0)}/512 any-face-dead={np.sum(dead0|dead1)} median first={np.median(first[first>=0]) if np.any(first>=0) else None} mean={first[first>=0].mean() if np.any(first>=0) else None}")
