#!/usr/bin/env python3
"""Analysis of the (4,0,4) reproduction.   python -u an.py OUTDIR RAWDIR [maxjobs]

Per seed there are two files from the same soups:
  OUTDIR/ch_4_0_4_sSEED.npz          research/shape/tslab.py run (unmodified rep.c, K = 16): the repository's pipeline
  RAWDIR/raw_4_0_4_sSEED_K1_cyc.npz  rep_cyc.exe at K = 1: per-generation last-alive times + any-period cycle detector
Rules compared on the same lives:
  A  repository rule on the repository's files (tslab.stats logic copied here to keep per-life ends).
  B  the same first-event logic at 1-generation resolution (face death or firewall formation, ties -> firewall,
     settle = min(840-multiple, last change against t-2)).
  C  the GPU rule: a life ends at the first generation an outer layer is empty; firewall life if a firewall exists in
     that state (fw time <= face time); a firewall alone does not end the life; settled: period 1/2 at lc2 + 1,
     other recognised periods (840-rule, or ladder period <= 128) at the recognition snapshot; else the cap.
  C2 = C with the exposure of firewalled lives cut at the firewall (isolates the continuation after a firewall).
"""
import glob, math, os, sys, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w
from analyze import death_times, ring_firewall, INF

OUTD, RAWD = sys.argv[1], sys.argv[2]
MAXJ = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9
BINS = [0, 60, 200, 1000, 3162, 10000, 16384]


def first_event(face, fw, st, ge):
    stop = np.where(st >= 0, st, ge).astype(float)
    fwm = fw.min(1)
    end = np.minimum.reduce([face, fwm, stop])
    kF = (face == end) & (face < fwm) & (face <= stop)
    kW = (fwm == end) & (fwm <= face) & (fwm <= stop)
    kS = (stop == end) & ~kF & ~kW & (st >= 0)
    return end, kF, kW, kS


def hazard(end, kF, label):
    print(f'  hazard of face deaths by age, rule {label} (death at generation T counted in lo < T <= hi; exposure of a life = min(T,hi) - min(T,lo)):')
    for lo, hi in zip(BINS[:-1], BINS[1:]):
        ex = (np.minimum(end, hi) - np.minimum(end, lo)).sum(); nF = int((kF & (end > lo) & (end <= hi)).sum())
        print(f'    {lo:6d}-{hi:6d}: F {nF:8d}  E {ex:.5g}  h = {nF / ex * 1e5:7.4f}e-5 +- {math.sqrt(nF) / ex * 1e5:.4f}e-5   ln(2E/F) = {math.log(2 * ex / nF):.4f} +- {1 / math.sqrt(nF):.4f}')


def line(label, end, kF, kW, kS):
    E = end.sum(); F = int(kF.sum())
    print(f'{label}: lives {len(end)}  E {E:.6g}  F {F}  W {int(kW.sum())}  settled {int(kS.sum())}  cap/other {len(end) - F - int(kW.sum()) - int(kS.sum())}  '
          f'F/E {F / E * 1e5:.4f}e-5   ln(2E/F) = {math.log(2 * E / F):.4f} +- {1 / math.sqrt(F):.4f}')
    return E, F


