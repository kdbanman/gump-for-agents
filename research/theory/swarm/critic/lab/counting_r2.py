"""Critic's lab: checks and lab requests for counting, round 2 (exact; no sampling).

  python3 counting_r2.py lemma7   Lemma 7 (a live edge cell thins its own support) by enumeration
  python3 counting_r2.py ck [kmax]  request 1: fixed-age exponents c_k of the one-row dice model D2 (default kmax 4)
  python3 counting_r2.py gap2     request 2: the horizon-2 exponents V1, V2, V3 against the true rule's c_2
  python3 counting_r2.py tilt     request 3: the tilted (Perron) measures of M_1 and M_2
  python3 counting_r2.py tri      request 5: lone cell and lone triangle of a periodic gump face over fair dice
  python3 counting_r2.py gump1    request 4, small version: one-generation death probability of whole periodic faces
"""
import sys, os, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prob_r1 as pr
import counting_r1 as c1m
import startpoints as sp

OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


def rule(s, n):
    return ((n + s >= 3) & (n <= 4)).astype(np.int64)


# -------------------------------------------------------------------------------------------------- lemma 7
def lemma7():
    # cells: (x,0); (x,1) with its row neighbours x+-1, x+-2; (x,2) with its row neighbours; (x,3); (x,4)
    names = ['e0', 'c1', 'c2', 'c3', 'c4'] + ['a%d' % i for i in range(4)] + ['b%d' % i for i in range(4)]
    cnt = {}
    for bits in itertools.product((0, 1), repeat=len(names)):
        v = dict(zip(names, bits))
        n1 = v['e0'] + v['c2'] + v['c3'] + sum(v['a%d' % i] for i in range(4))
        n2 = v['e0'] + v['c1'] + v['c3'] + v['c4'] + sum(v['b%d' % i] for i in range(4))
        y1 = int(n1 + v['c1'] >= 3 and n1 <= 4); y2 = int(n2 + v['c2'] >= 3 and n2 <= 4)
        key = (v['e0'], y1, y2)
        cnt[key] = cnt.get(key, 0) + 1
    tot = 1 << (len(names) - 1)
    p1 = {s: sum(c for (e, a, b), c in cnt.items() if e == s and a) / tot for s in (0, 1)}
    p2 = {s: sum(c for (e, a, b), c in cnt.items() if e == s and b) / tot for s in (0, 1)}
    check(abs(p1[0] - 85 / 128) < 1e-12 and abs(p1[1] - 76 / 128) < 1e-12 and abs(p2[0] - 161 / 256) < 1e-12 and abs(p2[1] - 119 / 256) < 1e-12,
          f"Lemma 7: P((x,1) alive at 1 | s) = {p1[0]:.6f}, {p1[1]:.6f} (85/128, 76/128); P((x,2) alive at 1 | s) = {p2[0]:.6f}, {p2[1]:.6f} (161/256, 119/256)")
    pair = {s: [cnt.get((s, a, b), 0) / tot for a in (0, 1) for b in (0, 1)] for s in (0, 1)}
    print("       joint law of ((x,1), (x,2)) at generation 1 given s: (00, 01, 10, 11) =", [round(v, 5) for v in pair[0]], "for s = 0;",
          [round(v, 5) for v in pair[1]], "for s = 1")
    return cnt, tot


