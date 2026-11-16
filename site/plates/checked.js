'use strict';
// ---------- checking ----------
(function () {
  const P = D.project, G = P.grades, sg = $('#f-grades'), mean = { A: 're-derived independently, by other code or another agent', B: 're-run by the auditor and matched', C: 'has a command, not yet re-run', D: 'no recipe to reproduce it' };
  sg.setAttribute('role', 'img'); sg.setAttribute('aria-label', 'A ' + G.A + ', B ' + G.B + ', C ' + G.C + ', D ' + G.D);
  ['A', 'B', 'C', 'D'].forEach((k, i) => E('span', { class: 'g' + (i + 1), style: 'flex:' + G[k] + ' 1 0' }, sg, G[k] > 3 ? k + ' ' + G[k] : ''));
  ['A', 'B', 'C', 'D'].forEach((k, i) => { const kk = E('span', { class: 'key' }, $('#k-grades')); const sw = E('span', { class: 'sw' }, kk); sw.style.background = getComputedStyle(sg.children[i]).backgroundColor; kk.appendChild(document.createTextNode(k + (k === 'D' ? ' (' + G.D + ')' : '') + ': ' + mean[k])); });
  $('#n-claims').textContent = G.total; $('#n-audits').textContent = P.audits.length;
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
