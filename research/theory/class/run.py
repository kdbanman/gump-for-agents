"""run.py -- drive gstep on (lattice, capped threshold) pairs.  Results are appended to
research/scratch/class/results.jsonl (one JSON object per run) and printed.

    python3 run.py bulk LATTICE b c [--n N] [--T T] [--p P]          torus: chaos, glass, settle or die?
    python3 run.py face LATTICE b c --m M --n N [--sec S] [--p P]    slab/strip: face-death law with censoring
    python3 run.py life LATTICE b c --R R [--T T]                    hull vessel: lifetimes of 64 soups
    python3 run.py rule LATTICE Bset Sset ...                        same with explicit B/S (e.g. 4,5 3,4,5)

Censoring (the pitfall): a replica is ended and reseeded, and NOT counted as a face death, when it settles
(period <= 2, or equal to a snapshot: periods <= 4096) or when a dead sealed set appears that is not a whole
boundary layer (a transverse cut or a pit).  tau_face = nfaces * exposure / face deaths (exposure = replica
generations older than T0).
"""
import argparse, json, math, os, subprocess, sys, time
import lattices as LT, theory as TH, vessel as VS

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, "..", "..", "scratch", "class")
GSTEP = os.path.join(SCR, "gstep")
RES = os.path.join(SCR, "results.jsonl")


def mask(s):
    m = 0
    for k in s:
        m |= 1 << k
    return m


def graph_file(V, tag):
    fn = os.path.join(SCR, f"g_{tag}_{os.getpid()}.bin")
    V.write(fn)
    return fn


def gstep(args):
    out = subprocess.run([GSTEP] + [str(a) for a in args], capture_output=True, text=True, check=True).stdout
    return [json.loads(l) for l in out.strip().split("\n") if l.strip()]


def save(rec):
    with open(RES, "a") as f:
        f.write(json.dumps(rec) + "\n")


def default_p(K, B, S):
    """Soup density: the upper mean-field fixed point if there is one, else mid-window."""
    fps = TH.mf_bulk(K, B, S)
    if fps:
        return min(0.8, max(0.25, fps[-1][0]))
    return min(0.8, max(0.25, (min(B) + max(B)) / (2.0 * K) + 0.05))


def bulk(lat, B, S, n=None, T=4096, p=None, seed=1, quiet=False):
    L = LT.get(lat)
    b = min(B)
    if n is None:
        n = 64 if L.dim == 2 else 10
    V = VS.torus(L, n)
    if p is None:
        p = default_p(L.K, B, S)
    fn = graph_file(V, "torus")
    rows = gstep(["bulk", fn, mask(B), mask(S), b, p, seed, T, 64])
    os.remove(fn)
    last, mid = rows[-1], rows[max(0, len(rows) - 3)]
    if last["running"] >= 48 and last["act"] >= 0.05 and last["act"] >= 0.6 * mid["act"]:
        cls = "chaos"
    elif last["running"] >= 16:
        cls = "glass" if last["act"] >= 0.002 else "clock"   # still moving, but little / decaying activity
    elif last["dens_all"] < 0.02:
        cls = "die"
    else:
        cls = "freeze"
    rec = dict(kind="bulk", lattice=lat, rule=TH.rule_name(B, S), b=b, N=V.N, n=n, T=T, p=round(p, 3), cls=cls,
               running=last["running"], sealed=last["sealed"], dens=last["dens"], act=last["act"],
               dens_all=last["dens_all"], act_mid=mid["act"], rows=rows)
    save(rec)
    if not quiet:
        print(f"bulk {lat:9s} {rec['rule']:22s} N={V.N} p={p:.2f} -> {cls:6s} running={last['running']}/64 "
              f"dens={last['dens']:.3f} act={last['act']:.3f} (mid {mid['act']:.3f}) dens_all={last['dens_all']:.3f} sealed={last['sealed']}")
    return rec


