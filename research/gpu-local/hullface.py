#!/usr/bin/env python3
"""The asymmetric (hull) octahedron face law on this card: a local runner around research/gpu/facelaw.py `run`
(soup 0.35 in |p|_1 <= R, exact hull, 8 faces, T0 = 200, tau_face = 8 * exposure / deaths), cycle guard on.

  python -u research/gpu-local/hullface.py tune R                 # replica-generations/s for several kernel shapes
  python -u research/gpu-local/hullface.py check                  # engine comparison every generation in the run's shape
  python -u research/gpu-local/hullface.py run R MINUTES SEED     # one run: a csv row + a json (raw lives, age bins)
  python research/gpu-local/hullface.py summary R [save]          # pooled ln tau_face, seeds, hazard by age; save: commit-size age tables

Rows: research/data/gpu_local_hull/hull_R{R}.csv. Per-run json: research/scratch/gpu-local/hull_R{R}_s{SEED}.json.
The commit (with a dirty mark) is read when the run starts, not when it ends.
"""
import csv, json, math, os, subprocess, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'research', 'gpu'))
import facelaw, gsim  # noqa: E402
from gsim import fl  # noqa: E402
DATA = os.path.join(ROOT, 'research', 'data', 'gpu_local_hull')
SCR = os.path.join(ROOT, 'research', 'scratch', 'gpu-local')
T0, GUARD = 200, 16
CFG = dict(WB=2, J=1, minb=1)     # kernel-B shape of the runs: 2 columns per block, fewest nodes-per-thread groups (gsim raises J to
                                  # ceil(n / 1024)), one block per SM. At R = 15: 3.5e8 replica-gens/s in 1,280 replicas, 2.7e5 gens/s
                                  # each (`tune 15`); 4 columns give 9% more in total at half the speed per replica (ages half as old).
FIELDS = ['R', 'A', 'seed', 'p', 'T0', 'gens', 'replicas', 'nodes', 'wall_s', 'exposure', 'deaths', 'settled12', 'settled3pw',
          'guard', 'exposure_guard', 'exposure_guard_past_snapshot', 'open', 'excluded', 'max_age', 'guard_first', 'config', 'code_commit', 'started_utc', 'cmd']


