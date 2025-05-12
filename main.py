from aima_libs.hanoi_states import ProblemHanoi, StatesHanoi
import heapq
import json
import itertools
counter = itertools.count()

def my_search_algorithms(problem):
    abierta = []
    costo = problem.path_cost(problem.initial,problem.actions(problem.initial)[0]) + hanoi_heuristic(problem.initial, problem.goal)
    movimientos_iniciales = []
    heapq.heappush(abierta, (costo,next(counter), problem.initial, movimientos_iniciales))
    
    cerrada = set()
    while abierta:
        costo,_, actual, movimientos = heapq.heappop(abierta)
        print(f"Evaluating state: {actual}")
        if actual==problem.goal:
            return actual, movimientos
        cerrada.add(actual)
        for accion in problem.actions(actual):
            nuevo_movimiento = {
                "type": "movement",
                "disk": accion.disk,
                "peg_start": accion.rod_input+1,
                "peg_end": accion.rod_out+1,
            }
            print(f"Evaluating action: {accion}")
            nuevo_estado = problem.result(actual, accion)
            nuevos_movimientos = movimientos + [nuevo_movimiento]
            
            if nuevo_estado not in cerrada:
                costo = problem.path_cost(actual,accion) + hanoi_heuristic(nuevo_estado,goal_state=problem.goal)
                print(f"New cost: {costo}")
                heapq.heappush(abierta, (costo,next(counter), nuevo_estado, nuevos_movimientos))


def hanoi_heuristic(current_state: StatesHanoi, goal_state: StatesHanoi) -> int:
    current_rods = current_state.get_state()
    goal_rods = goal_state.get_state()
    correct_disks = 0

    for i in range(len(current_rods)):
        for j in range(min(len(current_rods[i]), len(goal_rods[i]))):
            if current_rods[i][j] == goal_rods[i][j]:
                correct_disks += 1
            else:
                break  # stop comparing once a mismatch is found in the rod

    total_disks = current_state.number_of_disks
    return total_disks - correct_disks


def define_problem():
    # Initial and goal states
    initial_state = StatesHanoi([5, 4, 3, 2, 1], [], [], max_disks=5)
    goal_state = StatesHanoi([], [], [5, 4, 3, 2, 1], max_disks=5)

    # Define the problem
    problem = ProblemHanoi(initial=initial_state, goal=goal_state)
    return problem

def run_search(problem, algorithm):
    solution, movimientos = algorithm(problem)
    with open("movimientos.json", "w") as f:
        json.dump(movimientos, f, indent=4)
    if solution:
        print(f"\n✅ Solution found using {algorithm.__name__}")
        print("\n🔁 Steps to reach the goal:")
        print(f"Initial state:\n{problem.initial}")
        print(f"Goal state:\n{problem.goal}")
        print(f"Solution state:\n{solution}")

    else:
        print(f"❌ No solution found using {algorithm.__name__}")

if __name__ == '__main__':
    problem = define_problem()
    run_search(problem, my_search_algorithms)
