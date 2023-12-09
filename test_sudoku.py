if __name__ == "__main__":    
    from csp import *
    
    # tests 1: sudoku constructor implementation
    # partial assignment ordered as (row, col):value and a full 9x9 matrix
    # partial_assignment = {(9,1):3, (9,2):5, (9,3):8, (9,4):9, (9,5):2, (9,6):1, (9,7):6, (9,8):4, (9,9):7,
    #                       (8,1):4, (8,2):6, (8,3):7, (8,4):3, (8,5):5, (8,6):8, (8,7):2, (8,8):1, (8,9):9,
    #                       (7,1):9, (7,2):1, (7,3):2, (7,4):6, (7,5):4, (7,6):7, (7,7):8, (7,8):5, (7,9):3,
    #                       (6,1):8, (6,2):3, (6,3):4, (6,4):5, (6,5):9, (6,6):2, (6,7):1, (6,8):7, (6,9):6,
    #                       (5,1):2, (5,2):7, (5,3):1, (5,4):8, (5,5):3, (5,6):6, (5,7):9, (5,8):4, (5,9):5,
    #                       (4,1):5, (4,2):9, (4,3):6, (4,4):7, (4,5):1, (4,6):4, (4,7):3, (4,8):2, (4,9):8,
    #                       (3,1):7, (3,2):4, (3,3):3, (3,4):2, (3,5):8, (3,6):5, (3,7):6, (3,8):9, (3,9):1,
    #                       (2,1):6, (2,2):2, (2,3):9, (2,4):1, (2,5):7, (2,6):3, (2,7):4, (2,8):8, (2,9):5,
    #                       (1,1):1, (1,2):8, (1,3):5, (1,4):4, (1,5):6, (1,6):9, (1,7):7, (1,8):3, (1,9):2}
    
    # partial assignment ordered as (row, col):value 
    partial_assignment = {(9,1):5, (9,7):6,
                          (8,1):9, (8,4):5, (8,5):4, (8,7):8, 
                          (7,1):8, (7,6):1, (7,7):3, (7,8):7, 
                          (6,5):8, (6,6):9,
                          (5,4):7, (5,5):5, 
                          (4,4):3, (4,8):8, (4,9):2,
                          (3,1):1, (3,2):4, (3,4):8, (3,9):6,
                          (2,1):6, (2,2):7, (2,5):2, (2,8):1, (2,9):8,
                          (1,6):5, (1,7):4, }

    sudoku = SudokuCSP(partial_assignment)
    
    print(len(sudoku.variables))
    print('_______________________________________________________________________')
    print(sudoku.variables) 
    print('_______________________________________________________________________')
    print(sudoku.domains[(1,1)]) 
    print('_______________________________________________________________________')
    print(sudoku.domains[(5,7)]) 
    print('_______________________________________________________________________')
    print(sudoku.domains[(7,3)]) 
    print('_______________________________________________________________________')
    print(sudoku.adjacency[(1,1)]) 
    print('_______________________________________________________________________')
    print(sudoku.adjacency[(6,2)]) 
    print('_______________________________________________________________________')
    print(sudoku.adjacency[(3,9)]) 
    print('_______________________________________________________________________')
    
    # tests 2: run backtracking search on soduku
    import time
    start_time = time.time()
    sol_assignment = backtracking(sudoku)
    end_time = time.time()
    is_complete_and_consistent = sudoku.is_goal(sol_assignment)
    print('Sol: {}'.format(sol_assignment))
    print('Is sol complete and consistent: {}'.format(is_complete_and_consistent))
    print('Time taken: {} sec'.format(end_time - start_time))
    print('_______________________________________________________________________')

    visualize_sudoku_solution(sol_assignment, 'sudoku_sol.png')