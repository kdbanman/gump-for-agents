'use strict';
// ---- a memory cell, live (CLAIMS SG33, SG34, SG37-SG41). The runs are the object files' own (data/memory.json, copied by
//      collect.py from research/signals/push9/objects/call9.json and push8/objects/cell8.json), laid out by signals-core.js
//      (memory) and stepped by gump-core.js (makeSparse) on the files' torus of side H. The hand operations are the files'
//      (cells removed or made live at the given generations). Computed here at every even generation: each unit's letter,
//      read from its cells; whether the whole state is exactly the state of those letters (compared cell for cell); and at the
//      files' check generations, whether it is the letters the file states (site/checks/check-signals.js checks the same runs
//      against those checks and against reference/oracle.py at every generation). ----
(function () {
  const M = D.memory, O = M.obj, reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ctl = $('#c-mem'), tape = $('#f-mem-tape'), host = $('#f-mem'), read = $('#l-mem');
  let R, L, g, rows, k = 0, w = 0, timer = null, hold = 0, last = '', events, G, exact, filed;
  const cls = (s, i) => s[i] === '7' ? null : s[i] === 'd' ? 'd' : s[i] === 'f' && s[i - 1] === 'd' ? 'f' : s[i] === '?' ? 'x' : 'p';
  const COL = { d: 'var(--ember)', f: 'var(--ember)', p: 'var(--s1)', x: 'var(--ink-3)' }, OP = { d: 1, f: .45, p: 1, x: 1 };
  const stores = s => (s.match(/d+f/g) || []).map(x => x.length - 1);
  const pick = i => {
    k = i; R = M.runs[k]; L = sigCore.memory(O, R); g = makeSparse(R.H); g.setCells(L.start);
    G = Math.max(...R.checks.map(c => c[0])); rows = []; events = []; exact = 0; filed = [0, 0]; hold = 0; last = '';
    [...ctl.children].forEach((b, j) => b.setAttribute('aria-pressed', String(j === k)));
    note(); drawAll();
  };
  const word = () => L.decode(p => g.has(p));
  // at an even generation: the letters, whether the whole state is theirs, the file's check if there is one; then the hand operations
  const note = () => {
    const t = g.gen, op = L.ops[t];
    if (t % 2 === 0) {
      const s = word(); let same = false;
      if (s.indexOf('?') < 0) { const want = L.state(s); same = want.length === g.pop && want.every(p => g.has(p)); }
      if (same) exact++;
      rows.push([t, s]); last = s;
      const ck = R.checks.find(c => c[0] === t);
      if (ck) { filed[0]++; if (ck[1] === s && same) filed[1]++; }
    }
    if (op) {
      const [off, on] = op;
      off.forEach(p => {
        const u = L.unitOf(p), s = last, rel = s[u + 1] === 'd' || s[u] === 'd';
        events.push([t, rel ? 'the release: one stator beside the stretch removed by hand' : 'a pulse sent: one cell of the wire removed by hand']);
        g.set(p, false);
      });
      if (on.length) { events.push([t, 'the call: ' + on.length + ' cells of the call line made live by hand']); on.forEach(p => g.set(p, true)); }
    }
  };
  const one = () => { g.step(); note(); };
  const drawTape = () => {
    tape.textContent = '';
    const W = w, n = R.N, u = Math.min(16, (W - 8) / n), svg = S('svg', { viewBox: `0 0 ${W} 34`, width: W, height: 34, role: 'img', 'aria-label': 'The letters of the store wire at generation ' + g.gen + ': ' + last }, tape);
    const x0 = (W - u * n) / 2;
    for (let i = 0; i < n; i++) {
      const c = cls(last, i);
      S('rect', { x: x0 + i * u + .5, y: 6, width: u - 1, height: 22, rx: 2, fill: c ? COL[c] : 'var(--surface)', 'fill-opacity': c ? OP[c] : 1, stroke: 'var(--rule)', 'stroke-width': 1 }, svg);
      if (u >= 11) { const t = S('text', { x: x0 + i * u + u / 2, y: 21, 'text-anchor': 'middle', class: 't-mono', style: 'font-size:10px' }, svg); t.textContent = last[i]; }
    }
    (R.crossings || []).forEach(c => S('line', { x1: x0 + (c + .5) * u, x2: x0 + (c + .5) * u, y1: 0, y2: 34, stroke: 'var(--ink-2)', 'stroke-width': 2 }, svg));
  };
  const drawStrip = () => {
    host.textContent = '';
    const n = R.N, W = w, ml = 34, u = Math.min(16, (W - ml - 8) / n), x0 = ml, Hh = 240, rh = Hh / (G / 2 + 1);
    const svg = S('svg', { viewBox: `0 0 ${W} ${Hh + 26}`, width: W, height: Hh + 26, role: 'img', 'aria-label': 'Space-time strip of the store wire: one row every second generation, one column per unit, run ' + R.name }, host);
    const Y = t => 4 + (t / 2) * rh;
    S('rect', { x: x0, y: 4, width: u * n, height: Hh, fill: 'none', stroke: 'var(--rule)' }, svg);
    for (let i = 0; i < n; i++) {
      let start = null, c0 = null;
      const flush = (j) => { if (c0) S('rect', { x: x0 + i * u, y: Y(rows[start][0]), width: u, height: Math.max(.8, (j - start) * rh), fill: COL[c0], 'fill-opacity': OP[c0] }, svg); };
      for (let j = 0; j <= rows.length; j++) {
        const c = j < rows.length ? cls(rows[j][1], i) : null;
        if (c !== c0) { flush(j); start = j; c0 = c; }
      }
    }
    (R.crossings || []).forEach(c => S('line', { x1: x0 + (c + .5) * u, x2: x0 + (c + .5) * u, y1: 4, y2: 4 + Hh, stroke: 'var(--ink-2)', 'stroke-width': 1, 'stroke-dasharray': '3 3' }, svg));
    events.forEach(([t, s]) => { const y = Y(t); S('line', { x1: x0 - 6, x2: x0, y1: y, y2: y, stroke: s.indexOf('call') >= 0 ? 'var(--ink)' : 'var(--ember)', 'stroke-width': 2 }, svg); });
    [0, Math.round(G / 4), Math.round(G / 2), Math.round(3 * G / 4), G].forEach(t => { t -= t % 2; const e = S('text', { x: x0 - 8, y: Y(t) + 3, 'text-anchor': 'end', class: 't-mono', style: 'font-size:9px' }, svg); e.textContent = t; });
    const tt = S('text', { x: x0, y: Hh + 20, class: 't-mono', style: 'font-size:10px' }, svg); tt.textContent = 'units 1 to ' + n + ' →   generations ↓   marks: the hand operations';
  };
  const drawRead = () => {
    read.textContent = '';
    const st = stores(last), ev = events.filter(e => e[0] <= g.gen && e[0] > g.gen - 40);
    E('span', {}, read, 'generation ' + g.gen + ' · ');
    E('b', {}, read, st.length ? (st.length > 1 ? 'stores hold ' + st.join(' and ') : 'the store holds ' + st[0]) : 'no stretch on the wire');
    if (ev.length) E('span', {}, read, ' · ' + ev[ev.length - 1][1]);
    E('span', {}, read, ' · the whole state was exactly its letters at ' + exact + ' of ' + rows.length + ' even generations; the file’s ' + R.checks.length + ' checks: ' + filed[1] + ' of ' + filed[0] + ' so far ' + (filed[1] === filed[0] ? '✓' : '✗'));
  };
  const drawAll = () => { if (!w) return; drawTape(); drawStrip(); drawRead(); };
  M.runs.forEach((r, i) => { const b = E('button', { class: 'btn', type: 'button', 'aria-pressed': 'false' }, ctl, r.label); b.addEventListener('click', () => { pick(i); if (!timer && !reduce) play(); }); });
  const tick = () => {
    if (g.gen >= G) { if (++hold > 25) { pick((k + 1) % M.runs.length); } return; }
    for (let s = 0; s < 4 && g.gen < G; s++) one();
    drawAll();
  };
  const btn = $('#b-mem');
  const play = () => { if (!timer) timer = setInterval(tick, 60); btn.textContent = 'Pause'; };
  const stop = () => { clearInterval(timer); timer = null; btn.textContent = 'Play'; };
  btn.addEventListener('click', () => { timer ? stop() : play(); });
  $('#b-mem-r').addEventListener('click', () => { pick(k); });
  responsive(host, ww => { w = ww; drawAll(); });
  pick(0);
  if (reduce) { while (g.gen < G) one(); drawAll(); stop(); }
  else if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { if (!timer && btn.textContent !== 'Play') play(); } else if (timer) { clearInterval(timer); timer = null; } }), { threshold: .15 }).observe(host.closest('figure'));
  else play();
  const r0 = M.runs[0];
  $('#x-mem').textContent = 'Stepped live by this page, cell for cell, from the object files of the eighth and ninth pushes: the store of ' + r0.N + ' units (' + (38 + 5 * r0.N) + ' cells) with the call line across it, and the hand operations at the generations the files give. “Write 3, call; write 2, call”: two pulses meet and write 1, two more add one each, and the call sends the three out to the left, where the cap swallows them; then the same with two. “Call a store of 3 into a store of 1”: the left store ends holding 4. “Write 4, release by hand”: the eighth push’s cell, emptied by removing one stator beside the stretch. Above, the letters now; below, every second generation, one row each. The page reads each unit’s letter from its cells and compares the whole state with the state of those letters; at the generations the file checks, it compares with the file’s letters too. The same runs are checked against the reference stepper at every generation (site/checks/check-signals.js).';
  const T = $('#n-mem'), V = D.memory;
  numTile(T, 'write', 'Two pulses that meet leave a stretch holding 1; every later pulse that reaches it, from either side and two or more units behind the last, adds one. A block of m adjacent pulses adds ⌈m/2⌉. Capacity N − 4. Every stored state stands with period exactly 2.', ['proved', 'A: two codes on the reference stepper']);
  numTile(T, 'k pulses', 'come back out when one stator beside the stretch is removed at an even generation: exactly k, two units apart, the wire plain from generation 2k + 6, for every k (proof refereed, three gaps closed by the review). A second store two or more units away catches them and holds k + 1.', ['proved', 'A for every k']);
  numTile(T, 'a read', 'that leaves the store as it was: two adjacent pulses on a capped wire crossing the store at 60 degrees come back as one pulse beside a unit of plain wire and as none beside a unit of the variant wire; no cell of the store ever differs. It reads the one unit it crosses; a single pulse never reads. No write with a reader in place was found.', ['meas', 'A for the read; C for the surveys and negatives']);
  numTile(T, 'the call', 'Two adjacent pulses on the call line pass on unchanged and the stretch leaves as exactly k pulses; reusable; caught by another store (1 and 3 give 4); one line across two store wires calls both. Its whole effect on the store wire is one cell made live at one generation, and the law is proved for every k on the infinite wire (proof not refereed). Hazards: a call near a travelling pulse can destroy the wire; a pulse from the left disarms an armed store; two calls need 4k + 2 generations between them.', ['meas', 'A for the runs; B for the proof’s base runs']);
  numTile(T, 'one pulse', 'calls, on the store’s own wire, with the period-3 oscillator P3.15f beside the wall: at one arrival timing in three it releases the stretch as k pulses (k = 1 to 10) and the oscillator is as it would have been; it calls twice. A pulse sent past a place where a second store may stand releases the far store if that place is empty and is absorbed if a store is there.', ['unchk', 'B: the reviewer’s object, re-run by the lead; no second code']);
  numTile(T, 'k − 1', 'One less, with a zero exit: a call and one store pulse born 17 units before the crossing at the same generation release exactly k − 1 pulses for k ≥ 1, and for k = 0 the pulse goes on to the right. One relative timing only; both signals made by hand.', ['unchk', 'B: the reviewer’s code; no second code']);
  numTile(T, 'not together', 'Write, read and call do not coexist usefully on one store: where the reader can tell the stretch, a write or a call destroys it; where it survives, it answers the same whatever the count.', ['unchk', 'C: the reviewer’s code, not re-run']);
  const li = (Ls, b, t) => { const e = E('li', {}, Ls); if (b) E('b', {}, e, b + ' '); e.appendChild(document.createTextNode(t)); };
  const L1 = $('#l-mem-what');
  li(L1, 'A hand-operated accumulator.', 'In the reviewer’s words: set, add one, move-and-clear into the left neighbour, clear, and an emptiness test. Without a decrement every output is a sum of some of the inputs plus a constant, chosen only by which inputs are zero: no copy, doubling, subtraction, comparison or parity.');
  li(L1, 'The missing operation:', 'a decrement that reports zero. With an increment, that on two counters is a Minsky machine. The one-less collision is that operation, hand-timed and relocating: the count k − 1 leaves to the left, and nothing moves a count to the right.');
  li(L1, 'Still made by hand:', 'the calling pair (no signal of the machine makes it; one pulse into two is open), every pulse that writes, and the timing of the one-less collision. The pieces have not all been run together, and the one-less collision was not tried at the oscillator’s call, where its zero exit is the kind of pulse that starts the next call.');
  const L2 = $('#l-mem-check');
  li(L2, 'The live runs:', 'the object files’ own runs (cycle and move of the ninth push, count of the eighth). site/checks/check-signals.js steps each on this page’s stepper and asserts the file’s whole-state checks and agreement with reference/oracle.py at every generation; the pushes’ verifiers (verify_call9.py, verify_cell8.py) check the same runs on the reference stepper alone, and the lead ran them.');
  li(L2, 'The proofs:', 'the release for every k (the eighth push, refereed by its review); the call law for every k on the infinite wire for this line and seed place (the ninth push’s review, six base runs on the reference stepper re-run by the lead; the proof read by nobody but its author). The finite cell’s cap is measured to k = 40.');
  li(L2, 'Not checked:', 'the oscillator’s law beyond k = 10 and the still life’s beyond k = 8 on the reference stepper; the one-less collision at other seeds; the other 36 oscillators at three timings; the reader’s other 22 placements.');
  void V;
})();
