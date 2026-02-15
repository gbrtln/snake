# Window
WINDOW_TITLE  = "Snake"
WINDOW_WIDTH  = 640
WINDOW_HEIGHT = 640

# Grid
CELL_SIZE  = 20
GRID_COLS  = WINDOW_WIDTH  // CELL_SIZE   # 32
GRID_ROWS  = WINDOW_HEIGHT // CELL_SIZE   # 32

# Frame rate
FPS_OUTER     = 60    # outer render loop
FPS_INITIAL   = 10.0  # snake moves per second at start
FPS_INCREMENT = 0.5   # added every 5 food eaten
FPS_MAX       = 25.0

# Scoring
POINTS_PER_FOOD = 10

# Colors (R, G, B)
COLOR_BG            = (15,  20,  15)
COLOR_GRID          = (22,  30,  22)
COLOR_SNAKE_HEAD    = (60, 220,  60)
COLOR_SNAKE_BODY    = (34, 160,  34)
COLOR_SNAKE_OUTLINE = (20,  90,  20)
COLOR_FOOD          = (220,  50,  50)
COLOR_FOOD_SHINE    = (255, 120, 120)
COLOR_HUD_BG        = (10,  14,  10)
COLOR_HUD_TEXT      = (200, 240, 200)
COLOR_ACCENT        = (80, 220,  80)
COLOR_DIM           = (100, 100, 100)
COLOR_WHITE         = (240, 240, 240)
COLOR_BLACK         = (10,  10,  10)

# Leaderboard
LEADERBOARD_FILE = "leaderboard.json"
LEADERBOARD_MAX  = 10
