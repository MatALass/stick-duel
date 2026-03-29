import pygame

from stick_duel.combat.collision import intersects


def test_intersects_detects_overlap() -> None:
    assert intersects(pygame.Rect(0, 0, 50, 50), pygame.Rect(25, 25, 50, 50))


def test_intersects_detects_no_overlap() -> None:
    assert not intersects(pygame.Rect(0, 0, 20, 20), pygame.Rect(100, 100, 20, 20))
