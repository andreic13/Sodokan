from sokoban import Map
import numpy as np

def simulated_annealing(initial: Map, t_init: float, t_final: float,
    cooling: float, max_iters: int, seed: int, heuristic: callable):
    # seed pentry reproducibilitate
    if seed is not None:
        np.random.seed(seed)
        print(f"SA: Using seed {seed}")
    
    #iteratii maxime la stagnare
    stagnation_threshold = 4800

    state = initial.copy()
    cost = heuristic(state)
    best_state = state
    best_cost = cost
    t = t_init
    iters, built_states = 0, 0
    iters_since_last_update = 0
    
    while t > t_final and iters < max_iters:
        iters += 1
        iters_since_last_update += 1
        if best_state.is_solved():
            # am ajuns la solutie
            break

        # iau mutari posibile
        possible_moves = state.filter_possible_moves()
        
        if not possible_moves:
            # nu mai am mutari posibile
            t = t * cooling

            if iters_since_last_update >= stagnation_threshold:
                # reincep de la cea mai buna stare
                state = best_state.copy()
                cost = best_cost
                iters_since_last_update = 0
            continue # trec la urmatoarea iteratie

        # iau o mutare random si evaluez vecinul corespunzator
        random_move = np.random.choice(possible_moves)
        neighbor = state.copy()
        neighbor.apply_move(random_move)
        built_states += 1

        neigh_cost = heuristic(neighbor)
        delta_e = cost - neigh_cost

        # decid daca accept mutarea
        accept = False
        if delta_e > 0:
            accept = True
        else:
            if t > 1e-9:
                prob = np.exp(delta_e / t)
                if np.random.rand() < prob:
                    accept = True

        if accept:
            state = neighbor
            cost = neigh_cost

            # am gasit o stare mai buna
            if cost < best_cost:
                best_state = state
                best_cost = cost
                iters_since_last_update = 0

        # verific daca am stagnat
        if iters_since_last_update >= stagnation_threshold:
            # reincep de la cea mai buna stare
            state = best_state.copy()
            cost = best_cost
            iters_since_last_update = 0

        t = t * cooling
    
    return best_state.is_solved(), iters, built_states, best_state