// Analysis worker: receives full state snapshots, returns per-layer populations along the four
// body diagonals. Runs off the main thread so analysis never stalls stepping or rendering.
import { layerCounts } from './layers.js';

self.onmessage = (e) => {
  const { id, gen, layout, texels } = e.data;
  const t0 = performance.now();
  const diags = layerCounts(texels, layout);
  self.postMessage({ id, gen, diags, ms: performance.now() - t0 }, diags.map(d => d.counts.buffer));
};
