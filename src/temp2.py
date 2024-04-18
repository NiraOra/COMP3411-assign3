# def mcts(player, curr):
#     # least_depth = 81 # technically the amount you can fully go to. etc
#     best_move = None
#     best_score = MIN_EVAL
    
#     # Optimize move selection by considering only certain moves
#     possible_moves = [move for move in range(1, 10) if boards[curr][move] == EMPTY]
    
#     for move in possible_moves:
#      # selecting a move to expand upon
#         child_node = uct_pruning(node, total_visits)
#         #boards[curr][move] = player
#         avg_score, depth = monte_carlo_selection(player, curr, move)
#         #boards[curr][move] = EMPTY

#         if avg_score > best_score:
#             print(">>>>>> the least amount of depth", depth)
#             best_move = move
#             best_score = avg_score
    
#     print(f">>>>> we got the best score as {best_score:.2f}")
#     return best_move

# # replaying this move for X simulations and find the average outcome
# def monte_carlo_selection(player, curr, move):
#     total_score = 0
#     simulations = 500
    
#     # for those many solutions, make a temporary board copy and make the move; find the score and
#     # add that to the total score
#     for sims in range(simulations):
#         temp_boards = np.copy(boards)
#         #temp_boards[curr][move] = player

#         score, gotten_depth = simulate_random_game(move, temp_boards, player, curr)
#         total_score += score
#         #print("mcts is simulating its", sims, "th game and returning total score of", total_score)

#     # returns the average score of all the simulations for a given move
#     average_score = total_score / simulations
#     print(f"this is the average score: {average_score:.2f} for the move {move} on board {curr}")
#     return average_score, gotten_depth

# # CHECK if opp is close to winning
# def winning_pattern(boards, bd, p):
#     # check winning pattern lol
#     for x, y, z in ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)):
#       if (   (boards[bd][x] == EMPTY and boards[bd][y] == p and boards[bd][z] == p)
#             or (boards[bd][x] == p and boards[bd][y] == p and boards[bd][z] == EMPTY)
#             or (boards[bd][x] == p and boards[bd][y] == EMPTY and boards[bd][z] == p)):
#             # print("at at", x, y, z, "values", " for", s[p])
#             return True

#     return False

# # example simulation
# def simulate_random_game(first_move, temp_boards, player, curr):
#     current_player = player # simulate a move for current player first
#     current_board = curr    # make the move on the current board
#     # score = 0                
#     depth = 1
#     deep = 1
#     first_iteration = True
    
#     while True:
#         if first_iteration:
#             first_iteration = False
#             temp_boards[curr][first_move] = player
#             chosen_move = first_move
#         else:   
#             available_moves = [move for move in range(1, 10) if temp_boards[current_board][move] == EMPTY]
            
#             if not available_moves: # DRAW because there are no possible moves
#                 print("no moves left")
#                 return 0
            
#             chosen_move = random.choice(available_moves)             # Choose a random move
#             temp_boards[current_board][chosen_move] = current_player # Place the random move
#             #print_board(temp_boards)

#         if current_player == WE_PLAYED:
#             # if this moves lets us win, then return an encouraging score. try to win faster
#             if game_won(temp_boards, WE_PLAYED, current_board):
#                 # print("able to win!!!!!!!!!!!!!!!!!!!!!!!!!!")
#                 return (WIN_AMOUNT), depth #/ depth
#             elif winning_pattern(temp_boards, chosen_move, OPP_PLAYED):
#             # print("giving penalty score for move:", random_move, "on board", current_board)
#                 return (-WIN_AMOUNT), -depth #/ depth  # give a discouraging score and try to lose slower
#         else:     
#              # if this moves lets us win, then return an encouraging score. try to win faster
#             if game_won(temp_boards, OPP_PLAYED, current_board):
#                 # print("able to win!!!!!!!!!!!!!!!!!!!!!!!!!!")
#                 return (-WIN_AMOUNT), -depth #/ depth
#             elif winning_pattern(temp_boards, chosen_move, WE_PLAYED):
#             # print("giving penalty score for move:", random_move, "on board", current_board)
#                 return (WIN_AMOUNT), depth #/ depth  # give a discouraging score and try to lose slower

