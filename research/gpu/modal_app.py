"""Modal entry points for the GPU kernel (research/gpu/kernel.cuh).

  modal run research/gpu/modal_app.py::check --gpu T4      # bit-exact checks on the GPU (engine cases + fl.c)
  modal run research/gpu/modal_app.py::bench --gpu T4      # throughput grid
  modal run research/gpu/modal_app.py::cpubench            # fl.c on a Modal CPU container, for the cost comparison

The engine cases come from `python3 research/gpu/check.py engine-cases research/scratch/gpu/engine_cases.npz`
(the engine binary is built for the local CPU, so the cases are made locally and shipped as bytes).
"""
import os, sys
import modal

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
R = '/root/repo'

image = (modal.Image.from_registry('nvidia/cuda:12.4.1-devel-ubuntu22.04', add_python='3.12')
         .pip_install('numpy==2.2.6', 'cupy-cuda12x==13.4.1')
         .add_local_file(f'{ROOT}/research/fluct/fl.py', f'{R}/research/fluct/fl.py')
         .add_local_file(f'{ROOT}/research/fluct/fl.c', f'{R}/research/fluct/fl.c')
         .add_local_dir(f'{ROOT}/research/gpu', f'{R}/research/gpu', ignore=['__pycache__', '*.npz']))
app = modal.App('gump-gpu', image=image)


def _setup():
    sys.path.insert(0, f'{R}/research/gpu')
    os.chdir(R)


@app.function(gpu='T4', timeout=1800)
def check_remote(cases: bytes) -> bool:
    _setup()
    import check
    with open('/tmp/cases.npz', 'wb') as f:
        f.write(cases)
    ok = True
    for kw in (dict(kernel='global'), dict(kernel='shared'), dict(kernel='shared', J=3, WB=2, blocks=6)):
        ok &= check.check_engine('/tmp/cases.npz', 'gpu', 1024, **kw)
        ok &= check.check_fl('gpu', 64, R=7, T=3000, **kw)
        ok &= check.check_fl('gpu', 64, R=9, T=3000, **kw)
        ok &= check.check_fl('gpu', 64, R=13, T=1000, **kw)
    print('ALL OK' if ok else 'FAILURES', flush=True)
    return ok


@app.function(gpu='T4', timeout=3600)
def bench_remote(names=None, WTs=(2048, 8192, 32768, 131072), blocks=(128,), freeze=False):
    _setup()
    import subprocess, bench
    print(subprocess.run(['nvidia-smi', '--query-gpu=name,clocks.max.sm,memory.total', '--format=csv,noheader'],
                         capture_output=True, text=True).stdout, flush=True)
    out = []
    for name in names or bench.VESSELS:
        out += bench.bench_gpu(name, WTs, blocks, freeze=freeze)
    return out


SHARED_CONFIGS = [dict(WB=wb, J=j, minb=mb, blocks='occ') for mb in (1, 2) for j in (None, 'x2') for wb in (1, 2, 4)]


@app.function(gpu='T4', timeout=3600)
def bench_shared_remote(names=None, configs=None):
    _setup()
    import subprocess, bench
    print(subprocess.run(['nvidia-smi', '--query-gpu=name,clocks.max.sm,memory.total', '--format=csv,noheader'],
                         capture_output=True, text=True).stdout, flush=True)
    out = []
    import math
    for name in names or bench.VESSELS:
        n = bench.vessel(name)[0].n
        jmin = math.ceil(n / 1024)
        cf = [dict(c, J=(2 * jmin if c['J'] == 'x2' else jmin)) for c in (configs or SHARED_CONFIGS)]
        out += bench.bench_shared(name, cf)
    return out


@app.function(cpu=2.0, timeout=1800)
def cpubench_remote():
    _setup()
    import subprocess, bench
    print(subprocess.run(['bash', '-c', 'nproc; grep -m1 "model name" /proc/cpuinfo; grep -m1 -o "avx512f" /proc/cpuinfo'],
                         capture_output=True, text=True).stdout, flush=True)
    return [bench.bench_cpu(name, W) for name in bench.VESSELS for W in (4, 16)]


@app.local_entrypoint()
def check(gpu: str = 'T4', cases: str = f'{ROOT}/research/scratch/gpu/engine_cases.npz'):
    ok = check_remote.with_options(gpu=gpu).remote(open(cases, 'rb').read())
    print('remote checks:', 'ALL OK' if ok else 'FAILURES')


@app.local_entrypoint()
def bench(gpu: str = 'T4', freeze: bool = False):
    import json
    rows = bench_remote.with_options(gpu=gpu).remote(freeze=freeze)
    os.makedirs(f'{ROOT}/research/scratch/gpu', exist_ok=True)
    with open(f'{ROOT}/research/scratch/gpu/bench_{gpu}{"_freeze" if freeze else ""}.jsonl', 'w') as f:
        for r in rows:
            f.write(json.dumps(dict(r, gpu=gpu)) + '\n')


@app.local_entrypoint()
def cpubench():
    import json
    rows = cpubench_remote.remote()
    with open(f'{ROOT}/research/scratch/gpu/bench_modal_cpu.jsonl', 'w') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')


@app.local_entrypoint()
def bench_shared(gpu: str = 'T4', quick: bool = False):
    import json
    cf = [dict(WB=wb, J='x2', minb=1, blocks='occ') for wb in (1, 2, 4)] if quick else None
    rows = bench_shared_remote.with_options(gpu=gpu).remote(configs=cf)
    with open(f'{ROOT}/research/scratch/gpu/bench_shared_{gpu}.jsonl', 'w') as f:
        for r in rows:
            f.write(json.dumps(dict(r, gpu=gpu)) + '\n')


@app.function(gpu='A10G', timeout=6 * 3600)
def facelaw_remote(R: int, minutes: float, seed: int):
    _setup()
    import facelaw
    return facelaw.run(R, minutes * 60, seed, log=lambda x: print(x, flush=True))


@app.local_entrypoint()
def facelaw(r: int, minutes: float = 10, seed: int = 1, gpu: str = 'A10G', copies: int = 1):
    """`copies` containers in parallel (seeds seed..seed+copies-1); compact results to research/data/gpu_facelaw/."""
    import json
    d = f'{ROOT}/research/data/gpu_facelaw'
    os.makedirs(d, exist_ok=True)
    f = facelaw_remote.with_options(gpu=gpu)
    for out in f.starmap([(r, minutes, seed + i) for i in range(copies)]):
        path = f'{d}/R{r}_s{out["seed"]}_{gpu}.json'
        with open(path, 'w') as fh:
            json.dump(dict(out, gpu=gpu), fh)
        print('saved', path, 'gens', out['gens'], 'replicas', out['replicas'], 'wall', round(out['wall_s']))
