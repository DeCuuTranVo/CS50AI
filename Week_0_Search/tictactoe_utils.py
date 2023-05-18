from tictactoe import initial_state, player, actions, result, winner, terminal, utility

X = "X"
O = "O"
EMPTY = None

ROW = 0
COL = 1

def minimax(board) -> tuple[int, int]:
    """
    Returns the optimal action for the current player on the board.
    """
    game_tree = BoardTree(board)
    game_tree.build_tree()
    game_tree.backtrack_tree()
    # game_tree.traverse_tree()
    return game_tree.root_node.action_of_choice

class BoardTree(object):
    def __init__(self, board):
        if terminal(board):
            raise ValueError("Terminal boards are not allowed.")
        
        self.root_node = BoardNode(board= board, parent=None, action=None, layer=0)
        self.nodes_in_layers = [[],[],[],[],[],[],[],[],[]]
        
        
    def build_tree(self): # create tree game structure and calculate utility score at leaf nodes
        build_queue =  QueueFrontier()
        build_queue.add(self.root_node)
        self.nodes_in_layers[self.root_node.node_layer].append(self.root_node)
        
        while not build_queue.empty():
            current_node = build_queue.remove()  
            if terminal(current_node.board_state):
                continue
            
            possible_actions = actions(current_node.board_state)
            for an_action in possible_actions:
                a_result_board = result(current_node.board_state, an_action)                
                a_child_node = BoardNode(board=a_result_board, parent=current_node, action=an_action, layer=current_node.node_layer+1)
                current_node.children_nodes.append(a_child_node)
                self.nodes_in_layers[current_node.node_layer+1].append(a_child_node)
                
            for child_node in current_node.children_nodes:
                build_queue.add(child_node)
            
            
    def traverse_tree(self): # print game tree
        traverse_stack = StackFrontier()
        traverse_stack.add(self.root_node)
        while not traverse_stack.empty():
            # print(len(traverse_stack.frontier))
            
            current_node = traverse_stack.remove()
            # TODO
            print(current_node)
            # print(current_node.string_board_state)
            
            for child_node in current_node.children_nodes:
                traverse_stack.add(child_node)    
                
            
    def backtrack_tree(self):
        # Loop through node layers
        for current_layer in self.nodes_in_layers[::-1]:
            # Loop through nodes in each layers
            for current_node in current_layer: 
                # print(current_node)
                
                # if node in terminal state, update node utility
                if terminal(current_node.board_state):
                    # Compute utility of this node at terminal state
                    current_node.utility_of_choice = utility(board=current_node.board_state)
                    current_node.action_of_choice = None
                    
                    # Propagate this node's score, and action to parent node
                    current_node.parent_node.children_utility.append(current_node.utility_of_choice)
                    current_node.parent_node.children_action.append(current_node.taken_action)
                    # print(current_node)

                else: # if node is not in terminal state                    
                    # Decide current node's utility score and action from children nodes' utility score
                    # print(current_node)
                    if current_node.player == "X":
                        utility_of_choice = max(current_node.children_utility)
                    else: #current_node.player == "O":
                        utility_of_choice = min(current_node.children_utility)
                        
                    choice_index = current_node.children_utility.index(utility_of_choice)
                    action_of_choice = current_node.children_action[choice_index]
                        
                    # print(player(current_node.board_state), current_node.children_utility, current_node.children_action)
                    
                    # update utility_of_choice and action_of_choice in current_node
                    current_node.update_utility_of_choice(utility_of_choice) 
                    current_node.update_action_of_choice(action_of_choice)
                    
                    # Propagate this node's chosen utility and chosen action to parent node (the root node can not perform this operation)
                    if current_node.parent_node is not None:
                        current_node.parent_node.children_utility.append(current_node.utility_of_choice)
                        current_node.parent_node.children_action.append(current_node.action_of_choice)

                
        # self.traverse_tree()
        
        # for layer in self.nodes_in_layers[::-1]:
        #     # Loop through nodes in each layers
        #     for node in layer: 
        #         print(node)
            
        
        
# # helper class
class BoardNode(object):
    def __init__(self, board, parent, action, layer):
        self.parent_node = parent
        self.taken_action = action
        self.board_state = board 
        self.player = player(board)

        self.children_nodes = []
        self.node_layer = layer
        
        self.utility_of_choice = None
        self.children_utility = []
        
        self.action_of_choice = None
        self.children_action = []
        
    def update_action_of_choice(self, new_action):
        self.action_of_choice = new_action
        
    def update_utility_of_choice(self, new_score):
        self.utility_of_choice = new_score
        
    def __str__(self):
        node_attributes = {"board": self.board_state, "player": self.player, "taken_action": self.taken_action, "utility_of_choice": self.utility_of_choice, "action_of_choice": self.action_of_choice, "layer": self.node_layer, "children_utility": self.children_utility, "children_action": self.children_action} #"parent": self.parent_node,
        # return pprint.pformat(node_attributes)
        return self.node_layer*"\t" + str(node_attributes)
    
    # def string_board_state(self):
    #     board_copy = copy.deepcopy(self.board_state)
    #     for row_idx in range(len(board_copy)):
    #         for col_idx in range(len(board_copy[row_idx])):
    #             if board_copy[row_idx][col_idx] is EMPTY:
    #                 board_copy[row_idx][col_idx] = "_"
                    
    #     return_string = '\n'.join(map(''.join, board_copy))
    #     # print('\n'.join(map(''.join, board_copy)))
    #     return return_string
    
        
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, board_state):
        return any(node.board_state == board_state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        
        
if __name__ == "__main__":
    trial_board = [[EMPTY,"X","O"],
                   ["O","X",  EMPTY],
                   ["X", EMPTY, "O"]]
    
    # trial_board = [["O",EMPTY, "X"],
    #                ["X","O",  "X"],
    #                [EMPTY, EMPTY, "O"]]
         

    # print_board(trial_board)
    # my_tree = BoardTree(trial_board)
    # my_tree.build_tree()
    # my_tree.backtrack_tree()
    # my_tree.traverse_tree()
    optimal_move = minimax(board=trial_board)
    print(optimal_move)