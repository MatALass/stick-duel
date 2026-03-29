from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FighterInput:
    left: bool = False
    right: bool = False
    jump_pressed: bool = False
    fast_fall_pressed: bool = False
    melee_pressed: bool = False
    ranged_pressed: bool = False

    def consume_jump(self) -> bool:
        value = self.jump_pressed
        self.jump_pressed = False
        return value

    def consume_fast_fall(self) -> bool:
        value = self.fast_fall_pressed
        self.fast_fall_pressed = False
        return value

    def consume_melee(self) -> bool:
        value = self.melee_pressed
        self.melee_pressed = False
        return value

    def consume_ranged(self) -> bool:
        value = self.ranged_pressed
        self.ranged_pressed = False
        return value
