// App shell. Three decoupled activities share one WebGL2 context:
//  - stepping: as many generations per frame as an adaptive budget allows (fence back-pressure);
//  - statistics: GPU reduction after every generation into a ring texture, read back
//    asynchronously (or, if switched off, sampled every ~40 ms);
//  - analysis: whole-state snapshots read back asynchronously and analysed in a worker
//    ({111} layer populations -> kymograph, firewalls), each tagged with its generation;
// and rendering at display rate. Plus UI, editor and URL state.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { Sim } from './gl/sim.js';
import { Stats, RING } from './gl/stats.js';
import { Bricks } from './gl/bricks.js';
import { Readback } from './gl/readback.js';
import { CellView, PALETTE } from './render.js';
import { makeSeed, autoBox, placeSeed, hullPolytope, reembed, hullOf } from './seeds.js';
import { DIAGONALS, DIAG_NAMES, layerRange, faceSites, faceLaw } from './layers.js';
import { Strip } from './strip.js';
import { Kymo } from './kymo.js';
import { Faces, FACE_NAMES } from './faces.js';
import { Editor } from './editor.js';
import { GROUPS } from './symmetry.js';
import { encodeCells, decodeCells, cellsToText } from './cellcodec.js';
import { loadGallery, findItem, describe, speedFor, renderGallery } from './gallery.js';
import { SCENES } from './tour.js';

const $ = (id) => document.getElementById(id);
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const fmt = (n) => n == null ? '–' : Math.round(n).toLocaleString('en-US');

// ---------------------------------------------------------------- URL / spec
const DEFAULTS = { seed: 'cube', n: 11, k: 5, H: 60, shape: 'cube', density: 0.3, layers: 3, rng: 1,
  box: 'auto', bc: 'dead', speed: 'max', view: 'auto', face: 0.6, gen: 0, play: 0, lanes: 32, cells: '', cz: '',
  abs: 0, g0: 0, cam: '', color: 'orientation', diag: 0, slice: '', ortho: 0, rec: 1, kwin: 0, focus: '', id: '', gap: 3, stride: 1 };
const NUMERIC = ['n', 'k', 'H', 'density', 'layers', 'gap', 'rng', 'face', 'gen', 'play', 'lanes', 'abs', 'g0', 'diag', 'ortho', 'rec', 'kwin', 'gap', 'stride'];
const VIEW_KEYS = ['box', 'bc', 'speed', 'view', 'face', 'gen', 'play', 'lanes', 'cam', 'color', 'diag', 'slice', 'ortho', 'rec', 'abs', 'g0', 'kwin', 'focus', 'stride'];

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
  if (spec.seed === 'cells') keys.push(spec.cz ? 'cz' : 'cells');
  if (spec.seed === 'atlas') keys.push('id');
  if (spec.seed === 'soup') keys.push('shape', 'n', 'density', 'rng', ...(spec.shape === 'slab' ? ['layers'] : []), ...(spec.shape === 'gap' ? ['gap'] : []));
  return keys;
}
function shareURL(extra = {}) {
  const s = { ...app.spec, ...extra };
  const q = new URLSearchParams();
  for (const k of seedKeys(s)) q.set(k, s[k]);
  for (const k of VIEW_KEYS) if (s[k] !== DEFAULTS[k]) q.set(k, s[k]);
  if (tour.open && !extra.noTour) { q.set('tour', tour.i); if (tour.v) q.set('v', tour.v); }
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
const persp = new THREE.PerspectiveCamera(40, 1, 0.1, 5000);
const ortho = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 5000);
let camera = persp;
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
  persp.aspect = w / h; persp.updateProjectionMatrix();
  fitOrtho();
}
function fitOrtho() {
  const w = parseFloat(canvas.style.width) || 1, h = parseFloat(canvas.style.height) || 1;
  const dist = camera.position.distanceTo(controls.target);
  const half = dist * Math.tan(THREE.MathUtils.degToRad(persp.fov / 2));
  ortho.left = -half * w / h; ortho.right = half * w / h; ortho.top = half; ortho.bottom = -half;
  ortho.updateProjectionMatrix();
}
window.addEventListener('resize', resize);

// ---------------------------------------------------------------- app state
const app = {
  spec: readURL(),
  sim: null, stats: null, bricks: null, dims: null, torus: false, simId: 0,
  gen: 0, playing: false, runUntil: 0,
  spf: 1, acc: 0, frameFence: null,
  last: null, initialHull: null, prevHull: null, events: [], hullPoly: null,
  stepsWindow: [], lastFrame: performance.now(), frameTimes: [],
  statsInterval: 40, lastStatsStart: 0, statsDirty: true, bricksDirty: true,
  rec: true, snap: { pending: false, busy: false, last: 0, interval: 30, ms: 0, lastGen: -1 },
  diag: 0, slice: { on: false, lo: 0, hi: 0 }, edit: null,
};
app.rec = !!app.spec.rec;
app.diag = Math.min(3, Math.max(0, app.spec.diag | 0));
const strip = new Strip($('strip'));
const kymo = new Kymo($('kymo'), $('kprof'), $('k-label'), { onPickLayer: (n, s) => { setDiag(n); setSlice(true, s, s); } });
const editor = new Editor();
const faces = new Faces($('faces'));
const snapRB = new Readback(gl);
const worker = new Worker(new URL('./analysis-worker.js', import.meta.url), { type: 'module' });
window.gump = app;   // for tests / console poking
app.three = { renderer, scene, get camera() { return camera; }, view, gl };
app.kymo = kymo; app.editor = editor; app.faces = faces;

function buildSim(dims, torus, cells) {
  if (app.sim) { app.stats.dispose(); app.sim.dispose(); app.bricks.dispose(); }
  app.dims = dims; app.torus = torus; app.simId++;
  app.sim = new Sim(gl, dims[0], dims[1], dims[2], { torus, maxLanes: app.spec.lanes });
  app.stats = new Stats(gl, app.sim.layout);
  app.bricks = new Bricks(gl, app.sim.layout);
  // brick skipping measured 0.85-1.75x under SwiftShader (the hull clip already removes most empty
  // space); it only pays in bigger boxes
  app.useBricks = Math.max(...dims) > 48;
  app.sim.upload(cells);
  renderer.resetState();
  view.setLayout(app.sim.layout, app.bricks.layout);
  view.setMode(viewMode());
  boxLines.geometry.dispose();
  boxLines.geometry = new THREE.EdgesGeometry(new THREE.BoxGeometry(dims[0], dims[1], dims[2]));
  app.statsDirty = true; app.bricksDirty = true;
  app.snap.pending = false; app.snap.lastGen = -1;
  kymo.clear();
  view.setHullClip(null);      // re-armed by the first statistics of this state
  updateBoxInfo();
}
// Statistics of the generation the sim now holds (after reset, edit, resize).
function statsNow() { if (app.rec) app.stats.record(app.sim.texture, app.gen); else app.statsDirty = true; }

