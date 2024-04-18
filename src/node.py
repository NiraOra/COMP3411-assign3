# Node data structure in MCTS

# EMPTY = 2
# WE_PLAYED = 1
# OPP_PLAYED = 0
# class Node:
#     def __init__(self, current, boards):
#         self.move = current
#         self.visits = 0
#         self.wins = 0
#         self.children = []
#         self.curr_board = boards

#     def add_child(self, child_node):
#         self.children.append(child_node)
        
#     def pretty_print(self):
#         print(f">>>>> Node: {self.visits} with next move being {self.move}")
        
#     # checking the winning pattern within the node itself ??
#     def winning_pattern(self, boards, p):
#     # check winning pattern lol
#         bd = self.move
#         for x, y, z in ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)):
#             if (   (boards[bd][x] == EMPTY and boards[bd][y] == p and boards[bd][z] == p)
#                     or (boards[bd][x] == p and boards[bd][y] == p and boards[bd][z] == EMPTY)
#                     or (boards[bd][x] == p and boards[bd][y] == EMPTY and boards[bd][z] == p)):
#                     # print("at at", x, y, z, "values", " for", s[p])
#                     return True
#             return False
'''
USING:
1. UCT
2. MCTS
3. maybe RAVE ?

Explanation:

Here, we use a combination of MCTS and UCB1 along with some heuristics to determine the best move tha agent should choose to play against 
the opponent. 

MCTS [Monte Carlo Tree Search] (https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/) is an algorithm that can be used to help search for all the possible moves
using a tree-like data structure. This search has 4 phases: namely Initialisation, Selection, Expansion, Simulation and Back-propogation. 
1. Initilisation: we assert that the root node and add children to it, after which we iterate through the number of simulations.
2. Selection (using UBC1): here, we iterate through all the possible values of the node that can be added 
3. Expansion: 
4. Simulation:
5. Back-propogation:



'''



import random
import numpy as np

EMPTY = 2
WE_PLAYED = 1
OPP_PLAYED = 0
TERMINAL_POINT = -2

WIN_AMOUNT = 50

