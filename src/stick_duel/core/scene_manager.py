from __future__ import annotations

from typing import Any

from stick_duel.core.scene import Scene


class SceneManager:
    def __init__(self, game: Any) -> None:
        self.game = game
        self._registry: dict[str, type[Scene]] = {}
        self.current: Scene | None = None
        self.current_name: str | None = None

    def register(self, name: str, scene_class: type[Scene]) -> None:
        self._registry[name] = scene_class

    def go_to(self, name: str, payload: dict[str, Any] | None = None) -> None:
        try:
            scene_class = self._registry[name]
            self.current = scene_class(self.game)
            self.current_name = name
            self.current.enter(payload or {})
        except Exception as e:
            print("SCENE ERROR:", name)
            print(repr(e))
            raise
