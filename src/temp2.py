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