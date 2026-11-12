// Static build: copies the app, its data, the three.js files it uses and the source documents
// the tour cites into dist/. No bundler; every path is relative, so dist/ can be served from any
// directory of any static host (GitHub Pages included).
//   node tools/build.mjs   ->  dist/
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const WEB = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REPO = path.resolve(WEB, '..');
const DIST = path.join(WEB, 'dist');
const cp = (from, to, root = WEB) => { fs.mkdirSync(path.dirname(path.join(DIST, to)), { recursive: true }); fs.copyFileSync(path.join(root, from), path.join(DIST, to)); };

fs.rmSync(DIST, { recursive: true, force: true });
for (const f of ['style.css', 'source.html', 'data/gallery.json']) cp(f, f);
for (const f of fs.readdirSync(path.join(WEB, 'src'), { recursive: true })) {
  if (f.endsWith('.js')) cp(path.join('src', f), path.join('src', f));
}
const T = 'node_modules/three';
for (const f of ['build/three.module.js', 'build/three.core.js', 'examples/jsm/controls/OrbitControls.js', 'LICENSE'])
  cp(path.join(T, f), path.join('vendor/three', f));
fs.writeFileSync(path.join(DIST, 'index.html'), fs.readFileSync(path.join(WEB, 'index.html'), 'utf8').replaceAll('./node_modules/three/', './vendor/three/'));
// the documents the tour links to, served next to the app
const SOURCES = ['docs/AUTOMATON.md', 'docs/WHAT-I-SEE.md', 'research/NOTEBOOK.md', 'research/STATUS.md', 'research/atlas/README.md',
  'research/figures/peel_face_law.png', 'research/figures/phase_rulemap.png'];
for (const f of SOURCES) cp(f, path.join('sources', f), REPO);
fs.writeFileSync(path.join(DIST, 'src/config.js'), "// static build: the cited documents are copied to ./sources/\nexport const SOURCES = new URL('../sources/', import.meta.url).href;\n");
fs.writeFileSync(path.join(DIST, '.nojekyll'), '');   // GitHub Pages: serve files as they are
const size = (d) => fs.readdirSync(d, { recursive: true }).map(f => path.join(d, f)).filter(f => fs.statSync(f).isFile()).reduce((a, f) => a + fs.statSync(f).size, 0);
console.log(`dist/ written (${(size(DIST) / 1024).toFixed(0)} KiB): serve it as plain static files from any path`);
