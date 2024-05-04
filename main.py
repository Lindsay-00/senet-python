import pygame
from constants import SCREEN_HEIGHTS, SCREEN_WIDTH, BOARD_ORIGIN_X, BOARD_ORIGIN_Y, WIDTH, HEIGHT, TILE_MARGIN, TILE_SIZE, DICE_MARGIN, DICE_HEIGHT, DICE_WIDTH, WHITE
from game import Game
import time

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHTS))

pygame.display.set_caption('Senet')
FPS = 60

import sys

def print_and_log(*args, file_name="1_mix_sim.log", **kwargs):
    # Open the log file in append mode
    with open(file_name, "a") as log_file:
        # Print to stdout
        print(*args, **kwargs)
        # Print to log file
        print(*args, file=log_file, **kwargs)



def get_position_from_mouse(pos):
    x, y = pos
    if x >= BOARD_ORIGIN_X and y >= BOARD_ORIGIN_Y and x <= BOARD_ORIGIN_X + TILE_SIZE + TILE_MARGIN + WIDTH and y <= BOARD_ORIGIN_Y + HEIGHT + TILE_SIZE + TILE_MARGIN:
        row = (y - BOARD_ORIGIN_Y) // (TILE_SIZE)
        col = (x - BOARD_ORIGIN_X) // (TILE_SIZE)
        if (row >= 0 and row <= 2 and col >= 0 and col <= 9) or (row == 2 and col == 10):
            return row, col
        

def check_new_game(mouse_x, mouse_y):
    reset_x = BOARD_ORIGIN_X + WIDTH - DICE_WIDTH - DICE_MARGIN
    reset_y = BOARD_ORIGIN_Y + HEIGHT + DICE_MARGIN
    if reset_x <= mouse_x <= reset_x + DICE_WIDTH and reset_y <= mouse_y <= reset_y + DICE_HEIGHT:
        return True
    return False


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    is_active = True
    count = 0
    black_win = 0
    white_win = 0
    start_time = time.time()
    while run:
        clock.tick(FPS)
        if game.get_winner() != None:
            # is_active = False
            count += 1
            if game.board.who_is_winner() == WHITE:
                white_win += 1
            else:
                black_win += 1
            game.reset()
            print_and_log(count)
            print_and_log("white " + game.white_player.type + str(white_win))
            print_and_log("black " + game.gray_player.type + str(black_win))
            print_and_log((black_win - white_win) / count)
            print_and_log("average time " + str((time.time() - start_time) / count))
            if count == 5000:
                is_active = False


        # if no moves can be made, change turn
        if is_active:
            if game.state == 'PIECE':
                if not game.if_valid_piece():
                    game.change_turn()
                    print("No valid moves.")

            if game.board.current_player.get_type() != "human":
                game.ai_move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouse_x, mouse_y = pos
                if check_new_game(mouse_x, mouse_y):
                    game.reset()
                    is_active = True
                if is_active:
                    if game.board.current_player.type == "human":
                        if game.state == 'ROLL' and game.check_roll(mouse_x, mouse_y):
                            game.roll_dice()
                        elif game.state == 'PIECE':
                            if get_position_from_mouse(pos):
                                row, col = get_position_from_mouse(pos)
                                game.select(row, col)




        game.update()
        pygame.display.update()
    pygame.quit()


main()
