use std::collections::HashSet;
use std::hash::{Hash, Hasher};


#[derive(Debug, Clone)] // Derive PartialEq and Eq
pub struct States {
    pub rods: [Vec<u32>; 3],
    num_of_pegs: u32,
    acc_cost: f32,
    total_disks: usize,
}

impl States {
    pub fn new(rod1: Vec<u32>, rod2: Vec<u32>, rod3: Vec<u32>, acc_cost: f32) -> Self {
        let instance = Self {
            rods: [rod1.clone(), rod2.clone(), rod3.clone()],
            num_of_pegs: 3,
            acc_cost,
            total_disks: 0,
        };

        if !instance.check_uniqueness() {
            panic!("Duplicated disks");
        }

        if !instance.check_sortness() {
            panic!("Ilegal order of disks")
        }

        let total = instance.rods.iter().map(|r| r.len()).sum();

        Self {
            total_disks: total,
            ..instance
        }
    }

    pub fn check_uniqueness(&self) -> bool {
        let all_disks = self.rods.iter().flatten().copied();
        let unique: HashSet<_> = all_disks.clone().collect();
        let total_disks = all_disks.count();
        unique.len() == total_disks
    }
    pub fn check_sortness(&self) -> bool {
        for rod in &self.rods {
            if !rod.is_empty() {
                if rod.windows(2).all(|w| w[0] < w[1]) {
                    return false;
                }
            }
        }
        true
    }

    pub fn get_last_disk_rod(&self, number_rod: usize) -> Option<u32> {
        self.rods
            .get(number_rod)
            .and_then(|rod| rod.last().copied())
    }

    pub fn check_valid_disk_in_rod(&self, number_rod: usize, disk: u32) -> bool {
        match self.get_last_disk_rod(number_rod) {
            Some(top) => {
                disk < top
            }
            None => true,
        }
    }

    pub fn put_disk_in_rod(&mut self, num_rod: usize, disk: u32) -> Result<(), &'static str> {
        if self.check_valid_disk_in_rod(num_rod, disk) {
            if let Some(rod) = self.rods.get_mut(num_rod) {
                rod.push(disk);
                Ok(())
            } else {
                Err("Invalid rod")
            }
        } else {
            Err("Invalid movement: disk too large for top")
        }
    }

    pub fn pop_disk_from_rod(&mut self, number_rod: usize) -> Option<u32> {
        self.rods.get_mut(number_rod).and_then(|rod| rod.pop())
    }

    pub fn accumulate_cost(&mut self, cost: f32) {
        self.acc_cost += cost;
    }

    pub fn get_acc_cost(&self) -> f32 {
        self.acc_cost
    }

}
impl States {
    // ... existing methods ...

    pub fn pretty_print(&self) {
        let max_height = self.rods.iter().map(|r| r.len()).max().unwrap_or(0);

        println!("Rod 1 | Rod 2 | Rod 3");
        println!("----------------------");

        for i in (0..max_height).rev() {
            // Return the actual String, not a reference
            let r1 = self.rods[0].get(i).map_or("     ".to_string(), |d| d.to_string());
            let r2 = self.rods[1].get(i).map_or("     ".to_string(), |d| d.to_string());
            let r3 = self.rods[2].get(i).map_or("     ".to_string(), |d| d.to_string());

            println!(" {:^5}| {:^5}| {:^5}", r1, r2, r3);
        }

        println!(); // Add space between states
    }
}

impl PartialEq for States {
    fn eq(&self, other: &Self) -> bool {
        self.rods == other.rods && self.num_of_pegs == other.num_of_pegs
    }
}

impl Eq for States {} 

impl Hash for States {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.rods.hash(state);
        self.num_of_pegs.hash(state);
        self.acc_cost.to_bits().hash(state); // f32 can be hashed as bits
        self.total_disks.hash(state);
    }
}