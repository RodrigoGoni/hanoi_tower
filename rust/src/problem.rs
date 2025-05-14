
use crate::states::States;
use crate::actions::Action;

pub trait Problem<State,Action> 
where 
    State: Clone + PartialEq,
    Action: Clone
{
    fn goal_state(&self) -> Option<State> {
        None
    }
    fn actions(&self,state: &State) -> Vec<Action>;
    fn result(&self, state: &State, action: &Action) -> State;
    fn goal_test(&self,state: &State) -> bool {
        match self.goal_state() {
            Some(goal) => *state == goal,
            None => false,
        }
    }
    fn path_cost(&self, cost_so_far: f32, _state2: &State) -> f32 {
        cost_so_far + 1.0
    }
}


pub struct HanoiProblem {
    pub initial: States,
    pub goal: Option<States>
}

impl Problem<States,Action> for HanoiProblem {
    fn goal_state(&self) -> Option<States> {
        self.goal.clone()
    }
    fn actions(&self,state: &States) -> Vec<Action> {
        let mut actions = vec![];
        for from in 0..3 {
            if let Some(disk) = state.get_last_disk_rod(from) {
                for to in 0..3 {
                    if from != to && state.check_valid_disk_in_rod(to, disk){
                        actions.push(Action {
                            rod_input: from,
                            rod_output: to,
                            action: crate::actions::ACTIONS::Move,
                        });
                    }
                }
            }
        }
        actions
    }

    fn result(&self, state: &States, action: &Action) -> States {
        action.apply_action(state).unwrap_or_else(|_| state.clone())
    }
    fn goal_test(&self, state: &States) -> bool {
        if let Some(goal) = &self.goal {
            state == goal 
        } else {
            false
        }
    }
    fn path_cost(&self, cost_so_far: f32, _state2: &States) -> f32 {
        cost_so_far + _state2.get_acc_cost()
    }

}