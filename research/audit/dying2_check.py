"""Recompute the headline numbers of research/dying2/README.md (wrapped faces and tubes) and research/dying2/hull/README.md
(rimmed hull faces) from their own tables in data/, and the dying face by lag before death (2026-11-18).

Only the committed tables are read (the death records themselves are in research/scratch and were not opened).
Numbers that need the records (plunge medians, X at t_h, the cut variants) are compared with the studies' own report
files, not recomputed. Arithmetic only; nothing is re-run; writes nothing.

    python3 research/audit/dying2_check.py
"""
import csv, math, os, re
import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
os.chdir(ROOT)
D = 'research/dying2/data'
H = 'research/dying2/hull/data'
OK = True
BAD = []


def rows(p):
    return list(csv.DictReader(open(p)))


def check(label, got, want, tol):
    global OK
    good = abs(got - want) <= tol
    OK &= good
    if not good:
        BAD.append(f'{label}: recomputed {got}, quoted {want}')
    return '' if good else f'   <-- MISMATCH {label}: quoted {want}'


def comb(*e):
    return math.sqrt(sum(x * x for x in e))


# ============================================================== wrapped faces
FACES = [('W63', '1_4_21', 63), ('E84', '2_4_14', 84), ('T84', '1_12_28', 84), ('T96', '1_17_32', 96)]
# README table values (research/dying2/README.md, "Numbers")
Q = {'W63': dict(deaths=8000, rec=31723, lag=[.052, .131, .323, .567, .776, .894, .977, .992], kstar=2.73, kP=.084,
                 q=[.860, .641, .447, .304, .201], lnnu=[-12.70, -11.54, -9.44], lev=[-1.95, -4.17, -6.83], tail=.424,
                 lt9=.178, lag1=1.69, ben=[.76, .55, .69], cut1=4, Xl2=(.398, .471), P4=(32.4, 31.6),
                 band=[(.91, .84), (1.96, 1.80), (3.38, 2.97), (4.08, 3.72)]),
     'E84': dict(deaths=2500, rec=19148, lag=[.038, .094, .229, .448, .719, .860, .969, .989], kstar=2.63, kP=.061,
                 q=[.853, .633, .422, .277, .179], lnnu=[-17.10, -15.84, -13.63], lev=[-2.01, -4.65, -8.66], tail=.446,
                 lt9=.185, lag1=1.66, ben=[.70, .58, .74], cut1=5, Xl2=(.381, .461), P4=(43.3, 40.9),
                 band=[(1.04, .96), (2.44, 2.33), (4.01, 3.49), (4.78, 4.34)]),
     'T84': dict(deaths=2500, rec=19628, lag=[.038, .090, .210, .421, .697, .845, .966, .996], kstar=2.59, kP=.060,
                 q=[.846, .623, .413, .274, .177], lnnu=[-16.88, -15.62, -13.33], lev=[-2.20, -4.44, -8.10], tail=.473,
                 lt9=.180, lag1=1.63, ben=[.70, .61, .77], cut1=6, Xl2=(.341, .460), P4=(42.1, 39.6),
                 band=[(1.76, 1.49), (4.13, 3.60), (6.53, 5.35), (7.61, 6.63)]),
     'T96': dict(deaths=2503, rec=33434, lag=[.034, .080, .181, .372, .645, .824, .961, .991], kstar=2.62, kP=.053,
                 q=[.855, .625, .422, .275, .176], lnnu=[-19.25, -17.98, -15.63], lev=[-2.16, -4.86, -8.89], tail=.484,
                 lt9=.183, lag1=1.68, ben=[.68, .64, .80], cut1=6, Xl2=(.335, .458), P4=(46.6, 43.2),
                 band=[(2.03, 1.66), (4.91, 4.25), (7.53, 6.13), (8.80, 7.57)])}
