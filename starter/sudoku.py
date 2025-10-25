#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys

ROW = "ABCDEFGHI"
COL = "123456789"

#efficient lookups
ROW_INDEX = {ROW[i]: i for i in range(9)}
COL_INDEX = {COL[i]: i for i in range(9)}

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def build_neighbors():
    variable_positions = [r + c for r in ROW for c in COL]

    neighbors = {}
    for pos in variable_positions:
        r, c = pos[0], pos[1]
        row_neighbors = {r + col for col in COL if col != c}
        col_neighbors = {row + c for row in ROW if row != r}
        
        box_row_start = (ROW_INDEX[r] // 3) * 3
        box_col_start = (COL_INDEX[c] // 3) * 3 
        box_rows = ROW[box_row_start:box_row_start + 3]
        box_cols = COL[box_col_start:box_col_start + 3] 
        box_neighbors = {br + bc for br in box_rows for bc in box_cols if (br + bc) != pos}
        neighbors[pos] = row_neighbors | col_neighbors | box_neighbors
    return neighbors

NEIGHBORS = build_neighbors()
VARIABLE_POSITIONS = [r + c for r in ROW for c in COL]

def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    
    # I'll be using a Minimum Remaining Value heuristic and forward checking
    
    neighbors = NEIGHBORS
    
    #initialize the domains
    domains = {} 
    for pos in VARIABLE_POSITIONS:
        if board[pos] != 0:
            domains[pos] = set([board[pos]])
        else:
            used_values = set()
            for neighbor in neighbors[pos]:
                if board[neighbor] != 0:
                    used_values.add(board[neighbor])
            domains[pos] = set(range(1, 10)) - used_values

    for pos in VARIABLE_POSITIONS:
        if len(domains[pos]) == 0:
            return board 
        
    def completed_board(domains):
        for var in VARIABLE_POSITIONS:
            if len(domains[var]) != 1:
                return False
        return True
    
    # MRV and forward checking 
    def next_variable(domains):
        unassigned_vars = [var for var in VARIABLE_POSITIONS if len(domains[var]) > 1]
        if not unassigned_vars:
            return None
        return min(unassigned_vars, key=lambda var: len(domains[var]))

    
    def is_valid_assignment(domains):
        for pos in VARIABLE_POSITIONS:
            if len(domains[pos]) == 1:
                val = next(iter(domains[pos]))
                for n in neighbors[pos]:
                    if len(domains[n]) == 1 and next(iter(domains[n])) == val:
                        return False
        return True


    def order_values(var, domains):
        return sorted(
            domains[var],
            key=lambda v: sum(v in domains[n] for n in neighbors[var])
        )

    
    def search(domains):
        if completed_board(domains) and is_valid_assignment(domains):
            return domains
        
        var = next_variable(domains)
        if var is None:
            return None
        
        for value in order_values(var, domains):
            removed = []
            original_domain = domains[var]
            domains[var] = {value}

            consistent = True
            for neighbor in neighbors[var]:
                if value in domains[neighbor]:
                    domains[neighbor].remove(value)
                    removed.append(neighbor)
                    if len(domains[neighbor]) == 0:
                        consistent = False
                        break

            if consistent:
                result = search(domains)
                if result is not None:
                    return result

            for n in removed:
                domains[n].add(value)
            domains[var] = original_domain
        
        return None
    

    def get_singleton(s):
        return next(iter(s))

    sol = search(domains)
    if sol is not None:
        for var in VARIABLE_POSITIONS:
            board[var] = get_singleton(sol[var])
    
    
    solved_board = board
    return solved_board


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv[1]) < 9:
            print("Input string too short")
            exit()

        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        solved_board = backtracking(board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')
    else:
        print("Usage: python3 sudoku.py <input string>")
    
    print("Finishing all boards in file.")