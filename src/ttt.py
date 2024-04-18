import socket
import random
import sys
import numpy as np
from node import Node
import math

# code from TTT.py
# but this is our definition (as per agent.py); empty is 2 we played is 1 and opponent played is 0
EMPTY = 2
WE_PLAYED = 1
OPP_PLAYED = 0
# LETS SAY STILL PLAYING IS 4
STILL_PLAYING = 4
# NOT PLAYING 3
NOT_PLAYING = 3

'''ILLEGAL_MOVE  = 0
STILL_PLAYING = 1
WIN           = 2
LOSS          = 3
DRAW          = 4'''

MAX_MOVE      = 10
MAX_DEPTH     = 10

MAX           = 2
MIN           = 1

SCORE_DEFAULT = 3

MIN_EVAL = -1000000
MAX_EVAL =  1000000

PENALTY_AMOUNT = -100
WIN_AMOUNT = 2000

# TODO: options trialed so far
# 1. UCT: this should work if i figure out how the child nodes kinda fit in 
# 2. Evaluation: this takes more computation time than necessary; unless I combine it with the 
# MCTS simulation then it will not work
# 3. Move ordering: wouldn't really work unless we have a really good evaluation function (?) since keeping it at 5 as default (for example) may result in some other consequences that icbb to check


# Description
'''
To incorporate a working agent that can play against a human agent, we decided to use a MCTS approach (resource) along with some heuristics to improve the efficiency of the ultimate-tic-tac-toe game played.
Here, we have three major functions: mcts, monte_carlo_simulation and simulate_random_game. The goal of these three function is to iterate through the next available moves present after the opponent has made its move
(so, at the parent node) and then simulate the possible ways the game could continue on from there on using a tree data structure, where each of the child nodes to a node contains a possible move that could be made. By making this tree,
we can then iterate to the very end and determine to return a negative amount if the opponent wins or a positive amount if we win. By returning these amounts as per each simulation, we can then consider the average total
score accumulated at each possible move made from the "parent node" and then choose the best possible score from the available scores, which will then allow us to make the move. 

Our constraints were:
(i) Block the opponent if they have a winning pattern
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

(ii) Prune off the branches which does not allow us to win the game

Similar to checking the winning patters above, we chose to assign scores to the values that gave us a better chance of winning/not a better chance of winning. 


In order to reduce these constraints, we chose heuristics of UCT (CHANGE THIS IF NOT DONE) and also checking winning patterns. Here, UCT ____. Winning patterns allow us to check if the opponent has a chance to 
win the particular board and block the opponent accordingly by avoiding the move that allows the opponent to win. 
We also terminate at the points where we believe the opponent/we win. 

Thus, by using this strategy, we can choose the best possible move and then make this move. 
'''


# a board cell can hold:
#   0 - Empty
#   1 - We played here
#   2 - Opponent played here

# this is a global var that can be updated over here
# this is the current board to play in
curr = 0 

def uct_pruning(node, total_visits):
    best_score = float("-inf")
    best_child = None
    exploration_constant = 1.41  # Adjust the exploration constant
    
    for child in node.children:
        if child.visits == 0:
            return child
        
        exploitation = child.wins / child.visits
        exploration = math.sqrt(math.log(total_visits) / child.visits)
        score = exploitation + exploration_constant * exploration
        
        if score > best_score:
            best_score = score
            best_child = child
    
    return best_child

# OTHER TRIAL: move ordering: so that the children are easily ordered
def move_ordering_heuristic(node):
    to_order = node.children
    
    # order this shit
    
    # return the ordered thing
    return node



# MONTE CARLO TREE SEARCH
def mcts(player, curr, boards):
    # least_depth = 81 # technically the amount you can fully go to. etc
    best_move = None
    best_score = MIN_EVAL
    root_node = Node(curr, boards)
    
    # Optimize move selection by considering only certain moves
    # adding: root node addition to this shit
    possible_moves = [move for move in range(1, 10) if boards[curr][move] == EMPTY]
    for move in possible_moves:
        root_node.add_child(Node(move, boards))
  
    # for child in root_node.children: child.pretty_print()
    
    for child in root_node.children:
     # selecting a move to expand upon
        # child_node = uct_pruning(node, total_visits)
        #boards[curr][move] = player
        avg_score, depth = monte_carlo_selection(player, curr, child, boards)
        #boards[curr][move] = EMPTY

        if avg_score > best_score:
            # print(">>>>>> the least amount of depth", depth)
            best_move = move
            best_score = avg_score
    
    # print(f">>>>> we got the best score as {best_score:.2f}")
    return best_move

# replaying this move for X simulations and find the average outcome
def monte_carlo_selection(player, curr, node, boards):
    total_score = 0
    simulations = 500
    
    # for those many solutions, make a temporary board copy and make the move; find the score and
    # add that to the total score
    for sims in range(simulations):
        temp_boards = np.copy(boards)
        #temp_boards[curr][move] = player
        # incorporate UCT pruning over here ?
        # now, this is where we can add the UCT pruning bit

        score, gotten_depth, result_node = simulate_random_game(node, temp_boards, player, curr)
        
        # score = monte_carlo_evaluation(boards, curr, WE_PLAYED)
        # print(score)
        
        
        # just printing here
        # print(temp_node)


        
        total_score += score
        #print("mcts is simulating its", sims, "th game and returning total score of", total_score)

    # returns the average score of all the simulations for a given move
    average_score = total_score / simulations
    # print(f"this is the average score: {average_score:.2f} for the move {node.move} on board {curr}")
    return average_score, gotten_depth

