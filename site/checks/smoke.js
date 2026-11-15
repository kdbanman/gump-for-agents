// Smoke test of the built site: node site/checks/smoke.js [--artifact] [--shots DIR]   (from anywhere; needs the tree built)
// --artifact: test site/dist-artifact/ (the private artifact copy) instead of site/dist/, without the app, and fail on any
// request into app/.
// Serves site/dist with `python3 -m http.server` under the prefix /gump-for-agents/ (as GitHub Pages serves a project
// site under /<repo>/), opens every page of pages.json and the app at desktop (1280 px) and phone (390 px) width, and
// fails on: a console error or uncaught exception, a failed or 4xx/5xx request, a plate of pages.json missing from
// its page, a figure container (id f-* or c-*) left empty (overview pages only), or horizontal page overflow. With --shots it also saves
// a screenshot of every page at both widths in light and dark (deviceScaleFactor 1).
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os'), net = require('net');

const ARTIFACT = process.argv.includes('--artifact');
const SITE = path.resolve(__dirname, '..'), DIST = path.join(SITE, ARTIFACT ? 'dist-artifact' : 'dist'), PREFIX = 'gump-for-agents';
const shotsAt = process.argv.indexOf('--shots'), SHOTS = shotsAt > 0 ? path.resolve(process.argv[shotsAt + 1]) : null;
if (!fs.existsSync(path.join(DIST, 'index.html'))) { console.error(`site/${path.basename(DIST)} is not built: python3 site/build.py${ARTIFACT ? ' --artifact' : ''}`); process.exit(2); }
const pages = JSON.parse(fs.readFileSync(path.join(SITE, 'pages.json'), 'utf8'));
// figure containers that are meant to stay empty (none so far); add 'page:id' here with a reason if one appears
const EMPTY_OK = new Set([]);

const freePort = () => new Promise(ok => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => ok(p)); }); });

(async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'gump-site-'));
  fs.symlinkSync(DIST, path.join(tmp, PREFIX));
  const port = await freePort();
  const srv = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', tmp], { stdio: 'ignore' });
  const base = `http://127.0.0.1:${port}/${PREFIX}/`;
  for (let i = 0; i < 50; i++) { try { await fetch(base + 'index.html'); break; } catch { await new Promise(r => setTimeout(r, 100)); } }
  const browser = await chromium.launch();
  const targets = pages.map(p => ({ name: p.slug || 'index', url: (p.slug ? p.slug + '/' : '') + 'index.html', plates: p.plates.map(x => x.id) }))
    .concat(ARTIFACT ? [] : [{ name: 'app', url: 'app/index.html', plates: [], app: true }]);
  const widths = [['desktop', 1280, 900], ['phone', 390, 844]];
  const schemes = SHOTS ? ['light', 'dark'] : ['light'];
  if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });
  let bad = 0;
  const report = (t, w, msg) => { bad++; console.log(`FAIL ${t.name} @${w}: ${msg}`); };
  for (const t of targets) for (const [wn, W, H] of widths) for (const scheme of schemes) {
    const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1, colorScheme: scheme });
    const pg = await ctx.newPage(), errs = [];
    pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    pg.on('pageerror', e => errs.push('exception: ' + e.message));
    pg.on('requestfailed', r => errs.push('request failed: ' + r.url() + ' ' + (r.failure() || {}).errorText));
    pg.on('response', r => { if (r.status() >= 400) errs.push('HTTP ' + r.status() + ': ' + r.url()); });
    if (ARTIFACT) pg.on('request', r => { if (r.url().startsWith(base + 'app/')) errs.push('request into app/: ' + r.url()); });
    await pg.goto(base + t.url, { waitUntil: 'networkidle' });
    await pg.waitForTimeout(t.app ? 2500 : 800);
    const res = await pg.evaluate(plates => {
      const missing = plates.filter(id => { const e = document.getElementById(id); return !e || !e.offsetHeight; });
      const empty = [...document.querySelectorAll('[id^="f-"],[id^="c-"]')].filter(e => !e.childNodes.length && !e.textContent.trim()).map(e => e.id);
      const de = document.documentElement;
      return { missing, empty, over: Math.max(de.scrollWidth, document.body.scrollWidth) - de.clientWidth, title: document.title };
    }, t.plates);
    errs.forEach(e => report(t, wn, e));
    if (res.missing.length) report(t, wn, 'missing plates: ' + res.missing.join(' '));
    const empty = t.app ? [] : res.empty.filter(id => !EMPTY_OK.has(t.name + ':' + id));   // the app's f-* are its form fields
    if (empty.length) report(t, wn, 'empty figures: ' + empty.join(' '));
    if (res.over > 1) report(t, wn, `horizontal overflow of ${res.over} px`);
    if (SHOTS) await pg.screenshot({ path: path.join(SHOTS, `${t.name}-${wn}-${scheme}.png`), fullPage: true });
    if (scheme === 'light') console.log(`${errs.length || res.missing.length || empty.length || res.over > 1 ? 'bad ' : 'ok  '} ${t.name} @${wn} "${res.title}" (${t.plates.length} plates)`);
    await ctx.close();
  }
  await browser.close(); srv.kill(); fs.rmSync(tmp, { recursive: true, force: true });
  console.log(bad ? `smoke: ${bad} failure(s)` : `smoke: all pages clean (site/${path.basename(DIST)})`);
  process.exit(bad ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
