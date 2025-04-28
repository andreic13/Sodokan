import math

# numarul de cutii care nu sunt pe final
def misplaced_heuristic(map_state):
    total_cost = 0
    final_positions = map_state.targets
    box_positions = []
    for box in map_state.boxes.values():
        box_positions.append((box.x, box.y))
    
    # am vreo lista nula?
    if not box_positions:
        return 0 # = solutie
    if not final_positions:
        return math.inf # nu am unde sa pun cutiile
    
    boxes_misplaced = 0
    for box in box_positions:
        if box not in final_positions:
            boxes_misplaced += 1
    total_cost += boxes_misplaced

    return total_cost

def manhattan_distance(obj1, obj2):
    return abs(obj1[0] - obj2[0]) + abs(obj1[1] - obj2[1])

# suma distantelor de la cutii la cel mai apropiat final:
def manhattan_heuristic_var1(map_state):
    total_cost = 0
    final_positions = map_state.targets
    box_positions = []
    for box in map_state.boxes.values():
        box_positions.append((box.x, box.y))
    
    # am vreo lista nula?
    if not box_positions:
        return 0 # = solutie
    if not final_positions:
        return math.inf # nu am unde sa pun cutiile
    
    # pentru fiecare cutie, aleg cel mai apropiat final
    for box in box_positions:
        # daca cutia e deja pe final, nu mai adun nimic
        if box in final_positions:
            continue

        min_dist = math.inf
        for final in final_positions:
            dist = manhattan_distance(box, final)
            if dist < min_dist:
                min_dist = dist
        # adun distanta minima doar daca cutia nu e pe final
        if min_dist != math.inf:
            total_cost += min_dist
        else:
            return math.inf # distanta la final e infinita
        
    return total_cost

# suma distantelor de la cutii la cel mai apropiat final
# + distanta de la player la cea mai apropiata cutie
def manhattan_heuristic_var2(map_state):
    total_cost = 0
    final_positions = map_state.targets
    box_positions = []
    for box in map_state.boxes.values():
        box_positions.append((box.x, box.y))
    
    # am vreo lista nula?
    if not box_positions:
        return 0 # = solutie
    if not final_positions:
        return math.inf # nu am unde sa pun cutiile
    
    # pentru fiecare cutie, aleg cel mai apropiat final
    for box in box_positions:
        # daca cutia e deja pe final, nu mai adun nimic
        if box in final_positions:
            continue

        min_dist = math.inf
        for final in final_positions:
            dist = manhattan_distance(box, final)
            if dist < min_dist:
                min_dist = dist
        # adun distanta minima doar daca cutia nu e pe final
        if min_dist != math.inf:
            total_cost += min_dist
        else:
            return math.inf # distanta la final e infinita
    
    min_dist_player = math.inf
    player_position = (map_state.player.x, map_state.player.y)
    for box in box_positions:
        # caut cea mai apropiata cutie si pastrez distanta
        if box in final_positions:
            # daca cutia e deja pe final, nu vreau sa ajung la ea
            continue
        dist = manhattan_distance(player_position, box)
        if dist < min_dist_player:
            min_dist_player = dist
    if min_dist_player != math.inf:
        # adun distanta minima in mod ponderat
        total_cost += min_dist_player / 10
    
    return total_cost

# suma distantelor de la cutii la cel mai apropiat final liber
# + distanta de la player la cea mai apropiata cutie
# + penalizare infinita pentru cutiile care ajung intr-un colt al hartii
def manhattan_heuristic(map_state):
    total_cost = 0
    final_positions = map_state.targets
    box_positions = []
    for box in map_state.boxes.values():
        box_positions.append((box.x, box.y))
    
    # am vreo lista nula?
    if not box_positions:
        return 0 # = solutie
    if not final_positions:
        return math.inf # nu am unde sa pun cutiile
    
    # pentru fiecare cutie, aleg cel mai apropiat final
    for box in box_positions:
        # daca cutia e deja pe final, nu mai adun nimic
        if box in final_positions:
            continue

        min_dist = math.inf
        for final in final_positions:
            dist = manhattan_distance(box, final)
            if dist < min_dist:
                min_dist = dist
        # adun distanta minima doar daca cutia nu e pe final
        if min_dist != math.inf:
            total_cost += min_dist
        else:
            return math.inf # distanta la final e infinita
    
    min_dist_player = math.inf
    player_position = (map_state.player.x, map_state.player.y)
    for box in box_positions:
        # caut cea mai apropiata cutie si pastrez distanta
        if box in final_positions:
            # daca cutia e deja pe final, nu vreau sa ajung la ea
            continue
        dist = manhattan_distance(player_position, box)
        if dist < min_dist_player:
            min_dist_player = dist
    if min_dist_player != math.inf:
        # adun distanta minima in mod ponderat
        total_cost += min_dist_player / 10

    map_x = map_state.length
    map_y = map_state.width

    for box_pos in box_positions:
        if box_pos in final_positions:
            # poate avem final intr-un colt,
            # nu vreau sa fac starea inaccesibila
            continue

        box_x, box_y = box_pos

        # unde am blocaj
        up_blck = False
        down_blck = False
        left_blck = False
        right_blck = False

        if (box_x == map_x - 1):
            up_blck = True
        if (box_x == 0):
            down_blck = True
        if (box_y == 0):
            left_blck = True
        if (box_y == map_y - 1):
            right_blck = True

        # daca am sus/jos si stanga/dreapta = colt
        if (up_blck or down_blck) and (left_blck or right_blck):
            return math.inf

    return total_cost

# numarul de cutii care nu sunt pe final
# + distanta de la player la cea mai apropiata cutie
# + penalizare infinita pentru cutiile care ajung intr-un colt al hartii
def manhattan_heuristic_var4_with_misplaced(map_state):
    total_cost = 0
    final_positions = map_state.targets
    box_positions = []
    for box in map_state.boxes.values():
        box_positions.append((box.x, box.y))
    
    # am vreo lista nula?
    if not box_positions:
        return 0 # = solutie
    if not final_positions:
        return math.inf # nu am unde sa pun cutiile
    
    boxes_misplaced = 0
    for box in box_positions:
        if box not in final_positions:
            boxes_misplaced += 1
    total_cost += boxes_misplaced
    
    min_dist_player = math.inf
    player_position = (map_state.player.x, map_state.player.y)
    for box in box_positions:
        # caut cea mai apropiata cutie si pastrez distanta
        if box in final_positions:
            # daca cutia e deja pe final, nu vreau sa ajung la ea
            continue
        dist = manhattan_distance(player_position, box)
        if dist < min_dist_player:
            min_dist_player = dist
    if min_dist_player != math.inf:
        # adun distanta minima in mod ponderat
        total_cost += min_dist_player / 10

    map_x = map_state.length
    map_y = map_state.width

    for box_pos in box_positions:
        if box_pos in final_positions:
            # poate avem final intr-un colt,
            # nu vreau sa fac starea inaccesibila
            continue

        box_x, box_y = box_pos

        # unde am blocaj
        up_blck = False
        down_blck = False
        left_blck = False
        right_blck = False

        if (box_x == map_x - 1):
            up_blck = True
        if (box_x == 0):
            down_blck = True
        if (box_y == 0):
            left_blck = True
        if (box_y == map_y - 1):
            right_blck = True

        # daca am sus/jos si stanga/dreapta = colt
        if (up_blck or down_blck) and (left_blck or right_blck):
            return math.inf

    return total_cost