# CHECK if opp is close to winning
def winning_pattern(boards, bd, p):
    # check winning pattern lol
    for x, y, z in ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)):
      if (   (boards[bd][x] == EMPTY and boards[bd][y] == p and boards[bd][z] == p)
            or (boards[bd][x] == p and boards[bd][y] == p and boards[bd][z] == EMPTY)
            or (boards[bd][x] == p and boards[bd][y] == EMPTY and boards[bd][z] == p)):
            # print("at at", x, y, z, "values", " for", s[p])
            return True

    return False

# example simulation
def simulate_random_game(first_node, temp_boards, player, curr):
    current_player = player # simulate a move for current player first
    current_board = curr    # make the move on the current board
    # score = 0                
    depth = 1
    first_iteration = True
    curr_node = first_node
    chosen_node = None
    # iterate the visits
    # first_node.visits += 1
    
    while True:
        if first_iteration:
            first_iteration = False
            temp_boards[curr][first_node.move] = player
            # chosen_move = Node(first_node, temp_boards)
            chosen_move = first_node.move
            # the current node is as follows
            curr_node = Node(chosen_move, temp_boards)
            curr_node.visits += 1
            chosen_node = curr_node
        else:   
            available_moves = [move for move in range(1, 10) if temp_boards[current_board][move] == EMPTY]
            
            # adding the children in ?
            for move in available_moves:
                # so these are the children that can potentially be formed ??
                curr_node.add_child(Node(move, temp_boards))
                
            if not curr_node.children:
                return 0
        
            # so, it should sort through the available moves
            # ordered_moves = sorted(curr_node.children, key=move_ordering_heuristic(curr_node))
            
            # if not available_moves: # DRAW because there are no possible moves
            #     print("no moves left")
            #     return 0
  
            # chosen_move = random.choice(available_moves)             # Choose a random move
            # now, choosing a node but I am also printing it to check if the node is actually chosen
            # for child in curr_node.children:
            #     if child.move == 5:
            #         chosen_node = child
            #     else: 
            chosen_node = random.choice(curr_node.children)
            # so it works so far. hm
            # YES WORKED!
            temp_boards[current_board][chosen_node.move] = current_player # Place the random move
            #print_board(temp_boards)
            chosen_move = chosen_node.move
            chosen_node.visits += 1

        # print(f">> START >> \n so the chosen node atm is {chosen_node.pretty_print()}")
            
        if current_player == WE_PLAYED:
            # if this moves lets us win, then return an encouraging score. try to win faster
            if game_won(temp_boards, WE_PLAYED, current_board):
                # print("able to win!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return (WIN_AMOUNT), depth, first_node #/ depth
            elif winning_pattern(temp_boards, chosen_move, OPP_PLAYED):
            # print("giving penalty score for move:", random_move, "on board", current_board)
                return (-WIN_AMOUNT), -depth, first_node #/ depth  # give a discouraging score and try to lose slower
        else:     
            # if this moves lets us win, then return an encouraging score. try to win faster
            if game_won(temp_boards, OPP_PLAYED, current_board):
                # print("able to win!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return (-WIN_AMOUNT), -depth, first_node #/ depth
            elif winning_pattern(temp_boards, chosen_move, WE_PLAYED):
            # print("giving penalty score for move:", random_move, "on board", current_board)
                return (WIN_AMOUNT), depth, first_node #/ depth  # give a discouraging score and try to lose slower

        
        
        current_player = WE_PLAYED if current_player == OPP_PLAYED else OPP_PLAYED # swap the players
        current_board = chosen_node.move # move to the new board
        curr_node = chosen_node
        first_node.visits += 1
        # print(f">> END >> \n so the current node we get in the end is {curr_node.pretty_print()}, which should be the same")
        # so the next node chosen is also a node,, hmm
        # print(curr_node.pretty_print())
        depth += 1
        

def game_won(boards, p, bd):
    return (  ( boards[bd][1] == p and boards[bd][2] == p and boards[bd][3] == p )
        or( boards[bd][4] == p and boards[bd][5] == p and boards[bd][6] == p )
        or( boards[bd][7] == p and boards[bd][8] == p and boards[bd][9] == p )
        or( boards[bd][1] == p and boards[bd][4] == p and boards[bd][7] == p )
        or( boards[bd][2] == p and boards[bd][5] == p and boards[bd][8] == p )
        or( boards[bd][3] == p and boards[bd][6] == p and boards[bd][9] == p )
        or( boards[bd][1] == p and boards[bd][5] == p and boards[bd][9] == p )
        or( boards[bd][3] == p and boards[bd][5] == p and boards[bd][7] == p ))

# code from TTT.py file
# returns True if the whole board is full
# def full_board(boards):
#     for board in range(1, 10):
#         for cell in range(1, 10):
#             if boards[board][cell] == EMPTY:
#                 return False
#     return True