# ------------------------------------------------------------------------------------------------------- ck
def dk_d2(k, p, laws, cond_law=None, iters=3000, tol=1e-13):
    """Exponent of P(row empty at generation k) for one row of the 2D rule over dice, row 0 started Bernoulli(p).
    laws[t] = law (pi0, pi1, pi2) of b at the step t -> t+1 (t = 0..k-1). cond_law (optional, k = 2 only): a dict
    (s0, s1) -> law, used for the step 1 -> 2 instead of laws[1] (s0, s1 = the cell's own states at generations 0, 1).
    Transfer matrix on windows (x-2, x-1, x, x+1) of the rows S_0..S_{k-1}: 2^(4k) states, 2^k new bits per step."""
    A = [pr.a_table(l) for l in laws]
    if cond_law is not None:
        Ac = {key: pr.a_table(l) for key, l in cond_law.items()}
    nst = 1 << (4 * k)
    S = np.arange(nst, dtype=np.int64)
    win = [[(S >> (4 * t + i)) & 1 for i in range(4)] for t in range(k)]         # win[t][i] = S_t(x-2+i)
    W = np.zeros((nst, 1 << k)); nxt = np.zeros((nst, 1 << k), np.int64)
    for new in range(1 << k):
        nb = [(new >> t) & 1 for t in range(k)]                                    # S_t(x+2)
        w = np.where(win[0][2] == 1, p, 1 - p).astype(float)
        for t in range(k):
            kk = win[t][0] + win[t][1] + win[t][3] + nb[t]
            s = win[t][2]
            if t + 1 < k:
                target = win[t + 1][2]
                if cond_law is not None and t == 1:
                    pa = np.zeros(nst)
                    for (s0, s1), tab in Ac.items():
                        m = (win[0][2] == s0) & (win[1][2] == s1)
                        pa[m] = tab[s[m], kk[m]]
                else:
                    pa = A[t][s, kk]
                w = w * np.where(target == 1, pa, 1 - pa)
            else:
                if cond_law is not None and t == 1:
                    pa = np.zeros(nst)
                    for (s0, s1), tab in Ac.items():
                        m = (win[0][2] == s0) & (win[1][2] == s1)
                        pa[m] = tab[s[m], kk[m]]
                else:
                    pa = A[t][s, kk]
                w = w * (1 - pa)                                                   # S_k(x) = 0
        W[:, new] = w
        st = np.zeros(nst, np.int64)
        for t in range(k):
            wt = (win[t][1]) | (win[t][2] << 1) | (win[t][3] << 2) | (nb[t] << 3)
            st |= wt << (4 * t)
        nxt[:, new] = st
    v = np.ones(nst) / nst
    lam = 0.0
    flat_n = nxt.ravel()
    for it in range(iters):
        u = np.bincount(flat_n, weights=(v[:, None] * W).ravel(), minlength=nst)
        l2 = u.sum(); u /= l2
        if abs(l2 - lam) < tol and it > 50:
            lam = l2; break
        v, lam = u, l2
    return -np.log(lam), (W, nxt, v, lam)


def ck(kmax=4):
    print("request 1: c_k = -lim (1/L) ln P(row 0 empty at generation k), D2 on a ring, row 0 started Bernoulli(p)")
    binl = lambda r: ((1 - r) ** 2, 2 * r * (1 - r), r * r)
    for p, rho in ((0.5, 0.5), (0.472, 0.472), (0.6455, 0.472)):
        vals = []
        for k in range(1, kmax + 1):
            c, _ = dk_d2(k, p, [binl(rho)] * k)
            vals.append(c)
            print(f"   p = {p}, rho = {rho}: c_{k} = {c:.6f}", flush=True)
        print(f"   p = {p}, rho = {rho}: differences c_k - c_k+1: " + ', '.join(f"{a - b:.4f}" for a, b in zip(vals, vals[1:])))
    # check at k = 1 against the 16-state matrix, and k = 2 against a direct ring sum at L = 6
    c, _ = dk_d2(1, 0.5, [binl(0.5)])
    check(abs(c - 0.551535) < 1e-6, f"k = 1, p = rho = 1/2: {c:.6f} = the true rule's c_1 (0.551535)")
    L = 6; A = pr.a_table(binl(0.5))
    tot = 0.0
    for S0 in range(1 << L):
        b0 = [(S0 >> i) & 1 for i in range(L)]
        k0 = [b0[(x - 2) % L] + b0[(x - 1) % L] + b0[(x + 1) % L] + b0[(x + 2) % L] for x in range(L)]
        for S1 in range(1 << L):
            b1 = [(S1 >> i) & 1 for i in range(L)]
            w = 0.5 ** L
            for x in range(L):
                pa = A[b0[x], k0[x]]
                w *= pa if b1[x] else 1 - pa
            if w == 0: continue
            for x in range(L):
                k1 = b1[(x - 2) % L] + b1[(x - 1) % L] + b1[(x + 1) % L] + b1[(x + 2) % L]
                w *= 1 - A[b1[x], k1]
            tot += w
    c2, (W, nxt, v, lam) = dk_d2(2, 0.5, [binl(0.5)] * 2)
    # trace of the 6th power by periodic sequences of new-bit pairs
    tr = 0.0
    for seq in itertools.product(range(4), repeat=L):
        st = 0
        for t in range(2):
            for i in range(4):
                st |= ((seq[(-4 + i) % L] >> t) & 1) << (4 * t + i)
        w = 1.0
        for x in range(L):
            w *= W[st, seq[x]]
            if w == 0: break
            st = nxt[st, seq[x]]
        tr += w
    check(abs(tr - tot) < 1e-12, f"k = 2: P(row empty at generation 2) on a ring of 6 by direct summation {tot:.10f}, by the transfer matrix {tr:.10f}")
    print("   for comparison, exact steps of ln tau of D2(L, 1/2) on a ring at L = 15..18: 0.543, 0.528, 0.528, 0.533; D2(L, 0.472): 0.536, 0.523, 0.522, 0.526;")
    print("   on an interval (dead or reflecting ends), rho = 0.472: 0.460")