function boxFromSpec(spec, pts) {
  if (spec.seed === 'legacy' && spec.box === 'auto' && spec.H % 2 === 0 && spec.bc === 'torus')
    return { dims: [spec.H / 2, spec.H / 2, spec.H / 2], shift: [0, 0, 0] };   // the original's array torus
  const d = String(spec.box).split(/[,x]/).map(Number).filter(v => v > 0);
  const given = spec.box !== 'auto' && d.length ? (d.length === 3 ? d : [d[0], d[0], d[0]]) : null;
  if (spec.abs && given) return { dims: given, shift: [0, 0, 0] };              // absolute array coordinates
  const auto = autoBox(pts);
  if (!given) return auto;
  // centre the seed: keep auto's centring relative to the box centre
  return { dims: given, shift: given.map((N, t) => auto.shift[t] + 2 * Math.floor((N - auto.dims[t]) / 2)) };
}

async function resetToSeed() {
  const spec = app.spec;
  let seed;
  if (spec.seed === 'cells' && spec.cz) {
    try { const pts = await decodeCells(spec.cz); seed = { pts, name: `${pts.length / 3} cells (from link)` }; }
    catch (e) { seed = { pts: new Int32Array(0), name: 'unreadable cell link' }; }
  } else if (spec.seed === 'atlas') {
    await loadGallery();
    const it = findItem(spec.id);
    seed = it ? { pts: Int32Array.from(it.cells.flat()), name: `atlas ${it.id}` } : { pts: new Int32Array(0), name: `unknown atlas object ${spec.id}` };
    app.atlas = it;
  } else seed = makeSeed(spec);
  if (spec.seed !== 'atlas') app.atlas = null;
  if (app.edit) leaveEdit(false);
  const { dims, shift } = boxFromSpec(spec, seed.pts);
  const cells = new Uint8Array(dims[0] * dims[1] * dims[2]);
  const dropped = placeSeed(seed.pts, dims, shift, spec.bc === 'torus', cells);
  const h0 = hullOf(seed.pts);
  buildSim(dims, spec.bc === 'torus', cells);
  app.seedName = seed.name + (dropped ? ` (${dropped} cells did not fit)` : '');
  app.gen = spec.g0 || 0; app.acc = 0; app.initialGen = app.gen;
  app.initialHull = null; app.prevHull = null; app.events = []; app.last = null; app.faceS = null; app.symmetric = null;
  // T2: if the seed's hull fits the box, the run is the infinite-space run forever. Cleared for
  // good by anything that may have let the boundary act (seed clipped, resize below the hull).
  app.exact = !dropped && (!h0 || hullFits(hullPolytope({ loS: h0.loS.map((v, n) => v + dot(DIAGONALS[n], shift)), hiS: h0.hiS.map((v, n) => v + dot(DIAGONALS[n], shift)) })));
  strip.clear(); faces.clear();
  statsNow();
  app.runUntil = spec.gen > app.gen ? spec.gen : 0;
  setPlaying(!!spec.play || app.runUntil > 0);
  frameCamera(seed.pts.length ? seed.pts.map((v, i) => v + shift[i % 3]) : null);
  applySliceFromSpec();
  setFocus(defaultFocus());
  writeURL();
  syncForm();
}

let framedR = 10;
function frameCamera(pts) {
  // frame the seed's hull (what can ever be alive), not the whole box
  let r = 0.5 * Math.hypot(...app.dims);
  const h = pts && pts.length ? hullOf(pts) : null;
  if (h) { const poly = hullPolytope(h); r = Math.min(r, 0.25 * Math.hypot(...[0, 1, 2].map(t => poly.hi[t] - poly.lo[t] + 2)) + 1); }
  framedR = r;
  const c = String(app.spec.cam || '').split(',').map(Number);
  const dir = (c.length >= 3 && c.every(Number.isFinite) ? new THREE.Vector3(c[0], c[1], c[2]) : new THREE.Vector3(1.0, 0.75, 1.35)).normalize();
  const zoom = c.length === 4 && c[3] > 0 ? c[3] : 1;
  placeCamera(dir, r / Math.sin(THREE.MathUtils.degToRad(persp.fov / 2)) * 0.8 / zoom);
}
function placeCamera(dir, dist) {
  for (const cam of [persp, ortho]) {
    cam.position.copy(dir.clone().normalize().multiplyScalar(dist));
    cam.near = framedR * 0.01; cam.far = framedR * 40; cam.updateProjectionMatrix();
  }
  ortho.zoom = 1;
  controls.target.set(0, 0, 0);
  fitOrtho();
  controls.update();
}
let viewShift = 0;
function centreView() {
  const w = parseFloat(canvas.style.width) || 1, h = parseFloat(canvas.style.height) || 1;
  const over = ['tour', 'gallery', 'objcard'].map(id => $(id)).find(el => el.classList.contains('open'));
  const dx = over && window.innerWidth > 900 ? Math.round((over.offsetWidth + 8) / 2) : 0;
  if (dx === viewShift && (!dx || (persp.view && persp.view.fullWidth === w && persp.view.fullHeight === h))) return;
  viewShift = dx;
  for (const cam of [persp, ortho]) { if (dx) cam.setViewOffset(w, h, -dx, 0, w, h); else cam.clearViewOffset(); }
}
function setOrtho(on) {
  const next = on ? ortho : persp;
  if (next === camera) return;
  next.position.copy(camera.position); next.up.copy(camera.up);
  camera = next; controls.object = camera;
  app.spec.ortho = on ? 1 : 0;
  fitOrtho(); controls.update();
}
function lookAlong() {
  const d = new THREE.Vector3(...DIAGONALS[app.diag]);
  placeCamera(d, camera.position.distanceTo(controls.target) || framedR * 3);
}

