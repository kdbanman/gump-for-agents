#!/usr/bin/env python3
"""Run plan of the review of research/shape3, fixed before any production run (seeds, lengths; no stopping rule:
every job is run once to its full length, nothing is added after looking at results).

    python3 research/audit/shape3/plan.py list
    nohup python3 research/audit/shape3/plan.py lane 0 > research/scratch/audit_shape3/lane0.log 2>&1 &
    nohup python3 research/audit/shape3/plan.py lane 1 > research/scratch/audit_shape3/lane1.log 2>&1 &

st.c, 512 replicas (WW = 8), renewal lives, soup 0.4, no cap, events every generation, Brent settled test (any
period).  Event files: research/scratch/audit_shape3/ev_a_k_b_sSEED.txt; settled lives with period not dividing 840
also dump their state to z_a_k_b_sSEED.txt.
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import validate as v  # noqa: E402

# (lane, tag, torus, gens, seed)
JOBS = [
    (0, 'Q36', (1, 4, 12), 2_000_000, 71001), (0, 'Q36', (1, 3, 12), 2_000_000, 71002),
    (0, 'Q36', (1, 4, 12), 2_000_000, 71003), (0, 'Q36', (1, 3, 12), 2_000_000, 71004),
    (0, 'Q45', (1, 5, 15), 5_000_000, 71005), (0, 'Q45', (1, 4, 15), 5_000_000, 71006),
    (0, 'Q45', (1, 5, 15), 5_000_000, 71007), (0, 'Q45', (1, 4, 15), 5_000_000, 71008),
    (0, 'P1', (2, 2, 8), 4_000_000, 71009), (0, 'P1', (1, 6, 16), 4_000_000, 71010),
    (1, 'T72', (2, 4, 12), 75_000_000, 71011),
    # added 00:31 after the four Q36 jobs, before any Q45 / P1 / T72 result: zombie counts per job were 7, 1 (1,4,12) and
    # 11, 0 (1,3,12); these diagnostic jobs measure the zombie rate at A = 36 only and are NOT used in any d.
    (0, 'Z36', (1, 3, 12), 2_000_000, 71101), (0, 'Z36', (1, 4, 12), 2_000_000, 71102),
    (0, 'Z36', (1, 3, 12), 2_000_000, 71103), (0, 'Z36', (1, 4, 12), 2_000_000, 71104),
]


def evpath(L, seed, pre='ev'):
    return os.path.join(v.OUT, f'{pre}_{L[0]}_{L[1]}_{L[2]}_s{seed}.txt')


def run(L, gens, seed):
    v.build()
    g = v.geomfile(L)
    ev = evpath(L, seed)
    out = subprocess.run(['nice', '-n', '5', v.BIN, g, str(seed), str(gens), ev + '.tmp', '-z', evpath(L, seed, 'z')],
                         capture_output=True, text=True, check=True).stdout
    os.replace(ev + '.tmp', ev)
    open(evpath(L, seed, 'sum'), 'w').write(out)
    print(L, seed, out.strip(), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'list':
        for j in JOBS:
            print(j, 'done' if os.path.exists(evpath(j[2], j[4])) else '')
    else:
        lane = int(sys.argv[2])
        for ln, tag, L, gens, seed in JOBS:
            if ln == lane and not os.path.exists(evpath(L, seed)):
                run(L, gens, seed)
        print('LANE DONE', lane, flush=True)
