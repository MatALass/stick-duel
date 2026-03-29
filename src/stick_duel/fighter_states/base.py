from __future__ import annotations

from abc import ABC, abstractmethod


class FighterState(ABC):
    name = "base"
    allows_input = True
    interruptible = True

    def enter(self, fighter) -> None:
        pass

    def exit(self, fighter) -> None:
        pass

    @abstractmethod
    def update(self, fighter, dt: float) -> None:
        raise NotImplementedError
