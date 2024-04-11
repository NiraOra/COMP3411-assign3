#**********************************************************
#   ttt.py
#
#   UNSW CSE
#   COMP3411/9814
#   Code for Tic-Tac-Toe with Alpha-Beta search
#   This is for the 3x3 tic-tac-toe; need to do the same with a 9x9 one
#
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

def main():
    # so you have the board here ?
    # basically. need a 2d arrayyy
    board = EMPTY*np.ones(10,dtype=np.int32)
    # all the moves
    move = np.zeros(10,dtype=np.int32)
    # whichever is the best move ?
    best_move = np.zeros(10,dtype=np.int32)
    # is the agent being referred human or not ?
    is_human = (True,False)
    game_status = STILL_PLAYING
    player = 1
    m = 0

    # while m < MAX_MOVE (so m is being incremented ???) and you are still playing ?
    while m < MAX_MOVE and game_status == STILL_PLAYING:
        m += 1
        # just checking m basically
        print("m at this point is", m)
        # what
        # so either human or agent (which is us in this case)
        player = 1-player;
        # if the player is human ?
        if is_human[player]:
            print_board( board )
            move[m] = input('Enter move [1-9]: ')
            # ou wait. so if the move is not empty or if the move is not in the range of 1 to 9 ? or if the board is not empty then you
            # need to get a number that works
            while move[m] < 1 or move[m] > 9 or board[move[m]] != EMPTY:
                # then you ask for the move again
                move[m] = input('Enter move [1-9]: ')
        else:
            # this is where the agent gets to decide what to play so this is what we are coding
            # if in the range of 1-9 and board is empty, find the best move that can be made
            alphabeta( player,m,board,MIN_EVAL,MAX_EVAL,best_move )
            # and that move becomes the best move, which then allows you to make the best move
            # m = 1-9 iteration 
            move[m] = best_move[m];
        game_status = make_move( player, m, move, board )

    print_board( board )

# TODO: my best move love. this is where you shoudl implement the code
# now this has to be the best move function to be used atm
def best_move(bd, curr):
    temp()
    print_check(bd, curr)
    return 6
    # best_move = [-1]  # Initialize with an invalid move
    # player = 1
    # alpha = MIN_EVAL
    # beta = MAX_EVAL
    # best_score = MIN_EVAL

    # for m in range(1, 10):  # Loop through all possible moves
    #     if bd[curr][m] == EMPTY:  # If the move is legal
    #         # make_move() bd[curr][m]  # Make the move
    #         score = -alphabeta(1-player, 0, bd[curr], -beta, -alpha, best_move)  # Evaluate the move
    #         bd[curr][m] = EMPTY  # Undo the move

    #         if score > best_score:  # If this move is better than the previous best
    #             best_score = score
    #             best_move[0] = m  # Update the best move

    # return best_move[0]  # Return the best move's index


# just smth lol
def temp():
    print("HIILLLL")

#**********************************************************
#   Print the board
#
def print_board( bd ):
    sb = 'XO.'
    print('|',sb[bd[1]],sb[bd[2]],sb[bd[3]],'|')
    print('|',sb[bd[4]],sb[bd[5]],sb[bd[6]],'|')
    print('|',sb[bd[7]],sb[bd[8]],sb[bd[9]],'|')

#**********************************************************
#   Negamax formulation of alpha-beta search
#
def alphabeta( player, m, board, alpha, beta, best_move ):

    best_eval = MIN_EVAL;

    if game_won( 1-player, board ):   # LOSS
        return -1000 + m; # better to win faster (or lose slower)

    this_move = 0;
    for r in range( 1, 10):
        if board[r] == EMPTY:         # move is legal
            this_move = r
            board[this_move] = player # make move
            this_eval = -alphabeta(1-player,m+1,board,-beta,-alpha,best_move)
            print("At this point: ", this_eval, "with the best value being, ", best_eval)
            board[this_move] = EMPTY; # undo move
            if this_eval > best_eval:
                best_move[m] = this_move;
                best_eval = this_eval
                if best_eval > alpha:
                    alpha = best_eval
                    # what is beta even atp
                    print("alpha is ", alpha, "and beta MEOWW is ", beta)
                    if alpha >= beta: # cutoff
                        return( alpha )

    if this_move == 0:  # no legal moves
        return( 0 )     # DRAW
    else:
        print("alpha is sssss ", alpha)
        print("best move values", best_move)
        return( alpha )
#**********************************************************
#   printing out the values of the current board
#
def print_check( bd, curr ):
    # nothign much, just to check the O values are actually getting implemented
    print("this is where", curr)
    for i in range(9):
        print(bd[curr][i])

#**********************************************************
#   Make specified move on the board and return game status
#
def make_move( player, m, move, board ):
    print("m at this point is", m, "which is subject to change")
    if board[move[m]] != EMPTY:
        print('Illegal Move')
        return ILLEGAL_MOVE
    else:
        board[move[m]] = player
        if game_won( player, board ):
            return WIN
        elif full_board( board ):
            return DRAW
        else:
            return STILL_PLAYING

#**********************************************************
#   Return True if the board is full
#
def full_board( board ):
    b = 1
    while b <= 9 and board[b] != EMPTY:
        b += 1
    return( b == 10 )

#**********************************************************
#   Return True if game won by player p on board bd[]
#
def game_won( p, bd ):
    return(  ( bd[1] == p and bd[2] == p and bd[3] == p )
           or( bd[4] == p and bd[5] == p and bd[6] == p )
           or( bd[7] == p and bd[8] == p and bd[9] == p )
           or( bd[1] == p and bd[4] == p and bd[7] == p )
           or( bd[2] == p and bd[5] == p and bd[8] == p )
           or( bd[3] == p and bd[6] == p and bd[9] == p )
           or( bd[1] == p and bd[5] == p and bd[9] == p )
           or( bd[3] == p and bd[5] == p and bd[7] == p ))

if __name__ == '__main__':
    main()
