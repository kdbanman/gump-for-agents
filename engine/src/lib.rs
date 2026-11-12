//! gump: fast engine and instruments for the gump automaton (faces of the cubic
//! honeycomb, rule B45/S345). See `docs/AUTOMATON.md` and `engine/README.md`.
pub mod fast;
pub mod instruments;
pub mod seeds;
pub mod snapshot;
pub mod lattice;
pub mod rule;
pub mod scalar;

pub use fast::BitSim;
pub use lattice::{Boundary, Geometry, Hull, P3};
pub use rule::Rule;
pub use scalar::ScalarSim;
