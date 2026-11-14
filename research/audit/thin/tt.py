#!/usr/bin/env python3
"""Driver for tt.c, the review's own stepper for the thin torus (1,1),(0,b) (review of research/theory/thin/).
Graph from research/audit/shape/geom_check.my_slab (AUTOMATON.md's cube-index table); nothing from the thin line.

    python3 research/audit/thin/tt.py geom b                       # wall geometry checks
    python3 research/audit/thin/tt.py validate b GENS N            # det stepper vs the engine on the cubic N-torus
    python3 research/audit/thin/tt.py vtrace b MODE w wall GENS    # tt.c trace vs a python stepper (walls, coins)
    python3 research/audit/thin/tt.py run TAG MODE b w wall gens seed [maxprof]   # one chunk -> scratch/audit_thin/TAG/
    python3 research/audit/thin/tt.py stats TAG...                 # ln tau per face, by tag
MODE: det (m = 8 layers, faces 0 and 7) or model (rule on layers 0..w-1, coins of density 102/256 on w, w+1).
wall: number of sites whose face cells are held dead (0 = ring; 3 = segment of b - 3 sites).
"""
import glob, math, os, random, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'shape'))
import geom_check as gc  # noqa: E402

OUT = os.path.join(ROOT, 'research', 'scratch', 'audit_thin')
BIN = os.path.join(OUT, 'tt')
ENGINE = os.path.join(ROOT, 'engine', 'target', 'release', 'gump')
Q = 102
os.makedirs(OUT, exist_ok=True)


def build():
    src = os.path.join(HERE, 'tt.c')
    if not os.path.exists(BIN) or os.path.getmtime(BIN) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-DW=32', '-o', BIN + '.new', src])
        os.replace(BIN + '.new', BIN)


def site_cells(s, t, b):
    """site s = {Z_s, Y_s, X_{s+1}} of layer t, as my_slab tuples (ax, i, j, t)"""
    return [(2, 0, s % b, t), (1, 0, s % b, t), (0, 0, (s + 1) % b, t)]


def vessel(mode, b, w, wall):
    m = 8 if mode == 'det' else w + 2
    L = (1, 1, b)
    cells, idx, nb = gc.my_slab(L, m)
    faces = [0, m - 1] if mode == 'det' else [0]
    wallc = set()
    for t in faces:
        for s in range(wall):
            for c in site_cells(s, t, b):
                wallc.add(idx[c])
    face = [[idx[c] for s in range(b) for c in site_cells(s, t, b) if idx[c] not in wallc] for t in faces]
    coin = [n for n, c in enumerate(cells) if mode == 'model' and c[3] >= w]
    inter = [[n for n, c in enumerate(cells) if c[3] == t] for t in (range(1, m - 1) if mode == 'det' else range(1, w))]
    return cells, idx, nb, face, sorted(wallc), coin, inter


def write_vessel(mode, b, w, wall):
    cells, idx, nb, face, wallc, coin, inter = vessel(mode, b, w, wall)
    path = os.path.join(OUT, f'v_{mode}_{b}_{w}_{wall}.bin')
    with open(path + f'.{os.getpid()}', 'wb') as f:
        wr = lambda x: f.write(struct.pack('<i', x))
        wr(len(cells))
        for row in nb:
            for x in row:
                wr(-1 if x is None else x)
        wr(len(face))
        for l in face:
            wr(len(l)); [wr(x) for x in l]
        wr(len(wallc)); [wr(x) for x in wallc]
        wr(len(coin)); [wr(x) for x in coin]
        wr(Q if mode == 'model' else 0)
        wr(len(inter))
        for l in inter:
            wr(len(l)); [wr(x) for x in l]
        wr(1 if mode == 'det' else 0)
    os.replace(path + f'.{os.getpid()}', path)
    return path


