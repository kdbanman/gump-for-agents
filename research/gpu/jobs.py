#!/usr/bin/env python3
"""Long Modal runs that survive the local process: spawn on the deployed app, collect later by call id.

`modal run` ties a run to the local client: if the client dies (a restarted session), the app stops and the result is
lost. Instead:

  modal deploy research/gpu/modal_app.py                                  # once (idle deployments cost nothing)
  python3 research/gpu/jobs.py spawn facelaw '{"R": 43, "minutes": 180, "seed": 501, "centre": "c", "sym": true, "WB": 1, "pw": 1024}'
  python3 research/gpu/jobs.py status
  python3 research/gpu/jobs.py collect                                   # saves finished results like the entry points

Call ids and arguments are kept in research/scratch/gpu/jobs.json.
"""
import json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
DB = os.path.join(ROOT, 'research', 'scratch', 'gpu', 'jobs.json')
APP = 'gump-gpu'


def load():
    return json.load(open(DB)) if os.path.exists(DB) else []


def save(jobs):
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    json.dump(jobs, open(DB + '.new', 'w'), indent=1)
    os.replace(DB + '.new', DB)


def out_path(job, res):
    a = job['args']
    if job['fn'] == 'facelaw':
        tag = f"slab{a['slab']}" if a.get('slab') else f"{'sym' + a.get('centre', 'c') if a.get('sym') else ''}R{a['R']}"
        return os.path.join(ROOT, 'research', 'data', 'gpu_facelaw', f"{tag}_s{a['seed']}_A10G.json")
    raise ValueError(job['fn'])


def spawn(fn, args):
    import modal
    f = modal.Function.from_name(APP, f'{fn}_remote')
    call = f.spawn(**args)
    jobs = load()
    jobs.append(dict(fn=fn, args=args, call=call.object_id, spawned=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), done=False))
    save(jobs)
    print('spawned', fn, args, call.object_id)


def collect(wait=False):
    import modal
    jobs = load()
    for j in jobs:
        if j['done']:
            continue
        try:
            res = modal.FunctionCall.from_id(j['call']).get(timeout=None if wait else 0)
        except TimeoutError:
            print('running ', j['fn'], j['args'], j['call']); continue
        except Exception as e:  # noqa: BLE001 - report and keep going
            print('FAILED  ', j['fn'], j['args'], j['call'], repr(e)[:200]); j['done'] = 'failed'; continue
        p = out_path(j, res)
        with open(p, 'w') as fh:
            json.dump(dict(res, gpu='A10G'), fh)
        j['done'] = True; j['saved'] = p
        print('saved   ', p)
    save(jobs)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'spawn':
        spawn(sys.argv[2], json.loads(sys.argv[3]))
    elif cmd == 'collect':
        collect(wait='--wait' in sys.argv)
    elif cmd == 'status':
        for j in load():
            print(j['done'], j['fn'], j['args'], j['call'], j['spawned'])
