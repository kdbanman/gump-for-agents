#!/usr/bin/env python3
"""Forward-flux sampling (FFS) of a face death, along m = min over the faces of the outer-layer population.

The dynamics is deterministic, so a trial launched from a stored configuration is diversified by flipping one
random cell (one O_h orbit in a symmetric vessel) at layer depth >= D below every face (D = -1: no perturbation;
trials from the same configuration are then identical, which is still unbiased, only less efficient).

  stage 0 (flux): basin replicas (after a transient T0) are followed; a "crossing" is m <= lam0 after having been
                  at m >= lamA since the previous one. Phi = crossings / measured replica-generations.
  stage i:        M trials, each from a random stored configuration at lam_i (+ perturbation), run until
                  m <= lam_{i+1} (success, stored) or m >= lamA (failure).   k = Phi * prod P_i  (first-peel rate)
The basin run also counts deaths (m = 0) directly, a free check where deaths are not too rare.

  python3 research/fluct/ffs.py asym R [opts]                 asymmetric octahedral soup, density 0.35
  python3 research/fluct/ffs.py sym R c|v [opts]              O_h-symmetric soup |p - c|_1 <= R
  python3 research/fluct/ffs.py snap FILE c|v [opts]          diversified copies of a symmetric snapshot
opts: --D 2 --M 2000 --N0 1000 --delta auto --reps 4 --W 1 --T0 200 --tag NAME --seed 1
Results: one JSON line per repetition appended to research/scratch/fluct/ffs_{tag}.jsonl (repetitions already
there are skipped, so a killed job resumes at the next repetition).
"""
import argparse, json, math, os, sys, time, zlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl

BIG = 1 << 30


class Basin:
    """source of basin states: soups (asym or sym) or diversified copies of a snapshot"""
    def __init__(self, v, kind, p=0.35, snap_bits=None):
        self.v, self.kind, self.p, self.snap = v, kind, p, snap_bits

    def fresh(self, rng, pool=None):
        if self.kind == 'snap':
            return self.snap.copy() if not pool else pool[rng.integers(len(pool))].copy()
        return rng.random(self.v.n) < self.p


