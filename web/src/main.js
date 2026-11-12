// App shell: decoupled loop (GPU stepping under an adaptive per-frame budget, rendering at
// display rate, statistics by GPU reduction + async readback on their own cadence), UI, URL state.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { Sim } from './gl/sim.js';
import { Stats } from './gl/stats.js';
import { CellView, PALETTE } from './render.js';
import { makeSeed, autoBox, placeSeed, hullPolytope, reembed, hullOf } from './seeds.js';
import { DIAGONALS } from './cpu.js';
import { Strip } from './strip.js';

const $ = (id) => document.getElementById(id);
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const fmt = (n) => n == null ? '–' : Math.round(n).toLocaleString('en-US');

// ---------------------------------------------------------------- URL / spec
const DEFAULTS = { seed: 'cube', n: 11, k: 5, H: 60, shape: 'cube', density: 0.3, layers: 3, rng: 1,
  box: 'auto', bc: 'dead', speed: 'max', view: 'auto', face: 0.6, gen: 0, play: 0, lanes: 32, cells: '', cam: '' };
const NUMERIC = ['n', 'k', 'H', 'density', 'layers', 'rng', 'face', 'gen', 'play', 'lanes'];

function readURL() {
  const q = new URLSearchParams(location.search);
  const spec = { ...DEFAULTS };
  for (const [k, v] of q) if (k in DEFAULTS) spec[k] = NUMERIC.includes(k) ? Number(v) : v;
  return spec;
}
function seedKeys(spec) {
  const keys = ['seed'];
  if (spec.seed === 'cube') keys.push('n');
  if (spec.seed === 'key') keys.push('k');
  if (spec.seed === 'legacy') keys.push('H');
  if (spec.seed === 'cells') keys.push('cells');
  if (spec.seed === 'soup') keys.push('shape', 'n', 'density', 'rng', ...(spec.shape === 'slab' ? ['layers'] : []));
  return keys;
}
function shareURL(extra = {}) {
  const s = { ...app.spec, ...extra };
  const q = new URLSearchParams();
  for (const k of seedKeys(s)) q.set(k, s[k]);
  for (const k of ['box', 'bc', 'speed', 'view', 'face', 'gen', 'play', 'lanes', 'cam']) if (s[k] !== DEFAULTS[k]) q.set(k, s[k]);
  return `${location.origin}${location.pathname}?${q}`;
}
function writeURL() { history.replaceState(null, '', shareURL({ gen: 0, play: 0 })); }

// ---------------------------------------------------------------- GL / three setup
const canvas = $('view');
const gl = canvas.getContext('webgl2', { antialias: true, powerPreference: 'high-performance' });
if (!gl) { document.body.innerHTML = '<p style="padding:2em">WebGL2 is required.</p>'; throw new Error('no webgl2'); }
const renderer = new THREE.WebGLRenderer({ canvas, context: gl, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
const scene = new THREE.Scene();
scene.background = new THREE.Color(PALETTE.background);
const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 5000);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
const view = new CellView(scene);
const boxLines = new THREE.LineSegments(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0x8a817a, transparent: true, opacity: 0.6 }));
const hullLines = new THREE.LineSegments(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0xd9c9a0, transparent: true, opacity: 0.35 }));
scene.add(boxLines, hullLines);

function resize() {
  const wide = window.innerWidth > 900;
  const w = wide ? window.innerWidth - 332 : window.innerWidth, h = window.innerHeight;
  canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
  renderer.setSize(w, h, false);
  camera.aspect = w / h; camera.updateProjectionMatrix();
}
window.addEventListener('resize', resize);

// ---------------------------------------------------------------- app state
const app = {
  spec: readURL(),
  sim: null, stats: null, dims: null, torus: false,
  gen: 0, playing: false, runUntil: 0,
  spf: 1, acc: 0, frameFence: null,
  last: null, initialHull: null, prevHull: null, events: [],
  stepsWindow: [], lastFrame: performance.now(), frameTimes: [],
  statsInterval: 40, lastStatsStart: 0, statsDirty: true,
};
const strip = new Strip($('strip'));
window.gump = app;   // for tests / console poking
app.three = { renderer, scene, camera, view, gl };

function buildSim(dims, torus, cells) {
  if (app.sim) { app.stats.dispose(); app.sim.dispose(); }
  app.dims = dims; app.torus = torus;
  app.sim = new Sim(gl, dims[0], dims[1], dims[2], { torus, maxLanes: app.spec.lanes });
  app.stats = new Stats(gl, app.sim.layout);
  app.sim.upload(cells);
  renderer.resetState();
  view.setLayout(app.sim.layout);
  view.setMode(viewMode());
  boxLines.geometry.dispose();
  boxLines.geometry = new THREE.EdgesGeometry(new THREE.BoxGeometry(dims[0], dims[1], dims[2]));
  app.statsDirty = true;
  view.setHullClip(null);      // re-armed by the first statistics of this state
  updateBoxInfo();
}

