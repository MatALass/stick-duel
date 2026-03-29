from __future__ import annotations

from stick_duel.fighter_states.base import FighterState


class RespawnState(FighterState):
    name = "respawn"
    allows_input = False
    interruptible = False

    def __init__(self, duration: float = 0.5) -> None:
        self.duration = duration
        self.remaining = duration

    def enter(self, fighter) -> None:
        self.remaining = self.duration
        fighter.flash_timer = max(fighter.flash_timer, self.duration)
        fighter.set_attack_phase("idle")

    def update(self, fighter, dt: float) -> None:
        self.remaining -= dt
        if self.remaining <= 0:
            fighter.state_machine.change_state(fighter.state_factory.idle())
