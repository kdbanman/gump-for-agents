"""Regrowth against decline: is a dying boundary the time-reverse of a recovering one, and does the tail ratio of
the living boundary follow from ordinary regrowth?  (exponent.md, section "gump erodes, the toy flashes")

Driven-boundary model (numpy stepper, same graphs as drv.c): equilibrate, then CLEAR the boundary layer except a
seed (one random cell, or `seed` adjacent cells), and follow its population n_t.  Typical events only.
Outputs (JSON in research/scratch/exponent/regrow_<name>.json):
  - P(the seed takes: n reaches `top` before 0), mean n_t of trajectories that take;
  - one-generation increments d = n_{t+1} - n_t of ALL trajectories while lo <= n_t <= hi, and the root kappa > 0 of
    E[exp(-kappa d)] = 1  (Cramer-Lundberg: if n were a random walk with these increments, the stationary law of a
    living boundary would have P(n = k) / P(n = k+1) = exp(-kappa) in that range);
  - the same root for T-generation increments (T = 2, 3), to see what memory does.
python3 regrow.py gump R w [rounds] [reps]   |   python3 regrow.py toy w L [rounds] [reps]
"""
import json, os, sys, time
import numpy as np
import xp

def make_step(g, rule, rho):
    N, M = g['N'], g['M']; nb = np.asarray(g['nb']).copy(); nb[nb < 0] = N + M
    B = np.zeros(16, bool); S = np.zeros(16, bool)
    for k in range(16):
        B[k] = rule[0] >> k & 1; S[k] = rule[1] >> k & 1
    def step(x, rng):
        n = x[:, nb].sum(2)
        y = np.where(x[:, :N] == 1, S[n], B[n]).astype(np.uint8)
        x = np.empty_like(x); x[:, :N] = y; x[:, N:N + M] = rng.random((len(x), M)) < rho; x[:, N + M] = 0
        return x
    return step

def root(d, w=None):
    """kappa > 0 with sum w exp(-kappa d) = sum w, by bisection; nan if no negative increments."""
    d = np.asarray(d, float); w = np.ones_like(d) if w is None else np.asarray(w, float)
    if not (d < 0).any() or (w * d).sum() <= 0: return float('nan')
    f = lambda k: (w * np.exp(-k * d)).sum() / w.sum() - 1
    lo, hi = 1e-6, 0.05
    while f(hi) < 0 and hi < 50: hi *= 2
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

