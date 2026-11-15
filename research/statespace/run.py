#!/usr/bin/env python3
"""Driver: validate enum.c against the oracle on a vessel, enumerate its 2^N states, record a summary row.

  run.py one KIND ARGS... [--family F]   validate, enumerate (--counts when N <= 28), analyse the champion,
                                         append a row to data/vessels.jsonl, write data/champions/NAME.txt
  run.py list FAMILY                     print the vessel specs of a family (see FAMILIES below)

Bulk output (the enumerator's full report) goes to research/scratch/ss/NAME.out.
"""
import json, os, subprocess, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vessels as V

ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SCR = os.path.join(ROOT, 'research', 'scratch', 'ss')
ENUM = os.path.join(ROOT, 'research', 'scratch', 'ss_enum')
DATA = os.path.join(HERE, 'data')
NA = {'hull': 8, 'slab': 4, 'torus': 6}


def parse(txt):
    d = {}
    for line in txt.split('\n'):
        if ' = ' not in line:
            continue
        k, v = line.split(' = ', 1)
        d[k.strip()] = v.strip()
    r = {'N': int(d['cells']), 'goe': int(d['goe']), 'cycles': int(d['cycles']),
         'cyclic_states': int(d['cyclic_states']),
         'image_t': [int(x) for x in d['image_t'].split()],
         'image_stable_from_t': int(d['image_stable_from_t']),
         'transient_hist': [int(x) for x in d['transient_hist'].split()],
         'visited_hist': [int(x) for x in d['visited_hist(from 1)'].split()],
         'by_period': [[int(y) for y in x.split(':')] for x in d['by_period(period:cycles:states:basin)'].split()],
         'empty_basin': int(d['empty_basin']),
         'top_basins': [[int(x.split(':')[0]), int(x.split(':')[1]), x.split(':')[2]] for x in d['top_basins(size:period:rep)'].split()],
         'n_champions': int(d['n_champions'])}
    key = [k for k in d if k.startswith('champions(')][0]
    r['max_transient'] = int(key.split()[1].rstrip(')'))
    r['champions'] = d[key].split()
    r['champion_cycle_period'] = int(d['champion_cycle_period'])
    if 'entropy_t(bits; all | unsettled; unsettled_seeds)' in d:
        ent = []
        for x in d['entropy_t(bits; all | unsettled; unsettled_seeds)'].split():
            t, rest = x.split(':'); a, b = rest.split('|'); b, L = b.split(';')
            ent.append([int(t), float(a), float(b), int(float(L))])
        r['entropy_t'] = ent
    return r


def stats(r):
    S = 1 << r['N']
    th = np.array(r['transient_hist'], float); vh = np.array(r['visited_hist'], float)
    tt = np.arange(len(th)); vv = np.arange(1, len(vh) + 1)
    def med(h, x):
        c = np.cumsum(h); return int(x[np.searchsorted(c, S / 2)])
    r['mean_transient'] = float((th * tt).sum() / S)
    r['median_transient'] = med(th, tt)
    r['mean_visited'] = float((vh * vv).sum() / S)
    r['median_visited'] = med(vh, vv)
    r['mean_log2_visited'] = float((vh * np.log2(vv)).sum() / S)
    r['max_visited'] = int(vv[np.nonzero(vh)[0][-1]])
    r['largest_basin'] = r['top_basins'][0][0]
    return r


def champion_analysis(v, r):
    syms = v.symmetries()
    ch = [int(x, 16) for x in r['champions']]
    out = []
    for s in ch[:64]:
        bits = [(s >> i) & 1 for i in range(v.n)]
        stab = sum(1 for sg in syms if all(bits[sg[i]] == bits[i] for i in range(v.n)))
        out.append(stab)
    # orbits among the listed champions (complete only when all champions are listed)
    seen, orbits = set(), 0
    for s in ch:
        if s in seen:
            continue
        orbits += 1
        bits = [(s >> i) & 1 for i in range(v.n)]
        for sg in syms:
            t = 0
            for i in range(v.n):
                if bits[i]:
                    t |= 1 << sg[i]
            seen.add(t)
    return {'sym_order': len(syms), 'champion_stabilisers': out[:16],
            'champion_orbits': orbits if r['n_champions'] <= 256 else None}


def trajectory(fn, s, T):
    out = subprocess.run([ENUM, fn, '--iterate', str(T)], input='%x\n' % s, capture_output=True, text=True,
                         check=True).stdout.split()
    return [int(x, 16) for x in out]


def write_champion(v, r, fn):
    s = int(r['champions'][0], 16)
    T = r['max_transient'] + r['champion_cycle_period']
    traj = trajectory(fn, s, T)
    pops = [bin(x).count('1') for x in traj]
    os.makedirs(os.path.join(DATA, 'champions'), exist_ok=True)
    path = os.path.join(DATA, 'champions', v.name() + '.txt')
    with open(path, 'w') as f:
        f.write(f'# champion of vessel {v.kind} {" ".join(map(str, v.args))} ({v.n} cells): the seed with the longest\n')
        f.write(f'# transient, {r["max_transient"]} generations, then a cycle of period {r["champion_cycle_period"]};\n')
        f.write(f'# {r["n_champions"]} seeds share this transient. State (bit i = vessel cell i): {s:x}\n')
        f.write(f'# population along the trajectory: {" ".join(map(str, pops))}\n')
        f.write(f'# verify on reference/oracle.py: python3 research/statespace/champion.py {os.path.relpath(path, ROOT)}\n')
        f.write(f'vessel {v.kind} {" ".join(map(str, v.args))}\n')
        f.write(f'transient {r["max_transient"]}\nperiod {r["champion_cycle_period"]}\n')
        for i in range(v.n):
            if s >> i & 1:
                f.write('%d %d %d\n' % v.cells[i])
    return path, pops


