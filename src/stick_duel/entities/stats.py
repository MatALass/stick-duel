from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FighterStats:
    max_health: int
    move_speed: float
    jump_strength: float
    melee_damage: int
    melee_range: tuple[int, int]
    melee_knockback: tuple[float, float]
    melee_cooldown: float
    projectile_damage: int
    projectile_speed: float
    projectile_cooldown: float
    projectile_knockback: tuple[float, float]
    color: tuple[int, int, int]
    accent_color: tuple[int, int, int]
