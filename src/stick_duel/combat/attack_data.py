from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AttackData:
    name: str
    startup: float
    active: float
    recovery: float
    damage: int
    knockback_x: float
    knockback_y: float
    hitbox_width: int
    hitbox_height: int
    hitbox_offset_x: int
    hitbox_offset_y: int
