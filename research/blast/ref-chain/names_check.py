#!/usr/bin/env python3
"""ref-chain: every name in statements_chain.json and AxiomsChain.lean resolves to exactly one Chain constant.

  (run ChainAxiomSweep.lean first; it writes chain_names.txt)   python3 research/blast/ref-chain/names_check.py
"""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
names = [l.strip() for l in open(os.path.join(H, 'chain_names.txt')) if l.strip()]
d = json.load(open(os.path.join(H, '..', 'lean', 'statements_chain.json')))
short = [r[0] for sec in d for r in sec['rows']]
ax = [l.split()[-1] for l in open(os.path.join(H, '..', 'lean', 'mathlib', 'AxiomsChain.lean')) if l.startswith('#print axioms')]
bad = 0
for label, lst in (('json', short), ('axioms', ax)):
    for s in lst:
        r = [n for n in names if n == s or n.endswith('.' + s)]
        if len(r) != 1:
            print(label, s, '->', r); bad += 1
print(f"rows {len(short)}, axiom lines {len(ax)}, unresolved or ambiguous: {bad}")
