# codign the minimax algo here
# USING: ttt.py inspo

import numpy as np

EMPTY = 0
WE_PLAYED = 1
OPP_PLAYED = 2

MAX_MOVE = 10

MIN_EVAL = -100
MAX_EVAL =  100

i = 0

def best_move(board, curr):
    # the move
    move = np.zeros(10,dtype=np.int32)
    # whichever is the best move
    best_to_move = np.zeros(10,dtype=np.int32)
    # using the m = 0 
    m = 0
    n = np.random.randint(1,9)  # bro just an example lol
    # # temp()
    print(board[curr])
    game_stat = True
    while m < MAX_MOVE - 1 and game_stat == True:
        # so we update this first ??
        m += 1
        # so we are checking the player, m, using the current board, min val, max val and best move updated
        f = alphabeta(WE_PLAYED, m, board[curr], MIN_EVAL, MAX_EVAL, best_to_move)
        # gets updated basically
        move[m] = best_to_move[m]
        print("move m is", f)
    # actually. also check if the game has been won or not
    game_stat = game_won(board, WE_PLAYED) == True or game_won(board, OPP_PLAYED) == True or False
    # this is the end goal
    # return move[m]
    # TODO: REMOVE THIS SHIT
    return n
    
def temp():
    print("HIIIII!")
    
    
def alphabeta(player, m, board, alpha, beta, best_to_move):
    # beta value
    best_eval = MIN_EVAL
    
    # LOSS is sort of already checked right ? so no need to check loss here 
    # no actually. lets return. anyway. if there is a loss then we are here 
    if game_won(OPP_PLAYED, board):
        return -1000 + m
    
    this_move = 0;
    for r in range(1, 9):
        if m < MAX_MOVE - 1:
            if board[r] == EMPTY:         # move is legal
                this_move = r
                board[this_move] = player # make move
                this_eval = -alphabeta(WE_PLAYED,m+1,board,-beta,-alpha, best_to_move)
                # print("At this point: ", this_eval, "with the best value being, ", best_eval)
                board[this_move] = EMPTY; # undo move
                if this_eval > best_eval:
                    # TODO: m's val is out of bound ??
                    print("m here is ", m)
                    best_to_move[m] = this_move;
                    best_eval = this_eval
                    if best_eval > alpha:
                        alpha = best_eval
                        # what is beta even atp
                        # print("alpha is ", alpha, "and beta MEOWW is ", beta)
                        if alpha >= beta: # cutoff
                            return( alpha )
    if this_move == 0:  # no legal moves
        return( 0 )     # DRAW
    else:
        # print("alpha is sssss ", alpha)
        # print("best move values", best_move)
        return( alpha )
    # n = 3
    # return n

def game_won( p, bd ):
    global i
    print("game won called", bd, "at i", i)
    i += 1
    return(  ( bd[1] == p and bd[2] == p and bd[3] == p )
           or( bd[4] == p and bd[5] == p and bd[6] == p )
           or( bd[7] == p and bd[8] == p and bd[9] == p )
           or( bd[1] == p and bd[4] == p and bd[7] == p )
           or( bd[2] == p and bd[5] == p and bd[8] == p )
           or( bd[3] == p and bd[6] == p and bd[9] == p )
           or( bd[1] == p and bd[5] == p and bd[9] == p )
           or( bd[3] == p and bd[5] == p and bd[7] == p ))