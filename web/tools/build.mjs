// Static build: copies the app and the three.js files it uses into dist/ (no bundler).
//   node tools/build.mjs   ->  dist/ is deployable as plain static files
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const WEB = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIST = path.join(WEB, 'dist');
const cp = (from, to) => { fs.mkdirSync(path.dirname(path.join(DIST, to)), { recursive: true }); fs.copyFileSync(path.join(WEB, from), path.join(DIST, to)); };

fs.rmSync(DIST, { recursive: true, force: true });
for (const f of ['style.css']) cp(f, f);
for (const f of fs.readdirSync(path.join(WEB, 'src'), { recursive: true })) {
  if (f.endsWith('.js')) cp(path.join('src', f), path.join('src', f));
}
const T = 'node_modules/three';
for (const f of ['build/three.module.js', 'build/three.core.js', 'examples/jsm/controls/OrbitControls.js', 'LICENSE'])
  cp(path.join(T, f), path.join('vendor/three', f));
const html = fs.readFileSync(path.join(WEB, 'index.html'), 'utf8').replaceAll('./node_modules/three/', './vendor/three/');
fs.writeFileSync(path.join(DIST, 'index.html'), html);
const size = (d) => fs.readdirSync(d, { recursive: true }).map(f => path.join(d, f)).filter(f => fs.statSync(f).isFile()).reduce((a, f) => a + fs.statSync(f).size, 0);
console.log(`dist/ written (${(size(DIST) / 1024).toFixed(0)} KiB)`);
