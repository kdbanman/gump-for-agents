#!/usr/bin/env python3
"""round4_score.py: F1-F6 of PREDICTIONS.md "Round 4", scored as in "Round 4 definitions", from data/r4_company.csv.

    python3 research/dying/round4_score.py

Errors: each C, V from its bootstrap s.e.; derived quantities by propagating independent errors (levels are
different face sets, so independent; the caught and control sets are independent).
"""
import os, csv, math
HERE = os.path.dirname(os.path.abspath(__file__))
R = {}
for r in csv.DictReader(open(os.path.join(HERE, 'data', 'r4_company.csv'))):
    R[(int(r['A']), float(r['p']), r['kind'])] = r
MINF = 200


def get(A, p, kind='caught', f='C'):
    r = R.get((A, p, kind))
    if r is None or int(r['n_faces']) < MINF: return None
    return float(r[f]), float(r[f + '_se'])


def reached(A, p): return get(A, p) is not None


def fmt(v): return f'{v[0]:.4f} ± {v[1]:.4f}'


def mean(vs):
    m = sum(v[0] for v in vs) / len(vs); e = math.sqrt(sum(v[1] ** 2 for v in vs)) / len(vs); return m, e


print('reached (>= 200 caught faces with k >= 1):', {A: [p for p in (0.9, 0.75, 0.6, 0.45, 0.3, 0.15) if reached(A, p)] for A in (63, 84, 108)})
# F1
for A, lv in ((84, (0.15, 0.3, 0.45)), (108, (0.3, 0.45)), (108, (0.15, 0.3, 0.45)), (63, (0.15, 0.3, 0.45))):
    if not all(reached(A, p) for p in lv): print(f'F1 A={A} {lv}: not reached'); continue
    c = [get(A, p) for p in lv]; m = mean(c)[0]
    dev = max(abs(x[0] - m) / m for x in c) if len(lv) == 3 else abs(c[0][0] - c[1][0]) / m
    lab = 'max |C_i - m|/m' if len(lv) == 3 else '|C(0.3) - C(0.45)|/mean'
    print(f'F1 A={A} levels {lv}: C = {[fmt(x) for x in c]}; {lab} = {dev:.4f} (holds if <= 0.15): {"held" if dev <= 0.15 else "failed"}')
    if 0.15 in lv:
        a, b = get(A, 0.15), get(A, 0.45); q = a[0] / b[0]; qe = q * math.hypot(a[1] / a[0], b[1] / b[0])
        print(f'   against clause C(0.15)/C(0.45) = {q:.4f} ± {qe:.4f} (< 0.6: {"met" if q < 0.6 else "not met"})')
# F2, F5
lv108 = [p for p in (0.3, 0.15) if reached(108, p)]
m108 = mean([get(108, p) for p in lv108])
print(f'F2: levels {lv108} at A=108, mean C = {fmt(m108)} (holds if in [0.47, 0.63]): {"held" if 0.47 <= m108[0] <= 0.63 else "failed"}')
for A in (63, 84):
    mA = mean([get(A, p) for p in lv108]); d = (mA[0] - m108[0], math.hypot(mA[1], m108[1]))
    print(f'F5 (A={A} vs 108, levels {lv108}): mean C {fmt(mA)}; difference {fmt(d)}' + (' (holds if in [0.03, 0.12]): ' + ('held' if 0.03 <= d[0] <= 0.12 else 'failed') if A == 63 else ' (not scored)'))
# F3
for A in (108, 84, 63):
    c9, c75, c3 = get(A, 0.9), get(A, 0.75), get(A, 0.3)
    raw = {p: float(R[(A, p, 'caught')]['C_raw']) for p in (0.9, 0.75, 0.3)}
    S = raw[0.9] / c9[0]
    ok = abs(c9[0] - 0.9) <= 0.08 and abs(c75[0] - 0.75) <= 0.08 and c3[0] - 0.3 >= 0.2
    dd = [round(get(A, p)[0] - p, 4) for p in (0.9, 0.75, 0.6, 0.45, 0.3, 0.15) if reached(A, p)]
    print(f'F3 A={A}{" (scored)" if A == 108 else ""}: C(0.9)-0.9 = {c9[0] - 0.9:+.4f} ± {c9[1]:.4f}; C(0.75)-0.75 = {c75[0] - 0.75:+.4f} ± {c75[1]:.4f}; '
          f'C(0.3)-0.3 = {c3[0] - 0.3:+.4f} ± {c3[1]:.4f}: {"held" if ok else "failed"}. Raw form C_raw - pS: '
          f'{raw[0.9] - 0.9 * S:+.4f}, {raw[0.75] - 0.75 * S:+.4f} (S = {S:.4f}). C(p)-p over reached levels: {dd}')
# F4
for A in (108, 84, 63):
    V = {p: get(A, p, f='V') for p in (0.9, 0.75, 0.6, 0.45, 0.3, 0.15) if reached(A, p)}
    Vc = {p: get(A, p, 'control', 'V') for p in V}
    p1 = 0.15 if 0.15 in V else None
    a = V[0.9][0] < 0.05 and V[0.75][0] < 0.05
    s = f'F4 A={A}: V = {{{", ".join(f"{p}: {fmt(v)}" for p, v in V.items())}}}; control {{{", ".join(f"{p}: {fmt(v)}" for p, v in Vc.items())}}}. '
    s += f'V(0.9), V(0.75) < 0.05: {a}. '
    if p1:
        d1 = V[0.15][0] - V[0.3][0]; d2 = V[0.3][0] - V[0.45][0]; rr = d1 / d2
        rre = abs(rr) * math.hypot(math.hypot(V[0.15][1], V[0.3][1]) / d1, math.hypot(V[0.3][1], V[0.45][1]) / d2)
        b = abs(rr - 1) <= 0.3; s += f'[V(0.15)-V(0.3)]/[V(0.3)-V(0.45)] = {rr:.3f} ± {rre:.3f} (within 0.3 of 1: {b}). '
    else:
        b = None; s += 'linearity clause: 0.15 not reached. '
    c = Vc[0.45][0] < V[0.45][0] / 2; s += f'V_control(0.45)/V(0.45) = {Vc[0.45][0] / V[0.45][0]:.3f} (< 0.5: {c}). '
    s += 'Overall: ' + ('held' if a and b and c else 'failed' if b is not None else 'linearity clause not scorable here')
    print(s)
# F6
for A in (63, 84, 108):
    if not reached(A, 0.15): print(f'F6 A={A}: 0.15 not reached'); continue
    q = get(A, 0.15)[0] / get(A, 0.45)[0]; v, vc = get(A, 0.3, f='V'), get(A, 0.3, 'control', 'V')
    print(f'F6 A={A}: C(0.15)/C(0.45) = {q:.4f} (< 0.6: {q < 0.6}); V(0.3)/V_control(0.3) = {v[0] / vc[0]:.3f} (<= 1.5: {v[0] / vc[0] <= 1.5}); '
          f'met: {q < 0.6 and v[0] / vc[0] <= 1.5}')
