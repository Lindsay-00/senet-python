# board.py
import pygame
import random
from constants import BLACK, ROWS, COLS, WHITE, BOARD_ORIGIN_X, BOARD_ORIGIN_Y, TILE_SIZE, TILE_MARGIN, PALE_SAND, SOFT_TERRACOTTA, GRAY, REBIRTH, SQUARE_SIZE, WATER, THREE, EYE, BIRD, LIGHT_GRAY, DICE_WIDTH, DICE_HEIGHT, DICE_MARGIN, HEIGHT, WIDTH, AFTERLIFE, FONT_NAME
from piece import Piece
from copy import deepcopy

PIECE_NUM = 7

class Board:
    def __init__(self, current_player=None):
        self.board = [[0 for _ in range(10)] for _ in range(3)]
        self.white_left = PIECE_NUM
        self.gray_left = PIECE_NUM
        self.dice_num = 0
        self.turn = GRAY
        self.current_player = current_player
        self.create_pieces()


    def set_current_player(self, player):
        self.current_player = player

    def get_current_player(self):
        return self.current_player
    
    def change_turn(self):
        if self.turn == GRAY:
            self.turn = WHITE
            self.set_current_player(self.white_player)
        else:
            self.board.turn = GRAY
            self.board.set_current_player(self.gray_player)
        
        self.state = 'ROLL'
        self.board.update_dice(0)
        
    def draw_board(self, window):
        window.fill(WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                # Calculate tile coordinates
                x = BOARD_ORIGIN_X + col * TILE_SIZE
                y = BOARD_ORIGIN_Y + row * TILE_SIZE
                
                # Alternate tile colors
                if (row + col) % 2 == 0:
                    tile_color = PALE_SAND
                else:
                    tile_color = SOFT_TERRACOTTA

                # Draw tile background
                pygame.draw.rect(
                    window,
                    tile_color,
                    (x, y, TILE_SIZE - TILE_MARGIN, TILE_SIZE - TILE_MARGIN)
                )

                # Draw tile border
                pygame.draw.rect(
                    window,
                    BLACK,
                    (x, y, TILE_SIZE - TILE_MARGIN, TILE_SIZE - TILE_MARGIN),
                    1
                )

        # images
        # rebirth
        self.add_image(REBIRTH, 1, 5, window)
        # water
        self.add_image(WATER, 2, 6, window)
        # eye
        self.add_image(EYE, 2, 8, window)
        # three
        self.add_image(THREE, 2, 7, window)
        # bird 
        self.add_image(BIRD, 2, 5, window)
        # afterlife
        self.add_image(AFTERLIFE, 2, 10, window)

    def add_image(self, image, row, col, window):
        new_size = (SQUARE_SIZE, SQUARE_SIZE)
        scaled_sign = pygame.transform.scale(image, new_size)
        image_center_x = BOARD_ORIGIN_X + SQUARE_SIZE * col + TILE_MARGIN * col
        image_center_y = BOARD_ORIGIN_Y + SQUARE_SIZE * row + TILE_MARGIN * row
        window.blit(scaled_sign, (image_center_x, image_center_y))
    
    # for 7 pieces
    def create_pieces(self):
        for col in range(COLS):
            if col % 2 == 0:
                self.board[0][col] = Piece(0, col, WHITE)
            else:
                self.board[0][col] = Piece(0, col, GRAY)
        for col in range(9, 5, -1):
            if col % 2 == 1:
                self.board[1][col] = Piece(1, col, WHITE)
            else:
                self.board[1][col] = Piece(1, col, GRAY)

    def draw_dice_button(self, window):
        # Calculate button positions
        roll_button_x = BOARD_ORIGIN_X
        roll_button_y = BOARD_ORIGIN_Y + HEIGHT + DICE_MARGIN

        # Draw the roll dice button
        pygame.draw.rect(window, LIGHT_GRAY, (roll_button_x, roll_button_y, DICE_WIDTH, DICE_HEIGHT))
        pygame.draw.rect(window, BLACK, (roll_button_x, roll_button_y, DICE_WIDTH, DICE_HEIGHT), 1)

        # Draw the text on the button
        pygame.font.init()
        font = pygame.font.Font(FONT_NAME, 30)
        text = font.render('Roll Dice', True, BLACK)
        text_rect = text.get_rect(center=(roll_button_x + DICE_WIDTH // 2, roll_button_y + DICE_HEIGHT // 2))
        window.blit(text, text_rect)

    def draw_reset_button(self, window):
        reset_x = BOARD_ORIGIN_X + WIDTH - DICE_WIDTH - DICE_MARGIN
        reset_y = BOARD_ORIGIN_Y + HEIGHT + DICE_MARGIN

        pygame.draw.rect(window, LIGHT_GRAY, (reset_x, reset_y, DICE_WIDTH, DICE_HEIGHT))
        pygame.draw.rect(window, BLACK, (reset_x, reset_y, DICE_WIDTH, DICE_HEIGHT), 1)

        pygame.font.init()
        font = pygame.font.Font(FONT_NAME, 30)
        text = font.render('New Game', True, BLACK)
        text_rect = text.get_rect(center=(reset_x + DICE_WIDTH // 2, reset_y + DICE_HEIGHT // 2))
        window.blit(text, text_rect)

    def draw(self, window):
        self.draw_board(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)
        self.draw_dice_button(window)
        self.draw_reset_button(window)
    
        self.print_dice_result(self.dice_num, window)

    # given a piece, new row and new col; after checking if the piece can move
    def move(self, piece, row, col):
        # reaches (2, 10)
        if row == 2 and col == 10:
            self.remove(piece)
        else:
        # if reaches water
            if self.check_relocate(row, col):
                self.move_rebirth(piece)
            else:
                piece_new = self.board[row][col]
                cur_row, cur_col = piece.row, piece.col
                self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
                piece.move(row, col)
                if piece_new != 0:
                    piece_new.move(cur_row, cur_col)

    def check_relocate(self, row, col):
        if row == 2 and col == 6:
            return True
        return False
    
    def move_rebirth(self, piece):
        for y in range(5, 10):
            if self.board[1][y] == 0:
                self.move(piece, 1, y)
                return
        for y in range(9, -1, -1):
            if self.board[0][y] == 0:
                self.move(piece, 0, y)

    # get piece from a grid
    def get_piece(self, row, col):
        if row >= 0 and row <= 2 and col >= 0 and col <= 9:
            return self.board[row][col]
        elif row == 2 and col == 10:
            return 0
    
    # when a piece reaches (2, 10)
    def remove(self, piece):
        self.board[piece.row][piece.col] = 0
        piece.move(2, 10)
        if piece.color == GRAY:
            self.gray_left -= 1
        else:
            self.white_left -= 1

    def winner(self):
        if self.white_left <= 0:
            return ("White Wins!")
        elif self.gray_left <= 0:
            return ("Black Wins!")

        return None
    
    def is_terminal(self):
        if self.white_left <= 0 or self.gray_left <= 0:
            return True
        
        return False
    
    def who_is_winner(self):
        if self.white_left <= 0:
            return WHITE
        elif self.gray_left <= 0:
            return GRAY

        return None
    
    
    def update_dice(self, num):
        self.dice_num = num

    def print_dice_result(self, num, window):
        pygame.font.init()
        font = pygame.font.Font(FONT_NAME, 30)
        if num > 0:
            result_text = font.render("Rolled a " + str(num), True, BLACK)
            result_rect = result_text.get_rect(center=(BOARD_ORIGIN_X + DICE_WIDTH * 2 - DICE_MARGIN * 5, BOARD_ORIGIN_Y + HEIGHT + DICE_HEIGHT))
            window.blit(result_text, result_rect)
        else:
            result_text = font.render("Aleam nunc iacta!", True, BLACK)
            result_rect = result_text.get_rect(center=(BOARD_ORIGIN_X + DICE_WIDTH * 2 - DICE_MARGIN * 3, BOARD_ORIGIN_Y + HEIGHT + DICE_HEIGHT))
            window.blit(result_text, result_rect)

    def get_pieces_by_color(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    # for mcts
    # get valid pieces by color (self.turn)
    def get_actions(self):
        pieces = self.get_pieces_by_color(self.turn)
        valid_pieces = []
        for piece in pieces:
            if self.get_valid_moves_mcts(piece):
                valid_pieces.append(piece)
        return valid_pieces


    def successor(self, piece):
        new_copy = deepcopy(self)
        copied_piece = None
        if piece:
            copied_piece = new_copy.board[piece.row][piece.col]
        move = new_copy.get_valid_moves_mcts(copied_piece)
        if move:
            new_row, new_col = move
            new_copy.move(copied_piece, new_row, new_col)
    
        # prepare for the next round
        new_copy.change_turn_mcts()
        new_copy.roll_dice()
        return new_copy
    
    def successor_simulate(self, piece):
        move = self.get_valid_moves_mcts(piece)
        if move:
            new_row, new_col = move
            self.move(piece, new_row, new_col)
    
        # prepare for the next round
        self.change_turn_mcts()
        self.roll_dice()

    def random_step(self):
        valid_pieces = self.get_valid_pieces()
        if not valid_pieces:
            return None
        return random.choice(valid_pieces)

    
    def get_valid_pieces(self):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == self.turn:
                    if self.get_valid_moves_mcts(piece):
                        pieces.append(piece)

        return pieces

    # 1: 4/16, 2: 6/16 3: 4/16 4: 1/16 5:1/16
    def roll_dice(self):
        roll = random.randint(1, 16)

        # Map the roll to the dice result based on the given probabilities
        if roll == 1:
            dice_num = 5
        elif 2 <= roll <= 5:
            dice_num = 1
        elif 6 <= roll <= 11:
            dice_num = 2
        elif 12 <= roll <= 15:
            dice_num = 3
        else:
            dice_num = 4
        self.update_dice(dice_num)

    # def roll_dice(self):
    #     dice_num = random.randint(1, 5)
    #     self.update_dice(dice_num)

    def change_turn_mcts(self):
        if self.turn == GRAY:
            self.turn = WHITE
        else:
            self.turn = GRAY

    def payoff(self):
        winner = self.who_is_winner()
        if winner:
            return 1 if self.current_player.color == winner else -1
        print("error")
    
    def actor(self):
        if self.turn == self.current_player.color:
            return 0
        else: 
            return 1
        
    def get_valid_moves_mcts(self, piece):
        if not piece:
            # print("this is not a valid piece.")
            return None
        # print(piece)
        cur_row, cur_col = piece.row, piece.col
        new_position = self.calculate_new_position_mcts(cur_row, cur_col)
        # print(new_position)
        if not new_position:
            # print("no new position")
            return None
        new_row, new_col = new_position

        # Check if reaches the end
        if new_col == 10:
            return (new_row, new_col)

        new_color = self.check_color_mcts(new_row, new_col)

        # three or more other color pieces in a row; cannot swap or jump over
        if self.check_three_in_row(piece, new_row, new_col):
            # print("three in row")
            return None

        # two other color pieces in a row; cannot swap
        if self.check_two_in_row(piece, new_row, new_col):
            # print("two in row")
            return None
        
        # Check for swaps with pieces of the same color
        if new_color == piece.color:
            # print("piece with same color in square")
            return None

        # Check for moves to special grids
        if (new_row, new_col) in ((1, 5), (2, 5), (2, 6), (2, 7), (2, 8)) and new_color != 0:
            # print("special square occupied")
            return None

        # Additional rules for moves in the 3rd row
        if cur_row == 2:
            if new_col < 5:
                return (new_row, new_col)
            elif cur_col < 5 and new_col == 5:
                return (new_row, new_col)
            elif cur_col == 5:
                return (new_row, new_col)
            else:
                # print("rules for 2 row")
                if piece.col != 9:
                    return None

        return (new_row, new_col)
    
    def check_two_in_row(self, piece, new_row, new_col):
        left_col = new_col - 1
        right_col = new_col + 1
        color = self.check_color_mcts(new_row, new_col)
        if color == 0 or color == piece.color:
            return False
        if 0 <= left_col and self.check_color_mcts(new_row, left_col) == color:
            return True
        if right_col <= 9 and self.check_color_mcts(new_row, right_col) == color:
            return True
        return False

    # three or more other color pieces in a row; cannot swap or jump over
    # only when dice_num is 3 or 4 or 5 matters
    def check_three_in_row(self, piece, new_row, new_col):
        if self.dice_num < 3:
            return False
        # if change row
        if piece.row != new_row:
            # 0 row to 1 row
            col = piece.col
            if piece.row == 0:
                count = 0
                while col <= 9:
                    color = self.check_color_mcts(piece.row, col)
                    if color != piece.color and color != 0:
                        count += 1
                        if count == 3:
                            return True
                    else:
                        count = 0
                    col += 1
                count = 0
                for col in range(9, new_col - 3, -1):
                    color = self.check_color_mcts(piece.row + 1, col)
                    if color != piece.color and color != 0:
                        count += 1
                        if count == 3:
                            return True
                    else:
                        count = 0
            # 1 row to 2 row
            else:
                count = 0
                while col >= 0:
                    color = self.check_color_mcts(piece.row, col)
                    if color != piece.color and color != 0:
                        count += 1
                        if count == 3:
                            return True
                    else:
                        count = 0
                    col -= 1
                count = 0
                for col in range(0, new_col + 3):
                    color = self.check_color_mcts(piece.row + 1, col)
                    if color != piece.color and color != 0:
                        count += 1
                        if count == 3:
                            return True
                    else:
                        count = 0

        else:
            if piece.col <= new_col:
                if new_col + 3 > 10:
                    new_col = 10
                else:
                    new_col += 3
                start_col, end_col = piece.col + 1, new_col
            else:
                if new_col - 2 < 0:
                    new_col = 0
                else:
                    new_col -= 2
                start_col, end_col = new_col, piece.col
            count = 0
            for cur_col in range(start_col, end_col):
                color = self.check_color_mcts(piece.row, cur_col)
                if color != piece.color and color != 0:
                    count += 1
                    if count >= 3:
                        return True
                else:
                    count = 0
        return False

    def calculate_new_position_mcts(self, cur_row, cur_col):
        if cur_row == 2:
            if cur_col == 9 and cur_col + self.dice_num > 10: # 9 - (9 + 2 - 11)
                new_col = 11 - self.dice_num
                return cur_row, new_col
            elif cur_col + self.dice_num <= 10:
                return cur_row, cur_col + self.dice_num
            else:
                return None
        elif cur_row == 0:
            if cur_col + self.dice_num <= 9:
                return cur_row, cur_col + self.dice_num
            else:
                return cur_row + 1, 9 - (cur_col + self.dice_num - 9) + 1
        else:
            if cur_col - self.dice_num >= 0:
                return cur_row, cur_col - self.dice_num
            else:
                return cur_row + 1, self.dice_num - cur_col - 1
            
    def check_color_mcts(self, row, col):
        if self.board[row][col] != 0:
            return self.board[row][col].color
        else:
            return 0
        
    def board_to_tuple(self):
        return tuple(tuple(inner_list) for inner_list in self.board)
        
    def __repr__(self):
        return str(self.board)
    
    def same_board(self, other_board):
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] != other_board[i][j]:
                    return False
        return True

    
    def __eq__(self, other):
        if isinstance(other, Board):
            return self.turn == other.turn and self.dice_num == other.dice_num and self.same_board(other.board)
            # return self.turn == other.turn and self.same_board(other.board)
        return False


