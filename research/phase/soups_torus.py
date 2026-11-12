"""Density time series of whole-torus soups at many initial densities (engine, --every 1).
usage: python3 soups_torus.py N GENS RUNS_PER_P OUTDIR
Writes OUTDIR/ts_p{p}_r{rng}.csv (gen,pop,changed) and prints a JSON line per run."""
import subprocess, sys, os, json, csv
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../engine/target/release/gump')
N, gens, runs, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
os.makedirs(out, exist_ok=True)
ncell = 3 * N ** 3
ps = [round(0.02 + 0.04 * i, 2) for i in range(25)]
for p in ps:
    for r in range(runs):
        f = os.path.join(out, f'ts_p{p}_r{r}.csv')
        res = subprocess.run([G, 'run', '--soup', str(p), '--torus', str(N), '--rng', str(100 + r),
                              '--gens', str(gens), '--every', '1', '--lite', '--format', 'csv', '--out', f],
                             check=True, capture_output=True, text=True)
        summ = json.loads(res.stdout.strip().splitlines()[-1])
        rows = list(csv.DictReader(open(f)))
        rho = [int(x['pop']) / ncell for x in rows]
        print(json.dumps({'p0': p, 'rng': 100 + r, 'status': summ['status'], 'gen': summ['gen'],
                          'rho1': rho[1] if len(rho) > 1 else None,
                          'rho_end': int(summ['pop']) / ncell}), flush=True)
