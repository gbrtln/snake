import pygame
from constants import (
    FPS_OUTER,
    COLOR_ACCENT, COLOR_DIM, COLOR_HUD_TEXT, COLOR_WHITE,
)
from game import GameSession, UP, DOWN, LEFT, RIGHT


# ---------------------------------------------------------------------------
# Key → direction mapping
# ---------------------------------------------------------------------------
KEY_DIR = {
    pygame.K_UP:    UP,
    pygame.K_w:     UP,
    pygame.K_DOWN:  DOWN,
    pygame.K_s:     DOWN,
    pygame.K_LEFT:  LEFT,
    pygame.K_a:     LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_d:     RIGHT,
}

CONFIRM_KEYS = {pygame.K_SPACE, pygame.K_RETURN}


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------

class StateMachine:
    def __init__(self, renderer, leaderboard):
        self.renderer    = renderer
        self.leaderboard = leaderboard
        self.state       = StartState(self)

    def change(self, new_state):
        self.state = new_state

    def handle_event(self, event):
        self.state.handle_event(event)

    def update(self):
        self.state.update()

    def draw(self):
        self.state.draw(self.renderer)


# ---------------------------------------------------------------------------
# StartState
# ---------------------------------------------------------------------------

class StartState:
    def __init__(self, sm):
        self.sm     = sm
        self.frame  = 0

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in CONFIRM_KEYS:
            self.sm.change(PlayingState(self.sm))
        elif event.key == pygame.K_l:
            self.sm.change(LeaderboardState(self.sm, back_state_cls=StartState))

    def update(self):
        self.frame += 1

    def draw(self, r):
        r.draw_background()
        blink_color = COLOR_ACCENT if (self.frame // 30) % 2 == 0 else COLOR_DIM
        r.draw_overlay([
            ("SNAKE",              r.font_huge,   COLOR_ACCENT),
            ("PRESS SPACE TO PLAY", r.font_medium, blink_color),
            ("L  -  LEADERBOARD",  r.font_small,  COLOR_DIM),
        ])


# ---------------------------------------------------------------------------
# PlayingState
# ---------------------------------------------------------------------------

class PlayingState:
    def __init__(self, sm):
        self.sm      = sm
        self.session = GameSession()
        self._ticks  = 0          # frames since last game tick

    def _ticks_per_move(self):
        return FPS_OUTER / self.session.speed

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.sm.change(StartState(self.sm))
            return
        direction = KEY_DIR.get(event.key)
        if direction:
            self.session.snake.change_direction(direction)

    def update(self):
        self._ticks += 1
        if self._ticks >= self._ticks_per_move():
            self._ticks = 0
            self.session.update()
            if not self.session.alive:
                self.sm.change(GameOverState(self.sm, self.session))

    def draw(self, r):
        r.draw_background()
        r.draw_food(self.session.food)
        r.draw_snake(self.session.snake)
        r.draw_hud(self.session.score, self.session.speed)


# ---------------------------------------------------------------------------
# GameOverState
# ---------------------------------------------------------------------------

class GameOverState:
    def __init__(self, sm, session):
        self.sm            = sm
        self.session       = session
        self.score         = session.score
        self.is_high       = sm.leaderboard.is_high_score(self.score)
        self.name_entered  = not self.is_high   # skip name entry if not a high score
        self.name          = ""
        self.frame         = 0

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if not self.name_entered:
            # Name entry mode
            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key in CONFIRM_KEYS:
                if self.name.strip():
                    self.sm.leaderboard.add(self.name, self.score)
                    self.name_entered = True
            elif event.unicode and event.unicode.isprintable() and len(self.name) < 12:
                self.name += event.unicode.upper()
        else:
            # After name entered (or not a high score)
            if event.key in CONFIRM_KEYS:
                self.sm.change(PlayingState(self.sm))
            elif event.key == pygame.K_l:
                self.sm.change(LeaderboardState(self.sm, back_state_cls=StartState))

    def update(self):
        self.frame += 1

    def draw(self, r):
        # Draw the frozen game state underneath
        r.draw_background()
        r.draw_food(self.session.food)
        r.draw_snake(self.session.snake)
        r.draw_hud(self.score, self.session.speed)

        lines = [
            ("GAME OVER",          r.font_large,  (220, 50, 50)),
            (f"SCORE  {self.score}", r.font_medium, COLOR_HUD_TEXT),
        ]

        if self.is_high:
            lines.append(("NEW HIGH SCORE!", r.font_medium, COLOR_ACCENT))

        if not self.name_entered:
            cursor = "_" if (self.frame // 20) % 2 == 0 else " "
            lines.append(("ENTER YOUR NAME:", r.font_small, COLOR_HUD_TEXT))
            lines.append((f"{self.name}{cursor}", r.font_medium, COLOR_WHITE))
            lines.append(("ENTER to confirm", r.font_small, COLOR_DIM))
        else:
            lines.append(("SPACE - PLAY AGAIN", r.font_small, COLOR_HUD_TEXT))
            lines.append(("L     - LEADERBOARD", r.font_small, COLOR_DIM))

        r.draw_overlay(lines)


# ---------------------------------------------------------------------------
# LeaderboardState
# ---------------------------------------------------------------------------

class LeaderboardState:
    def __init__(self, sm, back_state_cls=None):
        self.sm             = sm
        self.back_state_cls = back_state_cls or StartState
        self.entries        = sm.leaderboard.top()

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in CONFIRM_KEYS or event.key == pygame.K_ESCAPE:
            self.sm.change(self.back_state_cls(self.sm))

    def update(self):
        pass

    def draw(self, r):
        r.draw_background()
        lines = [
            ("TOP  SCORES", r.font_large, COLOR_ACCENT),
        ]
        for i, entry in enumerate(self.entries):
            rank  = i + 1
            color = COLOR_ACCENT if rank == 1 else COLOR_HUD_TEXT
            name  = entry["name"][:12].ljust(12)
            score = str(entry["score"]).rjust(6)
            date  = entry["date"]
            line  = f"{rank:>2}. {name}  {score}  {date}"
            lines.append((line, r.font_small, color))

        if not self.entries:
            lines.append(("No scores yet. Play a game!", r.font_small, COLOR_DIM))

        lines.append(("", r.font_small, COLOR_DIM))  # spacer
        lines.append(("SPACE  -  BACK", r.font_small, COLOR_DIM))

        r.draw_overlay(lines)
