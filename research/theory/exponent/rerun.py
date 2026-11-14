"""Re-runs made on 2026-11-14 while writing exponent.md: one headline number per section, same graphs and
parameters as jobs.py, fresh records under tag 'rerun' (research/scratch/exponent/runs_rerun.json).
Chunk lengths adapt to wall time, so a re-run is a new sample, not a bit-identical replay.
    python3 rerun.py model | gump | slab | noise | cross3 | gap SECONDS | all"""
import sys
import xp
from jobs import RHO_TOY, RHO_GUMP, CROSS3

def model():      # section 3: eight rows on dice, L = 16 (filed 7.432 +- 0.014)
    xp.run('w8_L16', xp.toy_model(8, 16), rho=[RHO_TOY, RHO_TOY], deaths=3000, maxsec=90, tag='rerun')

def gump():       # section 5: hull face model R = 9, w = 4 (filed 9.808 +- 0.010)
    xp.run('R9_w4', xp.gump_model(9, 4), rule=xp.GUMP, p=0.35, T0=200, rho=[RHO_GUMP, RHO_GUMP], deaths=3000,
           maxsec=120, tag='rerun')

def slab():       # section 5: deterministic periodic slab 4 x 4 x 12, A = 48 (filed 9.937 +- 0.016)
    xp.run('slab_4x4_m12', xp.gump_slab(4, 4, 12), rule=xp.GUMP, p=0.35, T0=300, deaths=2000, maxsec=300, tag='rerun')

def noise():      # section 9: L = 16, eps = 1e-3 (filed 7.398 +- 0.011)
    xp.run('L16_eps0.001', xp.toy_strip(16, 16), eps=1e-3, deaths=3000, maxsec=120, tag='rerun')

def cross3():     # section 10: range-3 cross, H = 24, L = 24 (filed 5.254 +- 0.011)
    g = xp.toy_strip(24, 24, offs=CROSS3, fw=4); g['name'] = 'cross3_strip_24x24'
    xp.run('c3_H24_L24', g, rule=xp.GUMP, p=0.4, T0=100, deaths=3000, maxsec=120, tag='rerun')

def gap(sec):     # section 4: empty windows on strips 16 x 128 (filed: data/gap.json, 600 s of sampling)
    xp.run('gap_H16_L128', xp.toy_strip(16, 128), deaths=10 ** 9, maxsec=sec, tag='rerun_gap', chunk=500)

if __name__ == '__main__':
    w = sys.argv[1]
    if w in ('model', 'all'): model()
    if w in ('gump', 'all'): gump()
    if w in ('slab', 'all'): slab()
    if w in ('noise', 'all'): noise()
    if w in ('cross3', 'all'): cross3()
    if w == 'gap': gap(float(sys.argv[2]))
