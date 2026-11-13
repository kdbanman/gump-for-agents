// Atlas gallery: browse data/gallery.json (built by tools/gallery.mjs from the research atlas),
// load an object as the running seed, and show what is known about it. The live population is
// compared every generation with the catalogue's population for that phase.

let data = null;
export async function loadGallery() {
  if (!data) data = await (await fetch(new URL('../data/gallery.json', import.meta.url))).json();
  return data;
}
export function findItem(id) {
  if (!data) return null;
  for (const c of data.categories) { const it = c.items.find(i => i.id === id); if (it) return { ...it, category: c }; }
  return null;
}

const SYM_TOTAL = 48;
export function describe(it) {
  const kind = it.period === 1 ? 'still life' : `period-${it.period}${it.twist > 1 && it.quotient > 1 ? ` = ${it.twist} × ${it.quotient}` : it.lcm ? ` = lcm(${it.lcm.join(', ')})` : ''} oscillator`;
  const pops = it.period === 1 ? `${it.pops[0]} cells` : `${Math.min(...it.pops)}–${Math.max(...it.pops)} live cells, ${it.union} cells used over a period`;
  const seen = [];
  if (it.seen.soup_octa) seen.push(`${it.seen.soup_octa.toLocaleString('en-US')}× in 3D soups`);
  if (it.seen.soup_kagome) seen.push(`${it.seen.soup_kagome.toLocaleString('en-US')}× in one-layer soups`);
  if (it.legacy.length) seen.push(`in the original's ash (${[...new Set(it.legacy.map(s => s.replace('-piece', '')))].join(', ')})`);
  const facts = [
    `${kind}, ${pops}`,
    `symmetry: ${it.sym} of the ${SYM_TOTAL} cube symmetries fix it${it.period > 1 ? `; ${it.spacetime_sym} map its orbit to itself${it.flip ? ' (a flip: phase 1 is phase 0 turned)' : ''}` : ''}`,
    it.twist > 1 ? `twisted: after ${it.quotient} generations it is back as a copy of itself turned or mirrored by a symmetry of order ${it.twist}` : null,
    `{111} layers spanned along the four diagonals: ${it.layers.join(' / ')}${it.family === 'kagome' ? ' (one layer: a kagome object)' : ''}`,
    it.inStar ? 'lives entirely inside one vertex star' : null,
    it.exhaustive.length ? `found by exhaustive search (${it.exhaustive.join(', ')})` : null,
    seen.length ? `seen ${seen.join('; ')}` : null,
  ].filter(Boolean);
  return facts;
}
// a speed at which the period is visible: one period in ~2-4 s
export function speedFor(it) {
  const p = it.period;
  return p === 1 ? '2' : p <= 2 ? '2' : p <= 6 ? '5' : p <= 22 ? '10' : '30';
}

export function renderGallery(el, onPick, current) {
  if (!data) return;
  el.innerHTML = `<div class="ghead"><b>Atlas</b> <span class="dim">${data.categories.reduce((a, c) => a + c.items.length, 0)} objects from the research atlas (${data.source}), each re-checked by stepping</span><button class="gclose">×</button></div>` +
    data.categories.map(c => `<div class="gcat"><h4>${c.title} <span class="tag ${c.status}">${c.status}</span></h4><p class="dim">${c.blurb}</p><div class="chips">${
      c.items.map(i => `<button class="chip${i.id === current ? ' on' : ''}" data-id="${i.id}" title="${i.note.replace(/"/g, '&quot;')}">${i.id}<span>${i.period > 1 ? 'p' + i.period + (i.twist > 1 && i.quotient > 1 ? ' = ' + i.twist + '×' + i.quotient : '') + ' · ' : ''}${i.union}</span></button>`).join('')
    }</div></div>`).join('');
  el.querySelectorAll('.chip').forEach(b => b.addEventListener('click', () => onPick(b.dataset.id)));
  el.querySelector('.gclose').addEventListener('click', () => el.classList.remove('open'));
}
