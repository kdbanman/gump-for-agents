'use strict';
// ---- nothing listens (NB 2026-11-15 "the fifth signals push", "... reviewed"; CLAIMS SG23-SG25, SG27). All numbers quoted
//      (collect/sources/update-2026-11-15f.json, checked by collect.py; collect.py also checks that the four kinds add up to the
//      census and to the hole outcomes). Computed here: the row and column totals of the four kinds. The night refresh adds the
//      events the fifth review had not followed, the count an echo writes, and six pushes' forecasts (CLAIMS SG29, SG32;
//      collect/sources/update-2026-11-15g.json, ends6). ----
(function () {
  const X = D.ends, n = X.census[0], fo = X.four, ho = X.holes, ev = X.events, bs = X.beside, dv = X.divbeside, sat = X.sat, lim = X.limits, fw = X.followed, rw = X.rows, ct = X.count;
  $('#n-ends-n').textContent = fmtInt(n);
  $('#x-ends-def').textContent = 'The gun of the plates above fills its wire with a stream of moving objects, rakes, one every four generations. An end is whatever stands where the stream stops and swallows it: the line’s receiving cap is one, and a search found ' + fmtInt(n) + ' different ones (different up to moving or delaying them) that can stand in the narrow tube of the wire. A gap is a flaw that rides down the stream: a hole, one cell of a rake missing, or the second kind, K0, one cell of the wire itself missing. A listener would be an end left in a different lasting state by a gap than by none: the first step of any memory, and of any computer built from these parts. None is known.';
  const H = $('#f-ends');
  responsive(H, w => {
    const nar = w < 470, lw = nar ? 92 : 150, th = 44, cs = Math.min(nar ? 100 : 120, (w - lw - (nar ? 56 : 96)) / 2), h = th + 2 * cs + 46;
    const svg = S('svg', { viewBox: `0 0 ${w} ${h}`, width: w, height: h, role: 'img', 'aria-label': 'The ' + n + ' ends in four kinds: ' + fo[0] + ' heal a hole and K0, ' + fo[1] + ' heal a hole and are destroyed by K0, ' + fo[2] + ' are destroyed by a hole and heal K0, ' + fo[3] + ' are destroyed by both' }, H);
    const tx = (x, y, t, anc, cls) => { const e = S('text', { x, y, 'text-anchor': anc || 'start', class: cls || '' }, svg); e.textContent = t; return e; };
    const x0 = lw, y0 = th, big = Math.sqrt(Math.max(...fo));
    tx(x0 + cs, 12, nar ? 'K0, a wire cell missing:' : 'the second kind, K0 (a wire cell missing):', 'middle', 't-strong');
    tx(x0 + cs / 2, 32, 'healed', 'middle'); tx(x0 + 1.5 * cs, 32, 'destroyed', 'middle');
    tx(lw - 8, y0 + 14, 'a hole:', 'end', 't-strong');
    if (!nar) tx(lw - 8, y0 + 28, '(a rake cell missing)', 'end', 't-mono');
    ['healed', 'destroyed'].forEach((b, r) => tx(lw - 8, y0 + (r + 0.5) * cs + 4 + (r ? 0 : 12), b, 'end'));
    const col = k => k === 0 ? 'var(--s3)' : k === 3 ? 'var(--s-mute)' : 'var(--s1)';
    const what = ['heal both kinds', 'heal a hole, are destroyed by K0', 'are destroyed by a hole, heal K0', 'are destroyed by both'];
    fo.forEach((v, k) => {
      const r = k >> 1, c = k & 1, cx = x0 + (c + 0.5) * cs, cy = y0 + (r + 0.5) * cs, s = (cs - 14) * Math.sqrt(v) / big;
      S('rect', { x: x0 + c * cs + 1, y: y0 + r * cs + 1, width: cs - 2, height: cs - 2, fill: 'none', stroke: 'var(--rule)' }, svg);
      S('rect', { x: cx - s / 2, y: cy - s / 2, width: s, height: s, fill: col(k), 'fill-opacity': .85, rx: 2 }, svg);
      const t = tx(cx, s > 34 ? cy + 6 : cy - s / 2 - 6, fmtInt(v), 'middle', 't-strong halo'); t.style.fontSize = '15px';
      const hit = S('rect', { class: 'hit', x: x0 + c * cs, y: y0 + r * cs, width: cs, height: cs, tabindex: 0, fill: 'transparent' }, svg);
      tipOn(hit, () => [fmtInt(v) + ' ends ' + what[k], k === 1 ? 'the beam’s receiver is one of these' : k === 0 ? 'they forget both kinds of gap exactly' : k === 3 ? 'any one-cell gap destroys them' : 'they tell the two kinds apart only by dying of one']);
    });
    const rt = [fo[0] + fo[1], fo[2] + fo[3]], ct = [fo[0] + fo[2], fo[1] + fo[3]];
    rt.forEach((v, r) => tx(x0 + 2 * cs + 8, y0 + (r + 0.5) * cs + 4, fmtInt(v), 'start', 't-mono'));
    ct.forEach((v, c) => tx(x0 + (c + 0.5) * cs, y0 + 2 * cs + 18, fmtInt(v), 'middle', 't-mono'));
    tx(x0 + 2 * cs + 8, y0 + 2 * cs + 18, fmtInt(n), 'start', 't-mono t-strong');
    tx(4, h - 6, nar ? 'grey numbers: totals' : 'grey numbers: the totals of each row and column', 'start', 't-mono');
  });
  $('#x-ends').textContent = 'Each square’s area is the number of ends of that kind. Sent holes, ' + fmtInt(ho[0]) + ' ends heal exactly (the whole state equal to the run without the gap within ' + ho[1] + ' generations) and ' + fmtInt(ho[2]) + ' are destroyed, the same for every pattern of holes tried. Sent K0 they split again, so ' + fmtInt(fo[1] + fo[2]) + ' of the ' + fmtInt(n) + ' ends tell the two kinds apart, but only by dying of one: none is left alive and different. The lead ran every end on the reference stepper for holes (' + fmtInt(X.oracle[2]) + ' runs, all as the push said) and for K0 (' + X.lead124.slice(0, 3).map(fmtInt).join(', ') + ' and ' + X.lead124[3] + ', and one end that burns too slowly for that run and is dead on a longer one).';
  const U = $('#l-ends'), li = (b, t) => { const e = E('li', {}, U); E('b', {}, e, b + ' '); e.appendChild(document.createTextNode(t)); };
  li('The narrow tube.', 'Every end searched fits in the wire’s own tube, ' + sat[0] + ' × ' + sat[0] + ' cells across; a search in a wider tube was started and cut.');
  li('Periods ' + sat[1] + ' and ' + sat[4] + '.', 'The census holds every end whose period divides ' + sat[1] + '; a search as one constraint problem, by two encodings and three solvers (no certificate), finds no listener of period dividing ' + sat[1] + ', or ' + sat[4] + ' on a shorter stretch, that settles within ' + lim[1] + ' generations and disturbs at most ' + lim[0] + ' units of stream in front of it.');
  li('One-unit events.', 'Every change of one arriving rake by one unit: each subset of its cells removed, each dead cell of the tube made live, the rake replaced by bare wire, at every phase of its period: ' + fmtInt(ev[0]) + ' events per end, ' + fmtInt(ev[1]) + ' runs. Each ends healed or burns up the stream. One code, its stepper checked against the reference stepper. ' + fw[0] + ' of these events were at first counted as breaking the stream; they start a single signal moving up it instead (' + fw[2] + ' an echo, ' + fw[3] + ' the one-cell U of the plate above). The sixth review sent them to every end (' + fmtInt(rw[1]) + ' + ' + fmtInt(rw[2]) + ' runs): every end is left as it was, the signal leaving up the stream.');
  li('Beside the stream, sampled.', fmtInt(bs[0]) + ' catalogue clocks in random places beside the running line, each sent a hole: ' + fmtInt(bs[1]) + ' runs beside the wire, ' + fmtInt(bs[2]) + ' beside the receiving end. Each heals, or something is destroyed, or the echo on the plate above kills the gun. The divider’s own clock at every place and phase for N = ' + dv[0] + ': ' + fmtInt(dv[1]) + ' runs, ' + fmtInt(dv[2]) + ' heal, ' + fmtInt(dv[3]) + ' destroy it.');
  li('Not looked at:', 'gaps larger than one unit, anything outside the tube, and certificates for the solvers’ “no”.');
  const mem = $('#x-ends-mem'); E('b', {}, mem, 'The nearest thing to a memory after six pushes. '); mem.appendChild(document.createTextNode('An echo that runs into several holes in a row leaves behind it a standing stretch of yet another wire, wire B′, one unit longer for each further hole: a count. But it is written inside a stream that the meeting is turning into wire B on both sides of it, and in a finite line it is erased when the gun dies and the gun’s fire runs down the wire. It is proved to stand for spacings of ' + ct[0] + ' to ' + ct[1] + ' between the holes, on the infinite train only (the reviewer’s code). So after six pushes no listener and no loop is known: nothing found is left alive in a different lasting state by a signal. That has since changed: a finite line now keeps such a count standing (“A line that keeps a count”), 34 guns are left alive and changed by an echo, and a free-standing store holds a count that pulses write and a call gives back (“A memory cell”).'));
  const N = $('#n-ends'), pu = X.pushes;
  numTile(N, fmtInt(ho[0]) + ' · ' + fmtInt(ho[2]), 'ends that heal every pattern of holes, and that die of every one. No end is moved, delayed or changed by a hole.', ['meas', 'three codes']);
  numTile(N, '4 kinds', 'once the second gap is tried: ' + fo.map(fmtInt).join(', ') + '. Which gaps an end forgets is not a property of the end alone.', ['meas', 'two codes']);
  numTile(N, '0', 'ends left alive and changed, over all ' + ev[0] + ' one-unit changes of a rake at every one of the ' + fmtInt(n) + ' ends (' + fmtInt(ev[1]) + ' runs), now that the ' + fw[0] + ' that start an up-signal are followed too.', ['unchk', 'one code each, two reviews']);
  numTile(N, pu[1] + ' of ' + pu[0], 'of the lead’s forecasts over six pushes on signals held in some form; ' + pu[2] + ' failed.', ['meas', 'scored']);
})();

