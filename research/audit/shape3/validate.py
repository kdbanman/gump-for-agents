#!/usr/bin/env python3
"""Bit-exact validation of st.c against the Rust engine: the slab state of lane 0 (all other 511 lanes run their own
soups alongside, through the same vector loop) is lifted to the cubic N-torus (N Z^2 in the lattice, N >= 11 so that
>= 3 dead {111} layers separate the slab copies, which stay dead by T3) and compared, as a SET OF CELLS, with the
engine's --trace at every generation 0..GENS.

    python3 research/audit/shape3/validate.py a k b GENS N [SEED]
"""
import os, random, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import geom  # noqa: E402
OUT = os.path.join(ROOT, 'research', 'scratch', 'audit_shape3')
BIN = os.path.join(OUT, 'st')
ENGINE = os.path.join(ROOT, 'engine', 'target', 'release', 'gump')
os.makedirs(OUT, exist_ok=True)


def build():
    src = os.path.join(HERE, 'st.c')
    if not os.path.exists(BIN) or os.path.getmtime(BIN) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-o', BIN + '.new', src])
        os.replace(BIN + '.new', BIN)


def geomfile(L):
    path = os.path.join(OUT, f'g_{L[0]}_{L[1]}_{L[2]}.bin')
    if not os.path.exists(path):
        geom.write(L, path)
    return path


def in_lat(x, y, L):
    a, k, b = L
    return x % a == 0 and (y - (x // a) * k) % b == 0


def lift(cells, live, L, N):
    reps = [(x, y) for x in range(N) for y in range(N) if in_lat(x, y, L)]
    assert len(reps) * L[0] * L[2] == N * N
    pts = set()
    for i in live:
        X, Y, Z = cells[i]
        for x, y in reps:
            pts.add(((X + 2 * x) % (2 * N), (Y + 2 * y) % (2 * N), (Z - 2 * x - 2 * y) % (2 * N)))
    assert len(pts) == len(reps) * len(live)
    return pts


def validate(L, gens, N, seed=5):
    build()
    cells, *_ = geom.build(L)
    path = geomfile(L)
    rng = random.Random(seed)
    live = [i for i in range(len(cells)) if rng.random() < 0.4]
    tag = f'{L[0]}_{L[1]}_{L[2]}_{os.getpid()}'
    ini = os.path.join(OUT, f'vinit_{tag}.txt'); open(ini, 'w').write('\n'.join(map(str, live)))
    out = subprocess.run([BIN, path, str(seed), str(gens + 1), os.devnull, '-i', ini, '-t', 'all'],
                         capture_output=True, text=True, check=True).stdout
    mine = {}
    for line in out.splitlines():
        if line.startswith('T'):
            f = line.split(); mine[int(f[1])] = [int(x) for x in f[2:]]
    cf = os.path.join(OUT, f'vcells_{tag}.txt')
    open(cf, 'w').write('\n'.join(' '.join(map(str, q)) for q in lift(cells, live, L, N)))
    tr = os.path.join(OUT, f'vtrace_{tag}.txt')
    subprocess.run([ENGINE, 'run', '--cells', cf, '--torus', str(N), '--gens', str(gens), '--no-halt', '--trace', tr],
                   check=True, capture_output=True)
    ok = bad = 0; first_bad = None
    with open(tr) as f:
        for line in f:
            parts = line.split()
            gg = int(parts[0])
            if gg not in mine:
                continue
            eng = {tuple(int(v) % (2 * N) for v in c.split(',')) for c in parts[1:]}
            if eng == lift(cells, mine[gg], L, N):
                ok += 1
            else:
                bad += 1; first_bad = gg if first_bad is None else first_bad
    for x in (ini, cf, tr):
        os.remove(x)
    pops = [len(mine[g]) for g in sorted(mine)]
    print(f'validate {L} N={N}: generations compared {ok + bad} (of {gens + 1}), identical states {ok}, first mismatch '
          f'{first_bad}; lane-0 population {pops[0]} -> {pops[-1]}, distinct populations {len(set(pops))}', flush=True)
    return bad == 0 and ok == gens + 1


if __name__ == '__main__':
    a = list(map(int, sys.argv[1:]))
    sys.exit(0 if validate(tuple(a[:3]), a[3], a[4], *(a[5:6] or [5])) else 1)
