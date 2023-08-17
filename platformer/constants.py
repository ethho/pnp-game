GLOBAL_SCALE = 2
MAP_WIDTH = 30
MAP_HEIGHT = 20

# Constants used to scale our sprites from their original size
TILE_SCALING = 1 * GLOBAL_SCALE
# TILE_SCALING = 1 # Scale screen size without scaling the grid
CHARACTER_SCALING = TILE_SCALING
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 16
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
# GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING * GLOBAL_SCALE # Scale screen size without scaling the grid

# Tile map is 30 x 20 blocks of 16 sq pixels each
SCREEN_WIDTH = MAP_WIDTH * GRID_PIXEL_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * GRID_PIXEL_SIZE
SCREEN_TITLE = "Pook and Pook"

# Shooting Constants
SPRITE_SCALING_LASER = 0.8
SHOOT_SPEED = 15
BULLET_SPEED = 12
BULLET_DAMAGE = 25

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 6
GRAVITY = 1.
PLAYER_JUMP_SPEED = 20

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

PLAYER_START_X = 2
PLAYER_START_Y = 1

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_PLAYER2 = "Player2"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_BULLETS = "Bullets"

DEBUG = True