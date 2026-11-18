#!/usr/bin/env python3
"""Differential test: the Lean stepper against reference/oracle.py, state for state.

    python3 research/blast/lean/difftest.py GUMPCHECK OUTDIR [--quick]

GUMPCHECK is the `gumpcheck` executable (`lake build gumpcheck`); it reads a file of successive generations
written here from the oracle and checks that `stepFin` of each generation equals the next, as a set. By
`Gump.stepFin_config` (Gump/FiniteCorrect.lean) `stepFin` is `Gump.step`, so every comparison below compares
`Gump.step` itself with `oracle.step`.

Tests (all coordinates are shifted by an even vector so that they straddle zero; Lean sees negative integers):
  local    every neighbourhood: for each orientation a and each of the 2^13 states of a cell of axis a and its
           twelve neighbours (Basic.lean's `offsets a`, read from the source), one copy, spaced 6 apart so
           that no copy reaches another's centre. 3 x 8192 centres, one generation. This covers every input
           of the rule at the centres, so every neighbour count 0..12 for live and dead cells of each axis.
  soups    random boxes: cubes, slabs and rods of many sizes, densities 0.05..1.0, several seeds each, run
           until a state repeats or 60 generations.
  controls the same comparison with the oracle's rule mutated (a wrong offset, a wrong birth or survival
           number, a wrong parity test): each must be caught, i.e. produce at least one mismatch.

Coverage is counted independently of both steppers: for every compared transition, the triple (axis, alive,
count) of every cell of the oracle's array (the set comparison checks every one of them), counted with
Basic.lean's offsets. It is reported for the local test and for the soups separately.

Exit status 0 iff the baseline has no mismatch, the coverage has all 78 triples, and every control is caught.
Bulk files go to OUTDIR (use research/scratch/blast/lean/, which git ignores).
"""
import os, re, sys, subprocess, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle  # noqa: E402


def lean_offsets():
    """`Gump.offsets` as written in Gump/Basic.lean, parsed from the source."""
    src = open(os.path.join(HERE, 'Gump', 'Basic.lean'), encoding='utf-8').read()
    block = src[src.index('def offsets'):src.index('/-- The twelve neighbours of a cell')]
    parts = re.split(r'\|\s*\.(X|Y|Z)\s*=>', block)
    res = {}
    for name, text in zip(parts[1::2], parts[2::2]):
        res['XYZ'.index(name)] = [tuple(map(int, t)) for t in
                                  re.findall(r'⟨\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\s*⟩', text)]
    return res


LEAN = lean_offsets()
assert sorted(LEAN) == [0, 1, 2] and all(len(LEAN[a]) == 12 and len(set(LEAN[a])) == 12 for a in range(3))
assert all(sorted(LEAN[a]) == sorted(oracle.offsets(a)) for a in range(3)), "Basic.lean offsets != oracle offsets"


# ---------------------------------------------------------------- mutants of the oracle's rule (controls)

def coplanar_edge(a):
    """The four coplanar edge-sharing offsets +-2e_b, +-2e_c (the rule the owner meant to write in 2012)."""
    out = []
    for t in range(3):
        if t != a:
            for s in (2, -2):
                o = [0, 0, 0]; o[t] = s; out.append(tuple(o))
    return out


MUTANTS = {
    # name: (what it changes)
    'offset-one':   'a Y cell reads the coplanar edge-sharing face (2,0,0) instead of the corner face (2,0,2)',
    'offset-sign':  'a Z cell reads (1,0,-1) twice and never (1,0,1)',
    'offset-drop':  'an X cell has 11 neighbours: (0,2,2) is dropped',
    'offset-edge':  'all axes: the four corner faces replaced by the four coplanar edge-sharing faces',
    'birth-4':      'B4/S345',
    'birth-5':      'B5/S345',
    'birth-345':    'B345/S345',
    'birth-456':    'B456/S345',
    'survive-34':   'B45/S34',
    'survive-45':   'B45/S45',
    'survive-2345': 'B45/S2345',
    'survive-3456': 'B45/S3456',
    'parity-odd':   'a point is a cell of axis a when coordinate a is odd (the other two not tested)',
    'parity-swap':  'cells with x odd use the Y offsets and cells with y odd the X offsets',
    'parity-mask':  'the X mask is taken from y odd, the Y mask from x odd (cells of the wrong axis are written)',
}


