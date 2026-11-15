#!/usr/bin/env python3
"""ana.py: lifetimes from st.c records (own estimator).
    python3 ana.py            # every lives_*.bin in research/scratch/audit_symmetric
ln tau_face = ln(nf * E / D) +- 1/sqrt(D), E = sum max(0, age - T0), D = face deaths (F or F+W) at age > T0,
T0 = 512; nf = number of face orbits (from geo.py). Settled lives: age = snapshot age (upper bound); 'S-low'
counts them to half that age (the previous Brent snapshot; a lower bound). Per face orbit: deaths attributed to
the orbit(s) whose faces died; tau_orbit = E / D_orbit.
"""
import glob, os, sys, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import geo
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit_symmetric')


def load(path):
    r = np.fromfile(path, dtype=np.uint32).reshape(-1, 4)
    return r[:, 0].astype(np.int64), r[:, 1].astype(np.int64), r[:, 2].astype(np.int64), r[:, 3].astype(np.int64)


def est(age, ty, nf, t0=512):
    E = np.clip(age - t0, 0, None).sum(); late = age > t0
    D = int((((ty == 1) | (ty == 3)) & late).sum())
    return E, D, (math.log(nf * E / D) if D else float('nan')), (1 / math.sqrt(D) if D else float('nan'))


def main():
    rows = []
    for f in sorted(glob.glob(os.path.join(SCR, 'lives_*.bin'))):
        base = os.path.basename(f)[6:-4]; sysname, gname, seed = base.split('_')
        S, nb, orb, gens = geo.build(sysname, gname)
        _, fg = geo.summary(S, nb, orb, gens, gname)
        nf = len(fg)
        age, ty, fm, det = load(f)
        if len(age) == 0:
            continue
        E, D, lt, se = est(age, ty, nf)
        lowage = np.where(ty == 4, age // 2, age)
        _, _, ltl, _ = est(lowage, ty, nf)
        _, D128, lt128, _ = est(age, ty, nf, 128); _, D2k, lt2k, se2k = est(age, ty, nf, 2048)
        n = {k: int(((ty == k) & (age > 512)).sum()) for k in (1, 2, 3, 4, 5)}
        line = (f'{sysname:6s} {gname:4s} {seed:6s} A={len(S.faces[0]):3d} nf={nf} lives={len(age):7d} D={D:6d} '
                f'lntau={lt:8.4f} +- {se:.4f}  S-low {ltl:.4f}  T0=128 {lt128:.4f}  T0=2048 {lt2k:.4f} +- {se2k:.4f}  '
                f'F={n[1]} W={n[2]} X={n[3]} S={n[4]} open={n[5]}  Sexpo={np.clip(age[ty == 4] - 512, 0, None).sum() / E:.4f}')
        print(line)
        # per face orbit
        if nf > 1 and gname != 'c1':
            late = (age > 512) & ((ty == 1) | (ty == 3))
            parts = []
            for k, mem in enumerate(fg):
                mask = sum(1 << a for a in mem)
                Dk = int((late & ((fm & mask) != 0)).sum())
                names = '/'.join(''.join('+' if v > 0 else '-' for v in S.facenames[a]) for a in mem) if sysname[0] == 'v' else str(mem)
                parts.append(f'{names}: D={Dk} ln(E/D)={math.log(E / Dk) if Dk else float("nan"):.4f} +- {1 / math.sqrt(Dk) if Dk else 0:.4f}')
            multi = int((late & np.array([bin(int(x)).count('1') > len(fg[0]) for x in fm])).sum())
            print('     per face orbit: ' + '; '.join(parts) + f'; deaths with more than one orbit dead at once: {multi}')


if __name__ == '__main__':
    main()