class FFS:
    def __init__(self, v, basin, W, D, rng, T0):
        self.v, self.basin, self.D, self.rng, self.T0 = v, basin, D, rng, T0
        self.sim = fl.Sim(v, W, seed=int(rng.integers(1 << 62)))
        self.R = self.sim.R
        dep = v.node_depth()
        self.pert_nodes = np.nonzero(dep >= D)[0] if D >= 0 else None

    def perturb(self, r):
        if self.pert_nodes is not None:
            self.sim.flip(r, int(self.pert_nodes[self.rng.integers(len(self.pert_nodes))]))

    def m_now(self):
        return self.sim.m().astype(np.int64)

    def pilot(self, gens):
        """basin m statistics: R replicas, transient T0, then gens; replicas that die are refreshed"""
        sim = self.sim
        for r in range(self.R):
            sim.set(r, self.basin.fresh(self.rng)); self.perturb(r)
        ms = []
        sim.run(self.T0, record=False)
        c, _, _ = sim.run(gens, record=True)
        m = c[:, self.v.face_groups, :].min(1).astype(np.int64)
        alive = np.minimum.accumulate(m, axis=0) > 0
        return m[alive]

    def stage0(self, lam0, lamA, N0, chunk=64):
        sim, R = self.sim, self.R
        armed = np.zeros(R, bool); age = np.zeros(R, np.int64)
        for r in range(R):
            sim.set(r, self.basin.fresh(self.rng)); self.perturb(r)
        configs, anc = [], []
        expo = 0; deaths = 0; crossings = 0; pool_live = []
        t_wall = time.time()
        while crossings < N0:
            meas = age >= self.T0
            lo = np.where(~meas, -1, np.where(armed, lam0, 0))
            hi = np.where(~meas, BIG, np.where(armed, BIG, lamA))
            # transient replicas: stop at the end of their transient (cap the chunk)
            gens = int(min(chunk, max(1, (self.T0 - age[~meas]).min()) if (~meas).any() else chunk))
            sg, sm, mm = sim.run_until(gens, lo, hi)
            stepped = np.where(sg >= 0, sg, gens)
            expo += int(stepped[meas].sum()); age += stepped
            for r in np.nonzero((sg >= 0) & meas)[0]:
                if armed[r]:                       # crossed lam0
                    configs.append((np.packbits(sim.get(r)), crossings)); crossings += 1; armed[r] = False
                    if sm[r] == 0:
                        deaths += 1; self._refresh(r, age, armed, configs)
                elif sm[r] >= lamA:
                    armed[r] = True
                else:                              # m == 0 while disarmed: death
                    deaths += 1; self._refresh(r, age, armed, configs)
            # replicas whose state has m == 0 but not stopped can't exist (lo >= 0 catches it) except transient ones
            if (~meas).any():
                mnow = self.m_now()
                for r in np.nonzero(~meas & (mnow == 0))[0]:
                    self._refresh(r, age, armed, configs)
        return configs, crossings / expo, dict(expo=expo, deaths=deaths, crossings=crossings, wall=time.time() - t_wall)

    def _refresh(self, r, age, armed, configs):
        if self.basin.kind == 'snap':
            # Fleming-Viot style: copy a random other replica (alive, measured), perturb, transient again
            cand = [q for q in range(self.R) if q != r and age[q] >= self.T0]
            src = cand[self.rng.integers(len(cand))] if cand else None
            bits = self.sim.get(src) if src is not None else self.basin.fresh(self.rng)
        else:
            bits = self.basin.fresh(self.rng)
        self.sim.set(r, bits); self.perturb(r); age[r] = 0; armed[r] = False

    def stage(self, configs, lam_next, lamA, M, chunk=32, maxlen=200000):
        sim, R, n = self.sim, self.R, self.v.n
        launched = done = succ = 0; out = []; lens = []
        slot = np.full(R, -1)                    # config index per slot, -1 idle
        order = np.concatenate([self.rng.permutation(len(configs)) for _ in range(M // max(1, len(configs)) + 1)])[:M]  # stratified
        steps = np.zeros(R, np.int64)
        while done < M:
            for r in np.nonzero(slot < 0)[0]:
                if launched >= M: break
                j = int(order[launched])
                sim.set(r, np.unpackbits(configs[j][0], count=n).astype(bool)); self.perturb(r)
                slot[r] = j; steps[r] = 0; launched += 1
            act = slot >= 0
            lo = np.where(act, lam_next, -1); hi = np.where(act, lamA, 0)
            sg, sm, mm = sim.run_until(chunk, lo, hi)
            for r in np.nonzero(act)[0]:
                if sg[r] >= 0:
                    steps[r] += sg[r]; done += 1; lens.append(int(steps[r]))
                    if sm[r] <= lam_next:
                        succ += 1; out.append((np.packbits(sim.get(r)), configs[slot[r]][1]))
                    slot[r] = -1
                else:
                    steps[r] += chunk
                    if steps[r] > maxlen:
                        done += 1; slot[r] = -1; lens.append(int(steps[r]))   # counted as failure (never seen)
        return out, succ / M, float(np.mean(lens))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('kind'); ap.add_argument('a'); ap.add_argument('b', nargs='?')
    ap.add_argument('--D', type=int, default=2); ap.add_argument('--M', type=int, default=2000)
    ap.add_argument('--N0', type=int, default=1000); ap.add_argument('--delta', default='auto')
    ap.add_argument('--reps', type=int, default=4); ap.add_argument('--W', type=int, default=1)
    ap.add_argument('--T0', type=int, default=200); ap.add_argument('--tag', default=None)
    ap.add_argument('--seed', type=int, default=1); ap.add_argument('--pilot', type=int, default=2000)
    ap.add_argument('--lamA', type=int, default=None); ap.add_argument('--lam0', type=int, default=None)
    o = ap.parse_args()
    if o.kind == 'asym':
        R = int(o.a); v = fl.Vessel(fl.octa_hull(R), 'c', False); basin = Basin(v, 'soup')
    elif o.kind == 'sym':
        R = int(o.a); v = fl.Vessel(fl.octa_hull(R, o.b), o.b, True); basin = Basin(v, 'soup')
    else:
        cells, summ = fl.gump_cells(['--snapshot', o.a], 0, 'snap')
        v = fl.Vessel(summ['hull_final'], o.b, True); basin = Basin(v, 'snap', snap_bits=fl.bits_from_cells(v, cells))
    tag = o.tag or f'{o.kind}_{o.a}{o.b or ""}_D{o.D}'
    path = os.path.join(fl.SCR, f'ffs_{tag}.jsonl')
    have = sum(1 for _ in open(path)) if os.path.exists(path) else 0
    for rep in range(have, o.reps):
        rng = np.random.default_rng([o.seed, rep, zlib.crc32(tag.encode())])
        f = FFS(v, basin, o.W, o.D, rng, o.T0)
        t0 = time.time()
        m = f.pilot(o.pilot)
        mu, sd = float(m.mean()), float(m.std())
        lamA = o.lamA if o.lamA is not None else int(round(mu))
        lam0 = o.lam0 if o.lam0 is not None else int(round(mu - sd))
        delta = max(1, int(round(0.5 * sd))) if o.delta == 'auto' else int(o.delta)
        lams = list(range(lam0, 0, -delta)) + [0]
        configs, phi, st0 = f.stage0(lam0, lamA, o.N0)
        lnk = math.log(phi); var = 1.0 / st0['crossings']; stages = []
        for i in range(1, len(lams)):
            if not configs:
                lnk = -math.inf; break
            configs, P, L = f.stage(configs, lams[i], lamA, o.M)
            stages.append(dict(lam=lams[i], P=P, len=L, stored=len(configs), ancestors=len(set(a for _, a in configs)),
                               distinct=len(set(c.tobytes() for c, _ in configs))))
            if P == 0:
                lnk = -math.inf; break
            lnk += math.log(P); var += (1 - P) / (P * o.M)
        res = dict(tag=tag, rep=rep, A=v.A, nodes=v.n, D=o.D, M=o.M, N0=o.N0, T0=o.T0, mu_m=mu, sd_m=sd, lamA=lamA,
                   lams=lams, phi=phi, stage0=st0, stages=stages, ln_k=lnk, se_ln_k=math.sqrt(var),
                   tau_first=math.exp(-lnk) if lnk > -math.inf else None, wall=time.time() - t0)
        with open(path, 'a') as fh:
            fh.write(json.dumps(res) + '\n')
        print(f"{tag} rep {rep}: A={v.A} lamA={lamA} lams={lams[0]}..0 step {delta}; phi={phi:.4g}; "
              f"P=[{', '.join(f'{s['P']:.3f}' for s in stages)}]; ln tau_first = {-lnk:.3f} +- {math.sqrt(var):.3f} "
              f"(basin deaths {st0['deaths']} in {st0['expo']} gens); {time.time() - t0:.0f}s", flush=True)


if __name__ == '__main__':
    main()
