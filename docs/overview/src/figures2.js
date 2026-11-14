// ---------- the measured law ----------
const LN10 = Math.LN10;
function gens(ln) { // e^ln as a readable number of generations
  const v = Math.exp(ln);
  if (v < 1e7) return fmtInt(+v.toPrecision(3));
  const e = Math.floor(ln / LN10), m = v / Math.pow(10, e);
  return m.toFixed(1) + ' × ' + pow10(e);
}
(function () {
  const L = D.law, H = $('#f-law');
  responsive(H, w => {
    const f = frame(H, { w, h: 330, label: 'Mean life of a face against its area, log scale',
      x: { d: [20, 142], ticks: [30, 45, 63, 84, 108, 135], title: 'sites in the face' }, y: { d: [2, 13.4], ticks: [3, 6, 9, 12], fmt: pow10, title: 'mean life of a face, generations' }, m: { t: 26, r: 16, b: 38, l: 40 } });
    const [a, b] = L.slab_fit;
    S('line', { x1: f.X(24), y1: f.Y((a + b * 24) / LN10), x2: f.X(93), y2: f.Y((a + b * 93) / LN10), stroke: 'var(--s3)', 'stroke-width': 1.5 }, f.svg);
    L.slab.forEach(r => dot(f, r[0], r[1] / LN10, 'var(--s3)', () => ['Slab face, ' + r[0] + ' sites', gens(r[1]) + ' generations', r[3] + ' deaths counted'], { r: 3.6 }));
    const oct = L.oct.map(r => [r[0], r[2] / LN10]).concat(L.gpu.map(r => [r[0], r[2] / LN10]));
    S('path', { class: 'ln', stroke: 'var(--s1)', 'stroke-width': 1.5, d: pathOf(f, oct) }, f.svg);
    L.oct.forEach(r => dot(f, r[0], r[2] / LN10, 'var(--s1)', () => ['Hull face, ' + r[0] + ' sites', gens(r[2]) + ' generations', fmtInt(r[4]) + ' deaths counted']));
    L.gpu.forEach(r => dot(f, r[0], r[2] / LN10, 'var(--s1)', () => ['Hull face, ' + r[0] + ' sites (GPU)', gens(r[2]) + ' generations', fmtInt(r[4]) + ' deaths counted'], { hollow: true, se: r[3] / LN10 }));
    const top = L.gpu[L.gpu.length - 1];
    S('text', { x: f.X(top[0]) + 6, y: f.Y(top[2] / LN10) - 12, 'text-anchor': 'end', class: 't-strong' }, f.svg).textContent = top[0] + ' sites: ' + gens(top[2]) + ' generations';
    const s0 = L.oct[0]; S('text', { x: f.X(s0[0]) + 9, y: f.Y(s0[2] / LN10) + 14 }, f.svg).textContent = s0[0] + ' sites: ' + gens(s0[2]);
  });
  tableView($('#t-law'), ['face', 'sites', 'ln(mean life)', '± s.e.', 'deaths'],
    L.oct.map(r => ['hull, engine', r[0], r[2].toFixed(3), r[3], fmtInt(r[4])]).concat(L.gpu.map(r => ['hull, GPU', r[0], r[2].toFixed(3), r[3], fmtInt(r[4])])).concat(L.slab.map(r => ['slab', r[0], r[1].toFixed(3), r[2], r[3]])));
  const H2 = $('#f-slopes');
  responsive(H2, w => {
    const f = frame(H2, { w, h: 330, label: 'Local slope of the face law between neighbouring sizes',
      x: { d: [24, 141], ticks: [30, 63, 108, 135], title: 'sites in the face' }, y: { d: [0.196, 0.234], ticks: [0.20, 0.21, 0.22, 0.23], fmt: v => v.toFixed(2), title: 'added to ln(life) per site' }, m: { t: 26, r: 10, b: 38, l: 40 } });
    S('line', { x1: f.m.l, x2: w - f.m.r, y1: f.Y(0.2088), y2: f.Y(0.2088), stroke: 'var(--s3)', 'stroke-width': 1.5 }, f.svg);
    S('text', { x: w - f.m.r - 2, y: f.Y(0.2088) - 6, 'text-anchor': 'end', class: 'halo' }, f.svg).textContent = 'flat slab faces, 0.2088';
    S('line', { x1: f.m.l, x2: w - f.m.r, y1: f.Y(0.2077), y2: f.Y(0.2077), stroke: 'var(--retired)', 'stroke-width': 1 }, f.svg);
    const rt = S('text', { x: f.m.l + 4, y: f.Y(0.2077) + 13, class: 'halo', style: 'text-decoration:line-through' }, f.svg); rt.textContent = '0.2077';
    S('text', { x: f.m.l + 44, y: f.Y(0.2077) + 13, class: 'halo' }, f.svg).textContent = 'retired';
    L.slopes.forEach(r => {
      S('line', { x1: f.X(r[0]), x2: f.X(r[1]), y1: f.Y(r[2]), y2: f.Y(r[2]), stroke: 'var(--s1)', 'stroke-width': 2, 'stroke-linecap': 'round' }, f.svg);
      dot(f, (r[0] + r[1]) / 2, r[2], 'var(--s1)', () => ['From ' + r[0] + ' to ' + r[1] + ' sites', r[2] + ' per site' + (r[3] ? ' ± ' + r[3] : '')], { se: r[3] || 0, r: 4 });
    });
    const last = L.slopes[L.slopes.length - 1]; S('text', { x: f.X(last[1]), y: f.Y(last[2] + last[3]) - 7, 'text-anchor': 'end', class: 't-strong' }, f.svg).textContent = String(last[2]);
    S('text', { x: f.X(L.slopes[0][0]), y: f.Y(L.slopes[0][2]) + 16, class: 't-strong' }, f.svg).textContent = String(L.slopes[0][2]);
  });

  // the stationary tail
  const T = D.tail, HT = $('#f-tail');
  responsive(HT, w => {
    const f = frame(HT, { w, h: 270, label: 'Probability that a face of 45 sites holds k live cells, log scale',
      x: { d: [-1.2, 40], ticks: [0, 10, 20, 30, 39], fmt: v => v === 0 ? 'dead' : String(v), title: 'live cells in the face' }, y: { d: [-5.7, -0.7], ticks: [-5, -4, -3, -2, -1], fmt: pow10, title: 'share of generations' }, m: { t: 26, r: 12, b: 38, l: 44 } });
    const pts = T.ln_p.map((v, i) => [i + 1, v / LN10]), k1 = pts[0], k8 = pts[7], sl = (k8[1] - k1[1]) / 7;
    S('line', { x1: f.X(0), y1: f.Y(k1[1] - sl), x2: f.X(11), y2: f.Y(k1[1] + sl * 10), stroke: 'var(--ink-3)', 'stroke-width': 1 }, f.svg);
    S('path', { class: 'ln', stroke: 'var(--s1)', d: pathOf(f, pts) }, f.svg);
    pts.slice(0, 10).forEach(p => dot(f, p[0], p[1], 'var(--s1)', () => [p[0] + (p[0] > 1 ? ' live cells' : ' live cell'), 'one generation in ' + fmtInt(Math.round(Math.pow(10, -p[1])))], { r: 3.4 }));
    dot(f, 0, T.ln_h / LN10, 'var(--s1)', () => ['The face dies', 'once in ' + fmtInt(Math.round(Math.exp(-T.ln_h))) + ' generations'], { hollow: true });
    S('text', { x: f.X(0) + 10, y: f.Y(T.ln_h / LN10) + 16, class: 't-strong halo' }, f.svg).textContent = 'death rate';
    S('text', { x: f.X(22), y: f.Y(-1.05) - 8, 'text-anchor': 'middle', class: 'halo' }, f.svg).textContent = 'usual: about half full';
    S('text', { x: f.X(8.5), y: f.Y(pts[5][1]) + 4, class: 'halo' }, f.svg).textContent = '× 0.65 per cell fewer';
  });
  iso($('#f-ember'), [{ p: [1, 0, 0] }, { p: [0, 1, 0] }, { p: [0, 0, 1] }], { scale: 30, yaw: 0.7, pitch: 0.55, label: 'Three faces meeting at one corner of a cube', wires: [{ cls: 'wire', segs: cubeWire([0, 0, 0], 1) }] });
})();

