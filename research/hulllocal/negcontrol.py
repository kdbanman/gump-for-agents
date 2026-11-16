# Negative control for hl.py's oracle check: one neighbour entry of a face cell duplicated must MISMATCH.
# python3 research/hulllocal/negcontrol.py   (from the repository root)
import sys; sys.path.insert(0,'research/hulllocal'); import hl, numpy as np
v=hl.hull(13); orig=hl.hull
def broken(R):
    w=orig(R); i=w.faces[0][5]; w.nb[i,0]=w.nb[i,1]; return w
hl.hull=broken; print('control, one neighbour entry duplicated:', hl.check_hull(13,300))
