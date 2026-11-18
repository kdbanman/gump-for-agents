#!/usr/bin/env python3
"""A private copy of the pull request's nz.c that also prints, per replication, the ancestry of the final level:
every chain of the sampler keeps its initial state (the sampler never moves it), so every chain of the last ensemble
descends from one of the NBATCH x 512 fresh chains.  Appended to each REP line:
    anc_ens  distinct fresh chains the last ensemble (the chains at the level above 0, after the sweeps) descends from
    anc_hit  distinct fresh chains the chains with score 0 descend from;  lanes_hit: distinct lanes among those
    top_hit  share of the score-0 chains that descend from the commonest one;  n_hit: their number
The sampler itself is unchanged (same random numbers, same REP numbers; checked by run.sh).

    python3 research/audit/blastnoisy/patch_anc.py SRC/nz.c OUT/nz_anc.c
"""
import sys
s = open(sys.argv[1]).read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)


rep("*gmin2 = malloc(4 * NC);", "*gmin2 = malloc(4 * NC), *anc = malloc(4 * NC), *anc2 = malloc(4 * NC), *acnt = malloc(4 * NC);")
rep("int lam = LAM1, lev = 0; double prod = 1;", "for (long j = 0; j < NC; j++) anc[j] = (int)j;\n    int lam = LAM1, lev = 0; double prod = 1;")
rep("score2[j] = score[src]; gmin2[j] = gmin[src]; }", "score2[j] = score[src]; gmin2[j] = gmin[src]; anc2[j] = anc[src]; }")
rep("t2 = gmin; gmin = gmin2; gmin2 = t2; }", "t2 = gmin; gmin = gmin2; gmin2 = t2; t2 = anc; anc = anc2; anc2 = t2; }")
rep('rate[rep] = prod / TWIN; printf(" rate %.5e lntau %.4f\\n", rate[rep], rate[rep] > 0 ? -log(rate[rep]) : 99.0); fflush(stdout);',
    'rate[rep] = prod / TWIN; printf(" rate %.5e lntau %.4f", rate[rep], rate[rep] > 0 ? -log(rate[rep]) : 99.0);\n'
    '    { int de = 0, dh = 0, top = 0, nh = 0, dl = 0; memset(acnt, 0, 4 * NC);\n'
    '      for (long j = 0; j < NC; j++) { if (!acnt[anc[j]]) de++; acnt[anc[j]] = 1; }\n'
    '      memset(acnt, 0, 4 * NC);\n'
    '      if (lev > 1 && lam == 0) for (long j = 0; j < NC; j++) if (score[j] <= 0) { if (!acnt[anc[j]]) dh++; acnt[anc[j]]++; nh++; if (acnt[anc[j]] > top) top = acnt[anc[j]]; }\n'
    '      static char ls[NL]; memset(ls, 0, NL);\n'
    '      if (lev > 1 && lam == 0) for (long j = 0; j < NC; j++) if (score[j] <= 0 && !ls[anc[j] % NL]) { ls[anc[j] % NL] = 1; dl++; }\n'
    '      printf(" anc_ens %d anc_hit %d lanes_hit %d top_hit %.4f n_hit %d\\n", de, dh, dl, nh ? (double)top / nh : 0.0, nh); }\n'
    '    fflush(stdout);')
open(sys.argv[2], 'w').write(s)
