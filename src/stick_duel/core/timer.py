from __future__ import annotations


class Cooldown:
    def __init__(self, duration: float) -> None:
        self.duration = duration
        self.remaining = 0.0

    def ready(self) -> bool:
        return self.remaining <= 0.0

    def trigger(self) -> None:
        self.remaining = self.duration

    def update(self, dt: float) -> None:
        self.remaining = max(0.0, self.remaining - dt)
