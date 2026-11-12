"""Brute-force checks of the structure theorems in docs/AUTOMATON.md (T1-T4). Run: python3 reference/check_theory.py"""
import itertools, collections, numpy as np
from oracle import offsets, masks, step
# T1: for every orientation and every body diagonal d, histogram of d.offset over the 12 neighbours
ok = True
for a in range(3):
    for d in itertools.product((1,-1), repeat=3):
        h = collections.Counter(sum(di*oi for di,oi in zip(d,o)) for o in offsets(a))
        ok &= (dict(h) == {-4:1, -2:2, 0:6, 2:2, 4:1})
print("T1 layer histogram {-4:1,-2:2,0:6,+2:2,+4:1} for all 3 orientations x 8 diagonals:", ok)
# axis-aligned half-space: max neighbours a cell at distance 1 outside can have inside
for a in range(3):
    for ax in range(3):
        h = collections.Counter(o[ax] for o in offsets(a))
        print(f"  normal={a} along axis {ax}: offsets along axis -> {dict(sorted(h.items()))}")
# unit closed cube is a still life?
H=16; idx=np.indices((H,H,H)); masks_=masks(H); h=np.zeros((H,H,H),np.int8)
for p in [(7,8,8),(9,8,8),(8,7,8),(8,9,8),(8,8,7),(8,8,9)]: h[p]=1
h2=step(h,masks_); print("closed unit cube still life:", bool((h2==h).all()), "pop", int(h.sum()))
# random soup in one {111} layer stays in the layer; 3 dead layers = firewall (random soup both sides)
rng=np.random.default_rng(1); H=48; idx=np.indices((H,H,H)); masks_=masks(H); valid=masks_[0]|masks_[1]|masks_[2]; s=idx.sum(0)
box=(idx>=8).all(0)&(idx<40).all(0)
h=((rng.random((H,H,H))<0.4)&valid&box&(s==71)).astype(np.int8); layers0=set(np.unique(s[h==1]))
pops=[]
for g in range(60): h=step(h,masks_); pops.append(int(h.sum())); assert set(np.unique(s[h==1]))<=layers0
print("single-layer soup stays in its layer for 60 gens; pops:", pops[:8], "...", pops[-3:])
h=((rng.random((H,H,H))<0.35)&valid&box&((s<=67)|(s>=75))).astype(np.int8)   # dead layers 69,71,73
for g in range(200):
    h=step(h,masks_); assert not h[(s>=69)&(s<=73)].any()
print("3-layer dead slab stayed dead for 200 gens with soup on both sides; pop now", int(h.sum()))
h=((rng.random((H,H,H))<0.35)&valid&box&((s<=67)|(s>=73))).astype(np.int8)   # only 2 dead layers 69,71
br=None
for g in range(200):
    h=step(h,masks_)
    if h[(s>=69)&(s<=71)].any(): br=g+1; break
print("2-layer dead slab breached at gen:", br)