CARD = {'W63': (13.1622, 0.0007), 'E84': (17.5467, 0.0031), 'T84': (17.3175, 0.0031), 'T96': (19.7446, 0.0042)}
LAGQ = [1, 2, 3, 4, 6, 8, 12, 16]
W = {}
print('A. wrapped faces (research/dying2/data/)')
for nm, tag, A in FACES:
    rep = open(f'{D}/{tag}_report.txt').read()
    Pbar = float(re.search(r'Pbar = ([\d.]+)', rep).group(1)); sdP = float(re.search(r'sigma_P = ([\d.]+)', rep).group(1))
    lt = float(re.search(r'ln tau_face = ([\d.]+) \+- ([\d.]+)', rep).group(1))
    lte = float(re.search(r'ln tau_face = ([\d.]+) \+- ([\d.]+)', rep).group(2))
    nrec = int(re.search(r'(\d+) recovered dips', rep).group(1))
    ex = rows(f'{D}/{tag}_excursions.csv')
    k_ = np.array([int(x['k']) for x in ex]); reach = np.array([float(x['reach']) for x in ex])
    rec = np.array([float(x['recovered']) for x in ex]); dead = np.array([float(x['dead']) for x in ex])
    cen = np.array([float(x['censored']) for x in ex]); nu = np.array([float(x['nu_per_face_gen']) for x in ex])
    q = dead / (dead + rec)
    expo = reach[0] / nu[0]
    ident = max(abs(math.log(nu[i] * q[i] / (dead[0] / expo))) for i in range(1, A + 1))
    i = next(i for i in range(1, A + 1) if q[i - 1] >= 0.5 > q[i])
    kstar = i - 1 + (q[i - 1] - 0.5) / (q[i - 1] - q[i])
    lev = {p: int(math.ceil(p * Pbar)) - 1 for p in (0.9, 0.7, 0.5)}
    ks = np.arange(int(math.ceil(0.1 * Pbar)), int(0.45 * Pbar) + 1)
    tail = np.polyfit(ks, np.log(nu[ks]), 1)[0]
    lg = {int(x['lag']): x for x in rows(f'{D}/{tag}_lags.csv')}
    band = {int(x['lag']): x for x in rows(f'{D}/{tag}_band.csv')}
    ch = rows(f'{D}/{tag}_cutstart_hist.csv')
    cl = np.repeat([int(x['final_cut_start_lag']) for x in ch], [int(x['deaths']) for x in ch])
    cat = {int(x['k']): x for x in rows(f'{D}/{tag}_catches.csv')}
    tr = {(int(x['k']), int(x['dying'])): x for x in rows(f'{D}/{tag}_catch_traj.csv')}
    qq = Q[nm]
    W[nm] = dict(Pbar=Pbar, sdP=sdP, lt=lt, lte=lte, A=A, q=q, nu=nu, lev=lev, lg=lg, dead=dead[0], expo=expo)
    print(f'  {nm} ({tag}, A = {A}): Pbar {Pbar:.3f}, sigma_P {sdP:.3f}, ln tau {lt:.4f} +- {lte:.4f} (report); '
          f'minus the card\'s {CARD[nm][0]} {lt - CARD[nm][0]:+.4f} ({(lt - CARD[nm][0]) / comb(lte, CARD[nm][1]):+.1f})')
    kc = next((int(k_[j]) for j in range(len(cen)) if cen[j] > 0), None)
    print(f'    deaths {int(dead[0])}, censored excursions {int(cen[A])} (the first at minimum k = {kc}; none at k <= 3), recovered dips recorded {nrec}; '
          f'ln(face-gens at age > 512 / deaths) {math.log(expo / dead[0]):.4f}; '
          f'max |ln(nu q / death rate)| over k = 1..A {ident:.1e}'
          + check(f'{nm} deaths', int(dead[0]), qq['deaths'], 0) + check(f'{nm} rec', nrec, qq['rec'], 0))
    print(f'    q(1..5) ' + ' '.join(f'{q[k]:.3f}' for k in range(1, 6)) + f'; k* {kstar:.2f} = {kstar / Pbar:.3f} Pbar'
          + ''.join(check(f'{nm} q({k})', round(q[k], 3), qq['q'][k - 1], 0.0005) for k in range(1, 6))
          + check(f'{nm} k*', round(kstar, 2), qq['kstar'], 0.005) + check(f'{nm} k*/P', round(kstar / Pbar, 3), qq['kP'], 0.0005))
    print(f'    ln nu(<=k) at k = 2, 5, 10: ' + ' '.join(f'{math.log(nu[k]):.2f}' for k in (2, 5, 10))
          + f'; at 0.9, 0.7, 0.5 Pbar (k <= {lev[0.9]}, {lev[0.7]}, {lev[0.5]}): '
          + ' '.join(f'{math.log(nu[lev[p]]):.2f}' for p in (0.9, 0.7, 0.5))
          + f'; tail slope over k = {ks[0]}..{ks[-1]} {tail:.3f}; [ln nu(0.9) + ln tau]/A {(math.log(nu[lev[0.9]]) + lt) / A:.3f}'
          + ''.join(check(f'{nm} ln nu({k})', round(math.log(nu[k]), 2), v, 0.005) for k, v in zip((2, 5, 10), qq['lnnu']))
          + ''.join(check(f'{nm} ln nu({p})', round(math.log(nu[lev[p]]), 2), v, 0.005) for p, v in zip((0.9, 0.7, 0.5), qq['lev']))
          + check(f'{nm} tail', round(tail, 3), qq['tail'], 0.0005) + check(f'{nm} lt9', round((math.log(nu[lev[0.9]]) + lt) / A, 3), qq['lt9'], 0.0005))
    lags = [float(lg[l]['mean_P_over_Pbar']) for l in LAGQ]
    ben = [float(lg[l]['beneath_over_stationary']) for l in (4, 2, 0)]
    print(f'    P/Pbar at lags {LAGQ}: ' + ' '.join(f'{v:.3f}' for v in lags) + f'; live cells at lag 1 {lags[0] * Pbar:.2f}; '
          f'layer beneath at lag 4, 2, 0: ' + ' '.join(f'{v:.2f}' for v in ben)
          + ''.join(check(f'{nm} lag {l}', round(v, 3), w, 0.0006) for l, v, w in zip(LAGQ, lags, qq['lag']))
          + check(f'{nm} lag1 cells', round(lags[0] * Pbar, 2), qq['lag1'], 0.005)
          + ''.join(check(f'{nm} beneath', round(v, 2), w, 0.005) for v, w in zip(ben, qq['ben'])))
    bw = [(float(band[l]['band_width_cube_edges']), float(band[l]['band_width_null'])) for l in (8, 4, 2, 1)]
    xl2 = (float(band[2]['X']), float(band[2]['X_null_same_count']))
    print(f'    X at lag 2 / null {xl2[0]:.3f} / {xl2[1]:.3f}; empty band at lag 8, 4, 2, 1 (deaths / null): '
          + ', '.join(f'{a:.2f}/{b:.2f}' for a, b in bw) + f'; final 1-edge cut, median lag {np.median(cl):.0f} '
          f'(quartiles {np.quantile(cl, .25):.0f}-{np.quantile(cl, .75):.0f})'
          + check(f'{nm} X lag 2', round(xl2[0], 3), qq['Xl2'][0], 0.0005) + check(f'{nm} Xnull lag 2', round(xl2[1], 3), qq['Xl2'][1], 0.0005)
          + ''.join(check(f'{nm} band', round(a, 2), w[0], 0.005) + check(f'{nm} band null', round(b, 2), w[1], 0.005) for (a, b), w in zip(bw, qq['band']))
          + check(f'{nm} cut1', float(np.median(cl)), qq['cut1'], 0))
    kd = max(cat)
    dq = max(abs(float(cat[k]['q_catch']) - q[k]) for k in range(1, kd + 1))
    p4 = (float(tr[(4, 1)]['tau-4']), float(tr[(4, 0)]['tau-4']))
    print(f'    q from the catches against the online q, k = 1..{kd}: max difference {dq:.1e}; P at 4 generations before the '
          f'catch at k = 4, dying / recovered {p4[0]:.1f} / {p4[1]:.1f}; X at count = k (k = 2..5), dying / recovered / null: '
          + ', '.join(f'{float(cat[k]["X_dying_at_k"]):.2f}/{float(cat[k]["X_recovered_at_k"]):.2f}/{float(cat[k]["X_null_at_k"]):.2f}' for k in range(2, 6))
          + check(f'{nm} P4 dying', p4[0], qq['P4'][0], 0.051) + check(f'{nm} P4 rec', round(p4[1], 1), qq['P4'][1], 0.05)
          + check(f'{nm} q catch', dq, 0, 0.00006))

