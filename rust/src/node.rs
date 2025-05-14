use std::rc::Rc;
use crate::problem::Problem;

pub trait Node<S, A>: 'static
where
    S: Clone + Eq + std::hash::Hash + 'static,
    A: Clone + 'static,
{
    fn state(&self) -> &S;
    fn parent(&self) -> Option<Rc<dyn Node<S, A>>>;
    fn action(&self) -> Option<&A>;
    fn path_cost(&self) -> f32;

    fn child_node(&self, problem: &dyn crate::problem::Problem<S, A>, action: A) -> Rc<dyn Node<S, A>>;

    fn solution(&self) -> Vec<A> {
        self.path()
            .into_iter()
            .skip(1)
            .filter_map(|n| n.action().cloned())
            .collect()
    }

    fn expand(&self, problem: &dyn Problem<S, A>) -> Vec<Rc<dyn Node<S, A>>> {
        problem
            .actions(self.state())
            .into_iter()
            .map(|action| self.child_node(problem, action))
            .collect()
    }

    fn path(&self) -> Vec<Rc<dyn Node<S, A>>> {
        let mut node: Option<Rc<dyn Node<S, A>>> = Some(self.clone_rc());
        let mut path = vec![];
        while let Some(n) = node {
            node = n.parent(); // ← Both sides are Rc<dyn Node<S, A>>
            path.push(Rc::clone(&n));
        }
        path.reverse();
        path
    }

    fn clone_rc(&self) -> Rc<dyn Node<S, A>>;
}


#[derive(Clone)]
pub struct NodeHanoi<S, A> {
    pub state: S,
    pub parent: Option<Rc<dyn Node<S, A>>>,
    pub action: Option<A>,
    pub path_cost: f32,
    pub depth: usize,
}


impl<S, A> Node<S, A> for NodeHanoi<S, A>
where
    S: Clone + Eq + std::hash::Hash + 'static,
    A: Clone + 'static,
{
    fn state(&self) -> &S {
        &self.state
    }

    fn parent(&self) -> Option<Rc<dyn Node<S, A>>> {
        self.parent.clone()
    }

    fn action(&self) -> Option<&A> {
        self.action.as_ref()
    }

    fn path_cost(&self) -> f32 {
        self.path_cost
    }

    fn child_node(&self, problem: &dyn Problem<S, A>, action: A) -> Rc<dyn Node<S, A>> {
        let next_state = problem.result(&self.state, &action);
        let next_cost = problem.path_cost(self.path_cost, &next_state);
        Rc::new(NodeHanoi {
            state: next_state,
            parent: Some(self.clone_rc()),
            action: Some(action),
            path_cost: next_cost,
            depth: self.depth + 1,
        })
    }

    fn clone_rc(&self) -> Rc<dyn Node<S, A>> {
        Rc::new(self.clone())
    }
}