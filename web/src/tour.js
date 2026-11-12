// The guided tour: live scenes, each a URL spec for the app plus a few sentences. Every factual
// statement carries its status and a link to where it is established: [proved] in
// docs/AUTOMATON.md or the atlas (exhaustive search), [measured] in research/NOTEBOOK.md,
// [conjecture] where that is all it is. "watch" marks what the scene itself shows.

const A = 'docs/AUTOMATON.md', N = 'research/NOTEBOOK.md', ST = 'research/STATUS.md', W = 'docs/WHAT-I-SEE.md';
const fig = (f, label) => `<a class="src" href="source.html?f=${f}" target="_blank" rel="noopener">${label}</a>`;
const src = (f, find, label) => `<a class="src" href="source.html?f=${f}#${encodeURIComponent(find)}" target="_blank" rel="noopener">${label}</a>`;
const tag = (t) => `<span class="tag ${t}">${t}</span>`;

export const SCENES = [
  {
    id: 'faces',
    title: 'Cells are the faces of cubes',
    body: `<p>Fill space with cubes. Every square face is a cell, alive or dead. Each cube owns three of
      them, and a face is coloured by which way it points: x <i class="sw sx"></i>, y <i class="sw sy"></i>,
      z <i class="sw sz"></i> (the colours of the original 2012 program). ${src(A, '## 1. Lattice', 'definition')}</p>
      <p>Here is a 3×3×3 block of cubes with every face alive, drawn with a gap around each face so you can
      see them all. Drag to turn it, scroll to zoom. Press <b>next</b> to see what the cells do.</p>`,
    spec: { seed: 'cube', n: 3, face: 0.7, play: 0, cam: '1,0.75,1.35,1.6' },
    kymo: false,
  },
  {
    id: 'neighbours',
    title: 'Twelve neighbours, and the rule',
    body: `<p>A face's neighbours are the 8 faces that meet it at right angles along an edge (the other
      faces of the two cubes it separates) and the 4 faces in its own plane that touch it only at a corner.
      ${src(A, '## 2. Neighbourhood and rule', 'definition')}</p>
      <p>The rule is <b>B45/S345</b>: a dead face comes alive with exactly 4 or 5 live neighbours, and a
      live face stays alive with 3, 4 or 5. ${src(A, 'Rule (outer-totalistic', 'rule')}</p>
      <p>The highlighted face (white) and its 12 neighbours are coloured by how far they sit along a
      body diagonal of the cubes. Cut space into planes perpendicular to that diagonal: the neighbours
      always fall <b>1, 2, 6, 2, 1</b> across five consecutive planes. ${tag('proved')} ${src(A, 'T1 (layer histogram)', 'T1')}
      Click any face to move the highlight.</p>`,
    spec: { seed: 'cells', cells: '', box: 7, color: 'neighbourhood', face: 0.7, play: 0, cam: '1,0.45,0.2,2.6' },
    kymo: false,
  },
  {
    id: 'confinement',
    title: 'Nothing can cross a diagonal plane',
    body: `<p>That 1, 2, 6, 2, 1 has a striking consequence. Take the outermost plane that still holds live
      faces. A dead face just beyond it sees at most 1 + 2 = 3 live neighbours, never the 4 it needs to be
      born. So nothing is ever born outside the octahedron cut out by the eight outermost planes, and
      that octahedron can only shrink. ${tag('proved')} ${src(A, 'T2 (octahedral confinement)', 'T2')}</p>
      <p>Watch an 11×11×11 cube: it grows along the axes, where nothing stops it, until it fills its
      octahedron (the faint outline), and then it can grow no further. So no pattern can travel or grow forever, and
      every finite pattern eventually repeats. ${tag('proved')} ${src(A, 'Hence any finite pattern', 'T2, consequences')}</p>
      <p>A flat front of chaos advances into empty space at about 0.18 cube per generation along the
      axes, 0.17 along the face diagonals, and exactly 0 across the diagonal planes. So the octahedron is the
      shape everything grows into. ${tag('measured')} ${src(N, 'Chaos invading vacuum', 'notebook: fronts')}</p>`,
    spec: { seed: 'cube', n: 11, speed: '5', play: 1, face: 0.6, cam: '1,0.75,1.35,1.2' },
    kymo: false,
  },
  {
    id: 'firewall',
    title: 'Firewalls',
    body: `<p>Three empty planes in a row stay empty forever, and then the two sides can never influence each
      other again. ${tag('proved')} ${src(A, 'T3 (firewall)', 'T3')}</p>
      <p>Two empty planes are not enough: a face in the gap can collect 1 + 2 live neighbours from one side
      and 1 from the other. ${tag('proved')} ${src(A, 'Two dead layers are', 'T3')}</p>
      <p>Below the view, the layer chart shows each plane along the diagonal as a row (colour = how full it
      is, black = empty) with time running to the right; the 3D view looks along the planes, so the gap is the
      empty stripe. With a 3-plane gap the black band never closes.
      Switch to the 2-plane gap: in this run it fills within a few generations. ${tag('watch')}</p>`,
    variants: [
      { label: '3-plane gap', spec: { seed: 'soup', shape: 'gap', n: 6, gap: 3, density: 0.4, rng: 2, speed: '5', play: 1, color: 'layer', cam: '1,-1,0,1.5', ortho: 1, face: 0.6 } },
      { label: '2-plane gap', spec: { seed: 'soup', shape: 'gap', n: 6, gap: 2, density: 0.4, rng: 2, speed: '5', play: 1, color: 'layer', cam: '1,-1,0,1.5', ortho: 1, face: 0.6 } },
    ],
    kymo: true,
  },
  {
    id: 'kagome',
    title: 'A layer is a world of its own',
    body: `<p>Faces lying in a single diagonal plane form a <i>kagome</i> lattice, a pattern of triangles
      and hexagons. A pattern confined to one plane stays in it (T2 from both sides), so each plane is a
      complete two-dimensional automaton in which every face has 6 neighbours. ${tag('proved')} ${src(A, 'T4 (closed sub-automata)', 'T4')}</p>
      <p>Thin stacks of planes cannot sustain chaos. On wrap-around slabs, random soups one plane thick
      die in about 5–12 generations, two planes thick in about 50–100, and both grow only logarithmically
      with area. From three planes, lifetimes grow exponentially with size: three planes is the critical
      thickness. ${tag('measured')} ${src(N, 'critical thickness is 3 layers', 'notebook: thickness')}
      Thin slabs do not die by losing a face: they die when a firewall forms <i>across</i> them, along one
      of the other diagonals. ${tag('measured')} ${src(N, 'Thin slabs and the cheapest cut', 'notebook: cuts')}</p>
      <p>Compare finite slabs of 1, 2 and 3 planes here, coloured by plane (A, B, C stack like this
      forever). ${tag('watch')}</p>`,
    variants: [
      { label: '1 plane', spec: { seed: 'soup', shape: 'slab', n: 10, layers: 1, density: 0.45, rng: 3, speed: '5', play: 1, color: 'layer', cam: '1,1,1,1.3', face: 0.8 } },
      { label: '2 planes', spec: { seed: 'soup', shape: 'slab', n: 10, layers: 2, density: 0.45, rng: 3, speed: '10', play: 1, color: 'layer', cam: '1,1,1,1.3', face: 0.8 } },
      { label: '3 planes', spec: { seed: 'soup', shape: 'slab', n: 10, layers: 3, density: 0.45, rng: 3, speed: '30', play: 1, color: 'layer', cam: '1,1,1,1.3', face: 0.8 } },
    ],
    kymo: true,
  },
  {
    id: 'chaos',
    title: 'Chaos is a phase',
    body: `<p>Fill a box that wraps around (no faces, no edges) with random faces and it settles into a
      steady churn, whatever the box size: <b>0.4155</b> of all faces alive. About half the live faces
      die each generation and as many are born. ${tag('measured')} ${src(N, 'Steady density', 'notebook: bulk')}
      Watch the density readout, under the population, settle there.</p>
      <p>The churn looks the same in every direction, and correlations die within about one cube. Flip a single face and the
      difference spreads as a sphere at about 0.85 cube per generation. It crosses the diagonal planes
      freely: the barrier of T2 holds only against empty space. ${tag('measured')} ${src(N, 'Damage from one flipped cell', 'notebook: damage')}</p>
      <p>On a box this size the churn is effectively immortal. Wrap-around soups of a few hundred
      cells die quickly, but none of 512 soups of 6³ cubes or larger died within 10<sup>6</sup> generations. ${tag('measured')} ${src(N, 'Whole-torus soups (no faces) die', 'notebook')}</p>`,
    spec: { seed: 'soup', shape: 'cube', n: 20, box: 20, bc: 'torus', density: 0.3, rng: 5, speed: '30', play: 1, cam: '1,0.75,1.35,1' },
    kymo: false,
  },
  {
    id: 'peel',
    title: 'Long calm, then the faces peel',
    body: `<p>Confined in its octahedron, a big cube (11 on a side) churns for thousands of generations at
      about 0.39 alive, lower than the 0.4155 of free chaos. Its perfect symmetry is the reason: faces on
      the cube's mirror planes are depleted. ${tag('measured')} ${src(N, 'Confined chaos: the 0.39 is a symmetry artefact', 'notebook: symmetry')}</p>
      <p>Then it loses the outermost plane of every face at once. That plane can never be re-seeded (T2),
      so the octahedron shrinks a step at a time: here at generations 3,290, 3,477 and 3,796. This is the staircase in the
      original program's population plots. ${tag('measured')} ${src(N, 'Hull radius (outermost live layer', 'notebook: peeling')}</p>
      <p>How long a face lasts follows one law over six decades. The wait is memoryless, with mean
      about e<sup>0.209·A</sup> generations for a face plane of A sites. ${tag('measured')} ${src(N, 'Flat faces (slab, m = 8', 'notebook: face law')} ${fig('research/figures/peel_face_law.png', 'figure')}
      A symmetric pattern counts as if its faces were 7.7 times smaller, because symmetric regions die in lockstep. ${tag('measured')} ${src(N, 'effective area A/7.7', 'notebook')}
      So the side-13 cube lasts about 10<sup>5</sup> generations <i>because</i> it is symmetric. By the law, the same
      octahedron filled asymmetrically would hold each face for about 10<sup>41</sup>. ${tag('measured')} (law, extrapolated) ${src(ST, 'face ~10', 'status')}
      The original's unfinished side-19 run outlived everything only because its torus was too small:
      it wrapped around and lost its faces. Properly confined, the law puts it near 10<sup>12</sup> generations. (law, extrapolated) ${src(W, 'Properly confined, the law puts it', 'what I see')}</p>
      <p>The run starts at generation 3,200. In the layer chart, the top and bottom rows go black for good.
      The <i>faces</i> table on the right gives each face's live cells, its site count A, and the law's mean wait.</p>`,
    spec: { seed: 'cube', n: 11, gen: 3200, speed: '30', play: 1, kwin: 1000, cam: '1,0.75,1.35,1.2' },
    kymo: true,
  },
  {
    id: 'fauna',
    title: 'What is left: the fauna',
    body: `<p>When the chaos dies it leaves debris built from a small fauna.
      The <b>vertex star</b> is the 12 faces meeting at one corner. No face outside it ever sees more than 2
      of them, so it is a sealed little universe, and all of its 4,096 states settle within 3 generations. ${tag('proved')} ${src(N, 'The vertex star is a closed vessel', 'atlas')}
      Coloured by diagonal plane, it reads as a triangle, a kagome hexagon and a triangle in three
      consecutive planes. ${tag('measured')} ${src(N, 'vertex star (S12a) = triangle', 'notebook')}</p>
      <p><b>Hinges</b> are the smallest oscillators: faces that swing 90° about an edge every generation.
      Every period-2 oscillator up to 11 cells works this way. ${tag('proved')} ${src(N, 'Period 2: the smallest union', 'atlas')}
      Rarer <b>clockwork</b> runs at periods up to 66. ${tag('measured')} ${src(N, 'Soups in octahedral vessels', 'atlas')}</p>
      <p>The original's side-9 cube ends as one cube in the middle and a kagome hexagon on each of the
      8 faces of its octahedron. ${tag('measured')} ${src(N, '**Legacy ash**', 'atlas')}
      The gallery holds 41 objects from the atlas.</p>`,
    variants: [
      { label: 'vertex star', spec: { seed: 'atlas', id: 'S12a', speed: '2', play: 1, face: 0.7, color: 'layer', cam: '1,1,1.6,1' } },
      { label: 'hinge (p2)', spec: { seed: 'atlas', id: 'P2.6a', speed: '2', play: 1, face: 0.7 } },
      { label: 'clockwork p66', spec: { seed: 'atlas', id: 'P66.27a', speed: '10', play: 1, face: 0.7 } },
      { label: 'side-9 ash', spec: { seed: 'cube', n: 9, gen: 71, speed: '5', play: 0, face: 0.7 } },
    ],
    gallery: true,
    kymo: false,
  },
  {
    id: 'yours',
    title: 'Your turn',
    body: `<p>Everything above runs live on your graphics card. Try a random soup in an octahedron; such
      asymmetric soups live far longer than symmetric cubes of comparable size ${tag('measured')}
      ${src(N, 'asymmetric octahedral soups', 'notebook')}. Then explore freely: the
      gallery, the editor (press <b>E</b> to paint faces, with symmetry if you like), the layer slicer, and
      the colour modes. <i>Fate</i> mode shows which faces are about to die or be born. Every view has a
      shareable link.</p>
      <p>Why this rule? Among 960 neighbouring rules, chaos on a wrap-around box is common, but long-lived
      chaos <i>confined</i> to an octahedron is not. Gump is a minimal member of that rare group: remove any
      one count from B45/S345 and lifetimes collapse; add survival at 2 or 7 and they grow 30× or more. ${tag('measured')}
      ${src(N, 'is one of the 50 minimal elements', 'notebook: rule space')} ${fig('research/figures/phase_rulemap.png', 'rule map')}</p>`,
    spec: { seed: 'soup', shape: 'oct', n: 8, density: 0.35, rng: 7, speed: 'max', play: 1, cam: '1,0.75,1.35,1.2' },
    kymo: true,
    gallery: true,
  },
];
