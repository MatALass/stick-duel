import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from stick_duel.asset_loader import AssetLoader
from stick_duel.core.scene_manager import SceneManager
from stick_duel.scenes.menu_scene import MenuScene
from stick_duel.scenes.player_setup_scene import PlayerSetupScene


class DummyGame:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.assets = AssetLoader()


def test_scene_manager_switches_scene() -> None:
    game = DummyGame()
    manager = SceneManager(game)
    manager.register("menu", MenuScene)
    manager.register("setup", PlayerSetupScene)
    manager.go_to("menu")
    assert isinstance(manager.current, MenuScene)
    manager.go_to("setup")
    assert isinstance(manager.current, PlayerSetupScene)
    pygame.quit()
