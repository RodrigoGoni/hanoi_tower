# 🧠 Hanoi Tower - AI Solution

Este proyecto implementa una solución basada en inteligencia artificial para resolver el clásico juego de la **Torre de Hanoi**. Ideal para estudios de algoritmos, visualización de soluciones y prácticas de programación con Python.

---

## 🚀 Instalación

Sigue estos pasos para clonar el repositorio, crear un entorno virtual y ejecutar el proyecto.

### 1. Clonar el repositorio

git clone https://github.com/RodrigoGoni/hanoi_tower.git
cd hanoi_tower 

### 2. Crear y activar un entorno virtual

#### En Linux / macOS:
python3 -m venv hanoi
source hanoi/bin/activate
#### En Windows (PowerShell):
python -m venv hanoi
hanoi\Scripts\activate

### 3. Instalar las dependencias

pip install -r requirements.txt

## ▶️ Ejecución del proyecto

python main.py

# Trabajo Práctico: Torre de Hanoi - Inteligencia Artificial

## Autores
Tomas Corteggiano,
Rodrigo Iván Goñi

## Descripción
Este trabajo práctico consiste en el análisis e implementación de algoritmos de búsqueda aplicados al problema clásico de la Torre de Hanoi. Se utiliza un entorno simulado y estructuras de datos específicas para representar el problema, junto con diferentes variantes del algoritmo A* y funciones heurísticas.

---

## PEAS del problema

- **Performance**: Número de movimientos (idealmente el óptimo, que es igual a `2^n − 1`), memoria del programa utilizado y tiempo de ejecución.
- **Environment**: Discos y postes del juego, y la forma en que estos se ordenan. El entorno es determinista y estático.
- **Actuators**: El algoritmo desarrollado mediante la clase `ActionHanoi`.
- **Sensors**: Las estructuras de datos que definen el problema, es decir, las clases `ProblemHanoi` y `StatesHanoi`.

---

## Propiedades del entorno de trabajo

El entorno de la Torre de Hanoi presenta las siguientes características:
- Completamente observable
- Determinista
- Secuencial
- Estático
- Discreto
- De agente único

---

## Definiciones en el contexto del problema

- **Estado**: Una configuración específica de los discos en los postes.
- **Espacio de estados**: Todas las posibles configuraciones válidas de los discos en los postes.
- **Árbol de búsqueda**: Una representación de la exploración de los estados posibles mediante la aplicación de las acciones.
- **Nodo de búsqueda**: Un estado dentro del árbol de búsqueda, que además contiene información sobre la secuencia de acciones que llevaron a él.
- **Objetivo**: La configuración final deseada de los discos en los postes.
- **Acción**: Mover el disco superior de un poste a otro, respetando las reglas del juego (un disco más grande nunca puede estar encima de uno más pequeño).
- **Frontera**: El conjunto de estados que han sido generados durante la búsqueda pero que aún no han sido explorados.

---

## Algoritmos implementados

Se implementaron las siguientes variantes del algoritmo A*:

- `a_star` con heurística H1
- `a_star` con heurística H2
- `basic_a_star` con heurística H1
- `basic_a_star` con heurística H2

---

## Complejidad teórica del algoritmo A*

- **Complejidad temporal**: En el peor de los casos, `O(b^d)`, donde:
  - `b`: Factor de ramificación (3, por los tres postes)
  - `d`: Profundidad de la solución óptima
- **Complejidad espacial (memoria)**: También `O(b^d)`
- **Tiempo de ejecución en el peor caso**: Exponencial en el número de discos, `O(b * 2^n − 1)`

---

## Resultados experimentales

| Algoritmo          | Runs | Tiempo promedio (s) | Memoria promedio (KB) | Diferencia con óptimo | Soluciones óptimas |
|--------------------|------|----------------------|------------------------|------------------------|---------------------|
| a_star con H1      | 20   | 0.033042 ± 0.003577  | 194.73 ± 0.0           | 0 movimientos ± 0.0    | 20/20 (100.0%)      |
| a_star con H2      | 20   | 0.035064 ± 0.004473  | 199.96 ± 0.0           | 0 movimientos ± 0.0    | 20/20 (100.0%)      |
| basic_a_star con H1| 20   | 0.034124 ± 0.002955  | 220.37 ± 0.0           | 0 movimientos ± 0.0    | 20/20 (100.0%)      |
| basic_a_star con H2| 20   | 0.033283 ± 0.003181  | 202.1 ± 0.0            | 0 movimientos ± 0.0    | 20/20 (100.0%)      |

---

## Evaluación de la calidad de la solución

En todos los casos, los algoritmos implementados encontraron la **solución óptima** de `2^k − 1` movimientos, siendo `k` el número de discos. Esto se validó en 20 ejecuciones por algoritmo y heurística.

## Implementacion en Rust: Experimental

A modo de experimentacion se desarrollo el codigo en Rust. El mismo sigue las estructuras de datos del codigo de ejemplo en python y se aplica en este caso en particular solo el algoritmo A* a modo de ejemplo. Se dispone del codigo fuente, o bien el ejecutable compilado. 

---

## Entregables

- Código fuente del proyecto
- Archivo `README.md` con documentación teórica
- Archivos `.json` para el simulador son simulator/initial_state.json, simulator/goal_state.json, simulator/sequencea_star.json, simulator/queue_basic_a_star.json, se generan desdpues de cada ejecucion. ademas agregue un parametro --sequence para pasarle la ruta al archvio
---

## Consideraciones

- Se puede utilizar el código base del repositorio `hanoi_tower`.