function boxFromSpec(spec, pts) {
  if (spec.seed === 'legacy' && spec.box === 'auto' && spec.H % 2 === 0 && spec.bc === 'torus')
    return { dims: [spec.H / 2, spec.H / 2, spec.H / 2], shift: [0, 0, 0] };   // the original's array torus
  const auto = autoBox(pts);
  if (spec.box === 'auto') return auto;
  const d = String(spec.box).split(/[,x]/).map(Number).filter(v => v > 0);
  const dims = d.length === 3 ? d : [d[0], d[0], d[0]];
  // centre the seed: keep auto's centring relative to the box centre
  const shift = dims.map((N, t) => auto.shift[t] + 2 * Math.floor((N - auto.dims[t]) / 2));
  return { dims, shift };
}

function resetToSeed() {
  const spec = app.spec;
  const seed = makeSeed(spec);
  const { dims, shift } = boxFromSpec(spec, seed.pts);
  const cells = new Uint8Array(dims[0] * dims[1] * dims[2]);
  const dropped = placeSeed(seed.pts, dims, shift, spec.bc === 'torus', cells);
  const h0 = hullOf(seed.pts);
  buildSim(dims, spec.bc === 'torus', cells);
  app.seedName = seed.name + (dropped ? ` (${dropped} cells did not fit)` : '');
  app.gen = 0; app.acc = 0;
  app.initialHull = null; app.prevHull = null; app.events = []; app.last = null;
  // T2: if the seed's hull fits the box, the run is the infinite-space run forever. Cleared for
  // good by anything that may have let the boundary act (seed clipped, resize below the hull).
  app.exact = !dropped && (!h0 || hullFits(hullPolytope({ loS: h0.loS.map((v, n) => v + dot(DIAGONALS[n], shift)), hiS: h0.hiS.map((v, n) => v + dot(DIAGONALS[n], shift)) })));
  strip.clear();
  app.runUntil = spec.gen || 0;
  setPlaying(!!spec.play || app.runUntil > 0);
  frameCamera(seed.pts);
  writeURL();
  syncForm();
}

function frameCamera(pts) {
  // frame the seed's hull (what can ever be alive), not the whole box
  let r = 0.5 * Math.hypot(...app.dims);
  const h = pts && pts.length ? hullOf(pts) : null;
  if (h) { const poly = hullPolytope(h); r = Math.min(r, 0.25 * Math.hypot(...[0, 1, 2].map(t => poly.hi[t] - poly.lo[t] + 2)) + 1); }
  const c = String(app.spec.cam || '').split(',').map(Number);
  const dir = (c.length >= 3 && c.every(Number.isFinite) ? new THREE.Vector3(c[0], c[1], c[2]) : new THREE.Vector3(1.0, 0.75, 1.35)).normalize();
  const zoom = c.length === 4 && c[3] > 0 ? c[3] : 1;
  camera.position.copy(dir.multiplyScalar(r / Math.sin(THREE.MathUtils.degToRad(camera.fov / 2)) * 0.8 / zoom));
  controls.target.set(0, 0, 0);
  camera.near = r * 0.01; camera.far = r * 20; camera.updateProjectionMatrix();
  controls.update();
}

function setPlaying(p) { if (p && !app.playing) app.stepsWindow = []; app.playing = p; $('play').textContent = p ? '❚❚ pause' : '▶ play'; }

function stepOnce() { setPlaying(false); app.runUntil = 0; app.sim.step(1); app.gen++; app.statsDirty = true; }

// Resize on the fly, preserving state (blocking readback; user action only).
function resizeTo(dims, shiftOverride) {
  const old = app.dims, cells = app.sim.download();
  const shift = shiftOverride || dims.map((N, t) => 2 * Math.floor((N - old[t]) / 2));
  const r = reembed(cells, old, dims, shift, app.torus);
  const h = hullOf(r.pts);
  buildSim(dims, app.torus, r.cells);
  if (r.dropped || (h && !hullFits(hullPolytope(h)))) app.exact = false;
  // keep hull bookkeeping in the new array frame (s = d.p shifts by d.shift)
  const mv = (h) => h && { loS: h.loS.map((v, n) => v + dot(DIAGONALS[n], shift)), hiS: h.hiS.map((v, n) => v + dot(DIAGONALS[n], shift)) };
  app.prevHull = mv(app.prevHull); app.initialHull = mv(app.initialHull);
  app.spec.box = dims.join('x');
  if (r.dropped) pushEvent(`resize dropped ${r.dropped} live cells`);
  frameCamera(); writeURL(); syncForm();
}
function fitHull() {
  const cells = app.sim.download();
  const r = reembed(cells, app.dims, app.dims, [0, 0, 0], app.torus);
  if (!r.pts.length) return;
  const box = autoBox(r.pts);
  resizeTo(box.dims, box.shift);
}

