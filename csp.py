import copy
import matplotlib.pyplot as plt 
import seaborn as sns

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
    fixed_domains = copy.deepcopy(current_domains)
    revised = False
    for x in fixed_domains[i]:
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

'''
'''
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

class SudokuCSP:
    def __init__(self, partial_assignment={}):
        self.variables = [(i, j) for i in range(1, 10) for j in range(1, 10)]
        self.domains = {variable:[i for i in range(1, 10)] if variable not in partial_assignment else [partial_assignment[variable]] for variable in self.variables}
        self.adjacency = {variable:[] for variable in self.variables}
        
        for variable in self.variables:
            for i in range(1, 10):
                if i != variable[0]:
                    self.adjacency[variable].append((i, variable[1]))
        for variable in self.variables:
            for i in range(1, 10):
                if i != variable[1]:
                    self.adjacency[variable].append((variable[0], i))
        for variable in self.variables:
            for i in range(1, 10):
                for j in range(1, 10):
                    if ((i != variable[0]) and (j != variable[1])):
                        if (i - 1) // 3 == (variable[0] - 1) // 3 and (j - 1) // 3 == (variable[1] - 1) // 3:
                            self.adjacency[variable].append((i, j))
                        
                         
    def constraint_consistent(self, var1, val1, var2, val2):
        if (var2 in self.adjacency[var1]):
            return (val1 != val2)
        return True
    
    def check_partial_assignment(self, assignment):
        if assignment is None:
            return False
        for var1, val1 in assignment.items():
            for var2, val2 in assignment.items():
                if (var1 != var2) and not (self.constraint_consistent(var1, val1, var2, val2)):
                    return False
        return True
    
    def is_goal(self, assignment):
        if assignment is None:
            return False
        if len(assignment) == len(self.variables):
            return self.check_partial_assignment(assignment)
        return False
    
'''
    Visualize the sudoku board
'''

def visualize_sudoku_solution(assignment_solution, file_name):
    sudoku_board = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            sudoku_board[i][j] = assignment_solution[(i+1, j+1)]
    plt.figure(figsize=(9, 9))
    ax = sns.heatmap(sudoku_board, annot=True, linewidths=1.5, linecolor='k', cbar=False)
    ax.invert_yaxis()
    plt.savefig(file_name)
    plt.close()

