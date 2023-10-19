from itertools import permutations

def is_valid_state(state):
    pizzeria_ce, pizzeria_ds, bike, pub_ce, pub_ds = state
    return (pizzeria_ds == 0 or pizzeria_ds >= pizzeria_ce) and (pub_ds == 0 or pub_ds >= pub_ce)

def move_people(state, action):
    pizzeria_ce, pizzeria_ds, bike, pub_ce, pub_ds = state
    ce, ds = action
    new_pizzeria_ce = pizzeria_ce - ce
    new_pizzeria_ds = pizzeria_ds - ds
    new_bike = bike - ce - ds
    new_pub_ce = pub_ce + ce
    new_pub_ds = pub_ds + ds
    return (new_pizzeria_ce, new_pizzeria_ds, new_bike, new_pub_ce, new_pub_ds)

def find_solution(initial_state, max_bike_seats, max_iter =100):
    visited_states = set()
    stack = [(initial_state, [])]
    it = 0

    while stack and it <= max_iter:
        it += 1
        print(it)
        current_state, actions = stack.pop()

        # Verification of the objective (no ds or ce in pizzeria or on the bike (all in pub))
        if current_state[2] == 0:
            if current_state[0] == 0 and current_state[1] == 0:
                return actions  

        visited_states.add(current_state)

        ce, ds = current_state[0], current_state[1]

        list_seats = range(max_bike_seats + 1)

        for ce_perm in list_seats :
            for ds_perm in list_seats: 
            #it will iterate through the following pairs: for 2 bike seats we will have  ce_perm is 1, and ds_perm is 2. ce_perm is 1, and ds_perm is 0. ce_perm is 2, and ds_perm is 1. ce_perm is 2, and ds_perm is 0. ce_perm is 0, and ds_perm is 1. ce_perm is 0, and ds_perm is 2.

                if ce >= ce_perm and ds >= ds_perm:  # We verify we have enough students to satisfy the move
                    new_action = (ce_perm, ds_perm)
                    new_state = move_people(current_state, new_action)

                    if new_state not in visited_states and new_state[2] <= max_bike_seats and is_valid_state(new_state):
                        stack.append((new_state, actions + [new_action]))

    return None

# Example usage
initial_state = (3, 4, 0, 0, 0)  # (CE at pizzeria, DS at pizzeria, Bike seats, CE at pub, DS at pub)
max_bike_seats = 2
solution = find_solution(initial_state, max_bike_seats)

if solution:
    print("Solution found:")
    for action in solution:
        ce, ds = action
        print(f"Move {ce} CE and {ds} DS")

else:
    print("No solution found.")