#         current_player = WE_PLAYED if current_player == OPP_PLAYED else OPP_PLAYED # swap the players
#         current_board = chosen_move # move to the new board
#         depth += 1

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
2. Selection (using UBC1): here, we iterate through all the possible values of the node that can be made (thus, called child nodes) and expand the possibilities of that before we come to a selection criterion. 
Using the formulae provided (https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/), we determined that we should use the exploration constant 1.41 to decide
whether this child node would be the best possible scenario to choose. This is also enhanced by RAVE heuristics _____. 
3. Expansion: Here, we basically expand out the nodes and add all the child nodes we can, before we reach an end (where no more moves are possible as such).
4. Simulation: After we determine this, we choose the child nodes and start simulating the game based on the connections that we found. This is where we
also check if there is any winning moves possible with the opponent/with us, for which we basically boost our opportunity of winning. 

While simulating, we are trying to reduce the computation time by:

(i) Blocking the opponent if they have a winning pattern
For example, consider the board numbered 5 from the UTTT where the opponent is X and the moves placed are as follows:
[(1, 1), (1, 7), (7, 3), (3, 1), (1, 9)]*
   X        O       X       O       X
* The tuple is (board, spot chosen)

_________________________
| X . . | . .   | o . . |
| . . . | . . . | . . . |
| o . X | . . . | . . . |
_________________________
| , . . | . . . | . . . |
| . . . | . . . | . . . |
| . . . | . . . | . . . |
_________________________
| . . X | . . . | . . . |
| . . . | . . . | . . . |
| . . . | . . . | . . . |
_________________________

Where the opponent X has made a move at board 9 and we have to choose a move at board 9. 
As seen from the example, if we chose spot 1 at board 9, then the opponent will have a chance to win the game by a pattern [1 5 9].
So, to avoid this, we "block" the opponent by not considering this move and instead choosing any other move that will give us a better chance of winning. 

(ii) Pruning off the branches which does not allow us to win the game

Similar to checking the winning patters above, we chose to assign scores to the values that gave us a better chance of winning/not a better chance of winning. 

