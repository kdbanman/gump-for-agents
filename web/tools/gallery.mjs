// Builds data/gallery.json, the app's atlas gallery, from research/atlas/catalogue.jsonl.
//   node tools/gallery.mjs [path/to/catalogue.jsonl]
// Selection is by rules (smallest, most common, special periods, vertex-star membership) plus a
// short list of named objects; cell lists always come from the catalogue. Every object is
// re-stepped here with src/cpu.js in a box that holds its hull forever (T2, so the box is exact)
// and its period and per-phase populations must match the catalogue, or the build fails.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { stepCPU, DIAGONALS } from '../src/cpu.js';
import { autoBox, placeSeed } from '../src/seeds.js';

const WEB = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CAT = process.argv[2] || path.join(WEB, '../research/atlas/catalogue.jsonl');
const all = fs.readFileSync(CAT, 'utf8').trim().split('\n').map(l => JSON.parse(l));
const byId = new Map(all.map(o => [o.id, o]));
// objects of research/clockwork (not in the catalogue): looked up by id in the two jsonl files
const CLOCK = path.join(WEB, '../research/clockwork/objects');
const clockById = new Map(['census_long.jsonl', 'portrait_objects.jsonl'].flatMap(f =>
  fs.readFileSync(path.join(CLOCK, f), 'utf8').trim().split('\n').map(l => JSON.parse(l))).map(o => [o.id, o]));

// ---- stepping: period, pops and the union of all phases
function run(o) {
  const pts = Int32Array.from(o.cells.flat());
  const box = autoBox(pts, 2);
  const [nx, ny, nz] = box.dims;
  let cells = new Uint8Array(nx * ny * nz);
  placeSeed(pts, box.dims, box.shift, false, cells);
  const start = cells.slice(), pops = [], union = new Uint8Array(cells.length);
  const pop = (c) => c.reduce((a, v) => a + (v & 1) + ((v >> 1) & 1) + ((v >> 2) & 1), 0);
  for (let g = 0; g <= 200; g++) {
    if (g > 0 && cells.every((v, i) => v === start[i])) {
      const u = [];
      union.forEach((v, idx) => { for (let a = 0; a < 3; a++) if ((v >> a) & 1) { const p = [2 * (idx % nx), 2 * (Math.floor(idx / nx) % ny), 2 * Math.floor(idx / (nx * ny))]; p[a]++; u.push(p.map((x, t) => x - box.shift[t])); } });
      return { period: g, pops, union: u };
    }
    pops.push(pop(cells));
    cells.forEach((v, i) => { union[i] |= v; });
    cells = stepCPU(cells, nx, ny, nz, false);
  }
  return null;
}

// all union cells incident to one lattice vertex (the 12-face vertex star, a closed vessel)
function inOneStar(cells) {
  const p = cells[0], a = (p[0] & 1) ? 0 : (p[1] & 1) ? 1 : 2, [b, c] = [0, 1, 2].filter(t => t !== a);
  for (const sb of [1, -1]) for (const sc of [1, -1]) {
    const v = p.slice(); v[b] += sb; v[c] += sc;
    const ok = cells.every(q => { const qa = (q[0] & 1) ? 0 : (q[1] & 1) ? 1 : 2; return q[qa] === v[qa] && [0, 1, 2].every(t => t === qa || Math.abs(q[t] - v[t]) === 1); });
    if (ok) return true;
  }
  return false;
}

const isFlip = (o) => o.period === 2 && o.spacetime_sym === 2 * o.sym;
const seen = (o) => (o.sources.soup_octa || 0) + (o.sources.soup_kagome || 0);
const take = (pred, n, sort = (a, b) => a.union - b.union || a.id.localeCompare(b.id)) => all.filter(pred).sort(sort).slice(0, n);

