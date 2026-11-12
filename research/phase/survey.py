"""Rule-space survey around B45/S345: all B ⊆ {4..7} (non-empty) x S ⊆ {2..7}, plus optional extra rules.
usage: python3 survey.py torus OUT.jsonl [--n 24 --gens 3000 --procs 2]
       python3 survey.py vessel OUT.jsonl [--runs 16 --radii 6,8,10 --cap 100000]
torus: whole-torus soups at p0 in {0.15,0.3,0.5,0.7} (one each, rng 1); records status, final
       gen, mean density and mean turnover (cells changed / cells) over the last third.
vessel: octahedral soups (p=0.35, L1 radius R doubled units, open space) -> lifetime =
       cycle_start (gen at which the final cycle/still/extinction is entered), capped.
"""
import sys, os, json, argparse, subprocess, itertools, csv, io
from multiprocessing import Pool
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../engine/target/release/gump')
G = os.environ.get('GUMP', G)

def subsets(xs):
    for r in range(len(xs) + 1):
        yield from itertools.combinations(xs, r)

def rules(extra=()):
    out = []
    for b in subsets([4, 5, 6, 7]):
        if not b:
            continue
        for s in subsets([2, 3, 4, 5, 6, 7]):
            out.append('B' + ''.join(map(str, b)) + '/S' + ''.join(map(str, s)))
    return out + list(extra)

def torus_job(arg):
    rule, p0, n, gens = arg
    r = subprocess.run([G, 'run', '--rule', rule, '--soup', str(p0), '--torus', str(n), '--rng', '1',
                        '--gens', str(gens), '--every', '10', '--lite', '--format', 'csv',
                        '--hash-window', '65536', '--out', '/dev/stdout'], capture_output=True, text=True, check=True)
    lines = r.stdout.strip().splitlines()
    summ = json.loads(lines[-1])
    rows = [l for l in lines[:-1] if l and not l.startswith('{')]
    rd = list(csv.DictReader(io.StringIO('\n'.join(rows))))
    N = 3 * n ** 3
    tail = rd[len(rd) * 2 // 3:]
    rho = sum(int(x['pop']) for x in tail) / max(len(tail), 1) / N
    ch = [int(x['changed']) for x in tail if x['changed']]
    turn = sum(ch) / max(len(ch), 1) / N
    return {'rule': rule, 'p0': p0, 'n': n, 'status': summ['status'], 'period': summ['period'],
            'gen': summ['gen'], 'rho_end': summ['pop'] / N, 'rho_tail': rho, 'turn_tail': turn}

def vessel_job(arg):
    rule, runs, radii, cap = arg
    r = subprocess.run([G, 'ensemble', '--rule', rule, '--soup', '0.35', '--radius', str(radii[0]), '--runs', str(runs),
                        '--threads', '1', '--gens', str(cap), '--hash-window', '65536',
                        '--vary', 'radius=' + ','.join(map(str, radii))], capture_output=True, text=True, check=True)
    out = []
    for l in r.stdout.splitlines():
        d = json.loads(l)
        if d.get('type') != 'summary':
            continue
        R = int([p['value'] for p in d['params'] if p['key'] == 'radius'][0])
        life = d['cycle_start'] if d['cycle_start'] is not None else d['gen']
        out.append({'rule': rule, 'R': R, 'rng': d['rng'], 'status': d['status'], 'period': d['period'],
                    'life': life, 'pop': d['pop'], 'seed_pop': d['seed_pop']})
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode'); ap.add_argument('out')
    ap.add_argument('--n', type=int, default=24); ap.add_argument('--gens', type=int, default=3000)
    ap.add_argument('--procs', type=int, default=2)
    ap.add_argument('--runs', type=int, default=16); ap.add_argument('--radii', default='6,8,10')
    ap.add_argument('--cap', type=int, default=100000)
    ap.add_argument('--rules', default=None, help='comma list overriding the family')
    a = ap.parse_args()
    rl = a.rules.split(',') if a.rules else rules()
    with Pool(a.procs) as pool, open(a.out, 'w') as f:
        if a.mode == 'torus':
            jobs = [(r, p, a.n, a.gens) for r in rl for p in (0.15, 0.3, 0.5, 0.7)]
            for res in pool.imap_unordered(torus_job, jobs, chunksize=4):
                f.write(json.dumps(res) + '\n'); f.flush()
        else:
            radii = [int(x) for x in a.radii.split(',')]
            jobs = [(r, a.runs, radii, a.cap) for r in rl]
            for res in pool.imap_unordered(vessel_job, jobs):
                for x in res:
                    f.write(json.dumps(x) + '\n')
                f.flush()
