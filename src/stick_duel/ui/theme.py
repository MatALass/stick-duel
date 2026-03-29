from __future__ import annotations

from dataclasses import dataclass

from stick_duel.constants import BLACK, BLUE, DARK_PANEL, GOLD, LIGHT_BG, MID_PANEL, RED, WHITE


@dataclass(frozen=True)
class Theme:
    background: tuple[int, int, int] = LIGHT_BG
    panel: tuple[int, int, int] = DARK_PANEL
    panel_alt: tuple[int, int, int] = MID_PANEL
    text: tuple[int, int, int] = WHITE
    text_dark: tuple[int, int, int] = BLACK
    primary: tuple[int, int, int] = BLUE
    secondary: tuple[int, int, int] = RED
    accent: tuple[int, int, int] = GOLD
