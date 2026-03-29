from __future__ import annotations

import pygame

from stick_duel.constants import (
    BG_BOTTOM,
    BLACK,
    BLUE,
    GOLD,
    HEIGHT,
    RED,
    SOFT_TEXT,
    WHITE,
    WIDTH,
)
from stick_duel.core.scene import Scene, SceneResult
from stick_duel.ui.button import Button


class VictoryScene(Scene):
    def enter(self, payload: dict | None = None) -> None:
        payload = payload or {}
        self.winner_name = payload.get("winner_name", "Unknown")
        self.winner_fighter = payload.get("winner_fighter", "Fighter")
        self.background = self.game.assets.optional_image("images/background/fonde.png", size=(WIDTH, HEIGHT), fill_color=BG_BOTTOM)
        self.title_font = self.game.assets.font(68, bold=True)
        self.subtitle_font = self.game.assets.font(28)
        self.button_font = self.game.assets.font(26, bold=True)
        self.play_again = Button(pygame.Rect(560, 560, 220, 68), "Play Again", BLUE, (90, 150, 255), WHITE)
        self.main_menu = Button(pygame.Rect(820, 560, 220, 68), "Main Menu", RED, (255, 115, 128), WHITE)
        self.quit_button = Button(pygame.Rect(690, 650, 220, 68), "Quit", GOLD, (255, 214, 94), BLACK)

    def handle_event(self, event: pygame.event.Event) -> SceneResult | None:
        if event.type == pygame.QUIT:
            return SceneResult(quit_game=True)
        if self.play_again.clicked(event):
            return SceneResult(next_scene="setup")
        if self.main_menu.clicked(event):
            return SceneResult(next_scene="menu")
        if self.quit_button.clicked(event):
            return SceneResult(quit_game=True)
        return None

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        title = self.title_font.render(f"{self.winner_name} wins", True, WHITE)
        subtitle = self.subtitle_font.render(f"Winning fighter: {self.winner_fighter}", True, SOFT_TEXT)
        hint = self.subtitle_font.render("Ready for another round?", True, SOFT_TEXT)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 260)))
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 340)))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 390)))
        mouse_pos = pygame.mouse.get_pos()
        self.play_again.draw(screen, self.button_font, mouse_pos)
        self.main_menu.draw(screen, self.button_font, mouse_pos)
        self.quit_button.draw(screen, self.button_font, mouse_pos)
