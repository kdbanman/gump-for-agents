"""Walls V | (0 to 3 arbitrary units) | C for the 11 family wires V: which are stationary, and does the mirror rake 5f,
arriving from the C side, come back as a rake f with the wall as it was?  python3 wallturn.py (90 s; sg.Geom,
family.Piece).  Prints each arrangement where a rake goes back with the wall restored, then the tally."""
import sys, itertools; sys.path.insert(0,'.')
import family as F
from collections import Counter
pc=F.Piece(100); g=pc.g
ring=F.ring()
W=[m for m in range(16) if (lambda z:(g and (ring and (F.ring().__class__))) ) and True]
# which uniform masks are wires
wires=[]
for m in range(16):
    sub=[i for i in range(4) if m>>i&1]
    z=F.wire_state(ring,sub)
    if (ring.run(z,2)==z).all(): wires.append(m)
print('wires',[hex(m) for m in wires])
tally=Counter(); found=[]
for V in wires:
  for k in range(0,4):
    for ins in itertools.product(range(16),repeat=k):
        fn=lambda u: V if u<0 else (ins[u] if u<k else 0xb)
        z=pc.config(fn)
        if pc.decode(g.run(z,2,sparse=True),-30,30)!=pc.decode(z,-30,30): continue
        tally['stat']+=1
        x=pc.config(lambda u: 5 if u==k+12 else (0xf if u==k+13 else fn(u)))
        y=g.run(x,56,sparse=True); zz=g.run(z,56,sparse=True)
        dy=pc.decode(y,-40,60); dz=pc.decode(zz,-40,60)
        diff=''.join(a if a!=b else '.' for a,b in zip(dy,dz))
        right=dy[40+k+1:]
        rake=any(right[i]=='f' and right[i-1] not in '95' for i in range(1,len(right)))
        restored = dy[36:40+k+1]==dz[36:40+k+1]
        if rake and restored:
            tally['rake back']+=1
            found.append((hex(V),[hex(i) for i in ins],restored,diff))
            print(hex(V),[hex(i) for i in ins],'restored' if restored else 'changed', diff, flush=True)
print(tally)
