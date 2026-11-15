"""Lead's own check of the fourth push's rake gun (2026-11-15).  Uses only reference/oracle.py and the cell lists
capL, unit, gun of research/signals/objects/gun-5f.json (not the push's rake units, not its stepper, not its
expected states).

Object(N) = capL + N units of bare wire C (unit moved by k (2,0,-2), k = 0..N-1) + gun moved by N units, alone in
empty space.  Claim (research/signals/README.md section 20): a standing object of period 4 at the +v end of bare
wire C puts one moving object on the wire every 4 generations and is itself exactly restored.

Checked here, cell for cell, with D_j = state(4j) XOR state(0):
  1  the cells at x >= 2N (the gun's own units) are the same at t and t + 4 for every t <= 4J, and differ at t, t + 2;
  2  D_1 is not empty and lies wholly on the wire (x < 2N);
  3  D_(j+1) = D_j moved two units towards -v, together with D_1, for j = 1..J-1: each period adds one more copy
     of the same thing, and every earlier copy has moved on two units, unchanged;
  4  control: the same object without the gun's cells does not do this (D_2 is not D_1 moved plus D_1).

    python3 research/audit/signals_gun_lead_check.py [N]        (default N = 24; about 20 s)
"""
import json, sys
import numpy as np
sys.path.insert(0, 'reference')
import oracle

N = int(sys.argv[1]) if len(sys.argv) > 1 else 24
J = (N - 6) // 2
ob = json.load(open('research/signals/objects/gun-5f.json'))
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
capL, unit, gun = ([tuple(c) for c in ob[k]] for k in ('capL', 'unit', 'gun'))
wire = set(capL) | {tr(c, k) for c in unit for k in range(N)}
full = wire | {tr(c, N) for c in gun}
assert len(full) == len(capL) + N * len(unit) + len(gun)
H = 128
OFF = (20, 64, 2 * N + 40)                     # even offsets keep the cell classes
m = oracle.masks(H); valid = m[0] | m[1] | m[2]


def arr(cs):
    h = np.zeros((H, H, H), dtype=bool)
    for c in cs:
        x = tuple(c[i] + OFF[i] for i in range(3))
        assert all(8 <= v < H - 8 for v in x) and valid[x], (c, x)
        h[x] = True
    return h


def shift(a, k):                               # k units towards +v
    return np.roll(np.roll(a, 2 * k, axis=0), -2 * k, axis=2)


def history(h, T):
    out = [h]
    for _ in range(T):
        h = oracle.step(h, m); out.append(h)
    return out


gunzone = np.zeros((H, H, H), dtype=bool); gunzone[2 * N + OFF[0]:, :, :] = True
hist = history(arr(full), 4 * J)
ok = True
p4 = all(np.array_equal(hist[t][gunzone], hist[t + 4][gunzone]) for t in range(4 * J - 3))
p2 = any(not np.array_equal(hist[t][gunzone], hist[t + 2][gunzone]) for t in range(4 * J - 1))
ok &= p4 and p2
print(f'N = {N}, {len(full)} cells, {4 * J} generations on the oracle')
print(f'1  the gun\'s units repeat every 4 generations: {p4}; not every 2: {p2}')
D = [hist[4 * j] ^ hist[0] for j in range(J + 1)]
on_wire = bool(D[1].any()) and not (D[1] & gunzone).any()
ok &= on_wire
print(f'2  after one period the state differs from the start in {int(D[1].sum())} cells, all on the wire: {on_wire}')
grow = all(np.array_equal(D[j + 1], shift(D[j], -2) | D[1]) and not (shift(D[j], -2) & D[1]).any() for j in range(1, J))
ok &= grow
print(f'3  each period adds one more copy and moves the earlier ones two units towards -v, unchanged, {J - 1} times: {grow}')
print(f'   cells changed after {J} periods: {int(D[J].sum())} = {J} x {int(D[1].sum())}: {int(D[J].sum()) == J * int(D[1].sum())}')
hc = history(arr(wire), 8)
Dc = [hc[4 * j] ^ hc[0] for j in range(3)]
ctrl = not np.array_equal(Dc[2], shift(Dc[1], -2) | Dc[1])
ok &= ctrl
print(f'4  control, the same wire with no gun: does not do this: {ctrl}')
print('PASS' if ok else 'FAIL')
