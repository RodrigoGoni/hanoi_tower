use crate::states::States;

#[derive(Debug)]
#[derive(Clone)]
#[derive(PartialEq)]
pub enum ACTIONS {
    Move,
}

#[derive(Debug)]
#[derive(Clone)]
#[derive(PartialEq)]
pub struct Action {
    pub rod_input: usize,
    pub rod_output: usize,
    pub action: ACTIONS,
}

impl Action {

    pub fn apply_action(&self, state: &States) -> Result<States, &'static str> {
        if self.action == ACTIONS::Move {
            let mut new_state = state.clone();
    
            if let Some(disk) = new_state.pop_disk_from_rod(self.rod_input) {
                match new_state.put_disk_in_rod(self.rod_output, disk) {
                    Ok(_) => {
                        new_state.accumulate_cost(1.0);
                        Ok(new_state)
                    }
                    Err(err) => {
                        new_state.put_disk_in_rod(self.rod_input, disk).unwrap();
                        Err(err)
                    }
                }
            } else {
                Err("Input rod is empty")
            }
        } else {
            Ok(state.clone())
        }
    }

}
