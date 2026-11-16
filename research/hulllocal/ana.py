#!/usr/bin/env python3
"""Reduce the runs of hl.py: occupation statistics by position in the face, layer by layer, with block errors.

  python3 research/hulllocal/ana.py NAME_sSEED [...]      # one table per run
  python3 research/hulllocal/ana.py --all                 # every run in research/scratch/hulllocal

Cell classes (hull of radius R, face f = (d, sigma), the layer sigma d.p = R):
  depth k  = (R - sigma d.p) / 2, the layer index below face f (k = 0: the face layer);
  r        = min over the 6 other faces e (not f, not its opposite) of e's depth: how many layers of a
             neighbouring face lie between the cell and that face. r = 0: the cell is in the face layer of a
             second face too (the rim). Face layer interior: k = 0, r >= 3.
  For a layer k beneath: the column under the face interior is r >= k + 3.
Slab (m layers): face layers t = 0 and m-1; layer k beneath = t in {k, m-1-k}.
Statistics per class (exposure = alive replica-generations):
  rho      live cell-generations / (cells x exposure)
  births   births / (cells x exposure)
  dn, dnin dead cells' mean live-neighbour count, total and in the cell's own layer
  l35c     the share of live cells with 3-5 live neighbours (= survivors / live);  l35 = per cell (wraplocal's)
  var/A    per face: Var(face population) / A, the 8 (or 2) faces averaged
Errors: the scatter of the block means (blocks are independent soups), each block's two halves pooled.
"""
import glob, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hl  # noqa: E402

SCR = hl.SCR


def classes(v, name):
    """dict label -> (cells array with repetition allowed per face) of cell indices, pooled over equivalent faces"""
    out = {}
    if name.startswith('hull'):
        R = v.R
        for f in range(8):
            opp = f ^ 1
            others = [e for e in range(8) if e not in (f, opp)]
            k = v.depth[:, f]
            r = v.depth[:, others].min(1)
            own = np.argmin(v.depth, 1)
            for kk in range(0, 5):
                sel = k == kk
                for rr in range(0, R):
                    c = np.nonzero(sel & (r == rr))[0]
                    if len(c):
                        out.setdefault(('k', kk, 'r', rr), []).append(c)
                c = np.nonzero(sel & (r >= kk + 3))[0]
                if len(c):
                    out.setdefault(('k', kk, 'int'), []).append(c)
            out.setdefault(('face', 'all'), []).append(np.nonzero(k == 0)[0])
        out = {a: np.concatenate(b) for a, b in out.items()}
        # depth of the cell below the nearest face, whole vessel
        dmin = v.depth.min(1)
        for kk in range(dmin.max() + 1):
            out[('dmin', kk)] = np.nonzero(dmin == kk)[0]
    else:
        m = v.hkdm[3]
        for kk in range((m + 1) // 2):
            out[('k', kk, 'int')] = np.nonzero((v.t == kk) | (v.t == m - 1 - kk))[0]
        out[('face', 'all')] = out[('k', 0, 'int')]
    return out


def load(tag):
    z = np.load(os.path.join(SCR, tag + '.npz'))
    return z


def stats(z, cl):
    """per block (pooled halves) and per half (pooled blocks) arrays of each statistic for one class"""
    def per(sumax):
        live = z['live'].sum(sumax); birth = z['birth'].sum(sumax); dsum = z['dsum'].sum(sumax)
        dins = z['dinsum'].sum(sumax); dcnt = z['dcnt'].sum(sumax); l35 = z['l35'].sum(sumax)
        expo = z['expo'].sum(sumax)[..., 0]
        nc = len(cl)
        return dict(rho=live[..., cl].sum(-1) / (nc * expo), births=birth[..., cl].sum(-1) / (nc * expo),
                    dn=dsum[..., cl].sum(-1) / dcnt[..., cl].sum(-1), dnin=dins[..., cl].sum(-1) / dcnt[..., cl].sum(-1),
                    l35c=l35[..., cl].sum(-1) / live[..., cl].sum(-1), l35=l35[..., cl].sum(-1) / (nc * expo))
    return per(1), per(0)


def ms(a):
    return a.mean(), a.std(ddof=1) / np.sqrt(len(a))


def facevar(z, A):
    ps = z['popsum'].sum(1); p2 = z['pop2'].sum(1); ex = z['expo'].sum(1)     # (blocks, F), (blocks, 1)
    mean = ps / ex; var = p2 / ex - mean ** 2
    return var.mean(1) / A


def report(tag, show=True):
    z = load(tag)
    name = str(z['name'])
    v = hl.vessel(name)
    cl = classes(v, name)
    rows = {}
    for lab, c in cl.items():
        blk, hal = stats(z, c)
        rows[lab] = dict(n=len(c), **{k: ms(a) for k, a in blk.items()}, half=hal['rho'])
    A = len(v.faces[0])
    rows['var'] = ms(facevar(z, A))
    if show:
        nb = z['live'].shape[0]
        print(f'== {tag}: {name}, A = {A}, {nb} blocks x {64 * int(z["W"])} replicas, burn {int(z["burn"])}, measured '
              f'{int(z["gens"])}; alive after burn {int(np.sum(z["alive_burn"]))}, at end {int(np.sum(z["alive_end"]))}; '
              f'wall {float(z["wall"]):.0f} s')
        print(f'   {"class":<20}{"cells":>6} {"rho":>20} {"half1-half2":>12} {"births":>18} {"dead: n":>18} {"dead: n in":>18} '
              f'{"live 3-5 / live":>18} {"live 3-5 / cell":>18}')
        for lab, r in rows.items():
            if lab == 'var':
                continue
            if lab[0] == 'k' and lab[1] > 0 and lab[2] == 'r':
                continue
            f = lambda t: f'{t[0]:.6f} ± {t[1]:.6f}'
            print(f'   {str(lab):<20}{r["n"]:>6} {f(r["rho"]):>20} {r["half"][0] - r["half"][1]:>+12.6f} {f(r["births"]):>18} '
                  f'{f(r["dn"]):>18} {f(r["dnin"]):>18} {f(r["l35c"]):>18} {f(r["l35"]):>18}')
        print(f'   face population Var / A = {rows["var"][0]:.5f} ± {rows["var"][1]:.5f}')
    return rows, v, z


if __name__ == '__main__':
    tags = sys.argv[1:]
    if tags == ['--all']:
        tags = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(SCR, '*_s*.npz')))
    for t in tags:
        report(t)
