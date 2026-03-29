from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Projectile:
    owner_id: int
    x: float
    y: float
    vx: float
    damage: int
    knockback_x: float
    knockback_y: float
    color: tuple[int, int, int]
    radius: int = 8
    alive: bool = True
    kind: str = "orb"

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)

    def update(self, dt: float, width_limit: int) -> None:
        self.x += self.vx * dt
        if self.x < -100 or self.x > width_limit + 100:
            self.alive = False

    def draw(self, screen: pygame.Surface) -> None:
        center = (int(self.x), int(self.y))
        if self.kind == "arrow":
            direction = 1 if self.vx >= 0 else -1
            tail_len = 24
            pygame.draw.line(screen, self.color, (center[0] - direction * tail_len, center[1]), center, 4)
            pygame.draw.polygon(
                screen,
                self.color,
                [
                    (center[0], center[1]),
                    (center[0] - direction * 12, center[1] - 6),
                    (center[0] - direction * 12, center[1] + 6),
                ],
            )
            glow = pygame.Surface((52, 24), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (*self.color, 70), glow.get_rect())
            screen.blit(glow, (center[0] - glow.get_width() // 2, center[1] - glow.get_height() // 2))
            return

        glow = pygame.Surface((self.radius * 8, self.radius * 8), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*self.color, 55), (glow.get_width() // 2, glow.get_height() // 2), self.radius * 2)
        screen.blit(glow, (center[0] - glow.get_width() // 2, center[1] - glow.get_height() // 2))
        tail_length = max(16, int(abs(self.vx) * 0.03))
        direction = -1 if self.vx > 0 else 1
        pygame.draw.line(screen, self.color, center, (center[0] + direction * tail_length, center[1]), 4)
        pygame.draw.circle(screen, self.color, center, self.radius)
        pygame.draw.circle(screen, (255, 255, 255), center, max(2, self.radius // 3))
