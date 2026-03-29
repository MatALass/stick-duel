from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from stick_duel.asset_loader import AssetLoader
from stick_duel.entities.fighter import Fighter, FighterDefinition
from stick_duel.entities.stats import FighterStats


def make_definition(*, can_shoot: bool = True) -> FighterDefinition:
    return FighterDefinition(
        key="test",
        display_name="Test Fighter",
        description="Test fighter for automated tests",
        stats=FighterStats(
            max_health=100,
            move_speed=8.0,
            jump_strength=15.0,
            melee_damage=10,
            melee_range=(80, 60),
            melee_knockback=(8.0, 9.0),
            melee_cooldown=0.5,
            projectile_damage=12,
            projectile_speed=450.0,
            projectile_cooldown=0.8,
            projectile_knockback=(6.0, 7.0),
            color=(255, 255, 255),
            accent_color=(255, 0, 0),
        ),
        can_shoot=can_shoot,
    )


def make_fighter(
    player_id: int = 1,
    *,
    name: str = "P1",
    can_shoot: bool = True,
    spawn: tuple[int, int] = (250, 300),
) -> Fighter:
    return Fighter(
        player_id,
        name,
        make_definition(can_shoot=can_shoot),
        spawn,
        {"left": pygame.K_a, "right": pygame.K_d},
    )


class DummyGame:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.assets = AssetLoader()
