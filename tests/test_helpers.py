from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from stick_duel.entities.fighter import Fighter, FighterDefinition
from stick_duel.entities.stats import FighterStats


def ensure_pygame_ready() -> None:
    if not pygame.get_init():
        pygame.init()
    if not pygame.font.get_init():
        pygame.font.init()
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((1, 1))


ensure_pygame_ready()


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
    ensure_pygame_ready()
    return Fighter(
        player_id,
        name,
        make_definition(can_shoot=can_shoot),
        spawn,
        {"left": pygame.K_a, "right": pygame.K_d},
    )


class DummySound:
    def play(self, *args, **kwargs) -> None:
        return None


class DummyAssets:
    def optional_image(self, path: str, **kwargs) -> pygame.Surface:
        ensure_pygame_ready()
        size = kwargs.get("size", (64, 64))
        alpha = kwargs.get("alpha", True)
        fill_color = kwargs.get("fill_color")
        width, height = size
        flags = pygame.SRCALPHA if alpha else 0
        surface = pygame.Surface((width, height), flags)
        if fill_color is not None:
            surface.fill(fill_color)
        else:
            surface.fill((30, 30, 30, 255) if alpha else (30, 30, 30))
        return surface

    def image(
        self,
        path: str,
        *,
        size: tuple[int, int] | None = None,
        alpha: bool = True,
    ) -> pygame.Surface:
        return self.optional_image(path, size=size, alpha=alpha)

    def sound(self, path: str) -> DummySound:
        return DummySound()

    def font(self, size: int, bold: bool = False) -> pygame.font.Font:
        ensure_pygame_ready()
        font = pygame.font.Font(None, size)
        font.set_bold(bold)
        return font


class DummyGame:
    def __init__(self) -> None:
        ensure_pygame_ready()
        self.assets = DummyAssets()