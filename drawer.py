import pygame

from constants import UNICODE_CODING


class Drawer:
    def __init__(self, mode) -> None:
        self.mode = mode
        if self.mode != "Lukas":
            pass
        self.screen = pygame.display.set_mode((100 * 8, 100 * 8))
        pygame.font.init()
        self.font = pygame.font.Font("./font/DejaVuSans.ttf", 80)  # segoeuisymbol
        pygame.init()

    def draw(self, board) -> None:
        if self.mode == "Lukas":
            self.screen.fill("black")
            for y in range(8):
                for x in range(8):
                    pos = y * 8 + x
                    if (x + y) % 2 == 0:
                        pygame.draw.rect(
                            self.screen, (118, 150, 86), (x * 100, y * 100, 100, 100)
                        )
                    else:
                        pygame.draw.rect(
                            self.screen, (238, 238, 210), (x * 100, y * 100, 100, 100)
                        )
                    self.screen.blit(
                        self.font.render(UNICODE_CODING[board[pos]], True, (0, 0, 0)),
                        (x * 100 + 10, y * 100 + 5),
                    )
            pygame.display.flip()
        else:
            print(board)
