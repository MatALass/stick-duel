
from __future__ import annotations

import pygame

from stick_duel.constants import GREEN, HUD_BG, HUD_EDGE, RED, SOFT_TEXT, WHITE

DOT_SPACING = 18
DOT_RADIUS = 6


def _health_color(ratio: float) -> tuple[int, int, int]:
    if ratio > 0.65:
        return GREEN
    if ratio > 0.35:
        return (244, 190, 55)
    return RED



def draw_health_bar(screen: pygame.Surface, rect: pygame.Rect, current: int, maximum: int) -> None:
    pygame.draw.rect(screen, (24, 32, 44), rect, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), rect, width=2, border_radius=12)
    ratio = 0.0 if maximum <= 0 else max(0.0, min(1.0, current / maximum))
    fill_width = max(0, int((rect.width - 4) * ratio))
    if fill_width > 0:
        filled = pygame.Rect(rect.x + 2, rect.y + 2, fill_width, rect.height - 4)
        pygame.draw.rect(screen, _health_color(ratio), filled, border_radius=10)



def _draw_lives_block(
    screen: pygame.Surface,
    font: pygame.font.Font,
    panel: pygame.Rect,
    lives: int,
    color: tuple[int, int, int],
    align: str,
) -> None:
    label = font.render('Lives', True, SOFT_TEXT)
    count = max(0, lives)
    dots_width = max(0, count * DOT_SPACING - (DOT_SPACING - DOT_RADIUS * 2))
    block_width = label.get_width() + 10 + dots_width
    block_y = panel.y + 14

    if align == 'right':
        start_x = panel.right - 18 - block_width
    else:
        start_x = panel.x + 18

    screen.blit(label, (start_x, block_y))
    dot_center_y = block_y + label.get_height() // 2 + 1
    dot_start_x = start_x + label.get_width() + 14
    for index in range(count):
        cx = dot_start_x + index * DOT_SPACING
        pygame.draw.circle(screen, color, (cx, dot_center_y), DOT_RADIUS)
        pygame.draw.circle(screen, WHITE, (cx, dot_center_y), DOT_RADIUS, 2)



def draw_hud(screen: pygame.Surface, assets, fighter_left, fighter_right) -> None:
    title_font = assets.font(22, bold=True)
    small_font = assets.font(18)
    micro_font = assets.font(16)

    left_panel = pygame.Rect(32, 28, 400, 118)
    right_panel = pygame.Rect(1168, 28, 400, 118)
    for panel in (left_panel, right_panel):
        shadow = panel.move(0, 4)
        pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=22)
        pygame.draw.rect(screen, HUD_BG, panel, border_radius=22)
        pygame.draw.rect(screen, HUD_EDGE, panel, width=3, border_radius=22)

    screen.blit(title_font.render(fighter_left.name, True, WHITE), (left_panel.x + 18, left_panel.y + 12))
    screen.blit(small_font.render(fighter_left.definition.display_name, True, SOFT_TEXT), (left_panel.x + 18, left_panel.y + 42))
    draw_health_bar(screen, pygame.Rect(left_panel.x + 18, left_panel.y + 72, left_panel.width - 36, 18), fighter_left.health, fighter_left.definition.stats.max_health)
    hp_text = small_font.render(f"HP {fighter_left.health}/{fighter_left.definition.stats.max_health}", True, WHITE)
    screen.blit(hp_text, (left_panel.x + 18, left_panel.y + 95))
    _draw_lives_block(screen, micro_font, left_panel, fighter_left.stocks + 1, fighter_left.definition.stats.accent_color, align='right')

    name_surface = title_font.render(fighter_right.name, True, WHITE)
    role_surface = small_font.render(fighter_right.definition.display_name, True, SOFT_TEXT)
    screen.blit(name_surface, (right_panel.right - name_surface.get_width() - 18, right_panel.y + 12))
    screen.blit(role_surface, (right_panel.right - role_surface.get_width() - 18, right_panel.y + 42))
    draw_health_bar(screen, pygame.Rect(right_panel.x + 18, right_panel.y + 72, right_panel.width - 36, 18), fighter_right.health, fighter_right.definition.stats.max_health)
    hp_surface = small_font.render(f"HP {fighter_right.health}/{fighter_right.definition.stats.max_health}", True, WHITE)
    screen.blit(hp_surface, (right_panel.x + 18, right_panel.y + 95))
    _draw_lives_block(screen, micro_font, right_panel, fighter_right.stocks + 1, fighter_right.definition.stats.accent_color, align='left')

    info = assets.font(16).render('Esc • Pause', True, SOFT_TEXT)
    screen.blit(info, info.get_rect(center=(800, 38)))
