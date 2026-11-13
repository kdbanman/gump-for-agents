"""Run lists for the exponent study (one core; each call tops up runs_<tag>.json in research/scratch/exponent).
python3 jobs.py model1 | truth1 | gap | ...   (see the functions)"""
import sys, time
import xp
RHO_TOY = 0.472      # bulk density of the toy on a torus (research/toy2d README 4.3)
RHO_GUMP = 0.4155    # bulk density of gump (PROGRAM D4)

def budget(L):
    return {8: 20, 12: 25, 16: 40, 20: 60, 24: 150, 28: 300, 32: 600, 36: 1200, 40: 60}.get(L, 60)

def model(ws, Ls, rho=RHO_TOY, tag='model', deaths=3000, scale=1.0):
    for L in Ls:
        for w in ws:
            xp.run('w%d_L%d' % (w, L), xp.toy_model(w, L), rho=[rho, rho], deaths=deaths, maxsec=budget(L) * scale, tag=tag)

def truth(Ls, H=16, tag='truth', deaths=3000, scale=1.0):
    for L in Ls:
        xp.run('H%d_L%d' % (H, L), xp.toy_strip(H, L), deaths=deaths, maxsec=budget(L) * scale, tag=tag)

def noise(Ls=(12, 16, 20), epss=(1e-4, 1e-3, 1e-2, 3e-2), tag='noise'):
    for L in Ls:
        for e in epss:
            xp.run('L%d_eps%g' % (L, e), xp.toy_strip(16, L), eps=e, deaths=3000, maxsec=budget(L), tag=tag)

def slave(Ls=(12, 16, 20), w=1, d=7, tag='slave'):
    for L in Ls:
        xp.run('w%d_d%d_L%d' % (w, d, L), xp.toy_slave(16, L, w, d), deaths=3000, maxsec=budget(L) * 3, tag=tag, nev=1)

def rhoscan(w=4, Ls=(12, 16, 20), rhos=(0.35, 0.40, 0.44, 0.50, 0.55, 0.60), tag='rhoscan'):
    for L in Ls:
        for r in rhos:
            xp.run('w%d_L%d_rho%.2f' % (w, L, r), xp.toy_model(w, L), rho=[r, r], deaths=3000, maxsec=budget(L), tag=tag)

def gump(Rs=(7, 9, 11), ws=(1, 2, 3, 4, 5), tag='gump', rho=RHO_GUMP, scale=1.0, deaths=3000):
    bud = {7: 20, 9: 40, 11: 200, 13: 900}
    for R in Rs:
        for w in ws:
            xp.run('R%d_w%d' % (R, w), xp.gump_model(R, w), rule=xp.GUMP, p=0.35, T0=200, rho=[rho, rho], deaths=deaths,
                   maxsec=bud[R] * scale, tag=tag)

def slab(sizes=((3, 3), (3, 4), (4, 4), (4, 5)), m=12, tag='slab', scale=1.0):
    bud = {27: 30, 36: 60, 48: 200, 60: 600, 75: 1800}
    for a, b in sizes:
        xp.run('slab_%dx%d_m%d' % (a, b, m), xp.gump_slab(a, b, m), rule=xp.GUMP, p=0.35, T0=300, deaths=2000,
               maxsec=bud[3 * a * b] * scale, tag=tag)

CROSS3 = [(d, 0) for d in (1, 2, 3, -1, -2, -3)] + [(0, d) for d in (1, 2, 3, -1, -2, -3)]

def cross3(Ls=(16, 24, 32, 40, 48, 56, 64), H=24, tag='cross3'):
    """gump's rule B45/S345 on the 2D range-3 cross (12 neighbours; an edge cell sees 6 in-row + 3 below)."""
    for L in Ls:
        g = xp.toy_strip(H, L, offs=CROSS3, fw=4); g['name'] = 'cross3_strip_%dx%d' % (H, L)
        xp.run('c3_H%d_L%d' % (H, L), g, rule=xp.GUMP, p=0.4, T0=100, deaths=3000, maxsec=max(30, budget(min(L, 36) // 4 * 4) * 0.5), tag=tag)

def box(Ls=(12, 16, 20, 24), tag='box'):
    """the toy in L x L boxes is in research/toy2d; here: strips with OPEN ends are not needed."""
    pass

def slabmodel(sizes=((3, 3), (3, 4), (4, 4), (4, 5)), ws=(2, 3, 4, 5, 6, 8), tag='slabmodel', rho=RHO_GUMP):
    bud = {27: 20, 36: 40, 48: 120, 60: 400, 75: 1500}
    for a, b in sizes:
        for w in ws:
            xp.run('slab_%dx%d_w%d' % (a, b, w), xp.gump_slab_model(a, b, w), rule=xp.GUMP, p=0.35, T0=300, rho=[rho, rho],
                   deaths=3000, maxsec=bud[3 * a * b], tag=tag)

def rhoscan8(Ls=(16, 20), rhos=(0.30, 0.60), tag='rhoscan'):
    for L in Ls:
        for r in rhos:
            xp.run('w8_L%d_rho%.2f' % (L, r), xp.toy_model(8, L), rho=[r, r], deaths=3000, maxsec=budget(L), tag=tag)

if __name__ == '__main__':
    job = sys.argv[1]
    if job == 'model1':
        model((1, 2, 3, 4, 6, 8), (8, 12, 16, 20, 24))
    elif job == 'truth1':
        truth((8, 12, 16, 20, 24))
    elif job == 'model2':
        model((1, 2, 3, 4, 6, 8), (28,))
        truth((28,))
    elif job == 'model3':
        model((6, 8), (32,), deaths=2000)
        model((6,), (36,), deaths=1500, scale=1.25)
        model((6,), (40,), deaths=600, scale=40)
    elif job == 'gap':
        g = xp.toy_strip(16, 128)
        xp.run('gap_H16_L128', g, deaths=10 ** 9, maxsec=float(sys.argv[2]) if len(sys.argv) > 2 else 900, tag='gap', chunk=500)
    elif job == 'gapmodel':
        g = xp.toy_model(int(sys.argv[2]), 128)
        xp.run('gap_w%s_L128' % sys.argv[2], g, rho=[RHO_TOY, RHO_TOY], deaths=10 ** 9, maxsec=float(sys.argv[3]), tag='gap', chunk=500)
    elif job == 'noise':
        noise()
    elif job == 'slave':
        slave()
    elif job == 'rhoscan':
        rhoscan()
    elif job == 'gump':
        gump()
    elif job == 'gump13':
        gump(Rs=(13,), ws=tuple(int(v) for v in sys.argv[2].split(',')), deaths=400)
    elif job == 'slab':
        slab()
    elif job == 'cross3':
        cross3()
    elif job == 'slabmodel':
        slabmodel()
    elif job == 'slab75':
        slabmodel(sizes=((5, 5),), ws=(5,))
    elif job == 'rhoscan8':
        rhoscan8()
    else:
        raise SystemExit('unknown job')
