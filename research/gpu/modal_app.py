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
         .add_local_file(f'{ROOT}/research/peeling/geom.py', f'{R}/research/peeling/geom.py')
         .add_local_dir(f'{ROOT}/research/gpu', f'{R}/research/gpu', ignore=['__pycache__', '*.npz']))
app = modal.App('gump-gpu', image=image)


def _report(ok):
    """print the verdict and fail the `modal run` (non-zero exit) if a check failed"""
    print('remote checks:', 'ALL OK' if ok else 'FAILURES')
    if not ok:
        raise SystemExit(1)


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


@app.function(gpu='A10G', timeout=1800)
def check_defaults_remote() -> bool:
    """the production configuration (kernel B defaults) on the face-law vessels: stepping, and events with sparse
    soups whose faces die quickly"""
    _setup()
    import check
    ok = True
    for R, T in ((13, 1500), (15, 1500), (17, 1500)):
        ok &= check.check_fl('gpu', 0, R=R, T=T)
    for R, p, T in ((13, 0.2, 3000), (15, 0.2, 3000), (17, 0.2, 3000), (17, 0.15, 3000), (17, 0.25, 6000)):
        ok &= check.check_fl('gpu', 0, R=R, T=T, p=p)
    for R in (15, 17):
        ok &= check.check_reseed('gpu', R)
        ok &= check.check_reseed('gpu', R, kernel='global', WT=1024)
    print('ALL OK' if ok else 'FAILURES', flush=True)
    return ok


@app.function(gpu='A10G', timeout=3600)
def check_every_remote(cases: bytes) -> bool:
    """the lead's acceptance bar: bit-exact against the engine every generation (five cases incl. vertex-centred and
    the side-16 snapshot), for kernel B in its production shape and a non-default one, and for kernel A"""
    _setup()
    import check
    with open('/tmp/cases.npz', 'wb') as f:
        f.write(cases)
    ok = True
    for kw in (dict(kernel='shared'), dict(kernel='shared', J=3, WB=2, blocks=6), dict(kernel='global')):
        ok &= check.check_engine_every('/tmp/cases.npz', 'gpu', 1024, **kw)
    ok &= check.check_negative_controls('/tmp/cases.npz', 'gpu', 1024, kernel='shared')
    print('ALL OK' if ok else 'FAILURES', flush=True)
    return ok


@app.local_entrypoint()
def check_every(cases: str = f'{ROOT}/research/scratch/gpu/engine_cases.npz'):
    _report(check_every_remote.remote(open(cases, 'rb').read()))


@app.function(gpu='A10G', timeout=1800)
def check_periodic_remote(cases: bytes) -> bool:
    _setup()
    import check
    with open('/tmp/periodic.npz', 'wb') as f:
        f.write(cases)
    ok = check.check_periodic('/tmp/periodic.npz', pw=128)
    ok &= check.check_periodic('/tmp/periodic.npz', pw=32)
    ok &= check.check_periodic('/tmp/periodic.npz', pw=1024)
    ok &= check.check_periodic('/tmp/periodic.npz', pw=128, J=3, WB=1, blocks=12)
    return ok


@app.local_entrypoint()
def check_periodic(cases: str = f'{ROOT}/research/scratch/gpu/periodic_cases.npz'):
    _report(check_periodic_remote.remote(open(cases, 'rb').read()))


@app.function(gpu='A10G', timeout=1800)
def check_keep_remote() -> bool:
    _setup()
    import check
    ok = True
    for R, p, T in ((9, 0.35, 3000), (13, 0.2, 3000), (17, 0.2, 3000)):
        ok &= check.check_fl('gpu', 0, R=R, T=T, p=p, keep=True)
    return ok


@app.local_entrypoint()
def check_keep():
    _report(check_keep_remote.remote())


@app.function(gpu='A10G', timeout=4 * 3600)
def postpeel_remote(R: int, centre: str, states: int, seed: int, tau_b: float):
    _setup()
    import postpeel
    return postpeel.run(R, centre, states, seed, tau_b=tau_b, log=lambda x: print(x, flush=True))


@app.local_entrypoint()
def postpeel(r: int, centre: str = 'v', states: int = 9000, seed: int = 301, tau_b: float = 0.0):
    import json
    out = postpeel_remote.remote(r, centre, states, seed, tau_b or None)
    path = f'{ROOT}/research/data/gpu_facelaw/postpeel_{centre}R{r}_s{seed}.json'
    with open(path, 'w') as fh:
        json.dump(out, fh)
    print('saved', path, 'states', out['states'], 'wall', round(out['wall_s']))


