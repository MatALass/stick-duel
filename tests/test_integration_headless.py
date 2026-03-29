from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from stick_duel.core.scene import SceneResult
from stick_duel.game import Game


def test_game_apply_result_switches_scene_without_crashing() -> None:
    game = Game()

    assert game.scene_manager.current_name == "menu"

    game.apply_result(SceneResult(next_scene="setup"))
    assert game.scene_manager.current_name == "setup"

    game.apply_result(SceneResult(quit_game=True))
    assert game.running is False

    pygame.quit()
