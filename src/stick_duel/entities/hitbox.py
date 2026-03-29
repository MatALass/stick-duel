from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Hitbox:
    rect: pygame.Rect
    damage: int
    knockback_x: float
    knockback_y: float
    owner_id: int
