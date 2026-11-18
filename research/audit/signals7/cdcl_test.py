#!/usr/bin/env python3
"""The push's own SAT solver `cdcl7.cpp` (projected all-solutions enumeration) against brute force and against pysat.

    python3 cdcl_test.py small [K]     K random CNFs of 6..16 variables (clause widths 1..4), a random projection, a
                                       random cube: cdcl7's set of projected solutions == brute force over all 2^n
    python3 cdcl_test.py medium [K]    K random 3-CNFs of 60..140 variables near the threshold (thousands of conflicts,
                                       restarts, clause deletion), projection on 8..12 variables: cdcl7's set ==
                                       pysat (glucose4) enumeration with blocking clauses on the same projection
    python3 cdcl_test.py resume [K]    as medium, but cdcl7 is stopped by its time limit again and again and resumed
                                       from its own file; and split as pool7.py splits a cube (the parent's solutions
                                       copied into each child, the children's cubes partition it): union == pysat
    python3 cdcl_test.py ends C        the review's own CNF of the receiving ends at plane bound C (enum7.build),
                                       written as DIMACS: cdcl7's list == enum7's list (CaDiCaL)

cdcl7.cpp is compiled unchanged into the scratch directory (g++ -O2).
"""
import sys, os, subprocess, random, itertools, json, time
import orc7 as O

EXE = os.path.join(O.SCR, 'cdcl7')
SRC = os.path.join(O.PUSH, 'cdcl7.cpp')
TMP = os.path.join(O.SCR, 'cdcl_tmp'); os.makedirs(TMP, exist_ok=True)


def compile_():
    if not os.path.exists(EXE) or os.path.getmtime(EXE) < os.path.getmtime(SRC):
        subprocess.check_call(['g++', '-O2', '-std=c++17', '-o', EXE, SRC])


def write(stem, n, cl, proj, cube=None):
    with open(stem + '.cnf', 'w') as f:
        f.write(f'p cnf {n} {len(cl)}\n')
        for c in cl:
            f.write(' '.join(map(str, c)) + ' 0\n')
    open(stem + '.proj', 'w').write(' '.join(map(str, proj)) + '\n')
    if cube is not None:
        open(stem + '.cube', 'w').write(' '.join(map(str, cube)) + '\n')


