use std::collections::{BinaryHeap, HashMap, HashSet};
use std::cmp::Ordering;
use std::rc::Rc;
use crate::node::Node;
use crate::problem::Problem;

struct PriorityNode<S, A> {
    node: Rc<dyn Node<S, A>>,
    f_score: f32,
}

impl<S, A> Eq for PriorityNode<S, A> {}

impl<S, A> PartialEq for PriorityNode<S, A> {
    fn eq(&self, other: &Self) -> bool {
        self.f_score == other.f_score
    }
}

impl<S, A> PartialOrd for PriorityNode<S, A> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(other.f_score.partial_cmp(&self.f_score).unwrap_or(Ordering::Equal))
    }
}

impl<S, A> Ord for PriorityNode<S, A> {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap()
    }
}

pub fn a_star_search<S, A>(
    problem: &dyn Problem<S, A>,
    initial_node: Rc<dyn Node<S, A>>,
) -> Option<Rc<dyn Node<S, A>>>
where
    S: Clone + Eq + std::hash::Hash + 'static,
    A: Clone + 'static,
{
    let mut open_set = BinaryHeap::new();
    let mut closed_set = HashSet::new();
    let mut g_score = HashMap::new();

    let f_score = initial_node.path_cost();

    open_set.push(PriorityNode {
        node: initial_node.clone_rc(),
        f_score,
    });
    g_score.insert(initial_node.state().clone(), initial_node.path_cost());

    while let Some(PriorityNode { node, .. }) = open_set.pop() {
        if problem.goal_test(node.state()) {
            return Some(node);
        }

        if closed_set.contains(node.state()) {
            continue;
        }
        closed_set.insert(node.state().clone());

        for child in node.expand(problem) {
            let tentative_g = node.path_cost() + problem.path_cost(node.path_cost(), child.state());

            let state = child.state();
            if closed_set.contains(state) {
                continue;
            }

            let current_g = *g_score.entry(state.clone()).or_insert(f32::INFINITY);

            if tentative_g < current_g {
                g_score.insert(state.clone(), tentative_g);
                open_set.push(PriorityNode {
                    node: child.clone_rc(),
                    f_score: tentative_g,
                });
            }
        }
    }

    None 
}
