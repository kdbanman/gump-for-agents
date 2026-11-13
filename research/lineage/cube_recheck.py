#!/usr/bin/env python3
"""Re-test the 16 large plateaus of the closed cubes 13-16 (research/experiments/cube_vs_ensemble.py) with
 (a) the uncertainty of each ensemble mean tau (Gamma posterior from its deaths and exposure; the cube-centred x VF
     substitutes carry the VF spread too), and
 (b) the empirical distribution of T/tau from many single engine lineages at r = 31-36 (this directory), in place
     of an exact exponential.
Monte Carlo over 200,000 replicas of 16 plateaus. Statistics: S = sum of T/tau, N4 = # beyond 4 tau, N05 = # under
0.05 tau, and the joint (N4 >= 3 and N05 >= 3).
  python3 research/lineage/cube_recheck.py [CSV ...]    (lineage files as for analyze.py)
"""
import sys, os, csv, json, math, glob, gzip
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A
AMIN, VF, VF_SD = 408, 1.6, 0.15            # VF: vertex/cube factor where vertex-centred tau is unmeasured; sd of ln VF
area = A.area

def cube_plateaus():
    tau = {}
    for row in csv.DictReader(open("research/fluct/data/sym_residence.csv")):
        k = (int(row["A"]), row["centre"]); d = int(row["deaths"]); e = float(row["exposure"])
        D, E = tau.get(k, (0, 0.0)); tau[k] = (D + d, E + e)
    out = []
    for n in (13, 14, 15, 16):
        f = f"research/scratch/cubes/ev{n}.jsonl"
        if n == 16 and not os.path.exists(f): f = "research/data/cube16_events.jsonl"
        last = {}
        for line in open(f):
            e = json.loads(line)
            if e["type"] == "layer_death" and e["axis"] == 0 and e.get("cause") == "hull" and e["s"] > 0: last.setdefault(e["s"], e["last_alive"])
        cen = "v" if n % 2 == 0 else "c"; c0 = 3 if cen == "v" else 0; t = 0
        for s in sorted(last, reverse=True):
            r = s - c0; Ar = area(r)
            if last[s] <= t: continue
            T = last[s] - t; t = last[s]
            if Ar < AMIN: continue
            if (Ar, cen) in tau: D, E = tau[(Ar, cen)]; vf = 0
            elif (Ar, "c") in tau: D, E = tau[(Ar, "c")]; vf = 1
            else: continue
            out.append((n, r, T, D, E, vf))
    return out

def main():
    pl = cube_plateaus(); rng = np.random.default_rng(1); M = 200_000; k = len(pl)
    x_obs = np.array([T / (E / D * (VF if vf else 1)) for n, r, T, D, E, vf in pl])
    S, N4, N05 = x_obs.sum(), (x_obs > 4).sum(), (x_obs < 0.05).sum()
    print(f"{k} cube plateaus (A >= {AMIN}): S = {S:.1f}, beyond 4: {N4}, under 0.05: {N05}")
    # (a) tau uncertainty: x = T / tau with tau ~ E / Gamma(D) (flat prior on the rate), observed T fixed
    xs = np.empty((M, k))
    for j, (n, r, T, D, E, vf) in enumerate(pl):
        rate = rng.gamma(D, 1 / E, M)
        if vf: rate /= np.exp(math.log(VF) + VF_SD * rng.standard_normal(M))
        xs[:, j] = T * rate
    Ss = xs.sum(1)
    from scipy import stats
    p_S = np.mean(stats.gamma.sf(Ss, k)); p_4 = np.mean(stats.binom.sf((xs > 4).sum(1) - 1, k, math.exp(-4)))
    print(f"(a) averaged over the posterior of each tau: P(sum >= S) = {p_S:.4f}, P(>= N4 beyond 4) = {p_4:.4f}")
    print(f"    posterior median of S: {np.median(Ss):.1f};  of the side-16 R=40 ratio: {np.median(xs[:, [i for i,p in enumerate(pl) if p[0]==16 and p[1]==40][0]]):.2f}")
    # (b) null = empirical T/tau of the lineages here (structured + soup, reliable radii, after reweighting nothing)
    files = sys.argv[1:] or sorted(glob.glob("research/scratch/lineage/plateaus_*.csv")) or ["research/lineage/data/plateaus.csv.gz"]
    rows = A.load(files); tq = A.tau_q()
    emp = np.array([r["T"] / tq[(area(r["r"]), r["centre"])] for r in rows if r["died"] and A.RELIABLE(r["r"], r["centre"])
                    and (area(r["r"]), r["centre"]) in tq])
    emp = emp / emp.mean()                                       # remove the small offset of tau_q; keep the shape
    sim = rng.choice(emp, size=(M, k))
    s4, s05, ss = (sim > 4).sum(1), (sim < 0.05).sum(1), sim.sum(1)
    print(f"(b) null = {len(emp)} lineage plateaus (shape only): P(S >= {S:.1f}) = {np.mean(ss >= S):.4f}, "
          f"P(N4 >= {N4}) = {np.mean(s4 >= N4):.4f}, P(N05 >= {N05}) = {np.mean(s05 >= N05):.4f}, "
          f"P(both) = {np.mean((s4 >= N4) & (s05 >= N05)):.4f}")
    ex = rng.exponential(size=(M, k))
    print(f"    same with exact Exp(1):                    P(S >= {S:.1f}) = {np.mean(ex.sum(1) >= S):.4f}, "
          f"P(N4 >= {N4}) = {np.mean((ex > 4).sum(1) >= N4):.4f}, P(N05 >= {N05}) = {np.mean((ex < 0.05).sum(1) >= N05):.4f}, "
          f"P(both) = {np.mean(((ex > 4).sum(1) >= N4) & ((ex < 0.05).sum(1) >= N05)):.4f}")
    # look-elsewhere: the most extreme of several natural statistics (min of the four p-values) under Exp(1)
    def pvals(z):
        return np.stack([stats.gamma.sf(z.sum(1), k),
                         stats.binom.sf((z > 4).sum(1) - 1, k, math.exp(-4)),
                         stats.binom.sf((z < 0.05).sum(1) - 1, k, 1 - math.exp(-0.05)),
                         np.array([stats.kstest(row, "expon").pvalue for row in z])], 1)
    pv_obs = pvals(x_obs[None, :])[0]; pv_sim = pvals(ex[:20000])
    pmin = pv_obs.min(); p_le = np.mean(pv_sim.min(1) <= pmin)
    print(f"look-elsewhere: p-values (sum, >4, <0.05, KS) = {np.round(pv_obs, 4)}; smallest {pmin:.4f}; "
          f"chance the smallest of the four is this small under Exp(1): {p_le:.4f}")

if __name__ == "__main__":
    main()
