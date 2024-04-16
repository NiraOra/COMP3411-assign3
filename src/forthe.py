# !/usr/bin/python3
# #  agent.py
# #  Nine-Board Tic-Tac-Toe Agent starter code
# #  COMP3411/9814 Artificial Intelligence
# #  CSE, UNSW

# import socket
# import sys
# import numpy as np

# dis just a manual checkyyy (so if there are more than 4 then don't use it ?? but then
# # this is sooo badddd ugh)
# def manual_check(board_check, player):
#     # check: if for example the 3rd cell + 9th cell or 1st n 7th etc are filled; don't prefer 1
#     if boards[board_check][3] == player and boards[board_check][9] == player:
#         return True
#     if boards[board_check][1] == player and boards[board_check][7] == player:
#         return True
#     if boards[board_check][2] == player and boards[board_check][8] == player:
#         return True
#     # or, now if 1 and 3, 4 and 6, 7 and 9 are filled; don't prefer 1
#     if boards[board_check][1] == player and boards[board_check][3] == player or boards[board_check][4] == player and boards[board_check][6] == player or boards[board_check][7] == player and boards[board_check][9] == player:
#         return True
#     # or, now if 1 and 9, 2 and 8, 3 and 7, 4 and 6 are filled; don't prefer 1
#     if boards[board_check][1] == player and boards[board_check][9] == player or boards[board_check][3] == player and boards[board_check][7] == player:
#         return True
#     # or now, if 1 and 4, 2 and 5, 3 and 6, 4 and 7, 5 and 8, 6 and 9 are filled; don't prefer 1
#     if boards[board_check][1] == player and boards[board_check][4] == player or boards[board_check][2] == player and boards[board_check][5] == player or boards[board_check][3] == player and boards[board_check][6] == player or boards[board_check][4] == player and boards[board_check][7] == player or boards[board_check][5] == player and boards[board_check][8] == player or boards[board_check][6] == player and boards[board_check][9] == player:
#         return True
#     # this normal check
#     count = 0
#     for i in range(1, 10):
#         if boards[board_check][i] == player:
#             count += 1
    
#     return count >= 4

# # code from TTT.py
# # but this is our definition (as per agent.py); empty is 0 we played is 1 and opponent played is 2
# EMPTY = 0
# WE_PLAYED = 1
# OPP_PLAYED = 2
# # LETS SAY STILL PLAYING IS 4
# STILL_PLAYING = 4
# # NOT PLAYING 3
# NOT_PLAYING = 3

# '''ILLEGAL_MOVE  = 0
# STILL_PLAYING = 1
# WIN           = 2
# LOSS          = 3
# DRAW          = 4'''

# MAX_MOVE      = 10
# MAX_DEPTH     = 10

# MAX           = 2
# MIN           = 1

# MIN_EVAL = -1000000
# MAX_EVAL =  1000000

# # a board cell can hold:
# #   0 - Empty
# #   1 - We played here
# #   2 - Opponent played here

# # the boards are of size 10 because index 0 isn't used
# boards = np.zeros((10, 10), dtype="int8") 
# for board in range (1,10):
#     for cell in range (1,10):
#         boards[board][cell] = EMPTY # filling the board with empty

# s = ["0", "X", "."]
# curr = 0 # this is the current board to play in

# ###############################################################################

# # print a row
# def print_board_row(bd, a, b, c, i, j, k):
#     print(" "+s[bd[a][i]]+" "+s[bd[a][j]]+" "+s[bd[a][k]]+" | " \
#              +s[bd[b][i]]+" "+s[bd[b][j]]+" "+s[bd[b][k]]+" | " \
#              +s[bd[c][i]]+" "+s[bd[c][j]]+" "+s[bd[c][k]])

# # Print the entire board
# def print_board(board):
#     print_board_row(board, 1,2,3,1,2,3)
#     print_board_row(board, 1,2,3,4,5,6)
#     print_board_row(board, 1,2,3,7,8,9)
#     print(" ------+-------+------")
#     print_board_row(board, 4,5,6,1,2,3)
#     print_board_row(board, 4,5,6,4,5,6)
#     print_board_row(board, 4,5,6,7,8,9)
#     print(" ------+-------+------")
#     print_board_row(board, 7,8,9,1,2,3)
#     print_board_row(board, 7,8,9,4,5,6)
#     print_board_row(board, 7,8,9,7,8,9)
#     print()

# ###############################################################################

