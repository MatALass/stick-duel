from __future__ import annotations

import pygame

from stick_duel.constants import BG_BOTTOM, BG_TOP, BLACK, BLUE, DARK_PANEL, GOLD, HEIGHT, PLAYER_1_COLOR, PLAYER_2_COLOR, RED, SOFT_TEXT, WHITE, WIDTH
from stick_duel.core.scene import Scene, SceneResult
from stick_duel.entities.fighter import FighterDefinition
from stick_duel.entities.stats import FighterStats
from stick_duel.ui.button import Button
from stick_duel.ui.input_box import InputBox


class PlayerSetupScene(Scene):
    def enter(self, payload: dict | None = None) -> None:
        _ = payload
        self.background = self.game.assets.optional_image("images/background/fonde.png", size=(WIDTH, HEIGHT), fill_color=BG_BOTTOM)
        self.title_font = self.game.assets.font(54, bold=True)
        self.text_font = self.game.assets.font(21)
        self.small_font = self.game.assets.font(18)
        self.button_font = self.game.assets.font(24, bold=True)
        self.name_font = self.game.assets.font(24, bold=True)
        self.header_font = self.game.assets.font(32, bold=True)
        self.label_font = self.game.assets.font(20)

        self.fighters = {
            "swordsman": FighterDefinition(
                key="swordsman",
                display_name="Swordsman",
                description="Close-range pressure and stronger melee knockback.",
                stats=FighterStats(
                    max_health=100,
                    move_speed=8.0,
                    jump_strength=16.8,
                    melee_damage=18,
                    melee_range=(90, 80),
                    melee_knockback=(9.5, 10.5),
                    melee_cooldown=0.38,
                    projectile_damage=0,
                    projectile_speed=0.0,
                    projectile_cooldown=999.0,
                    projectile_knockback=(0.0, 0.0),
                    color=(230, 236, 240),
                    accent_color=(255, 187, 70),
                ),
                can_shoot=False,
            ),
            "archer": FighterDefinition(
                key="archer",
                display_name="Archer",
                description="Lighter melee but better spacing with projectiles.",
                stats=FighterStats(
                    max_health=100,
                    move_speed=8.5,
                    jump_strength=17.6,
                    melee_damage=12,
                    melee_range=(70, 70),
                    melee_knockback=(7.0, 8.0),
                    melee_cooldown=0.34,
                    projectile_damage=14,
                    projectile_speed=620.0,
                    projectile_cooldown=0.68,
                    projectile_knockback=(7.0, 7.0),
                    color=(225, 240, 255),
                    accent_color=(112, 189, 255),
                ),
                can_shoot=True,
            ),
        }

        self.p1_name = InputBox(pygame.Rect(150, 210, 300, 54), text="", placeholder="Player 1")
        self.p2_name = InputBox(pygame.Rect(1150, 210, 300, 54), text="", placeholder="Player 2")
        self.back_button = Button(pygame.Rect(60, 58, 180, 56), "Back", BLUE, (90, 150, 255), WHITE)
        self.start_button = Button(pygame.Rect(610, 800, 380, 70), "Start Match", GOLD, (255, 214, 94), BLACK)
        self.p1_selected = "swordsman"
        self.p2_selected = "archer"
        self.selection_rects = self._build_selection_rects()

    def _build_selection_rects(self) -> dict[str, dict[str, pygame.Rect]]:
        return {
            "p1": {
                "swordsman": pygame.Rect(110, 330, 320, 300),
                "archer": pygame.Rect(450, 330, 320, 300),
            },
            "p2": {
                "swordsman": pygame.Rect(830, 330, 320, 300),
                "archer": pygame.Rect(1170, 330, 320, 300),
            },
        }

    def handle_event(self, event: pygame.event.Event) -> SceneResult | None:
        if event.type == pygame.QUIT:
            return SceneResult(quit_game=True)
        self.p1_name.handle_event(event)
        self.p2_name.handle_event(event)
        if self.back_button.clicked(event):
            return SceneResult(next_scene="menu")
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for key, rect in self.selection_rects["p1"].items():
                if rect.collidepoint(event.pos):
                    self.p1_selected = key
            for key, rect in self.selection_rects["p2"].items():
                if rect.collidepoint(event.pos):
                    self.p2_selected = key
        if self.start_button.clicked(event):
            return SceneResult(
                next_scene="game",
                payload={
                    "p1_name": self.p1_name.value(),
                    "p2_name": self.p2_name.value(),
                    "p1_fighter": self.p1_selected,
                    "p2_fighter": self.p2_selected,
                    "fighters": self.fighters,
                },
            )
        return None

    def _draw_mini_fighter(self, screen: pygame.Surface, rect: pygame.Rect, accent: tuple[int, int, int], ranged: bool) -> None:
        cx = rect.x + 62
        cy = rect.y + 100
        glow = pygame.Surface((120, 120), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*accent, 60), (60, 60), 36)
        screen.blit(glow, (cx - 60, cy - 54))
        pygame.draw.circle(screen, WHITE, (cx, cy - 30), 15, 3)
        pygame.draw.line(screen, WHITE, (cx, cy - 14), (cx, cy + 24), 4)
        pygame.draw.line(screen, WHITE, (cx, cy + 24), (cx - 16, cy + 52), 4)
        pygame.draw.line(screen, WHITE, (cx, cy + 24), (cx + 16, cy + 52), 4)
        pygame.draw.line(screen, WHITE, (cx, cy), (cx - 24, cy + 10), 4)
        pygame.draw.line(screen, WHITE, (cx, cy), (cx + 24, cy + 8), 4)
        if ranged:
            pygame.draw.arc(screen, accent, pygame.Rect(cx + 6, cy - 4, 22, 44), 0.9, 5.2, 3)
            pygame.draw.line(screen, accent, (cx + 16, cy + 0), (cx + 16, cy + 36), 2)
            pygame.draw.line(screen, WHITE, (cx + 16, cy + 18), (cx + 42, cy + 18), 2)
        else:
            pygame.draw.line(screen, accent, (cx + 20, cy - 4), (cx + 42, cy - 26), 5)
            pygame.draw.circle(screen, accent, (cx + 44, cy - 28), 5)

    def _draw_wrapped_text(self, screen: pygame.Surface, text: str, font: pygame.font.Font, color: tuple[int, int, int], rect: pygame.Rect, max_lines: int = 3) -> None:
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            test = f"{current} {word}".strip()
            if font.size(test)[0] <= rect.width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        lines = lines[:max_lines]
        y = rect.y
        for line in lines:
            surf = font.render(line, True, color)
            screen.blit(surf, (rect.x, y))
            y += font.get_linesize()


    def _draw_card(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        fighter: FighterDefinition,
        selected: bool,
        player_color: tuple[int, int, int],
    ) -> None:
        shadow = rect.move(0, 8)
        pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=28)
        pygame.draw.rect(screen, DARK_PANEL, rect, border_radius=28)
        pygame.draw.rect(screen, player_color if selected else (92, 106, 130), rect, width=4, border_radius=28)

        self._draw_mini_fighter(screen, rect, fighter.stats.accent_color, fighter.can_shoot)

        content_left = rect.x + 118
        content_width = rect.width - 140

        title = self.name_font.render(fighter.display_name, True, WHITE)
        screen.blit(title, (content_left, rect.y + 18))

        desc_rect = pygame.Rect(content_left, rect.y + 58, content_width, 78)
        self._draw_wrapped_text(screen, fighter.description, self.small_font, SOFT_TEXT, desc_rect)

        stats_top = rect.y + 188
        stat_lines = [
            f"Melee  {fighter.stats.melee_damage}",
            f"Ranged  {'Yes' if fighter.can_shoot else 'No'}",
            f"Speed  {fighter.stats.move_speed:.1f}",
        ]
        for i, line in enumerate(stat_lines):
            screen.blit(self.small_font.render(line, True, WHITE), (rect.x + 22, stats_top + i * 24))

        badge_text = 'Selected' if selected else 'Click to select'
        badge = pygame.Rect(rect.x + 22, rect.bottom - 44, 170, 30)
        pygame.draw.rect(screen, player_color if selected else (52, 63, 84), badge, border_radius=12)

        badge_text_surface = self.small_font.render(badge_text, True, BLACK if selected else WHITE)
        screen.blit(badge_text_surface, badge_text_surface.get_rect(center=badge.center))

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 20, 140))
        screen.blit(overlay, (0, 0))

        gradient = self.game.assets.build_vertical_gradient((WIDTH, HEIGHT), BG_TOP, BG_BOTTOM)
        gradient.set_alpha(64)
        screen.blit(gradient, (0, 0))

        title = self.title_font.render("Player Setup", True, WHITE)
        subtitle = self.text_font.render(
            "Choose names and fighters before starting the match.", True, SOFT_TEXT
        )

        screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 128)))

        mouse_pos = pygame.mouse.get_pos()

        self.back_button.draw(screen, self.button_font, mouse_pos)
        self.start_button.draw(screen, self.button_font, mouse_pos)

        self.p1_name.draw(screen, self.text_font, self.text_font, "Player 1")
        self.p2_name.draw(screen, self.text_font, self.text_font, "Player 2")

        left_label = self.header_font.render("Player 1", True, PLAYER_1_COLOR)
        right_label = self.header_font.render("Player 2", True, PLAYER_2_COLOR)

        screen.blit(left_label, (110, 290))
        screen.blit(right_label, (830, 290))

        for key, rect in self.selection_rects["p1"].items():
            self._draw_card(screen, rect, self.fighters[key], self.p1_selected == key, PLAYER_1_COLOR)

        for key, rect in self.selection_rects["p2"].items():
            self._draw_card(screen, rect, self.fighters[key], self.p2_selected == key, PLAYER_2_COLOR)