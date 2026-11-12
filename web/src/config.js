// Where the project's source documents (docs/AUTOMATON.md, research/NOTEBOOK.md, ...) are fetched
// from: the repository root when served from the repo (npm run serve); tools/build.mjs rewrites
// this file to './sources/' (relative to the page) for the static build, which carries copies.
export const SOURCES = new URL('../../', import.meta.url).href;
