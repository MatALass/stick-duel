from __future__ import annotations

import pygame

from stick_duel.constants import (
    BG_BOTTOM,
    BG_TOP,
    BLUE,
    DARK_PANEL,
    HEIGHT,
    PLAYER_1_COLOR,
    PLAYER_2_COLOR,
    SOFT_TEXT,
    WHITE,
    WIDTH,
)
from stick_duel.core.scene import Scene, SceneResult
from stick_duel.ui.button import Button


class ControlsScene(Scene):
    def enter(self, payload: dict | None = None) -> None:
        _ = payload
        self.background = self.game.assets.optional_image("images/background/fonde.png", size=(WIDTH, HEIGHT), fill_color=BG_BOTTOM)
        self.title_font = self.game.assets.font(54, bold=True)
        self.body_font = self.game.assets.font(22)
        self.section_font = self.game.assets.font(34, bold=True)
        self.button_font = self.game.assets.font(24, bold=True)
        self.back_button = Button(pygame.Rect(60, 58, 180, 56), "Back", BLUE, (90, 150, 255), WHITE)
        self.controls_left = ["Q / D  •  Move", "Z  •  Jump", "S  •  Fast fall", "F  •  Melee", "G  •  Ranged"]
        self.controls_right = ["Left / Right  •  Move", "Up  •  Jump", "Down  •  Fast fall", "Enter  •  Melee", "Right Shift  •  Ranged"]

    def handle_event(self, event: pygame.event.Event) -> SceneResult | None:
        if event.type == pygame.QUIT:
            return SceneResult(quit_game=True)
        if self.back_button.clicked(event):
            return SceneResult(next_scene="menu")
        return None

    def _draw_panel(self, screen: pygame.Surface, rect: pygame.Rect, title: str, lines: list[str], edge: tuple[int, int, int]) -> None:
        shadow = rect.move(0, 6)
        pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=28)
        pygame.draw.rect(screen, DARK_PANEL, rect, border_radius=28)
        pygame.draw.rect(screen, edge, rect, width=4, border_radius=28)
        pygame.draw.rect(screen, (255, 255, 255, 15), rect.inflate(-10, -10), width=1, border_radius=22)
        screen.blit(self.section_font.render(title, True, WHITE), (rect.x + 34, rect.y + 30))
        for idx, line in enumerate(lines):
            text = self.body_font.render(line, True, WHITE)
            screen.blit(text, (rect.x + 34, rect.y + 100 + idx * 58))

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 20, 136))
        screen.blit(overlay, (0, 0))
        gradient = self.game.assets.build_vertical_gradient((WIDTH, HEIGHT), BG_TOP, BG_BOTTOM)
        gradient.set_alpha(70)
        screen.blit(gradient, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        self.back_button.draw(screen, self.button_font, mouse_pos)
        title = self.title_font.render("Controls", True, WHITE)
        subtitle = self.body_font.render("Optimized for one keyboard: left side for P1, arrows + right cluster for P2.", True, SOFT_TEXT)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 148)))

        self._draw_panel(screen, pygame.Rect(170, 220, 520, 420), "Player 1", self.controls_left, PLAYER_1_COLOR)
        self._draw_panel(screen, pygame.Rect(910, 220, 520, 420), "Player 2", self.controls_right, PLAYER_2_COLOR)

        footer = self.body_font.render("Esc pauses or resumes the match.", True, WHITE)
        screen.blit(footer, footer.get_rect(center=(WIDTH // 2, 760)))
