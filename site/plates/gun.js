'use strict';
// ---- a gun (NB 2026-11-15, "the fourth signals push", "... reviewed"; CLAIMS SG16-SG18). The object is research/signals/objects
//      line-C.json, copied by collect.py; laid out by signals-core.js (line) and drawn by kit.js (sigLine). Computed here: the
//      period, by comparing whole states. N = 12 is one of the lengths check-signals.js checks against the oracle (PAGE_LINES). ----
(function () {
  const G = D.signals4, N = 12;
  $('#n-gun-N').textContent = N;
  sigLine($('#f-gun'), $('#l-gun'), $('#b-gun'), G.objects.line, N, [G.line[0], 2 * N], 'The line: a cap, ' + N + ' units of wire C and the gun; rakes cross the wire from the gun to the cap');
  const T = $('#n-gun');
  numTile(T, G.gun[0] + ' cells', 'with period exactly ' + G.gun[1] + ': the gun. It starts by itself against bare wire, and every period it is exactly as it was, with one more rake on the wire.', ['meas', 'three codes']);
  numTile(T, 'every length', 'of wire from ' + G.line[1] + ' units up: cap, wire and gun make one free-standing object of period ' + G.line[0] + '. Emitter, wire and receiver, closed into one thing.', ['proved', 'proof re-derived']);
  numTile(T, fmtInt(G.heal[0]) + ' words', 'of missing rakes in the stream at 16 units, every one: each gap travels to the cap, is swallowed, and the object is as if nothing had happened.', ['meas', 'exhaustive']);
  numTile(T, 'overturned', '“Nothing found can write a message onto a wire from a standing object”, the third push’s reading of a few hours before.', ['ret', 'corrected']);
})();
