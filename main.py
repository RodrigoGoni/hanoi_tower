from aima_libs.hanoi_states import ProblemHanoi, StatesHanoi, ActionHanoi
import heapq
import json
import itertools
import logging
import time
import tracemalloc

logging.basicConfig(
    filename="logs/hanoi_solver.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

counter = itertools.count()


def calc_f(problem: ProblemHanoi, accion: ActionHanoi, estado_actual: StatesHanoi, nuevo_estado: StatesHanoi, heuristic) -> tuple:
    """
    Calculate the f value for the A* algorithm.
    :param estado: The current state of the Tower of Hanoi.
    :param accion: The action taken to reach the current state.
    :param inicial: The initial state of the Tower of Hanoi.
    :return: The f value.
    """
    g = problem.path_cost(estado_actual, accion)
    h = heuristic(nuevo_estado, problem.goal)
    return g, h, g + h


def a_star(problem: ProblemHanoi, heuristic) -> tuple[StatesHanoi, list]:
    """
    A* search algorithm for the Tower of Hanoi problem.
    Profe segui pseudocódigo para este algoritmo, A* es un algoritmo que ya he usado en el pasado,
    para el path planning en robotica. Para la implementacion de este algoritmo, tuve activado el
    copilot.
    :param problem: The Tower of Hanoi problem instance.
    :return: A tuple containing the solution state and the list of movements.
    """

    abierta = []
    movimientos_previos = []
    g_inicial, _, f_inicial = calc_f(problem, problem.actions(problem.initial)
                                     [0], problem.initial, problem.initial, heuristic)
    heapq.heappush(abierta, (f_inicial, next(counter), movimientos_previos,
                   problem.initial))
    cerrada = set()
    mejores_costos = {problem.initial: g_inicial}
    while abierta:

        f, _, movimientos_previos, actual = heapq.heappop(abierta)

        if actual == problem.goal:
            return actual, movimientos_previos, abierta, cerrada
        if actual in cerrada:
            continue
        cerrada.add(actual)
        for accion in problem.actions(actual):
            nuevo_movimiento = {
                "type": "movement",
                "disk": accion.disk,
                "peg_start": accion.rod_input+1,
                "peg_end": accion.rod_out+1,
            }
            nuevo_estado = problem.result(actual, accion)
            nuevo_g, nuevo_h, nuevo_f = calc_f(
                problem, accion, actual, nuevo_estado, heuristic)
            if nuevo_estado not in mejores_costos or nuevo_g < mejores_costos[nuevo_estado]:
                mejores_costos[nuevo_estado] = nuevo_g
                heapq.heappush(abierta, (nuevo_f, next(counter), movimientos_previos + [nuevo_movimiento],
                               nuevo_estado))
    return None, []


def basic_a_star(problem: ProblemHanoi, heuristic) -> tuple[StatesHanoi, list]:
    abierta = []
    movimientos_previos = []
    g_inicial, _, f_inicial = calc_f(problem, problem.actions(problem.initial)
                                     [0], problem.initial, problem.initial, heuristic)
    heapq.heappush(abierta, (f_inicial, next(counter), movimientos_previos,
                   problem.initial))
    cerrada = set()
    while abierta:
        f, _, movimientos_previos, actual = heapq.heappop(abierta)

        if actual == problem.goal:
            return actual, movimientos_previos, abierta, cerrada

        if actual in cerrada:
            continue
        cerrada.add(actual)
        for accion in problem.actions(actual):
            nuevo_estado = problem.result(actual, accion)
            nuevo_movimiento = {
                "type": "movement",
                "disk": accion.disk,
                "peg_start": accion.rod_input+1,
                "peg_end": accion.rod_out+1,
            }
            _, _, nuevo_f = calc_f(
                problem, accion, actual, nuevo_estado, heuristic)
            if nuevo_estado not in cerrada:
                heapq.heappush(abierta, (nuevo_f, next(counter), movimientos_previos + [nuevo_movimiento],
                               nuevo_estado))

    return None, []


def hanoi_heuristic_2(current_state: StatesHanoi, goal_state: StatesHanoi) -> int:
    """
    Improved heuristic for the Tower of Hanoi.
    This heuristic considers:
    - Disks not in the correct rod.
    - Disks out of order (a larger disk above a smaller one).
    """
    current_rods = current_state.get_state()
    goal_rods = goal_state.get_state()
    total_disks = current_state.number_of_disks

    misplaced_penalty = 0
    disorder_penalty = 0

    # Build a mapping from disk -> correct rod (goal position)
    disk_goal_rod = {}
    for rod_index, rod in enumerate(goal_rods):
        for disk in rod:
            disk_goal_rod[disk] = rod_index

    for rod_index, rod in enumerate(current_rods):
        for depth, disk in enumerate(rod):
            # 1. Penalize if disk is not on its goal rod
            if disk_goal_rod[disk] != rod_index:
                misplaced_penalty += 1

            # 2. Penalize if any disk above this one is smaller (invalid state)
            if depth > 0 and rod[depth - 1] < disk:
                disorder_penalty += 1

    return misplaced_penalty + disorder_penalty


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
    with open("simulator/goal_state.json", "r") as f:
        goal_state_data = json.load(f)
    peg_1 = goal_state_data.get("peg_1", [])
    peg_2 = goal_state_data.get("peg_2", [])
    peg_3 = goal_state_data.get("peg_3", [])
    if is_valid_hanoi_state(peg_1, peg_2, peg_3, max_disks=5):
        print("Goal state is valid.")
    else:
        print("Goal state is invalid.")
        return None
    goal_state = StatesHanoi(peg_1, peg_2, peg_3, max_disks=5)

    problem = ProblemHanoi(initial=initial_state, goal=goal_state)
    return problem


def run_search(problem: ProblemHanoi, algorithm, heuristic) -> None:
    logger.info(
        "#################### Starting search algorithm ####################")
    logger.info(f"Running search algorithm: {algorithm.__name__}")
    logger.info(f"Initial state:\n{problem.initial}")
    logger.info(f"Goal state:\n{problem.goal}")
    tracemalloc.start()  # Start measuring memory
    start_time = time.perf_counter()  # High-resolution timer
    solution, movimientos, abierta, exploration = algorithm(problem, heuristic)
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()  # Stop measuring memory
    logger.info(f"Execution time: {end_time - start_time:.6f} seconds")
    logger.info(f"Peak memory usage: {peak / 1024:.2f} KB")
    with open(f"simulator/sequence{algorithm.__name__}.json", "w") as f:
        json.dump(movimientos, f, indent=4)
    abierta_serializable = []
    for f_val, count, _, estado in abierta:
        abierta_serializable.append({
            "f": f_val,
            "count": count,
            "estado": estado.__str__(),
        })

    with open(f"simulator/queue_{algorithm.__name__}.json", "w") as f:
        json.dump(abierta_serializable, f, indent=4)
    if solution:
        logger.info(f"Cantidad de nodos abiertos: {len(abierta)}")
        logger.info(f"Cantidad de nodos movimientos: {len(movimientos)}")
        logger.info(f"Cantidad de nodos cerrados: {len(exploration)}")
        optimal_moves = 2**problem.initial.number_of_disks - 1
        logger.info(f"Solicion optima es 2^n - 1 = {optimal_moves}")
        if len(movimientos) == optimal_moves:
            logger.info("Solution is optimal")
        else:
            logger.info("Solution is not optimal")
        logger.info(f"Solution found: {solution}")

    else:
        logger.info(f"❌ No solution found using {algorithm.__name__}")


if __name__ == '__main__':
    problem = define_problem()
    if problem is None:
        print("Invalid initial state. Exiting.")
        exit(1)
    logger.info("Starting Tower of Hanoi solver")

    run_search(problem,  basic_a_star, heuristic=hanoi_heuristic)
    run_search(problem, basic_a_star, heuristic=hanoi_heuristic_2)
    run_search(problem, a_star, heuristic=hanoi_heuristic)
    run_search(problem, a_star, heuristic=hanoi_heuristic_2)
