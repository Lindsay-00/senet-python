import pygame
from board import Board
from constants import WHITE, BLACK, BLUE, BOARD_ORIGIN_X, BOARD_ORIGIN_Y, TILE_MARGIN, GRAY, TILE_SIZE, HEIGHT, DICE_MARGIN, DICE_HEIGHT, DICE_WIDTH, GOLD, SCREEN_WIDTH, WIDTH, FONT_NAME, CRIMSON
from playerfactory import PlayerFactory

class Game:
    def __init__(self, window):
        self._init()
        self.window = window
        

    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        self.draw_next_move()
        self.draw_turn_button()
        self.draw_finished_button()
        self.draw_ai_move()
        self.draw_new_game()
        pygame.display.update()

    def _init(self, white_type="heuristic", gray_type="mcts"):
        self.selected = None
        self.board = Board()
        self.valid_moves = None
        self.state = 'ROLL'
        self._factory = PlayerFactory()
        self.white_player = self._factory.create_player(WHITE, self.board, white_type)
        self.gray_player = self._factory.create_player(GRAY, self.board, gray_type)
        self.board.set_current_player(self.gray_player)
        self.ai_piece = None

    def reset(self):
        self._init()

    def change_state(self):
        if self.state == 'ROLL':
            self.state = 'PIECE'
        else:
            self.state = 'ROLL'


    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.valid_moves = None
                self.select(row, col)
        # else:
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.board.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves_mcts(piece)
            return True
        return False
    
    def if_valid_piece(self):
        if self.board.get_valid_pieces() == []:
            return False
        return True

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and (row, col) == self.valid_moves:
            self.board.move(self.selected, row, col)
            self.change_turn()
        else:
            return False
        return True
    
    def change_turn(self):
        self.valid_moves = None
        if self.board.turn == GRAY:
            self.board.turn = WHITE
            self.board.set_current_player(self.white_player)
        else:
            self.board.turn = GRAY
            self.board.set_current_player(self.gray_player)
        
        self.state = 'ROLL'
        # self.board.update_dice(0)

    def get_winner(self):
        return self.board.winner()
    
    def get_board(self):
        return self.board

    def roll_dice(self):
        # used only by human player
        self.board.roll_dice()
        self.ai_piece = None
        self.change_state()

    def check_roll(self, mouse_x, mouse_y):
        roll_button_x = BOARD_ORIGIN_X
        roll_button_y = BOARD_ORIGIN_Y + HEIGHT + DICE_MARGIN
        if roll_button_x <= mouse_x <= roll_button_x + DICE_WIDTH and roll_button_y <= mouse_y <= roll_button_y + DICE_HEIGHT:
            return True
        return False

    def draw_valid_moves(self, move):
        if move != None:
            row, col = move
            x = BOARD_ORIGIN_X + col * TILE_SIZE
            y = BOARD_ORIGIN_Y + row * TILE_SIZE
            pygame.draw.rect(
                    self.window,
                    BLUE,
                    (x, y, TILE_SIZE - TILE_MARGIN, TILE_SIZE - TILE_MARGIN),
                    3
                )
            if self.selected:
                row, col = self.selected.row, self.selected.col
                x = BOARD_ORIGIN_X + col * TILE_SIZE
                y = BOARD_ORIGIN_Y + row * TILE_SIZE
                pygame.draw.rect(
                        self.window,
                        BLUE,
                        (x, y, TILE_SIZE - TILE_MARGIN, TILE_SIZE - TILE_MARGIN),
                        3
                    )
                
    def draw_new_game(self):
        if self.get_winner():
            reset_x = BOARD_ORIGIN_X + WIDTH - DICE_WIDTH - DICE_MARGIN
            reset_y = BOARD_ORIGIN_Y + HEIGHT + DICE_MARGIN

            pygame.draw.rect(
                            self.window,
                            GOLD,
                            (reset_x, reset_y, DICE_WIDTH, DICE_HEIGHT),
                            5
                        )
            
    def draw_ai_move(self):
        if self.ai_piece:
            piece = self.ai_piece

            row, col = piece.row, piece.col
            x = BOARD_ORIGIN_X + col * TILE_SIZE
            y = BOARD_ORIGIN_Y + row * TILE_SIZE
            pygame.draw.rect(
                self.window,
                CRIMSON,
                (x, y, TILE_SIZE - TILE_MARGIN, TILE_SIZE - TILE_MARGIN),
                3
            )


    def draw_next_move(self):
        current_player = self.board.get_current_player()
        if current_player.type == "human":
            if self.state == 'ROLL':
                x = BOARD_ORIGIN_X
                y = BOARD_ORIGIN_Y + HEIGHT + DICE_MARGIN
                pygame.draw.rect(
                            self.window,
                            GOLD,
                            (x, y, DICE_WIDTH, DICE_HEIGHT),
                            5
                        )
            elif self.state == 'PIECE':
                pieces = self.board.get_valid_pieces()
                for piece in pieces:
                    row, col = piece.row, piece.col
                    x = BOARD_ORIGIN_X + col * TILE_SIZE
                    y = BOARD_ORIGIN_Y + row * TILE_SIZE
                    pygame.draw.rect(
                        self.window,
                        GOLD,
                        (x, y, TILE_SIZE - TILE_MARGIN, TILE_SIZE - TILE_MARGIN),
                        5
                    )



    def draw_turn_button(self):
        turn_x = SCREEN_WIDTH // 2 - DICE_WIDTH // 2
        turn_y = BOARD_ORIGIN_Y // 2 - DICE_MARGIN

        pygame.draw.rect(self.window, BLACK, (turn_x, turn_y, DICE_WIDTH, DICE_HEIGHT), 1)
        self.turn_text(turn_x, turn_y)

    def turn_text(self, turn_x, turn_y):
        pygame.font.init()
        font = pygame.font.Font(FONT_NAME, 30)
        if not self.get_winner():
            color = "Black"
            if self.board.turn == GRAY:
                color = "Black"
            else:
                color = "White"
            text = font.render(color + "'s Turn", True, BLACK)
        else:
            text = font.render(self.get_winner(), True, BLACK)

        text_rect = text.get_rect(center=(turn_x + DICE_WIDTH // 2, turn_y + DICE_HEIGHT // 2))
        self.window.blit(text, text_rect)

    def draw_finished_button(self):
        finished_x, finished_y = BOARD_ORIGIN_X + WIDTH - DICE_WIDTH - DICE_MARGIN, BOARD_ORIGIN_Y // 2 - DICE_HEIGHT

        pygame.draw.rect(self.window, BLACK, (finished_x, finished_y, DICE_WIDTH, DICE_HEIGHT * 2), 1)

        pygame.font.init()
        font = pygame.font.Font(FONT_NAME, 24)
        text = font.render(str(7 - self.board.gray_left) + " Black Finished", True, BLACK)
        text_rect = text.get_rect(center=(finished_x + DICE_WIDTH // 2, finished_y + DICE_HEIGHT // 2))
        self.window.blit(text, text_rect)
             
        text = font.render(str(7 - self.board.white_left) + " White Finished", True, BLACK)
        text_rect = text.get_rect(center=(finished_x + DICE_WIDTH // 2, BOARD_ORIGIN_Y // 2 + DICE_HEIGHT // 2))
        self.window.blit(text, text_rect)

    def ai_move(self):
        # current_player.ai_move()
        returned_piece = self.get_ai_piece()
        best_piece = None
        if returned_piece:
            best_piece = self.board.board[returned_piece.row][returned_piece.col]
        self.ai_piece = best_piece
        # print(best_piece, self.board.dice_num)
        if not best_piece:
            self.change_turn()
            # print(self.board.turn + "No valid moves.")
        else:
            move = self.board.get_valid_moves_mcts(best_piece)
            # print(type(move))
            # print(self.board.dice_num)
            new_row, new_col = move
            # print(new_row, new_col)
            self.ai_move_piece(best_piece, new_row, new_col)
        # print(self.board)

    def get_ai_piece(self):
        current_player = self.board.get_current_player()
        return current_player.each_turn()
    
    def ai_move_piece(self, piece, new_row, new_col):
        self.board.move(piece, new_row, new_col)
        self.change_turn()