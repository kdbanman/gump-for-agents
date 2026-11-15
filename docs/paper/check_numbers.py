# Number check for the draft's update of 2026-11-15 (docs/paper/FACTCHECK.md, "Update of 2026-11-15").
# For every passage changed in that update, lists each number and reports whether it occurs as a token in the
# ledger rows (research/CLAIMS.md) and notebook entries (research/NOTEBOOK.md) the passage cites.
# A number not found there is reported as "draft" if it already occurs in the draft as committed before the update
# (a size or value the passage refers back to), otherwise as "UNSOURCED". Passages of the second update of
# 2026-11-15 (the symmetric collapse, the new clocks) compare with the draft as of bb22eda, the commit before it.
# Passages changed after the audit of 2026-11-15 compare with the draft as of e126a10.
# Run from the repo root: python3 docs/paper/check_numbers.py [--base REV] [--draft PATH]
# (default base 98a66d8, the commit before the update; under 1 s). Negative control: --draft on a copy with a number
# altered must report it UNSOURCED (see FACTCHECK.md).
# Signs are not compared (the source may write the difference the other way round); check those by eye.
import re, subprocess, sys

BASE = sys.argv[sys.argv.index('--base') + 1] if '--base' in sys.argv else '98a66d8'
DRAFT = sys.argv[sys.argv.index('--draft') + 1] if '--draft' in sys.argv else 'docs/paper/draft.md'
draft = open(DRAFT).read()
old = subprocess.run(['git', 'show', BASE + ':docs/paper/draft.md'], capture_output=True, text=True).stdout
claims = open('research/CLAIMS.md').read().split('\n')
nb = open('research/NOTEBOOK.md').read()

NB = {  # short name -> substring of the entry heading
    'second': 'the second variable at equal shortest loop',
    'zombie': 'lives that settle and are not recognised',
    'thin': 'the thinnest face: no derivation',
    'const': 'is there one asymptotic cost per cell',
    'addendum': 'the asymptotic constant: what the corrected analysis adds',
    'patches': 'empty patches on a face too large to die: the forecast missed',
    'forecast': 'a forecast before the run: empty patches',
    'symmetric': 'the symmetric collapse: pairing faces across an edge',
    'clocks': 'what the unrecognised settled states are',
    'audit': 'the audit of the rows nobody had re-run',
}

def nb_entry(key):
    h = NB[key]
    i = nb.index(h)
    i = nb.rindex('\n## ', 0, i)
    j = nb.find('\n## 2026', i + 5)
    return nb[i:j if j > 0 else None]

def row(cid):
    for l in claims:
        if l.startswith('| ' + cid + ' |'):
            return l
    raise KeyError(cid)