// ---- selection
const NOTES = {
  S6a: 'The closed cube: its six faces each touch exactly four others. The commonest ash in 3D soups and the debris of the side-9 and side-11 legacy cubes.',
  S6b: 'Two cube corners kissing at a vertex.',
  S6c: 'The fourth 6-cell still life.',
  KS6a: 'The kagome hexagon: six faces in one {111} layer. The commonest ash of the one-layer automaton; side 9 leaves eight of them, one on each face of its octahedron.',
  S12a: 'The vertex star: all 12 faces meeting at one lattice vertex. A sealed vessel — no outside cell ever sees more than 2 of them — whose 4096 states all settle within 3 generations.',
  'P2.6a': 'The smallest phase of any oscillator: 3 stator cells and a three-fold propeller of hinges, each face swinging 90° about an edge every generation.',
  'P3.11a': 'The smallest period-3 oscillator: no p3 fits in 12 cells (exhaustive), this one uses 13.',
  'P3.13a': 'The commonest period-3 object in soup ash.',
  'P4.11a': 'Smallest period 4 seen (union 14; none exists with union ≤ 10).',
  'P5.17a': 'The commonest period-5 object in soup ash.',
  'P10.17a': 'No stator at all: all 36 cells move.',
  'P11.23a': 'A prime period, 11.',
  'P13.22a': 'A prime period, 13.',
  'P14.17a': 'The commonest high-period object in soup ash.',
  'P16.15a': 'Period 16.',
  'P22.20a': 'Period 22.',
  'P48.34a': 'Period 48 = 2 × 24: after 24 generations the object reappears mirrored, and it takes two such halves to come home.',
  'P66.27a': 'Period 66 = 2 × 33: phase t+33 is phase t mirrored. A flat plate three layers thick that fills its own 45-cell box.',
  'C48.24a': 'A screw: every 8 generations the whole 42-cell plate reappears turned 60° and inverted, so it takes 6 × 8 = 48 generations to come home. Found by sampling a box chosen for its six-fold symmetry; never seen in soup.',
  'C36.33a': 'A quarter turn about a cube axis every 9 generations, so 4 × 9 = 36. It fills the whole 60-cell vertex-centred octahedron.',
  'C12.43a': 'Period 12 = 6 × 2: a sixth of a turn every 2 generations. It fills the same 60-cell box as C36.33a.',
  'C40.24a': 'Period 40 = 2 × 20: a mirror image of itself after 20 generations. It fills its 47-cell hull.',
  'C44.26a': 'Not a twist and not one loop: a period-4 rotor and a period-11 rotor on a shared frame. No cell has period 44.',
  'C35.29a': 'The longest single loop found: 35 generations with no twist; 37 of its 47 cells carry the full period.',
  S8b: 'Six of these sit around the side-10 legacy ash.',
  S32a: 'Twelve of these make the side-8 legacy ash.',
  S72a: 'The 72-cell centrepiece of the side-10 ash: six vertex stars packed together.',
  S384a: 'The whole side-8 legacy ash, full cube symmetry.',
};
const used = new Set();
const pick = (objs) => objs.filter(o => o && !used.has(o.id)).map(o => (used.add(o.id), o));
const ids = (...xs) => xs.map(x => byId.get(x)).filter(Boolean);

const stillSmall = pick(take(o => o.period === 1 && o.union === 6, 10));
const runs = new Map();
const runOf = (o) => { if (!runs.has(o.id)) runs.set(o.id, run(o)); return runs.get(o.id); };
// inside one star: the union of all phases (not just phase 0) lies on the 12 faces of one vertex
const starObjs = all.filter(o => o.union <= 12 && o.period <= 2 && o.family === '3d' && inOneStar(runOf(o).union)).sort((a, b) => a.union - b.union || a.id.localeCompare(b.id));
const star = pick([byId.get('S12a'), ...starObjs.filter(o => o.period === 1 && o.id !== 'S12a' && !used.has(o.id)).slice(0, 5)]);
const hinges = pick(take(o => isFlip(o) && o.family === '3d' && o.union <= 11, 7));
const ash = pick(take(o => o.period === 1 && o.family === '3d' && seen(o) >= 100, 5, (a, b) => seen(b) - seen(a)));
const clock = pick(ids('P3.11a', 'P3.13a', 'P4.11a', 'P5.17a', 'P10.15a', 'P10.17a', 'P11.23a', 'P13.22a', 'P14.17a', 'P16.15a', 'P22.20a'));
const twisted = pick([...ids('P66.27a', 'P48.34a'), ...['C48.24a', 'C36.33a', 'C12.43a', 'C40.24a', 'C44.26a', 'C35.29a'].map(i => { const o = clockById.get(i); if (!o) throw new Error('missing ' + i); return { ...o, family: '3d', clock: true }; })]);
const kag = pick([...ids('KS6a', 'KS9a', 'KS11a'), ...take(o => o.family === 'kagome' && o.period === 2, 1), ...take(o => o.family === 'kagome' && o.period === 3, 1), ...take(o => o.family === 'kagome' && o.period === 4, 1)]);
const legacy = pick(ids('S8b', 'S32a', 'S72a', 'S384a'));

