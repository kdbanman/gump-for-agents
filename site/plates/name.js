'use strict';
// ---------- prior art ----------
(function () {
  const want = ['Crutchfield', 'Durrett', 'Mountford', 'Bramson', 'Politi', 'Eppstein', 'Houghton'], H = $('#f-prior');
  const rows = D.project.prior.filter(r => want.some(k => r[1].indexOf(k) >= 0)).map(r => ({ y: parseInt(String(r[0]).match(/\d{4}/)[0], 10), ys: String(r[0]).replace(/\s*\(.*\)/, ''), who: r[1].replace(/J\. P\. |K\. |D\. |R\. H\. |R\. |X\.-F\. |T\. S\. |M\. R\. E\. |S\. M\. |E\. |M\. |C\. |A\. /g, ''), line: r[2], read: r[3] }));
  rows.push({ y: 2012, ys: '2012', who: 'gump', line: 'Your Processing sketch: a rule chosen by hand on the faces of the cubic honeycomb.', read: '', gump: 1 });
  rows.sort((a, b) => a.y - b.y).forEach(r => { E('span', { class: 'y' }, H, r.ys); const d = E('div', { class: 'w' + (r.gump ? ' gump' : '') }, H); E('b', {}, d, r.who + '. '); E('span', {}, d, r.line + ' '); if (r.read) E('em', {}, d, '[' + r.read + ']'); });
  D.project.known.split('; ').forEach(s => E('li', {}, $('#l-known'), s.charAt(0).toUpperCase() + s.slice(1)));
  D.project.ours.slice(0, 5).forEach(s => E('li', {}, $('#l-ours'), s.charAt(0).toUpperCase() + s.slice(1)));
})();

// ---- prior art after three passes (NB 2026-11-14, "prior art, third pass: what the adversarial review changed") ----
(function () {
  const P = D.prior3, cap = s => s.charAt(0).toUpperCase() + s.slice(1);
  const ko = $('#l-known'), ou = $('#l-ours'); ko.textContent = ''; ou.textContent = '';
  P.known.forEach(s => E('li', {}, ko, cap(s)));
  ['half-space confinement method (Eppstein)', 'period/mod twists on hex grids (LifeWiki)'].forEach(s => { if (D.project.known.indexOf(s) >= 0) E('li', {}, ko, cap(s)); });
  P.ours.forEach(s => E('li', {}, ou, cap(s) + (s.indexOf('shape and twist') >= 0 ? ' (the second variable looked for there was then not found)' : '')));
  // add the third pass's works to the list of what was read, in year order
  const H = $('#f-prior'), items = [];
  for (let i = 0; i < H.children.length; i += 2) items.push([parseInt(H.children[i].textContent, 10), H.children[i], H.children[i + 1]]);
  P.refs.forEach(r => { const y = E('span', { class: 'y' }), d = E('div', { class: 'w' }); y.textContent = String(r[0]); E('b', {}, d, r[1] + '. '); E('span', {}, d, r[2] + ' '); if (r[3]) E('em', {}, d, '[' + r[3] + ']'); items.push([r[0] + 0.5, y, d]); });
  items.sort((a, b) => a[0] - b[0]).forEach(x => { H.appendChild(x[1]); H.appendChild(x[2]); });
})();