class Node:
    def __init__(self, move, board, parent=None):
        self.move = move
        self.board = board
        self.children = []
        self.parent = parent
        self.visits = 0
        self.wins = 0
        # self.rave_visits = 0
        # self.rave_wins = 0

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
    
    # winning pattern!
    def winning_pattern(self, board, bd, p):
    # check winning pattern lol
        bd = self.move
        for x, y, z in ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)):
            if (   (board[bd][x] == EMPTY and board[bd][y] == p and board[bd][z] == p)
                    or (board[bd][x] == p and board[bd][y] == p and board[bd][z] == EMPTY)
                    or (board[bd][x] == p and board[bd][y] == EMPTY and board[bd][z] == p)):
                    # print("at at", x, y, z, "values", " for", s[p])
                    return True
            return False

    # def update_rave_stats(self, result):
    #     self.rave_visits += 1
    #     if result == WE_PLAYED:
    #         self.rave_wins += 1
    #     elif result == OPP_PLAYED:
    #         self.rave_wins -= 1

    # to select a chidl that works
    def uct_select_child(self):
        # can change ?
        exploration_constant = 1.41
        best_score = float('-inf')
        best_child = None
        unvisited_children = []
        
        for child in self.children:
            if child.visits == 0:
                unvisited_children.append(child)
            else:
                # formula taken from: https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
                exploitation = child.wins / child.visits
                exploration = exploration_constant * np.sqrt(np.log(self.visits) / child.visits)
                score = exploitation + exploration
                if score > best_score:
                    best_score = score
                    best_child = child

        # if self.rave_visits == 0:
        #     rave_value = 0
        # else:
        #     rave_value = self.rave_wins / self.rave_visits
        #     score += rave_value

        if best_child is None:
            # If all children are unvisited, randomly select one
            best_child = random.choice(unvisited_children) if unvisited_children else random.choice(self.children)

        return best_child

    def simulate(self):
        # Simulate a random playout from this node
        temp_board = np.copy(self.board)
        current_player = WE_PLAYED
        
        while True:
            # Select a child node to explore
            if not self.children:
                # Handle terminal state or leaf node creation
                return TERMINAL_POINT
            
            child = self.uct_select_child()  # Use a selection strategy to choose a child node
            
            # Update the game state based on the selected child node
            small_board_idx = self.move
            move_now = child.move
            # available_moves = [move for move in range(1, 10) if temp_board[small_board_idx][move] == EMPTY]
            
            # # if no available moves, return the fact that it is done
            # if not available_moves:
            #     child.wins -= 1
            #     return TERMINAL_POINT
            
            # random_move = random.choice(available_moves)
            temp_board[small_board_idx][move_now] = current_player

            if current_player == WE_PLAYED:
                # if this move lets us win, then return an encouraging score to win faster
                if child.game_won(temp_board, small_board_idx, WE_PLAYED):
                    return WE_PLAYED
                elif child.winning_pattern(temp_board, small_board_idx, OPP_PLAYED):
                    return OPP_PLAYED  # give a discouraging score to lose slower
            else:     
                # if this move lets us win, then return an encouraging score to win faster
                if child.game_won(temp_board, small_board_idx, OPP_PLAYED):
                    return OPP_PLAYED
                elif child.winning_pattern(temp_board, small_board_idx, WE_PLAYED):
                    return WE_PLAYED  # give a discouraging score to lose slower
            
            # iterate accordingly ?
            self = child
            current_player = WE_PLAYED if current_player == OPP_PLAYED else OPP_PLAYED

    def backpropagate(self, result):
        self.visits += 1
        # self.update_rave_stats(result)
        if result == WE_PLAYED:
            self.wins += 1
        elif result == OPP_PLAYED:
            self.wins -= 1
        elif result == TERMINAL_POINT:
            self.wins -= 1

    def game_won(self, boards, bd, p):
        return (  ( boards[bd][1] == p and boards[bd][2] == p and boards[bd][3] == p )
        or( boards[bd][4] == p and boards[bd][5] == p and boards[bd][6] == p )
        or( boards[bd][7] == p and boards[bd][8] == p and boards[bd][9] == p )
        or( boards[bd][1] == p and boards[bd][4] == p and boards[bd][7] == p )
        or( boards[bd][2] == p and boards[bd][5] == p and boards[bd][8] == p )
        or( boards[bd][3] == p and boards[bd][6] == p and boards[bd][9] == p )
        or( boards[bd][1] == p and boards[bd][5] == p and boards[bd][9] == p )
        or( boards[bd][3] == p and boards[bd][5] == p and boards[bd][7] == p ))

    def game_draw(self, board):
        # Implement the game_draw function for a 3x3 board
        for curr in range(1, 10):
            for move in range(1, 10):
                if board[curr][move] == EMPTY:
                    return False
        return True

def uct_search(board, curr):
    iterations = 1000
    # initial state of the board
    root = Node(curr, board)
    
    # adding children
    for move in range(1, 10):
        if board[curr][move] == EMPTY:
            root.add_child(Node(move, board))
    
    # for the iterations ?
    for _ in range(iterations):
        # we have a node at root, and adding children
        node = root
    
        # Selection phase
        while node.children:
            # selecting a child ? -> will choose smth based on the UCT algos
            node = node.uct_select_child()
        
        # okay so obv this happens every iteration lol
        # print("node selected is", node.move)  
        
        # after selection phase (so it is either random selection or a child actually gets selected)
        # Expansion phase
        small_board_idx = node.move
        # get all the  moves that can be selected and see how it goes
        available_moves = [move for move in range(1, 10) if board[small_board_idx][move] == EMPTY]
        # if there are moves, then choose a move
        if available_moves:
            # choosing a move
            random_move = random.choice(available_moves)
            # copy board
            new_board = np.copy(board)
            # place our move there
            new_board[small_board_idx][random_move] = WE_PLAYED
            # make a new node and add to the child of the node
            new_node = Node(random_move, new_board)
            node.add_child(new_node)
            # simulate + backpropogate from there on
            node = new_node
        # Simulation phase
        # so we simulate the way it works then we back propogate the result
        result = node.simulate()
        # Backpropagation phase
        while node:
            node.backpropagate(result)
            node = node.parent
    return max(root.children, key=lambda child: child.visits).move

