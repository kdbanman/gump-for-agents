'use strict';
// ---- a clock that edits the message (NB 2026-11-15, "the fourth signals push reviewed"; CLAIMS SG19, SG22). The object is
//      research/signals/objects/divider-C8.json, copied by collect.py; drawn by kit.js (sigLine). Computed here: the period.
//      N = 12 is one of the lengths check-signals.js checks against the oracle (PAGE_DIVIDERS). ----
(function () {
  const G = D.signals4, N = 12, dv = G.divider, st = G.stroke;
  sigLine($('#f-div'), $('#l-div'), $('#b-div'), G.objects.divider, N, [dv[1], 2 * N - 3], 'The divider: the line of ' + N + ' units with the clock C8.24a beside the wire; every second rake becomes a gap');
  const T = $('#n-div');
  numTile(T, 'one cell', 'is the whole coupling, born once in ' + dv[1] + ' generations. The gun fires at the highest rate there is, so the gaps are the only message.', ['meas', 'three codes']);
  numTile(T, st[0] + ' → ' + st[1], 'cells, at ' + st[2] + ' units, when one cell is taken from the wire at the right place, one generation before the stroke: the clock is destroyed. Left alone, and under every word of gaps, it is never changed.', ['meas', 'reviewer; the lead re-ran it']);
  numTile(T, 'no reader', 'Nothing found reads the word, and a second clock on the halved stream does nothing more (' + st[3] + ' placements).', ['open', 'open']);
})();
