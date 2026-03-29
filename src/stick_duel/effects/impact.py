
from __future__ import annotations

import random
from dataclasses import dataclass

import pygame


class ScreenShake:
    def __init__(self) -> None:
        self.timer = 0.0
        self.intensity = 0

    def trigger(self, intensity: int = 6, duration: float = 0.12) -> None:
        self.intensity = max(self.intensity, intensity)
        self.timer = max(self.timer, duration)

    def update(self, dt: float) -> None:
        self.timer = max(0.0, self.timer - dt)
        if self.timer == 0.0:
            self.intensity = 0

    def get_offset(self) -> tuple[int, int]:
        if self.timer <= 0 or self.intensity <= 0:
            return (0, 0)
        return (
            random.randint(-self.intensity, self.intensity),
            random.randint(-self.intensity, self.intensity),
        )


class HitFreeze:
    def __init__(self) -> None:
        self.timer = 0.0

    def trigger(self, duration: float = 0.05) -> None:
        self.timer = max(self.timer, duration)

    def update(self, dt: float) -> None:
        self.timer = max(0.0, self.timer - dt)

    @property
    def active(self) -> bool:
        return self.timer > 0.0


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    radius: int
    life: float
    color: tuple[int, int, int]


class ImpactParticles:
    def __init__(self) -> None:
        self.particles: list[Particle] = []

    def spawn(self, x: float, y: float, color: tuple[int, int, int], count: int = 10) -> None:
        for _ in range(count):
            speed_x = random.uniform(-160.0, 160.0)
            speed_y = random.uniform(-180.0, 60.0)
            self.particles.append(
                Particle(
                    x=x,
                    y=y,
                    vx=speed_x,
                    vy=speed_y,
                    radius=random.randint(2, 4),
                    life=random.uniform(0.12, 0.28),
                    color=color,
                )
            )

    def update(self, dt: float) -> None:
        alive: list[Particle] = []
        for particle in self.particles:
            particle.x += particle.vx * dt
            particle.y += particle.vy * dt
            particle.vy += 360.0 * dt
            particle.life -= dt
            if particle.life > 0.0:
                alive.append(particle)
        self.particles = alive

    def draw(self, screen: pygame.Surface, offset: tuple[int, int] = (0, 0)) -> None:
        ox, oy = offset
        for particle in self.particles:
            alpha = max(30, int(255 * min(1.0, particle.life / 0.28)))
            surf = pygame.Surface((particle.radius * 4, particle.radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(
                surf,
                (*particle.color, alpha),
                (surf.get_width() // 2, surf.get_height() // 2),
                particle.radius,
            )
            screen.blit(surf, (particle.x + ox - surf.get_width() // 2, particle.y + oy - surf.get_height() // 2))