// ---------- symmetry and the cubes ----------
(function () {
  const Sy = D.sym, H = $('#f-sym'), best = new Map();
  Sy.cpu.forEach(r => best.set(r[0] + r[1], { A: r[0], c: r[1], deaths: r[2], ln: r[3], se: r[4], how: 'engine' }));
  Sy.gpu.forEach(r => best.set(r[0] + r[1], { A: r[0], c: r[1], deaths: r[2], ln: r[3], se: r[4], how: 'GPU' }));
  const pts = [...best.values()].sort((a, b) => a.A - b.A);
  responsive(H, w => {
    const f = frame(H, { w, h: 300, label: 'Mean life of a face of a fully symmetric soup against its area',
      x: { d: [335, 850], ticks: [360, 459, 570, 693, 828], title: 'sites in the face' }, y: { d: [4, 11], ticks: [4, 6, 8, 10], fmt: pow10, title: 'mean life of a face, generations' }, m: { t: 26, r: 16, b: 38, l: 40 } });
    const fit = A => (Sy.fit[0] + Sy.fit[1] * A + Sy.fit[2] * Math.sqrt(A)) / LN10, cur = [];
    for (let A = 400; A <= 835; A += 15) cur.push([A, fit(A)]);
    S('path', { class: 'ln', stroke: 'var(--ink-3)', 'stroke-width': 1.2, d: pathOf(f, cur) }, f.svg);
    pts.forEach(p => dot(f, p.A, p.ln / LN10, 'var(--s2)', () => [p.A + ' sites, centred on a ' + (p.c === 'c' ? 'cube' : 'vertex'), gens(p.ln) + ' generations', fmtInt(p.deaths) + ' deaths counted (' + p.how + ')'], { hollow: p.c === 'v', se: p.se > 0.06 ? p.se / LN10 : 0, r: 4.2 }));
    const top = pts[pts.length - 1];
    S('text', { x: f.X(top.A) - 10, y: f.Y(top.ln / LN10) - 2, 'text-anchor': 'end', class: 't-strong' }, f.svg).textContent = top.A + ' sites: ' + gens(top.ln);
  });
  tableView($('#t-sym'), ['sites', 'centre', 'ln(mean life)', '± s.e.', 'deaths', 'run on'], pts.map(p => [p.A, p.c === 'c' ? 'cube' : 'vertex', p.ln.toFixed(3), p.se, fmtInt(p.deaths), p.how]));

  const C = D.cubes, HC = $('#f-cubes');
  responsive(HC, w => {
    const f = frame(HC, { w, h: 300, label: 'Lifetime of the closed cubes of side 8 to 16, log scale',
      x: { d: [7.3, 17.7], ticks: [8, 10, 12, 14, 16, 17], fmt: v => v === 17 ? '17?' : String(v), title: 'side of the cube' }, y: { d: [0.8, 11.2], ticks: [2, 4, 6, 8, 10], fmt: pow10, title: 'generations until still' }, m: { t: 26, r: 14, b: 38, l: 40 } });
    const lg = v => Math.log10(v), bar = (x, lo, hi, lines) => { const r = S('rect', { x: f.X(x) - 2.5, y: f.Y(lg(hi)), width: 5, height: f.Y(lg(lo)) - f.Y(lg(hi)), rx: 2.5, fill: 'var(--ink-3)', tabindex: 0 }, f.svg); tipOn(r, lines); };
    S('path', { class: 'ln', stroke: 'var(--s2)', 'stroke-width': 1.2, 'stroke-opacity': .6, d: pathOf(f, C.rows.map(r => [r[0], lg(r[1])])) }, f.svg);
    bar(15.72, C.f16[0], C.f16[2], () => ['Forecast for side 16', 'mean ' + gens(Math.log(C.f16[1])) + ', 90% range ' + gens(Math.log(C.f16[0])) + ' to ' + gens(Math.log(C.f16[2]))]);
    bar(17, C.f17[0], C.f17[2], () => ['Forecast for side 17, first face', 'mean ' + gens(Math.log(C.f17[1])) + ' generations; not run']);
    C.rows.forEach(r => dot(f, r[0], lg(r[1]), 'var(--s2)', () => ['Side ' + r[0], fmtInt(r[1]) + ' generations', r[2] ? 'leaves ' + r[2] + ' live faces' : 'leaves nothing'], { r: 4.2 }));
    const lab = (n, s, dx, dy, anchor) => { const r = C.rows.find(x => x[0] === n); S('text', { x: f.X(n) + dx, y: f.Y(lg(r[1])) + dy, 'text-anchor': anchor || 'start', class: 't-strong halo' }, f.svg).textContent = s; };
    lab(11, '4,218', 8, 12); lab(13, '169,049', 8, 12); lab(16, '2.9 billion', -9, -6, 'end');
  });
})();

