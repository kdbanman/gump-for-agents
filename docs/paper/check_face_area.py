# Direct count used in draft.md, Section 5.1: cells with exactly one odd doubled coordinate and |p-c|_1 <= R, and the size A of the outermost {111} layer. Run: python3 docs/paper/check_face_area.py (about 10 s).
import itertools
def count(R, c):
    N=0; lay={}
    rng=range(-R-2,R+3)
    for x in rng:
        for y in rng:
            for z in rng:
                if (x%2)+(y%2)+(z%2)!=1: continue
                if abs(x-c[0])+abs(y-c[1])+abs(z-c[2])>R: continue
                N+=1
                s=(x-c[0])+(y-c[1])+(z-c[2])
                lay[s]=lay.get(s,0)+1
    smax=max(lay)
    return N,smax,lay[smax]
for R in (7,9,11,13,15,17,27,33,37):
    N,s,A=count(R,(0,0,0)); k=(R+1)//2
    print('cube-centred R',R,'N',N,'top layer s',s,'A',A,'3k(k+1)/2',3*k*(k+1)//2)
for R in (28,30,36,40,42,44):
    N,s,A=count(R,(1,1,1)); k=R//2
    print('vertex-centred R',R,'N',N,'top layer s',s,'A',A,'3k(k+1)/2',3*k*(k+1)//2)
