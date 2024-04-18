import socket
import random
import sys
import numpy as np
import node as nd
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


# a board cell can hold:
#   0 - Empty
#   1 - We played here
#   2 - Opponent played here

# this is a global var that can be updated over here
# this is the current board to play in
curr = 0 

# MONTE CARLO TREE SEARCH
def mcts(player, curr, boards):
    # least_depth = 81 # technically the amount you can fully go to. etc
    best_move = None
    best_score = MIN_EVAL
    # so now, this has the nodes and shit right. like this is the current board
    root_node = nd.Node(curr, boards) 
    
    # Optimize move selection by considering only certain moves
    possible_moves = [move for move in range(1, 10) if boards[curr][move] == EMPTY]
    # possible node combos
    for move in possible_moves:
        child = nd.Node(move, boards)
        root_node.add_child(child)
    
    # Generate child nodes for possible moves
    # root_node.add_children([nd.Node(move, boards) for move in range(1, 10) if boards[curr][move] == EMPTY])
    
    # now all added; iterate through root node ?
    for child in root_node.children:
     # selecting a move to expand upon
        #boards[curr][move] = player
        avg_score, depth = monte_carlo_selection(root_node, player, curr, move, boards)
        # also get the uct pruning thing ?; so we do this before the whole thing or ???? idk
        # child_node = uct_pruning(node, depth)
        #boards[curr][move] = EMPTY

        if avg_score > best_score:
            print(">>>>>> the least amount of depth", depth)
            best_move = move
            best_score = avg_score
    
    print(f">>>>> we got the best score as {best_score:.2f}")
    return best_move

# replaying this move for X simulations and find the average outcome
def monte_carlo_selection(node, player, curr, move, boards):
    total_score = 0
    simulations = 500
    
    # for those many solutions, make a temporary board copy and make the move; find the score and
    # add that to the total score
    for sims in range(simulations):
        temp_boards = np.copy(boards)
        #temp_boards[curr][move] = player

        # give the node itself so the move is not required anymore ?
        score, gotten_depth = simulate_random_game(move, temp_boards, player, curr, node)
        total_score += score
        #print("mcts is simulating its", sims, "th game and returning total score of", total_score)

    # returns the average score of all the simulations for a given move
    average_score = total_score / simulations
    print(f"this is the average score: {average_score:.2f} for the move {move} on board {curr}")
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
def simulate_random_game(first_move, temp_boards, player, curr, node):
    # check the iterations and shit
    current_player = player # simulate a move for current player first
    current_board = curr    # make the move on the current board               
    depth = 1
    first_iteration = True
    
    while True:
        if first_iteration:
            first_iteration = False
            temp_boards[curr][first_move] = player
            chosen_move = first_move
        else:   
            available_moves = [move for move in range(1, 10) if temp_boards[current_board][move] == EMPTY]
            # TODO: this makes an error for some reason ?? hmm
            # for sppp in available_moves:
            #     ideal = nd.Node(sppp, temp_boards)
            #     node.add_child(ideal)
            
            if not available_moves: # DRAW because there are no possible moves
                print("no moves left")
                return 0
            
            chosen_move = random.choice(available_moves)             # Choose a random move
            temp_boards[current_board][chosen_move] = current_player # Place the random move
            #print_board(temp_boards)

        if current_player == WE_PLAYED:
            # if this moves lets us win, then return an encouraging score. try to win faster
            if game_won(temp_boards, WE_PLAYED, current_board):
                # print("able to win!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return (WIN_AMOUNT), depth #/ depth
            elif winning_pattern(temp_boards, chosen_move, OPP_PLAYED):
            # print("giving penalty score for move:", random_move, "on board", current_board)
                return (-WIN_AMOUNT), -depth #/ depth  # give a discouraging score and try to lose slower
        else:     
             # if this moves lets us win, then return an encouraging score. try to win faster
            if game_won(temp_boards, OPP_PLAYED, current_board):
                # print("able to win!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return (-WIN_AMOUNT), -depth #/ depth
            elif winning_pattern(temp_boards, chosen_move, WE_PLAYED):
            # print("giving penalty score for move:", random_move, "on board", current_board)
                return (WIN_AMOUNT), depth #/ depth  # give a discouraging score and try to lose slower

        current_player = WE_PLAYED if current_player == OPP_PLAYED else OPP_PLAYED # swap the players
        current_board = chosen_move # move to the new board
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