print('  comparisons quoted in the README:')
w, e, t, t9 = W['W63'], W['E84'], W['T84'], W['T96']
lnnu = lambda F, k: math.log(F['nu'][k])  # noqa: E731
print(f'    W63 -> E84: ln nu(<=2) {lnnu(e, 2) - lnnu(w, 2):+.2f}, q(2) {e["q"][2] - w["q"][2]:+.3f}, ln nu(0.9 Pbar) '
      f'{lnnu(e, e["lev"][0.9]) - lnnu(w, w["lev"][0.9]):+.2f}, ln tau {e["lt"] - w["lt"]:+.3f} ({(e["lt"] - w["lt"]) / 21:.4f} per cell)'
      + check('W63->E84 nu2', round(lnnu(w, 2) - lnnu(e, 2), 2), 4.40, 0.005) + check('W63->E84 q2', round(w['q'][2] - e['q'][2], 3), 0.008, 0.0005))
print(f'    T84 - E84: ln tau {t["lt"] - e["lt"]:+.3f}; ln nu(<=10) {lnnu(t, 10) - lnnu(e, 10):+.2f}, q(10) {t["q"][10]:.4f} / {e["q"][10]:.4f}; '
      f'at Pbar/2 (k <= {t["lev"][0.5]} / {e["lev"][0.5]}): ln nu {lnnu(t, t["lev"][0.5]) - lnnu(e, e["lev"][0.5]):+.2f}, '
      f'ln q {math.log(t["q"][t["lev"][0.5]] / e["q"][e["lev"][0.5]]):+.2f}'
      + check('T84-E84 nu10', round(lnnu(t, 10) - lnnu(e, 10), 2), 0.30, 0.005)
      + check('T84-E84 nu half', round(lnnu(t, t['lev'][0.5]) - lnnu(e, e['lev'][0.5]), 2), 0.56, 0.005)
      + check('T84-E84 q half', round(math.log(t['q'][t['lev'][0.5]] / e['q'][e['lev'][0.5]]), 2), -0.35, 0.005))