def c16(x):
    return -(-x // 16) * 16


seeds = sorted(int(f.rsplit('_s', 1)[1][:-4]) for f in glob.glob(os.path.join(OUTD, 'ch_4_0_4_s*.npz')))
seeds = [s for s in seeds if os.path.exists(os.path.join(RAWD, f'raw_4_0_4_s{s}_K1_cyc.npz'))][:MAXJ]
print(f'{len(seeds)} jobs, seeds {seeds[0]}..{seeds[-1]}  ({OUTD}, {RAWD})')
acc = collections.defaultdict(list); mism = 0; job = []
for s in seeds:
    o = np.load(os.path.join(OUTD, f'ch_4_0_4_s{s}.npz')); r = np.load(os.path.join(RAWD, f'raw_4_0_4_s{s}_K1_cyc.npz'))
    ge = int(o['gen_end']); assert ge == int(r['gen_end']) == 16384 and int(o['cap']) == 16384
    keys = [tuple(k) for k in r['keys'].tolist()]
    outer = [keys.index((0, 1)), keys.index((0, 15))]
    rings = [[i for i, k in enumerate(keys) if k[0] == d] for d in (1, 2, 3)]
    la1 = r['la'].astype(np.int64); st = r['st'].astype(np.int64); lc2 = r['lc2'].astype(np.int64)
    # K = 16 quantities derived from K = 1, exactly as tslab.run / geom.Vessel.run would compute them
    la16 = np.where(la1 < 0, -1, np.minimum(c16(la1), ge))
    D16 = death_times(la16, ge)
    face16 = np.minimum(D16[:, outer[0]], D16[:, outer[1]])
    fw16 = np.stack([ring_firewall(D16[:, c], ring=True) for c in rings], 1)
    st16 = np.where(st >= 0, np.minimum(st, np.minimum(c16(lc2), ge - 16)), -1)
    bad = int((face16 != o['face']).sum() + (fw16 != o['fw']).sum() + (st16 != o['settle']).sum())
    mism += bad
    # rule A on the repository's own file
    eA, fA, wA, sA = first_event(o['face'], o['fw'], o['settle'], ge)
    # rule B
    D1 = death_times(la1, ge)
    face1 = np.minimum(D1[:, outer[0]], D1[:, outer[1]])
    fw1 = np.stack([ring_firewall(D1[:, c], ring=True) for c in rings], 1)
    st1 = np.where(st >= 0, np.minimum(st, lc2), -1)
    eB, fB, wB, sB = first_event(face1, fw1, st1, ge)
    # rule C (GPU)
    fwm = fw1.min(1)
    cyc_at, cyc_p = r['extra'][:, 0].astype(np.int64), r['extra'][:, 1].astype(np.int64)
    stC = np.where(st >= 0, np.minimum(st, lc2 + 1), -1)
    stC = np.where((st < 0) & (cyc_p >= 1) & (cyc_p <= 128), cyc_at, stC)
    stopC = np.where(stC >= 0, stC, ge).astype(float)
    eC = np.minimum(face1, stopC)
    hasF = np.isfinite(face1) & (face1 <= stopC)
    fC = hasF & (fwm > face1); wC = hasF & (fwm <= face1); sC = ~hasF & (stC >= 0)
    eC2 = np.where(np.isfinite(fwm) & (fwm < eC), fwm, eC)
    # unrecognised cycles in rule A: no event, not settled by the 840 rule, but the ladder found a cycle
    noev = ~np.isfinite(face1) & ~np.isfinite(fwm)
    unrec = noev & (st < 0) & (cyc_p > 0)
    for k, v in dict(eA=eA, fA=fA, wA=wA, sA=sA, eB=eB, fB=fB, wB=wB, sB=sB, eC=eC, fC=fC, wC=wC, sC=sC, eC2=eC2, face1=face1, fwm=fwm,
                     unrec=unrec, cyc_at=cyc_at, cyc_p=cyc_p, st=st, noev=noev, face16=o['face'], fw16=o['fw'].min(1),
                     sfw=sC & np.isfinite(fwm)).items():
        acc[k].append(v)
    job.append((eA.sum(), int(fA.sum())))
Z = {k: np.concatenate(v) for k, v in acc.items()}
print(f'K=16 files against K=1 raw (face, fw x3, settle; derived as tslab.run does): {mism} mismatching entries over {len(Z["eA"])} lives')
print()
EA, FA = line('A  repository rule, K=16 files  ', Z['eA'], Z['fA'], Z['wA'], Z['sA'])
EB, FB = line('B  same logic per generation    ', Z['eB'], Z['fB'], Z['wB'], Z['sB'])
EC, FC = line('C  GPU rule                     ', Z['eC'], Z['fC'], Z['wC'], Z['sC'])
E2, F2 = line('C2 GPU rule, cut at the firewall', Z['eC2'], Z['fC'], Z['wC'], Z['sC'])
print(f'   C: settled on a firewalled state {int(Z["sfw"].sum())}; firewall lives W {int(Z["wC"].sum())}')
lt = lambda E, F: math.log(2 * E / F)
print(f'steps: A -> B {lt(EB, FB) - lt(EA, FA):+.5f} (dE {EB - EA:+.4g}, dF {FB - FA:+d});  '
      f'B -> C {lt(EC, FC) - lt(EB, FB):+.5f} (dE {EC - EB:+.4g}, dF {FC - FB:+d});  A -> C {lt(EC, FC) - lt(EA, FA):+.5f}')
t16 = np.isfinite(Z['face16']) & (Z['face16'] == Z['fw16'])
print(f'ties: face and firewall in the same 16-window (K=16, go to the firewall) {int(t16.sum())}; of these per generation: face first '
      f'{int((t16 & (Z["face1"] < Z["fwm"])).sum())}, firewall first {int((t16 & (Z["fwm"] < Z["face1"])).sum())}, same generation {int((t16 & (Z["fwm"] == Z["face1"])).sum())}')
fb = np.isfinite(Z['face1']) & (Z['fwm'] < Z['face1'])
print(f'firewall strictly before the face death, face death later within the run: {int(fb.sum())}; '
      f'mean wait {np.mean((Z["face1"] - Z["fwm"])[fb]):.0f} generations')
print()
hazard(Z['eA'], Z['fA'], 'A'); hazard(Z['eB'], Z['fB'], 'B'); hazard(Z['eC'], Z['fC'], 'C (GPU rule)')
print()
u = Z['unrec']
print(f'event-free lives not settled by the 840 rule but found in a cycle by the ladder detector: {int(u.sum())}; periods '
      f'{sorted(collections.Counter(Z["cyc_p"][u].tolist()).items())}; exposure counted after the detecting snapshot {int((16384 - Z["cyc_at"][u]).sum())} '
      f'({(16384 - Z["cyc_at"][u]).sum() / EA:.2e} of E)')
m = Z['cyc_p'] > 0
nd = m & (840 % np.maximum(Z['cyc_p'], 1) != 0)
print(f'all cycles seen by the ladder (any life, incl. after its event): {int(m.sum())}; periods not dividing 840: '
      f'{sorted(collections.Counter(Z["cyc_p"][nd].tolist()).items())}')
ev = Z['noev'] & m
print(f'event-free lives in a cycle (faces alive, no firewall): {int(ev.sum())}; periods {sorted(collections.Counter(Z["cyc_p"][ev].tolist()).items())}')
print(f'event-free lives at the cap not known to be in any cycle: {int((Z["noev"] & ~m & (Z["st"] < 0)).sum())}')
print()
Ej = np.array([j[0] for j in job]); Fj = np.array([j[1] for j in job]); lam = Fj.sum() / Ej.sum()
chi = ((Fj - lam * Ej) ** 2 / (lam * Ej)).sum()
lj = np.log(2 * Ej / Fj)
print(f'per job (rule A): chi2 of F_j against lam E_j = {chi:.1f} on {len(job) - 1}; ln tau per job: sd {lj.std(ddof=1):.4f} (Poisson {np.mean(1 / np.sqrt(Fj)):.4f}), min {lj.min():.4f}, max {lj.max():.4f}')
if len(job) >= 152:
    nblk = len(job) // 76
    bl = [math.log(2 * Ej[i * 76:(i + 1) * 76].sum() / Fj[i * 76:(i + 1) * 76].sum()) for i in range(nblk)]
    print('blocks of 76 jobs (the size of the repository row), rule A: ' + ' '.join(f'{x:.4f}' for x in bl) + f'   sd {np.std(bl, ddof=1):.4f}')
