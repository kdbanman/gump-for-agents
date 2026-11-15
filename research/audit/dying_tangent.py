"""Lead's look, 2026-11-15: is the dip curve of a face a parabola joined to its own tangent line?

I(p) = [ln nu(0.9) - ln nu(p)] / A from research/dying/data/r3_excursions.csv (c1 faces, A = 45..108, and the
rim-free slab face).  If a depleted face is a mixture of an emptied region and a remnant held at relative density
p_t, the large-deviation cost is the convex envelope of the homogeneous branch and the empty point:
    I(p) = g (1-p)^2            for p >= p_t          (g from the shallow dips)
    I(p) = I(p_t) + 2 g (1-p_t) (p_t - p)   below     (the tangent at p_t)
so that I(0) = g (1 - p_t^2).  Printed: g fitted on 0.6 <= p <= 0.85, the local slope of I between neighbouring
levels (per unit p per site, and per live cell), where the slope stops growing (p_t read off the data), and the
end point the construction gives against the end point from the lifetime.
Run: python3 research/audit/dying_tangent.py
"""
import csv, math, collections
rows = collections.defaultdict(list)
for r in csv.DictReader(open('research/dying/data/r3_excursions.csv')):
    rows[(r['spec'], int(r['A']), float(r['pbar']))].append((float(r['p']), float(r['ln_nu']), float(r['ln_nu_se']), int(r['n_reach']), int(r['dead'])))
lntau = {}
for r in csv.DictReader(open('research/dying/data/r2_stationary.csv')):
    if r['group'] == 'c1' and r['ln_tau_face']:
        lntau[int(r['A'])] = float(r['ln_tau_face'])
lntau.setdefault(45, None)
for (spec, A, pbar), L in sorted(rows.items(), key=lambda kv: (kv[0][0].startswith('hex'), kv[0][1])):
    L.sort()
    d = {p: ln for p, ln, se, n, dead in L}
    if 0.9 not in d:
        continue
    I = {p: (d[0.9] - d[p]) / A for p in d}
    # g from the shallow part: least squares through I = g[(1-p)^2 - 0.01]
    xs = [((1 - p) ** 2 - 0.01, I[p]) for p in I if 0.6 <= p <= 0.85]
    g = sum(x * y for x, y in xs) / sum(x * x for x, y in xs)
    rho = pbar / A
    print(f"\n{spec}  A={A}  Pbar={pbar}  rho={rho:.3f}  g(0.6-0.85)={g:.4f}  ln nu(0.9)={d[0.9]:.3f}")
    ps = sorted(I)
    print("   p     I(p)    parabola   slope/site  slope/live cell")
    for a, b in zip(ps[:-1], ps[1:]):
        s = (I[a] - I[b]) / (b - a)
        print(f"  {a:4.2f}  {I[a]:.4f}  {g*((1-a)**2-0.01):.4f}    {s:.4f}     {s/rho:.3f}")
    # tangent point from the data: mean slope over 0.1 <= p <= 0.45 (unweighted line)
    T = [(p, I[p]) for p in ps if 0.1 <= p <= 0.45]
    n = len(T); mx = sum(p for p, _ in T) / n; my = sum(y for _, y in T) / n
    sl = -sum((p - mx) * (y - my) for p, y in T) / sum((p - mx) ** 2 for p, _ in T)
    pt = 1 - sl / (2 * g)
    I0_line = my + sl * mx
    I0_tan = g * (1 - pt * pt) - 0.01 * g
    out = f"   tail slope {sl:.4f}/site ({sl/rho:.3f}/live cell); tangency at p_t = 1 - slope/2g = {pt:.3f}; "
    out += f"I(0): line through the tail {I0_line:.4f}, parabola+tangent {I0_tan:.4f}"
    lt = lntau.get(A)
    if lt and not spec.startswith('hex'):
        out += f", from the lifetime [ln tau + ln nu(0.9)]/A = {(lt + d[0.9]) / A:.4f}"
    print(out)