for k in range(1, 6):
    vals = [W[n]['q'][k] for n in W]
    se = [math.sqrt(W[n]['q'][k] * (1 - W[n]['q'][k]) / (W[n]['dead'] / W[n]['q'][k])) for n in W]
    print(f'    q({k}) over the four faces: {min(vals):.3f}-{max(vals):.3f} (spread {max(vals) - min(vals):.3f}; binomial errors '
          + ' '.join(f'{x:.3f}' for x in se) + ')')
print(f'    co-deaths 0 in {int(sum(W[n]["dead"] for n in W))} deaths (quoted 15,503)' + check('deaths total', int(sum(W[n]['dead'] for n in W)), 15503, 0))

# ============================================================== hull faces
print('\nB. hull faces (research/dying2/hull/data/)')
QH = {11: dict(A=63, lt=13.6429, Pbar=31.253, lag=[.998, .955, .676, .314, .114, .052], lag1=(1.62, 1, 1, 4),
               q=[.769, .499, .298, .180, .064, .0139], kstar=2.00, kP=.064, nu3=-12.43, nb=(.772, .960, .999),
               rows=(1.10, 1.01, .84, .79), corn=(.91, 1.17, 1.04, .92), dead=42489),
      13: dict(A=84, lt=18.151, Pbar=42.448, lag=[.999, .951, .611, .233, .081, .038], lag1=(1.61, 1, 1, 4),
               q=[.770, .496, .296, .176, .060, .0122], kstar=1.98, kP=.047, nu3=-16.93, nb=(.806, .970, .999),
               rows=(1.12, 1.06, .83, .79), corn=(.92, 1.22, 1.10, .92), dead=8891)}
