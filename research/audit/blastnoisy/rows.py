#!/usr/bin/env python3
"""Statistics of sampler rows (REP lines of the pull request's nz, or of this directory's nz_anc).

    python3 research/audit/blastnoisy/rows.py DIR_OR_FILES ... [--ref LNTAU ERR]

Groups the runs by their header (R, M, LAM1, DELTA, NSWEEP, KFLIP).  A run (one header line and its REP lines; a
file may hold several) shares 512 lanes among its replications.  Per group:
  K replications in F runs; ln tau = -ln(mean rate); its error (a) from the scatter of the replications, as the pull
  request does, (b) from the scatter of the run means (replications of a run are not independent if the lanes are
  remembered), with the ratio of the two variances; bootstrap 95% intervals of ln tau resampling replications and
  resampling runs; the shape of the distribution of rate / mean (quantiles, skewness, the largest shares, how many
  replications carry half the rate); the value in the first and second half of the files and by seed hundreds;
  ancestry columns when present (median and quartiles of anc_hit, top_hit).
With --ref, the difference from the reference is printed with the combined error.
"""
import glob, math, os, sys
import numpy as np

args = sys.argv[1:]
ref = None
if '--ref' in args:
    i = args.index('--ref'); ref = (float(args[i + 1]), float(args[i + 2])); del args[i:i + 3]
files = []
for a in args:
    files += sorted(glob.glob(os.path.join(a, '*.txt'))) if os.path.isdir(a) else sorted(glob.glob(a))
groups = {}
for f in files:
    key = None; rates = []; anc = []; seed = 0

    def flush():
        if key and rates:
            groups.setdefault(key, []).append((seed, np.array(rates), list(anc)))
    for line in open(f):
        if line.startswith('# sub'):                 # a header starts a run (files may hold several runs)
            flush(); rates = []; anc = []
            t = line.split(); d = dict(zip(t[2::2], t[3::2])); seed = int(d['seed'])
            key = tuple((k, d[k]) for k in ('R', 'A', 'M', 'eps', 'LAM1', 'DELTA', 'NSWEEP', 'KFLIP'))
        elif line.startswith('REP') and ' rate ' in line and key:
            rates.append(float(line.split(' rate ')[1].split()[0]))
            if ' anc_ens ' in line:
                t = line.split(' anc_ens ')[1].split()
                anc.append((int(t[0]), int(t[2]), int(t[4]), float(t[6]), int(t[8])))
    flush()
rng = np.random.default_rng(1)
for key in sorted(groups, key=lambda k: (int(dict(k)['R']), -float(dict(k)['eps']), int(dict(k)['DELTA']), int(dict(k)['NSWEEP']))):
    d = dict(key); runs = sorted(groups[key], key=lambda x: x[0])
    r = np.concatenate([x[1] for x in runs]); K = len(r); F = len(runs)
    m = r.mean(); est = -math.log(m); rel = r.std(ddof=1) / m; err = rel / math.sqrt(K)
    rm = np.array([x[1].mean() for x in runs]); nper = K / F
    err_run = rm.std(ddof=1) / math.sqrt(F) / rm.mean() if F > 1 else float('nan')
    vr = (err_run / err) ** 2 if F > 1 else float('nan')
    bs = np.sort([-math.log(rng.choice(r, K).mean()) for _ in range(4000)])
    if F > 1:
        idx = rng.integers(0, F, (4000, F))
        num = np.array([x[1].sum() for x in runs]); cnt = np.array([len(x[1]) for x in runs])
        bsr = np.sort(-np.log(num[idx].sum(1) / cnt[idx].sum(1)))
    x = r / m; srt = np.sort(x)[::-1]
    half = int(np.searchsorted(np.cumsum(srt), 0.5 * x.sum()) + 1)
    skew = ((x - 1) ** 3).mean() / x.std() ** 3
    q = np.quantile(x, [0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
    print(f"R {d['R']} ({d['A']} cells) eps {float(d['eps']):.5f} M {d['M']} LAM1 {d['LAM1']} DELTA {d['DELTA']} NSWEEP {d['NSWEEP']} KFLIP {d['KFLIP']}: "
          f"{K} replications in {F} runs")
    line = f"    ln tau {est:.4f} +- {err:.4f} (replications) / +- {err_run:.4f} (run means; variance ratio {vr:.2f})"
    if ref:
        line += f";  minus reference {est - ref[0]:+.4f} +- {math.hypot(err, ref[1]):.4f} / +- {math.hypot(err_run, ref[1]):.4f}"
    print(line)
    print(f"    bootstrap 95%: replications [{bs[100]:.3f}, {bs[3899]:.3f}]" + (f", runs [{bsr[100]:.3f}, {bsr[3899]:.3f}]" if F > 1 else ''))
    print(f"    rate / mean: sd {rel:.3f}, skewness {skew:.2f}, quantiles 5/25/50/75/95/99%: " + ' '.join(f'{v:.2f}' for v in q)
          + f", largest {srt[0]:.2f} {srt[1]:.2f} {srt[2]:.2f}, {half} carry half, zero-rate {int((r == 0).sum())};"
          f" median ln tau_k {np.median(-np.log(r[r > 0])):.3f}")
    if F >= 4:
        h = F // 2
        a = np.concatenate([x[1] for x in runs[:h]]); b = np.concatenate([x[1] for x in runs[h:]])
        ea = a.std(ddof=1) / a.mean() / math.sqrt(len(a)); eb = b.std(ddof=1) / b.mean() / math.sqrt(len(b))
        print(f"    first half of the files {-math.log(a.mean()):.4f} +- {ea:.4f}, second half {-math.log(b.mean()):.4f} +- {eb:.4f}", end='')
        hund = {}
        for s, rr, _ in runs:
            hund.setdefault(s // 100, []).append(rr)
        if len(hund) > 1:
            print(';  by seed hundred: ' + ', '.join(
                f"{k}xx: {-math.log(np.concatenate(v).mean()):.4f} +- {np.concatenate(v).std(ddof=1) / np.concatenate(v).mean() / math.sqrt(len(np.concatenate(v))):.4f} ({len(np.concatenate(v))})"
                for k, v in sorted(hund.items())), end='')
        print()
    anc = [a for x in runs for a in x[2]]
    if anc:
        an = np.array(anc, float)
        qa = lambda c: ' / '.join(f'{v:.0f}' for v in np.quantile(an[:, c], [0.25, 0.5, 0.75]))
        print(f"    ancestry of the last level (quartiles): last ensemble descends from {qa(0)} fresh chains; the score-0 chains from {qa(1)} "
              f"(lanes {qa(2)}); share of the commonest ancestor among them {np.quantile(an[:, 3], 0.25):.2f} / {np.median(an[:, 3]):.2f} / {np.quantile(an[:, 3], 0.75):.2f}; "
              f"replications with <= 2 ancestors: {int((an[:, 1] <= 2).sum())} of {len(an)}")
        # does the estimate depend on how many ancestors survive?
        lo = an[:, 1] <= np.median(an[:, 1])
        if len(an) == len(r) and lo.sum() and (~lo).sum():
            print(f"    mean rate / overall mean: replications with anc_hit <= median {r[lo].mean() / m:.3f} ({int(lo.sum())}), above {r[~lo].mean() / m:.3f} ({int((~lo).sum())})")