# # choose a move to play
# def play(player):
#     # TODO: OKAY IDEALLY CURR IS ALSO GLOBAL SO NO NEED TO CALL IT ANYWHERE. done
#     # print_board(boards)
#     # initialise an array to track all the moves and a second array to track the best moves
#     move = np.zeros(MAX_MOVE,dtype=np.int32)
#     best_move = np.zeros(MAX_MOVE,dtype=np.int32)
#     # initializing depth and player; player is currently us
#     m = 0
#     # player = WE_PLAYED
#     game_state = STILL_PLAYING
#     n = 6
#     depth = MAX_DEPTH
    
#     # while we can still play basically
#     while m < MAX_MOVE and game_state == STILL_PLAYING:
#         # iterate to next element in the array
#         m += 1 
#         # then, we get the alpha beta pruning shit
#         alpha_beta(WE_PLAYED, m, curr, MIN_EVAL, MAX_EVAL, best_move)
#         # after the best move is updated, make it the move
#         move[m] = best_move[m]
#         # then, get game status
#         game_state = place(curr, move[m], player)

#     # n = move[m] = best_move[m]
#     print("Player ", WE_PLAYED," is playing in cell ", move[m], "of board", curr)
#     #print("This is move index", m)
#     # place the current thing in, 
#     place(curr, move[m], 1)
#     # print_board(boards)
#     # hardly think we need to return this shit but whatever
#     return move[m]

# # place a move in the global boards
# def place(current_board, num, player):
#     global curr
#     curr = num
#     boards[current_board][num] = player
#     # check if game has won over here
#     return STILL_PLAYING if game_won(player, current_board) else NOT_PLAYING

#     '''if game_won(player, board):
#         return # win
#     if full_board():
#         return # draw'''
        
# ###############################################################################   
# # nega max WITH alpha beta over here
# def alpha_beta(player, m, curr, alpha, beta, best_move):
#     # we are checking this first
#     best_eval = MIN_EVAL
#     # here, now if other player has won, return the value
#     if game_won(OPP_PLAYED, curr):
#         return MAX_EVAL - m
    
#     # starting here
#     this_move = 0
#     # for 1-10, we are checking the moves being legal or not
#     for r in range( 1, 10):
#         # if move is legal (so it is empty)
#         if boards[curr][r] == EMPTY:         # move is legal
#             # so our current r is the value where it can be placed
#             this_move = r
#             # also making the move possible so we can check possibilities
#             boards[curr][this_move] = player 
#             # recursive check for possibilities 
#             this_eval = -alpha_beta(1 + player, m + 1, curr, -beta, -alpha, best_move)
#             # if this is not possible, empty the move (best_move is updated anyway)
#             boards[curr][this_move] = EMPTY; 
#             # if the value at this point is greater than the best evaluated move, then update the best move + best_eval
#             if this_eval > best_eval:
#                 best_move[m] = this_move;
#                 best_eval = this_eval
#                 # HEURISTIC: if the best evaluated move is greater than alpha (should initially be the case bc alpha is a vv small number)
#                 if best_eval > alpha:
#                     # update alpha
#                     alpha = best_eval
#                     # OUR HEURISTIC cutoff; so if alpha is greater than beta, return alpha
#                     if alpha >= beta:
#                         return( alpha )
    
#     # this should be a draw btw; could be a case of a full board
#     # update this accordingly ??
#     if this_move == 0:
#         return (0)
#     else:
#         # really, return alpha to check and see how it goes
#         return(alpha)
    
# ###############################################################################
# # code from TTT.py file
# def game_won(p, bd):
#     return (  ( boards[bd][1] == p and boards[bd][2] == p and boards[bd][3] == p )
#         or( boards[bd][4] == p and boards[bd][5] == p and boards[bd][6] == p )
#         or( boards[bd][7] == p and boards[bd][8] == p and boards[bd][9] == p )
#         or( boards[bd][1] == p and boards[bd][4] == p and boards[bd][7] == p )
#         or( boards[bd][2] == p and boards[bd][5] == p and boards[bd][8] == p )
#         or( boards[bd][3] == p and boards[bd][6] == p and boards[bd][9] == p )
#         or( boards[bd][1] == p and boards[bd][5] == p and boards[bd][9] == p )
#         or( boards[bd][3] == p and boards[bd][5] == p and boards[bd][7] == p ))

