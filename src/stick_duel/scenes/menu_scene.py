from __future__ import annotations

import pygame

from stick_duel.constants import BLACK, BLUE, GOLD, HEIGHT, LIGHT_BG, RED, WHITE, WIDTH
from stick_duel.core.scene import Scene, SceneResult
from stick_duel.ui.button import Button


class MenuScene(Scene):
    def enter(self, payload: dict | None = None) -> None:
        _ = payload
        self.background = self.game.assets.optional_image("images/background/fonde.png", size=(WIDTH, HEIGHT))
        self.logo = self.game.assets.optional_image("images/logo/stick_duel_logo.png", size=(760, 360))
        self.title_font = self.game.assets.font(64, bold=True)
        self.subtitle_font = self.game.assets.font(24)
        self.button_font = self.game.assets.font(28, bold=True)
        self.buttons = [
            Button(pygame.Rect(640, 430, 320, 72), "Play", BLUE, (74, 145, 255), WHITE),
            Button(pygame.Rect(640, 520, 320, 72), "Controls", RED, (255, 115, 128), WHITE),
            Button(pygame.Rect(640, 610, 320, 72), "Quit", GOLD, (255, 214, 94), BLACK),
        ]

    def handle_event(self, event: pygame.event.Event) -> SceneResult | None:
        if event.type == pygame.QUIT:
            return SceneResult(quit_game=True)
        if self.buttons[0].clicked(event):
            return SceneResult(next_scene="setup")
        if self.buttons[1].clicked(event):
            return SceneResult(next_scene="controls")
        if self.buttons[2].clicked(event):
            return SceneResult(quit_game=True)
        return None

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 20, 80))
        screen.blit(overlay, (0, 0))
        screen.blit(self.logo, self.logo.get_rect(center=(WIDTH // 2, 220)))

        subtitle = "A modular local 2D fighting game built with Python and Pygame"
        subtitle_surface = self.subtitle_font.render(subtitle, True, WHITE)
        screen.blit(subtitle_surface, subtitle_surface.get_rect(center=(WIDTH // 2, 360)))

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(screen, self.button_font, mouse_pos)

        footer = self.subtitle_font.render("Realised by Mathieu ALASSOEUR and Yanis CHEIKH", True, LIGHT_BG)
        screen.blit(footer, footer.get_rect(center=(WIDTH // 2, HEIGHT - 50)))