// ---------- the flat cousin's law ----------
(function () {
  const H = $('#f-toylaw'), P = D.toylaw;
  responsive(H, w => {
    const f = frame(H, { w, h: 250, label: 'Mean wait for an edge of the two-dimensional rule to die, against its length',
      x: { d: [10, 38], ticks: P.map(r => r[0]), title: 'length of the edge, cells' }, y: { d: [2, 7.2], ticks: [3, 4, 5, 6, 7], fmt: logfmt, title: 'mean wait, generations' }, m: { t: 26, r: 14, b: 38, l: 70 } });
    S('path', { class: 'ln', stroke: 'var(--s3)', 'stroke-width': 1.5, d: pathOf(f, P.map(r => [r[0], r[1] / LN10])) }, f.svg);
    P.forEach(r => dot(f, r[0], r[1] / LN10, 'var(--s3)', () => ['Edge of ' + r[0] + ' cells', gens(r[1]) + ' generations', fmtInt(r[3]) + ' deaths counted']));
  });
})();

// ---------- prior art ----------
(function () {
  const want = ['Crutchfield', 'Durrett', 'Mountford', 'Bramson', 'Politi', 'Eppstein', 'Houghton'], H = $('#f-prior');
  const rows = D.project.prior.filter(r => want.some(k => r[1].indexOf(k) >= 0)).map(r => ({ y: parseInt(String(r[0]).match(/\d{4}/)[0], 10), ys: String(r[0]).replace(/\s*\(.*\)/, ''), who: r[1].replace(/J\. P\. |K\. |D\. |R\. H\. |R\. |X\.-F\. |T\. S\. |M\. R\. E\. |S\. M\. |E\. |M\. |C\. |A\. /g, ''), line: r[2], read: r[3] }));
  rows.push({ y: 2012, ys: '2012', who: 'gump', line: 'Your Processing sketch: a rule chosen by hand on the faces of the cubic honeycomb.', read: '', gump: 1 });
  rows.sort((a, b) => a.y - b.y).forEach(r => { E('span', { class: 'y' }, H, r.ys); const d = E('div', { class: 'w' + (r.gump ? ' gump' : '') }, H); E('b', {}, d, r.who + '. '); E('span', {}, d, r.line + ' '); if (r.read) E('em', {}, d, '[' + r.read + ']'); });
  D.project.known.split('; ').forEach(s => E('li', {}, $('#l-known'), s.charAt(0).toUpperCase() + s.slice(1)));
  D.project.ours.slice(0, 5).forEach(s => E('li', {}, $('#l-ours'), s.charAt(0).toUpperCase() + s.slice(1)));
})();

