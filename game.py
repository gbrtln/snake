import random
from constants import (
    GRID_COLS, GRID_ROWS,
    FPS_INITIAL, FPS_INCREMENT, FPS_MAX,
    POINTS_PER_FOOD,
)

# Directions as (dx, dy)
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)

OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


class Snake:
    def __init__(self):
        cx, cy = GRID_COLS // 2, GRID_ROWS // 2
        self.body      = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self.next_dir  = RIGHT
        self._grew     = False

    @property
    def head(self):
        return self.body[0]

    def change_direction(self, new_dir):
        if new_dir != OPPOSITE.get(self.direction):
            self.next_dir = new_dir

    def move(self):
        self.direction = self.next_dir
        dx, dy = self.direction
        hx, hy = self.head
        new_head = (hx + dx, hy + dy)
        self.body.insert(0, new_head)
        if not self._grew:
            self.body.pop()
        self._grew = False

    def grow(self):
        self._grew = True

    def is_wall_collision(self):
        hx, hy = self.head
        return not (0 <= hx < GRID_COLS and 0 <= hy < GRID_ROWS)

    def is_self_collision(self):
        return self.head in self.body[1:]


class Food:
    def __init__(self, snake_body):
        self.position = self._random_pos(snake_body)

    def _random_pos(self, occupied):
        occupied_set = set(occupied)
        all_cells = [(c, r) for c in range(GRID_COLS) for r in range(GRID_ROWS)]
        free = [cell for cell in all_cells if cell not in occupied_set]
        return random.choice(free) if free else (0, 0)

    def respawn(self, snake_body):
        self.position = self._random_pos(snake_body)


class GameSession:
    def __init__(self):
        self.snake      = Snake()
        self.food       = Food(self.snake.body)
        self.score      = 0
        self.food_count = 0
        self.speed      = FPS_INITIAL
        self.alive      = True

    def update(self):
        """Advance one game tick. Returns True if still alive."""
        self.snake.move()

        if self.snake.is_wall_collision() or self.snake.is_self_collision():
            self.alive = False
            return False

        if self.snake.head == self.food.position:
            self.snake.grow()
            self.food.respawn(self.snake.body)
            self.score      += POINTS_PER_FOOD
            self.food_count += 1
            if self.food_count % 5 == 0:
                self.speed = min(self.speed + FPS_INCREMENT, FPS_MAX)

        return True
