from __future__ import annotations

from dataclasses import dataclass

from stick_duel.constants import FRICTION, GRAVITY, HEIGHT, MAX_HORIZONTAL_SPEED, WIDTH
from stick_duel.utils.math_utils import clamp


@dataclass
class PhysicsBody:
    x: float
    y: float
    width: int
    height: int
    velocity_x: float = 0.0
    velocity_y: float = 0.0

    def apply_gravity(self) -> None:
        self.velocity_y += GRAVITY

    def apply_friction(self) -> None:
        self.velocity_x *= FRICTION
        if abs(self.velocity_x) < 0.15:
            self.velocity_x = 0.0

    def clamp_velocity(self) -> None:
        self.velocity_x = clamp(self.velocity_x, -MAX_HORIZONTAL_SPEED, MAX_HORIZONTAL_SPEED)

    def step(self) -> None:
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.x < 0:
            self.x = 0
            self.velocity_x = 0
        if self.x + self.width > WIDTH:
            self.x = WIDTH - self.width
            self.velocity_x = 0
        if self.y < 0:
            self.y = 0
            self.velocity_y = 0
        if self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height
            self.velocity_y = 0
