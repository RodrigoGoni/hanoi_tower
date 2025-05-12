from aima_libs.hanoi_states import ProblemHanoi, StatesHanoi
import heapq
import json
import itertools
import logging

logging.basicConfig(
    filename="logs/hanoi_solver.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

counter = itertools.count()


def my_search_algorithms(problem: ProblemHanoi) -> tuple[StatesHanoi, list]:
    """
    A* search algorithm for the Tower of Hanoi problem. 
    Profe segui pseudocódigo para este algoritmo, A* es un algoritmo que ya he usado en el pasado,
    para el path planning en robotica. Para la implementacion de este algoritmo, tuve activado el
    copilot.
    :param problem: The Tower of Hanoi problem instance.
    :return: A tuple containing the solution state and the list of movements.
    """

    abierta = []
    costo = problem.path_cost(problem.initial, problem.actions(problem.initial)[
                              0]) + hanoi_heuristic(problem.initial, problem.goal)
    movimientos_iniciales = []
    heapq.heappush(abierta, (costo, next(counter),
                   problem.initial, movimientos_iniciales))
    cerrada = set()

    while abierta:
        costo, _, actual, movimientos = heapq.heappop(abierta)
        logger.info(f"Evaluating state: {actual}")
        logger.info(f"Current cost: {costo}")
        if actual == problem.goal:
            return actual, movimientos
        cerrada.add(actual)

        for accion in problem.actions(actual):
            nuevo_movimiento = {
                "type": "movement",
                "disk": accion.disk,
                "peg_start": accion.rod_input+1,
                "peg_end": accion.rod_out+1,
            }
            logger.info(f"Evaluating action: {accion}")
            nuevo_estado = problem.result(actual, accion)
            nuevos_movimientos = movimientos + [nuevo_movimiento]

            if nuevo_estado not in cerrada:
                costo = problem.path_cost(
                    actual, accion) + hanoi_heuristic(nuevo_estado, goal_state=problem.goal)
                heapq.heappush(abierta, (costo, next(counter),
                               nuevo_estado, nuevos_movimientos))


def hanoi_heuristic(current_state: StatesHanoi, goal_state: StatesHanoi) -> int:
    """
    Heuristic function for the Tower of Hanoi problem.
    This heuristic is based on the number of disks that are in the correct position.
    :param current_state: The current state of the Tower of Hanoi.
    :param
    goal_state: The goal state of the Tower of Hanoi.
    :return: The heuristic value.
    """
    current_rods = current_state.get_state()
    goal_rods = goal_state.get_state()
    correct_disks = 0

    for i in range(len(current_rods)):
        for j in range(min(len(current_rods[i]), len(goal_rods[i]))):
            if current_rods[i][j] == goal_rods[i][j]:
                correct_disks += 1
            else:
                break

    total_disks = current_state.number_of_disks
    return total_disks - correct_disks


def is_valid_hanoi_state(peg_1, peg_2, peg_3, max_disks):
    # Combine all disks from the three pegs
    all_disks = peg_1 + peg_2 + peg_3

    # Check that each disk is unique and in the correct range
    if sorted(all_disks) != list(range(1, max_disks + 1)):
        return False

    # Check that each peg is in strictly decreasing order
    for peg in [peg_1, peg_2, peg_3]:
        if peg != sorted(peg, reverse=True):
            return False

    return True


def define_problem() -> ProblemHanoi:
    """
    Define the Tower of Hanoi problem.
    :return: An instance of the Tower of Hanoi problem.
    """
    with open("simulator/initial_state.json", "r") as f:
        initial_state_data = json.load(f)
    peg_1 = initial_state_data.get("peg_1", [])
    peg_2 = initial_state_data.get("peg_2", [])
    peg_3 = initial_state_data.get("peg_3", [])
    if is_valid_hanoi_state(peg_1, peg_2, peg_3, max_disks=5):
        print("Initial state is valid.")
    else:
        print("Initial state is invalid.")
        return None
    # Create the initial state instance
    initial_state = StatesHanoi(peg_1, peg_2, peg_3, max_disks=5)
    goal_state = StatesHanoi([], [], [5, 4, 3, 2, 1], max_disks=5)

    problem = ProblemHanoi(initial=initial_state, goal=goal_state)
    return problem


def run_search(problem: ProblemHanoi, algorithm):
    logger.info(f"Running search algorithm: {algorithm.__name__}")
    solution, movimientos = algorithm(problem)
    with open("simulator/sequence.json", "w") as f:
        json.dump(movimientos, f, indent=4)
    if solution:
        logger.info(f"Solution found: {solution}")
        logger.info(f"Solution found using {algorithm.__name__}")
        logger.info(f"Initial state:\n{problem.initial}")
        logger.info(f"Goal state:\n{problem.goal}")
        logger.info(f"Solution state:\n{solution}")

    else:
        logger.info(f"❌ No solution found using {algorithm.__name__}")


if __name__ == '__main__':
    problem = define_problem()
    if problem is None:
        print("Invalid initial state. Exiting.")
        exit(1)
    logger.info("Starting Tower of Hanoi solver")
    logger.info(f"Initial state:\n{problem.initial}")
    logger.info(f"Goal state:\n{problem.goal}")
    logger.info("Running search algorithm")
    logger.info(f"Algorithm: {my_search_algorithms.__name__}")
    run_search(problem, my_search_algorithms)