# ----------------------------------------------------------------------------------------------------- gap2
def pair_laws():
    """true rule, uniform soup, half-plane: law of the pair ((x,1), (x,2)) at generation 1; and given (s0, s1), the
    states of (x,0) at generations 0 and 1."""
    names = ['e0', 'c1', 'c2', 'c3', 'c4'] + ['a%d' % i for i in range(4)] + ['b%d' % i for i in range(4)] + ['r%d' % i for i in range(4)]
    joint = {}
    for bits in itertools.product((0, 1), repeat=len(names)):
        v = dict(zip(names, bits))
        n1 = v['e0'] + v['c2'] + v['c3'] + sum(v['a%d' % i] for i in range(4))
        n2 = v['e0'] + v['c1'] + v['c3'] + v['c4'] + sum(v['b%d' % i] for i in range(4))
        y1 = int(n1 + v['c1'] >= 3 and n1 <= 4); y2 = int(n2 + v['c2'] >= 3 and n2 <= 4)
        n0 = sum(v['r%d' % i] for i in range(4)) + v['c1'] + v['c2']
        s1 = int(n0 + v['e0'] >= 3 and n0 <= 4)
        key = (v['e0'], s1, y1 + y2)
        joint[key] = joint.get(key, 0) + 1
    tot = float(1 << len(names))
    marg = [sum(c for (s0, s1, b), c in joint.items() if b == bb) / tot for bb in range(3)]
    cond = {}
    for s0 in (0, 1):
        for s1 in (0, 1):
            z = sum(c for (a, b_, bb), c in joint.items() if a == s0 and b_ == s1)
            cond[(s0, s1)] = tuple(joint.get((s0, s1, bb), 0) / z for bb in range(3))
    return tuple(marg), cond


def gap2():
    print("request 2: horizon 2, uniform start (density 1/2); exponent per cell of P(row 0 empty at generation 2)")
    binl = lambda r: ((1 - r) ** 2, 2 * r * (1 - r), r * r)
    marg, cond = pair_laws()
    v1, _ = dk_d2(2, 0.5, [binl(0.5), binl(0.5)])
    v2, _ = dk_d2(2, 0.5, [binl(0.5), marg])
    v3, _ = dk_d2(2, 0.5, [binl(0.5), marg], cond_law=cond)
    print(f"   law of b at generation 1 (true rule from soup): {tuple(round(x, 5) for x in marg)}, mean {marg[1] + 2 * marg[2]:.4f}")
    for key in sorted(cond):
        print(f"       given (s0, s1) = {key}: {tuple(round(x, 5) for x in cond[key])}, mean {cond[key][1] + 2 * cond[key][2]:.4f}")
    print(f"   V0 (true rule) = 0.467693;  V1 (fresh fair dice at generation 1) = {v1:.6f};  V2 (dice with the true pair law) = {v2:.6f};  "
          f"V3 (pair law given the cell's own two states) = {v3:.6f}")
    print(f"   V1 - V2 = {v1 - v2:+.4f} (density);  V2 - V3 = {v2 - v3:+.4f} (own-column feedback);  V3 - V0 = {v3 - 0.467693:+.4f} (everything spatial)")


