from player import Player
import random
import time
from collections import defaultdict
from copy import deepcopy
import math
import pdb

class AIPlayer(Player):
    def __init__(self, color, board, type):
        super().__init__(color, board, type)
        self.time_limit = 5
    
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

    def dice(self):
        return random.choice([1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 5])

    def mcts(self):
        new_board = deepcopy(self.board)
        root = Node(new_board)
        start_time = time.time()
        while self.time_limit > time.time() - start_time:
            current_node = root
            # traverse
            while current_node.fully_expanded and not current_node.state.is_terminal():
                best_child = None
                best_reward = float('-inf')
                cur_dice = self.dice()
                for child in current_node.children:
                    if child.state.dice_num == cur_dice:
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
                for piece in current_node.state.get_actions():
                    new_state = current_node.state.successor(piece)
                    new_node = Node(new_state, current_node, piece, False)
                    # pdb.set_trace()
                    if new_node not in current_node.children:
                        current_node.children.append(new_node)
                        fully_expanded = (len(current_node.state.get_actions()) * 5 == len(current_node.children))
                        current_node.set_fully_expanded(fully_expanded)
                        break
                # if random.random() < 0.2:
                # # random simulation
                #     current_reward = self.simulate(new_node)
                # else:
                # heuristic simulation
                current_reward = self.simulate_heuristic(new_node)
            
            # backpropagate
            while new_node is not None:
                # print("update")
                new_node.reward += current_reward
                new_node.visits += 1
                new_node = new_node.parent
        
        piece_dict = defaultdict(lambda: [0, 0, None])
        self.prep_dict(root, piece_dict)

        best_reward = float('-inf')
        best_piece = None
        # for child in root.children:
        #     if child.visits == 0:
        #         continue
        #     actor_multiplier = 1 if root.state.actor() == 0 else -1
        #     new_reward = (child.reward / child.visits) * actor_multiplier
        #     print(child.piece, new_reward, child.reward, child.visits, child.state.dice_num)
        #     if new_reward >= best_reward:
        #         best_piece = child.piece
        #         best_reward = new_reward
        for key, reward_visits in piece_dict.items():
            actor_multiplier = 1 if root.state.actor() == 0 else -1
            new_reward = (reward_visits[0] / reward_visits[1]) * actor_multiplier
            print(reward_visits[2], new_reward, reward_visits)
            if new_reward >= best_reward:
                best_piece = reward_visits[2]
                best_reward = new_reward

        print("best")
        print(best_piece)
        print(root.state.dice_num)
        print(root.state)
        return best_piece
    
    def prep_dict(self, root, piece_dict):
        for child in root.children:
            key = (child.piece.row, child.piece.col)
            # value: [reward, visits, piece]
            piece_dict[key][0] += child.reward
            piece_dict[key][1] += child.visits
            piece_dict[key][2] = child.piece



    def simulate(self, node):
        board = deepcopy(node.state)
        # print("start s")
        while not board.is_terminal():
            piece = board.random_step()
            board.successor_simulate(piece)
        # print("end s")
        # print(board.winner())
        return board.payoff()
    
    def simulate_heuristic(self, node):
        board = deepcopy(node.state)
        while not board.is_terminal():
            piece = self.select_heuristic(board)
            board.successor_simulate(piece)
        return board.payoff()


    def select_heuristic(self, board):
        valid_pieces = board.get_valid_pieces()
        if not valid_pieces:
            return None
        best_score = float('-inf')
        best_piece = None
        special_grid = [(2, 7), (2, 8), (2, 9)]
        for piece in valid_pieces:
            score = 0
            valid_move = board.get_valid_moves_mcts(piece)
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
    
    def each_turn(self):
        self.roll_dice()
        if self.type == "heuristic":
            return self.heuristic()
        elif self.type == "random":
            return self.random()
        elif self.type == "mcts":
            pieces =  self.board.get_actions()
            if len(pieces) == 0:
                return None
            elif len(pieces) == 1:
                return pieces[0]
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
            return self.state == other.state
        return False
    
    def __repr__(self):
        return str(self.state.board)
    
    def set_fully_expanded(self, boolean):
        self.fully_expanded = boolean
    
    def set_parent(self, parent):
        self.parent = parent
    

            