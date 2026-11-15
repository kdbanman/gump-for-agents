#!/usr/bin/env python3
"""The faces behind the plate "What a short way round costs" (site/plates/wrap.*).   python3 site/collect/sources/scripts/wrap.py

Run from the repository root. Uses the lead's refit research/audit/wrap_haz_lead.py as it stands (its own loader,
load(), and its frozen parameters; nothing refitted here) and writes site/collect/sources/wrap.json:
  faces   every face of A >= 48 with shortest loop^2 >= 12 and at most one loop direction shorter than sqrt(21)
          (the faces of `python3 research/audit/wrap_haz_lead.py --single`): A, its short loop^2 (or none), ln tau_face,
          its error, the sources pooled
  line0   the weighted straight line through the faces with no short loop among them (computed here; CLAIMS WL2 says
          0.2086 +- 0.0001 per cell, which is asserted)
  frozen  LAW_FROZEN, LINES_FROZEN, POW_FROZEN, HAZ_FROZEN copied from the script
  tubes   per family (one short loop of 12, 13, 16, 19, or none from 63 cells up) its own weighted straight line, computed
          here as the script's --tube computes it (ln tau(72) and the slope, with errors; chi2); collect.py checks the
          slopes against research/wrap/PREDICTIONS.md
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join('research', 'audit'))
import wrap_haz_lead as W   # noqa

faces = [f for f in W.load() if len(f['loops']) <= 1]
assert len(faces) >= 39, len(faces)
z = [f for f in faces if not f['loops']]
assert len(z) == 14, len(z)
A = np.array([f['A'] for f in z], float) - 63; y = np.array([f['y'] for f in z]); w = np.array([f['se'] ** -2 for f in z])
X = np.vstack([np.ones_like(A), A]).T
cov = np.linalg.inv(X.T @ (X * w[:, None])); p = cov @ (X.T @ (w * y))
chi = float((((X @ p) - y) ** 2 * w).sum())
assert abs(p[1] - 0.2086) < 0.0002, p
out = {"src": "research/audit/wrap_haz_lead.py (the lead's refit, its loader and frozen forms; CLAIMS WL1-WL3)",
       "how": "python3 site/collect/sources/scripts/wrap.py (from the repository root; numpy, scipy)",
       "faces": [[f['A'], (f['loops'] or [None])[0], round(f['y'], 4), round(f['se'], 4), f['srcs']] for f in faces],
       "line0": {"a63": round(float(p[0]), 5), "c": round(float(p[1]), 5), "se_c": round(float(cov[1, 1] ** 0.5), 5),
                 "chi2": round(chi, 1), "n": len(z)},
       "frozen": {"LAW": W.LAW_FROZEN, "LINES": W.LINES_FROZEN, "POW": W.POW_FROZEN, "HAZ": W.HAZ_FROZEN}}
def wline(fs):
    A = np.array([f['A'] for f in fs], float) - 72; y = np.array([f['y'] for f in fs]); w = np.array([f['se'] ** -2 for f in fs])
    X = np.vstack([np.ones_like(A), A]).T
    cv = np.linalg.inv(X.T @ (X * w[:, None])); q = cv @ (X.T @ (w * y))
    return {"a72": round(float(q[0]), 5), "se_a72": round(float(cv[0, 0] ** .5), 5), "c": round(float(q[1]), 5), "se_c": round(float(cv[1, 1] ** .5), 5),
            "chi2": round(float((((X @ q) - y) ** 2 * w).sum()), 1), "n": len(fs), "A": [min(f['A'] for f in fs), max(f['A'] for f in fs)]}
out["tubes"] = {str(q or "none"): wline([f for f in faces if f['loops'] == ([] if q is None else [q]) and (q is not None or f['A'] >= 63)])
                for q in (None, 12, 13, 16, 19)}
dst = os.path.join('site', 'collect', 'sources', 'wrap.json')
open(dst, 'w').write(json.dumps(out, indent=0) + '\n')
print(dst, len(faces), 'faces; line through', len(z), 'faces with no short loop:', out['line0'])
