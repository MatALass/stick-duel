from __future__ import annotations

import pygame

from stick_duel.asset_loader import AssetLoader
from stick_duel.config import SCREEN_HEIGHT, SCREEN_WIDTH, TARGET_FPS
from stick_duel.core.scene import SceneResult
from stick_duel.core.scene_manager import SceneManager
from stick_duel.scenes.controls_scene import ControlsScene
from stick_duel.scenes.game_scene import GameScene
from stick_duel.scenes.menu_scene import MenuScene
from stick_duel.scenes.player_setup_scene import PlayerSetupScene
from stick_duel.scenes.victory_scene import VictoryScene


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.assets = AssetLoader()
        self.scene_manager = SceneManager(self)
        self._register_scenes()
        self.assets.maybe_play_music("audio/music/theme.mp3")

    def _register_scenes(self) -> None:
        self.scene_manager.register("menu", MenuScene)
        self.scene_manager.register("controls", ControlsScene)
        self.scene_manager.register("setup", PlayerSetupScene)
        self.scene_manager.register("game", GameScene)
        self.scene_manager.register("victory", VictoryScene)
        self.scene_manager.go_to("menu")

    def apply_result(self, result):
        if result is None:
            return

        if result.quit_game:
            self.running = False
            return

        if result.next_scene is not None:
            self.scene_manager.go_to(result.next_scene, result.payload)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(TARGET_FPS) / 1000.0
            scene = self.scene_manager.current
            if scene is None:
                self.running = False
                continue

            for event in pygame.event.get():
                result = scene.handle_event(event)
                self.apply_result(result)
                if not self.running:
                    break

            if not self.running:
                break

            self.apply_result(scene.update(dt))
            scene.draw(self.screen)
            pygame.display.flip()

        self.assets.stop_music()
        pygame.quit()