# # code from TTT.py file
# # returns True if the whole board is full
# def full_board():
#     b = 0
#     for board in range(1, 10):
#         for cell in range(1, 10):
#             if boards[board][cell] != EMPTY:
#                 b += 1
#     if ( b == MAX_MOVE ):
#         return True
#     else:
#         return False

# # UNUSED
# # function which calculates the score for the current player
# # function is WRONG
# def calculateScore(board, depth, player):
#     if full_board: # if the game is tied, then the player receives 0
#         return 0
#     elif game_won( player, board ): # if the player wins, then their score is determined by 
#                     # the number of moves taken.
#         return MAX_EVAL/depth
#     else: # else the opponent wins.
#         return MIN_EVAL/depth

# ###############################################################################

# # read what the server sent us and
# # parse only the strings that are necessary
# def parse(string):
#     if "(" in string:
#         command, args = string.split("(")
#         args = args.split(")")[0]
#         args = args.split(",")
#     else:
#         command, args = string, []


#     # init tells us that a new game is about to begin.
#     # start(x) or start(o) tell us whether we will be playing first (x)
#     # or second (o); we might be able to ignore start if we internally
#     # use 'X' for *our* moves and 'O' for *opponent* moves.

#     # second_move(K,L) means that the (randomly generated)
#     # first move was into square L of sub-board K,
#     # and we are expected to return the second move.
#     if command == "second_move":
#         # place the first move (randomly generated for opponent)
#         place(int(args[0]), int(args[1]), 0)
#         return play(WE_PLAYED)  # choose and return the second move

#     # third_move(K,L,M) means that the first and second move were
#     # in square L of sub-board K, and square M of sub-board L,
#     # and we are expected to return the third move.
#     elif command == "third_move":
#         # place the first move (randomly generated for us)
#         place(int(args[0]), int(args[1]), 1)
#         # place the second move (chosen by opponent)
#         place(curr, int(args[2]), 0)
#         # m += 1
#         return play(WE_PLAYED) # choose and return the third move

#     # nex_move(M) means that the previous move was into
#     # square M of the designated sub-board,
#     # and we are expected to return the next move.
#     elif command == "next_move":
#         # place the previous move (chosen by opponent)
#         place(curr, int(args[0]), 0)
#         return play(WE_PLAYED) # choose and return our next move

#     elif command == "win":      
#         print("Yay!! We win!! :)")
#         return -1

#     elif command == "loss":
#         print("We lost :(")
#         return -1

#     return 0

# ###############################################################################

# # connect to socket
# def main():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

#     s.connect(('localhost', port))
#     while True:
#         text = s.recv(1024).decode()
#         if not text:
#             continue
#         for line in text.split("\n"):
#             response = parse(line)
#             if response == -1:
#                 s.close()
#                 return
#             elif response > 0:
#                 s.sendall((str(response) + "\n").encode())

# if __name__ == "__main__":
#     main()


# temp_boards = np.copy(boards)
    # current_player = player
    # current_board = curr
    
    # while True:
    #     # get all available moves (ok so this should be based on 
    #     # the board not being empty AND the opponent has no chance of winning at that point in time)
    #     available_moves = [move for move in range(1, 10) if temp_boards[current_board][move] == EMPTY and not opponent_winning_pattern(temp_boards, move)]
    #     # print("the available moves at that point is", available_moves)
        
    #     if not available_moves:
    #         # Game is a draw if no more moves are available
    #         return 0
        
    #     # prioritizing center (?)
    #     if 5 in available_moves:
    #         random_move = 5
    #     else:
    #         random_move = random.choice(available_moves)
    #     temp_boards[current_board][random_move] = current_player
        
    #     # CHECK THIS FIRST -> so if there's a chance that the opponent wins then we have to return the penalty amount as answer
    #     # if opponent_winning_pattern(temp_boards, current_board):
    #     #     # print("your total score should NOT get it. whatevers")
    #     #     return PENALTY_AMOUNT
        
    #     if game_won(current_player, current_board) and current_player == WE_PLAYED:
    #         # Current player wins
    #         return 1
    #     elif game_won(current_player, current_board) and current_player == OPP_PLAYED:
    #         # opponent won
    #         return PENALTY_AMOUNT
    #     elif full_board():
    #         # Game is a draw
    #         return 0
        
    #     # Switch players and boards for the next move
    #     current_player = WE_PLAYED if current_player == OPP_PLAYED else OPP_PLAYED
    #     current_board = random_move