function setPlaying(p) {
  if (p && app.edit) leaveEdit(true);
  if (p && !app.playing) app.stepsWindow = [];
  app.playing = p; $('play').textContent = p ? '❚❚ pause' : '▶ play';
}

// stride K: one displayed step is K generations (speed counts displayed steps); max speed ignores it
const stride = () => Math.max(1, Math.floor(Number(app.spec.speed === 'max' ? 1 : app.spec.stride) || 1));
function stepOnce() {
  if (app.edit) leaveEdit(true);
  setPlaying(false); app.runUntil = 0;
  const k = stride();
  if (app.rec && k > 1) for (let i = 0; i < k; i++) { app.sim.step(1); app.gen++; app.stats.record(app.sim.texture, app.gen); }
  else { app.sim.step(k); app.gen += k; }
  app.bricksDirty = true; statsNow();
}

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
  if (app.slice.on) { const ds = dot(DIAGONALS[app.diag], shift); app.slice.lo += ds; app.slice.hi += ds; }
  app.spec.box = dims.join('x');
  if (r.dropped) pushEvent(`resize dropped ${r.dropped} live cells`);
  pushEvent(`gen ${fmt(app.gen)}: resized to ${dims.join('×')} (layer history restarts)`);
  statsNow();
  frameCamera(r.pts); applySlice(); writeURL(); syncForm();
}
function fitHull() {
  const cells = app.sim.download();
  const r = reembed(cells, app.dims, app.dims, [0, 0, 0], app.torus);
  if (!r.pts.length) return;
  const box = autoBox(r.pts);
  resizeTo(box.dims, box.shift);
}

// ---------------------------------------------------------------- statistics → instruments
function pushEvent(msg) { app.events.unshift(msg); app.events.length = Math.min(app.events.length, 200); }

// One generation's statistics (every generation when recording; samples otherwise).
function onStats(gen, s, exact) {
  app.last = { gen, s, exact };
  strip.add(gen, s.pop, s.count);
  if (s.faceHi) faces.add(gen, [...s.faceHi, ...s.faceLo], exact);
  if (!(s.pop && s.loS)) {
    if (app.hullPoly) { hullLines.geometry.setDrawRange(0, 0); app.hullPoly = null; }
    return;
  }
  const p = app.prevHull;
  if (p && s.loS.every((v, n) => v === p.loS[n]) && s.hiS.every((v, n) => v === p.hiS[n])) return;
  const h = { loS: s.loS.slice(), hiS: s.hiS.slice() };
  if (!app.initialHull) app.initialHull = h;
  if (p) {
    const at = exact ? `gen ${fmt(gen)}` : `gen ≤${fmt(gen)}`;
    DIAGONALS.forEach((d, n) => {
      // the outermost layer of a face went extinct (permanently, T2); its last population is in the previous sample
      const lastPop = (q) => { const v = faces.val[q]; return v.length > 1 ? v[v.length - 2] : '?'; };
      const before = exact ? 'the generation before' : 'at the previous sample';
      if (h.hiS[n] < p.hiS[n]) { pushEvent(`${at}: face ${FACE_NAMES[n]} layer s=${p.hiS[n]} extinct (held ${lastPop(n)} cells ${before}); max s → ${h.hiS[n]}`); kymo.mark(gen, n); faces.extinct(gen, n); }
      if (h.loS[n] > p.loS[n]) { pushEvent(`${at}: face ${FACE_NAMES[n + 4]} layer s=${p.loS[n]} extinct (held ${lastPop(n + 4)} cells ${before}); min s → ${h.loS[n]}`); kymo.mark(gen, n); faces.extinct(gen, n + 4); }
    });
  }
  app.prevHull = h;
  // face areas A (sites of each outermost layer inside the hull) and when each face's layer became outermost
  const fs = faceSites(app.dims, h);
  app.faceA = [...fs.hi, ...fs.lo];
  const sNow = [...h.hiS, ...h.loS];
  if (!app.faceS) app.faceSince = sNow.map(() => gen);
  else app.faceSince = sNow.map((v, q) => v === app.faceS[q] ? app.faceSince[q] : gen);
  app.faceS = sNow;
  if (!app.torus) view.setHullClip(h);
  const poly = hullPolytope(h);
  const pos = [];
  for (const [a, b] of poly.edges) for (const v of [poly.verts[a], poly.verts[b]])
    pos.push(v[0] / 2 + 0.5 - app.dims[0] / 2, v[1] / 2 + 0.5 - app.dims[1] / 2, v[2] / 2 + 0.5 - app.dims[2] / 2);
  hullLines.geometry.dispose();
  hullLines.geometry = new THREE.BufferGeometry();
  hullLines.geometry.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  app.hullPoly = poly;
}

// Whole-state snapshots -> worker -> {111} layer populations.
worker.onmessage = (e) => {
  const { id, gen, diags, ms } = e.data;
  app.snap.busy = false;
  app.snap.ms = ms;
  app.snap.interval = Math.max(30, 3 * ms);
  if (id !== app.simId) return;
  if (e.data.symmetric !== null && e.data.symmetric !== undefined) app.symmetric = { value: e.data.symmetric, gen };
  for (const f of kymo.add(gen, diags))
    pushEvent(`gen ≤${fmt(gen)}: firewall along ${DIAG_NAMES[f.diag]}, empty layers s ${f.from}…${f.to} (T3: permanent)`);
  app.layerGen = gen;
};
function snapshots(now) {
  for (const job of snapRB.poll()) {
    app.snap.pending = false;
    if (job.tag.simId !== app.simId) continue;
    app.snap.busy = true;
    worker.postMessage({ id: job.tag.simId, gen: job.tag.gen, layout: app.sim.layout, texels: job.data }, [job.data.buffer]);
  }
  if (app.snap.pending || app.snap.busy || now - app.snap.last < app.snap.interval || app.snap.lastGen === app.gen) return;
  const L = app.sim.layout;
  snapRB.start([{ fb: app.sim.framebuffer, x: 0, y: 0, w: L.width, h: L.height }], { gen: app.gen, simId: app.simId });
  app.snap.pending = true; app.snap.last = now; app.snap.lastGen = app.gen;
}

