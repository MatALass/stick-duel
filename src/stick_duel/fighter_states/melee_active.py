from __future__ import annotations

from stick_duel.fighter_states.base import FighterState


class MeleeActiveState(FighterState):
    name = "melee_active"
    interruptible = False

    def __init__(self, duration: float) -> None:
        self.duration = duration
        self.remaining = duration

    def enter(self, fighter) -> None:
        fighter.set_attack_phase("melee")
        fighter.melee_contact_consumed = False
        self.remaining = self.duration

    def update(self, fighter, dt: float) -> None:
        fighter.apply_horizontal_input(acceleration=0.10)
        self.remaining -= dt
        if self.remaining <= 0:
            fighter.state_machine.change_state(fighter.state_factory.melee_recovery())