# ----------------------------------------------------------------------------------------------------- tilt
def tilt():
    print("request 3: the tilted (Perron) measures of the horizon-1 and horizon-2 matrices at density 1/2")
    T = c1m.k1_matrix(0.5)
    ev, R = np.linalg.eig(T); i = int(np.argmax(ev.real)); r = np.abs(R[:, i].real); lam = ev.real[i]
    ev2, Lv = np.linalg.eig(T.T); j = int(np.argmax(ev2.real)); l = np.abs(Lv[:, j].real)
    # pair measure over (state, next): windows of five cells (a, b, c, d, e)
    P5 = np.zeros(32)
    for s in range(16):
        for e in (0, 1):
            t = ((s << 1) & 15) | e
            P5[(s << 1) | e] += l[s] * T[s, t] * r[t]
    P5 /= P5.sum()
    dens = sum(P5[w] for w in range(32) if (w >> 2) & 1)
    print(f"   k = 1: density of live edge cells at generation 0 in the dying ensemble: {dens:.4f} (soup: 0.5); windows 00000: {P5[0]:.4f} (soup 0.0312); "
          f"isolated live cell 00100: {P5[4]:.4f} (soup 0.0312); full window 11111: {P5[31]:.4f}")
    # k = 2 with the 2^16-state matrix of counting_r1; split the weight by the generation-1 state of the centre cell
    W, nxt = c1m.k2_weights(0.5)
    nst = 1 << 16
    flat = nxt.ravel()
    v = np.ones(nst) / nst; u = np.ones(nst) / nst
    for it in range(600):
        v2 = np.bincount(flat, weights=(v[:, None] * W).ravel(), minlength=nst); lam2 = v2.sum(); v2 /= lam2
        u2 = (W * u[nxt]).sum(1); u2 /= u2.sum()
        if it > 50 and np.abs(v2 - v).max() < 1e-15: v, u = v2, u2; break
        v, u = v2, u2
    mu = v * u; mu /= mu.sum()                                   # tilted measure on window states
    S = np.arange(nst)
    r0 = [(S >> i) & 1 for i in range(8)]                        # columns x-4..x+3
    dens0 = float((mu * r0[4]).sum())
    w5 = sum(r0[i] << (i - 2) for i in range(2, 7))              # cells x-2..x+2
    f00000 = float(mu[w5 == 0].sum()); f00100 = float(mu[w5 == 4].sum())
    # generation-1 density: recompute the centre cell's generation-1 state inside the weights
    S64 = S.astype(np.int64)
    r1 = [(S64 >> (8 + i)) & 1 for i in range(4)]; r2 = [(S64 >> (12 + i)) & 1 for i in range(4)]
    num = 0.0; den = 0.0
    for new in range(8):
        a0, a1, a2 = new & 1, (new >> 1) & 1, (new >> 2) & 1
        R0 = r0 + [np.full_like(S64, a0)]; R1 = r1 + [np.full_like(S64, a1)]; R2 = r2 + [np.full_like(S64, a2)]
        g0 = []
        for c in range(-2, 3):
            n = R0[c + 2] + R0[c + 3] + R0[c + 5] + R0[c + 6] + R1[c + 2] + R2[c + 2]
            g0.append(rule(R0[c + 4], n))
        for r3 in (0, 1):
            for r4 in (0, 1):
                n1 = R1[0] + R1[1] + R1[3] + R1[4] + R0[4] + R2[2] + r3
                y1 = rule(R1[2], n1)
                n2 = R2[0] + R2[1] + R2[3] + R2[4] + R1[2] + R0[4] + r3 + r4
                y2 = rule(R2[2], n2)
                G = rule(g0[2], g0[0] + g0[1] + g0[3] + g0[4] + y1 + y2)
                wgt = v * (G == 0) / 32.0 * u[nxt[:, new]]
                num += float((wgt * g0[2]).sum()); den += float(wgt.sum())
    print(f"   k = 2: density of live edge cells at generation 0: {dens0:.4f}; at generation 1: {num / den:.4f}; windows 00000 at generation 0: {f00000:.4f}; "
          f"isolated live cell 00100: {f00100:.4f}   (c_2 = {5 * np.log(2) - np.log(lam2 * 32):.6f})")


# ------------------------------------------------------------------------------------------------------ tri
def face_data(a, b, m=4):
    cells, nb = sp.make_slab(a, b, m)
    face = [i for i, cc in enumerate(cells) if cc[2] == -1]
    fs = set(face)
    inl = {i: [j for j in nb[i] if j in fs] for i in face}
    ben = {i: [j for j in nb[i] if j not in fs] for i in face}
    comps, _ = sp.components(face, ben)
    return cells, face, inl, ben, comps


def death_prob(face, inl, ben, live, rho):
    """exact P(face empty next) over product dice of density rho, for a set `live` of live face cells: only the
    cells beneath face cells with k >= 1 or alive matter."""
    live = set(live)
    act = [i for i in face if i in live or any(j in live for j in inl[i])]
    under = sorted(set(j for i in act for j in ben[i]))
    tot = 0.0; cnt = 0
    for bits in itertools.product((0, 1), repeat=len(under)):
        val = dict(zip(under, bits))
        ok = True
        for i in act:
            k = sum(1 for j in inl[i] if j in live)
            bb = sum(val[j] for j in ben[i])
            x = 1 if i in live else 0
            if (3 if x else 4) <= k + bb <= 5:
                ok = False; break
        if ok:
            s = sum(bits); tot += rho ** s * (1 - rho) ** (len(under) - s); cnt += 1
    return tot, cnt, len(under)


