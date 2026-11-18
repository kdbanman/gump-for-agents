#!/usr/bin/env python3
"""validate.py (blast/model): the graph stepper used for the population histograms (research/dying/ex3.c, whose
dynamics is research/theory/symmetric/sy.c) against a naive stepper written here from reference/oracle.py's
neighbour offsets and rule constants only.

For each wrapped slab "gen_a_k_b_c1" (8 {111} layers s = 1..15, period lattice a*(2,0,-2) + k*(0,2,-2), b*(0,2,-2);
outside the slab dead for ever) and each hull "oct_R_c_c1":
  1. a random 0.4-soup is stepped T generations by the naive stepper (a dict of doubled coordinates; the wrap is
     done here by integer division, not by geom.py);
  2. the same soup is given to `sy trace` on geom.py's graph file; compared: the population at every generation
     0..T and the full cell set at generations 1, 2, 3, 10, 100 and T (sy prints the final node list);
  3. negative control: one neighbour slot of one node of the graph file is redirected to another node; the
     comparison must fail;
  4. ex3's lives file must be byte-identical to sy's on a short renewal run (same seed).

    python3 research/blast/model/validate.py [T] [SPEC ...]     (default T = 1500)
"""
import os, subprocess, sys, tempfile, random
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SCR = os.path.join(ROOT, 'research', 'scratch', 'blast', 'model')
sys.path.insert(0, os.path.join(ROOT, 'reference'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'theory', 'symmetric'))
from oracle import offsets, BIRTH, SURVIVE      # ground truth: neighbourhood and rule
import geom                                      # only to learn which node of the graph file is which cell

SY = os.path.join(SCR, 'sy'); EX3 = os.path.join(SCR, 'ex3')


def axis_of(p):
    return [i for i in range(3) if p[i] % 2][0]


def make_slab(a, k, b):
    def canon(p):
        x, y, z = p
        s = x + y + z
        if s < 1 or s > 15:
            return None
        m = x // (2 * a); x -= 2 * a * m; y -= 2 * k * m
        y %= 2 * b
        return (x, y, s - x - y)
    cells = set()
    for s in range(1, 16, 2):
        for x in range(2 * a):
            for y in range(2 * b):
                p = (x, y, s - x - y)
                if sum(c % 2 for c in p) == 1:
                    cells.add(p)
    return cells, canon


def make_oct(R):
    cells = set()
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            for z in range(-R, R + 1):
                if abs(x) + abs(y) + abs(z) <= R and (x % 2) + (y % 2) + (z % 2) == 1:
                    cells.add((x, y, z))
    return cells, (lambda p: p if p in cells else None)


def naive_step(live, cells, canon):
    cnt = {}
    for p in live:
        for o in offsets(axis_of(p)):
            q = canon((p[0] + o[0], p[1] + o[1], p[2] + o[2]))
            if q is not None:
                cnt[q] = cnt.get(q, 0) + 1
    new = set()
    for q, n in cnt.items():
        if (q in live and n in SURVIVE) or (q not in live and n in BIRTH):
            new.add(q)
    return new


def sy_trace(graph, nodes, T):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
        fh.write(' '.join(str(i) for i in sorted(nodes)) + '\n'); init = fh.name
    out = subprocess.run([SY, graph, 'trace', init, str(T)], capture_output=True, text=True).stdout.split('\n')
    os.unlink(init)
    pops = []; final = None
    for ln in out:
        t = ln.split()
        if len(t) == 2 and t[0].isdigit() and len(pops) == int(t[0]):
            pops.append(int(t[1]))
        elif ln.startswith('final') or (len(pops) == T + 1 and ln.strip()):
            final = set(int(x) for x in ln.replace('final', '').replace(':', ' ').split())
    return pops, final