def run(g, rule, rho, name, rounds=20, reps=2000, burn=250, T=48, seed_cells=1, lo=4, hi=14, top=None, rseed=1):
    rng = np.random.default_rng(rseed); step = make_step(g, rule, rho)
    N, M = g['N'], g['M']; face = np.asarray(g['lines'][0][1]); A = len(face)
    nbf = np.asarray(g['nb'])[face]                      # for adjacent seeds
    top = top or int(0.35 * A)
    traj = []; t0 = time.time()
    for r in range(rounds):
        x = np.zeros((reps, N + M + 1), np.uint8); x[:, :N] = rng.random((reps, N)) < 0.4; x[:, N:N + M] = rng.random((reps, M)) < rho
        for t in range(burn): x = step(x, rng)
        alive = x[:, face].any(1)
        # clear the face except a seed
        keep = np.zeros((reps, A), bool); c0 = rng.integers(0, A, reps); keep[np.arange(reps), c0] = True
        if seed_cells > 1:
            fidx = {int(c): i for i, c in enumerate(face)}
            for i in range(reps):
                cand = [fidx[int(j)] for j in nbf[c0[i]] if int(j) in fidx]
                for j in rng.permutation(cand)[:seed_cells - 1]: keep[i, j] = True
        xf = np.zeros((reps, A), np.uint8); xf[keep] = 1; x[:, face] = xf
        ns = [x[:, face].sum(1).astype(np.int64)]
        for t in range(T):
            x = step(x, rng); ns.append(x[:, face].sum(1).astype(np.int64))
        traj.append(np.array(ns).T[alive])
        print('round %d/%d  %.0f s' % (r + 1, rounds, time.time() - t0), flush=True)
    n = np.concatenate(traj)                              # (trajectories, T+1)
    # outcome: first time n = 0 (dies) or n >= top (takes)
    dead = (n == 0); took = (n >= top)
    td = np.where(dead.any(1), dead.argmax(1), 10 ** 6); tt = np.where(took.any(1), took.argmax(1), 10 ** 6)
    takes = tt < td; dies = td < tt
    out = dict(name=name, A=A, trajectories=int(len(n)), p_take=float(takes.mean()), p_die=float(dies.mean()), top=top,
               mean_take=[float(v) for v in n[takes].mean(0)], mean_all=[float(v) for v in n.mean(0)], lo=lo, hi=hi)
    # increments while lo <= n_t <= hi (before absorption at 0), all trajectories
    for Tinc in (1, 2, 3, 4):
        a = n[:, :-Tinc]; b = n[:, Tinc:]
        ok = (a >= lo) & (a <= hi) & (np.arange(a.shape[1])[None, :] < td[:, None])
        d = (b - a)[ok]
        out['kappa_T%d' % Tinc] = root(d) / 1.0; out['mean_inc_T%d' % Tinc] = float(d.mean()); out['var_inc_T%d' % Tinc] = float(d.var())
        out['n_inc_T%d' % Tinc] = int(len(d)); out['neg_frac_T%d' % Tinc] = float((d < 0).mean())
        if Tinc == 1:
            out['kappa_by_n'] = {int(k): root((b - a)[ok & (a == k)]) for k in range(lo, hi + 1)}
            vals, cnt = np.unique(d, return_counts=True); out['inc_hist'] = {int(v): int(c) for v, c in zip(vals, cnt)}
    fn = os.path.join(xp.SCR, 'regrow_%s.json' % name)
    json.dump(out, open(fn, 'w'))
    print('%s: A = %d, %d trajectories from a %d-cell seed: takes %.3f, dies %.3f' % (name, A, len(n), seed_cells, out['p_take'], out['p_die']))
    print('  mean n_t of the trajectories that take, t = 0..16: ' + ' '.join('%.1f' % v for v in out['mean_take'][:17]))
    for Tinc in (1, 2, 3, 4):
        k = out['kappa_T%d' % Tinc]
        print('  %d-generation increments at %d <= n <= %d: mean %+.2f var %.2f, negative %.2f; root kappa = %.3f per generation-step -> exp(-kappa) = %.3f' %
              (Tinc, lo, hi, out['mean_inc_T%d' % Tinc], out['var_inc_T%d' % Tinc], out['neg_frac_T%d' % Tinc], k, np.exp(-k)))
    print('  kappa by n (1 generation): ' + ' '.join('%d:%.2f' % (k, v) for k, v in out['kappa_by_n'].items()))
    return out

if __name__ == '__main__':
    which = sys.argv[1]; a1, a2 = int(sys.argv[2]), int(sys.argv[3])
    rounds = int(sys.argv[4]) if len(sys.argv) > 4 else 20; reps = int(sys.argv[5]) if len(sys.argv) > 5 else 2000
    seedc = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    if which == 'gump':
        g = xp.gump_model(a1, a2); run(g, xp.GUMP, 0.4155, 'gump_R%d_w%d_s%d' % (a1, a2, seedc), rounds, reps, seed_cells=seedc)
    elif which == 'slab':
        g = xp.gump_slab_model(a1, a1, a2); run(g, xp.GUMP, 0.4155, 'slab_%d_w%d_s%d' % (a1, a2, seedc), rounds, reps, seed_cells=seedc, hi=20)
    else:
        g = xp.toy_model(a1, a2); run(g, xp.TOY, 0.472, 'toy_w%d_L%d_s%d' % (a1, a2, seedc), rounds, reps, seed_cells=seedc, lo=3, hi=8)
