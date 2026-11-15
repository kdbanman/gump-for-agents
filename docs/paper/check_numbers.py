# Number check for the draft's update of 2026-11-15 (docs/paper/FACTCHECK.md, "Update of 2026-11-15").
# For every passage changed in that update, lists each number and reports whether it occurs as a token in the
# ledger rows (research/CLAIMS.md) and notebook entries (research/NOTEBOOK.md) the passage cites.
# A number not found there is reported as "draft" if it already occurs in the draft as committed before the update
# (a size or value the passage refers back to), otherwise as "UNSOURCED". Passages of the second update of
# 2026-11-15 (the symmetric collapse, the new clocks) compare with the draft as of bb22eda, the commit before it.
# Passages changed after the audit of 2026-11-15 compare with the draft as of e126a10; those of the fourth update
# (how a face dies, the 4 x 5 patch rerun, the second card) with the draft as of 67e0371; those of the fifth (dying
# rounds 3-4, the wrapped faces on the second card, signals, the state space, bookkeeping) with a8e925a. A source
# 'file:PATH' is a tracked file cited directly.
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
    'dying1': 'how a face dies (the first look',
    'dying2': 'a death is a dip that keeps going',
    'patch45': 'the 4 × 5 empty patch, rerun on the CPU',
    'card': 'a second card (the GTX 1080',
    # fifth update (base a8e925a); keys carry the date so that they match the heading, not a mention in another entry
    'dying3': '2026-11-15: what the dips say about the price of a cell',
    'dying4': '2026-11-15: a depleted face thins as one thing',
    'dying4r': '2026-11-15: round 4 reviewed',
    'card93': '2026-11-15: the 93-cell torus lands below',
    'tori5': '2026-11-15: five wrapped faces on one driver',
    'tori5r': '2026-11-15: the five tori, reviewed',
    'sig1': '2026-11-15: gump carries signals',
    'sig1r': '2026-11-15: the first signals push reviewed',
    'sig2': '2026-11-15: a clock of every length',
    'sig2r': '2026-11-15: the second signals push reviewed',
    'ss': '2026-11-15: how much of its state space',
    'ssr': '2026-11-15: the state-space study reviewed',
}

