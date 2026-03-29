from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

OwnerT = TypeVar("OwnerT")


class Stateful(Protocol[OwnerT]):
    name: str
    allows_input: bool
    interruptible: bool

    def enter(self, owner: OwnerT) -> None: ...
    def exit(self, owner: OwnerT) -> None: ...
    def update(self, owner: OwnerT, dt: float) -> None: ...


@dataclass
class StateMachine(Generic[OwnerT]):
    owner: OwnerT
    current_state: Stateful[OwnerT]

    def __post_init__(self) -> None:
        self.current_state.enter(self.owner)

    @property
    def state_name(self) -> str:
        return self.current_state.name

    def change_state(self, new_state: Stateful[OwnerT]) -> None:
        if self.current_state.name == new_state.name and type(self.current_state) is type(new_state):
            return
        self.current_state.exit(self.owner)
        self.current_state = new_state
        self.current_state.enter(self.owner)

    def update(self, dt: float) -> None:
        self.current_state.update(self.owner, dt)
