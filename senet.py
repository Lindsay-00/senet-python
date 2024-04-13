# main.py
import pygame
from board import Board

# Initialize Pygame
pygame.init()

# Define the screen dimensions and board properties
screen_width, screen_height = 1024, 560
board_width, board_height = 1024, 320
border_padding = 10
board_origin_x = (screen_width - board_width) // 2 + border_padding
board_origin_y = (screen_height - board_height) // 2 + border_padding

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Senet Board Game')

# Define colors
GRAY = (128, 128, 128)

# Board specifications
board_rows = 3
board_columns = 10
board = Board(screen, board_origin_x, board_origin_y, board_width, board_height, board_rows, board_columns, border_padding)

# Initialize clock
clock = pygame.time.Clock()

# Main game loop
running = True
dice_roll_result = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if a player button was clicked
            player_clicked = board.check_button_click(event.pos)
            if player_clicked == 'player1':
                print("Player 1 button clicked")
                # Handle player 1 button click
            elif player_clicked == 'player2':
                print("Player 2 button clicked")
                # Handle player 2 button click

            mouse_x, mouse_y = event.pos
            dice_roll_result =  board.dice_clicked(mouse_x, mouse_y, dice_roll_result)


    # Fill the screen
    screen.fill(GRAY)

    # Draw the board and buttons
    board.draw_board()
    board.draw_player_buttons()
    board.draw_dice_button()
    board.print_dice_result(dice_roll_result)


    # Update the display
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Quit the game
pygame.quit()