def check(spec, T, graph=None, quiet=False):
    t = spec.split('_')
    if t[0] == 'gen':
        cells, canon = make_slab(int(t[1]), int(t[2]), int(t[3]))
    else:
        cells, canon = make_oct(int(t[1]))
    q = geom.build(spec)
    f = q.f
    node_of = {tuple(int(c) for c in f.cells[i]): int(q.orb[i]) for i in range(len(f.cells))}
    assert set(node_of) == cells, (len(node_of), len(cells))
    assert len(set(node_of.values())) == len(cells)          # c1: one node per cell
    if graph is None:
        graph = os.path.join(SCR, f'graph_{spec}.txt')
        if not os.path.exists(graph):
            geom.write_graph(q, graph)
    rng = random.Random(20261118)
    live = set(p for p in sorted(cells) if rng.random() < 0.4)
    init_nodes = set(node_of[p] for p in live)
    marks = [m for m in (1, 2, 3, 10, 100, T) if m <= T]
    pops_n = [len(live)]; states = {}
    cur = live
    for g in range(1, T + 1):
        cur = naive_step(cur, cells, canon); pops_n.append(len(cur))
        if g in marks:
            states[g] = set(node_of[p] for p in cur)
    pops_s, _ = sy_trace(graph, init_nodes, T)
    ok = pops_s == pops_n
    for m in marks:
        _, fin = sy_trace(graph, init_nodes, m)
        ok = ok and fin == states[m]
    if not quiet:
        print(f'{spec}: cells {len(cells)}, T {T}, population at T {pops_n[-1]} (min over run {min(pops_n)}), '
              f'{"MATCH" if ok else "MISMATCH"} (populations at every generation, cell sets at {marks})')
    return ok


def negative(spec, T):
    graph = os.path.join(SCR, f'graph_{spec}.txt')
    lines = open(graph).read().split('\n')
    n = int(lines[0]); row = lines[1 + n // 2].split()
    old = int(row[0]); row[0] = str((old + 7) % n)
    lines[1 + n // 2] = ' '.join(row)
    bad = os.path.join(SCR, f'graph_{spec}_bad.txt'); open(bad, 'w').write('\n'.join(lines))
    ok = check(spec, T, graph=bad, quiet=True)
    os.unlink(bad)
    print(f'{spec}: negative control (one neighbour slot of node {n // 2} redirected): '
          f'{"FAILS AS IT SHOULD" if not ok else "PASSED: THE CHECK IS BLIND"}')
    return not ok


def same_lives(spec):
    graph = os.path.join(SCR, f'graph_{spec}.txt')
    a = os.path.join(SCR, f'v_sy_{spec}.bin'); b = os.path.join(SCR, f'v_ex_{spec}.bin')
    subprocess.run([SY, graph, 'run', '77', '0.4', '20000', '4', a], capture_output=True)
    subprocess.run([EX3, graph, 'run', '77', '0.4', '20000', '4', b, '30', '512', os.path.join(SCR, 'v_h.txt'), '-1',
                    os.path.join(SCR, 'v_d.bin'), '512'], capture_output=True)
    same = open(a, 'rb').read() == open(b, 'rb').read() and os.path.getsize(a) > 0
    print(f'{spec}: ex3 lives file {"identical to" if same else "DIFFERS FROM"} sy\'s ({os.path.getsize(a)} bytes)')
    for p in (a, b, os.path.join(SCR, 'v_h.txt'), os.path.join(SCR, 'v_d.bin')):
        if os.path.exists(p):
            os.unlink(p)
    return same


if __name__ == '__main__':
    args = sys.argv[1:]
    T = int(args[0]) if args and args[0].isdigit() else 1500
    specs = [a for a in args if not a.isdigit()] or ['gen_4_0_4_c1', 'gen_1_7_19_c1', 'gen_1_4_21_c1',
                                                     'gen_1_8_20_c1', 'gen_1_5_22_c1', 'gen_1_4_22_c1',
                                                     'gen_1_12_28_c1', 'gen_1_4_28_c1', 'oct_9_c_c1', 'oct_11_c_c1',
                                                     'oct_13_c_c1']
    allok = True
    for s in specs:
        allok &= check(s, T) and negative(s, T) and same_lives(s)
    print('ALL OK' if allok else 'FAILED')