def mutant_step(name):
    if name is None:
        return oracle.step                      # the ground truth, unmodified
    offs = {a: list(oracle.offsets(a)) for a in range(3)}
    birth, survive = oracle.BIRTH, oracle.SURVIVE
    maskfn = oracle.masks
    if name == 'offset-one':
        i = offs[1].index((2, 0, 2)); offs[1][i] = (2, 0, 0)
    elif name == 'offset-sign':
        i = offs[2].index((1, 0, 1)); offs[2][i] = (1, 0, -1)
    elif name == 'offset-drop':
        offs[0].remove((0, 2, 2))
    elif name == 'offset-edge':
        for a in range(3):
            offs[a] = coplanar_edge(a) + [o for o in offs[a] if o[a] != 0]
    elif name.startswith('birth-'):
        birth = tuple(int(ch) for ch in name[6:])
    elif name.startswith('survive-'):
        survive = tuple(int(ch) for ch in name[8:])
    elif name == 'parity-odd':
        maskfn = lambda H: [np.indices((H, H, H))[a] % 2 == 1 for a in range(3)]
    elif name == 'parity-swap':
        offs[0], offs[1] = offs[1], offs[0]
    elif name == 'parity-mask':
        maskfn = lambda H: (lambda m: [m[1], m[0], m[2]])(oracle.masks(H))
    else:
        raise ValueError(name)

    def step(h, m):
        m = maskfn(h.shape[0])
        new = np.zeros_like(h)
        for a in range(3):
            cnt = np.zeros(h.shape, np.int8)
            for o in offs[a]:
                cnt += np.roll(h, tuple(-d for d in o), axis=(0, 1, 2))
            born = (h == 0) & np.isin(cnt, birth)
            stay = (h == 1) & np.isin(cnt, survive)
            new[m[a] & (born | stay)] = 1
        return new
    return step


# ---------------------------------------------------------------- coverage, counted with Lean's offsets

def lean_counts(h):
    return [sum(np.roll(h, tuple(-d for d in o), axis=(0, 1, 2)) for o in LEAN[a]) for a in range(3)]


def add_coverage(cov, h, m):
    cnts = lean_counts(h.astype(np.int16))
    for a in range(3):
        c = cnts[a]
        relevant = m[a]                        # every cell of the array: the set comparison checks them all
        for alive in (0, 1):
            sel = relevant & (h == alive)
            cov[a, alive] += np.bincount(c[sel].ravel(), minlength=13)[:13]


# ---------------------------------------------------------------- running one test

def write_states(path, states, shift):
    with open(path, 'w') as f:
        for g, h in enumerate(states):
            pts = np.argwhere(h == 1) - shift
            f.write(f'G {g} {len(pts)}\n')
            f.write(''.join(f'{x} {y} {z}\n' for x, y, z in pts))


def lean_compare(gumpcheck, path):
    r = subprocess.run([gumpcheck, 'states', path], capture_output=True, text=True)
    out = r.stdout
    bad = sum(1 for l in out.splitlines() if l.startswith('MISMATCH'))
    m = re.search(r'(\d+) generations compared .* (\d+) mismatches', out)
    if m is None:
        raise RuntimeError(f'gumpcheck failed on {path}: {out} {r.stderr}')
    gens, mism = int(m.group(1)), int(m.group(2))
    assert mism == bad and (r.returncode == 0) == (mism == 0)
    return gens, mism