def face(lat, B, S, m, n, sec=60, p=None, T0=200, maxg=10 ** 9, seed=1, u=None, quiet=False, chk=16):
    L = LT.get(lat)
    b = min(B)
    if u is None:
        u = TH.sealed_rays(L, b)[0]
    V = VS.slab(L, tuple(u), m, n)
    if p is None:
        p = default_p(L.K, B, S)
    fn = graph_file(V, "slab")
    r = gstep(["qsd", fn, mask(B), mask(S), b, p, seed, T0, maxg, sec, chk])[0]
    os.remove(fn)
    A = V.info["face_cells"]
    nf = r["face"]
    tau = 2 * (r["exposure"] + r["running"]) / nf if nf else None   # replicas still running at the end are censored, not dropped
    lntau = math.log(tau) if nf else None
    mean_age = r["sum_age"] / nf if nf else None
    cv = None
    if nf >= 10:
        var = r["sum_age2"] / nf - mean_age ** 2
        cv = math.sqrt(max(var, 0)) / mean_age if mean_age > 0 else None
    rec = dict(kind="face", lattice=lat, rule=TH.rule_name(B, S), b=b, u=list(u), m=m, n=n, A=A, N=V.N, p=round(p, 3),
               tau=tau, lntau=lntau, err=(1 / math.sqrt(nf) if nf else None), cv=cv, **{k: v for k, v in r.items() if k != 'N'})
    save(rec)
    if not quiet:
        print(f"face {lat:9s} {rec['rule']:18s} m={m} A={A:4d} N={V.N:5d}: face={nf} seal={r['seal']} p2={r['p2']} cyc={r['cyc']} "
              f"early={r['early']} tau={tau if tau is None else round(tau, 1)} ln={lntau if lntau is None else round(lntau, 2)} "
              f"cv={cv if cv is None else round(cv, 2)} dens(int,face,next)={r['dens']} act={r['act']} gens={r['gens']} {r['sec']}s")
    return rec


def life(lat, B, S, R, T=100000, p=None, seed=1, quiet=False):
    L = LT.get(lat)
    b = min(B)
    V = VS.hull(L, b, R)
    if p is None:
        p = default_p(L.K, B, S)
    fn = graph_file(V, "hull")
    r = gstep(["life", fn, mask(B), mask(S), b, p, seed, T])[0]
    os.remove(fn)
    st = sorted(x if x >= 0 else T for x in r["settle"])
    med = st[len(st) // 2]
    rec = dict(kind="life", lattice=lat, rule=TH.rule_name(B, S), b=b, R=R, N=V.N, p=round(p, 3), T=T, median=med,
               q25=st[16], q75=st[48], unfinished=sum(1 for x in r["settle"] if x < 0), final_dens=r["final_dens"])
    save(rec)
    if not quiet:
        print(f"life {lat:9s} {rec['rule']:18s} R={R} N={V.N}: median {med} (q25 {st[16]}, q75 {st[48]}), "
              f"unfinished {rec['unfinished']}/64, final density {r['final_dens']:.3f}")
    return rec


def parse_set(s):
    return set(int(a) for a in s.split(",") if a != "")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("lattice")
    ap.add_argument("x")
    ap.add_argument("y")
    ap.add_argument("--n", type=int)
    ap.add_argument("--m", type=int, default=16)
    ap.add_argument("--R", type=int, default=8)
    ap.add_argument("--T", type=int, default=4096)
    ap.add_argument("--p", type=float)
    ap.add_argument("--sec", type=float, default=60)
    ap.add_argument("--T0", type=int, default=200)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--rule", action="store_true", help="x, y are explicit B and S sets")
    a = ap.parse_args()
    L = LT.get(a.lattice)
    if a.rule:
        B, S = parse_set(a.x), parse_set(a.y)
    else:
        B, S = TH.capped(int(a.x), int(a.y), L.K)
    if a.cmd == "bulk":
        bulk(a.lattice, B, S, a.n, a.T, a.p, a.seed)
    elif a.cmd == "face":
        face(a.lattice, B, S, a.m, a.n, a.sec, a.p, a.T0, seed=a.seed)
    elif a.cmd == "life":
        life(a.lattice, B, S, a.R, a.T, a.p, a.seed)