// ---------- the swarm ----------
(function () {
  const W = D.swarm, H = $('#f-swarm'), col = { 'confirmed-by-critic': 'var(--ink)', 'claimed': 'var(--s-mute)', 'open': 'var(--grid)' };
  ['probability', 'counting', 'path', 'source'].forEach(k => {
    const L = W.lines[k], c = E('div', { class: 'sline' }, H), n = t => L.results.filter(r => r[2] === t).length;
    E('h3', {}, c, L.label); E('p', { class: 'idea' }, c, L.line);
    const r = E('div', { class: 'rounds' }, c); for (let i = 0; i < L.written; i++) E('i', { class: i < L.refereed ? 'on' : '' }, r); E('span', {}, r, L.written + ' rounds written, ' + L.refereed + ' refereed');
    const sg = E('div', { class: 'seg', role: 'img', 'aria-label': n('confirmed-by-critic') + ' results checked by the critic, ' + n('claimed') + ' claimed, ' + n('open') + ' open, ' + L.dropped + ' refuted or withdrawn' }, c);
    [['a', n('confirmed-by-critic')], ['b', n('claimed')], ['c', n('open')], ['d', L.dropped]].forEach(([cl, v]) => { if (v) E('span', { class: cl, style: 'flex:' + v + ' 1 0' }, sg, String(v)); });
    const tp = E('p', { class: 'top' }, c); E('b', {}, tp, 'So far'); tp.appendChild(document.createTextNode(L.top));
    const d = E('details', {}, c); E('summary', {}, d, 'All ' + L.results.length + ' results'); const ul = E('ul', {}, d);
    L.results.forEach(x => { const li = E('li', {}, ul); E('i', { style: 'background:' + col[x[2]] + (x[2] === 'open' ? ';box-shadow:inset 0 0 0 1px var(--ink-3)' : '') }, li); E('span', {}, li, x[1]); });
  });
  const N = $('#n-swarm'), C = W.counts, num = (v, l) => { const d = E('div', { class: 'num' }, N); E('span', { class: 'v' }, d, String(v)); E('span', { class: 'l' }, d, l); };
  num(C.rounds_written, 'rounds written; ' + C.rounds_refereed_full + ' refereed in full'); num(C.corrections, 'corrections to the problem as the lead posed it');
  num(C.graveyard, 'dead ideas buried, each with its reason'); num(C.lab_results_solver, 'exact computations run by the critic for the solvers');
  num(C.library_sources, 'sources on the librarian’s shelf; ' + W.library.not_obtained + ' could not be obtained'); num(C.predictions, 'predictions filed in advance; none run yet');
  W.dead.forEach(x => { const li = E('li', {}, $('#l-dead')); E('b', {}, li, x[0]); li.appendChild(document.createTextNode('  ' + x[1])); });
  W.alive.forEach(x => { const li = E('li', {}, $('#l-alive')); E('b', {}, li, x[0] + '. '); li.appendChild(document.createTextNode(x[1])); });
  $('#c-swarm').textContent = 'No formula for the rate yet. Exponential lifetime is proved only for relatives of gump driven by dice or by provably random sources, and those proofs lean on two cited facts not yet on the shelf.';
  const t = E('table', {}, $('#t-errors')), hr = E('tr', {}, E('thead', {}, t)); ['', 'the lead had said', 'the critic showed'].forEach(h => E('th', {}, hr, h));
  const tb = E('tbody', {}, t); W.errors.forEach(e => { const tr = E('tr', {}, tb); e.forEach((c, i) => E('td', { style: i ? 'text-align:left;white-space:normal' : '' }, tr, c)); });
})();