HH = {}
for R, qq in QH.items():
    A = qq['A']
    out = open(f'{H}/R{R}_analyze_out.txt').read()
    Pbar = float(re.search(r'P bar = ([\d.]+)', out).group(1)); U = int(re.search(r'U = (\d+)', out).group(1))
    lt = float(re.search(r'ln\(8E/F\) = ([\d.]+) \+- ([\d.]+)', out).group(1))
    ex = {int(x['k']): x for x in rows(f'{H}/R{R}_excursions.csv')}
    qv = {k: float(ex[k]['q']) for k in ex}
    i = next(i for i in sorted(ex) if i > 0 and qv[i - 1] >= 0.5 > qv[i])
    kstar = i - 1 + (qv[i - 1] - 0.5) / (qv[i - 1] - qv[i])
    tc = {int(x['lag']): x for x in rows(f'{H}/R{R}_death_timecourse.csv')}
    # the positions table has unquoted commas inside its first field: rejoin the leading fields
    lines = [l.rstrip('\n').split(',') for l in open(f'{H}/R{R}_positions.csv')]
    hdr = lines[0]; nnum = len(hdr) - 1
    pos = {','.join(l[:len(l) - nnum]): dict(zip(hdr[1:], l[len(l) - nnum:])) for l in lines[1:]}
    cells = rows(f'{H}/R{R}_cells.csv')
    nrow0 = sum(1 for c in cells if c['row'] == '0')
    occ0 = sum(float(c['stationary_occupancy']) for c in cells if c['row'] == '0')
    occ = sum(float(c['stationary_occupancy']) for c in cells)
    HH[R] = dict(A=A, Pbar=Pbar, lt=lt, q=qv, tc=tc, U=U, ex=ex)
    print(f'  R = {R} (A = {A}, {len(cells)} cells): Pbar {Pbar:.3f}, U = {U}, ln tau {lt}; face cells in the rim row (shared with an '
          f'edge neighbour) {nrow0} of {len(cells)}, holding {occ0:.2f} of the {occ:.2f} live cells of the living face '
          f'({occ0 / occ:.3f})' + check(f'R{R} cells', len(cells), A, 0))
    print(f'    q at k = 1, 2, 3, 4, 6, 9: ' + ' '.join(f'{qv[k]:.4f}' for k in (1, 2, 3, 4, 6, 9)) + f' (errors '
          + ' '.join(f'{float(ex[k]["q_se"]):.4f}' for k in (1, 2, 3, 4, 6, 9)) + f'); k* {kstar:.2f} = {kstar / Pbar:.3f} Pbar; '
          f'ln nu(min <= 3) {math.log(float(ex[3]["nu_per_face_gen"])):.2f}; dead excursions {ex[0]["n_reaching"]}; '
          f'largest censored share at k <= 9 {max(float(ex[k]["censored_share"]) for k in range(10)):.4f}'
          + ''.join(check(f'R{R} q({k})', round(qv[k], 4 if k == 9 else 3), v, 0.00006 if k == 9 else 0.0005) for k, v in zip((1, 2, 3, 4, 6, 9), qq['q']))
          + check(f'R{R} k*', round(kstar, 2), qq['kstar'], 0.005) + check(f'R{R} k*/P', round(kstar / Pbar, 3), qq['kP'], 0.0005)
          + check(f'R{R} nu3', round(math.log(float(ex[3]['nu_per_face_gen'])), 2), qq['nu3'], 0.005)
          + check(f'R{R} dead', int(ex[0]['n_reaching']), qq['dead'], 0))
    lg = [float(tc[l]['mean_over_Pbar']) for l in (32, 16, 8, 4, 2, 1)]
    l1 = tc[1]
    nb = [float(tc[0][c]) for c in ('edge_nb_over_Pbar', 'vertex_nb_over_Pbar', 'opposite_over_Pbar')]
    print(f'    P/Pbar at lags 32, 16, 8, 4, 2, 1: ' + ' '.join(f'{v:.3f}' for v in lg)
          + f'; live cells at lag 1 mean {float(l1["mean"]):.2f} (5% {l1["q05"]}, median {l1["q50"]}, 95% {l1["q95"]}); '
          f'neighbours at death edge / vertex / opposite ' + ' / '.join(f'{v:.3f}' for v in nb)
          + ''.join(check(f'R{R} lag', round(v, 3), w_, 0.0006) for v, w_ in zip(lg, qq['lag']))
          + check(f'R{R} lag1', round(float(l1['mean']), 2), qq['lag1'][0], 0.005)
          + ''.join(check(f'R{R} nb', round(v, 3), w_, 0.0006) for v, w_ in zip(nb, qq['nb'])))
    p = pos['dying, lag 1']
    rr = [float(p[c]) for c in ('row0_rel', 'row1_rel', 'row2_rel', 'row3p_rel')]
    cc = [float(p[c]) for c in ('corner_lt1_rel', 'corner_1_2_rel', 'corner_2_3_rel', 'corner_ge3_rel')]
    p3 = pos['dying, first P<=3, P==3 there']
    print(f'    last cells (lag 1) over stationary share, rows 0, 1, 2, >= 3: ' + ' '.join(f'{v:.2f}' for v in rr)
          + '; by corner distance: ' + ' '.join(f'{v:.2f}' for v in cc)
          + f'; rim row at the first passage to 3 cells {float(p3["row0_rel"]):.2f}; stationary share of the rim row '
          f'{float(pos["stationary_share"]["row0_rel"]):.3f}'
          + ''.join(check(f'R{R} rows', round(v, 2), w_, 0.005) for v, w_ in zip(rr, qq['rows']))
          + ''.join(check(f'R{R} corner', round(v, 2), w_, 0.005) for v, w_ in zip(cc, qq['corn'])))
    cq = rows(f'{H}/R{R}_condq.csv')
    for k in (4, 6):
        r_ = [x for x in cq if x['k'] == str(k) and x['class'].startswith('rim-row')]
        print(f'    q at first passage to exactly {k}, by cells on the rim row: '
              + ', '.join(f'{x["value"]}: {float(x["q"]):.3f}' for x in r_))
    sp = [x for x in cq if x['k'] == '3' and 'spread' in x['class']]
    print('    k = 3 by spread: ' + ', '.join(f'{x["class"]} {x["value"]}: {float(x["q"]):.3f}' for x in sp))
    ed = {(int(x['k']), int(x['dies'])): x for x in rows(f'{H}/R{R}_equal_depth.csv')}
    if R == 11:
        print('    equal depth k = 3: P at -8, -4, -2 dying / recovered: '
              + ', '.join(f'{float(ed[(3, 1)][c]):.1f} / {float(ed[(3, 0)][c]):.1f}' for c in ('P_at_-8', 'P_at_-4', 'P_at_-2'))
              + f'; descent median dying / recovered {ed[(3, 1)]["descent_median"]} / {ed[(3, 0)]["descent_median"]}')
        OK &= abs(float(ed[(3, 1)]['P_at_-8']) - 27.5) < 0.05 and abs(float(ed[(3, 0)]['P_at_-8']) - 27.6) < 0.05
        OK &= abs(float(ed[(3, 1)]['P_at_-4']) - 19.4) < 0.05 and abs(float(ed[(3, 0)]['P_at_-4']) - 18.8) < 0.05
        OK &= abs(float(ed[(3, 1)]['P_at_-2']) - 10.7) < 0.05 and abs(float(ed[(3, 0)]['P_at_-2']) - 9.5) < 0.05
