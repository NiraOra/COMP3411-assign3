# Node data structure in MCTS

EMPTY = 2
WE_PLAYED = 1
OPP_PLAYED = 0
class Node:
    def __init__(self, current, boards):
        self.move = current
        self.visits = 0
        self.wins = 0
        self.children = []
        self.curr_board = boards

    def add_child(self, child_node):
        self.children.append(child_node)
        
    def pretty_print(self):
        print(f">>>>> Node: {self.visits} with next move being {self.move}")
        
    # checking the winning pattern within the node itself ??
    def winning_pattern(self, boards, p):
    # check winning pattern lol
        bd = self.move
        for x, y, z in ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)):
            if (   (boards[bd][x] == EMPTY and boards[bd][y] == p and boards[bd][z] == p)
                    or (boards[bd][x] == p and boards[bd][y] == p and boards[bd][z] == EMPTY)
                    or (boards[bd][x] == p and boards[bd][y] == EMPTY and boards[bd][z] == p)):
                    # print("at at", x, y, z, "values", " for", s[p])
                    return True
            return False