"""push 8b: finite capped wires and their signals, each a standing object of empty space (checked by `python3
wires.py`: period 2, and each signal runs to the far cap, is swallowed, and the object is restored).

  capped_B(ua, ub)   eater cap (the left cap of objects/register-BBp.json) + units ua..ub-1 of wire B + its half-turn
  capped_C(ua, ub)   capL + units ua..ub-1 of wire C + capR of objects/clock-C.json
  SIGB               the symmetry (g, t) with SIGB(wire B) = wire B' in the same tube, same generation
"""
import json
import numpy as np
import lab
from lab import tr, unit, HT, MIR

_reg = lab.load('register-BBp')
_frame = [tuple(c) for c in (json.loads(_reg['frame']) if isinstance(_reg['frame'], str) else _reg['frame'])]
CAPL_B = [c for c in _frame if c[0] < 0]            # the -v cap of wire B; its wire begins at unit -6
CAPR_BP = [c for c in _frame if c[0] > 0]           # the +v cap of wire B' of the register; wire ends at unit 16
_clk = lab.load('clock-C')
CAPL_C = [tuple(c) for c in _clk['capL']]           # wire C begins at unit 0
CAPR_C = [tuple(c) for c in _clk['capR']]           # for N units: moved by N units


def capped_B(ua, ub):
    """cells (list of tuples) at an even generation: cap, wire B on units ua..ub-1, cap."""
    left = [tr(c, ua + 6) for c in CAPL_B]
    # the half-turn image of (left cap + wire) is wire B on units <= 7 and a cap on units 8, 9
    img = {HT(c) for c in CAPL_B} | {HT(tr(c, u)) for c in lab.B0 for u in range(-6, 4)}
    right = [tr(c, ub - 8) for c in img if unit(c) >= 8]
    body = [tr(c, u) for c in lab.B0 for u in range(ua, ub)]
    return sorted(set(left) | set(body) | set(right))


def capped_C(ua, ub):
    left = [tr(c, ua) for c in CAPL_C]
    right = [tr(c, ub) for c in CAPR_C]
    body = [tr(c, u) for c in lab.C0 for u in range(ua, ub)]
    return sorted(set(left) | set(body) | set(right))


def pulse(defect, u):
    """the two cells of a pulse on file (lab.PULSE_B has its first cell in unit 6), moved so that it is at unit u."""
    u0 = min(unit(c) for c in defect)
    return [tr(c, u - u0) for c in defect]


def SIGB(c):
    """wire B at an even generation -> wire B' at an odd generation, same tube, same direction (found by search:
    `python3 wires.py` checks it)."""
    return (-c[2], c[1], 6 - c[0])


if __name__ == '__main__':
    import line
    ok = True
    k = lab.pk(capped_B(-10, 10))
    good = lab.same(lab.run(k, 2), k) and not lab.same(lab.run(k, 1), k)
    ua, s = line.letters(k)
    print('PASS' if good else 'FAIL', f'capped wire B: {len(k)} cells, period 2;  units from {ua}: {s}'); ok &= good
    for name, d, u, dirn in (('pulse B right', lab.PULSE_B, -6, 1), ('pulse B left', [tuple(c) for c in lab.load('pulse-B-left')['defect']], 6, -1)):
        x = lab.xor(k, lab.pk(pulse(d, u)))
        # after 2j generations the difference is the pulse moved j units
        rigid = all(lab.same(lab.xor(lab.run(x, 2 * j), k), lab.pk(pulse(d, u + dirn * j))) for j in range(1, 9))
        healed = lab.same(lab.run(x, 80), k)
        print('PASS' if rigid and healed else 'FAIL', f'{name}: moves one unit per 2 generations for 8 units: {rigid}; swallowed by the cap, object restored at generation 80: {healed}')
        ok &= rigid and healed
    kc = lab.pk(capped_C(-10, 10))
    good = lab.same(lab.run(kc, 2), kc) and not lab.same(lab.run(kc, 1), kc)
    ua, s = line.letters(kc)
    print('PASS' if good else 'FAIL', f'capped wire C: {len(kc)} cells, period 2;  units from {ua}: {s}'); ok &= good
    for name, d, u, dirn in (('pulse C right (p>)', lab.PULSE_C, -6, 1), ('pulse C left (p<)', lab.PULSE_C_LEFT, 6, -1)):
        x = lab.xor(kc, lab.pk(pulse(d, u)))
        rigid = all(lab.same(lab.xor(lab.run(x, 2 * j), kc), lab.pk(pulse(d, u + dirn * j))) for j in range(1, 9))
        healed = lab.same(lab.run(x, 80), kc)
        print('PASS' if rigid and healed else 'FAIL', f'{name}: moves one unit per 2 generations for 8 units: {rigid}; swallowed by the cap, object restored at generation 80: {healed}')
        ok &= rigid and healed
    img = lab.pk([SIGB(tr(c, u)) for c in lab.B0 for u in range(-8, 9)])
    want = lab.pk([tr(c, u) for c in line.WBP[1] for u in range(-8, 9)])
    good = len(lab.xor(img, want)) <= 12 and all(abs(lab.unit(c)) >= 7 for c in lab.up(lab.xor(img, want)))
    print('PASS' if good else 'FAIL', "SIGB maps wire B (even generation) onto wire B' (odd generation), same axis and direction"); ok &= good
    kp = lab.run(lab.pk([SIGB(c) for c in capped_B(-10, 10)]), 1)
    ua, s = line.letters(kp)
    good = lab.same(lab.run(kp, 2), kp)
    print('PASS' if good else 'FAIL', f"capped wire B' = SIGB(capped wire B) one generation on: period 2; units from {ua}: {s}"); ok &= good
    print('ALL PASS' if ok else 'SOME FAIL')
