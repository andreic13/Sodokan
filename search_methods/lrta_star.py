from sokoban import Map

import math

def LRTA_star(initial: Map, max_steps: int, h: str):
    H = {}
    Rezultat = {}
    sprev = None
    aprev = None

    if initial.is_solved():
        return True, 0, 0, initial

    state = initial.copy()

    steps = 0
    built_states = 0

    while steps < max_steps:
        # daca s este stare finala
        if state.is_solved():
            break

        state_repr = str(state)
        steps += 1
        
        # daca s este stare noua atunci H[s] ←− h(s)
        if state_repr not in H:
            H[state_repr] = h(state)
        
        # daca sprev ̸= ⊥
        if sprev is not None:
            # Rezultat[sprev , aprev] ←− s
            sprev_repr = str(sprev)
            Rezultat[(sprev_repr, aprev)] = state

            # scot min b din actiuni(sprev)
            min_b = math.inf

            # H[sprev]
            for b in sprev.filter_possible_moves():
                next_state = sprev.copy()
                next_state.apply_move(b)
                built_states += 1
                next_state_repr = str(next_state)

                if next_state_repr in H:
                    cost = 1 + H[next_state_repr]
                else:
                    cost = h(next_state)

                if cost < min_b:
                    min_b = cost
            
            H[sprev_repr] = min_b

        # sprev ←− s
        sprev = state.copy()

        # intoarce cea mai buna actiune/b din actiuni(s)
        min_b = math.inf
        best_action = None
        best_next_state = None
        for b in state.filter_possible_moves():
            next_state = state.copy()
            next_state.apply_move(b)
            built_states += 1
            next_state_repr = str(next_state)

            if next_state_repr in H:
                cost = 1 + H[next_state_repr]
            else:
                cost = h(next_state)

            if cost < min_b:
                min_b = cost
                best_action = b
                best_next_state = next_state

        # update state si aprev pentru urmatoarea iteratie
        state = best_next_state
        aprev = best_action

    return state.is_solved(), steps, built_states, state
