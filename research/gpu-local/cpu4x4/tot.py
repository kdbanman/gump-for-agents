import glob, os, sys, math
import numpy as np
for d in sys.argv[1:]:
    E = 0.0; F = 0; W = 0; n = 0; S = 0
    for f in sorted(glob.glob(os.path.join(d, 'ch_4_0_4_s*.npz'))):
        o = np.load(f); st = o['settle']; ge = int(o['gen_end'])
        stop = np.where(st >= 0, st, ge).astype(float); fwm = o['fw'].min(1); face = o['face']
        end = np.minimum.reduce([face, fwm, stop]); kF = (face == end) & (face < fwm) & (face <= stop)
        kW = (fwm == end) & (fwm <= face) & (fwm <= stop)
        E += end.sum(); F += int(kF.sum()); W += int(kW.sum()); n += len(end); S += int(((stop == end) & ~kF & ~kW & (st >= 0)).sum())
    print(f'{d}: lives {n} E {E:.6g} F {F} W {W} settled {S} F/E {F / E * 1e5:.4f}e-5 ln(2E/F) = {math.log(2 * E / F):.4f} +- {1 / math.sqrt(F):.4f}')
