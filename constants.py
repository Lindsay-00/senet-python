import pygame

SCREEN_WIDTH, SCREEN_HEIGHTS = 1280, 560
WIDTH, HEIGHT = 1024, 320
ROWS, COLS = 3, 10
PADDING = 10
BOARD_ORIGIN_X = (SCREEN_WIDTH - WIDTH) // 2 + PADDING
BOARD_ORIGIN_Y = (SCREEN_HEIGHTS - HEIGHT) // 2 + PADDING
TILE_SIZE = (WIDTH - 2 * PADDING) // COLS
TILE_MARGIN = 5
SQUARE_SIZE = TILE_SIZE - TILE_MARGIN

# Dice button specifications
DICE_WIDTH = 200
DICE_HEIGHT = 40
DICE_MARGIN = 20

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BEIGE = (245, 245, 220)
GRAY = (169, 169, 169)
BLUE = (0, 71, 171)
LIGHT_BEIGE = (255, 248, 220)
PALE_SAND = (239, 235, 192)
SOFT_TERRACOTTA = (204, 153, 102)
LIGHT_GRAY = (211, 211, 211)
GOLD = (255, 223, 0)
CRIMSON = (220, 20, 60)

# Images
REBIRTH = pygame.image.load('assets/rebirth.png')
WATER = pygame.image.load('assets/water.png')
EYE = pygame.image.load('assets/eye.png')
THREE = pygame.image.load('assets/three.png')
BIRD = pygame.image.load('assets/bird.png')
AFTERLIFE = pygame.image.load('assets/afterlife.png')

FONT_NAME = pygame.font.match_font('timesnewroman')