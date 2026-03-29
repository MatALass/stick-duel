from __future__ import annotations

from stick_duel.fighter_states.base import FighterState


class DeadState(FighterState):
    name = "dead"
    allows_input = False
    interruptible = False

    def enter(self, fighter) -> None:
        fighter.set_attack_phase("idle")
        fighter.body.velocity_x = 0.0
        fighter.body.velocity_y = 0.0

    def update(self, fighter, dt: float) -> None:
        fighter.body.velocity_x = 0.0
        fighter.body.velocity_y = 0.0