// ---------------------------------------------------------------- statistics → instruments
function pushEvent(msg) { app.events.unshift(msg); app.events.length = Math.min(app.events.length, 50); }

function onStats(gen, s) {
  app.last = { gen, s };
  strip.add(gen, s.pop, s.count);
  if (s.pop && s.loS) {
    const h = { loS: s.loS.slice(), hiS: s.hiS.slice() };
    if (!app.initialHull) app.initialHull = h;
    if (app.prevHull) {
      DIAGONALS.forEach((d, n) => {
        const name = `(${d.map(v => v > 0 ? '+' : '−').join('')})`;
        if (h.hiS[n] < app.prevHull.hiS[n]) pushEvent(`gen ≤${gen}: ${name} max s ${app.prevHull.hiS[n]} → ${h.hiS[n]}`);
        if (h.loS[n] > app.prevHull.loS[n]) pushEvent(`gen ≤${gen}: ${name} min s ${app.prevHull.loS[n]} → ${h.loS[n]}`);
      });
    }
    app.prevHull = h;
    if (!app.torus) view.setHullClip(h);
    const poly = hullPolytope(h);
    const pos = [];
    for (const [a, b] of poly.edges) for (const v of [poly.verts[a], poly.verts[b]])
      pos.push(v[0] / 2 + 0.5 - app.dims[0] / 2, v[1] / 2 + 0.5 - app.dims[1] / 2, v[2] / 2 + 0.5 - app.dims[2] / 2);
    hullLines.geometry.dispose();
    hullLines.geometry = new THREE.BufferGeometry();
    hullLines.geometry.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    app.hullPoly = poly;
  } else {
    hullLines.geometry.setDrawRange(0, 0);
    app.hullPoly = null;
  }
}

function updateBoxInfo() {
  const L = app.sim.layout;
  $('boxinfo').innerHTML = `${app.dims.join('×')} cubes, ${app.torus ? 'torus' : 'dead outside'} · ${fmt(3 * app.dims[0] * app.dims[1] * app.dims[2])} cells<br>` +
    `<span class="dim">${L.LANES} lanes/word · atlas ${L.width}×${L.height} · ${app.seedName || ''}</span>`;
  $('bcToggle').textContent = app.torus ? '⇄ dead outside' : '⇄ torus';
}

function updateInstruments(now) {
  $('gen').textContent = fmt(app.gen);
  // generations/s over the last second of issued steps (stepping is fence-throttled, so issued ≈ completed)
  // (time, generation) history; rate over the last ~1-2 s
  const w = app.stepsWindow; w.push([now, app.gen]);
  while (w.length > 2 && now - w[1][0] > 1000) w.shift();
  const gps = w.length > 1 && now > w[0][0] ? (app.gen - w[0][1]) / (now - w[0][0]) * 1000 : 0;
  $('gps').textContent = app.playing ? (gps >= 100 ? fmt(gps) : gps.toFixed(1)) : 'paused';
  const ft = app.frameTimes; const fps = ft.length > 1 ? 1000 * (ft.length - 1) / (ft[ft.length - 1] - ft[0]) : 0;
  $('spf').textContent = `${Math.round(app.spf)} gens/frame budget`;
  $('fps').textContent = `${fps.toFixed(0)} fps`;
  const last = app.last;
  if (last) {
    const s = last.s;
    $('pop').textContent = fmt(s.pop);
    $('popx').textContent = fmt(s.count[0]); $('popy').textContent = fmt(s.count[1]); $('popz').textContent = fmt(s.count[2]);
    $('statsage').textContent = last.gen === app.gen ? 'statistics current' : `statistics from gen ${fmt(last.gen)} (sampled asynchronously)`;
    hullTable(s);
    edgeStatus(s);
  }
  $('hullevents').innerHTML = app.events.map(e => `<div>${e}</div>`).join('');
  strip.draw();
}