h11, h13 = HH[11], HH[13]
z6 = (h11['q'][6] - h13['q'][6]) / comb(float(h11['ex'][6]['q_se']), float(h13['ex'][6]['q_se']))
print(f'  ln tau 84 - 63: {h13["lt"] - h11["lt"]:.3f}; ln(q(9) at 63 / at 84) {math.log(h11["q"][9] / h13["q"][9]):.3f}; '
      f'q(6) 63 - 84 {h11["q"][6] - h13["q"][6]:+.4f} ({z6:.1f} sigma)'
      + check('hull 4.51', round(h13['lt'] - h11['lt'], 2), 4.51, 0.005) + check('hull 0.13', round(math.log(h11['q'][9] / h13['q'][9]), 2), 0.13, 0.005))

# ============================================================== the unreconciled q
print('\nC. q(k) for k = 1, 2, 3: wrapped (min <= k, recovery at P >= Pbar) against hull (min <= k, recovery at P >= U)')
for nm in ('W63', 'E84', 'T84', 'T96'):
    F = W[nm]
    print(f'  {nm}: ' + ' '.join(f'{F["q"][k]:.3f}' for k in (1, 2, 3)) + f'  (recovery threshold P >= {math.ceil(F["Pbar"])}, Pbar {F["Pbar"]:.2f})')