// ---------- checking ----------
(function () {
  const P = D.project, G = P.grades, sg = $('#f-grades'), mean = { A: 're-derived independently, by other code or another agent', B: 're-run by the auditor and matched', C: 'has a command, not yet re-run', D: 'no recipe to reproduce it' };
  sg.setAttribute('role', 'img'); sg.setAttribute('aria-label', 'A ' + G.A + ', B ' + G.B + ', C ' + G.C + ', D ' + G.D);
  ['A', 'B', 'C', 'D'].forEach((k, i) => E('span', { class: 'g' + (i + 1), style: 'flex:' + G[k] + ' 1 0' }, sg, G[k] > 3 ? k + ' ' + G[k] : ''));
  ['A', 'B', 'C', 'D'].forEach((k, i) => { const kk = E('span', { class: 'key' }, $('#k-grades')); const sw = E('span', { class: 'sw' }, kk); sw.style.background = getComputedStyle(sg.children[i]).backgroundColor; kk.appendChild(document.createTextNode(k + (k === 'D' ? ' (' + G.D + ')' : '') + ': ' + mean[k])); });
  document.querySelectorAll('.n-corr').forEach(e => { e.textContent = D.corrections.length; });
  const by = new Map(); D.corrections.forEach(c => by.set(c.who, (by.get(c.who) || 0) + 1));
  const rows = [...by.entries()].sort((a, b) => b[1] - a[1]), mx = rows[0][1];
  rows.forEach(([who, n]) => barRow($('#f-caught'), who, n / mx, String(n), who.indexOf('automaton') >= 0 ? 'hot' : ''));
  const F = $('#f-forecasts');
  D.forecasts.forEach(fc => { const r = String(fc.result || '').toLowerCase(), hit = /hit/.test(r), bad = /miss|half|pending|open/.test(r), cls = hit && !bad ? 'st-meas' : !hit && /miss/.test(r) ? 'st-ret' : 'st-once';
    const d = E('div', {}, F); E('span', { class: 'st ' + cls, title: fc.result || '' }, d); E('span', {}, d, fc.line); });
  const t = E('table', {}, $('#t-corr')), hr = E('tr', {}, E('thead', {}, t)); ['what was said', 'what is held now', 'caught by'].forEach(h => E('th', { style: 'text-align:left' }, hr, h));
  const tb = E('tbody', {}, t); D.corrections.forEach(c => { const tr = E('tr', {}, tb); [c.said, c.now, c.by].forEach(x => E('td', { style: 'text-align:left;white-space:normal;vertical-align:top;min-width:140px' }, tr, x || '')); });
})();

