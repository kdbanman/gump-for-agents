#!/bin/bash
# Push 7 end-of-run driver: waits for the two open cube trees (5 x 5 C = 27; 3 x 3 period dividing 8, C = 35) and the
# long oracle checks, until every one is finished or the hard stop STOP (UTC) is reached; then stops this push's own
# processes (matched by their command lines: pool7.py / cdcl7.exe on these stems, verify7.py), decodes each list
# (complete or not: the union of the solutions found), runs census7 and summary7 on it, writes oracle records for it and
# checks them (rings <= 260 units), and writes everything to final7.txt.  Run from research/scratch/signals/p7:
#     bash ../../../signals/push7/finish7.sh "2026-11-18 06:30"
STOP=$(date -u -d "$1 UTC" +%s)
PY=/c/Users/kdbanman/.venvs/gump-gpu/Scripts/python.exe
S=../../../signals/push7
OUT=final7.txt
echo "finish7 started $(date -u)" > $OUT
alldone() { grep -q ALL fb27_5.pool.log && grep -q ALL fb35_3p8.pool.log && grep -q "ALL PASS\|SOME FAIL" verify_final_heavy.log; }
while [ $(date -u +%s) -lt $STOP ] && ! alldone; do sleep 120; done
echo "wait ended $(date -u)" >> $OUT
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { (\$_.Name -eq 'python.exe' -or \$_.Name -eq 'cdcl7.exe') -and (\$_.CommandLine -like '*pool7.py fb*' -or \$_.CommandLine -like '*cdcl7*fb27_5*' -or \$_.CommandLine -like '*cdcl7*fb35_3p8*' -or \$_.CommandLine -like '*verify7.py*') } | ForEach-Object { Stop-Process -Id \$_.ProcessId -Confirm:\$false -ErrorAction SilentlyContinue }" >> $OUT 2>&1
sleep 5
for st in fb27_5 fb35_3p8; do
  echo "=== $st: $(tail -n1 $st.pool.log)" >> $OUT
  $PY -c "
import json,os
st='$st'; t=json.load(open(st+'.cube/tree.json'))
leaves=[k for k,v in t.items() if v['children'] is None]
def done(k):
    f=st+'.cube/'+k+'.sols'
    if not os.path.exists(f): return False
    L=[l for l in open(f).read().split(chr(10)) if l]
    return bool(L) and L[-1].startswith('DONE')
d=[k for k in leaves if done(k)]
sols=set()
for k in t:
    f=st+'.cube/'+k+'.sols'
    if os.path.exists(f): sols|={l.strip() for l in open(f) if l.startswith('S ')}
open(st+'.final.sols','w').write(''.join(s+chr(10) for s in sorted(sols))+('DONE %d'%len(sols)+chr(10) if len(d)==len(leaves) else ''))
print(st, 'tree', len(t), 'cubes,', len(leaves), 'leaves,', len(d), 'leaves DONE,', len(sols), 'distinct solutions; COMPLETE' if len(d)==len(leaves) else '; NOT COMPLETE')
" >> $OUT 2>&1
  $PY $S/cnf7.py decode $st $st.final.sols >> $OUT 2>&1
  $PY -u $S/census7.py c_$st.json $st.list.json > c_$st.log 2>&1
  $PY $S/summary7.py c_$st.json >> $OUT 2>&1
  $PY $S/make7.py obj_$st.json c_$st.json --per 5 --seed 8 >> $OUT 2>&1
done
$PY -c "
import json
for f in ['obj_fb27_5.json','obj_fb35_3p8.json']:
    try: d=json.load(open(f))
    except Exception as e: print(f, e); continue
    for r in d['records']: r['name']=f[4:-5]+'-'+r['name']
    json.dump(d,open(f,'w'))
" >> $OUT 2>&1
$PY $S/merge7.py objects7_new.json obj_fb27_5.json obj_fb35_3p8.json >> $OUT 2>&1
$PY -u $S/verify7.py objects7_new.json --maxL 260 > verify_new.log 2>&1
echo "=== verify of the new records (rings <= 260): $(grep -c PASS verify_new.log) PASS, $(grep -c FAIL verify_new.log) FAIL" >> $OUT
echo "=== heavy verify of objects7.json: $(grep -c PASS verify_final_heavy.log) PASS, $(grep -c FAIL verify_final_heavy.log) FAIL; $(tail -n1 verify_final_heavy.log | cut -c1-60)" >> $OUT
grep -h FAIL verify_new.log verify_final_heavy.log | cut -c1-200 >> $OUT
echo "finish7 ended $(date -u)" >> $OUT
