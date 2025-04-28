import os
import time
from sokoban import Map
from search_methods.lrta_star import LRTA_star
from search_methods.simulated_annealing import simulated_annealing

class Solver:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.results = []

    def run_algo(self, algo_name: str, map_name: str, algo_params: dict):
        map_path = os.path.join(self.input_dir, f"{map_name}.yaml")
        print(f"\n=== Algo {algo_name} on {map_name} ===")

        initial_map = Map.from_yaml(map_path)
        map_to_test = initial_map.copy()
        final_map = map_to_test
        solved = False
        iters = 0
        states = 0
        exec_time = 0.0
        pull_moves = -1


        # retin timpul initial
        start_time = time.time()

        if algo_name.lower() == 'lrta*':
            solved, iters, states, final_map = LRTA_star(map_to_test, **algo_params)
        elif algo_name.lower() == 'sa':
            solved, iters, states, final_map = simulated_annealing(map_to_test, **algo_params)
        else:
            return None

        # cat a durat algoritmul
        exec_time = time.time() - start_time

        if solved:
            pull_moves = final_map.undo_moves

        result_data = {
            'algorithm': algo_name,
            'map': map_name,
            'solved': solved,
            'iterations': iters,
            'built_states': states,
            'execution_time': exec_time,
            'pull_moves': pull_moves
        }

        print(f"Solved? {solved}, Time={exec_time:.3f}s, Iterations={iters}, Explored states={states}, Pulls={pull_moves if solved else 'N/A'}")
        print("===================")

        return result_data

    def run_all(self, map_names: list[str], algorithms: list[str],
                        sa_params: dict = {}, lrta_params: dict = {}):
        self.results = []  # clear rezultate anterioare
        all_params = {'sa': sa_params, 'lrta*': lrta_params}

        for map_name in map_names:
            for algo in algorithms:
                params = all_params.get(algo.lower(), {})
                result = self.run_algo(algo, map_name, params)
                if result:
                    self.results.append(result)

        print("\n===========END OF TESTS===========")
        return self.results