// ---------- timeline ----------
(function () {
  const T = D.project.timeline, H = $('#f-timeline'), t0 = Date.parse(T.first_commit.slice(0, 20)), t1 = Date.parse(T.last_commit.slice(0, 20));
  const ms = T.milestones.map(m => ({ t: Date.parse(m.date.replace('Z', ':00Z')), text: m.text })), prs = T.pull_requests.map(p => ({ t: Date.parse(p.date.replace('Z', ':00Z')), n: p.n, title: p.title }));
  const hh = t => new Date(t).toISOString().slice(5, 16).replace('T', ' ');
  responsive(H, w => {
    const svg = S('svg', { viewBox: `0 0 ${w} 98`, width: w, height: 98, role: 'img', 'aria-label': 'Timeline of milestones and merged pull requests over 33 hours' }, H), ml = 8, mr = 8;
    const X = t => ml + (t - t0) / (t1 - t0) * (w - ml - mr);
    S('line', { class: 'ax', x1: ml, x2: w - mr, y1: 44, y2: 44 }, svg);
    for (let t = Date.parse('2026-11-12T18:00:00Z'); t < t1; t += 6 * 3600e3) { const d = new Date(t), mid = d.getUTCHours() === 0;
      S('line', { class: 'ax', x1: X(t), x2: X(t), y1: mid ? 30 : 40, y2: 48 }, svg);
      S('text', { x: X(t), y: 62, 'text-anchor': X(t) > w - 30 ? 'end' : 'middle', class: 't-mono' }, svg).textContent = mid ? d.toISOString().slice(5, 10) : String(d.getUTCHours()).padStart(2, '0') + 'h'; }
    ms.forEach(m => { S('line', { x1: X(m.t), x2: X(m.t), y1: 20, y2: 44, stroke: 'var(--ember)', 'stroke-width': 1.5 }, svg); const c = S('circle', { cx: X(m.t), cy: 18, r: 4.5, fill: 'var(--ember)', stroke: 'var(--surface)', 'stroke-width': 2 }, svg);
      const hit = S('circle', { class: 'hit', cx: X(m.t), cy: 18, r: 11, tabindex: 0 }, svg); tipOn(hit, () => [m.text, hh(m.t) + ' UTC']); });
    prs.forEach(p => { const c = S('rect', { x: X(p.t) - 4, y: 70, width: 8, height: 8, fill: 'var(--surface)', stroke: 'var(--ink)', 'stroke-width': 1.5 }, svg);
      const hit = S('rect', { class: 'hit', x: X(p.t) - 9, y: 64, width: 18, height: 20, tabindex: 0 }, svg); tipOn(hit, () => ['Pull request ' + p.n + ' merged', p.title]); });
    S('text', { x: ml, y: 12 }, svg).textContent = 'findings and events';
    S('text', { x: ml, y: 94 }, svg).textContent = 'merged pull requests';
  });
  ms.forEach(m => { const li = E('li', {}, $('#l-miles')); E('time', {}, li, hh(m.t)); E('span', {}, li, m.text); });
})();
$('#stamp').textContent = 'Repository state of ' + D.project.timeline.last_commit.slice(0, 10) + '. Research is paused.';
