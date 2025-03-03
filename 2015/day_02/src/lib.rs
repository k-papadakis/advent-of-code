#[derive(Debug, Clone, Copy)]
pub struct Prism {
    pub l: u32,
    pub w: u32,
    pub h: u32,
}

impl Prism {
    fn face_areas(&self) -> [u32; 3] {
        [self.l * self.w, self.l * self.h, self.w * self.h]
    }

    fn face_perimeters(&self) -> [u32; 3] {
        [
            2 * (self.l + self.w),
            2 * (self.l + self.h),
            2 * (self.w + self.h),
        ]
    }

    fn volume(&self) -> u32 {
        self.l * self.w * self.h
    }

    pub fn required_paper(&self) -> u32 {
        let faces = self.face_areas();
        let min_face = faces.into_iter().min().unwrap();
        let area = 2 * faces.iter().sum::<u32>();
        area + min_face
    }

    pub fn required_ribbon(&self) -> u32 {
        let perimeters = self.face_perimeters();
        let min_perimeter = perimeters.into_iter().min().unwrap();
        let volume = self.volume();
        min_perimeter + volume
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_required_paper() {
        let prism1 = Prism { l: 2, w: 3, h: 4 };
        println!("{:?}", prism1.face_areas());
        assert_eq!(prism1.required_paper(), 58);

        let prism2 = Prism { l: 1, w: 1, h: 10 };
        assert_eq!(prism2.required_paper(), 43);
    }

    #[test]
    fn test_requirerd_ribbon() {
        let prism1 = Prism { l: 2, w: 3, h: 4 };
        assert_eq!(prism1.required_ribbon(), 34);

        let prism2 = Prism { l: 1, w: 1, h: 10 };
        assert_eq!(prism2.required_ribbon(), 14);
    }
}
