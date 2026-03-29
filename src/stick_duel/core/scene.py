from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SceneResult:
    next_scene: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    quit_game: bool = False


class Scene:
    def __init__(self, game: Any) -> None:
        self.game = game

    def enter(self, payload: dict[str, Any] | None = None) -> None:
        _ = payload

    def handle_event(self, event: Any) -> SceneResult | None:
        _ = event
        return None

    def update(self, dt: float) -> SceneResult | None:
        _ = dt
        return None

    def draw(self, screen: Any) -> None:
        _ = screen
