#!/usr/bin/env python3
"""The acceptance checks of research/gpu/README.md "Correctness", run on the local card instead of Modal.

  python research/gpu-local/acceptance.py cases            # build the engine reference cases (CPU, minutes)
  python research/gpu-local/acceptance.py all              # every group below; exits non-zero on any failure
  python research/gpu-local/acceptance.py every periodic   # chosen groups

Each group calls the same check.* functions with the same arguments as the Modal entry point named beside it in
GROUPS, so a pass here is the same statement as a pass there, on this card. Groups marked fl.c need gcc (fl.c is
built by research/fluct/fl.py, cpu.c by research/gpu/gsim.py, both with `gcc -shared`).
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'research', 'gpu'))
import check  # noqa: E402

CASES = os.path.join(ROOT, 'research', 'scratch', 'gpu')
ENGINE = os.path.join(CASES, 'engine_cases.npz')
PERIODIC = os.path.join(CASES, 'periodic_cases.npz')
SLAB = os.path.join(CASES, 'slab_cases.npz')
SLAB12 = [os.path.join(CASES, f'slab12_r{r}.npz') for r in (3, 4)]


def build_cases(force=False):
    os.makedirs(CASES, exist_ok=True)
    jobs = [(ENGINE, lambda p: check.engine_cases(p)),
            (SLAB, lambda p: check.slab_cases(p)),
            (SLAB12[0], lambda p: check.slab_cases(p, N=12, m=8, T=300, rng=3)),
            (SLAB12[1], lambda p: check.slab_cases(p, N=12, m=8, T=300, rng=4)),
            (PERIODIC, lambda p: check.periodic_cases(p))]
    for path, make in jobs:
        if force or not os.path.exists(path):
            t = time.time(); make(path); print(f'  built {os.path.basename(path)} in {time.time() - t:.0f} s', flush=True)


def g_check():          # modal_app.check_remote (the first acceptance run, T4)
    ok = True
    for kw in (dict(kernel='global'), dict(kernel='shared'), dict(kernel='shared', J=3, WB=2, blocks=6)):
        ok &= check.check_engine(ENGINE, 'gpu', 1024, **kw)
        ok &= check.check_fl('gpu', 64, R=7, T=3000, **kw)
        ok &= check.check_fl('gpu', 64, R=9, T=3000, **kw)
        ok &= check.check_fl('gpu', 64, R=13, T=1000, **kw)
    return ok


def g_every():          # modal_app.check_every_remote: the acceptance bar
    ok = True
    for kw in (dict(kernel='shared'), dict(kernel='shared', J=3, WB=2, blocks=6), dict(kernel='global')):
        ok &= check.check_engine_every(ENGINE, 'gpu', 1024, **kw)
    ok &= check.check_negative_controls(ENGINE, 'gpu', 1024, kernel='shared')
    return ok


def g_periodic():       # modal_app.check_periodic_remote
    ok = check.check_periodic(PERIODIC, pw=128)
    ok &= check.check_periodic(PERIODIC, pw=32)
    ok &= check.check_periodic(PERIODIC, pw=1024)
    ok &= check.check_periodic(PERIODIC, pw=128, J=3, WB=1, blocks=12)
    return ok


def g_defaults():       # modal_app.check_defaults_remote (fl.c)
    ok = True
    for R, T in ((13, 1500), (15, 1500), (17, 1500)):
        ok &= check.check_fl('gpu', 0, R=R, T=T)
    for R, p, T in ((13, 0.2, 3000), (15, 0.2, 3000), (17, 0.2, 3000), (17, 0.15, 3000), (17, 0.25, 6000)):
        ok &= check.check_fl('gpu', 0, R=R, T=T, p=p)
    return ok & g_reseed()


def g_reseed():         # modal_app.check_reseed_remote (fl.c)
    ok = True
    for R in (15, 17):
        ok &= check.check_reseed('gpu', R)
        ok &= check.check_reseed('gpu', R, kernel='global', WT=1024)
    return ok


def g_keep():           # modal_app.check_keep_remote (fl.c)
    ok = True
    for R, p, T in ((9, 0.35, 3000), (13, 0.2, 3000), (17, 0.2, 3000)):
        ok &= check.check_fl('gpu', 0, R=R, T=T, p=p, keep=True)
    return ok


def g_slab():           # modal_app.check_slab_remote (engine; fl.c for the second half)
    ok = check.check_slab_every(SLAB, 'gpu', 0)
    for N1, N2 in ((6, 6), (6, 7)):
        ok &= check.check_fl_slab('gpu', 0, N1, N2, 8, T=3000, p=0.2)
    return ok


def g_patches():        # modal_app.check_patches_remote
    import patches
    ok = True
    for path in SLAB12:
        ok &= check.check_slab_every(path, 'gpu', 0)
    ok &= patches.validate(log=lambda x: print(x, flush=True))
    return ok


def g_cpu():            # `check.py all cpu CASES`: the CPU build of kernel A (cpu.c) against the engine and fl.c
    WT = 4
    ok = check.check_engine(ENGINE, 'cpu', WT)
    ok &= check.check_engine_every(ENGINE, 'cpu', WT)
    ok &= check.check_negative_controls(ENGINE, 'cpu', WT)
    for R, T in ((7, 3000), (9, 3000), (13, 1000)):
        ok &= check.check_fl('cpu', WT, R=R, T=T)
    return ok


GROUPS = dict(every=g_every, periodic=g_periodic, check=g_check, defaults=g_defaults, keep=g_keep, slab=g_slab,
              patches=g_patches, cpu=g_cpu)

if __name__ == '__main__':
    args = sys.argv[1:] or ['all']
    if args[0] == 'cases':
        build_cases(force='--force' in args); sys.exit(0)
    names = list(GROUPS) if args == ['all'] else args
    verdict = {}
    for name in names:
        t = time.time()
        print(f'=== {name}', flush=True)
        try:
            verdict[name] = bool(GROUPS[name]())
        except Exception as e:                                    # a crash is a failure, reported with its cause
            import traceback; traceback.print_exc(); verdict[name] = False
        print(f'=== {name}: {"OK" if verdict[name] else "FAIL"} ({time.time() - t:.0f} s)', flush=True)
    print('summary:', ' '.join(f'{k}={"OK" if v else "FAIL"}' for k, v in verdict.items()))
    print('ALL OK' if all(verdict.values()) else 'FAILURES')
    sys.exit(0 if all(verdict.values()) else 1)
