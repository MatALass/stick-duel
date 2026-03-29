from __future__ import annotations

import pygame

from stick_duel.constants import TITLE
from stick_duel.game import Game


def run() -> None:
    game = Game()
    pygame.display.set_caption(TITLE)
    game.run()
