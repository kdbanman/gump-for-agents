#!/usr/bin/env python3
"""Driver for ring.c (thin torus, packed rings).

    python3 run.py validate                       # ring.c against the reference stepper (= oracle) and the engine
    python3 run.py run TAG det|model b m_or_w SECONDS [T0] [GS] [rho16] [WALL] [K]   # chunks until SECONDS; resumable
                                                  # (K: the wider torus (1,K),(0,b), stepped by ringk.c)
    python3 run.py stats TAG...                   # ln tau per tag from the chunk files (prefix match with *)

Chunk files: research/scratch/thin/<TAG>/c<k>.txt (one per chunk, seed = hash of tag and k). A run can be killed
at any time: finished chunks are kept, the unfinished one is lost.
"""
import glob, hashlib, math, os, subprocess, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(ROOT, 'research', 'scratch', 'thin')
BIN = os.path.join(OUT, 'ring')
BINK = os.path.join(OUT, 'ringk')       # the tori (1,k),(0,b); ring.c is the reference for k = 1
ENGINE = os.path.join(ROOT, 'engine', 'target', 'release', 'gump')
sys.path.insert(0, HERE)
import thin  # noqa: E402

P0 = 26214          # soup density 0.4 (x 65536)
RHO = 26112         # coin density 102/256 = 0.3984 (x 65536): the thin torus's bulk density (layers 2-5: 0.397)


def build():
    os.makedirs(OUT, exist_ok=True)
    for exe, files in ((BIN, ('ring.c', 'nbr.h')), (BINK, ('ringk.c', 'nbrk.h'))):
        src = [os.path.join(HERE, f) for f in files]
        if not os.path.exists(exe) or os.path.getmtime(exe) < max(map(os.path.getmtime, src)):
            subprocess.check_call(['gcc', '-O3', '-march=native', '-o', exe + '.new', src[0]])
            os.replace(exe + '.new', exe)


def ring(mode, b, mw, seed, gens, T0, out, cap=0, gs=0, rho=RHO, p0=P0, extra=(), notch=0, k=1, force_k=False):
    if k != 1 or force_k:
        extra = (*extra, '-k', str(k))
    subprocess.check_call([BINK if (k != 1 or force_k) else BIN, mode, str(b), str(mw), str(rho), str(p0), str(seed), str(gens), str(T0), str(cap),
                           str(gs), out, *extra, *(('-n', str(notch)) if notch else ())])


def parse(path):
    d = {}
    with open(path) as f:
        lines = f.read().splitlines()
    h = lines[0].split(); d['head'] = dict(zip(h[0::2], h[1::2]))
    t = lines[1].split()[1:]; d['tot'] = {k: float(v) for k, v in zip(t[0::2], t[1::2])}
    for line in lines[2:]:
        p = line.split(); d[p[0]] = np.array(p[1:], float)
    return d


def read_dump(path, b, nt):
    """dump -> array [gens + 1, lanes, nt * 3 * b] of 0/1"""
    rows = {}
    for line in open(path):
        p = line.split(); g, l = int(p[0]), int(p[1])
        words = [int(x, 16) for x in p[3:]]
        bits = np.array([(w >> c) & 1 for w in words for c in range(b)], np.int8)
        rows[(g, l)] = bits
    G = max(g for g, _ in rows) + 1; NLn = max(l for _, l in rows) + 1
    return np.array([[rows[(g, l)] for l in range(NLn)] for g in range(G)])