@app.function(gpu='A10G', timeout=1800)
def check_slab_remote(cases: bytes) -> bool:
    """slab vessels: every generation against the engine's torus slab, and stepping + face deaths against fl.c on the
    production slab graphs (kernel B, production shape)"""
    _setup()
    import check
    with open('/tmp/slab.npz', 'wb') as f:
        f.write(cases)
    ok = check.check_slab_every('/tmp/slab.npz', 'gpu', 0)
    for N1, N2 in ((6, 6), (6, 7)):
        ok &= check.check_fl_slab('gpu', 0, N1, N2, 8, T=3000, p=0.2)
    return ok


@app.local_entrypoint()
def check_slab(cases: str = f'{ROOT}/research/scratch/gpu/slab_cases.npz'):
    _report(check_slab_remote.remote(open(cases, 'rb').read()))


@app.function(gpu='A10G', timeout=1800)
def check_reseed_remote() -> bool:
    _setup()
    import check
    ok = True
    for R in (15, 17):
        ok &= check.check_reseed('gpu', R)
        ok &= check.check_reseed('gpu', R, kernel='global', WT=1024)
    return ok


@app.local_entrypoint()
def check_defaults(reseed_only: bool = False):
    if reseed_only:
        _report(check_reseed_remote.remote())
        return
    _report(check_defaults_remote.remote())


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
    _report(ok)


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
def facelaw_remote(R: int, minutes: float, seed: int, centre: str = 'c', sym: bool = False, slab: str = '', p: float = 0.0,
                   WB: int = 0, pw: int = 128):
    _setup()
    import facelaw
    sl = tuple(int(x) for x in slab.split('x')) if slab else None
    cfg = dict(pw=pw)
    if WB:
        cfg['WB'] = WB
    return facelaw.run(R, minutes * 60, seed, p=p or (0.4 if sl else 0.35), centre=centre, sym=sym, slab=sl,
                       log=lambda x: print(x, flush=True), **cfg)


@app.local_entrypoint()
def facelaw(r: int = 0, minutes: float = 10, seed: int = 1, gpu: str = 'A10G', copies: int = 1, centre: str = 'c', sym: bool = False,
            slab: str = '', wb: int = 0, pw: int = 128):
    """slab='6x7x8' runs a rim-free slab (p = 0.4 unless given); wb, pw: columns per block, settle window."""
    """`copies` containers in parallel (seeds seed..seed+copies-1); compact results to research/data/gpu_facelaw/."""
    import json
    d = f'{ROOT}/research/data/gpu_facelaw'
    os.makedirs(d, exist_ok=True)
    f = facelaw_remote.with_options(gpu=gpu)
    for out in f.starmap([(r, minutes, seed + i, centre, sym, slab, 0.0, wb, pw) for i in range(copies)]):
        tag = f'slab{slab}' if slab else f'{"sym" + centre if sym else ""}R{r}'
        path = f'{d}/{tag}_s{out["seed"]}_{gpu}.json'
        with open(path, 'w') as fh:
            json.dump(dict(out, gpu=gpu), fh)
        print('saved', path, 'gens', out['gens'], 'replicas', out['replicas'], 'wall', round(out['wall_s']))


@app.function(gpu='A10G', timeout=4 * 3600)
def cubelike_remote(data: bytes):
    _setup()
    import io, numpy as np, cubelike
    d = np.load(io.BytesIO(data))
    states = np.unpackbits(d['states'], axis=1)[:, :int(d['n'])].astype(bool)
    return cubelike.run(states, log=lambda x: print(x, flush=True))


@app.local_entrypoint()
def cubelike(prepared: str = f'{ROOT}/research/scratch/gpu/cubelike_v40.npz'):
    """the lead's experiment c; `python3 research/gpu/cubelike.py prepare` makes the input (fl.c, local)"""
    import json, numpy as np
    raw = open(prepared, 'rb').read()
    d = np.load(prepared)
    res = cubelike_remote.remote(raw)
    out = dict(lineages=int(len(d['specs'])), nseeds=int(d['nseeds']), hist=json.loads(str(d['hist'])), burst=int(d['burst']),
               specs=d['specs'].tolist(), result={str(k): v for k, v in res.items()})
    path = f'{ROOT}/research/data/gpu_facelaw/cubelike_v40.json'
    with open(path, 'w') as fh:
        json.dump(out, fh)
    print('saved', path)


@app.function(timeout=900)
def relay_remote(call_id: str):
    """fetch a finished call's result inside Modal and return it zlib-compressed: results above a few MB otherwise come
    back through a blob host this environment does not reach (see README, Running on Modal)"""
    import base64, json, zlib
    import modal as m
    res = m.FunctionCall.from_id(call_id).get()
    sizes = {k: len(json.dumps(v)) for k, v in res.items()}
    z = base64.b64encode(zlib.compress(json.dumps(res).encode(), 9)).decode()
    return dict(sizes=sizes, z=z)
