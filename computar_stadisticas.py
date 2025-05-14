import re
import statistics
from collections import defaultdict

# Ruta del archivo de log
log_path = "logs/hanoi_solver.log"

# Expresiones regulares
algorithm_pattern = re.compile(r"Running search algorithm: ([\w_]+)")
time_pattern = re.compile(r"Execution time: ([\d.]+) seconds")
memory_pattern = re.compile(r"Peak memory usage: ([\d.]+) KB")
moves_pattern = re.compile(r"Cantidad de nodos movimientos: (\d+)")
optimal_pattern = re.compile(r"Solicion optima es .* = (\d+)")

# Estructura: { (algoritmo, heuristica): { 'times': [], 'memory': [], 'moves': [], 'optimal': [], 'is_optimal': [] } }
data = defaultdict(lambda: {'times': [], 'memory': [],
                   'moves': [], 'optimal': [], 'is_optimal': []})

current_algorithm = None
heuristic_counter = defaultdict(int)

with open(log_path, 'r', encoding='utf-8') as file:
    for line in file:
        if match := algorithm_pattern.search(line):
            current_algorithm = match.group(1)
            heuristic_counter[current_algorithm] += 1
            heuristic_id = heuristic_counter[current_algorithm]
            current_key = (current_algorithm, f"H{(heuristic_id - 1) % 2 + 1}")
        elif match := time_pattern.search(line):
            data[current_key]['times'].append(float(match.group(1)))
        elif match := memory_pattern.search(line):
            data[current_key]['memory'].append(float(match.group(1)))
        elif match := moves_pattern.search(line):
            data[current_key]['moves'].append(int(match.group(1)))
        elif match := optimal_pattern.search(line):
            opt = int(match.group(1))
            data[current_key]['optimal'].append(opt)
            # Verificamos si fue óptima comparando con el último valor de 'moves'
            if data[current_key]['moves']:
                last_move = data[current_key]['moves'][-1]
                data[current_key]['is_optimal'].append(last_move == opt)

# Función para media y desviación estándar


def mean_std(values):
    return round(statistics.mean(values), 6), round(statistics.stdev(values), 6) if len(values) > 1 else (round(values[0], 6), 0.0)


# Mostrar resultados por algoritmo y heurística
print("== RESULTADOS POR ALGORITMO Y HEURÍSTICA ==")
for (alg, heur), values in sorted(data.items()):
    if not values['times']:
        continue
    exec_mean, exec_std = mean_std(values['times'])
    mem_mean, mem_std = mean_std(values['memory'])
    diffs = [m - o for m, o in zip(values['moves'], values['optimal'])]
    diff_mean, diff_std = mean_std(diffs)
    opt_count = sum(values['is_optimal'])
    total = len(values['is_optimal'])
    opt_ratio = round(100 * opt_count / total, 2) if total > 0 else 0.0

    print(f"\n--- {alg} con {heur} ---")
    print(f"  → Runs: {total}")
    print(f"  → Tiempo promedio: {exec_mean}s ± {exec_std}")
    print(f"  → Memoria promedio: {mem_mean}KB ± {mem_std}")
    print(f"  → Diferencia con óptimo: {diff_mean} movimientos ± {diff_std}")
    print(f"  → Soluciones óptimas: {opt_count}/{total} ({opt_ratio}%)")
