use std::fmt;

#[derive(Clone, Debug)]
pub struct Password(String);

impl Password {
    pub fn new(password: String) -> Self {
        assert!(
            password.chars().all(|c| c.is_ascii_lowercase()),
            "Password must contain only lowercase ASCII letters"
        );
        Self(password)
    }

    pub fn password(&self) -> &str {
        &self.0
    }
}

impl fmt::Display for Password {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl Password {
    fn increment(&mut self) -> Option<&Self> {
        for (i, c) in unsafe { self.0.as_bytes_mut() }
            .iter_mut()
            .enumerate()
            .rev()
        {
            if *c == b'z' {
                if i == 0 {
                    break;
                }
                *c = b'a';
            } else {
                *c += 1;
                return Some(self);
            }
        }
        None
    }

    fn contains_straight(&self) -> bool {
        self.0
            .as_bytes()
            .windows(3)
            .any(|w| w[0] + 1 == w[1] && w[1] + 1 == w[2])
    }

    fn contains_confusing(&self) -> bool {
        self.0.contains(['i', 'o', 'l'])
    }

    fn contains_non_overlapping_pairs(&self) -> bool {
        let mut pairs = self.0.as_bytes().windows(2).filter(|&w| w[0] == w[1]);
        pairs.next().is_some_and(|p| pairs.any(|q| q != p))
    }

    fn is_valid(&self) -> bool {
        self.contains_straight()
            && !self.contains_confusing()
            && self.contains_non_overlapping_pairs()
    }
}

#[derive(Clone)]
pub struct PasswordGenerator {
    password: Password,
}

impl PasswordGenerator {
    pub fn new(password: Password) -> Self {
        let mut password = password;
        password.increment();
        Self { password }
    }
}

impl Iterator for PasswordGenerator {
    type Item = Password;

    fn next(&mut self) -> Option<Self::Item> {
        while !self.password.is_valid() {
            self.password.increment()?;
        }
        let valid_password = self.password.clone();
        self.password.increment();
        Some(valid_password)
    }
}