def validate_dump(mode, b, mw, gens, seed=5, notch=0, k=1, force_k=False, gs=0, ccoin=None):
    """Every lane, every generation: the dumped next state is the reference stepper's image of the dumped state,
    except where a life ended; ends (deaths, ages) are recomputed and compared with ring's own tallies."""
    nt = mw + 2 if mode == 'model' else mw
    dp = os.path.join(OUT, f'dump_{os.getpid()}.txt'); out = os.path.join(OUT, f'vout_{os.getpid()}.txt')
    cc = ('-c', *map(str, ccoin)) if ccoin else ()
    ring(mode, b, mw, seed, gens, 0, out, extra=('-d', dp, *cc), notch=notch, k=k, force_k=force_k, gs=gs)
    D = read_dump(dp, b, nt); r = parse(out)
    nb = thin.graph(b, nt, k)
    nd = mw * 3 * b
    faces = [np.arange(3 * b)] + ([np.arange((mw - 1) * 3 * b, mw * 3 * b)] if mode == 'det' else [])
    wall = np.zeros(nd, bool)                       # face cells held dead: sites 0..notch-1 = {Z_s, Y_s, X_{s+1}}
    for f in faces:
        for s_ in range(notch):
            wall[f[0] + 2 * b + s_] = wall[f[0] + b + s_] = wall[f[0] + (s_ + 1) % b] = True
    assert not D[:, :, :nd][:, :, wall].any(), 'a wall cell is alive in the dump'
    # every end of a life is re-derived here by ring.c's stated rules (head of ring.c), not read from its output
    NLn = D.shape[1]
    bad = 0; deaths = 0; expo = 0; born = np.zeros(NLn, int); settled = 0; interior = 0; steps = 0
    snap = [None] * NLn; snapage = [0] * NLn
    # one-generation moves of face cells by (state, live face neighbours), recounted for ring.c's `trans`
    trans = np.zeros((2, 7, 2), int)
    inface = [np.array([[j for j, (dt, _, _) in zip(nb[i], thin.TABK[k][(i // b) % 3]) if dt == 0] for i in f]) for f in faces]
    for g in range(gens):
        for l in range(NLn):
            nxt = thin.step_ref(D[g, l], nb)[:nd]
            nxt[wall] = 0
            g1 = g + 1; age = g1 - born[l]; end = 0; L = age
            if gs and g1 % gs == 0:
                for f, nf_ in zip(faces, inface):
                    keep = ~wall[f]
                    np.add.at(trans, (D[g, l][f][keep], D[g, l][nf_].sum(1)[keep], nxt[f][keep]), 1)
            nde = sum(int(nxt[f].sum() == 0) for f in faces)
            got = D[g + 1, l][:nd]
            steps += 1
            if nde:
                deaths += nde; end = 1
            else:
                if snapage[l] and (mode == 'det' or mw >= 4) and (nxt == snap[l]).all() and (mode == 'det' or not nxt[3 * b:].any()):
                    end = 2; settled += 1; L = snapage[l]
                if not end and age >= 16 and age & (age - 1) == 0:
                    snap[l] = nxt.copy(); snapage[l] = age
                if not end and g1 % 840 == 0:
                    alive = nxt.reshape(mw, 3 * b).any(1); last = mw - 2 if mode == 'det' else mw - 1
                    if any(not alive[t:t + 3].any() for t in range(1, last - 1)):
                        end = 3; interior += 1
            if end:
                expo += L; born[l] = g1; snapage[l] = 0; snap[l] = None
            elif not (got == nxt).all():
                bad += 1
    expo += int((gens - born).sum())
    t = r['tot']
    ok = (bad == 0 and deaths == int(t['alldeaths']) and settled == int(t['settled']) and interior == int(t['interior'])
          and expo == int(r['expo'].sum()))
    if gs and 'trans' in r:
        ok = ok and (trans.reshape(-1) == r['trans'].astype(int)).all()
    msg = (f'validate_dump {mode}{" [ringk]" if (k != 1 or force_k) else ""} (1,{k}),(0,{b}) layers={mw} wall={notch}: {steps} lane-steps, {bad} wrong, deaths {deaths} '
           f'(ring: {int(t["alldeaths"])}), repeating {settled} ({int(t["settled"])}), firewall {interior} ({int(t["interior"])}), '
           f'exposure {expo} ({int(r["expo"].sum())})' + (f', moves by (state, k) recounted: {int(trans.sum())}' if gs and 'trans' in r else ''))
    if mode == 'model' and ccoin:
        # coins that know the face above them: frequencies given the face, and no memory
        X = D[:gens].reshape(-1, D.shape[2]).astype(int); zmax = 0.0; res = np.zeros((X.shape[0], 6 * b))
        for i in range(3 * b, 9 * b):
            t, o = i // (3 * b), (i // b) % 3
            ups = [j for j, (dt, _, _) in zip(nb[i], thin.TAB[o]) if dt == -t]      # the face cells that read this coin
            assert len(ups) == 3 - t
            j_ = X[:, ups].sum(1); p = (np.array(ccoin[:3]) if t == 1 else np.array(ccoin[3:])) / 65536
            res[:, i - 3 * b] = X[:, i] - p[j_]
        for t, pr in ((1, ccoin[:3]), (2, ccoin[3:])):
            cells = np.arange(t * 3 * b, (t + 1) * 3 * b)
            jj = np.stack([X[:, [j for j, (dt, _, _) in zip(nb[i], thin.TAB[(i // b) % 3]) if dt == -t]].sum(1) for i in cells], 1)
            for v, p16 in enumerate(pr):
                sel = jj == v; n_ = int(sel.sum()); p = p16 / 65536
                if n_ > 100:
                    zmax = max(zmax, abs(X[:, cells][sel].sum() - n_ * p) / math.sqrt(n_ * p * (1 - p)))
        R3 = res.reshape(gens, D.shape[1], 6 * b)
        ac = float(np.mean(R3[1:] * R3[:-1]) / np.mean(R3 ** 2)); nn_ = R3[1:].size
        msg += f'; conditional coins: largest |z| of a frequency {zmax:.2f}, correlation of residuals in time {ac:+.5f} (1/sqrt(n) = {1 / math.sqrt(nn_):.5f})'
        ok = ok and zmax < 4.5 and abs(ac) < 5 / math.sqrt(nn_)
    elif mode == 'model':
        nz = D[:gens, :, nd:].astype(float)                  # coins
        dens = nz.mean(); n = nz.size
        z = (dens - RHO / 65536) / math.sqrt(dens * (1 - dens) / n)
        ac = np.mean((nz[1:] - dens) * (nz[:-1] - dens)) / (dens * (1 - dens))      # lag 1 in time
        sp = np.mean((nz[:, :, 1:] - dens) * (nz[:, :, :-1] - dens)) / (dens * (1 - dens))   # adjacent cells
        ln = np.mean((nz[:, 1:] - dens) * (nz[:, :-1] - dens)) / (dens * (1 - dens))  # adjacent lanes
        msg += (f'; coins: density {dens:.5f} (want {RHO / 65536:.5f}, z = {z:+.2f}), correlation in time {ac:+.5f}, '
                f'between cells {sp:+.5f}, between lanes {ln:+.5f} (1/sqrt(n) = {1 / math.sqrt(n):.5f})')
        ok = ok and abs(z) < 4 and max(abs(ac), abs(sp), abs(ln)) < 5 / math.sqrt(n)
    for f in (dp, out):
        os.remove(f)
    print(msg, 'OK' if ok else 'FAIL')
    return ok


def validate_pca(b, gens, p16, seed=9, notch=0):
    """Mode pca from a dump: wall cells stay dead; the moves by (state, live face neighbours) equal ring.c's own
    `trans` (steps that end in a death left out of both); their frequencies agree with the table; the residuals of
    cells that are face neighbours are uncorrelated (the cells are updated independently)."""
    tf = os.path.join(OUT, f'ptab_{os.getpid()}.txt'); open(tf, 'w').write(' '.join(str(int(x)) for x in np.asarray(p16).reshape(-1)))
    dp = os.path.join(OUT, f'dump_{os.getpid()}.txt'); out = os.path.join(OUT, f'vout_{os.getpid()}.txt')
    ring('pca', b, 1, seed, gens, 0, out, extra=('-d', dp, '-p', tf), notch=notch, gs=1)
    D = read_dump(dp, b, 1); r = parse(out)
    nb = thin.graph(b, 1)
    inface = np.array([[j for j, (dt, _, _) in zip(nb[i], thin.TAB[i // b]) if dt == 0] for i in range(3 * b)])
    wall = np.zeros(3 * b, bool)
    for s_ in range(notch):
        wall[2 * b + s_] = wall[b + s_] = wall[(s_ + 1) % b] = True
    assert not D[:, :, wall].any(), 'a wall cell is alive in the dump'
    X = D[:-1].reshape(-1, 3 * b); Y = D[1:].reshape(-1, 3 * b)
    kk = X[:, inface].sum(-1)
    P = np.asarray(p16, float).reshape(2, 7) / 65536
    trans = np.zeros((2, 7, 2), int)
    np.add.at(trans, (X[:, ~wall], kk[:, ~wall], Y[:, ~wall]), 1)
    mine = r['trans'].astype(int).reshape(2, 7, 2)
    ndeath = int(r['tot']['alldeaths'])
    # ring.c counts the true next state, the dump shows the fresh soup after a death: allow for those steps
    same = np.abs(trans - mine).sum() <= 2 * ndeath * int((~wall).sum())
    zmax = 0.0
    for s_ in (0, 1):
        for q in range(7):
            n = mine[s_, q].sum(); p = P[s_, q]
            if n > 0 and 0 < p < 1:
                zmax = max(zmax, abs(mine[s_, q, 1] - n * p) / math.sqrt(n * p * (1 - p)))
            elif n > 0:
                same = same and mine[s_, q, 1] == (n if p >= 1 else 0)
    res = (Y - P[X, kk]) * (~wall)                                         # residuals; zero mean under the model
    pairs = [(i, j) for i in range(3 * b) for j in inface[i] if i < j and not wall[i] and not wall[j]]
    c = np.array([np.mean(res[:, i] * res[:, j]) for i, j in pairs]); n = res.shape[0]
    var = np.mean(res[:, [i for i, _ in pairs]] ** 2 * res[:, [j for _, j in pairs]] ** 2, axis=0)
    zc = np.abs(c) / np.sqrt(var / n + 1e-300)
    for f in (dp, out, tf):
        os.remove(f)
    ok = bool(same) and zmax < 4.5 and zc.max() < 4.5
    print(f'validate_pca b={b} wall={notch}: {X.shape[0]} lane-steps, {ndeath} deaths, moves by (state, k) equal to the dump: {bool(same)}; '
          f'largest |z| of a frequency against the table {zmax:.2f}; largest |z| of a covariance between neighbours {zc.max():.2f} '
          f'({len(pairs)} pairs)', 'OK' if ok else 'FAIL')
    return ok


def validate_engine(b, m, gens, seed=3, k=1):
    """Lane 0 from a listed soup against the engine on the cubic b-torus (b copies), population every generation."""
    rng = np.random.default_rng(seed)
    n = m * 3 * b
    live = np.nonzero(rng.random(n) < 0.4)[0]
    ini = os.path.join(OUT, f'ini_{os.getpid()}.txt'); open(ini, 'w').write('\n'.join(map(str, live)))
    dp = os.path.join(OUT, f'dump_{os.getpid()}.txt'); out = os.path.join(OUT, f'vout_{os.getpid()}.txt')
    ring('det', b, m, seed, gens, 0, out, extra=('-i', ini, '-d', dp), k=k)
    mine = []
    for line in open(dp):
        p = line.split()
        if p[1] == '0':
            mine.append(sum(bin(int(x, 16)).count('1') for x in p[3:]))
    pts = set()
    for i in live:
        t, o, c = i // (3 * b), (i // b) % 3, i % b
        p0 = thin.doubled(t, o, c)
        for s in range(b):
            pts.add(((p0[0] + 2 * s) % (2 * b), (p0[1] + 2 * k * s) % (2 * b), (p0[2] - 2 * (1 + k) * s) % (2 * b)))
    assert len(pts) == b * len(live)
    cf = os.path.join(OUT, f'cells_{os.getpid()}.txt'); open(cf, 'w').write('\n'.join(' '.join(map(str, q)) for q in sorted(pts)))
    pl = os.path.join(OUT, f'pl_{os.getpid()}.txt')
    subprocess.run([ENGINE, 'run', '--cells', cf, '--torus', str(b), '--gens', str(gens), '--no-halt', '--poplog', pl],
                   check=True, capture_output=True)
    ref = {int(l.split()[0]): int(l.split()[1]) for l in open(pl)}
    # compare until lane 0's first reseed (a face death): the engine has no reseeding
    nmatch = 0
    for g, v in enumerate(mine):
        if g in ref and ref[g] == v * b:
            nmatch += 1
        else:
            break
    for f in (ini, dp, out, cf, pl):
        os.remove(f)
    ok = nmatch >= min(gens, 200)
    print(f'validate_engine (1,{k}),(0,{b}) m={m}: populations equal to the engine (x{b} copies) for the first {nmatch} generations '
          f'of {gens} (a mismatch after a face death is the reseeding); {len(set(mine[:nmatch]))} distinct', 'OK' if ok else 'FAIL')
    return ok, nmatch


def chunk_seed(tag, k):
    return int(hashlib.sha256(f'{tag}:{k}'.encode()).hexdigest()[:12], 16)


def run(tag, mode, b, mw, seconds, T0=256, gs=0, rho=RHO, gens=None, notch=0, k=1, extra=()):
    build()
    d = os.path.join(OUT, tag); os.makedirs(d, exist_ok=True)
    t0 = time.time(); nchunk = len(glob.glob(os.path.join(d, 'c*.txt')))
    # chunk length: about 60 s
    if gens is None:
        tt = time.time(); ring(mode, b, mw, 1, 20000, T0, os.path.join(OUT, f'probe_{os.getpid()}.txt'), gs=gs, rho=rho, notch=notch, k=k, extra=extra)
        os.remove(os.path.join(OUT, f'probe_{os.getpid()}.txt'))
        gens = max(20000, int(20000 * 60 / max(time.time() - tt, 1e-3)))
    while time.time() - t0 < seconds:
        tmp = os.path.join(d, f'tmp_{os.getpid()}')
        ring(mode, b, mw, chunk_seed(tag, nchunk), gens, T0, tmp, gs=gs, rho=rho, notch=notch, k=k, extra=extra)
        os.replace(tmp, os.path.join(d, f'c{nchunk}.txt')); nchunk += 1
    print(f'{tag}: {nchunk} chunks', flush=True)


def load(tag):
    fs = sorted(glob.glob(os.path.join(OUT, tag, 'c*.txt')))
    if not fs:
        return None
    acc = None
    for f in fs:
        r = parse(f)
        if acc is None:
            acc = r; acc['n'] = 1; continue
        for k, v in r.items():
            if k == 'head':
                assert all(v[q] == acc['head'][q] for q in ('mode', 'b', 'layers', 'T0', 'rho16')) \
                    and v.get('notch', '0') == acc['head'].get('notch', '0') and v.get('twist', '1') == acc['head'].get('twist', '1')
            elif k == 'tot':
                for kk in v:
                    acc['tot'][kk] += v[kk]
            elif k in acc and len(acc[k]) == len(v):
                acc[k] = acc[k] + v
            elif k not in acc:
                acc[k] = v
        acc['n'] += 1
    return acc


def lntau(acc, cut=30.0, full=False):
    """Per-face ln tau = ln(nface * exposure / deaths) from the age-binned record, ages in [T0, 2^K): K is the first
    bin edge beyond `cut` mean lives (survival e^-cut: no life of the chaotic state gets there). Exposure found
    beyond 2^K is a life that stopped dying without being recognised as repeating (README, "Subtle points"); it is
    left out and reported by `stats` (and returned with full=True). Error 1/sqrt(deaths)."""
    nface = 2 if acc['head']['mode'] == 'det' else 1
    T0 = int(acc['head']['T0']); k0 = T0.bit_length() - 1
    assert 1 << k0 == T0, 'T0 must be a power of two (the age bins are powers of two)'
    e, d = np.asarray(acc['expo'], float), np.asarray(acc['deaths'], float)
    K = k0 + 1
    while K < len(e):
        E, F = e[k0:K].sum(), d[k0:K].sum()
        if F > 0 and (1 << K) >= cut * E / F:
            break
        K += 1
    E, F = e[k0:K].sum(), d[k0:K].sum()
    if F == 0:
        return (float('nan'), float('nan'), 0, 0.0) if full else (float('nan'), float('nan'), 0)
    out = (math.log(nface * E / F), 1 / math.sqrt(F), int(F))
    return out + (float(e[K:].sum()),) if full else out


def stats(tags):
    for pat in tags:
        for d in sorted(glob.glob(os.path.join(OUT, pat))):
            tag = os.path.basename(d); acc = load(tag)
            if acc is None:
                continue
            lt, er, F, excess = lntau(acc, full=True); h = acc['head']; t = acc['tot']
            # hazard in three age classes of the binned record (ages >= T0)
            T0 = int(h['T0']); ex, de = acc['expo'], acc['deaths']
            ks = [k for k in range(len(ex)) if (1 << k) - 1 >= T0 and ex[k] > 0]
            thirds = ''
            if ks:
                cum = np.cumsum(ex[ks]); cuts = np.searchsorted(cum, [cum[-1] / 3, 2 * cum[-1] / 3])
                parts = [ks[:cuts[0] + 1], ks[cuts[0] + 1:cuts[1] + 1], ks[cuts[1] + 1:]]
                nf = 2 if h['mode'] == 'det' else 1
                thirds = ' '.join(f'{math.log(nf * ex[p].sum() / de[p].sum()):.3f}' if p and de[p].sum() > 0 else '-' for p in parts)
            print(f'{tag:28s} {h["mode"]:5s} b={h["b"]:>2s} A={3 * int(h["b"]):3d} layers={h["layers"]} chunks={acc["n"]:4d} '
                  f'deaths={F:8d} ln tau = {lt:.4f} +- {er:.4f}  settled={int(t["settled"])} interior={int(t["interior"])} '
                  f'both={int(t["both"])}  by age: {thirds}' + (f'  LEFT OUT: {excess:.3g} lane-generations of lives older than 30 mean lives' if excess else ''))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'validate':
        build()
        ok = True
        ok &= thin.oracle_check(16, 8, 300)
        ok &= thin.oracle_check(12, 5, 200)
        for (mode, b, mw, g) in [('det', 16, 8, 400), ('det', 5, 8, 300), ('det', 64, 8, 150), ('det', 7, 3, 1000),
                                 ('model', 16, 5, 300), ('model', 6, 1, 2000), ('model', 64, 2, 150), ('model', 9, 3, 1000)]:
            ok &= validate_dump(mode, b, mw, g)
        for (mode, b, mw, g, nn) in [('det', 12, 8, 600, 3), ('det', 64, 8, 100, 5), ('model', 9, 1, 2000, 3), ('model', 20, 5, 300, 4)]:
            ok &= validate_dump(mode, b, mw, g, notch=nn)
        # small systems, where lives end in repeating states and behind firewalls: every such end re-derived
        for (mode, b, mw, g, nn) in [('det', 5, 8, 5040, 0), ('det', 6, 9, 5040, 0), ('det', 7, 3, 2000, 0), ('det', 9, 5, 3000, 3),
                                     ('model', 8, 4, 4000, 3), ('model', 7, 5, 4000, 0), ('det', 16, 12, 200, 3), ('model', 16, 8, 200, 3),
                                     ('model', 6, 6, 5040, 0), ('model', 8, 8, 5040, 3)]:
            ok &= validate_dump(mode, b, mw, g, notch=nn)
        # the moves of face cells by (state, live face neighbours) recounted; the face-only automaton (mode pca)
        for (mode, b, mw, g, nn, gs_) in [('det', 12, 8, 600, 0, 1), ('det', 11, 8, 900, 3, 2), ('model', 9, 1, 1500, 3, 1), ('det', 6, 4, 1500, 0, 1)]:
            ok &= validate_dump(mode, b, mw, g, notch=nn, gs=gs_)
        ptab = [[0, 4100, 23000, 45000, 37000, 11500, 0], [4600, 23500, 51000, 59000, 38000, 12000, 0]]
        ok &= validate_pca(24, 3000, ptab)
        ok &= validate_pca(12, 6000, ptab, notch=3)
        for (b, g, nn) in [(12, 3000, 0), (10, 3000, 3)]:      # coins that know the face above them (ccoin.py)
            ok &= validate_dump('model', b, 1, g, notch=nn, ccoin=(17000, 24000, 30000, 24000, 28000))
        for (b, m, g) in [(16, 8, 3000), (24, 8, 3000), (40, 8, 1500)]:
            ok &= validate_engine(b, m, g)[0]
        # ringk.c: equal to the reference stepper at k = 1 (with and without wall) and on the wider tori; engine
        for (mode, b, mw, g, nn, kk) in [('det', 16, 8, 300, 0, 1), ('det', 12, 8, 400, 3, 1), ('model', 9, 3, 600, 0, 1),
                                          ('det', 16, 8, 300, 0, 2), ('det', 20, 8, 200, 0, 3), ('det', 24, 8, 150, 0, 4),
                                          ('model', 16, 5, 200, 0, 2), ('det', 11, 3, 600, 0, 2),
                                          ('det', 7, 8, 5040, 0, 2), ('model', 9, 4, 4000, 0, 2)]:
            ok &= validate_dump(mode, b, mw, g, notch=nn, k=kk, force_k=True)
        for (b, m, g, kk) in [(16, 8, 2000, 2), (24, 8, 2000, 2), (20, 8, 2000, 3)]:
            ok &= validate_engine(b, m, g, k=kk)[0]
        print('ALL OK' if ok else 'FAILED')
        sys.exit(0 if ok else 1)
    elif cmd == 'run':
        tag, mode, b, mw, seconds = sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])
        T0 = int(sys.argv[7]) if len(sys.argv) > 7 else 256
        gs = int(sys.argv[8]) if len(sys.argv) > 8 else 0
        rho = int(sys.argv[9]) if len(sys.argv) > 9 else RHO
        notch = int(sys.argv[10]) if len(sys.argv) > 10 else 0
        kk = int(sys.argv[11]) if len(sys.argv) > 11 else 1
        run(tag, mode, b, mw, seconds, T0, gs, rho, notch=notch, k=kk)
    elif cmd == 'stats':
        stats(sys.argv[2:] or ['*'])
