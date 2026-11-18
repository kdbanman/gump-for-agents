'use strict';
// ---- a line that keeps a count (CLAIMS SG35, SG36; NB 2026-11-18 "three more signals results in one night"). Numbers from
//      D.reg (quotes of collect/sources/update-2026-11-18.json, checked by collect.py); the prose is typed from the same quotes. ----
(function () {
  const R = D.reg, l7 = R.line7, lb = R.line7b, g = R.guns34;
  const li = (b, t) => { const e = E('li', {}, $('#l-reg')); if (b) E('b', {}, e, b + ' '); e.appendChild(document.createTextNode(t)); };
  li('The line.', 'A gun, a train of rakes on a wire and a mirrored end. An echo E and n holes sent down it turn the whole line into a standing wire B capped at both ends, period ' + lb[0] + ' from generation ' + lb[1] + ', holding the count as a stretch of the variant wire. Rebuilt by the review on the reference stepper alone: the states for n = 1 to ' + lb[2] + ' differ by exactly the cells claimed; a ' + fmtInt(lb[3]) + '-generation run agrees.');
  li('What it stores.', 'Nothing unless the second hole is three or more rakes behind the first; then the number of holes exactly (up to ' + l7[1] + ' in a ' + l7[2] + '-unit line) and the place of the second hole. Holes that arrive after the wire B has formed still count.');
  li('What is new.', 'The standing object is the second push’s register with two walls and new caps; new is that a running line converts itself into it, written by holes.');
  li('Still no listener at an end.', fmtInt(l7[3]) + ' ends at C ≤ ' + l7[4] + ' and ' + fmtInt(l7[5]) + ' at C ≤ ' + l7[6] + ': none is left alive and changed by a gap (“Nothing listens”).');
  li('Not checked:', 'the oracle sample at C ≤ 37 (4 ends only) and a quarter of the one at C ≤ 39; no gun census row on the reference stepper; the push’s own check scripts; period 8; the 5 × 5 tube beyond one end.');
  const N = $('#n-reg');
  numTile(N, 'n holes', 'held exactly, in a register that stands for ever with period ' + l7[0] + ': the line counts its own holes.', ['proved', 'A: two codes on the reference stepper']);
  numTile(N, g[2] + ' of ' + g[0], 'guns at C ≤ ' + g[1] + ' survive the echo E, changed: left standing, and from then on firing a hole with every rake. With one of them and a healing end, E alone turns the line into a clock of period 4N − 12 (or −16, −20), N = ' + g[3] + ' to ' + g[4] + '. At C ≤ ' + g[5] + ' all ' + g[6] + ' guns die, as the sixth push found. Nothing is known to turn them back.', ['unchk', 'C: the reviewer’s code alone, on the reference stepper’s step; nobody has repeated it']);
  numTile(N, 'corrected', '“No gun survives the answer”, as this site said on “An echo”, holds for the 67 guns at C ≤ 37 and is refuted at C ≤ 39 (the record keeps the correction).', ['ret', 'refuted by the seventh push’s review']);
})();
