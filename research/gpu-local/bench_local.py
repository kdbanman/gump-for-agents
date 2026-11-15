#!/usr/bin/env python3
"""Throughput on this card, comparable row for row with research/data/gpu_bench/bench_shared_A10G.jsonl.

  python -u research/gpu-local/bench_local.py [OUT.jsonl]   (default research/data/gpu_local_bench/bench_shared_GTX1080.jsonl)

Kernel B (shared memory): bench.bench_shared with the same 12 configurations as modal_app.SHARED_CONFIGS (WB in 1, 2,
4; J = minimum or twice the minimum; minb in 1, 2; blocks = SMs x blocks that fit), on bench.VESSELS plus the 6 x 6 x 8
slab (the A = 108 slab face). Kernel A (global memory): bench.bench on the same vessels. Configurations that do not fit
in this card's 48 KB of shared memory per block are recorded as errors (gsim's assert), which is the fit table.
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'research', 'gpu'))
import bench, gsim  # noqa: E402

bench.VESSELS['slab 6x6x8 (A=108)'] = (None, None, None, None)
_vessel = bench.vessel


def vessel(name):
    if name.startswith('slab'):
        from vessels import SlabVessel
        return SlabVessel(6, 6, 8), None
    return _vessel(name)


bench.vessel = vessel
CONFIGS = [dict(WB=wb, J=j, minb=mb, blocks='occ') for mb in (1, 2) for j in (None, 'x2') for wb in (1, 2, 4)]

if __name__ == '__main__':
    import cupy as cp
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'research', 'data', 'gpu_local_bench', 'bench_shared_GTX1080.jsonl')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    dev = cp.cuda.Device()
    card = dict(card=cp.cuda.runtime.getDeviceProperties(0)['name'].decode(), sms=dev.attributes['MultiProcessorCount'],
                smem_block_optin=dev.attributes['MaxSharedMemoryPerBlockOptin'], cuda_driver=cp.cuda.runtime.driverGetVersion(),
                cupy=cp.__version__)
    rows = []
    for name in bench.VESSELS:
        n = vessel(name)[0].n
        jmin = math.ceil(n / 1024)
        cf = [dict(c, J=(2 * jmin if c['J'] == 'x2' else jmin)) for c in CONFIGS]
        for r in bench.bench_shared(name, cf):
            rows.append(dict(r, **card))
        for r in bench.bench_gpu(name, WTs=(2048, 8192, 32768), blocks=(128,)):
            rows.append(dict(r, kernel='global', **card))
    with open(out, 'w') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')
    print(f'{len(rows)} rows -> {out}')