// ---- since 2026-11-18 (CLAIMS SG33-SG41; OPEN-PROBLEMS 13 (v), (y), (aa)-(ae)); numbers from D.reg, quoted in update-2026-11-18.json ----
(function () {
  const R = D.reg, l7 = R.line7, g = R.guns34, L = $('#l-ends-since');
  const li = (b, t) => { const e = E('li', {}, L); if (b) E('b', {}, e, b + ' '); e.appendChild(document.createTextNode(t)); };
  li('The ends still do not listen.', fmtInt(l7[5]) + ' ends at C ≤ ' + l7[6] + ': none is left alive and changed by a gap. But ' + g[2] + ' of ' + g[0] + ' guns are left alive and changed by the echo (one code; “A line that keeps a count”).');
  li('A store listens.', 'Away from the ends, pulses write a count into a wire, a pulse reads one bit of it, a pair of pulses on a crossing wire reads a unit without disturbing it, and a pair on a crossing wire calls the count back out as that many pulses, which another store catches (“A memory cell”).');
  li('Still missing:', 'a source for the calling pair (one pulse into two); copying, doubling, subtracting or comparing counts; a write with a reader in place (write, read and call do not coexist usefully on one store); a decrement that reports zero and leaves the count where it can be decremented again (the one-less collision does it once, hand-timed); any operation started by a signal the machine made itself; the pieces run together under schedules that respect the hazards; a referee for the proof of the call.');
})();