function updateBoxInfo() {
  const L = app.sim.layout;
  $('boxinfo').innerHTML = `${app.dims.join('×')} cubes, ${app.torus ? 'torus' : 'dead outside'} · ${fmt(3 * app.dims[0] * app.dims[1] * app.dims[2])} cells<br>` +
    `<span class="dim">${L.LANES} lanes/word · atlas ${L.width}×${L.height} · ${app.seedName || ''}</span>`;
  $('bcToggle').textContent = app.torus ? '⇄ dead outside' : '⇄ torus';
}

function updateInstruments(now) {
  $('gen').textContent = fmt(app.gen);
  const w = app.stepsWindow; w.push([now, app.gen]);
  while (w.length > 2 && now - w[1][0] > 1000) w.shift();
  const gps = w.length > 1 && now > w[0][0] ? (app.gen - w[0][1]) / (now - w[0][0]) * 1000 : 0;
  $('gps').textContent = app.edit ? 'editing' : app.playing ? (gps >= 100 ? fmt(gps) : gps.toFixed(1)) : 'paused';
  const ft = app.frameTimes; const fps = ft.length > 1 ? 1000 * (ft.length - 1) / (ft[ft.length - 1] - ft[0]) : 0;
  $('spf').textContent = `${Math.round(app.spf)} gens/frame budget`;
  $('fps').textContent = `${fps.toFixed(0)} fps`;
  const last = app.last;
  if (last) {
    const s = last.s;
    $('pop').textContent = fmt(s.pop);
    $('density').textContent = (s.pop / (3 * app.dims[0] * app.dims[1] * app.dims[2])).toFixed(4);
    $('popx').textContent = fmt(s.count[0]); $('popy').textContent = fmt(s.count[1]); $('popz').textContent = fmt(s.count[2]);
    const lag = app.gen - last.gen;
    $('statsage').textContent = (app.rec ? 'statistics of every generation' : 'statistics sampled every ~40 ms') +
      (lag ? ` · shown: gen ${fmt(last.gen)} (${fmt(lag)} behind)` : ' · current');
    hullTable(s);
    edgeStatus(s);
  }
  const lg = app.layerGen;
  $('k-foot').title = lg != null ? `layer analysis of gen ${lg} took ${app.snap.ms.toFixed(1)} ms in the worker` : '';
  $('hullevents').innerHTML = app.events.slice(0, 60).map(e => `<div>${e}</div>`).join('');
  $('legend').innerHTML = legend();
  faceTable();
  objCard();
  strip.draw();
  faces.draw();
  kymo.draw();
}

function legend() {
  const sw = (c) => `<i class="sw" style="background:rgb(${c.join(',')})"></i>`;
  const m = app.spec.color;
  if (m === 'layer') return `${sw(PALETTE.abc[0])}A ${sw(PALETTE.abc[1])}B ${sw(PALETTE.abc[2])}C — kagome layers along ${DIAG_NAMES[app.diag]}, by (s−1)/2 mod 3`;
  if (m === 'fate') return `from each cell's live-neighbour count n: ${sw(PALETTE.x.map(v => Math.round(v * 0.6)))}survives (n = 3–5) · ${sw(PALETTE.dies)}dies next · ${sw(PALETTE.born)}born next (n = 4, 5) · ${sw(PALETTE.near)}<i>outline</i>: dead with n = 3, one live neighbour short of birth`;
  if (m === 'neighbourhood') return `click any face to focus it. ${sw(PALETTE.focus)}focus and its 12 neighbours by layer offset Δs along ${DIAG_NAMES[app.diag]}: ${PALETTE.ds.map((c, i) => sw(c) + (['−4 (1)', '−2 (2)', '0 (6)', '+2 (2)', '+4 (1)'][i])).join(' ')} — full size = live, smaller = dead`;
  if (m === 'change') return `${sw(PALETTE.born)}born this generation · ${sw(PALETTE.x.map(v => Math.round(v * 0.55)))}survived (dimmed orientation colour) · ${sw(PALETTE.died)}died (small)`;
  return `${sw(PALETTE.x)}x-normal ${sw(PALETTE.y)}y-normal ${sw(PALETTE.z)}z-normal`;
}

