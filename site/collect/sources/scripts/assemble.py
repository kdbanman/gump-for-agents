#!/usr/bin/env python3
"""Assemble series.json from part3d.json, part2d.json, part_lineage.json.   python3 <dir>/assemble.py <dir>"""
import json, sys
E = sys.argv[1]; X = "E=" + E + "; G=./engine/target/release/gump; mkdir -p $E/run61; "
p3 = json.load(open(f'{E}/part3d.json')); p2 = json.load(open(f'{E}/part2d.json')); pl = json.load(open(f'{E}/part_lineage.json'))
RUN = (X + "$G run --soup 0.4 --radius 11 --rng 61 --every 1 --kymo $E/run61/kymo.csv --events $E/run61/events.jsonl "
       "--poplog $E/run61/pop.txt --out /dev/null && $G run --soup 0.4 --radius 11 --rng 61 --gens 150000 "
       "--cells-out $E/run61/cells150000.txt && python3 $E/gump3d.py $E")
s = p3['soup_staircase']
s['how'] = RUN + "   (layer deaths identical to: $G ensemble --soup 0.4 --radius 11 --rng 61 --runs 1 --layer-deaths all)"
s['note'] = ("Seed chosen as the 2nd-longest of rng 1..64 at R=11 (lifetimes 29k-547k; repo median ~1.46e5, "
             "research/peeling/octa_first.csv), so 4 faces die slowly over 322k-403k and then the hull collapses in the "
             "last ~5k generations; pop is a min/max envelope per bucket, gen 0 = the seed. All 34 deaths are cause 'hull' (T2).")
f = p3['face_death_closeup']
f['how'] = RUN
f['note'] = ("The first three deaths of the run above (all original outer faces); pop[i] is the layer count at gen "
             "gens[0]+i, and the layer is 0 at death_gen. Area 63 for an untruncated face; 51 once a neighbouring face "
             "had died (the edge row is cut off). Not an ensemble: one run.")
k = p3['kagome_face']
k['how'] = RUN
k['note'] = ("Live flags cross-checked: 38 live = engine kymograph count and `gump show --gens 150000 --diag 0 --layer 11`; "
             "in-layer kagome bonds are distance sqrt2 (4 per site) plus sqrt8 across hexagons (2). The face is a triangle; "
             "gump show draws a wider window with extra dead sites outside the hull.")
p2['how'] = ("E=" + E + "; python3 $E/toy2d.py check && python3 $E/toy2d.py run 22 4 $E/part2d.json   "
             "(lifetime scan: python3 $E/toy2d.py scan 22 1 12 gave 18.9k-37.0k)")
p2['note'] = ("Own numpy stepper, checked bit-for-bit for 3000 gens against research/experiments/toy2d_check.py's step. "
              "Edges only move inward (confinement); the last state is a still life of 60 cells, so the box never empties.")
pl['how'] = "python3 " + E + "/lineage_hist.py " + E + "/part_lineage.json"
pl['note'] = ("Structured plateaus = lineage_check.py's 'structured' line (n=1238, mean 0.998); soups shown too. "
              "The 16 cube ratios come from cube_vs_ensemble.py and use a different tau (research/fluct/data/sym_residence.csv "
              "ensembles), not the soup-lineage tau; 'exp_expected' = Exp(1) counts for n=1238.")
out = {"_about": "Real runs of the gump engine (engine/target/release/gump, B45/S345) and repo data; generated 2026-11-14.",
       "soup_staircase": s, "face_death_closeup": f, "kagome_face": k, "toy2d_run": p2, "lineage_histogram": pl,
       "missing": []}
json.dump(out, open(f'{E}/series.json', 'w'), separators=(',', ':'))
