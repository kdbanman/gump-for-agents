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
    ok = check.check_engine('/tmp/cases.npz', 'gpu', 1024)
    ok &= check.check_fl('gpu', 64, R=7, T=3000)
    ok &= check.check_fl('gpu', 64, R=9, T=3000)
    ok &= check.check_fl('gpu', 64, R=13, T=1000)
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