# (label, start marker, end marker or None for "to the next blank line", ledger ids, notebook entries)
SPEC = [
    ('Abstract: shape, constant, thin face', 'refuted, as were five candidate', "half a wide face's.",
     ['SH9', 'SH6', 'CN1', 'TH3'], ['second', 'const', 'thin']),
    ('Abstract: settled replicas', 'Settled replicas missed by the detectors', '(Section 12).', ['ZL1', 'ZL2'], ['zombie']),
    ('5.2 Table 2 note', '† These runs admit no bound', None, ['ZL2'], ['zombie']),
    ('5.5 Table 3 caption', 'no bound on settled replicas the GPU missed (ZL2, Section 12); the longer', '(*preliminary*, C).',
     ['ZL2'], ['zombie']),
    ('7.1 Table 6 caption', 'GPU missed (ZL2, Section 12); the run at A = 96', 'bound either (ZL2).', ['ZL2'], ['zombie']),
    ('6 thin-face bullet', '- *The thinnest periodic face* (TH4', None, ['TH4'], ['thin']),
    ('Table 5 row 15', '| 15 | Five candidate second variables', '\n', ['SH9'], ['second']),
    ('Table 5 row 16', '| 16 | Empty patches', '\n', ['GP10'], ['patches', 'forecast']),
    ('Table 5 row 17', '| 17 | The thin-face study', '\n', ['TH7'], ['thin']),
    ('Table 5 row 18', '| 18 | The constant analysis', '\n', ['CN2'], ['patches', 'second']),
    ('7.2 SH2', '**[measured]** (SH2; A: two codes)', None, ['SH2'], []),
    ('7.2 SH6, SH7', '**The difference does not persist', None, ['SH6', 'SH7'], ['second']),
    ('7.2 SH8, SH9', '**[proved]** (SH8; A)', None, ['SH8', 'SH9'], ['second']),
    ('7.2 reading', '**Reading** **[conjecture; not tested]**', None, [], ['second']),
    ('7.3 Table 8 caption', 'The loop² 3 entries are local', 'Section 7.4).', ['TH1'], ['thin']),
    ('7.4 TH1, TH2', 'The torus with periods (1,1) and (0,b)', None, ['TH1', 'TH2'], ['thin']),
    ('7.4 TH3', '**[measured: the fits]** (TH3; B)', None, ['TH3'], ['thin']),
    ('7.4 TH4-TH6', '**Why it is not derived.**', None, ['TH4', 'TH5', 'TH6'], ['thin']),
    ('7.5 CN1', '**[measured, model-free]** (CN1; A)', None, ['CN1'], ['const', 'addendum']),
    ('7.5 GP10', '**Empty patches** (GP10;', None, ['GP10'], ['patches', 'forecast']),
    ('10.3 items 2-3', '2. **The constant.**', '4. **Symmetric faces', ['CN1', 'TH3', 'SH6'], ['const', 'thin', 'second']),
    ('11 ranking item 1', 'isolated only to about', 'novelty', ['CN1', 'ZL2'], ['const', 'zombie']),
    ('11 shape paragraph', 'It would have moved up the list', None, [], []),
    ('12 threat to validity', '**Threat to validity: lives that settle', 'falling steeply with area.', ['ZL1', 'ZL2', 'Z13'], ['zombie', 'clocks']),
    # second update of 2026-11-15 (the symmetric collapse, S5-S9; the new clocks, Z12, Z13); base bb22eda
    ('Abstract: symmetric collapse', 'Symmetric initial conditions die exponentially sooner,', 'deficit. This', ['S6', 'S7'], ['symmetric'], 'bb22eda'),
    ('5.5 S2 qualification', 'slope is open. Two qualifications', '(below).', ['S2', 'S8'], ['symmetric'], 'bb22eda'),
    ('5.5 centring (S3, S9)', '- *Centre matters, but not', 'changing difference.', ['S3', 'S9'], ['symmetric'], 'bb22eda'),
    ('5.5 why: intro', '**Why symmetric faces die sooner', None, [], ['symmetric'], 'bb22eda'),
    ('5.5 S5', '**[proved]** (S5; A)', None, ['S5'], ['symmetric'], 'bb22eda'),
    ('5.5 Table 3a', '| symmetry imposed (octahedral vessel', None, ['S6'], ['symmetric'], 'bb22eda'),
    ('5.5 Table 3a caption', 'Table 3a. The edge ladder.', None, ['S6'], ['symmetric'], 'bb22eda'),
    ('5.5 S7', '**[measured]** (S7; B', None, ['S7'], ['symmetric'], 'bb22eda'),
    ('5.5 S8', '**[measured]** (S8; B', None, ['S8'], ['symmetric'], 'bb22eda'),
    ('5.5 what this corrects', '*What this corrects.*', None, ['P7'], ['symmetric'], 'bb22eda'),
    ('5.5 what remains preliminary', '*What remains preliminary.*', None, ['S5', 'S4', 'SW3'], [], 'bb22eda'),
    ('Table 5 row 19', '| 19 | The symmetric-collapse', '\n', ['S7'], ['symmetric'], 'bb22eda'),
    ('8 Z12', '**[proved, by stepping]** (Z12;', '14 of period 13).', ['Z12'], ['clocks'], 'bb22eda'),
    ('10.3 item 4', '4. **Symmetric faces:**', '5. **Infinite volume.**', ['S2', 'S7', 'S8', 'S9'], ['symmetric'], 'bb22eda'),
    ('11 table row, symmetry', 'Conceptually close to standard symmetry reduction', '\n', ['S5', 'S6'], ['symmetric'], 'bb22eda'),
    ('11 ranking item 3', '3. **Symmetry shortens lifetimes', '4. **The structure theorems', ['S6', 'S8', 'S4'], ['symmetric'], 'bb22eda'),
    # pass after the audit of 2026-11-15 (research/AUDIT-2026-11-15.md): released and narrowed markers; base e126a10
    ('3 T9 minimality', 'The minimality of the 36-cell two-layer set', 'it is not claimed.)', ['T9'], ['audit'], 'e126a10'),
    ('3 thickness (K1, K3)', 'theorem about sealed sets can, the role of thickness 3', 'periods 3 to 12.', ['K1', 'K3'], ['audit'], 'e126a10'),
    ('4 P4-P6', '**Correlations, damage and fronts.**', None, ['P4', 'P5', 'P6', 'P2'], ['audit'], 'e126a10'),
    ('5.1 F2', '**[measured]** (F2; B', '0.62, 0.47.', ['F2'], ['audit'], 'e126a10'),
    ('5.3 F10, F12', '**[measured]** (F10; B', None, ['F10', 'F12'], ['audit'], 'e126a10'),
    ('5.4 F11', '**[measured]** (F11; B', '0.356·N.', ['F11'], ['audit'], 'e126a10'),
    ('5.5 SW3', '**[measured]** (SW3;', 'replicas.', ['SW3'], ['audit'], 'e126a10'),
    ('5.6 L3', 'side-16 cube was lucky (*post hoc*', 'same data)', ['L3'], ['audit'], 'e126a10'),
    ('Table 5 row 14', '| 14 | The remnant', '\n', ['SW7'], ['audit'], 'e126a10'),
    ('Table 5 row 18 grade', '| 18 | The constant analysis', '\n', ['CN2'], ['audit'], 'e126a10'),
    ('6 X3', '(X3; B: the reviewer', None, ['X3'], ['audit'], 'e126a10'),
    ('8 Z2-Z4', '**[proved, exhaustive]** (Z2; B', 'union exactly 13.', ['Z2', 'Z3', 'Z4'], ['audit'], 'e126a10'),
    ('8 Z5', '**[measured]** (Z5; B', '48 and 66.', ['Z5'], ['audit'], 'e126a10'),
    ('8 Z10', '**[measured]** (Z10; B', 'heal).', ['Z10'], ['audit'], 'e126a10'),
    ('9 G2-G4, SW4', '**[proved]** (G2; B', 'intact edge.', ['G2', 'G3', 'G4', 'SW4'], ['audit'], 'e126a10'),
    ('10.1 enumerations', 'exhaustive enumerations of Section 8 at the sizes', 'union ≤ 10)', ['Z1', 'Z2', 'Z3', 'Z4'], ['audit'], 'e126a10'),
    ('10.1 preliminary enumerations', '*Preliminary* (exhaustive computer enumerations', None, ['Z2', 'Z3', 'Z4'], ['audit'], 'e126a10'),
    ('Appendix', 'Superseded and therefore absent', None, ['F7', 'S1', 'F9', 'GP4'], ['audit'], 'e126a10'),
]

SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻', '0123456789-')

def numbers(text):
    t = text.replace('−', '-')
    t = re.sub(r'10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)', lambda m: '10^' + m.group(1).translate(SUP), t)
    t = re.sub(r'`[^`]*`', ' ', t)                       # file names and commands
    t = re.sub(r'\b(Sections?|Table|Tables|row|rows|Figure)\s+[\d.,– and]+', ' ', t)  # cross-references
    t = re.sub(r'[A-Za-z_]+\d+[a-z]?', ' ', t)           # ids such as SH6, R43, s501, Q1, 46baf66
    out = []
    for m in re.finditer(r'10\^-?\d+|\d[\d,]*(?:\.\d+)?', t):
        x = m.group(0).rstrip(',').replace(',', '')
        out.append(x)
    return out

def tokens(text):
    return set(numbers(text))

flat = draft.replace('\n', ' ')  # same length as the draft; markers match across line breaks

def passage(label, start, end):
    i = flat.find(start)
    if i < 0:
        sys.exit('marker not found for ' + label + ': ' + start)
    if end is None:
        j = draft.find('\n\n', i)
    elif end == '\n':
        j = draft.find('\n', i)
    else:
        j = flat.find(end, i + len(start))
        if j < 0:
            sys.exit('end marker not found for ' + label)
        j += len(end)
    return draft[i:j]

old_tok = tokens(old)
olds = {}
total = bad = internal = 0
for label, start, end, ids, nbs, *base in SPEC:
    if base:
        if base[0] not in olds:
            olds[base[0]] = tokens(subprocess.run(['git', 'show', base[0] + ':docs/paper/draft.md'], capture_output=True, text=True).stdout)
        ot = olds[base[0]]
    else:
        ot = old_tok
    text = passage(label, start, end)
    src = ' '.join(row(c) for c in ids) + ' ' + ' '.join(nb_entry(k) for k in nbs)
    st = tokens(src)
    miss, draft_only = [], []
    nums = numbers(text)
    for x in dict.fromkeys(nums):
        total += 1
        if x in st:
            continue
        if x in ot:
            draft_only.append(x); internal += 1
        else:
            miss.append(x); bad += 1
    flag = 'OK ' if not miss else 'BAD'
    print(f'{flag} {label}: {len(set(nums))} numbers; cites {", ".join(ids + ["NB:" + k for k in nbs]) or "nothing"}')
    if draft_only:
        print('      in the earlier draft only:', ' '.join(draft_only))
    if miss:
        print('      UNSOURCED:', ' '.join(miss))
print(f'\n{total} distinct numbers per passage; {total - bad - internal} in the cited sources, '
      f'{internal} only in the earlier draft, {bad} unsourced')
sys.exit(1 if bad else 0)
