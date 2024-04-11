# codign the minimax algo here

import numpy as np

EMPTY = 2

ILLEGAL_MOVE  = 0
STILL_PLAYING = 1
WIN           = 2
LOSS          = 3
DRAW          = 4

MAX_MOVE      = 9

MIN_EVAL = -100
MAX_EVAL =  100

def best_move(board, curr):
    move = np.zeros(10,dtype=np.int32)
    # whichever is the best move ?
    best_to_move = np.zeros(10,dtype=np.int32)
    m = 0
    temp()
    print(board[curr])
    n = alphabeta(1, m, board[curr], MIN_EVAL, MAX_EVAL, best_to_move)
    move[m] = best_to_move[m]
    return n
    
def temp():
    print("HIIIII!")
    
    
def alphabeta(player, m, board, alpha, beta, best_to_move):
    # beta value
    best_eval = MIN_EVAL
    
    if game_won( 1-player, board ):   # LOSS
        return -1000 + m; # better to win faster (or lose slower)
    this_move = 0;
    for r in range( 1, 10):
        if board[r] == EMPTY:         # move is legal
            this_move = r
            board[this_move] = player # make move
            this_eval = -alphabeta(1-player,m+1,board,-beta,-alpha, best_to_move)
            # print("At this point: ", this_eval, "with the best value being, ", best_eval)
            board[this_move] = EMPTY; # undo move
            if this_eval > best_eval:
                best_to_move[m] = this_move;
                best_eval = this_eval
                if best_eval > alpha:
                    alpha = best_eval
                    # what is beta even atp
                    # print("alpha is ", alpha, "and beta MEOWW is ", beta)
                    if alpha >= beta: # cutoff
                        return( alpha )
    # if this_move == 0:  # no legal moves
    #     return( 0 )     # DRAW
    # else:
    #     print("alpha is sssss ", alpha)
    #     print("best move values", best_move)
    #     return( alpha )
    n = 6
    return n

def game_won( p, bd ):
    return(  ( bd[1] == p and bd[2] == p and bd[3] == p )
           or( bd[4] == p and bd[5] == p and bd[6] == p )
           or( bd[7] == p and bd[8] == p and bd[9] == p )
           or( bd[1] == p and bd[4] == p and bd[7] == p )
           or( bd[2] == p and bd[5] == p and bd[8] == p )
           or( bd[3] == p and bd[6] == p and bd[9] == p )
           or( bd[1] == p and bd[5] == p and bd[9] == p )
           or( bd[3] == p and bd[5] == p and bd[7] == p ))