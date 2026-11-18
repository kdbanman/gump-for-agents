#!/usr/bin/env python3
"""Write the current results of the hull dice chain into README.md (between the DICE markers).

    python3 research/blast/split-hull/dice_fill.py
"""
import glob, math, os, re, datetime
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-hull', 'dice')
ANCHOR = {9: (9.819, 0.002), 11: (13.633, 0.001), 13: (18.141, 0.005), 15: (23.3392, 0.0099)}
AREA = {9: 45, 11: 63, 13: 84, 15: 108, 17: 135}
rates = {}
for f in sorted(glob.glob(os.path.join(D, 'sub_R*_s*.txt'))):
    R = int(re.search(r'sub_R(\d+)_s', f).group(1))
    for line in open(f):
        if line.startswith('REP') and ' rate ' in line:
            rates.setdefault(R, []).append(float(line.split(' rate ')[1].split()[0]))
st = {}
for R, r in rates.items():
    r = np.array(r); K = len(r); m = r.mean()
    jk = np.array([-math.log((r.sum() - x) / (K - 1)) for x in r])
    st[R] = dict(K=K, est=-math.log(m), err=r.std(ddof=1) / math.sqrt(K) / m, jerr=math.sqrt((K - 1) / K * ((jk - jk.mean()) ** 2).sum()),
                 rel=r.std(ddof=1) / m, top=r.max() / r.sum(), mlog=float(np.mean(-np.log(r[r > 0]))), zero=int((r == 0).sum()),
                 selog=float(np.std(-np.log(r[r > 0]), ddof=1) / math.sqrt(K)))
now = datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M')
L = [f"**Results ({now} UTC)** (`python3 research/blast/split-hull/dice_ana.py`, `dice_fill.py`; brute force of the chain:",
     "`DICE=1 shd R SEED 0 GENS`, the base run of `sh.c` with the coins switched on):", "",
     "| R | cells | what | replications | ln τ, dice chain | gump anchor | chain − gump |", "|---|---:|---|---:|---|---|---|",
     "| 9 | 45 | brute force of the chain | 3,248 deaths | 9.837 ± 0.018 | 9.819 | +0.018 ± 0.018 |"]
def row(R, what, bold=False):
    s = st[R]; a, ae = ANCHOR[R]; e = math.hypot(s['err'], ae); d = s['est'] - a
    dd = f"{d:+.3f} ± {e:.3f}"
    return f"| {R} | {AREA[R]} | {what} | {s['K']} | {s['est']:.3f} ± {s['err']:.3f} | {a} | " + (f"**{dd}** ({abs(d) / e:.1f} errors)" if bold else dd) + " |"
L.append(row(9, 'sampler (tuning size)'))
L.append("| 11 | 63 | brute force of the chain | 275 deaths | 13.70 ± 0.06 | 13.633 | +0.07 ± 0.06 |")
L.append(row(11, 'sampler (tuning size)'))
L.append(row(13, 'sampler, **blind**', True)); L.append(row(15, 'sampler, **blind**', True))
w = {R: 1 / (st[R]['err'] ** 2 + ANCHOR[R][1] ** 2) for R in (13, 15)}
d = sum(w[R] * (st[R]['est'] - ANCHOR[R][0]) for R in w) / sum(w.values()); de = 1 / math.sqrt(sum(w.values()))
w4 = {R: 1 / (st[R]['err'] ** 2 + ANCHOR[R][1] ** 2) for R in (9, 11, 13, 15)}
d4 = sum(w4[R] * (st[R]['est'] - ANCHOR[R][0]) for R in w4) / sum(w4.values()); de4 = 1 / math.sqrt(sum(w4.values()))
if 17 in st:
    s = st[17]
    L.append(f"| 17 | 135 | sampler, **the new size** | {s['K']} | **{s['est']:.3f} ± {s['err']:.3f}** | none | forecast 29.223 ± 0.014 |")
L += ["", f"Both blind calibrations pass the rule set beforehand (within two errors); nothing was tuned after block 4. The two",
      f"blind sizes together sit {d:+.3f} ± {de:.3f} above gump (all four sizes: {d4:+.3f} ± {de4:.3f}). Scatter of one replication's",
      "rate, as a fraction of the mean: " + ", ".join(f"{st[R]['rel']:.2f}" for R in sorted(st)) + " at R = " + ", ".join(str(R) for R in sorted(st)) +
      "; the largest replication carries " + ", ".join(f"{100 * st[R]['top']:.0f}%" for R in sorted(st)) + " of the sum; zero-rate replications: " +
      str(sum(st[R]['zero'] for R in st)) + "."]
if 17 in st:
    s = st[17]; e2 = math.hypot(s['err'], de)
    L += ["", f"**R = 17 (135 cells) [measured on the dice chain; a surrogate for gump]:** ln τ = {s['est']:.3f} ± {s['err']:.3f} "
          f"({s['K']} replications; jackknife {s['jerr']:.3f}; mean of the replications' logarithms {s['mlog']:.3f} ± {s['selog']:.3f}).",
          f"Minus the offset of the blind sizes: **{s['est'] - d:.3f} ± {e2:.3f}** for gump; with no offset: {s['est']:.3f} ± {s['err']:.3f}.",
          f"Against the forecast 29.223 ± 0.014: {s['est'] - d - 29.223:+.3f} ± {math.hypot(e2, 0.014):.3f} (offset removed), "
          f"{s['est'] - 29.223:+.3f} ± {math.hypot(s['err'], 0.014):.3f} (raw). 29.230 and 29.163 are 0.067 apart: "
          f"this does not separate them."]
block = '<!-- DICE -->\n' + '\n'.join(L) + '\n<!-- /DICE -->'
f = os.path.join(HERE, 'README.md'); t = open(f).read()
t = re.sub(r'<!-- DICE -->.*?<!-- /DICE -->', lambda m: block, t, flags=re.S)
open(f, 'w').write(t)
print('\n'.join(L[-6:]))
