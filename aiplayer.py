from player import Player
import random
import time
from collections import defaultdict
from copy import deepcopy
import math

class AIPlayer(Player):
    def __init__(self, color, board, type):
        super().__init__(color, board, type)
        self.time_limit = 0.5
    
    def heuristic(self):
        valid_pieces = self.board.get_valid_pieces()
        if not valid_pieces:
            return None
        best_score = float('-inf')
        best_piece = None
        special_grid = [(2, 7), (2, 8), (2, 9)]
        for piece in valid_pieces:
            score = 0
            valid_move = self.board.get_valid_moves_mcts(piece)
            if valid_move == (2, 10):
                score += 10
            elif valid_move == (2, 5):
                score += 8
            elif valid_move in special_grid:
                score += 7
            elif valid_move == (1, 5):
                score += 5
            elif valid_move == (2, 6):
                score -= 5
            else:
                score += 1
            if score >= best_score:
                best_score = score
                best_piece = piece
        return best_piece
    
    def random(self):
        valid_pieces = self.board.get_valid_pieces()
        if not valid_pieces:
            return None
        return random.choice(valid_pieces)
    
    def update_time_limit(self, limit):
        self.time_limit = limit

    def mcts(self):
        new_board = deepcopy(self.board)
        root = Node(new_board)
        start_time = time.time()
        # print("dice2")
        # print(root.state.dice_num)
        # print(root.state)
        while self.time_limit > time.time() - start_time:
            current_node = root
            # print("dice2.5")
            # print(current_node.state.dice_num)
            # print(root.state)
            # traverse
            while current_node.fully_expanded and not current_node.state.is_terminal():
                # print("dice4")
                # print(current_node.state.dice_num)
                # print(current_node.state)
                best_child = None
                best_reward = float('-inf')
                for child in current_node.children:
                    exploitation = child.reward / child.visits
                    actor_multiplier = 1 if current_node.state.actor() == 0 else -1
                    exploration = math.sqrt(2 * math.log(child.parent.visits) / child.visits) * actor_multiplier
                    if best_reward < exploitation + exploration:
                        best_reward = exploitation + exploration
                        best_child = child

                best_child.set_parent(current_node)
                current_node = best_child
                
                
            # expand
            current_reward = 0
            new_node = None
            if current_node.state.is_terminal():
                current_reward = current_node.state.payoff()
            elif len(current_node.state.get_actions()) == 0:
                new_state = current_node.state.successor(None)
                new_node = Node(new_state, current_node, None, True)
                current_node.children.append(new_node)
            else:
                # print("dice3")
                # print(current_node.state.dice_num)
                # print(current_node.state)
                for piece in current_node.state.get_actions():
                    new_state = current_node.state.successor(piece)
                    # print("cur state")
                    # print(current_node.state)
                    # print("new_state")
                    # print(new_state)
                    new_node = Node(new_state, current_node, piece, False)
                    if new_node not in current_node.children:
                        current_node.children.append(new_node)
                        fully_expanded = (len(current_node.state.get_actions()) == len(current_node.children))
                        current_node.set_fully_expanded(fully_expanded)
                        break
                # simulation
                # print("dicechild")
                # print(new_node.state.dice_num)
                # print(new_node.state)
                current_reward = self.simulate(new_node)
                # print(new_node.state.dice_num)
                # print(new_node.state)
            
            # backpropagate
            while new_node is not None:
                # print("update")
                new_node.reward += current_reward
                new_node.visits += 1
                new_node = new_node.parent
        
        best_reward = float('-inf')
        best_piece = None
        for child in root.children:
            if child.visits == 0:
                continue
            actor_multiplier = 1 if root.state.actor() == 0 else -1
            new_reward = (child.reward / child.visits) * actor_multiplier
            # print(new_reward, child.reward, child.visits)
            if new_reward >= best_reward:
                best_piece = child.piece
                best_reward = new_reward
        # print("best")
        # print(best_piece)
        # print(root.state.dice_num)
        return best_piece



    def simulate(self, node):
        board = deepcopy(node.state)
        # print("start s")
        while not board.is_terminal():
            piece = board.random_step()
            board.successor_simulate(piece)
        # print("end s")
        # print(board.winner())
        return board.payoff()
   
    def each_turn(self):
        self.roll_dice()
        if self.type == "heuristic":
            return self.heuristic()
        elif self.type == "random":
            return self.random()
        elif self.type == "mcts":
            piece =  self.mcts()
            if not piece:
                piece = self.heuristic()
            return piece
        
class Node:
    def __init__(self, state, parent=None, piece=None, fully_expanded=False):
        # state is the board, node.state = self.board
        self.state = state
        self.parent = parent
        self.piece = piece
        self.children = []
        self.visits = 0
        self.reward = 0
        self.fully_expanded = fully_expanded

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.state.turn == other.state.turn and self.state.board == other.state.board and self.state.dice_num == other.state.dice_num
        return False
    
    def __repr__(self):
        return str(self.state.board)
    
    def set_fully_expanded(self, boolean):
        self.fully_expanded = boolean
    
    def set_parent(self, parent):
        self.parent = parent
    

            