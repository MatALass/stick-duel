from __future__ import annotations

import pygame


def intersects(rect_a: pygame.Rect, rect_b: pygame.Rect) -> bool:
    return rect_a.colliderect(rect_b)