def run(stem, secs=None, cube=False, sols=None):
    sols = sols or stem + '.sols'
    a = [EXE, stem + '.cnf', stem + '.proj', sols, str(secs if secs else 1e9)]
    if cube:
        a.append(stem + '.cube')
    p = subprocess.run(a, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    lines = [l for l in open(sols).read().split('\n') if l]
    return p.returncode, [l[2:] for l in lines if l.startswith('S ')], (lines[-1] if lines else '')


def brute(n, cl, proj, cube):
    out = set()
    for bits in itertools.product((0, 1), repeat=n):
        v = lambda l: bits[abs(l) - 1] == (1 if l > 0 else 0)
        if all(any(v(l) for l in c) for c in cl) and all(v(l) for l in cube):
            out.add(''.join(str(bits[p - 1]) for p in proj))
    return out


def pysat_enum(n, cl, proj, cube=()):
    from pysat.solvers import Solver
    out = set()
    with Solver(name='glucose4', bootstrap_with=cl + [[l] for l in cube]) as sv:
        while sv.solve():
            m = sv.get_model()
            out.add(''.join('1' if m[p - 1] > 0 else '0' for p in proj))
            sv.add_clause([(-p if m[p - 1] > 0 else p) for p in proj])
    return out


def rand3(rnd, n, m):
    return [[v if rnd.random() < 0.5 else -v for v in rnd.sample(range(1, n + 1), 3)] for _ in range(m)]


def main():
    compile_()
    mode = sys.argv[1]; K = int(sys.argv[2]) if len(sys.argv) > 2 else None
    rnd = random.Random(7); stem = os.path.join(TMP, mode)
    bad = 0; t0 = time.time()
    if mode == 'small':
        K = K or 400; nsol = 0; unsat = 0
        for k in range(K):
            n = rnd.randint(6, 16); m = rnd.randint(n, int(3.5 * n))
            cl = [[v if rnd.random() < 0.5 else -v for v in rnd.sample(range(1, n + 1), rnd.randint(1, 4) if rnd.random() < 0.3 else 3)] for _ in range(m)]
            proj = rnd.sample(range(1, n + 1), rnd.randint(1, n))
            cube = [v if rnd.random() < 0.5 else -v for v in rnd.sample(range(1, n + 1), rnd.randint(0, 3))]
            write(stem, n, cl, proj, cube)
            if os.path.exists(stem + '.sols'):
                os.remove(stem + '.sols')
            rc, got, last = run(stem, cube=True)
            want = brute(n, cl, proj, cube)
            ok = rc == 0 and last.startswith('DONE') and set(got) == want and len(got) == len(want)
            nsol += len(want); unsat += not want
            if not ok:
                bad += 1; print('  MISMATCH', k, n, m, len(got), len(want), last)
        print(f'small: {K} random CNFs ({unsat} with no solution, {nsol} projected solutions in all): {K - bad} agree with brute force, {bad} differ; {time.time() - t0:.0f} s')
    elif mode in ('medium', 'resume'):
        K = K or (40 if mode == 'medium' else 12); nsol = 0; conf = 0; stops = 0; splits = 0
        for k in range(K):
            if mode == 'medium':
                n = rnd.randint(60, 140); m = int(n * rnd.uniform(3.9, 4.3))
            else:
                n = rnd.randint(150, 190); m = int(n * rnd.uniform(4.0, 4.2))     # hard enough to be stopped
            cl = rand3(rnd, n, m); proj = rnd.sample(range(1, n + 1), rnd.randint(8, 12))
            want = pysat_enum(n, cl, proj)
            write(stem, n, cl, proj)
            if os.path.exists(stem + '.sols'):
                os.remove(stem + '.sols')
            if mode == 'medium':
                rc, got, last = run(stem)
                ok = rc == 0 and last.startswith('DONE') and set(got) == want and len(got) == len(want)
            else:
                # (1) stop and resume from the file until DONE
                secs = 0.02; before = -1
                while True:
                    rc, got, last = run(stem, secs=secs)
                    if rc == 0:
                        break
                    assert rc == 3, rc
                    stops += 1
                    if len(got) == before:
                        secs *= 2            # no new solution in this slice: a longer one (a slice must fit the last proof)
                    before = len(got)
                ok = last.startswith('DONE') and set(got) == want and len(got) == len(want)
                # (2) pool7's split: a parent stopped early, its S lines copied into four children on two more
                #     projection variables
                os.remove(stem + '.sols')
                rc, parent, last = run(stem, secs=0.01)
                union = set(parent)
                if rc == 3:
                    splits += 1
                    for bits in itertools.product((0, 1), repeat=2):
                        cs = stem + f'.child{bits[0]}{bits[1]}'
                        open(cs, 'w').write(''.join(f'S {s}\n' for s in parent))
                        open(stem + '.cube', 'w').write(' '.join(str(p if b else -p) for p, b in zip(proj[:2], bits)) + '\n')
                        rc2, got2, last2 = run(stem, cube=True, sols=cs)
                        ok &= rc2 == 0 and last2.startswith('DONE')
                        union |= set(got2)
                ok &= union == want
            nsol += len(want)
            if not ok:
                bad += 1; print('  MISMATCH', k, n, m, len(got), len(want), last)
        print(f'{mode}: {K} random 3-CNFs of {"60..140" if mode == "medium" else "150..190"} variables ({nsol} projected solutions in all{", " + str(stops) + " stops and resumes, " + str(splits) + " instances split as pool7 splits" if mode == "resume" else ""}): '
              f'{K - bad} agree with pysat glucose4, {bad} differ; {time.time() - t0:.0f} s')
    elif mode == 'hard':
        # harder instances: thousands of conflicts each, so that restarts and learnt-clause deletion are exercised
        K = K or 10; nsol = 0; confl = []
        for k in range(K):
            n = rnd.randint(170, 210); m = int(n * rnd.uniform(4.15, 4.3))
            cl = rand3(rnd, n, m); proj = rnd.sample(range(1, n + 1), 6)
            want = pysat_enum(n, cl, proj)
            write(stem, n, cl, proj)
            if os.path.exists(stem + '.sols'):
                os.remove(stem + '.sols')
            a = [EXE, stem + '.cnf', stem + '.proj', stem + '.sols', '1e9']
            p = subprocess.run(a, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            lines = [l for l in open(stem + '.sols').read().split('\n') if l]
            got = [l[2:] for l in lines if l.startswith('S ')]
            cf = [int(x.split(',')[-1].split()[0]) for x in p.stdout.split('\n') if x.startswith('DONE:') and 'conflicts' in x]
            confl += cf
            ok = p.returncode == 0 and lines[-1].startswith('DONE') and set(got) == want and len(got) == len(want)
            nsol += len(want)
            if not ok:
                bad += 1; print('  MISMATCH', k, n, m, len(got), len(want))
        print(f'hard: {K} random 3-CNFs of 170..210 variables ({nsol} projected solutions in all; cdcl7 conflicts per instance {min(confl)}..{max(confl)}; '
              f'its clause deletion starts at 4,000): {K - bad} agree with pysat glucose4, {bad} differ; {time.time() - t0:.0f} s')
    elif mode == 'ends':
        import enum7
        C = int(sys.argv[2]); frame = sys.argv[3] if len(sys.argv) > 3 else 'fb'
        cells, X, f, P = enum7.build(frame, C)
        stem = os.path.join(TMP, f'{frame}{C}')
        write(stem, f.n, f.cl, X[0])
        if os.path.exists(stem + '.sols'):
            os.remove(stem + '.sols')
        rc, got, last = run(stem)
        mine = {tuple(cells[i] for i in range(len(cells)) if b[i] == '1') for b in got}
        ref = {tuple(map(tuple, e)) for e in json.load(open(os.path.join(O.SCR, f'{frame}_{C}.json')))['list']}
        print(f'ends {frame} C={C}: cdcl7 {last}, {len(mine)} solutions; enum7 (CaDiCaL) {len(ref)}; equal as sets: {mine == ref}; {time.time() - t0:.0f} s')
        bad = mine != ref
    print('PASS' if not bad else 'FAIL')


if __name__ == '__main__':
    main()
