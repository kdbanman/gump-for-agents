'use strict';
// ---------- timeline ----------
(function () {
  const T = D.project.timeline, H = $('#f-timeline'), t0 = Date.parse(T.first_commit.slice(0, 20)), t1 = Date.parse(T.last_commit.slice(0, 20));
  const ms = T.milestones.map(m => ({ t: Date.parse(m.date.replace('Z', ':00Z')), text: m.text })), prs = T.pull_requests.map(p => ({ t: Date.parse(p.date.replace('Z', ':00Z')), n: p.n, title: p.title }));
  const hh = t => new Date(t).toISOString().slice(5, 16).replace('T', ' ');
  responsive(H, w => {
    const svg = S('svg', { viewBox: `0 0 ${w} 98`, width: w, height: 98, role: 'img', 'aria-label': 'Timeline of milestones and merged pull requests' }, H), ml = 8, mr = 8;
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

(function () { // headline of 'Built, and when', from git (collect.py)
  const T = D.project.timeline, h = Math.round((Date.parse(T.last_commit.slice(0, 19) + 'Z') - Date.parse(T.first_commit.slice(0, 19) + 'Z')) / 3600e3), n = T.pull_requests.length;
  $('#h-built').textContent = h + ' hours, ' + fmtInt(T.totals.commits) + ' commits, ' + n + ' merged pull requests.';
})();