const CATEGORIES = [
  { id: 'smallest', title: 'The smallest still lifes', status: 'proved', items: stillSmall,
    blurb: 'Nothing with fewer than 6 cells survives, and there are exactly four 6-cell still lifes (exhaustive search).' },
  { id: 'star', title: 'The vertex star and what lives inside it', status: 'proved', items: star,
    blurb: 'The 12 faces around one vertex form a sealed vessel: every one of its 4096 states settles within 3 generations, into a still life or a 2-cycle (or dies). Most small fauna are pieces of a star; the still lifes here (and two of the 6-cell ones) live entirely inside one.' },
  { id: 'hinges', title: 'Hinges: period-2 flips', status: 'proved', items: hinges,
    blurb: 'All 13 period-2 oscillators with at most 11 cells are flips whose moving cells swing 90° about a shared edge each generation. Most of these live inside a single vertex star (marked).' },
  { id: 'ash', title: 'Common ash', status: 'measured', items: ash,
    blurb: 'The still lifes left most often by random soups in octahedral vessels (26,900 soups).' },
  { id: 'clockwork', title: 'Clockwork', status: 'measured', items: clock,
    blurb: 'Oscillators found in soup ash, periods 3 to 22. 11% of soups leave at least one oscillator.' },
  { id: 'twisted', title: 'Twisted clocks', status: 'measured', items: twisted,
    blurb: 'The longest periods are twisted: after only L = P/m generations the object returns as a rotated or mirrored copy of itself, where m (2, 3, 4 or 6) is the order of a symmetry of its box, so P = m × L. Objects marked C are not in the atlas; they were found by sampling boxes chosen for their symmetry. The last two are untwisted, for contrast.' },
  { id: 'kagome', title: 'One layer: the kagome automaton', status: 'proved', items: kag,
    blurb: 'A single {111} layer is closed (T4): a kagome lattice where each cell has 6 neighbours. Its smallest oscillator has period 2 and 18 cells.' },
  { id: 'legacy', title: 'Pieces of the original\'s ash', status: 'measured', items: legacy,
    blurb: 'Still lifes left behind by the original program\'s closed-cube runs (sides 8 and 10).' },
];

// ---- verify and emit
let bad = 0;
const out = { generated: new Date().toISOString().slice(0, 10), source: 'research/atlas/catalogue.jsonl and research/clockwork/objects', categories: [] };
for (const cat of CATEGORIES) {
  const items = [];
  for (const o of cat.items) {
    const r = runOf(o);
    // clockwork objects carry min/max population only; their per-phase pops come from the stepping
    const ok = r && r.period === o.period && r.union.length === o.union &&
      (o.clock ? Math.min(...r.pops) === o.minpop && Math.max(...r.pops) === o.maxpop && o.twist * o.quotient_length === o.period
        : r.pops.length === o.pops.length && r.pops.every((v, i) => v === o.pops[i]));
    if (!ok) { bad++; console.error(`MISMATCH ${o.id}: catalogue p${o.period} pops ${o.pops || `${o.minpop}..${o.maxpop}`} union ${o.union}; stepped ${r && `p${r.period} pops ${r.pops} union ${r.union.length}`}`); continue; }
    const twist = o.clock ? o.twist : o.spacetime_sym / o.sym;
    items.push({
      id: o.id, family: o.family, period: o.period, pops: o.clock ? r.pops : o.pops, union: o.union, sym: o.sym, spacetime_sym: o.spacetime_sym,
      twist, quotient: o.period / twist, ...(o.id === 'C44.26a' ? { lcm: [4, 11] } : {}),
      layers: o.layers, strict: o.strict, seen: { soup_octa: o.sources?.soup_octa || 0, soup_kagome: o.sources?.soup_kagome || 0 },
      legacy: o.sources?.legacy || [], exhaustive: o.sources?.exhaustive || [], inStar: o.union <= 12 && inOneStar(r.union),
      flip: isFlip(o), note: NOTES[o.id] || '', cells: o.cells,
    });
  }
  out.categories.push({ id: cat.id, title: cat.title, status: cat.status, blurb: cat.blurb, items });
}
const n = out.categories.reduce((a, c) => a + c.items.length, 0);
fs.mkdirSync(path.join(WEB, 'data'), { recursive: true });
fs.writeFileSync(path.join(WEB, 'data/gallery.json'), JSON.stringify(out));
console.log(`gallery: ${n} objects in ${out.categories.length} categories, each re-stepped (${bad} mismatches)`);
for (const c of out.categories) console.log(`  ${c.title}: ${c.items.map(i => i.id).join(' ')}`);
process.exit(bad ? 1 : 0);
