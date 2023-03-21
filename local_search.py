import numpy as np

def tour_cost(state, adj_matrix):
    cost = 0
    for i in range(1, len(state)):
        cost += adj_matrix[state[i-1]][state[i]]
    return cost

def random_swap(state):
    idx1, idx2 = np.random.choice(len(state), size=2, replace=False)
    copyState = [i for i in state]
    copyState[idx1], copyState[idx2] = copyState[idx2], copyState[idx1]
    return copyState

def simulated_annealing(initial_state, adj_matrix, initial_T = 1000):
    current_state = initial_state
    T = initial_T
    iters = 0
    T *= 0.99
    while T >= 1e-14:
        T *= 0.99
        next_state = random_swap(current_state)
        delta = tour_cost(current_state, adj_matrix) - tour_cost(next_state, adj_matrix)
        if delta > 0:
            current_state = next_state
        elif delta <= 0:
            if np.random.rand() < np.exp(delta/T):
                current_state = next_state
        iters += 1

    return current_state, iters
    
