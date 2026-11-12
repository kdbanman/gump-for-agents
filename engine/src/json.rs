//! Minimal JSON writing (no dependencies).

pub trait ToJson {
    fn json(&self) -> String;
}

macro_rules! num {
    ($($t:ty),*) => {$(impl ToJson for $t { fn json(&self) -> String { self.to_string() } })*};
}
num!(u8, u16, u32, u64, usize, i32, i64);

impl ToJson for f64 {
    fn json(&self) -> String {
        if self.is_finite() {
            let s = format!("{}", self);
            if s.contains('e') || s.contains('.') { s } else { format!("{s}.0") }
        } else {
            "null".into()
        }
    }
}
impl ToJson for bool {
    fn json(&self) -> String {
        self.to_string()
    }
}
impl ToJson for str {
    fn json(&self) -> String {
        let mut o = String::with_capacity(self.len() + 2);
        o.push('"');
        for c in self.chars() {
            match c {
                '"' => o.push_str("\\\""),
                '\\' => o.push_str("\\\\"),
                '\n' => o.push_str("\\n"),
                '\t' => o.push_str("\\t"),
                '\r' => o.push_str("\\r"),
                c if (c as u32) < 0x20 => o.push_str(&format!("\\u{:04x}", c as u32)),
                c => o.push(c),
            }
        }
        o.push('"');
        o
    }
}
impl ToJson for String {
    fn json(&self) -> String {
        self.as_str().json()
    }
}
impl ToJson for &str {
    fn json(&self) -> String {
        (*self).json()
    }
}
impl<T: ToJson> ToJson for Option<T> {
    fn json(&self) -> String {
        match self {
            Some(v) => v.json(),
            None => "null".into(),
        }
    }
}
impl<T: ToJson> ToJson for [T] {
    fn json(&self) -> String {
        let parts: Vec<String> = self.iter().map(|v| v.json()).collect();
        format!("[{}]", parts.join(","))
    }
}
impl<T: ToJson> ToJson for Vec<T> {
    fn json(&self) -> String {
        self.as_slice().json()
    }
}
impl<T: ToJson, const N: usize> ToJson for [T; N] {
    fn json(&self) -> String {
        self.as_slice().json()
    }
}
impl<A: ToJson, B: ToJson> ToJson for (A, B) {
    fn json(&self) -> String {
        format!("[{},{}]", self.0.json(), self.1.json())
    }
}

/// Raw, already-encoded JSON.
pub struct Raw(pub String);
impl ToJson for Raw {
    fn json(&self) -> String {
        self.0.clone()
    }
}

/// Object builder preserving field order.
#[derive(Default)]
pub struct Obj {
    s: String,
}

impl Obj {
    pub fn new() -> Self {
        Obj { s: String::from("{") }
    }
    pub fn f<T: ToJson + ?Sized>(mut self, k: &str, v: &T) -> Self {
        if self.s.len() > 1 {
            self.s.push(',');
        }
        self.s.push_str(&k.json());
        self.s.push(':');
        self.s.push_str(&v.json());
        self
    }
    pub fn end(mut self) -> String {
        self.s.push('}');
        self.s
    }
}