function hullTable(s) {
  const rows = ['<tr><th>d</th><th>min s</th><th>max s</th><th>layers</th><th>start</th></tr>'];
  DIAGONALS.forEach((d, n) => {
    const name = `(${d.map(v => v > 0 ? '+' : '−').join('')})`;
    if (!s.loS) { rows.push(`<tr><td>${name}</td><td colspan=4>empty</td></tr>`); return; }
    const i0 = app.initialHull;
    const w = (s.hiS[n] - s.loS[n]) / 2 + 1, w0 = i0 ? (i0.hiS[n] - i0.loS[n]) / 2 + 1 : w;
    const cl = (b) => b ? ' class="shrunk"' : '';
    rows.push(`<tr><td>${name}</td><td${cl(i0 && s.loS[n] > i0.loS[n])}>${s.loS[n]}</td><td${cl(i0 && s.hiS[n] < i0.hiS[n])}>${s.hiS[n]}</td><td${cl(w < w0)}>${w}</td><td class="dim">${w0}</td></tr>`);
  });
  $('hull').innerHTML = rows.join('');
}

// Does a hull polytope (doubled coords, array frame) fit the current box? Dead outside: every
// cell it can hold is representable (0 <= p <= 2N-1). Torus: conservative, it stays clear of its
// own wrapped images by more than the interaction range.
function hullFits(poly) {
  return app.torus ? [0, 1, 2].every(t => poly.hi[t] - poly.lo[t] <= 2 * app.dims[t] - 6)
    : [0, 1, 2].every(t => poly.lo[t] >= 0 && poly.hi[t] <= 2 * app.dims[t] - 1);
}

function edgeStatus(s) {
  const el = $('edge');
  if (!s.pop) { el.innerHTML = '<span class="dim">no live cells</span>'; return; }
  const lim = app.dims.map(N => 2 * N - 1);
  const gap = Math.min(...[0, 1, 2].map(t => Math.min(s.lo[t], lim[t] - s.hi[t])));   // doubled units
  const msgs = [];
  const poly = app.hullPoly;
  const fits = poly && hullFits(poly);
  if (app.torus) {
    const ext = Math.max(...[0, 1, 2].map(t => s.hi[t] - s.lo[t] - (2 * app.dims[t] - 6)));
    if (ext > 0) msgs.push('<span class="alert">pattern spans the torus: it interacts with its own wrapped image</span>');
  } else if (gap <= 2) msgs.push('<span class="alert">⚠ live cells at the boundary: births outside are being suppressed</span>');
  else if (gap <= 8) msgs.push(`<span class="${fits ? 'dim' : 'alert'}">live cells ${Math.floor(gap / 2)} cube${Math.floor(gap / 2) === 1 ? '' : 's'} from the boundary</span>`);
  if (poly) {
    msgs.push(!fits ? '<span class="alert">hull exceeds the box: the boundary can change the outcome</span>'
      : app.exact ? '<span class="ok">hull fits: this run equals the infinite-space run, forever (T2)</span>'
      : '<span class="ok">hull fits from now on</span> <span class="dim">(earlier generations may have felt the boundary)</span>');
  }
  el.innerHTML = msgs.join('<br>');
}

// ---------------------------------------------------------------- the loop
function frame(now) {
  requestAnimationFrame(frame);
  const dt = Math.min(0.1, (now - app.lastFrame) / 1000);
  app.lastFrame = now;
  app.frameTimes.push(now); while (app.frameTimes.length > 30) app.frameTimes.shift();

  // 1. Is the GPU done with last frame's work? That is the back-pressure signal.
  let gpuIdle = true;
  if (app.frameFence) {
    gpuIdle = gl.getSyncParameter(app.frameFence, gl.SYNC_STATUS) === gl.SIGNALED;
    if (gpuIdle) { gl.deleteSync(app.frameFence); app.frameFence = null; }
  }

  // 2. Stepping: as many generations as the adaptive budget allows.
  let steps = 0;
  if (app.playing) {
    if (gpuIdle) app.spf = Math.min(app.spf * 1.1 + 1, 200000); else app.spf = Math.max(1, app.spf * 0.7);
    const cap = gpuIdle ? Math.floor(app.spf) : 1;
    let want;
    if (app.runUntil > app.gen) want = app.runUntil - app.gen;
    else if (app.spec.speed === 'max') want = cap;
    else { app.acc = Math.min(app.acc + Number(app.spec.speed) * dt, Math.max(cap, 1)); want = Math.floor(app.acc); }
    steps = Math.min(want, cap);
    if (app.spec.speed !== 'max' && !(app.runUntil > app.gen)) app.acc -= steps;
    if (steps > 0) { app.sim.step(steps); app.gen += steps; }
    if (app.runUntil && app.gen >= app.runUntil) { app.runUntil = 0; if (!app.spec.play) setPlaying(false); app.statsDirty = true; }
  }

  // 3. Statistics on their own cadence; never blocking.
  const got = app.stats.poll();
  if (got) onStats(got.tag, got.stats);
  if (!app.stats.pending && (app.statsDirty || (app.playing && now - app.lastStatsStart > app.statsInterval))) {
    app.stats.start(app.sim.texture, app.gen);
    app.lastStatsStart = now; app.statsDirty = false;
  }

  // 4. Render at display rate.
  renderer.resetState();
  controls.update();
  view.update(app.sim.texture, camera, { faceScale: Number($('v-face').value), border: $('v-border').checked ? 1 : 0 });
  hullLines.visible = $('v-hull').checked;
  boxLines.visible = $('v-box').checked;
  renderer.render(scene, camera);
  if (!app.frameFence) app.frameFence = gl.fenceSync(gl.SYNC_GPU_COMMANDS_COMPLETE, 0);
  gl.flush();

  if (!app.lastUI || now - app.lastUI > 120) { app.lastUI = now; updateInstruments(now); }
}

