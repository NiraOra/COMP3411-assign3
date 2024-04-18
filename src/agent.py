#!/usr/bin/python3
#  agent.py
#  Nine-Board Tic-Tac-Toe Agent starter code
#  COMP3411/9814 Artificial Intelligence
#  CSE, UNSW

import socket
import random
import sys
import numpy as np
import node as nd
import math
import ttt

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

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8") 
for board in range (1,10):
    for cell in range (1,10):
        boards[board][cell] = EMPTY # filling the board with empty

s = ["0", "X", "."]
curr = 0 # this is the current board to play in

###############################################################################

# print a row
def print_board_row(bd, a, b, c, i, j, k):
    print(" "+s[bd[a][i]]+" "+s[bd[a][j]]+" "+s[bd[a][k]]+" | " \
             +s[bd[b][i]]+" "+s[bd[b][j]]+" "+s[bd[b][k]]+" | " \
             +s[bd[c][i]]+" "+s[bd[c][j]]+" "+s[bd[c][k]])

# Print the entire board
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()

###############################################################################

# choose a move to play
def play():
    # used ttt file to put all the code there; we are done in that sense
    move = ttt.mcts(WE_PLAYED, curr, boards)
    # temp: using the current agent file
    # move = mcts(WE_PLAYED, curr)
    print("Player", WE_PLAYED, "is playing in cell", move, "of board", curr)
    # make move
    place(curr, move, 1)
    print_board(boards)
    return move

def mcts(player, curr):
    # least_depth = 81 # technically the amount you can fully go to. etc
    best_move = None
    best_score = MIN_EVAL
    
    # Optimize move selection by considering only certain moves
    possible_moves = [move for move in range(1, 10) if boards[curr][move] == EMPTY]
    
    for move in possible_moves:
     # selecting a move to expand upon
        # child_node = uct_pruning(node, total_visits)
        #boards[curr][move] = player
        avg_score, depth = monte_carlo_selection(player, curr, move)
        #boards[curr][move] = EMPTY

        if avg_score > best_score:
            # print(">>>>>> the least amount of depth", depth)
            best_move = move
            best_score = avg_score
    
    print(f">>>>> we got the best score as {best_score:.2f}")
    return best_move

# replaying this move for X simulations and find the average outcome
def monte_carlo_selection(player, curr, move):
    total_score = 0
    simulations = 500
    
    # for those many solutions, make a temporary board copy and make the move; find the score and
    # add that to the total score
    for sims in range(simulations):
        temp_boards = np.copy(boards)
        #temp_boards[curr][move] = player

        score, gotten_depth = simulate_random_game(move, temp_boards, player, curr)
        total_score += score
        #print("mcts is simulating its", sims, "th game and returning total score of", total_score)

    # returns the average score of all the simulations for a given move
    average_score = total_score / simulations
    # print(f"this is the average score: {average_score:.2f} for the move {move} on board {curr}")
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
def simulate_random_game(first_move, temp_boards, player, curr):
    current_player = player # simulate a move for current player first
    current_board = curr    # make the move on the current board
    # score = 0                
    depth = 1
    deep = 1
    first_iteration = True
    
    while True:
        if first_iteration:
            first_iteration = False
            temp_boards[curr][first_move] = player
            chosen_move = first_move
        else:   
            available_moves = [move for move in range(1, 10) if temp_boards[current_board][move] == EMPTY]
            
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

###############################################################################  
# place a move in the global boards
def place(current_board, num, player):
    global curr
    curr = num
    boards[current_board][num] = player

###############################################################################

# read what the server sent us and
# parse only the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []


    # init tells us that a new game is about to begin.
    # start(x) or start(o) tell us whether we will be playing first (x)
    # or second (o); we might be able to ignore start if we internally
    # use 'X' for *our* moves and 'O' for *opponent* moves.

    # second_move(K,L) means that the (randomly generated)
    # first move was into square L of sub-board K,
    # and we are expected to return the second move.
    if command == "second_move":
        # place the first move (randomly generated for opponent)
        place(int(args[0]), int(args[1]), 0)
        return play()  # choose and return the second move

    # third_move(K,L,M) means that the first and second move were
    # in square L of sub-board K, and square M of sub-board L,
    # and we are expected to return the third move.
    elif command == "third_move":
        # place the first move (randomly generated for us)
        place(int(args[0]), int(args[1]), 1)
        # place the second move (chosen by opponent)
        place(curr, int(args[2]), 0)
        # m += 1
        return play() # choose and return the third move

    # nex_move(M) means that the previous move was into
    # square M of the designated sub-board,
    # and we are expected to return the next move.
    elif command == "next_move":
        # place the previous move (chosen by opponent)
        place(curr, int(args[0]), 0)
        return play() # choose and return our next move

    elif command == "win":      
        print("Yay!! We win!! :)")
        return -1

    elif command == "loss":
        print("We lost :(")
        return -1

    return 0

###############################################################################

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()