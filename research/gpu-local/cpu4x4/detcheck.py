#!/usr/bin/env python3
"""Independent check of rep.c's layer detectors and of the event derivation used in an.py, per generation.

T soups (numpy rng, density 0.4) on the (4,0,4) x 8 slab. Each is fed to the unmodified rep.exe as replica 0
(-i, W = 1, K = 1, cap CAP); the same soups are stepped by a plain numpy stepper (neighbour table from tslab, rule
B45/S345 written here), which records for every layer the last generation it had a live cell, the first generation
an outer layer is empty, the first generation the STATE has three cyclically consecutive empty layers in one of the
three transverse rings (looked up in the state, not from last-alive times), and whether the state at the face-death
generation has such a firewall.  Compared with rep's la columns and with the times derived from them.

    python -u detcheck.py T CAP SEED
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w
from w import tslab, geom
from analyze import death_times, ring_firewall, INF

T, CAP, SEED = map(int, sys.argv[1:4])
v = tslab.tslab(4, 0, 4)
n = len(v.cells); keys = [k for k, _ in v.layers]; nL = len(keys)
nb = v.nb.copy(); nb[nb < 0] = n
M = np.zeros((nL, n + 1), np.int32)
for L, (_, idx) in enumerate(v.layers):
    M[L, idx] = 1
rng = np.random.default_rng(SEED)
S = np.zeros((T, n + 1), np.int8); S[:, :n] = rng.random((T, n)) < 0.4
S0 = S.copy()
vb = os.path.join(HERE, 'tmp', f'det_{os.getpid()}.bin'); v.write(vb)
# rep on each soup
LA = np.zeros((T, nL), np.int64); GE = np.zeros(T, np.int64)
for t in range(T):
    ci = os.path.join(HERE, 'tmp', f'det_{os.getpid()}.txt'); open(ci, 'w').write('\n'.join(map(str, np.nonzero(S0[t, :n])[0])))
    pr = subprocess.run([w.REPX, vb, '1', '0.4', '1', str(CAP), '1', '-i', ci], capture_output=True, text=True, check=True)
    row = list(map(int, pr.stdout.splitlines()[0].split())); assert row[0] == 0
    LA[t] = row[4:4 + nL]; GE[t] = int(pr.stderr.split()[-1])
os.remove(vb); os.remove(ci)
# numpy stepper
la = np.full((T, nL), -1, np.int64)
outer = [keys.index((0, 1)), keys.index((0, 15))]
rings = [[i for i, k in enumerate(keys) if k[0] == d] for d in (1, 2, 3)]
face_first = np.full(T, -1, np.int64); fw_first = np.full(T, -1, np.int64); fw_at_face = np.zeros(T, bool)
ge = int(GE.max())
for g in range(ge + 1):
    alive = (S.astype(np.int32) @ M.T) > 0                      # [T, nL]
    use = g <= GE                                               # rep stops early only if all 64 replicas settled
    la[alive & use[:, None]] = g
    fw = np.zeros(T, bool)
    for r in rings:
        a = alive[:, r]; m = len(r)
        for i in range(m):
            fw |= ~a[:, i] & ~a[:, (i + 1) % m] & ~a[:, (i + 2) % m]
    newfw = fw & (fw_first < 0); fw_first[newfw] = g
    fd = (~alive[:, outer]).any(1) & (face_first < 0) & (g >= 1)
    face_first[fd] = g; fw_at_face[fd] = fw[fd]
    if g == ge:
        break
    c = S[:, nb].sum(2, dtype=np.int32)
    new = ((c == 4) | (c == 5) | ((c == 3) & (S[:, :n] == 1))).astype(np.int8)
    S[:, :n] = new
ok_la = np.array_equal(la, LA)
print(f'{T} soups, cap {CAP}: rep gen_end min {GE.min()} max {GE.max()}; la (32 layers, per generation) identical: {ok_la}; '
      f'mismatching entries {int((la != LA).sum())}')
D = death_times(LA, GE[:, None] * np.ones((1, nL)))
face = np.minimum(D[:, outer[0]], D[:, outer[1]])
fwt = np.minimum.reduce([ring_firewall(D[:, r], ring=True) for r in rings])
ff = np.where(face_first >= 0, face_first, INF); fwf = np.where(fw_first >= 0, fw_first, INF)
# derived times are only defined if the layer is dead at gen_end; direct ones compared where both finite or both inf
print('face death gen (derived la+1) == first empty outer layer (direct):', np.array_equal(face, ff),
      f'[{int(np.isfinite(ff).sum())} face deaths]')
print('firewall gen (derived) == first firewalled state (direct):', np.array_equal(fwt, fwf), f'[{int(np.isfinite(fwf).sum())} firewalls]')
k_direct = fw_at_face[np.isfinite(ff)]; k_der = (fwt <= face)[np.isfinite(ff)]
print('kind at face death (firewalled state: direct vs fw_time <= face_time):', np.array_equal(k_direct, k_der),
      f'[{int(k_direct.sum())} firewalled at face death]')
print('first-event face deaths (face < fw):', int((np.isfinite(face) & (face < fwt)).sum()), ' fw-first:', int((np.isfinite(fwt) & (fwt <= face)).sum()),
      ' fw strictly before face:', int((fwt < face).sum()), ' same generation:', int((np.isfinite(face) & (fwt == face)).sum()))
