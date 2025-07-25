import pygame

from constants import UNICODE_CODING, SWITCHABLE, WHITE
from typing import TYPE_CHECKING

from moves import Move
from tile import rank7

if TYPE_CHECKING:
    from board import Board


class Drawer:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((100 * 8, 100 * 8))
        pygame.font.init()
        self.font = pygame.font.Font("./font/DejaVuSans.ttf", 80)
        pygame.init()

    def draw(self, board: "Board", promo_pos: int|None = None, pos_to_move: list[Move] = []) -> None:
        if promo_pos is not None:
            darker = 86
        else:
            darker = 0
        if board.color == WHITE:
            print("idk")
            flip = list(enumerate(range(8)))
        else:
            flip = list(enumerate(range(7, -1, -1)))
        self.screen.fill("black")
        for y, iy in flip:
            for x, ix in flip:
                pos = y * 8 + x
                if (ix + iy) % 2 == 0:
                    pygame.draw.rect(
                        self.screen, (238 - darker, 238 - darker, 210 - darker), (ix * 100, iy * 100, 100, 100)
                    )
                else:
                    pygame.draw.rect(
                        self.screen, (118 - darker, 150 - darker, 86 - darker), (ix * 100, iy * 100, 100, 100)
                    )
                self.screen.blit(
                    self.font.render(UNICODE_CODING[board[pos]], True, (0, 0, 0)),
                    (ix * 100 + 10, iy * 100 + 5),
                )
                for move in pos_to_move:
                    if move.to % 8 == x and move.to // 8 == y:
                        pygame.draw.circle(self.screen, (180, 180, 180), (ix * 100 + 50, iy * 100 + 50), 10)

        if promo_pos is not None:
            ix = promo_pos % 8
            for iy in range(len(SWITCHABLE)):
                if promo_pos in rank7:
                    if (ix + iy) % 2 == 0:
                        pygame.draw.rect(
                            self.screen, (238, 238, 210), (ix * 100, iy * 100, 100, 100)
                        )
                    else:
                        pygame.draw.rect(
                            self.screen, (118, 150, 86), (ix * 100, iy * 100, 100, 100)
                        )
                    self.screen.blit(
                        self.font.render(UNICODE_CODING[SWITCHABLE[iy] + board.color], True,(0, 0, 0)),
                        (ix * 100 + 10, iy * 100 + 5),
                    )
                else:
                    if (ix + iy) % 2 == 0:
                        pygame.draw.rect(
                            self.screen, (238, 238, 210), (ix * 100, (7 - iy) * 100, 100, 100)
                        )
                    else:
                        pygame.draw.rect(
                            self.screen, (118, 150, 86), (ix * 100, (7 - iy) * 100, 100, 100)
                        )
                    self.screen.blit(
                        self.font.render(UNICODE_CODING[SWITCHABLE[iy] + board.color], True,(0, 0, 0)),
                        (ix * 100 + 10, (7 - iy) * 100 + 5),
                    )
        pygame.display.flip()