def git_head():
    """short commit, with '+dirty' when tracked code (research/gpu, research/shape, the .py here) differs from it"""
    try:
        h = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        d = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no', '--', 'research/gpu', 'research/shape', 'research/fluct', 'research/gpu-local/*.py'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return h + ('+dirty' if d else '')
    except OSError:
        return 'unknown'


def sim_cfg():
    import cupy as cp
    sms = cp.cuda.Device().attributes['MultiProcessorCount']
    return dict(WB=CFG['WB'], J=CFG['J'], minb=CFG['minb'], blocks=CFG['minb'] * sms)


def vessel(R):
    v = fl.Vessel(fl.octa_hull(R, 'c'), 'c', False)
    return v, gsim.seed_mask(v, R)


def tune(R):
    import cupy as cp
    v, sd = vessel(R)
    sms = cp.cuda.Device().attributes['MultiProcessorCount']
    print(f'R = {R}: A = {v.A}, nodes {v.n}', flush=True)
    for mb in (1, 2):
        for WB in (1, 2, 4):
            for J in (None, math.ceil(v.n / 1024)):
                try:
                    s = gsim.Sim(v, backend='gpu', seedable=sd, WB=WB, J=J, minb=mb, blocks=mb * sms)
                except AssertionError as e:
                    print(f'minb={mb} WB={WB} J={J}: does not fit {e}', flush=True)
                    continue
                s.reseed(np.arange(s.R), seed=1, p=0.35)
                s.step(64); cp.cuda.Device().synchronize()
                K = 1 << 14
                t = time.perf_counter(); s.step(K); cp.cuda.Device().synchronize(); dt = time.perf_counter() - t
                print(f'minb={mb} WB={WB} J={s.J} T={s.T} blocks={s.blocks} replicas={s.R}: {s.R * K / dt:.3g} replica-gens/s, '
                      f'{K / dt:.3g} gens/s per replica', flush=True)
                del s


def run(R, minutes, seed, **kw):
    head, started = git_head(), time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    out = facelaw.run(R, minutes * 60, seed, guard=GUARD, raw_cap=3000000, **dict(sim_cfg(), **kw))
    out['code_commit'], out['started_utc'] = head, started
    return out


def row(out):
    a = out['agg'][T0] if T0 in out['agg'] else out['agg'][str(T0)]
    g = out.get('guard') or {}
    e5 = e5s = 0
    if g.get('recognised'):                 # kind-5 lives: [replica, age at recognition, snapshot age]
        gl = facelaw.unpack(g['lives'])
        e5 = int(np.clip(gl[1] - T0, 0, None).sum())
        e5s = int((gl[1] - np.maximum(gl[2], T0)).clip(0).sum())      # the part after the snapshot: certainly in the cycle
    k3 = a['settled_long']
    return dict(R=out['R'], A=out['A'], seed=out['seed'], p=out['p'], T0=T0, gens=out['gens'], replicas=out['replicas'],
                nodes=out['nodes'], wall_s=round(out['wall_s']), exposure=a['exposure'], deaths=a['deaths'],
                settled12=a['settled'] - k3 - g.get('recognised', 0), settled3pw=k3, guard=g.get('recognised', 0),
                exposure_guard=e5, exposure_guard_past_snapshot=e5s, open=a['censored'], excluded=a['excluded'], max_age=out['max_age'],
                guard_first=g.get('first', 0), config=json.dumps(out['config']).replace(',', ';'),
                code_commit=out['code_commit'], started_utc=out['started_utc'], cmd=out.get('cmd', ''))


def summary(R, save=False):
    rows = list(csv.DictReader(open(os.path.join(DATA, f'hull_R{R}.csv'))))
    seeds = [r['seed'] for r in rows]
    if len(set(seeds)) != len(seeds):
        sys.exit(f'hull_R{R}.csv has two rows with the same seed: not pooled')
    E = sum(int(r['exposure']) for r in rows); F = sum(int(r['deaths']) for r in rows)
    print(f'hull octahedron R = {R}, A = {rows[0]["A"]}: {len(rows)} runs, exposure after T0 = {E:.5g}, face deaths {F}, '
          f'settled {sum(int(r["settled12"]) + int(r["settled3pw"]) for r in rows)}, guard {sum(int(r["guard"]) for r in rows)} '
          f'(exposure {sum(int(r["exposure_guard"]) for r in rows) / E:.2e} of the total)')
    print(f'  ln tau_face = ln(8 E / F) = {math.log(8 * E / F):.4f} +- {1 / math.sqrt(F):.4f}')
    cut = sum(int(r.get('exposure_guard_past_snapshot') or 0) for r in rows)
    print(f'  with kind-5 exposure cut at the snapshot age: {math.log(8 * (E - cut) / F):.4f}' if cut else
          '  no kind-5 exposure past a snapshot: the two exposure conventions coincide')
    chi2 = 0
    for r in rows:
        e, f = int(r['exposure']), int(r['deaths'])
        chi2 += (f - F * e / E) ** 2 / (F * e / E)
        print(f'  seed {r["seed"]}: deaths {f}, ln = {math.log(8 * e / f):.4f} +- {1 / math.sqrt(f):.4f}, '
              f'max age {int(r["max_age"]):.3g}, commit {r["code_commit"]}')
    print(f'  seeds: chi2 = {chi2:.2f} on {len(rows) - 1}')
    hs = []
    for r in rows:
        p = os.path.join(SCR, f'hull_R{R}_s{r["seed"]}.json')
        q = os.path.join(DATA, f'hist_R{R}_s{r["seed"]}.json')       # the run's age table, committed
        if os.path.exists(p):
            j = json.load(open(p)); hs.append(j['bins'])
            if save:
                keys = ('R', 'A', 'seed', 'p', 'gens', 'replicas', 'nodes', 'wall_s', 'config', 'agg', 'bins', 'max_age',
                        'guard', 'code_commit', 'started_utc', 'cmd')
                json.dump({k: j[k] for k in keys if k in j}, open(q, 'w'))
        elif os.path.exists(q):
            hs.append(json.load(open(q))['bins'])
    if hs:
        ed = np.array(hs[0]['edges'], float)
        ex = np.sum([h['exposure'] for h in hs], 0).astype(float); fd = np.sum([h['deaths'] for h in hs], 0).astype(float)
        keep = ed[:-1] >= T0
        tot = fd[keep].sum() / ex[keep].sum()
        print(f'  hazard of a face death by age, relative to the mean rate at ages >= {T0} '
              f'({len(hs)} of {len(rows)} runs have a json here):')
        i = int(np.argmax(keep))
        while i < len(ex):                       # merge bins until each has >= 400 deaths
            j, e, f = i, 0.0, 0.0
            while j < len(ex) and (f < 400 or e == 0):
                e += ex[j]; f += fd[j]; j += 1
            if e > 0:
                print(f'    age {ed[i]:>10.3g} - {ed[j]:<10.3g}: deaths {int(f):7d}, hazard / mean = {f / e / tot:.3f} '
                      f'+- {math.sqrt(max(f, 1)) / e / tot:.3f}')
            i = j


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'tune':
        tune(int(sys.argv[2]))
    elif what == 'check':
        import check
        eng = os.path.join(ROOT, 'research', 'scratch', 'gpu', 'engine_cases.npz')
        kw = sim_cfg()
        ok = check.check_engine_every(eng, 'gpu', 1024, **kw)
        ok &= not check.check_engine_every(eng, 'gpu', 1024, control='shift', Tmax=300, **kw)
        ok &= not check.check_engine_every(eng, 'gpu', 1024, control='flip', Tmax=300, **kw)
        print('CHECK OK' if ok else 'CHECK FAILED', kw)
        sys.exit(0 if ok else 1)
    elif what == 'run':
        R, minutes, seed = int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
        out = run(R, minutes, seed)
        out['cmd'] = ' '.join(['python', '-u', 'research/gpu-local/hullface.py'] + sys.argv[1:])
        os.makedirs(DATA, exist_ok=True); os.makedirs(SCR, exist_ok=True)
        json.dump(out, open(os.path.join(SCR, f'hull_R{R}_s{seed}.json'), 'w'))
        path = os.path.join(DATA, f'hull_R{R}.csv')
        new = not os.path.exists(path)
        with open(path, 'a', newline='') as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            if new:
                w.writeheader()
            w.writerow(row(out))
        print(json.dumps(row(out)))
    elif what == 'summary':
        summary(int(sys.argv[2]), save='save' in sys.argv[3:])
