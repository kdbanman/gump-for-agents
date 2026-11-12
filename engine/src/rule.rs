//! Outer-totalistic rules over neighbour counts 0..=12.

use std::fmt;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct Rule {
    /// bit n set: a dead cell with n live neighbours is born
    pub birth: u16,
    /// bit n set: a live cell with n live neighbours survives
    pub survive: u16,
}

impl Rule {
    /// The gump rule B45/S345.
    pub const GUMP: Rule = Rule { birth: (1 << 4) | (1 << 5), survive: (1 << 3) | (1 << 4) | (1 << 5) };

    #[inline]
    pub fn next(&self, alive: bool, n: u32) -> bool {
        let set = if alive { self.survive } else { self.birth };
        (set >> n) & 1 == 1
    }

    pub fn is_gump(&self) -> bool {
        *self == Rule::GUMP
    }

    /// Smallest birth count (None if nothing is ever born). T2/T3 hold when this is >= 4.
    pub fn min_birth(&self) -> Option<u32> {
        (0..=12).find(|&n| (self.birth >> n) & 1 == 1)
    }

    /// Parse `B45/S345`, `b45/s345`, `B4,5/S3,4,5` (commas needed for counts >= 10),
    /// or `B/S` style with empty sets.
    pub fn parse(s: &str) -> Result<Rule, String> {
        let s = s.trim();
        let (bpart, spart) = s.split_once('/').ok_or_else(|| format!("rule '{s}': expected B…/S…"))?;
        fn set(part: &str, letter: char) -> Result<u16, String> {
            let mut chars = part.chars();
            let l = chars.next().ok_or("empty rule part")?;
            if l.to_ascii_uppercase() != letter {
                return Err(format!("rule part '{part}' should start with {letter}"));
            }
            let body: String = chars.collect();
            let mut m = 0u16;
            let items: Vec<String> = if body.contains(',') {
                body.split(',').filter(|t| !t.is_empty()).map(|t| t.to_string()).collect()
            } else {
                body.chars().map(|c| c.to_string()).collect()
            };
            for it in items {
                let n: u32 = it.trim().parse().map_err(|_| format!("bad count '{it}' in rule"))?;
                if n > 12 {
                    return Err(format!("count {n} > 12 in rule"));
                }
                m |= 1 << n;
            }
            Ok(m)
        }
        Ok(Rule { birth: set(bpart, 'B')?, survive: set(spart, 'S')? })
    }
}

impl fmt::Display for Rule {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let list = |m: u16| -> String {
            let v: Vec<u32> = (0..=12).filter(|&n| (m >> n) & 1 == 1).collect();
            if v.iter().any(|&n| n >= 10) {
                v.iter().map(|n| n.to_string()).collect::<Vec<_>>().join(",")
            } else {
                v.iter().map(|n| n.to_string()).collect::<String>()
            }
        };
        write!(f, "B{}/S{}", list(self.birth), list(self.survive))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn parse_roundtrip() {
        assert_eq!(Rule::parse("B45/S345").unwrap(), Rule::GUMP);
        assert_eq!(Rule::parse("b4,5/s3,4,5").unwrap(), Rule::GUMP);
        for s in ["B45/S345", "B4/S", "B/S0", "B4,10,12/S3,11"] {
            assert_eq!(Rule::parse(s).unwrap().to_string(), s);
        }
        assert!(Rule::parse("B4,13/S").is_err());
    }
}
