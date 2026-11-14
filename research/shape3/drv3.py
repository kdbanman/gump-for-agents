#!/usr/bin/env python3
"""Driver for research/shape3: reuses research/audit/shape/ts.c + ts.py (the review's independent bit-sliced stepper,
renewal lives, events every K generations), output redirected to research/scratch/shape3/.

    python3 research/shape3/drv3.py validate a k b GENS N        # population vs the engine (cubic N-torus), W=8 lanes
    python3 research/shape3/drv3.py same a k b GENS SEED          # ts3 and ts.c give identical event files (all lanes)
    python3 research/shape3/drv3.py run a k b W GENS SEED [CAP]   # CAP default 10^15 = no cap
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'shape'))
import subprocess  # noqa
import ts  # noqa
ts.OUT = os.path.join(ROOT, 'research', 'scratch', 'shape3')
ts.BIN = os.path.join(ts.OUT, 'ts3')
os.makedirs(ts.OUT, exist_ok=True)
NOCAP = 10 ** 15
SRC3 = os.path.join(HERE, 'ts3.c')
TSC = os.path.join(ts.OUT, 'ts_review')


def build():
    """ts3 from research/shape3/ts3.c; ts_review from the review's unmodified research/audit/shape/ts.c."""
    for src, out in ((SRC3, ts.BIN), (os.path.join(ROOT, 'research', 'audit', 'shape', 'ts.c'), TSC)):
        if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
            subprocess.check_call(['gcc', '-O3', '-march=native', '-o', out + '.new', src])
            os.replace(out + '.new', out)


ts.build = build
_orig_run = subprocess.run


def _run_w8(cmd, *a, **k):
    """ts.validate passes W=1 (scalar path); force W=8 so that the AVX-512 kernel used in production is the one
    compared with the engine (replica 0 = lane 0; the other 511 replicas run a random soup alongside)."""
    if cmd and cmd[0] == ts.BIN and '-i' in cmd:
        cmd = list(cmd); cmd[2] = '8'
    return _orig_run(cmd, *a, **k)


def same(L, gens, seed, W=8):
    build(); _, path = ts.vessel(L)
    outs = []
    for b in (ts.BIN, TSC):
        ev = os.path.join(ts.OUT, f'same_{os.path.basename(b)}_{os.getpid()}.txt')
        subprocess.run([b, path, str(W), '0.4', str(seed), str(NOCAP), '8', str(gens), ev], check=True, capture_output=True)
        outs.append(open(ev).read()); os.remove(ev)
    ok = outs[0] == outs[1]
    print(f'same {L} W={W} gens={gens} seed={seed}: {len(outs[0].splitlines())} event lines, identical={ok}')
    return ok

if __name__ == '__main__':
    c = sys.argv[1]; args = list(map(int, sys.argv[2:]))
    L = tuple(args[:3])
    if c == 'validate':
        subprocess.run = _run_w8; ts.subprocess.run = _run_w8
        sys.exit(0 if ts.validate(L, args[3], args[4]) else 1)
    elif c == 'same':
        sys.exit(0 if same(L, args[3], args[4]) else 1)
    elif c == 'run':
        ts.run(L, args[3], args[4], args[5], *(args[6:7] or [NOCAP]))