def nb_entry(key):
    if key.startswith('file:'):  # a tracked file cited directly (a review, a README, a data report)
        return open(key[5:]).read()
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
    ('7.5 GP10', '**Empty patches** (GP10;', None, ['GP10'], ['patches', 'forecast', 'patch45']),  # patch45 added with the fourth update
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
    # fourth update of 2026-11-15 (how a face dies, DY1-DY7; the 4 x 5 patch rerun, GP10; the second card, GL1, GL2); base 67e0371
    ('Abstract: how a face dies', 'Looked at in', 'the end runs.', ['DY1', 'DY2', 'DY5'], ['dying1', 'dying2'], '67e0371'),
    ('5.5 S7 pointer', 'Section 5.6 looks at the dying faces', 'at all times).', ['S7', 'DY2'], ['dying1'], '67e0371'),
    ('5.6 intro', 'The edge ladder of Table 3a was explained', None, ['DY1'], ['dying1', 'dying2'], '67e0371'),
    ('5.6 DY1', '**The run-up.**', None, ['DY1', 'F12'], ['dying1'], '67e0371'),
    ('5.6 DY2', '**What a tie changes.**', None, ['DY2', 'S6'], ['dying1'], '67e0371'),
    ('5.6 DY3', '**The neighbour.**', None, ['DY3'], ['dying1'], '67e0371'),
    ('5.6 DY4', '**A death is a dip that keeps going.**', None, ['DY4', 'S6'], ['dying2'], '67e0371'),
    ('5.6 DY5', '**[measured]** (DY5; A', None, ['DY5'], ['dying2'], '67e0371'),
    ('5.6 DY6', '**[measured]** (DY6; A', None, ['DY6'], ['dying2'], '67e0371'),
    ('5.6 DY7', '**[measured]** (DY7; A)', None, ['DY7'], ['dying2'], '67e0371'),
    ('5.6 withdrawn', '*Readings withdrawn after the review.*', None, ['DY2', 'S6'], ['dying1', 'dying2'], '67e0371'),
    ('5.6 forecasts', '*Forecasts.* The lead', None, ['DY1'], ['dying1', 'dying2'], '67e0371'),
    ('Table 5 row 20', '| 20 | How a face dies, first', '\n', ['DY1'], ['dying1', 'file:research/dying/README.md'], '67e0371'),
    ('Table 5 row 21', '| 21 | How a face dies, second', '\n', ['DY4', 'DY7'], ['dying2'], '67e0371'),
    ('7.3 Table 8 footnote', '‡ The file', 'note of 2026-11-15).', ['SH3', 'GL1'], ['card', 'file:research/shape2/data/explore_report.txt'], '67e0371'),
    ('7.3 Table 8 row 48-60', '| d ln τ_face/dA, A = 48 → 60', '\n', ['SH3', 'GL1'], ['card', 'file:research/shape2/data/explore_report.txt'], '67e0371'),
    ('7.3 SH4', '**[measured]** (SH4; A', None, ['SH4', 'GL1'], ['card'], '67e0371'),
    # (7.5 equilateral note: passage removed in the fifth update; its content is now under 7.5 part C scored)
    ('12 second card', 'A second card (a different', 'repeated on it.', ['GL1'], ['card'], '67e0371'),
    ('12 guard', '**A guard, and its limit.**', None, ['GL2'], ['card'], '67e0371'),
    ('12 census errors', '**Errors of the census pipeline.**', None, ['GL1'], ['card'], '67e0371'),
    ('12 verification counts', '(142 claims', 'claims_tally.py`)', [], [], '67e0371'),
    # fifth update of 2026-11-15 (dying rounds 3-4, DY8-DY15; wrapped faces on the second card, GL3; signals, SG1-SG10;
    # state space, SS1-SS3; bookkeeping); base a8e925a
    ('5.6 intro grades', 'Every result of these two', 'own grades.', [], [], 'a8e925a'),
    ('5.6 DY5 tail', '**[measured]** (DY5; A', None, ['DY5'], ['dying2'], 'a8e925a'),
    ('5.6 round 3 intro', '**Round 3: the dips across sizes.**', None, ['DY8'], ['dying3'], 'a8e925a'),
    ('5.6 DY8', '**[measured]** (DY8;', None, ['DY8'], ['dying3'], 'a8e925a'),
    ('5.6 DY9', '**[measured]** (DY9;', None, ['DY9'], ['dying3'], 'a8e925a'),
    ('5.6 DY10', '**[measured]** (DY10;', None, ['DY10'], ['dying3'], 'a8e925a'),
    ('5.6 DY11', '**[measured]** (DY11;', None, ['DY11'], ['dying3'], 'a8e925a'),
    ('5.6 round 4 intro', '**Round 4: is a depleted face', None, ['DY13'], ['dying4', 'dying4r'], 'a8e925a'),
    ('5.6 DY13', '**[measured]** (DY13;', None, ['DY13'], ['dying4', 'dying4r'], 'a8e925a'),
    ('5.6 the null', '*What does not follow.*', None, ['DY13'], ['dying4r'], 'a8e925a'),
    ('5.6 DY14', '**[measured]** (DY14;', None, ['DY14'], ['dying4r'], 'a8e925a'),
    ('5.6 DY15', '**[measured]** (DY15;', None, ['DY15'], ['dying4', 'dying4r'], 'a8e925a'),
    ('5.6 what a caught face is', '*What a caught face is and is not.*', None, ['DY11', 'DY13'], ['dying3', 'dying4', 'dying4r'], 'a8e925a'),
    ('5.6 forecasts 3-4', '*Forecasts and what was not checked.* Round 3', None, [], ['dying3', 'dying4', 'dying4r'], 'a8e925a'),
    ('Table 5 row 18 pointer', '| 18 | The constant analysis', '\n', ['CN2'], [], 'a8e925a'),
    ('Table 5 row 22', '| 22 | How a face dies, third', '\n', ['DY8', 'DY10', 'DY11'], ['dying3'], 'a8e925a'),
    ('Table 5 row 23', '| 23 | How a face dies, fourth', '\n', ['DY13', 'DY14'], ['dying4', 'dying4r'], 'a8e925a'),
    ('Table 5 row 24', '| 24 | Equilateral face tori', '\n', ['GL3'], ['card93', 'tori5', 'file:research/constant/PREDICTIONS.md'], 'a8e925a'),
    ('Table 5 row 25', '| 25 | The lead', '\n', ['GL3'], ['card93', 'tori5', 'file:research/constant/PREDICTIONS.md'], 'a8e925a'),
    ('Table 5 row 26', '| 26 | The lead', '\n', ['SG1'], ['sig1', 'sig2', 'sig2r', 'file:research/signals/PREDICTIONS.md'], 'a8e925a'),
    ('Table 5 row 27', '| 27 | The lead', '\n', ['SS1'], ['ss'], 'a8e925a'),
    ('Table 5 caption', 'rounds 3 and 4 of the same file as scored', 'J1–J10', [], [], 'a8e925a'),
    ('7.1 pointer', 'decided** by these slabs', '(Section 7.5).', ['GL3'], [], 'a8e925a'),
    ('7.3 Table 8 stamping', 'The census stamps layer deaths', 'at most 0.0003.', ['SH3', 'GL3'], ['tori5r'], 'a8e925a'),
    ('7.5 CN1 note', 'Neither a capillary-wave law', None, ['CN1'], ['tori5'], 'a8e925a'),
    ('7.5 tori intro', '**Wrapped faces of constant shape', None, ['GL3'], [], 'a8e925a'),
    ('7.5 Table 8a', '| n | period lattice | A |', None, ['GL1', 'GL3', 'DY12'],
     ['card93', 'tori5', 'tori5r', 'file:research/constant/PREDICTIONS.md'], 'a8e925a'),
    ('7.5 Table 8a caption', 'Table 8a. Equilateral face tori', None, ['GL3'], ['card93', 'tori5r'], 'a8e925a'),
    ('7.5 line and kink', '**[measured]** (GL3; B for the line', None, ['GL3'], ['tori5', 'tori5r'], 'a8e925a'),
    ('7.5 against the hull', '**Against the hull family.**', None, ['DY9', 'CN1'], ['tori5', 'const'], 'a8e925a'),
    ('7.5 part C scored', '**The forecasts, scored**', None, ['GL3'],
     ['card93', 'tori5', 'file:research/constant/PREDICTIONS.md', 'file:research/audit/REVIEW-gpu-local-pr23.md'], 'a8e925a'),
    ('6.1 intro', '### 6.1 How much of its state space', None, [], ['ss', 'ssr'], 'a8e925a'),
    ('6.1 visited = settling', '**[proved]** An orbit of a deterministic', None, ['SS1'], ['ss'], 'a8e925a'),
    ('6.1 SS1', '**[proved by enumeration]** (SS1;', None, ['SS1'], ['ss', 'ssr'], 'a8e925a'),
    ('6.1 SS2', '**[proved, from single runs]** (SS2;', None, ['SS2'], ['ss', 'ssr'], 'a8e925a'),
    ('6.1 SS3', '**[measured]** (SS3;', None, ['SS3'], ['ss', 'ssr'], 'a8e925a'),
    ('6.1 bearing', '*Bearing on Section 6.*', None, ['X1'], ['ss', 'ssr'], 'a8e925a'),
    ('8 Z10 pointer', 'No object found in these censuses', 'constructs objects that do.', [], [], 'a8e925a'),
    ('8.1 intro', '### 8.1 Signals', None, ['SG1'], ['sig1', 'sig2'], 'a8e925a'),
    ('8.1 SG1', '**Pulses.** **[measured]** (SG1;', None, ['SG1'], ['sig1', 'sig1r'], 'a8e925a'),
    ('8.1 remarks', '*Two remarks* **[proved; no ledger row]**', None, [], ['sig1r', 'file:research/signals/README.md'], 'a8e925a'),
    ('8.1 SG2', '**A transmission, with a capacity.**', None, ['SG2'], ['sig1', 'sig1r'], 'a8e925a'),
    ('8.1 SG3', '**Interaction.** **[measured]** (SG3;', None, ['SG3'], ['sig1r'], 'a8e925a'),
    ('8.1 SG4', '**Bounds of the first search.**', None, ['SG4'], ['sig1', 'sig1r'], 'a8e925a'),
    ('8.1 Theorem 8', '**Theorem 8 (a clock of every length)', None, ['SG5'],
     ['sig2', 'sig2r', 'file:research/signals/README.md'], 'a8e925a'),
    ('8.1 SG6', '**A rake and a collision gate.**', None, ['SG6'], ['sig2', 'sig2r', 'file:research/signals/README.md'], 'a8e925a'),
    ('8.1 counter', '**A counter.** **[measured, oracle]**', None, ['SG7'], ['sig2', 'sig2r'], 'a8e925a'),
    ('8.1 Theorem 9', '**Theorem 9 (the tape)', None, ['SG7'], ['sig2', 'sig2r', 'file:research/signals/README.md'], 'a8e925a'),
    ('8.1 SG8', '**Where carriers come from.**', None, ['SG8'], ['sig2', 'sig2r'], 'a8e925a'),
    ('8.1 SG9', '**A wire against chaos.**', None, ['SG9', 'T3'], ['sig2', 'sig2r'], 'a8e925a'),
    ('8.1 SG10', '**Absent inside stated bounds.**', None, ['SG10'], ['sig2', 'sig2r'], 'a8e925a'),
    ('8.1 open', '**Open.** A corner between', None, [], ['sig2', 'sig2r'], 'a8e925a'),
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
