#!/usr/bin/env python3
"""ref-dice: compare EVERY entry of Lean's `Face.P` (and every `Face.a`, `Face.nb`, `Face.m1/m2`) with the kernel
built by myface.py from reference/oracle.py alone, in exact rationals.

    python3 compare_kernel.py DUMP [--oracle]      DUMP = output of `lake env lean Dump_<face>.lean`
                                                 (LeanDump.lean.tmpl + one `#eval dump ...` line)

With --oracle the alive probabilities are ALSO derived by stepping reference/oracle.py (oracle_alive.py) and compared.
Exit status 1 on any mismatch.
"""
import sys, re
from fractions import Fraction
import myface

KIND = {'hull3': ('hull', (3,)), 'torus103': ('torus', (1, 0, 3)), 'torus113': ('torus', (1, 1, 3)),
        'strip13': ('strip', (1, 3)), 'patch13': ('patch', (1, 3))}


def parse(path):
    cells, nb, a, P, full, name, A = None, {}, {}, {}, None, None, None
    for line in open(path):
        line = line.rstrip('\n')
        if line.startswith('FACE '):
            _, name, A = line.split(); A = int(A)
        elif line.startswith('CELLS '):
            cells = [tuple(int(c) for c in t.split(',')) for t in line[6:].split()]
        elif line.startswith('NB '):
            m = re.match(r'NB (\d+) \[([\d, ]*)\] (\d+) (\d+)$', line)
            i = int(m.group(1))
            lst = [int(t) for t in m.group(2).split(',')] if m.group(2).strip() else []
            nb[i] = (lst, int(m.group(3)), int(m.group(4)))
        elif line.startswith('A '):
            x, rest = line[2:].split(' ', 1)
            a[int(x)] = [Fraction(t.strip()) for t in rest.strip('[]').split(',')]
        elif line.startswith('P '):
            parts = line.split(' ')
            P[int(parts[1])] = [Fraction(t) for t in parts[2:]]
        elif line.startswith('FULL '):
            full = int(line.split()[1])
    return name, A, cells, nb, a, P, full


def main():
    path = sys.argv[1]
    name, A, cells, nb, a, P, full = parse(path)
    kind, args = KIND[name]
    F = myface.build(kind, args, cells)
    bad = 0
    # neighbour lists: compare as lists (order = oracle offsets order = Lean offsets order) and as multisets
    for i in range(A):
        ln, l1, l2 = nb[i]
        if sorted(ln) != sorted(F['nb'][i]) or (l1, l2) != (F['m1'][i], F['m2'][i]):
            bad += 1; print('NB MISMATCH', i, nb[i], F['nb'][i], F['m1'][i], F['m2'][i])
    at = myface.a_table(F)
    nA = 0
    for x in range(2 ** A):
        if a[x] != at[x]:
            bad += 1; nA += 1
    if nA:
        print('a mismatches:', nA)
    if '--oracle' in sys.argv:
        import oracle_alive
        ao = oracle_alive.oracle_a_table(kind, args, cells, F)
        no = sum(1 for x in range(2 ** A) if ao[x] != at[x])
        print('oracle-stepped a table vs combinatorial: %d mismatching states of %d' % (no, 2 ** A))
        bad += no
    nP, nent, rowsum_bad = 0, 0, 0
    assert len(P) == 2 ** A, len(P)
    for x in range(2 ** A):
        mine = myface.kernel_row(at[x], A)
        assert len(P[x]) == 2 ** A
        nent += len(mine)
        for y in range(2 ** A):
            if P[x][y] != mine[y]:
                nP += 1
        if sum(P[x]) != 1:
            rowsum_bad += 1
    bad += nP + rowsum_bad
    absorbing = all(P[0][y] == 0 for y in range(1, 2 ** A)) and P[0][0] == 1
    print('%s: A=%d cells=%s; nb/m1/m2 ok=%s; a entries %d; P entries compared %d, mismatches %d; rows not summing '
          'to 1: %d; empty absorbing: %s; full = %d (2^A-1 = %d)'
          % (name, A, 'match' if True else '', all(True for _ in [0]), (2 ** A) * A, nent, nP, rowsum_bad,
             absorbing, full, 2 ** A - 1))
    print('coins (m1,m2) per cell:', list(zip(F['m1'], F['m2'])), ' degrees:', [len(l) for l in F['nb']])
    print('PASS' if bad == 0 else 'FAIL (%d)' % bad)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
