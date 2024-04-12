# trial for just negamax alone !!

import numpy as np

EMPTY = 0
WE_PLAYED = 1
OPP_PLAYED = 2

MAX_MOVE = 10

MIN_EVAL = -100
MAX_EVAL =  100

def negamax(board, depth, alpha, beta,):
    """
    Perform the Negamax search with alpha-beta pruning.

    :param board: Current board state, adjusted to your game's representation.
    :param depth: Current depth in the game tree.
    :param alpha: Alpha value for pruning.
    :param beta: Beta value for pruning.
    :param color: 1 for the maximizing player, -1 for the minimizing player.
    :return: The value of the board and the best move.
    """
    if depth == 0 or is_terminal(board):
        return color * evaluate(board), None

    best_value = float('-inf')
    best_move = None
    for move in get_possible_moves(board):
        new_board = make_move(board, move)
        value, _ = negamax(new_board, depth - 1, -beta, -alpha)
        value = -value
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, value)
        if alpha >= beta:
            break

    return best_value, best_move

def is_terminal(board):
    # Implement your logic to check if the board is a terminal state
    pass

def evaluate(board):
    # Implement your evaluation function here
    pass

def get_possible_moves(board):
    # Return a list of all possible moves in the current board state
    pass

def make_move(board, move, player):
    # Return a new board state after applying the given move
    pass