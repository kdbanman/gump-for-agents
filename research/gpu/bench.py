#!/usr/bin/env python3
"""Throughput of kernel.cuh (GPU) and of fl.c (one CPU core) on the same vessel graphs.

Unit: node-updates/s = graph nodes x replicas x generations / s (a node is a cell, or an O_h orbit in a symmetric
vessel). replica-gens/s = node-updates/s / nodes is what an ensemble experiment buys.

  python3 research/gpu/bench.py cpu        # fl.c baseline on this machine (single thread)
  (GPU: research/gpu/modal_app.py bench)
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsim
from gsim import fl

VESSELS = {  # name -> (hull, centre, sym, seed radius or None)
    'asym R=15 (A=108)': (lambda: fl.octa_hull(15), 'c', False, 15),
    'asym R=19 (A=165)': (lambda: fl.octa_hull(19), 'c', False, 19),
    'O_h vertex hull 45 (1366 orbits)': (lambda: [[-45, 45]] * 4, 'v', True, None),
}


def vessel(name):
    h, c, sym, R = VESSELS[name]
    v = fl.Vessel(h(), c, sym)
    return v, (gsim.seed_mask(v, R) if R else None)


def bench_gpu(name, WTs=(2048, 8192, 32768, 131072), blocks=(128,), target_s=1.0, freeze=False):
    import cupy as cp
    v, sd = vessel(name)
    out = []
    for WT in WTs:
        for blk in blocks:
            s = gsim.Sim(v, WT, 'gpu', seedable=sd, block=blk)
            s.reseed(np.arange(s.R), seed=1, p=0.35)
            s.step(8, freeze=freeze); cp.cuda.Device().synchronize()
            K = 16
            while True:
                t = time.perf_counter(); s.step(K, freeze=freeze); cp.cuda.Device().synchronize(); dt = time.perf_counter() - t
                if dt > target_s / 4 or K > 1 << 20:
                    break
                K *= 4
            nu = v.n * s.R * K / dt
            out.append(dict(vessel=name, nodes=v.n, WT=WT, block=blk, replicas=s.R, gens=K, s=round(dt, 3),
                            node_updates_per_s=float(f'{nu:.3g}'), replica_gens_per_s=float(f'{nu / v.n:.3g}'), freeze=freeze))
            print(json.dumps(out[-1]), flush=True)
            del s
    return out


def bench_shared(name, configs, target_s=1.0):
    """configs: dicts of Sim(kernel='shared') options (WB, J, blocks); blocks may be 'occ' = SMs x blocks that fit."""
    import cupy as cp
    v, sd = vessel(name)
    dev = cp.cuda.Device()
    sms, smem_sm = dev.attributes['MultiProcessorCount'], dev.attributes['MaxSharedMemoryPerMultiprocessor']
    thr_sm = dev.attributes['MaxThreadsPerMultiProcessor']
    out = []
    for cfg in configs:
        cfg = dict(cfg)
        occ = cfg.pop('blocks', None) == 'occ'
        try:
            s = gsim.Sim(v, backend='gpu', seedable=sd, kernel='shared', **cfg)
            if occ:
                per = max(1, min(smem_sm // (s.smem + 1024), thr_sm // s.T, cfg.get('minb', 1)))
                s = gsim.Sim(v, backend='gpu', seedable=sd, kernel='shared', blocks=sms * per, **cfg)
        except Exception as e:  # noqa: BLE001
            print(json.dumps(dict(vessel=name, cfg=cfg, error=str(e)[:200])), flush=True)
            continue
        s.reseed(np.arange(s.R), seed=1, p=0.35)
        s.step(8, freeze=True); cp.cuda.Device().synchronize()
        K = 64
        while True:
            t = time.perf_counter(); s.step(K, freeze=True); cp.cuda.Device().synchronize(); dt = time.perf_counter() - t
            if dt > target_s / 4 or K > 1 << 22:
                break
            K *= 4
        nu = v.n * s.R * K / dt
        attrs = s._run.attributes
        out.append(dict(vessel=name, nodes=v.n, kernel='shared', WB=s.WB, J=s.J, T=s.T, blocks=s.blocks, smem=s.smem,
                        regs=attrs.get('num_regs'), local_bytes=attrs.get('local_size_bytes'), replicas=s.R, gens=K,
                        s=round(dt, 3), node_updates_per_s=float(f'{nu:.3g}'), replica_gens_per_s=float(f'{nu / v.n:.3g}')))
        print(json.dumps(out[-1]), flush=True)
        del s
    return out


def bench_cpu(name, W=4, target_s=2.0):
    v, sd = vessel(name)
    f = fl.Sim(v, W=W)
    rng = np.random.default_rng(1)
    bits = rng.random((f.R, v.n)) < 0.35
    if sd is not None:
        bits &= sd
    f.set_all(bits)
    K = 16
    while True:
        t = time.perf_counter(); f.run(K, record=False); dt = time.perf_counter() - t
        if dt > target_s / 4:
            break
        K *= 4
    nu = v.n * f.R * K / dt
    r = dict(vessel=name, nodes=v.n, backend='fl.c 1 thread', W=W, replicas=f.R, gens=K, s=round(dt, 3),
             node_updates_per_s=float(f'{nu:.3g}'), replica_gens_per_s=float(f'{nu / v.n:.3g}'))
    print(json.dumps(r), flush=True)
    return r


if __name__ == '__main__':
    if sys.argv[1] == 'cpu':
        for name in VESSELS:
            for W in (1, 4, 16):
                bench_cpu(name, W)
