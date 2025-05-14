mod a_start_search;
mod actions;
mod node;
mod problem;
mod states;

use a_start_search::a_star_search;
use actions::Action;
use node::NodeHanoi;
use problem::HanoiProblem;
use states::States;
use std::rc::Rc;
use std::time::Instant;

fn main() {
    let state_i = States::new(vec![5, 4, 3, 2, 1], vec![], vec![], 0.0);
    let state_f = States::new(vec![], vec![], vec![5, 4, 3, 2, 1], 0.0);

    let problem: HanoiProblem = HanoiProblem {
        initial: state_i.clone(),
        goal: Some(state_f),
    };

    let root_node: Rc<NodeHanoi<States, Action>> = Rc::new(NodeHanoi {
        state: state_i.clone(),
        parent: None,
        action: None,
        path_cost: 0.0,
        depth: 0,
    });

    let start = Instant::now();

    let result = a_star_search(&problem, root_node);

    let duration = start.elapsed();

    println!("⏱️ A* search took {:.4} seconds", duration.as_secs_f64());

    match result {
        Some(solution_node) => {
            println!(
                "✅ Solution found in {} moves.",
                solution_node.solution().len()
            );
        }
        None => {
            println!("❌ No solution found.");
        }
    }
}
