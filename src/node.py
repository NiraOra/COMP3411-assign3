# Node data structure in MCTS


class Node:
    def __init__(self, state, boards):
        self.curr = state
        self.visits = 0
        self.wins = 0
        self.children = []
        self.curr_board = boards

    def add_child(self, child_node):
        self.children.append(child_node)
        
    def pretty_print(self):
        print(f">>>>> Node: {self.visits} with next move being {self.curr}")