5. Back-propogation: After we find a place where either we/opponent win, we back propogate and update the number of wins accordingly. Then, based on most wins, we choose
the best possible move and then return this move. [RAVE updated -> if using RAVE]
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
        self.draws = 0
        self.losses = 0
        self.score = 0
        self.rave_visits = 0
        self.rave_wins = 0

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

    def update_rave_stats(self, result):
        self.rave_visits += 1
        if result == WE_PLAYED:
            self.rave_wins += 1

    # to select a child that works
    def uct_select_child(self):
        # get the constant, etc
        exploration_constant = 1.41
        best_score = float('-inf')
        best_child = None
        unvisited_children = []

        # for every child, check the visits; if it is not visited then append to the unvisited array
        for child in self.children:
            if child.visits == 0:
                unvisited_children.append(child)
            else:
                # otherwise, calculate the score
                exploitation = child.wins / child.visits
                exploration = exploration_constant * np.sqrt(np.log(self.visits) / child.visits)
                score = exploitation + exploration
                
                # Incorporate RAVE statistics into the score so we can choose more effectively
                # rave_value = 0
                # if child.rave_visits > 0:
                #     rave_value = child.rave_wins / child.rave_visits
                # score += rave_value

                # based on the biggest score, choose the best child
                if score > best_score:
                    # print(f">>>>>> Score at this point is {score:.2f}")
                    best_score = score
                    best_child = child

        # If all children are unvisited, randomly select one from the unvisited array and return
        if best_child is None:
            best_child = random.choice(unvisited_children) if unvisited_children else random.choice(self.children)

        return best_child

    def simulate(self):
        # Simulate a random playout from this node
        temp_board = np.copy(self.board)
        current_player = WE_PLAYED
        # score = 0
        
        while True:
            available = [move for move in range(1, 10) if temp_board[self.move][move] == EMPTY]
            for move in available:
                self.add_child(Node(move, temp_board, self))
            
            # Select a child node to explore
            if not self.children: 
                # Handle terminal state or leaf node creation
                return TERMINAL_POINT
            
            # TODO: actually, need to add children here right?
            # probs not !!!
            
            child = self.uct_select_child()  # Use a selection strategy to choose a child node
            # child = random.choice(self.children)
            
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
            
            if current_player == OPP_PLAYED:
                # if this move lets us win, then return an encouraging score to win faster
                if child.game_won(temp_board, move_now, WE_PLAYED):
                    return WIN_AMOUNT
                elif child.winning_pattern(temp_board, move_now, OPP_PLAYED):
                    # print(f">>>> YESS for {child.move}")
                    return (-WIN_AMOUNT)  # give a discouraging score to lose slower
                elif child.board_full(temp_board, move_now): # checking if the next move makes a board full
                    return TERMINAL_POINT
            else:   
                # if this move lets us win, then return an encouraging score to win faster
                if child.game_won(temp_board, move_now, OPP_PLAYED):
                    return (-WIN_AMOUNT)
                elif child.winning_pattern(temp_board, move_now, WE_PLAYED):
                    return WIN_AMOUNT  # give a discouraging score to win faster
                elif child.board_full(temp_board, move_now):
                    return TERMINAL_POINT
                
            # if child.game_draw(temp_board):
            #     return TERMINAL_POINT
            
            # iterate accordingly ?
            self = child
            current_player = WE_PLAYED if current_player == OPP_PLAYED else OPP_PLAYED

    # def backpropagate(self, result):
    #     # okay lets add RAVE too
    #     self.visits += 1
    #     if result == WIN_AMOUNT:
    #         self.wins += 1
    #     elif result == (-WIN_AMOUNT):
    #         self.losses += 1
            
    #     if self.parent is not None:
    #         self.parent.backpropagate(result)
    def backpropagate(self, result):
        stack = [self]
        while stack:
            node = stack.pop()
            node.visits += 1
            if result == WIN_AMOUNT:
                node.wins += 1
            elif result == (-WIN_AMOUNT):
                node.losses += 1
            elif result == TERMINAL_POINT:
                node.draws += 1
            
            if node.parent is not None:
                stack.append(node.parent)
        #     self.wins -= 1
        # self.update_rave_stats(result)
        # if result == WE_PLAYED:
        #     self.wins += 1
        # 
        # # IDK IF THIS GETS CHECKED AT ANY POINT IN TIME
        # elif result == TERMINAL_POINT:
        #     self.wins += 0
        # self.update_rave_stats(result)
        
    def board_full(self, board, curr):
        for move in range(1, 10):
                if board[curr][move] == EMPTY:
                    return False
        return True

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
    iterations = 2000
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
            # selecting a child; randomizing the algorithm ATM
            # TODO: check if better to use UCT
            node = random.choice(node.children)
        
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
        # while node:
        node.backpropagate(result)
            # node = node.parent
       
    # USING THE RATIO of win to loss TO CALCULATE THE BEST MOVE     
    ratio = 0  
    
    best_move = max(root.children, key=lambda child: child.visits).move 
    # best_move = None
    
    for child in root.children:
        # print(f" why {child.wins} with losses {child.losses} with visits {child.visits}")
        visit_temp = child.visits
        # win_temp = child.wins
        # loss_temp = child.losses
        
        if visit_temp == 0:
            continue
        else: 
            score = (child.wins - child.losses) / child.visits
            
            if child.draws > 0:
                score += 0.5 * child.draws
            
            if score > ratio:
                # print(">>>> here <<<<<")
                ratio = score
                best_move = child.move
    # print(f">>>>> max wins move is: {mommm} for the node visits {whwhw}")
    
    return best_move

