import pygame
from constants import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE,
    COLOR_BG, COLOR_GRID,
    COLOR_SNAKE_HEAD, COLOR_SNAKE_BODY, COLOR_SNAKE_OUTLINE,
    COLOR_FOOD, COLOR_FOOD_SHINE,
    COLOR_HUD_BG, COLOR_HUD_TEXT,
    FPS_OUTER,
)


class Renderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self._load_fonts()

    def _load_fonts(self):
        self.font_huge   = pygame.font.SysFont("monospace", 72, bold=True)
        self.font_large  = pygame.font.SysFont("monospace", 36, bold=True)
        self.font_medium = pygame.font.SysFont("monospace", 24)
        self.font_small  = pygame.font.SysFont("monospace", 16)

    # ------------------------------------------------------------------
    # Background / grid
    # ------------------------------------------------------------------

    def draw_background(self):
        self.screen.fill(COLOR_BG)
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (WINDOW_WIDTH, y))

    # ------------------------------------------------------------------
    # Snake
    # ------------------------------------------------------------------

    def draw_snake(self, snake):
        for i, (col, row) in enumerate(snake.body):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            inner = rect.inflate(-2, -2)
            pygame.draw.rect(self.screen, COLOR_SNAKE_OUTLINE, rect, border_radius=4)
            pygame.draw.rect(self.screen, color, inner, border_radius=3)
        self._draw_eyes(snake)

    def _draw_eyes(self, snake):
        col, row = snake.head
        dx, dy   = snake.direction
        cx = col * CELL_SIZE + CELL_SIZE // 2
        cy = row * CELL_SIZE + CELL_SIZE // 2
        # Perpendicular vector for the two eyes
        perp_x, perp_y = -dy, dx
        eye_offset = CELL_SIZE // 4
        fwd_offset  = CELL_SIZE // 5
        for sign in (+1, -1):
            ex = cx + sign * perp_x * eye_offset + dx * fwd_offset
            ey = cy + sign * perp_y * eye_offset + dy * fwd_offset
            pygame.draw.circle(self.screen, (240, 240, 240), (int(ex), int(ey)), 3)
            pygame.draw.circle(self.screen, (10,  10,  10),  (int(ex), int(ey)), 1)

    # ------------------------------------------------------------------
    # Food
    # ------------------------------------------------------------------

    def draw_food(self, food):
        col, row = food.position
        cx = col * CELL_SIZE + CELL_SIZE // 2
        cy = row * CELL_SIZE + CELL_SIZE // 2
        r  = CELL_SIZE // 2 - 2
        pygame.draw.circle(self.screen, COLOR_FOOD,       (cx, cy), r)
        pygame.draw.circle(self.screen, COLOR_FOOD_SHINE, (cx - r // 3, cy - r // 3), max(r // 3, 2))

    # ------------------------------------------------------------------
    # HUD
    # ------------------------------------------------------------------

    def draw_hud(self, score: int, speed: float):
        hud_rect = pygame.Rect(0, 0, WINDOW_WIDTH, CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_HUD_BG, hud_rect)
        score_surf = self.font_small.render(f"SCORE  {score:>6}", True, COLOR_HUD_TEXT)
        speed_surf = self.font_small.render(f"SPEED  {speed:>4.1f}", True, COLOR_HUD_TEXT)
        self.screen.blit(score_surf, (8, 2))
        self.screen.blit(speed_surf, (WINDOW_WIDTH - speed_surf.get_width() - 8, 2))

    # ------------------------------------------------------------------
    # Overlay helper
    # ------------------------------------------------------------------

    def draw_overlay(self, lines):
        """Draw a semi-transparent dark panel and render centered text.

        lines: list of (text, font, color) tuples, rendered top-to-bottom.
        """
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))
        total_h = sum(font.get_height() + 8 for _, font, _ in lines)
        y = (WINDOW_HEIGHT - total_h) // 2
        for text, font, color in lines:
            surf = font.render(text, True, color)
            x = (WINDOW_WIDTH - surf.get_width()) // 2
            self.screen.blit(surf, (x, y))
            y += surf.get_height() + 8

    # ------------------------------------------------------------------
    # Loop helpers
    # ------------------------------------------------------------------

    def flip(self):
        pygame.display.flip()

    def tick(self):
        self.clock.tick(FPS_OUTER)
