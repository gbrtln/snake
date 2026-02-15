import sys
import pygame
from renderer    import Renderer
from leaderboard import Leaderboard
from states      import StateMachine


def main():
    renderer    = Renderer()
    leaderboard = Leaderboard()
    sm          = StateMachine(renderer, leaderboard)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                sm.handle_event(event)

        sm.update()
        sm.draw()
        renderer.flip()
        renderer.tick()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