def tri():
    print("request 5: periodic gump face 4 x 4 (no doubled neighbours), cells beneath i.i.d.")
    cells, face, inl, ben, comps = face_data(4, 4)
    c0 = face[0]
    cube = [cp for cp in comps if c0 in cp][0]
    for rho in (0.5, 0.4155):
        p1, n1, u1 = death_prob(face, inl, ben, [c0], rho)
        f1 = (1 - 3 * rho ** 3 + 3 * rho ** 5 - rho ** 6) * (1 - rho ** 3) ** 4
        p3, n3, u3 = death_prob(face, inl, ben, cube, rho)
        f3 = (1 - rho) ** 6 * (1 - 2 * rho ** 3 + rho ** 5) ** 6
        check(abs(p1 - f1) < 1e-12 and abs(p3 - f3) < 1e-12,
              f"rho = {rho}: lone cell {p1:.6f} (formula {f1:.6f}; {n1} of 2^{u1} patterns at rho = 1/2); lone triangle {p3:.6f} (formula {f3:.6f}; {n3} of 2^{u3})")
    nbrs_tri = sorted(set(j for i in cube for j in inl[i]) - set(cube))
    ks = [sum(1 for j in inl[i] if j in cube) for i in nbrs_tri]
    cubes_n = sorted(len([i for i in cp if i in nbrs_tri]) for cp in comps if any(i in nbrs_tri for i in cp))
    check(len(nbrs_tri) == 12 and set(ks) == {1} and cubes_n == [2] * 6, f"the triangle has {len(nbrs_tri)} dead in-face neighbours, each with k = {sorted(set(ks))}, "
                                                                         f"lying {cubes_n} to a cube")


# ---------------------------------------------------------------------------------------------------- gump1
def gump1():
    print("request 4, small version: P(whole periodic face empty after one generation) over fair dice, by the cube criterion, every configuration")
    for (a, b) in ((3, 3),):
        cells, face, inl, ben, comps = face_data(a, b)
        A = len(face)
        dup = any(len(set(inl[i])) < len(inl[i]) for i in face)
        pos = {i: t for t, i in enumerate(face)}
        nstate = 1 << A
        S = np.arange(nstate, dtype=np.uint32)
        logw = np.zeros(nstate, np.float32)
        zero = np.zeros(nstate, bool)
        for cp in comps:
            ach = sp.achievable(cp, ben)
            und = sorted(set(j for i in cp for j in ben[i]))
            # multiplicity of each b-triple among the 2^6 assignments
            mult = {}
            for bits in itertools.product((0, 1), repeat=len(und)):
                val = dict(zip(und, bits))
                t = tuple(sum(val[j] for j in ben[i]) for i in cp)
                mult[t] = mult.get(t, 0) + 1
            # key = (x, k) for the three cells -> index
            xs = [((S >> np.uint32(pos[i])) & 1).astype(np.uint8) for i in cp]
            ks = []
            for i in cp:
                k = np.zeros(nstate, np.uint8)
                for j in inl[i]:
                    k += ((S >> np.uint32(pos[j])) & 1).astype(np.uint8)
                ks.append(k)
            key = np.zeros(nstate, np.int32)
            for x, k in zip(xs, ks):
                key = key * 14 + (x.astype(np.int32) * 7 + k)
            table = np.zeros(14 ** 3)
            for combo in itertools.product(range(14), repeat=3):
                idx = (combo[0] * 14 + combo[1]) * 14 + combo[2]
                w = 0
                for t, mu in mult.items():
                    if all(not ((3 if c // 7 else 4) <= (c % 7) + bb <= 5) for c, bb in zip(combo, t)):
                        w += mu
                table[idx] = w / 64.0
            wv = table[key]
            zero |= wv == 0
            logw += np.log(np.maximum(wv, 1e-300)).astype(np.float32)
            del xs, ks, key, wv
        w = np.where(zero, 0.0, np.exp(logw.astype(np.float64)))
        D1 = w.sum() / nstate
        pop = np.zeros(nstate, np.uint8)
        for i in range(A):
            pop += ((S >> np.uint32(i)) & 1).astype(np.uint8)
        dens = float((w * pop).sum() / w.sum()) / A
        print(f"   face {a} x {b} ({A} cells" + (", doubled neighbours" if dup else "") + f"): P(empty at generation 1) = {D1:.6e}; -ln/A = {-np.log(D1) / A:.4f}; "
              f"configurations that can be emptied: {int((~zero).sum())} of {nstate}; density of the face in the dying ensemble {dens:.4f}", flush=True)


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'lemma7': lemma7()
    elif what == 'ck': ck(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    elif what == 'gap2': gap2()
    elif what == 'tilt': tilt()
    elif what == 'tri': tri()
    elif what == 'gump1': gump1()
    print('ALL OK' if OK else 'SOMETHING FAILED')