function hullTable(s) {
  const rows = ['<tr><th>d</th><th>min s</th><th>max s</th><th>layers</th><th>start</th></tr>'];
  DIAGONALS.forEach((d, n) => {
    const name = DIAG_NAMES[n];
    if (!s.loS) { rows.push(`<tr><td>${name}</td><td colspan=4>empty</td></tr>`); return; }
    const i0 = app.initialHull;
    const w = (s.hiS[n] - s.loS[n]) / 2 + 1, w0 = i0 ? (i0.hiS[n] - i0.loS[n]) / 2 + 1 : w;
    const cl = (b) => b ? ' class="shrunk"' : '';
    rows.push(`<tr${n === app.diag ? ' class="sel"' : ''}><td>${name}</td><td${cl(i0 && s.loS[n] > i0.loS[n])}>${s.loS[n]}</td><td${cl(i0 && s.hiS[n] < i0.hiS[n])}>${s.hiS[n]}</td><td${cl(w < w0)}>${w}</td><td class="dim">${w0}</td></tr>`);
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
  if (app.playing && !app.edit) {
    // grow only when the budget was the limiting factor last frame
    if (gpuIdle) { if (app.budgetBound) app.spf = Math.min(app.spf * 1.1 + 1, 200000); } else app.spf = Math.max(1, app.spf * 0.7);
    let cap = gpuIdle ? Math.floor(app.spf) : 1;
    if (app.rec) cap = Math.min(cap, RING - 1 - app.stats.unflushed);
    let want;
    if (app.runUntil > app.gen && app.spec.speed === 'max') want = app.runUntil - app.gen;
    else if (app.spec.speed === 'max') want = cap;
    else { app.acc = Math.min(app.acc + Number(app.spec.speed) * dt, Math.max(cap, 1)); want = Math.floor(app.acc) * stride(); }
    let steps = Math.max(0, Math.min(want, cap, app.runUntil > app.gen ? app.runUntil - app.gen : Infinity));
    if (!app.runUntil && stride() > 1) steps -= steps % stride();   // whole displayed steps only, so phases stay aligned
    app.budgetBound = want >= cap;
    if (app.spec.speed !== 'max') app.acc -= steps / stride();
    if (steps > 0) {
      if (app.rec) for (let i = 0; i < steps; i++) { app.sim.step(1); app.gen++; app.stats.record(app.sim.texture, app.gen); }
      else { app.sim.step(steps); app.gen += steps; }
      app.bricksDirty = true;
    }
    if (app.runUntil && app.gen >= app.runUntil) { app.runUntil = 0; if (!app.spec.play) setPlaying(false); statsNow(); }
  }

  // 3. Statistics: flush this frame's ring slots; collect whatever has landed. Never blocks.
  if (app.rec) app.stats.flush();
  const got = app.stats.poll();
  for (const x of got.samples) onStats(x.gen, x.stats, true);
  if (got.sample) onStats(got.sample.tag, got.sample.stats, false);
  if (!app.rec && !app.stats.pending && (app.statsDirty || (app.playing && now - app.lastStatsStart > app.statsInterval))) {
    app.stats.start(app.sim.texture, app.gen);
    app.lastStatsStart = now; app.statsDirty = false;
  }

  // 4. Layer analysis on its own cadence (snapshot -> worker).
  snapshots(now);

  // 5. Render at display rate (centred in the part of the canvas not covered by a left overlay).
  centreView();
  renderer.resetState();
  controls.update();
  const ray = view.drawn === 'raymarch';
  if (ray && app.useBricks && app.bricksDirty) { app.bricks.update(app.sim.texture, app.sim.prevTexture, app.spec.color === 'change'); app.bricksDirty = false; renderer.resetState(); }
  view.update(app.sim, app.bricks.tex, ray && app.useBricks, camera, { faceScale: Number($('v-face').value), border: $('v-border').checked ? 1 : 0 });
  hullLines.visible = $('v-hull').checked;
  boxLines.visible = $('v-box').checked;
  renderer.render(scene, camera);
  if (!app.frameFence) app.frameFence = gl.fenceSync(gl.SYNC_GPU_COMMANDS_COMPLETE, 0);
  gl.flush();

  if (!app.lastUI || now - app.lastUI > 120) { app.lastUI = now; updateInstruments(now); }
}

// ---------------------------------------------------------------- diagonal, slicer, colour
function setDiag(n) {
  app.diag = n; app.spec.diag = n;
  for (const el of document.querySelectorAll('select.diag')) el.value = String(n);
  kymo.setDiag(n);
  view.setLayerDiag(DIAGONALS[n]);
  if (app.slice.on) { const s = clampSlice(app.slice.lo, app.slice.hi); app.slice.lo = s[0]; app.slice.hi = s[1]; }
  if (app.edit && app.edit.kind === 'layer') { app.edit.d = DIAGONALS[n]; clampEdit(); }
  applySlice(); writeURL();
}
function clampSlice(lo, hi) {
  const r = layerRange(app.dims, DIAGONALS[app.diag]);
  const top = r.base + 2 * (r.count - 1);
  const fix = (v) => { v = Math.round(v); if (!(v & 1)) v += 1; return Math.min(top, Math.max(r.base, v)); };
  lo = fix(lo); hi = fix(hi);
  return lo <= hi ? [lo, hi] : [hi, lo];
}
function setSlice(on, lo = app.slice.lo, hi = app.slice.hi) {
  [lo, hi] = clampSlice(lo, hi);
  app.slice = { on, lo, hi };
  applySlice(); writeURL();
}
function applySlice() {
  const s = app.slice;
  view.setLayerDiag(DIAGONALS[app.diag]);
  view.setSlice(s.on ? { d: DIAGONALS[app.diag], lo: s.lo, hi: s.hi } : null);
  kymo.setSlice(s.on ? { diag: app.diag, lo: s.lo, hi: s.hi } : null);
  app.spec.slice = s.on ? `${s.lo},${s.hi}` : '';
  $('s-on').checked = s.on; $('s-lo').value = s.lo; $('s-hi').value = s.hi;
}
function applySliceFromSpec() {
  const v = String(app.spec.slice || '').split(',').map(Number);
  setDiag(app.diag);
  if (v.length === 2 && v.every(Number.isFinite)) setSlice(true, v[0], v[1]);
  else { const h = app.last && app.last.s.loS; setSlice(false, h ? h[app.diag] : 1, h ? h[app.diag] : 1); }
}
function moveSlice(k) { setSlice(true, app.slice.lo + 2 * k, app.slice.hi + 2 * k); }
function hullS() { const s = app.last && app.last.s; return s && s.loS ? [s.loS[app.diag], s.hiS[app.diag]] : null; }

// ---------------------------------------------------------------- editor
function editSetFromUI() {
  const kind = $('e-kind').value;
  return kind === 'plane' ? { kind, axis: Number($('e-axis').value), coord: Number($('e-coord').value) }
    : { kind, d: DIAGONALS[app.diag], s: Number($('e-coord').value) };
}
function clampEdit() {
  const set = app.edit, r = Editor.range(set, app.dims);
  const key = set.kind === 'plane' ? 'coord' : 's';
  let v = Math.round(set[key]); if (!(v & 1)) v += 1;
  set[key] = Math.min(r.hi, Math.max(r.lo, v));
  $('e-coord').value = set[key];
  view.setEdit(set);
  document.querySelectorAll('[data-e]').forEach(el => { el.style.display = set.kind === el.dataset.e ? '' : 'none'; });
}
function enterEdit() {
  if (app.edit) return;
  setPlaying(false); app.runUntil = 0;
  editor.begin(app.sim.download(), app.dims);
  editor.group = $('e-sym').value;
  const c = editor.centre;
  // start on the set through the pattern's centre
  const kind = $('e-kind').value;
  app.edit = kind === 'plane' ? { kind, axis: Number($('e-axis').value), coord: 0 } : { kind, d: DIAGONALS[app.diag], s: 0 };
  if (kind === 'plane') { const v = c[app.edit.axis]; app.edit.coord = (v & 1) ? v : v + 1; }
  else app.edit.s = dot(DIAGONALS[app.diag], c) | 1;
  clampEdit();
  $('editsec').classList.add('on'); $('e-toggle').textContent = '✓ done';
  $('e-centre').textContent = `centre ${c.join(',')}`;
  view.setMode(viewMode());
  $('e-status').textContent = '';
}
function editChanged() {
  app.sim.upload(editor.cells);
  app.bricksDirty = true; app.edited = true;
  app.prevHull = null; app.initialHull = null; app.faceS = null; app.faceA = null; app.symmetric = null;   // an edit can grow the hull: restart the bookkeeping
  statsNow();
}
async function leaveEdit(keep = true) {
  if (!app.edit) return;
  app.edit = null;
  view.setEdit(null); view.setMode(viewMode());
  $('editsec').classList.remove('on'); $('e-toggle').textContent = '✎ edit';
  const cells = editor.end();
  if (!keep || !app.edited) return;
  app.edited = false;
  // the edited state becomes the run's seed: absolute array coordinates in this box, from this generation
  const r = reembed(cells, app.dims, app.dims, [0, 0, 0], app.torus);
  const h = hullOf(r.pts);
  app.exact = !h || hullFits(hullPolytope(h));
  pushEvent(`gen ${fmt(app.gen)}: state edited (${r.pts.length / 3} cells); hull bookkeeping restarts`);
  Object.assign(app.spec, { seed: 'cells', box: app.dims.join('x'), abs: 1, g0: app.gen, bc: app.torus ? 'torus' : 'dead' });
  if (r.pts.length / 3 <= 40) { app.spec.cells = cellsToText(r.pts); app.spec.cz = ''; }
  else { app.spec.cz = await encodeCells(r.pts); app.spec.cells = ''; }
  app.seedName = `edited state, ${r.pts.length / 3} cells`;
  updateBoxInfo(); writeURL(); syncForm();
}
function onEditClick(e) {
  const [o, d] = cubeRay(e);
  const hit = editor.pick(o, d, app.edit);
  if (!hit) return;
  const n = editor.toggle(hit.p, DIAGONALS[app.diag]);
  $('e-status').textContent = `${hit.p.join(',')} ${n > 1 ? `(+${n - 1} by symmetry)` : ''}`;
  editChanged();
}

// ---------------------------------------------------------------- UI wiring
const FORM = ['seed', 'n', 'k', 'H', 'shape', 'density', 'layers', 'gap', 'rng', 'cells', 'id', 'box', 'bc'];
// 'auto': vertex-pulled quads cost ~18 vertices per cell slot every frame; the ray-marcher costs
// ~pixels x path length inside the hull, minus empty bricks. Quads up to ~2.7M slots.
function viewMode() {
  if (app.spec.view !== 'auto') return app.spec.view;
  return 3 * app.dims[0] * app.dims[1] * app.dims[2] <= 2.7e6 ? 'quads' : 'raymarch';
}
function syncForm() {
  for (const k of FORM) $('f-' + k).value = app.spec[k];
  $('speed').value = String(app.spec.speed);
  const st = $('stride');
  if (![...st.options].some(o => o.value === String(app.spec.stride))) st.add(new Option(String(app.spec.stride), String(app.spec.stride)));
  st.value = String(app.spec.stride);
  $('v-mode').value = app.spec.view;
  $('v-face').value = app.spec.face;
  $('v-color').value = app.spec.color;
  $('v-ortho').checked = !!app.spec.ortho;
  $('rec').checked = app.rec;
  $('k-win').value = String(app.spec.kwin); kymo.setWindow(app.spec.kwin);
  view.setColorMode(app.spec.color);
  view.setMode(viewMode());
  showSeedFields();
}
function showSeedFields() {
  const kind = $('f-seed').value;
  document.querySelectorAll('[data-for]').forEach(el => { el.style.display = el.dataset.for.split(' ').includes(kind) ? '' : 'none'; });
}
function readForm() {
  for (const k of FORM) { const v = $('f-' + k).value; app.spec[k] = NUMERIC.includes(k) ? Number(v) : v; }
  app.spec.cz = ''; app.spec.abs = 0; app.spec.g0 = 0;
}
for (const el of document.querySelectorAll('select.diag')) {
  el.innerHTML = DIAG_NAMES.map((n, i) => `<option value="${i}">${n}</option>`).join('');
  el.addEventListener('change', () => setDiag(Number(el.value)));
}
$('e-sym').innerHTML = Object.entries(GROUPS).map(([k, g]) => `<option value="${k}">${g.label}</option>`).join('');
$('f-seed').addEventListener('change', showSeedFields);
$('apply').addEventListener('click', () => { readForm(); app.spec.gen = 0; app.spec.play = 0; resetToSeed(); });
$('play').addEventListener('click', () => setPlaying(!app.playing));
$('step').addEventListener('click', stepOnce);
$('speed').addEventListener('change', () => { app.spec.speed = $('speed').value; app.acc = 0; writeURL(); });
$('stride').addEventListener('change', () => { app.spec.stride = Number($('stride').value); app.acc = 0; writeURL(); });
$('rec').addEventListener('change', () => { app.stats.flush(); app.rec = $('rec').checked; app.spec.rec = app.rec ? 1 : 0; statsNow(); writeURL(); });
$('v-mode').addEventListener('change', () => { app.spec.view = $('v-mode').value; view.setMode(viewMode()); writeURL(); });
$('v-color').addEventListener('change', () => { app.spec.color = $('v-color').value; view.setColorMode(app.spec.color); app.bricksDirty = true; writeURL(); });
$('v-face').addEventListener('input', () => { app.spec.face = Number($('v-face').value); writeURL(); });
$('v-ortho').addEventListener('change', () => { setOrtho($('v-ortho').checked); writeURL(); });
$('v-along').addEventListener('click', lookAlong);
$('v-reset').addEventListener('click', () => { app.spec.cam = ''; frameCamera(null); });
$('s-on').addEventListener('change', () => setSlice($('s-on').checked));
$('s-lo').addEventListener('change', () => setSlice(true, Number($('s-lo').value), Math.max(Number($('s-lo').value), app.slice.hi)));
$('s-hi').addEventListener('change', () => setSlice(true, Math.min(app.slice.lo, Number($('s-hi').value)), Number($('s-hi').value)));
$('s-up').addEventListener('click', () => moveSlice(1));
$('s-down').addEventListener('click', () => moveSlice(-1));
$('s-one').addEventListener('click', () => setSlice(true, app.slice.lo, app.slice.lo));
$('s-facehi').addEventListener('click', () => { const h = hullS(); if (h) setSlice(true, h[1], h[1]); });
$('s-facelo').addEventListener('click', () => { const h = hullS(); if (h) setSlice(true, h[0], h[0]); });
$('s-all').addEventListener('click', () => { const h = hullS(); if (h) setSlice(true, h[0], h[1]); });
$('k-mode').addEventListener('change', () => kymo.setMode($('k-mode').value));
$('k-win').addEventListener('change', () => { app.spec.kwin = Number($('k-win').value); kymo.setWindow(app.spec.kwin); writeURL(); });
$('k-hide').addEventListener('click', () => { $('layers').classList.toggle('collapsed'); $('k-hide').textContent = $('layers').classList.contains('collapsed') ? '+' : '–'; });
$('share').addEventListener('click', async () => {
  const url = shareURL({ gen: app.gen, play: app.playing ? 1 : 0, noTour: true });
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
  statsNow(); writeURL(); syncForm();
});
// editor
$('e-toggle').addEventListener('click', () => app.edit ? leaveEdit(true) : enterEdit());
$('e-kind').addEventListener('change', () => { if (app.edit) { const old = app.edit; app.edit = editSetFromUI(); if (app.edit.kind !== old.kind) { const c = editor.centre; if (app.edit.kind === 'plane') app.edit.coord = c[app.edit.axis] | 1; else app.edit.s = dot(DIAGONALS[app.diag], c) | 1; } clampEdit(); } });
$('e-axis').addEventListener('change', () => { if (app.edit) { app.edit.axis = Number($('e-axis').value); app.edit.coord = editor.centre[app.edit.axis] | 1; clampEdit(); } });
$('e-coord').addEventListener('change', () => { if (app.edit) { app.edit[app.edit.kind === 'plane' ? 'coord' : 's'] = Number($('e-coord').value); clampEdit(); } });
const moveEdit = (k) => { if (!app.edit) return; app.edit[app.edit.kind === 'plane' ? 'coord' : 's'] += 2 * k; clampEdit(); };
$('e-up').addEventListener('click', () => moveEdit(1));
$('e-down').addEventListener('click', () => moveEdit(-1));
$('e-sym').addEventListener('change', () => { editor.group = $('e-sym').value; });
$('e-fill').addEventListener('click', () => { if (app.edit && editor.fillSet(app.edit, 1)) editChanged(); });
$('e-rand').addEventListener('click', () => { if (app.edit && editor.fillSet(app.edit, 1, Number($('e-rho').value))) editChanged(); });
$('e-clearset').addEventListener('click', () => { if (app.edit && editor.fillSet(app.edit, 0)) editChanged(); });
$('e-clear').addEventListener('click', () => { if (app.edit) { editor.clearAll(); editChanged(); } });
$('e-undo').addEventListener('click', () => { if (app.edit && editor.undo()) editChanged(); });
$('e-run').addEventListener('click', async () => { await leaveEdit(true); setPlaying(true); });
let down = null;
canvas.addEventListener('pointerdown', (e) => { down = [e.clientX, e.clientY]; });
canvas.addEventListener('pointerup', (e) => {
  const click = down && Math.hypot(e.clientX - down[0], e.clientY - down[1]) < 4;
  down = null;
  if (!click) return;
  if (app.edit) onEditClick(e);
  else if (app.spec.color === 'neighbourhood') { const hit = pickAny(e); if (hit) setFocus(hit.p); }
});
function cubeRay(e) {
  const rect = canvas.getBoundingClientRect();
  const ndc = new THREE.Vector2(((e.clientX - rect.left) / rect.width) * 2 - 1, -((e.clientY - rect.top) / rect.height) * 2 + 1);
  const rc = new THREE.Raycaster(); rc.setFromCamera(ndc, camera);
  const o = rc.ray.origin, d = rc.ray.direction;
  return [[o.x + app.dims[0] / 2, o.y + app.dims[1] / 2, o.z + app.dims[2] / 2], [d.x, d.y, d.z]];
}
// first slot (live or dead) under the cursor
function pickAny(e) { editor.dims = app.dims; const [o, d] = cubeRay(e); return editor.pick(o, d, { kind: 'any' }, 0.5 * Number($('v-face').value)); }
function setFocus(p) { app.focus = p; app.spec.focus = p.join(','); view.setFocus(p); writeURL(); }
function defaultFocus() {
  const v = String(app.spec.focus || '').split(',').map(Number);
  if (v.length === 3 && v.every(Number.isInteger) && ((v[0] & 1) + (v[1] & 1) + (v[2] & 1)) === 1) return v;
  return [2 * Math.floor(app.dims[0] / 2) + 1, 2 * Math.floor(app.dims[1] / 2), 2 * Math.floor(app.dims[2] / 2)];
}
window.addEventListener('keydown', async (e) => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
  if (app.edit) {
    if (e.key === 'ArrowUp') { e.preventDefault(); return moveEdit(1); }
    if (e.key === 'ArrowDown') { e.preventDefault(); return moveEdit(-1); }
    if ((e.ctrlKey || e.metaKey) && e.key === 'z') { if (editor.undo()) editChanged(); return; }
    if (e.key === 'Escape' || e.key === 'e' || e.key === 'E') return leaveEdit(true);
    if (e.key === 'Enter') { await leaveEdit(true); return setPlaying(true); }
  }
  if (e.key === ' ') { e.preventDefault(); setPlaying(!app.playing); }
  else if (e.key === '.' || e.key === 'ArrowRight') stepOnce();
  else if (e.key === 'e' || e.key === 'E') enterEdit();
  else if (e.key === '[') moveSlice(-1);
  else if (e.key === ']') moveSlice(1);
  else if (e.key >= '1' && e.key <= '9') { Object.assign(app.spec, { seed: 'key', k: Number(e.key), box: 'auto', gen: 0, play: 0, cz: '', abs: 0, g0: 0 }); resetToSeed(); }
});

// ---------------------------------------------------------------- per-face table + peeling law
const fmtT = (t) => !isFinite(t) ? '∞' : t < 1e6 ? fmt(t) : `10^${Math.log10(t).toFixed(1)}`;
function faceTable() {
  const s = app.last && app.last.s;
  if (!s || !s.faceHi || !app.faceA || !app.faceS || app.torus) {
    $('facetab').innerHTML = ''; $('facenote').textContent = app.torus ? 'no faces on a torus' : ''; return;
  }
  const sym = app.symmetric && app.symmetric.value;
  const live = [...s.faceHi, ...s.faceLo];
  const rows = ['<tr><th>face</th><th>layer s</th><th>live</th><th>sites A</th><th title="mean wait to extinction from the measured law">law τ</th><th>held for</th></tr>'];
  for (let q = 0; q < 8; q++) {
    const A = app.faceA[q], t = faceLaw(A, sym), alt = faceLaw(A, !sym);
    rows.push(`<tr><td>${FACE_NAMES[q]}</td><td>${app.faceS[q]}</td><td>${live[q]}</td><td>${A}</td><td title="${sym ? 'without' : 'with'} the symmetric divisor: ${fmtT(alt)}">${fmtT(t)}</td><td>${fmt(app.gen - app.faceSince[q])}${app.faceSince[q] === app.initialGen ? '+' : ''}</td></tr>`);
  }
  $('facetab').innerHTML = rows.join('');
  const symTxt = app.symmetric == null ? 'symmetry not yet checked' : sym ? `state is O_h-symmetric (checked at gen ${fmt(app.symmetric.gen)}), so A/7.7 is used` : `state is not O_h-symmetric (gen ${fmt(app.symmetric.gen)})`;
  $('facenote').innerHTML = `law τ = e<sup>−0.09 + 0.209·A</sup>, the measured mean wait for a face layer of A sites to die (a fit to flat faces of mixed widths, A = 27–90; at equal area a narrower face dies sooner; octahedral faces ran 1.7–1.9× longer). ${symTxt}. Waits are memoryless: a face that has held long is not "due"; a smaller τ means a likelier next peel. <a class="src" href="source.html?f=research/NOTEBOOK.md#${encodeURIComponent('Flat faces (slab, m = 8')}" target="_blank" rel="noopener">source</a>`;
}

// ---------------------------------------------------------------- atlas object card
function objCard() {
  const el = $('objcard'), it = app.atlas;
  const show = it && !tour.open && !$('gallery').classList.contains('open');
  el.classList.toggle('open', !!show);
  if (!show) return;
  const phase = ((app.gen - (app.spec.g0 || 0)) % it.period + it.period) % it.period;
  const live = app.last && app.last.gen === app.gen ? app.last.s.pop : null;
  const want = it.pops[phase];
  const check = live == null ? '' : live === want ? ` <span class="ok">✓ matches the catalogue</span>` : ` <span class="alert">✗ catalogue says ${want}</span>`;
  const key = `${it.id}|${phase}|${live}`;
  if (el.dataset.key === key) return;
  el.dataset.key = key;
  el.innerHTML = `<div class="row"><b>${it.id}</b><span class="dim">${it.category.title}</span></div>` +
    (it.note ? `<div>${it.note}</div>` : '') + `<ul>${describe(it).map(f => `<li>${f}</li>`).join('')}</ul>` +
    `<div class="live dim">phase ${phase} of ${it.period} · live ${live ?? '…'}${check}</div>` +
    `<div class="buttons"><button id="oc-gal">▦ gallery</button></div>`;
  $('oc-gal').addEventListener('click', openGallery);
}
async function openGallery() {
  await loadGallery();
  renderGallery($('gallery'), pickAtlas, app.spec.seed === 'atlas' ? app.spec.id : null);
  $('gallery').classList.add('open');
  if (tour.open) closeTour();
}
async function pickAtlas(id) {
  await loadGallery();
  const it = findItem(id);
  Object.assign(app.spec, { ...DEFAULTS, seed: 'atlas', id, speed: it ? speedFor(it) : '2', play: 1, face: 0.7, rec: app.spec.rec, view: app.spec.view });
  await resetToSeed();
  renderGallery($('gallery'), pickAtlas, id);
  $('gallery').classList.remove('open');
}
$('galBtn').addEventListener('click', () => $('gallery').classList.contains('open') ? $('gallery').classList.remove('open') : openGallery());

// ---------------------------------------------------------------- the tour
const tour = { open: false, i: 0, v: 0 };
async function showScene(i, v = 0) {
  i = Math.max(0, Math.min(SCENES.length - 1, i));
  const sc = SCENES[i];
  v = sc.variants ? Math.max(0, Math.min(sc.variants.length - 1, v)) : 0;
  Object.assign(tour, { open: true, i, v });
  $('tour').classList.add('open'); $('gallery').classList.remove('open');
  $('t-step').textContent = `tour · ${i + 1} of ${SCENES.length}`;
  $('t-title').textContent = sc.title;
  $('t-body').innerHTML = sc.body;
  $('t-variants').innerHTML = (sc.variants || []).map((x, j) => `<button data-v="${j}" class="${j === v ? 'on' : ''}">${x.label}</button>`).join('') +
    (sc.gallery ? '<button id="t-gal">▦ open the gallery</button>' : '');
  $('t-variants').querySelectorAll('[data-v]').forEach(b => b.addEventListener('click', () => showScene(i, Number(b.dataset.v))));
  if (sc.gallery) $('t-gal').addEventListener('click', openGallery);
  $('t-prev').disabled = i === 0; $('t-next').textContent = i === SCENES.length - 1 ? 'explore freely →' : 'next →';
  const spec = sc.variants ? sc.variants[v].spec : sc.spec;
  setOrtho(false);
  app.spec = { ...DEFAULTS, rec: app.spec.rec, ...spec };
  $('layers').classList.toggle('collapsed', !sc.kymo); $('k-hide').textContent = sc.kymo ? '–' : '+';
  await resetToSeed();
}
function closeTour() {
  tour.open = false; $('tour').classList.remove('open'); writeURL();
}
$('tourBtn').addEventListener('click', () => showScene(tour.i, tour.v));
$('t-close').addEventListener('click', closeTour);
$('t-prev').addEventListener('click', () => showScene(tour.i - 1));
$('t-next').addEventListener('click', () => tour.i === SCENES.length - 1 ? closeTour() : showScene(tour.i + 1));

resize();
setOrtho(!!app.spec.ortho);
{
  // Landing: no parameters -> the tour; ?tour=N[&v=M] -> that scene; anything else -> that run.
  const q = new URLSearchParams(location.search);
  const start = !location.search || q.has('tour') ? showScene(Number(q.get('tour') || 0), Number(q.get('v') || 0)) : resetToSeed();
  start.then(() => requestAnimationFrame(frame));
}