// ---------------------------------------------------------------- UI wiring
const FORM = ['seed', 'n', 'k', 'H', 'shape', 'density', 'layers', 'rng', 'cells', 'box', 'bc'];
// 'auto': vertex-pulled quads cost ~18 vertices per cell slot every frame; the ray-marcher costs
// ~pixels x path length inside the hull. Quads up to ~2.7M cell slots, ray-march beyond.
function viewMode() {
  if (app.spec.view !== 'auto') return app.spec.view;
  return 3 * app.dims[0] * app.dims[1] * app.dims[2] <= 2.7e6 ? 'quads' : 'raymarch';
}
function syncForm() {
  for (const k of FORM) $('f-' + k).value = app.spec[k];
  $('speed').value = String(app.spec.speed);
  $('v-mode').value = app.spec.view;
  $('v-face').value = app.spec.face;
  view.setMode(viewMode());
  showSeedFields();
}
function showSeedFields() {
  const kind = $('f-seed').value;
  document.querySelectorAll('[data-for]').forEach(el => { el.style.display = el.dataset.for.split(' ').includes(kind) ? '' : 'none'; });
}
function readForm() {
  for (const k of FORM) { const v = $('f-' + k).value; app.spec[k] = NUMERIC.includes(k) ? Number(v) : v; }
}
$('f-seed').addEventListener('change', showSeedFields);
$('apply').addEventListener('click', () => { readForm(); app.spec.gen = 0; app.spec.play = 0; resetToSeed(); });
$('play').addEventListener('click', () => setPlaying(!app.playing));
$('step').addEventListener('click', stepOnce);
$('speed').addEventListener('change', () => { app.spec.speed = $('speed').value; app.acc = 0; writeURL(); });
$('v-mode').addEventListener('change', () => { app.spec.view = $('v-mode').value; view.setMode(viewMode()); writeURL(); });
$('v-face').addEventListener('input', () => { app.spec.face = Number($('v-face').value); writeURL(); });
$('share').addEventListener('click', async () => {
  const url = shareURL({ gen: app.gen, play: app.playing ? 1 : 0 });
  try { await navigator.clipboard.writeText(url); $('share').textContent = 'copied ✓'; } catch { prompt('link', url); }
  setTimeout(() => { $('share').textContent = 'copy link'; }, 1500);
});
$('resize').addEventListener('click', () => {
  const d = $('resizeN').value.split(/[,x ]+/).map(Number).filter(v => v > 0);
  if (d.length === 1 || d.length === 3) resizeTo(d.length === 1 ? [d[0], d[0], d[0]] : d);
});
$('fit').addEventListener('click', fitHull);
$('bcToggle').addEventListener('click', () => {
  const cells = app.sim.download();
  app.spec.bc = app.torus ? 'dead' : 'torus';
  buildSim(app.dims, !app.torus, cells);
  const h = hullOf(reembed(cells, app.dims, app.dims, [0, 0, 0], app.torus).pts);
  if (h && !hullFits(hullPolytope(h))) app.exact = false;
  writeURL(); syncForm();
});
window.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
  if (e.key === ' ') { e.preventDefault(); setPlaying(!app.playing); }
  else if (e.key === '.' || e.key === 'ArrowRight') stepOnce();
  else if (e.key >= '1' && e.key <= '9') { Object.assign(app.spec, { seed: 'key', k: Number(e.key), box: 'auto', gen: 0, play: 0 }); resetToSeed(); }
});

resize();
resetToSeed();
requestAnimationFrame(frame);
