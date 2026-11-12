// Analysis worker: receives full state snapshots, returns per-layer populations along the four
// body diagonals, and the number of sites per layer inside the snapshot's own hull (cached: the
// hull changes rarely). Runs off the main thread so analysis never stalls stepping or rendering.
import { layerCounts, hullSites, hullOfCounts, isOhSymmetric, liveCells } from './layers.js';

let cache = { key: null, sites: null };
self.onmessage = (e) => {
  const { id, gen, layout, texels } = e.data;
  const t0 = performance.now();
  const diags = layerCounts(texels, layout);
  const hull = hullOfCounts(diags);
  const dims = [layout.nx, layout.ny, layout.nz];
  const key = hull && `${dims}|${hull.loS}|${hull.hiS}`;
  if (key && key !== cache.key) cache = { key, sites: hullSites(dims, hull) };
  diags.forEach((d, n) => { d.sites = key ? cache.sites[n].slice() : new Uint32Array(d.counts.length); });
  // O_h symmetry of the state (for the peeling law's symmetric effective area); skipped for huge states
  const pop = diags[0].counts.reduce((a, b) => a + b, 0);
  const symmetric = hull && pop <= 2e6 ? isOhSymmetric(liveCells(texels, layout), hull) : null;
  self.postMessage({ id, gen, diags, symmetric, ms: performance.now() - t0 }, diags.flatMap(d => [d.counts.buffer, d.sites.buffer]));
};