for R in (11, 13):
    print(f'  hull R = {R}: ' + ' '.join(f'{HH[R]["q"][k]:.3f}' for k in (1, 2, 3)) + f'  (recovery threshold P >= {HH[R]["U"]}, Pbar {HH[R]["Pbar"]:.2f})')
for k in (1, 2, 3):
    a, b = W['W63']['q'][k], HH[11]['q'][k]
    sa = math.sqrt(a * (1 - a) / (W['W63']['dead'] / a)); sb = float(HH[11]['ex'][k]['q_se'])
    print(f'  A = 63, k = {k}: W63 - hull {a - b:+.3f} +- {comb(sa, sb):.3f} ({(a - b) / comb(sa, sb):.0f} sigma)')

# ============================================================== population by lag before death
print('\nD. the dying face by lag before death: mean, median and upper quantiles, as P/Pbar and as P/A')
print('   (wrapped tables give q75 and q90 at lags 1, 2, 3, 4, 6, 8, 12; hull tables give q75 and q95 at 1-6, 8, 10, 12)')
for nm, tag, A in FACES:
    F = W[nm]; lg = F['lg']; Pb = F['Pbar']
    live = [l for l in lg if l >= 64]
    ref = {c: np.mean([float(lg[l][c]) for l in live]) for c in ('mean_P_over_Pbar', 'q50', 'q75', 'q90')}
    print(f'  {nm} (A = {A}, Pbar {Pb:.2f} = {Pb / A:.3f} of the face, sigma_P {F["sdP"] / Pb:.3f} Pbar); living reference '
          f'(lags 64-3583, averaged): mean {ref["mean_P_over_Pbar"]:.3f}, median {ref["q50"]:.3f}, q75 {ref["q75"]:.3f}, q90 {ref["q90"]:.3f} Pbar'
          f' (q90 = {ref["q90"] * Pb:.1f} cells = {ref["q90"] * Pb / A:.3f} of the face)')
    for l in (1, 2, 3, 4, 6, 8, 12):
        x = lg[l]
        v = [float(x[c]) for c in ('mean_P_over_Pbar', 'q50', 'q75', 'q90')]
        print(f'    lag {l:2d}: /Pbar mean {v[0]:.3f} median {v[1]:.3f} q75 {v[2]:.3f} q90 {v[3]:.3f} | /A '
              + ' '.join(f'{u * Pb / A:.3f}' for u in v) + f' | q90 in cells {v[3] * Pb:.0f}; q90 minus living q90 '
              f'{v[3] - ref["q90"]:+.3f} Pbar; q90 is {(v[3] - 1) * Pb / F["sdP"]:+.1f} sigma_P from Pbar')
    OK &= float(lg[4]['q90']) > ref['q90'] + 0.2
