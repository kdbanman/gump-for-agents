const { makeGump } = require('/home/user/gump-for-agents/docs/overview/gump-core.js');
const fs = require('fs');
const ref = fs.readFileSync('/home/user/gump-for-agents/reference/golden/legacy_cube_side11_H60.txt','utf8').trim().split('\n').map(l=>+l.split(/\s+/)[1]);
const H = 68, c = 34, g = makeGump(H); g.seedBox(23, 45);
const rad = () => { let r = 0; const s = g.state; for (let i = 0; i < g.M; i++) { const k = g.cell[i]; if (s[k]) { const x = Math.floor(k/(H*H)), y = Math.floor(k/H)%H, z = k%H; const d = Math.abs(x-c)+Math.abs(y-c)+Math.abs(z-c); if (d > r) r = d; } } return r; };
let mism = 0, pops = [g.pop], rads = [rad()], peaks = 0;
for (let k = 1; k < ref.length; k++) { g.step(); if (g.pop !== ref[k]) mism++; pops.push(g.pop); rads.push(rad()); }
console.log('H=68 vs legacy log mismatches', mism, 'seed pop', pops[0], 'max pop', Math.max(...pops), 'at', pops.indexOf(Math.max(...pops)));
// hull radius changes
let ch = []; for (let k = 1; k < rads.length; k++) if (rads[k] !== rads[k-1]) ch.push([k, rads[k]]);
console.log('radius changes', JSON.stringify(ch));
// plateau means between changes after growth
fs.writeFileSync('/tmp/claude-0/-home-user-gump-for-agents/7cc48160-f729-54b0-abc5-8ed60edf8c93/scratchpad/explainer/side11.json', JSON.stringify({pops, rads_changes: ch}));
console.log('pop samples', [1,5,10,20,30,40,60,100,500,1000,2000,3000,3500,4000,4100,4200,4218].map(k=>k+':'+pops[k]).join(' '));