def run_test(gumpcheck, path, h0, gens, step, cov=None, stop_on_repeat=True):
    H = h0.shape[0]
    m = oracle.masks(H)
    states = [h0]
    seen = {h0.tobytes(): 0}
    h = h0
    for g in range(1, gens + 1):
        if cov is not None:
            add_coverage(cov, h, m)
        h = step(h, m)
        states.append(h)
        key = h.tobytes()
        if stop_on_repeat and key in seen:
            break
        seen[key] = g
        # the torus must never matter: keep every live cell 4 away from the array's faces
        assert not (h[:4].any() or h[-4:].any() or h[:, :4].any() or h[:, -4:].any()
                    or h[:, :, :4].any() or h[:, :, -4:].any()), f'{path}: pattern reached the array edge'
    shift = (H // 2) & ~1                      # even: parity, hence every axis, is preserved
    write_states(path, states, shift)
    return lean_compare(gumpcheck, path)


def local_seed():
    """3 x 2^13 copies of a cell and its 12 neighbours, every state of the 13 once per axis."""
    n = (30, 30, 28)
    H = 6 * max(n) + 16                        # 196
    h = np.zeros((H, H, H), np.int8)
    s = 0
    for a in range(3):
        unit = np.eye(3, dtype=int)[a]
        for mask in range(1 << 13):
            i, j, k = s // (n[1] * n[2]), (s // n[2]) % n[1], s % n[2]
            c = np.array([8 + 6 * i, 8 + 6 * j, 8 + 6 * k]) + unit
            if mask >> 12 & 1:
                h[tuple(c)] = 1
            for b, o in enumerate(LEAN[a]):
                if mask >> b & 1:
                    h[tuple(c + np.array(o))] = 1
            s += 1
    return h


def soup_seed(H, hx, hy, hz, dens, seed):
    m = oracle.masks(H)
    valid = m[0] | m[1] | m[2]
    c = H // 2
    box = np.zeros((H, H, H), bool)
    box[c - hx:c + hx + 1, c - hy:c + hy + 1, c - hz:c + hz + 1] = True
    rng = np.random.default_rng(seed)
    return ((rng.random((H, H, H)) < dens) & valid & box).astype(np.int8)


def soup_list(quick):
    shapes = [(2, 2, 2), (3, 3, 3), (4, 4, 4), (5, 5, 5), (6, 6, 6), (8, 8, 8), (10, 10, 10),
              (9, 9, 1), (12, 12, 2), (1, 10, 10), (2, 12, 3), (1, 1, 14), (2, 3, 14), (6, 1, 3)]
    dens = [0.05, 0.15, 0.3, 0.4, 0.5, 0.65, 0.8, 0.95, 1.0]
    seeds = [1, 2] if not quick else [1]
    if quick:
        shapes, dens = shapes[::3], dens[::2]
    out = []
    for (hx, hy, hz) in shapes:
        for d in dens:
            for s in seeds:
                if d == 1.0 and s > 1:
                    continue                   # a full box does not depend on the seed
                out.append((hx, hy, hz, d, 1000 * hx + 100 * hy + 10 * hz + s + int(d * 1e4)))
    return out


def soup_H(hx, hy, hz):
    return 2 * (hx + hy + hz) + 16             # the hull's L1 radius is at most hx+hy+hz (T2)


def main():
    gumpcheck, outdir = sys.argv[1], sys.argv[2]
    quick = '--quick' in sys.argv
    os.makedirs(outdir, exist_ok=True)
    t0 = time.time()
    # sanity: the mutant machinery with no mutation is the oracle
    hh = soup_seed(40, 5, 5, 5, 0.4, 7); mm = oracle.masks(40)
    gen = mutant_step('birth-45')
    assert (gen(hh, mm) == oracle.step(hh, mm)).all()

    cov = np.zeros((3, 2, 13), np.int64)
    covl = np.zeros((3, 2, 13), np.int64)
    total_gens = total_bad = 0
    print('Basic.lean offsets parsed and equal to oracle.offsets as sets, for each axis')
    # 1. every neighbourhood
    hl = local_seed()
    g, bad = run_test(gumpcheck, os.path.join(outdir, 'local.txt'), hl, 1, oracle.step, covl)
    total_gens += g; total_bad += bad
    print(f'local: 3 axes x 8192 neighbourhood states ({int(hl.sum())} live cells), {g} generation, {bad} mismatches')
    # 2. soups
    soups = soup_list(quick)
    nsoup_bad = 0; ncells = 0
    for (hx, hy, hz, d, seed) in soups:
        H = soup_H(hx, hy, hz)
        h0 = soup_seed(H, hx, hy, hz, d, seed)
        ncells += int(h0.sum())
        g, bad = run_test(gumpcheck, os.path.join(outdir, 'soup.txt'), h0, 60, oracle.step, cov)
        total_gens += g; total_bad += bad; nsoup_bad += (bad > 0)
        if bad:
            print(f'  soup {hx},{hy},{hz} density {d} seed {seed}: {bad} mismatches')
    print(f'soups: {len(soups)} seeds (boxes {len(set(s[:3] for s in soups))} shapes, densities '
          f'{sorted(set(s[3] for s in soups))}), {ncells} live cells in the seeds, {nsoup_bad} with a mismatch')
    print(f'baseline: {total_gens} generations compared state for state, {total_bad} mismatches '
          f'({time.time() - t0:.0f}s)')
    # coverage
    for label, cv in (('local test', covl), ('soups', cov)):
        miss = [(a, al, n) for a in range(3) for al in range(2) for n in range(13) if cv[a, al, n] == 0]
        print(f'coverage, {label}: cells of each (axis, state, live-neighbour count 0..12) over the compared '
              f'transitions; {78 - len(miss)}/78 triples hit')
        for a in range(3):
            for al in range(2):
                print(f'  axis {"XYZ"[a]} {"live" if al else "dead"}: ' + ' '.join(str(int(v)) for v in cv[a, al]))
        if miss:
            print(f'  missing: {miss}')
    missing = [(a, al, n) for a in range(3) for al in range(2) for n in range(13) if covl[a, al, n] == 0]
    # 3. negative controls
    ctl = soup_list(True)[::2]
    uncaught = []
    print(f'controls: each mutant of the oracle against the unmutated Lean stepper; local test, and {len(ctl)} soups')
    for name, what in MUTANTS.items():
        st = mutant_step(name)
        gl, bl = run_test(gumpcheck, os.path.join(outdir, f'ctl_local.txt'), hl, 1, st)
        caught_soups = 0; bad_gens = 0
        for (hx, hy, hz, d, seed) in ctl:
            H = soup_H(hx, hy, hz)
            try:
                g, bad = run_test(gumpcheck, os.path.join(outdir, 'ctl_soup.txt'),
                                  soup_seed(H, hx, hy, hz, d, seed), 30, st)
            except AssertionError:            # a mutant can grow past the hull and reach the array edge
                g, bad = 1, 1
            caught_soups += (bad > 0); bad_gens += bad
        ok = bl > 0 or caught_soups > 0
        if not ok:
            uncaught.append(name)
        print(f'  {name:13s} {"caught" if ok else "NOT CAUGHT"}: local {bl} mismatch, soups {caught_soups}/{len(ctl)} '
              f'({bad_gens} mismatching generations) -- {what}')
    passed = total_bad == 0 and not missing and not uncaught
    print(f'difftest: {"PASS" if passed else "FAIL"} ({time.time() - t0:.0f}s)')
    sys.exit(0 if passed else 1)


if __name__ == '__main__':
    main()
