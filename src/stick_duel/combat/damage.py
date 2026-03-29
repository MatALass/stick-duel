from __future__ import annotations


def apply_damage(current_health: int, damage: int) -> int:
    return max(0, current_health - damage)
