"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None
      

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count number of X and number of O
    count_X = 0
    count_O = 0
    for row in board:
        for cell in row:
            if cell == "X":
                count_X += 1
            elif cell == "O":
                count_O += 1
            else:
                continue
    
    # If number of X > number of O => return O
    if count_X > count_O:
        return "O"
    else: # If number of X == number of O => return X
        return "X"
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    for row_idx in range(len(board)):
        for col_idx in range(len(board[row_idx])):
            if (board[row_idx][col_idx] is None):
                action = (row_idx, col_idx)
                action_set.add(action)
                
    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    ROW = 0
    COL = 1
    
    # Check if the action is valid on the board
    if board[action[ROW]][action[COL]] != EMPTY: # Is cell occupied?
        raise Exception(f"This action is illegal: cell ({action[ROW]},{action[COL]}) has been occupied")
    
    if (action[ROW] < 0) or (action[ROW] > 2) or (action[COL] < 0) or (action[COL] > 2): # Is the cell in action inside the board?
        raise Exception(f"This action is illegal: cell ({action[ROW]},{action[COL]}) is outside the board")
    
    # Decide which player is going to play based on the current board state
    player_sign = player(board)
    
    # Create a deep copy of the old board
    result_board = copy.deepcopy(board)
    
    # Update the cell state on the result board based on the action and the player
    result_board[action[ROW]][action[COL]] = player_sign
    
    # Return result board  
    return result_board


def winner(board): # or None
    """
    Returns the winner of the game, if there is one.
    """
    # Conditions for X to win, return "X"
    if     ((board[0][0]=="X") and (board[0][1]=="X") and (board[0][2]=="X")) \
        or ((board[1][0]=="X") and (board[1][1]=="X") and (board[1][2]=="X")) \
        or ((board[2][0]=="X") and (board[2][1]=="X") and (board[2][2]=="X")) \
        or ((board[0][0]=="X") and (board[1][0]=="X") and (board[2][0]=="X")) \
        or ((board[0][1]=="X") and (board[1][1]=="X") and (board[2][1]=="X")) \
        or ((board[0][2]=="X") and (board[1][2]=="X") and (board[2][2]=="X")) \
        or ((board[0][0]=="X") and (board[1][1]=="X") and (board[2][2]=="X")) \
        or ((board[0][2]=="X") and (board[1][1]=="X") and (board[2][0]=="X")):
        return "X"
    
    # Conditions for O to win, return "O"
    elif   ((board[0][0]=="O") and (board[0][1]=="O") and (board[0][2]=="O")) \
        or ((board[1][0]=="O") and (board[1][1]=="O") and (board[1][2]=="O")) \
        or ((board[2][0]=="O") and (board[2][1]=="O") and (board[2][2]=="O")) \
        or ((board[0][0]=="O") and (board[1][0]=="O") and (board[2][0]=="O")) \
        or ((board[0][1]=="O") and (board[1][1]=="O") and (board[2][1]=="O")) \
        or ((board[0][2]=="O") and (board[1][2]=="O") and (board[2][2]=="O")) \
        or ((board[0][0]=="O") and (board[1][1]=="O") and (board[2][2]=="O")) \
        or ((board[0][2]=="O") and (board[1][1]=="O") and (board[2][0]=="O")):
        return "O"
    else: #If there is a tie, or the game state is not terminal, return None
        return None
    
    
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If some one has won the game, return true
    if winner(board) != None: 
        return True
    # If no one won, but all cells has been filled , return true
    elif len(actions(board)) == 0:
        return True
    # Else, the game is still in progress, return false
    else: 
        return False
    

def utility(board) :
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Assume that utility function will only be called on a board if terminal(board) is True.
    # if terminal(board) == True: #assume that the board is in terminal state
    the_winner = winner(board)
    if the_winner == "X":
        return 1
    elif the_winner == "O":
        return -1
    else: #If the game ended in a tie
        return 0
    # else: 
    #     raise Exception("This function should only be called on terminal board state!")
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if the board is at terminal state, the minimax function will return None
    if terminal(board):
        return None
    
    # traverse the board to find the optimal action 
    optimal_action, optimal_utility = optimize_action(board=board, depth=0)      
    return optimal_action


def optimize_action(board, depth):
    # # travel through the sub-board in a recursive manner
    # print("\t"*depth,board)
    utility_value = None
    optimal_action = None    
    
    #check if the board is at terminal state
    if not terminal(board):
        # posible actions:
        action_list = list(actions(board))
        
        # compute result board of each actions:           
        result_boards = [result(board, an_action) for an_action in list(action_list)]
        
        # recursively call minimax on each result board            
        utility_list = [optimize_action(a_result_board, depth=depth+1) for a_result_board in result_boards]
            
        # choose an optimal utility value and optimal action from nodes
        if player(board) == "X": # if "X" is the player, choose the action with max score
            optimal_action, utility_value = maximize_option(action_list, utility_list)
        else: # if "O" is the player, choose the action with min score
            optimal_action, utility_value = minimize_option(action_list, utility_list)
    
        ## Print function for debugging
        # if depth == 0:
        #     print(board)
        #     print("Player", player(board))
        #     print(action_list, sep="\t")
        #     print(utility_list, sep="\t")
        #     print(optimal_action, utility_value)
            
    else: # at terminal state
        # compute utility function
        utility_value = utility(board)
        optimal_action = None
    
    ## travel through the sub-board in a recursive manner and print the result (for debugging purposes)
    # depth_space = "\t"*depth
    # print(f"{depth_space} {board}, utility: {utility_value}, player: {player(board)}, optimal action: {optimal_action}, depth: {depth}")
    
    # Return optimal_action and optimal utility_value at first board
    if depth == 0:
        return optimal_action, utility_value
    else: # For other board, only return utility_value
        return utility_value
    

def maximize_option(action_list, utility_list):
    """
    Returns the maximum utility score with the respective action
    """
    max_utility = -2
    max_action = None
    for i in range(len(utility_list)):     
        if utility_list[i] > max_utility:
            max_utility = utility_list[i]
            max_action = action_list[i]
    return max_action, max_utility
            

def minimize_option(action_list, utility_list):
    """
    Returns the minimum utility score with the respective action
    """
    min_utility = +2
    min_action = None
    for i in range(len(utility_list)):        
        if utility_list[i] < min_utility:
            min_utility = utility_list[i]
            min_action = action_list[i]
    return min_action, min_utility
           

# if __name__ == "__main__":
#     trial_board = [["X", "O", "O"],
#                    ["O", "X", "X"],
#                    ["O", "X",  EMPTY]]        
    
#     optimal_action = minimax(trial_board)
#     print(optimal_action)

        
# potential problems: unallowed modification 06/04/2023
# 1. if__name__ == "main__": Done (commented it out)
# 2. raise ValueError: change to raise Exception, comment out the exception in utility: Done
# 3. copy.deepcopy: not a problem, other uses this package
# 4. change the return type of actions(board) from list[tuple] to set[tuple]