def one(kind, args, family):
    v = V.make(kind, args)
    os.makedirs(SCR, exist_ok=True)
    fn = os.path.join(SCR, v.name() + '.nb'); v.write(fn)
    t0 = time.time()
    val = subprocess.run([sys.executable, os.path.join(HERE, 'validate.py'), ENUM, kind] + [str(a) for a in args]
                         + ['--states', '40', '--gens', '40'], capture_output=True, text=True)
    if not val.stdout.startswith('OK'):
        print('VALIDATION FAILED', v.name(), val.stdout, val.stderr); sys.exit(1)
    cmd = [ENUM, fn] + (['--counts'] if v.n <= 28 else [])
    txt = subprocess.run(['nice', '-n', '10'] + cmd, capture_output=True, text=True, check=True).stdout
    open(os.path.join(SCR, v.name() + '.out'), 'w').write(txt)
    r = stats(parse(txt))
    # validate the champions too, over their whole transient and one period
    ex = ','.join(r['champions'][:8])
    val2 = subprocess.run([sys.executable, os.path.join(HERE, 'validate.py'), ENUM, kind] + [str(a) for a in args]
                          + ['--states', '0', '--gens', str(r['max_transient'] + r['champion_cycle_period']), '--extra', ex],
                          capture_output=True, text=True)
    if not val2.stdout.startswith('OK'):
        print('CHAMPION VALIDATION FAILED', v.name(), val2.stdout, val2.stderr); sys.exit(1)
    r.update(champion_analysis(v, r))
    path, pops = write_champion(v, r, fn)
    deg = v.degree_profile()
    r.update({'name': v.name(), 'kind': kind, 'args': list(v.args), 'family': family, 'multi': v.multi(),
              'cells_deg_ge4': int((deg >= 4).sum()), 'cells_deg_ge3': int((deg >= 3).sum()),
              'champion_pops': pops, 'validated': val.stdout.strip() + ' | champions: ' + val2.stdout.strip(),
              'seconds': round(time.time() - t0, 1)})
    r['champions'] = r['champions'][:16]
    with open(os.path.join(DATA, 'vessels.jsonl'), 'a') as f:
        f.write(json.dumps(r) + '\n')
    print(f"{v.name():32s} N={v.n:2d} goe={r['goe'] / 2 ** v.n:.4f} cyc={r['cyclic_states']} ncyc={r['cycles']} "
          f"maxT={r['max_transient']} meanT={r['mean_transient']:.2f} medT={r['median_transient']} "
          f"empty={r['empty_basin'] / 2 ** v.n:.3f} big={r['largest_basin'] / 2 ** v.n:.3f} sym={r['sym_order']} "
          f"stab={r['champion_stabilisers'][:4]} {r['seconds']}s", flush=True)


def best_slab(k, m):
    """lattice (p,q,r) of index k with the largest shortest in-plane loop (then the largest second loop)"""
    best = None
    for p in range(1, k + 1):
        if k % p: continue
        rr = k // p
        for q in range(p):
            rows = [(p, 0, -p), (q, rr, -q - rr)]
            l1 = V.shortest2(rows)
            # second successive minimum
            vecs = []
            for a in range(-4, 5):
                for b in range(-4, 5):
                    if a or b:
                        w = a * np.array(rows[0]) + b * np.array(rows[1]); vecs.append((int(w @ w), tuple(w)))
            vecs.sort()
            l2 = next(l for l, w in vecs if np.linalg.matrix_rank(np.array([vecs[0][1], w])) == 2)
            key = (l1, l2, -p)
            if best is None or key > best[0]:
                best = (key, (p, q, rr, m))
    return best[1]


def best_torus(k):
    best = None
    for L in V.hnf_lattices(k):
        a, b, c, d, e, f = L
        rows = [(a, 0, 0), (b, c, 0), (d, e, f)]
        l1 = V.shortest2(rows)
        v = V.torus(*L)
        mult = sum(len(r) - len(set(r)) for r in v.nb.tolist())
        key = (l1, -mult, -a)
        if best is None or key > best[0]:
            best = (key, L)
    return best[1]


def family(F):
    if F == 'hull':
        rows = []
        for line in open(os.path.join(ROOT, 'research', 'scratch', 'ss_hulls40.txt')):
            w = line.split(); rows.append((int(w[0]), [int(x) for x in w[1:9]]))
        return [('hull', b) for n, b in sorted(rows) if n <= 27 and n >= 2]
    if F == 'slab3all':
        return [('slab', [p, q, k // p, 3]) for k in (1, 2, 3) for p in range(1, k + 1) if k % p == 0 for q in range(p)]
    if F.startswith('slab'):
        m = int(F[4:]); kmax = 30 // (3 * m)
        return [('slab', list(best_slab(k, m))) for k in range(1, kmax + 1)]
    if F == 'torus':
        return [('torus', list(best_torus(k))) for k in range(1, 11)]
    raise ValueError(F)


if __name__ == '__main__':
    if sys.argv[1] == 'list':
        for kind, a in family(sys.argv[2]):
            print(kind, *a)
    elif sys.argv[1] == 'one':
        kind = sys.argv[2]; args = [int(x) for x in sys.argv[3:3 + NA[kind]]]
        fam = sys.argv[sys.argv.index('--family') + 1] if '--family' in sys.argv else kind
        one(kind, args, fam)
