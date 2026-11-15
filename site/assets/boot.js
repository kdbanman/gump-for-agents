'use strict';
// Loads what one page needs, then runs its plate scripts in page order.
//   <script src="../assets/boot.js" data-root="../" data-data="law tail project" data-plates="law shape">
// data-data names files data/<key>.json; each becomes D.<key>, as on the old single page. data-plates names
// plates/<id>.js. build.py writes both lists from pages.json and the plate scripts' own uses of D.
const D = {};
(function () {
  const me = document.currentScript, root = me.dataset.root || '';
  const list = s => (s || '').split(/\s+/).filter(Boolean);
  const fail = msg => {
    const el = document.getElementById('boot-err');
    if (el) { el.hidden = false; el.textContent = msg; }
    console.error(msg);
  };
  const get = k => fetch(root + 'data/' + k + '.json').then(r => {
    if (!r.ok) throw new Error('data/' + k + '.json: HTTP ' + r.status);
    return r.json();
  }).then(v => { D[k] = v; });
  const run = src => new Promise((ok, no) => {
    const s = document.createElement('script');
    s.src = src; s.async = false;
    s.onload = ok; s.onerror = () => no(new Error(src + ' did not load'));
    document.body.appendChild(s);
  });
  Promise.all(list(me.dataset.data).map(get))
    .then(() => Promise.all(list(me.dataset.plates).map(id => run(root + 'plates/' + id + '.js')).concat(run(root + 'assets/stamp.js'))))
    .catch(e => fail('Part of this page could not be drawn: ' + e.message + '. Reload, or open the page from a web server rather than from a file.'));
})();
