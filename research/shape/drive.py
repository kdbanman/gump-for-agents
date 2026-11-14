#!/usr/bin/env python3
"""Run tslab.py lives on up to three cores until each torus has its target number of face deaths.

    nohup python3 research/shape/drive.py TARGET a,k,b a,k,b ... > research/scratch/shape/drive.log 2>&1 &

Each job: `taskset -c CORE tslab.py run a k b 500000 SEED 16` (1,024 lives, cap 5e5). Seeds are $SEEDBASE + 1000*index + n,
unique per torus (tslab.load asserts it). Restartable: existing files count, new seeds skip used ones.
Stops when every torus has TARGET face deaths (first-event face deaths, tslab.stats) or after --hours.
"""
import glob, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tslab  # noqa: E402

CAP, W, CORES = 500000, 16, [0, 1, 2]
BASE = int(os.environ.get('SEEDBASE', '0'))   # A = 72 used 0; A = 60 used 100000


def deaths(t):
    if not glob.glob(os.path.join(tslab.OUT, f'ch_{t[0]}_{t[1]}_{t[2]}_s*.npz')):
        return 0
    return tslab.stats(*t)['F']


def main():
    target = int(sys.argv[1]); hours = 1.9
    tori = [tuple(map(int, s.split(','))) for s in sys.argv[2:]]
    t0 = time.time()
    used = {t: {int(f.rsplit('_s', 1)[1][:-4]) for f in glob.glob(os.path.join(tslab.OUT, f'ch_{t[0]}_{t[1]}_{t[2]}_s*.npz'))}
            for t in tori}
    pending = {t: 0 for t in tori}          # jobs in flight per torus
    done_F = {t: deaths(t) for t in tori}
    running = {}                             # core -> (proc, torus)
    while True:
        for c, (p, t) in list(running.items()):
            if p.poll() is not None:
                del running[c]; pending[t] -= 1; done_F[t] = deaths(t)
                print(f'{time.time() - t0:7.0f}s {t}: {done_F[t]} face deaths', flush=True)
        if time.time() - t0 > hours * 3600:
            break
        for c in CORES:
            if c in running:
                continue
            # expected deaths per job ~ current rate; schedule the torus furthest from target
            need = [(done_F[t] / target + pending[t] * 0.05, t) for t in tori if done_F[t] + pending[t] * 300 < target]
            if not need:
                continue
            t = min(need)[1]
            n = 0
            while BASE + 1000 * tori.index(t) + n in used[t]:
                n += 1
            seed = BASE + 1000 * tori.index(t) + n; used[t].add(seed)
            p = subprocess.Popen(['taskset', '-c', str(c), 'python3', os.path.join(HERE, 'tslab.py'), 'run',
                                  *map(str, t), str(CAP), str(seed), str(W)], stdout=subprocess.DEVNULL)
            running[c] = (p, t); pending[t] += 1
        if not running:
            break
        time.sleep(2)
    print('done', {t: done_F[t] for t in tori}, flush=True)


if __name__ == '__main__':
    main()
