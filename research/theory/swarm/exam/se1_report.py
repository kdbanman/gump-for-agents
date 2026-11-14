"""S-E1 scoring from parity.c outputs (research/scratch/exam/se1_L*.txt)."""
import math, os
SCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'scratch', 'exam')
pred = {12: 6.4282, 14: 7.6056, 16: 8.6764}
for L in (12, 14, 16):
    d = {}
    for line in list(open(os.path.join(SCR, 'se1_L%d.txt' % L)))[1:]:
        k, *v = line.split(); d[k] = [float(x) for x in v]
    E, D = d['exposure'][0], d['deaths'][0]; lt = -math.log(D / E); e = 1 / math.sqrt(D)
    be, bd = d['bexp'], d['bdth']           # bins: 1 = ages 30-39, ..., 7 = 90-99, 8.. = 100-199
    e1, d1, e2, d2 = sum(be[1:8]), sum(bd[1:8]), sum(be[8:]), sum(bd[8:])
    h1, h2 = d1 / e1, d2 / e2; z = (h1 - h2) / math.sqrt(d1 / e1 ** 2 + d2 / e2 ** 2)
    o, od = d['one'][0], d['onedie'][0]; q = od / o; qe = math.sqrt(q * (1 - q) / o)
    print('L=%d deaths %d  ln tau %.4f +- %.4f (pred %.4f; diff %+.4f = %+.2f sigma) | hazard ages 30-99 %.4e, 100-199 %.4e (z %+.2f) | '
          'P(empty next | one cell) %.4f +- %.4f over %d visits (pred 0.2373, z %+.2f)'
          % (L, D, lt, e, pred[L], lt - pred[L], (lt - pred[L]) / e, h1, h2, z, q, qe, o, (q - 0.2373) / qe))
