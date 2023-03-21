import copy

def ac3(csp, arcs_queue=None, current_domains=None, assignment=None):
    if arcs_queue is None:
        arcs_queue = set()
        for i in csp.variables:
            for j in csp.adjacency[i]:
                arcs_queue.add((i, j))
    arcs_queue = set(arcs_queue)
    if current_domains is None:
        current_domains = copy.deepcopy(csp.domains)
    while len(arcs_queue) != 0:
        (i, j) = arcs_queue.pop()
        if revise(csp, current_domains, i, j):
            if len(current_domains[i]) == 0:
                return False, current_domains
            for k in (csp.adjacency[i]):
                if k != j:
                    if(assignment is not None and k not in assignment):
                        arcs_queue.add((k, i))
    return True, current_domains

def revise(csp, current_domains, i, j):
    revised = False
    for x in current_domains[i]:
        conflict = 0
        for y in current_domains[j]:
            if not csp.constraint_consistent(i, x, j, y):
                conflict += 1
        if conflict == len(current_domains[j]):
            current_domains[i].remove(x)
            revised = True
    return revised

'''
    Backtracking search
'''
def backtracking(csp):
    return backtracking_helper(csp, assignment={}, current_domains=copy.deepcopy(csp.domains))

def backtracking_helper(csp, assignment ={}, current_domains=None):
    if csp.is_goal(assignment):
        return assignment
    var = select_unassigned_variable(csp, current_domains, assignment)
    for value in order_domain_values(csp, var, current_domains):
        if csp.check_partial_assignment(assignment):
            assignment[var] = value
            current_domains[var] = [value]
            arcs_queue = {(i, var) for i in csp.adjacency[var] if i not in assignment}
            is_consistent, updated_domains = ac3(csp, arcs_queue, copy.deepcopy(current_domains), assignment)
            if is_consistent:
                result = backtracking_helper(csp, copy.deepcopy(assignment), copy.deepcopy(updated_domains))
                if result is not None:
                    return result
            del assignment[var]
    return None

'''
    Selects the next unassigned variable
'''
def select_unassigned_variable(csp, current_domains, assignment):
    vars = {}
    for var in csp.variables:
        if var not in assignment:
            vars[var] = len(current_domains[var])

    minimumLen = vars[min(vars, key=vars.get)]
    minimumVars = [i for i in vars if vars[i] == minimumLen]

    if len(minimumVars) == 1:
        return min(minimumVars)
    
    return min(minimumVars, key=lambda x: len([i for i in csp.adjacency[x] if i not in assignment]))
        
'''
    Orders the domain values of a variable
'''
def order_domain_values(csp, var, current_domains):
    order = {}
    for value in current_domains[var]:
        order[value] = 0
        for neighbor in csp.adjacency[var]:
            for value2 in current_domains[neighbor]:
                if not csp.constraint_consistent(var, value, neighbor, value2):
                    order[value] += 1
    return sorted(order, key=order.get)