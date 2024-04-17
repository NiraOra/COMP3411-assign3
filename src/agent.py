#!/usr/bin/python3
#  agent.py
#  Nine-Board Tic-Tac-Toe Agent starter code
#  COMP3411/9814 Artificial Intelligence
#  CSE, UNSW

import socket
import random
import sys
import numpy as np


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
WIN_AMOUNT = 100


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
    # # TODO: OKAY IDEALLY CURR IS ALSO GLOBAL SO NO NEED TO CALL IT ANYWHERE. done
    move = mcts(WE_PLAYED, curr)
    print("Player", WE_PLAYED, "is playing in cell", move, "of board", curr)
    # make move
    place(curr, move, 1)
    print_board(boards)
    return move
    
###############################################################################  

# ATTEMPTING MONTE CARLO TREE SEARCH 

# for the MCTS, we are attempting to find the best move from 1 - 10 ig
# we place it, then get score and then check if it the best move possible
# if yes, then updated and keep going till we get to the part
# return the best move possible
def mcts(player, curr):
    best_move = None
    # okay so. we give more score to the one in the middle because there is more chance of it 
    # having a draw if anything 
    best_score = MIN_EVAL
    
    for move in range(1, 10):
        if boards[curr][move] == EMPTY:
            boards[curr][move] = player
            score = monte_carlo_simulation(player, curr, move)
            boards[curr][move] = EMPTY

            if score > best_score:
                best_move = move
                best_score = score
                print("well score", score, " and the best score", best_score, " at the move", move)
    
    print("we got the best score as", best_score)
    return best_move

# monte carlo simulation 
def monte_carlo_simulation(player, curr, move):
    best_score = 0
    # example number of simulations
    # MAX CAN GO without too many illegal moves/timeouts is at 177. so set it at that for the current run
    # more simulations -> the more it can actually do shit ??? idk
    # simulations = 177 (should be 81)
    simulations = 100
    
    # for those many solutions, make a temporary board copy and make the move; find the score and
    # add that to the total score
    for _ in range(simulations):
        temp_boards = np.copy(boards)
        temp_boards[curr][move] = player

        score = simulate_random_game(player, curr)
        # counter += 1
        # total_score += score
        if score > best_score:
            best_score = score
        # print("Score is", score, "and best score atm is", best_score)

    # basically the total score over the number of simulations
    return best_score/simulations

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
def simulate_random_game(player, curr):
    # Create a copy of the current boards state
    # TODO: remove illegal move at X placed in 1 for cell 1
    # TODO: always scoring zero at move 1 after like 8 moves made
    # TODO: score thing first (priority over certain moves) OR count the depth to win (return a tuple)
    temp_boards = np.copy(boards)
    current_player = player
    score = 0
    current_board = curr
    
    while True:
        available_moves = [move for move in range(1, 10) if temp_boards[current_board][move] == EMPTY]
        
        prioritized_moves = []
        for move in available_moves:
            # first priority: OUR winning pattern
            if winning_pattern(temp_boards, move, WE_PLAYED):
                # temp_boards[current_board][move] = WE_PLAYED
                prioritized_moves.append(move)
                # return score + MAX_EVAL
            
            # temp_boards[current_board][move] = OPP_PLAYED
            if winning_pattern(temp_boards, move, OPP_PLAYED):
                # print("herereee")
                # temp_boards[current_board][move] = EMPTY
                # available_moves.remove(move)
                return score + PENALTY_AMOUNT  # Block the opponent and exit the loop
            # temp_boards[current_board][move] = EMPTY
        
        if not available_moves: # DRAW bc no moves
            print("no moves")
            return 0    
        
        # if prioritized_moves:
        #     move = prioritized_moves
        # # If no immediate threat, choose a random move
        # random_move = random.choice(available_moves)
        if prioritized_moves:
            score += 8
            random_move = random.choice(prioritized_moves)
        # elif 5 in available_moves:
        #     score += 0.5
        #     random_move = 5
        else:
            random_move = random.choice(available_moves)

        temp_boards[current_board][random_move] = current_player
        
        if game_won(current_player, current_board) and current_player == WE_PLAYED:
            return score + 50
        elif game_won(current_player, current_board) and current_player == OPP_PLAYED:
            return -1
        elif full_board():
            # no moves 
            # really small num; like 4
            return NOT_PLAYING
        
        score += SCORE_DEFAULT
        # if random_move is the corners then weight it by like 0.1 or smth ?
        if random_move in (1, 3, 7, 9):
            score += 0.1
            
        current_player = WE_PLAYED if current_player == OPP_PLAYED else OPP_PLAYED
        current_board = random_move

        # Implement other heuristics and enhancements as needed

    # return random.randint(0, 100) 
    
# place a move in the global boards
def place(current_board, num, player):
    global curr
    curr = num
    boards[current_board][num] = player

###############################################################################
# code from TTT.py file
def game_won(p, bd):
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
def full_board():
    for board in range(1, 10):
        for cell in range(1, 10):
            if boards[board][cell] == EMPTY:
                return False
    return True
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
