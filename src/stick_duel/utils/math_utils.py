from __future__ import annotations


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def sign(value: float) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0