def geom(b):
    """the wall: with G = 3 sites held dead no live face cell left of the wall is a face neighbour of one right of it;
    also print for G = 1, 2. Site contiguity: doubled coordinate along the ring axis of the cells of a site."""
    cells, idx, nb, *_ = vessel('det', b, 0, 0)
    for G in (1, 2, 3):
        dead = {idx[c] for s in range(G) for c in site_cells(s, 0, b)}
        live = [n for n, c in enumerate(cells) if c[3] == 0 and n not in dead]
        lset = set(live)
        cross = 0
        for n in live:
            for x in nb[n]:
                if x in lset:
                    # site index of each
                    pass
        # sides: sites G..b-1; "cross" = face-face neighbour pairs whose sites differ by more than b/2 around the wall
        def site_of(n):
            ax, i, j, t = cells[n]
            return j if ax in (1, 2) else (j - 1) % b
        for n in live:
            for x in nb[n]:
                if x in lset:
                    s1, s2 = site_of(n), site_of(x)
                    if abs(s1 - s2) > b // 2:
                        cross += 1
        print(f'b={b} wall G={G}: face-neighbour pairs across the wall (within the face layer) = {cross}')
    # neighbours of a face cell by layer and site shift
    for ax in range(3):
        n = idx[(ax, 0, 5, 0)] if True else 0
        sh = sorted((cells[x][3], 'XYZ'[cells[x][0]], (cells[x][2] - 5 + b // 2) % b - b // 2) for x in nb[n] if x is not None)
        print('XYZ'[ax], sh)


def step_py(state, nb, keep, n):
    new = [0] * n
    for i in range(n):
        if i not in keep:
            continue
        k = sum(state[x] for x in nb[i] if x is not None)
        new[i] = 1 if (k in (4, 5) or (state[i] and k == 3)) else 0
    return new


def validate(b, gens, N, seed=5):
    """det ring, no walls: tt.c trace of lane 0 vs the engine on the cubic N-torus (population x copies)."""
    build()
    cells, idx, nb, face, wallc, coin, inter = vessel('det', b, 0, 0)
    path = write_vessel('det', b, 0, 0)
    tr = os.path.join(OUT, f'tr_{os.getpid()}.txt')
    subprocess.run([BIN, path, str(seed), '1', '0', '/dev/null', '-t', tr, str(gens)], check=True)
    states = [l.split()[2] for l in open(tr)]
    L = (1, 1, b)
    assert gc.in_lat((N, 0), L) and gc.in_lat((0, N), L) and N >= 11
    reps = [(x, y) for x in range(N) for y in range(N) if gc.in_lat((x, y), L)]
    kc = len(reps); assert kc * b == N * N
    live = [i for i, ch in enumerate(states[0]) if ch == '1']
    pts = set()
    for i in live:
        p = gc.doubled(cells[i])
        for x, y in reps:
            pts.add(tuple((p[k] + 2 * v) % (2 * N) for k, v in enumerate((x, y, -x - y))))
    assert len(pts) == kc * len(live)
    cf = os.path.join(OUT, f'cells_{os.getpid()}.txt'); open(cf, 'w').write('\n'.join(' '.join(map(str, q)) for q in pts))
    pl = os.path.join(OUT, f'pl_{os.getpid()}.txt')
    subprocess.run([ENGINE, 'run', '--cells', cf, '--torus', str(N), '--gens', str(gens), '--no-halt', '--poplog', pl],
                   check=True, capture_output=True)
    ref = {int(l.split()[0]): int(l.split()[1]) for l in open(pl)}
    mine = [s.count('1') for s in states]
    comp = [(g, v) for g, v in enumerate(mine) if g in ref]
    bad = [g for g, v in comp if ref[g] != v * kc]
    print(f'validate b={b} N={N} x{kc}: compared {len(comp)} generations, mismatches {len(bad)} (first {bad[:1]}), '
          f'pops {mine[:3]}..{mine[-1]}, distinct {len(set(mine))}')
    for x in (tr, cf, pl):
        os.remove(x)
    return len(comp) >= gens - 1 and not bad


def vtrace(b, mode, w, wall, gens, seed=9):
    """tt.c trace (lane 0, every generation) checked cell by cell against step_py; walls dead; coin density."""
    build()
    cells, idx, nb, face, wallc, coin, inter = vessel(mode, b, w, wall)
    path = write_vessel(mode, b, w, wall)
    tr = os.path.join(OUT, f'tr_{os.getpid()}.txt')
    subprocess.run([BIN, path, str(seed), '1', '0', '/dev/null', '-t', tr, str(gens)], check=True)
    st = [[int(ch) for ch in l.split()[2]] for l in open(tr)]
    n = len(cells); cs = set(coin); keep = set(range(n)) - cs
    bad = 0; wl = 0; ncoin = 0; scoin = 0; ac = []
    for g in range(len(st) - 1):
        nx = step_py(st[g], nb, keep, n)
        for i in wallc:
            nx[i] = 0
        bad += sum(1 for i in keep if nx[i] != st[g + 1][i])
        wl += sum(st[g + 1][i] for i in wallc)
        for i in coin:
            ncoin += 1; scoin += st[g][i]
        if coin:
            ac.append(sum((st[g][i] - Q / 256) * (st[g + 1][i] - Q / 256) for i in coin) / len(coin))
    msg = f'vtrace {mode} b={b} w={w} wall={wall}: {len(st) - 1} steps, cell mismatches {bad}, live wall cells {wl}'
    if coin:
        d = scoin / ncoin; z = (d - Q / 256) / math.sqrt(Q / 256 * (1 - Q / 256) / ncoin)
        r = sum(ac) / len(ac) / (Q / 256 * (1 - Q / 256))
        msg += f', coin density {d:.4f} (z {z:+.2f}), lag-1 corr {r:+.4f} (1/sqrt n {1 / math.sqrt(ncoin):.4f})'
    pops = [sum(s[i] for i in face[0]) for s in st]
    msg += f', face0 pop {pops[:3]}..{pops[-1]}'
    print(msg)
    os.remove(tr)
    return bad == 0 and wl == 0


def run(tag, mode, b, w, wall, gens, seed, maxprof=0, T0=256):
    build()
    path = write_vessel(mode, b, w, wall)
    d = os.path.join(OUT, tag); os.makedirs(d, exist_ok=True)
    out = os.path.join(d, f's{seed}.txt')
    if os.path.exists(out):
        print(tag, seed, 'exists'); return
    args = [BIN, path, str(seed), str(gens), str(T0), out + '.tmp']
    if maxprof:
        args += ['-P', os.path.join(d, f'p{seed}.txt'), str(maxprof)]
    subprocess.run(args, check=True)
    hdr = open(out + '.tmp').readline().strip()
    open(out + '.tmp', 'a').write(f'meta mode {mode} b {b} w {w} wall {wall}\n')
    os.replace(out + '.tmp', out)
    print(tag, seed, hdr, flush=True)


def load(tag):
    files = sorted(glob.glob(os.path.join(OUT, tag, 's*.txt')))
    acc = dict(E=0.0, F=0, both=0, S=0, Wf=0, maxage=0, n=0, expo=None, deaths=None, faces=None, chunk=[])
    for fn in files:
        ls = open(fn).read().split('\n')
        h = ls[0].split(); kv = {h[i]: h[i + 1] for i in range(0, len(h) - 1, 2)}
        e = list(map(float, ls[1].split()[1:])); dd = list(map(int, ls[2].split()[1:]))
        acc['E'] += float(kv['exposure']); acc['F'] += int(kv['deaths']); acc['both'] += int(kv['both'])
        acc['S'] += int(kv['settled']); acc['Wf'] += int(kv['firewall']); acc['maxage'] = max(acc['maxage'], int(kv['maxage']))
        acc['faces'] = int(kv['faces']); acc['n'] += 1
        acc['expo'] = e if acc['expo'] is None else [x + y for x, y in zip(acc['expo'], e)]
        acc['deaths'] = dd if acc['deaths'] is None else [x + y for x, y in zip(acc['deaths'], dd)]
        acc['chunk'].append((float(kv['exposure']), int(kv['deaths'])))
    return acc


def lntau(acc):
    F = acc['F']
    return math.log(acc['faces'] * acc['E'] / F), 1 / math.sqrt(F)


def stats(tags):
    for pat in tags:
        for d in sorted(glob.glob(os.path.join(OUT, pat))):
            tag = os.path.basename(d); acc = load(tag)
            if not acc['n'] or not acc['F']:
                continue
            lt, er = lntau(acc)
            # chunk scatter chi2 of rates
            r = acc['F'] / acc['E']; chi2 = sum((f - r * e) ** 2 / (r * e) for e, f in acc['chunk'])
            # hazard by age bins with >= 1000 deaths, merged from the top
            e, dd = acc['expo'], acc['deaths']; parts = []; ce = cd = 0; lo = None
            for j in range(len(e)):
                if e[j] == 0:
                    continue
                lo = j if lo is None else lo
                ce += e[j]; cd += dd[j]
                if cd >= max(1000, acc['F'] // 4):
                    parts.append(f'[2^{lo},2^{j + 1}): {math.log(acc["faces"] * ce / cd):.3f}({1 / math.sqrt(cd):.3f})'); ce = cd = 0; lo = None
            if cd:
                parts.append(f'[2^{lo},..): {math.log(acc["faces"] * ce / cd):.3f}({1 / math.sqrt(cd):.3f})' if cd else '')
            tau = acc['faces'] * acc['E'] / acc['F']
            print(f'{tag:16s} chunks={acc["n"]:3d} deaths={acc["F"]:7d} ln tau = {lt:.4f} +- {er:.4f}  both={acc["both"]} '
                  f'settled={acc["S"]} firewall={acc["Wf"]} maxage/tau={acc["maxage"] / tau:.1f} chi2={chi2:.1f}/{acc["n"] - 1}  '
                  f'by age: ' + ' '.join(parts))


if __name__ == '__main__':
    c = sys.argv[1]; a = sys.argv[2:]
    if c == 'geom':
        geom(int(a[0]))
    elif c == 'validate':
        sys.exit(0 if validate(int(a[0]), int(a[1]), int(a[2])) else 1)
    elif c == 'vtrace':
        sys.exit(0 if vtrace(int(a[0]), a[1], int(a[2]), int(a[3]), int(a[4])) else 1)
    elif c == 'run':
        run(a[0], a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5]), int(a[6]), *(map(int, a[7:8])))
    elif c == 'stats':
        stats(a)
