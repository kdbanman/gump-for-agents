'use strict';
// ---------- the rule ----------
(function () {
  const faces = [{ p: [1, 0, 0], cls: 'f-c' }];
  for (const a of [-2, 2]) for (const b of [-2, 2]) faces.push({ p: [1, a, b], cls: 'f-n2' });
  for (const x of [0, 2]) for (const s of [-1, 1]) { faces.push({ p: [x, s, 0], cls: 'f-n1' }); faces.push({ p: [x, 0, s], cls: 'f-n1' }); }
  iso($('#f-nb'), faces, { scale: 22, yaw: 0.52, pitch: 0.4, label: 'A face of the cubic honeycomb and its twelve neighbours', wires: [{ cls: 'wire', segs: cubeWire([0, 0, 0], 1).concat(cubeWire([2, 0, 0], 1)) }] });
  // the same neighbourhood seen face-on: the 3 x 3 block of faces in the face's own plane
  const pv = S('svg', { viewBox: '0 0 118 136', width: 118, height: 136, role: 'img', 'aria-label': 'Seen face-on: the four corner-touching faces are watched, the four edge-sharing faces are not' }, $('#f-nbplan'));
  S('text', { x: 59, y: 11, 'text-anchor': 'middle', class: 't-mono' }, pv).textContent = 'seen face-on';
  for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
    const centre = r === 1 && c === 1, corner = r !== 1 && c !== 1;
    S('rect', { x: 4 + c * 37, y: 22 + r * 37, width: 35, height: 35, fill: centre ? 'var(--ink)' : corner ? 'var(--s3)' : 'var(--surface)', 'fill-opacity': corner ? .72 : 1, stroke: centre || corner ? 'none' : 'var(--ink-3)', 'stroke-width': 1.5 }, pv);
  }
  const R = $('#f-rule'); E('span', { class: 'lab' }, R, 'live neighbours');
  for (let n = 0; n <= 12; n++) E('span', { class: 'h' }, R, String(n));
  [['empty face', [4, 5]], ['live face', [3, 4, 5]]].forEach(([lab, on]) => { E('span', { class: 'lab' }, R, lab); for (let n = 0; n <= 12; n++) E('span', { class: 'c' + (on.includes(n) ? ' on' : n >= 6 ? ' over' : '') }, R); });
})();
