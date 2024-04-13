import random
from constants import ROWS, COLS

class Player:
    def __init__(self, color, board, type):
        self.color = color
        self.board = board
        self.grid = self.board.board
        self.selected = None
        self.type = type
        self.pieces = self.get_all_pieces()
        self.dice_num = self.get_dice_num()

    def get_all_pieces(self):
        pieces = []
        for row in self.grid:
            for piece in row:
                if piece != 0 and piece.color == self.color:
                    pieces.append(piece)
        return pieces
    
    def get_dice_num(self):
        return self.board.dice_num
    
    def roll_dice(self):
        # call roll dice function in board.py
        self.board.roll_dice()
    
    # def roll_dice(self):
    #     self.dice_num = random.randint(1, 5)
    #     self.board.update_dice(self.dice_num)
    #     return self.dice_num
    
    def get_valid_moves(self, piece):
        if not piece:
            print("this is not a valid piece.")
        cur_row, cur_col = piece.row, piece.col
        new_position = self.calculate_new_position(cur_row, cur_col)
        if not new_position:
            return None
        new_row, new_col = new_position

        # Check if reaches the end
        if new_col == 10:
            return (new_row, new_col)

        new_color = self.check_color(new_row, new_col)

        # Check for swaps with pieces of the same color
        if new_color == piece.color:
            return None

        # Check for moves to special grids
        if (new_row, new_col) in ((1, 5), (2, 5), (2, 6), (2, 7), (2, 8)) and new_color != 0:
            return None

        # Additional rules for moves in the first row
        if cur_row == 2:
            if new_col < 5:
                return (new_row, new_col)
            elif cur_col < 5 and new_col == 5:
                return (new_row, new_col)
            elif cur_col == 5:
                return (new_row, new_col)
            else:
                return None

        return (new_row, new_col)

    def calculate_new_position(self, cur_row, cur_col):
        if cur_row == 2:
            if cur_col + self.board.dice_num <= 10:
                return cur_row, cur_col + self.board.dice_num
            else:
                return None
        elif cur_row == 0:
            if cur_col + self.board.dice_num <= 9:
                return cur_row, cur_col + self.board.dice_num
            else:
                return cur_row + 1, 9 - (cur_col + self.board.dice_num - 9) + 1
        else:
            if cur_col - self.board.dice_num >= 0:
                return cur_row, cur_col - self.board.dice_num
            else:
                return cur_row + 1, self.board.dice_num - cur_col - 1


    # def get_valid_pieces(self):
    #     pieces = []
    #     for x in range(ROWS):
    #         for y in range(COLS):
    #             if self.grid[x][y] != 0 and self.grid[x][y].color == self.color:
    #                 if self.get_valid_moves(self.grid[x][y]):
    #                     pieces.append(self.grid[x][y])

    #     return pieces
    
    def check_color(self, row, col):
        if self.grid[row][col] != 0:
            return self.grid[row][col].color
        else:
            return 0
    
    def get_type(self):
        return self.type

    def ai_move(self):
        print("this is ai")
    
            