for R in (11, 13):
    F = HH[R]; tc = F['tc']; Pb = F['Pbar']; A = F['A']
    live = [l for l in tc if l >= 32]
    ref = {c: np.mean([float(tc[l][c]) for l in live]) for c in ('mean', 'q50', 'q75', 'q95')}
    print(f'  hull R = {R} (A = {A}, Pbar {Pb:.2f} = {Pb / A:.3f} of the face); living reference (lags 32-4000, averaged): '
          f'mean {ref["mean"] / Pb:.3f}, median {ref["q50"] / Pb:.3f}, q75 {ref["q75"] / Pb:.3f}, q95 {ref["q95"] / Pb:.3f} Pbar'
          f' (q95 = {ref["q95"]:.1f} cells = {ref["q95"] / A:.3f} of the face)')
    mx = 0
    for l in (1, 2, 3, 4, 5, 6, 8, 10, 12):
        x = tc[l]
        v = [float(x[c]) for c in ('mean', 'q50', 'q75', 'q95')]
        mx = max(mx, v[3])
        print(f'    lag {l:2d}: /Pbar mean {v[0] / Pb:.3f} median {v[1] / Pb:.3f} q75 {v[2] / Pb:.3f} q95 {v[3] / Pb:.3f} | /A '
              + ' '.join(f'{u / A:.3f}' for u in v) + f' | q95 minus living q95 {(v[3] - ref["q95"]) / Pb:+.3f} Pbar')
    OK &= mx <= ref['q95']
    print(f'    largest q95 at lags 1-12: {mx:.0f} cells, living q95 {ref["q95"]:.1f}')

# ============================================================== statements that do not follow as worded
print('\nE. checks of wording')


def qse(F, k):
    q = F['q'][k]; n = F['dead'] / q
    return math.sqrt(q * (1 - q) / n)


for k in (3, 4, 5):
    d_ = W['W63']['q'][k] - W['E84']['q'][k]
    print(f'  q({k}) W63 - E84 {d_:+.3f} +- {comb(qse(W["W63"], k), qse(W["E84"], k)):.3f} ({d_ / comb(qse(W["W63"], k), qse(W["E84"], k)):.1f} sigma)')
for k in (1, 2, 3, 5, 10):
    d_ = math.log(W['T84']['q'][k] / W['E84']['q'][k]); de_ = comb(qse(W['T84'], k) / W['T84']['q'][k], qse(W['E84'], k) / W['E84']['q'][k])
    print(f'  ln q({k}) T84 - E84 {d_:+.3f} +- {de_:.3f} ({d_ / de_:.1f} sigma); ln nu(<={k}) T84 - E84 '
          f'{math.log(W["T84"]["nu"][k] / W["E84"]["nu"][k]):+.3f}')
for R in (11, 13):
    txt = open(f'{H}/R{R}_analyze_out.txt').read()
    m_ = re.search(r'plunge \(last generation with P >= Pbar/2 -> first empty\):\s+([\d.]+)\s+[\d.]+\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', txt)
    print(f'  hull R = {R} plunge "last P >= Pbar/2 to first empty": mean {m_.group(1)}, quartiles {m_.group(2)}-{m_.group(4)}, median '
          f'{m_.group(3)}; on the wrapped / round-1 definition t_d - t_h (one generation less): median {float(m_.group(3)) - 1:.0f}, '
          f'mean {float(m_.group(1)) - 1:.2f}')
for nm, tag, A in FACES:
    txt = open(f'{D}/{tag}_report.txt').read()
    m_ = re.search(r'plunge t_d - t_h: median ([\d.]+), quartiles (\d+)-(\d+), mean ([\d.]+)', txt)
    print(f'  {nm} plunge t_d - t_h (report): median {m_.group(1)}, quartiles {m_.group(2)}-{m_.group(3)}, mean {m_.group(4)}')
vl = open(f'{H}/validate.log').read()
print(f'  hull validate.log: {vl.count("VALIDATE OK")} "VALIDATE OK" lines, {vl.count("all equal")} "all equal" lines; '
      f'no validation log is kept for the wrapped recorder dy.c (data/ holds none)')

if BAD:
    print('\nmismatches: ' + '; '.join(BAD))
print('\nPASS' if OK else '\nFAIL')
