# Snake

A classic Snake game built with Python and Pygame.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green?logo=python&logoColor=white)

## Features

- Smooth grid-based movement with arrow keys or WASD
- Progressive difficulty -- speed increases every 5 food eaten
- Persistent local leaderboard (top 10 scores)
- Name entry for high scores
- Retro green-on-dark aesthetic with rounded snake segments and animated eyes

## Getting Started

### Prerequisites

- Python 3.x
- Pygame

```bash
pip install pygame
```

### Running the Game

```bash
python main.py
```

## Controls

| Key | Action |
|---|---|
| Arrow keys / WASD | Move the snake |
| Space / Enter | Start game, confirm, play again |
| Escape | Return to title screen |
| L | View leaderboard |

## Project Structure

```
snake/
├── main.py          # Entry point and game loop
├── game.py          # Snake, Food, and GameSession logic
├── renderer.py      # Pygame drawing (grid, snake, food, HUD, overlays)
├── states.py        # State machine (Start, Playing, GameOver, Leaderboard)
├── leaderboard.py   # Score persistence (JSON)
├── constants.py     # All tunable settings (colors, grid size, speeds)
└── leaderboard.json # Saved scores (auto-generated)
```

## Configuration

All game parameters live in `constants.py` and can be tweaked freely:

| Setting | Default | Description |
|---|---|---|
| `WINDOW_WIDTH/HEIGHT` | 640 | Window size in pixels |
| `CELL_SIZE` | 20 | Size of each grid cell |
| `FPS_INITIAL` | 10.0 | Starting snake speed |
| `FPS_MAX` | 25.0 | Maximum snake speed |
| `POINTS_PER_FOOD` | 10 | Score per food eaten |

## License

This project is open source and available under the [MIT License](LICENSE).
