#!/usr/bin/env python3
"""Final cycle of every listed champion (up to 256 per vessel), added to data/vessels.jsonl as
`champion_end` = {"period P, population Q": count}. `champion_cycle_period` (from enum.c) is the FIRST champion's only.

  python3 research/statespace/champ_periods.py      (needs research/scratch/ss/NAME.nb and NAME.out from run.py)
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run as R


def ends(name, champs, T):
    fn = os.path.join(R.SCR, name + '.nb')
    out = subprocess.run([R.ENUM, fn, '--iterate', str(T + 300)], input=''.join(c + '\n' for c in champs),
                         capture_output=True, text=True, check=True).stdout.split('\n')
    res = {}
    for line in out[:len(champs)]:
        tr = [int(x, 16) for x in line.split()]
        s = tr[T]
        per = next(k for k in range(1, 301) if tr[T + k] == s)
        assert all(tr[T - 1 + k] != tr[T - 1] for k in range(1, per + 1)), 'transient shorter than claimed'
        key = f'period {per}, population {bin(s).count("1")}'
        res[key] = res.get(key, 0) + 1
    return res


def main():
    path = os.path.join(HERE, 'data', 'vessels.jsonl')
    rows = [json.loads(l) for l in open(path)]
    for r in rows:
        txt = open(os.path.join(R.SCR, r['name'] + '.out')).read()
        champs = R.parse(txt)['champions']          # up to 256 listed by enum.c
        r['champion_end'] = ends(r['name'], champs, r['max_transient'])
        r['champion_end_listed'] = len(champs)
    with open(path, 'w') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')
    for r in rows:
        if len(r['champion_end']) > 1 or r['N'] >= 27:
            print(r['name'], r['N'], r['n_champions'], r['champion_end'])


if __name__ == '__main__':
    main()
